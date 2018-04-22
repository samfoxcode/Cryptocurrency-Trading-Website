from django.contrib import admin
from django.urls import path, include
from account import views

urlpatterns = [
    path('account/', views.account, name='account'),
    path('signedinhome/', views.signedinhome, name='signedinhome'),
    path('', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('logout/',views.logout_view,name = 'logout'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell'),
    path('load_info/', views.load_info, name='load_info')
]