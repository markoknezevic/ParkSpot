"""Marshmallow helpers for API responses."""

from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from marshmallow import Schema


P = ParamSpec("P")
R = TypeVar("R")


def marshal_with(
    schema: Schema,
) -> Callable[[Callable[P, R]], Callable[P, dict[str, Any]]]:
    """Serialize a route's return value with a Marshmallow schema."""

    def decorator(function: Callable[P, R]) -> Callable[P, dict[str, Any]]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> dict[str, Any]:
            return schema.dump(function(*args, **kwargs))

        return wrapper

    return decorator
