---
name: "documentation"
category: "technical-writing"
version: "1.0.0"
tags: ["technical-writing", "documentation", "doc-as-code", "style-guide", "multi-format"]
---

# Technical Documentation Authoring & Lifecycle Management

## Overview

This module provides a comprehensive toolkit for authoring, enforcing, and managing technical documentation across the full content lifecycle. It bridges the gap between raw content creation and production-grade documentation systems by offering programmatic style guide enforcement, cross-reference integrity checking, multi-format rendering pipelines, and content lifecycle automation.

The core philosophy is doc-as-code: documentation lives alongside source code, is reviewed through the same pull request workflows, and is validated through automated checks. The module supports Markdown as the primary authoring format but can render to HTML, PDF, and AsciiDoc. It includes a style guide engine that enforces consistency across tense, voice, terminology, and formatting rules — catching drift before it reaches readers.

Documentation teams face unique challenges: stale content accumulates silently, cross-references break as files move, style inconsistencies erode trust, and multi-format publishing introduces rendering divergence. This module addresses each of these problems with deterministic tooling rather than manual review processes. Every component is designed to be invoked from CI/CD pipelines, local pre-commit hooks, or interactive authoring sessions.

The module's architecture is modular and composable. Style guide rules can be shared across projects, cross-reference managers can be scoped to subdirectories, and rendering pipelines can be extended with custom formatters. This design allows teams to adopt individual capabilities incrementally rather than requiring a wholesale migration to a new documentation system.

## Core Capabilities

- **Style Guide Enforcement**: Define and enforce writing standards (terminology, tense, voice, formatting) across all documentation files with rule-based validation and auto-fix suggestions.
- **Cross-Reference Management**: Detect broken internal links, generate link inventories, and auto-update cross-references when files are renamed or reorganized.
- **Multi-Format Rendering**: Render Markdown documentation to HTML, PDF, and AsciiDoc with consistent output using template engines and CSS-based styling.
- **Content Lifecycle Tracking**: Monitor documentation freshness, flag stale content, track authorship, and manage review cycles with configurable TTL policies.
- **Documentation Site Generation**: Build static documentation sites from folder structures with navigation generation, search indexing, and version tagging.
- **Template Management**: Maintain reusable documentation templates for common patterns (API reference, tutorial, conceptual guide, troubleshooting).
- **Terminology Glossary**: Centralized terminology management with inline validation, consistency checking, and glossary generation.
- **Content Quality Metrics**: Measure readability scores, word count targets, heading hierarchy compliance, and content completeness against defined schemas.

## Usage Examples

### Style Guide Enforcement

```python
from documentation import StyleGuide, StyleRule, Severity

# Define a style guide with domain-specific rules
guide = StyleGuide(
    project="my-api",
    rules=[
        StyleRule(
            id="SG-001",
            name="use-active-voice",
            pattern=r"\b(is|are|was|were)\s+\w+ed\b",
            severity=Severity.WARNING,
            suggestion="Use active voice instead of passive construction.",
            applies_to=["conceptual", "tutorial"]
        ),
        StyleRule(
            id="SG-002",
            name="avoid-jargon",
            terms=["utilize", "leverage", "synergy"],
            replacement_map={"utilize": "use", "leverage": "use", "synergy": "cooperation"},
            severity=Severity.ERROR
        ),
        StyleRule(
            id="SG-003",
            name="second-person",
            pattern=r"\bwe\b",
            severity=Severity.INFO,
            suggestion="Address the reader directly with 'you' instead of 'we'."
        ),
    ]
)

# Validate a documentation file
results = guide.validate("docs/getting-started.md")
for violation in results.violations:
    print(f"[{violation.rule_id}] Line {violation.line}: {violation.message}")
    if violation.suggestion:
        print(f"  Suggestion: {violation.suggestion}")

# Auto-fix where possible
guide.auto_fix("docs/getting-started.md", dry_run=True)
```

### Cross-Reference Integrity

