from io import StringIO
from typing import Dict, List

from tdd_ai_py.frequency_counter import create_frequency_map
from tdd_ai_py.huffman_encoder import generate_huffman_codes
from tdd_ai_py.huffman_tree_builder import HuffmanNode, build_huffman_tree


def _assert_codes_are_prefix_free(codes: Dict[str, List[int]]) -> None:
    code_list = list(codes.values())
    for i, code1 in enumerate(code_list):
        for j, code2 in enumerate(code_list):
            if i != j:
                # Check if code1 is prefix of code2
                if len(code1) <= len(code2):
                    is_prefix = code2[: len(code1)] == code1
                    assert (
                        not is_prefix
                    ), f"Code '{code1}' is prefix of '{code2}'"


def _assert_optimal_code_lengths(
    codes: Dict[str, List[int]], frequencies: Dict[str, int]
) -> None:
    for char1 in frequencies:
        for char2 in frequencies:
            if (
                frequencies[char1] > frequencies[char2]
            ):  # char1 is strictly more frequent
                code1_len = len(codes[char1])
                code2_len = len(codes[char2])

                assert code1_len <= code2_len, (
                    f"More frequent char '{char1}' (freq={frequencies[char1]}) "
                    f"has longer code (len={code1_len}) than less frequent char "
                    f"'{char2}' (freq={frequencies[char2]}) "
                    f"with code length {code2_len}"
                )


class TestHuffmanEncoder:
    def test_generates_code_for_single_root_node(self) -> None:
        root_node = HuffmanNode(weight=1, character="a")

        codes = generate_huffman_codes(root_node)

        assert codes == {"a": [0]}

    def test_generates_codes_for_tree_with_two_leaf_nodes(self) -> None:
        left_node = HuffmanNode(weight=1, character="a")
        right_node = HuffmanNode(weight=1, character="b")
        root_node = HuffmanNode(weight=2, left=left_node, right=right_node)

        codes = generate_huffman_codes(root_node)

        assert codes == {"a": [0], "b": [1]}

    def test_huffman_codes_have_prefix_property_and_optimal_lengths(
        self,
    ) -> None:
        text = "she sells seashells on the seashore"

        input_stream = StringIO(text)
        frequencies = create_frequency_map(input_stream)
        huffman_tree = build_huffman_tree(frequencies)
        codes = generate_huffman_codes(huffman_tree)

        _assert_codes_are_prefix_free(codes)
        _assert_optimal_code_lengths(codes, frequencies)
