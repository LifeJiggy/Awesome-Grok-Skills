#!/bin/bash

# Awesome Grok Skills Setup Script
# This script installs the skill library into your Grok environment

set -e

echo "🚀 Setting up Awesome Grok Skills..."

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "skills" ]; then
    print_error "Please run this script from the awesome-grok-skills repository root"
    exit 1
fi

# Get the absolute path of the repository
REPO_ROOT=$(pwd)
print_status "Repository root: $REPO_ROOT"

# Determine Grok skills directory
GROK_DIR="$HOME/.grok"
if [ -n "$GROK_SKILLS_PATH" ]; then
    GROK_DIR=$(dirname "$GROK_SKILLS_PATH")
fi

print_status "Grok directory: $GROK_DIR"

# Create Grok directories if they don't exist
mkdir -p "$GROK_DIR/skills"
mkdir -p "$GROK_DIR/agents"
mkdir -p "$GROK_DIR/templates"

print_status "Created Grok directories"

# Function to create symlink
create_symlink() {
    local source="$1"
    local target="$2"
    local description="$3"
    
    if [ -L "$target" ]; then
        print_warning "Symlink already exists for $description, removing..."
        rm "$target"
    elif [ -e "$target" ]; then
        print_error "Target exists for $description but is not a symlink: $target"
        return 1
    fi
    
    ln -s "$source" "$target"
    print_success "Linked $description"
}

# Create symlinks for skill categories
print_status "Creating skill symlinks..."

create_symlink "$REPO_ROOT/skills/core" "$GROK_DIR/skills/core" "Core Skills"
create_symlink "$REPO_ROOT/skills/web-dev" "$GROK_DIR/skills/web-dev" "Web Development Skills"
create_symlink "$REPO_ROOT/skills/mobile" "$GROK_DIR/skills/mobile" "Mobile Development Skills"
create_symlink "$REPO_ROOT/skills/backend" "$GROK_DIR/skills/backend" "Backend Development Skills"
create_symlink "$REPO_ROOT/skills/security" "$GROK_DIR/skills/security" "Security Skills"
create_symlink "$REPO_ROOT/skills/data-science" "$GROK_DIR/skills/data-science" "Data Science Skills"
create_symlink "$REPO_ROOT/skills/indie-hacker" "$GROK_DIR/skills/indie-hacker" "Indie Hacker Skills"
create_symlink "$REPO_ROOT/skills/devops" "$GROK_DIR/skills/devops" "DevOps Skills"
create_symlink "$REPO_ROOT/skills/crypto-web3" "$GROK_DIR/skills/crypto-web3" "Crypto/Web3 Skills"

# Create symlink for agents
create_symlink "$REPO_ROOT/agents" "$GROK_DIR/agents" "Agents"

# Create symlink for templates
create_symlink "$REPO_ROOT/templates" "$GROK_DIR/templates" "Templates"

# Set up environment variables
print_status "Setting up environment variables..."

# Update shell configuration
update_shell_config() {
    local config_file="$1"
    
    if [ -f "$config_file" ]; then
        # Remove old entries
        sed -i.tmp '/# Awesome Grok Skills/,/^$/d' "$config_file" 2>/dev/null || true
        rm -f "$config_file.tmp"
        
        # Add new entries
        cat >> "$config_file" << 'EOF'

# Awesome Grok Skills
export GROK_SKILLS_PATH="$HOME/.grok/skills"
export GROK_AGENTS_PATH="$HOME/.grok/agents"
export GROK_TEMPLATES_PATH="$HOME/.grok/templates"
export PATH="$PATH:$HOME/.grok/scripts"

EOF
        print_success "Updated $config_file"
    fi
}

# Update common shell configs
for config in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
    if [ -f "$config" ]; then
        update_shell_config "$config"
    fi
done

# Create Grok config if it doesn't exist
GROK_CONFIG="$GROK_DIR/config.yaml"
if [ ! -f "$GROK_CONFIG" ]; then
    print_status "Creating Grok configuration file..."
    
    cat > "$GROK_CONFIG" << 'EOF'
# Awesome Grok Skills Configuration
skills_directory: ~/.grok/skills
agents_directory: ~/.grok/agents
templates_directory: ~/.grok/templates

# Default skills to use
default_skill: "core/tdd"

# Cache configuration
cache:
  enabled: true
  directory: ~/.grok/cache
  ttl: 3600  # 1 hour

# Enabled agents
agents:
  full_stack_planner:
    path: "agents/full-stack-planner/GROK.md"
    enabled: true
  code_review_team:
    path: "agents/code-review-team/GROK.md"
    enabled: true
  market_research_oracle:
    path: "agents/market-research-oracle/GROK.md"
    enabled: true

# Skill chains for common workflows
skill_chains:
  fullstack_web_app:
    - "core/tdd"
    - "web-dev/nextjs-fullstack"
    - "web-dev/supabase-auth"
  
  mobile_app:
    - "core/tdd"
    - "mobile/expo-react-native"
    - "web-dev/supabase-auth"
  
  api_backend:
    - "core/tdd"
    - "backend/fastapi-best-practices"
    - "security/vuln-audit-grok"
EOF
    print_success "Created Grok configuration file"
fi

# Create cache directory
mkdir -p "$GROK_DIR/cache"

# Create scripts directory and symlink setup scripts
mkdir -p "$GROK_DIR/scripts"
ln -sf "$REPO_ROOT/scripts/validate.sh" "$GROK_DIR/scripts/validate" 2>/dev/null || true
ln -sf "$REPO_ROOT/scripts/setup.sh" "$GROK_DIR/scripts/setup" 2>/dev/null || true

# Test installation
print_status "Testing installation..."

if [ -f "$GROK_DIR/skills/core/tdd/GROK.md" ]; then
    print_success "Core skills are accessible"
else
    print_error "Core skills not accessible"
    exit 1
fi

if [ -f "$GROK_DIR/agents/full-stack-planner/GROK.md" ]; then
    print_success "Agents are accessible"
else
    print_error "Agents not accessible"
    exit 1
fi

if [ -f "$GROK_DIR/templates/project-GROK.md" ]; then
    print_success "Templates are accessible"
else
    print_error "Templates not accessible"
    exit 1
fi

# Completion message
echo ""
echo "🎉 Installation completed successfully!"
echo ""
print_success "Awesome Grok Skills has been installed to your Grok environment"

echo ""
echo "📁 Installed Components:"
echo "  Skills: $GROK_DIR/skills/"
echo "  Agents: $GROK_DIR/agents/"
echo "  Templates: $GROK_DIR/templates/"
echo "  Config: $GROK_DIR/config.yaml"

echo ""
echo "🚀 Quick Start:"
echo "  1. Restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
echo "  2. Test with: grok --skill core/tdd --project ./test-project"
echo "  3. View available skills: ls -la ~/.grok/skills/"

echo ""
echo "📚 Documentation:"
echo "  - README: $REPO_ROOT/README.md"
echo "  - Contributing: $REPO_ROOT/CONTRIBUTING.md"
echo "  - Global Install Guide: $REPO_ROOT/templates/global-skills-install.md"

echo ""
echo "💬 Need Help?"
echo "  - Discord: https://discord.gg/grok-skills"
echo "  - GitHub Issues: https://github.com/your-username/awesome-grok-skills/issues"

echo ""
print_success "Enjoy building with Grok! 🤖✨"