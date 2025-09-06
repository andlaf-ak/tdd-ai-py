from collections import Counter
from typing import Dict, List

from .huffman_tree_builder import HuffmanNode, HuffmanTreeBuilder


class HuffmanCompressor:

    def __init__(self) -> None:
        self._tree_builder = HuffmanTreeBuilder()

    def create_frequency_map(self, text: str) -> Dict[str, int]:
        return dict(Counter(text))

    def select_and_join_lowest_nodes(
        self, nodes: List[HuffmanNode]
    ) -> HuffmanNode:
        return self._tree_builder.select_and_join_lowest_nodes(nodes)

    def build_huffman_tree(self, frequency_map: Dict[str, int]) -> HuffmanNode:
        return self._tree_builder.build_huffman_tree(frequency_map)
