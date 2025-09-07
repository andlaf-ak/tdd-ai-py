import struct
from io import BytesIO
from typing import cast


class Decompressor:
    def __init__(self, input_stream: BytesIO):
        self._input_stream = input_stream

    def read_length(self) -> int:
        return self._read_big_endian_int()

    def _read_big_endian_int(self) -> int:
        bytes_data: bytes = self._input_stream.read(4)
        return cast(int, struct.unpack(">I", bytes_data)[0])
