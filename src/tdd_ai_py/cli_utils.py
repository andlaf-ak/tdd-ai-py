"""Common utilities for command-line scripts."""

import sys
from typing import BinaryIO, Callable


def validate_args() -> str | None:
    """Validate command line arguments and return input filename or None."""
    return sys.argv[1] if len(sys.argv) == 2 else None


def handle_file_operation(operation: Callable[[str, BinaryIO], None], filename: str, output_stream: BinaryIO) -> None:
    """Handle file operations with common error handling."""
    try:
        operation(filename, output_stream)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied accessing '{filename}'.", file=sys.stderr)
        sys.exit(1)
    except (OSError, IOError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
