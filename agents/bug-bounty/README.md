# BugBounty Agent

Comprehensive bug bounty program management, vulnerability triage, reward calculation, and security advisory coordination agent.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The BugBounty Agent is a comprehensive toolkit for managing bug bounty programs and security research workflows. It provides:

- **Program Manager**: Create and manage bug bounty programs with scopes and reward structures
- **Submission Triage**: Validate, assess severity, and prioritize vulnerability submissions
- **Reward Engine**: Calculate bounties based on severity, quality, and impact
- **Advisory Service**: Create and publish security advisories with CVE coordination
- **Researcher Manager**: Track researcher performance, rankings, and payment history
- **Analytics Engine**: Generate reports and insights on program effectiveness

## Features

### Program Management

- Create and configure bug bounty programs
- Define in-scope and out-of-scope targets
- Configure reward ranges by severity
- Set response and resolution timeframes
- Manage program lifecycle (draft, active, paused, archived)

### Vulnerability Triage

- Submission validation and quality checks
- CVSS-based severity assessment
- Duplicate detection using text similarity
- Priority assignment and queue management
- Triage workflow with status tracking

### Reward Calculation

- Severity-based bounty calculation
- Quality and impact multipliers
- Bonus calculations for high-quality reports
- Reward caps and minimums
- Payment processing and history

### Security Advisory

- CVE assignment and tracking
- Advisory drafting and coordination
- Coordinated disclosure timelines
- Multi-channel publication
- Stakeholder notifications

### Researcher Management

- Researcher profile management
- Performance tracking and statistics
- Rankings and leaderboards
- Payment history
- Communication management

### Analytics and Reporting

- Vulnerability trend analysis
- Researcher performance metrics
- Program effectiveness metrics
- Custom report generation
- Dashboard data export

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills/agents/bug-bounty

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from agents.bug-bounty.agent import BugBountyAgent, ProgramConfig

# Initialize agent
agent = BugBountyAgent()

# Create bug bounty program
program = agent.create_program(
    name="Web Application Security Program",
    description="Public bug bounty program for web applications",
    reward_range="100-10000",
    scope=[
        {"target": "*.example.com", "type": "domain"},
        {"target": "api.example.com", "type": "api"}
    ]
)

print(f"Program created: {program['id']}")
```

### Run Demo

```bash
python agents/bug-bounty/agent.py
```

## Installation

### Prerequisites

- Python 3.9+
- pip package manager
- Virtual environment (recommended)

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Dependencies

**Core:**
- Python 3.9+
- typing-extensions
- dataclasses
- pydantic (for validation)

**Optional:**
- fastapi (for API server)
- sqlalchemy (for database ORM)
- redis (for caching)
- celery (for task queue)
- prometheus-client (for metrics)

## Usage

### Creating a Bug Bounty Program

```python
from agents.bug-bounty.agent import BugBountyAgent

agent = BugBountyAgent()

# Define program configuration
program_config = {
    "name": "Security Bug Bounty Program",
    "description": "Bug bounty program for web and mobile applications",
    "organization": "Example Corp",
    "contact": "security@example.com",
    "reward_range": "100-50000",
    "response_time": 48,  # hours
    "resolution_time": 90,  # days
    "scope": [
        {"target": "*.example.com", "type": "domain"},
        {"target": "api.example.com", "type": "api"},
        {"target": "mobile.example.com", "type": "mobile"}
    ],
    "out_of_scope": [
        {"target": "*.test.example.com", "type": "domain"},
        {"target": "*.staging.example.com", "type": "domain"}
    ]
}

