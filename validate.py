#!/usr/bin/env python3
import os
import sys
import json
import re

# Import shared utilities to eliminate code duplication
from pathlib import Path
from core.shared_utils import load_yaml_file

def main():
    # This script must be run from the root of the repository.
    try:
        from jsonschema import validate, ValidationError
    except ImportError:
        print("Error: jsonschema is not installed. Please run 'pip install jsonschema'", file=sys.stderr)
        sys.exit(1)

    print("--- Running Configuration Validator ---")

    # Load schemas
    try:
        with open('schemas/role_schema.json', 'r') as f:
            role_schema = json.load(f)
        with open('schemas/tool_schema.json', 'r') as f:
            tool_schema = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: Could not load schema files. Make sure you are in the repo root.", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    error_count = 0

    # Validate roles
    print("\nValidating roles in /role/...")
    for root, _, files in os.walk('role'):
        for file in files:
            if file.endswith('.yaml'):
                path = os.path.join(root, file)
                try:
                    instance = load_yaml_file(Path(path))
                    validate(instance=instance, schema=role_schema)
                    print(f"  ✅ {path}")
                except (ValidationError, Exception) as e:
                    print(f"  ❌ {path} - Validation Failed!")
                    print(f"     {e}")
                    error_count += 1

    # Validate tools
    print("\nValidating tools in /tool/...")
    for root, _, files in os.walk('tool'):
        for file in files:
            if file.endswith('.yaml'):
                path = os.path.join(root, file)
                try:
                    instance = load_yaml_file(Path(path))
                    validate(instance=instance, schema=tool_schema)
                    print(f"  ✅ {path}")
                except (ValidationError, Exception) as e:
                    print(f"  ❌ {path} - Validation Failed!")
                    print(f"     {e}")
                    error_count += 1

    if error_count > 0:
        print(f"\n--- Validation Complete: Found {error_count} errors. ---")
        sys.exit(1)
    else:
        print("\n--- Validation Complete: All configuration files are valid! ---")

if __name__ == "__main__":
    main()
