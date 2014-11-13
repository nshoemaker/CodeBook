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
#####################################################

from content_views import *
g2 = Github('dmouli', 'Spongebob5%')

def get_correct_context(request, source):
	context = {}
	profile_user = request.user
	if (source == 'search'):
		context["repos"] = Repository.objects.filter(repo_id=3222)
    	context['files'] = RepoFile.objects.filter(id=10)
    	context["source"] = 'search'
    	context['comment_form'] = CommentForm()
    	context['profile_user'] = profile_user
	return context 

def get_template(source):
	if (source == 'search'):
		return "codebook/search-results-page.html"
	else:
		return "/"

def get_auth_user_git(request):
	social = request.user.social_auth.get(provider='github')
	token = social.extra_data['access_token']
	g = Github(token)
	return g

def signin(request):
    pass

# Like or Unlike a Comment
def like_comment(request, source, comment_id):
	context = {}
	comment = Comment.objects.get(id=comment_id)
	profile_user = ProfileUser.objects.get(user = request.user)

	if not (comment.likers.filter(liked_by=profile_user)):
		comment.likers.add(profile_user)
		comment.save()
	# User has already liked comment - click will "un-like"
	else:
		comment.likers.remove(profile_user)
		comment.save()

	# Ask others how they sent back to correct page
	return redirect('/' + source)

# Watch or Unwatch a Repository 
def watch_repo(request, source, repo_id):
	g = get_auth_user_git(request)
	repo = g.get_repo(int(repo_id))
	user = g.get_user()

	if (user.has_in_subscriptions(repo)):
		print "CAME INTO HAS WATCHED"
		# User has already watched this repo - click will "un-watch"
		user.remove_from_subscriptions(repo)
	else:
		print "CAME INTO ADD TO WATCHED"
		user.add_to_subscriptions(repo)

	return redirect(reverse(source))

# Star or Unstar a Repository 
def star_repo(request, source, repo_id):
	g = get_auth_user_git(request)
	repo = g.get_repo(int(repo_id))
	user = g.get_user()

	if (user.has_in_starred(repo)):
		# User has already watched this repo - click will "un-watch"
		user.remove_from_starred(repo)
	else:
		user.add_to_starred(repo)

	return redirect(reverse(source))

# Save or Unsave a Post
def save_file(request, source, file_id):
	profile_user = request.user
	repofile = RepoFile.objects.get(id=file_id)
	user_saves = Saved.objects.get(profile_user=profile_user)

	if not (user_saves.files.filter(id=file_id)):
		user_saves.files.add(repofile)
		user_saves.save()
		repofile.savers.add(profile_user)
		repofile.save()
	# User has already saved this post - click will "un-save"
	else:
		user_saves.files.remove(repofile)
		user_saves.save()
		repofile.savers.remove(profile_user)
		repofile.save()
	# Ask others how they sent back to correct page
	return redirect('/' + source)

def search(request):
    social = request.user.social_auth.get(provider='github')
    token = social.extra_data['access_token']
    g = Github(token)
    profile_user = request.user
    context = {}
    
    # Temp code to populate the search page #
    """
    repo_obj = Repository(repo_id = 7986587)
    repo_obj.save()
    repo_gilbert = g.get_repo(7986587)
    file_index = repo_gilbert.get_contents("index.html")
    path = file_index.path
    new_file = RepoFile(repository=repo_obj, path=path, average_difficulty=0, average_quality=0)
    new_file.save()
    """
    
    """
    repos = g.get_organization("github").get_repos()
    i = 0
    for repo in repos:
        if (i < 5):
            new_repo = Repository(repo_id = repo.id)
            new_repo.save()
            if (i == 0):
                repofile = repo.get_contents("README.md")
                path = repofile.path
                new_file = RepoFile(repository=new_repo, path=path, average_difficulty=0, average_quality=0)
                new_file.save()
            i = i + 1
        else:
            break
    """
    # End temp code to populate the search page #
    
    context["repos"] = Repository.objects.filter(repo_id=3222)
    context['files'] = RepoFile.objects.filter(id=10)
    context["source"] = 'search'
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user 
    return render(request, "codebook/search-results-page.html", context)

def comment(request, comment_type, source, id):
	context = {}

	if request.method == "GET":
		context['comment_form'] = CommentForm()
		return redirect(reverse(source))

	profile_user = request.user
	new_comment = Comment(profile_user=profile_user)
	form = CommentForm(request.POST, instance=new_comment)
	if not form.is_valid():
		context['form'] = form
		return redirect(reverse(source))
	form.save()

	if (comment_type == 'repo'):
		repo = Repository.objects.get(repo_id=id)
		repo.comments.add(new_comment)
		repo.save()
	else:
		repoFile = RepoFile.objects.get(id=id)
		repoFile.comments.add(new_comment)
		repoFile.save()
	return redirect(reverse(source))
