__author__ = 'nora'
from content_views import *
from user_action_views import *
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction

from django.core.exceptions import ObjectDoesNotExist

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response


# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

from django.db.models import Q

from codebook.models import *
from codebook.forms import *

from datetime import datetime
from django.utils import timezone

import json

"""
To use this class: 
Initialize as Repo(None,Repository.repo_id,user) if want to create from database model repository. 
Initialize as Repo(githubrepo,0,user) if want to create from github repo.
User is github user, get by g.get_user() of authenticated g user.
"""
class Repo:
    def __init__(self, repo, id, user, hub):
        if(repo is None):
            repo = hub.get_repo(id)
            self.comments = Comment.objects.filter(repository__repo_id = repo.id)
        else:
            self.comments = Comment.objects.none()
        branches = repo.get_branches()
        SHA = branches[0].commit.sha
        tree = repo.get_git_tree(SHA).tree
        self.default_file_name = ""
        self.default_file_contents = ""
        self.default_file_path = ""
        try:
            for i in xrange(len(tree)):
                deffile = repo.get_contents(tree[i].path)
                if deffile.type == 'file':
                    self.default_file_name = deffile.name
                    self.default_file_contents = base64.b64decode(deffile.content)
                    self.default_file_path = deffile.path
                    break
            #check first thing blob type
        except:
            pass
        self.id = repo.id
        self.name = repo.name
        self.description = repo.description
        self.url = repo.html_url
        self.langs = repo.language
        self.org = repo.organization
        self.owner_name = repo.owner.login
        self.owner_prof_pic = repo.owner.avatar_url
        self.is_current_user_starring = user.has_in_starred(repo) 
        self.star_count = repo.stargazers_count
        self.is_current_user_watching = user.has_in_watched(repo) 
        self.watch_count = repo.watchers_count
        self.file_tree = tree
        self.readme = repo.get_readme()
        self.readme_contents = base64.b64decode(self.readme.content)
        self.doc_rating = 0
        self.difficulty_rating = 0
        self.tag_list = None

def get_formatted_nodes(self, tree, repo):
    print tree
    print " "
    print tree.path
    print tree.mode
    print tree.url
    print tree.type
    res = {}
    for el in tree:
        title = repo.get_file_contents(el.path).name
        hideCheckbox = 'true'
        if el.type == 'tree':
            isFolder = 'true'
            isLazy = 'true'
        else:
            isFolder = 'false'
            isLazy = 'false'
        key = str(repo.id) + '---' + el.sha
        node = {"title": title,
                "key": key,
                "isFolder": isFolder,
                "isLazy": isLazy,
                "hideCheckox": hideCheckbox}
        res.append(node)
    return json.dumps(res, encoding="Latin-1")

@login_required
def expand_folder(request):
    if request.is_ajax():
        social = request.user.social_auth.get(provider='github')
        token = social.extra_data['access_token']
        hub = Github(token)
        profile_user = request.user
        if request.GET:
            rep_id = request.GET.get("repo_id")
            sha = request.GET.get("sha")
        elif request.POST:
            rep_id = request.POST.get("repo_id")
            sha = request.POST.get("sha")
        rep = hub.get_repo(int(rep_id))
        next_level = rep.get_git_tree(sha).tree
        #j = get_formatted_nodes(next_level, rep)
        res = []
        print "NEXT LEVEL SIZE: "+ str(len(next_level))
        for el in next_level:
            title = el.path
            hideCheckbox = True
            if el.type == 'tree':
                print "FOLDER: " + el.path
                isFolder = True
                isLazy = True
            else:
                isFolder = False
                isLazy = False
            key = str(rep.id) + '---' + el.sha
            node = {"title": title,
                    "key": key,
                    "isFolder": isFolder,
                    "isLazy": isLazy,
                    "hideCheckox": hideCheckbox}
            res.append(node)
        j = json.dumps(res, encoding="Latin-1")
        print rep_id
        return HttpResponse(j, content_type="application/json")
    else:
        pass

def get_top_level(request):
    if request.is_ajax():
        social = request.user.social_auth.get(provider='github')
        token = social.extra_data['access_token']
        hub = Github(token)
        if request.GET:
            rep_id = request.GET.get("repo_id")
        elif request.POST:
            rep_id = request.POST.get("repo_id")
        print rep_id
        try:
            rep = hub.get_repo(int(rep_id))
        except:
            print 'bad'
            rep = g.get_repo(int(rep_id))
        # TODO: what if there is no mater branch????
        try:
            master = rep.get_branch('master')
        except:
            master = rep.get_branches()[0]
        SHA = master.commit.sha
        next_level = rep.get_git_tree(SHA).tree
        #j = get_formatted_nodes(next_level, rep)
        res = []
        print "NEXT LEVEL SIZE: "+ str(len(next_level))
        for el in next_level:
            title = el.path
            hideCheckbox = True
            if el.type == 'tree':
                print "FOLDER: " + el.path
                isFolder = True
                isLazy = True
            else:
                isFolder = False
                isLazy = False
            key = str(rep.id) + '---' + el.sha
            node = {"title": title,
                    "key": key,
                    "isFolder": isFolder,
                    "isLazy": isLazy,
                    "hideCheckox": hideCheckbox}
            res.append(node)
        j = json.dumps(res, encoding="Latin-1")
        print rep_id
        return HttpResponse(j, content_type="application/json")
    else:
        pass


