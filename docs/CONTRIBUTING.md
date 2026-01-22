# Contributing to Awesome Grok Skills

Thank you for your interest in contributing! This guide will help you get started.

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Git
- A GitHub account

### Setting Up Your Development Environment

```bash
# Fork the repository
gh repo fork LifeJiggy/Awesome-Grok-Skills

# Clone your fork
git clone https://github.com/YOUR_USERNAME/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## 📝 Contribution Types

### 1. Adding a New Skill Domain

Skills are specialized knowledge domains. To add a new skill:

1. Create the directory structure:
   ```
   skills/[skill-name]/
   ├── GROK.md
   └── resources/
       └── [skillname].py
   ```

2. Follow the [skill template](templates/skill-template.md)

3. Ensure your Python code includes:
   - All necessary imports
   - Type hints
   - Docstrings
   - Example usage in `if __name__ == "__main__":`

4. Test your implementation:
   ```bash
   python -m pytest tests/ -v
   ```

5. Validate documentation:
   ```bash
   python scripts/validate-structure.py
   ```

### 2. Adding a New Agent

Agents are AI-powered entities that perform complex tasks. To add a new agent:

1. Create the directory structure:
   ```
   agents/[agent-name]/
   ├── GROK.md
   └── agent.py
   ```

2. Follow the [agent template](templates/agent-template.md)

3. Implement the agent class with clear capabilities

4. Add comprehensive docstrings

5. Test your agent:
   ```bash
   python -m pytest tests/ -k agent_name -v
   ```

### 3. Improving Existing Skills/Agents

We welcome improvements to existing skills and agents:

- Bug fixes
- Performance optimizations
- New features
- Documentation improvements
- Test additions

## 📐 Style Guide

### Python Code Style

We follow PEP 8 with some modifications:

```python
# Use type hints
def process_data(input_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process input data and return results.
    
    Args:
        input_data: List of dictionaries containing input data
        
    Returns:
        Dictionary containing processed results
    """
    # Your code here
    pass

# Use dataclasses for data models
@dataclass
class DataPoint:
    """A single data point for analysis."""
    id: str
    value: float
    timestamp: datetime

# Use dataclasses for configuration
@dataclass
class Config:
    """Configuration for the skill."""
    enabled: bool = True
    timeout: int = 30
    retry_count: int = 3
```

### GROK.md Style

Each skill and agent must have a GROK.md file:

```markdown
# Skill/Agent Name

## Overview
Brief description of what this skill/agent does.

## Capabilities
- List of main capabilities
- Each capability on a new line

## Usage
How to use this skill/agent.

## Examples
Code examples showing usage.

## Integration
How it integrates with other skills/agents.
```

### Commit Messages

We follow conventional commits:

```
feat: Add new skill domain for quantum computing
fix: Fix type error in NLP resource file
docs: Update README with new agents
refactor: Improve performance of analytics engine
test: Add unit tests for IoT agent
chore: Update dependencies
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/unit/test_skills.py -v

# Run with coverage
python -m pytest --cov=. tests/

# Run linting
python -m ruff check .
python -m mypy .
```

### Writing Tests

```python
import pytest
from skills.example.resources.example import ExampleEngine

class TestExampleEngine:
    """Tests for ExampleEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = ExampleEngine()
    
    def test_process_data(self):
        """Test data processing."""
        result = self.engine.process_data([{"value": 1.0}])
        assert result is not None
        assert len(result) == 1
    
    def test_edge_cases(self):
        """Test edge case handling."""
        with pytest.raises(ValueError):
            self.engine.process_data([])
```

## 🔍 Code Review Process

1. **Pull Request Title**: Use conventional commit format
2. **Description**: Explain what you changed and why
3. **Tests**: Ensure all tests pass
4. **Linting**: No linting errors
5. **Documentation**: Update relevant docs
6. **Review**: At least one approval required

### Review Criteria

- Code quality and maintainability
- Test coverage
- Documentation completeness
- Performance impact
- Security considerations

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Description**: What you were trying to do
2. **Steps to Reproduce**: Detailed reproduction steps
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Python version, etc.
6. **Screenshots/Logs**: If applicable

## 💡 Suggestions

For feature requests:

1. Check if it already exists
2. Explain the use case
3. Describe the expected implementation
4. Consider integration with existing skills

## 📚 Resources

- [Python Style Guide](STYLE_GUIDE.md)
- [Testing Guide](TESTING_GUIDE.md)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 🏆 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributors graph

Thank you for contributing! 🚀
