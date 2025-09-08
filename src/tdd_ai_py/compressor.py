from typing import BinaryIO

from .bit_writer import BitWriter
from .frequency_counter import create_frequency_map
from .huffman_encoder import generate_huffman_codes
from .huffman_tree_builder import build_huffman_tree
from .stream_utils import iter_bytes
from .tree_serializer import serialize_tree


class HuffmanCompressor:
    def compress(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        # First pass: build frequency map by reading from stream
        frequency_map = create_frequency_map(input_stream)
        length = sum(frequency_map.values())

        huffman_tree = build_huffman_tree(frequency_map)

        # Write length and tree serialization
        output_stream.write(length.to_bytes(4, byteorder="big"))
        serialized_tree = serialize_tree(huffman_tree)
        codes = generate_huffman_codes(huffman_tree)

        bit_writer = BitWriter(output_stream)

        for bit in serialized_tree:
            bit_writer.write_bit(bit)

        # Second pass: seek back to start and encode the input
        input_stream.seek(0)
        for byte_value in iter_bytes(input_stream):
            code = codes[byte_value]
            for bit in code:
                bit_writer.write_bit(bit)

        bit_writer.flush()
