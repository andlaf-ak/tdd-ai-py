from typing import BinaryIO, TextIO

from .bit_writer import BitWriter
from .frequency_counter import create_frequency_map
from .huffman_encoder import generate_huffman_codes
from .huffman_tree_builder import build_huffman_tree
from .tree_serializer import serialize_tree


class StreamCompressor:
    def compress(self, input_stream: TextIO, output_stream: BinaryIO) -> None:
        text = input_stream.read()

        length = len(text)
        output_stream.write(length.to_bytes(4, byteorder="big"))

        frequency_map = create_frequency_map(text)
        huffman_tree = build_huffman_tree(frequency_map)

        serialized_tree = serialize_tree(huffman_tree)
        codes = generate_huffman_codes(huffman_tree)

        bit_writer = BitWriter(output_stream)

        for bit_char in serialized_tree:
            bit_writer.write_bit(int(bit_char))

        for char in text:
            code = codes[char]
            for bit_char in code:
                bit_writer.write_bit(int(bit_char))

        bit_writer.flush()
