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


class UserPredictionForm(forms.Form):
    game_id = forms.CharField(max_length=100)
    home_team = forms.CharField(max_length=70)
    away_team = forms.CharField(max_length=70)
    sign = forms.CharField(max_length=10)
    odd = forms.CharField(max_length=10)
    thoughts = forms.CharField(widget=forms.Textarea())
