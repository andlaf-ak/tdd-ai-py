from itertools import chain
from typing import List

from .huffman_tree_builder import HuffmanNode


def serialize_tree(root: HuffmanNode) -> List[int]:
    return (
        [1] + [int(bit) for bit in format(root.character, "08b")]
        if root.character is not None
        else [0] + list(chain(*(serialize_tree(child) for child in [root.left, root.right] if child)))
    )
