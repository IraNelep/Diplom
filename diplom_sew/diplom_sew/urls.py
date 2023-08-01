from django.contrib import admin
from django.urls import path
from main_project import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('signupuser/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('info/', views.info, name='info'),
    path('sews/', views.sews, name='sews'),
    path('todos/', views.todos, name='todos'),
    path('shemi_vishivki/', views.shemi_vishivki, name='shemi_vishivki'),
]
