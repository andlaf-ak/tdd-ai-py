from io import BytesIO

from tdd_ai_py.decompressor import Decompressor


class TestDecompressor:
    def test_reads_4_byte_length_from_input_stream(self) -> None:
        input_stream = BytesIO(b"\x00\x00\x00\x07")
        decompressor = Decompressor(input_stream)

        length = decompressor.read_length()

        assert length == 7
