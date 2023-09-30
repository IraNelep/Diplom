from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from django.contrib import auth, messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.base import TemplateView
from .models import *


def home(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'main_project/home.html', context)

def message(request):
    mess = Message.objects.all()
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('message')

    context = {'form': form,
               'mess': mess}
    return render(request, 'main_project/message.html', context)# '

def signupuser(request):
    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            subject = 'Ура! Ваш аккаунт создан!'
            message = username + '! Добро пожаловать на наш сайт! Ведите себя прилично.'
            print(form.cleaned_data)
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
            except BadHeaderError:
                return HttpResponse('Обнаружен неверный заголовок')


            messages.success(request, "Вы успешно зарегистрировались!")
            form.save()
            return redirect('loginuser')
    else:
        form = RegisterUserForm()
    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'main_project/signupuser.html', context)


def loginuser(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'main_project/loginuser.html', context)


@login_required(login_url='loginuser')
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')


def shemi_vishivki(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    prof = Product.objects.filter(name__icontains=search_query)
    page = request.GET.get('page')
    results = 2
    paginator = Paginator(prof, results)

    try:
        prof = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        prof = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        prof = paginator.page(page)

    context = {
        'categories': ProductCategory.objects.all(),
        'products': prof,
        'search_query': search_query,
        'paginator': paginator,

    }
    return render(request, 'main_project/shemi_vishivki.html', context)


def table_muline(request):
    return render(request, 'main_project/table_muline.html')


def article(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    arts = Article.objects.filter(name__icontains=search_query)
    page = request.GET.get('page')
    results = 2
    paginator = Paginator(arts, results)

    try:
        arts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        arts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        arts = paginator.page(page)

    context = {
        'arts': arts,
        'search_query': search_query,
        'paginator': paginator,

    }
    return render(request, 'main_project/article.html', context)


def shemi_vyazania(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    vyaz = Vyazanie.objects.filter(name__icontains=search_query)
    page = request.GET.get('page')
    results = 2
    paginator = Paginator(vyaz, results)

    try:
        vyaz = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        vyaz = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        vyaz = paginator.page(page)

    context = {
        'categories': ProductCategory.objects.all(),
        'vyazanie': vyaz,
        'search_query': search_query,
        'paginator': paginator,

    }
    return render(request, 'main_project/shemi_vyazania.html', context)


def table_kruch(request):
    return render(request, 'main_project/table_kruch.html')


@login_required(login_url='loginuser')
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shemi_vishivki')

    context = {'form': form}
    return render(request, 'main_project/create_project.html', context)


@login_required(login_url='loginuser')
def create_vyaz(request):
    form = VyazanieForm()
    if request.method == 'POST':
        form = VyazanieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shemi_vyazania')

    context = {'form': form}
    return render(request, 'main_project/create_vyaz.html', context)


@login_required(login_url='loginuser')
def create_article(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('article')

    context = {'form': form}
    return render(request, 'main_project/create_article.html', context)


def project(request, pk):
    project_obj = Product.objects.get(id=pk)
    return render(request, 'main_project/single_project.html', {'project': project_obj})


def single_article(request, pk):
    art = Article.objects.get(id=pk)
    return render(request, 'main_project/single_article.html', {'art': art})


def single_vyaz(request, pk):
    vyaz = Vyazanie.objects.get(id=pk)
    return render(request, 'main_project/single_vyaz.html', {'vyaz': vyaz})


