from googletrans import Translator

def translate(src, dest, text):
    translator= Translator()
    translation= translator.translate(text, dest=dest, src=src)
    return translation.text 



