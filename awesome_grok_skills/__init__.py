#!/usr/bin/env python3
"""CLI entry point for Awesome Grok Skills."""

import sys
from pathlib import Path


def main():
    """Main CLI entry point."""
    print("Awesome Grok Skills CLI")
    print("Usage: grok --agent <agent-name> --help")
    print("Available agents: See agents/ directory")
    print("Available skills: See skills/ directory")
    sys.exit(0)


if __name__ == "__main__":
    main()
