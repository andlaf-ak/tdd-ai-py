# Huffman Compression Implementation

A production-ready Huffman compression and decompression implementation in Python, developed using Test-Driven Development (TDD) principles with Claude Code and Claude Sonnet 4.

## What is Huffman Compression?

Huffman compression is a lossless data compression algorithm that assigns variable-length codes to characters based on their frequency of occurrence. Characters that appear more frequently get shorter codes, while less frequent characters get longer codes, resulting in overall size reduction.

This implementation provides:

- **Complete Huffman encoding/decoding** with proper tree serialization
- **Efficient bit-level I/O** with buffered reading and writing
- **Functional programming approach** optimized for performance
- **Full round-trip compression** that perfectly reconstructs original data
- **Comprehensive CLI tools** for file compression and decompression

## Development

This project was developed collaboratively with:
- **[Claude Code](https://claude.ai/code)** - Anthropic's official CLI for Claude
- **Claude Sonnet 4** - The underlying AI model
- **Test-Driven Development** methodology throughout

## Features

- Lossless Huffman compression and decompression
- Clean, test-driven design with 100% test coverage
- Full type annotations and static typing (mypy)
- Optimized bit operations with buffered I/O
- CLI entry points for easy file processing
- Comprehensive test suite with round-trip verification

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

### Command Line Interface

The easiest way to use the compression tools:

```bash
# Compress a file
huffman-compress input.txt > compressed.huf

# Decompress a file
huffman-decompress compressed.huf > restored.txt

# Verify the round-trip worked
diff input.txt restored.txt  # Should show no differences
```

### Programmatic API

For integration into Python applications:

```python
from tdd_ai_py import HuffmanCompressor, HuffmanDecompressor
from io import BytesIO

# Compress data
original_data = b"This is a test message for Huffman compression!"
input_stream = BytesIO(original_data)
compressed_stream = BytesIO()

compressor = HuffmanCompressor()
compressor.compress(input_stream, compressed_stream)
compressed_data = compressed_stream.getvalue()

print(f"Original size: {len(original_data)} bytes")
print(f"Compressed size: {len(compressed_data)} bytes")
print(f"Compression ratio: {len(compressed_data)/len(original_data)*100:.1f}%")

# Decompress data
decompressed_stream = BytesIO()
decompressor = HuffmanDecompressor()
decompressor.decompress(BytesIO(compressed_data), decompressed_stream)

# Verify perfect reconstruction
assert decompressed_stream.getvalue() == original_data
print("✅ Round-trip compression successful!")
```

## How It Works

This Huffman compression implementation follows the standard algorithm. Let's trace through with the example **"abracadabra"**:

### Step 1: Frequency Analysis
Count how often each character appears:
```
'a': 5 times  (45.5%)
'b': 2 times  (18.2%)
'r': 2 times  (18.2%)
'c': 1 time   (9.1%)
'd': 1 time   (9.1%)
```

### Step 2: Tree Construction
Build a binary tree by repeatedly combining the two least frequent nodes:

```
Initial nodes: c(1), d(1), b(2), r(2), a(5)

Combine c(1) + d(1) = cd(2)
Nodes: b(2), r(2), cd(2), a(5)

Combine b(2) + r(2) = br(4)
Nodes: cd(2), br(4), a(5)

Combine cd(2) + br(4) = cdbr(6)
Nodes: a(5), cdbr(6)

Combine a(5) + cdbr(6) = root(11)
```

Final tree structure:
```
        root(11)
       /        \
    a(5)      cdbr(6)
               /      \
            cd(2)    br(4)
           /    \    /    \
         c(1)  d(1) b(2) r(2)
```

### Step 3: Code Generation
Assign binary codes by tree paths (0=left, 1=right):
```
a: 0        (1 bit)  - most frequent gets shortest code
c: 100      (3 bits)
d: 101      (3 bits)
b: 110      (3 bits)
r: 111      (3 bits)
```

### Step 4: Encode the Data
Replace each character with its code:
```
Original:  a b r a c a d a b r a
Encoded:   0 110 111 0 100 0 101 0 110 111 0
Result:    01101110100010101101110
```

**Compression achieved**: 23 bits vs. 88 bits (8 bits × 11 characters) = **74% compression!**

### Step 5: Tree Serialization
The tree structure must be stored so the decompressor can rebuild it. This implementation uses a clever binary encoding:

**Serialization Format:**
- **Leaf nodes**: `1` + 8-bit character code
- **Internal nodes**: `0` + serialized left child + serialized right child

**For our "abracadabra" tree:**
```
        root(11)
       /        \
    a(5)      cdbr(6)
               /      \
            cd(2)    br(4)
           /    \    /    \
         c(1)  d(1) b(2) r(2)
```

**Serialization process (pre-order traversal):**
1. `root`: Internal → `0`
2. `a`: Leaf → `1` + `01100001` (ASCII 'a' = 97)
3. `cdbr`: Internal → `0`
4. `cd`: Internal → `0`
5. `c`: Leaf → `1` + `01100011` (ASCII 'c' = 99)
6. `d`: Leaf → `1` + `01100100` (ASCII 'd' = 100)
7. `br`: Internal → `0`
8. `b`: Leaf → `1` + `01100010` (ASCII 'b' = 98)
9. `r`: Leaf → `1` + `01110010` (ASCII 'r' = 114)

**Final serialized tree:**
```
0 1 01100001 0 0 1 01100011 1 01100100 0 1 01100010 1 01110010
```

**Total**: 1 + 9 + 1 + 1 + 9 + 9 + 1 + 9 + 9 = **49 bits** for tree structure

### Step 6: Complete Compressed File
The final compressed file contains:
1. **Serialized tree** (49 bits)
2. **Encoded data** (23 bits)
3. **Padding bits** to align to byte boundary

**Total compressed size**: ~72 bits = 9 bytes vs. original 11 bytes = **18% savings**

*Note: For longer texts, the tree overhead becomes negligible and compression ratios improve dramatically.*

### Decompression Process
1. **Read tree structure** from the bit stream
2. **Reconstruct the Huffman tree** using the serialized format
3. **Decode data bits** by traversing tree (0=left, 1=right) until reaching leaves
4. **Output characters** as leaves are reached
5. **Perfect reconstruction** of original "abracadabra"

## Performance

This implementation is optimized for both correctness and performance:

- **Buffered I/O**: 8KB buffers for efficient file reading/writing
- **Iterative Algorithms**: Stack-based tree operations avoid recursion limits
- **Functional Design**: Leverages Python's optimized built-in functions
- **Memory Efficient**: Streaming approach for large files

Compression effectiveness varies by data type:
- **Text files**: Typically 40-60% of original size
- **Repetitive data**: Can achieve 20-30% compression ratios
- **Random data**: May expand due to tree overhead (expected behavior)

## Project Structure

```
src/tdd_ai_py/
├── compress.py                 # CLI compression entry point
├── decompress.py              # CLI decompression entry point
├── compression/               # Compression pipeline
│   ├── bit_writer.py         # Efficient bit-level output
│   ├── frequency_analyzer.py # Character frequency counting
│   ├── huffman_encoder.py    # Code generation from tree
│   ├── huffman_tree_builder.py # Tree construction algorithms
│   ├── stream_utils.py       # I/O utilities
│   └── tree_serializer.py    # Tree encoding for storage
├── decompression/            # Decompression pipeline
│   ├── bit_reader.py        # Efficient bit-level input
│   ├── data_decoder.py      # Huffman code decoding
│   └── tree_deserializer.py # Tree reconstruction
└── huffman.py               # Main compressor/decompressor classes

tests/                       # Comprehensive test suite with 100% coverage
docs/                       # Development methodology and principles
```

## 📚 Documentation

For detailed documentation, see the [`docs/`](./docs/) directory:

- **[Development Principles](./docs/principles/)** - Coding standards and TDD methodology
- **[Documentation Index](./docs/README.md)** - Complete documentation overview

## Development with Claude Code

This project showcases collaborative development between human expertise and AI assistance:

- **Test-Driven Development** maintained throughout the entire process
- **Functional programming patterns** optimized for both readability and performance
- **Comprehensive testing** including edge cases and round-trip verification
- **Performance optimization** guided by algorithmic complexity analysis
- **Code quality** maintained with type hints, linting, and formatting
