from django import forms
from .models import AudioFile  # Importa tu modelo real

class AudioFileForm(forms.ModelForm):
    language_choices = [
        ('es', 'Español'),
        ('en', 'Inglés'),
        ('fr', 'Francés'),
        # Agrega más idiomas según sea necesario
    ]
    language = forms.ChoiceField(choices=language_choices, label="Selecciona el idioma")

    class Meta:
        model = AudioFile  # Reemplaza con tu modelo real
        fields = ['audio', 'language']  # Asegúrate de incluir el campo 'language'

