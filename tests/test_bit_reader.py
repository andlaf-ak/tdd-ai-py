"""Tests for bit reader that reads bits from input stream."""

from io import StringIO

from tdd_ai_py.bit_reader import BitReader


class TestBitReader:
    """Test cases for bit reader algorithm."""

    def test_reads_single_bit_from_stream(self) -> None:
        """Test that bit reader reads most significant bit from 8-bit buffer."""
        input_stream = StringIO("a")
        bit_reader = BitReader(input_stream)

        result = bit_reader.read_bit()

        # 'a' = ASCII 97 = 01100001 in binary, MSB is 0
        assert result == 0
