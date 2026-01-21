# Global Skills Installation Guide

## Overview

This guide explains how to install and integrate Awesome Grok Skills into your local Grok environment for seamless access across all your projects.

## Installation Methods

### 1. Symlink Method (Recommended)

Create symlinks from your Grok skills directory to this repository:

```bash
# Navigate to your Grok skills directory
cd ~/.grok/skills/

# Create symlinks for skill categories
ln -s /path/to/awesome-grok-skills/skills/core ./core
ln -s /path/to/awesome-grok-skills/skills/web-dev ./web-dev
ln -s /path/to/awesome-grok-skills/skills/mobile ./mobile
ln -s /path/to/awesome-grok-skills/skills/backend ./backend
ln -s /path/to/awesome-grok-skills/skills/security ./security
ln -s /path/to/awesome-grok-skills/skills/data-science ./data-science
ln -s /path/to/awesome-grok-skills/skills/indie-hacker ./indie-hacker
ln -s /path/to/awesome-grok-skills/skills/devops ./devops

# Create symlinks for agents
ln -s /path/to/awesome-grok-skills/agents ./agents

# Create symlink for templates
ln -s /path/to/awesome-grok-skills/templates ./templates
```

### 2. Clone Method

Clone the repository directly into your Grok skills directory:

```bash
# Navigate to your Grok skills directory
cd ~/.grok/

# Clone the repository
git clone https://github.com/your-username/awesome-grok-skills.git skills

# The skills will be available as:
# ~/.grok/skills/skills/core/tdd/GROK.md
# ~/.grok/skills/skills/web-dev/nextjs-fullstack/GROK.md
# etc.
```

### 3. Copy Method

Copy the skills to your Grok environment:

```bash
# Navigate to your Grok skills directory
cd ~/.grok/skills/

# Copy core skills
cp -r /path/to/awesome-grok-skills/skills/core ./
cp -r /path/to/awesome-grok-skills/skills/web-dev ./
cp -r /path/to/awesome-grok-skills/skills/mobile ./
cp -r /path/to/awesome-grok-skills/skills/backend ./

# Copy agents
cp -r /path/to/awesome-grok-skills/agents ./

# Copy templates
cp -r /path/to/awesome-grok-skills/templates ./
```

## Verification

After installation, verify the skills are accessible:

```bash
# List available skills
ls -la ~/.grok/skills/

# Check a specific skill
cat ~/.grok/skills/core/tdd/GROK.md | head -10

# Verify agents
ls -la ~/.grok/agents/
```

## Skill Structure

Each skill follows this structure:

```
skill-category/
├── skill-name/
│   ├── GROK.md              # Main skill definition
│   ├── resources/           # Optional resources and examples
│   │   ├── examples.md
│   │   └── templates/
│   └── scripts/             # Optional helper scripts
│       ├── setup.sh
│       └── validate.sh
```

## Configuration

### 1. Environment Variables

Add to your shell profile (`.bashrc`, `.zshrc`, etc.):

```bash
export GROK_SKILLS_PATH="$HOME/.grok/skills"
export GROK_AGENTS_PATH="$HOME/.grok/agents"
export GROK_TEMPLATES_PATH="$HOME/.grok/templates"
```

### 2. Grok Configuration

If Grok uses a configuration file, add:

```yaml
# ~/.grok/config.yaml
skills_directory: ~/.grok/skills
agents_directory: ~/.grok/agents
templates_directory: ~/.grok/templates

# Default skill to use
default_skill: "core/tdd"

# Agent configurations
agents:
  full_stack_planner:
    path: "agents/full-stack-planner/GROK.md"
    enabled: true
  code_review_team:
    path: "agents/code-review-team/GROK.md"
    enabled: true
```

## Usage Examples

### Using Skills

```bash
# Use TDD skill for a project
grok --skill core/tdd --project ./my-app

# Use Next.js fullstack skill
grok --skill web-dev/nextjs-fullstack --project ./next-app

# Use multiple skills
grok --skill core/tdd --skill web-dev/supabase-auth --project ./app
```

### Using Agents

```bash
# Use full-stack planner for project architecture
grok --agent full-stack-planner --requirements ./requirements.md

# Use code review team for code quality
grok --agent code-review-team --source ./src/

# Use market research oracle for validation
grok --agent market-research-oracle --idea "AI-powered calendar"
```

### Using Templates

```bash
# Create new project with template
grok --template project-GROK.md --project ./new-project

# Initialize with specific skills
grok --template project-GROK.md --skills core/tdd,web-dev/nextjs-fullstack --project ./app
```

## Updates and Maintenance

### Updating Skills

```bash
# Navigate to the repository
cd ~/.grok/skills || cd /path/to/awesome-grok-skills

# Pull latest changes
git pull origin main

# If using symlinks, no additional steps needed
# If using copy/clone, re-run installation
```

### Adding Custom Skills

1. Create new skill directory:
```bash
mkdir -p ~/.grok/skills/custom/my-skill
```

