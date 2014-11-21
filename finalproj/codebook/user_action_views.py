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
import sys
g = Github('dmouli', 'Spongebob5%')

class Repo:
    def __init__(self, repo, id, user):         
        if(repo is None):
            repo = g.get_repo(id)
        branches = repo.get_branches()
        SHA = branches[0].commit.sha
        tree = repo.get_git_tree(SHA,True).tree
        try:
            deffile = repo.get_contents(tree[0].path)
        except:
            deffile = repo.get_readme()
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
        self.is_current_user_watching = user.has_in_watched(repo) 
        self.watch_count = repo.watchers_count
        self.file_tree = tree
        self.readme = repo.get_readme()
        self.readme_contents = base64.b64decode(self.readme.content)
        self.default_file_name = deffile.name
        self.default_file_contents = base64.b64decode(deffile.content)
        self.default_file_path = deffile.path
        self.doc_rating = 0
        self.difficulty_rating = 0
        self.tag_list = None
        self.comments = Comment.objects.none()

def quick_search(request, language):
    context={}
    if request.user:
        profile_user = request.user
        social = request.user.social_auth.get(provider='github')
        token = social.extra_data['access_token']
        g = Github(token)
    query = "language:"+language+" stars:>=500"
    repos = g.search_repositories(query,sort='stars',order='desc').get_page(0)
    these_repo_results = []
    for repo in repos[:10]:
        x = Repo(repo, repo.id, g.get_user())         
        print x.name
        these_repo_results.append(x) 
    context["repos"] = these_repo_results
    context['files'] = RepoFile.objects.filter(id=10)
    context["source"] = 'search'
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user 
    context['filter'] = 'Languages'
    context['searchtext'] = language
    return render(request, "codebook/search-results-page.html", context)

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


def search(request):
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
    
    if(choice == 'User'):
        repos = []
        files = [] 
        users = g.search_users(text,sort='followers',order='desc')
        for user in users:
            for repo in user.get_repos().get_page(0):
               repos.append(repo)
    
    elif(choice == 'Repo'):
        files = [] 
        repos = g.search_repositories(text,sort='stars',order='desc').get_page(0)
    
    elif(choice == 'Code'):
        print "CAME IN HERE"
        repos = [] 
        query = text+" user:github size:>10000"
        files = g.search_code(query)
        for f in files:
            print f.name+": "+f.html_url
    
    else:
        #check that language?
        files = [] 
        query = "language:"+text+" stars:>=500"
        repos = g.search_repositories(query,sort='stars',order='desc').get_page(0)


    these_file_results = []
    for i in xrange(min(len(list(files)),10)):
        file_name = files[i].name
        print file_name + "\n"
        file_contents = files[i].repository.get_contents(file_name)
        print file_contents + "\n"
        file_path = file_contents.path 
        print file_path + "\n"

    these_repo_results = []
    for repo in repos[:10]:
        x = Repo(repo, repo.id, g.get_user())        
        print x.name
        these_repo_results.append(x) 
     
        """branches = repos[i].get_branches()
        SHA = branches[0].commit.sha
        tree = repos[i].get_git_tree(SHA,True).tree
        for elt in tree:
            try:
                size = repos[i].get_contents(elt.path).size
                name = repos[i].get_contents(elt.path).name
                if repos[i].get_contents(elt.path).size>0:
                    new_file = RepoFile(repository=new_repo, path=elt.path, average_difficulty=0, average_quality=0)
                    new_file.save()
            except:
                pass"""

    # Temp code to populate the search page #
    #repo_obj = Repository(repo_id = 7986587)
    #repo_obj.save()
    #repo_gilbert = g.get_repo(7986587)
    #file_index = repo_gilbert.get_contents("index.html")
    #path = file_index.path
    #new_file = RepoFile(repository=repo_obj, path=path, average_difficulty=0, average_quality=0)
    #new_file.save()
    
    context["repos"] = these_repo_results
    context['files'] = RepoFile.objects.all()
    context["source"] = 'search'
    context['comment_form'] = CommentForm()
    context['profile_user'] = profile_user 
    context['gh_user'] = g.get_user()
    context['searchtext'] = text
    context['filter'] = choice
    return render(request, "codebook/search-results-page.html", context)

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
