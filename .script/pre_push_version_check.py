#!/usr/bin/env python3
"""
Pre-push hook for version increment validation

This script is called as a pre-push hook to check whether the developer
has manually incremented the version before pushing changes to the repository.
"""

from pathlib import Path
import subprocess
import sys


def main():
    """Pre-push hook entry point."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent

    # Path to the main version check script
    version_check_script = script_dir / "version_increment_check.py"

    if not version_check_script.exists():
        print("❌ Version check script not found:", version_check_script)
        return 1

    # Run the version check script
    try:
        result = subprocess.run([sys.executable, str(version_check_script)], check=False)

        return result.returncode
    except Exception as e:
        print(f"❌ Error running version check: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
