# utils/translation_utils.py
from flask import logging
from deep_translator import GoogleTranslator

translator = GoogleTranslator()

def translate_text(text, target_lang):
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        return text