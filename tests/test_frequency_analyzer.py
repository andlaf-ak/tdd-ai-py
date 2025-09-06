"""Tests for the frequency analyzer module."""

from typing import Dict

from tdd_ai_py.frequency_analyzer import create_frequency_map


class TestCreateFrequencyMap:
    """Test cases for the create_frequency_map function."""

    def test_creates_frequency_map_from_input_string(self) -> None:
        """Test that frequency map is correctly created from input string."""
        # ARRANGE
        input_string = "abracadabra"
        expected_frequency_map = {"a": 5, "b": 2, "r": 2, "c": 1, "d": 1}

        # ACT
        result = create_frequency_map(input_string)

        # ASSERT
        assert result == expected_frequency_map

    def test_creates_frequency_map_from_empty_string(self) -> None:
        """Test that empty frequency map is created from empty string."""
        # ARRANGE
        input_string = ""
        expected_frequency_map: Dict[str, int] = {}

        # ACT
        result = create_frequency_map(input_string)

        # ASSERT
        assert result == expected_frequency_map

    def test_creates_frequency_map_from_single_character(self) -> None:
        """Test frequency map creation from single character string."""
        # ARRANGE
        input_string = "a"
        expected_frequency_map = {"a": 1}

        # ACT
        result = create_frequency_map(input_string)

        # ASSERT
        assert result == expected_frequency_map

    def test_create_frequency_map_with_hello(self) -> None:
        """Test the create_frequency_map function with 'hello'."""
        # ARRANGE
        input_string = "hello"
        expected_frequency_map = {"h": 1, "e": 1, "l": 2, "o": 1}

        # ACT
        result = create_frequency_map(input_string)

        # ASSERT
        assert result == expected_frequency_map
