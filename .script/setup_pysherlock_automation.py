#!/usr/bin/env python3
"""
Setup automatic version increment for PySherlock

This script sets up the automation to automatically increment versions
in PySherlock when changes are pushed.
"""

from pathlib import Path
import shutil
import subprocess
import sys


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


def run_command(command: list, check: bool = True) -> tuple[bool, str]:
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip() if e.stderr else str(e)


def check_prerequisites():
    """Check if all prerequisites are installed."""
    log("🔍 Checking prerequisites...", Colors.BLUE)

    # Check if we're in PySherlock repository
    if not Path("pyproject.toml").exists():
        log("❌ pyproject.toml not found. Are you in the PySherlock repository?", Colors.RED)
        return False

    # Check if it's actually PySherlock
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()
            if "ansys-sherlock-core" not in content and "pysherlock" not in content.lower():
                log("❌ This doesn't appear to be the PySherlock repository", Colors.RED)
                return False
    except Exception as e:
        log(f"❌ Error reading pyproject.toml: {e}", Colors.RED)
        return False

    # Check git
    success, _ = run_command(["git", "--version"])
    if not success:
        log("❌ Git is not installed or not accessible", Colors.RED)
        return False

    # Check Python
    success, _ = run_command([sys.executable, "--version"])
    if not success:
        log("❌ Python is not accessible", Colors.RED)
        return False

    log("✅ Prerequisites check passed", Colors.GREEN)
    return True


def install_dependencies():
    """Install required dependencies."""
    log("📦 Installing dependencies...", Colors.BLUE)

    dependencies = ["toml", "pre-commit"]

    for dep in dependencies:
        log(f"Installing {dep}...", Colors.BLUE)
        success, output = run_command([sys.executable, "-m", "pip", "install", dep])

        if not success:
            log(f"❌ Failed to install {dep}: {output}", Colors.RED)
            return False

        log(f"✅ {dep} installed successfully", Colors.GREEN)

    return True


def setup_automation_scripts():
    """Copy automation scripts to PySherlock repository."""
    log("📄 Setting up automation scripts...", Colors.BLUE)

    # Create automation directory in PySherlock
    automation_dir = Path(".pysherlock-automation")
    automation_dir.mkdir(exist_ok=True)

    # Get current script directory
    current_dir = Path(__file__).parent

    # Scripts to copy
    scripts_to_copy = ["auto_version_increment.py", "pre_push_version_increment.py"]

    for script in scripts_to_copy:
        source = current_dir / script
        dest = automation_dir / script

        if not source.exists():
            log(f"❌ Source script not found: {source}", Colors.RED)
            return False

        try:
            shutil.copy2(source, dest)
            # Make executable
            dest.chmod(0o755)
            log(f"✅ Copied {script}", Colors.GREEN)
        except Exception as e:
            log(f"❌ Failed to copy {script}: {e}", Colors.RED)
            return False

    log("✅ Automation scripts set up successfully", Colors.GREEN)
    return True


def update_precommit_config():
    """Update or create pre-commit configuration."""
    log("⚙️  Updating pre-commit configuration...", Colors.BLUE)

    precommit_config = Path(".pre-commit-config.yaml")
    current_dir = Path(__file__).parent
    template_config = current_dir / "pysherlock_precommit_config.yaml"

    if not template_config.exists():
        log("❌ Template pre-commit config not found", Colors.RED)
        return False

    # Backup existing config if it exists
    if precommit_config.exists():
        backup_path = Path(".pre-commit-config.yaml.backup")
        shutil.copy2(precommit_config, backup_path)
        log(f"✅ Backed up existing config to {backup_path}", Colors.YELLOW)

    # Read template and update paths
    try:
        with open(template_config, "r") as f:
            config_content = f.read()

        # Update the entry path to use the automation directory
        config_content = config_content.replace(
            "entry: python pre_push_version_increment.py",
            "entry: python .pysherlock-automation/pre_push_version_increment.py",
        )

        with open(precommit_config, "w") as f:
            f.write(config_content)

        log("✅ Pre-commit configuration updated", Colors.GREEN)
        return True

    except Exception as e:
        log(f"❌ Failed to update pre-commit config: {e}", Colors.RED)
        return False


def install_precommit_hooks():
    """Install pre-commit hooks."""
    log("🪝 Installing pre-commit hooks...", Colors.BLUE)

    # Install pre-commit hooks
    success, output = run_command(["pre-commit", "install"])
    if not success:
        log(f"❌ Failed to install pre-commit hooks: {output}", Colors.RED)
        return False

    # Install pre-push hooks specifically
    success, output = run_command(["pre-commit", "install", "--hook-type", "pre-push"])
    if not success:
        log(f"❌ Failed to install pre-push hooks: {output}", Colors.RED)
        return False

    log("✅ Pre-commit hooks installed successfully", Colors.GREEN)
    return True


def test_setup():
    """Test the setup by running a dry-run."""
    log("🧪 Testing setup...", Colors.BLUE)

    # Test the auto increment script
    script_path = Path(".pysherlock-automation/auto_version_increment.py")
    if not script_path.exists():
        log("❌ Auto increment script not found", Colors.RED)
        return False

    # Run with --help to test if it works
    success, output = run_command([sys.executable, str(script_path), "--help"], check=False)

    if success or "usage:" in output.lower() or "automatic version" in output.lower():
        log("✅ Auto increment script is working", Colors.GREEN)
    else:
        log("⚠️  Auto increment script test inconclusive", Colors.YELLOW)

    # Test pre-commit
    success, output = run_command(["pre-commit", "--version"])
    if not success:
        log("❌ Pre-commit test failed", Colors.RED)
        return False

    log("✅ Setup test completed", Colors.GREEN)
    return True


