from io import BytesIO
from typing import List

import pytest

from tdd_ai_py.decompressor import HuffmanDecompressor

from .test_helpers import bits_and_bytes


def _bits_to_bytes(bit_string: str) -> bytes:
    """Convert bit string to bytes with padding."""
    bit_list, _ = bits_and_bytes(bit_string)
    # Pad to byte boundary
    while len(bit_list) % 8 != 0:
        bit_list.append(0)

    byte_values: List[int] = []
    for i in range(0, len(bit_list), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bit_list[i + j]
        byte_values.append(byte)
    return bytes(byte_values)


def _create_test_data(
    length: int, tree_bits: str, data_bits: str = ""
) -> bytes:
    """Create test data with length header and bit content."""
    length_bytes = length.to_bytes(4, byteorder="big")
    content_bytes = _bits_to_bytes(tree_bits + data_bits)
    return length_bytes + content_bytes


class TestDecompressor:
    @pytest.mark.parametrize(
        "length, tree_bits, data_bits, expected_char, expected_left_char, expected_decoded",
        [
            # Single character 'a': Tree "101100001" (9 bits) + data "000000" (6 bits for "aaaaaa")
            (6, "101100001", "000000", ord("a"), None, b"aaaaaa"),
            # Two symbols 'a'/'b': Tree "0" + "1" + "01100001" + "1" + "01100010" (19 bits)
            (12, "0101100001101100010", "000111001101", None, ord("a"), None),
        ],
        ids=["single_character", "two_symbols"],
    )
    def test_decompresses_data(
        self,
        length: int,
        tree_bits: str,
        data_bits: str,
        expected_char: int | None,
        expected_left_char: int | None,
        expected_decoded: bytes | None,
    ) -> None:
        """Test decompression of various tree structures."""
        data_bytes = _create_test_data(length, tree_bits, data_bits)

        data_stream = BytesIO(data_bytes)
        output_stream = BytesIO()
        decompressor = HuffmanDecompressor()

        decompressor.decompress(data_stream, output_stream)

        # Verify length reading
        assert decompressor.get_length() == length

        # Verify tree deserialization
        tree = decompressor.get_tree()

        if tree.is_leaf:
            assert tree.character == expected_char
            # Test the new decode functionality
            decoded_data = output_stream.getvalue()
            assert decoded_data == expected_decoded
        else:
            assert tree.character == expected_char
            assert tree.left is not None
            assert tree.right is not None
            assert tree.left.character == expected_left_char
            assert tree.right.character == ord("b")
