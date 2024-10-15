from django.core.management.base import BaseCommand
import os
import google.generativeai as genai
from dotenv import load_dotenv



class Command(BaseCommand):
    help = 'Create examples for translated text'

    def handle(message, self,  *args, **kwargs):
      load_dotenv('api_key.env')
      api_key = os.getenv('GEMMINI_API_KEY')

      if api_key is None:
          print("Error: No se encontró la clave API en las variables de entorno")
          return

        # Configurar la API de Gemini con la clave
      genai.configure(api_key=api_key)

      # Create the model
      generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
      }

      model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
        system_instruction="Se te entregará el nombre de un idioma seguido del signo porcentaje y una oración, luego nuevamente el porcentaje y un segundo idioma. Crea tres ejemplos coherentes y concisos en el primer idioma dado, usando esa palabra u oración, asegurate de que cada ejemplo no sea unicamente la palabra u oración brindada. Cada ejemplo debe tener un máximo de 30 palabras y ser traducido al idioma original (Segundo idioma dado). Separa cada ejemplo de su traducción con | y deja una línea en blanco entre cada ejemplo.",
      )

      history=[]
      chat_session = model.start_chat(
        history=history
      )

      response = chat_session.send_message(message)

      return(response.text)