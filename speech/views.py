from django.http import HttpResponse
from gtts import gTTS
import io

# Vista para convertir texto a voz
def text_to_speech(request):
    text = request.GET.get('text', '')
    language = request.GET.get('language', 'en')

    if not text:
        return HttpResponse(status=400, content="Text is required")

    # Generar el audio usando gTTS
    tts = gTTS(text=text, lang=language)
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)

    # Asegurarse de que el puntero del archivo esté al principio
    audio_file.seek(0)

    # Responder con el archivo de audio en formato MP3
    response = HttpResponse(audio_file.read(), content_type='audio/mpeg')
    response['Content-Disposition'] = 'inline; filename="audio.mp3"'  # Inline para reproducción directa

    return response
