from .huffman_tree_builder import HuffmanNode


def serialize_tree(root: HuffmanNode) -> str:
    """Serialize a Huffman tree using depth-first traversal.

    Rules:
    - Internal nodes: emit "0"
    - Leaf nodes: emit "1" + 8-bit ASCII representation of character
    """
    if root.character is not None:
        # Leaf node: emit "1" + 8-bit ASCII representation
        return "1" + format(ord(root.character), "08b")

    # Internal node: emit "0" + serialize left and right subtrees
    result = "0"
    if root.left:
        result += serialize_tree(root.left)
    if root.right:
        result += serialize_tree(root.right)
    return result
