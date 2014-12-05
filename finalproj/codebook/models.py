from django.db import models

from django.db.models import Q

from django.contrib.auth.models import User, UserManager, AbstractBaseUser
from django.utils import timezone
from github import Github 

import base64
import multiprocessing 

class Stack(models.Model):
    name = models.CharField(max_length=40)
    icon = models.CharField(max_length=40)

class Language(models.Model):
    name = models.CharField(max_length=20)

class ProfileUser(AbstractBaseUser):
    is_anonymous = models.BooleanField(default = False)
    username = models.CharField(default = "", max_length=100)
    firstname = models.CharField(default = "", max_length=100)
    lastname = models.CharField(default = "", max_length=100)
    objects = UserManager()
    date_joined = models.DateTimeField(default=timezone.now())
    is_active   = models.BooleanField(default=True)
    is_admin    = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    email = models.CharField(default = "", max_length=100)
    
    class Meta:
        db_table = u'profile_user'

    def get_full_name(self):
        return self.firstname + self.lastname
    
    def get_username(self):
        return self.username

    def get_id(self, g, username=None):
        try:
            if (username != None):
                return g.get_user(username).id
            else:
                return g.get_user().id
        except:
            return 0

    def get_avatar_url(self, g, username=None):
        try:
            if (username != None):
                return g.get_user(username).avatar_url
            else:
                return g.get_user().avatar_url
        except:
            return "static 'img/default_profile.jpg'"

    def get_git_profile_url(self, g, username=None):
        try:
            if (username != None):
                return g.get_user(username).html_url
            else:
                return g.get_user().html_url
        except:
            return "None"
    
    def get_repos(self, g, username=None):
        try:
            if (username != None):
                return g.get_user(username).get_repos()
            else:
                return g.get_user().get_repos()
        except:
            pass 

    def get_following(self, g, username=None):
        try:
            if (username != None):
                return g.get_user(username).get_followers()
            else:
                return g.get_user().get_followers()
        except:
            pass

    def get_email(self, g, username=None):
        try:
            if (username != None):
                email = g.get_user(username).email
            else:
                email = g.get_user().email

            if (email == "" or email == " "):
                return "None"
            else:
                return email
        except:
            return "None"


    def get_website(self, g, username=None):
        try:
            if (username != None):
                return g.get_user(username).blog
            else:
                return g.get_user().blog
        except:
            return "None"

    def get_company(self, g, username=None):
        try:
            if (username != None):
                return g.get_user(username).company
            else:
                return g.get_user().company
        except:
            return "None"

    def get_bio(self, g, username=None):
        try:
            if (username != None):
                return g.get_user(username).bio 
            else:
                return g.get_user().bio 
        except:
            return "None"


class UserRating(models.Model):
    profile_user = models.ForeignKey(ProfileUser)
    language = models.ForeignKey(Language)
    proficiency = models.IntegerField()  # how well they think they know the language
    credibility = models.IntegerField()  # how well we think they know the language


class Comment(models.Model):
    profile_user = models.ForeignKey(ProfileUser)
    text = models.CharField(max_length=400)  # text of comment
    date_time = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=2048)  # relative path file comment on
    likers = models.ManyToManyField(ProfileUser, related_name="liked_by")

class Tag(models.Model):
    text = models.CharField(max_length=20)
    profile_user = models.ForeignKey(ProfileUser, related_name="created")
    date_time = models.DateTimeField(auto_now_add=True)
    endorsements = models.ManyToManyField(ProfileUser)
    # tagger field with hash info about tagger - name, email, date

class Repository(models.Model):
    repo_id = models.IntegerField(primary_key=True)
    comments = models.ManyToManyField(Comment)
    languages = models.ManyToManyField(Language)

class RepoFile (models.Model):
    repository = models.ForeignKey(Repository)
    path = models.CharField(max_length=2048)
    comments = models.ManyToManyField(Comment)
    savers = models.ManyToManyField(ProfileUser, related_name="saved_by")
    average_difficulty = models.IntegerField(blank=True)
    average_quality = models.IntegerField(blank=True)
    tags = models.ManyToManyField(Tag)

    def get_creator(self, g):
        try:
            repo_id = self.repository.repo_id
            repo = g.get_repo(repo_id)
            return repo.owner.name
        except:
            return ""

    def get_name(self, g):
        try:
            repo_id = self.repository.repo_id
            repo = g.get_repo(repo_id)
            return repo.get_contents(self.path).name
        except:
            return ""

    def get_language(self, g):
        return "file_lang"

    def get_date_created(self, g):
        return "1/1/2014"

    def get_content(self, g):
        try:
            repo_id = self.repository.repo_id
            repo = g.get_repo(repo_id)
            content = repo.get_contents(self.path).content
            return base64.b64decode(content)
        except:
            return "-- No Content --"


class Difficulty(models.Model):
    rating = models.IntegerField()
    repository = models.ForeignKey(Repository)
    profile_user = models.ForeignKey(ProfileUser)
    date_time = models.DateTimeField(auto_now_add=True)

class Documentation(models.Model):
    rating = models.IntegerField()
    repository = models.ForeignKey(Repository)
    profile_user = models.ForeignKey(ProfileUser)
    date_time = models.DateTimeField(auto_now_add=True)

class Saved(models.Model):
    profile_user = models.ForeignKey(ProfileUser)
    repo_file = models.ForeignKey(RepoFile)
    date_time = models.DateTimeField(auto_now_add=True)
