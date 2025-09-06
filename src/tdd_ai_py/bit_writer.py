class BitWriter:

    def __init__(self) -> None:
        self._buffer = 0
        self._bit_count = 0

    def write_bit(self, bit: int) -> None:
        # Shift buffer left and add the new bit
        self._buffer = (self._buffer << 1) | (bit & 1)
        self._bit_count += 1

    def flush(self) -> bytes:
        if self._bit_count == 0:
            return bytes()

        # Pad remaining bits with zeros to complete the byte
        padded_buffer = self._buffer << (8 - self._bit_count)

        # Reset internal state
        self._buffer = 0
        self._bit_count = 0

        return bytes([padded_buffer])
