from io import BytesIO
from typing import Dict

from tdd_ai_py.compression.frequency_counter import create_frequency_map


class TestCreateFrequencyMap:
    def test_creates_frequency_map_from_input_stream(self) -> None:
        input_stream = BytesIO(b"abracadabra")
        expected_frequency_map: Dict[int, int] = {
            ord("a"): 5,
            ord("b"): 2,
            ord("r"): 2,
            ord("c"): 1,
            ord("d"): 1,
        }

        result = create_frequency_map(input_stream)

        assert result == expected_frequency_map

    def test_creates_frequency_map_from_empty_stream(self) -> None:
        input_stream = BytesIO(b"")
        expected_frequency_map: Dict[int, int] = {}

        result = create_frequency_map(input_stream)

        assert result == expected_frequency_map

    def test_creates_frequency_map_from_single_character_stream(self) -> None:
        input_stream = BytesIO(b"a")
        expected_frequency_map = {ord("a"): 1}

        result = create_frequency_map(input_stream)

        assert result == expected_frequency_map

    def test_create_frequency_map_with_hello_stream(self) -> None:
        input_stream = BytesIO(b"hello")
        expected_frequency_map = {
            ord("h"): 1,
            ord("e"): 1,
            ord("l"): 2,
            ord("o"): 1,
        }

        result = create_frequency_map(input_stream)

        assert result == expected_frequency_map
