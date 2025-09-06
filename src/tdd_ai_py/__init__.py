"""TDD AI Python package for Huffman compression.

This package provides implementations of the Huffman compression algorithm
using test-driven development principles.
"""

from .frequency_analyzer import create_frequency_map
from .huffman import HuffmanCompressor
from .huffman_tree_builder import HuffmanNode, HuffmanTreeBuilder

__all__ = [
    "HuffmanNode",
    "HuffmanCompressor",
    "HuffmanTreeBuilder",
    "create_frequency_map",
]
