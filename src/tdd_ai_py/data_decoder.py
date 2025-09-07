from typing import BinaryIO

from .bit_reader import BitReader
from .huffman_tree_builder import HuffmanNode


def decode_data(
    root: HuffmanNode,
    bit_reader: BitReader,
    length: int,
    output_stream: BinaryIO,
) -> None:
    if root.is_leaf:
        _decode_single_character_data(root, length, output_stream)
    else:
        _decode_multi_character_data(root, bit_reader, length, output_stream)


def _decode_single_character_data(
    root: HuffmanNode, length: int, output_stream: BinaryIO
) -> None:
    _validate_leaf_has_character(root)
    assert root.character is not None  # After validation, we know it's not None
    data = bytes([root.character] * length)
    output_stream.write(data)


def _decode_multi_character_data(
    root: HuffmanNode,
    bit_reader: BitReader,
    length: int,
    output_stream: BinaryIO,
) -> None:
    decoder = _CompressedDataDecoder(root, length, output_stream)
    decoder.decode(bit_reader)


class _CompressedDataDecoder:
    def __init__(self, root: HuffmanNode, length: int, output_stream: BinaryIO):
        self._root = root
        self._length = length
        self._current_node = root
        self._output_stream = output_stream
        self._characters_decoded = 0

    def decode(self, bit_reader: BitReader) -> None:
        while not self._should_stop_decoding():
            try:
                bit = bit_reader.read_bit()
                self._process_bit(bit)
            except (IndexError, EOFError):
                # End of stream reached
                break

    def _should_stop_decoding(self) -> bool:
        return self._characters_decoded == self._length

    def _process_bit(self, bit: int) -> None:
        self._current_node = _traverse_tree(self._current_node, bit)
        if self._current_node.is_leaf:
            self._add_decoded_character()
            self._reset_to_root()

    def _add_decoded_character(self) -> None:
        _validate_leaf_has_character(self._current_node)
        assert (
            self._current_node.character is not None
        )  # After validation, we know it's not None
        self._output_stream.write(bytes([self._current_node.character]))
        self._characters_decoded += 1

    def _reset_to_root(self) -> None:
        self._current_node = self._root


def _validate_leaf_has_character(node: HuffmanNode) -> None:
    if node.character is None:
        raise ValueError("Leaf node must have a character")


def _traverse_tree(node: HuffmanNode, bit: int) -> HuffmanNode:
    if bit == 0:
        if node.left is None:
            raise ValueError("Invalid tree structure: missing left child")
        return node.left
    if node.right is None:
        raise ValueError("Invalid tree structure: missing right child")
    return node.right
