from typing import BinaryIO, Dict

from .higher_order_functions import create_frequency_map_functional
from .immutable_data import FrequencyMap
from .stream_utils import iter_bytes


def create_frequency_map(input_stream: BinaryIO) -> Dict[int, int]:
    """Create frequency map from input stream (legacy interface).

    Args:
        input_stream: Binary stream to analyze

    Returns:
        Dictionary mapping byte values to frequencies
    """
    frequency_map: Dict[int, int] = {}
    for byte_value in iter_bytes(input_stream):
        frequency_map[byte_value] = frequency_map.get(byte_value, 0) + 1
    return frequency_map


def create_frequency_map_immutable(input_stream: BinaryIO) -> FrequencyMap:
    """Create immutable frequency map from input stream.

    Args:
        input_stream: Binary stream to analyze

    Returns:
        Immutable FrequencyMap instance
    """
    frequencies = create_frequency_map_functional(input_stream)
    return FrequencyMap(frequencies=frequencies)
