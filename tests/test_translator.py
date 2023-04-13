from subtitles_translator.available_languages import AvailableLanguages
from subtitles_translator.translator import Translator


def test_translate():
    translator = Translator(source_language=AvailableLanguages("en"), target_language=AvailableLanguages("fr"))
    source_test = "Hello World!"
    translated_test = translator.translate(source_test)
    assert translated_test == "Bonjour le monde!"
