"""Tests for compressed data decoder that traverses tree using bits."""

from typing import Callable

import pytest

from tdd_ai_py.compressed_data_decoder import decode_compressed_data
from tdd_ai_py.huffman_tree_builder import HuffmanNode


def _create_single_character_tree() -> HuffmanNode:
    """Create tree with single character 'a'."""
    return HuffmanNode(weight=1, character="a")


def _create_two_character_tree() -> HuffmanNode:
    """Create binary tree with 'a' (left) and 'b' (right)."""
    left_a = HuffmanNode(weight=1, character="a")
    right_b = HuffmanNode(weight=1, character="b")
    return HuffmanNode(weight=2, left=left_a, right=right_b)


def _create_three_character_tree() -> HuffmanNode:
    """Create complex tree with 'a' (0), 'b' (10), 'c' (11)."""
    left_a = HuffmanNode(weight=1, character="a")
    right_internal_left_b = HuffmanNode(weight=1, character="b")
    right_internal_right_c = HuffmanNode(weight=1, character="c")
    right_internal = HuffmanNode(
        weight=2, left=right_internal_left_b, right=right_internal_right_c
    )
    return HuffmanNode(weight=3, left=left_a, right=right_internal)


class TestCompressedDataDecoder:
    """Test cases for compressed data decoder algorithm."""

    @pytest.mark.parametrize(
        "tree_builder, bits, length, expected",
        [
            (_create_single_character_tree, "0", 1, "a"),
            (_create_two_character_tree, "01100011", 8, "abbaaabb"),
            (_create_three_character_tree, "101110110010", 7, "bcbcaab"),
            (_create_three_character_tree, "1011101100100000", 7, "bcbcaab"),
        ],
        ids=[
            "single_character",
            "two_characters",
            "three_characters",
            "with_length_limit",
        ],
    )
    def test_decodes_compressed_data(
        self,
        tree_builder: Callable[[], HuffmanNode],
        bits: str,
        length: int,
        expected: str,
    ) -> None:
        """Test compressed data decoding for various scenarios."""
        tree = tree_builder()
        result = decode_compressed_data(tree, bits, length)
        assert result == expected
