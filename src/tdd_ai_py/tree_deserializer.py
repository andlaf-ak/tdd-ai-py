from .bit_reader import BitReader
from .huffman_tree_builder import HuffmanNode


def deserialize_tree(bit_reader: BitReader) -> HuffmanNode:
    node_type_bit = bit_reader.read_bit()

    if node_type_bit == 1:
        # Leaf node: read 8-bit value
        byte_value = 0
        for _ in range(8):
            bit = bit_reader.read_bit()
            byte_value = (byte_value << 1) | bit
        return HuffmanNode(weight=0, character=byte_value)

    # Internal node: recursively read left and right subtrees
    left_node = deserialize_tree(bit_reader)
    right_node = deserialize_tree(bit_reader)
    return HuffmanNode(weight=0, left=left_node, right=right_node)
