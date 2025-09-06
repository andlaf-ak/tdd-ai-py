"""Tests for Huffman code generation from tree paths."""

from tdd_ai_py.huffman_encoder import generate_huffman_codes
from tdd_ai_py.huffman_tree_builder import HuffmanNode


class TestHuffmanEncoder:
    """Test cases for generating Huffman codes from tree paths."""

    def test_generates_code_for_single_root_node(self) -> None:
        """Test that single root node generates code '0'."""
        root_node = HuffmanNode(weight=1, character="a")

        codes = generate_huffman_codes(root_node)

        assert codes == {"a": "0"}
