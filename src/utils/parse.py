
"""
utils/parse.py

Small helper utilities for safely accessing nested dictionaries, without
pulling in heavy dependencies.

Kept intentionally minimal and deterministic.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional


def get_nested(
    data: Mapping[str, Any],
    path: Iterable[str],
    default: Optional[Any] = None,
) -> Any:
    """
    Safely get a nested value from a mapping using a path of keys.

    Parameters
    ----------
    data : Mapping[str, Any]
        The dictionary-like object to traverse.
    path : Iterable[str]
        A sequence of keys representing the nested path.
    default : Any, optional
        Value to return if any key is missing.

    Returns
    -------
    Any
        The value at the nested path, or `default` if not found.
    """
    current: Any = data
    for key in path:
        if not isinstance(current, Mapping):
            return default
        if key not in current:
            return default
        current = current[key]
    return current
