from itertools import islice
from typing import BinaryIO, Iterator, List


def chunk_bits(bits: Iterator[int], size: int = 8) -> Iterator[List[int]]:
    """Chunk bits into groups of specified size."""
    bit_iter = iter(bits)
    while True:
        chunk = list(islice(bit_iter, size))
        if not chunk:
            break
        yield chunk


def bits_to_byte(bit_chunk: List[int]) -> int:
    """Convert a list of bits to a single byte value."""
    padded_bits = bit_chunk + [0] * (8 - len(bit_chunk))
    return sum(bit << (7 - i) for i, bit in enumerate(padded_bits))


def bits_to_bytes(bits: Iterator[int]) -> Iterator[int]:
    """Convert a stream of bits into complete bytes."""
    return (bits_to_byte(chunk) for chunk in chunk_bits(bits))


class BitWriter:
    def __init__(self, output_stream: BinaryIO) -> None:
        self._output_stream = output_stream
        self._bits: List[int] = []

    def write_bit(self, bit: int) -> None:
        self._bits.append(bit & 1)

    def flush(self) -> None:
        byte_data = bytes(bits_to_bytes(iter(self._bits)))
        self._output_stream.write(byte_data)
        self._bits.clear()
