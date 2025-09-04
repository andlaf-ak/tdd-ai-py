"""Tests for the Calculator module."""

import pytest

from tdd_ai_py.calculator import Calculator


class TestCalculator:
    """Test cases for the Calculator class."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.calculator = Calculator()

    def test_add_positive_numbers(self) -> None:
        """Test addition of positive numbers."""
        result = self.calculator.add(2, 3)
        assert result == 5

    def test_add_negative_numbers(self) -> None:
        """Test addition of negative numbers."""
        result = self.calculator.add(-2, -3)
        assert result == -5

    def test_add_mixed_numbers(self) -> None:
        """Test addition of positive and negative numbers."""
        result = self.calculator.add(5, -3)
        assert result == 2

    def test_add_floats(self) -> None:
        """Test addition of floating point numbers."""
        result = self.calculator.add(2.5, 3.7)
        assert result == pytest.approx(6.2)

    def test_add_invalid_types(self) -> None:
        """Test that addition raises TypeError for invalid input types."""
        with pytest.raises(TypeError, match="Both arguments must be numbers"):
            self.calculator.add("2", 3)  # type: ignore

        with pytest.raises(TypeError, match="Both arguments must be numbers"):
            self.calculator.add(2, "3")  # type: ignore

    def test_subtract_positive_numbers(self) -> None:
        """Test subtraction of positive numbers."""
        result = self.calculator.subtract(5, 3)
        assert result == 2

    def test_subtract_negative_result(self) -> None:
        """Test subtraction resulting in negative number."""
        result = self.calculator.subtract(3, 5)
        assert result == -2

    def test_subtract_floats(self) -> None:
        """Test subtraction of floating point numbers."""
        result = self.calculator.subtract(5.5, 2.3)
        assert result == pytest.approx(3.2)

    def test_subtract_invalid_types(self) -> None:
        """Test that subtraction raises TypeError for invalid input types."""
        with pytest.raises(TypeError, match="Both arguments must be numbers"):
            self.calculator.subtract("5", 3)  # type: ignore

    def test_multiply_positive_numbers(self) -> None:
        """Test multiplication of positive numbers."""
        result = self.calculator.multiply(4, 5)
        assert result == 20

    def test_multiply_by_zero(self) -> None:
        """Test multiplication by zero."""
        result = self.calculator.multiply(5, 0)
        assert result == 0

    def test_multiply_negative_numbers(self) -> None:
        """Test multiplication of negative numbers."""
        result = self.calculator.multiply(-3, -4)
        assert result == 12

    def test_multiply_floats(self) -> None:
        """Test multiplication of floating point numbers."""
        result = self.calculator.multiply(2.5, 4.0)
        assert result == pytest.approx(10.0)

    def test_multiply_invalid_types(self) -> None:
        """Test that multiplication raises TypeError for invalid input types."""
        with pytest.raises(TypeError, match="Both arguments must be numbers"):
            self.calculator.multiply("4", 5)  # type: ignore

    def test_divide_positive_numbers(self) -> None:
        """Test division of positive numbers."""
        result = self.calculator.divide(10, 2)
        assert result == 5.0

    def test_divide_floats(self) -> None:
        """Test division of floating point numbers."""
        result = self.calculator.divide(7.5, 2.5)
        assert result == pytest.approx(3.0)

    def test_divide_by_zero(self) -> None:
        """Test that division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            self.calculator.divide(5, 0)

    def test_divide_invalid_types(self) -> None:
        """Test that division raises TypeError for invalid input types."""
        with pytest.raises(TypeError, match="Both arguments must be numbers"):
            self.calculator.divide("10", 2)  # type: ignore

    def test_divide_zero_by_number(self) -> None:
        """Test dividing zero by a number."""
        result = self.calculator.divide(0, 5)
        assert result == 0.0

    def test_chained_operations(self) -> None:
        """Test chaining multiple calculator operations together."""
        # Test: (10 + 5) * 2 - 8 / 4 = 15 * 2 - 2 = 30 - 2 = 28
        step1 = self.calculator.add(10, 5)  # 15
        step2 = self.calculator.multiply(step1, 2)  # 30
        step3 = self.calculator.divide(8, 4)  # 2
        result = self.calculator.subtract(step2, step3)  # 28
        assert result == 28

    def test_calculator_with_zero(self) -> None:
        """Test calculator operations involving zero."""
        # Addition with zero
        assert self.calculator.add(5, 0) == 5
        assert self.calculator.add(0, 5) == 5

        # Subtraction with zero
        assert self.calculator.subtract(5, 0) == 5
        assert self.calculator.subtract(0, 5) == -5

        # Multiplication with zero
        assert self.calculator.multiply(5, 0) == 0
        assert self.calculator.multiply(0, 5) == 0

    def test_calculator_precision_edge_cases(self) -> None:
        """Test calculator with precision edge cases for floating point numbers."""
        # Test very small numbers
        result = self.calculator.add(0.1, 0.2)
        assert result == pytest.approx(0.3)

        # Test very large numbers
        large_num1 = 1e10
        large_num2 = 2e10
        result = self.calculator.add(large_num1, large_num2)
        assert result == pytest.approx(3e10)

        # Test division resulting in repeating decimal
        result = self.calculator.divide(1, 3)
        assert result == pytest.approx(0.3333333333333333)
