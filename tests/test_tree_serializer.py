"""Tests for Huffman tree serialization using depth-first traversal."""

from tdd_ai_py.huffman_tree_builder import HuffmanNode
from tdd_ai_py.tree_serializer import serialize_tree


class TestTreeSerializer:
    """Test cases for tree serialization algorithm."""

    def test_serializes_single_leaf_node(self) -> None:
        """Test that single leaf node emits '1' + 8-bit character."""
        leaf_node = HuffmanNode(weight=1, character="a")

        result = serialize_tree(leaf_node)

        # 'a' = ASCII 97 = 01100001 in binary
        assert result == "101100001"
