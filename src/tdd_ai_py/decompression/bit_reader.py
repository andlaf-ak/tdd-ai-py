from typing import BinaryIO, Iterator


def bits_from_stream(input_stream: BinaryIO, buffer_size: int = 8192) -> Iterator[int]:
    """Generate bits from a byte stream using buffered reads for efficiency."""
    while True:
        buffer = input_stream.read(buffer_size)
        if not buffer:
            return
        for byte_value in buffer:
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
