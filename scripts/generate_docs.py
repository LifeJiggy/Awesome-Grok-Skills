#!/usr/bin/env python3
"""
Documentation Generator - Generate documentation for skills and agents.

Usage:
    python scripts/generate_docs.py [--skills] [--agents] [--all]
"""

import argparse
import subprocess
import sys
from pathlib import Path


def generate_docs(scope: str) -> int:
    """Generate documentation."""
    project_root = Path(__file__).parent.parent
    
    if scope == "all":
        cmd = ["pdoc", "-o", str(project_root / "docs" / "api"),
               str(project_root / "skills"), str(project_root / "agents")]
    elif scope == "skills":
        cmd = ["pdoc", "-o", str(project_root / "docs" / "api" / "skills"),
               str(project_root / "skills")]
    elif scope == "agents":
        cmd = ["pdoc", "-o", str(project_root / "docs" / "api" / "agents"),
               str(project_root / "agents")]
    
    print(f"Generating {scope} documentation...")
    return subprocess.run(cmd).returncode


def main():
    parser = argparse.ArgumentParser(description="Generate documentation")
    parser.add_argument("--skills", action="store_true", help="Generate skill docs")
    parser.add_argument("--agents", action="store_true", help="Generate agent docs")
    parser.add_argument("--all", action="store_true", help="Generate all docs")
    
    args = parser.parse_args()
    
    scopes = []
    if args.skills:
        scopes.append("skills")
    if args.agents:
        scopes.append("agents")
    if args.all or not scopes:
        scopes.append("all")
    
    for scope in scopes:
        exit_code = generate_docs(scope)
        if exit_code != 0:
            sys.exit(exit_code)
    
    print("\n✅ Documentation generated!")


if __name__ == "__main__":
    main()
