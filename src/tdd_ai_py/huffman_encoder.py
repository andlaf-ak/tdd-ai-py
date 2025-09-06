from typing import Dict

from .huffman_tree_builder import HuffmanNode


def generate_huffman_codes(root: HuffmanNode) -> Dict[str, str]:
    if root.character is not None:
        return {root.character: "0"}

    codes: Dict[str, str] = {}

    def traverse(node: HuffmanNode, code: str) -> None:
        if node.character is not None:
            codes[node.character] = code
        else:
            if node.left:
                traverse(node.left, code + "0")
            if node.right:
                traverse(node.right, code + "1")

    traverse(root, "")
    return codes
