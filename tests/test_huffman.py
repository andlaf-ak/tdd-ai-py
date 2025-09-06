"""Tests for the Huffman compression algorithm."""

from tdd_ai_py.huffman import HuffmanCompressor, HuffmanNode


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

    def test_creates_binary_tree_node_from_two_values(self) -> None:
        """Test that a binary tree node is created from two frequency values."""
        # ARRANGE
        char1, freq1 = "c", 1
        char2, freq2 = "d", 1
        expected_weight = 2

        # ACT
        result = self.compressor.create_node_from_values(char1, freq1, char2, freq2)

        # ASSERT
        assert isinstance(result, HuffmanNode)
        assert result.weight == expected_weight

        # Assert left and right nodes exist before accessing their attributes
        assert result.left is not None
        assert result.right is not None

        assert result.left.character == char1
        assert result.left.weight == freq1
        assert result.right.character == char2
        assert result.right.weight == freq2

    def test_creates_node_from_lowest_frequencies(self) -> None:
        """Test that a node is created from the two lowest frequencies in a frequency map."""
        # ARRANGE
        frequency_map = {"a": 5, "b": 2, "r": 2, "c": 1, "d": 1}
        # The two lowest frequencies are 'c':1 and 'd':1
        expected_weight = 2

        # ACT
        result = self.compressor.create_node_from_lowest_frequencies(frequency_map)

        # ASSERT
        assert isinstance(result, HuffmanNode)
        assert result.weight == expected_weight

        # Assert left and right nodes exist before accessing their attributes
        assert result.left is not None
        assert result.right is not None

        # Should combine the two lowest frequency characters (c and d)
        left_char = result.left.character
        right_char = result.right.character
        assert {left_char, right_char} == {"c", "d"}
        assert result.left.weight == 1
        assert result.right.weight == 1
