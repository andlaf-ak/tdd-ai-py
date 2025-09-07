from io import BytesIO

from tdd_ai_py.decompressor import Decompressor


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
