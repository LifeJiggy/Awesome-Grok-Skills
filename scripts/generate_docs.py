#!/usr/bin/env python3
"""
Documentation Generator - Generate documentation for skills and agents.

Usage:
    python scripts/generate_docs.py [--skills] [--agents] [--all]
"""

import argparse
import re
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


def get_agent_description(agent_file: Path) -> str:
    """Extract agent description from agent.py"""
    content = agent_file.read_text()
    
    docstring = re.search(r'"""(.+?)"""', content, re.DOTALL)
    if docstring:
        desc = docstring.group(1).strip().split('\n')[0]
        return desc
    
    return "Agent for managing and automating tasks."


def get_agent_class_name(agent_file: Path) -> str:
    """Extract main agent class name from agent.py"""
    content = agent_file.read_text()
    
    match = re.search(r'class\s+(\w+Agent)\s*[:(]', content)
    if match:
        return match.group(1)
    
    return "Agent"


def generate_readme(agent_name: str, agent_file: Path) -> str:
    """Generate README.md content"""
    description = get_agent_description(agent_file)
    class_name = get_agent_class_name(agent_file)
    
    return f'''# {agent_name.replace('-', ' ').title().replace(' ', '')} Agent

{description}

## Quick Start

```python
from agents.{agent_name}.agent import {class_name}

agent = {class_name}()
result = agent.run()
print(result)
```

## Run the Agent

```bash
python agents/{agent_name}/agent.py
```

## Files

- `agent.py` - Main implementation
- `GROK.md` - Agent instructions
- `ARCHITECTURE.md` - System architecture
- `README.md` - This file
'''


def generate_architecture(agent_name: str) -> str:
    """Generate ARCHITECTURE.md content"""
    name = agent_name.replace('-', ' ').title().replace(' ', '')
    
    return f'''# {name} Agent Architecture

## Overview

This document describes the architecture for the {name} Agent.

## System Components

```
┌─────────────────────────────────────────┐
│         {name} Agent                    │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────┐  │
│  │ Component 1 │  │   Component 2   │  │
│  └─────────────┘  └─────────────────┘  │
│  ┌─────────────┐  ┌─────────────────┐  │
│  │ Component 3 │  │   Component 4  │  │
│  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────┘
```

## Data Flow

```
Input → Processing → Output
```

## Key Components

### 1. Core Processing

Description of core processing logic.

### 2. Configuration Management

How configuration is handled.

### 3. Integration Layer

How the agent integrates with external systems.

## Configuration

```yaml
config:
  option1: value1
  option2: value2
```

## Performance

| Metric | Value |
|--------|-------|
| Response Time | TBD |
| Throughput | TBD |

## Security Considerations

- Authentication requirements
- Authorization rules
- Data protection measures
'''


def generate_agent_docs(scope: str) -> int:
    """Generate README.md and ARCHITECTURE.md for agents."""
    agents_dir = Path(__file__).parent.parent / "agents"
    
    if scope not in ("agents", "all"):
        return 0
    
    print("Generating agent documentation...")
    
    for agent_dir in sorted(agents_dir.iterdir()):
        if not agent_dir.is_dir():
            continue
        
        agent_file = agent_dir / "agent.py"
        if not agent_file.exists():
            continue
        
        agent_name = agent_dir.name
        print(f"  - {agent_name}")
        
        readme_file = agent_dir / "README.md"
        readme_content = generate_readme(agent_name, agent_file)
        readme_file.write_text(readme_content)
        
        arch_file = agent_dir / "ARCHITECTURE.md"
        arch_content = generate_architecture(agent_name)
        arch_file.write_text(arch_content)
    
    return 0


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
        exit_code = generate_agent_docs(scope)
        if exit_code != 0:
            sys.exit(exit_code)
    
    print("\nGenerated README.md and ARCHITECTURE.md for all agents.")


if __name__ == "__main__":
    main()
