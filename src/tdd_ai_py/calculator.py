"""Calculator module for basic arithmetic operations."""

from typing import Union


class Calculator:
    """A simple calculator class for basic arithmetic operations."""

    def add(
        self, a: Union[int, float], b: Union[int, float]
    ) -> Union[int, float]:
        """Add two numbers together.

        Args:
            a: First number
            b: Second number

        Returns:
            The sum of a and b
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Both arguments must be numbers")
        return a + b

    def subtract(
        self, a: Union[int, float], b: Union[int, float]
    ) -> Union[int, float]:
        """Subtract two numbers.

        Args:
            a: The number to be subtracted from
            b: The number to subtract

        Returns:
            The difference of a and b

        Raises:
            TypeError: If either of the inputs is not a number
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Both arguments must be numbers")
        return a - b

    def multiply(
        self, a: Union[int, float], b: Union[int, float]
    ) -> Union[int, float]:
        """Multiply two numbers.

        Args:
            a: The first number
            b: The second number

        Returns:
            The product of a and b

        Raises:
            TypeError: If either of the inputs is not a number
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Both arguments must be numbers")
        return a * b

    def divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        """Divide a by b.

        Args:
            a: Number to be divided
            b: Number to divide by

        Returns:
            The quotient of a and b

        Raises:
            TypeError: If inputs are not numbers
            ZeroDivisionError: If b is zero
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Both arguments must be numbers")
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
