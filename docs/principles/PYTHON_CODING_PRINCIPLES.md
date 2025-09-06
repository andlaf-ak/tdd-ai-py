# Python Coding Principles

## Python-Specific Clean Code Principles

### Naming Conventions (PEP 8)

#### Functions and Methods
- Use `snake_case` for function and method names
- Use verbs that clearly describe what the function does
```python
# Good
def calculate_total_price(base_price: float, tax_rate: float) -> float:
    return base_price * (1 + tax_rate)

def validate_email_address(email: str) -> bool:
    return "@" in email and "." in email
```

#### Variables
- Use `snake_case` for variable names
- Use intention-revealing names
```python
# Bad
d = 5  # elapsed time in days
usr_nm = "john"

# Good
elapsed_time_in_days = 5
username = "john"
```

#### Classes
- Use `PascalCase` for class names
- Use nouns that represent the concept
```python
# Good
class Calculator:
    pass

class PaymentProcessor:
    pass

class UserRepository:
    pass
```

#### Constants
- Use `SCREAMING_SNAKE_CASE` for constants
```python
# Good
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
TAX_RATE = 0.08
```

### Import Organization (PEP 8)
```python
"""Module docstring describing the purpose of this module."""

# Standard library imports
import sys
from typing import Union, Optional, List, Dict

# Third-party imports
import pytest
import numpy as np
import requests

# Local imports
from myproject.calculator import Calculator
from myproject.utils import format_number
```

### Class Structure
```python
class Calculator:
    """A simple calculator class for basic arithmetic operations.

    This class provides methods for performing basic mathematical
    operations on numeric values with proper error handling.
    """

    # Class constants
    MAX_PRECISION = 10
    DEFAULT_DECIMAL_PLACES = 2

    def __init__(self) -> None:
        """Initialize the calculator with default settings."""
        self._precision = self.DEFAULT_DECIMAL_PLACES

    def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Add two numbers together.

        Args:
            a: First number to add
            b: Second number to add

        Returns:
            The sum of a and b

        Raises:
            TypeError: If either argument is not a number
        """
        self._validate_numeric_inputs(a, b)
        return a + b

    def _validate_numeric_inputs(self, *args: Union[int, float]) -> None:
        """Validate that all arguments are numeric types.

        Args:
            *args: Variable number of arguments to validate

        Raises:
            TypeError: If any argument is not a number
        """
        for arg in args:
            if not isinstance(arg, (int, float)):
                raise TypeError("All arguments must be numbers")
```

### Type Hints (PEP 484)
```python
from typing import Union, Optional, List, Dict, Tuple, Any

# Function parameters and return types
def calculate_average(numbers: List[float]) -> float:
    return sum(numbers) / len(numbers)

# Union types for multiple acceptable types
def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return a + b

# Optional for nullable values
def find_user(user_id: int) -> Optional[Dict[str, Any]]:
    # Returns user dict or None if not found
    pass

# Complex types
def process_data(data: Dict[str, List[int]]) -> Tuple[int, float]:
    total = sum(sum(values) for values in data.values())
    average = total / len(data)
    return total, average
```

### Docstrings (Google Style)
```python
def divide(a: Union[int, float], b: Union[int, float]) -> float:
    """Divide a by b.

    This function performs division with proper error handling for
    edge cases like division by zero and type validation.

    Args:
        a: Number to be divided (dividend)
        b: Number to divide by (divisor)

    Returns:
        The quotient of a divided by b as a float

    Raises:
        TypeError: If inputs are not numbers
        ZeroDivisionError: If b is zero

    Example:
        >>> divide(10, 2)
        5.0
        >>> divide(7, 3)
        2.3333333333333335
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

### Error Handling
```python
# Use specific exception types
def validate_positive_number(value: Union[int, float]) -> None:
    """Validate that a number is positive."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"Expected number, got {type(value).__name__}")

    if value <= 0:
        raise ValueError(f"Expected positive number, got {value}")

# Custom exceptions for domain-specific errors
class CalculationError(Exception):
    """Base exception for calculation-related errors."""
    pass

class InvalidOperationError(CalculationError):
    """Raised when an invalid mathematical operation is attempted."""
    pass

# Use try-except for external dependencies
def load_configuration(file_path: str) -> Dict[str, Any]:
    """Load configuration from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {e}")
