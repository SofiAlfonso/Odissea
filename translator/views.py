from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import RegisterForm, LoginForm
from .models import Register
from django.urls import reverse


# Create your views here.
def home(request):
    if not request.session.get('usuario_autenticado'):
        login_url=reverse('login')
        return redirect(login_url)
    return render(request, 'home.html')

def register(request):
    if request.method=='POST':
        form= RegisterForm(request.POST)
        if form.is_valid():  
            form.save()
            request.session['usuario_autenticado'] = True
            return redirect('home')
        else:
          print("Form errors:", form.errors)  
    else:
        form=RegisterForm()
    return render(request, 'register.html', {'form':form} )

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            print(f"Attempting login with username: {username}")
            print({password})

            # Verificar si existe un usuario con el nombre de usuario proporcionado
            try:
                user = Register.objects.get(username=username)
                print(user.password)
                print(user.username)

                print(user.password)
                # Comparar la contraseña del formulario con la de la base de datos
                if user.password==password:
                    # Autenticación exitosa
                    request.session['usuario_autenticado'] = True
                    request.session['user_id'] = user.id
                    return redirect('home')
                else:
                    form.add_error(None,"")
            except Register.DoesNotExist:
                # Usuario no encontrado
                form.add_error(None,"")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    # Eliminar las variables de sesión relacionadas con la autenticación
    try:
        del request.session['usuario_autenticado']
        del request.session['usuario_id']
    except KeyError:
        pass

    # Redirigir al usuario a la página de inicio de sesión o cualquier otra página
    return redirect('login')