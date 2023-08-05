from typing import Iterable, List, Optional, Set, Tuple

from ipsum.parse.sentencizer import Sentencizer
from ipsum.parse.skeletonizer import Skeletonizer
from ipsum.parse.standardizer import Standardizer
from ipsum.parse.worderizer import Worderizer
from ipsum.utils import is_capitalized, is_lower


class Parser:
    """Provides a unified interface to various language parsing tasks."""

    def __init__(
        self,
        word_chars: str,
        internal_punctuation: Iterable[str],
        endings: Iterable[str],
        starting_punctuation: Optional[Iterable[str]] = None,
        matched_punctuation: Optional[Iterable[Tuple[str, str]]] = None,
        stop_words: Optional[Iterable[str]] = None,
        *,
        additional_substitutions: Optional[Iterable[Tuple[str, str]]] = None,
    ) -> None:
        """Initialize the parser.

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
            stop_words: Unimportant words that should be treated like punctuation.
            additional_substitutions: Additional language-specific substitutions.
                An iterable of (pattern, replacement) tuples.
        """
        self._standardizer = Standardizer(additional_substitutions)
        self._word_extractor = Worderizer(word_chars)
        self._sentence_extractor = Sentencizer(
            word_chars, internal_punctuation, endings
        )
        self._sentence_tokenizer = Skeletonizer(
            word_chars,
            internal_punctuation,
            endings,
            starting_punctuation,
            matched_punctuation,
        )

        self.stop_words: Set[str] = set()
        if stop_words is not None:
            self.stop_words = set(word.lower() for word in stop_words)

    def extract_words(self, text: str) -> List[str]:
        """Return a list of all valid words in document with repetition."""
        return self._word_extractor(text)

    def extract_sentences(self, text: str) -> List[str]:
        """Return a list of all valid sentences in the text."""
        return self._sentence_extractor(text)

    def extract_skeletons(
        self,
        text: str,
        lowercase_words: Set[str],
        capitalized_words: Set[str],
    ) -> List[List[str]]:
        """Returns all valid sentence skeletons in a corpus (with duplicates)."""
        sentences = self.extract_sentences(text)

        skeletons = []
        for sentence in sentences:
            try:
                skeleton = self._sentence_tokenizer(
                    sentence, lowercase_words, capitalized_words, self.stop_words
                )
                skeletons.append(skeleton)
            except ValueError:
                pass

        return skeletons

    def standardize(self, text: str) -> str:
        """Returns a standardized copy of the given text."""
        return self._standardizer(text)

    def get_words(self, texts: Iterable[str]) -> List[str]:
        """Returns all words extracted from standardized texts (with duplicates)."""
        words = []
        for text in texts:
            standardized_text = self.standardize(text)
            words.extend(self.extract_words(standardized_text))

        return words

    # FIXME: Rename
    def get_word_counts(self, texts: Iterable[str]) -> Tuple[List[str], List[str]]:
        """Returns all non-stop lowercase and uppercase words (with duplicates)."""
        words = self.get_words(texts)
        unique_words = set(words)

        lowercase_words: List[str] = []
        capitalized_words: List[str] = []
        for word in words:
            if word in self.stop_words or word.lower() in self.stop_words:
                continue
            elif is_capitalized(word) and word.lower() in unique_words:
                lowercase_words.append(word.lower())
            elif is_capitalized(word):
                capitalized_words.append(word)
            elif is_lower(word):
                lowercase_words.append(word)

        return lowercase_words, capitalized_words

    def get_sentences(self, texts: Iterable[str]) -> List[str]:
        """Returns all sentence candidates in the texts after standardization."""
        sentences = []
        for text in texts:
            standardized_text = self.standardize(text)
            sentences.extend(self.extract_sentences(standardized_text))
        return sentences

    def get_skeletons(
        self,
        texts: Iterable[str],
        lowercase_words: Set[str],
        capitalized_words: Set[str],
    ) -> List[List[str]]:
        """Returns all valid sentence skeletons from the standardized texts."""
        skeletons = []
        for text in texts:
            standardized_text = self.standardize(text)
            skeletons += self.extract_skeletons(
                standardized_text, lowercase_words, capitalized_words
            )
        return skeletons