@transaction.atomic
def post_repo_comment(request, id):
    if request.is_ajax():
        try:
            comment_form = CommentForm(request.POST)
        except:
            print 'ERROR 1'
            return HttpResponse('Error')
        repo = Repository.objects.get_or_create(repo_id=id)#get_object_or_404(Repository, repo_id=id)
        profile_user = request.user

        if not comment_form.is_valid():
            context = {}
            context['form' + str(repo.repo_id)] = comment_form
            print 'ERROR 2'
            return HttpResponse('Error')

        com_new = comment_form.save(commit=False)
        com_new.profile_user = profile_user
        comment_form.save()

        repo = Repository.objects.get(repo_id=id)
        repo.comments.add(com_new)
        repo.save()

        
        context = {}
        context['comment'] = com_new

        return render_to_response('codebook/comment.html', context, content_type="html")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


@transaction.atomic
def post_file_comment(request, id):
    if request.is_ajax():
        print "Comes into file comment"
        try:
            comment_form = CommentForm(request.POST)
        except:
            return HttpResponse('Error')
        file = get_object_or_404(RepoFile, id=id)
        profile_user = request.user

        if not comment_form.is_valid():
            context = {}
            context['form' + str(file.id)] = comment_form
            return HttpResponse('Error')

        com_new = comment_form.save(commit=False)
        com_new.profile_user = profile_user
        comment_form.save()

        repoFile = RepoFile.objects.get(id=id)
        repoFile.comments.add(com_new)
        repoFile.save()

        context = {}
        context['comment'] = com_new

        return render_to_response('codebook/comment.html', context, content_type="html")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def star_repo(request, id):
    if request.is_ajax():
        g = get_auth_user_git(request)
        repo = g.get_repo(int(id))
        user = g.get_user()

        if (user.has_in_starred(repo)):
            pass;
        else:
            user.add_to_starred(repo)
        
        Repository.objects.get_or_create(repo_id=id)
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def unstar_repo(request, id):
    if request.is_ajax():
        g = get_auth_user_git(request)
        repo = g.get_repo(int(id))
        user = g.get_user()

        if (user.has_in_starred(repo)):
            user.remove_from_starred(repo)
        else:
            pass; 
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def watch_repo(request, id):
    if request.is_ajax():
        g = get_auth_user_git(request)
        repo = g.get_repo(int(id))
        user = g.get_user()

        if (user.has_in_subscriptions(repo)):
            # User has already watched this repo - click will "un-watch"
            pass
        else:
            user.add_to_subscriptions(repo)
        Repository.objects.get_or_create(repo_id=id)
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def unwatch_repo(request, id):
    context = {}
    if request.is_ajax():
        g = get_auth_user_git(request)
        repo = g.get_repo(int(id))
        user = g.get_user()

        if (user.has_in_subscriptions(repo)):
            user.remove_from_subscriptions(repo)
        else:
            # User has not watched this repo
            pass

        context['gh_user'] = user
        return render_to_response('codebook/repository.html', context, content_type="html")
    else:
        # uhhhhhhhh awk. this should never happen
        pass

def save_file(request, id):
    if request.is_ajax():
        profile_user = request.user
        repofile = RepoFile.objects.get(id=id)
        try:
            # User has already saved this post
            saved_file = Saved.objects.get(profile_user=profile_user, repo_file=repofile)
            pass
        except:
            saved_file = Saved(profile_user=profile_user, repo_file=repofile)
            saved_file.save() 
            repofile.savers.add(profile_user)
            repofile.save() 
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def unsave_file(request, id):
    context = {}
    if request.is_ajax():
        profile_user = request.user
        repofile = RepoFile.objects.get(id=id)
        try:
            # User has already saved this post - click will "un-save"
            saved_file = Saved.objects.get(profile_user=profile_user, repo_file=repofile)
            saved_file.delete() 
        except:
            # User has not saved this post
            pass
        return render_to_response('codebook/file.html', context, content_type="html")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def like_comment(request, id):
    if request.is_ajax():
        context = {}
        comment = Comment.objects.get(id=id)
        profile_user = request.user 

        if (comment.likers.filter(liked_by=profile_user)):
            # User has already liked comment
            pass
        else:
            # User has not liked comment 
            comment.likers.add(profile_user)
            comment.save()
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def unlike_comment(request, id):
    if request.is_ajax():
        context = {}
        comment = Comment.objects.get(id=id)
        profile_user = request.user

        if (comment.likers.filter(liked_by=profile_user)):
            # User has already liked comment
            comment.likers.remove(profile_user)
            comment.save()
        else:
            # User has not liked comment 
            pass
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass

