
from deep_translator import GoogleTranslator

def translate_text(text, language):

    try:
        translated = GoogleTranslator(
            source='auto',
            target=language.lower()
        ).translate(text)

        return translated

    except:
        return "Translation unavailable."
