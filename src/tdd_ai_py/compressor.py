from .frequency_counter import create_frequency_map
from .huffman_tree_builder import HuffmanNode, build_huffman_tree


class HuffmanCompressor:
    def compress(self, text: str) -> HuffmanNode:
        frequency_map = create_frequency_map(text)
        return build_huffman_tree(frequency_map)
