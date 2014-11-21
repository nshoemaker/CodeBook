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


@transaction.atomic
def post_repo_comment(request, id):
    if request.is_ajax():
        try:
            comment_form = CommentForm(request.POST)
        except:
            print 'ERROR 1'
            return HttpResponse('Error')
        repo = get_object_or_404(Repository, repo_id=id)
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
        for repo in g.get_user('charliesome').get_repos():
            langs = repo.get_languages()
            for lang in langs.keys():
                try:
                    language = Language.objects.get(name=lang)
                except:
                    language = Language(name=lang,icon='icon-prog-python')
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
        try:
            lang = Language.objects.get(name=language_name, icon='icon-prog-python')
        except:
            print 0
            lang = Language(name=language_name, icon='icon-prog-python')
            lang.save()
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