# Create program
program = agent.create_program(**program_config)
print(f"Program created with ID: {program['id']}")
```

### Submitting a Vulnerability

```python
# Researcher submits a vulnerability
submission = agent.submit_vulnerability(
    program_id=program["id"],
    researcher_id="researcher-123",
    title="SQL Injection in login form",
    description="The login form at /login is vulnerable to SQL injection...",
    severity="high",
    proof_of_concept={
        "steps": [
            "Navigate to https://example.com/login",
            "Enter SQL injection payload in username field",
            "Observe database error message"
        ],
        "payload": "' OR '1'='1 --",
        "screenshot": "screenshot.png",
        "video": "https://youtu.be/..."
    },
    target_url="https://example.com/login",
    parameter="username",
    cvss_metrics={
        "attack_vector": "network",
        "attack_complexity": "low",
        "privileges_required": "none",
        "user_interaction": "none",
        "scope": "unchanged",
        "confidentiality": "high",
        "integrity": "high",
        "availability": "high"
    }
)

print(f"Submission created: {submission['id']}")
```

### Triage Workflow

```python
# Triage the submission
triaged = agent.triage_submission(
    submission_id=submission["id"],
    validate=True,
    assess_severity=True,
    check_duplicates=True
)

print(f"Valid: {triaged['valid']}")
print(f"Severity: {triaged['severity']}")
print(f"CVSS Score: {triaged['cvss_score']}")
print(f"Duplicates: {triaged['duplicates']}")
```

### Calculating Bounty

```python
# Calculate bounty for submission
bounty = agent.calculate_bounty(
    submission_id=submission["id"],
    apply_multipliers=True
)

print(f"Base bounty: ${bounty['base_bounty']}")
print(f"Final bounty: ${bounty['final_bounty']}")
print(f"Multipliers applied: {bounty['multipliers_applied']}")
```

### Issuing Security Advisory

```python
# Create and publish advisory
advisory = agent.issue_advisory(
    submission_id=submission["id"],
    cve_id=None,  # Auto-assign if None
    remediation="Update to version 2.1.0 or apply the provided patch",
    publish=True
)

print(f"Advisory created: {advisory['id']}")
print(f"CVE ID: {advisory['cve_id']}")
print(f"Published: {advisory['published']}")
```

### Managing Researchers

```python
# Register researcher
researcher = agent.register_researcher(
    username="security_researcher",
    email="researcher@example.com",
    display_name="John Doe",
    skills=["web-security", "sql-injection", "xss"]
)

print(f"Researcher registered: {researcher['id']}")

# Get researcher rankings
rankings = agent.get_researcher_rankings(period="monthly")

for ranking in rankings[:10]:
    print(f"#{ranking['rank']}: {ranking['username']} - ${ranking['total_bounties']}")
```

## API Reference

### BugBountyAgent

Main orchestrator class that coordinates all components.

```python
class BugBountyAgent:
    def __init__(self, config: Dict = None)
    def create_program(self, name: str, description: str, **kwargs) -> Dict
    def submit_vulnerability(self, program_id: str, **kwargs) -> Dict
    def triage_submission(self, submission_id: str, **kwargs) -> Dict
    def calculate_bounty(self, submission_id: str, **kwargs) -> Dict
    def issue_advisory(self, submission_id: str, **kwargs) -> Dict
    def register_researcher(self, **kwargs) -> Dict
    def get_researcher_rankings(self, period: str) -> List[Dict]
    def generate_report(self, program_id: str) -> Dict
```

### ProgramManager

Manage bug bounty programs.

```python
class ProgramManager:
    def create_program(self, config: ProgramConfig) -> Program
    def update_program(self, program_id: str, updates: Dict) -> Program
    def add_scope(self, program_id: str, scope: Scope) -> Scope
    def remove_scope(self, program_id: str, scope_id: str) -> bool
    def get_program(self, program_id: str) -> Program
    def list_programs(self, status: str = None) -> List[Program]
```

### SubmissionTriage

Triage vulnerability submissions.

```python
class SubmissionTriage:
    def submit_vulnerability(self, data: SubmissionData) -> Submission
    def validate_submission(self, submission_id: str) -> ValidationResult
    def assess_severity(self, submission_id: str) -> SeverityResult
    def detect_duplicates(self, submission_id: str) -> List[Submission]
    def assign_priority(self, submission_id: str) -> Priority
    def update_status(self, submission_id: str, status: str) -> Submission
