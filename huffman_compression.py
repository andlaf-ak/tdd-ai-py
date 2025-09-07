#!/usr/bin/env python3
"""
Huffman Compression Main Module

This script compresses a file using Huffman coding and outputs the result to stdout.

Usage:
    python huffman_compression.py <input_file>

Example:
    python huffman_compression.py input.txt > compressed.bin
"""

import sys
from typing import BinaryIO

from src.tdd_ai_py.compressor import HuffmanCompressor


def main() -> None:
    """Main function to compress a file and output to stdout."""
    if len(sys.argv) != 2:
        print(
            "Usage: python huffman_compression.py <input_file>", file=sys.stderr
        )
        sys.exit(1)

    input_filename = sys.argv[1]

    try:
        # Open input file in binary mode
        with open(input_filename, "rb") as input_file:
            # Use stdout in binary mode for compressed output
            output_stream: BinaryIO = sys.stdout.buffer

            # Create compressor and compress the file
            compressor = HuffmanCompressor()
            compressor.compress(input_file, output_stream)

    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(
            f"Error: Permission denied accessing '{input_filename}'.",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
