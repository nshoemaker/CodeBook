##############################################################
##############################################################
##  ajax_views.py:                                          ##
##                                                          ##
##  Contains actions which implement different user actions ##
##      with ajax calls for quick loading                   ##
##############################################################
##############################################################
from views_base import *
import itertools

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
        key = str(repo.id) + '---' + el.sha + '---' + el.path
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
            parent_path = request.GET.get("path")
        elif request.POST:
            rep_id = request.POST.get("repo_id")
            sha = request.POST.get("sha")
            parent_path = request.POST.get("path")
        rep = hub.get_repo(int(rep_id))
        next_level = rep.get_git_tree(sha).tree

        res = []
        for el in next_level:
            title = el.path
            full_path = str(parent_path) + "/" + str(el.path)
            hideCheckbox = True
            if el.type == 'tree':
                isFolder = True
                isLazy = True
            else:
                isFolder = False
                isLazy = False
            key = str(rep.id) + '---' + el.sha + '---' + full_path
            node = {"title": title,
                    "key": key,
                    "isFolder": isFolder,
                    "isLazy": isLazy,
                    "hideCheckox": hideCheckbox}
            res.append(node)
        j = json.dumps(res, encoding="Latin-1")
        return HttpResponse(j, content_type="application/json")
    else:
        pass

@login_required
def get_top_level(request):
    if request.is_ajax():
        social = request.user.social_auth.get(provider='github')
        token = social.extra_data['access_token']
        hub = Github(token)
        if request.GET:
            rep_id = request.GET.get("repo_id")
        elif request.POST:
            rep_id = request.POST.get("repo_id")
        try:
            rep = hub.get_repo(int(rep_id))
        except:
            print 'bad'
            rep = hub.get_repo(int(rep_id))
        # TODO: what if there is no mater branch????
        try:
            master = rep.get_branch('master')
        except:
            master = rep.get_branches()[0]
        SHA = master.commit.sha
        next_level = rep.get_git_tree(SHA).tree
        res = []
        for el in next_level:
            title = el.path
            hideCheckbox = True
            if el.type == 'tree':
                isFolder = True
                isLazy = True
            else:
                isFolder = False
                isLazy = False
            key = str(rep.id) + '---' + el.sha + '---' + el.path
            node = {"title": title,
                    "key": key,
                    "isFolder": isFolder,
                    "isLazy": isLazy,
                    "hideCheckox": hideCheckbox}
            res.append(node)
        j = json.dumps(res, encoding="Latin-1")
        return HttpResponse(j, content_type="application/json")
    else:
        pass

@login_required
@transaction.atomic
def post_repo_comment(request, id):
    if request.is_ajax():
        try:
            comment_form = CommentForm(request.POST)
        except:
            print 'ERROR 1'
            return HttpResponse('Error')
        repo, repo_created = Repository.objects.get_or_create(repo_id=id)
        g = get_auth_user_git(request)
        if repo_created:
            langs = g.get_repo(int(id)).get_languages().keys()
            for l in langs:
                lang, created = Language.objects.get_or_create(name=l)
                repo.languages.add(lang)
                repo.save()
        
        profile_user = request.user

        if not comment_form.is_valid():
            context = {}
            context['form' + str(repo.repo_id)] = comment_form
            print 'ERROR 2'
            return HttpResponse('Error')

        com_new = comment_form.save(commit=False)
        com_new.profile_user = profile_user
        comment_form.save()

        com_new.profile_user.get_avatar_url = com_new.profile_user.get_avatar_url(g)

        repo = Repository.objects.get(repo_id=id)
        repo.comments.add(com_new)
        repo.save()

        
        context = {}
        context['comment'] = com_new

        return render_to_response('codebook/comment.html', context, content_type="html")
    else:
        # uhhhhhhhh awk. this should never happen
        pass

@login_required
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

