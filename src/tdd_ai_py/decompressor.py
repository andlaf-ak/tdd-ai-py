import struct
from io import BytesIO
from typing import BinaryIO, cast

from .bit_reader import BitReader
from .data_decoder import decode_data
from .tree_deserializer import deserialize_tree


def _read_big_endian_int(stream: BytesIO) -> int:
    """Read a 4-byte big-endian integer from stream."""
    bytes_data: bytes = stream.read(4)
    return cast(int, struct.unpack(">I", bytes_data)[0])


def decompress(input_stream: BytesIO, output_stream: BinaryIO) -> None:
    """Pure function for Huffman decompression.

    Args:
        input_stream: Source compressed data
        output_stream: Destination for decompressed data
    """
    length = _read_big_endian_int(input_stream)

    bit_reader = BitReader(input_stream)
    tree = deserialize_tree(bit_reader)

    decode_data(tree, bit_reader, length, output_stream)


# Legacy class wrapper for backward compatibility
class HuffmanDecompressor:
    def decompress(
        self, input_stream: BytesIO, output_stream: BinaryIO
    ) -> None:
        decompress(input_stream, output_stream)
