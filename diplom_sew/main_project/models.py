from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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