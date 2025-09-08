"""Functional programming examples for Huffman compression.

This module demonstrates various functional programming patterns
applied to the Huffman compression algorithm.
"""

from io import BytesIO
from typing import cast

from .frequency_counter import create_frequency_map_immutable
from .functional_utils import pipe
from .higher_order_functions import fold_left
from .huffman_encoder import generate_huffman_codes
from .huffman_tree_builder import build_huffman_tree
from .result_types import Err, Result
from .safe_compression import safe_compress, safe_round_trip


def functional_compression_pipeline(data: bytes) -> Result[bytes, str]:
    """Demonstrate functional compression pipeline.

    This example shows how to use the functional programming features
    to perform compression in a purely functional style.

    Args:
        data: Raw data to compress

    Returns:
        Result containing compressed data or error
    """
    input_stream = BytesIO(data)
    output_stream = BytesIO()

    # Use safe compression with error handling
    result = safe_compress(input_stream, output_stream)

    if result.is_ok():
        return result.map(lambda _: output_stream.getvalue())
    return result  # type: ignore


def functional_analysis_example(data: bytes) -> dict:
    """Demonstrate functional analysis of data.

    Args:
        data: Data to analyze

    Returns:
        Analysis results
    """
    input_stream = BytesIO(data)

    # Create immutable frequency map
    freq_map = create_frequency_map_immutable(input_stream)

    # Functional pipeline for analysis
    def analyze_compression_ratio() -> float:
        if len(data) == 0:
            return 0.0

        # Build tree and codes functionally
        tree = build_huffman_tree(dict(freq_map.frequencies))
        codes = generate_huffman_codes(tree)

        # Calculate theoretical compressed size
        total_bits = fold_left(
            lambda acc, byte_val: acc
            + len(codes[byte_val]) * freq_map.get_frequency(byte_val),
            0,
            freq_map.unique_bytes,
        )

        return total_bits / (len(data) * 8)

    return {
        "original_size": len(data),
        "unique_bytes": len(freq_map.unique_bytes),
        "most_frequent": (
            max(freq_map.frequencies.items(), key=lambda x: x[1])
            if freq_map.frequencies
            else None
        ),
        "theoretical_compression_ratio": analyze_compression_ratio(),
        "total_characters": freq_map.total_count,
    }


def functional_round_trip_example(data: bytes) -> Result[bool, str]:
    """Demonstrate functional round-trip testing.

    Args:
        data: Data to test

    Returns:
        Result indicating if round trip was successful
    """
    return safe_round_trip(data).map(lambda result: result == data)


def demonstrate_functional_composition() -> None:
    """Demonstrate functional composition patterns."""
    # Example data
    test_data = b"hello world! this is a test of functional programming."

    # Pipeline example
    def process_data(data: bytes) -> str:
        def format_analysis(analysis: dict) -> str:
            return (
                f"Processed {analysis['original_size']} bytes with "
                f"{analysis['unique_bytes']} unique characters"
            )

        result: str = pipe(
            data,
            functional_analysis_example,
            format_analysis,
        )
        return result

    # Execute examples
    print("=== Functional Programming Examples ===")
    print(f"Processing: {test_data!r}")  # Use !r for proper byte representation
    print(process_data(test_data))

    # Round trip test
    round_trip_result = functional_round_trip_example(test_data)
    if round_trip_result.is_ok():
        print(f"Round trip successful: {round_trip_result.unwrap()}")
    else:
        error_result = cast(Err[bool, str], round_trip_result)
        print(f"Round trip failed: {error_result.error}")

    # Compression test
    compression_result = functional_compression_pipeline(test_data)
    if compression_result.is_ok():
        compressed_data = compression_result.unwrap()
        ratio = len(compressed_data) / len(test_data)
        print(f"Compression ratio: {ratio:.2%}")
    else:
        compression_error = cast(Err[bytes, str], compression_result)
        print(f"Compression failed: {compression_error.error}")


if __name__ == "__main__":
    demonstrate_functional_composition()
