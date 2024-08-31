from django import forms
from .models import Register, UploadedImage, UploadedFile
from django.contrib.auth.hashers import make_password

# Formulario para el registro
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register  # Modelo del cual trae los datos
        fields = [
            'name',
            'username',
            'email',
            'password',
            'origin_country',
            'origin_language'
        ]

# Formulario de Django para el login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

# Formulario para subir imágenes
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage  # Modelo del cual se sube la imagen
        fields = ('image',)  # Una tupla con un solo campo, nota la coma al final

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
