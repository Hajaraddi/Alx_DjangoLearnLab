from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content'] 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['content'] #Only the content is editable
        widgets ={
             'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'})
        }               