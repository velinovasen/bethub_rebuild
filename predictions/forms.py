from django import forms
from django.forms import ModelForm

from .models import *


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32,
                                       widget=forms.PasswordInput
                                       )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
