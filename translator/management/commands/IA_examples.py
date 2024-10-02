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
        system_instruction="Tono relajado y fácil de comprehender, conciso, no hagas preguntas, ni saludes, ni te despidas. Debes contestar tres ejemplos cada uno de no más de 100 palabras, que se encuentren separados, la respuesta debe darse en el idioma que te pida y, luego, separada, la misma respuesta traducida en el que esté escrito el texto y sobre la aplicación de la palabra u oración que te entrege. El idioma estará en minuscula, separado con un signo de porcentaje del texto sobre el cual darás los ejemplos. Los ejemplos no deben tener ninguna explicación adicional.\n",
      )

      history=[]
      chat_session = model.start_chat(
        history=history
      )

      response = chat_session.send_message(message)

      print(response.text)