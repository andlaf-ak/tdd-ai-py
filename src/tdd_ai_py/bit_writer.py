from typing import BinaryIO


class BitWriter:
    def __init__(self, output_stream: BinaryIO) -> None:
        self._buffer = 0
        self._bit_count = 0
        self._output_stream = output_stream

    def write_bit(self, bit: int) -> None:
        # Shift buffer left and add the new bit
        self._buffer = (self._buffer << 1) | (bit & 1)
        self._bit_count += 1

        # Auto-flush when we have 8 bits
        if self._bit_count == 8:
            self._flush_byte()

    def flush(self) -> None:
        if self._bit_count == 0:
            return

        # Pad remaining bits with zeros to complete the byte
        padded_buffer = self._buffer << (8 - self._bit_count)

        # Write to stream
        self._output_stream.write(bytes([padded_buffer]))

        # Reset internal state
        self._buffer = 0
        self._bit_count = 0

    def _flush_byte(self) -> None:
        """Flush a complete byte when buffer is full."""
        self._output_stream.write(bytes([self._buffer]))

        self._buffer = 0
        self._bit_count = 0
