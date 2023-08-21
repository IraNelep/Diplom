from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# class Blog(models.Model):
#     title = models.CharField(max_length=255, verbose_name='Название')
#     slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
#     content = models.TextField(blank=True, verbose_name='Контент')
#     photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Фото")
#     time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
#     time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
#     is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
#     # cat = models.ForeignKey('Category', on_delete=models.PROTECT)
#
#     def __str__(self):
#         return self.title
#
#     def get_absolute_url(self):
#         return reverse('post', kwargs={'post_slug': self.slug})
#
#     class Meta:  # перевод админки на русский язык
#         verbose_name = 'Выкройка'
#         verbose_name_plural = 'Выкройки'
#         ordering = ['-time_created']


# class Todo(models.Model):
#     title = models.CharField(max_length=100, verbose_name='Название выкройки')
#     created = models.DateTimeField(auto_now_add=True)
#     date_completed = models.DateTimeField(blank=True, null=True)
#     important = models.BooleanField(default=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     image = models.ImageField(blank=True, null=True, verbose_name='Изображение')
#     category = models.CharField(max_length=100, verbose_name='Категория выкройки')
#
#     def __str__(self):
#         return self.title


class Letter(models.Model):
    name = models.CharField(max_length=100, name='name')
    email = models.EmailField(max_length=100, name='email')
    text = models.TextField(max_length=400, name='text')

    def __str__(self):
        return self.text


class ProductCategory(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Категории')
    description = models.TextField(blank=True, max_length=200, verbose_name='Описание')

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    image = models.ImageField(upload_to='products_images/', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')# привязать категорию к продукту

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    add_photo = models.ImageField(upload_to='products_images/add/', blank=True, verbose_name='Фото')

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"