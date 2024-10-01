from django import forms
from .models import UploadedImage, UploadedFile


# Formulario para subir imágenes
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage  # Modelo del cual se sube la imagen
        fields = ('image',)  # Una tupla con un solo campo

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']


