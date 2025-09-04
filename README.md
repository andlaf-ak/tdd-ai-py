# TDD AI Python Calculator

A simple calculator implementation developed using Test-Driven Development (TDD) principles.

## Features

- Basic arithmetic operations: addition, subtraction, multiplication, division
- Input validation and error handling
- Comprehensive test coverage

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
from tdd_ai_py.calculator import Calculator

calc = Calculator()
result = calc.add(2, 3)  # Returns 5
```

## Project Structure

- `src/tdd_ai_py/calculator.py` - Main calculator implementation
- `tests/test_calculator.py` - Comprehensive test suite
- `pyproject.toml` - Project configuration and dependencies
