from typing import List


def bits(binary_string: str) -> List[int]:
    """Convert binary string to list of integers."""
    return [int(bit) for bit in binary_string]
