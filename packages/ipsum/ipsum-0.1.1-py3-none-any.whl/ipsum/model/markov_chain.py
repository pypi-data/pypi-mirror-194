from collections import defaultdict
from itertools import accumulate
import random
from typing import cast, Dict, Generic, List, Sequence, TypeVar, Union

from ipsum.exceptions import ModelAlreadyFinalizedError
from ipsum.exceptions import ModelNotFinalizedError

START = "__START__"
END = "__END__"
FILL = "__FILL__"

T = TypeVar("T")
U = Union[T, str]


class MarkovChain(Generic[T]):
    """A Markov chain model."""

    def __init__(self) -> None:
        """Initialize Markov chain."""
        self._transitions: Dict[U, Dict[U, int]] = defaultdict(
            lambda: defaultdict(lambda: 0)
        )
        self._destinations: Dict[U, List[U]] = dict()
        self._cum_weights: Dict[U, List[int]] = dict()

        self.finalized = False

    def generate_sequence(self) -> List[T]:
        """Randomly generates a sequence.

        The sequence is generated according to the transition probabilities of
        the underlying Markov chain.

        Returns:
            A list representing a full run of the Markov model.

        Raises:
            ModelNotFinalizedError: If the model is not finalized.
        """
        if not self.finalized:
            raise ModelNotFinalizedError

        state = START
        run = []
        while state != END:
            population = self._destinations[state]
            cum_weights = self._cum_weights[state]
            next_state = random.choices(population, cum_weights=cum_weights)[0]

            if next_state != END:
                run.append(next_state)
            state = next_state

        return cast(List[T], run)

    def train(self, examples: Sequence[Sequence[T]]) -> None:
        """Trains the model on the given data.

        Args:
            examples: Each element of examples represents one sequence.

        Raises:
            ModelAlreadyFinalizedError: If the model is already finalized.
        """
        if self.finalized:
            raise ModelAlreadyFinalizedError

        for run in examples:
            self._train_from_example(run)

    def _train_from_example(self, example: Sequence[U]) -> None:
        prev_state: U = START
        for state in example:
            self._transitions[prev_state][state] += 1
            prev_state = state
        self._transitions[prev_state][END] += 1

    def finalize(self) -> None:
        """Finalizes the model.

        After finalizing, the model can no longer be trained on any additional
        data, but it is placed in a state from which it ican be used to generate
        new sequences.
        """
        if self.finalized:
            return

        for start_state, counts in self._transitions.items():
            self._destinations[start_state] = list(counts.keys())
            self._cum_weights[start_state] = list(accumulate(counts.values()))
        self.finalized = True


class MarkovChainWithMemory(MarkovChain, Generic[T]):
    """A Markov chain model with memory (i.e. a Markov model of higher order)."""

    def __init__(self, order: int) -> None:
        """Initialize Markov chain.

        Args:
            order: A positive integer representing the order of the Markov chain, i.e.
                the number of past states that a future state depends on.

        Raises:
            ValueError: If order is not a positive integer.
        """
        if not isinstance(order, int) or order < 1:
            raise ValueError("Order must be a positive integer.")
        self._order = order
        super().__init__()

    def train(self, examples: Sequence[Sequence[T]]) -> None:
        """Trains the model on the given data.

        Args:
            examples: Each element of examples represents one sequence.

        Raises:
            ModelAlreadyFinalizedError: If the model is already finalized.
        """
        if self.finalized:
            raise ModelAlreadyFinalizedError

        for run in examples:
            states = [
                tuple(run[i : i + self._order])
                for i in range(0, max(len(run) - self._order, 0) + 1)
            ]
            self._train_from_example(states)

    def generate_sequence(self) -> List[T]:
        """Randomly generates a sequence.

        The sequence is generated according to the transition probabilities of
        the underlying Markov chain.

        Returns:
            A list representing a full run of the Markov model.

        Raises:
            ModelNotFinalizedError: If the model is not finalized.
        """
        if not self.finalized:
            raise ModelNotFinalizedError

        sequence = super().generate_sequence()
        if len(sequence) > 1:
            return list(sequence[0]) + [state[-1] for state in sequence[1:]]
        return []
