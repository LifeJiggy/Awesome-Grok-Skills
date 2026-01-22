"""
Unit tests for skill template and basic functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestSkillStructure:
    """Test skill directory structure."""
    
    def test_skills_directory_exists(self, project_root):
        """Test that skills directory exists."""
        skills_path = project_root / "skills"
        assert skills_path.exists()
        assert skills_path.is_dir()
    
    def test_agents_directory_exists(self, project_root):
        """Test that agents directory exists."""
        agents_path = project_root / "agents"
        assert agents_path.exists()
        assert agents_path.is_dir()
    
    def test_templates_directory_exists(self, project_root):
        """Test that templates directory exists."""
        templates_path = project_root / "templates"
        assert templates_path.exists()
        assert templates_path.is_dir()
    
    def test_scripts_directory_exists(self, project_root):
        """Test that scripts directory exists."""
        scripts_path = project_root / "scripts"
        assert scripts_path.exists()
        assert scripts_path.is_dir()
    
    def test_docs_directory_exists(self, project_root):
        """Test that docs directory exists."""
        docs_path = project_root / "docs"
        assert docs_path.exists()
        assert docs_path.is_dir()


class TestSkillContent:
    """Test skill file content."""
    
    def test_each_skill_has_grok_md(self, project_root):
        """Test that each skill has a GROK.md file."""
        skills_path = project_root / "skills"
        
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                grok_file = skill_dir / "GROK.md"
                assert grok_file.exists(), f"Missing GROK.md in {skill_dir.name}"
    
    def test_each_skill_has_resources(self, project_root):
        """Test that each skill has a resources directory."""
        skills_path = project_root / "skills"
        
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                resources_dir = skill_dir / "resources"
                assert resources_dir.exists(), f"Missing resources/ in {skill_dir.name}"
    
    def test_each_skill_has_python_file(self, project_root):
        """Test that each skill has at least one Python file."""
        skills_path = project_root / "skills"
        
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                resources_dir = skill_dir / "resources"
                if resources_dir.exists():
                    python_files = list(resources_dir.glob("*.py"))
                    assert len(python_files) > 0, f"No Python files in {skill_dir.name}/resources/"
    
    def test_grok_md_has_required_sections(self, project_root):
        """Test that GROK.md files have required sections."""
        skills_path = project_root / "skills"
        
        required_sections = ["Overview", "Usage", "API Reference"]
        
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                grok_file = skill_dir / "GROK.md"
                if grok_file.exists():
                    content = grok_file.read_text()
                    for section in required_sections:
                        assert f"## {section}" in content, \
                            f"Missing {section} section in {skill_dir.name}/GROK.md"


class TestAgentStructure:
    """Test agent directory structure."""
    
    def test_each_agent_has_grok_md(self, project_root):
        """Test that each agent has a GROK.md file."""
        agents_path = project_root / "agents"
        
        for agent_dir in agents_path.iterdir():
            if agent_dir.is_dir():
                grok_file = agent_dir / "GROK.md"
                assert grok_file.exists(), f"Missing GROK.md in {agent_dir.name}"
    
    def test_each_agent_has_agent_py(self, project_root):
        """Test that each agent has an agent.py file."""
        agents_path = project_root / "agents"
        
        for agent_dir in agents_path.iterdir():
            if agent_dir.is_dir():
                agent_file = agent_dir / "agent.py"
                assert agent_file.exists(), f"Missing agent.py in {agent_dir.name}"


class TestTemplates:
    """Test template files."""
    
    def test_skill_template_exists(self, project_root):
        """Test that skill template exists."""
        template_path = project_root / "templates" / "skill-template.md"
        assert template_path.exists()
    
    def test_agent_template_exists(self, project_root):
        """Test that agent template exists."""
        template_path = project_root / "templates" / "agent-template.md"
        assert template_path.exists()
    
    def test_project_template_exists(self, project_root):
        """Test that project template exists."""
        template_path = project_root / "templates" / "project-GROK.md"
        assert template_path.exists()


class TestScripts:
    """Test script files."""
    
    def test_setup_script_exists(self, project_root):
        """Test that setup script exists."""
        script_path = project_root / "scripts" / "setup.py"
        assert script_path.exists()
    
    def test_generate_skill_script_exists(self, project_root):
        """Test that generate_skill script exists."""
        script_path = project_root / "scripts" / "generate_skill.py"
        assert script_path.exists()
    
    def test_validate_script_exists(self, project_root):
        """Test that validate script exists."""
        script_path = project_root / "scripts" / "validate_structure.py"
        assert script_path.exists()
    
    def test_setup_script_is_executable(self, project_root):
        """Test that setup script has proper shebang."""
        script_path = project_root / "scripts" / "setup.py"
        content = script_path.read_text()
        assert "#!/usr/bin/env python3" in content


class TestDocumentation:
    """Test documentation files."""
    
    def test_contributing_md_exists(self, project_root):
        """Test that CONTRIBUTING.md exists."""
        doc_path = project_root / "docs" / "CONTRIBUTING.md"
        assert doc_path.exists()
    
    def test_code_of_conduct_exists(self, project_root):
        """Test that CODE_OF_CONDUCT.md exists."""
        doc_path = project_root / "docs" / "CODE_OF_CONDUCT.md"
        assert doc_path.exists()
    
    def test_style_guide_exists(self, project_root):
        """Test that STYLE_GUIDE.md exists."""
        doc_path = project_root / "docs" / "STYLE_GUIDE.md"
        assert doc_path.exists()
    
    def test_testing_guide_exists(self, project_root):
        """Test that TESTING_GUIDE.md exists."""
        doc_path = project_root / "docs" / "TESTING_GUIDE.md"
        assert doc_path.exists()
    
    def test_deployment_guide_exists(self, project_root):
        """Test that DEPLOYMENT.md exists."""
        doc_path = project_root / "docs" / "DEPLOYMENT.md"
        assert doc_path.exists()


class TestPythonImports:
    """Test Python import functionality."""
    
    def test_skill_module_imports(self, project_root):
        """Test that skill modules can be imported."""
        skills_path = project_root / "skills"
        
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                resources_dir = skill_dir / "resources"
                if resources_dir.exists():
                    for py_file in resources_dir.glob("*.py"):
                        module_name = f"skills.{skill_dir.name}.resources.{py_file.stem}"
                        try:
                            __import__(module_name)
                        except ImportError as e:
                            pytest.fail(f"Failed to import {module_name}: {e}")
    
    def test_agent_module_imports(self, project_root):
        """Test that agent modules can be imported."""
        agents_path = project_root / "agents"
        
        for agent_dir in agents_path.iterdir():
            if agent_dir.is_dir():
                agent_file = agent_dir / "agent.py"
                if agent_file.exists():
                    module_name = f"agents.{agent_dir.name}.agent"
                    try:
                        __import__(module_name)
                    except ImportError as e:
                        pytest.fail(f"Failed to import {module_name}: {e}")


class TestReadme:
    """Test README file."""
    
    def test_readme_exists(self, project_root):
        """Test that README.md exists."""
        readme_path = project_root / "README.md"
        assert readme_path.exists()
    
    def test_readme_has_badges(self, project_root):
        """Test that README has badges."""
        readme_path = project_root / "README.md"
        content = readme_path.read_text()
        
        assert "[![Awesome]" in content
        assert "[![License" in content
        assert "[![Skills]" in content
        assert "[![Agents]" in content
    
    def test_readme_has_structure_section(self, project_root):
        """Test that README has structure section."""
        readme_path = project_root / "README.md"
        content = readme_path.read_text()
        
        assert "## 📁 Complete Repository Structure" in content
