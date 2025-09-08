from .bit_reader import BitReader
from .huffman_tree_builder import HuffmanNode


def deserialize_tree(bit_reader: BitReader) -> HuffmanNode:
    return (
        HuffmanNode(weight=0, character=sum(bit_reader.read_bit() << (7 - i) for i in range(8)))
        if bit_reader.read_bit() == 1
        else HuffmanNode(weight=0, left=deserialize_tree(bit_reader), right=deserialize_tree(bit_reader))
    )
