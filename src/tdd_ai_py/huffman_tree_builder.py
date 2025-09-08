import heapq
from typing import Callable, Dict, List, Tuple, TypeVar

T = TypeVar("T")


def find_two_lowest_items(items: List[T], key_func: Callable[[T], int]) -> Tuple[T, T]:
    if not items:
        raise ValueError("At least one item is required")
    return (items[0], items[0]) if len(items) == 1 else (sorted(items, key=key_func)[0], sorted(items, key=key_func)[1])


class HuffmanNode:
    def __init__(
        self,
        weight: int,
        character: int | None = None,
        left: "HuffmanNode | None" = None,
        right: "HuffmanNode | None" = None,
    ):
        self.weight = weight
        self.character = character
        self.left = left
        self.right = right

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def __lt__(self, other: "HuffmanNode") -> bool:
        return self.weight < other.weight

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HuffmanNode):
            return False
        return (
            self.weight == other.weight
            and self.character == other.character
            and self.left == other.left
            and self.right == other.right
        )


def create_leaf_node(character: int, weight: int) -> HuffmanNode:
    return HuffmanNode(weight=weight, character=character)


def create_internal_node(left: HuffmanNode, right: HuffmanNode) -> HuffmanNode:
    return HuffmanNode(weight=left.weight + right.weight, left=left, right=right)


def build_huffman_tree(frequency_map: Dict[int, int]) -> HuffmanNode:
    def build_tree_recursive(nodes: List[HuffmanNode]) -> HuffmanNode:
        return (
            nodes[0]
            if len(nodes) == 1
            else build_tree_recursive(
                [
                    create_internal_node(*heapq.nsmallest(2, nodes)),
                    *[node for node in nodes if node not in heapq.nsmallest(2, nodes)],
                ]
            )
        )

    initial_nodes = [create_leaf_node(char, freq) for char, freq in frequency_map.items()]
    return build_tree_recursive(initial_nodes)
