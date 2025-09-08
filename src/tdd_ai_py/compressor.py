from typing import BinaryIO, Dict, List

from .bit_writer import BitWriter
from .frequency_counter import create_frequency_map
from .huffman_encoder import generate_huffman_codes
from .huffman_tree_builder import build_huffman_tree
from .stream_utils import iter_bytes
from .tree_serializer import serialize_tree


def _write_header(
    frequency_map: Dict[int, int], output_stream: BinaryIO
) -> int:
    """Write compression header (length) and return it."""
    length = sum(frequency_map.values())
    output_stream.write(length.to_bytes(4, byteorder="big"))
    return length


def _build_and_serialize_tree(
    frequency_map: Dict[int, int], bit_writer: BitWriter
) -> Dict[int, List[int]]:
    """Build Huffman tree, serialize it, and return codes."""
    huffman_tree = build_huffman_tree(frequency_map)
    serialized_tree = serialize_tree(huffman_tree)
    codes = generate_huffman_codes(huffman_tree)

    for bit in serialized_tree:
        bit_writer.write_bit(bit)

    return codes


def _encode_data(
    input_stream: BinaryIO, codes: Dict[int, List[int]], bit_writer: BitWriter
) -> None:
    """Encode input data using Huffman codes."""
    input_stream.seek(0)
    for byte_value in iter_bytes(input_stream):
        code = codes[byte_value]
        for bit in code:
            bit_writer.write_bit(bit)
    bit_writer.flush()


def compress(input_stream: BinaryIO, output_stream: BinaryIO) -> None:
    """Pure function for Huffman compression using functional pipeline.

    Args:
        input_stream: Source data to compress
        output_stream: Destination for compressed data
    """
    # Functional pipeline approach
    frequency_map = create_frequency_map(input_stream)

    # Write header
    _write_header(frequency_map, output_stream)

    # Create bit writer and process tree and data
    bit_writer = BitWriter(output_stream)
    codes = _build_and_serialize_tree(frequency_map, bit_writer)
    _encode_data(input_stream, codes, bit_writer)


# Legacy class wrapper for backward compatibility
class HuffmanCompressor:
    def compress(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        compress(input_stream, output_stream)
