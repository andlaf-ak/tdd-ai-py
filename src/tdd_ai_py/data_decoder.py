from .bit_reader import BitReader
from .huffman_tree_builder import HuffmanNode


def decode_data(root: HuffmanNode, bit_reader: BitReader, length: int) -> bytes:
    if root.is_leaf:
        return _decode_single_character_data(root, length)

    return _decode_multi_character_data(root, bit_reader, length)


def _decode_single_character_data(root: HuffmanNode, length: int) -> bytes:
    _validate_leaf_has_character(root)
    assert root.character is not None  # After validation, we know it's not None
    return bytes([root.character] * length)


def _decode_multi_character_data(
    root: HuffmanNode, bit_reader: BitReader, length: int
) -> bytes:
    decoder = _CompressedDataDecoder(root, length)
    return decoder.decode(bit_reader)


class _CompressedDataDecoder:
    def __init__(self, root: HuffmanNode, length: int):
        self._root = root
        self._length = length
        self._current_node = root
        self._result: list[int] = []
        self._characters_decoded = 0

    def decode(self, bit_reader: BitReader) -> bytes:
        while not self._should_stop_decoding():
            try:
                bit = bit_reader.read_bit()
                self._process_bit(bit)
            except (IndexError, EOFError):
                # End of stream reached
                break
        return bytes(self._result)

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
        self._result.append(self._current_node.character)
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
