"""This module contains all classes and methods used for parsing text."""

from typing import Union

from ipsum.parse.language.bg import bg_parser
from ipsum.parse.language.de import de_parser
from ipsum.parse.language.el import el_parser
from ipsum.parse.language.en import en_parser
from ipsum.parse.language.es import es_parser
from ipsum.parse.language.fr import fr_parser
from ipsum.parse.language.it import it_parser
from ipsum.parse.language.mk import mk_parser
from ipsum.parse.language.nl import nl_parser
from ipsum.parse.language.sq import sq_parser
from ipsum.parse.language.sr import sr_parser
from ipsum.parse.language.sv import sv_parser
from ipsum.parse.parser import Parser
from ipsum.supported_languages import SupportedLanguage

__all__ = ["Parser", "load_parser"]


def load_parser(language: Union[str, SupportedLanguage]) -> Parser:
    """Return parser for given language.

    Args:
        language: The full English name of the language (e.g."Macedonian"), the
            ISO 639-1 code of the language (e.g. "mk"), or a SupportedLanguage
            instance (e.g. SupportedLanguage.Macedonian).

    Returns:
        Target language parser.

    Raises:
        ValueError: If it cannot match the requested language.
    """
    for candidate_language in SupportedLanguage:
        if (
            language == candidate_language
            or language.lower() == candidate_language.name.lower()
            or language.lower() == candidate_language.value.lower()
        ):
            language_code = candidate_language.value
            break
    else:
        raise ValueError(f"{language} is not a supported language.")

    parsers = {
        "bg": bg_parser,
        "de": de_parser,
        "el": el_parser,
        "en": en_parser,
        "es": es_parser,
        "fr": fr_parser,
        "it": it_parser,
        "mk": mk_parser,
        "nl": nl_parser,
        "sq": sq_parser,
        "sr": sr_parser,
        "sv": sv_parser,
    }
    return parsers[language_code]
