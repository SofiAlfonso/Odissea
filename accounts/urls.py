from django.contrib import admin
from django.urls import path

import translator.views as translator_views
from translator.views import *

urlpatterns = [
    path('register/', translator_views.register, name='register'),
    path('', translator_views.custom_login, name='login'),
    path('logout/', translator_views.logout_view, name='logout'),
]