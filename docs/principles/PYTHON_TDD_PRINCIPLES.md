# Python Test-Driven Development Principles

## Python-Specific TDD Implementation

### Test Structure (Python Pattern)
```python
def test_returns_sum_when_adding_positive_numbers(self) -> None:
    """Clear description of what behavior is being tested."""
    calculator = Calculator()
    first_number = 5
    second_number = 3

    result = calculator.add(first_number, second_number)

    assert result == 8
```

### Python Test Setup
```python
class TestCalculator:
    """Test cases for the Calculator class."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.calculator = Calculator()

    def teardown_method(self) -> None:
        """Clean up after each test method if needed."""
        pass
```

### Python Test Patterns
```python
# Testing exceptions
def test_raises_exception_when_dividing_by_zero(self) -> None:
    """Test that division by zero raises appropriate exception."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        self.calculator.divide(5, 0)

# Testing floating point precision
def test_maintains_precision_with_floating_point_arithmetic(self) -> None:
    """Test floating point calculations maintain expected precision."""
    result = self.calculator.add(0.1, 0.2)
    assert result == pytest.approx(0.3)

# Parametrized tests
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (1.5, 2.5, 4.0),
])
def test_returns_correct_sum_for_various_inputs(self, a, b, expected):
    """Test addition with various input combinations."""
    result = self.calculator.add(a, b)
    assert result == expected
```

## Python Test Organization

### Test File Structure
```python
"""Tests for the Calculator module."""

import pytest
from unittest.mock import Mock, patch

from myproject.calculator import Calculator


class TestCalculator:
    """Test cases for the Calculator class."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.calculator = Calculator()

    def test_returns_sum_when_adding_positive_numbers(self) -> None:
        """Test that adding positive numbers returns correct sum."""
        # Test implementation
        pass
```

### Pytest Fixtures
```python
import pytest

@pytest.fixture
def calculator():
    """Provide a fresh calculator instance for each test."""
    return Calculator()

@pytest.fixture
def sample_numbers():
    """Provide sample test data."""
    return [1, 2, 3, 4, 5]

@pytest.fixture(scope="session")
def expensive_resource():
    """Provide expensive resource that's created once per test session."""
    resource = create_expensive_resource()
    yield resource
    resource.cleanup()

def test_uses_fixtures(calculator, sample_numbers):
    """Test that uses pytest fixtures."""
    result = calculator.add(sample_numbers[0], sample_numbers[1])
    assert result == 3
```

### Mock for External Dependencies
```python
from unittest.mock import Mock, patch, MagicMock

def test_external_service_integration():
    """Test integration with external service using mocks."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'rate': 0.08}

        tax_calculator = TaxCalculator()
        result = tax_calculator.calculate_tax(100)

        assert result == 8.0
        mock_get.assert_called_once()

def test_with_mock_object():
    """Test using mock objects for dependencies."""
    mock_logger = Mock()
    calculator = Calculator(logger=mock_logger)

    calculator.add(2, 3)

    mock_logger.log.assert_called_with("Addition: 2 + 3 = 5")
```

## Python TDD Patterns

### Property-Based Testing with Hypothesis
```python
from hypothesis import given, strategies as st

@given(
    a=st.floats(min_value=-1000, max_value=1000, allow_nan=False),
    b=st.floats(min_value=-1000, max_value=1000, allow_nan=False)
)
def test_addition_is_commutative(a: float, b: float):
    """Test that addition is commutative for any valid inputs."""
    calculator = Calculator()
    assert calculator.add(a, b) == calculator.add(b, a)

@given(
    numbers=st.lists(st.floats(min_value=0, max_value=100), min_size=1, max_size=10)
)
def test_sum_is_always_positive_for_positive_inputs(numbers: List[float]):
    """Test that sum of positive numbers is always positive."""
    result = sum(numbers)
    assert result >= 0
```

### Testing Pure Functions
```python
# Good - Test pure functions with table-driven tests
@pytest.mark.parametrize("operation, a, b, expected", [
    (add, 2, 3, 5),
    (subtract, 5, 3, 2),
    (multiply, 4, 5, 20),
    (divide, 10, 2, 5.0),
])
def test_pure_operations(operation: Callable, a: float, b: float, expected: float):
    """Test pure mathematical operations."""
    result = operation(a, b)
    assert result == expected

# Good - Test function composition
def test_function_composition():
    """Test that composed functions work correctly."""
    validate_and_double = lambda x: double(validate_positive_number(x))

    result = validate_and_double(5)
    assert result == 10

    with pytest.raises(ValueError):
        validate_and_double(-5)
```

### Testing Immutable Data Structures
```python
def test_immutable_calculation_result():
    """Test that CalculationResult is truly immutable."""
    original = CalculationResult(value=10.0, operation="add", operands=(5.0, 5.0))

    # Creating a new instance with different precision shouldn't modify original
    modified = original.with_precision(3)

    assert original.value == 10.0  # Original unchanged
    assert modified.value == 10.0  # New instance has same value
    assert original is not modified  # Different objects
```

### Testing Error Handling Patterns
```python
def test_result_type_success():
    """Test successful operation with Result type."""
    result = safe_divide(10, 2)

    assert isinstance(result, Success)
    assert result.value == 5.0

def test_result_type_error():
    """Test error case with Result type."""
    result = safe_divide(10, 0)

    assert isinstance(result, Error)
    assert "Cannot divide by zero" in result.message

def test_optional_return_found():
    """Test Optional return when item is found."""
    calculations = [
        CalculationResult(5.0, "add", (2.0, 3.0)),
        CalculationResult(6.0, "multiply", (2.0, 3.0))
    ]

    result = find_calculation_by_id(calculations, "add")

    assert result is not None
    assert result.value == 5.0

def test_optional_return_not_found():
    """Test Optional return when item is not found."""
    calculations = []

    result = find_calculation_by_id(calculations, "add")

    assert result is None
```

