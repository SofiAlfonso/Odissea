from django import forms
from .models import AudioFile  

class AudioFileForm(forms.ModelForm):
    language_choices = [
        ('es', 'Español'),
        ('en', 'Inglés'),
        ('fr', 'Francés'),
     
    ]
    language = forms.ChoiceField(choices=language_choices, label="Selecciona el idioma")

    class Meta:
        model = AudioFile 
        fields = ['audio', 'language']  

