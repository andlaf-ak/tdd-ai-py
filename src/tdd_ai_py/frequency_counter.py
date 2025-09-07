from typing import Dict, TextIO


def create_frequency_map(input_stream: TextIO) -> Dict[str, int]:
    frequency_map: Dict[str, int] = {}
    while True:
        char = input_stream.read(1)
        if not char:
            break
        frequency_map[char] = frequency_map.get(char, 0) + 1
    return frequency_map
