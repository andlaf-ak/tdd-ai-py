"""Tests for the Huffman compressor."""

from io import BytesIO, StringIO

from tdd_ai_py.compressor import HuffmanCompressor


class TestHuffmanCompressor:
    """Test cases for the HuffmanCompressor class."""

    def test_compresses_single_character_to_byte_stream(self) -> None:
        """Test that single character produces: length(4 bytes) + serialized tree + encoded data."""
        input_stream = StringIO("a")
        output_stream = BytesIO()
        compressor = HuffmanCompressor()

        compressor.compress(input_stream, output_stream)

        output_stream.seek(0)
        result = output_stream.read()

        # Expected format:
        # - First 4 bytes: length = 1 (0x00000001 in big-endian)
        # - Serialized tree: "1" + 8-bit 'a' = "101100001" (9 bits)
        # - Encoded data: "0" (1 bit, code for single character)
        # Total: 9 + 1 = 10 bits of tree+data, padded to 16 bits = 2 bytes
        # Tree+data bits: "1011000010" padded to "1011000010000000"
        expected = bytes(
            [0, 0, 0, 1]
        ) + bytes(  # Length: 1 (4 bytes, big-endian)
            [0xB0, 0x80]
        )  # "1011000010000000" = 0xB080
        assert result == expected
