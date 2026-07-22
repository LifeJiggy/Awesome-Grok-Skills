---
name: "release-notes"
category: "technical-writing"
version: "1.0.0"
tags: ["technical-writing", "release-notes", "changelog", "semantic-versioning", "migration"]
---

# Automated Release Note Generation & Changelog Management

## Overview

Release notes are the primary communication channel between software maintainers and their users. This module provides a complete pipeline for generating, classifying, and publishing release notes from source code changes, issue trackers, and pull request metadata. It enforces semantic versioning, detects breaking changes, generates migration guides, and manages deprecation notices across multiple release channels.

The core workflow ingests commit messages, pull request titles, and issue labels, then classifies each change into categories: Added, Changed, Deprecated, Removed, Fixed, and Security. The classification engine uses conventional commit prefixes (feat:, fix:, breaking:, deprecate:), PR labels, and custom heuristics to produce structured changelogs without manual curation.

Semantic versioning enforcement ensures that version bumps accurately reflect the nature of changes. The module analyzes the classified changes between two versions and validates that the version number follows semver rules: patch for backwards-compatible fixes, minor for backwards-compatible additions, major for breaking changes. It flags version mismatches and prevents accidental major version bumps from being published.

For breaking changes, the module automatically generates migration guides by analyzing code diffs, extracting API surface changes, and producing step-by-step instructions for consumers. Deprecation notices are tracked across versions, ensuring that deprecated features receive adequate warning periods before removal.

The multi-channel publishing system formats release notes for different audiences: concise summaries for Slack, detailed changelogs for GitHub Releases, structured data for RSS feeds, and rich HTML for documentation sites. Each channel receives appropriately formatted content without manual intervention.

## Core Capabilities

- **Automated Changelog Generation**: Transform commit histories, PR titles, and issue labels into categorized, human-readable changelogs following Keep a Changelog format.
- **Semantic Versioning Enforcement**: Validate version bumps against the actual nature of changes, flagging mismatches between version numbers and change severity.
- **Breaking Change Detection**: Identify and document backward-incompatible changes with specific impact analysis and migration guidance.
- **Migration Guide Generation**: Produce step-by-step migration instructions for breaking changes, including code diffs and before/after examples.
- **Deprecation Notice Management**: Track deprecated features across versions, enforce warning periods, and generate deprecation timeline documentation.
- **Multi-Channel Publishing**: Format and distribute release notes to GitHub Releases, Slack, email newsletters, documentation sites, and RSS feeds.
- **Conventional Commit Parsing**: Parse and validate conventional commit messages (feat:, fix:, breaking:, chore:) with configurable type mappings.
- **Release Communication Templates**: Pre-built templates for major, minor, and patch release announcements with customizable branding and tone.

## Usage Examples

### Changelog Generation from Commits

```python
from release_notes import ChangelogGenerator, ChangeCategory

generator = ChangelogGenerator(
    repo_path=".",
    from_ref="v1.4.0",
    to_ref="v1.5.0",
    category_map={
        "feat": ChangeCategory.ADDED,
        "fix": ChangeCategory.FIXED,
        "breaking": ChangeCategory.REMOVED,
        "deprecate": ChangeCategory.DEPRECATED,
        "perf": ChangeCategory.CHANGED,
        "security": ChangeCategory.SECURITY,
    }
)

changelog = generator.generate()
print(changelog.to_markdown())

# Validate that all commits are classified
unclassified = generator.get_unclassified()
if unclassified:
    print(f"Warning: {len(unclassified)} commits could not be classified")
    for commit in unclassified:
        print(f"  - {commit.hash[:8]}: {commit.message}")
```

### Semantic Versioning Enforcement

```python
from release_notes import SemVerEnforcer, Version

enforcer = SemVerEnforcer(
    current_version="1.4.0",
    changelog=changelog
)

recommended = enforcer.recommend_version()
print(f"Current: {enforcer.current_version}")
print(f"Recommended: {recommended}")
print(f"Bumping to: {enforcer.validate_bump(recommended)}")

# Check for accidental breaking changes
breaking = enforcer.get_breaking_changes()
if breaking:
    print(f"Breaking changes detected — major version bump required")
    for change in breaking:
        print(f"  - {change.description}")
```

### Migration Guide Generation

