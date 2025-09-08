from typing import Dict, List

from .huffman_tree_builder import HuffmanNode


def generate_huffman_codes(root: HuffmanNode) -> Dict[int, List[int]]:
    """Generate Huffman codes using pure functional approach."""

    def _generate_codes(
        node: HuffmanNode, code: List[int]
    ) -> Dict[int, List[int]]:
        # Base case: leaf node
        if node.character is not None:
            return {node.character: code}

        # Recursive case: merge codes from children
        left_codes = _generate_codes(node.left, code + [0]) if node.left else {}
        right_codes = (
            _generate_codes(node.right, code + [1]) if node.right else {}
        )
        return {**left_codes, **right_codes}

    # Handle single character case
    if root.character is not None:
        return {root.character: [0]}

    return _generate_codes(root, [])
