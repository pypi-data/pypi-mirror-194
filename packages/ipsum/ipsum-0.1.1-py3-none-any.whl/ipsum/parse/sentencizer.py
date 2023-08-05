import re
from typing import Iterable, List


class Sentencizer:
    """Used to split a text into sentences based on detecting line endings."""

    def __init__(
        self,
        word_chars: str,
        internal_punctuation: Iterable[str],
        endings: Iterable[str],
    ) -> None:
        """Initialize the sentencizer.

        Args:
            word_chars: Valid word characters.
            internal_punctuation: Valid internal punctuation.
            endings: Terminal punctuation. Put multi-character punctuation such
                as ?! first, since endings are matched in the order that they
                are given in.
        """
        self.pattern = f"({'|'.join((re.escape(x) for x in endings))})"

    def __call__(self, text: str) -> List[str]:
        """Apply the sentencizer to a text.

        Args:
            text: The text to process.

        Returns:
            A list of sentences.
        """
        split = re.split(self.pattern, text)[:-1]
        result = [
            (sentence + ending).strip()
            for (sentence, ending) in zip(split[::2], split[1::2])
        ]
        return result
