#!/usr/bin/env python3
"""
Benchmark Script - Run performance benchmarks.

Usage:
    python scripts/benchmark.py [--skills] [--agents] [--all]
"""

import argparse
import time
import sys
from pathlib import Path
from typing import Callable, Any


def benchmark_function(func: Callable, *args, **kwargs) -> tuple:
    """Run a function and measure time."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed


def benchmark_skill_import(skill: str) -> float:
    """Benchmark skill import time."""
    start = time.perf_counter()
    try:
        __import__(f"skills.{skill}.resources.{skill.replace('-', '_')}")
    except ImportError:
        pass
    return time.perf_counter() - start


def benchmark_agent_import(agent: str) -> float:
    """Benchmark agent import time."""
    start = time.perf_counter()
    try:
        __import__(f"agents.{agent}.agent")
    except ImportError:
        pass
    return time.perf_counter() - start


def run_benchmarks(scope: str) -> None:
    """Run benchmarks."""
    project_root = Path(__file__).parent.parent
    
    if scope in ("all", "skills"):
        skills_path = project_root / "skills"
        skills = [s.name for s in skills_path.iterdir() if s.is_dir()]
        print(f"\n📊 Benchmarking {len(skills)} skills...")
        total = 0
        for skill in skills[:10]:  # Sample first 10
            t = benchmark_skill_import(skill)
            total += t
            print(f"  {skill}: {t*1000:.2f}ms")
        print(f"  Average: {total/10*1000:.2f}ms")
    
    if scope in ("all", "agents"):
        agents_path = project_root / "agents"
        agents = [a.name for a in agents_path.iterdir() if a.is_dir()]
        print(f"\n📊 Benchmarking {len(agents)} agents...")
        total = 0
        for agent in agents[:10]:  # Sample first 10
            t = benchmark_agent_import(agent)
            total += t
            print(f"  {agent}: {t*1000:.2f}ms")
        print(f"  Average: {total/10*1000:.2f}ms")


def main():
    parser = argparse.ArgumentParser(description="Run benchmarks")
    parser.add_argument("--skills", action="store_true", help="Benchmark skills")
    parser.add_argument("--agents", action="store_true", help="Benchmark agents")
    parser.add_argument("--all", action="store_true", help="Benchmark all")
    
    args = parser.parse_args()
    
    scopes = []
    if args.skills:
        scopes.append("skills")
    if args.agents:
        scopes.append("agents")
    if args.all or not scopes:
        scopes.append("all")
    
    for scope in scopes:
        run_benchmarks(scope)
    
    print("\n✅ Benchmarks complete!")


if __name__ == "__main__":
    main()
