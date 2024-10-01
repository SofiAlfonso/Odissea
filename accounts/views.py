from django.shortcuts import render, redirect
from translator.forms import RegisterForm, LoginForm
from translator.models import Register

# Create your views here.
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

#view para el login
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

#Vista para cerrar sesión
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
