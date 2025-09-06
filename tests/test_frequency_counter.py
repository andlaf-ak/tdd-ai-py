from typing import Dict

from tdd_ai_py.frequency_counter import create_frequency_map


class TestCreateFrequencyMap:

    def test_creates_frequency_map_from_input_string(self) -> None:
        # ARRANGE
        input_string = "abracadabra"
        expected_frequency_map: Dict[str, int] = {
            "a": 5,
            "b": 2,
            "r": 2,
            "c": 1,
            "d": 1,
        }

        # ACT
        result = create_frequency_map(input_string)

        # ASSERT
        assert result == expected_frequency_map

    def test_creates_frequency_map_from_empty_string(self) -> None:
        # ARRANGE
        input_string = ""
        expected_frequency_map: Dict[str, int] = {}

        # ACT
        result = create_frequency_map(input_string)

        # ASSERT
        assert result == expected_frequency_map

    def test_creates_frequency_map_from_single_character(self) -> None:
        # ARRANGE
        input_string = "a"
        expected_frequency_map = {"a": 1}

        # ACT
        result = create_frequency_map(input_string)

        # ASSERT
        assert result == expected_frequency_map

    def test_create_frequency_map_with_hello(self) -> None:
        # ARRANGE
        input_string = "hello"
        expected_frequency_map = {"h": 1, "e": 1, "l": 2, "o": 1}

        # ACT
        result = create_frequency_map(input_string)

        # ASSERT
        assert result == expected_frequency_map
