#!/usr/bin/env python3
"""
Sync README.md with actual repository structure.

This script updates the README with current skills and agents.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json


def get_skills_list(root: Path) -> list:
    """Get list of all skills."""
    skills_path = root / "skills"
    if not skills_path.exists():
        return []
    
    skills = []
    for skill_dir in sorted(skills_path.iterdir()):
        if skill_dir.is_dir():
            grok_file = skill_dir / "GROK.md"
            description = ""
            if grok_file.exists():
                content = grok_file.read_text()
                # Extract description from overview section
                if "## Overview" in content:
                    overview = content.split("## Overview")[1].split("##")[0].strip()
                    description = overview.split("\n")[0][:100]
            skills.append({
                "name": skill_dir.name.replace("-", " ").replace("_", " ").title(),
                "slug": skill_dir.name,
                "description": description or "Skill implementation"
            })
    return skills


def get_agents_list(root: Path) -> list:
    """Get list of all agents."""
    agents_path = root / "agents"
    if not agents_path.exists():
        return []
    
    agents = []
    for agent_dir in sorted(agents_path.iterdir()):
        if agent_dir.is_dir():
            grok_file = agent_dir / "GROK.md"
            description = ""
            if grok_file.exists():
                content = grok_file.read_text()
                if "## Overview" in content:
                    overview = content.split("## Overview")[1].split("##")[0].strip()
                    description = overview.split("\n")[0][:100]
            agents.append({
                "name": agent_dir.name.replace("-", " ").replace("_", " ").title(),
                "slug": agent_dir.name,
                "description": description or "Agent implementation"
            })
    return agents


def update_readme_stats(root: Path, readme_path: Path) -> None:
    """Update README with current statistics."""
    skills = get_skills_list(root)
    agents = get_agents_list(root)
    
    readme_content = readme_path.read_text()
    
    # Update skill count
    readme_content = readme_content.replace(
        "**Total Skill Domains** | 30+",
        f"**Total Skill Domains** | {len(skills)}"
    )
    readme_content = readme_content.replace(
        "50+ Skills",
        f"{len(skills)}+ Skills"
    )
    
    # Update agent count
    readme_content = readme_content.replace(
        "**Total Specialized Agents** | 25+",
        f"**Total Specialized Agents** | {len(agents)}"
    )
    readme_content = readme_content.replace(
        "50+ Agents",
        f"{len(agents)}+ Agents"
    )
    
    # Update date
    date = datetime.now().strftime("%B %d, %Y")
    readme_content = readme_content.replace(
        "Last Updated: January 2025",
        f"Last Updated: {date}"
    )
    
    readme_path.write_text(readme_content)
    print(f"✅ Updated README with {len(skills)} skills and {len(agents)} agents")


def generate_skills_table(skills: list) -> str:
    """Generate markdown table for skills."""
    table = "| Skill | Description | Status |\n"
    table += "|-------|-------------|--------|\n"
    
    for skill in skills:
        name = skill["name"]
        slug = skill["slug"]
        desc = skill["description"]
        table += f"| **[{name}](skills/{slug}/)** | {desc} | ✅ Complete |\n"
    
    return table


def generate_agents_table(agents: list) -> str:
    """Generate markdown table for agents."""
    table = "| Agent | Description | Status |\n"
    table += "|-------|-------------|--------|\n"
    
    for agent in agents:
        name = agent["name"]
        slug = agent["slug"]
        desc = agent["description"]
        table += f"| **[{name}](agents/{slug}/)** | {desc} | ✅ Active |\n"
    
    return table


def main():
    """Main function."""
    root = Path(__file__).parent.parent.resolve()
    readme_path = root / "README.md"
    
    if not readme_path.exists():
        print_error("README.md not found")
        return 1
    
    print("🔄 Syncing README with repository structure...\n")
    
    # Get counts
    skills = get_skills_list(root)
    agents = get_agents_list(root)
    
    print(f"📚 Found {len(skills)} skills")
    print(f"🤖 Found {len(agents)} agents")
    
    # Update README
    update_readme_stats(root, readme_path)
    
    # Generate reports
    report = {
        "skills_count": len(skills),
        "agents_count": len(agents),
        "skills": skills,
        "agents": agents,
        "updated": datetime.now().isoformat()
    }
    
    report_path = root / "repository_stats.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"📊 Statistics saved to: {report_path}")
    
    print("\n✅ README sync complete!")
    return 0


def print_error(text: str) -> None:
    print(f"❌ {text}")


if __name__ == "__main__":
    sys.exit(main())
