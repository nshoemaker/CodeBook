from django.db import models

from django.contrib.auth.models import User

from django.db.models import Q

class Stack(models.Model):
    name = models.CharField(max_length=40)
    icon = models.CharField(max_length=40)

class Language(models.Model):
    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=40)
    #extensions = models.CharField(max_length=20)

class Rating(models.Model):
    language = models.ForeignKey(Language)
    proficiency = models.IntegerField()  # how well they think they know the language
    credibility = models.IntegerField()  # how well we think they know the language

class ProfileUser(models.Model):
    # note that there will be some id that we can use to get profile info for this user from github
    languages = models.ManyToManyField(Language, related_name="languages_liked")

    def get_username(self):
        return "username"

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

    def get_compant(self):
        return "User Company"

    def get_bio(self):
        return "This is my user bio."

class Comment(models.Model):
    profile_user = models.ForeignKey(ProfileUser)
    text = models.CharField(max_length=400)  # text of comment
    date_time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=400)  # relative path file comment on
    likers = models.ManyToManyField(ProfileUser, related_name="liked_by")

class Repository(models.Model):
    # note that there will need to be an extra field with some github id that we use
    comments = models.ManyToManyField(Comment)

    def get_creator(self):
        return "repository_creator"

    def get_name(self):
        return "repository_name"

    def get_language(self):
        return "repository_language"

    def get_date_created(self):
        return "1/1/2014"

    def get_star_count(self):
        return 100

    def get_watch_count(self):
        return 300

    def get_kb_size(self):
        return 24

    def get_watchers(self):
        pass



class Post (models.Model):
    creator = models.ForeignKey(ProfileUser)
    name = models.CharField(max_length=200)
    repository = models.ForeignKey(Repository)
    language = models.ManyToManyField(Language, related_name="language_used_in_post", blank=True)
    stack = models.ManyToManyField(Stack, related_name="stack_used_in_post", blank=True)
    date_created = models.DateTimeField(auto_now_add=False)
    star_count = models.IntegerField()
    comments = models.ManyToManyField(Comment)
    savers = models.ManyToManyField(ProfileUser, related_name="saved_by")

class Tag(models.Model):
    text = models.CharField(max_length=20)
    profile_user = models.ForeignKey(ProfileUser, related_name="created")
    repository = models.ForeignKey(Repository)
    date_time = models.DateTimeField(auto_now_add=True)
    endorsements = models.ManyToManyField(ProfileUser)
    # tagger field with hash info about tagger - name, email, date

class Difficulty(models.Model):
    rating = models.IntegerField()
    repository = models.ForeignKey(Repository)
    profile_user = models.ForeignKey(ProfileUser)
    date_time = models.DateTimeField(auto_now_add=True)

class Watch(models.Model):
    # can list watchers and list repositories being watched
    profile_user = models.ForeignKey(ProfileUser)
    repositories = models.ManyToManyField(Repository)
    date_time = models.DateTimeField(auto_now_add=True)

class Star(models.Model):
    # can list stargazers and list repositories being starred
    profile_user = models.ForeignKey(ProfileUser)
    repository = models.ForeignKey(Repository)
    date_time = models.DateTimeField(auto_now_add=True)

#class Saved(models.Model):
#    profile_user = models.ForeignKey(ProfileUser)
#    posts = models.ManyToManyField(Post)
#    date_time = models.DateTimeField(auto_now_add=True)
