---
name: Project GROK.md Template
category: templates
difficulty: beginner
time_estimate: "30 minutes"
dependencies: []
tags: ["template", "project-setup", "grok-integration"]
grok_personality: "project-architect"
description: "Base project memory file template for initializing new Grok-powered projects"
---

# Project GROK.md Template

## Project Information

```yaml
project:
  name: ""
  description: ""
  version: "0.1.0"
  author: ""
  created_at: ""
  last_updated: ""
  
grok_integration:
  personality_type: ""
  primary_skills: []
  secondary_skills: []
  custom_prompts: []
  
domain:
  industry: ""
  target_audience: ""
  business_model: ""
  success_metrics: []
```

## Technology Stack

```yaml
tech_stack:
  frontend:
    framework: ""
    ui_library: ""
    state_management: ""
    build_tools: []
  
  backend:
    language: ""
    framework: ""
    database: ""
    cache: ""
    deployment: ""
  
  development:
    testing: []
    linting: []
    ci_cd: []
    monitoring: []
```

## Project Structure

```
project_name/
├── docs/                   # Documentation
├── src/                    # Source code
├── tests/                  # Test files
├── scripts/                # Build/deployment scripts
├── .github/                # GitHub workflows
├── .env.example           # Environment variables template
├── README.md              # Project README
├── package.json           # Dependencies (if applicable)
└── GROK.md               # This file
```

## Development Workflow

### 1. Setup Instructions

```bash
# Clone and setup
git clone <repository_url>
cd <project_name>

# Install dependencies
npm install  # Node.js
# OR
pip install -r requirements.txt  # Python

# Configure environment
cp .env.example .env
# Edit .env with your values

# Run development server
npm run dev  # Node.js
# OR
python -m uvicorn main:app --reload  # Python FastAPI
```

### 2. Development Commands

```yaml
commands:
  start: ""
  test: ""
  lint: ""
  build: ""
  deploy: ""
  
database:
  migrate: ""
  seed: ""
  reset: ""
```

## Grok Integration

### 1. Active Skills

```yaml
active_skills:
  - skill_name: ""
    enabled: true
    configuration: {}
    custom_rules: []
  
  - skill_name: ""
    enabled: false
    reason: "Not needed for current scope"
```

### 2. Custom Prompts

```yaml
custom_prompts:
  code_review: |
    Review this code for:
    1. Performance optimizations
    2. Security vulnerabilities
    3. Code quality issues
    4. Best practices adherence
    Provide specific, actionable feedback.
  
  architecture_decision: |
    Analyze this architectural decision:
    1. Scalability implications
    2. Maintenance considerations
    3. Trade-offs involved
    4. Alternative approaches
    Provide recommendation with rationale.
  
  feature_planning: |
    Plan the implementation of this feature:
    1. Break down into technical tasks
    2. Identify dependencies
    3. Estimate effort
    4. Define acceptance criteria
    5. Consider edge cases
```

### 3. Project-Specific Rules

```yaml
project_rules:
  coding_standards:
    - "Use TypeScript for type safety"
    - "Follow ES6+ conventions"
    - "Implement comprehensive error handling"
    - "Write tests for all public methods"
  
  architecture_patterns:
    - "Prefer composition over inheritance"
    - "Implement dependency injection"
    - "Use repository pattern for data access"
    - "Apply single responsibility principle"
  
  security_requirements:
    - "Validate all inputs"
    - "Sanitize all outputs"
    - "Implement proper authentication"
    - "Use HTTPS for all communications"
```

## Quality Gates

### 1. Code Quality

```yaml
quality_gates:
  code_coverage:
    minimum: "80%"
    files_to_exclude: ["*.test.*", "*.spec.*"]
  
  performance:
    load_time: "< 2 seconds"
    api_response: "< 500ms"
    memory_usage: "< 512MB"
  
  security:
    vulnerability_scan: "Zero high/critical issues"
    dependency_audit: "All dependencies up-to-date"
    code_analysis: "No security warnings"
```

### 2. Testing Strategy

```yaml
testing_strategy:
  unit_tests:
    framework: ""
    coverage_target: "80%"
    test_patterns: ["*.test.*", "*.spec.*"]
  
  integration_tests:
    scope: ["API endpoints", "Database operations"]
    framework: ""
  
  e2e_tests:
    scope: ["Critical user journeys"]
    framework: ""
    environment: "staging"
```

## Deployment Strategy

### 1. Environments

```yaml
environments:
  development:
    url: ""
    description: "Local development environment"
    auto_deploy: false
  
  staging:
    url: ""
    description: "Pre-production testing environment"
    auto_deploy: true
  
  production:
    url: ""
    description: "Live production environment"
    auto_deploy: false
    requires_approval: true
```

### 2. CI/CD Pipeline

```yaml
ci_cd:
  triggers: ["push", "pull_request"]
  
  stages:
    - name: "lint"
      command: "npm run lint"
      fail_fast: true
    
    - name: "test"
      command: "npm run test"
      coverage: true
    
    - name: "build"
      command: "npm run build"
      artifacts: ["dist/"]
    
    - name: "security_scan"
      command: "npm audit"
      fail_on_vulnerabilities: true
    
    - name: "deploy_staging"
      condition: "branch == develop"
      command: "deploy.sh staging"
    
    - name: "deploy_production"
      condition: "branch == main"
      command: "deploy.sh production"
      requires_approval: true
```

## Monitoring and Observability

### 1. Metrics to Track

```yaml
metrics:
  performance:
    - "Response time"
    - "Throughput"
    - "Error rate"
    - "Resource utilization"
  
  business:
    - "User engagement"
    - "Conversion rate"
    - "Revenue impact"
    - "Feature adoption"
  
  operations:
    - "Uptime"
    - "Deployment frequency"
    - "Mean time to recovery"
    - "Change failure rate"
```

