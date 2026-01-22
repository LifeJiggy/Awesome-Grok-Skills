# Style Guide

This guide defines the coding standards and patterns used throughout Awesome Grok Skills.

## 📋 Table of Contents

1. [General Principles](#general-principles)
2. [Python Style](#python-style)
3. [Code Organization](#code-organization)
4. [Documentation](#documentation)
5. [Naming Conventions](#naming-conventions)
6. [Error Handling](#error-handling)
7. [Performance](#performance)
8. [Security](#security)

---

## 🎯 General Principles

### DRY (Don't Repeat Yourself)
- Extract common functionality into shared utilities
- Use inheritance and composition appropriately
- Avoid code duplication across skills and agents

### KISS (Keep It Simple, Stupid)
- Prefer simple solutions over complex ones
- Avoid premature optimization
- Write readable, maintainable code

### SOLID Principles
- **S**ingle Responsibility: Each class has one reason to change
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes can replace base types
- **I**nterface Segregation: Many specific interfaces over one general
- **D**ependency Inversion: Depend on abstractions, not concretions

### YAGNI (You Aren't Gonna Need It)
- Don't add functionality until it's necessary
- Avoid speculative code
- Implement what's needed, not what's anticipated

---

## 🐍 Python Style

### PEP 8 Compliance

We follow PEP 8 with these additions:

```python
# Line length: 100 characters max
# Indentation: 4 spaces (no tabs)
# Blank lines: 2 between classes, 1 between methods

class ExampleClass:
    """A short description of the class.
    
    A longer description can be provided here if needed.
    """
    
    CONSTANT_VALUE = "example"
    
    def __init__(self, param: str) -> None:
        """Initialize the class.
        
        Args:
            param: Description of parameter
        """
        self._param = param
    
    def method_name(self, value: int) -> bool:
        """Short description of method.
        
        Args:
            value: Description of value
            
        Returns:
            Description of return value
        """
        return bool(value)
```

### Type Hints

**Required for all public APIs:**

```python
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime

# Use type hints
def process_items(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process a list of items."""
    result: Dict[str, Any] = {}
    for item in items:
        result[item["id"]] = item["value"]
    return result

# Use Optional for nullable types
def find_item(items: List[str], target: str) -> Optional[int]:
    """Find index of target in items.
    
    Returns:
        Index if found, None otherwise
    """
    try:
        return items.index(target)
    except ValueError:
        return None

# Use Union for multiple types
def parse_value(value: Union[str, int, float]) -> float:
    """Parse value to float."""
    return float(value)
```

**Avoid**:

```python
# ❌ Bad
def func(a, b):
    return a + b

# ❌ Bad
def func(a: list, b: dict) -> any:
    pass

# ✅ Good
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
```

### Dataclasses

Use dataclasses for data models:

```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class User:
    """A user in the system."""
    id: str
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    roles: List[str] = field(default_factory=list)
    is_active: bool = True

@dataclass
class Config:
    """Configuration for a skill or agent."""
    enabled: bool = True
    timeout: int = 30
    retry_count: int = 3
    options: Dict[str, Any] = field(default_factory=dict)
```

### Enums

Use Enum for fixed sets:

```python
from enum import Enum, auto

class Status(Enum):
    """Status of a process or task."""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

class Priority(Enum):
    """Priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
```

---

## 📁 Code Organization

### File Structure

```
skill-name/
├── GROK.md              # Required: Skill documentation
├── __init__.py          # Optional: Package initialization
└── resources/
    └── skillname.py     # Required: Main implementation
```

### Imports

**Order:**

1. Standard library
2. Third-party
3. Local application

```python
# Standard library
import json
from datetime import datetime
from typing import List, Dict, Optional

# Third-party
import numpy as np
import pandas as pd
from pydantic import BaseModel

# Local
from .base import BaseClass
from ..utils import helper_function
```

**Avoid wildcard imports:**

```python
# ❌ Bad
from module import *

# ✅ Good
from module import ClassName, function_name
```

### Class Structure

```python
class ExampleEngine:
    """Engine for processing examples.
    
    This class provides functionality for processing and analyzing
    example data with high performance and accuracy.
    """
    
    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize the engine.
        
        Args:
            config: Optional configuration object
        """
        self._config = config or Config()
        self._initialize()
    
    def _initialize(self) -> None:
        """Private initialization method."""
        pass
    
    def process(self, data: List[Dict]) -> Dict[str, Any]:
        """Process input data.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed results
        """
        pass
    
    def __enter__(self) -> "ExampleEngine":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up resources."""
        pass
```

---

## 📝 Documentation

### Docstring Format

We use Google-style docstrings:

```python
def function_name(param1: str, param2: int = 10) -> bool:
    """Short description of the function.
    
    A longer description that provides more details about what
    the function does and how it works.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not positive
        
    Example:
        >>> function_name("test", 5)
        True
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    if param2 <= 0:
        raise TypeError("param2 must be positive")
    return True
```

### Comments

**Use sparingly, prefer self-documenting code:**

```python
# ✅ Good: Self-documenting
total_revenue = sum(order.amount for order in orders)

# ✅ Good: Complex algorithm explanation
# Use binary search for O(log n) performance
def binary_search(sorted_list: List[int], target: int) -> Optional[int]:
    pass

# ❌ Bad: Obvious comments
# Increment i by 1
i += 1

# ❌ Bad: Commented-out code
# def old_function():
#     pass
```

---

## 🏷️ Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Packages | lowercase with underscores | `neural_architecture_search` |
| Modules | lowercase with underscores | `nas_pipelines.py` |
| Classes | PascalCase | `NeuralArchitectureSearch` |
| Functions | snake_case | `process_data()` |
| Variables | snake_case | `data_point` |
| Constants | UPPER_SNAKE_CASE | `MAX_TIMEOUT` |
| Private methods | _snake_case | `_private_method()` |
| Type variables | PascalCase | `T = TypeVar('T')` |

**Variable Naming:**

```python
# ✅ Good
user_id = "123"
is_active = True
items_list = []
results_dict = {}

# ❌ Bad
d = "123"
act = True
lst = []
dict_var = {}

# Abbreviations (use sparingly)
# ✅ Acceptable
num_items = 10
max_val = 100
id_list = []

# ❌ Avoid
n = 10
mx = 100
ids = []
```

---

## ⚠️ Error Handling

### Use Specific Exceptions

```python
class CustomError(Exception):
    """Base exception for custom errors."""
    pass

class ValidationError(CustomError):
    """Raised when validation fails."""
    pass

class ConfigurationError(CustomError):
    """Raised when configuration is invalid."""
    pass

# ✅ Good
def validate_config(config: Dict) -> None:
    if "required_key" not in config:
        raise ValidationError("Missing required key: required_key")

# ❌ Bad: Catching too broad
try:
    risky_operation()
except Exception:
    pass
```

### Context Managers

```python
from contextlib import contextmanager

@contextmanager
def file_handler(filepath: str):
    """Context manager for file handling."""
    file = open(filepath, "r")
    try:
        yield file
    finally:
        file.close()

# Usage
with file_handler("data.txt") as f:
    content = f.read()
```

### Result Objects

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Result:
    """Result of an operation."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    
    @property
    def value(self) -> Any:
        if self.success:
            return self.data
        raise ValueError(f"Cannot get value from failed result: {self.error}")
```

---

## 🚀 Performance

### Avoid Premature Optimization

```python
# ✅ Good: Clear code first
def process_items(items: List[Dict]) -> List[Dict]:
    return [item for item in items if item["active"]]

# Optimize later if profiling shows it's needed
# @lru_cache(maxsize=128)
# def cached_process_items(items: Tuple[Dict, ...]) -> Tuple[Dict, ...]:
#     return tuple(process_items(items))
```

### Use Generators for Large Data

```python
def process_large_dataset(filepath: str) -> Generator[Dict, None, None]:
    """Process large dataset row by row."""
    with open(filepath, "r") as f:
        for line in f:
            yield json.loads(line)
```

### Efficient Data Structures

```python
from collections import defaultdict, deque
from typing import Dict, List

# Use defaultdict for missing keys
def count_words(text: str) -> Dict[str, int]:
    counts = defaultdict(int)
    for word in text.split():
        counts[word] += 1
    return dict(counts)

# Use deque for queue operations
def recent_items(n: int) -> deque:
    return deque(maxlen=n)
```

---

## 🔒 Security

### Never Hardcode Secrets

```python
import os
from dataclasses import dataclass

@dataclass
class SecurityConfig:
    """Security configuration - load from environment."""
    api_key: str = os.environ.get("API_KEY", "")
    db_password: str = os.environ.get("DB_PASSWORD", "")
    
    def __post_init__(self):
        if not self.api_key:
            raise ValueError("API_KEY environment variable required")
```

### Input Validation

```python
import re
from typing import Any

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection."""
    return user_input.strip().encode("ascii", "ignore").decode("ascii")
```

### Safe File Operations

```python
from pathlib import Path

def read_config(config_path: str) -> Dict:
    """Safely read configuration file."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {config_path}")
    return json.loads(path.read_text())
```

---

## 📚 Additional Resources

- [PEP 8](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [Pydantic](https://pydantic-docs.helpmanual.io/) for validation

---

**Remember: Code is read much more often than it's written. Write for clarity! 📖**
