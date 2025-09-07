"""Round-trip tests for Huffman compression and decompression.

Tests that decompress(compress(x)) == x for various inputs.
"""

from io import BytesIO

import pytest

from tdd_ai_py.compressor import HuffmanCompressor
from tdd_ai_py.decompressor import Decompressor


class TestRoundTrip:
    """Test round-trip compression and decompression."""

    @pytest.mark.parametrize(
        "test_data",
        [
            # Single character
            "a",
            # Two characters
            "ab",
            # Classic test phrase with repetition
            "abracadabra",
            # Pangram with good compression potential
            "she sells seashells on the seashore",
            # Lorem ipsum - longer text with natural language patterns
            """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
Sed ut perspiciatis unde omnis iste natus error sit voluptate accusantium
doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
consequuntur magni dolores eos qui ratione voluptate sequi nesciunt.""",
        ],
        ids=[
            "single_character",
            "two_characters",
            "repeated_pattern",
            "pangram",
            "lorem_ipsum",
        ],
    )
    def test_round_trip_compression(self, test_data: str) -> None:
        """Test that decompress(compress(x)) == x for various inputs."""
        # Convert string to bytes for binary processing
        original_bytes = test_data.encode("utf-8")

        # Compress the data
        input_stream = BytesIO(original_bytes)
        compressed_stream = BytesIO()
        compressor = HuffmanCompressor()
        compressor.compress(input_stream, compressed_stream)

        # Get compressed data
        compressed_data = compressed_stream.getvalue()

        # Decompress the data
        compressed_input = BytesIO(compressed_data)
        decompressed_stream = BytesIO()
        decompressor = Decompressor()
        decompressor.decompress(compressed_input, decompressed_stream)
        decompressed_bytes = decompressed_stream.getvalue()

        # Verify round-trip integrity
        assert decompressed_bytes == original_bytes

        # Convert back to string for additional verification
        decompressed_text = decompressed_bytes.decode("utf-8")
        assert decompressed_text == test_data
