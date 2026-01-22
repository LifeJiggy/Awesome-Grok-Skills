#!/usr/bin/env python3
"""
Generate a new skill for Awesome Grok Skills.

Usage:
    python scripts/generate_skill.py skill-name [--path PATH] [--force]
"""

import argparse
import os
import sys
from pathlib import Path
from string import Template
from datetime import datetime


def print_success(text: str) -> None:
    """Print a success message."""
    print(f"✅ {text}")


def print_warning(text: str) -> None:
    """Print a warning message."""
    print(f"⚠️  {text}")


def print_error(text: str) -> None:
    """Print an error message."""
    print(f"❌ {text}")


def get_template_path() -> Path:
    """Get the templates directory."""
    return Path(__file__).parent.parent / "templates"


def get_skill_template() -> str:
    """Get the skill GROK.md template."""
    return """# $name

## Overview

Brief description of this skill domain and what problems it solves.

## Capabilities

- **Capability 1**: Description of first capability
- **Capability 2**: Description of second capability
- **Capability 3**: Description of third capability

## Technologies

- Technology 1
- Technology 2
- Technology 3

## Installation

```bash
grok --skill $slug --install
```

## Usage

### Basic Example

```python
from skills.$slug.resources.$module import ${class_name}Engine

engine = ${class_name}Engine()
result = engine.process(data)
print(result)
```

### Advanced Usage

```python
from skills.$slug.resources.$module import ${class_name}Engine, Config

config = Config(
    enabled=True,
    timeout=30,
    retry_count=3
)

engine = ${class_name}Engine(config=config)
results = engine.batch_process(large_dataset)
```

## API Reference

### ${class_name}Engine

The main engine class for this skill.

#### `__init__(config: Optional[Config] = None)`

Initialize the engine with optional configuration.

**Parameters:**
- `config`: Optional configuration object

#### `process(data: Any) -> Any`

Process input data.

**Parameters:**
- `data`: Input data to process

**Returns:** Processed result

#### `batch_process(datasets: List[Any]) -> List[Any]`

Process multiple datasets.

**Parameters:**
- `datasets`: List of datasets to process

**Returns:** List of processed results

### Config

Configuration dataclass for the engine.

**Fields:**
- `enabled`: Enable/disable the engine (default: True)
- `timeout`: Request timeout in seconds (default: 30)
- `retry_count`: Number of retries on failure (default: 3)

## Examples

### Example 1: Data Processing

```python
from skills.$slug.resources.$module import ${class_name}Engine

engine = ${class_name}Engine()
data = {"input": "value"}
result = engine.process(data)
```

### Example 2: Batch Processing

```python
from skills.$slug.resources.$module import ${class_name}Engine

engine = ${class_name}Engine()
datasets = [
    {"data": 1},
    {"data": 2},
    {"data": 3}
]
results = engine.batch_process(datasets)
```

## Integration

This skill can be combined with:

- **Agent Name**: For automated workflows
- **Other Skill**: For chained processing

## Performance

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Single process | O(n) | O(n) |
| Batch process | O(n*m) | O(n*m) |

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details.

---

Generated on: $date
"""


