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
from django.urls import reverse_lazy # как редирект в функциях
# from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


# menu = [
#     {'title': 'Схемы вышивки', 'url_name': 'shemi_vishivki'},
#     {'title': 'Схемы вязания', 'url_name': 'index'},
#     {'title': 'Схемы плетения', 'url_name': 'index'},
#     {'title': 'Книги', 'url_name': 'index'},
#     {'title': 'Журналы', 'url_name': 'index'},
#     {'title': 'Статьи', 'url_name': 'index'},
#     {'title': 'Таблицы', 'url_name': 'index'},
#     {'title': 'Калькуляторы', 'url_name': 'index'},
#
# ]

class ContactFormView(FormView):
    form_class = ContactForms
    template_name = 'main_project/info.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form): # доп функционал
        print(form.cleaned_data)
        subject = 'Message'
        body = {
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'content': form.cleaned_data['content'],
        }
        message = '\n'.join(body.values())
        try:
            send_mail(
                subject,
                message,
                form.cleaned_data['email'],
                ['admin@localhost']
            )
        except BadHeaderError:
            return HttpResponse('Найден некорректный заголовок')
        return redirect('index')


def home(request):
    return render(request, 'main_project/home.html')


def info(request):
    return render(request, 'main_project/info.html')


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
            return render(request, 'main_project/loginuser.html', {'form': AuthenticationForm(), 'error': 'Неверные данные для входа'})
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
    sews = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'main_project/sews.html', {'sews': sews})


@login_required
def todos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'main_project/todos.html', {'todos': todos})



def shemi_vishivki(request):
    return render(request, 'main_project/shemi_vishivki.html')