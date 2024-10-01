from django.contrib import admin
from django.urls import path

from accounts import views as account_views

urlpatterns = [
    path('register/', account_views.register, name='register'),
    path('', account_views.custom_login, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
]