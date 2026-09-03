# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Script to generate requirements-for-safety.txt from pyproject.toml.

This script extracts project dependencies from pyproject.toml and writes them
to requirements-for-safety.txt, which is used by the safety vulnerability checker.
"""

from pathlib import Path
import sys

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def generate_requirements_for_safety() -> None:
    """
    Generate requirements-for-safety.txt from pyproject.toml.

    Raises
    ------
    FileNotFoundError
        If pyproject.toml is not found.
    """
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {pyproject_path.absolute()}")

    # Read and parse pyproject.toml
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomllib.load(f)

    # Extract dependencies from the [project] section
    dependencies = pyproject_data.get("project", {}).get("dependencies", [])

    if not dependencies:
        print("Warning: No dependencies found in pyproject.toml")
        dependencies = []

    # Write to output file (overwrites if exists)
    output_path = Path("requirements-for-safety.txt")
    with open(output_path, "w") as f:
        f.write(
            "# Project dependencies for safety vulnerability scanning\n"
            "# Auto-generated from pyproject.toml - do not edit manually\n"
            "# Run: python generate_requirements_for_safety.py\n\n"
        )
        for dep in dependencies:
            f.write(f"{dep}\n")

    print(f"  Successfully generated: {output_path.absolute()}")
    print(f"  Dependencies: {len(dependencies)}")
    for dep in dependencies:
        print(f"    - {dep}")


if __name__ == "__main__":
    try:
        generate_requirements_for_safety()
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
