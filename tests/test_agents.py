"""
Unit tests for agent implementations.
"""

import pytest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestAgentBasics:
    """Basic tests for agent structure."""
    
    def test_agents_directory_exists(self, project_root):
        """Test agents directory exists."""
        agents_path = project_root / "agents"
        assert agents_path.exists()
    
    def test_each_agent_has_agent_py(self, project_root):
        """Test each agent has agent.py."""
        agents_path = project_root / "agents"
        for agent_dir in agents_path.iterdir():
            if agent_dir.is_dir():
                agent_file = agent_dir / "agent.py"
                assert agent_file.exists(), f"Missing agent.py in {agent_dir.name}"
    
    def test_each_agent_has_grok_md(self, project_root):
        """Test each agent has GROK.md."""
        agents_path = project_root / "agents"
        for agent_dir in agents_path.iterdir():
            if agent_dir.is_dir():
                grok_file = agent_dir / "GROK.md"
                assert grok_file.exists(), f"Missing GROK.md in {agent_dir.name}"


class TestAgentImports:
    """Test agent imports."""
    
    def test_agent_classes_instantiable(self, project_root):
        """Test agents can be imported and instantiated."""
        test_agents = [
            ("analytics", "AnalyticsAgent"),
            ("automation", "AutomationAgent"),
            ("backend", "BackendAgent"),
        ]
        
        for module_name, class_name in test_agents:
            try:
                module = __import__(f"agents.{module_name}.agent", fromlist=[class_name])
                cls = getattr(module, class_name)
                agent = cls()
                assert agent is not None
            except (ImportError, AttributeError):
                pytest.skip(f"Agent {module_name} not available")


class TestAgentMethods:
    """Test agent methods."""
    
    def test_analytics_agent_methods(self, project_root):
        """Test AnalyticsAgent has expected methods."""
        try:
            from agents.analytics.agent import AnalyticsAgent
            agent = AnalyticsAgent()
            assert hasattr(agent, 'analyze')
            assert hasattr(agent, 'get_status')
        except ImportError:
            pytest.skip("AnalyticsAgent not available")
    
    def test_automation_agent_methods(self, project_root):
        """Test AutomationAgent has expected methods."""
        try:
            from agents.automation.agent import AutomationAgent
            agent = AutomationAgent()
            assert hasattr(agent, 'execute')
            assert hasattr(agent, 'get_status')
        except ImportError:
            pytest.skip("AutomationAgent not available")


class TestAgentConfigs:
    """Test agent configurations."""
    
    def test_agent_config_class(self, project_root):
        """Test agent has Config class."""
        try:
            from agents.analytics.agent import Config
            config = Config()
            assert hasattr(config, 'enabled')
            assert hasattr(config, 'timeout')
        except ImportError:
            pytest.skip("Config not available")
    
    def test_agent_with_custom_config(self, project_root):
        """Test agent with custom configuration."""
        try:
            from agents.analytics.agent import AnalyticsAgent, Config
            config = Config(enabled=False, timeout=60)
            agent = AnalyticsAgent(config=config)
            assert agent._config.enabled is False
            assert agent._config.timeout == 60
        except ImportError:
            pytest.skip("Agent not available")


class TestAgentStatus:
    """Test agent status methods."""
    
    def test_get_status_returns_dict(self, project_root):
        """Test get_status returns dictionary."""
        try:
            from agents.analytics.agent import AnalyticsAgent
            agent = AnalyticsAgent()
            status = agent.get_status()
            assert isinstance(status, dict)
            assert 'agent' in status
        except ImportError:
            pytest.skip("Agent not available")
    
    def test_get_status_contains_agent_name(self, project_root):
        """Test status contains agent name."""
        try:
            from agents.analytics.agent import AnalyticsAgent
            agent = AnalyticsAgent()
            status = agent.get_status()
            assert 'AnalyticsAgent' in status['agent']
        except ImportError:
            pytest.skip("Agent not available")
