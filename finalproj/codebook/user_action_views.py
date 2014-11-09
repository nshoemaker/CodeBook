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
def like_comment(request, comment_id):
	context = {}
	comment = Comment.objects.get(id=id)

	if not (comment.likers.filter(user=request.user)):
		liker = ProfileUser.objects.get(user=request.user)
		comment.likers.add(liker)
		comment.save
	# User has already liked comment - click will "un-like"
	else:
		liker = ProfileUser.objects.get(user=request.user)
		comment.likers.remove(disliker)
		comment.save()

	# Ask others how they sent back to correct page
	return redirect("/")

# Watch or Unwatch a Repository 
def watch_repo(request, repo_id):
	profile_user = ProfileUser.objects.get(user=request.user)
	repo = Repository.objects.get(id=repo_id)
	user_watches = Watch.objects.get(profile_user=profile_user)

	if not (user_watches.repositories.filter(id=repo.id)):
		user_watches.repositories.add(repo)
		user_watches.save()
		repo.watchers.add(profile_user)
		repo.save()
	# User has already watched this repo - click will "un-watch"
	else:
		user_watches.repositories.remove(repo)
		user_watches.save()
		repo.watchers.remove(profile_user)
		repo.save()

	# Ask others how they sent back to correct page
	return redirect('/')

# Save or Unsave a Post
def save_post(request, post_id):
	profile_user = ProfileUser.objects.get(user=request.user)
	post = Repository.objects.get(id=post_id)
	user_saves = Saved.objects.get(profile_user=profile_user)

	if not (user_saves.posts.filter(id=post.id)):
		user_saves.posts.add(post)
		user_saves.save()
		post.savers.add(profile_user)
		post.save()
	# User has already saved this post - click will "un-save"
	else:
		user_saves.posts.remove(post)
		user_saves.save()
		post.savers.remove(profile_user)
		post.save()

	# Ask others how they sent back to correct page
	return redirect('/')

def search(request):
	context = {}
	context["repos"] = Repository.objects.all
	context["source"] = 'codebook/search_results'
	context['comment_form'] = CommentForm()
	return render(request, "codebook/search-results-page.html", context)

def comment_repo(request, source, repo_id):
	context = {}

	if request.method == "GET":
		context['comment_form'] = CommentForm()
		return redirect('/' + source)

	new_user = ProfileUser()
	new_user.save()
	new_comment = Comment(profile_user=new_user)
	form = CommentForm(request.POST, instance=new_comment)
	if not form.is_valid():
		context['form'] = form
		return redirect('/' + source)
	form.save()
	repo = Repository.objects.get(repo_id=repo_id)
	repo.comments.add(new_comment)
	repo.save()
	return redirect('/' + source)