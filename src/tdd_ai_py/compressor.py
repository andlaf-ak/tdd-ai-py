from itertools import chain
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
        codes = generate_huffman_codes(huffman_tree)

        # Write length and prepare bit stream
        output_stream.write(length.to_bytes(4, byteorder="big"))

        # Second pass: seek back to start and create all bits functionally
        input_stream.seek(0)
        all_bits = chain(serialize_tree(huffman_tree), *(codes[byte_value] for byte_value in iter_bytes(input_stream)))

        # Write all bits
        bit_writer = BitWriter(output_stream)
        for bit in all_bits:
            bit_writer.write_bit(bit)
        bit_writer.flush()