@login_required
def star_repo(request, id):
    if request.is_ajax():
        g = get_auth_user_git(request)
        repo = g.get_repo(int(id))
        user = g.get_user()

        if (user.has_in_starred(repo)):
            pass;
        else:
            user.add_to_starred(repo)
        
        repo, repo_created = Repository.objects.get_or_create(repo_id=id)
        if repo_created:
            g = get_auth_user_git(request)
            langs = g.get_repo(int(id)).get_languages().keys()
            for l in langs:
                lang,created = Language.objects.get_or_create(name=l)
                repo.languages.add(lang)
                repo.save()
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


@login_required
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


@login_required
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

        repo, repo_created = Repository.objects.get_or_create(repo_id=id)
        if repo_created:
            g = get_auth_user_git(request)
            langs = g.get_repo(int(id)).get_languages().keys()
            for l in langs:
                lang,created = Language.objects.get_or_create(name=l)
                repo.languages.add(lang)
                repo.save()
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


@login_required
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


@transaction.atomic
@login_required
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


@login_required
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

@transaction.atomic
@login_required
def like_comment(request, id):
    if request.is_ajax():
        context = {}
        comment = Comment.objects.get(id=id)
        profile_user = request.user 

        if (profile_user in comment.likers.all()):
            # User has already liked comment\
            pass
        else:
            # 'User has not liked comment... liking'
            comment.likers.add(profile_user)
            comment.save()
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass

@transaction.atomic
@login_required
def unlike_comment(request, id):
    if request.is_ajax():
        context = {}
        comment = Comment.objects.get(id=id)
        profile_user = request.user

        if (profile_user in comment.likers.all()):
            #'User has already liked comment... unliking'
            comment.likers.remove(profile_user)
            comment.save()
        else:
            #'User has not liked comment'
            pass
        return HttpResponse('True', content_type="text")
    else:
        # uhhhhhhhh awk. this should never happen
        pass

@transaction.atomic
@login_required
def rate_credibility(request):
    if request.is_ajax():
        g = get_auth_user_git(request)
        if g.get_rate_limit().rate.remaining < 250:
            return HttpResponse('False', content_type="text")
 
        #user statistics
        #numFollowers = g.get_user().followers
        #numRepos = g.get_user().public_repos
        for repo in g.get_user().get_repos():
            langs = repo.get_languages()
            for lang in langs.keys():
                try:
                    for l in (Language.objects.filter(name__iexact=lang)):
                        lang_name = l.name
                    language = Language.objects.get(name=lang_name)
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

@transaction.atomic
@login_required
def add_proficiency(request):
    if request.is_ajax():
        context = {}
        language_name = request.POST.get('language')
        proficiency = request.POST.get('proficiency')
        profile_user = request.user
        lang_name = language_name

        for l in (Language.objects.filter(name__iexact=language_name)):
            print "FOUND A LANGUAGE IN OBJECTS: " + l.name 
            lang_name = l.name

        lang, lang_created = Language.objects.get_or_create(name=lang_name)
        print "Lang name:" + str(lang.name) + "Lang created:" + str(lang_created)

        user_ratings = UserRating.objects.filter(profile_user=profile_user)
        updated = False
        for r in user_ratings:
            if r.language.name == lang_name:
                print "updated"
                r.proficiency = proficiency
                r.save()
                updated = True
                rating = r

        if (not updated):
            print "not updated"
            rating = UserRating.objects.create(profile_user=profile_user, language=lang, proficiency=proficiency, credibility=0)
            rating.save()
        """
        try:
            rating = UserRating.objects.get(profile_user=profile_user, language=lang)
            rating.update(proficiency=proficiency)
            rating.save()
            print 1
        except:
            print 2
            rating = UserRating.objects.create(profile_user=profile_user, language=lang, proficiency=proficiency, credibility=0)
            rating.save()"""
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

