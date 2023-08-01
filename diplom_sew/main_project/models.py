from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Фото")
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta: # перевод админки на русский язык
        verbose_name = 'Выкройка'
        verbose_name_plural = 'Выкройки'
        ordering = ['-time_created']


class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Letter(models.Model):
    name = models.CharField(max_length=100, name='name')
    email = models.EmailField(max_length=100, name='email')
    text = models.TextField(max_length=400, name='text')

    def __str__(self):
        return self.text
