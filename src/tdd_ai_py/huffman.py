from typing import Dict, List

from .frequency_analyzer import create_frequency_map
from .huffman_tree_builder import HuffmanNode, HuffmanTreeBuilder


class HuffmanCompressor:

    def __init__(self) -> None:
        self._tree_builder = HuffmanTreeBuilder()

    def create_frequency_map(self, text: str) -> Dict[str, int]:
        return create_frequency_map(text)

    def create_node_from_values(
        self, char1: str, freq1: int, char2: str, freq2: int
    ) -> HuffmanNode:
        return self._tree_builder.create_node_from_values(
            char1, freq1, char2, freq2
        )

    def select_and_join_lowest_nodes(
        self, nodes: List[HuffmanNode]
    ) -> HuffmanNode:
        return self._tree_builder.select_and_join_lowest_nodes(nodes)

    def build_huffman_tree(self, frequency_map: Dict[str, int]) -> HuffmanNode:
        return self._tree_builder.build_huffman_tree(frequency_map)
