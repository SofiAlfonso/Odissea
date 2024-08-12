from django.db import models

# Create your models here.

#Modelo para el registro de usuarios

class Register (models.Model):
    name = models.CharField (max_length=100,help_text= "Ingrese su nombre completo")
    email= models.EmailField(help_text="Ingrese su correo electrónico")
    username= models.CharField(max_length=150, unique=True,help_text="Ingrese un nombre de usuario", primary_key=True)
    password= models.CharField(max_length=128, help_text="Ingrese su contraseña")
    origin_country= models.TextChoices("Colombia", "Panamá", "México", "Estados Unidos","Canadá")
    origin_language= models.TextChoices("Español", "Inglés", "Fránces")