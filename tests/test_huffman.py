"""Tests for the Huffman compression algorithm."""

from tdd_ai_py.huffman import HuffmanCompressor
from tdd_ai_py.huffman_tree_builder import HuffmanNode


class TestHuffmanCompressor:
    """Test cases for the HuffmanCompressor class."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.compressor = HuffmanCompressor()

    def test_creates_frequency_map_from_input_string(self) -> None:
        """Test that frequency map is correctly created from input string."""
        # ARRANGE
        input_string = "abracadabra"
        expected_frequency_map = {"a": 5, "b": 2, "r": 2, "c": 1, "d": 1}

        # ACT
        result = self.compressor.create_frequency_map(input_string)

        # ASSERT
        assert result == expected_frequency_map

    def test_selects_and_joins_two_lowest_frequency_nodes(self) -> None:
        """Test that two lowest frequency nodes are selected and joined into
        a new internal node."""
        # ARRANGE
        node1 = HuffmanNode(weight=1, character="c")
        node2 = HuffmanNode(weight=1, character="d")
        node3 = HuffmanNode(weight=2, character="b")
        node4 = HuffmanNode(weight=5, character="a")
        nodes = [node1, node2, node3, node4]

        # ACT
        result = self.compressor.select_and_join_lowest_nodes(nodes)

        # ASSERT
        assert isinstance(result, HuffmanNode)
        assert result.weight == 2  # 1 + 1
        assert result.character is None  # Internal node has no character

        # Assert children exist and contain the two lowest frequency nodes
        assert result.left is not None
        assert result.right is not None

        # The children should be the original nodes with frequencies 1
        left_weight = result.left.weight
        right_weight = result.right.weight
        assert {left_weight, right_weight} == {1, 1}

        left_char = result.left.character
        right_char = result.right.character
        assert {left_char, right_char} == {"c", "d"}
        assert result.left.weight == 1
        assert result.right.weight == 1

    def test_builds_complete_huffman_tree(self) -> None:
        """Test that a complete Huffman tree is built from a frequency map."""
        # ARRANGE
        frequency_map = {"a": 5, "b": 2, "r": 2, "c": 1, "d": 1}
        # Expected tree structure:
        # Root(11)
        # ├── a(5)
        # └── Internal(6)
        #     ├── Internal(4)
        #     │   ├── b(2)
        #     │   └── r(2)
        #     └── Internal(2)
        #         ├── c(1)
        #         └── d(1)

        # ACT
        result = self.compressor.build_huffman_tree(frequency_map)

        # ASSERT
        assert isinstance(result, HuffmanNode)
        assert result.weight == 11  # Sum of all frequencies
        assert result.character is None  # Root is internal node

        # Should have left and right children
        assert result.left is not None
        assert result.right is not None

        # One child should be 'a' with weight 5, other should be internal
        # with weight 6
        weights = {result.left.weight, result.right.weight}
        assert weights == {5, 6}

        # Find the leaf node 'a' and internal node
        if result.left.weight == 5:
            a_node = result.left
            internal_node = result.right
        else:
            a_node = result.right
            internal_node = result.left

        assert a_node.character == "a"
        assert internal_node.character is None
