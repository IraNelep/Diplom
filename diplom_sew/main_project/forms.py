from django import forms
from .models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import uuid
from datetime import timedelta
from django.utils.timezone import now


class ProjectForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'category']


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'description', 'category']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'body']


class VyazanieForm(ModelForm):
    class Meta:
        model = Vyazanie
        fields = ['name', 'image', 'description', 'category']

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    email = forms.CharField(label='Email', widget=forms.EmailInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

