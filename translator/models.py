from django.db import models

# Create your models here.

#Modelo para el registro de usuarios
class CountryChoices(models.TextChoices):
    COLOMBIA = 'CO', 'Colombia'
    PANAMA = 'PA', 'Panamá'
    MEXICO = 'MX', 'México'
    USA = 'US', 'Estados Unidos'
    CANADA = 'CA', 'Canadá'

class LanguageChoices(models.TextChoices):
    EPAÑOL= 'ES', 'Español'
    INGLES= 'EN', 'Inglés'
    FRANCES= 'FR', 'Frances'


class Register (models.Model):
    name = models.CharField (max_length=100,help_text= "Ingrese su nombre completo")
    email= models.EmailField(help_text="Ingrese su correo electrónico")
    username= models.CharField(max_length=150, unique=True,help_text="Ingrese un nombre de usuario", primary_key=True)
    password= models.CharField(max_length=128, help_text="Ingrese su contraseña")
    origin_country= models.CharField(max_length=2, choices=CountryChoices.choices, default=CountryChoices.COLOMBIA)
    origin_language=models.CharField(max_length=2,choices=LanguageChoices.choices,default=LanguageChoices.INGLES )
