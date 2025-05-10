from googletrans import Translator
import logging

def translate_text(text: str, target_lang: str = 'am'):
    """
    Translates text to the target language (default: Amharic).
    Returns a dictionary with original and translated text.
    """
    try:
        translator = Translator()
        # Convert 'am' to 'amharic' as googletrans uses full language names
        target = 'amharic' if target_lang == 'am' else target_lang
        translated = translator.translate(text, dest=target)
        if not translated or not translated.text:
            raise ValueError("Translation returned empty result")
        return {"original": text, "translated": translated.text}
    except Exception as e:
        logging.error(f"Translation error: {str(e)}")
        # Return None instead of silently falling back to original text
        return None
