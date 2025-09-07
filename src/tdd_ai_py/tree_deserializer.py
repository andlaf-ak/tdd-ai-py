from .huffman_tree_builder import HuffmanNode


def deserialize_tree(serialized_tree: str) -> HuffmanNode:
    """Deserialize a Huffman tree from depth-first traversal bit string.

    Rules:
    - "1" followed by 8-bit ASCII = leaf node
    - "0" = internal node (followed by left and right subtrees)
    """
    result, _ = _deserialize_tree_recursive(serialized_tree, 0)
    return result


def _deserialize_tree_recursive(
    serialized_tree: str, index: int
) -> tuple[HuffmanNode, int]:
    """Recursively deserialize tree starting at given index.

    Returns (node, next_index).
    """
    if serialized_tree[index] == "1":
        return _parse_leaf_node(serialized_tree, index)
    return _parse_internal_node(serialized_tree, index)


def _parse_leaf_node(
    serialized_tree: str, index: int
) -> tuple[HuffmanNode, int]:
    """Parse leaf node: '1' + 8-bit ASCII. Returns (node, next_index)."""
    ascii_bits = serialized_tree[index + 1 : index + 9]
    character = chr(int(ascii_bits, 2))
    node = HuffmanNode(weight=0, character=character)
    return node, index + 9


def _parse_internal_node(
    serialized_tree: str, index: int
) -> tuple[HuffmanNode, int]:
    """Parse internal node: '0' + left subtree + right subtree.

    Returns (node, next_index).
    """
    left_node, next_index = _deserialize_tree_recursive(
        serialized_tree, index + 1
    )
    right_node, final_index = _deserialize_tree_recursive(
        serialized_tree, next_index
    )
    node = HuffmanNode(weight=0, left=left_node, right=right_node)
    return node, final_index
