"""Frequency analysis module for character frequency mapping."""

from collections import Counter
from typing import Dict


def create_frequency_map(text: str) -> Dict[str, int]:
    """Create a frequency map from input text.

    Pure function that analyzes text and returns character frequencies.

    Args:
        text: The input string to analyze

    Returns:
        A dictionary mapping characters to their frequencies
    """
    return dict(Counter(text))
