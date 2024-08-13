from django import forms
from . models import Register

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