```

### RewardEngine

Calculate and manage rewards.

```python
class RewardEngine:
    def calculate_bounty(self, submission: Submission, program: Program) -> BountyResult
    def apply_multipliers(self, base_bounty: float, submission: Submission) -> float
    def process_payment(self, submission_id: str) -> Payment
    def get_payment_history(self, researcher_id: str) -> List[Payment]
    def generate_receipt(self, payment_id: str) -> Receipt
```

### AdvisoryService

Manage security advisories.

```python
class AdvisoryService:
    def create_advisory(self, submission: Submission, program: Program) -> Advisory
    def assign_cve(self, advisory_id: str) -> str
    def coordinate_disclosure(self, advisory_id: str, timeline: int) -> DisclosurePlan
    def publish_advisory(self, advisory_id: str) -> PublicationResult
    def notify_stakeholders(self, advisory_id: str) -> List[Notification]
```

### ResearcherManager

Manage researcher relationships.

```python
class ResearcherManager:
    def register_researcher(self, data: ResearcherRegistration) -> Researcher
    def update_profile(self, researcher_id: str, updates: Dict) -> Researcher
    def track_performance(self, researcher_id: str) -> PerformanceMetrics
    def calculate_rankings(self, period: str) -> List[ResearcherRanking]
    def process_payment(self, researcher_id: str, amount: float) -> Payment
```

## Examples

### Example 1: Complete Bug Bounty Workflow

```python
from agents.bug-bounty.agent import BugBountyAgent

agent = BugBountyAgent()

# 1. Create program
program = agent.create_program(
    name="Web App Security Program",
    description="Bug bounty for web applications",
    reward_range="100-10000",
    scope=[{"target": "*.example.com", "type": "domain"}]
)

# 2. Register researcher
researcher = agent.register_researcher(
    username="hacker123",
    email="hacker@example.com"
)

# 3. Submit vulnerability
submission = agent.submit_vulnerability(
    program_id=program["id"],
    researcher_id=researcher["id"],
    title="XSS in profile page",
    description="Stored XSS vulnerability...",
    severity="high",
    proof_of_concept={"steps": [...], "screenshot": "xss.png"}
)

# 4. Triage submission
triaged = agent.triage_submission(submission["id"])

# 5. Calculate bounty
bounty = agent.calculate_bounty(submission["id"])
print(f"Bounty: ${bounty['final_bounty']}")

# 6. Issue advisory
advisory = agent.issue_advisory(
    submission["id"],
    publish=True
)
```

### Example 2: Batch Triage

```python
# Triage multiple submissions
submissions = agent.get_pending_submissions(program_id="program-123")

for submission in submissions:
    triaged = agent.triage_submission(submission["id"])
    
    if triaged["valid"]:
        bounty = agent.calculate_bounty(submission["id"])
        print(f"Submission {submission['id']}: ${bounty['final_bounty']}")
```

### Example 3: Generate Program Report

```python
# Generate analytics report
report = agent.generate_report(
    program_id="program-123",
    period="monthly"
)

print(f"Total submissions: {report['total_submissions']}")
print(f"Total bounties paid: ${report['total_bounties_paid']}")
print(f"Top researcher: {report['top_researcher']}")
```

## Configuration

### Agent Configuration

```yaml
# config.yaml
app:
  name: "BugBounty Agent"
  version: "2.0.0"
  environment: "production"
  debug: false

database:
  url: "postgresql://user:pass@localhost:5432/bugbounty"
  pool_size: 5
  max_overflow: 10

redis:
  url: "redis://localhost:6379"
  db: 0

rabbitmq:
  url: "amqp://localhost:5672"
  exchange: "bugbounty"
  queue: "submissions"

security:
  secret_key: "your-secret-key"
  algorithm: "HS256"
  access_token_expire_minutes: 30

reward:
  min_bounty: 100
  max_bounty: 50000
  default_multipliers:
    low: 1.0
    medium: 2.0
    high: 3.0
    critical: 5.0

