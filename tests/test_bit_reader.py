from io import BytesIO

from tdd_ai_py.decompression.bit_reader import BitReader


class TestBitReader:
    def test_reads_single_bit_from_stream(self) -> None:
        input_stream = BytesIO(b"a")
        bit_reader = BitReader(input_stream)

        result = bit_reader.read_bit()

        # 'a' = ASCII 97 = 01100001 in binary, MSB is 0
        assert result == 0
