"""Monadic error handling with Result types."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")


class Result(Generic[T, E], ABC):
    """Abstract base class for Result monad."""

    @abstractmethod
    def is_ok(self) -> bool:
        """Check if result is successful."""
        pass  # pylint: disable=unnecessary-pass

    @abstractmethod
    def is_err(self) -> bool:
        """Check if result is an error."""
        pass  # pylint: disable=unnecessary-pass

    @abstractmethod
    def map(self, func: Callable[[T], U]) -> "Result[U, E]":
        """Map function over successful value."""
        pass  # pylint: disable=unnecessary-pass

    @abstractmethod
    def map_err(self, func: Callable[[E], U]) -> "Result[T, U]":
        """Map function over error value."""
        pass  # pylint: disable=unnecessary-pass

    @abstractmethod
    def and_then(self, func: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        """Chain operations that may fail."""
        pass  # pylint: disable=unnecessary-pass

    @abstractmethod
    def unwrap(self) -> T:
        """Extract value or raise exception."""
        pass  # pylint: disable=unnecessary-pass

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Extract value or return default."""
        pass  # pylint: disable=unnecessary-pass


@dataclass(frozen=True)
class Ok(Result[T, E]):
    """Successful result containing a value."""

    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def map(self, func: Callable[[T], U]) -> Result[U, E]:
        try:
            return Ok(func(self.value))
        except Exception as e:  # pylint: disable=broad-exception-caught
            return Err(e)  # type: ignore

    def map_err(self, func: Callable[[E], U]) -> Result[T, U]:
        return Ok(self.value)  # type: ignore

    def and_then(self, func: Callable[[T], Result[U, E]]) -> Result[U, E]:
        try:
            return func(self.value)
        except Exception as e:  # pylint: disable=broad-exception-caught
            return Err(e)  # type: ignore

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, default: T) -> T:
        return self.value


@dataclass(frozen=True)
class Err(Result[T, E]):
    """Error result containing an error value."""

    error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def map(self, func: Callable[[T], U]) -> Result[U, E]:
        return Err(self.error)  # type: ignore

    def map_err(self, func: Callable[[E], U]) -> Result[T, U]:
        return Err(func(self.error))  # type: ignore

    def and_then(self, func: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return Err(self.error)  # type: ignore

    def unwrap(self) -> T:
        raise RuntimeError(f"Called unwrap on an Err value: {self.error}")

    def unwrap_or(self, default: T) -> T:
        return default


def safe_call(func: Callable[[], T]) -> Result[T, str]:
    """Safely call a function and return Result."""
    try:
        return Ok(func())
    except Exception as e:  # pylint: disable=broad-exception-caught
        return Err(str(e))


def safe_call_with_args(
    func: Callable[..., T], *args: object, **kwargs: object
) -> Result[T, str]:
    """Safely call a function with arguments and return Result."""
    try:
        return Ok(func(*args, **kwargs))
    except Exception as e:  # pylint: disable=broad-exception-caught
        return Err(str(e))
