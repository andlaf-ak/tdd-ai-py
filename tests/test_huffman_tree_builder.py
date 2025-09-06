"""Tests for the HuffmanTreeBuilder module."""

import pytest

from tdd_ai_py.huffman_tree_builder import (
    HuffmanNode,
    build_huffman_tree,
    create_internal_node,
    create_leaf_node,
    find_two_lowest_items,
)


class TestHuffmanNode:
    """Test cases for the HuffmanNode data class."""

    def test_creates_leaf_node(self) -> None:
        """Test creation of a leaf node."""
        character = "a"
        weight = 5

        node = HuffmanNode(weight=weight, character=character)

        assert node.character == character
        assert node.weight == weight
        assert node.left is None
        assert node.right is None
        assert node.is_leaf

    def test_creates_internal_node(self) -> None:
        """Test creation of an internal node."""
        left_node = HuffmanNode(weight=2, character="b")
        right_node = HuffmanNode(weight=3, character="c")
        weight = 5

        node = HuffmanNode(weight=weight, left=left_node, right=right_node)

        assert node.character is None
        assert node.weight == weight
        assert node.left == left_node
        assert node.right == right_node
        assert not node.is_leaf

    def test_node_comparison_for_heap(self) -> None:
        """Test that nodes can be compared by weight for heap operations."""
        node1 = HuffmanNode(weight=1, character="a")
        node2 = HuffmanNode(weight=2, character="b")

        assert node1 < node2
        assert not (node2 < node1)
        assert not (node1 < node1)  # Equal weights

    def test_node_equality(self) -> None:
        """Test node equality comparison."""
        node1 = HuffmanNode(weight=1, character="a")
        node2 = HuffmanNode(weight=1, character="a")
        node3 = HuffmanNode(weight=2, character="a")

        assert node1 == node2
        assert node1 != node3
        assert node1 != "not a node"


class TestBuildHuffmanTree:
    """Test cases for the build_huffman_tree function."""

    def test_builds_complete_huffman_tree(self) -> None:
        """Test that a complete Huffman tree is built from a frequency map."""
        frequency_map = {"a": 5, "b": 2, "r": 2, "c": 1, "d": 1}

        result = build_huffman_tree(frequency_map)

        assert isinstance(result, HuffmanNode)
        assert result.weight == 11  # Sum of all frequencies

        # Root should be an internal node
        assert not result.is_leaf
        assert result.left is not None
        assert result.right is not None

    def test_builds_single_node_tree(self) -> None:
        """Test building tree with single character."""
        frequency_map = {"a": 5}

        result = build_huffman_tree(frequency_map)

        assert isinstance(result, HuffmanNode)
        assert result.weight == 5
        assert result.character == "a"
        assert result.is_leaf


class TestHuffmanTreeBuilderFunctions:
    """Test cases for standalone tree builder functions."""

    def test_create_leaf_node_function(self) -> None:
        """Test the standalone create_leaf_node function."""
        character = "x"
        weight = 10

        result = create_leaf_node(character, weight)

        assert result.character == character
        assert result.weight == weight
        assert result.is_leaf

    def test_create_internal_node_function(self) -> None:
        """Test the standalone create_internal_node function."""
        left = create_leaf_node("a", 2)
        right = create_leaf_node("b", 3)

        result = create_internal_node(left, right)

        assert result.weight == 5  # 2 + 3
        assert result.left == left
        assert result.right == right
        assert not result.is_leaf
        assert result.character is None

    def test_find_two_lowest_items_with_numbers(self) -> None:
        """Test find_two_lowest_items with numeric items."""
        numbers = [5, 2, 8, 1, 9, 3]

        result = find_two_lowest_items(numbers, lambda x: x)

        assert result == (1, 2)

    def test_find_two_lowest_items_with_tuples(self) -> None:
        """Test find_two_lowest_items with tuple items."""
        items = [("a", 5), ("b", 2), ("c", 8), ("d", 1)]

        result = find_two_lowest_items(items, lambda x: x[1])

        assert result == (("d", 1), ("b", 2))

    def test_find_two_lowest_items_with_single_item(self) -> None:
        """Test find_two_lowest_items with single item returns that item
        twice."""
        single_item = [42]

        result = find_two_lowest_items(single_item, lambda x: x)

        assert result == (42, 42)

    def test_find_two_lowest_items_with_empty_list(self) -> None:
        """Test that find_two_lowest_items raises error with empty list."""
        empty_list: list[int] = []

        with pytest.raises(ValueError, match="At least one item is required"):
            find_two_lowest_items(empty_list, lambda x: x)
