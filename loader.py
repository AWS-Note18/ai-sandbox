"""Utilities for loading agent and tool definitions by name.

This module provides a small, dependency-light loader that keeps lookups
deterministic while preventing directory traversal.  The helper mirrors the
structure discussed in the design notes so that callers can simply reference
``load_agent("serena-agent")`` or ``load_tool("find_symbol")`` without
sprinkling ``../`` segments throughout the codebase.

The implementation intentionally avoids any dynamic imports or execution – it
only parses YAML documents into Python dictionaries.  This makes it safe to use
from automated tooling or tests where deterministic behaviour is required.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from core.shared_utils import load_yaml_file, validate_path_safety, SharedLoaderError


BASE_PATH = Path(__file__).resolve().parent


class LoaderError(FileNotFoundError):
    """Raised when a requested agent or tool definition cannot be found."""

def load_agent(agent_name: str) -> Dict[str, Any]:
    """Load ``role/<agent_name>/role.yaml`` and return its parsed contents."""

    if not agent_name or "/" in agent_name or ".." in agent_name:
        raise LoaderError("Agent names must be simple identifiers without path separators.")

    role_dir = validate_path_safety(BASE_PATH / "role" / agent_name, BASE_PATH)
    role_file = role_dir / "role.yaml"
    if not role_file.exists():
        raise LoaderError(f"Agent definition for '{agent_name}' was not found.")
    return load_yaml_file(role_file)


def load_tool(tool_name: str) -> Dict[str, Any]:
    """Load a tool specification by its short name."""

    if not tool_name or "/" in tool_name or ".." in tool_name:
        raise LoaderError("Tool names must be simple identifiers without path separators.")

    tools_root = validate_path_safety(BASE_PATH / "tool", BASE_PATH)
    direct = tools_root / f"{tool_name}.yaml"
    candidates = [direct] if direct.exists() else []

    if not candidates:
        from core.shared_utils import find_files_by_pattern
        pattern = f"**/{tool_name}.yaml"
        candidates = find_files_by_pattern(tools_root, pattern)

    for candidate in candidates:
        if candidate.is_file():
            return load_yaml_file(candidate)

    raise LoaderError(f"Tool specification for '{tool_name}' was not found.")


__all__ = ["load_agent", "load_tool", "LoaderError"]

