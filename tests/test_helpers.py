from typing import List, Tuple


def bits_and_bytes(binary_string: str) -> Tuple[List[int], bytes]:
    """Convert binary string to list of integers and bytes."""
    bit_list = [int(bit) for bit in binary_string]

    # Pad to byte boundary
    padded_bits = bit_list.copy()
    while len(padded_bits) % 8 != 0:
        padded_bits.append(0)

    # Convert to bytes
    byte_values: List[int] = []
    for i in range(0, len(padded_bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | padded_bits[i + j]
        byte_values.append(byte)

    return bit_list, bytes(byte_values)
