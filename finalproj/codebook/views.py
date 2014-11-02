from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction

from django.core.exceptions import ObjectDoesNotExist

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

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

from django.db.models import Q

#from codebook.models import *
#from codebook.forms import *

from datetime import datetime
from django.utils import timezone

import json

def front(request):
    context = {}

    return render(request, 'codebook/front-page.html', context)

#@login_required
def news(request):
    context = {}
    # TODO: this is just temporary. Replace with actual list of languages the user likes.
    lang_list = ['java', 'python', 'csharp', 'cpp', 'c']
    context['lang_list'] = lang_list
    return render(request, 'codebook/news-page.html', context)

#@login_required
def watching(request):
    context = {}
    return render(request, 'codebook/watching-page.html', context)

#@login_required
def starred(request):
    context = {}
    return render(request, 'codebook/starred-page.html', context)

#@login_required
def following(request):
    context = {}
    # TODO: this is just temporary. Replace with actual list of user ids of people the user is following (max 10)
    following_list_short = ['1','2','3','4','5','6','7','8','9','10','11','12']
    context['following_list_short'] = following_list_short
    return render(request, 'codebook/following-page.html', context)

