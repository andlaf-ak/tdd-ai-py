"""Tests for Huffman tree deserialization from bit strings."""

from tdd_ai_py.huffman_tree_builder import HuffmanNode
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

    def test_deserializes_tree_with_two_leaf_nodes(self) -> None:
        """Test that tree with root and two leaves deserializes correctly."""
        serialized_tree = self._build_binary_tree_serialization()

        result = deserialize_tree(serialized_tree)

        self._assert_is_internal_node(result)
        self._assert_left_child_is_character(result, "a")
        self._assert_right_child_is_character(result, "b")

    def _build_binary_tree_serialization(self) -> str:
        """Build serialized tree: root(internal) -> left('a'), right('b')."""
        # 'a' = ASCII 97 = 01100001, 'b' = ASCII 98 = 01100010
        return "0" + "1" + "01100001" + "1" + "01100010"

    def _assert_is_internal_node(self, node: HuffmanNode) -> None:
        """Assert node is an internal node with left and right children."""
        assert node.character is None
        assert node.weight == 0
        assert not node.is_leaf
        assert node.left is not None
        assert node.right is not None

    def _assert_left_child_is_character(
        self, node: HuffmanNode, expected_char: str
    ) -> None:
        """Assert left child is a leaf with expected character."""
        assert node.left is not None
        assert node.left.character == expected_char
        assert node.left.is_leaf

    def _assert_right_child_is_character(
        self, node: HuffmanNode, expected_char: str
    ) -> None:
        """Assert right child is a leaf with expected character."""
        assert node.right is not None
        assert node.right.character == expected_char
        assert node.right.is_leaf
