#!/usr/bin/env python3
"""
Linter Script - Run code linters and formatters.

Usage:
    python scripts/lint.py [--fix]
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_linter(linter: str, fix: bool = False) -> int:
    """Run a linter."""
    project_root = Path(__file__).parent.parent
    
    linters = {
        "ruff": ["ruff", "check", str(project_root)],
        "mypy": ["mypy", str(project_root / "skills"), str(project_root / "agents")],
        "black": ["black", "--check", str(project_root)],
    }
    
    if linter in linters:
        cmd = linters[linter]
        if fix and linter == "ruff":
            cmd.append("--fix")
        print(f"Running {linter}...")
        return subprocess.run(cmd).returncode
    return 0


def main():
    parser = argparse.ArgumentParser(description="Run linters")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues")
    parser.add_argument("--all", action="store_true", help="Run all linters")
    
    args = parser.parse_args()
    
    linters = ["ruff", "mypy", "black"] if args.all else ["ruff"]
    
    for linter in linters:
        exit_code = run_linter(linter, args.fix)
        if exit_code != 0:
            sys.exit(exit_code)
    
    print("\n✅ All linters passed!")


if __name__ == "__main__":
    main()
