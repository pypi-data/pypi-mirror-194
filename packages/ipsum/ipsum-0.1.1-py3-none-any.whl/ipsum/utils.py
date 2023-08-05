from typing import Generator, Iterable, List, Literal, Sequence, Sized, TypeVar

T = TypeVar("T")


def is_lower(s: str) -> bool:
    """Returns True if all alphabet characters are in lowercase."""
    return s.islower()


def is_capitalized(s: str) -> bool:
    # noqa: DAR101, DAR201
    """Returns True if the first alphabet character is uppercase.

    If the string does not contain any alphabet characters it returns False.
    """
    for char in s:
        if char.isalpha() and char.isupper():
            return True
        if char.isalpha() and char.islower():
            return False
    return False


def is_word(s: str) -> bool:
    """Returns True if the string contains an alphabet character."""
    return any(c.isalpha() for c in s)


def capitalize_sentence(sentence: str) -> str:
    """Returns sentence with the first alphabet character capitalized."""
    for i in range(0, len(sentence)):
        if sentence[i].isalpha():
            return sentence[:i] + sentence[i:].capitalize()
    return sentence


LastChunkMethods = Literal["drop", "incomplete"]


def iterate_over_chunks(
    sequence: Sequence[T],
    chunk_size: int,
    last_chunk_method: LastChunkMethods = "drop",
) -> Generator[Sequence[T], None, None]:
    """Iterate over slices of a fixed size of a sequence.

    Args:
        sequence: The sequence of item to split into chunks.
        chunk_size: The target size for each individual chunk.
        last_chunk_method: What to do with the final chunk if len(sequence) is
            not a multiple of chunk_size: "incomplete" yields the partially filled
            final chunk, "drop" silently drops it.

    Yields:
        A subsequence of size no more than chunk_size.
    """
    n = len(sequence)
    for chunk in (sequence[i : i + chunk_size] for i in range(0, n, chunk_size)):
        if len(chunk) == chunk_size:
            yield chunk
        elif len(chunk) > 0 and last_chunk_method == "incomplete":
            yield chunk


def compute_length_weights(
    population: Iterable[Sized], weights: Iterable[float]
) -> List[float]:
    """Returns a list where each entry is the total weight of items of index size."""
    max_len = max(len(item) for item in population)
    length_weights = [0.0] * (max_len + 1)

    for item, weight in zip(population, weights):
        length_weights[len(item)] += weight

    return length_weights


def reweight_by_length(
    population: List[str],
    population_weights: Sequence[float],
    length_weights: Sequence[float],
) -> List[float]:
    """Reweights weights so that total weight by length matches length_weights."""
    max_population_length = max(len(item) for item in population)

    arr_length = max(max_population_length + 1, len(length_weights))
    pop_weights_by_length = [0.0] * arr_length

    length_weights = list(length_weights)
    length_weights.extend(0 for _ in range(arr_length - len(length_weights)))

    for item, weight in zip(population, population_weights):
        pop_weights_by_length[len(item)] += weight

    return [
        round(
            weight * length_weights[len(item)] / pop_weights_by_length[len(item)],
            4,
        )
        for item, weight in zip(population, population_weights)
    ]
