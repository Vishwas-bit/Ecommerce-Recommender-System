from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django import forms

from . import models


# class UserAdminCreationForm(UserCreationForm):
#     """
#     A Custom form for creating new users.
#     """
#
#     class Meta:
#         model = get_user_model()
#         fields = ['email']


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'first_name', 'last_name', 'phone', 'profile_pic', 'DOB']

class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'phone', 'profile_pic', 'DOB']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


def CreateUserForm():
    return None