```python
from documentation import CrossReferenceManager

manager = CrossReferenceManager(root_dir="docs/")

# Build link inventory across all Markdown files
inventory = manager.build_inventory()
print(f"Found {len(inventory.internal_links)} internal links across {len(inventory.files)} files")

# Check for broken references
broken = manager.check_integrity()
for ref in broken:
    print(f"BROKEN: {ref.source_file}:{ref.line} -> {ref.target} (reason: {ref.reason})")

# Auto-update links after a file rename
manager.rename_map = {
    "docs/architecture.md": "docs/system-design/architecture-overview.md"
}
manager.update_references(dry_run=False)
```

### Multi-Format Rendering

```python
from documentation import DocumentationRenderer, OutputFormat

renderer = DocumentationRenderer(
    template_dir="templates/",
    css_path="styles/docs.css",
    base_url="https://docs.example.com"
)

# Render to HTML
renderer.render(
    source="docs/",
    output_format=OutputFormat.HTML,
    output_dir="_build/html/"
)

# Render to PDF with custom options
renderer.render(
    source="docs/",
    output_format=OutputFormat.PDF,
    output_dir="_build/pdf/",
    pdf_options={
        "page_size": "A4",
        "margin": "2cm",
        "toc_depth": 3,
        "header": "Example Project Documentation",
        "footer": "Page {page_number}"
    }
)
```

### Content Lifecycle Management

```python
from documentation import ContentLifecycleManager, FreshnessPolicy

manager = ContentLifecycleManager(
    policies=[
        FreshnessPolicy(content_type="api-reference", max_age_days=90, require_reviewer=True),
        FreshnessPolicy(content_type="tutorial", max_age_days=180, notify_authors=True),
        FreshnessPolicy(content_type="conceptual", max_age_days=365),
        FreshnessPolicy(content_type="changelog", max_age_days=30),
    ]
)

# Audit content freshness
audit = manager.audit("docs/")
print(f"Total docs: {audit.total}")
print(f"Stale: {audit.stale_count}")
print(f"Missing review: {audit.needs_review_count}")

for doc in audit.stale_documents:
    print(f"  STALE ({doc.days_since_update}d): {doc.path} — last updated by {doc.author}")

# Generate staleness report
manager.generate_report(audit, output="docs/audit-report.md")
```

### Terminology Management

```python
from documentation import TerminologyManager, GlossaryEntry

glossary = TerminologyManager()
glossary.add_entry(GlossaryEntry(
    term="Kubernetes",
    definition="An open-source container orchestration platform",
    aliases=["k8s", "kube"],
    category="infrastructure"
))
glossary.add_entry(GlossaryEntry(
    term="gRPC",
    definition="A high-performance RPC framework by Google",
    aliases=["grpc", "GRPC"],
    category="protocols"
))

# Validate terminology across docs
violations = glossary.validate_file("docs/getting-started.md")
for line_num, term, suggestion in violations:
    print(f"Line {line_num}: {suggestion}")

# Generate glossary document
glossary.generate_glossary(output_path="docs/glossary.md")
```

### Content Quality Analysis

```python
from documentation import ContentQualityAnalyzer

analyzer = ContentQualityAnalyzer()
metrics = analyzer.analyze("docs/getting-started.md")
if metrics:
    print(f"Word count: {metrics.word_count}")
    print(f"Reading level: {metrics.reading_level}")
    print(f"Heading hierarchy valid: {metrics.heading_hierarchy_valid}")
    print(f"Avg words per sentence: {metrics.avg_words_per_sentence:.1f}")
```

## Best Practices

