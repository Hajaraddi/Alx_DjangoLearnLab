from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.Emailfield(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']