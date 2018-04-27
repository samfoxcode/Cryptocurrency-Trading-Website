from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from home import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('index_search/', views.index_search, name='index_search'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('signin/', views.signin, name='signin'),
    path('login/',views.login_view,name = 'login'),
    path('logout/',views.logout_view,name = 'logout'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('contact_em/', views.contact_em, name='contact_em')
    
]