```python
from release_notes import MigrationGuideGenerator

generator = MigrationGuideGenerator(
    from_version="1.4.0",
    to_version="2.0.0"
)

guide = generator.generate(
    breaking_changes=changelog.breaking_changes,
    code_diffs=generator.extract_diffs("src/", "v1.4.0", "v2.0.0")
)

# Render as Markdown
print(guide.to_markdown())

# Publish to documentation site
generator.publish(guide, output_dir="docs/migrations/")
```

### Deprecation Notice Management

```python
from release_notes import DeprecationManager, DeprecationNotice

manager = DeprecationManager(
    notices_dir="docs/deprecations/",
    warning_period_versions=3
)

# Register a new deprecation
notice = DeprecationNotice(
    feature="legacy-auth-endpoint",
    deprecated_in="1.5.0",
    removal_in="2.0.0",
    replacement="/api/v2/auth",
    reason="Replaced by OAuth 2.0 flow",
    migration_steps=[
        "Update authentication requests to use /api/v2/auth",
        "Remove client_id parameter (now derived from JWT)",
        "Update token refresh logic for new response format"
    ]
)
manager.register(notice)

# Check if any deprecations have exceeded warning period
expired = manager.check_expirations(current_version="1.8.0")
for notice in expired:
    print(f"WARNING: '{notice.feature}' was deprecated in {notice.deprecated_in} "
          f"and should have been removed by {notice.removal_in}")
```

### Multi-Channel Publishing

```python
from release_notes import ReleasePublisher, Channel

publisher = ReleasePublisher(
    channels={
        Channel.GITHUB_RELEASES: {"repo": "org/repo", "token_env": "GH_TOKEN"},
        Channel.SLACK: {"webhook_env": "SLACK_WEBHOOK", "channel": "#releases"},
        Channel.DOCUMENTATION: {"output_dir": "docs/releases/"},
    }
)

# Publish release notes across all channels
results = publisher.publish(
    version="1.5.0",
    title="Release 1.5.0 — New Dashboard API",
    changelog=changelog,
    assets=["dist/app-1.5.0.tar.gz"]
)

for channel, result in results.items():
    status = "OK" if result.success else f"FAILED: {result.error}"
    print(f"  {channel.value}: {status}")
```

### Conventional Commit Parsing

```python
from release_notes import CommitParser, ParsedCommit

parser = CommitParser(
    types={
        "feat": "Features",
        "fix": "Bug Fixes",
        "docs": "Documentation",
        "style": "Styling",
        "refactor": "Code Refactoring",
        "perf": "Performance",
        "test": "Tests",
        "chore": "Maintenance",
        "breaking": "Breaking Changes",
        "deprecate": "Deprecations",
    }
)

commit = parser.parse("feat(api): add user search endpoint")
print(f"Type: {commit.type}")
print(f"Scope: {commit.scope}")
print(f"Description: {commit.description}")
print(f"Is Breaking: {commit.is_breaking}")

# Parse commit with body
full = parser.parse(
    "feat(auth): implement OAuth 2.0 flow\n\n"
    "Replace legacy auth endpoint with OAuth 2.0.\n\n"
    "BREAKING CHANGE: /api/v1/auth is removed."
)
print(f"Breaking: {full.is_breaking}")
print(f"Body: {full.body}")
```

### Release Communication Templates

```python
from release_notes import ReleaseTemplate, TemplateType

template = ReleaseTemplate(type=TemplateType.MAJOR_RELEASE)
content = template.render(
    version="2.0.0",
    highlights=[
        "OAuth 2.0 authentication replaces legacy API keys",
        "New dashboard API with real-time updates",
        "Improved error responses with detailed codes"
    ],
    breaking_changes_count=3,
    migration_guide_url="https://docs.example.com/migrations/v2",
    changelog_url="https://github.com/org/repo/releases/tag/v2.0.0"
)
print(content)
```

## Best Practices

