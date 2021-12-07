from django import forms
from .models import *
from django.contrib.auth.models import User


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('topic', 'name', 'description')


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password', 'confirm_password')
