"""Huffman compression algorithm implementation.

This module provides a unified interface for Huffman compression by combining
frequency analysis and tree building capabilities.
"""

from typing import Dict, List

from .frequency_analyzer import create_frequency_map
from .huffman_tree_builder import HuffmanNode, HuffmanTreeBuilder


class HuffmanCompressor:
    """A class for Huffman compression and decompression.

    This class provides a unified interface for both frequency analysis and
    Huffman tree building. It delegates to specialized functions and classes
    for better separation of concerns.
    """

    def __init__(self) -> None:
        """Initialize the compressor with tree builder."""
        self._tree_builder = HuffmanTreeBuilder()

    def create_frequency_map(self, text: str) -> Dict[str, int]:
        """Create a frequency map from input text."""
        return create_frequency_map(text)

    def create_node_from_values(
        self, char1: str, freq1: int, char2: str, freq2: int
    ) -> HuffmanNode:
        """Create a binary tree node from two character-frequency pairs."""
        return self._tree_builder.create_node_from_values(
            char1, freq1, char2, freq2
        )

    def select_and_join_lowest_nodes(
        self, nodes: List[HuffmanNode]
    ) -> HuffmanNode:
        """Select the two lowest frequency nodes and join them into a new
        internal node."""
        return self._tree_builder.select_and_join_lowest_nodes(nodes)

    def build_huffman_tree(self, frequency_map: Dict[str, int]) -> HuffmanNode:
        """Build a complete Huffman tree from a frequency map."""
        return self._tree_builder.build_huffman_tree(frequency_map)
