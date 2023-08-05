import re
from typing import Iterable, List, Optional, Set, Tuple

from ipsum.utils import is_capitalized, is_word

CAPITALIZED_WORD = "__CAP_WRD__"
LOWERCASE_WORD = "__LC_WRD__"


class Skeletonizer:
    """Used to extract sentence skeleton from a sentence."""

    def __init__(
        self,
        word_chars: str,
        internal_punctuation: Iterable[str],
        endings: Iterable[str],
        starting_punctuation: Optional[Iterable[str]] = None,
        matched_punctuation: Optional[Iterable[Tuple[str, str]]] = None,
    ) -> None:
        """Initialize the skeletonizer.

        Args:
            word_chars: Valid word characters.
            internal_punctuation: Valid internal punctuation.
            endings: Terminal punctuation. Put multi-character punctuation such
                as ?! first, since endings are matched in the order that they
                are given in.
            starting_punctuation: Punctuation marks that can be used to start a
                sentence, e.g. ¿ and ¡ in Spanish.
            matched_punctuation: Punctuation marks that always occur in matched
                pairs, e.g. ( and ).
        """
        self._internal_punctuation = internal_punctuation
        self._endings = set(endings)
        self._starting_punctuation = set(starting_punctuation or ())
        self._matched_punctuation = dict(matched_punctuation or ())

        splitters = set().union(
            [" "],
            internal_punctuation,
            endings,
            self._starting_punctuation,
            self._matched_punctuation.keys(),
            self._matched_punctuation.values(),
        )

        self._split_at = re.compile(f"({'|'.join(re.escape(c) for c in splitters)})")

    def __call__(
        self,
        sentence: str,
        lowercase_words: Set[str],
        capitalized_words: Set[str],
        stop_words: Set[str],
    ) -> List[str]:
        """Attempts to produce a skeleton corresponding to the given sentence.

        Args:
            sentence: The sentence to process.
            lowercase_words: Words in the language that are usually written lowercase.
            capitalized_words: Words in the langauge are are always capitalized.
            stop_words: Words that should be treated like punctuation, i.e.
                preserved as they are instead of replacing with a token.

        Returns:
            The skeleton of the given sentence or None.

        Raises:
            ValueError: Sentence is not valid.
        """
        tokens = re.split(self._split_at, sentence)
        valid_tokens = [token for token in tokens if token != ""]  # noqa: S105

        left_matched_punctuation = set(self._matched_punctuation.keys())
        right_matched_punctuation = set(self._matched_punctuation.values())

        result = []
        matched_stack: List[str] = []
        prev_token = None
        for idx, token in enumerate(valid_tokens):
            if idx == 0 and token in self._starting_punctuation:
                result.append(token)
            elif idx == 0 or (idx == 1 and prev_token in self._starting_punctuation):
                if not is_word(token) or not is_capitalized(token):
                    raise ValueError("First word in sentence must be capitalized.")
                elif token.lower() in stop_words:
                    result.append(token)
                elif token.lower() in lowercase_words:
                    result.append(LOWERCASE_WORD)
                elif token in capitalized_words:
                    result.append(CAPITALIZED_WORD)
            elif idx == len(valid_tokens) - 1:
                if token in self._endings:
                    result.append(token)
                else:
                    raise ValueError(f"Invalid sentence ending: {token}")
            elif token.lower() in stop_words:
                result.append(token)
            elif token.lower() in lowercase_words:
                result.append(LOWERCASE_WORD)
            elif token in capitalized_words:
                result.append(CAPITALIZED_WORD)
            elif (
                token in right_matched_punctuation
                and len(matched_stack) > 0
                and matched_stack[-1] == token
            ):
                matched_stack.pop()
                result.append(token)
            elif token in left_matched_punctuation:
                matched_stack.append(self._matched_punctuation[token])
                result.append(token)
            elif token in self._internal_punctuation:
                result.append(token)
            elif token == " ":
                result.append(" ")

            else:
                raise ValueError(f"Invalid token: {token}")
            prev_token = token

        if len(matched_stack) > 0:
            raise ValueError(f"Failed to match tokens: {''.join(matched_stack)}")
        return result
