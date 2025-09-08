"""Safe compression functions using monadic error handling."""

from io import BytesIO
from typing import BinaryIO

from .compressor import compress as unsafe_compress
from .decompressor import decompress as unsafe_decompress
from .result_types import Result, safe_call_with_args


def safe_compress(
    input_stream: BinaryIO, output_stream: BinaryIO
) -> Result[None, str]:
    """Safely compress data with error handling.

    Args:
        input_stream: Source data to compress
        output_stream: Destination for compressed data

    Returns:
        Result indicating success or error message
    """
    return safe_call_with_args(unsafe_compress, input_stream, output_stream)


def safe_decompress(
    input_stream: BytesIO, output_stream: BinaryIO
) -> Result[None, str]:
    """Safely decompress data with error handling.

    Args:
        input_stream: Source compressed data
        output_stream: Destination for decompressed data

    Returns:
        Result indicating success or error message
    """
    return safe_call_with_args(unsafe_decompress, input_stream, output_stream)


def safe_round_trip(data: bytes) -> Result[bytes, str]:
    """Safely perform compression and decompression round trip.

    Args:
        data: Original data to test

    Returns:
        Result containing decompressed data or error message
    """

    def round_trip() -> bytes:
        # Compression
        input_stream = BytesIO(data)
        compressed_stream = BytesIO()
        unsafe_compress(input_stream, compressed_stream)

        # Decompression
        compressed_stream.seek(0)
        decompressed_stream = BytesIO()
        unsafe_decompress(compressed_stream, decompressed_stream)

        return decompressed_stream.getvalue()

    return safe_call_with_args(round_trip)


def compress_with_validation(
    input_stream: BinaryIO, output_stream: BinaryIO
) -> Result[int, str]:
    """Compress data and return compressed size with validation.

    Args:
        input_stream: Source data to compress
        output_stream: Destination for compressed data

    Returns:
        Result containing compressed size or error message
    """

    def compress_and_measure() -> int:
        initial_position = (
            output_stream.tell() if hasattr(output_stream, "tell") else 0
        )
        unsafe_compress(input_stream, output_stream)

        if hasattr(output_stream, "tell"):
            return output_stream.tell() - initial_position
        if hasattr(output_stream, "getvalue"):
            return len(output_stream.getvalue())  # type: ignore
        return 0  # Can't measure

    return safe_call_with_args(compress_and_measure)