@login_required
def rate_credibility(request):
    if request.is_ajax():
        social = request.user.social_auth.get(provider='github')
        token = social.extra_data['access_token']
        g = Github(token)
 
        #user statistics
        #numFollowers = g.get_user().followers
        #numRepos = g.get_user().public_repos
        for repo in g.get_user().get_repos():
            langs = repo.get_languages()
            for lang in langs.keys():
                try:
                    language = Language.objects.get(name=lang)
                except:
                    language = Language(name=lang)
                    language.save()
                try:
                    rating = UserRating.objects.get(language=language,profile_user=request.user)
                except:
                    rating = UserRating(profile_user=request.user,credibility=0,proficiency=0,language=language)
                    rating.save()
                rating.credibility = min(langs[lang]/1000,100)
                rating.save()
        #for r in UserRating.objects.filter(profile_user=request.user):
        #    print r.language.name, r.credibility
  
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass

@login_required
def add_proficiency(request):
    if request.is_ajax():
        context = {}
        language_name = request.POST.get('language')
        proficiency = request.POST.get('proficiency')
        profile_user = request.user
        print language_name
        print proficiency
        for l in Language.objects.filter(name=language_name):
            print l.name
            print l.id

        lang = Language.objects.get_or_create(name=language_name, icon='icon-prog-python')
        print lang.name
        try:
            rating = UserRating.objects.get(profile_user=profile_user, language=lang)
            rating.update(proficiency=proficiency)
            rating.save()
            print 1
        except:
            print 2
            rating = UserRating.objects.create(profile_user=profile_user, language=lang, proficiency=proficiency, credibility=0)
            rating.save()
        context['rating'] = rating
        """
        for r in UserRating.objects.all():
            print "----------------------"
            print r.profile_user.username
            print r.language.name
            print r.language.id
            print 'cred: ' + str(r.credibility)
            print 'prof: ' + str(r.proficiency)
        """
        return render_to_response('codebook/proficiency.html', context, content_type="html")
        pass
    else:
        # uhhhhhhhh awk. this should never happen
        pass

@login_required()
def sort_lang_stream_recent(request):
    if request.is_ajax():
        context = {}
        context['repos'] = {}
        return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
    else:
        # uhhhhhhhh awk. this should never happen
        pass

def sort_lang_stream_popular(request):
    if request.is_ajax():
        context = {}
        context['repos'] = {}
        return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
    else:
        # uhhhhhhhh awk. this should never happen
        pass

# Given a search type and some text, returns a list of repositories
def repo_search_list(request):
    if request.is_ajax():
        social = request.user.social_auth.get(provider='github')
        token = social.extra_data['access_token']
        g = Github(token)
        profile_user = request.user
        context = {}
        context['repos'] = {}
        choice = request.GET.get("types")
        text = request.GET.get("text")

        if(choice == 'User'):
            repos = []
            files = []
            users = g.search_users(text,sort='followers',order='desc')
            for user in users:
                for repo in user.get_repos().get_page(0):
                   repos.append(repo)

        elif(choice == 'Repo'):
            files = []
            repos = g.search_repositories(text,sort='stars',order='desc').get_page(0)

        elif(choice == 'Code'):
            print "CAME IN HERE"
            repos = []
            query = text+" user:github size:>10000"
            files = g.search_code(query).get_page(0)
                
        else:
            #check that language?
            files = []
            query = "language:"+text+" stars:>=500"
            repos = g.search_repositories(query,sort='stars',order='desc').get_page(0)
        """
        these_file_results = []
        for f in files[:10]:
            file_name = f.name
            print file_name + "\n"
            file_contents = base64.b64decode(f.content)
            print file_contents + "\n"
            file_path = f.path
            print file_path + "\n"
            try:
                repo = Repository.objects.get(repo_id = repo.f.repository.id)
                x = Repo(None,repo.repo_id,g.get_user())
            except ObjectDoesNotExist:
                x = Repo(repo, repo.id, g.get_user())
            repofile(repository = Repo(f.repository,id=f.repository.id,g.get_user()),   
        """
        these_repo_results = []
        for repo in repos[:10]:
            try:
                repo = Repository.objects.get(repo_id = repo.id)
                x = Repo(None,repo.repo_id,g.get_user(), g)
            except ObjectDoesNotExist:
                x = Repo(repo, repo.id, g.get_user(), g)
            print x.name
            these_repo_results.append(x)
        context["repos"] = these_repo_results
        context['comment_form'] = CommentForm()
        """
        for r in these_repo_results:
            print "----------------------"
            print r.name
            for t in r.file_tree:
                rep = g.get_repo(r.id)
                if (t.type == 'tree'):
                    el = rep.get_git_tree(t.sha).tree
                    print " "
                    print t.path
                    print t.mode
                    print t.url
                    print t.type
                    for l in el:
                        print " "
                        print "     " + l.path
                        print "     " + str(l.size)
                        print "     " + l.mode
                        print "     " + l.url
                        print "     " + l.type"""
        return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
    else:
        # uhhhhhhhh awk. this should never happen
        pass
