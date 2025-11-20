"""
constraint_loader.py

Minimal loader for structured multimodal constraint specs.

This module is intentionally simple: it only parses YAML into a Python dict
and does a light sanity check. All higher-level logic is left to callers.
"""

from __future__ import annotations

import os
from typing import Any, Dict

import yaml


class ConstraintLoadError(Exception):
    """Raised when the constraint file cannot be loaded or parsed."""


def load_constraints(path: str) -> Dict[str, Any]:
    """
    Load a constraint specification from a YAML file.

    Parameters
    ----------
    path : str
        Path to the YAML file.

    Returns
    -------
    Dict[str, Any]
        Parsed constraint dictionary.

    Raises
    ------
    ConstraintLoadError
        If file is missing, unreadable, or invalid YAML.
    """
    if not os.path.exists(path):
        raise ConstraintLoadError(f"Constraint file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as exc:  # noqa: BLE001
        raise ConstraintLoadError(f"Failed to read constraint file: {exc}") from exc

    if not isinstance(data, dict):
        raise ConstraintLoadError(
            f"Constraint file must parse to a mapping, got: {type(data)!r}"
        )

    # Minimal sanity checks (kept intentionally light)
    for key in ("INTENT", "ANCHOR", "CONTROL", "OUTPUT"):
        if key not in data:
            # Do not fail hard; just warn via comment field
            data.setdefault("_warnings", []).append(
                f"Top-level key {key!r} missing from constraint spec."
            )

    return data
