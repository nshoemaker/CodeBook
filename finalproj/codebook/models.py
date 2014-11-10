from django.db import models

from django.db.models import Q

from github import Github 
# g = Github(user, password) - USE THIS ONE TO TEST B/C IT WON'T HIT RATE LIMIT
g = Github()

import base64

class Stack(models.Model):
    name = models.CharField(max_length=40)
    icon = models.CharField(max_length=40)

class Language(models.Model):
    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=40)
    #extensions = models.CharField(max_length=20)

class UserRating(models.Model):
    language = models.ForeignKey(Language)
    proficiency = models.IntegerField()  # how well they think they know the language
    credibility = models.IntegerField()  # how well we think they know the language

class ProfileUser(models.Model):
    # note that there will be some id that we can use to get profile info for this user from github
    languages = models.ManyToManyField(Language, related_name="languages_liked")

    def get_username(self):
        return "User #" + str(self.id)

    def get_id(self):
        return 1

    def get_avatar_url(self):
        return "https://github.com/images/error/octocat_happy.gif"

    def get_git_profile_url(self):
        return "https://api.github.com/users/octocat"
    
    def get_repos(self):
        pass

    def get_following(self):
        pass

    def get_email(self):
        return "user@email.com"

    def get_website(self):
        return "userwebsite.com"

    def get_company(self):
        return "User Company"

    def get_bio(self):
        return "This is my user bio."

class Comment(models.Model):
    profile_user = models.ForeignKey(ProfileUser)
    text = models.CharField(max_length=400)  # text of comment
    date_time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=400)  # relative path file comment on
    likers = models.ManyToManyField(ProfileUser, related_name="liked_by")

#class FileComment (models.Model):
#    profile_user = models.ForeignKey(ProfileUser)
#    text = models.CharField(max_length=400)
#    date_time = models.DateTimeField(auto_now_add=True)
#    path = models.CharField(max_length=400)  # relative path file comment on
#    likers = models.ManyToManyField(ProfileUser, related_name="comment_liked_by")

class Tag(models.Model):
    text = models.CharField(max_length=20)
    profile_user = models.ForeignKey(ProfileUser, related_name="created")
    date_time = models.DateTimeField(auto_now_add=True)
    endorsements = models.ManyToManyField(ProfileUser)
    # tagger field with hash info about tagger - name, email, date

class Repository(models.Model):
    repo_id = models.IntegerField(primary_key=True)
    comments = models.ManyToManyField(Comment)

    def get_url(self):
        return g.get_repo(self.repo_id).html_url

    def get_creator(self):
        return g.get_repo(self.repo_id).owner.name

    def get_name(self):
        return g.get_repo(self.repo_id).name

    def get_language(self):
        return g.get_repo(self.repo_id).language

    def get_date_created(self):
        return g.get_repo(self.repo_id).created_at

    def get_star_count(self):
        return g.get_repo(self.repo_id).stargazers_count

    def get_watch_count(self):
        return g.get_repo(self.repo_id).watchers_count

    def get_kb_size(self):
        return g.get_repo(self.repo_id).size

    def get_watchers(self):
        pass

class RepoFile (models.Model):
    repository = models.ForeignKey(Repository)
    path = models.CharField(max_length=400)
    comments = models.ManyToManyField(Comment)
    savers = models.ManyToManyField(ProfileUser, related_name="saved_by")
    average_difficulty = models.IntegerField(blank=True)
    average_quality = models.IntegerField(blank=True)
    tags = models.ManyToManyField(Tag)

    def get_creator(self):
        repo_id = self.repository.repo_id
        repo = g.get_repo(repo_id)
        return repo.owner.name

    def get_name(self):
        repo_id = self.repository.repo_id
        repo = g.get_repo(repo_id)
        return repo.get_contents(self.path).name

    def get_language(self):
        return "file_lang"

    def get_date_created(self):
        return "1/1/2014"

    def get_content(self):
        repo_id = self.repository.repo_id
        repo = g.get_repo(repo_id)
        content = repo.get_contents(self.path).content
        return base64.b64decode(content)


class Difficulty(models.Model):
    rating = models.IntegerField()
    repo_file = models.ForeignKey(RepoFile)
    profile_user = models.ForeignKey(ProfileUser)
    date_time = models.DateTimeField(auto_now_add=True)

#class Watch(models.Model):
    # can list watchers and list repositories being watched
    #profile_user = models.ForeignKey(ProfileUser)
    #repositories = models.ManyToManyField(Repository)
    #date_time = models.DateTimeField(auto_now_add=True)

#class Star(models.Model):
    # can list stargazers and list repositories being starred
    #profile_user = models.ForeignKey(ProfileUser)
    #repository = models.ForeignKey(Repository)
    #date_time = models.DateTimeField(auto_now_add=True)

class Saved(models.Model):
    profile_user = models.ForeignKey(ProfileUser, primary_key=True)
    files = models.ManyToManyField(RepoFile)
    date_time = models.DateTimeField(auto_now_add=True)