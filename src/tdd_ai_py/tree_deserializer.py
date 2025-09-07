from .huffman_tree_builder import HuffmanNode


def deserialize_tree(serialized_tree: str) -> HuffmanNode:
    result, _ = _deserialize_tree_recursive(serialized_tree, 0)
    return result


def _deserialize_tree_recursive(
    serialized_tree: str, index: int
) -> tuple[HuffmanNode, int]:
    if serialized_tree[index] == "1":
        return _parse_leaf_node(serialized_tree, index)
    return _parse_internal_node(serialized_tree, index)


def _parse_leaf_node(
    serialized_tree: str, index: int
) -> tuple[HuffmanNode, int]:
    ascii_bits = serialized_tree[index + 1 : index + 9]
    character = chr(int(ascii_bits, 2))
    node = HuffmanNode(weight=0, character=character)
    return node, index + 9


def _parse_internal_node(
    serialized_tree: str, index: int
) -> tuple[HuffmanNode, int]:
    left_node, next_index = _deserialize_tree_recursive(
        serialized_tree, index + 1
    )
    right_node, final_index = _deserialize_tree_recursive(
        serialized_tree, next_index
    )
    node = HuffmanNode(weight=0, left=left_node, right=right_node)
    return node, final_index
