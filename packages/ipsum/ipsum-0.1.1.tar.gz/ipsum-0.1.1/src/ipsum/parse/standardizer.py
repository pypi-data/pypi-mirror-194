import re
from typing import Iterable, Optional, Tuple


class Standardizer:
    """Used to standardize text by doing regex substitutions.

    First applies a collection of default base substitutions, and then any
    additional language-specific substitutions.
    """

    _base_substitutions = [
        (r"\r", ""),  # strip carriage returns
        (r"(\w)[-–]\n(\w)", r"\1\2"),  # dehyphenate
        (r"\s+", " "),  # strip extraneous whitespace
        (r"\.{2,}", "…"),  # use ellipsis instead of repeated periods
        (r"\s+[-–—]\s+", r"—"),  # replace spaced dashes with em dashes
        (
            r"\s+([,:;.…])",
            r"\1",
        ),  # remove space before certain punctuation
        (
            r"(\w)([,:;.…])(\w)",
            r"\1\2 \3",
        ),  # put 1 space after certain punctuation
    ]

    def __init__(
        self, additional_substitutions: Optional[Iterable[Tuple[str, str]]] = None
    ) -> None:
        """Initialize the standardizer.

        Args:
            additional_substitutions: Additional language-specific substitutions.
                An iterable of (pattern, replacement) tuples.
        """
        self._additional_substitutions = []
        if additional_substitutions is not None:
            self._additional_substitutions = list(additional_substitutions)

    def __call__(self, text: str) -> str:
        """Apply the standardizer to a text.

        Args:
            text: The text to process.

        Returns:
            The text after applying all the substitutions.
        """
        for pattern, repl in self._base_substitutions:
            text = re.sub(pattern, repl, text)

        for pattern, repl in self._additional_substitutions:
            text = re.sub(pattern, repl, text)

        return text