## Python TDD Workflow

### Example Python TDD Session
```python
# 1. RED - Write failing test
def test_calculates_power_correctly(self):
    """Test that power calculation returns correct result."""
    result = self.calculator.power(2, 3)
    assert result == 8

# Run test - should fail
# pytest tests/test_calculator.py::TestCalculator::test_calculates_power_correctly

# 2. GREEN - Implement minimal solution
def power(self, base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
    """Calculate base raised to the power of exponent."""
    return base ** exponent

# Run test - should pass
# pytest tests/test_calculator.py::TestCalculator::test_calculates_power_correctly

# 3. REFACTOR - Add type checking, validation, documentation
def power(self, base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
    """Calculate base raised to the power of exponent.

    Args:
        base: The base number
        exponent: The power to raise the base to

    Returns:
        The result of base^exponent

    Raises:
        TypeError: If inputs are not numbers
    """
    self._validate_numeric_inputs(base, exponent)
    return base ** exponent

# Run all tests to ensure nothing broke
# pytest tests/
```

### Test Organization Strategies
```python
# Organize tests by feature/behavior
class TestArithmeticOperations:
    """Tests for basic arithmetic operations."""

    def test_addition_behavior(self):
        pass

    def test_subtraction_behavior(self):
        pass

class TestValidation:
    """Tests for input validation."""

    def test_validates_numeric_inputs(self):
        pass

    def test_handles_invalid_inputs(self):
        pass

class TestErrorHandling:
    """Tests for error conditions."""

    def test_division_by_zero(self):
        pass

    def test_overflow_conditions(self):
        pass
```

### Testing Async Code
```python
import pytest
import asyncio

class TestAsyncCalculator:
    """Tests for asynchronous calculator operations."""

    @pytest.mark.asyncio
    async def test_async_calculation(self):
        """Test asynchronous calculation."""
        calculator = AsyncCalculator()
        result = await calculator.async_add(2, 3)
        assert result == 5

    @pytest.mark.asyncio
    async def test_async_error_handling(self):
        """Test error handling in async operations."""
        calculator = AsyncCalculator()

        with pytest.raises(ValueError):
            await calculator.async_divide(10, 0)
```

## Python Test Configuration

### pytest.ini Configuration
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --strict-config
    --verbose
    --tb=short
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=90
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Make Targets for Python TDD Workflow
```bash
# Testing
test:          # Run pytest
	poetry run pytest

test-cov:      # Run tests with coverage
	poetry run pytest --cov=src --cov-report=term-missing

test-watch:    # Run tests in watch mode (requires pytest-watch)
	poetry run ptw tests/ src/

test-fast:     # Run fast tests only
	poetry run pytest -m "not slow"

# TDD specific targets
tdd:           # Run single test file for TDD workflow
	poetry run pytest $(FILE) -v

red:           # Run tests expecting failures (for RED phase)
	poetry run pytest --tb=short -x

green:         # Run tests expecting all to pass (for GREEN phase)
	poetry run pytest --tb=short

refactor:      # Run all tests after refactoring
	poetry run pytest --cov=src
```

## Python TDD Anti-Patterns to Avoid

```python
# Bad - Testing implementation details
def test_internal_method_call(self):
    """Don't test private methods directly."""
    calculator = Calculator()
    # This test will break during refactoring
    result = calculator._validate_input(5)  # Testing private method
    assert result == 5

# Good - Test behavior through public interface
def test_validates_input_through_public_method(self):
    """Test validation through public interface."""
    calculator = Calculator()
    # This test survives refactoring
    result = calculator.add(5, 3)
    assert result == 8

# Bad - Tests that depend on order
class TestCalculator:
    def test_first_calculation(self):
        self.calculator = Calculator()
        self.result = self.calculator.add(2, 3)
        assert self.result == 5

    def test_second_calculation(self):
        # This test depends on the previous test running first!
        result = self.calculator.add(self.result, 2)
        assert result == 7

# Good - Independent tests
class TestCalculator:
    def setup_method(self):
        self.calculator = Calculator()

    def test_first_calculation(self):
        result = self.calculator.add(2, 3)
        assert result == 5

    def test_second_calculation(self):
        result = self.calculator.add(5, 2)  # Independent test data
        assert result == 7

# Bad - Overly complex test setup
def test_complex_calculation(self):
    # Too much setup obscures what's being tested
    calculator = Calculator()
    calculator.set_precision(3)
    calculator.set_mode("advanced")
    calculator.load_constants_from_file("test_constants.json")
    result = calculator.calculate_complex_formula(x=2, y=3, z=4)
    assert result == expected_complex_result

# Good - Simple, focused test
def test_calculates_formula_correctly(self):
    # Clear, simple test with minimal setup
    calculator = Calculator(precision=3, mode="advanced")

    result = calculator.calculate_formula(x=2, y=3, z=4)

    assert result == pytest.approx(expected_result, abs=0.001)
```

---

**Python TDD Remember**: Use pytest's powerful features (fixtures, parametrize, markers), test behavior not implementation, keep tests simple and independent, and leverage Python's functional features to write testable code.
