from .huffman_tree_builder import HuffmanNode


def serialize_tree(root: HuffmanNode) -> str:
    if root.character is not None:
        # Leaf node: emit "1" + 8-bit ASCII representation
        ascii_value = ord(root.character)
        binary_representation = format(ascii_value, "08b")  # 8-bit binary
        return "1" + binary_representation

    # For internal nodes (not needed yet, but placeholder)
    return ""
