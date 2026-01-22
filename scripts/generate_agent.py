#!/usr/bin/env python3
"""
Generate an agent for Awesome Grok Skills.

Usage:
    python scripts/generate_agent.py agent-name [--path PATH] [--force]
"""

import argparse
import os
import sys
from pathlib import Path
from string import Template
from datetime import datetime


def get_agent_template() -> str:
    """Get the agent Python template."""
    return '''"""$name Agent Implementation."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class $class_nameCapability(Enum):
    """Capabilities of the agent."""
    PROCESS = "process"
    ANALYZE = "analyze"
    GENERATE = "generate"
    VALIDATE = "validate"


@dataclass
class Config:
    """Configuration for $name agent."""
    api_key: str = ""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 60
    retry_count: int = 3
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResponse:
    """Response from the agent."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ${class_name}Agent:
    """$name Agent for automated task completion.
    
    This agent provides intelligent automation for $name tasks
    with high accuracy and efficiency.
    """
    
    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize the agent.
        
        Args:
            config: Optional configuration object
        """
        self._config = config or Config()
        self._history: List[Dict[str, Any]] = []
        self._task_count = 0
    
    def execute(self, task: str, data: Dict[str, Any]) -> AgentResponse:
        """Execute a task.
        
        Args:
            task: Task to execute
            data: Task data
            
        Returns:
            AgentResponse with result
        """
        self._task_count += 1
        
        try:
            if task == "process":
                result = self._process(data)
            elif task == "analyze":
                result = self._analyze(data)
            elif task == "generate":
                result = self._generate(data)
            elif task == "validate":
                result = self._validate(data)
            else:
                return AgentResponse(
                    success=False,
                    error=f"Unknown task: {task}"
                )
            
            self._history.append({
                "task": task,
                "data": data,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            
            return AgentResponse(
                success=True,
                data=result,
                metadata={"task": task, "timestamp": datetime.now().isoformat()}
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                error=str(e)
            )
    
    def _process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data."""
        return {"processed": data, "timestamp": datetime.now().isoformat()}
    
    def _analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data."""
        return {"analysis": "result", "input": data}
    
    def _generate(self, data: Dict[str, Any]) -> str:
        """Generate content."""
        return f"Generated content for: {data}"
    
    def _validate(self, data: Dict[str, Any]) -> bool:
        """Validate data."""
        return bool(data)
    
    def chat(self, message: str) -> str:
        """Chat with the agent.
        
        Args:
            message: User message
            
        Returns:
            Agent response
        """
        self._history.append({
            "type": "chat",
            "input": message,
            "timestamp": datetime.now().isoformat()
        })
        return f"Response to: {message}"
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status.
        
        Returns:
            Status dictionary
        """
        return {
            "agent": "${class_name}Agent",
            "status": "ready",
            "tasks_completed": self._task_count,
            "history_count": len(self._history),
            "config": {
                "model": self._config.model,
                "temperature": self._config.temperature
            }
        }
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get task history.
        
        Returns:
            List of past tasks
        """
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear task history."""
        self._history = []


def main():
    """Main function demonstrating usage."""
    print(f"$name Agent Demo")
    print("=" * 40)
    
    # Create agent
    config = Config(api_key="demo-key")
    agent = ${class_name}Agent(config=config)
    
    # Execute task
    print("Executing process task...")
    response = agent.execute("process", {"input": "value"})
    print(f"Response: {response.success} - {response.data}")
    
    # Chat
    print("\\nChat session:")
    response = agent.chat("Hello, agent!")
    print(f"Agent: {response}")
    
    # Status
    print("\\nAgent Status:")
    print(agent.get_status())


if __name__ == "__main__":
    main()
'''


def get_agent_grok_template() -> str:
    """Get the agent GROK.md template."""
    return '''# $name Agent

## Overview

Brief description of what this agent does.

## Capabilities

- **Task Processing**: Execute automated tasks
- **Analysis**: Analyze input data
- **Generation**: Generate content
- **Validation**: Validate data and results

## Usage

### Basic Example

```python
from agents.$slug.agent import ${class_name}Agent

agent = ${class_name}Agent()
result = agent.execute(task="process", data={"input": "value"})
print(result)
```

### Chat Example

```python
from agents.$slug.agent import ${class_name}Agent

agent = ${class_name}Agent()
response = agent.chat("Your message")
print(response)
```

## Configuration

```python
from agents.$slug.agent import ${class_name}Agent, Config

config = Config(
    api_key="your-key",
    model="gpt-4",
    temperature=0.7
)

agent = ${class_name}Agent(config=config)
```

## API Reference

### ${class_name}Agent

- `execute(task, data)`: Execute a task
- `chat(message)`: Chat with the agent
- `get_status()`: Get agent status
- `get_history()`: Get task history
- `clear_history()`: Clear task history

### Config

- `api_key`: API key
- `model`: Model name
- `temperature`: Response temperature
- `timeout`: Request timeout

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## License

MIT License

---

Generated on: $date
'''


def generate_agent_name(slug: str) -> tuple:
    """Generate agent name components from slug."""
    parts = slug.replace("-", " ").replace("_", " ").title().split()
    name = " ".join(parts)
    class_name = "".join(parts)
    module = slug.replace("-", "_")
    return name, class_name, module, slug


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate a new agent")
    parser.add_argument("name", help="Agent name (e.g., data-analyst)")
    parser.add_argument("--path", default=".", help="Base path")
    parser.add_argument("--force", action="store_true", help="Overwrite")
    
    args = parser.parse_args()
    
    base_path = Path(args.path).resolve()
    print(f"\n📁 Project path: {base_path}")
    
    name, class_name, module, slug = generate_agent_name(args.name)
    print(f"📝 Agent: {name} (class: {class_name})")
    
    agent_path = base_path / "agents" / slug
    agent_path.mkdir(parents=True, exist_ok=True)
    
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Write agent.py
    python_template = Template(get_agent_template())
    python_content = python_template.substitute(
        name=name,
        class_name=class_name,
        module=module,
        slug=slug
    )
    (agent_path / "agent.py").write_text(python_content)
    print(f"  Created: {agent_path / 'agent.py'}")
    
    # Write GROK.md
    grok_template = Template(get_agent_grok_template())
    grok_content = grok_template.substitute(
        name=name,
        class_name=class_name,
        slug=slug,
        date=date
    )
    (agent_path / "GROK.md").write_text(grok_content)
    print(f"  Created: {agent_path / 'GROK.md'}")
    
    print(f"\n✅ Agent '{name}' created successfully!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
