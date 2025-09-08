#!/usr/bin/env python3
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

from .cli_utils import handle_file_operation, validate_args
from .decompression.decompressor import HuffmanDecompressor


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

    handle_file_operation(decompress_file, input_filename, sys.stdout.buffer)


if __name__ == "__main__":
    main()
