import heapq
from typing import Callable, Dict, List, Tuple, TypeVar

T = TypeVar("T")


def find_two_lowest_items(
    items: List[T], key_func: Callable[[T], int]
) -> Tuple[T, T]:
    if len(items) == 0:
        raise ValueError("At least one item is required")

    if len(items) == 1:
        return items[0], items[0]

    sorted_items = sorted(items, key=key_func)
    return sorted_items[0], sorted_items[1]


class HuffmanNode:
    def __init__(
        self,
        weight: int,
        character: str | None = None,
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


def create_leaf_node(character: str, weight: int) -> HuffmanNode:
    return HuffmanNode(weight=weight, character=character)


def create_internal_node(left: HuffmanNode, right: HuffmanNode) -> HuffmanNode:
    return HuffmanNode(
        weight=left.weight + right.weight, left=left, right=right
    )


def build_huffman_tree(frequency_map: Dict[str, int]) -> HuffmanNode:
    # Create initial leaf nodes and build a min-heap
    heap = [
        create_leaf_node(char, freq) for char, freq in frequency_map.items()
    ]
    heapq.heapify(heap)

    # Keep combining nodes until only one remains
    while len(heap) > 1:
        # Pop the two nodes with lowest weights (O(log n) each)
        left_node = heapq.heappop(heap)
        right_node = heapq.heappop(heap)

        # Create new internal node and push it back (O(log n))
        combined_node = create_internal_node(left_node, right_node)
        heapq.heappush(heap, combined_node)

    # Return the root node
    return heap[0]
