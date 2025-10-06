#!/usr/bin/env python3
"""
Automatic Version Incrementer for PySherlock

This script automatically increments the version in pyproject.toml based on:
1. Changelog entries (using towncrier fragments)
2. Git commit messages
3. File changes analysis

It runs as a pre-push hook to automatically bump version before merging.
"""

from enum import Enum
from pathlib import Path
import re
import subprocess
import sys
from typing import List, Optional, Tuple

import toml


class VersionBumpType(Enum):
    PATCH = "patch"
    MINOR = "minor"
    MAJOR = "major"


class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    BOLD = "\033[1m"
    NC = "\033[0m"


def log(message: str, color: str = Colors.NC):
    """Print colored log message."""
    print(f"{color}{message}{Colors.NC}")


def run_git_command(command: List[str]) -> Tuple[bool, str]:
    """Run git command and return success status and output."""
    try:
        result = subprocess.run(["git"] + command, capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip() if e.stderr else str(e)


def parse_version(version_str: str) -> Tuple[int, int, int, str]:
    """Parse semantic version string into components."""
    # Handle dev versions like "0.12.dev0"
    if ".dev" in version_str:
        version_str = version_str.split(".dev")[0]

    # Parse semantic version
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(.*)$", version_str)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3))
        suffix = match.group(4)
        return major, minor, patch, suffix

    # Fallback for incomplete versions
    parts = version_str.split(".")
    major = int(parts[0]) if len(parts) > 0 else 0
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    return major, minor, patch, ""


def increment_version(version_str: str, bump_type: VersionBumpType) -> str:
    """Increment version based on bump type."""
    major, minor, patch, suffix = parse_version(version_str)

    if bump_type == VersionBumpType.MAJOR:
        major += 1
        minor = 0
        patch = 0
    elif bump_type == VersionBumpType.MINOR:
        minor += 1
        patch = 0
    else:  # PATCH
        patch += 1

    # Remove dev suffix for releases
    return f"{major}.{minor}.{patch}"


def analyze_changelog_fragments() -> VersionBumpType:
    """Analyze towncrier changelog fragments to determine version bump."""
    changelog_dir = Path("doc/changelog.d")
    if not changelog_dir.exists():
        return VersionBumpType.PATCH

    fragment_files = list(changelog_dir.glob("*.*.md"))
    if not fragment_files:
        return VersionBumpType.PATCH

    # Analyze fragment types for version bump determination
    has_breaking = False
    has_feature = False
    has_fix = False

    for fragment in fragment_files:
        fragment_name = fragment.stem
        if any(keyword in fragment_name.lower() for keyword in ["added", "changed"]):
            if any(
                breaking in fragment.read_text().lower()
                for breaking in ["breaking", "breaking change", "incompatible"]
            ):
                has_breaking = True
            else:
                has_feature = True
        elif "fixed" in fragment_name.lower():
            has_fix = True

    # Determine bump type based on changes
    if has_breaking:
        return VersionBumpType.MAJOR
    elif has_feature:
        return VersionBumpType.MINOR
    else:
        return VersionBumpType.PATCH


def analyze_commit_messages() -> VersionBumpType:
    """Analyze commit messages since last tag to determine version bump."""
    # Get commits since last tag
    success, output = run_git_command(["describe", "--tags", "--abbrev=0"])
    if not success:
        # No tags exist, analyze all commits on branch
        success, output = run_git_command(["log", "--oneline", "origin/main..HEAD"])
    else:
        last_tag = output
        success, output = run_git_command(["log", f"{last_tag}..HEAD", "--oneline"])

    if not success or not output:
        return VersionBumpType.PATCH

    commit_messages = output.lower()

    # Check for breaking changes
    breaking_keywords = [
        "breaking change",
        "breaking:",
        "break:",
        "major:",
        "incompatible",
        "remove",
        "delete api",
    ]
    if any(keyword in commit_messages for keyword in breaking_keywords):
        return VersionBumpType.MAJOR

    # Check for new features
    feature_keywords = [
        "feat:",
        "feature:",
        "add:",
        "new:",
        "minor:",
        "implement",
        "enhance",
        "improvement",
    ]
    if any(keyword in commit_messages for keyword in feature_keywords):
        return VersionBumpType.MINOR

    # Default to patch for fixes, docs, etc.
    return VersionBumpType.PATCH


def analyze_code_changes() -> VersionBumpType:
    """Analyze code changes to determine appropriate version bump."""
    # Get changed files
    success, output = run_git_command(["diff", "--name-only", "origin/main..HEAD"])

    if not success:
        return VersionBumpType.PATCH

    changed_files = output.split("\n") if output else []

    # Analyze types of changes
    has_api_changes = False
    has_new_features = False
    has_breaking_changes = False

    for file in changed_files:
        file_lower = file.lower()

        # Check for API changes
        if any(
            pattern in file
            for pattern in ["src/ansys/sherlock/core/", "__init__.py", "api", "interface"]
        ):
            # Get the actual diff to analyze
            success, diff_output = run_git_command(["diff", "origin/main..HEAD", "--", file])

            if success and diff_output:
                diff_lower = diff_output.lower()

                # Look for breaking changes
                if any(
                    pattern in diff_lower
                    for pattern in [
                        "-def ",
                        "-class ",
                        "removed",
                        "deprecated",
                        "raise notimplementederror",
                        "breaking",
                    ]
                ):
                    has_breaking_changes = True

                # Look for new features (new functions/classes)
                if any(
                    pattern in diff_lower
                    for pattern in ["+def ", "+class ", "new feature", "implement"]
                ):
                    has_new_features = True

                # Look for API changes
                if "+def " in diff_lower or "+class " in diff_lower:
                    has_api_changes = True

    # Determine version bump
    if has_breaking_changes:
        return VersionBumpType.MAJOR
    elif has_new_features or has_api_changes:
        return VersionBumpType.MINOR
    else:
        return VersionBumpType.PATCH


def determine_version_bump() -> VersionBumpType:
    """Determine the appropriate version bump by analyzing multiple sources."""
    log("🔍 Analyzing changes to determine version bump...", Colors.BLUE)

    # Analyze different sources
    changelog_bump = analyze_changelog_fragments()
    commit_bump = analyze_commit_messages()
    code_bump = analyze_code_changes()

    log(f"📋 Changelog analysis suggests: {changelog_bump.value}", Colors.BLUE)
    log(f"💬 Commit message analysis suggests: {commit_bump.value}", Colors.BLUE)
    log(f"📝 Code changes analysis suggests: {code_bump.value}", Colors.BLUE)

    # Choose the highest priority bump type
    bump_priority = {VersionBumpType.MAJOR: 3, VersionBumpType.MINOR: 2, VersionBumpType.PATCH: 1}

    all_bumps = [changelog_bump, commit_bump, code_bump]
    final_bump = max(all_bumps, key=lambda x: bump_priority[x])

    log(f"🎯 Final decision: {final_bump.value} version bump", Colors.GREEN)
    return final_bump


def get_current_version() -> Optional[str]:
    """Get current version from pyproject.toml."""
    try:
        with open("pyproject.toml", "r") as f:
            data = toml.load(f)
            return data.get("project", {}).get("version")
    except Exception as e:
        log(f"Error reading pyproject.toml: {e}", Colors.RED)
        return None


def update_version_in_pyproject(new_version: str) -> bool:
    """Update version in pyproject.toml file."""
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()

        # Replace version using regex to preserve formatting
        updated_content = re.sub(
            r'^version = "[^"]*"', f'version = "{new_version}"', content, flags=re.MULTILINE
        )

        if updated_content == content:
            log("❌ Could not find version field in pyproject.toml", Colors.RED)
            return False

        with open("pyproject.toml", "w") as f:
            f.write(updated_content)

        return True
    except Exception as e:
        log(f"Error updating pyproject.toml: {e}", Colors.RED)
        return False


def should_skip_version_increment() -> bool:
    """Check if version increment should be skipped."""
    current_branch = ""
    success, output = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
    if success:
        current_branch = output

    # Skip on main branch
    if current_branch in ["main", "master"]:
        log("ℹ️  On main branch, skipping auto-increment", Colors.YELLOW)
        return True

    # Skip if no changes since main
    success, output = run_git_command(["diff", "--name-only", "origin/main..HEAD"])

    if not success or not output.strip():
        log("ℹ️  No changes detected, skipping auto-increment", Colors.YELLOW)
        return True

    # Check if version was already manually updated
    success, output = run_git_command(
        ["diff", "origin/main..HEAD", "--name-only", "pyproject.toml"]
    )

    if success and "pyproject.toml" in output:
        # Check if version line was changed
        success, diff_output = run_git_command(["diff", "origin/main..HEAD", "pyproject.toml"])

        if success and "version = " in diff_output:
            log("ℹ️  Version already manually updated, skipping auto-increment", Colors.YELLOW)
            return True

    return False


def commit_version_change(old_version: str, new_version: str, bump_type: VersionBumpType):
    """Commit the version change."""
    log("📝 Committing version change...", Colors.BLUE)

    # Stage the pyproject.toml file
    success, _ = run_git_command(["add", "pyproject.toml"])
    if not success:
        log("❌ Failed to stage pyproject.toml", Colors.RED)
        return False

    # Create commit message
    commit_msg = f"chore: bump version from {old_version} to {new_version} ({bump_type.value})"

    # Commit the change
    success, _ = run_git_command(["commit", "-m", commit_msg])
    if not success:
        log("❌ Failed to commit version change", Colors.RED)
        return False

    log(f"✅ Committed version bump: {old_version} → {new_version}", Colors.GREEN)
    return True


def main():
    """Main entry point for automatic version incrementer."""
    log("🚀 Automatic Version Incrementer for PySherlock", Colors.BOLD)

    # Check if we're in a git repository
    if not Path(".git").exists():
        log("❌ Not in a git repository", Colors.RED)
        return 1

    # Check if pyproject.toml exists
    if not Path("pyproject.toml").exists():
        log("❌ pyproject.toml not found", Colors.RED)
        return 1

    # Check if we should skip version increment
    if should_skip_version_increment():
        return 0

    # Get current version
    current_version = get_current_version()
    if not current_version:
        log("❌ Could not read current version", Colors.RED)
        return 1

    log(f"📦 Current version: {current_version}", Colors.BLUE)

    # Determine version bump type
    bump_type = determine_version_bump()

    # Calculate new version
    new_version = increment_version(current_version, bump_type)

    log(f"🎯 Bumping version: {current_version} → {new_version} ({bump_type.value})", Colors.GREEN)

    # Confirm with user (optional - can be disabled for full automation)
    if "--no-confirm" not in sys.argv:
        response = input(f"\nProceed with version bump to {new_version}? (Y/n): ").lower().strip()
        if response and response not in ["y", "yes"]:
            log("❌ Version bump cancelled by user", Colors.YELLOW)
            return 1

    # Update version in pyproject.toml
    if not update_version_in_pyproject(new_version):
        return 1

    log(f"✅ Updated pyproject.toml with version {new_version}", Colors.GREEN)

    # Commit the change
    if not commit_version_change(current_version, new_version, bump_type):
        return 1

    log("\n🎉 Version auto-increment completed successfully!", Colors.GREEN)
    log(f"📦 New version: {new_version}", Colors.BOLD)

    return 0


if __name__ == "__main__":
    sys.exit(main())
