#!/bin/bash

# Huffman Compression Test Script
# This script creates test files of various sizes, compresses and decompresses them,
# and verifies that the round-trip process preserves the original data.

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test configuration
TEST_DIR="test_files"
RESULTS_FILE="test_results.log"

# Statistics
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to create a test file with specific content and size
create_test_file() {
    local filename=$1
    local size=$2
    local content_type=$3

    case $content_type in
        "single_byte")
            # Single byte repeated
            if [ $size -eq 1 ]; then
                printf 'a' > "$filename"
            else
                yes 'a' | head -c $size > "$filename"
            fi
            ;;
        "two_bytes")
            # Two bytes alternating (good compression)
            for ((i=0; i<size; i++)); do
                if ((i % 2 == 0)); then
                    printf 'a'
                else
                    printf 'b'
                fi
            done > "$filename"
            ;;
        "random")
            # Random bytes (poor compression)
            head -c $size /dev/urandom > "$filename"
            ;;
        "text")
            # Repeating text pattern
            local pattern="Hello, World! This is a test. "
            local pattern_length=${#pattern}
            local repetitions=$((size / pattern_length + 1))
            printf "$pattern%.0s" $(seq 1 $repetitions) | head -c $size > "$filename"
            ;;
        "ascii")
            # ASCII printable characters
            for ((i=0; i<size; i++)); do
                printf "\\$(printf '%03o' $((32 + (i % 95))))"
            done > "$filename"
            ;;
    esac
}

# Function to run compression/decompression test
test_compression() {
    local original_file=$1
    local test_name=$2

    local compressed_file="${original_file}.compressed"
    local decompressed_file="${original_file}.decompressed"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    print_status $BLUE "Testing: $test_name"

    # Get original file size
    local original_size=$(wc -c < "$original_file")
    print_status $NC "  Original size: $original_size bytes"

    # Compress the file
    if ! python3 ../huffman_compression.py "$original_file" > "$compressed_file" 2>"${compressed_file}.err"; then
        local compression_error=$(cat "${compressed_file}.err" 2>/dev/null || echo "Unknown error")
        print_status $RED "  ❌ FAILED: Compression failed"
        print_status $RED "    Error: $compression_error"
        echo "FAILED: $test_name - Compression failed: $compression_error" >> "$RESULTS_FILE"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        rm -f "${compressed_file}.err"
        return 1
    fi
    rm -f "${compressed_file}.err"

    # Get compressed file size
    local compressed_size=$(wc -c < "$compressed_file")
    local compression_ratio=$(echo "scale=2; $compressed_size / $original_size * 100" | bc -l)
    print_status $NC "  Compressed size: $compressed_size bytes (${compression_ratio}% of original)"

    # Check compression effectiveness
    local ratio_int=$(echo "$compression_ratio" | cut -d. -f1)
    if [ "$ratio_int" -lt 100 ]; then
        print_status $GREEN "  ✅ COMPRESSION: File was compressed successfully"
    else
        print_status $YELLOW "  ⚠️  WARNING: File expanded instead of compressing"
    fi

    # Decompress the file
    if ! python3 ../huffman_decompression.py "$compressed_file" > "$decompressed_file" 2>"${decompressed_file}.err"; then
        local decompression_error=$(cat "${decompressed_file}.err" 2>/dev/null || echo "Unknown error")
        print_status $RED "  ❌ FAILED: Decompression failed"
        print_status $RED "    Error: $decompression_error"
        echo "FAILED: $test_name - Decompression failed: $decompression_error" >> "$RESULTS_FILE"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        rm -f "${decompressed_file}.err"
        return 1
    fi
    rm -f "${decompressed_file}.err"

    # Compare original and decompressed files
    if cmp -s "$original_file" "$decompressed_file"; then
        print_status $GREEN "  ✅ PASSED: Files match perfectly"
        echo "PASSED: $test_name - Original: $original_size bytes, Compressed: $compressed_size bytes (${compression_ratio}%)" >> "$RESULTS_FILE"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        print_status $RED "  ❌ FAILED: Files do not match"
        echo "FAILED: $test_name - Round-trip verification failed" >> "$RESULTS_FILE"
        FAILED_TESTS=$((FAILED_TESTS + 1))

        # Show differences for debugging
        local decompressed_size=$(wc -c < "$decompressed_file")
        print_status $RED "    Original size: $original_size, Decompressed size: $decompressed_size"

        return 1
    fi

    # Clean up intermediate files
    rm -f "$compressed_file" "$decompressed_file"

    echo ""
}

