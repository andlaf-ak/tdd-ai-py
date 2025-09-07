from io import BytesIO
from typing import Callable, List

import pytest

from tdd_ai_py.bit_reader import BitReader
from tdd_ai_py.huffman_tree_builder import HuffmanNode
from tdd_ai_py.tree_deserializer import deserialize_tree

from .test_helpers import bits_and_bytes


def _bits_to_byte_stream(bit_list: List[int]) -> BytesIO:
    """Convert list of bits to BytesIO stream, padding to byte boundary."""
    # Pad to byte boundary
    padded_bits = bit_list[:]
    while len(padded_bits) % 8 != 0:
        padded_bits.append(0)

    # Convert to bytes
    byte_values: List[int] = []
    for i in range(0, len(padded_bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | padded_bits[i + j]
        byte_values.append(byte)

    return BytesIO(bytes(byte_values))


def _validate_single_leaf(node: HuffmanNode, expected_char: str) -> None:
    assert node.character == expected_char
    assert node.weight == 0
    assert node.left is None
    assert node.right is None
    assert node.is_leaf


def _validate_binary_tree(
    node: HuffmanNode, left_char: str, right_char: str
) -> None:
    # Root should be internal node
    assert node.character is None
    assert node.weight == 0
    assert not node.is_leaf
    assert node.left is not None
    assert node.right is not None

    # Validate children
    assert node.left.character == left_char
    assert node.left.is_leaf
    assert node.right.character == right_char
    assert node.right.is_leaf


def _validate_complex_tree(node: HuffmanNode) -> None:
    # Root should be internal node
    assert node.character is None
    assert not node.is_leaf
    assert node.left is not None
    assert node.right is not None

    # Left child should be 'a'
    assert node.left.character == "a"
    assert node.left.is_leaf

    # Right child should be internal node
    right_internal = node.right
    assert right_internal.character is None
    assert not right_internal.is_leaf
    assert right_internal.left is not None
    assert right_internal.right is not None

    # Right internal's children should be 'b' and 'c'
    assert right_internal.left.character == "b"
    assert right_internal.left.is_leaf
    assert right_internal.right.character == "c"
    assert right_internal.right.is_leaf


def _validate_single_a(node: HuffmanNode) -> None:
    _validate_single_leaf(node, "a")


def _validate_binary_ab(node: HuffmanNode) -> None:
    _validate_binary_tree(node, "a", "b")


class TestTreeDeserializer:
    @pytest.mark.parametrize(
        "serialized_tree, validator",
        [
            (bits_and_bytes("1" + "01100001")[0], _validate_single_a),
            (
                bits_and_bytes("0" + "1" + "01100001" + "1" + "01100010")[0],
                _validate_binary_ab,
            ),
            (
                bits_and_bytes(
                    "0"
                    + "1"
                    + "01100001"
                    + "0"
                    + "1"
                    + "01100010"
                    + "1"
                    + "01100011"
                )[0],
                _validate_complex_tree,
            ),
        ],
        ids=["single_leaf", "binary_tree", "complex_tree"],
    )
    def test_deserializes_tree(
        self,
        serialized_tree: List[int],
        validator: Callable[[HuffmanNode], None],
    ) -> None:
        byte_stream = _bits_to_byte_stream(serialized_tree)
        bit_reader = BitReader(byte_stream)
        result = deserialize_tree(bit_reader)
        validator(result)
