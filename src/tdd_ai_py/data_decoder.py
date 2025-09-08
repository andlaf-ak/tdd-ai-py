from itertools import islice
from typing import BinaryIO, Iterator, cast

from .bit_reader import BitReader
from .huffman_tree_builder import HuffmanNode


def decode_data(
    root: HuffmanNode,
    bit_reader: BitReader,
    length: int,
    output_stream: BinaryIO,
) -> None:
    characters = (
        [root.character] * length
        if root.is_leaf and root.character is not None
        else list(islice(decode_characters(root, bit_reader), length))
    )
    output_stream.write(bytes(characters))


def decode_characters(root: HuffmanNode, bit_reader: BitReader) -> Iterator[int]:
    """Decode characters from bit stream using Huffman tree."""

    def get_character() -> int:
        node = root
        while not node.is_leaf:
            bit = bit_reader.read_bit()
            node = cast(HuffmanNode, node.left if bit == 0 else node.right)
        return cast(int, node.character)

    try:
        while True:
            yield get_character()
    except (EOFError, IndexError):
        pass


def validate_and_extract_character(node: HuffmanNode) -> int:
    """Pure function to validate and extract character from leaf node."""
    if node.character is None:
        raise ValueError("Leaf node must have a character")
    return node.character
