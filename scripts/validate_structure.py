#!/usr/bin/env python3
"""
Validate the repository structure for Awesome Grok Skills.

This script checks that all skills and agents follow the required structure.
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any
import json


@dataclass
class ValidationResult:
    """Result of a validation check."""
    passed: bool
    message: str
    path: Path


class RepositoryValidator:
    """Validator for repository structure."""
    
    def __init__(self, root_path: Path):
        """Initialize the validator.
        
        Args:
            root_path: Path to the repository root
        """
        self.root = root_path
        self.results: List[ValidationResult] = []
    
    def validate_all(self) -> bool:
        """Run all validations.
        
        Returns:
            True if all validations pass
        """
        print("🔍 Validating repository structure...\n")
        
        self.validate_directories()
        self.validate_skills_structure()
        self.validate_agents_structure()
        self.validate_templates()
        self.validate_scripts()
        
        return all(r.passed for r in self.results)
    
    def validate_directories(self) -> None:
        """Validate required directories exist."""
        print("📁 Checking directories...")
        
        required_dirs = ["skills", "agents", "templates", "scripts", "docs"]
        
        for dir_name in required_dirs:
            path = self.root / dir_name
            if path.exists() and path.is_dir():
                self.add_result(True, f"{dir_name}/ exists", path)
            else:
                self.add_result(False, f"{dir_name}/ missing", path)
    
    def validate_skills_structure(self) -> None:
        """Validate all skills have correct structure."""
        print("\n📚 Checking skills structure...")
        
        skills_path = self.root / "skills"
        if not skills_path.exists():
            self.add_result(False, "skills directory missing", skills_path)
            return
        
        # Count skills
        skill_count = 0
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                skill_count += 1
                self.validate_single_skill(skill_dir)
        
        print(f"   Found {skill_count} skills")
        self.add_result(True, f"Total skills: {skill_count}", skills_path)
    
    def validate_single_skill(self, skill_path: Path) -> None:
        """Validate a single skill directory."""
        # Check for GROK.md
        grok_file = skill_path / "GROK.md"
        if grok_file.exists():
            self.add_result(True, "GROK.md exists", grok_file)
        else:
            self.add_result(False, "GROK.md missing", grok_file)
        
        # Check for resources directory
        resources_path = skill_path / "resources"
        if resources_path.exists() and resources_path.is_dir():
            self.add_result(True, "resources/ exists", resources_path)
            
            # Check for Python files
            python_files = list(resources_path.glob("*.py"))
            if python_files:
                self.add_result(True, f"Python files: {len(python_files)}", resources_path)
            else:
                self.add_result(False, "No Python files in resources/", resources_path)
        else:
            self.add_result(False, "resources/ missing", resources_path)
    
    def validate_agents_structure(self) -> None:
        """Validate all agents have correct structure."""
        print("\n🤖 Checking agents structure...")
        
        agents_path = self.root / "agents"
        if not agents_path.exists():
            self.add_result(False, "agents directory missing", agents_path)
            return
        
        # Count agents
        agent_count = 0
        for agent_dir in agents_path.iterdir():
            if agent_dir.is_dir():
                agent_count += 1
                self.validate_single_agent(agent_dir)
        
        print(f"   Found {agent_count} agents")
        self.add_result(True, f"Total agents: {agent_count}", agents_path)
    
    def validate_single_agent(self, agent_path: Path) -> None:
        """Validate a single agent directory."""
        # Check for GROK.md
        grok_file = agent_path / "GROK.md"
        if grok_file.exists():
            self.add_result(True, "GROK.md exists", grok_file)
        else:
            self.add_result(False, "GROK.md missing", grok_file)
        
        # Check for agent.py
        agent_file = agent_path / "agent.py"
        if agent_file.exists():
            self.add_result(True, "agent.py exists", agent_file)
        else:
            self.add_result(False, "agent.py missing", agent_file)
    
    def validate_templates(self) -> None:
        """Validate template files."""
        print("\n📋 Checking templates...")
        
        templates_path = self.root / "templates"
        if not templates_path.exists():
            self.add_result(False, "templates directory missing", templates_path)
            return
        
        required_templates = [
            "skill-template.md",
            "agent-template.md",
            "project-GROK.md"
        ]
        
        for template in required_templates:
            template_path = templates_path / template
            if template_path.exists():
                self.add_result(True, f"{template} exists", template_path)
            else:
                self.add_result(False, f"{template} missing", template_path)
    
    def validate_scripts(self) -> None:
        """Validate script files."""
        print("\n🔧 Checking scripts...")
        
        scripts_path = self.root / "scripts"
        if not scripts_path.exists():
            self.add_result(False, "scripts directory missing", scripts_path)
            return
        
        script_files = list(scripts_path.glob("*.py"))
        if script_files:
            self.add_result(True, f"Scripts found: {len(script_files)}", scripts_path)
        else:
            self.add_result(False, "No Python scripts", scripts_path)
    
    def add_result(self, passed: bool, message: str, path: Path) -> None:
        """Add a validation result."""
        self.results.append(ValidationResult(passed, message, path))
    
    def print_summary(self) -> None:
        """Print validation summary."""
        print("\n" + "=" * 60)
        print("  VALIDATION SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)
        
        print(f"\nTotal checks: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        
        if failed > 0:
            print("\n❌ Failed checks:")
            for result in self.results:
                if not result.passed:
                    print(f"   - {result.message}")
                    print(f"     Path: {result.path}")
        
        print("\n" + "=" * 60)
        
        if failed == 0:
            print("  🎉 All validations passed!")
        else:
            print(f"  ⚠️  {failed} validation(s) need attention")
        
        print("=" * 60 + "\n")
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate a validation report."""
        return {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "total_checks": len(self.results),
            "passed": sum(1 for r in self.results if r.passed),
            "failed": sum(1 for r in self.results if not r.passed),
            "results": [
                {
                    "passed": r.passed,
                    "message": r.message,
                    "path": str(r.path)
                }
                for r in self.results
            ]
        }


def main() -> int:
    """Main function."""
    # Determine root path
    if len(sys.argv) > 1:
        root_path = Path(sys.argv[1]).resolve()
    else:
        root_path = Path(__file__).parent.parent.resolve()
    
    # Create validator
    validator = RepositoryValidator(root_path)
    
    # Run validation
    all_passed = validator.validate_all()
    
    # Print summary
    validator.print_summary()
    
    # Generate report
    report = validator.generate_report()
    report_path = root_path / "validation_report.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"📊 Report saved to: {report_path}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
