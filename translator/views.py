#Login and register libraries 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import RegisterForm, LoginForm
from . forms import ImageUploadForm
from . forms import FileUploadForm
from .models import Register
from django.urls import reverse
from translator import text_translate as tt


# Create your views here.

#Vista de la página principal
def home(request):
    totext=""

    #Get into home
    if not request.session.get('usuario_autenticado'): #Recuperación de dato sobre el inicio de sesión de un usuario
        login_url=reverse('login') # Acceso al login url
        return redirect(login_url) # redireccionando al login
    
    #Translate
    
    src= request.session['user_src']
    dest= request.GET.get('destination_language')
    text= request.GET.get('inputText')
    print(dest)
    print(src)
    print(text)
    if text: 
        totext= tt.translate(src, dest, text)
    else:
        text=""
    return render(request, 'home.html',{'totext':totext,'text':text,'src':tt.LANGUAGES[src.lower()],'dest':tt.LANGUAGES.items()})

#vista de la página de registro
def register(request):
    if request.method=='POST':

        #Obtención de los datos en el formulario
        form= RegisterForm(request.POST)
        if form.is_valid():
            print("enviados")
            #Almacenamiento en la base de datos  
            form.save()
            #Permiso para ingresar a home (login automático)
            request.session['usuario_autenticado'] = True 
            origin_country = form.cleaned_data.get('origin_country')
            request.session['user_src']= origin_country
            return redirect('home')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error en {field}: {error}")
            form.add_error(None, "Nombre de usuario ocupado")
    else:
        form=RegisterForm()
    return render(request, 'register.html', {'form':form})

#vie para el login
def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #tomando los datos del inicio de sesion (formulario por defecto de django)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            print(f"Attempting login with username: {username}")
            print({password})

            # Verificar si existe un usuario con el nombre de usuario proporcionado
            try:
                user = Register.objects.get(username=username)
               
                # Comparar la contraseña del formulario con la de la base de datos (contra sin encriptación)
                if user.password==password:
                    # Autenticación exitosa
                    request.session['usuario_autenticado'] = True 
                    request.session['usuar_id'] = user.id #id del usuario en la sesión
                    request.session['user_src']= user.origin_language
                    return redirect('home')
                else:
                    #contrseña incorrecta
                    form.add_error(None, "Información inválida")
            except Register.DoesNotExist:
                # Usuario no encontrado
                form.add_error(None, "Información inválida")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

#Vista para cerra sesión
def logout_view(request):
    # Eliminar las variables de sesión relacionadas con la autenticación
    try:
        del request.session['usuario_autenticado']
        del request.session['user_id']
        del request.session['user_src']
    except KeyError:
        pass

    # Redirigir al usuario a la página de inicio de sesión o cualquier otra página
    return redirect('login')

from django.shortcuts import render, redirect
from .forms import ImageUploadForm

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_upload')  # Redirige después de guardar para evitar que el formulario se vuelva a enviar si se recarga la página.
    else:
        # Si es una solicitud GET, muestra un formulario vacío
        form = ImageUploadForm()

    # Asegúrate de que el contexto sea un diccionario, no un conjunto
    context = {'form': form}
    return render(request, 'upload.html', context)



def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirige a una página de éxito
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
