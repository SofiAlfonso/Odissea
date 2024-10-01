#libraries 
from django.shortcuts import render, redirect
from googletrans import Translator, LANGUAGES
from . forms import FileUploadForm
from django.urls import reverse


# Functions
def translate(src, dest, text):
    translator= Translator()
    translation= translator.translate(text, dest=dest, src=src)
    return translation.text 

#Vista de la página principal
def text_translation(request):

    totext = ""
    extracted_text = request.session.get('extracted_text', '')

    if not request.session.get('usuario_autenticado'):
        login_url = reverse('login')
        return redirect(login_url)

    src = request.session['user_src']
    dest = request.GET.get('destination_language')
    text = request.GET.get('inputText')
    cambio= request.GET.get('cambio_lengua')
    
    print(f"Valor de cambio_lengua: {cambio}")
    
    
    if dest==None:
        dest="en"

    if cambio== "intercambiar":
        dest, src= src, dest
        request.session['user_src'] = src
        print("cambio")
    if text:
        totext = translate(src, dest, text)
    else:
        text = ""

    if 'extracted_text' in request.session:
        del request.session['extracted_text']

    return render(request, 'text_translation.html', {
        'totext': totext,
        'text': extracted_text or text,
        'src': LANGUAGES[src.lower()],
        'dest': LANGUAGES.items(),
        'ldest':LANGUAGES[dest.lower()]
    })




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





  