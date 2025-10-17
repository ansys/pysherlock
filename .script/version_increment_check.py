#!/usr/bin/env python3
"""
Simple Version Increment Checker for PySherlock

This script simply checks if the version in pyproject.toml has been incremented
compared to the main branch. It's a basic check to ensure developers update
the version when making changes.
"""

from pathlib import Path
import subprocess
import sys
from typing import Optional, Tuple

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        import toml as tomllib


def run_git_command(command: list) -> Tuple[bool, str]:
    """Run git command and return success status and output."""
    try:
        result = subprocess.run(["git"] + command, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip() if e.stderr else str(e)


def get_current_version() -> Optional[str]:
    """Get current version from pyproject.toml."""
    try:
        with open("pyproject.toml", "r", encoding="utf-8") as f:
            content = f.read()
            # Use toml library for compatibility
            import toml

            data = toml.loads(content)
            return data.get("project", {}).get("version")
    except Exception as e:
        print(f"[ERROR] Error reading pyproject.toml: {e}")
        return None


def get_main_branch_version() -> Optional[str]:
    """Get version from main branch pyproject.toml."""
    try:
        success, output = run_git_command(["show", "origin/main:pyproject.toml"])
        if not success:
            return None

        import toml

        data = toml.loads(output)
        return data.get("project", {}).get("version")
    except Exception as e:
        print(f"[ERROR] Error reading version from main branch: {e}")
        return None


def should_skip_version_check() -> bool:
    """Check if version check should be skipped."""
    # Skip on main branch
    success, output = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
    if success and output in ["main", "master"]:
        print("[INFO] On main branch, skipping version check")
        return True

    # Check for changes - include both committed and staged changes
    has_changes = False

    # Check for committed changes since main
    success, committed_changes = run_git_command(["diff", "--name-only", "origin/main..HEAD"])
    if success and committed_changes.strip():
        print(f"[INFO] Found committed changes: {len(committed_changes.split())} files")
        has_changes = True

    # Check for staged changes
    success, staged_changes = run_git_command(["diff", "--name-only", "--cached"])
    if success and staged_changes.strip():
        print(f"[INFO] Found staged changes: {len(staged_changes.split())} files")
        has_changes = True

    # Check for unstaged changes
    success, unstaged_changes = run_git_command(["diff", "--name-only"])
    if success and unstaged_changes.strip():
        print(f"[INFO] Found unstaged changes: {len(unstaged_changes.split())} files")
        has_changes = True

    if not has_changes:
        print("[INFO] No changes detected (committed, staged, or unstaged), skipping version check")
        return True

    return False


def version_incremented(version1: str, version2: str) -> bool:
    """Check if version2 is greater than version1."""

    def parse_version(version_str: str) -> tuple:
        # Handle dev versions like "0.12.dev0"
        if ".dev" in version_str:
            version_str = version_str.split(".dev")[0]

        # Parse semantic version
        parts = version_str.split(".")
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        return major, minor, patch

    v1_major, v1_minor, v1_patch = parse_version(version1)
    v2_major, v2_minor, v2_patch = parse_version(version2)

    return (v2_major, v2_minor, v2_patch) > (v1_major, v1_minor, v1_patch)


def main():
    """Main entry point for simple version increment checker."""
    print("[INFO] Simple Version Increment Checker for PySherlock")

    # Check if we're in a git repository
    if not Path(".git").exists():
        print("[ERROR] Not in a git repository")
        return 1

    # Check if pyproject.toml exists
    if not Path("pyproject.toml").exists():
        print("[ERROR] pyproject.toml not found")
        return 1

    # Check if we should skip version check
    should_skip = should_skip_version_check()
    if should_skip:
        return 0

    # Get current version
    current_version = get_current_version()
    if not current_version:
        print("[ERROR] Could not read current version")
        return 1

    # Get main branch version
    main_version = get_main_branch_version()
    if not main_version:
        print("[ERROR] Could not read version from main branch")
        return 1

    print(f"[INFO] Main branch version: {main_version}")
    print(f"[INFO] Current branch version: {current_version}")

    # Simple check: was version incremented?
    if version_incremented(main_version, current_version):
        print(f"[SUCCESS] Version was incremented: {main_version} -> {current_version}")
        print("[SUCCESS] Version check passed!")
        return 0
    elif main_version == current_version:
        print(f"[WARNING] Version was not changed from {main_version}")
        print("[INFO] Consider incrementing the version in pyproject.toml to reflect your changes")
        print("[FAIL] Version check failed - version not incremented")
        return 1  # Actually fail instead of warning
    else:
        print(f"[ERROR] Version was decreased: {main_version} -> {current_version}")
        print("[ERROR] This is not recommended and may cause issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