2. Create GROK.md with proper frontmatter
3. Add resources and scripts as needed
4. Update skill registry if applicable

### Contributing Back

When you improve skills:

```bash
# Fork the repository
# Create feature branch
git checkout -b feature/my-improvement

# Make your changes
git add .
git commit -m "Add my improvement"

# Push and create pull request
git push origin feature/my-improvement
```

## Troubleshooting

### Common Issues

1. **Skills not found**
   - Verify symlink paths are correct
   - Check permissions on skill files
   - Ensure Grok is looking in the right directory

2. **Permission errors**
   ```bash
   chmod -R 755 ~/.grok/skills
   chmod -R 755 ~/.grok/agents
   chmod -R 755 ~/.grok/templates
   ```

3. **Path issues**
   - Use absolute paths in symlinks
   - Update environment variables
   - Restart your shell after changes

### Debug Mode

Enable debug logging:

```bash
export GROK_DEBUG=1
grok --skill core/tdd --debug
```

## Integration with IDEs

### VS Code

Install Grok extension and configure:

```json
{
  "grok.skillsPath": "~/.grok/skills",
  "grok.agentsPath": "~/.grok/agents",
  "grok.templatesPath": "~/.grok/templates",
  "grok.defaultSkill": "core/tdd"
}
```

### Vim/Neovim

Add to your configuration:

```vim
" ~/.vimrc or ~/.config/nvim/init.vim
let g:grok_skills_path = expand('~/.grok/skills')
let g:grok_agents_path = expand('~/.grok/agents')
```

## Performance Optimization

### Caching Skills

Enable skill caching for faster access:

```yaml
# ~/.grok/config.yaml
cache:
  enabled: true
  directory: ~/.grok/cache
  ttl: 3600  # 1 hour
```

### Lazy Loading

Configure skills to load on demand:

```yaml
# ~/.grok/config.yaml
lazy_loading: true
preload_skills: ["core/tdd", "web-dev/nextjs-fullstack"]
```

## Team Setup

### Shared Skills Repository

For teams, set up a shared skills repository:

1. Create organization repository
2. Install via organization's Git host
3. Configure team members with same setup

### Standardized Templates

Create team-specific templates:

```bash
mkdir -p ~/.grok/templates/team
# Add team-specific templates
```

## Backup and Recovery

### Backup Configuration

```bash
# Create backup script
cat > ~/.grok/backup.sh << 'EOF'
#!/bin/bash
backup_dir="$HOME/.grok-backup-$(date +%Y%m%d)"
mkdir -p "$backup_dir"

cp -r ~/.grok/skills "$backup_dir/"
cp -r ~/.grok/agents "$backup_dir/"
cp -r ~/.grok/templates "$backup_dir/"
cp ~/.grok/config.yaml "$backup_dir/" 2>/dev/null || true

echo "Backup created: $backup_dir"
EOF

chmod +x ~/.grok/backup.sh
```

### Restore Configuration

```bash
# Restore from backup
backup_dir="$HOME/.grok-backup-YYYYMMDD"
cp -r "$backup_dir/skills" ~/.grok/
cp -r "$backup_dir/agents" ~/.grok/
cp -r "$backup_dir/templates" ~/.grok/
cp "$backup_dir/config.yaml" ~/.grok/" 2>/dev/null || true
```

## Advanced Configuration

### Skill Chains

Configure skills to work in sequence:

```yaml
# ~/.grok/skill-chains.yaml
fullstack_development:
  - core/tdd
  - web-dev/nextjs-fullstack
  - web-dev/supabase-auth
  - backend/fastapi-best-practices

mobile_app:
  - core/tdd
  - mobile/expo-react-native
  - web-dev/supabase-auth
```

### Conditional Skills

Load skills based on project type:

```yaml
# ~/.grok/conditional-skills.yaml
project_types:
  webapp:
    - web-dev/nextjs-fullstack
    - web-dev/tailwind-shadcn
    - web-dev/supabase-auth
  
  mobileapp:
    - mobile/expo-react-native
    - web-dev/supabase-auth
  
  api:
    - backend/fastapi-best-practices
    - core/tdd
```

## Community Resources

- **GitHub Repository**: https://github.com/your-username/awesome-grok-skills
- **Discord Community**: [Join our Discord]
- **Documentation**: https://awesome-grok-skills.docs.com
- **Video Tutorials**: [YouTube Channel]

## Support

For issues and questions:

1. Check the [FAQ](https://github.com/your-username/awesome-grok-skills/wiki/FAQ)
2. Search existing [issues](https://github.com/your-username/awesome-grok-skills/issues)
3. Create a [new issue](https://github.com/your-username/awesome-grok-skills/issues/new)
4. Join our [Discord community](https://discord.gg/your-server)

---

By following this guide, you'll have the Awesome Grok Skills seamlessly integrated into your development workflow, enabling you to leverage Grok's full potential across all your projects.