# Main test function
run_tests() {
    print_status $YELLOW "🚀 Starting Huffman Compression Tests"
    echo ""

    # Create test directory
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"

    # Clear results file
    > "../$RESULTS_FILE"

    # Test 1: Single byte file
    print_status $BLUE "=== Single Byte Tests ==="
    create_test_file "test_1byte.txt" 1 "single_byte"
    test_compression "test_1byte.txt" "Single byte (1 byte)"

    # Test 2: Small files with different patterns
    print_status $BLUE "=== Small File Tests ==="

    sizes=(2 3 5 8 10 16 32)
    for size in "${sizes[@]}"; do
        create_test_file "test_${size}byte_single.txt" $size "single_byte"
        test_compression "test_${size}byte_single.txt" "Single character repeated ($size bytes)"

        create_test_file "test_${size}byte_two.txt" $size "two_bytes"
        test_compression "test_${size}byte_two.txt" "Two characters alternating ($size bytes)"
    done

    # Test 3: Medium files
    print_status $BLUE "=== Medium File Tests ==="

    sizes=(64 128 256 512 1024)
    for size in "${sizes[@]}"; do
        create_test_file "test_${size}byte_text.txt" $size "text"
        test_compression "test_${size}byte_text.txt" "Repeating text pattern ($size bytes)"

        create_test_file "test_${size}byte_ascii.txt" $size "ascii"
        test_compression "test_${size}byte_ascii.txt" "ASCII characters ($size bytes)"
    done

    # Test 4: Large files
    print_status $BLUE "=== Large File Tests ==="

    sizes=(2048 4096 8192 16384)
    for size in "${sizes[@]}"; do
        create_test_file "test_${size}byte_text.txt" $size "text"
        test_compression "test_${size}byte_text.txt" "Large text file ($size bytes)"
    done

    # Test 5: Random data (should compress poorly)
    print_status $BLUE "=== Random Data Tests ==="

    sizes=(64 256 1024)
    for size in "${sizes[@]}"; do
        create_test_file "test_${size}byte_random.txt" $size "random"
        test_compression "test_${size}byte_random.txt" "Random data ($size bytes)"
    done

    # Clean up test files
    rm -f *.txt
    cd ..
    rmdir "$TEST_DIR"
}

# Function to print test summary
print_summary() {
    echo ""
    print_status $YELLOW "📊 Test Summary"
    print_status $YELLOW "=================="
    print_status $NC "Total tests: $TOTAL_TESTS"
    print_status $GREEN "Passed: $PASSED_TESTS"
    print_status $RED "Failed: $FAILED_TESTS"

    if [ $FAILED_TESTS -eq 0 ]; then
        print_status $GREEN "🎉 All tests passed!"
    else
        print_status $RED "❌ Some tests failed. Check $RESULTS_FILE for details."
    fi

    echo ""
    print_status $BLUE "Detailed results saved to: $RESULTS_FILE"
}

# Check if required scripts exist
check_dependencies() {
    if [ ! -f "huffman_compression.py" ]; then
        print_status $RED "Error: huffman_compression.py not found"
        exit 1
    fi

    if [ ! -f "huffman_decompression.py" ]; then
        print_status $RED "Error: huffman_decompression.py not found"
        exit 1
    fi

    # Check if bc is available for calculations
    if ! command -v bc &> /dev/null; then
        print_status $YELLOW "Warning: bc not found. Compression ratios will not be calculated."
    fi
}

# Main execution
main() {
    print_status $BLUE "Huffman Compression Test Suite"
    print_status $BLUE "=============================="
    echo ""

    check_dependencies
    run_tests
    print_summary

    # Exit with error code if any tests failed
    if [ $FAILED_TESTS -gt 0 ]; then
        exit 1
    fi
}

# Run the tests
main "$@"