def create_usage_instructions():
    """Create usage instructions file."""
    log("📚 Creating usage instructions...", Colors.BLUE)

    instructions = """# PySherlock Automatic Version Increment

This automation has been set up to automatically increment the version in `pyproject.toml`
when you push changes to the repository.

## How it works

1. **Pre-push Hook**: When you run `git push`, the pre-push hook automatically analyzes your changes
2. **Smart Analysis**: The system looks at:
   - Towncrier changelog fragments in `doc/changelog.d/`
   - Git commit messages
   - Code changes in the repository
3. **Version Bump**: Based on the analysis, it determines whether to do a:
   - **PATCH** bump (x.y.Z) - for bug fixes, docs, small changes
   - **MINOR** bump (x.Y.0) - for new features, enhancements
   - **MAJOR** bump (X.0.0) - for breaking changes, API changes
4. **Automatic Update**: Updates `pyproject.toml` and commits the change

## Usage

### Normal Development Flow
```bash
# Make your changes
git add .
git commit -m "fix: resolve issue with connection timeout"

# Push your changes - version will be auto-incremented
git push origin your-branch
```

### Manual Version Control
If you want to manually control the version increment, you can run:

```bash
# Run manually with confirmation prompt
python .pysherlock-automation/auto_version_increment.py

# Run without confirmation (automated)
python .pysherlock-automation/auto_version_increment.py --no-confirm
```

### Changelog Integration
The system works best with towncrier changelog fragments:

```bash
# Create changelog fragment for a bug fix
echo "Fixed connection timeout issue." > doc/changelog.d/123.fixed.md

# Create changelog fragment for a new feature
echo "Added new authentication method." > doc/changelog.d/124.added.md

# Commit and push - version will be incremented appropriately
git add . && git commit -m "fix: connection timeout" && git push
```

## Configuration

### Version Bump Rules
- **MAJOR** (breaking changes):
  - Breaking changes in commit messages
  - API changes that remove/modify existing functions
  - Changelog fragments indicating breaking changes

- **MINOR** (new features):
  - New features in commit messages (`feat:`, `feature:`, `add:`)
  - New functions/classes added to API
  - Changelog fragments with new features

- **PATCH** (bug fixes):
  - Bug fixes, documentation updates, small improvements
  - Default for changes that don't match MAJOR/MINOR criteria

### Skipping Auto-increment
The system automatically skips version increment when:
- You're on the main branch
- No changes detected since main branch
- Version was already manually updated in the PR

### Troubleshooting

If the auto-increment fails:
1. Check that all dependencies are installed: `pip install toml pre-commit`
2. Ensure you're in the PySherlock repository root
3. Check that `pyproject.toml` exists and is readable
4. Run manually to see detailed error messages

### Disabling
To temporarily disable auto-increment:
```bash
# Skip pre-push hooks for one push
git push --no-verify

# Or remove the hook temporarily
pre-commit uninstall --hook-type pre-push
```

To re-enable:
```bash
pre-commit install --hook-type pre-push
```

## Files Created
- `.pysherlock-automation/` - Contains automation scripts
- `.pre-commit-config.yaml` - Updated with version increment hook
- `PYSHERLOCK_VERSION_AUTOMATION.md` - This documentation

## Support
If you encounter issues with the version automation, check:
1. The automation scripts in `.pysherlock-automation/`
2. Pre-commit hook configuration in `.pre-commit-config.yaml`
3. Run the automation manually for debugging
"""

    try:
        with open("PYSHERLOCK_VERSION_AUTOMATION.md", "w") as f:
            f.write(instructions)
        log("✅ Usage instructions created: PYSHERLOCK_VERSION_AUTOMATION.md", Colors.GREEN)
        return True
    except Exception as e:
        log(f"❌ Failed to create instructions: {e}", Colors.RED)
        return False


def main():
    """Main setup function."""
    log("🚀 PySherlock Automatic Version Increment Setup", Colors.BOLD)
    log("=" * 50, Colors.BOLD)

    # Check prerequisites
    if not check_prerequisites():
        return 1

    # Install dependencies
    if not install_dependencies():
        return 1

    # Setup automation scripts
    if not setup_automation_scripts():
        return 1

    # Update pre-commit configuration
    if not update_precommit_config():
        return 1

    # Install pre-commit hooks
    if not install_precommit_hooks():
        return 1

    # Test setup
    if not test_setup():
        log("⚠️  Setup completed but tests failed. Please check manually.", Colors.YELLOW)

    # Create usage instructions
    create_usage_instructions()

    log("\n" + "=" * 50, Colors.BOLD)
    log("🎉 Setup completed successfully!", Colors.GREEN)
    log("\nNext steps:", Colors.BOLD)
    log("1. Review PYSHERLOCK_VERSION_AUTOMATION.md for usage instructions", Colors.BLUE)
    log("2. Test the setup by making a small change and pushing", Colors.BLUE)
    log("3. The version will be automatically incremented on git push", Colors.BLUE)
    log("\nHappy coding! 🐍✨", Colors.GREEN)

    return 0


if __name__ == "__main__":
    sys.exit(main())
