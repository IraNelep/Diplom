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


# class BlogCategory(ListView):
#     model = Todo
#     template_name = 'main_project/home.html'
#     context_object_name = 'posts'
#     allow_empty = False
#
#     def get_queryset(self):
#         return Blog.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
    #     # context['cat_selected'] = context['posts'][0].cat_id
    #     # context['menu'] = menu
    #     c = Category.objects.get(slug=self.kwargs['cat_slug'])
    #     c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
    #     return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(FormView):
    form_class = ContactForms
    template_name = 'main_project/info.html'
    success_url = reverse_lazy('home')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title='Обратная связь')
    #     return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # доп функционал
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
    context = {
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'main_project/home.html', context)


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
    return render(request, 'main_project/sews.html', context) #, {'sews': sews}


@login_required
def todos(request):
    # context = {
    #     'categories': ProductCategory.objects.all(),
    #     'products': Product.objects.all(),
    # }
    # todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'main_project/sews.html', context)  #, {'todos': todos}


def shemi_vishivki(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'main_project/shemi_vishivki.html', context)


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
