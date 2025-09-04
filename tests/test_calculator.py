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
        """Test division of zero by a number."""
        result = self.calculator.divide(0, 5)
        assert result == 0.0
