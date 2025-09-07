#!/usr/bin/env python3
"""
Huffman Decompression Main Module

This script decompresses a file that was compressed using Huffman coding and outputs the result to stdout.

Usage:
    python huffman_decompression.py <compressed_file>

Example:
    python huffman_decompression.py compressed.bin > decompressed.txt
"""

import sys
from io import BytesIO
from pathlib import Path
from typing import BinaryIO

# Add src directory to Python path so we can import tdd_ai_py
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tdd_ai_py.decompressor import HuffmanDecompressor  # noqa: E402


def main() -> None:
    """Main function to decompress a file and output to stdout."""
    if len(sys.argv) != 2:
        print(
            "Usage: python huffman_decompression.py <compressed_file>",
            file=sys.stderr,
        )
        sys.exit(1)

    input_filename = sys.argv[1]

    try:
        # Open input file in binary mode and read into BytesIO
        with open(input_filename, "rb") as input_file:
            compressed_data = input_file.read()
            input_stream = BytesIO(compressed_data)

            # Use stdout in binary mode for decompressed output
            output_stream: BinaryIO = sys.stdout.buffer

            # Create decompressor and decompress the file
            decompressor = HuffmanDecompressor()
            decompressor.decompress(input_stream, output_stream)

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
