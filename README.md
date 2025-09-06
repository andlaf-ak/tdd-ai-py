# TDD AI Python

A Python project demonstrating Test-Driven Development (TDD) principles with Huffman compression implementation.

## Features

- Huffman compression and decompression algorithm
- Pure functional approach with immutable data structures
- Comprehensive test coverage
- Type annotations throughout

## Installation

This project uses Poetry for dependency management. To set up the project:

```bash
poetry install
```

## Running Tests

Run the test suite using pytest:

```bash
poetry run pytest
```

For verbose output:

```bash
poetry run pytest -v
```

## Usage

```python
from tdd_ai_py.huffman import HuffmanCompressor

compressor = HuffmanCompressor()
frequency_map = compressor.create_frequency_map("hello world")
huffman_tree = compressor.build_huffman_tree(frequency_map)
```

## Project Structure

- `src/tdd_ai_py/huffman.py` - Huffman compression implementation
- `tests/test_huffman.py` - Comprehensive test suite
- `docs/` - Project documentation
  - `principles/` - Development principles and best practices
  - `dev/` - Development setup and tooling guides
- `pyproject.toml` - Project configuration and dependencies

## 📚 Documentation

For detailed documentation, see the [`docs/`](./docs/) directory:

- **[Development Principles](./docs/principles/)** - Coding standards and TDD methodology
- **[Development Setup](./docs/dev/)** - Tooling and workflow instructions
- **[Documentation Index](./docs/README.md)** - Complete documentation overview
