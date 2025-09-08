from typing import BinaryIO, Iterator


def bits_from_stream(input_stream: BinaryIO) -> Iterator[int]:
    """Generate bits from a byte stream."""
    while True:
        byte_data = input_stream.read(1)
        if not byte_data:
            return
        byte_value = byte_data[0]
        for i in range(8):
            yield (byte_value >> (7 - i)) & 1


class BitReader:
    def __init__(self, input_stream: BinaryIO):
        self._bits = bits_from_stream(input_stream)

    def read_bit(self) -> int:
        try:
            return next(self._bits)
        except StopIteration as exc:
            raise EOFError("No more data available") from exc
