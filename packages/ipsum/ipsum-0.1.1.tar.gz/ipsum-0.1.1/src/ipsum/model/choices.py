import itertools
import json
import operator
import random
from typing import Any, Generic, Iterable, List, Tuple, Type, TypeVar, Union

from typing_extensions import Self

T = TypeVar("T")


class ChoicesModel(Generic[T]):
    """A statistical model for generating a list of elements chosen with replacement."""

    def __init__(self, counts_table: Iterable[Tuple[T, float]]) -> None:
        """Initializes a ChoicesModel.

        Args:
            counts_table: A list of (item, count) tuples.
        """
        # having a canonical order simplifies equality checking
        sorted_counts_table = sorted(
            counts_table, key=operator.itemgetter(1, 0), reverse=True
        )
        self._items = [item for (item, _) in sorted_counts_table]
        counts = [count for (_, count) in sorted_counts_table]
        self._cum_weights = list(itertools.accumulate(counts))

    def generate_choices(self, k: int) -> List[T]:
        """Return a k sized list of items chosen from population with replacement."""
        return random.choices(self._items, cum_weights=self._cum_weights, k=k)

    def generate_choice(self) -> T:
        """Return a single item chosen from the population."""
        return self.generate_choices(1)[0]

    def __eq__(self, other: Any) -> bool:
        """Test for equality."""
        if not isinstance(other, self.__class__):
            return False
        return self._items == other._items and self._cum_weights == other._cum_weights

    def to_json(self) -> str:
        """Return a JSON representation of the model.

        It can be persisted and then later used to reconstruct the model.

        Returns:
            A JSON string.
        """
        return json.dumps(
            {
                "items": self._items,
                "cum_weights": self._cum_weights,
            }
        )

    @classmethod
    def from_json(cls: Type[Self], json_data: Union[str, bytes, bytearray]) -> Self:
        """Return a model corresponding to the given JSON representation."""
        data = json.loads(json_data)
        model = cls([])
        model._items = data["items"]
        model._cum_weights = data["cum_weights"]
        return model
