from io import BytesIO
from typing import Callable, List, Tuple

import pytest

from tdd_ai_py.decompressor import Decompressor

from .test_helpers import bits


def _create_single_character_test_data() -> (
    Tuple[bytes, int, bool, str | None, str | None]
):
    """Create test data for single character 'a' tree."""
    # Length (4 bytes) + serialized tree for 'a' (9 bits = 2 bytes with padding)
    # Tree: "101100001" for character 'a'
    # 10110000 = 0xB0, 1 padded to 10000000 = 0x80
    data_bytes = b"\x00\x00\x00\x01\xB0\x80"
    expected_length = 1
    expected_is_leaf = True
    expected_character = "a"
    expected_left_character = None
    return (
        data_bytes,
        expected_length,
        expected_is_leaf,
        expected_character,
        expected_left_character,
    )


def _create_two_symbol_test_data() -> (
    Tuple[bytes, int, bool, str | None, str | None]
):
    """Create test data for two symbol 'a'/'b' tree."""
    # Length (4 bytes) + tree for 'a'/'b' + encoded "aaabbbaabbab"
    # Tree: "0" + "1" + "01100001" + "1" + "01100010" (19 bits)
    # Sequence "aaabbbaabbab" with codes a=0, b=1: "000111001101" (12 bits)
    # Total: 31 bits padded to 32 bits = 4 bytes
    tree_bits = "0" + "1" + "01100001" + "1" + "01100010"  # 19 bits
    data_bits = "000111001101"  # 12 bits for "aaabbbaabbab"
    combined_bits = tree_bits + data_bits + "0"  # 32 bits with padding

    # Convert to bytes using bits() helper
    combined_bit_list = bits(combined_bits)
    bit_chunks = [combined_bit_list[i : i + 8] for i in range(0, 32, 8)]
    byte_values: List[int] = []
    for chunk in bit_chunks:
        byte = 0
        for bit in chunk:
            byte = (byte << 1) | bit
        byte_values.append(byte)
    tree_and_data_bytes = bytes(byte_values)

    # Length (12) + tree and data bytes
    data_bytes = b"\x00\x00\x00\x0C" + tree_and_data_bytes
    expected_length = 12
    expected_is_leaf = False
    expected_character = None
    expected_left_character = "a"
    return (
        data_bytes,
        expected_length,
        expected_is_leaf,
        expected_character,
        expected_left_character,
    )


class TestDecompressor:
    @pytest.mark.parametrize(
        "test_data_func, test_description",
        [
            (_create_single_character_test_data, "single_character"),
            (_create_two_symbol_test_data, "two_symbols"),
        ],
        ids=["single_character", "two_symbols"],
    )
    def test_decompresses_data(
        self,
        test_data_func: Callable[
            [], Tuple[bytes, int, bool, str | None, str | None]
        ],
        test_description: str,
    ) -> None:
        """Test decompression of various tree structures."""
        (
            data_bytes,
            expected_length,
            expected_is_leaf,
            expected_character,
            expected_left_character,
        ) = test_data_func()

        data_stream = BytesIO(data_bytes)
        decompressor = Decompressor()

        decompressor.decompress(data_stream)

        # Verify length reading
        assert decompressor.get_length() == expected_length

        # Verify tree deserialization
        tree = decompressor.get_tree()
        assert tree.is_leaf == expected_is_leaf

        if expected_is_leaf:
            # Single character tree
            assert tree.character == expected_character
        else:
            # Multi-symbol tree
            assert tree.character == expected_character
            assert tree.left is not None
            assert tree.right is not None
            assert tree.left.character == expected_left_character
            assert tree.right.character == "b"
