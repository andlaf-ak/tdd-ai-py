from .huffman_tree_builder import HuffmanNode


def decode_compressed_data(root: HuffmanNode, bits: str) -> str:
    if root.is_leaf:
        return _decode_single_node_tree(root)

    return _decode_multi_node_tree(root, bits)


def _decode_single_node_tree(root: HuffmanNode) -> str:
    if root.character is None:
        raise ValueError("Leaf node must have a character")

    return _character_to_8bit_ascii(root.character)


def _decode_multi_node_tree(root: HuffmanNode, bits: str) -> str:
    result: str = ""
    current_node: HuffmanNode = root

    for bit in bits:
        current_node = _traverse_tree(current_node, bit)

        if current_node.is_leaf:
            if current_node.character is None:
                raise ValueError("Leaf node must have a character")
            result += current_node.character
            current_node = root

    return result


def _traverse_tree(node: HuffmanNode, bit: str) -> HuffmanNode:
    if bit == "0":
        if node.left is None:
            raise ValueError("Invalid tree structure: missing left child")
        return node.left
    if node.right is None:
        raise ValueError("Invalid tree structure: missing right child")
    return node.right


def _character_to_8bit_ascii(character: str) -> str:
    return format(ord(character), "08b")
