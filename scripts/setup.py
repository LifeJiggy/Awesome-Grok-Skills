#!/usr/bin/env python3
"""
Setup Script for Awesome Grok Skills

This script sets up the development environment and creates necessary symlinks.
"""

import os
import sys
import shutil
from pathlib import Path


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def print_step(step: str) -> None:
    """Print a step indicator."""
    print(f"📦 {step}...")


def print_success(text: str) -> None:
    """Print a success message."""
    print(f"✅ {text}")


def print_warning(text: str) -> None:
    """Print a warning message."""
    print(f"⚠️  {text}")


def print_error(text: str) -> None:
    """Print an error message."""
    print(f"❌ {text}")


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.resolve()


def check_python_version() -> bool:
    """Check if Python version is sufficient."""
    print_step("Checking Python version")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} ✓")
        return True
    else:
        print_error(f"Python 3.9+ required, found {version.major}.{version.minor}")
        return False


def create_virtual_environment(venv_path: Path) -> bool:
    """Create a virtual environment."""
    print_step(f"Creating virtual environment at {venv_path}")
    
    try:
        import venv
        venv.create(venv_path, with_pip=True)
        print_success("Virtual environment created")
        return True
    except ImportError:
        print_warning("venv module not available, skipping virtual environment")
        return True


def install_dependencies(venv: bool = True) -> bool:
    """Install project dependencies."""
    print_step("Installing dependencies")
    
    project_root = get_project_root()
    requirements_file = project_root / "requirements.txt"
    dev_requirements_file = project_root / "requirements-dev.txt"
    
    if venv:
        python_path = project_root / "venv" / "Scripts" / "python.exe" if sys.platform == "win32" else project_root / "venv" / "bin" / "python"
        pip_cmd = [str(python_path), "-m", "pip"]
    else:
        pip_cmd = [sys.executable, "-m", "pip"]
    
    try:
        # Install base requirements
        if requirements_file.exists():
            print("  Installing base requirements...")
            os.system(" ".join(pip_cmd + ["install", "-r", str(requirements_file)]))
        
        # Install dev requirements
        if dev_requirements_file.exists():
            print("  Installing development requirements...")
            os.system(" ".join(pip_cmd + ["install", "-r", str(dev_requirements_file), "-q"]))
        
        print_success("Dependencies installed")
        return True
    except Exception as e:
        print_error(f"Failed to install dependencies: {e}")
        return False


def create_symlinks() -> bool:
    """Create symlinks for skills and agents."""
    print_step("Creating symlinks")
    
    project_root = get_project_root()
    skills_dir = project_root / "skills"
    agents_dir = project_root / "agents"
    templates_dir = project_root / "templates"
    
    # Determine Grok config directory
    if sys.platform == "win32":
        grok_dir = Path.home() / ".grok"
    else:
        grok_dir = Path.home() / ".config" / "grok"
    
    try:
        # Create .grok directory if it doesn't exist
        grok_dir.mkdir(parents=True, exist_ok=True)
        print(f"  Created {grok_dir}")
        
        # Create skills symlink
        skills_link = grok_dir / "skills"
        if skills_link.exists() or skills_link.is_symlink():
            if skills_link.is_symlink():
                skills_link.unlink()
            elif skills_link.exists():
                print_warning(f"skills link exists but is not a symlink at {skills_link}")
        else:
            skills_link.symlink_to(skills_dir)
            print_success(f"Linked skills: {skills_dir}")
        
        # Create agents symlink
        agents_link = grok_dir / "agents"
        if agents_link.exists() or agents_link.is_symlink():
            if agents_link.is_symlink():
                agents_link.unlink()
            else:
                print_warning(f"agents link exists but is not a symlink at {agents_link}")
        else:
            agents_link.symlink_to(agents_dir)
            print_success(f"Linked agents: {agents_dir}")
        
        # Create templates symlink
        templates_link = grok_dir / "templates"
        if templates_link.exists() or templates_link.is_symlink():
            if templates_link.is_symlink():
                templates_link.unlink()
            else:
                print_warning(f"templates link exists but is not a symlink at {templates_link}")
        else:
            templates_link.symlink_to(templates_dir)
            print_success(f"Linked templates: {templates_dir}")
        
        return True
    except Exception as e:
        print_error(f"Failed to create symlinks: {e}")
        return False


def setup_precommit() -> bool:
    """Setup pre-commit hooks."""
    print_step("Setting up pre-commit hooks")
    
    try:
        import pre_commit
        os.system("pre-commit install")
        print_success("Pre-commit hooks installed")
        return True
    except ImportError:
        print_warning("pre-commit not installed, skipping")
        return True


def verify_installation() -> bool:
    """Verify the installation was successful."""
    print_step("Verifying installation")
    
    project_root = get_project_root()
    
    checks = [
        ("Skills directory", (project_root / "skills").exists()),
        ("Agents directory", (project_root / "agents").exists()),
        ("Templates directory", (project_root / "templates").exists()),
        ("Scripts directory", (project_root / "scripts").exists()),
    ]
    
    all_passed = True
    for name, check in checks:
        if check:
            print_success(f"  {name} exists")
        else:
            print_error(f"  {name} missing")
            all_passed = False
    
    return all_passed


def print_summary() -> None:
    """Print installation summary."""
    print_header("Setup Complete! 🎉")
    
    project_root = get_project_root()
    
    print("📁 Project Structure:")
    print(f"   Root: {project_root}")
    print(f"   Skills: {project_root / 'skills'}")
    print(f"   Agents: {project_root / 'agents'}")
    print(f"   Templates: {project_root / 'templates'}")
    
    print("\n🚀 Next Steps:")
    print("   1. Activate virtual environment (if created):")
    if sys.platform == "win32":
        print(f"      {project_root / 'venv' / 'Scripts' / 'activate'}")
    else:
        print(f"      source {project_root / 'venv' / 'bin' / 'activate'}")
    
    print("\n   2. Run tests:")
    print("      python -m pytest tests/ -v")
    
    print("\n   3. Start development!")
    
    print("\n📚 Documentation:")
    print("   - CONTRIBUTING.md: Contribution guidelines")
    print("   - STYLE_GUIDE.md: Code style guide")
    print("   - TESTING_GUIDE.md: Testing standards")
    print("   - DEPLOYMENT.md: Deployment guide")


def main() -> int:
    """Main setup function."""
    print_header("Awesome Grok Skills Setup")
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Create virtual environment
    if "--no-venv" not in sys.argv:
        venv_path = get_project_root() / "venv"
        create_virtual_environment(venv_path)
    
    # Install dependencies
    install_dependencies(venv="--no-venv" not in sys.argv)
    
    # Create symlinks
    create_symlinks()
    
    # Setup pre-commit
    if "--no-precommit" not in sys.argv:
        setup_precommit()
    
    # Verify installation
    verify_installation()
    
    # Print summary
    print_summary()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
