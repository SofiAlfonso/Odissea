from django.shortcuts import render, redirect
from django.http import HttpResponse
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import io
from django.urls import reverse
from .management.commands.IA_examples import Command as Commandexamples
from .management.commands.IA_suggestions import Command as Commandsuggestions

# Función de traducción
def translate(src, dest, text):
    translator = Translator()
    translation = translator.translate(text, dest=dest, src=src)
    return translation.text

# Vista principal de traducción y generación de audio
def text_translation(request):
    totext = ""
    examples_response = None
    show_modal = False
    show_modal2 = False
    sugerencias_response = None
    error= False

    # Redirigir a login si no ha iniciado sesión
    if not request.session.get('usuario_autenticado'):
        login_url = reverse('login')
        return redirect(login_url)

    extracted_text_image = request.session.get('extracted_text', '')
    extracted_text_audio = request.session.get('extracted_text_audio', '')
    src = request.session.get('user_src', 'en')  # Lengua de origen por defecto
    dest = request.GET.get('destination_language', 'es')  # Lengua de destino por defecto
    text = request.GET.get('inputText', '')  # Texto de entrada
    cambio = request.GET.get('cambio_lengua')  # Intercambiar idioma
    examples = request.GET.get('examples')  # Dar ejemplos
    sugerencia= request.GET.get('sugerencias')  # Dar sugerencias

    # Generar ejemplos si se ha solicitado
    if examples == "examples" and text:
        examples_response = make_examples(dest, text, LANGUAGES[src.lower()]).split('\n')
        show_modal = True

    # Generar sugerencias si se ha solicitado
    if sugerencia == "sugerencias" and text:
        sugerencias_response = make_sugerencias(dest, text, LANGUAGES[src.lower()]).split('\n')
        show_modal2 = True


    # Intercambiar lenguaje
    if cambio == "intercambiar":
        dest, src = src, dest
        request.session['user_src'] = src

    # Traducir el texto
    if text:
        try: 
            totext = translate(src, dest, text)
        except:
            error= True

    # Limpiar las sesiones de texto extraído
    if 'extracted_text' in request.session:
        del request.session['extracted_text']
    if 'extracted_text_audio' in request.session:
        del request.session['extracted_text_audio']

    # Guardar el texto traducido en la sesión para usarlo en el audio
    request.session['translated_text'] = totext


    return render(request, 'text_translation.html', {
        'totext': totext,
        'text': extracted_text_image or extracted_text_audio or text,
        'src': LANGUAGES[src.lower()],
        'dest': LANGUAGES.items(),
        'examples_response': examples_response,
        'show_modal': show_modal,
        'last_language': dest,
        'show_modal2': show_modal2,
        'sugerencias_response': sugerencias_response,
        'error': error
    })

# Función para generar ejemplos
def make_examples(dest, text, src):
    dest = LANGUAGES[dest.lower()]
    query = f"{dest}%{text}%{src}"
    print(query)
    return Commandexamples.handle(query, Commandexamples.handle)

# Función para generar sugerencias
def make_sugerencias(dest, text, src):
    dest = LANGUAGES[dest.lower()]
    query = f"{dest}%{text}%{src}"
    print(query)
    return Commandsuggestions.handle(query, Commandsuggestions.handle)

