from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.models import AbstractUser



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class ProductCategory(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Категории')
    description = models.TextField(blank=True, max_length=200, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    image = models.ImageField(upload_to='products_images/', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 verbose_name='Категория')  # привязать категорию к продукту

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Схемы вышивки"
        verbose_name_plural = "Схемы вышивки"

class Vyazanie(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    image = models.ImageField(upload_to='products_images/', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 verbose_name='Категория')  # привязать категорию к продукту

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Схемы вязания"
        verbose_name_plural = "Схемы вязания"


class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    add_photo = models.ImageField(upload_to='products_images/add/', blank=True, verbose_name='Фото')

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Article(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    # image = models.ImageField(upload_to='products_images1/', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 verbose_name='Категория')  # привязать категорию к продукту

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статьи"
        verbose_name_plural = "Статьи"

class Message(models.Model):
    name = models.CharField(max_length=256, blank=True, verbose_name='Имя')
    email = models.EmailField(max_length=256, blank=True, verbose_name='Email')
    body = models.TextField(blank=True, verbose_name='Текст')
    created = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return self.body
    class Meta:
     verbose_name = 'Отзыв'
     verbose_name_plural = 'Отзывы'

  #   name = models.CharField(max_length=256, verbose_name='Название')
  # #  project = models.ForeignKey(Product, on_delete=models.CASCADE)
  #   body = models.TextField(verbose_name='Текст сообщения')
  #   created = models.DateTimeField(auto_now_add=True)
  #
  #   def __str__(self):
  #       return self.created
  #

