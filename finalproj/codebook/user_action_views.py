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

from content_views import *

def signin(request):
    pass

# Like or Unlike a Comment
def like_comment(request, source, comment_id):
    context = {}
    comment = Comment.objects.get(id=comment_id)

    # right now, liking and unliking works for a comment by profile_user 1 ONLY
    if not (comment.likers.filter(id=1)):
        liker = ProfileUser.objects.get(id=1)
        comment.likers.add(liker)
        comment.save()
    # User has already liked comment - click will "un-like"
    else:
        liker = ProfileUser.objects.get(id=1)
        comment.likers.remove(liker)
        comment.save()

    # Ask others how they sent back to correct page
    return redirect('/' + source)

# Watch or Unwatch a Repository 
def watch_repo(request, source, repo_id):
	authenticated_user = request.user #object
	repo = g.get_repo(repo_id)

	if (authenticated_user.has_in_watched(repo)):
		# User has already watched this repo - click will "un-watch"
		authenticated_user.remove_from_watched(repo)
	else:
		authenticated_user.add_to_watched(repo)

	# Ask others how they sent back to correct page
	return redirect('/' + source)

# Star or Unstar a Repository 
def star_repo(request, source, repo_id):
	authenticated_user = 0 #object
	repo = g.get_repo(repo_id)

	if (authenticated_user.has_in_starred(repo)):
		# User has already watched this repo - click will "un-watch"
		authenticated_user.remove_from_starred(repo)
	else:
		authenticated_user.add_to_starred(repo)

	# Ask others how they sent back to correct page
	return redirect('/' + source)

# Save or Unsave a Post
def save_file(request, file_id):
	profile_user = ProfileUser.objects.get(user=request.user)
	repofile = RepoFile.objects.get(id=file_id)
	user_saves = Saved.objects.get(profile_user=profile_user)

	if not (user_saves.files.filter(id=file_id)):
		user_saves.files.add(repofile)
		user_saves.save()
		repofile.savers.add(profile_user)
		repofile.save()
	# User has already saved this post - click will "un-save"
	else:
		user_saves.posts.remove(repofile)
		user_saves.save()
		repofile.savers.remove(profile_user)
		repofile.save()

	# Ask others how they sent back to correct page
	return redirect('/')

def search(request):
    context = {}
    social = request.user.social_auth.get(provider='github')
    token = social.extra_data['access_token']
    g = Github(token)
    new_repo = Repository(g.get_user().get_repos()[0].id)  #Repository(repo_id=3222)
    new_repo.save()
    new_user = ProfileUser()
    new_user.save()
    context["repos"] = Repository.objects.all
    context["source"] = 'codebook/search_results'
    context['comment_form'] = CommentForm()
    context['profile_user'] = ProfileUser.objects.get(id=1)
    return render(request, "codebook/search-results-page.html", context)

def comment(request, comment_type, source, id):
	print "COMMENT TYPE" + comment_type
	context = {}

	if request.method == "GET":
		context['comment_form'] = CommentForm()
		return redirect('/' + source)

	# For now, creating a new user for each comment 
	# Need to change this once user authentication is a thing
	new_user = ProfileUser()
	new_user.save()
	new_comment = Comment(profile_user=new_user)
	form = CommentForm(request.POST, instance=new_comment)
	if not form.is_valid():
		context['form'] = form
		return redirect('/' + source)
	form.save()
	repo = Repository.objects.get(repo_id=id)
	repo.comments.add(new_comment)
	repo.save()
	return redirect('/' + source)

	if (comment_type == 'repo'):
		repo = Repository.objects.get(repo_id=id)
		repo.comments.add(new_comment)
		repo.save()
	else:
		repoFile = RepoFile.objects.get(id=id)
		repoFile.comments.add(new_comment)
		repoFile.save()
	return redirect('/' + source)
