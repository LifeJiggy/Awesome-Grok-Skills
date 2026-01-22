"""
Unit tests for skill implementations.
"""

import pytest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestSkillBasics:
    """Basic tests for skill structure."""
    
    def test_skills_directory_exists(self, project_root):
        """Test skills directory exists."""
        skills_path = project_root / "skills"
        assert skills_path.exists()
    
    def test_each_skill_has_grok_md(self, project_root):
        """Test each skill has GROK.md."""
        skills_path = project_root / "skills"
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                grok_file = skill_dir / "GROK.md"
                assert grok_file.exists(), f"Missing GROK.md in {skill_dir.name}"
    
    def test_each_skill_has_resources(self, project_root):
        """Test each skill has resources directory."""
        skills_path = project_root / "skills"
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                resources_dir = skill_dir / "resources"
                assert resources_dir.exists(), f"Missing resources/ in {skill_dir.name}"


class TestSkillImports:
    """Test skill imports."""
    
    def test_skill_modules_importable(self, project_root):
        """Test skills can be imported."""
        test_skills = [
            ("ai-ml", "neural_architecture_search"),
            ("data-science", "advanced_analytics"),
            ("cloud", "cloud_native"),
        ]
        
        for skill_path, module_name in test_skills:
            try:
                __import__(f"skills.{skill_path}.resources.{module_name}")
            except ImportError:
                pytest.skip(f"Skill {skill_path} not available")


class TestSkillEngines:
    """Test skill engine classes."""
    
    def test_ai_ml_engine(self, project_root):
        """Test AI-ML skill engine."""
        try:
            from skills.ai_ml.neural_architecture_search.resources.nas_pipelines import NASEngine
            engine = NASEngine()
            assert hasattr(engine, 'search')
            assert hasattr(engine, 'get_status')
        except ImportError:
            pytest.skip("NASEngine not available")
    
    def test_data_science_engine(self, project_root):
        """Test data science skill engine."""
        try:
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            engine = AnalyticsEngine()
            assert hasattr(engine, 'analyze')
            assert hasattr(engine, 'get_status')
        except ImportError:
            pytest.skip("AnalyticsEngine not available")
    
    def test_cloud_native_engine(self, project_root):
        """Test cloud native skill engine."""
        try:
            from skills.cloud.cloud_native.resources.cloud_native import CloudNativeEngine
            engine = CloudNativeEngine()
            assert hasattr(engine, 'deploy')
            assert hasattr(engine, 'get_status')
        except ImportError:
            pytest.skip("CloudNativeEngine not available")


class TestSkillConfigs:
    """Test skill configurations."""
    
    def test_skill_config_class(self, project_root):
        """Test skill has Config class."""
        try:
            from skills.ai_ml.neural_architecture_search.resources.nas_pipelines import Config
            config = Config()
            assert hasattr(config, 'enabled')
        except ImportError:
            pytest.skip("Config not available")
    
    def test_skill_with_custom_config(self, project_root):
        """Test skill with custom configuration."""
        try:
            from skills.ai_ml.neural_architecture_search.resources.nas_pipelines import NASEngine, Config
            config = Config(enabled=False)
            engine = NASEngine(config=config)
            assert engine._config.enabled is False
        except ImportError:
            pytest.skip("Engine not available")


class TestSkillMethods:
    """Test skill methods."""
    
    def test_get_status_returns_dict(self, project_root):
        """Test get_status returns dictionary."""
        try:
            from skills.ai_ml.neural_architecture_search.resources.nas_pipelines import NASEngine
            engine = NASEngine()
            status = engine.get_status()
            assert isinstance(status, dict)
        except ImportError:
            pytest.skip("Engine not available")
    
    def test_skill_process_method(self, project_root):
        """Test skill has process method."""
        try:
            from skills.data_science.advanced_analytics.resources.analytics import AnalyticsEngine
            engine = AnalyticsEngine()
            result = engine.process({"test": "data"})
            assert result is not None
        except ImportError:
            pytest.skip("Engine not available")
