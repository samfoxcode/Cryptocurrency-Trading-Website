from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register')
]