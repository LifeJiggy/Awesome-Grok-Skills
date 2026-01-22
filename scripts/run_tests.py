#!/usr/bin/env python3
"""
Test Runner Script - Run comprehensive tests for Awesome Grok Skills.

Usage:
    python scripts/run_tests.py [--unit] [--integration] [--e2e] [--coverage]
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_tests(test_type: str, coverage: bool = False) -> int:
    """Run tests based on type."""
    project_root = Path(__file__).parent.parent
    
    if test_type == "all":
        cmd = ["pytest", str(project_root / "tests"), "-v"]
    else:
        cmd = ["pytest", str(project_root / "tests" / test_type), "-v"]
    
    if coverage:
        cmd.extend(["--cov", ".", "--cov-report", "term-missing"])
    
    print(f"Running {test_type} tests...")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--e2e", action="store_true", help="Run e2e tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    test_types = []
    if args.unit:
        test_types.append("unit")
    if args.integration:
        test_types.append("integration")
    if args.e2e:
        test_types.append("e2e")
    if args.all or not test_types:
        test_types = ["unit", "integration", "e2e"]
    
    for test_type in test_types:
        exit_code = run_tests(test_type, args.coverage)
        if exit_code != 0:
            sys.exit(exit_code)
    
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    main()
