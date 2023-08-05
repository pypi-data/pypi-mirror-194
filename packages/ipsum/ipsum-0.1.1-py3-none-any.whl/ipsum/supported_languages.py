from enum import Enum


class SupportedLanguage(str, Enum):
    """Language codes of languages currently supported by Ipsum."""

    Albanian = "sq"
    Bulgarian = "bg"
    Dutch = "nl"
    English = "en"
    French = "fr"
    German = "de"
    Greek = "el"
    Italian = "it"
    Macedonian = "mk"
    Serbian = "sr"
    Spanish = "es"
    Swedish = "sv"
