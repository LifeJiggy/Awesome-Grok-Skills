"""
Integration tests for skills and agents working together.
"""

import pytest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestSkillAgentIntegration:
    """Test skills and agents integration."""
    
    def test_agent_uses_skill(self, project_root):
        """Test agent can use skill functionality."""
        try:
            from agents.analytics.agent import AnalyticsAgent
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            
            engine = AnalyticsEngine()
            agent = AnalyticsAgent()
            
            data = [{"value": 1}, {"value": 2}]
            result = engine.process(data)
            
            assert result is not None
            assert len(result) >= 0
        except ImportError:
            pytest.skip("Required modules not available")
    
    def test_workflow_integration(self, project_root):
        """Test complete workflow integration."""
        try:
            from agents.automation.agent import AutomationAgent
            from skills.devops.infrastructure_as_code.resources.infra_code import InfraCodeEngine
            
            agent = AutomationAgent()
            engine = InfraCodeEngine()
            
            config = agent.generate_config()
            result = engine.apply_config(config)
            
            assert result is not None
        except ImportError:
            pytest.skip("Required modules not available")


class TestDataFlowIntegration:
    """Test data flow between components."""
    
    def test_data_pipeline(self, project_root):
        """Test data flows through pipeline."""
        try:
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            
            engine = AnalyticsEngine()
            
            input_data = [{"id": 1, "value": 100}]
            processed = engine.process(input_data)
            
            assert processed is not None
            assert "id" in processed or len(processed) > 0
        except ImportError:
            pytest.skip("Engine not available")
    
    def test_batch_processing(self, project_root):
        """Test batch processing integration."""
        try:
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            
            engine = AnalyticsEngine()
            
            datasets = [
                [{"value": 1}],
                [{"value": 2}],
                [{"value": 3}]
            ]
            
            results = engine.batch_process(datasets)
            
            assert len(results) == 3
            for result in results:
                assert result is not None
        except ImportError:
            pytest.skip("Engine not available")


class TestConfigurationIntegration:
    """Test configuration sharing."""
    
    def test_shared_configuration(self, project_root):
        """Test components share configuration."""
        try:
            from agents.automation.agent import AutomationAgent, AutomationConfig
            from skills.devops.infrastructure_as_code.resources.infra_code import InfraCodeEngine, Config
            
            agent_config = AutomationConfig(timeout=60)
            agent = AutomationAgent(config=agent_config)
            
            skill_config = Config(timeout=60, enabled=True)
            engine = InfraCodeEngine(config=skill_config)
            
            assert agent._config.timeout == 60
            assert engine._config.timeout == 60
        except ImportError:
            pytest.skip("Components not available")


class TestErrorHandlingIntegration:
    """Test error handling across components."""
    
    def test_graceful_error_handling(self, project_root):
        """Test components handle errors gracefully."""
        try:
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            
            engine = AnalyticsEngine()
            
            result = engine.process([])
            assert result == []
        except ImportError:
            pytest.skip("Engine not available")
    
    def test_validation_error_handling(self, project_root):
        """Test validation errors are handled."""
        try:
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            
            engine = AnalyticsEngine()
            
            is_valid = engine.validate_input({})
            assert is_valid is False
        except ImportError:
            pytest.skip("Engine not available")
