#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
Huffman Decompression Script

Usage:
    python -m tdd_ai_py.decompress <compressed_file | ->

Examples:
    # From file to stdout
    python -m tdd_ai_py.decompress compressed.bin > decompressed.txt

    # From stdin to stdout
    cat compressed.bin | python -m tdd_ai_py.decompress - > decompressed.txt
"""

import sys
from io import BytesIO
from typing import BinaryIO, Optional

from .decompression.decompressor import HuffmanDecompressor


def validate_args() -> Optional[str]:
    """Validate args and return input filename or '-' for stdin, or None."""
    return sys.argv[1] if len(sys.argv) == 2 else None


def decompress_stream(input_stream: BinaryIO, output_stream: BinaryIO) -> None:
    """Decompress a binary stream using Huffman decompression."""
    # Decompressor expects a seekable stream; wrap if necessary
    if not input_stream.seekable():
        input_stream = BytesIO(input_stream.read())
    HuffmanDecompressor().decompress(input_stream, output_stream)


def decompress_file(input_filename: str, output_stream: BinaryIO) -> None:
    """Decompress a file using Huffman decompression."""
    with open(input_filename, "rb") as input_file:
        decompress_stream(input_file, output_stream)


def main() -> None:
    """Main function to decompress a file or stdin and output to stdout."""
    input_filename = validate_args()

    if not input_filename:
        print(
            "Usage: python -m tdd_ai_py.decompress <compressed_file | ->", file=sys.stderr
        )
        sys.exit(1)

    try:
        if input_filename == "-":
            decompress_stream(sys.stdin.buffer, sys.stdout.buffer)
        else:
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
