"""
Test configuration for Awesome Grok Skills.
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return [
        {"id": "1", "value": 100.0, "label": "A"},
        {"id": "2", "value": 200.0, "label": "B"},
        {"id": "3", "value": 150.0, "label": "C"},
    ]


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        "timeout": 30,
        "retry_count": 3,
        "enabled": True
    }


@pytest.fixture
def mock_api_response():
    """Mock API response."""
    return {
        "status": "success",
        "data": [{"id": 1, "name": "test"}],
        "count": 1
    }


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory."""
    return tmp_path


@pytest.fixture
def mock_grok_api():
    """Mock Grok API."""
    with patch("skills.core.real_time_research.resources.real_time_research.GrokClient") as mock:
        yield mock


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
