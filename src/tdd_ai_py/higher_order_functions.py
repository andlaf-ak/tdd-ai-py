"""Higher-order functions for functional transformations."""

from functools import reduce
from typing import BinaryIO, Callable, Dict, Iterable, List, TypeVar

from .stream_utils import iter_bytes

T = TypeVar("T")
U = TypeVar("U")


def fold_left(
    func: Callable[[T, U], T], initial: T, iterable: Iterable[U]
) -> T:
    """Left fold (reduce) operation.

    Args:
        func: Binary function to apply
        initial: Initial accumulator value
        iterable: Sequence to fold over

    Returns:
        Final accumulated value
    """
    return reduce(func, iterable, initial)


def map_transform(func: Callable[[T], U], iterable: Iterable[T]) -> List[U]:
    """Transform each element using the given function.

    Args:
        func: Transformation function
        iterable: Sequence to transform

    Returns:
        List of transformed elements
    """
    return list(map(func, iterable))


def filter_transform(
    predicate: Callable[[T], bool], iterable: Iterable[T]
) -> List[T]:
    """Filter elements using the given predicate.

    Args:
        predicate: Filter function
        iterable: Sequence to filter

    Returns:
        List of filtered elements
    """
    return list(filter(predicate, iterable))


def create_frequency_map_functional(input_stream: BinaryIO) -> Dict[int, int]:
    """Create frequency map using functional approach.

    Args:
        input_stream: Binary stream to analyze

    Returns:
        Dictionary mapping byte values to frequencies
    """

    def accumulate_frequency(
        acc: Dict[int, int], byte_value: int
    ) -> Dict[int, int]:
        return {**acc, byte_value: acc.get(byte_value, 0) + 1}

    return fold_left(accumulate_frequency, {}, iter_bytes(input_stream))


def encode_bytes_functional(
    byte_values: Iterable[int], codes: Dict[int, List[int]]
) -> List[int]:
    """Encode bytes to bits using functional approach.

    Args:
        byte_values: Sequence of byte values to encode
        codes: Huffman codes mapping

    Returns:
        List of encoded bits
    """

    def flatten_code(acc: List[int], byte_value: int) -> List[int]:
        return acc + codes[byte_value]

    return fold_left(flatten_code, [], byte_values)


def apply_to_stream(
    func: Callable[[T], U], stream_iter: Iterable[T]
) -> List[U]:
    """Apply function to each element in a stream.

    Args:
        func: Function to apply
        stream_iter: Stream iterator

    Returns:
        List of results
    """
    return map_transform(func, stream_iter)


def count_frequencies_functional(
    bytes_iterable: Iterable[int],
) -> Dict[int, int]:
    """Count byte frequencies using purely functional approach.

    Args:
        bytes_iterable: Iterable of byte values

    Returns:
        Frequency mapping
    """

    # Using immutable operations only
    def add_frequency(
        frequencies: Dict[int, int], byte_val: int
    ) -> Dict[int, int]:
        # Create new dict rather than mutating
        return {**frequencies, byte_val: frequencies.get(byte_val, 0) + 1}

    return fold_left(add_frequency, {}, bytes_iterable)
