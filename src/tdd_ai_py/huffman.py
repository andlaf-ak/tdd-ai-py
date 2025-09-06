"""Huffman compression algorithm implementation."""

import heapq
from collections import Counter
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, order=True)
class HuffmanNode:
    """A node in the Huffman binary tree.

    This immutable data class represents a node in the Huffman tree structure.
    Leaf nodes contain characters, while internal nodes combine frequencies.
    The order=True parameter enables natural sorting by weight for heap operations.
    """

    weight: int
    character: Optional[str] = None
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

    @property
    def is_leaf(self) -> bool:
        """Check if this node is a leaf node."""
        return self.left is None and self.right is None


def create_leaf_node(character: str, weight: int) -> HuffmanNode:
    """Create a leaf node for a single character.

    Args:
        character: The character to store in the leaf
        weight: The frequency of the character

    Returns:
        A HuffmanNode representing a leaf with the given character and weight
    """
    return HuffmanNode(weight=weight, character=character)


def create_internal_node(left: HuffmanNode, right: HuffmanNode) -> HuffmanNode:
    """Create an internal node from two child nodes.

    Args:
        left: The left child node
        right: The right child node

    Returns:
        A HuffmanNode with combined weight and the given children
    """
    return HuffmanNode(weight=left.weight + right.weight, left=left, right=right)


def find_two_lowest_items(items: List[T], key_func: Callable[[T], int]) -> Tuple[T, T]:
    """Generic function to find two items with lowest values based on a key function.

    Args:
        items: List of items to search
        key_func: Function to extract comparison key from each item

    Returns:
        Tuple containing the two items with lowest values
    """
    two_lowest = heapq.nsmallest(2, items, key=key_func)
    return two_lowest[0], two_lowest[1]


def find_two_lowest_nodes(nodes: List[HuffmanNode]) -> Tuple[HuffmanNode, HuffmanNode]:
    """Find the two nodes with lowest frequencies from a list of nodes.

    Args:
        nodes: List of HuffmanNode objects

    Returns:
        Tuple containing the two nodes with lowest frequencies
    """
    return find_two_lowest_items(nodes, lambda node: node.weight)


def find_two_lowest_frequencies(
    frequency_map: Dict[str, int]
) -> Tuple[Tuple[str, int], Tuple[str, int]]:
    """Find the two entries with lowest frequencies from a frequency map.

    Args:
        frequency_map: Dictionary mapping characters to their frequencies

    Returns:
        Tuple containing the two (character, frequency) pairs with lowest frequencies
    """
    return find_two_lowest_items(list(frequency_map.items()), lambda x: x[1])


def create_frequency_map(text: str) -> Dict[str, int]:
    """Create a frequency map from input text.

    Pure function that analyzes text and returns character frequencies.

    Args:
        text: The input string to analyze

    Returns:
        A dictionary mapping characters to their frequencies
    """
    return dict(Counter(text))


def combine_nodes(left: HuffmanNode, right: HuffmanNode) -> HuffmanNode:
    """Combine two nodes into a new internal node.

    Pure function that creates a new internal node from two existing nodes.

    Args:
        left: Left child node
        right: Right child node

    Returns:
        New internal node combining the two inputs
    """
    return create_internal_node(left, right)


class HuffmanCompressor:
    """A class for Huffman compression and decompression.

    This class provides methods to build Huffman trees and compress/decompress text
    using the Huffman coding algorithm. All methods delegate to pure functions
    for better testability and composability.
    """

    def create_frequency_map(self, text: str) -> Dict[str, int]:
        """Create a frequency map from input text.

        Args:
            text: The input string to analyze

        Returns:
            A dictionary mapping characters to their frequencies
        """
        return create_frequency_map(text)

    def create_node_from_values(
        self, char1: str, freq1: int, char2: str, freq2: int
    ) -> HuffmanNode:
        """Create a binary tree node from two character-frequency pairs.

        Args:
            char1: First character
            freq1: Frequency of first character
            char2: Second character
            freq2: Frequency of second character

        Returns:
            A HuffmanNode with the two characters as leaves and combined weight
        """
        left_node = create_leaf_node(char1, freq1)
        right_node = create_leaf_node(char2, freq2)
        return combine_nodes(left_node, right_node)

    def create_node_from_lowest_frequencies(
        self, frequency_map: Dict[str, int]
    ) -> HuffmanNode:
        """Create a binary tree node from the two lowest frequencies in a frequency map.

        Args:
            frequency_map: Dictionary mapping characters to their frequencies

        Returns:
            A HuffmanNode combining the two characters with lowest frequencies
        """
        (char1, freq1), (char2, freq2) = find_two_lowest_frequencies(frequency_map)
        return self.create_node_from_values(char1, freq1, char2, freq2)

    def select_and_join_lowest_nodes(self, nodes: List[HuffmanNode]) -> HuffmanNode:
        """Select the two lowest frequency nodes and join them into a new internal node.

        Args:
            nodes: List of HuffmanNode objects

        Returns:
            A new HuffmanNode combining the two nodes with lowest frequencies
        """
        left_node, right_node = find_two_lowest_nodes(nodes)
        return combine_nodes(left_node, right_node)
