"""
Shared utilities for the AI Agent Framework.

This module contains common functions used across different parts of the system
to eliminate code duplication and improve maintainability.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple
import re

try:  # pragma: no cover - dependency optionality
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - fallback handled below
    yaml = None


class SharedLoaderError(FileNotFoundError):
    """Raised when a requested file cannot be found."""


def load_yaml_file(path: Path) -> Dict[str, Any]:
    """Parse a YAML file and return a dictionary.

    This is a shared implementation used by both loader.py and validate.py
    to avoid code duplication.
    """
    with path.open("r", encoding="utf-8") as handle:
        text = handle.read()

    if yaml is not None:
        try:
            data = yaml.safe_load(text) or {}
        except yaml.YAMLError as exc:  # pragma: no cover - transparent re-raise
            raise SharedLoaderError(f"Failed to parse YAML at '{path}': {exc}") from exc
        return data if isinstance(data, dict) else {}

    return _fallback_yaml_load(text)


def _fallback_yaml_load(text: str) -> Dict[str, Any]:
    """Parse a minimal subset of YAML without third-party dependencies.

    Shared fallback implementation for YAML parsing.
    """
    tokens = _tokenise_yaml(text)
    stream = _TokenStream(tokens)
    document = _parse_mapping(stream, 0)
    return document


def _tokenise_yaml(text: str) -> List[Tuple[int, str]]:
    """Tokenize YAML text into indentation and content pairs."""
    tokens: List[Tuple[int, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if "\t" in line[:indent]:
            raise SharedLoaderError("Tabs are not supported in YAML indentation.")
        tokens.append((indent, stripped))
    return tokens


class _TokenStream:
    """Simple token stream for YAML parsing."""
    def __init__(self, tokens: List[Tuple[int, str]]):
        self._tokens = tokens
        self._index = 0

    def peek(self) -> Tuple[int, str] | None:
        if self._index >= len(self._tokens):
            return None
        return self._tokens[self._index]

    def pop(self) -> Tuple[int, str] | None:
        token = self.peek()
        if token is not None:
            self._index += 1
        return token


def _parse_mapping(stream: _TokenStream, current_indent: int) -> Dict[str, Any]:
    """Parse a YAML mapping (dictionary)."""
    mapping: Dict[str, Any] = {}

    while True:
        token = stream.peek()
        if token is None:
            break
        indent, content = token
        if indent < current_indent:
            break
        if indent > current_indent:
            raise SharedLoaderError("Invalid indentation in YAML mapping.")

        stream.pop()
        if content.startswith("- "):
            raise SharedLoaderError("List item encountered where a mapping key was expected.")

        key, _, value_part = content.partition(":")
        key = key.strip()
        value_part = value_part.strip()

        if value_part:
            mapping[key] = _parse_scalar(value_part)
            continue

        next_token = stream.peek()
        if next_token is None or next_token[0] <= indent:
            mapping[key] = {}
            continue

        if next_token[1].startswith("- "):
            mapping[key] = _parse_sequence(stream, indent + 2)
        else:
            mapping[key] = _parse_mapping(stream, next_token[0])

    return mapping


def _parse_sequence(stream: _TokenStream, base_indent: int) -> List[Any]:
    """Parse a YAML sequence (list)."""
    sequence: List[Any] = []

    while True:
        token = stream.peek()
        if token is None:
            break
        indent, content = token
        if indent < base_indent or not content.startswith("- "):
            break

        stream.pop()
        value_part = content[2:].strip()
        if value_part:
            sequence.append(_parse_scalar(value_part))
            continue

        next_token = stream.peek()
        if next_token is None or next_token[0] <= indent:
            sequence.append({})
            continue

        if next_token[1].startswith("- "):
            sequence.append(_parse_sequence(stream, next_token[0]))
        else:
            sequence.append(_parse_mapping(stream, next_token[0]))

    return sequence


def _parse_scalar(value: str) -> Any:
    """Parse a YAML scalar value."""
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if lower in {"null", "~"}:
        return None
    # attempt integer then float parsing
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    # Try to parse as number
    try:
        if '.' in value:
            return float(value)
        return int(value)
    except ValueError:
        pass
    return value


def validate_path_safety(path: Path, base_path: Path) -> Path:
    """Validate that a path stays within the repository boundary."""
    resolved = path.resolve()
    if not resolved.is_relative_to(base_path):
        raise SharedLoaderError(f"Access to '{path}' is outside of the repository root.")
    return resolved


def find_files_by_pattern(directory: Path, pattern: str) -> List[Path]:
    """Find files matching a pattern in a directory recursively."""
    return list(directory.rglob(pattern))


__all__ = [
    "load_yaml_file",
    "validate_path_safety",
    "find_files_by_pattern",
    "SharedLoaderError"
]