"""Tests for the bit writer module."""

from io import BytesIO

import pytest

from tdd_ai_py.compression.bit_writer import BitWriter


class TestBitWriter:
    """Test cases for the BitWriter component."""

    @pytest.mark.parametrize(
        "bit_count, expected_bytes",
        [
            (1, bytes([128])),  # 1 bit: 10000000 -> 128
            (8, bytes([255])),  # 8 bits: 11111111 -> 255
            (9, bytes([255, 128])),  # 9 bits: 11111111 + 10000000 -> 255, 128
            (
                17,
                bytes([255, 255, 128]),
            ),  # 17 bits: 11111111 + 11111111 + 10000000 -> 255, 255, 128
        ],
    )
    def test_writes_bits_to_output_stream(self, bit_count: int, expected_bytes: bytes) -> None:
        """Test that BitWriter writes correct bytes to stream for different bit counts."""
        output_stream = BytesIO()
        writer = BitWriter(output_stream)

        # Write the specified number of '1' bits
        for _ in range(bit_count):
            writer.write_bit(1)

        writer.flush()

        # Check that correct bytes were written to stream
        output_stream.seek(0)
        result = output_stream.read()
        assert result == expected_bytes
