##############################################################
##############################################################
##  views_base.py:                                 		  	##
##                                                        	##
##	Contains imports, classes, and methods needed by all  	##
##		views - imported by ajac_view, user_action_views,	##
##		content_views, and file_tree_views					##
##############################################################
##############################################################


from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
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
from datetime import datetime
# Used to interact with Github API 
from github import Github 

from codebook.models import *
from codebook.forms import *

import json
import sys
import os
import urllib
from django.db.models import Avg

"""
To use this class: 
Initialize as Repo(None,Repository.repo_id,user) if want to create from database model repository. 
Initialize as Repo(githubrepo,0,user) if want to create from github repo.
User is github user, get by g.get_user() of authenticated g user.
"""
class Repo:
    def __init__(self, repo, id, user, hub):
        if(repo is None):
            repo = hub.get_repo(int(id))
            try:
                repository = Repository.objects.get(repo_id__exact=id)
                self.doc_rating = repository.documentation_set.aggregate(Avg('rating')).values()[0]
                self.difficulty_rating = repository.difficulty_set.aggregate(Avg('rating')).values()[0]
            except:
                self.difficulty_rating = 0
                self.doc_rating = 0
            if self.doc_rating == None:
                self.doc_rating = 0
            if self.difficulty_rating == None:
                self.difficulty_rating = 0
            self.comments = Comment.objects.filter(repository__repo_id = repo.id)

        else:
            self.comments = Comment.objects.none()
            self.doc_rating = 0
            self.difficulty_rating = 0

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
        self.tag_list = None
"""      except Exception,e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno) 
            print str(e)
"""

def get_auth_user_git(request):
    social = request.user.social_auth.get(provider='github')
    token = social.extra_data['access_token']
    g = Github(token)
    return g
