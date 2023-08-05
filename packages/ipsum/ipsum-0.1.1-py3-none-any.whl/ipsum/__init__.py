"""Library for procedurally-generating text that resembles a particular language."""
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


from ipsum.model import LanguageModel
from ipsum.model import load_all_models
from ipsum.model import load_model
from ipsum.supported_languages import SupportedLanguage

__all__ = ["LanguageModel", "load_all_models", "load_model", "SupportedLanguage"]
