from typing import Dict

from .huffman_tree_builder import HuffmanNode


def generate_huffman_codes(root: HuffmanNode) -> Dict[str, str]:
    if root.character is not None:
        return {root.character: "0"}
    return {}
