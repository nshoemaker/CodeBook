##############################################################
##############################################################
##  content_views.py:                                       ##
##                                                          ##
##  Contains actions which populate pages of the web app    ##
##  Actions:                                                ##
##      front           - populates front page              ##
##      news            - populates my languages stream     ##
##      watching        - populates watch stream            ##
##      saved           - populates saved stream            ##
##      following       - populates following-page.html     ##
##      my_profile_view - populates view of own profile     ##
##      profile_view    - populates view of a profile page  ##
##                                                          ##
##############################################################
##############################################################

from views_base import *
g = Github('dmouli', 'Spongebob5%')
"""
g = Github(token)
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

    context['searchform'] = SearchForm()
    context["source"] = 'watching'
    context['repos'] = {}
    context['profile_user'] = request.user
    context['gh_user'] = user
    return render(request, 'codebook/watching-page.html', context)


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
