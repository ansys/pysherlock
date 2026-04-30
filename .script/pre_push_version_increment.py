#!/usr/bin/env python3
"""
Pre-push hook for automatic version increment

This script is called as a pre-push hook to automatically increment
the version before pushing changes to the repository.
"""

from pathlib import Path
import subprocess
import sys


def main():
    """Pre-push hook entry point."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent

    # Path to the main auto increment script
    auto_increment_script = script_dir / "auto_version_increment.py"

    if not auto_increment_script.exists():
        print("❌ Auto increment script not found:", auto_increment_script)
        return 1

    # Run the auto increment script with no confirmation (automated)
    try:
        result = subprocess.run(
            [sys.executable, str(auto_increment_script), "--no-confirm"], check=False
        )

        return result.returncode
    except Exception as e:
        print(f"❌ Error running auto increment: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