@login_required
def sort_lang_stream_recent(request):
    if request.is_ajax():
        context = {}
        g = get_auth_user_git(request)
        if g.get_rate_limit().rate.remaining < 250:
            context['repos'] = []
            context['message'] = "Error rate limit exceeded"
            return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
        profile_user = request.user

        try:
            language = request.GET['language']
            query = "language:" + language + " stars:>=500"
            repos = g.search_repositories(query,sort='updated',order='desc').get_page(0)
        except:
            repos = []
            no_results = 'true'
            context['no_results'] = no_results
            context['my_languages_stream_no_results'] = 'true'
        these_repo_results = []
        for repo in repos[:5]:
            try:
                repo = Repository.objects.get(repo_id = repo.id)
                x = Repo(None,repo.repo_id,g.get_user(), g)
            except ObjectDoesNotExist:
                x = Repo(repo, repo.id, g.get_user(), g)
            for comment in x.comments:
                comment.profile_user.get_avatar_url = comment.profile_user.get_avatar_url(g, comment.profile_user.username)
            these_repo_results.append(x)
        context["repos"] = these_repo_results
        context['profile_user'] = profile_user
        context['comment_form'] = CommentForm()
        return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
    else:
        # uhhhhhhhh awk. this should never happen
        pass

@login_required
def sort_lang_stream_popular(request):
    if request.is_ajax():
        context = {}
        g = get_auth_user_git(request)
        if g.get_rate_limit().rate.remaining < 250:
            context["repos"] = []
            context['profile_user'] = request.user
            context['message'] = "Error rate limit exceeded"
            return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
        profile_user = request.user

        try:
            language = request.GET['language']
            query = "language:" + language + " stars:>=700"
            repos = g.search_repositories(query,sort='stars',order='desc').get_page(0)
        except:
            repos = []
            no_results = 'true'
            context['no_results'] = no_results
            context['my_languages_stream_no_results'] = 'true'
        these_repo_results = []
        for repo in repos[:5]:
            try:
                repo = Repository.objects.get(repo_id = repo.id)
                x = Repo(None,repo.repo_id,g.get_user(), g)
            except ObjectDoesNotExist:
                x = Repo(repo, repo.id, g.get_user(), g)
            for comment in x.comments:
                comment.profile_user.get_avatar_url = comment.profile_user.get_avatar_url(g, comment.profile_user.username)
            these_repo_results.append(x)
        context["repos"] = these_repo_results
        context['profile_user'] = request.user
        context['comment_form'] = CommentForm()
        return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
    else:
        # uhhhhhhhh awk. this should never happen
        pass


def dbrepodiffy(dbrepo, gitrepo, contribs, level):
    avgdif=0
    difobjs = dbrepo.difficulty_set.all()
    smcount = 0
    for obj in difobjs:
        avgdif += obj.rating
        smcount += 1
    if smcount > 0:
        avgdif = avgdif/smcount
    else:
        avgdif = (contribs/10 + gitrepo.size/10000)/2 
    avgdif = min(avgdif,5)
    return level==0 or (level==1 and avgdif<=2) or (level==2 and avgdif>2 and avgdif<=4) or (level==3 and avgdif>4)

