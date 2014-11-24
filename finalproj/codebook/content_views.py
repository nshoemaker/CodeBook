############################################################
############################################################
##  content_views.py:                                     ##
##                                                        ##
##  Contains actions which populate pages of the web app  ##
##  Actions:                                              ##
##      front     - populates front-page.html             ##
##      news      - populates news-page.html              ##
##      watching  - populates watching-page.html          ##
##      starred   - populates starred-page.html           ##
##      following - populates following-page.html         ##
############################################################
############################################################

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction

from django.core.exceptions import ObjectDoesNotExist

from github import Github 
# g = Github(user, password) - USE THIS ONE TO TEST B/C IT WON'T HIT RATE LIMIT
g = Github('dmouli', 'Spongebob5%')
"""
g = Github(token)
"""

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from django.template.context import RequestContext

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

from django.db.models import Q

from codebook.models import *
from codebook.forms import *

from datetime import datetime
from django.utils import timezone

import json

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
        self.file_tree = None
        try:
            branches = repo.get_branches()
            SHA = branches[0].commit.sha
            tree = repo.get_git_tree(SHA,False).tree
            self.file_tree = tree
            for i in xrange(len(tree)):
                deffile = repo.get_contents(tree[i].path)
                if deffile.type == 'file':
                    self.default_file_name = deffile.name
                    self.default_file_contents = base64.b64decode(deffile.content)
                    self.default_file_path = deffile.path
                    break
            self.readme = None
            self.readme_contents = ""
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
        self.is_current_user_watching = user.has_in_subscriptions(repo) 
        self.watch_count = repo.watchers_count
        self.doc_rating = 0
        self.difficulty_rating = 0
        self.tag_list = None
"""      except Exception,e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno) 
            print str(e)
"""

def my_profile_view(request):
    context = {}
    context["profile_user"] = request.user
    context['searchform'] = SearchForm()
    context["view_my_profile"] = 'true'
    context['ratings'] = UserRating.objects.filter(profile_user = request.user)
    return render(request, 'codebook/view_my_profile.html', context)

def profile_view(request, username):
    context = {}
    # TODO change this to the username of the user
    profile_user = get_object_or_404(ProfileUser, username=username)
    context["profile_user"] = profile_user
    context['searchform'] = SearchForm()
    if (profile_user == request.user):
        context["view_my_profile"] = 'true'
    context['ratings'] = UserRating.objects.filter(profile_user = profile_user)
    return render(request, 'codebook/profile.html', context)

def get_auth_user_git(request):
    social = request.user.social_auth.get(provider='github')
    token = social.extra_data['access_token']
    g = Github(token)
    return g

def saved(request):
    context = {}
    files = [] 
    profile_user = request.user
    user_saves = Saved.objects.filter(profile_user=profile_user)

    for save in user_saves:
        files.append(save.repo_file)
    context['searchform'] = SearchForm()
    context['files'] = files
    context["source"] = 'saved'
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user
    return render(request, 'codebook/saved-files.html', context)

def front(request):
    context = {}
    context['searchform'] = SearchForm()
    if request.user and not request.user.is_anonymous:
        context['user'] = request.user
    return render(request, 'codebook/front-page.html', context)

#@login_required
def news(request):
    context = {}
    # TODO: this is just temporary. Replace with actual list of languages the user likes.
    lang_list = ['java', 'python', 'csharp', 'cpp', 'c']
    context['lang_list'] = lang_list
    context['searchform'] = SearchForm()
    #profile_user = ProfileUser.objects.get(user=request.user)
    #user_langs = profile_user.languages.all
    #context['profile_user'] = profile_user
    #context['lang_list'] = user_langs
    return render(request, 'codebook/news-page.html', context)

#@login_required
def watching(request):
    context = {}
    g = get_auth_user_git(request)
    user = g.get_user()
    watched = user.get_subscriptions()

    recent_watched = []
    for repo in watched[:10]:
        try:
            repo = Repository.objects.get(repo_id = repo.id)
            x = Repo(None, repo.repo_id, user, g)
        except ObjectDoesNotExist:
            x = Repo(repo, repo.id, user, g)
        recent_watched.append(x)
    context['searchform'] = SearchForm()
    context["source"] = 'watching'
    context['repos'] = recent_watched
    context['comment_form'] = CommentForm()
    context['profile_user'] = request.user
    context['gh_user'] = user
    return render(request, 'codebook/watching-page.html', context)


#@login_required
def following(request):
    context = {}
    # TODO: this is just temporary. Replace with actual list of user ids of people the user is following (max 10)
    following_list_short = ['1','2','3','4','5','6','7','8','9','10','11','12']
    context['following_list_short'] = following_list_short
    context['searchform'] = SearchForm()
    #context['profile_user'] = ProfileUser.objects.get(user=request.user)
    return render(request, 'codebook/following-page.html', context)


def sandbox(request):
    social = request.user.social_auth.get(provider='github')
    token = social.extra_data['access_token']
    context = {}
    """
    g = Github(token)
    repo_obj = Repository(repo_id = 7986587)
    repo_obj.save()
    print repo_obj.get_url()
    repo_gilbert = g.get_repo(7986587)
    file_index = repo_gilbert.get_contents("index.html")
    path = file_index.path
    new_file = RepoFile(repository=repo_obj, path=path, average_difficulty=0, average_quality=0)
    new_file.save()
    """
    profile_user = request.user

    for repo in Repository.objects.all():
        print "_____________________________"
        print str(repo.repo_id)
        print str(repo.get_url)
        print str(repo.get_name)

    for file in RepoFile.objects.all():
        print "++++++++++++++++++++++++++++++++++++++"
        print file.get_name
        print file.get_content
    context['searchform'] = SearchForm()
    context["repos"] = {}
    context['files'] = RepoFile.objects.all
    #context['file'] = RepoFile.objects.all()[0]
    context["source"] = 'codebook/search_results'
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user #ProfileUser.objects.get(id=1)
    return render(request, "codebook/sandbox.html", context)
