from django import forms
from django.contrib.auth import get_user_model
from blog.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
