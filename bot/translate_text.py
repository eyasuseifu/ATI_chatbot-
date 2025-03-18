# bot/translate_text.py
from deep_translator import GoogleTranslator
import logging

def translate_text(text: str, target_lang: str = 'am'):
    """
    Translates text to the target language (default: Amharic).
    """
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        return text  # Return the original text if translation fails