### 2. Alerting Rules

```yaml
alerts:
  critical:
    - "Service down"
    - "Error rate > 5%"
    - "Response time > 5s"
  
  warning:
    - "Memory usage > 80%"
    - "CPU usage > 80%"
    - "Disk space > 90%"
```

## Documentation Requirements

### 1. Required Documentation

```yaml
documentation:
  user_facing:
    - "README.md with setup instructions"
    - "API documentation (if applicable)"
    - "User guide (if applicable)"
  
  developer_facing:
    - "Architecture documentation"
    - "Development setup guide"
    - "Contributing guidelines"
    - "Code style guide"
  
  operational:
    - "Deployment guide"
    - "Monitoring setup"
    - "Troubleshooting guide"
    - "Disaster recovery plan"
```

## Risk Management

### 1. Known Risks

```yaml
risks:
  technical:
    - risk: "Third-party dependency failure"
      impact: "High"
      probability: "Medium"
      mitigation: "Fallback implementations"
    
    - risk: "Database performance bottleneck"
      impact: "High"
      probability: "Low"
      mitigation: "Database optimization plan"
  
  business:
    - risk: "Feature scope creep"
      impact: "Medium"
      probability: "High"
      mitigation: "Strict change control process"
```

## Success Criteria

### 1. Technical Success Metrics

```yaml
technical_success:
  performance:
    - "All response times under 2s"
    - "99.9% uptime"
    - "Zero critical security vulnerabilities"
  
  quality:
    - "Code coverage above 80%"
    - "Zero critical bugs in production"
    - "All features fully documented"
  
  scalability:
    - "Handle 10x current load"
    - "Deploy to additional regions"
    - "Support horizontal scaling"
```

### 2. Business Success Metrics

```yaml
business_success:
  user_satisfaction:
    - "NPS score > 8"
    - "User retention > 80%"
    - "Support tickets < 5% of users"
  
  business_objectives:
    - "Revenue target met"
    - "Market share achieved"
    - "Customer acquisition cost within budget"
```

## Project Evolution

### 1. Planned Enhancements

```yaml
future_roadmap:
  next_release:
    - "Feature A implementation"
    - "Performance optimization"
    - "Security enhancements"
  
  future_quarter:
    - "Advanced feature B"
    - "Mobile application"
    - "Advanced analytics"
  
  long_term:
    - "Machine learning integration"
    - "Global expansion"
    - "Enterprise features"
```

### 2. Technology Migration Plan

```yaml
technology_evolution:
  planned_upgrades:
    - dependency: "React"
      current_version: "18.x"
      target_version: "19.x"
      timeline: "Q2 2024"
      risk: "Low"
    
    - dependency: "PostgreSQL"
      current_version: "14.x"
      target_version: "16.x"
      timeline: "Q3 2024"
      risk: "Medium"
```

## Team Guidelines

### 1. Collaboration Rules

```yaml
collaboration:
  code_review:
    required_reviewers: 2
    auto_assign: true
    approval_requirements: ["One senior dev"]
  
  communication:
    slack_channels: ["#dev", "#announcements"]
    standup_schedule: "Daily 9:00 AM"
    sprint_planning: "Bi-weekly Monday"
  
  issue_tracking:
    bug_severity_levels: ["Critical", "High", "Medium", "Low"]
    feature_priority_levels: ["Must-have", "Should-have", "Nice-to-have"]
    sprint_size: "2 weeks"
```

## Learning and Improvement

### 1. Knowledge Sharing

```yaml
knowledge_sharing:
  code_reviews: "Focus on learning, not just approval"
  documentation: "Document decisions and trade-offs"
  retrospectives: "Identify improvement opportunities"
  
  training:
    new_technologies: "Quarterly tech talks"
    best_practices: "Monthly code review sessions"
    domain_knowledge: "Bi-weekly product demos"
```

### 2. Continuous Improvement

```yaml
continuous_improvement:
  metrics_tracking:
    - "Velocity trends"
    - "Bug discovery rates"
    - "Technical debt indicators"
    - "Team satisfaction"
  
  improvement_process:
    1. "Collect metrics and feedback"
    2. "Identify improvement areas"
    3. "Define action items"
    4. "Implement changes"
    5. "Measure impact"
    6. "Iterate"
```

## Custom Notes

```markdown
## Project-Specific Notes

Add any project-specific information, constraints, or special considerations here:

### Special Requirements
- [ ] List any special requirements
- [ ] Compliance requirements
- [ ] Industry-specific constraints

### Known Limitations
- [ ] Current technical limitations
- [ ] Resource constraints
- [ ] Timeline constraints

### Important Decisions
- [ ] Record key architectural decisions
- [ ] Note rejected alternatives
- [ ] Document rationale
```

---

## How to Use This Template

1. **Copy and Customize**: Duplicate this file and customize for your specific project
2. **Update YAML Sections**: Fill in the YAML blocks with your project details
3. **Add Custom Rules**: Add project-specific coding rules and guidelines
4. **Configure Grok Integration**: Set up the skills and prompts that Grok should use
5. **Reference During Development**: Keep this file handy for quick reference
6. **Update Regularly**: Keep the file updated as the project evolves

## Integration with Awesome Grok Skills

This template is designed to work seamlessly with the skills in this repository:

- Use `tdd` skill for testing strategy
- Use `nextjs-fullstack` for web applications
- Use `supabase-auth` for authentication
- Use `real-time-research` for market validation
- Use `physics-simulation` for computational projects

The skills can be automatically integrated by updating the `active_skills` section with the appropriate skill configurations.