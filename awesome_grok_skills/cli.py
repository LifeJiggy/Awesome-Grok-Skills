#!/usr/bin/env python3
"""CLI entry point for Awesome Grok Skills."""

import argparse
import importlib.util
import sys
from pathlib import Path


def list_agents():
    """List all available agents."""
    agents_dir = Path(__file__).parent.parent / "agents"
    agents = []
    for agent_dir in agents_dir.iterdir():
        if agent_dir.is_dir():
            agent_file = agent_dir / "agent.py"
            if agent_file.exists():
                agents.append(agent_dir.name)
    return sorted(agents)


def list_skills():
    """List all available skills."""
    skills_dir = Path(__file__).parent.parent / "skills"
    skills = []
    for skill_dir in skills_dir.rglob("resources/*.py"):
        if "__pycache__" not in str(skill_dir):
            skills.append(str(skill_dir.parent.relative_to(skills_dir)))
    return sorted(set(skills))


def run_agent(agent_name: str, args: argparse.Namespace):
    """Run a specific agent."""
    agent_path = Path(__file__).parent.parent / "agents" / agent_name / "agent.py"
    if not agent_path.exists():
        print(f"Error: Agent '{agent_name}' not found")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("agent_module", agent_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["agent_module"] = module
    spec.loader.exec_module(module)

    if hasattr(module, 'main'):
        module.main()
    else:
        print(f"No main() function found in agent {agent_name}")
        print("Available in module:", [x for x in dir(module) if not x.startswith('_')])


def run_skill(skill_name: str, args: argparse.Namespace):
    """Run a specific skill."""
    skill_path = Path(__file__).parent.parent / "skills" / skill_name / "resources" / f"{skill_name.replace('-', '_')}.py"
    if not skill_path.exists():
        skill_path = Path(__file__).parent.parent / "skills" / skill_name / "resources" / "resources.py"

    if not skill_path.exists():
        print(f"Error: Skill '{skill_name}' not found")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("skill_module", skill_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["skill_module"] = module
    spec.loader.exec_module(module)

    if hasattr(module, 'main'):
        module.main()
    else:
        print(f"No main() function found in skill {skill_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Awesome Grok Skills - AI Agent and Skill Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list-agents              List all available agents
  %(prog)s --list-skills              List all available skills
  %(prog)s --agent full-stack-planner Run the full-stack-planner agent
  %(prog)s --agent development        Run the development agent
  %(prog)s --skill ai-ml/neural-architecture-search  Run a skill
        """
    )

    parser.add_argument("--list-agents", action="store_true", help="List all available agents")
    parser.add_argument("--list-skills", action="store_true", help="List all available skills")
    parser.add_argument("--agent", type=str, help="Run a specific agent by name")
    parser.add_argument("--skill", type=str, help="Run a specific skill by name")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.list_agents:
        agents = list_agents()
        print(f"\n{'='*60}")
        print("  Available Agents")
        print(f"{'='*60}\n")
        for agent in agents:
            print(f"  - {agent}")
        print(f"\n  Total: {len(agents)} agents\n")
        return 0

    if args.list_skills:
        skills = list_skills()
        print(f"\n{'='*60}")
        print("  Available Skills")
        print(f"{'='*60}\n")
        for skill in skills:
            print(f"  - {skill}")
        print(f"\n  Total: {len(skills)} skills\n")
        return 0

    if args.agent:
        if args.verbose:
            print(f"Running agent: {args.agent}")
        run_agent(args.agent, args)
        return 0

    if args.skill:
        if args.verbose:
            print(f"Running skill: {args.skill}")
        run_skill(args.skill, args)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    main()
