import asyncio
from googletrans import Translator

translator = Translator()

async def translate_text_async(text, dest_lang='en'):
    """
    Translate text to destination language asynchronously.
    """
    try:
        translated = await translator.translate(text, dest=dest_lang)
        return translated.text
    except Exception as e:
        return f"Translation error: {e}"

def translate_text(text, dest_lang='en'):
    """
    Synchronous wrapper for translation.
    """
    return asyncio.run(translate_text_async(text, dest_lang))

def detect_language(text):
    """
    Detect the language of the text.
    """
    try:
        detected = translator.detect(text)
        return detected.lang
    except Exception as e:
        return f"Detection error: {e}"
