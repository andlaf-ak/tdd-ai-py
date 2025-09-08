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
from pathlib import Path
from typing import BinaryIO, Optional

# Add src directory to Python path so we can import tdd_ai_py
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tdd_ai_py.compression.compressor import HuffmanCompressor  # noqa: E402


def validate_args() -> Optional[str]:
    """Validate command line arguments and return input filename or None."""
    return sys.argv[1] if len(sys.argv) == 2 else None


def compress_file(input_filename: str, output_stream: BinaryIO) -> None:
    """Compress a file using Huffman compression."""
    with open(input_filename, "rb") as input_file:
        HuffmanCompressor().compress(input_file, output_stream)


def main() -> None:
    """Main function to compress a file and output to stdout."""
    input_filename = validate_args()

    if not input_filename:
        print("Usage: python huffman_compression.py <input_file>", file=sys.stderr)
        sys.exit(1)

    try:
        compress_file(input_filename, sys.stdout.buffer)
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied accessing '{input_filename}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
