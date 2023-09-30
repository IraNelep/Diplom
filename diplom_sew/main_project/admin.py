from django.contrib import admin
from .models import *
from django import forms
from django.utils.safestring import mark_safe

class PhotoAdd(admin.StackedInline):
    model = Photo
    fields = ('product', 'add_photo')
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoAdd]
    list_display = ['id', 'name', 'category']
    list_display_links = ['id', 'name']


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('product', 'add_photo')


admin.site.register(Article)
admin.site.register(Message)
admin.site.register(Vyazanie)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(Photo, PhotoAdmin)


admin.site.site_header = 'Админ-панель блога'
admin.site.site_title = 'Админ-панель блога'