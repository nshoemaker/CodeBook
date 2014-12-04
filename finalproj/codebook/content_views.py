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

@login_required
def my_profile_view(request):
    context = {}
    context["profile_user"] = request.user
    context['searchform'] = SearchForm()
    context["view_my_profile"] = 'true'
    context['ratings'] = UserRating.objects.filter(profile_user = request.user)
    return render(request, 'codebook/view_my_profile.html', context)

@login_required
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

@login_required
def saved(request):
    context = {}
    files = [] 
    profile_user = request.user
    user_saves = Saved.objects.filter(profile_user=profile_user)
    g = get_auth_user_git(request)

    for save in user_saves:
        save.repo_file.get_name = save.repo_file.get_name(g)
        save.repo_file.get_creator = save.repo_file.get_creator(g)
        save.repo_file.get_content = save.repo_file.get_content(g)
        files.append(save.repo_file)
    context['searchform'] = SearchForm()
    context['files'] = files
    context["source"] = 'saved'
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user
    return render(request, 'codebook/saved-files.html', context)

def login_page(request):
    context = {}
    return render(request, 'codebook/login-page.html', context)


def front(request):
    context = {}
    context['searchform'] = SearchForm()
    if request.user and not request.user.is_anonymous:
        context['user'] = request.user
        social = request.user.social_auth.get(provider='github')
        token = social.extra_data['access_token']
        g = Github(token)
        if g.get_rate_limit().rate.remaining < 250:
            pass
            #return unavailable page
    return render(request, 'codebook/front-page.html', context)

@login_required
def news(request):
    context = {}
    profile_user = request.user
    user_ratings = UserRating.objects.filter(profile_user=profile_user)
    lang_list = []

    for rating in user_ratings:
        lang = rating.language
        print "ORIGINAL LANG = " + lang.name + "___"
        lang_name = ((lang.name).lower()).strip()
        print "CONVERTED LANG = " + lang_name + "___"
        lang_list.append(lang_name)

    # TODO: this is just temporary. Replace with actual list of languages the user likes.
    #lang_list = ['java', 'python', 'csharp', 'cpp', 'c']
    context['lang_list'] = lang_list[:12]
    context['searchform'] = SearchForm()
    return render(request, 'codebook/news-page.html', context)

@login_required
def watching(request):
    context = {}
    g = get_auth_user_git(request)
    user = g.get_user()

    context['searchform'] = SearchForm()
    context["source"] = 'watching'
    context['comment_form'] = CommentForm()
    context['profile_user'] = request.user
    context['gh_user'] = user
    return render(request, 'codebook/watching-page.html', context)


@login_required
def sandbox(request):
    social = request.user.social_auth.get(provider='github')
    token = social.extra_data['access_token']
    context = {}

    #g = Github(token)
    #repo_obj = Repository(repo_id = 23319657)
    #repo_obj.save()
    #print repo_obj.get_url()
    #repo_gilbert = g.get_repo(7986587)
    #file_index = repo_gilbert.get_contents("index.html")
    #path = file_index.path
    #new_file = RepoFile(repository=repo_obj, path=path, average_difficulty=0, average_quality=0)
    #new_file.save()

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

