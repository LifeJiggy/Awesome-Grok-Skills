#!/usr/bin/env python3
"""CLI entry point for Awesome Grok Skills.

Discovers and launches agents (``agents/<name>/agent.py``) and skills
(``skills/<category>/<skill-name>/<skill_name>.py``) from the project root.

The package is laid out as::

    <project_root>/
        agents/<agent-name>/agent.py            # each defines main()
        skills/<category>/<skill-name>/<skill_name_with_underscores>.py

Both agents and skills are loaded dynamically with ``importlib`` so the
repository can be extended without touching this file.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable, Iterable, List, Optional

# Project root is two levels up from this file (src/ -> <project_root>).
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = PROJECT_ROOT / "agents"
SKILLS_DIR = PROJECT_ROOT / "skills"


def _discover_dirs_with_file(parent: Path, target_filename: str) -> List[Path]:
    """Return sorted child directories of *parent* that contain *target_filename*.

    Silently returns an empty list if *parent* does not exist, so the CLI is
    usable even when only one of ``agents/`` / ``skills/`` is present.
    """
    if not parent.is_dir():
        return []
    found = []
    for child in parent.iterdir():
        if child.is_dir() and (child / target_filename).exists():
            found.append(child)
    return sorted(found)


def list_agents() -> List[str]:
    """List all available agent names (sorted)."""
    return [d.name for d in _discover_dirs_with_file(AGENTS_DIR, "agent.py")]


def _find_skill_script(skill_dir: Path) -> Optional[Path]:
    """Locate the runnable ``.py`` script inside a skill directory.

    A skill lives at ``skills/<category>/<skill-name>/`` and its runnable
    script is named after the skill with dashes replaced by underscores
    (e.g. ``skills/accessibility/aria-implementation/aria_implementation.py``).

    Falls back to ``resources.py`` for legacy layouts. Returns ``None`` if no
    candidate is found.
    """
    primary = skill_dir / f"{skill_dir.name.replace('-', '_')}.py"
    if primary.exists():
        return primary
    legacy = skill_dir / "resources" / "resources.py"
    if legacy.exists():
        return legacy
    return None


def list_skills() -> List[str]:
    """List all available skills as ``<category>/<skill-name>`` (sorted, unique)."""
    if not SKILLS_DIR.is_dir():
        return []
    skills: List[str] = []
    for category_dir in sorted(SKILLS_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        for skill_dir in sorted(category_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            if _find_skill_script(skill_dir) is not None:
                skills.append(f"{category_dir.name}/{skill_dir.name}")
    # Deduplicate defensively (category/skill pairs are unique already).
    return sorted(set(skills))


def _load_module(module_path: Path, module_name: str) -> ModuleType:
    """Dynamically import *module_path* under a unique *module_name*.

    Uses a unique name per call so repeated invocations do not overwrite each
    other in ``sys.modules`` (the previous implementation reused the same key
    for every agent/skill, causing stale modules to leak across calls).
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - extremely rare
        raise ImportError(f"Could not build import spec for {module_path}")
    module = importlib.util.module_from_spec(spec)
    # Register before exec so the module can import itself by name if needed.
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        # Don't leave a half-loaded module in sys.modules on failure.
        sys.modules.pop(module_name, None)
        raise
    return module


def _run_entry(name: str, module_path: Path, kind: str, verbose: bool) -> int:
    """Load *module_path* and invoke its ``main()`` if present.

    Returns a process exit code. Emits a helpful error if the file is missing
    or has no ``main()``.
    """
    if not module_path.exists():
        print(f"Error: {kind.capitalize()} '{name}' not found at {module_path}", file=sys.stderr)
        return 1

    if verbose:
        print(f"Running {kind}: {name}")
        print(f"  path: {module_path}")

    module_name = f"awesome_grok_skills_{kind}_{name.replace('-', '_').replace('/', '_')}"
    try:
        module = _load_module(module_path, module_name)
    except Exception as exc:  # noqa: BLE001 - surface any load failure to the user
        print(f"Error: failed to load {kind} '{name}': {exc}", file=sys.stderr)
        return 1

    main_fn: Optional[Callable[..., object]] = getattr(module, "main", None)
    if main_fn is None or not callable(main_fn):
        print(f"No main() function found in {kind} {name}", file=sys.stderr)
        public = [x for x in dir(module) if not x.startswith("_")]
        print(f"Available in module: {public}", file=sys.stderr)
        return 1

    try:
        result = main_fn()
    except SystemExit as exc:
        # Honour explicit sys.exit() calls inside the entry's main().
        return int(exc.code) if exc.code is not None else 0
    # main() may return None, an int, or anything coercible to int-ish.
    if isinstance(result, int):
        return result
    return 0


def run_agent(agent_name: str, verbose: bool = False) -> int:
    """Run a specific agent by name. Returns a process exit code."""
    agent_path = AGENTS_DIR / agent_name / "agent.py"
    return _run_entry(agent_name, agent_path, "agent", verbose)


def run_skill(skill_name: str, verbose: bool = False) -> int:
    """Run a specific skill by ``<category>/<skill-name>``. Returns a process exit code."""
    if "/" not in skill_name:
        print(
            f"Error: skill '{skill_name}' must be specified as '<category>/<skill-name>'.\n"
            f"Use --list-skills to see available skills.",
            file=sys.stderr,
        )
        return 1

    category, _, name = skill_name.partition("/")
    skill_dir = SKILLS_DIR / category / name
    skill_path = _find_skill_script(skill_dir)
    if skill_path is None:
        print(f"Error: Skill '{skill_name}' not found under {skill_dir}", file=sys.stderr)
        return 1
    return _run_entry(skill_name, skill_path, "skill", verbose)


def _print_list(title: str, items: Iterable[str]) -> int:
    """Print a bordered list of *items* and a total count. Returns 0."""
    items = list(items)
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")
    for item in items:
        print(f"  - {item}")
    label = title.rsplit(" ", 1)[-1].lower()
    print(f"\n  Total: {len(items)} {label}\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser (exposed for tests/scripting reuse)."""
    parser = argparse.ArgumentParser(
        description="Awesome Grok Skills - AI Agent and Skill Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s --list-agents              List all available agents
  %(prog)s --list-skills              List all available skills
  %(prog)s --agent full-stack-planner Run the full-stack-planner agent
  %(prog)s --agent development        Run the development agent
  %(prog)s --skill ai-ml/neural-architecture-search  Run a skill
""",
    )
    parser.add_argument("--list-agents", action="store_true", help="List all available agents")
    parser.add_argument("--list-skills", action="store_true", help="List all available skills")
    parser.add_argument("--agent", type=str, help="Run a specific agent by name")
    parser.add_argument("--skill", type=str, help="Run a specific skill by name (<category>/<skill-name>)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point. Parses *argv* (or ``sys.argv``) and dispatches.

    Returns a process exit code suitable for ``sys.exit(main())``.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_agents:
        return _print_list("Available Agents", list_agents())

    if args.list_skills:
        return _print_list("Available Skills", list_skills())

    if args.agent:
        return run_agent(args.agent, verbose=args.verbose)

    if args.skill:
        return run_skill(args.skill, verbose=args.verbose)

    # No action requested: show help and exit non-zero so scripts can detect a no-op.
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
