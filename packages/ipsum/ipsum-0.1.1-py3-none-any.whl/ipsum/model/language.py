import collections
import json
import random
from typing import (
    Any,
    cast,
    Counter,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    Union,
)
import zipfile

from typing_extensions import Self

from ipsum.corpus import Corpus
from ipsum.exceptions import ModelAlreadyFinalizedError
from ipsum.exceptions import ModelNotFinalizedError
from ipsum.model.choices import ChoicesModel
from ipsum.model.markov_chain import MarkovChainWithMemory
from ipsum.parse.parser import Parser
from ipsum.parse.skeletonizer import CAPITALIZED_WORD
from ipsum.parse.skeletonizer import LOWERCASE_WORD
from ipsum.utils import capitalize_sentence, compute_length_weights
from ipsum.utils import is_word
from ipsum.utils import reweight_by_length


class LanguageModel:
    """A statistical model for generating text that resembles a language."""

    def __init__(
        self,
        *,
        order: int = 2,
        max_skeletons: int = 200,
        vocabulary_size: int = 4_000,
        max_word_length: int = 17,
        min_sentence_length: int = 20,
    ) -> None:
        """Initialize a new language model.

        Note that a LanguageModel has to be trained by calling self.train()
        before it can be used to generate any data.

        Args:
            order: Size of the chunks that words from the corpus get divided
                into when training the Markov chains.
            max_skeletons: The number of different sentence skeletons to learn.
            vocabulary_size: The total number of distinct words, capitalized or
                lowercase, but not including stop words for the model to generate.
            max_word_length: Maximum character length of generated words.
            min_sentence_length: Minimum number of tokens in sentences.
        """
        self._order = order
        self._sentence_model: Optional[ChoicesModel[List[str]]] = None
        self._lowercase_model: Optional[ChoicesModel[str]] = None
        self._capitalized_model: Optional[ChoicesModel[str]] = None
        self._max_skeletons = max_skeletons
        self._vocabulary_size = vocabulary_size
        self._max_word_length = max_word_length
        self._min_sentence_length = min_sentence_length
        self._trained = False

    def train(
        self,
        lowercase_words: Sequence[str],
        capitalized_words: Sequence[str],
        stop_words: Iterable[str],
        skeletons: List[List[str]],
    ) -> None:
        """Trains a language model on the given data.

        After training, the model can no longer be given any additional examples,
        but it is in a state in which it can be used to generate new data.

        Args:
            lowercase_words: Collection of words used to train the Markov chain
                that handles the LowercaseWord token.
            capitalized_words: Words to train the CapitalizedWord token Markov chain.
            stop_words: Collection of words that are treated as punctuation by model.
            skeletons: Sentence skeleton examples used to train the sentence model.

        Raises:
            ModelAlreadyFinalizedError: If the model has already been trained.
        """
        if self._trained:
            raise ModelAlreadyFinalizedError

        self._train_word_models(lowercase_words, capitalized_words, set(stop_words))
        self._train_sentence_model(skeletons)
        self._trained = True

    def _train_word_models(
        self,
        lowercase_words: Sequence[str],
        capitalized_words: Sequence[str],
        stop_words: Set[str],
    ) -> None:
        total_word_count = len(lowercase_words) + len(capitalized_words)

        capitalized_ratio = len(capitalized_words) / total_word_count
        capitalized_vocab_size = int(capitalized_ratio * self._vocabulary_size)
        lowercase_vocab_size = self._vocabulary_size - capitalized_vocab_size

        avoid_words = set(
            word
            for word in set().union(lowercase_words, capitalized_words)
            if len(word) > self._order
        ).union(stop_words)

        self._capitalized_model = self._generate_vocabulary(
            capitalized_words, avoid_words, stop_words, capitalized_vocab_size
        )

        self._lowercase_model = self._generate_vocabulary(
            lowercase_words, avoid_words, stop_words, lowercase_vocab_size
        )

    def _generate_vocabulary(
        self,
        words: Sequence[str],
        avoid_words: Set[str],
        stop_words: Set[str],
        size: int,
    ) -> ChoicesModel[str]:
        chain: MarkovChainWithMemory[str] = MarkovChainWithMemory(self._order)
        chain.train(words)
        chain.finalize()

        generated_word_counter: Counter[str] = collections.Counter()
        while True:
            generated_words = [
                "".join(chain.generate_sequence()) for _ in range(15 * size)
            ]
            valid_words = [
                word
                for word in generated_words
                if word not in avoid_words
                and word.lower() not in avoid_words
                and len(word) <= self._max_word_length
            ]
            generated_word_counter += collections.Counter(valid_words)
            if len(generated_word_counter.keys()) > size:
                break

        # Adjust word frequency by word length to better match corpus.
        generated_word_count_tuples = generated_word_counter.most_common(size)
        generated_words = [word for word, _ in generated_word_count_tuples]
        generated_weights = [weight for _, weight in generated_word_count_tuples]

        observed_word_count_tuples = collections.Counter(
            word
            for word in words
            if len(word) <= self._max_word_length
            and word not in stop_words
            and word.lower() not in stop_words
        ).most_common()
        observed_words = [word for word, _ in observed_word_count_tuples]
        observed_weights = [weight for _, weight in observed_word_count_tuples]

        length_weights = compute_length_weights(observed_words, observed_weights)
        new_weights = reweight_by_length(
            generated_words, generated_weights, length_weights
        )
        model = ChoicesModel(zip(generated_words, new_weights))

        return model

    def _train_sentence_model(self, skeletons: List[List[str]]) -> None:
        skeleton_tuples = [tuple(skeleton) for skeleton in skeletons]
        skeleton_counter = collections.Counter(skeleton_tuples)

        good_skeletons_counter = collections.Counter(
            {
                skeleton: count
                for (skeleton, count) in skeleton_counter.items()
                if len(skeleton) >= self._min_sentence_length
            }
        )
        top_tuple_skeletons = good_skeletons_counter.most_common(self._max_skeletons)
        top_skeletons = [(list(s), count) for (s, count) in top_tuple_skeletons]
        self._sentence_model = ChoicesModel(top_skeletons)

    def generate_words(self, num_of_words: int) -> List[str]:
        """Return randomly generated words."""
        if not self._trained:
            raise ModelNotFinalizedError
        sentence_model = cast(ChoicesModel[List[str]], self._sentence_model)

        result: List[str] = []
        while len(result) < num_of_words:
            skeleton = sentence_model.generate_choice()
            words = [self._handle_token(token) for token in skeleton if is_word(token)]
            result.extend(words)
        return result[:num_of_words]

    def generate_sentences(self, num_of_sentences: int) -> List[str]:
        """Return randomly generated sentences."""
        if not self._trained:
            raise ModelNotFinalizedError

        sentence_model = cast(ChoicesModel[List[str]], self._sentence_model)
        skeletons = sentence_model.generate_choices(num_of_sentences)
        sentences = [self._fill_skeleton(skeleton) for skeleton in skeletons]
        return sentences

    def generate_paragraphs(self, num_of_paragraphs: int) -> List[str]:
        """Return randomly generated paragraphs."""
        if not self._trained:
            raise ModelNotFinalizedError

        return [self._generate_paragraph() for _ in range(num_of_paragraphs)]

    def _generate_paragraph(self) -> str:
        # corresponds to weights of [3, 4, 5, 5, 6, 5, 5, 4, 3]
        sentence_count = random.choices(
            [2, 3, 4, 5, 6, 7, 8, 9, 10],
            cum_weights=[3, 7, 12, 17, 23, 28, 33, 37, 40],
            k=1,
        )[0]

        sentences = self.generate_sentences(sentence_count)
        return " ".join(sentences)

    def _fill_skeleton(self, skeleton: List[str]) -> str:
        sentence = "".join(self._handle_token(token) for token in skeleton)
        return capitalize_sentence(sentence)

    def _handle_token(self, token: str) -> str:
        # if _handle_token was invoked, we assume caller checked model was trained
        capitalized_model = cast(ChoicesModel[str], self._capitalized_model)
        lowercase_model = cast(ChoicesModel[str], self._lowercase_model)

        if token == CAPITALIZED_WORD:
            return capitalized_model.generate_choice()
        elif token == LOWERCASE_WORD:
            return lowercase_model.generate_choice()
        else:
            return token

    @classmethod
    def from_corpus(cls: Type[Self], parser: Parser, corpus: Corpus) -> Self:
        """Returns a LanguageModel trained from a corpus given a parser."""
        model = cls()

        lowercase_words, capitalized_words = parser.get_word_counts(corpus)

        skeletons = parser.get_skeletons(
            corpus, set(lowercase_words), set(capitalized_words)
        )

        model.train(lowercase_words, capitalized_words, parser.stop_words, skeletons)
        return model

    def to_json(self) -> str:
        """Return a JSON representation of the model.

        It can be persisted and then later used to reconstruct the model.

        Returns:
            A JSON string.
        """
        data: Any = {
            "order": self._order,
            "trained": self._trained,
            "max_skeletons": self._max_skeletons,
            "vocabulary_size": self._vocabulary_size,
            "max_word_length": self._max_word_length,
            "min_sentence_length": self._min_sentence_length,
            "sentence_model": None,
            "lowercase_model": None,
            "capitalized_model": None,
        }

        # we have to check each individually to satisfy the type checker
        if self._sentence_model is not None:
            data["sentence_model"] = self._sentence_model.to_json()

        if self._lowercase_model is not None:
            data["lowercase_model"] = self._lowercase_model.to_json()

        if self._capitalized_model is not None:
            data["capitalized_model"] = self._capitalized_model.to_json()

        return json.dumps(data)

    def save_model(self, file_path: str) -> None:
        """Save a LanguageModel to disk."""
        json_data = self.to_json()
        with zipfile.ZipFile(file_path, "w") as zip:
            zip.writestr("model", json_data, zipfile.ZIP_LZMA)

    @classmethod
    def load_model(cls: Type[Self], file_path: str) -> Self:
        """Load a LanguageModel from disk."""
        with zipfile.ZipFile(file_path, "r") as zip:
            content = zip.read("model").decode("utf-8")
        return cls.from_json(content)

    @classmethod
    def from_json(cls: Type[Self], json_data: Union[str, bytes, bytearray]) -> Self:
        """Return a model corresponding to the given JSON representation."""
        data = json.loads(json_data)
        model = cls(
            order=data["order"],
            max_skeletons=data["max_skeletons"],
            vocabulary_size=data["vocabulary_size"],
            max_word_length=data["max_word_length"],
            min_sentence_length=data["min_sentence_length"],
        )
        model._trained = data["trained"]

        if model._trained:
            model._sentence_model = ChoicesModel.from_json(data["sentence_model"])
            model._lowercase_model = ChoicesModel.from_json(data["lowercase_model"])
            model._capitalized_model = ChoicesModel.from_json(data["capitalized_model"])

        return model
