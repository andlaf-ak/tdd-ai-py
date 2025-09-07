from io import BytesIO
from typing import Callable

import pytest

from tdd_ai_py.bit_reader import BitReader
from tdd_ai_py.data_decoder import decode_data
from tdd_ai_py.huffman_tree_builder import HuffmanNode

from .test_helpers import bits_and_bytes


def _create_single_character_tree() -> HuffmanNode:
    return HuffmanNode(weight=1, character=ord("a"))


def _create_two_character_tree() -> HuffmanNode:
    left_a = HuffmanNode(weight=1, character=ord("a"))
    right_b = HuffmanNode(weight=1, character=ord("b"))
    return HuffmanNode(weight=2, left=left_a, right=right_b)


def _create_three_character_tree() -> HuffmanNode:
    left_a = HuffmanNode(weight=1, character=ord("a"))
    right_internal_left_b = HuffmanNode(weight=1, character=ord("b"))
    right_internal_right_c = HuffmanNode(weight=1, character=ord("c"))
    right_internal = HuffmanNode(
        weight=2, left=right_internal_left_b, right=right_internal_right_c
    )
    return HuffmanNode(weight=3, left=left_a, right=right_internal)


class TestDataDecoder:
    @pytest.mark.parametrize(
        "tree_builder, data_bits, length, expected",
        [
            (_create_single_character_tree, "0", 1, b"a"),
            (_create_two_character_tree, "01100011", 8, b"abbaaabb"),
            (_create_three_character_tree, "101110110010", 7, b"bcbcaab"),
            (_create_three_character_tree, "101110110010", 7, b"bcbcaab"),
        ],
        ids=[
            "single_character",
            "two_characters",
            "three_characters",
            "with_length_limit",
        ],
    )
    def test_decodes_data(
        self,
        tree_builder: Callable[[], HuffmanNode],
        data_bits: str,
        length: int,
        expected: bytes,
    ) -> None:
        tree = tree_builder()
        _, data_bytes = bits_and_bytes(data_bits)
        bit_reader = BitReader(BytesIO(data_bytes))
        result = decode_data(tree, bit_reader, length)
        assert result == expected