def get_python_template() -> str:
    """Get the Python implementation template."""
    return '''"""$name Skill Implementation."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
import json


class $class_nameType(Enum):
    """Types for $name."""
    TYPE_A = "type_a"
    TYPE_B = "type_b"
    TYPE_C = "type_c"


@dataclass
class Config:
    """Configuration for $name engine."""
    enabled: bool = True
    timeout: int = 30
    retry_count: int = 3
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class $class_nameData:
    """Data model for $name."""
    id: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ${class_name}Engine:
    """Engine for $name processing and analysis.
    
    This engine provides functionality for processing $name data
    with high performance and accuracy.
    """
    
    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize the $name engine.
        
        Args:
            config: Optional configuration object
        """
        self._config = config or Config()
        self._initialized = False
        self._processed_count = 0
    
    def _initialize(self) -> None:
        """Private initialization method."""
        if not self._initialized:
            self._initialized = True
            # Initialize resources here
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed results dictionary
        """
        self._initialize()
        
        # Validate input
        if not data:
            raise ValueError("Input data cannot be empty")
        
        # Process data
        result = {
            "input": data,
            "processed_at": datetime.now().isoformat(),
            "status": "success"
        }
        
        self._processed_count += 1
        return result
    
    def batch_process(self, datasets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple datasets.
        
        Args:
            datasets: List of datasets to process
            
        Returns:
            List of processed results
        """
        self._initialize()
        results = []
        
        for dataset in datasets:
            try:
                result = self.process(dataset)
                results.append(result)
            except Exception as e:
                results.append({
                    "error": str(e),
                    "dataset": dataset,
                    "status": "failed"
                })
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            "total_processed": self._processed_count,
            "is_initialized": self._initialized,
            "config": {
                "enabled": self._config.enabled,
                "timeout": self._config.timeout
            }
        }
    
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate input data.
        
        Args:
            data: Data to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(data, dict):
            return False
        
        required_fields = ["id", "value"]
        return all(field in data for field in required_fields)
    
    def cleanup(self) -> None:
        """Clean up resources."""
        self._initialized = False


class ${class_name}Agent:
    """Agent for $name automation and orchestration."""
    
    def __init__(self, engine: Optional[${class_name}Engine] = None) -> None:
        """Initialize the agent.
        
        Args:
            engine: Optional engine instance
        """
        self.engine = engine or ${class_name}Engine()
    
    def execute_task(self, task: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using the engine.
        
        Args:
            task: Task to execute
            data: Task data
            
        Returns:
            Task result
        """
        if task == "process":
            return self.engine.process(data)
        elif task == "batch":
            return self.engine.batch_process(data.get("datasets", []))
        else:
            raise ValueError(f"Unknown task: {task}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status.
        
        Returns:
            Status dictionary
        """
        return {
            "agent": "${class_name}Agent",
            "status": "ready",
            "engine_status": self.engine.get_statistics()
        }


def main():
    """Main function demonstrating usage."""
    print(f"$name Skill Demo")
    print("=" * 40)
    
    # Create engine
    config = Config(enabled=True, timeout=60)
    engine = ${class_name}Engine(config=config)
    
    # Process single item
    data = {
        "id": "test-001",
        "value": 42.5,
        "metadata": {"source": "demo"}
    }
    
    print(f"Processing: {data}")
    result = engine.process(data)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Batch processing
    datasets = [
        {"id": "001", "value": 10.0},
        {"id": "002", "value": 20.0},
        {"id": "003", "value": 30.0}
    ]
    
    print("\\nBatch Processing:")
    batch_results = engine.batch_process(datasets)
    print(f"Processed {len(batch_results)} items")
    
    # Statistics
    print("\\nStatistics:")
    print(json.dumps(engine.get_statistics(), indent=2))


if __name__ == "__main__":
    main()
'''


def generate_skill_name(slug: str) -> tuple:
    """Generate skill name components from slug."""
    # Convert slug to PascalCase
    parts = slug.replace("-", " ").replace("_", " ").title().split()
    name = " ".join(parts)
    class_name = "".join(parts)
    module = slug.replace("-", "_")
    return name, class_name, module, slug


def create_skill_directory(slug: str, path: Path) -> Path:
    """Create the skill directory structure."""
    skill_path = path / "skills" / slug
    resources_path = skill_path / "resources"
    
    skill_path.mkdir(parents=True, exist_ok=True)
    resources_path.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    init_file = resources_path / "__init__.py"
    init_file.write_text(f'"""$slug skill resources."""\n')
    
    return skill_path


