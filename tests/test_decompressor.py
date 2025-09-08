from io import BytesIO
from typing import List

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


def _create_test_data(length: int, tree_bits: str, data_bits: str = "") -> bytes:
    """Create test data with length header and bit content."""
    length_bytes = length.to_bytes(4, byteorder="big")
    content_bytes = _bits_to_bytes(tree_bits + data_bits)
    return length_bytes + content_bytes


class TestDecompressor:
    def test_decompresses_single_character(self) -> None:
        """Test decompression of single character data."""
        # Single character 'a': Tree "101100001" (9 bits) + data "000000" (6 bits for "aaaaaa")
        length = 6
        tree_bits = "101100001"
        data_bits = "000000"
        expected_decoded = b"aaaaaa"

        data_bytes = _create_test_data(length, tree_bits, data_bits)
        data_stream = BytesIO(data_bytes)
        output_stream = BytesIO()
        decompressor = HuffmanDecompressor()

        decompressor.decompress(data_stream, output_stream)

        # Verify the decompressed output matches expected result
        decoded_data = output_stream.getvalue()
        assert decoded_data == expected_decoded
        assert len(decoded_data) == length

    def test_decompressor_handles_empty_output_stream(self) -> None:
        """Test that decompressor works with fresh output stream."""
        # Simple test to verify the decompressor doesn't depend on removed methods
        length = 1
        tree_bits = "101100001"  # Single character 'a'
        data_bits = "0"  # Single 'a'

        data_bytes = _create_test_data(length, tree_bits, data_bits)
        data_stream = BytesIO(data_bytes)
        output_stream = BytesIO()
        decompressor = HuffmanDecompressor()

        # This should not raise any errors
        decompressor.decompress(data_stream, output_stream)

        decoded_data = output_stream.getvalue()
        assert len(decoded_data) == length
