from .huffman_tree_builder import HuffmanNode


def deserialize_tree(serialized_tree: str) -> HuffmanNode:
    """Deserialize a Huffman tree from depth-first traversal bit string.

    Rules:
    - "1" followed by 8-bit ASCII = leaf node
    - "0" = internal node (followed by left and right subtrees)
    """
    if serialized_tree.startswith("1"):
        return _deserialize_leaf_node(serialized_tree)

    # This will be needed for internal nodes later
    raise NotImplementedError("Internal nodes not yet implemented")


def _deserialize_leaf_node(serialized_tree: str) -> HuffmanNode:
    """Deserialize a leaf node from '1' + 8-bit ASCII."""
    ascii_bits = serialized_tree[1:9]
    ascii_value = int(ascii_bits, 2)
    character = chr(ascii_value)
    return HuffmanNode(weight=0, character=character)
