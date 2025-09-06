"""Huffman compression algorithm implementation."""

import heapq
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class HuffmanNode:
    """A node in the Huffman binary tree.

    This immutable data class represents a node in the Huffman tree structure.
    Leaf nodes contain characters, while internal nodes combine frequencies.
    """

    weight: int
    character: Optional[str] = None
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None


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
    combined_weight = left.weight + right.weight
    return HuffmanNode(weight=combined_weight, left=left, right=right)


def find_two_lowest_frequencies(
    frequency_map: Dict[str, int]
) -> Tuple[Tuple[str, int], Tuple[str, int]]:
    """Find the two entries with lowest frequencies from a frequency map.

    Args:
        frequency_map: Dictionary mapping characters to their frequencies

    Returns:
        Tuple containing the two (character, frequency) pairs with lowest frequencies
    """
    # Use heapq.nsmallest for efficient selection of two smallest items
    smallest_items = heapq.nsmallest(2, frequency_map.items(), key=lambda x: x[1])
    return smallest_items[0], smallest_items[1]


def create_frequency_map(text: str) -> Dict[str, int]:
    """Create a frequency map from input text.

    Pure function that analyzes text and returns character frequencies.

    Args:
        text: The input string to analyze

    Returns:
        A dictionary mapping characters to their frequencies
    """
    return dict(Counter(text))


class HuffmanCompressor:
    """A class for Huffman compression and decompression.

    This class provides methods to build Huffman trees and compress/decompress text
    using the Huffman coding algorithm.
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

        This method creates leaf nodes for each character and combines them
        into a single internal node with the sum of their frequencies.

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
        return create_internal_node(left_node, right_node)

    def create_node_from_lowest_frequencies(
        self, frequency_map: Dict[str, int]
    ) -> HuffmanNode:
        """Create a binary tree node from the two lowest frequencies in a frequency map.

        Uses an efficient algorithm to find the two lowest frequency entries
        and combines them into a single Huffman tree node.

        Args:
            frequency_map: Dictionary mapping characters to their frequencies

        Returns:
            A HuffmanNode combining the two characters with lowest frequencies
        """
        (char1, freq1), (char2, freq2) = find_two_lowest_frequencies(frequency_map)
        return self.create_node_from_values(char1, freq1, char2, freq2)
