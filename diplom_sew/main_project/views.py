from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from .models import Product, ProductCategory
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import *
from django.urls import reverse_lazy  # как редирект в функциях
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def form_valid(self, form):  # доп функционал
    form = ContactForms()
    print(form.cleaned_data)
    subject = 'Message'
    context = {
        'name': form.cleaned_data['name'],
        'email': form.cleaned_data['email'],
        'content': form.cleaned_data['content'],
    }
    message = '\n'.join(context.values())
    try:
        send_mail(
            subject,
            message,
            form.cleaned_data['email'],
            ['admin@localhost']
        )
    except BadHeaderError:
        return HttpResponse('Найден некорректный заголовок')
    return redirect('index', context)


def home(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'main_project/home.html', context)


def message(request):
    recipient = 'iranelep@gmail.com'
    form = MessageForm()

    try:
        sender = request.user.profile  # пользователь существует
    except:
        sender = None  # пользователя  нет

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:  # автоматический ввод имени и емейла если пользователь существует
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully send!')
            return redirect('message', pk=recipient)

    context = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'main_project/message.html', context)


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'main_project/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'main_project/signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'Такое имя пользователя уже существует. Задайте другое имя.'})
        else:
            return render(request, 'main_project/signupuser.html',
                          {'form': UserCreationForm(),
                           'error': 'Пароли не совпадают.'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'main_project/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'main_project/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Неверные данные для входа'})
        else:
            login(request, user)
            return redirect('home')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def sews(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all(),
    }
    # sews = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'main_project/sews.html', context)  # , {'sews': sews}


@login_required
def todos(request):
    # context = {
    #     'categories': ProductCategory.objects.all(),
    #     'products': Product.objects.all(),
    # }
    # todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'main_project/sews.html', context)  # , {'todos': todos}


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


def shemi_pletenia(request):
    return render(request, 'main_project/shemi_pletenia.html')


def shemi_vyazania(request):
    return render(request, 'main_project/shemi_vyazania.html')


def table_kruch(request):
    return render(request, 'main_project/table_kruch.html')


@login_required
def sews(request):
    if request.method == 'GET':
        return render(request, 'main_project/sews.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)  # все данные попадут в переменную пост
            new_todo = form.save(commit=False)
            new_todo.user = request.user  # models.py/class Todo/user
            new_todo.save()
            return redirect('sews')
        except ValueError:
            return render(request, 'main_project/sews.html', {
                'form': TodoForm(),
                'error': 'Неверные данные. Попробуйте еще раз.'
            })
