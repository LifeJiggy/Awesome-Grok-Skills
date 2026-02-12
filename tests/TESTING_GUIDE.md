# Testing Guide

This guide covers testing standards and practices for Awesome Grok Skills.

## 📋 Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Test Structure](#test-structure)
3. [Writing Tests](#writing-tests)
4. [Test Types](#test-types)
5. [Running Tests](#running-tests)
6. [Coverage Requirements](#coverage-requirements)
7. [Mocking](#mocking)
8. [CI/CD Integration](#cicd-integration)

---

## 🎯 Testing Philosophy

### Why We Test

- **Reliability**: Catch bugs before users do
- **Refactoring**: Confidence when changing code
- **Documentation**: Tests serve as living documentation
- **Performance**: Ensure optimizations don't break functionality

### Testing Pyramid

```
        /\
       /  \
      /    \     E2E Tests (10%)
     /------\
    /        \
   /          \   Integration Tests (20%)
  /------------\
 /              \
/                \  Unit Tests (70%)
------------------
```

---

## 📁 Test Structure

### Directory Layout

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_skills/
│   │   ├── __init__.py
│   │   ├── test_ai_ml.py
│   │   ├── test_cloud.py
│   │   └── test_data_science.py
│   └── test_agents/
│       ├── __init__.py
│       ├── test_analytics.py
│       └── test_research.py
├── integration/             # Integration tests
│   ├── __init__.py
│   ├── test_skills_agents.py
│   └── test_workflows.py
└── e2e/                     # End-to-end tests
    ├── __init__.py
    └── test_full_flows.py
```

### conftest.py

```python
import pytest
from unittest.mock import MagicMock, patch
from typing import Generator

@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent

@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        "timeout": 30,
        "retry_count": 3,
        "enabled": True
    }

@pytest.fixture
def sample_data() -> Generator[List[Dict], None, None]:
    """Sample data for testing."""
    data = [
        {"id": "1", "value": 100.0, "label": "A"},
        {"id": "2", "value": 200.0, "label": "B"},
        {"id": "3", "value": 150.0, "label": "C"},
    ]
    yield data

@pytest.fixture
def mock_api_response():
    """Mock API response."""
    return {
        "status": "success",
        "data": [{"id": 1, "name": "test"}],
        "count": 1
    }
```

---

## ✍️ Writing Tests

### Unit Test Template

```python
import pytest
from skills.example.resources.example import ExampleEngine, Config

class TestExampleEngine:
    """Unit tests for ExampleEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = ExampleEngine(Config(enabled=True))
    
    def test_initialization(self):
        """Test engine initialization."""
        assert self.engine.enabled is True
        assert self.engine._processed_count == 0
    
    def test_process_data_success(self, sample_data):
        """Test successful data processing."""
        result = self.engine.process(sample_data)
        assert result is not None
        assert len(result) == 3
        assert self.engine._processed_count == 3
    
    def test_process_empty_data(self):
        """Test processing empty data."""
        result = self.engine.process([])
        assert result == []
    
    def test_process_with_custom_config(self):
        """Test processing with custom configuration."""
        engine = ExampleEngine(Config(timeout=60))
        assert engine.timeout == 60
    
    def test_invalid_data_raises_error(self):
        """Test that invalid data raises ValueError."""
        with pytest.raises(ValueError):
            self.engine.process([{"invalid": "data"}])
    
    def test_statistics_calculation(self, sample_data):
        """Test statistics calculation."""
        stats = self.engine.calculate_statistics(sample_data)
        assert stats["count"] == 3
        assert stats["sum"] == 450.0
        assert stats["mean"] == 150.0
```

### Integration Test Template

```python
import pytest
from skills.example.resources.example import ExampleEngine
from agents.example_agent import ExampleAgent

class TestSkillsAgentsIntegration:
    """Integration tests for skills and agents."""
    
    def test_engine_and_agent_workflow(self):
        """Test complete workflow from agent to engine."""
        agent = ExampleAgent()
        engine = ExampleEngine()
        
        # Agent generates configuration
        config = agent.generate_config()
        
        # Engine uses configuration
        result = engine.process_with_config(config)
        
        assert result is not None
        assert agent.validate_result(result) is True
    
    def test_multi_step-process(self):
        """Test multi-step processing pipeline."""
        pipeline = [
            ExampleEngine(),
            ValidationEngine(),
            ExportEngine()
        ]
        
        data = [{"value": 100}]
        for engine in pipeline:
            data = engine.process(data)
        
        assert len(data) == 1
```

### E2E Test Template

```python
import pytest
import subprocess
import sys

class TestEndToEnd:
    """End-to-end tests for complete workflows."""
    
    def test_skill_cli_usage(self):
        """Test using skill from command line."""
        result = subprocess.run(
            [sys.executable, "-m", "skills.example.cli", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "help" in result.stdout.lower()
    
    def test_agent_completion(self):
        """Test agent completes task successfully."""
        agent = ExampleAgent()
        result = agent.complete_task(
            prompt="Analyze this data",
            data={"sample": "data"}
        )
        assert result.success is True
        assert result.output is not None
```

---

## 🧪 Test Types

### Unit Tests

```python
# tests/unit/test_skills/test_data_processing.py

from skills.data_science.resources.analytics import AnalyticsEngine
import pytest

class TestDataProcessing:
    """Unit tests for data processing functionality."""
    
    def test_normalize_data(self):
        """Test data normalization."""
        engine = AnalyticsEngine()
        data = [1, 2, 3, 4, 5]
        normalized = engine.normalize(data, method="minmax")
        
        assert min(normalized) == 0.0
        assert max(normalized) == 1.0
    
    def test_outlier_detection(self):
        """Test outlier detection."""
        engine = AnalyticsEngine()
        data = [1, 2, 3, 4, 100]  # 100 is outlier
        outliers = engine.detect_outliers(data, method="zscore")
        
        assert 100 in outliers
        assert len(outliers) == 1
    
    def test_correlation_matrix(self):
        """Test correlation calculation."""
        engine = AnalyticsEngine()
        df = {"a": [1, 2, 3], "b": [2, 4, 6], "c": [1, 1, 1]}
        corr = engine.correlation_matrix(df)
        
        assert corr["a"]["b"] == 1.0
        assert corr["a"]["c"] == 0.0
```

### Property-Based Tests

```python
from hypothesis import given, strategies as st

class TestProperties:
    """Property-based tests for invariants."""
    
    @given(st.lists(st.floats(allow_nan=False)))
    def test_normalization_preserves_order(self, data):
        """Normalization should preserve data order."""
        if len(data) == 0:
            return
        
        engine = AnalyticsEngine()
        normalized = engine.normalize(data, method="minmax")
        
        # Check relative order preserved
        for i in range(len(data) - 1):
            if data[i] < data[i + 1]:
                assert normalized[i] <= normalized[i + 1]
    
    @given(st.lists(st.integers(min_value=0)))
    def test_sum_unchanged_after_sorting(self, data):
        """Sorting should not change sum."""
        original_sum = sum(data)
        sorted_data = sorted(data)
        assert sum(sorted_data) == original_sum
```

### Performance Tests

```python
import pytest
import time
from skills.example.resources.example import ExampleEngine

class TestPerformance:
    """Performance and load tests."""
    
    def test_processing_speed(self):
        """Test that processing completes within time limit."""
        engine = ExampleEngine()
        large_data = [{"value": i} for i in range(10000)]
        
        start = time.time()
        result = engine.process(large_data)
        elapsed = time.time() - start
        
        # Should process 10k items in under 1 second
        assert elapsed < 1.0
        assert len(result) == 10000
    
    def test_concurrent_processing(self):
        """Test concurrent processing performance."""
        import concurrent.futures
        
        engine = ExampleEngine()
        data_chunks = [[{"value": i} for i in range(1000)] for _ in range(10)]
        
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(engine.process, data_chunks))
        elapsed = time.time() - start
        
        assert len(results) == 10
        assert all(len(r) == 1000 for r in results)
```

---

## 🏃 Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_skills/test_ai_ml.py

# Run specific test class
pytest tests/unit/test_skills/test_ai_ml.py::TestNeuralArchitectureSearch

# Run specific test
pytest tests/unit/test_skills/test_ai_ml.py::TestNeuralArchitectureSearch::test_initialization
```

### Useful Options

```bash
# Run with coverage
pytest --cov=. --cov-report=html

# Run in parallel
pytest -n auto

# Stop on first failure
pytest -x

# Run tests matching pattern
pytest -k "test_process"

# Show local variables in tracebacks
pytest -l

# Capture output
pytest -s  # show stdout
pytest --capture=no

# Generate JUnit XML
pytest --junitxml=test-results.xml

# Generate HTML report
pytest --html=report.html
```

### Configuration (pytest.ini)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
filterwarnings =
    ignore::DeprecationWarning
```

---

## 📊 Coverage Requirements

### Minimum Coverage

| Component | Minimum Coverage |
|-----------|------------------|
| Core Skills | 90% |
| Agents | 85% |
| Utilities | 95% |
| Integration | 70% |

### Coverage Report

```bash
# Generate coverage report
pytest --cov=. --cov-report=term-missing --cov-report=html

# View HTML report
open htmlcov/index.html

# Coverage by file
pytest --cov=. --cov-report=table

# Fail if coverage below threshold
pytest --cov=. --cov-fail-under=80
```

### Coverage Configuration (pyproject.toml)

```toml
[tool.coverage.run]
source = ["skills", "agents"]
omit = [
    "tests/*",
    "*/__init__.py",
    "*/*/__init__.py"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:"
]
```

---

## 🎭 Mocking

### Using unittest.mock

```python
from unittest.mock import MagicMock, patch, Mock
import pytest

class TestWithMocks:
    """Tests using mocks."""
    
    def test_external_api_call(self, mock_api_response):
        """Test handling of external API calls."""
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_api_response
            mock_get.return_value.status_code = 200
            
            result = call_external_api("https://api.example.com/data")
            
            assert result == mock_api_response
            mock_get.assert_called_once()
    
    def test_database_operations(self):
        """Test database operations with mock."""
        mock_db = MagicMock()
        mock_db.query.return_value = [{"id": 1, "name": "test"}]
        
        service = DataService(mock_db)
        result = service.get_user("test")
        
        assert result["name"] == "test"
        mock_db.query.assert_called_once()
    
    def test_file_operations(self, tmp_path):
        """Test file operations."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test data")
        
        engine = FileEngine(str(test_file))
        content = engine.read()
        
        assert content == "test data"
```

### Using pytest-mock

```python
import pytest

class TestWithPytestMocker:
    """Tests using pytest-mock fixture."""
    
    def test_with_mocker(self, mocker):
        """Use mocker fixture for mocking."""
        mock_function = mocker.patch("module.function")
        mock_function.return_value = "mocked"
        
        result = module.function()
        
        assert result == "mocked"
        mock_function.assert_called_once()
    
    def test_spy_on_method(self, mocker):
        """Spy on existing method."""
        engine = ExampleEngine()
        spy = mocker.spy(engine, "process_data")
        
        engine.run([{"value": 1}])
        
        spy.assert_called_once_with([{"value": 1}])
    
    def test_mocking_property(self, mocker):
        """Mock property access."""
        engine = ExampleEngine()
        mocker.patch.object(engine, "enabled", new_callable=lambda: property(lambda self: False))
        
        assert engine.enabled is False
```

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/tests.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      
      - name: Run unit tests
        run: |
          pytest tests/unit/ -v --cov=skills --cov=agents
          pytest tests/unit/ -v --cov=skills --cov=agents --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: unittests
          name: codecov-umbrella

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      
      - name: Run integration tests
        run: pytest tests/integration/ -v

  lint:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install linters
        run: pip install ruff mypy black
      
      - name: Run ruff
        run: ruff check .
      
      - name: Run mypy
        run: mypy skills/ agents/
      
      - name: Run black
        run: black --check .
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key
  
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
  
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

---

## 📝 Test Checklist

Before submitting a PR, ensure:

- [ ] All tests pass (`pytest`)
- [ ] Coverage meets minimum requirements
- [ ] No linting errors (`ruff`, `mypy`)
- [ ] New tests added for new functionality
- [ ] Tests are isolated and don't depend on external services
- [ ] Tests are fast (under 1 second each)
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] Integration tests pass for affected components

---

## 🔗 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Hypothesis](https://hypothesis.readthedocs.io/)
- [pytest-mock](https://pytest-mock.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Remember: Tests are not just for catching bugs—they're for building confidence! 🧪**
