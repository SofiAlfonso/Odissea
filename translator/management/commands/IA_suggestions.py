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
        system_instruction="Se te entregará un idioma, seguido del signo porcentaje y texto, nuevamente un porcentaje y finalmente un segundo idioma(esto no debe ser parte de la respuesta). Redacta tres sugerencias de no más de 100 palabras cada una, estas deben servir para continuar con la conversación, para sonar como nativo o en general servir de recomendación. La sugerencias deben darse según la frase brindada y darse en el idioma original y luego traducida al segundo idioma. La estructura de las sugerencias es: tipo de sugerencia en el idioma 2(¿Para qué sirve la recomendación?) => sugerencia en idioma 1|sugerencia en idioma 2, separando cada sugerencia con una línea en blanco.",
      )

      history=[]
      chat_session = model.start_chat(
        history=history
      )

      response = chat_session.send_message(message)

      return(response.text)