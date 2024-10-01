from django.urls import path
from translator import views as translator_views

urlpatterns = [
    path('text_translation/', translator_views.text_translation, name='text_translation'),
]