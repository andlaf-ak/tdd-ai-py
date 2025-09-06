"""Tests for bit writer component that buffers bits and emits bytes."""

from io import BytesIO

from tdd_ai_py.bit_writer import BitWriter


class TestBitWriter:
    """Test cases for the BitWriter component."""

    def test_writes_single_bit_and_flushes_to_byte(self) -> None:
        """Test writing single bit '1' and flushing produces byte 10000000."""
        output_stream = BytesIO()
        writer = BitWriter(output_stream)

        writer.write_bit(1)
        writer.flush()

        # Check that byte was written to stream with pattern 10000000 (128)
        output_stream.seek(0)
        result = output_stream.read()
        assert result == bytes([128])

    def test_writes_bits_to_output_stream(self) -> None:
        """Test that BitWriter writes bytes directly to an output stream."""
        output_stream = BytesIO()
        writer = BitWriter(output_stream)

        writer.write_bit(1)
        writer.flush()

        # Check that byte was written to stream, not returned
        output_stream.seek(0)
        result = output_stream.read()
        assert result == bytes([128])
