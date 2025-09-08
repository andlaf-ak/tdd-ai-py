from typing import Dict, List

from .huffman_tree_builder import HuffmanNode


def generate_huffman_codes(root: HuffmanNode) -> Dict[int, List[int]]:
    """Generate Huffman codes using pure functional approach."""

    def _generate_codes(node: HuffmanNode, code: List[int]) -> Dict[int, List[int]]:
        return (
            {node.character: code}
            if node.character is not None
            else {
                **(_generate_codes(node.left, code + [0]) if node.left else {}),
                **(_generate_codes(node.right, code + [1]) if node.right else {}),
            }
        )

    return (
        {root.character: [0]} if root.character is not None else _generate_codes(root, [])
    )