1. **Use conventional commits consistently**: Adopt a commit message format (feat:, fix:, breaking:) and enforce it through CI hooks. Consistent messages enable automated changelog generation.
2. **Bump versions based on content, not schedule**: Semantic versioning reflects the nature of changes, not your release calendar. A patch release with breaking changes is a major release regardless of timing.
3. **Write migration guides for every breaking change**: A breaking change without a migration guide is hostile to your users. Include before/after code examples and step-by-step instructions.
4. **Give deprecation warnings at least 2 minor versions**: Don't remove features immediately after deprecation. Allow users time to migrate by maintaining deprecated features for at least 2 minor versions.
5. **Keep release notes in the repository**: Store CHANGELOG.md in the repo root and generate it as part of your release CI pipeline. This ensures notes are versioned alongside the code.
6. **Categorize every change**: Uncategorized changes confuse readers. If a change doesn't fit standard categories, create a custom category rather than leaving it uncategorized.
7. **Test your release process**: Run a dry-run release before publishing. Validate version bumps, changelog generation, and multi-channel publishing work correctly.
8. **Highlight user-visible changes**: Don't list internal refactors or test additions as top-level changes. Group them under a "Maintenance" or "Internal" section. Lead with features and fixes that users care about.
9. **Include upgrade difficulty ratings**: Rate breaking changes by migration effort (trivial, moderate, complex) to help users plan upgrade windows.
10. **Archive release notes**: Maintain a searchable archive of all past release notes. Users often need to reference what changed between specific versions.

## Related Modules

- [documentation](../documentation/GROK.md) — General technical documentation authoring and lifecycle management
- [api-docs](../api-docs/GROK.md) — OpenAPI specification generation and API reference documentation
- [tutorials](../tutorials/GROK.md) — Progressive tutorial authoring and learning path design
- [architecture-docs](../architecture-docs/GROK.md) — Architecture Decision Records and system design documentation

## Advanced Configuration

### Conventional Commit Parser Configuration

Customize commit parsing with a YAML configuration:

```yaml
# release-notes-config.yml
commit_parser:
  types:
    feat: Features
    fix: Bug Fixes
    docs: Documentation
    style: Styling
    refactor: Code Refactoring
    perf: Performance
    test: Tests
    chore: Maintenance
    breaking: Breaking Changes
    deprecate: Deprecations
  scopes:
    api: API Changes
    auth: Authentication
    db: Database
    ui: User Interface
  breaking_patterns:
    - "BREAKING CHANGE:"
    - "BREAKING-CHANGE:"
    - "!: "
  body_parsers:
    - pattern: "Refs: #(\\d+)"
      extract: issue_number
```

### Semantic Versioning Policy

Configure versioning behavior:

```yaml
semver:
  auto_bump: true
  require_major_for_breaking: true
  allow_prerelease: true
  prerelease_tags: [alpha, beta, rc]
  version_file: VERSION
  tag_prefix: "v"
  changelog_file: CHANGELOG.md
```

### Migration Guide Configuration

```yaml
migration:
  auto_generate: true
  template: templates/migration-guide.md
  include_code_diffs: true
  diff_options:
    context_lines: 3
    ignore_whitespace: true
  format:
    include_before_after: true
    include_timestamp: true
    max_steps: 20
```

### Deprecation Policy Configuration

```yaml
deprecation:
  warning_period_minor_versions: 2
  notify_on_deprecation: true
  removal_reminder_days: 30
  tracking_file: docs/deprecations.json
  auto_generate_timeline: true
```

### Multi-Channel Publishing Configuration

```yaml
publishing:
  channels:
    github_releases:
      enabled: true
      repo: "org/repo"
      token_env: "GH_TOKEN"
      draft: false
      prerelease: false
    slack:
      enabled: true
      webhook_env: "SLACK_WEBHOOK"
      channel: "#releases"
      mention_on_major: "@channel"
    documentation:
      enabled: true
      output_dir: "docs/releases/"
      format: markdown
    email:
      enabled: false
      smtp_host: "smtp.example.com"
      recipients_file: "release-recipients.txt"
```

## Architecture Patterns

### Release Pipeline

The release notes system follows a pipeline architecture:

```
Commit History -> Parsing -> Classification -> Enrichment -> Formatting -> Publishing
        |            |             |               |              |             |
    Git Log      Conventional   Category Map   Breaking      Templates    GitHub/Slack
    PR Titles    Commit Parse   Severity       Change        Markdown     Email/RSS
    Issue Labels Regex Match    Grouping       Detection     HTML         Documentation
```

### Changelog Generation Pipeline

