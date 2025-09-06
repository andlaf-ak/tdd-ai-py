"""Tests for the Huffman compressor."""

from tdd_ai_py.compressor import HuffmanCompressor
from tdd_ai_py.huffman_tree_builder import HuffmanNode


class TestHuffmanCompressor:
    """Test cases for the HuffmanCompressor class."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.compressor = HuffmanCompressor()

    def test_compresses_basic_input_successfully(self) -> None:
        """Test that compressor can process input text and create huffman tree."""
        input_text = "she sells seashells on the seashore"

        huffman_tree = self.compressor.compress(input_text)

        assert isinstance(huffman_tree, HuffmanNode)
        assert huffman_tree.weight == len(input_text)
        assert not huffman_tree.is_leaf
        assert huffman_tree.character is None
        assert huffman_tree.left is not None
        assert huffman_tree.right is not None

    def test_compresses_single_character_input(self) -> None:
        """Test that single character input produces tree with only root node."""
        input_text = "a"

        huffman_tree = self.compressor.compress(input_text)

        assert isinstance(huffman_tree, HuffmanNode)
        assert huffman_tree.weight == 1
        assert huffman_tree.is_leaf
        assert huffman_tree.character == "a"
        assert huffman_tree.left is None
        assert huffman_tree.right is None
