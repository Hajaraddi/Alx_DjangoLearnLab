from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Tag 

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

class PostForm(forms.ModelForm):
    # Let users enter tags as comme-separated
    tags = forms.CharField(required=False,help_text="Add tags separated by commas")
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags'] 

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            #process tags
            tags_str = self.cleaned_data['tags']
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                instance.tags.add(tag)

        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['content'] #Only the content is editable
        widgets ={
             'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'})
        }               