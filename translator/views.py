#libraries 
from django.shortcuts import render, redirect
from googletrans import Translator, LANGUAGES
from . forms import ImageUploadForm
from . forms import FileUploadForm
from django.urls import reverse
from PIL import Image
import pytesseract
import cv2
from PIL import Image as PILImage
import os

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


def upload_image(request):
    if not request.session.get('usuario_autenticado'):
        login_url = reverse('login')
        return redirect(login_url)
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            
            uploaded_image = form.save()
            
            
            image_path = uploaded_image.image.path
            
            
            cv_image = cv2.imread(image_path)
            
            pil_image = PILImage.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
            
            extracted_text = pytesseract.image_to_string(pil_image)

            
            request.session['extracted_text'] = extracted_text
            
            uploaded_image.delete()  # elimina la instancia de la base de datos y el archivo
            if os.path.exists(image_path):
                os.remove(image_path)  #elimina el archivo de la carpeta de almacenamiento
            
            return redirect('text_translation')
    else:
        form = ImageUploadForm()

    return render(request, 'upload_image.html', {'form': form})

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

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



#Función aún no terminada para tomar fotos con la cámara
def capture_and_translate(request):
    if not request.session.get('usuario_autenticado'):
        login_url = reverse('login')
        return redirect(login_url)
    # Inicializa la cámara
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return redirect('text_translation')  

    
    ret, frame = cap.read()

    if not ret:
        print("No se pudo capturar la imagen.")
        cap.release()
        return redirect('text_translation')  

    
    image_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

     
    text = pytesseract.image_to_string(image_pil)

    
    cap.release()
    cv2.destroyAllWindows()

    
    request.session['extracted_text'] = text

    return redirect('text_translation')  