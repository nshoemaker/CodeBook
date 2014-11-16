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

def my_profile_view(request):
    context = {}
    context["profile_user"] = request.user
    context["view_my_profile"] = 'true'
    return render(request, 'codebook/view_my_profile.html', context)

def profile_view(request, username):
    context = {}
    # TODO change this to the username of the user
    profile_user = get_object_or_404(ProfileUser, username=username)
    context["profile_user"] = profile_user

    if (profile_user == request.user):
        context["view_my_profile"] = 'true'
    return render(request, 'codebook/profile.html', context)

def get_auth_user_git(request):
    social = request.user.social_auth.get(provider='github')
    token = social.extra_data['access_token']
    g = Github(token)
    return g

def saved(request):
    context = {}

    # Dummy test = "authenticated user" is ProfUser 1 
    profile_user = request.user
    user_saves = Saved.objects.get(profile_user=profile_user)

    context['files'] = user_saves.files.all
    context["source"] = 'saved'
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user
    return render(request, 'codebook/saved-files.html', context)

def front(request):
    context = {}
    if request.user and not request.user.is_anonymous:
        try:
            ProfileUser.objects.get(user=request.user)
        except:
          new_profile_user = request.user
          new_profile_user.save()
          new_saves = Saved(profile_user=new_profile_user)
          new_saves.save()
        context['user'] = new_profile_user
        social = request.user.social_auth.get(provider='github')
        token = social.extra_data['access_token']
        context['searchform'] = SearchForm()
        #g = Github(token)
    return render(request, 'codebook/front-page.html', context)

#@login_required
def news(request):
    context = {}
    # TODO: this is just temporary. Replace with actual list of languages the user likes.
    lang_list = ['java', 'python', 'csharp', 'cpp', 'c']
    context['lang_list'] = lang_list

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

    i = 0
    for repo in watched:
        if (i < 10):
            new_repo = Repository(repo_id = repo.id)
            new_repo.save()
            recent_watched.append(new_repo)
            i = i+1
        else:
            break

    """
    context = {}
    context['repos'] = request.user.get_watched()
    context["source"] = 'codebook/watching'
    context['comment_form'] = CommentForm()
    context['profile_user'] = request.user
    return render(request, 'codebook/watching-page.html', context)
    """
    context["source"] = 'watching'
    context['repos'] = recent_watched
    context['comment_form'] = CommentForm()
    context['profile_user'] = request.user
    return render(request, 'codebook/watching-page.html', context)


#@login_required
def following(request):
    context = {}
    # TODO: this is just temporary. Replace with actual list of user ids of people the user is following (max 10)
    following_list_short = ['1','2','3','4','5','6','7','8','9','10','11','12']
    context['following_list_short'] = following_list_short
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

    context["repos"] = Repository.objects.all
    context['files'] = RepoFile.objects.all
    context['file'] = RepoFile.objects.all()[0]
    context["source"] = 'codebook/search_results'
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user #ProfileUser.objects.get(id=1)
    return render(request, "codebook/sandbox.html", context)
