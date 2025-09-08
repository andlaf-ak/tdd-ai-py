#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
Huffman Decompression Script

Usage:
    python -m tdd_ai_py.decompress <compressed_file>

Example:
    python -m tdd_ai_py.decompress compressed.bin > decompressed.txt
"""

import sys
from io import BytesIO
from typing import BinaryIO

from .decompression.decompressor import HuffmanDecompressor


def validate_args() -> str | None:
    """Validate command line arguments and return input filename or None."""
    return sys.argv[1] if len(sys.argv) == 2 else None


def decompress_file(input_filename: str, output_stream: BinaryIO) -> None:
    """Decompress a file using Huffman decompression."""
    with open(input_filename, "rb") as input_file:
        input_stream = BytesIO(input_file.read())
        HuffmanDecompressor().decompress(input_stream, output_stream)


def main() -> None:
    """Main function to decompress a file and output to stdout."""
    input_filename = validate_args()

    if not input_filename:
        print("Usage: python -m tdd_ai_py.decompress <compressed_file>", file=sys.stderr)
        sys.exit(1)

    try:
        decompress_file(input_filename, sys.stdout.buffer)
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