```

## Python-Specific Functional Programming

### Prefer Functional Programming Approaches

**Principle**: Favor immutable data, pure functions, and functional patterns over stateful, object-oriented approaches when possible.

### Pure Functions Over Stateful Methods
```python
# Bad - Stateful approach with mutable state
class Calculator:
    def __init__(self):
        self.last_result = 0

    def add_and_store(self, a, b):
        self.last_result = a + b
        return self.last_result

# Good - Pure function approach
def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers and return the result."""
    return a + b

def calculate_with_history(operations: List[Tuple[str, float, float]]) -> List[float]:
    """Calculate multiple operations and return results list."""
    return [
        add(a, b) if op == 'add' else
        subtract(a, b) if op == 'subtract' else
        multiply(a, b) if op == 'multiply' else
        divide(a, b)
        for op, a, b in operations
    ]
```

### Immutable Data Structures
```python
from dataclasses import dataclass
from typing import NamedTuple

# Good - Immutable data with dataclass
@dataclass(frozen=True)
class CalculationResult:
    """Immutable calculation result."""
    value: float
    operation: str
    operands: Tuple[float, ...]

    def with_precision(self, precision: int) -> 'CalculationResult':
        """Return new instance with different precision (immutable update)."""
        rounded_value = round(self.value, precision)
        return CalculationResult(rounded_value, self.operation, self.operands)

# Good - NamedTuple for simple immutable data
class Point(NamedTuple):
    x: float
    y: float

    def translate(self, dx: float, dy: float) -> 'Point':
        """Return new point translated by dx, dy."""
        return Point(self.x + dx, self.y + dy)
```

### Function Composition and Higher-Order Functions
```python
from functools import reduce, partial
from typing import Callable

# Good - Compose simple functions
def validate_number(value: Union[int, float]) -> Union[int, float]:
    """Validate that input is a number."""
    if not isinstance(value, (int, float)):
        raise TypeError("Input must be a number")
    return value

def ensure_positive(value: Union[int, float]) -> Union[int, float]:
    """Ensure number is positive."""
    if value <= 0:
        raise ValueError("Number must be positive")
    return value

def validate_positive_number(value: Union[int, float]) -> Union[int, float]:
    """Compose validation functions."""
    return ensure_positive(validate_number(value))

# Good - Higher-order functions for operations
def create_binary_operation(op: Callable[[float, float], float]) -> Callable[[float, float], float]:
    """Create a validated binary operation."""
    def operation(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        validate_number(a)
        validate_number(b)
        return op(a, b)
    return operation

# Usage
safe_add = create_binary_operation(lambda x, y: x + y)
safe_multiply = create_binary_operation(lambda x, y: x * y)

# Good - Use partial application
multiply_by_tax_rate = partial(lambda price, rate: price * (1 + rate), rate=0.08)
```

### List/Dict Comprehensions and Generator Expressions
```python
# Good - Functional data transformation
def calculate_compound_interest(principal: float, rate: float, periods: int) -> List[float]:
    """Calculate compound interest for each period functionally."""
    return [
        principal * (1 + rate) ** period
        for period in range(1, periods + 1)
    ]

def filter_valid_calculations(results: List[CalculationResult]) -> List[CalculationResult]:
    """Filter out invalid calculation results."""
    return [
        result for result in results
        if result.value is not None and not math.isnan(result.value)
    ]

# Good - Use map/filter/reduce for transformations
def apply_operations(numbers: List[float], operations: List[Callable[[float], float]]) -> List[float]:
    """Apply a series of operations to numbers functionally."""
    return [
        reduce(lambda x, op: op(x), operations, number)
        for number in numbers
    ]
```

### Avoid Side Effects and Mutations
```python
# Bad - Function with side effects
calculation_log = []

def add_with_logging(a: float, b: float) -> float:
    result = a + b
    calculation_log.append(f"{a} + {b} = {result}")  # Side effect!
    return result

# Good - Pure function that returns data
def add_with_log_data(a: float, b: float) -> Tuple[float, str]:
    """Add numbers and return both result and log entry."""
    result = a + b
    log_entry = f"{a} + {b} = {result}"
    return result, log_entry

def process_calculations(operations: List[Tuple[float, float]]) -> Tuple[List[float], List[str]]:
    """Process multiple calculations and return results and logs."""
    results_and_logs = [add_with_log_data(a, b) for a, b in operations]
    results = [result for result, _ in results_and_logs]
    logs = [log for _, log in results_and_logs]
    return results, logs
```

### Use Functional Error Handling Patterns
```python
from typing import Union, Optional
from dataclasses import dataclass

# Good - Result type pattern for error handling
@dataclass(frozen=True)
class Success:
    value: float

@dataclass(frozen=True)
class Error:
    message: str

Result = Union[Success, Error]

def safe_divide(a: float, b: float) -> Result:
    """Divide two numbers with functional error handling."""
    if b == 0:
        return Error("Cannot divide by zero")
    return Success(a / b)

def chain_calculations(value: float, operations: List[Callable[[float], Result]]) -> Result:
    """Chain operations that might fail."""
    current = Success(value)

    for operation in operations:
        if isinstance(current, Error):
            return current
        current = operation(current.value)

    return current

# Good - Optional type for nullable values
def find_calculation_by_id(calculations: List[CalculationResult], calc_id: str) -> Optional[CalculationResult]:
    """Find calculation by ID without exceptions."""
    return next(
        (calc for calc in calculations if calc.operation == calc_id),
        None
    )
```

### Context Managers
```python
# Good - Use context managers for resource management
def read_data_file(file_path: str) -> str:
    """Read data from a file safely."""
    with open(file_path, 'r') as file:
        return file.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def calculation_context(precision: int):
    """Context manager for temporarily setting calculation precision."""
    old_precision = get_current_precision()
    set_precision(precision)
    try:
        yield
    finally:
        set_precision(old_precision)
```

### Dataclasses for Data Structures
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class CalculationResult:
    """Result of a mathematical calculation."""
    value: float
    operation: str
    operands: tuple
    precision: int = 2
    error: Optional[str] = None

    def __str__(self) -> str:
        """String representation of the calculation result."""
        if self.error:
            return f"Error: {self.error}"
        return f"{self.operation}{self.operands} = {self.value:.{self.precision}f}"
```

### List Comprehensions and Generator Expressions
```python
# Good - Use comprehensions for simple transformations
def calculate_squares(numbers: List[int]) -> List[int]:
    """Calculate squares of all numbers in the list."""
    return [num ** 2 for num in numbers]

def filter_positive_numbers(numbers: List[float]) -> List[float]:
    """Filter out negative numbers and zero."""
    return [num for num in numbers if num > 0]

# Use generator expressions for memory efficiency
def sum_of_squares(numbers: List[int]) -> int:
    """Calculate sum of squares efficiently."""
    return sum(num ** 2 for num in numbers)
```

## Python-Specific Anti-Patterns to Avoid

```python
# Bad - Mutable default arguments
def add_item(item, items=[]):
    items.append(item)
    return items

# Good - Use None and create new list
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Bad - Catching generic exceptions
try:
    risky_operation()
except Exception:
    pass

# Good - Catch specific exceptions
try:
    risky_operation()
except (ValueError, TypeError) as e:
    logger.error(f"Invalid input: {e}")
    raise

# Bad - Using bare assert for validation
def divide(a, b):
    assert b != 0
    return a / b

# Good - Use proper exception handling
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

# Bad - Not using f-strings for string formatting
name = "John"
age = 30
message = "Hello, my name is %s and I am %d years old" % (name, age)

# Good - Use f-strings (Python 3.6+)
name = "John"
age = 30
message = f"Hello, my name is {name} and I am {age} years old"

# Bad - Not using pathlib for file operations
import os
file_path = os.path.join("data", "file.txt")
with open(file_path, "r") as f:
    content = f.read()

# Good - Use pathlib
from pathlib import Path
file_path = Path("data") / "file.txt"
content = file_path.read_text()
```

---

**Python-Specific Remember**: Follow PEP 8 style guide, use type hints consistently, write comprehensive docstrings, leverage Python's powerful features (comprehensions, context managers, dataclasses), and prefer functional programming patterns when possible.
