from .huffman_tree_builder import HuffmanNode


def decode_compressed_data(root: HuffmanNode) -> str:
    if root.is_leaf:
        return _decode_single_node_tree(root)

    raise NotImplementedError("Multi-node trees not yet implemented")


def _decode_single_node_tree(root: HuffmanNode) -> str:
    if root.character is None:
        raise ValueError("Leaf node must have a character")

    return _character_to_8bit_ascii(root.character)


def _character_to_8bit_ascii(character: str) -> str:
    return format(ord(character), "08b")
