from django import forms
from models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('profile_user', 'path', 'likers', 'date_time')
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leave a Comment'})
        }

class SearchForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Search'}))
    types = forms.ChoiceField(choices=(('Lang', 'Languages'),('Repo','Repository'),('User','User'),('Code','Code')))
