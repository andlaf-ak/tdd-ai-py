from typing import List

from .huffman_tree_builder import HuffmanNode


def serialize_tree(root: HuffmanNode) -> List[int]:
    if root.character is not None:
        # Leaf node: emit [1] + 8-bit ASCII representation
        ascii_bits = [int(bit) for bit in format(ord(root.character), "08b")]
        return [1] + ascii_bits

    # Internal node: emit [0] + serialize left and right subtrees
    result = [0]
    if root.left:
        result.extend(serialize_tree(root.left))
    if root.right:
        result.extend(serialize_tree(root.right))
    return result
