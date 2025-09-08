#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
Huffman Compression Script

Usage:
    python -m tdd_ai_py.compress <input_file>

Example:
    python -m tdd_ai_py.compress input.txt > compressed.bin
"""

import sys
from typing import BinaryIO

from .compression.compressor import HuffmanCompressor


def validate_args() -> str | None:
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
        print("Usage: python -m tdd_ai_py.compress <input_file>", file=sys.stderr)
        sys.exit(1)

    try:
        compress_file(input_filename, sys.stdout.buffer)
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied accessing '{input_filename}'.", file=sys.stderr)
        sys.exit(1)
    except (OSError, IOError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