1. **Treat documentation as code**: Store docs in the same repository, review through pull requests, and validate with automated checks before merging.
2. **Enforce style at CI time**: Run style guide checks as part of your CI pipeline — not as an afterthought. Fail builds on critical violations.
3. **Version your documentation alongside your code**: Tag documentation with release versions so readers can access docs matching their software version.
4. **Automate freshness checks**: Set up automated audits that flag content older than a threshold and notify original authors.
5. **Use semantic heading hierarchy**: Never skip heading levels (H1 -> H3). Maintaining H1 -> H2 -> H3 order ensures correct document outline generation and accessibility.
6. **Maintain a centralized glossary**: Define domain terms once and validate usage across all documentation to prevent terminology drift.
7. **Preview before publishing**: Always render documentation to the target format in a staging environment before publishing. Multi-format rendering introduces subtle differences.
8. **Track documentation coverage**: Measure what percentage of your public API, features, and tutorials have corresponding documentation. Treat gaps as high-priority items.
9. **Use inclusive language**: Avoid ableist, gendered, and exclusionary terms in documentation. Maintain a list of preferred alternatives and validate automatically.
10. **Measure readability**: Target a Flesch-Kincaid grade level appropriate for your audience. API docs can be technical; tutorials should be accessible.

## Integration Patterns

### CI/CD Pipeline Integration

```yaml
# .github/workflows/docs-check.yml
name: Documentation Checks
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Style Guide Check
        run: python -m documentation.style --project my-api --fail-on error
      - name: Cross-Reference Integrity
        run: python -m documentation.xref --root docs/ --check-broken
      - name: Content Freshness
        run: python -m documentation.lifecycle --audit docs/ --max-age 365
```

### Pre-commit Hook Setup

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: doc-style
        name: Documentation Style Check
        entry: python -m documentation.style --fix
        language: system
        files: \.md$
      - id: doc-xref
        name: Cross-Reference Check
        entry: python -m documentation.xref --check
        language: system
        files: \.md$
```

## Architecture Notes

The module uses a plugin architecture for rendering backends. Each output format (HTML, PDF, AsciiDoc) is implemented as a renderer class that inherits from `BaseRenderer`. Custom renderers can be registered at runtime:

```python
from documentation import DocumentationRenderer, BaseRenderer

class CustomRenderer(BaseRenderer):
    def render_content(self, markdown: str) -> str:
        # Custom rendering logic
        return transformed_content

renderer = DocumentationRenderer()
renderer.register_format("custom", CustomRenderer)
```

Style guide rules are composable and support inheritance. A project can extend a base style guide with project-specific overrides:

```python
from documentation import StyleGuide, StyleRule

base_rules = load_style_guide("company-base")
project_rules = [
    StyleRule(id="PROJ-001", name="project-specific", pattern=r"...")
]
guide = StyleGuide(project="my-service", rules=base_rules + project_rules)
```

## Related Modules

- [api-docs](../api-docs/GROK.md) — OpenAPI specification generation and API reference documentation
- [tutorials](../tutorials/GROK.md) — Progressive tutorial authoring and learning path design
- [architecture-docs](../architecture-docs/GROK.md) — ADRs, system design docs, and architecture diagrams
- [release-notes](../release-notes/GROK.md) — Automated release note generation and changelog management

## Advanced Configuration

### Style Guide Configuration

The style guide engine supports a YAML-based configuration format that can be shared across projects. Define your style rules in a `.style-guide.yml` file at the repository root or reference a shared configuration from a central repository.

```yaml
# .style-guide.yml
project: my-project
extends: company-base-style
rules:
  - id: SG-001
    name: use-active-voice
    pattern: "\\b(is|are|was|were)\\s+\\w+ed\\b"
    severity: warning
    suggestion: "Use active voice instead of passive construction."
    applies_to: [conceptual, tutorial]
  - id: SG-002
    name: avoid-jargon
    terms: [utilize, leverage, synergy]
    replacement_map:
      utilize: use
      leverage: use
      synergy: cooperation
    severity: error
  - id: SG-003
    name: heading-hierarchy
    max_depth: 4
    require_h1: true
    severity: error
  - id: SG-004
    name: inclusive-language
    terms:
      - master/slave: primary/replica
      - whitelist/blacklist: allowlist/blocklist
      - sanity check: confidence check
    severity: warning
