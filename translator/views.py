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

    #Devuelve al login si no se ha iniciado sesión
    if not request.session.get('usuario_autenticado'):
        login_url = reverse('login')
        return redirect(login_url)
    
    extracted_text = request.session.get('extracted_text', '') #Texto escaneado
    src = request.session['user_src'] #Lengua de origen
    dest = request.GET.get('destination_language') # Lengua de destino
    text = request.GET.get('inputText') #Texto de entrada
    cambio= request.GET.get('cambio_lengua') #Intercambiar idioma
    examples= request.GET.get('examples') # Dar ejemplos
    
    #Dar ejemplos
    if (examples=="examples") and text :
        examples_response= make_examples(dest, text).split('\n')
    
    # Lenguaje de destino por defecto
    if dest==None:
        dest="en"

    # Intercambiar lenguaje
    if cambio== "intercambiar":
        dest, src= src, dest
        request.session['user_src'] = src
        print("cambio")
    
    # Traducir
    if text:
        totext = translate(src, dest, text)
    else:
        text = ""

    # Traducir imagen escaneada
    if 'extracted_text' in request.session:
        del request.session['extracted_text']

    return render(request, 'text_translation.html', {
        'totext': totext,
        'text': extracted_text or text,
        'src': LANGUAGES[src.lower()],
        'dest': LANGUAGES.items(),
        'ldest':LANGUAGES[dest.lower()],
        'examples_response':examples_response
    })

def make_examples(dest, text):
    dest= LANGUAGES[dest.lower()]
    query= f"{dest}%{text}"
    print(query)
    return Command.handle(query,Command.handle)


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





  