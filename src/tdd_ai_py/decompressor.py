import struct
from io import BytesIO
from typing import Optional, cast

from .bit_reader import BitReader
from .data_decoder import decode_data
from .huffman_tree_builder import HuffmanNode
from .tree_deserializer import deserialize_tree


class Decompressor:
    def __init__(self) -> None:
        self._length: Optional[int] = None
        self._tree: Optional[HuffmanNode] = None
        self._decoded_data: Optional[bytes] = None

    def decompress(self, data_stream: BytesIO) -> None:
        self._length = self._read_big_endian_int(data_stream)

        bit_reader = BitReader(data_stream)
        self._tree = deserialize_tree(bit_reader)

        self._decoded_data = decode_data(self._tree, bit_reader, self._length)

    def get_length(self) -> int:
        assert self._length is not None
        return self._length

    def get_tree(self) -> HuffmanNode:
        assert self._tree is not None
        return self._tree

    def get_decoded_data(self) -> bytes:
        assert self._decoded_data is not None
        return self._decoded_data

    def _read_big_endian_int(self, stream: BytesIO) -> int:
        bytes_data: bytes = stream.read(4)
        return cast(int, struct.unpack(">I", bytes_data)[0])
