from io import BytesIO


class BitReader:
    def __init__(self, input_stream: BytesIO):
        self._input_stream = input_stream
        self._buffer = 0
        self._bits_in_buffer = 0

    def read_bit(self) -> int:
        if self._needs_new_byte():
            self._load_next_byte()

        return self._extract_next_bit()

    def _needs_new_byte(self) -> bool:
        return self._bits_in_buffer == 0

    def _load_next_byte(self) -> None:
        byte_data = self._input_stream.read(1)
        self._buffer = byte_data[0]
        self._bits_in_buffer = 8

    def _extract_next_bit(self) -> int:
        bit = (self._buffer >> 7) & 1
        self._buffer = (self._buffer << 1) & 0xFF
        self._bits_in_buffer -= 1
        return bit
