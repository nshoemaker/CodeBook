from views import *

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