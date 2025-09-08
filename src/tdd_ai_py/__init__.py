"""TDD AI Python package for Huffman compression.

This package provides implementations of the Huffman compression algorithm
using test-driven development principles.
"""

from .compression.compressor import HuffmanCompressor
from .compression.frequency_counter import create_frequency_map
from .compression.huffman_tree_builder import HuffmanNode, build_huffman_tree
from .decompression.decompressor import HuffmanDecompressor

__all__ = [
    "HuffmanCompressor",
    "HuffmanDecompressor",
    "create_frequency_map",
    "HuffmanNode",
    "build_huffman_tree",
]
