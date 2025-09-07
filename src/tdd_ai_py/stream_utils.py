from typing import BinaryIO, Iterator


def iter_bytes(input_stream: BinaryIO) -> Iterator[int]:
    """Iterate over bytes from a binary stream.

    Yields each byte value as an integer.
    """
    while True:
        byte_data = input_stream.read(1)
        if not byte_data:
            break
        yield byte_data[0]
