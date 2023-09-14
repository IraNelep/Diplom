from django.contrib import admin
from django.urls import path
from main_project import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('signupuser/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('message/', views.message, name='message'),
    path('sews/', views.sews, name='sews'),
    path('todos/', views.todos, name='todos'),
    path('shemi_vishivki/', views.shemi_vishivki, name='shemi_vishivki'),
    path('table_muline/', views.table_muline, name='table_muline'),
    path('table_kruch/', views.table_kruch, name='table_kruch'),
    path('shemi_vyazania/', views.shemi_vyazania, name='shemi_vyazania'),
    path('shemi_pletenia/', views.shemi_pletenia, name='shemi_pletenia'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
