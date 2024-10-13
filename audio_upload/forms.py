from django import forms
from .models import AudioFile

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
<<<<<<< HEAD
        fields = ['title', 'audio']
=======
        fields = [ 'audio']
>>>>>>> redireccion
