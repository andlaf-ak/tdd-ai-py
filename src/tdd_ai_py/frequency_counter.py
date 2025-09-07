from typing import BinaryIO, Dict

from .stream_utils import iter_bytes


def create_frequency_map(input_stream: BinaryIO) -> Dict[int, int]:
    frequency_map: Dict[int, int] = {}
    for byte_value in iter_bytes(input_stream):
        frequency_map[byte_value] = frequency_map.get(byte_value, 0) + 1
    return frequency_map
