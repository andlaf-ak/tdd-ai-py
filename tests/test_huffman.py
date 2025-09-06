"""Tests for the Huffman compression algorithm."""

from tdd_ai_py.huffman import HuffmanCompressor


class TestHuffmanCompressor:
    """Test cases for the HuffmanCompressor class."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.compressor = HuffmanCompressor()

    def test_creates_frequency_map_from_input_string(self) -> None:
        """Test that frequency map is correctly created from input string."""
        # ARRANGE
        input_string = "abracadabra"
        expected_frequency_map = {"a": 5, "b": 2, "r": 2, "c": 1, "d": 1}

        # ACT
        result = self.compressor.create_frequency_map(input_string)

        # ASSERT
        assert result == expected_frequency_map
