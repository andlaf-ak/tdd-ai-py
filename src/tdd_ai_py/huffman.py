"""Huffman compression algorithm implementation."""

from collections import Counter
from typing import Dict


class HuffmanCompressor:
    """A class for Huffman compression and decompression."""

    def create_frequency_map(self, text: str) -> Dict[str, int]:
        """Create a frequency map from input text.

        Args:
            text: The input string to analyze

        Returns:
            A dictionary mapping characters to their frequencies
        """
        return dict(Counter(text))
