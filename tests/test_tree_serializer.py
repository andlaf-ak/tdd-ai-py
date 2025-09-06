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

    def test_serializes_tree_with_two_leaf_nodes(self) -> None:
        """Test that tree with root and two leaves emits correct depth-first traversal."""
        left_leaf = HuffmanNode(weight=1, character="a")
        right_leaf = HuffmanNode(weight=1, character="b")
        root = HuffmanNode(weight=2, left=left_leaf, right=right_leaf)

        result = serialize_tree(root)

        # Depth-first: root(internal)=0, left(leaf)=1+8bits_a, right(leaf)=1+8bits_b
        # 'a' = ASCII 97 = 01100001, 'b' = ASCII 98 = 01100010
        expected = "0" + "1" + "01100001" + "1" + "01100010"
        assert result == expected

    def test_serializes_complex_tree_with_nested_internal_node(self) -> None:
        """Test serialization of tree: root -> (left='a', right_internal -> (left='b', right='c'))."""
        # Build tree structure:
        #       root (internal)
        #      /              \
        #   'a' (leaf)    internal node
        #                    /        \
        #                'b' (leaf)  'c' (leaf)

        left_leaf_a = HuffmanNode(weight=1, character="a")
        right_internal_left_b = HuffmanNode(weight=1, character="b")
        right_internal_right_c = HuffmanNode(weight=1, character="c")
        right_internal = HuffmanNode(
            weight=2, left=right_internal_left_b, right=right_internal_right_c
        )
        root = HuffmanNode(weight=3, left=left_leaf_a, right=right_internal)

        result = serialize_tree(root)

        # Depth-first traversal:
        # 1. root (internal) -> "0"
        # 2. left subtree: 'a' (leaf) -> "1" + "01100001"
        # 3. right subtree (internal) -> "0"
        # 4. right-left subtree: 'b' (leaf) -> "1" + "01100010"
        # 5. right-right subtree: 'c' (leaf) -> "1" + "01100011"
        # 'a'=97=01100001, 'b'=98=01100010, 'c'=99=01100011
        expected = (
            "0" + "1" + "01100001" + "0" + "1" + "01100010" + "1" + "01100011"
        )
        assert result == expected
