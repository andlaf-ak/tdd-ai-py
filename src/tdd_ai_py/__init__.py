"""TDD AI Python package for Huffman compression.

This package provides implementations of the Huffman compression algorithm
using test-driven development principles, with both imperative and functional
programming interfaces.
"""

from .compressor import HuffmanCompressor, compress
from .decompressor import HuffmanDecompressor, decompress
from .frequency_counter import (
    create_frequency_map,
    create_frequency_map_immutable,
)
from .functional_utils import compose, curry, pipe
from .higher_order_functions import (
    apply_to_stream,
    count_frequencies_functional,
    create_frequency_map_functional,
    encode_bytes_functional,
    filter_transform,
    fold_left,
    map_transform,
)
from .huffman_tree_builder import HuffmanNode, build_huffman_tree
from .immutable_data import CompressionContext, FrequencyMap, HuffmanCodes
from .result_types import Err, Ok, Result, safe_call, safe_call_with_args
from .safe_compression import (
    compress_with_validation,
    safe_compress,
    safe_decompress,
    safe_round_trip,
)

__all__ = [
    # Core functional interfaces (recommended)
    "compress",
    "decompress",
    "safe_compress",
    "safe_decompress",
    # Legacy class interfaces (for backward compatibility)
    "HuffmanCompressor",
    "HuffmanDecompressor",
    # Frequency analysis (imperative and functional)
    "create_frequency_map",
    "create_frequency_map_immutable",
    "create_frequency_map_functional",
    # Immutable data structures
    "FrequencyMap",
    "HuffmanCodes",
    "CompressionContext",
    # Higher-order functions
    "fold_left",
    "map_transform",
    "filter_transform",
    "apply_to_stream",
    "encode_bytes_functional",
    "count_frequencies_functional",
    # Functional composition utilities
    "pipe",
    "compose",
    "curry",
    # Monadic error handling
    "Result",
    "Ok",
    "Err",
    "safe_call",
    "safe_call_with_args",
    "safe_round_trip",
    "compress_with_validation",
    # Core data structures and utilities
    "HuffmanNode",
    "build_huffman_tree",
]
