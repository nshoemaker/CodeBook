############################################################
############################################################
##  user_action_views.py:                                 ##
##                                                        ##
##  Contains actions which perform user actions  		  ##
##  Actions:                                              ##
##      like_comment - Like/dislike a comment             ##
##      watch_repo   - Watch/Unwatch a Repository         ##
##      save_post    - Save/Unsave a Post                 ##
############################################################
############################################################
from views_base import *

def signin(request):
    pass

# new_search is called when a user searches with the textbox and
# search type dropdown list.
# This is an initial funciton that fleshes out the front end
# subsiquently (on document ready) and ajax function is called
# to actually populate the search with a real list of repositories
# (ajax_views.py action repo_search_list)
@login_required
def new_search(request):
    g = get_auth_user_git(request)
    profile_user = request.user
    context = {}

    searchform = SearchForm(request.GET)
    if not searchform.is_valid():
        print searchform.errors
        return None

    text = searchform.cleaned_data['text']
    choice = searchform.cleaned_data['types']

    context['repos'] = {}
    context['files'] = {}
    context["source"] = 'search'
    context['searchform'] = SearchForm()
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user
    context['gh_user'] = g.get_user()
    context['searchtext'] = text
    context['filter'] = choice
    return render(request, "codebook/search-results-page.html", context)

# new_quick_search is called when a user clicks a language button
# This is an initial funciton that fleshes out the front end
# subsiquently (on document ready) and ajax function is called
# to actually populate the search with a real list of repositories
# (ajax_views.py action repo_search_list
@login_required
def new_quick_search(request, language):
    context={}
    if request.user:
        profile_user = request.user
    context["repos"] = {}
    context['files'] = {}
    context["source"] = 'search'
    context['searchform'] = SearchForm()
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user
    context['filter'] = 'Languages'
    context['searchtext'] = language
    return render(request, "codebook/search-results-page.html", context)
