from typing import BinaryIO, Iterator


def iter_bytes(input_stream: BinaryIO, buffer_size: int = 8192) -> Iterator[int]:
    """Iterate over bytes from a binary stream using buffered reads.

    Yields each byte value as an integer.
    """
    while True:
        buffer = input_stream.read(buffer_size)
        if not buffer:
            break
        yield from buffer
