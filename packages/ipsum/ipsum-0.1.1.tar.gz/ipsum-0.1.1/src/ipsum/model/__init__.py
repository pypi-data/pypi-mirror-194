"""This module contains all the probabilistic models used in Ipsum."""

import os
from typing import Dict, Union

from ipsum.model.language import LanguageModel
from ipsum.supported_languages import SupportedLanguage

__all__ = ["LanguageModel", "load_all_models", "load_model"]


def load_all_models() -> Dict[SupportedLanguage, LanguageModel]:
    """Load all models from disk into a dictionary of models."""
    result = {language: load_model(language) for language in SupportedLanguage}
    return result


def load_model(language: Union[str, SupportedLanguage]) -> LanguageModel:
    """Load from disk and return requested language model.

    Args:
        language: The full English name of the language (e.g."Macedonian"), the
            ISO 639-1 code of the language (e.g. "mk"), or a SupportedLanguage
            instance (e.g. SupportedLanguage.Macedonian).

    Returns:
        Target language model.

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

    models_dir_path = _get_models_dir_path()
    model_path = os.path.join(models_dir_path, f"{language_code}.zip")
    language_model = LanguageModel.load_model(model_path)

    return language_model


def _get_models_dir_path() -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    models_dir_path = os.path.join(dir_path, "..", "trained_models")
    return models_dir_path
