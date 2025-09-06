"""Huffman tree building module."""

import heapq
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple, TypeVar

T = TypeVar("T")


def find_two_lowest_items(
    items: List[T], key_func: Callable[[T], int]
) -> Tuple[T, T]:
    """Generic function to find two items with lowest values based on a key.

    Args:
        items: List of items to search
        key_func: Function to extract comparison key from each item

    Returns:
        Tuple containing the two items with lowest values.
        If only one item exists, returns that item twice.

    Raises:
        ValueError: If the items list is empty
    """
    if len(items) == 0:
        raise ValueError("At least one item is required")

    if len(items) == 1:
        return items[0], items[0]

    sorted_items = sorted(items, key=key_func)
    return sorted_items[0], sorted_items[1]


@dataclass(frozen=True)
class HuffmanNode:
    """A node in the Huffman binary tree.

    This immutable data class represents a node in the Huffman tree structure.
    Leaf nodes contain characters, while internal nodes combine frequencies.
    """

    weight: int
    character: Optional[str] = None
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

    @property
    def is_leaf(self) -> bool:
        """Check if this node is a leaf node."""
        return self.left is None and self.right is None

    def __lt__(self, other: "HuffmanNode") -> bool:
        """Enable comparison for heap operations based only on weight."""
        return self.weight < other.weight

    def __eq__(self, other: object) -> bool:
        """Enable equality comparison."""
        if not isinstance(other, HuffmanNode):
            return False
        return (
            self.weight == other.weight
            and self.character == other.character
            and self.left == other.left
            and self.right == other.right
        )


def create_leaf_node(character: str, weight: int) -> HuffmanNode:
    """Create a leaf node for a single character."""
    return HuffmanNode(weight=weight, character=character)


def create_internal_node(left: HuffmanNode, right: HuffmanNode) -> HuffmanNode:
    """Create an internal node combining two child nodes."""
    return HuffmanNode(
        weight=left.weight + right.weight, left=left, right=right
    )


class HuffmanTreeBuilder:
    """A class for building Huffman trees from frequency maps."""

    def create_node_from_values(
        self, char1: str, freq1: int, char2: str, freq2: int
    ) -> HuffmanNode:
        """Create a binary tree node from two character-frequency pairs."""
        left_node = create_leaf_node(char1, freq1)
        right_node = create_leaf_node(char2, freq2)
        return create_internal_node(left_node, right_node)

    def select_and_join_lowest_nodes(
        self, nodes: List[HuffmanNode]
    ) -> HuffmanNode:
        """Select the two lowest frequency nodes and join them into a new
        internal node."""
        left_node, right_node = find_two_lowest_items(
            nodes, lambda node: node.weight
        )
        return create_internal_node(left_node, right_node)

    def build_huffman_tree(self, frequency_map: Dict[str, int]) -> HuffmanNode:
        """Build a complete Huffman tree from a frequency map.

        Uses a heap-based approach for efficient selection of lowest weight
        nodes. Repeatedly selects the two nodes with lowest weights and joins
        them until only one root node remains.

        Args:
            frequency_map: Dictionary mapping characters to their frequencies

        Returns:
            The root node of the complete Huffman tree
        """
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
