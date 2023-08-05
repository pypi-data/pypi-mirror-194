import re
from typing import List


class Worderizer:
    """Used to extract from a text all words (concurrent runs of valid characters)."""

    def __init__(self, word_chars: str) -> None:
        """Initialize the worderizer.

        Args:
            word_chars: All valid word characters in target language.
        """
        word_char = f"[{re.escape(word_chars)}]"
        non_word_char = f"[^{re.escape(word_chars)}]"

        self._re = re.compile(
            f"(?:^|{non_word_char})({word_char}+)(?=$|{non_word_char})"
        )

    def __call__(self, text: str) -> List[str]:
        """Apply the worderizer to a text.

        Args:
            text: The text to process.

        Returns:
            A list of words.
        """
        return self._re.findall(text)
