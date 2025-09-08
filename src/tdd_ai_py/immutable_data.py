"""Immutable data structures for functional programming."""

from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Mapping


@dataclass(frozen=True)
class FrequencyMap:
    """Immutable frequency mapping for bytes."""

    frequencies: Mapping[int, int]

    @property
    def total_count(self) -> int:
        """Get total count of all bytes."""
        return sum(self.frequencies.values())

    @property
    def unique_bytes(self) -> FrozenSet[int]:
        """Get set of unique byte values."""
        return frozenset(self.frequencies.keys())

    def get_frequency(self, byte_value: int) -> int:
        """Get frequency for a specific byte value."""
        return self.frequencies.get(byte_value, 0)


@dataclass(frozen=True)
class HuffmanCodes:
    """Immutable Huffman codes mapping."""

    codes: Mapping[int, List[int]]

    def get_code(self, byte_value: int) -> List[int]:
        """Get Huffman code for a byte value."""
        return self.codes[byte_value]

    @property
    def byte_values(self) -> FrozenSet[int]:
        """Get all byte values that have codes."""
        return frozenset(self.codes.keys())


@dataclass(frozen=True)
class CompressionHeader:
    """Immutable compression header data."""

    length: int

    def to_bytes(self) -> bytes:
        """Convert header to bytes for serialization."""
        return self.length.to_bytes(4, byteorder="big")


@dataclass(frozen=True)
class CompressionContext:
    """Immutable context for compression operation."""

    frequency_map: FrequencyMap
    header: CompressionHeader
    codes: HuffmanCodes

    @classmethod
    def create(cls, frequencies: Dict[int, int]) -> "CompressionContext":
        """Create compression context from frequency dictionary."""
        freq_map = FrequencyMap(frequencies=frequencies)
        header = CompressionHeader(length=freq_map.total_count)
        # Note: codes will be created separately after tree building
        return cls(
            frequency_map=freq_map,
            header=header,
            codes=HuffmanCodes(codes={}),  # Placeholder
        )

    def with_codes(self, codes: Dict[int, List[int]]) -> "CompressionContext":
        """Create new context with Huffman codes."""
        return CompressionContext(
            frequency_map=self.frequency_map,
            header=self.header,
            codes=HuffmanCodes(codes=codes),
        )
