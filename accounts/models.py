from django.db import models
from googletrans import LANGUAGES

# Create your models here.

# Opciones de país
class CountryChoices(models.TextChoices):
    COLOMBIA = 'CO', 'Colombia'
    PANAMA = 'PA', 'Panamá'
    MEXICO = 'MX', 'México'
    USA = 'US', 'Estados Unidos'
    CANADA = 'CA', 'Canadá'

class LanguageChoices(models.TextChoices):
   
   @classmethod
   def get_choices(cls):
       return[(key, value) for key, value in LANGUAGES.items()]
      
#Modelo de registro (tabala en la base de datos)
class Register (models.Model):
    name = models.CharField (max_length=100)
    email= models.EmailField()
    username= models.CharField(max_length=100, unique=True)
    password= models.CharField(max_length=128)
    origin_country= models.CharField(max_length=2, choices=CountryChoices.choices, default=CountryChoices.COLOMBIA)
    origin_language=models.CharField(max_length=5,choices=LanguageChoices.get_choices(), default='en' )

    def __str__(self):
        return self.username