```
Input Sources -> Deduplication -> Grouping -> Sorting -> Rendering -> Output
      |               |              |           |           |          |
  Commits/PRs    Hash Check    Category     Date/Type   Template   Markdown
  Issues         Author Merge  Priority     Breaking    Interp     JSON/RSS
  Manual Notes   Scope Group   Impact       First       Format     HTML
```

### Version Validation Pipeline

```
Proposed Version -> Change Analysis -> Semver Check -> Breaking Check -> Approval
        |                |                |               |               |
    User Input      Commit Diff      Policy Match    Impact Score    CI Gate
    Tag Check       PR Analysis      Auto-suggest    Migration Need  Manual Review
```

### Deprecation Lifecycle

```python
from release_notes import DeprecationManager, DeprecationState

# Deprecation lifecycle states
states = {
    "active": "Feature is in use",
    "deprecated": "Warning period started",
    "removal_scheduled": "Removal version confirmed",
    "removed": "Feature no longer available",
}

# Track deprecation timeline
manager = DeprecationManager(notices_dir="docs/deprecations/")
notice = manager.register(
    feature="legacy-auth",
    deprecated_in="1.5.0",
    removal_in="2.0.0"
)
# notice.state transitions: active -> deprecated -> removal_scheduled -> removed
```

## Integration Guide

### CI/CD Pipeline Integration

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release-notes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Generate Changelog
        run: python -m release_notes.changelog --from ${{ github.event.before }} --to ${{ github.sha }}
      - name: Validate Version
        run: python -m release_notes.semver --check
      - name: Publish Release
        run: python -m release_notes.publish --channels github,slack
```

### IDE Integration

Real-time changelog validation through LSP:

```python
from release_notes import ReleaseNotesLSPServer

server = ReleaseNotesLSPServer(
    changelog_path="CHANGELOG.md",
    config_path="release-notes-config.yml",
    live_validation=True
)
server.start()
```

### Webhook Integration

```python
from release_notes import ReleasePublisher, WebhookNotifier

notifier = WebhookNotifier(
    channels={
        "slack": {"webhook_url": "https://hooks.slack.com/xxx"},
        "teams": {"webhook_url": "https://outlook.office.com/xxx"},
    }
)

# Notify on release
publisher = ReleasePublisher(channels={"slack": config, "teams": config})
publisher.publish(version="1.5.0", title="Release 1.5.0", changelog=changelog)
```

## Performance Optimization

### Caching Changelog

Cache generated changelogs to avoid regeneration:

```python
from release_notes import ChangelogGenerator, CacheConfig

generator = ChangelogGenerator(
    repo_path=".",
    from_ref="v1.4.0",
    to_ref="v1.5.0",
    cache_config=CacheConfig(
        enabled=True,
        cache_dir=".changelog-cache/",
        ttl_seconds=3600
    )
)
```

### Parallel Publishing

Publish to multiple channels concurrently:

```python
from release_notes import ReleasePublisher, ParallelConfig

publisher = ReleasePublisher(
    channels=config,
    parallel_config=ParallelConfig(enabled=True, workers=4)
)
results = publisher.publish(version="1.5.0", changelog=changelog)
```

### Incremental Changelog Updates

Only process new commits since last release:

```python
from release_notes import ChangelogGenerator, DiffMode

generator = ChangelogGenerator(
    repo_path=".",
    from_ref="v1.4.0",
    to_ref="HEAD",
    diff_mode=DiffMode.INCREMENTAL  # Only process new commits
)
```

## Security Considerations

### Authentication

Secure access to publishing channels:

```python
from release_notes import SecurityConfig

config = SecurityConfig(
    github_token_env="GH_TOKEN",
    slack_webhook_env="SLACK_WEBHOOK",
    require_https=True,
    verify_webhooks=True
)
```

### Access Control

Control who can publish release notes:

```python
from release_notes import AccessControl, ReleasePermission

acl = AccessControl()
acl.grant(role="maintainer", permissions=[ReleasePermission.PUBLISH, ReleasePermission.EDIT])
acl.grant(role="developer", permissions=[ReleasePermission.VIEW, ReleasePermission.COMMENT])
```

### Input Validation

Validate all inputs to prevent injection:

```python
from release_notes import InputValidator

