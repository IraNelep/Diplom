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
    path('create_project/', views.create_project, name='create_project'),
    path('create_article/', views.create_article, name='create_article'),
    path('create_vyaz/', views.create_vyaz, name='create_vyaz'),
    path('shemi_vishivki/', views.shemi_vishivki, name='shemi_vishivki'),
    path('table_muline/', views.table_muline, name='table_muline'),
    path('table_kruch/', views.table_kruch, name='table_kruch'),
    path('shemi_vyazania/', views.shemi_vyazania, name='shemi_vyazania'),
    path('article/', views.article, name='article'),
    path('project/<str:pk>/', views.project, name='project'),
    path('single_article/<str:pk>/', views.single_article, name='single_article'),
    path('single_vyaz/<str:pk>/', views.single_vyaz, name='single_vyaz'),
    # path('verify/<str:email>/<uuid:code>/', views.EmailVerificationView.as_view(), name='email_verification'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
