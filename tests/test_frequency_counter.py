from io import StringIO
from typing import Dict

from tdd_ai_py.frequency_counter import create_frequency_map


class TestCreateFrequencyMap:
    def test_creates_frequency_map_from_input_stream(self) -> None:
        input_stream = StringIO("abracadabra")
        expected_frequency_map: Dict[str, int] = {
            "a": 5,
            "b": 2,
            "r": 2,
            "c": 1,
            "d": 1,
        }

        result = create_frequency_map(input_stream)

        assert result == expected_frequency_map

    def test_creates_frequency_map_from_empty_stream(self) -> None:
        input_stream = StringIO("")
        expected_frequency_map: Dict[str, int] = {}

        result = create_frequency_map(input_stream)

        assert result == expected_frequency_map

    def test_creates_frequency_map_from_single_character_stream(self) -> None:
        input_stream = StringIO("a")
        expected_frequency_map = {"a": 1}

        result = create_frequency_map(input_stream)

        assert result == expected_frequency_map

    def test_create_frequency_map_with_hello_stream(self) -> None:
        input_stream = StringIO("hello")
        expected_frequency_map = {"h": 1, "e": 1, "l": 2, "o": 1}

        result = create_frequency_map(input_stream)

        assert result == expected_frequency_map
