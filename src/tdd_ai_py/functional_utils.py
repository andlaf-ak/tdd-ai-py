"""Functional programming utilities for composition and pipelines."""

from functools import reduce
from typing import Any, Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def pipe(value: T, *functions: Callable[[Any], Any]) -> Any:
    """Functional composition pipeline.

    Applies functions in sequence to transform the initial value.

    Args:
        value: Initial value to transform
        *functions: Functions to apply in sequence

    Returns:
        Final transformed value

    Example:
        result = pipe(5, lambda x: x * 2, lambda x: x + 1)  # Returns 11
    """
    return reduce(lambda acc, func: func(acc), functions, value)


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose functions from right to left.

    Args:
        *functions: Functions to compose

    Returns:
        Composed function

    Example:
        add_one_then_double = compose(lambda x: x * 2, lambda x: x + 1)
        result = add_one_then_double(5)  # Returns 12
    """

    def composed(value: Any) -> Any:
        return reduce(lambda acc, func: func(acc), reversed(functions), value)

    return composed


def curry(func: Callable) -> Callable:
    """Simple currying decorator for partial application.

    Args:
        func: Function to curry

    Returns:
        Curried version of the function
    """

    def curried(*args: object, **kwargs: object) -> Callable[..., Any]:
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)  # type: ignore
        return lambda *more_args, **more_kwargs: curried(
            *(args + more_args), **{**kwargs, **more_kwargs}
        )

    return curried
