# TDD AI Python

A Python project demonstrating Test-Driven Development (TDD) principles with a production-ready Huffman compression/decompression implementation.

## Features

- Huffman compression and decompression
- Clean, test-driven design with high coverage
- Type annotations and static typing (mypy)
- CLI entry points for easy usage

## Installation

This project uses Poetry. To set up the project:

```bash
poetry install
```

Optionally install the package in editable mode to get CLI commands:

```bash
poetry install --with dev
```

This exposes the following console commands (via Poetry scripts):

- `huffman-compress`
- `huffman-decompress`

## Running Tests

Run the test suite using pytest:

```bash
poetry run pytest -v --cov=src/tdd_ai_py --cov-report=term-missing
```

## Usage

Programmatic API:

```python
from tdd_ai_py import HuffmanCompressor, HuffmanDecompressor
from io import BytesIO

# Compress bytes
src = BytesIO(b"hello world")
out = BytesIO()
HuffmanCompressor().compress(src, out)
compressed = out.getvalue()

# Decompress bytes
from io import BytesIO
restored = BytesIO()
HuffmanDecompressor().decompress(BytesIO(compressed), restored)
assert restored.getvalue() == b"hello world"
```

Command line:

```bash
# Compress a file to stdout (redirect to a file)
huffman-compress input.txt > compressed.bin

# Decompress a file to stdout (redirect to a file)
huffman-decompress compressed.bin > output.txt
```

## Project Structure

- `src/tdd_ai_py/compress.py` - CLI entry for compression
- `src/tdd_ai_py/decompress.py` - CLI entry for decompression
- `src/tdd_ai_py/compression/` - Compression modules (bit I/O, encoder, tree)
- `src/tdd_ai_py/decompression/` - Decompression modules
- `tests/` - Comprehensive test suite
- `docs/` - Project documentation
- `pyproject.toml` - Project configuration and dependencies

## 📚 Documentation

For detailed documentation, see the [`docs/`](./docs/) directory:

- **[Development Principles](./docs/principles/)** - Coding standards and TDD methodology
- **[Documentation Index](./docs/README.md)** - Complete documentation overview