validator = InputValidator(
    rules={
        "version": {"pattern": r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$", "required": True},
        "title": {"max_length": 200, "sanitize": True},
        "changelog_path": {"extension": [".md", ".txt"], "writable": True},
    }
)
```

### Rate Limiting

Protect publishing endpoints from abuse:

```yaml
rate_limiting:
  changelog_generation:
    requests_per_minute: 10
    burst_size: 5
  publishing:
    requests_per_minute: 5
    burst_size: 2
  version_validation:
    requests_per_minute: 30
    burst_size: 10
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Version mismatch | Breaking change without major bump | Run `python -m release_notes.semver --check` |
| Unclassified commits | Missing conventional commit prefix | Update commit messages or add type mapping |
| Multi-channel publish failed | Channel-specific auth issue | Check credentials and webhook URLs |
| Deprecation expired | Warning period exceeded | Remove feature or extend deprecation |
| Migration guide incomplete | Missing code diffs | Ensure git tags exist for both versions |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from release_notes import ChangelogGenerator
generator = ChangelogGenerator(repo_path=".", debug=True)
```

### Log Output

```
[DEBUG] release_notes.parser: Parsing 47 commits between v1.4.0 and v1.5.0
[DEBUG] release_notes.semver: Analyzing changes for version recommendation
[WARNING] release_notes.parser: 3 commits could not be classified
[ERROR] release_notes.publisher: Slack publish failed: webhook URL invalid
[INFO] release_notes.changelog: Generated changelog with 12 entries
```

## API Reference

### ChangelogGenerator

```python
class ChangelogGenerator:
    def __init__(self, repo_path: str, from_ref: str, to_ref: str,
                 category_map: Dict[str, ChangeCategory] = None):
        """Initialize the changelog generator."""

    def generate(self) -> Changelog:
        """Generate a changelog from commit history."""

    def get_unclassified(self) -> List[Commit]:
        """Get commits that could not be classified."""
```

### SemVerEnforcer

```python
class SemVerEnforcer:
    def __init__(self, current_version: str, changelog: Changelog):
        """Initialize the version enforcer."""

    def recommend_version(self) -> str:
        """Recommend the next version based on changes."""

    def validate_bump(self, proposed: str) -> str:
        """Validate and return the proposed version bump."""

    def get_breaking_changes(self) -> List[Change]:
        """Get all breaking changes in the changelog."""
```

### MigrationGuideGenerator

```python
class MigrationGuideGenerator:
    def __init__(self, from_version: str, to_version: str):
        """Initialize the migration guide generator."""

    def generate(self, breaking_changes: List[Change],
                 code_diffs: Dict[str, str] = None) -> MigrationGuide:
        """Generate a migration guide from breaking changes."""

    def publish(self, guide: MigrationGuide, output_dir: str) -> None:
        """Publish the migration guide to the documentation site."""
```

## Data Models

### Changelog

```python
@dataclass
class Changelog:
    version: str
    date: str
    entries: Dict[ChangeCategory, List[Change]]
    breaking_changes: List[Change]
    metadata: Dict[str, Any]
```

### Change

```python
@dataclass
class Change:
    category: ChangeCategory
    description: str
    commit_hash: str
    author: str
    scope: Optional[str]
    is_breaking: bool
    migration_hint: Optional[str]
```

### MigrationGuide

```python
@dataclass
class MigrationGuide:
    from_version: str
    to_version: str
    sections: List[MigrationSection]
    code_diffs: Dict[str, str]
    generated_at: datetime
```

### DeprecationNotice

```python
@dataclass
class DeprecationNotice:
    feature: str
    deprecated_in: str
    removal_in: str
    replacement: Optional[str]
    reason: str
    migration_steps: List[str]
    state: str  # active, deprecated, removal_scheduled, removed
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "-m", "release_notes.server", "--host", "0.0.0.0", "--port", "8080"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: release-notes-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: release-notes
  template:
    spec:
      containers:
        - name: release-notes
          image: release-notes:latest
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 1Gi
```

## Monitoring & Observability

### Metrics Collection

```python
from release_notes import MetricsCollector

metrics = MetricsCollector(prefix="release_notes")
metrics.histogram("changelog_generation_seconds", duration)
metrics.counter("releases_published_total", count, labels={"channel": "github"})
metrics.counter("breaking_changes_total", count, labels={"severity": "major"})
```

### Alerting Rules

```yaml
groups:
  - name: release-notes
    rules:
      - alert: ChangelogGenerationFailure
        expr: rate(release_notes_changelog_errors_total[1h]) > 1
        labels:
          severity: warning
        annotations:
          summary: "Changelog generation is failing"
      - alert: PublishFailure
        expr: rate(release_notes_publish_errors_total[1h]) > 5
        labels:
          severity: critical
        annotations:
          summary: "Release publishing is failing"
```

## Testing Strategy

### Unit Tests

```python
def test_conventional_commit_parsing():
    parser = CommitParser(types={"feat": "Features", "fix": "Bug Fixes"})
    commit = parser.parse("feat(api): add user search endpoint")
    assert commit.type == "feat"
    assert commit.scope == "api"
    assert commit.description == "add user search endpoint"

def test_version_recommendation():
    enforcer = SemVerEnforcer("1.4.0", changelog)
    recommended = enforcer.recommend_version()
    assert recommended == "1.5.0"
```

### Integration Tests

```python
def test_full_release_pipeline():
    generator = ChangelogGenerator(repo_path=".", from_ref="v1.4.0", to_ref="v1.5.0")
    changelog = generator.generate()
    assert len(changelog.entries) > 0

    enforcer = SemVerEnforcer("1.4.0", changelog)
    version = enforcer.recommend_version()

    publisher = ReleasePublisher(channels={"github": config})
    results = publisher.publish(version=version, changelog=changelog)
    assert results["github"].success
```

## Versioning & Migration

### Semantic Versioning

The release notes module follows semantic versioning:
- **Major**: Breaking changes to public API or configuration format
- **Minor**: New features, new channels, new templates
- **Patch**: Bug fixes, improved parsing accuracy

### Deprecation Policy

Deprecated features receive warnings for one minor version before removal. Migration guides are provided for all breaking changes.

### Version Compatibility

| Module Version | Minimum Supported Git Version | Notes |
|---------------|------------------------------|-------|
| 1.4.x | 2.30.0 | Full feature support |
| 1.3.x | 2.25.0 | Limited tag support |
| 1.2.x | 2.20.0 | Basic commit parsing |

## Glossary

| Term | Definition |
|------|-----------|
| **Semantic Versioning** | Version numbering scheme (MAJOR.MINOR.PATCH) |
| **Conventional Commit** | A structured commit message format (feat:, fix:, etc.) |
| **Breaking Change** | A modification that is not backward-compatible |
| **Changelog** | A human-readable list of changes between versions |
| **Deprecation Warning** | A notice that a feature will be removed in a future version |
| **Migration Guide** | Step-by-step instructions for upgrading between versions |
| **Release Channel** | A distribution channel (GitHub, Slack, email, documentation) |
| **Change Category** | Classification of a change (Added, Changed, Deprecated, etc.) |

## Changelog

### v1.4.0 (Latest)
- Added advanced commit parsing with custom type mappings
- Added multi-channel publishing with parallel execution
- Improved breaking change detection accuracy

### v1.3.0
- Added migration guide generation with code diffs
- Added deprecation notice management
- Improved changelog formatting

### v1.2.0
- Added semantic versioning enforcement
- Added breaking change detection
- Improved conventional commit parsing

### v1.1.0
- Added multi-channel publishing
- Added release communication templates
- Improved changelog generation

### v1.0.0
- Initial release with changelog generation
- Conventional commit parsing
- Version validation
- Deprecation tracking

## Contributing Guidelines

### How to Contribute

1. Fork the repository and create a feature branch
2. Follow existing code style and patterns
3. Write tests for new features
4. Update documentation as needed
5. Ensure all CI checks pass
6. Submit a pull request with a clear description

### Adding New Commit Types

1. Add the type to the parser configuration
2. Add a corresponding category map entry
3. Write tests for parsing and classification
4. Update documentation

### Adding New Publishing Channels

1. Implement the channel publisher interface
2. Add configuration schema
3. Write integration tests
4. Update documentation

## License

MIT License

Copyright (c) 2025 Example Organization

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Dependencies

- `gitpython` >= 3.1 — Git repository interaction
- `pyyaml` >= 6.0 — YAML configuration parsing
- `requests` >= 2.31 — HTTP client for channel publishing
- `jinja2` >= 3.1 — Template rendering for release notes
- `semver` >= 3.0 — Semantic versioning utilities
