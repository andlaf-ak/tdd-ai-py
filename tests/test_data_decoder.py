from io import BytesIO
from typing import Callable

import pytest

from tdd_ai_py.bit_reader import BitReader
from tdd_ai_py.data_decoder import decode_data
from tdd_ai_py.huffman_tree_builder import HuffmanNode


def _create_single_character_tree() -> HuffmanNode:
    return HuffmanNode(weight=1, character="a")


def _create_two_character_tree() -> HuffmanNode:
    left_a = HuffmanNode(weight=1, character="a")
    right_b = HuffmanNode(weight=1, character="b")
    return HuffmanNode(weight=2, left=left_a, right=right_b)


def _create_three_character_tree() -> HuffmanNode:
    left_a = HuffmanNode(weight=1, character="a")
    right_internal_left_b = HuffmanNode(weight=1, character="b")
    right_internal_right_c = HuffmanNode(weight=1, character="c")
    right_internal = HuffmanNode(
        weight=2, left=right_internal_left_b, right=right_internal_right_c
    )
    return HuffmanNode(weight=3, left=left_a, right=right_internal)


class TestDataDecoder:
    @pytest.mark.parametrize(
        "tree_builder, data_bytes, length, expected",
        [
            (
                _create_single_character_tree,
                b"\x00",
                1,
                "a",
            ),  # "0" padded to "00000000"
            (_create_two_character_tree, b"\x63", 8, "abbaaabb"),  # "01100011"
            (
                _create_three_character_tree,
                b"\xBB\x20",
                7,
                "bcbcaab",
            ),  # "101110110010" + padding
            (
                _create_three_character_tree,
                b"\xBB\x20",  # "1011101100100000"
                7,
                "bcbcaab",
            ),
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
        data_bytes: bytes,
        length: int,
        expected: str,
    ) -> None:
        tree = tree_builder()
        bit_reader = BitReader(BytesIO(data_bytes))
        result = decode_data(tree, bit_reader, length)
        assert result == expected