def write_skill_files(skill_path: Path, name: str, class_name: str, module: str, slug: str) -> None:
    """Write the skill GROK.md and Python files."""
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Write GROK.md
    grok_template = Template(get_skill_template())
    grok_content = grok_template.substitute(
        name=name,
        class_name=class_name,
        module=module,
        slug=slug,
        date=date
    )
    
    grok_file = skill_path / "GROK.md"
    grok_file.write_text(grok_content)
    print(f"  Created: {grok_file}")
    
    # Write Python implementation
    python_template = Template(get_python_template())
    python_content = python_template.substitute(
        name=name,
        class_name=class_name,
        module=module
    )
    
    python_file = skill_path / "resources" / f"{module}.py"
    python_file.write_text(python_content)
    print(f"  Created: {python_file}")


def update_readme(slug: str, name: str) -> None:
    """Update README.md with new skill."""
    readme_path = Path(__file__).parent.parent / "README.md"
    
    if not readme_path.exists():
        print_warning("README.md not found, skipping update")
        return
    
    # Read existing README
    content = readme_path.read_text()
    
    # Find the skills table and add new entry
    skill_entry = f"| **[{name}](skills/{slug}/)** | Description | ✅ NEW |\n"
    
    # Insert before the last "---" section
    if "### 🌐 Web & Mobile Development" in content:
        # Add to appropriate section based on slug
        sections = {
            "ai": ("### 🧠 AI & Machine Learning", 1),
            "data": ("### 🌍 Data Science & Analytics", 1),
            "blockchain": ("### ⛓️ Blockchain & Web3", 1),
            "cloud": ("### ☁️ Cloud & Infrastructure", 1),
            "security": ("### 🔐 Security & Compliance", 1),
            "quantum": ("### 🚀 Advanced Technologies", 1),
            "health": ("### 🏥 Healthcare & Life Sciences", 1),
            "finance": ("### 🏦 Finance & Business", 1),
            "education": ("### 📚 Education & HR", 1),
            "creative": ("### 🎨 Creative & Media", 1),
            "gov": ("### 🏛️ Governance & Public Sector", 1),
            "urban": ("### 🏙️ Urban & Environmental", 1),
            "entertainment": ("### 🎭 Entertainment & Sports", 1),
            "web": ("### 🌐 Web & Mobile Development", 0),
        }
        
        for key, (section, offset) in sections.items():
            if key in slug.lower():
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if section in line:
                        insert_idx = i + offset
                        lines.insert(insert_idx, skill_entry)
                        content = "\n".join(lines)
                        break
                break
    
    readme_path.write_text(content)
    print_success("Updated README.md")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate a new skill for Awesome Grok Skills")
    parser.add_argument("name", help="Skill name (e.g., quantum-computing)")
    parser.add_argument("--path", default=".", help="Base path for the project")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--no-readme", action="store_true", help="Skip README update")
    
    args = parser.parse_args()
    
    # Get paths
    base_path = Path(args.path).resolve()
    print(f"\n📁 Project path: {base_path}")
    
    # Generate name components
    name, class_name, module, slug = generate_skill_name(args.name)
    print(f"📝 Skill: {name} (class: {class_name}, module: {module})")
    
    # Create directory
    skill_path = create_skill_directory(slug, base_path)
    
    # Check if already exists
    if (skill_path / "GROK.md").exists() and not args.force:
        print_error(f"Skill '{slug}' already exists. Use --force to overwrite.")
        return 1
    
    # Write files
    write_skill_files(skill_path, name, class_name, module, slug)
    
    # Update README
    if not args.no_readme:
        update_readme(slug, name)
    
    print(f"\n✅ Skill '{name}' created successfully!")
    print(f"   Location: {skill_path}")
    print(f"\n📝 Next steps:")
    print(f"   1. Edit {skill_path / 'GROK.md'} to add detailed documentation")
    print(f"   2. Implement functionality in {skill_path / 'resources' / f'{module}.py'}")
    print(f"   3. Add tests in tests/unit/test_skills/")
    print(f"   4. Run: python -m pytest tests/ -v")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
