import heapq
from typing import Callable, Dict, List, Tuple, TypeVar

T = TypeVar("T")


def find_two_lowest_items(items: List[T], key_func: Callable[[T], int]) -> Tuple[T, T]:
    """Find the two items with lowest key values using heap operations for O(n)."""
    if not items:
        raise ValueError("At least one item is required")
    if len(items) == 1:
        return (items[0], items[0])

    # Use heapq.nsmallest for O(n) complexity instead of sorting
    two_smallest = heapq.nsmallest(2, items, key=key_func)
    return (two_smallest[0], two_smallest[1])


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
    """Build Huffman tree using iterative heap-based approach to avoid recursion."""
    # Create initial heap of leaf nodes
    heap = [create_leaf_node(char, freq) for char, freq in frequency_map.items()]
    heapq.heapify(heap)

    # Iteratively build tree using heap operations (no recursion)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = create_internal_node(left, right)
        heapq.heappush(heap, merged)

    return heap[0]
