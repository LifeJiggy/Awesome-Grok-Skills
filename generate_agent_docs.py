#!/usr/bin/env python3
"""Generate README.md and ARCHITECTURE.md for all agents."""

from pathlib import Path
import re


def get_agent_description(agent_file):
    content = agent_file.read_text()
    docstring = re.search(r'"""(.+?)"""', content, re.DOTALL)
    if docstring:
        return docstring.group(1).strip().split('\n')[0]
    return 'Agent for managing and automating tasks.'


def get_agent_class_name(agent_file):
    content = agent_file.read_text()
    match = re.search(r'class\s+(\w+Agent)\s*[:(]', content)
    if match:
        return match.group(1)
    return 'Agent'


def generate_readme(agent_name, agent_file):
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


def generate_architecture(agent_name):
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
│  │ Component 3 │  │   Component 4   │  │
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


def main():
    agents_dir = Path('agents')
    for agent_dir in sorted(agents_dir.iterdir()):
        if not agent_dir.is_dir():
            continue
        agent_file = agent_dir / 'agent.py'
        if not agent_file.exists():
            continue
        agent_name = agent_dir.name
        print(f'Generating: {agent_name}')
        readme_content = generate_readme(agent_name, agent_file)
        (agent_dir / 'README.md').write_text(readme_content, encoding='utf-8')
        arch_content = generate_architecture(agent_name)
        (agent_dir / 'ARCHITECTURE.md').write_text(arch_content, encoding='utf-8')

    print('\nDone!')


if __name__ == '__main__':
    main()
