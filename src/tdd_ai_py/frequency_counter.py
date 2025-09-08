from collections import Counter
from typing import BinaryIO, Dict

from .stream_utils import iter_bytes


def create_frequency_map(input_stream: BinaryIO) -> Dict[int, int]:
    """Create frequency map using functional programming approach.

    Uses functional composition: stream -> iterable -> counter -> dict
    """
    return dict(Counter(iter_bytes(input_stream)))
