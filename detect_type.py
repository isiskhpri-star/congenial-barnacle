"""Utility module for detecting the type of a variable."""

import collections
import datetime
import re
from typing import Any


def detect_type(variable: Any) -> dict:
    """Detect the type of a variable and return detailed type information.

    Args:
        variable: The variable whose type should be detected.

    Returns:
        A dictionary containing:
            - type: The basic type name (e.g., "int", "str", "list").
            - full_type: The fully qualified type name including module.
            - category: A high-level category (e.g., "numeric", "sequence",
              "mapping", "boolean", "none", "text", "binary", "set",
              "callable", "datetime", "regex", "other").
            - is_iterable: Whether the variable supports iteration.
            - is_mutable: Whether the variable is a mutable type.
            - length: The length of the variable if applicable, else None.
    """
    var_type = type(variable)
    type_name = var_type.__name__
    module = var_type.__module__
    full_type = f"{module}.{type_name}" if module != "builtins" else type_name

    category = _categorize(variable)

    is_iterable = _is_iterable(variable)

    is_mutable = _is_mutable(variable)

    length = None
    try:
        length = len(variable)
    except TypeError:
        pass

    return {
        "type": type_name,
        "full_type": full_type,
        "category": category,
        "is_iterable": is_iterable,
        "is_mutable": is_mutable,
        "length": length,
    }


def _categorize(variable: Any) -> str:
    """Return a high-level category string for the variable."""
    if variable is None:
        return "none"
    if isinstance(variable, bool):
        return "boolean"
    if isinstance(variable, (int, float, complex)):
        return "numeric"
    if isinstance(variable, str):
        return "text"
    if isinstance(variable, (bytes, bytearray, memoryview)):
        return "binary"
    if isinstance(variable, dict):
        return "mapping"
    if isinstance(variable, (list, tuple, range)):
        return "sequence"
    if isinstance(variable, (set, frozenset)):
        return "set"
    if callable(variable):
        return "callable"
    if isinstance(variable, (datetime.date, datetime.time, datetime.datetime)):
        return "datetime"
    if isinstance(variable, re.Pattern):
        return "regex"
    return "other"


def _is_iterable(variable: Any) -> bool:
    """Check whether the variable supports iteration."""
    try:
        iter(variable)
        return True
    except TypeError:
        return False


def _is_mutable(variable: Any) -> bool:
    """Check whether the variable is a commonly known mutable type."""
    return isinstance(variable, (list, dict, set, bytearray))


def detect_type_name(variable: Any) -> str:
    """Return just the type name of the variable as a string.

    Args:
        variable: The variable whose type name should be detected.

    Returns:
        The type name as a string (e.g., "int", "str", "list").
    """
    return type(variable).__name__


# --- Demo ---
if __name__ == "__main__":
    samples = [
        42,
        3.14,
        2 + 3j,
        "hello",
        True,
        None,
        [1, 2, 3],
        (1, 2, 3),
        {"a": 1, "b": 2},
        {1, 2, 3},
        frozenset([1, 2]),
        b"bytes",
        bytearray(b"mutable bytes"),
        range(10),
        lambda x: x,
        datetime.datetime.now(),
        re.compile(r"\d+"),
    ]

    for sample in samples:
        info = detect_type(sample)
        print(f"Value: {str(sample):<30} | Type: {info['type']:<15} | "
              f"Category: {info['category']:<10} | Iterable: {info['is_iterable']} | "
              f"Mutable: {info['is_mutable']} | Length: {info['length']}")
