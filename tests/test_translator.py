import pytest

from subtitles_translator.available_languages import AvailableLanguages
from subtitles_translator.translator import Subtitles, Translator


@pytest.fixture
def raw_subtitles() -> list[str]:
    raw_str = """
1
00:00:00,498 --> 00:00:02,827
Hello World!
"""
    raw_subtitles = raw_str.split("\n")

    return raw_subtitles


@pytest.fixture
def subtitles(raw_subtitles) -> Subtitles:
    subtitles = Subtitles(raw_subtitles)

    return subtitles


@pytest.fixture
def translator() -> Translator:
    translator = Translator(AvailableLanguages("en"), AvailableLanguages("fr"))

    return translator


def test_translate():
    translator = Translator(source_language=AvailableLanguages("en"), target_language=AvailableLanguages("fr"))
    source_test = "Hello World!"
    translated_test = translator.translate(source_test)
    assert translated_test == "Bonjour le monde!"


def test_translate_subtitles(translator, subtitles):
    translator.translate_subtitles(subtitles)
    assert subtitles.full_text_lines[3] == "Bonjour le monde!"
