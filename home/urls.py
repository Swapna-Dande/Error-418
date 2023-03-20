from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.auth, name = 'auth'),
    path('register',views.register,name='register'),
    path('test',views.test,name='test'),
    path('login',views.login_user,name='login'),
    path('home',views.index,name='index'),
]
