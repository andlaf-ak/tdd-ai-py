import struct
from io import BytesIO
from typing import BinaryIO, cast

from .bit_reader import BitReader
from .data_decoder import decode_data
from .tree_deserializer import deserialize_tree


def read_big_endian_int(stream: BytesIO) -> int:
    """Read a 4-byte big-endian integer from stream."""
    return cast(int, struct.unpack(">I", stream.read(4))[0])


class HuffmanDecompressor:
    def decompress(self, input_stream: BytesIO, output_stream: BinaryIO) -> None:
        length = read_big_endian_int(input_stream)
        bit_reader = BitReader(input_stream)
        tree = deserialize_tree(bit_reader)
        decode_data(tree, bit_reader, length, output_stream)
