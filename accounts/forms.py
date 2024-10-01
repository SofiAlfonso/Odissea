from django import forms
from translator.models import Register

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