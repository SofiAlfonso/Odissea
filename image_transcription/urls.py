from django.urls import path
from image_transcription import views as image_transcription_views

urlpatterns = [
    path('upload_images/', image_transcription_views.upload_image, name='upload_image'),
    path('capture_and_translate/', image_transcription_views.capture_and_translate, name='capture_and_translate'),
]