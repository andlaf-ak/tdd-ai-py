#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
Huffman Compression Script

Usage:
    python -m tdd_ai_py.compress <input_file | ->

Examples:
    # From file to stdout
    python -m tdd_ai_py.compress input.txt > compressed.bin

    # From stdin to stdout
    cat input.txt | python -m tdd_ai_py.compress - > compressed.bin
"""

import sys
from io import BytesIO
from typing import BinaryIO, Optional

from .compression.compressor import HuffmanCompressor


def validate_args() -> Optional[str]:
    """Validate args and return input filename or '-' for stdin, or None."""
    return sys.argv[1] if len(sys.argv) == 2 else None


def compress_stream(input_stream: BinaryIO, output_stream: BinaryIO) -> None:
    """Compress a binary stream using Huffman compression.

    If the input stream is not seekable (e.g., stdin), it will be fully read into
    memory first so the compressor can perform two passes without relying on seek().
    """
    if not input_stream.seekable():
        input_stream = BytesIO(input_stream.read())
    HuffmanCompressor().compress(input_stream, output_stream)


def compress_file(input_filename: str, output_stream: BinaryIO) -> None:
    """Compress a file using Huffman compression."""
    with open(input_filename, "rb") as input_file:
        compress_stream(input_file, output_stream)


def main() -> None:
    """Main function to compress a file or stdin and output to stdout."""
    input_filename = validate_args()

    if not input_filename:
        print("Usage: python -m tdd_ai_py.compress <input_file | ->", file=sys.stderr)
        sys.exit(1)

    try:
        if input_filename == "-":
            compress_stream(sys.stdin.buffer, sys.stdout.buffer)
        else:
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
