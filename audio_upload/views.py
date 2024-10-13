from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import AudioFileForm
import speech_recognition as sr
import os

def upload_audio(request):
    if not request.session.get('usuario_autenticado'):
        login_url = reverse('login')
        return redirect(login_url)
    
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_audio = form.save()
            audio_path = uploaded_audio.audio.path

            # Transcribir el audio
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
                try:
                    extracted_text_audio = recognizer.recognize_google(audio_data)
                    request.session['extracted_text_audio'] = extracted_text_audio
                except sr.UnknownValueError:
                    request.session['extracted_text_audio'] = "No se pudo transcribir el audio."
                except sr.RequestError as e:
                    request.session['extracted_text_audio'] = f"Error en el servicio de reconocimiento: {e}"

            # Eliminar el archivo de audio después de procesarlo
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            return redirect('text_translation')  
    else:
        form = AudioFileForm()
    
    return render(request, 'upload_audio.html', {'form': form})

def upload_success(request):
    audio_extracted_text = request.session.get('audio_extracted_text', '')
    return render(request, 'audio_success.html', {'audio_extracted_text': audio_extracted_text})