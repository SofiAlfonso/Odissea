
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_audio, name='upload_audio'),
    path('success/', views.upload_success, name='audio_success'),
<<<<<<< HEAD
=======
    
>>>>>>> redireccion
]

