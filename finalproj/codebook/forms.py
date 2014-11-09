from django import forms
from models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('profile_user', 'path', 'likers', 'date_time')
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comment on this Repository'})
        }