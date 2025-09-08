import struct
from io import BytesIO
from typing import BinaryIO, Optional, cast

from .bit_reader import BitReader
from .data_decoder import decode_data
from .huffman_tree_builder import HuffmanNode
from .tree_deserializer import deserialize_tree


class HuffmanDecompressor:
    def __init__(self) -> None:
        self._length: Optional[int] = None
        self._tree: Optional[HuffmanNode] = None

    def decompress(
        self, input_stream: BytesIO, output_stream: BinaryIO
    ) -> None:
        self._length = self._read_big_endian_int(input_stream)

        bit_reader = BitReader(input_stream)
        self._tree = deserialize_tree(bit_reader)

        decode_data(self._tree, bit_reader, self._length, output_stream)

    def _read_big_endian_int(self, stream: BytesIO) -> int:
        bytes_data: bytes = stream.read(4)
        return cast(int, struct.unpack(">I", bytes_data)[0])