# Given a search type and some text, returns a list of repositories
@login_required
def repo_search_list(request):
    if request.is_ajax():
        context = {}
        g = get_auth_user_git(request)
        profile_user = request.user
        if g.get_rate_limit().rate.remaining < 250:
            context["repos"] = []
            context['profile_user'] = profile_user
            context['message'] = "Error rate limit exceeded"
            return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
        print "Start is:", g.get_rate_limit().rate.remaining
        context['repos'] = {}
        choice = request.GET.get("types")
        text = request.GET.get("text")
        text = text.replace('+',' ').strip().lower()

        easy = ['easy','beginner','simple']
        medium = ['medium', 'intermediate']
        hard = ['hard','difficult','advanced']
        levels = easy+medium+hard

        level = 0
        if any(word in text for word in easy):
            level = 1
        if any(word in text for word in medium):
            level = 2
        if any(word in text for word in hard):
            level = 3

        word_list = text.split()
        text = ' '.join([i for i in word_list if i not in levels])
        count = 0
        dbrepos = []
        nondbrepos = []
        langrepos = []
        
        if(choice == 'User'):
            repos = []
            results = []
            users = g.search_users(text,sort='followers',order='desc')
            for user in users:
                for repo in user.get_repos().get_page(0):
                    results.append(repo)
            repos.append(results)

        elif(choice == 'Repo'):
            repos = []
            results = g.search_repositories(text,sort='stars',order='desc').get_page(0)
            repos.append(results)
                
        elif(choice == 'Lang'):
            repos = []
            if text in languages:
                for currrepo in Repository.objects.filter(languages__name__iexact = text).distinct():
                    #language update code
                    repo_id = int(currrepo.repo_id)
                    dblangs = currrepo.languages.all()
                    repo = g.get_repo(repo_id)
                    gitlangs = repo.get_languages().keys()
                    if (dblangs.count()>len(gitlangs)):
                        for l in dblangs:
                            currrepo.languages.remove(l)
                    for l in gitlangs:
                        if not dblangs.filter(name=l).exists():
                            lang,created = Language.objects.get_or_create(name=l)
                            currrepo.languages.add(lang)
                            currrepo.save()
                    #difficulty calc
                    try:
                        contribs = len(list(repo.get_contributors()))
                        if dbrepodiffy(currrepo, repo, contribs, level): 
                            x = Repo(None,repo_id,g.get_user(), g)
                            langrepos.append(x)
                            count+=1
                    except:
                        continue
                if count<=7: 
                    query = "language:"+text+" stars:>=500"
                    results = g.search_repositories(query,sort='stars',order='desc').get_page(0)
                    repos.append(results)
            else:
                context["repos"] = []
                context['profile_user'] = profile_user
                context['message'] = "No results matched your search."
                return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
        else:
            print "problem"

        these_repo_results = []
        
        repos=list(itertools.chain(*repos))
        if len(repos) < 1 and len(langrepos)<1:
            #no valid results
            context["repos"] = []
            context['profile_user'] = profile_user
            context['message'] = "No results matched your search."
            return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
        for repo in repos:
            if count>7:
                break
            try:
                contribs = len(list(repo.get_contributors()))
            except:
                continue
            avgdif = 0
            try:
                currrepo = Repository.objects.get(repo_id = repo.id)
                if choice == 'Lang':
                    continue
                if dbrepodiffy(currrepo,repo,contribs,level): 
                    x = Repo(None,int(currrepo.repo_id),g.get_user(), g)
                    dbrepos.append(x)
                    print x.name
                    count += 1
            except ObjectDoesNotExist:
                avgdif = (contribs/10 + repo.size/10000)/2 
                avgdif = min(avgdif,5)
                if level==0 or (level==1 and avgdif<=2) or (level==2 and avgdif>2 and avgdif<=4) or (level==3 and avgdif>4):
                    x = Repo(repo, int(repo.id), g.get_user(), g)
                    nondbrepos.append(x)
                    count += 1
                    print x.name

            for comment in x.comments:
                comment.profile_user.get_avatar_url = comment.profile_user.get_avatar_url(g, comment.profile_user.username)

        these_repo_results = langrepos+dbrepos+nondbrepos
        these_repo_results.sort(key=lambda x: x.doc_rating, reverse= True)
        context["repos"] = these_repo_results
        context['comment_form'] = CommentForm()
        # DO NOT DELETE THE FOLLOWING LINE IT ALLOWS COMMENT LIKES AND DISLIKES TO POPULATE CORRECTLY
        context['profile_user'] = profile_user
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

@login_required
def get_file_contents(request):
    if request.is_ajax():
        context = {}
        hub = get_auth_user_git(request)
        if hub.get_rate_limit().rate.remaining < 250:
            context["repo"] = []
            context['message'] = "Error rate limit exceeded"
            return render_to_response('codebook/file-contents-combined-extra-info.html', context, content_type="html")
        if request.GET:
            rep_id = request.GET.get("repo_id")
            sha = request.GET.get("sha")
            path = request.GET.get("path")
        elif request.POST:
            rep_id = request.POST.get("repo_id")
            sha = request.POST.get("sha")
            path = request.POST.get("path")
        rep = hub.get_repo(int(rep_id))
        blob = rep.get_git_blob(sha)
        print blob.encoding
        content = blob.content
        filecontent = "no file content to show."
        if blob and content:
            filecontent = base64.b64decode(content)
        else:
            pass
        context['file_content'] = filecontent
        context['repo'] = rep
        context['file_path'] = path
        return render_to_response('codebook/file-contents-combined-extra-info.html', context, content_type="html")

    else:
        pass