```

### Rendering Configuration

Configure output rendering through a `doc-config.yml` file:

```yaml
rendering:
  default_format: html
  output_dir: _build
  template_dir: templates
  base_url: https://docs.example.com
  html:
    theme: documentation-theme
    syntax_highlighting: true
    line_numbers: false
    max_toc_depth: 3
  pdf:
    page_size: A4
    margin: 2cm
    header: "Project Documentation"
    footer: "Page {page_number}"
  asciidoc:
    backend: html5
    icons: font
```

### Lifecycle Policy Configuration

```yaml
lifecycle:
  policies:
    - content_type: api-reference
      max_age_days: 90
      require_reviewer: true
      notify_on_stale: true
    - content_type: tutorial
      max_age_days: 180
      notify_authors: true
    - content_type: conceptual
      max_age_days: 365
    - content_type: changelog
      max_age_days: 30
  review_escalation:
    after_days: 14
    escalate_to: documentation-team
  staleness_thresholds:
    warning: 60
    critical: 90
```

## Architecture Patterns

### Plugin-Based Rendering

The rendering system uses a plugin architecture where each output format is a renderer class inheriting from `BaseRenderer`. This allows adding new formats without modifying core code.

```python
from documentation import BaseRenderer, RendererRegistry

class MarkdownRenderer(BaseRenderer):
    format_name = "markdown"

    def render_content(self, markdown: str, metadata: dict) -> str:
        return self.apply_frontmatter(markdown, metadata)

    def validate_output(self, content: str) -> bool:
        return content.startswith("---") or content.startswith("#")

registry = RendererRegistry()
registry.register(MarkdownRenderer)
renderer = registry.get("markdown")
```

### Composable Style Guide Inheritance

Style guides support a hierarchical inheritance model. Create a base style guide at the organization level and extend it per-project:

```python
from documentation import StyleGuide, StyleRule, merge_guides

base_guide = StyleGuide.load("company-base-style")
project_guide = StyleGuide(
    project="payment-service",
    rules=[
        StyleRule(id="PAY-001", name="payment-terminology",
                  terms=["money", "funds"], severity="error"),
    ]
)

merged = merge_guides(base_guide, project_guide)
```

### Content Lifecycle State Machine

Content moves through defined states during its lifecycle:

```python
from documentation import ContentState

# States: DRAFT -> IN_REVIEW -> APPROVED -> PUBLISHED -> STALE -> ARCHIVED
valid_transitions = {
    ContentState.DRAFT: [ContentState.IN_REVIEW],
    ContentState.IN_REVIEW: [ContentState.DRAFT, ContentState.APPROVED],
    ContentState.APPROVED: [ContentState.PUBLISHED],
    ContentState.PUBLISHED: [ContentState.STALE],
    ContentState.STALE: [ContentState.IN_REVIEW, ContentState.ARCHIVED],
}
```

## Integration Guide

### IDE Integration

The module provides Language Server Protocol (LSP) integration for real-time documentation validation in editors:

```python
from documentation import DocumentationLSPServer

server = DocumentationLSPServer(
    style_guide_path=".style-guide.yml",
    watch_patterns=["docs/**/*.md"],
    live_preview=True
)
server.start()
```

### Documentation CMS Integration

Export documentation sets for import into CMS platforms:

```python
from documentation import CMSExporter, CMSTarget

exporter = CMSExporter(source_dir="docs/")

exporter.export(
    target=CMSTarget.CONFLUENCE,
    space_key="ENG",
    parent_page="Documentation",
    credentials_env="CONFLUENCE_TOKEN"
)

exporter.export(
    target=CMSTarget.NOTION,
    database_id="docs-database",
    credentials_env="NOTION_TOKEN"
)
```

### Git Hooks Integration

```bash
#!/bin/bash
# .git/hooks/pre-commit
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')

if [ -n "$CHANGED_FILES" ]; then
    echo "Checking documentation style..."
    python -m documentation.style --files $CHANGED_FILES --fail-on warning
    if [ $? -ne 0 ]; then
        echo "Documentation style check failed."
        exit 1
    fi

    echo "Checking cross-references..."
    python -m documentation.xref --check --files $CHANGED_FILES
    if [ $? -ne 0 ]; then
        echo "Broken cross-references detected."
        exit 1
    fi