notifications:
  email:
    enabled: true
    smtp_server: "smtp.example.com"
    smtp_port: 587
  slack:
    enabled: true
    webhook_url: "https://hooks.slack.com/..."
```

### Environment Variables

```bash
# Application
APP_NAME=BugBounty Agent
APP_VERSION=2.0.0
APP_ENV=production

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/bugbounty
DATABASE_POOL_SIZE=5

# Redis
REDIS_URL=redis://localhost:6379
REDIS_DB=0

# RabbitMQ
RABBITMQ_URL=amqp://localhost:5672

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Rewards
MIN_BOUNTY=100
MAX_BOUNTY=50000
```

## Best Practices

### Program Management

1. **Clear Scope**: Define in-scope and out-of-scope targets explicitly
2. **Realistic Rewards**: Set reward ranges aligned with industry standards
3. **Timely Response**: Respond to submissions within 48 hours
4. **Transparent Rules**: Publish clear program rules and policies
5. **Safe Harbor**: Provide safe harbor provisions for researchers

### Triage Process

1. **Standardized Criteria**: Use CVSS and consistent evaluation criteria
2. **Quality Checks**: Validate submission quality and reproducibility
3. **Duplicate Detection**: Implement automated duplicate detection
4. **Clear Communication**: Provide feedback on submissions
5. **Timely Resolution**: Aim for resolution within 90 days

### Reward Management

1. **Fair Calculation**: Use transparent, consistent calculation methods
2. **Quality Bonuses**: Reward high-quality submissions
3. **Timely Payment**: Process payments promptly
4. **Clear Receipts**: Provide detailed payment receipts
5. **Tax Compliance**: Handle tax reporting requirements

### Advisory Publication

1. **Coordinated Disclosure**: Follow coordinated disclosure timelines
2. **Complete Information**: Include all necessary details in advisories
3. **Clear Remediation**: Provide clear remediation guidance
4. **Credit Researchers**: Acknowledge researcher contributions
5. **Multiple Channels**: Publish to appropriate channels

### Researcher Relations

1. **Respectful Communication**: Maintain professional, respectful tone
2. **Timely Responses**: Respond to questions and submissions quickly
3. **Clear Feedback**: Provide constructive feedback on submissions
4. **Fair Treatment**: Apply rules consistently to all researchers
5. **Recognition**: Acknowledge and celebrate researcher contributions

## Troubleshooting

### Common Issues

**Issue: Submission not being triaged**
```python
# Check submission status
submission = agent.get_submission(submission_id)
print(f"Status: {submission['status']}")

# Manually trigger triage
agent.triage_submission(submission_id, force=True)
```

**Issue: Bounty calculation incorrect**
```python
# Debug bounty calculation
bounty = agent.calculate_bounty(submission_id, debug=True)
print(f"Base bounty: {bounty['base_bounty']}")
print(f"Multipliers: {bounty['multipliers_applied']}")
print(f"Final bounty: {bounty['final_bounty']}")
```

**Issue: CVE assignment failing**
```python
# Check CVE assignment
try:
    cve_id = agent.assign_cve(submission_id)
    print(f"CVE assigned: {cve_id}")
except CVEAssignmentError as e:
    print(f"CVE assignment failed: {e}")
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Initialize agent with debug
agent = BugBountyAgent(config={"debug": True})
```

### Performance Profiling

```python
import cProfile
import pstats

# Profile agent execution
profiler = cProfile.Profile()
profiler.enable()

result = agent.run()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills/agents/bug-bounty

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
pylint agents/bug-bounty/agent.py
```

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: [Link to documentation]
- Issues: [GitHub Issues]
- Discussions: [GitHub Discussions]
- Email: [support email]

## Changelog

### Version 2.0.0 (2026-06-05)

- Complete rewrite with comprehensive features
- Program management with scope and reward configuration
- Advanced submission triage with CVSS assessment
- Duplicate detection using text similarity
- Reward calculation with quality multipliers
- Security advisory management with CVE coordination
- Researcher management and rankings
- Analytics and reporting
- Coordinated disclosure workflows
