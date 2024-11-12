from django.urls import path
from . import views

urlpatterns = [
    path('text-to-speech/', views.text_to_speech, name='text_to_speech'),
]