fi
```

## Performance Optimization

### Caching Rendered Output

The rendering pipeline supports content-based caching:

```python
from documentation import DocumentationRenderer, CacheConfig

renderer = DocumentationRenderer(
    cache_config=CacheConfig(
        enabled=True,
        cache_dir=".doc-cache/",
        invalidate_on=["docs/**/*.md", "templates/**"],
        max_cache_size_mb=500
    )
)
renderer.render(source="docs/", output_format=OutputFormat.HTML)
```

### Parallel Cross-Reference Checking

For large documentation sets, enable parallel cross-reference scanning:

```python
from documentation import CrossReferenceManager, ParallelConfig

manager = CrossReferenceManager(
    root_dir="docs/",
    parallel_config=ParallelConfig(enabled=True, workers=4, chunk_size=50)
)
inventory = manager.build_inventory()
```

### Incremental Style Validation

Validate only changed files in CI:

```yaml
- name: Incremental Style Check
  run: |
    CHANGED=$(git diff --name-only origin/main -- '*.md')
    if [ -n "$CHANGED" ]; then
      echo "$CHANGED" | python -m documentation.style --stdin --fail-on warning
    fi
```

## Security Considerations

### Content Security

Documentation rendered to HTML should be sanitized to prevent XSS attacks:

```python
from documentation import DocumentationRenderer, SecurityConfig

renderer = DocumentationRenderer(
    security_config=SecurityConfig(
        sanitize_html=True,
        allowed_tags=["p", "h1", "h2", "h3", "code", "pre", "a", "img", "ul", "ol", "li"],
        strip_scripts=True,
        csp_policy="default-src 'self'; script-src 'none'"
    )
)
```

### Access Control

Restrict documentation access based on audience classification:

```python
from documentation import AccessControl, Audience

acl = AccessControl()
acl.grant(audience=Audience.INTERNAL, paths=["docs/internal/**"])
acl.grant(audience=Audience.PARTNER, paths=["docs/partner/**"])
acl.grant(audience=Audience.PUBLIC, paths=["docs/public/**"])

assert acl.is_accessible("docs/internal/architecture.md", Audience.PUBLIC) is False
```

### Sensitive Data Detection

Scan documentation for accidentally committed secrets:

```python
from documentation import SensitiveDataScanner

scanner = SensitiveDataScanner(
    patterns=[
        r"AKIA[0-9A-Z]{16}",
        r"ghp_[0-9a-zA-Z]{36}",
        r"-----BEGIN (RSA )?PRIVATE KEY",
        r"password\s*[:=]\s*\S+",
    ]
)

