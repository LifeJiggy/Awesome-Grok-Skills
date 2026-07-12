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
