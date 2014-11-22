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
import sys
g = Github('dmouli', 'Spongebob5%')


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

# Save or Unsave a Post
def save_file(request, source, file_id):

    profile_user = request.user
    repofile = RepoFile.objects.get(id=file_id)
    try:
        saved_file = Saved.objects.get(profile_user=profile_user, repo_file=repofile)
        # User has already saved this post - click will "un-save"
        saved_file.delete() 
    except:
        saved_file = Saved(profile_user=profile_user, repo_file=repofile)
        saved_file.save() 
        repofile.savers.add(profile_user)
        repofile.save() 
	return redirect('/' + source)


"""
Technically, this should never be called
"""
def comment(request, comment_type, source, id):
    print "THIS IS GETTING CALLED"
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

@login_required
def new_search(request):
    social = request.user.social_auth.get(provider='github')
    token = social.extra_data['access_token']
    g = Github(token)
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
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user
    context['gh_user'] = g.get_user()
    context['searchtext'] = text
    context['filter'] = choice
    return render(request, "codebook/search-results-page.html", context)

@login_required
def new_quick_search(request, language):
    context={}
    if request.user:
        profile_user = request.user
    context["repos"] = {}
    context['files'] = {}
    context["source"] = 'search'
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user
    context['filter'] = 'Languages'
    context['searchtext'] = language
    return render(request, "codebook/search-results-page.html", context)
