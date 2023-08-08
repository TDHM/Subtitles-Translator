from __future__ import annotations

from enum import Enum


class AvailableLanguages(Enum):
    """Ensure type safety by providing a representation of supported languages.
    These language codes are used to import opus-mt model finetuned by Helsinki University.
    See full list of available languages/models here: https://huggingface.co/Helsinki-NLP

    """

    english = "en"
    french = "fr"
    spanish = "es"
    german = "de"
    russian = "ru"
    arabic = "ar"
    hindi = "hi"
    italian = "it"
    chinese = "zh"
    dutch = "nl"
