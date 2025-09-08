#!/usr/bin/env python3
"""
Huffman Compression Script

Usage:
    python -m tdd_ai_py.compress <input_file>

Example:
    python -m tdd_ai_py.compress input.txt > compressed.bin
"""

import sys
from typing import BinaryIO

from .cli_utils import handle_file_operation, validate_args
from .compression.compressor import HuffmanCompressor


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

    handle_file_operation(compress_file, input_filename, sys.stdout.buffer)


if __name__ == "__main__":
    main()
