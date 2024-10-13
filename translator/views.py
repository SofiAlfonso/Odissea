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
    extracted_text_image = request.session.get('extracted_text', '')
    extracted_text_audio = request.session.get('extracted_text_audio', '')

    if not request.session.get('usuario_autenticado'):
        login_url = reverse('login')
        return redirect(login_url)

    src = request.session['user_src']
    dest = request.GET.get('destination_language')
    text = request.GET.get('inputText')
    cambio = request.GET.get('cambio_lengua')

    if dest is None:
        dest = "en"

    if cambio == "intercambiar":
        dest, src = src, dest
        request.session['user_src'] = src

    # Elegir el texto a traducir
    if extracted_text_audio:
        totext = translate(src, dest, extracted_text_audio)
    elif extracted_text_image:
        totext = translate(src, dest, extracted_text_image)
    elif text:
        totext = translate(src, dest, text)

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
        'ldest': LANGUAGES[dest.lower()]
    })


def make_examples(dest, text):
    dest= LANGUAGES[dest.lower()]
    query= f"{dest}%{text}"
    print(query)
    Command.handle(query,Command.handle)




#Aun no está en funcionamiento
def upload_file(request):
    if not request.session.get('usuario_autenticado'):
        login_url = reverse('login')
        return redirect(login_url)
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')  
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})





  