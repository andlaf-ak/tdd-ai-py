from typing import List

from .huffman_tree_builder import HuffmanNode


def serialize_tree(root: HuffmanNode) -> List[int]:
    """Serialize Huffman tree using iterative approach to avoid recursion depth issues."""
    result = []
    stack = [root]

    while stack:
        node = stack.pop()

        if node.character is not None:
            # Leaf node: 1 + 8-bit character
            result.append(1)
            result.extend(int(bit) for bit in format(node.character, "08b"))
        else:
            # Internal node: 0 + children (added in reverse order for correct traversal)
            result.append(0)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

    return result
