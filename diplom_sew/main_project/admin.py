from django.contrib import admin
from django.contrib import admin
from django import forms
from .models import *
from django import forms
from django.utils.safestring import mark_safe
# from ckeditor_uploader.widgets import CKEditorUploadingWidget





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




admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(Photo, PhotoAdmin)

