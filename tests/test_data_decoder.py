from typing import Callable, List

import pytest

from tdd_ai_py.data_decoder import decode_data
from tdd_ai_py.huffman_tree_builder import HuffmanNode

from .test_helpers import bits


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
        "tree_builder, bits, length, expected",
        [
            (_create_single_character_tree, bits("0"), 1, "a"),
            (_create_two_character_tree, bits("01100011"), 8, "abbaaabb"),
            (_create_three_character_tree, bits("101110110010"), 7, "bcbcaab"),
            (
                _create_three_character_tree,
                bits("1011101100100000"),
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
        bits: List[int],
        length: int,
        expected: str,
    ) -> None:
        tree = tree_builder()
        result = decode_data(tree, bits, length)
        assert result == expected
