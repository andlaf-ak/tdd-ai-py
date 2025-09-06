"""Tests for bit writer component that buffers bits and emits bytes."""

from tdd_ai_py.bit_writer import BitWriter


class TestBitWriter:
    """Test cases for the BitWriter component."""

    def test_writes_single_bit_and_flushes_to_byte(self) -> None:
        """Test writing single bit '1' and flushing produces byte 10000000."""
        writer = BitWriter()

        writer.write_bit(1)
        result = writer.flush()

        # After writing bit '1' and flushing, expect byte with pattern 10000000 (128)
        assert result == bytes([128])
