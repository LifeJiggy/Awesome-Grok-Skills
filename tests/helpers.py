"""
Test utilities for Awesome Grok Skills.
"""

import pytest
from pathlib import Path
from typing import Any, Dict, List, Optional
import json


class TestHelpers:
    """Helper methods for testing."""
    
    @staticmethod
    def create_temp_skill(name: str, base_path: Path) -> Path:
        """Create a temporary skill for testing."""
        skill_path = base_path / "skills" / name
        skill_path.mkdir(parents=True, exist_ok=True)
        (skill_path / "resources").mkdir(exist_ok=True)
        return skill_path
    
    @staticmethod
    def create_temp_agent(name: str, base_path: Path) -> Path:
        """Create a temporary agent for testing."""
        agent_path = base_path / "agents" / name
        agent_path.mkdir(parents=True, exist_ok=True)
        return agent_path
    
    @staticmethod
    def create_test_data(count: int = 10) -> List[Dict[str, Any]]:
        """Create test data."""
        return [
            {
                "id": str(i),
                "value": float(i * 10),
                "label": f"Item {i}",
                "active": i % 2 == 0
            }
            for i in range(count)
        ]


class AssertionHelpers:
    """Custom assertion helpers."""
    
    @staticmethod
    def assert_valid_response(response: Dict[str, Any]) -> None:
        """Assert that a response has required fields."""
        assert "success" in response
        assert "data" in response
    
    @staticmethod
    def assert_valid_config(config: Any) -> None:
        """Assert that a config object has required fields."""
        assert hasattr(config, "enabled")
        assert hasattr(config, "timeout")
    
    @staticmethod
    def assert_processed_result(result: Any) -> None:
        """Assert that a processed result is valid."""
        assert result is not None
        if isinstance(result, dict):
            assert "status" in result or "result" in result


class MockHelpers:
    """Mock helpers for testing."""
    
    @staticmethod
    def mock_grok_response(content: str = "Test response") -> Dict[str, Any]:
        """Create a mock Grok response."""
        return {
            "choices": [
                {
                    "message": {
                        "content": content
                    }
                }
            ]
        }
    
    @staticmethod
    def mock_api_response(status: int = 200, data: Dict = None) -> MagicMock:
        """Create a mock API response."""
        mock_response = MagicMock()
        mock_response.status_code = status
        mock_response.json.return_value = data or {"status": "ok"}
        return mock_response
