#libraries 
from django.shortcuts import render, redirect
from googletrans import Translator, LANGUAGES
from . forms import FileUploadForm
from django.urls import reverse
from .management.commands.IA_examples import Command

# Functions
def translate(src, dest, text):
    translator= Translator()
    translation= translator.translate(text, dest=dest, src=src)
    return translation.text 

#Vista de la página principal
def text_translation(request):
    totext = ""
    examples_response= None
    show_modal = False
    extracted_text_image = request.session.get('extracted_text', '')
    extracted_text_audio = request.session.get('extracted_text_audio', '')

    #Devuelve al login si no se ha iniciado sesión
    if not request.session.get('usuario_autenticado'):
        login_url = reverse('login')
        return redirect(login_url)
    
    src = request.session['user_src'] #Lengua de origen
    dest = request.GET.get('destination_language') # Lengua de destino
    text = request.GET.get('inputText') #Texto de entrada
    cambio= request.GET.get('cambio_lengua') #Intercambiar idioma
    examples= request.GET.get('examples') # Dar ejemplos
    
    #Dar ejemplos
    if (examples=="examples") and text :
        examples_response= make_examples(dest, text, LANGUAGES[src.lower()]).split('\n')
        show_modal = True
    
    # Lenguaje de destino por defecto
    if dest:
        request.session['user_dest'] = dest  # Guardar nueva lengua de destino en la sesión
    else:
        dest = request.session.get('user_dest', 'en') 

    # Intercambiar lenguaje
    if cambio== "intercambiar":
        dest, src= src, dest
        request.session['user_src'] = src
        print("cambio")
    
    # Traducir
    src = request.session['user_src']
    dest = request.GET.get('destination_language')
    text = request.GET.get('inputText')
    cambio = request.GET.get('cambio_lengua')
    if text:
        totext = translate(src, dest, text)
    else:
        text = ""


    # Limpiar las sesiones de texto extraído
    if 'extracted_text' in request.session:
        del request.session['extracted_text']
    if 'extracted_text_audio' in request.session:
        del request.session['extracted_text_audio']

    return render(request, 'text_translation.html', {
        'totext': totext,
        'text': extracted_text_image or extracted_text_audio or text,
        'src': LANGUAGES[src.lower()],
        'dest': LANGUAGES.items(),
        'examples_response':examples_response,
        'show_modal': show_modal,
        'last_language':dest,

    })


def make_examples(dest, text, src):
    dest= LANGUAGES[dest.lower()]
    query= f"{dest}%{text}%{src}"
    print(query)
    return Command.handle(query,Command.handle)








  