findings = scanner.scan_directory("docs/")
for finding in findings:
    print(f"SENSITIVE: {finding.path}:{finding.line} - {finding.pattern_name}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Broken cross-references | File renamed without updating links | Run `python -m documentation.xref --fix` |
| Style guide false positives | Regex pattern too broad | Adjust pattern specificity or add exclusions |
| PDF rendering fails | Missing wkhtmltopdf | Install wkhtmltopdf or use weasyprint backend |
| Stale content not flagged | Lifecycle policy misconfigured | Verify content_type matches frontmatter tags |
| Glossary validation misses | Term aliases not registered | Add aliases to GlossaryEntry definitions |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from documentation import DocumentationRenderer
renderer = DocumentationRenderer(debug=True)
renderer.render(source="docs/", output_format=OutputFormat.HTML)
```

### Log Output

```
[DEBUG] documentation.renderer: Processing docs/getting-started.md
[DEBUG] documentation.style: Applying rules SG-001, SG-002, SG-003
[DEBUG] documentation.xref: Checking 47 internal links
[WARNING] documentation.xref: BROKEN: docs/getting-started.md:23 -> ../api/reference.md
[INFO] documentation.renderer: Rendered 12 files to _build/html/
```

## API Reference

### DocumentationRenderer

```python
class DocumentationRenderer:
    def __init__(self, template_dir: str = "templates/",
                 css_path: str = None, base_url: str = None,
                 cache_config: CacheConfig = None,
                 security_config: SecurityConfig = None):
        """Initialize the documentation renderer."""

    def render(self, source: str, output_format: OutputFormat,
               output_dir: str, **options) -> RenderResult:
        """Render documentation from source to target format."""

    def register_format(self, name: str, renderer: BaseRenderer) -> None:
        """Register a custom renderer for a new output format."""

    def render_file(self, source_file: str, output_format: OutputFormat) -> str:
        """Render a single file and return the output path."""
```

### CrossReferenceManager

```python
class CrossReferenceManager:
    def __init__(self, root_dir: str, parallel_config: ParallelConfig = None):
        """Initialize the cross-reference manager."""

    def build_inventory(self) -> LinkInventory:
        """Build a complete inventory of internal links."""

    def check_integrity(self) -> List[BrokenReference]:
        """Check for broken internal references."""

    def update_references(self, rename_map: Dict[str, str],
                          dry_run: bool = True) -> UpdateReport:
        """Update references after file renames."""
```

### ContentLifecycleManager

```python
class ContentLifecycleManager:
    def __init__(self, policies: List[FreshnessPolicy]):
        """Initialize with freshness policies."""

    def audit(self, doc_dir: str) -> AuditReport:
        """Audit content freshness across all documents."""

    def generate_report(self, audit: AuditReport, output: str) -> None:
        """Generate a staleness report as Markdown."""

    def notify_stale(self, audit: AuditReport) -> NotificationReport:
        """Send notifications for stale content."""
```

## Data Models

### DocumentationSet

```python
@dataclass
class DocumentationSet:
    id: str
    name: str
    version: str
    source_files: List[str]
    output_formats: List[OutputFormat]
    style_guide: Optional[str]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
```

### ValidationViolation

```python
@dataclass
class ValidationViolation:
    rule_id: str
    rule_name: str
    severity: Severity
    file_path: str
    line: int
    column: int
    message: str
    suggestion: Optional[str]
    auto_fixable: bool
```

### AuditReport

```python
@dataclass
class AuditReport:
    total: int
    fresh: int
    stale_count: int
    needs_review_count: int
    stale_documents: List[StaleDocument]
    generated_at: datetime
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
CMD ["python", "-m", "documentation.server", "--host", "0.0.0.0", "--port", "8080"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: documentation-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: documentation
  template:
    spec:
      containers:
        - name: documentation
          image: documentation:latest
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 1Gi
          volumeMounts:
            - name: docs-volume
              mountPath: /app/docs
      volumes:
        - name: docs-volume
          persistentVolumeClaim:
            claimName: docs-pvc
```

## Monitoring & Observability

### Metrics Collection

```python
from documentation import MetricsCollector

metrics = MetricsCollector(prefix="documentation")
metrics.histogram("render_duration_seconds", duration, labels={"format": "html"})
metrics.counter("render_files_total", count, labels={"format": "pdf"})
metrics.counter("style_violations_total", violations, labels={"severity": "error"})
metrics.gauge("docs_stale_count", stale_count)
```

### Alerting Rules

```yaml
groups:
  - name: documentation
    rules:
      - alert: HighStaleContentRate
        expr: documentation_stale_ratio > 0.3
        for: 7d
        labels:
          severity: warning
        annotations:
          summary: "Over 30% of documentation is stale"
      - alert: BrokenReferencesDetected
        expr: documentation_broken_xrefs > 0
        for: 1d
        labels:
          severity: critical
        annotations:
          summary: "Broken cross-references detected"
```

## Testing Strategy

### Unit Tests

```python
def test_style_guide_detects_passive_voice():
    guide = StyleGuide(rules=[passive_voice_rule])
    results = guide.validate_string("The file was created by the system.")
    assert len(results.violations) == 1
    assert results.violations[0].rule_id == "SG-001"

def test_cross_reference_detection():
    manager = CrossReferenceManager(root_dir="test/fixtures/docs/")
    broken = manager.check_integrity()
    assert len(broken) == 2

def test_content_freshness_audit():
    manager = ContentLifecycleManager(policies=[default_policy])
    audit = manager.audit("test/fixtures/docs/")
    assert audit.stale_count >= 1
```

### Integration Tests

```python
def test_full_render_pipeline():
    renderer = DocumentationRenderer(template_dir="templates/")
    result = renderer.render(
        source="test/fixtures/docs/",
        output_format=OutputFormat.HTML,
        output_dir="/tmp/test-output/"
    )
    assert result.files_rendered > 0
    assert result.errors == 0
```

## Versioning & Migration

### Semantic Versioning

The documentation module follows semantic versioning:
- **Major**: Breaking changes to public API or configuration format
- **Minor**: New features, new renderer formats, new style rules
- **Patch**: Bug fixes, performance improvements

### Migration Guide (v1.x to v2.0)

```python
# v1.x style guide format
guide = StyleGuide(
    rules_file="style-guide.json",  # Deprecated
    project="my-project"
)

# v2.0 style guide format
guide = StyleGuide(
    config_path=".style-guide.yml",  # New YAML-based config
    project="my-project",
    extends="company-base-style"     # New inheritance support
)
```

## Glossary

| Term | Definition |
|------|-----------|
| **Style Guide** | A set of rules governing writing conventions, terminology, and formatting |
| **Cross-Reference** | An internal link from one documentation file to another |
| **Freshness** | The age of documentation content relative to its last review |
| **Stale Content** | Documentation that has not been reviewed within its policy threshold |
| **Rendering** | The process of converting Markdown to target formats (HTML, PDF) |
| **Content Lifecycle** | The states a document passes through from draft to archived |
| **Terminology Glossary** | A centralized dictionary of approved terms and their definitions |
| **Doc-as-Code** | Managing documentation using the same tools as source code |

## Changelog

### v1.4.0 (Latest)
- Added terminology management system with glossary generation
- Added content quality analyzer with readability scoring
- Improved style guide rule composition and inheritance

### v1.3.0
- Added content lifecycle management with freshness policies
- Added automated staleness detection and notification
- Improved audit report generation

### v1.2.0
- Added PDF rendering with customizable page layout
- Improved cross-reference auto-fix reliability
- Added accessibility checking for rendered HTML output

### v1.1.0
- Added broken link detection with auto-fix suggestions
- Improved style guide false positive rate
- Added template inheritance for documentation templates

### v1.0.0
- Initial release with style guide enforcement
- Cross-reference integrity checking
- Multi-format rendering (HTML, PDF, AsciiDoc)
- Content lifecycle tracking

## Contributing Guidelines

### How to Contribute

1. Fork the repository and create a feature branch
2. Follow existing code style and patterns
3. Write tests for new features
4. Update documentation as needed
5. Ensure all CI checks pass
6. Submit a pull request with a clear description

### Development Setup

```bash
git clone https://github.com/example/documentation-module.git
cd documentation-module
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest
```

### Adding New Style Rules

Define new rules in the appropriate style guide configuration file. Each rule must have:
- A unique ID (format: SG-XXX)
- A descriptive name
- A pattern or term list
- A severity level (info, warning, error)
- A suggestion for fixing violations

### Adding New Renderers

Extend `BaseRenderer` and implement the `render_content` method. Register the renderer with `DocumentationRenderer.register_format()`. Include unit tests.

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

- `markdown` >= 3.5 — Markdown processing
- `weasyprint` >= 60.0 — PDF rendering
- `pyyaml` >= 6.0 — YAML configuration parsing
- `jinja2` >= 3.1 — Template rendering
- `pygments` >= 2.15 — Syntax highlighting
- `requests` >= 2.31 — HTTP client for CMS integration
