from django import forms
from . models import Register
from django.contrib.auth.hashers import make_password

class RegisterForm(forms.ModelForm):
    class Meta:
        model= Register
        fields=[
            'name',
            'username',
            'email',
            'password',
            'origin_country',
            'origin_language'

        ]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

