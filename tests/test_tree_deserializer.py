"""Tests for Huffman tree deserialization from bit strings."""

from tdd_ai_py.tree_deserializer import deserialize_tree


class TestTreeDeserializer:
    """Test cases for tree deserialization algorithm."""

    def test_deserializes_single_leaf_node(self) -> None:
        """Test that '1' + 8-bit character deserializes to single leaf node."""
        # 'a' = ASCII 97 = 01100001 in binary
        serialized_tree = "101100001"

        result = deserialize_tree(serialized_tree)

        assert result.character == "a"
        assert result.weight == 0  # Weight not preserved in serialization
        assert result.left is None
        assert result.right is None
        assert result.is_leaf
