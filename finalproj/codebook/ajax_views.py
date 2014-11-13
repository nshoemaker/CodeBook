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
        """
        TODO: put in code to star a repo (something like this:)

	    g = get_auth_user_git(request)
	    repo = g.get_repo(int(id))
	    user = g.get_user()
		user.add_to_starred(repo)

        """
        pass
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def unstar_repo(request, id):
    if request.is_ajax():
        """
        TODO: put in code to star a repo (something like this:)

	    g = get_auth_user_git(request)
	    repo = g.get_repo(int(id))
	    user = g.get_user()
		user.remove_from_starred(repo)

        """
        pass
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def watch_repo(request, id):
    if request.is_ajax():
        """
        TODO: put in code to star a repo (whatever alternative we come up with. Formerly:)

	    g = get_auth_user_git(request)
	    repo = g.get_repo(int(id))
	    user = g.get_user()
		user.add_to_subscriptions(repo)

        """
        pass
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def unwatch_repo(request, id):
    if request.is_ajax():
        """
        TODO: put in code to star a repo (whatever alternative we come up with. Formerly:)

	    g = get_auth_user_git(request)
	    repo = g.get_repo(int(id))
	    user = g.get_user()
		user.remove_to_subscriptions(repo)

        """
        pass
    else:
        # uhhhhhhhh awk. this should never happen
        pass
