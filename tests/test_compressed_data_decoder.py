"""Tests for compressed data decoder that traverses tree using bits."""

from tdd_ai_py.compressed_data_decoder import decode_compressed_data
from tdd_ai_py.huffman_tree_builder import HuffmanNode


class TestCompressedDataDecoder:
    """Test cases for compressed data decoder algorithm."""

    def test_decodes_single_bit_with_root_only_tree(self) -> None:
        """Test that bit '0' with root-only tree emits the root's character."""
        # Tree with only root node containing 'a'
        root = HuffmanNode(weight=1, character="a")

        result = decode_compressed_data(root)

        # Should emit the 8-bit ASCII for 'a' = 01100001
        expected = "01100001"
        assert result == expected
