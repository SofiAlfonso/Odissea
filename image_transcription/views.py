from django.shortcuts import render, redirect
from PIL import Image
import pytesseract
import cv2
from PIL import Image as PILImage
import os
from django.urls import reverse
from .forms import ImageUploadForm
# Create your views here.

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

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
