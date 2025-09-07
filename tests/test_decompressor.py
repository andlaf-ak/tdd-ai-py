from io import BytesIO
from typing import List

from tdd_ai_py.decompressor import Decompressor

from .test_helpers import bits


class TestDecompressor:
    def test_reads_serialized_tree_for_single_character(self) -> None:
        # Length (4 bytes) + serialized tree for 'a' (9 bits = 2 bytes with padding)
        # Tree: "101100001" for character 'a'
        # 10110000 = 0xB0, 1 padded to 10000000 = 0x80
        data_stream = BytesIO(b"\x00\x00\x00\x01\xB0\x80")
        decompressor = Decompressor()

        decompressor.decompress(data_stream)

        # Verify length reading
        assert decompressor.get_length() == 1

        # Verify tree deserialization
        tree = decompressor.get_tree()
        assert tree.is_leaf
        assert tree.character == "a"

    def test_decompresses_two_symbol_sequence(self) -> None:
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
        data_stream = BytesIO(b"\x00\x00\x00\x0C" + tree_and_data_bytes)
        decompressor = Decompressor()

        decompressor.decompress(data_stream)

        # Verify length reading
        assert decompressor.get_length() == 12

        # Verify tree deserialization
        tree = decompressor.get_tree()
        assert not tree.is_leaf  # Should be internal node for two symbols
        assert tree.left is not None
        assert tree.right is not None
        assert tree.left.character == "a"
        assert tree.right.character == "b"