@login_required
def watch_list(request):
    g = get_auth_user_git(request)
    context = {}
    if g.get_rate_limit().rate.remaining < 250:
        context["repos"] = []
        context['profile_user'] = request.user
        context['message'] = "Error rate limit exceeded"
        return render_to_response('codebook/repository-list-combined.html', context, content_type="html")
    user = g.get_user()
    watched = user.get_subscriptions()

    recent_watched = []
    for repo in watched[:10]:
        try:
            repo = Repository.objects.get(repo_id = repo.id)
            x = Repo(None, repo.repo_id, user, g)
        except ObjectDoesNotExist:
            x = Repo(repo, repo.id, user, g)

        for comment in x.comments:
            comment.profile_user.get_avatar_url = comment.profile_user.get_avatar_url(g, comment.profile_user.username)
        recent_watched.append(x)

    context['repos'] = recent_watched
    context['comment_form'] = CommentForm()
    context['profile_user'] = request.user
    return render_to_response('codebook/repository-list-combined.html', context, content_type="html")

@transaction.atomic
@login_required
def save_file_from_repo(request):
    if request.is_ajax:
        profile_user = request.user
        #social = request.user.social_auth.get(provider='github')
        #token = social.extra_data['access_token']
        #hub = Github(token)
        if request.GET:
            repo_id = int(request.GET.get("repo_id"))
            path = request.GET.get("file_path")
        elif request.POST:
            repo_id = int(request.POST.get("repo_id"))
            path = request.POST.get("file_path")

        if path == None or repo_id == None:
            return HttpResponse('False', content_type="text")

        repo, repo_created = Repository.objects.get_or_create(repo_id=repo_id)
        if repo_created:
            g = get_auth_user_git(request)
            langs = g.get_repo(int(repo_id)).get_languages().keys()
            for l in langs:
                lang,created = Language.objects.get_or_create(name=l)
                repo.languages.add(lang)
                repo.save()
        file, file_created = RepoFile.objects.get_or_create( path=path, average_difficulty=0, average_quality=0, repository=repo)
        saved, saved_created = Saved.objects.get_or_create(profile_user=profile_user, repo_file=file)
        file.savers.add(profile_user)
        file.save()
        return HttpResponse('True', content_type="text")
    else:
        pass


@login_required
@transaction.atomic
def rate_documentation(request):
    if request.is_ajax:
        profile_user = request.user
        if request.POST.get("rating") == None or request.POST.get("repo_id") == None:
            return HttpResponse('True', content_type="text")
        repo_id = int(request.POST.get("repo_id"))
        rating = int(request.POST.get("rating"))

        print repo_id
        print rating

        repo, repo_created = Repository.objects.get_or_create(repo_id=repo_id)
        if repo_created:
            g = get_auth_user_git(request)
            langs = g.get_repo(int(repo_id)).get_languages().keys()
            for l in langs:
                lang,created = Language.objects.get_or_create(name=l)
                repo.languages.add(lang)
                repo.save()
        print repo_created
        documentation, documentation_created = Documentation.objects.update_or_create(profile_user=profile_user, rating=rating, repository=repo)
        print documentation_created
        return HttpResponse('True', content_type="text")
    else:
        pass

@login_required
@transaction.atomic
def rate_difficulty(request):
    if request.is_ajax:
        profile_user = request.user
        if request.POST.get("rating") == None or request.POST.get("repo_id") == None:
            return HttpResponse('True', content_type="text")
        rating = int(request.POST.get("rating"))

        repo_id = int(request.POST.get("repo_id"))


        repo, repo_created = Repository.objects.get_or_create(repo_id=repo_id)

        if repo_created:
            g = get_auth_user_git(request)
            langs = g.get_repo(int(repo_id)).get_languages().keys()
            for l in langs:
                lang,created = Language.objects.get_or_create(name=l)
                repo.languages.add(lang)
                repo.save()
        difficulty, difficulty_updated = Difficulty.objects.update_or_create(profile_user=profile_user, rating=rating, repository=repo)
        print difficulty_updated
        return HttpResponse('True', content_type="text")
    else:
        pass
