"""Utilities for text objects."""


from textwrap import dedent
from typing import Any

from beartype import beartype


@beartype
def ensure_str(x: Any, /) -> str:
    """Ensure an object is a string."""
    if isinstance(x, str):
        return x
    msg = f"{x=}"
    raise NotAStringError(msg)


class NotAStringError(TypeError):
    """Raised when an object is not a string."""


@beartype
def strip_and_dedent(text: str, /) -> str:
    """Strip and dedent a string."""
    return dedent(text.strip("\n")).strip("\n")
