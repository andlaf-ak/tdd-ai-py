from typing import List

from .huffman_tree_builder import HuffmanNode


def deserialize_tree(serialized_tree: List[int]) -> HuffmanNode:
    result, _ = _deserialize_tree_recursive(serialized_tree, 0)
    return result


def _deserialize_tree_recursive(
    serialized_tree: List[int], index: int
) -> tuple[HuffmanNode, int]:
    if serialized_tree[index] == 1:
        return _parse_leaf_node(serialized_tree, index)
    return _parse_internal_node(serialized_tree, index)


def _parse_leaf_node(
    serialized_tree: List[int], index: int
) -> tuple[HuffmanNode, int]:
    ascii_bits = serialized_tree[index + 1 : index + 9]
    ascii_value = 0
    for bit in ascii_bits:
        ascii_value = (ascii_value << 1) | bit
    character = chr(ascii_value)
    node = HuffmanNode(weight=0, character=character)
    return node, index + 9


def _parse_internal_node(
    serialized_tree: List[int], index: int
) -> tuple[HuffmanNode, int]:
    left_node, next_index = _deserialize_tree_recursive(
        serialized_tree, index + 1
    )
    right_node, final_index = _deserialize_tree_recursive(
        serialized_tree, next_index
    )
    node = HuffmanNode(weight=0, left=left_node, right=right_node)
    return node, final_index
