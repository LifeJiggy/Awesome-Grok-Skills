
# Accessibility Agent

> **THE** definitive accessibility auditing and remediation agent for modern web applications.
> WCAG 2.0/2.1/2.2/3.0 compliant. Production-ready. Built for scale.

---

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Core Concepts](#core-concepts)
7. [API Reference](#api-reference)
8. [Usage Patterns](#usage-patterns)
9. [Report Formats](#report-formats)
10. [Remediation](#remediation)
11. [Plugin System](#plugin-system)
12. [History & Trends](#history--trends)
13. [Batch Operations](#batch-operations)
14. [Integration Hooks](#integration-hooks)
15. [Performance Tuning](#performance-tuning)
16. [Security & Privacy](#security--privacy)
17. [Extending the Agent](#extending-the-agent)
18. [Troubleshooting](#troubleshooting)
19. [FAQ](#faq)
20. [Contributing](#contributing)

---

---

## Overview

The Accessibility Agent is a comprehensive, modular system for auditing, reporting,
and remediating accessibility issues in web content. It is designed to be:

- **Standards-first**: WCAG 2.0, 2.1, 2.2, 3.0 and Section 508.
- **Comprehensive**: semantic HTML, ARIA, keyboard navigation, color contrast,
  headings, links, forms, tables, landmarks, focus management, and more.
- **Actionable**: generated reports include specific element selectors, severity
  ratings, WCAG criterion references, and suggested code fixes.
- **Extensible**: plugin architecture for custom rules and parsers.
- **Integration-friendly**: exports to Lighthouse and axe-core formats.

The agent works in three phases:

1. **Parse** - Convert raw HTML into a structured DOM tree.
2. **Analyze** - Run a configurable suite of analyzers over the DOM.
3. **Report / Remediate** - Produce multi-format reports and prioritized
   remediation plans.

---

---

## Key Features

### Multi-Standard Compliance

- WCAG 2.0 A / AA / AAA
- WCAG 2.1 A / AA / AAA
- WCAG 2.2 A / AA / AAA (flashing, dragging, target size)
- WCAG 3.0 draft alignment
- Section 508 (US federal)

### Analyzer Coverage

| Analyzer | Checks |
|----------|--------|
| SemanticAnalyzer | Heading hierarchy, landmarks, images, forms, links, tables, language, title |
| ARIAAnalyzer | Role validity, required states, name calculation, hidden conflicts |
| KeyboardAnalyzer | Traps, skip links, tab order, focus visibility, click handlers |
| ColorAnalyzer | Contrast ratios, large text thresholds, color blindness simulation |

### Report Formats

- HTML (interactive, styled)
- Markdown (GitHub-friendly)
- JSON (machine-readable)
- CSV (spreadsheets)
- PDF (print-ready placeholder)
- JUnit XML (CI/CD gates)

### Remediation

- Prioritized `RemediationPlan` with `RemediationStep` objects
- Estimated effort per step
- Dry-run and apply modes
- Backup-before-fix support

### Plugin System

- Drop `.py` files into configured directories
- Subclass `PluginBase`
- Automatic discovery and execution
- Error isolation per plugin

### History & Trends

- JSON-backed audit history
- Retention policies
- Score trending over time

### Batch & Async

- `batch_audit(urls)` for sequential URLs
- `batch_audit_async(urls, concurrency=4)` for concurrent fetching

### Integration Hooks

- `to_lighthouse_format()` for Google Lighthouse compatibility
- `to_axe_core_format()` for Deque axe-core compatibility

---

---

## Quick Start

```python
from agents.accessibility.agent import AccessibilityAgent, Config

agent = AccessibilityAgent()

result = agent.audit("https://example.com")
print(f"Score: {result.score}%")
print(f"Issues: {len(result.issues)}")

# Markdown report
report = agent.generate_report(result, fmt="markdown")

# Save JSON
report = agent.generate_report(result, fmt="json", output_path="report.json")

# Remediation plan
plan = agent.create_remediation_plan()
print(plan.summary)
```

---

---

## Installation

```bash
# Clone the repository
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills

# Optional: install optional dependencies for richer parsing
pip install beautifulsoup4 lxml

# Optional: for PDF generation
pip install weasyprint
```

---

---

## Configuration

Full configuration reference with defaults:

```python
from agents.accessibility.agent import Config, WCAGVersion, WCAGLevel, ReportFormat

config = Config(
    # Standard selection
    standard="wcag2.1-aa",
    wcag_version=WCAGVersion.WCAG_21,
    wcag_level=WCAGLevel.AA,

    # Analyzer toggles
    aria_checks=True,
    keyboard_navigation_checks=True,
    semantic_checks=True,
    color_contrast_checks=True,
    heading_structure_checks=True,
    link_text_checks=True,
    form_label_checks=True,
    table_structure_checks=True,
    landmark_checks=True,
    focus_management_checks=True,
    document_language_checks=True,
    skip_to_content_checks=True,
    media_checks=True,

    # Color analysis
    color_blindness_checks=True,
    simulate_screen_reader=False,

    # Reporting
    generate_report=True,
    report_formats=[ReportFormat.HTML, ReportFormat.JSON, ReportFormat.MARKDOWN],
    output_directory="./accessibility_reports",

    # History
    history_enabled=True,
    history_file="accessibility_history.json",
    retention_days=90,

    # Performance
    concurrency=4,
    cache_results=True,
    cache_ttl_hours=24,
    max_retries=3,
    retry_delay_seconds=1.0,

    # Remediation
    auto_fix_enabled=False,
    max_auto_fixes_per_run=10,
    backup_before_fix=True,

    # Plugins
    plugin_directories=["./accessibility_plugins"],
    custom_rules=[],

    # Networking
    timeout=60,
    user_agent="AccessibilityAgent/2.0",
    viewport_width=1280,
    viewport_height=720,
)

agent = AccessibilityAgent(config=config)
```

---

---

## Core Concepts

### WCAG Levels

- **A** - Minimum accessibility.
- **AA** - Required for most legal compliance (target default).
- **AAA** - Highest level; often not achievable for entire sites.

### Severity Levels

| Severity | Score Penalty | Meaning |
|----------|---------------|---------|
| CRITICAL | 15.0 | Blocks assistive technology usage. |
| HIGH | 8.0 | Major barrier for users with disabilities. |
| MEDIUM | 4.0 | Noticeable friction or missing best practice. |
| LOW | 1.0 | Minor issue or enhancement opportunity. |

### Issue Categories

- `color-contrast`
- `aria`
- `keyboard`
- `semantic-html`
- `images`
- `forms`
- `headings`
- `links`
- `landmarks`
- `focus`
- `tables`
- `multimedia`
- `document`
- `custom`

---

---

## API Reference

### `AccessibilityAgent`

#### Initialization

```python
agent = AccessibilityAgent(config=None)
```

If no `Config` is provided, defaults are used.

#### `audit(url: str) -> AuditResult`

Audit a live URL.

```python
result = agent.audit("https://example.com")
```

Raises `AuditError` if the URL cannot be fetched.

#### `audit_html(html: str, base_url: str = "") -> AuditResult`

Audit raw HTML content.

```python
html = Path("index.html").read_text()
result = agent.audit_html(html, base_url="https://example.com")
```

#### `generate_report(result, fmt, output_path) -> str`

Generate a report.

```python
report = agent.generate_report(
    result=result,
    fmt="html",            # or ReportFormat.HTML
    output_path="report.html"
)
```

#### `create_remediation_plan(result=None) -> RemediationPlan`

Build a prioritized remediation plan from an audit result.

```python
plan = agent.create_remediation_plan()
print(plan.summary)
for step in plan.steps:
    print(step.priority, step.description, step.estimated_minutes)
```

#### `apply_remediation(plan=None, dry_run=True) -> Dict[str, Any]`

Apply a plan (dry-run by default).

#### `export_issues(result=None, fmt="json") -> str`

Export raw issues in JSON, CSV, or Markdown.

#### `batch_audit(urls: List[str]) -> List[AuditResult]`

Audit multiple URLs sequentially.

#### `batch_audit_async(urls, concurrency=4) -> List[AuditResult]`

Audit multiple URLs concurrently.

#### `get_status() -> Dict[str, Any]`

Return agent status including audit count, plugin list, and last score.

#### `get_history() -> List[Dict[str, Any]]`

Return audit history entries.

#### `to_lighthouse_format() -> Dict[str, Any]`

Convert last result to Lighthouse format.

#### `to_axe_core_format() -> Dict[str, Any]`

Convert last result to axe-core format.

#### `register_custom_plugin(plugin_class) -> None`

Register a plugin class at runtime.

---

---

## Usage Patterns

### Pattern 1: Single URL Audit

```python
agent = AccessibilityAgent()
result = agent.audit("https://example.com")
print(result.summary())

html_report = agent.generate_report(result, fmt="html", output_path="audit.html")
```

### Pattern 2: CI/CD Gate

```python
result = agent.audit_html(Path("dist/index.html").read_text())
if result.score < 90 or result.critical_count() > 0:
    raise SystemExit("Accessibility gate failed")
```

### Pattern 3: Batch Scanning

```python
urls = ["https://a.example.com", "https://b.example.com"]
results = agent.batch_audit(urls)
for r in results:
    print(r.url, r.score)
```

### Pattern 4: Regression Testing

```python
before = agent.audit("https://example.com")
# ... apply fixes ...
after = agent.audit("https://example.com")
diff = agent.compare_results(before)
print(diff)
```

### Pattern 5: Custom Plugin

```python
from agents.accessibility.agent import PluginBase, DOMNode, Config, AccessibilityIssue

class MyCustomRule(PluginBase):
    def get_name(self):
        return "my-custom-rule"

    def get_version(self):
        return "1.0.0"

    def analyze(self, dom_node, config):
        issues = []
        for node in self._flatten(dom_node):
            if node.tag_name == "marquee":
                issues.append(AccessibilityIssue(
                    id="marquee-deprecated",
                    criterion="2.2.2 Pause, Stop, Hide",
                    description="Deprecated <marquee> element.",
                    impact="Flickering/moving content.",
                    elements=[node.xpath],
                    suggestion="Replace with CSS animation.",
                    severity=...,
                    category=...,
                ))
        return issues

agent.register_custom_plugin(MyCustomRule)
```

---

---

## Report Formats

### HTML Report

- Color-coded severity badges.
- Collapsible issue sections.
- Inline remediation snippets.
- Responsive layout.

### Markdown Report

```markdown
# Accessibility Report: https://example.com
**Score:** 82.5%
**Date:** 2026-06-03
**Issues:** 14

## Summary
- Critical: 2
- High: 4
- Medium: 5
- Low: 3

## CRITICAL Issues (2)

### 4.1.2 Name, Role, Value
- **Description:** Button has no accessible name.
- **Impact:** Screen readers cannot identify this element.
- **Elements:** /html/body/button[3]
- **Suggestion:** Add aria-label or text content.

```
<button aria-label="Search">Search</button>
```
```

### JSON Report

- Structured issue objects.
- Serialized enums as strings.
- ISO-8601 timestamps.

### CSV Report

Columns: `id`, `severity`, `category`, `criterion`, `description`, `impact`,
`elements`, `suggestion`, `wcag_version`, `wcag_level`.

### JUnit XML

Useful for CI/CD:

```xml
<testsuites>
  <testsuite name="Accessibility Audit" tests="14" failures="2" errors="0">
    <testcase name="4.1.2 Name, Role, Value">
      <failure message="Button has no accessible name.">
        Add aria-label or text content.
      </failure>
    </testcase>
  </testsuite>
</testsuites>
```

---

---

## Remediation

### RemediationPlan Structure

```python
plan = agent.create_remediation_plan()
print(plan.summary)
print(plan.total_estimated_minutes)
for step in plan.steps:
    print(step.description, step.priority, step.estimated_minutes)
```

### Applying Plans

```python
# Dry run
result = agent.apply_remediation(dry_run=True)

# Live apply (requires auto_fix_enabled in config)
result = agent.apply_remediation(dry_run=False)
```

### Custom Remedies per Issue

When creating issues manually, set:

- `remediation_type` from `RemediationType` enum.
- `remediation_code` with the exact fix snippet.

---

---

## Plugin System

### Plugin Base Class

```python
class PluginBase(abc.ABC):
    @abc.abstractmethod
    def get_name(self) -> str:
        ...

    @abc.abstractmethod
    def get_version(self) -> str:
        ...

    @abc.abstractmethod
    def analyze(self, dom_node: DOMNode, config: Config) -> List[AccessibilityIssue]:
        ...
```

### Loading Plugins

```python
# Via config
config = Config(plugin_directories=["./my_plugins"])
agent = AccessibilityAgent(config)

# Or dynamically
agent.register_custom_plugin(MyPluginClass)
```

### Example Plugin: Marquee Detector

```python
class MarqueePlugin(PluginBase):
    def get_name(self):
        return "marquee-detector"

    def get_version(self):
        return "1.0.0"

    def analyze(self, dom_node, config):
        issues = []
        for node in self._flatten(dom_node):
            if node.tag_name == "marquee":
                issues.append(AccessibilityIssue(
                    id="marquee-element",
                    criterion="2.2.2 Pause, Stop, Hide",
                    description="Deprecated marquee element detected.",
                    impact="Moving content is distracting and cannot be paused.",
                    elements=[node.xpath],
                    suggestion="Remove marquee; use CSS animation with prefers-reduced-motion.",
                    severity=IssueSeverity.MEDIUM,
                    category=IssueCategory.MULTIMEDIA,
                ))
        return issues
```

---

---

## History & Trends

```python
# Get last 50 audits
trend = agent.get_history()

# Clear history
agent.clear_history()
```

History entries include:

- `timestamp`
- `url`
- `score`
- `issues_count`
- `critical`, `high`, `medium`, `low` counts

---

---

## Batch Operations

```python
urls = [f"https://example.com/page/{i}" for i in range(100)]
results = agent.batch_audit(urls)

# Or async
import asyncio
results = asyncio.run(agent.batch_audit_async(urls, concurrency=8))
```

---

---

## Integration Hooks

### Lighthouse

```python
lh = agent.to_lighthouse_format()
# {
#   "categories": {
#     "accessibility": {
#       "score": 0.82,
#       "auditRefs": [...]
#     }
#   },
#   "audits": {...}
# }
```

### axe-core

```python
axe = agent.to_axe_core_format()
# {
#   "violations": [...],
#   "passes": [],
#   "incomplete": [],
#   "inapplicable": []
# }
```

### JUnit (CI)

```python
xml = agent.generate_report(result, fmt="junit")
Path("junit.xml").write_text(xml)
```

---

---

## Performance Tuning

### Large Pages

- Set `max_issues_per_category` to cap analyzer output.
- Disable analyzers you don't need (e.g., `media_checks=False`).
- Use `cache_results=True` to avoid re-parsing unchanged content.

### Batch Scans

- Use `batch_audit_async` with `concurrency` tuned to network capacity.
- Set `timeout` appropriately to avoid hanging on slow endpoints.

### Memory

- `AuditHistory` is pruned automatically by `retention_days`.
- Keep `history_file` on a fast disk or disable history for CI runs.

---

---

## Security & Privacy

- Fetches use only `User-Agent` and standard HTTP headers.
- No secrets, cookies, or auth tokens are handled by default.
- Reports may contain DOM text; redact PII before sharing reports externally.
- Plugins execute in-process; only run trusted plugin code.

---

---

## Extending the Agent

### Custom Analyzers

While the built-in analyzers cover most cases, you can extend by wrapping
`PluginBase` or contributing new analyzer classes to the module.

### Custom Report Formats

Add a method to `ReportGenerator`:

```python
def _generate_xml(self, result: AuditResult) -> str:
    ...
```

Then call:

```python
agent.generate_report(result, fmt=ReportFormat("xml"))
```

### Custom Remediation Backends

Extend `RemediationEngine.apply_plan()` to support:

- File patching
- Pull request creation
- Git branch management

---

---

## Troubleshooting

### BeautifulSoup Missing

The agent falls back to a lightweight parser. Install for better results:

```bash
pip install beautifulsoup4
```

For lxml:

```bash
pip install lxml
```

### Low Scores Unexpectedly

- Check `plugin_directories` for noisy plugins.
- Disable analyzers one by one to isolate the source.
- Review `confidence` values on manually created issues.

### Color Contrast Failures

Inline styles are inspected. Ensure CSS is inlined or adjust the parser
integration to extract computed styles from a headless browser.

### Reports Not Generating

Verify `output_directory` exists and is writable. Check for
`ReportGenerationError` in logs with verbosity enabled.

---

---

## FAQ

**Q: Does this agent run JavaScript?**
A: Not by default. For SPAs, integrate a headless browser fetch backend or
inspect the pre-rendered HTML.

**Q: Can it scan PDFs?**
A: Not directly. Convert PDFs to HTML first, then audit.

**Q: Does it support WCAG 3.0?**
A: Partial. The `WCAGVersion` enum includes 3.0; specific 3.0 tests are being
added incrementally.

**Q: How are scores calculated?**
A: `100.0 - sum(issue.score_penalty * confidence)`, clamped to `[0, 100]`.

**Q: Can I use this in CI/CD?**
A: Yes. Use `audit_html()` on build artifacts and the JUnit report for gates.

---

---

## Contributing

We welcome contributions! Please see the main [CONTRIBUTING.md](../../CONTRIBUTING.md)
for guidelines.

For this agent specifically:

- Add analyzers as new classes under `agents/accessibility/`.
- Update `AccessibilityAgent.audit_html()` to wire them in.
- Add report formats by extending `ReportGenerator`.
- Write unit tests under `tests/agents/accessibility/`.

---

---

## Advanced Usage

### Multi-Standard Auditing

```python
from agents.accessibility.agent import AccessibilityAgent, Config, WCAGVersion, WCAGLevel

for version in [WCAGVersion.WCAG_20, WCAGVersion.WCAG_21, WCAGVersion.WCAG_22]:
    for level in [WCAGLevel.A, WCAGLevel.AA, WCAGLevel.AAA]:
        config = Config(wcag_version=version, wcag_level=level)
        agent = AccessibilityAgent(config)
        result = agent.audit_html(html)
        print(f"{version.value} {level.value.upper()}: {result.score}%")
```

### Comparison Across Time

```python
import json
from pathlib import Path

history_file = Path("accessibility_history.json")
history = json.loads(history_file.read_text()) if history_file.exists() else []

for entry in history[-5:]:
    print(f"{entry['timestamp'][:10]}: {entry['score']}% ({entry['issues_count']} issues)")

# Output:
# 2026-06-01: 72.0% (18 issues)
# 2026-06-02: 78.5% (14 issues)
# 2026-06-03: 85.0% (10 issues)
```

### Integration with Test Frameworks

```python
import pytest
from agents.accessibility.agent import AccessibilityAgent, Config

@pytest.fixture
def a11y_agent():
    return AccessibilityAgent(config=Config(generate_report=False, history_enabled=False))

def test_homepage_accessibility(a11y_agent):
    html = Path("public/index.html").read_text()
    result = a11y_agent.audit_html(html)
    assert result.score >= 90, f"Score {result.score}% below threshold"
    assert result.critical_count() == 0, "Critical issues found"
```

### Slack Alerting on Regression

```python
import json
from urllib.request import Request, urlopen

def notify_slack(webhook_url: str, message: str):
    payload = json.dumps({"text": message}).encode()
    req = Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
    urlopen(req)

def audit_and_alert(agent, url, webhook_url):
    result = agent.audit(url)
    if result.score < 80:
        notify_slack(
            webhook_url,
            f"Accessibility regression on {url}: {result.score}% "
            f"({result.critical_count()} critical issues)",
        )
    return result
```

### Scheduled Batch Audits

```python
import schedule
import time

def nightly_audit():
    urls = ["https://example.com", "https://blog.example.com"]
    agent = AccessibilityAgent()
    results = agent.batch_audit(urls)
    for r in results:
        print(f"{r.url}: {r.score}%")

schedule.every().day.at("02:00").do(nightly_audit)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Headless Browser Integration (Playwright)

```python
from playwright.sync_api import sync_playwright

class PlaywrightFetcher:
    def fetch(self, url: str, timeout: int = 60) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.set_default_timeout(timeout * 1000)
            page.goto(url, wait_until="networkidle")
            html = page.content()
            browser.close()
            return html

fetcher = PlaywrightFetcher()
html = fetcher.fetch("https://example.com")
agent = AccessibilityAgent()
result = agent.audit_html(html, base_url="https://example.com")
```

### GitHub PR Comment Bot

```python
import os
from github import Github

def comment_on_pr(repo_name: str, pr_number: int, report_md: str):
    token = os.environ["GITHUB_TOKEN"]
    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(f"## Accessibility Audit\n\n{report_md}")

# Usage in CI:
# report = agent.generate_report(result, fmt="markdown")
# comment_on_pr("owner/repo", 123, report)
```

---

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.

---

---

## Contact

- **Issues**: https://github.com/LifeJiggy/Awesome-Grok-Skills/issues
- **Discord**: Join the Grok Skills community
- **Email**: support@awesome-grok-skills.md

---

---

*Accessibility Agent v2.1.0 - Part of the Awesome Grok Skills collection.*

*"The web is for everyone. Let's audit it."* ♿
