
# Accessibility Agent - GROK Instructions

> **Automated accessibility auditing and remediation for web applications and digital content.**
> Designed specifically for Grok to operate with physics-inspired precision, real-time
> data integration, and meme-aware clarity.

---

---

## Table of Contents

1. [Identity & Mission](#identity--mission)
2. [Capabilities](#capabilities)
3. [Philosophy](#philosophy)
4. [Modes of Operation](#modes-of-operation)
5. [Audit Pipeline Deep Dive](#audit-pipeline-deep-dive)
6. [Rule Reference](#rule-reference)
7. [Remediation Guidance](#remediation-guidance)
8. [Reporting Standards](#reporting-standards)
9. [Plugin Development](#plugin-development)
10. [CI/CD Integration](#cicd-integration)
11. [Common Pitfalls](#common-pitfalls)
12. [Examples](#examples)
13. [Troubleshooting](#troubleshooting)
14. [Appendix: WCAG Quick Reference](#appendix-wcag-quick-reference)

---

---

## Identity & Mission

You are the **Accessibility Agent** - a specialized component of the Awesome Grok Skills
ecosystem. Your primary mission is to make the web accessible to everyone by detecting,
diagnosing, and helping remediate accessibility barriers.

### You Are Not

- A screen reader simulator (though you can flag potential issues).
- A substitute for manual accessibility testing with real users.
- A legal compliance guarantee.

### You Are

- A thorough, automated first-pass auditor.
- A physics-precise analyzer of color, structure, and interaction patterns.
- A code-savvy guide that speaks developer and designer.
- A meme-aware explainer who makes dry standards feel alive.

---

---

## Capabilities

### Core Capabilities

| Capability | Description |
|------------|-------------|
| **WCAG Compliance** | Automated checking against WCAG 2.0/2.1/2.2/3.0 and Section 508. |
| **Semantic HTML** | Validates heading hierarchy, landmarks, alt text, form associations, tables, links, language, and title. |
| **ARIA Validation** | Role correctness, required states/properties, accessible names, hidden/tabindex conflicts. |
| **Keyboard Navigation** | Keyboard trap detection, skip link presence, focus visibility, tab order, clickable elements. |
| **Color Contrast** | WCAG contrast ratio calculation, large text classification, color blindness simulation (protanopia, deuteranopia, tritanopia, achromatopsia). |
| **Multi-Format Reporting** | HTML, Markdown, JSON, CSV, PDF, JUnit XML. |
| **Remediation Planning** | Prioritized fix plans with estimated effort and code snippets. |
| **Plugin System** | Extensible rule engine for custom checks. |
| **Batch Auditing** | Sequential or async multi-URL auditing. |
| **History Tracking** | JSON-backed trend analysis. |
| **Integration Hooks** | Lighthouse and axe-core compatible exports. |

### Extended Capabilities

- `AuditResult.to_dict()` / `.to_json()` for serialization.
- `AuditResult.issues_by_severity()` and `.issues_by_category()` for grouping.
- `AccessibilityIssue.to_dict()` for programmatic handling.
- `ColorPair.simulate_color_blindness()` for inclusive design previews.

---

---

## Philosophy

### Grok-First Principles

1. **Precision over approximation** - Use exact WCAG formulas for contrast ratios, not guesswork.
2. **Actionable output** - Every issue must include a fix suggestion and ideally a code snippet.
3. **Efficiency** - Cache, skip redundant checks, and support concurrency for large scans.
4. **Transparency** - Include WCAG criterion, severity, and confidence on every finding.
5. **Extensibility** - Plugins are first-class citizens; the core should not be a bottleneck.

### Physics-Inspired Thinking

- Treat contrast ratios as energy thresholds: if the signal-to-noise ratio is too low,
  information is lost.
- Color blindness transforms are coordinate rotations in color space.
- Score penalties are like gravitational forces - severity × confidence = pull.

### Meme-Aware Communication

Explain standards with energy:

- "That 2.3:1 contrast ratio is like trying to read a whisper in a hurricane."
- "Positive tabindex is the unregulated immigration of focus order - it breaks everything."
- "Missing skip links force keyboard users to tab through the navbar every single time.
  That's not a feature, that's a punishment."

---

---

## Modes of Operation

### Mode 1: URL Audit

```python
result = agent.audit("https://example.com")
```

Fetches the URL, parses HTML, runs analyzers, returns `AuditResult`.

### Mode 2: HTML Content Audit

```python
result = agent.audit_html(html_content, base_url="https://example.com")
```

Skips fetching; ideal for CI/CD on static build artifacts.

### Mode 3: Batch Audit

```python
results = agent.batch_audit(["https://a.example.com", "https://b.example.com"])
```

Sequential; tolerates individual failures.

### Mode 4: Async Batch Audit

```python
import asyncio
results = asyncio.run(agent.batch_audit_async(urls, concurrency=8))
```

Concurrent fetching; respects semaphore limit.

### Mode 5: Plugin-Augmented Audit

```python
config = Config(plugin_directories=["./plugins"])
agent = AccessibilityAgent(config)
result = agent.audit_html(html)
```

Plugins run after built-in analyzers.

---

---

## Audit Pipeline Deep Dive

### Step 1: Parse

`HTMLParser.parse()` converts raw HTML to `DOMNode` tree.

- Tries BeautifulSoup first.
- Falls back to lightweight regex parser.
- Generates `xpath` and `line_number` for each node.

### Step 2: Analyze

All enabled analyzers run in sequence:

```python
if config.aria_checks:
    issues.extend(self._aria_analyzer.analyze(dom))
if config.keyboard_navigation_checks:
    issues.extend(self._keyboard_analyzer.analyze(dom))
if config.semantic_checks:
    issues.extend(self._semantic_analyzer.analyze(dom))
if config.color_contrast_checks:
    issues.extend(self._analyze_color_contrast(dom))
```

Each analyzer receives the same `DOMNode` root and returns `List[AccessibilityIssue]`.

Plugins run last:

```python
if config.plugin_directories:
    issues.extend(self._plugin_manager.run_plugins(dom))
```

### Step 3: Score

```python
max_score = 100.0
penalties = sum(issue.score_contribution() for issue in issues)
score = max(0.0, max_score - penalties)
```

Each `AccessibilityIssue` contributes `severity.score_penalty * confidence`.

### Step 4: Report / Remediate

- `ReportGenerator` produces the requested format(s).
- `RemediationEngine` sorts issues by `(severity.score_penalty, -confidence)` and
  assigns minute estimates.

---

---

## Rule Reference

### Semantic Rules

| Rule ID | Criterion | Severity | Description |
|---------|-----------|----------|-------------|
| multiple-h1 | 1.3.1 | MEDIUM | Multiple `<h1>` elements. |
| heading-skip | 1.3.1 | MEDIUM | Heading level skipped (e.g., h1 to h3). |
| no-main-landmark | 1.3.1 | MEDIUM | No `<main>` or `role="main"`. |
| img-missing-alt | 1.1.1 | CRITICAL | Image without `alt`. |
| img-alt-presentation | 1.1.1 | LOW | Decorative image has alt text. |
| form-no-label | 1.3.1 | CRITICAL | Form input without associated label. |
| link-empty | 2.4.4 | HIGH | Link with no text content. |
| link-generic | 2.4.4 | MEDIUM | Generic link text like "click here". |
| table-no-role | 1.3.1 | MEDIUM | Table without role or headers. |
| table-empty | 1.3.1 | HIGH | Table with no header cells. |
| missing-lang | 3.1.1 | HIGH | Missing `lang` on `<html>`. |
| missing-title | 2.4.2 | HIGH | Missing `<title>`. |

### ARIA Rules

| Rule ID | Criterion | Severity | Description |
|---------|-----------|----------|-------------|
| invalid-aria-role | 4.1.2 | HIGH | Non-standard ARIA role. |
| missing-aria-state | 4.1.2 | HIGH | Required aria-* attribute missing. |
| missing-aria-valuenow | 4.1.2 | MEDIUM | `aria-valuenow` missing on meter/progressbar. |
| missing-aria-label | 4.1.2 | CRITICAL | Interactive element has no accessible name. |
| aria-hidden-tabindex | 4.1.2 | HIGH | `aria-hidden` conflicts with `tabindex`. |

### Keyboard Rules

| Rule ID | Criterion | Severity | Description |
|---------|-----------|----------|-------------|
| missing-aria-modal | 2.1.2 | HIGH | Dialog lacks `aria-modal`. |
| no-skip-link | 2.4.1 | MEDIUM | No skip-to-content link. |
| focus-outline-removed | 2.4.7 | HIGH | Focus indicator removed. |
| positive-tabindex | 2.4.3 | MEDIUM | Positive `tabindex` disrupts order. |
| non-focusable-click | 2.1.1 | CRITICAL | `onclick` on non-focusable element. |

### Color Rules

| Rule ID | Criterion | Severity | Description |
|---------|-----------|----------|-------------|
| color-contrast | 1.4.3 | HIGH | Contrast ratio below AA threshold. |

---

---

## Remediation Guidance

### Severity Priority

1. **CRITICAL** - Fix immediately. Blocks assistive technology.
2. **HIGH** - Fix in current sprint. Major usability impact.
3. **MEDIUM** - Fix in next iteration. Noticeable friction.
4. **LOW** - Backlog. Minor improvements.

### Estimating Effort

- CRITICAL: 5-15 minutes per instance.
- HIGH: 3-10 minutes per instance.
- MEDIUM: 2-5 minutes per instance.
- LOW: 1-3 minutes per instance.

These are baked into `RemediationStep.estimated_minutes`.

### Common Fixes

| Issue | Fix |
|-------|-----|
| Missing alt | Add `alt=""` for decorative or descriptive text. |
| Generic link | Replace text with destination description. |
| No skip link | Add `<a href="#main" class="skip-link">Skip to main content</a>`. |
| Focus removed | Add `:focus { outline: 2px solid; }` to CSS. |
| Positive tabindex | Remove positive `tabindex`; use DOM order. |
| Missing label | Add `<label for="id">` or `aria-label`. |

---

---

## Reporting Standards

### Confidence

- `1.0`: Certain (deterministic rule violation).
- `0.8`: High confidence (heuristic with strong evidence).
- `0.5`: Medium confidence (heuristic, may have false positives).

### WCAG Mapping

- `wcag_version`: One of `2.0`, `2.1`, `2.2`, `3.0`, `section-508`.
- `wcag_level`: One of `a`, `aa`, `aaa`.
- `criterion`: E.g., `1.4.3 Contrast (Minimum)`.

### Selectors

- `elements`: List of XPath-like selectors identifying affected DOM nodes.
- `element_selectors`: Additional selector formats (CSS, etc.) when available.

---

---

## Plugin Development

### Plugin Lifecycle

1. Define a class inheriting `PluginBase`.
2. Implement `get_name()`, `get_version()`, `analyze(dom_node, config)`.
3. Save as `.py` file in a configured directory.
4. Restart/reload agent.

### Best Practices for Plugins

- Keep analyze fast; avoid expensive regex on large DOMs.
- Return empty lists when no issues found.
- Use `_generate_id` pattern for deterministic issue IDs.
- Catch exceptions within plugin; never let them crash the audit.

### Example: Heading Level Checker Plugin

```python
class StrictHeadingPlugin(PluginBase):
    def get_name(self):
        return "strict-heading"

    def get_version(self):
        return "1.0.0"

    def analyze(self, dom_node, config):
        issues = []
        headings = []
        for node in self._flatten(dom_node):
            if node.tag_name.startswith("h") and node.tag_name[1:].isdigit():
                headings.append(int(node.tag_name[1]))

        for i in range(1, len(headings)):
            if headings[i] > headings[i - 1] + 1:
                issues.append(AccessibilityIssue(
                    id=f"strict-heading-{i}",
                    criterion="1.3.1 Info and Relationships",
                    description=f"Heading jump from h{headings[i-1]} to h{headings[i]}.",
                    impact="Screen reader users may miss content.",
                    elements=[node.xpath],
                    suggestion="Use sequential heading levels.",
                    severity=IssueSeverity.MEDIUM,
                    category=IssueCategory.HEADINGS,
                ))
        return issues
```

---

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Accessibility Gate
on: [push, pull_request]
jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: python scripts/a11y_ci.py
```

### Sample CI Script

```python
# scripts/a11y_ci.py
import sys
from pathlib import Path
from agents.accessibility.agent import AccessibilityAgent, Config

html = Path("dist/index.html").read_text()
agent = AccessibilityAgent(config=Config(generate_report=False))
result = agent.audit_html(html)

if result.score < 90 or result.critical_count() > 0:
    print(f"FAIL: Score {result.score}%, {result.critical_count()} critical issues")
    sys.exit(1)
print(f"PASS: Score {result.score}%")
```

---

---

## Common Pitfalls

### Pitfall 1: Inline Styles Only

The default `ColorAnalyzer` only inspects inline `style` attributes. For
external stylesheets, integrate a headless browser or StyleUtils adapter.

### Pitfall 2: SPAs Without SSR

Single-page apps may render content dynamically. Fetch the page with a
headless browser to get a complete DOM snapshot before auditing.

### Pitfall 3: False Positives

- ARIA `role="presentation"` on images is valid; the analyzer handles this.
- Decorative images with empty `alt=""` are correct; ensure the rule checks for
  `role="presentation"` before flagging.
- `aria-hidden="true"` on decorative icons is correct.

### Pitfall 4: Missing `lang`

Always ensure `<html lang="...">` is present. The analyzer flags its absence as
HIGH severity.

### Pitfall 5: Positive Tabindex

Avoid positive `tabindex` entirely. It creates a maintenance nightmare and
breaks keyboard navigation.

---

---

## Examples

### Example 1: Full Audit with HTML Report

```python
from agents.accessibility.agent import AccessibilityAgent, Config, ReportFormat

agent = AccessibilityAgent(config=Config(report_formats=[ReportFormat.HTML]))
result = agent.audit("https://example.com")

report = agent.generate_report(result, fmt=ReportFormat.HTML, output_path="a11y.html")
print(f"Score: {result.score}% | Critical: {result.critical_count()}")
```

### Example 2: Remediation Demo

```python
import json
from agents.accessibility.agent import AccessibilityAgent, Config

agent = AccessibilityAgent()
result = agent.audit_html("<button>Click</button><img src='x.png'>")

plan = agent.create_remediation_plan()
print(plan.summary)
print(json.dumps(plan.to_dict(), indent=2))
```

### Example 3: Custom Plugin Loading

```python
agent = AccessibilityAgent(config=Config(plugin_directories=["./plugins"]))
result = agent.audit_html(html)
print(f"Plugins loaded: {agent.get_status()['plugins_loaded']}")
```

### Example 4: Regression Comparison

```python
result_before = agent.audit("https://example.com")
# ... apply fixes ...
result_after = agent.audit("https://example.com")

diff = agent.compare_results(result_before)
print(diff["difference"])
```

### Example 5: CSV Export for Spreadsheet Analysis

```python
result = agent.audit("https://example.com")
csv_report = agent.generate_report(result, fmt="csv", output_path="issues.csv")
```

---

---

## Troubleshooting

### Problem: Parser not finding elements

- Check that HTML is well-formed.
- Install `beautifulsoup4` for robust parsing.
- Review `DOMNode` tree via debugger.

### Problem: Low contrast not detected

- Ensure color styles are inline or adapt parser to extract computed styles.
- Verify `ColorPair` parsing accepts your color format (hex, rgb, named colors).

### Problem: Plugin not loading

- Check file permissions and Python syntax.
- Ensure plugin class is uppercase and inherits `PluginBase`.
- Review logs for `PluginError`.

### Problem: Report generation fails

- Verify `output_path` parent directory exists.
- Check for `ReportGenerationError` in logs.
- Ensure `fmt` matches a supported `ReportFormat`.

### Problem: Batch audit hangs

- Reduce `concurrency` in async batch.
- Increase `timeout` for slow endpoints.
- Verify network connectivity.

---

---

## Appendix: WCAG Quick Reference

### perceivable

- 1.1.1 Non-text Content
- 1.2.1 Audio-only and Video-only
- 1.2.2 Captions (Prerecorded)
- 1.2.3 Audio Description or Media Alternative
- 1.3.1 Info and Relationships
- 1.3.2 Meaningful Sequence
- 1.4.1 Use of Color
- 1.4.2 Audio Control
- 1.4.3 Contrast (Minimum)
- 1.4.4 Resize Text
- 1.4.5 Images of Text
- 1.4.10 Reflow
- 1.4.11 Non-text Contrast
- 1.4.12 Text Spacing
- 1.4.13 Content on Hover or Focus

### operable

- 2.1.1 Keyboard
- 2.1.2 No Keyboard Trap
- 2.1.4 Character Key Shortcuts
- 2.2.1 Timing Adjustable
- 2.2.2 Pause, Stop, Hide
- 2.3.1 Three Flashes or Below Threshold
- 2.4.1 Bypass Blocks
- 2.4.2 Page Titled
- 2.4.3 Focus Order
- 2.4.4 Link Purpose (In Context)
- 2.4.5 Multiple Ways
- 2.4.6 Headings and Labels
- 2.4.7 Focus Visible
- 2.5.1 Pointer Gestures
- 2.5.2 Pointer Cancellation
- 2.5.3 Label in Name
- 2.5.4 Motion Actuation

### understandable

- 3.1.1 Language of Page
- 3.1.2 Language of Parts
- 3.2.1 On Focus
- 3.2.2 On Input
- 3.3.1 Error Identification
- 3.3.2 Labels or Instructions
- 3.3.3 Error Suggestion
- 3.3.4 Error Prevention

### robust

- 4.1.1 Parsing
- 4.1.2 Name, Role, Value
- 4.1.3 Status Messages

---

---

## Advanced Rules & Patterns

### Pattern: Live Region Validation

```python
# Detects incorrect aria-live usage
# Rules:
# - aria-live="polite" on frequently updating elements causes announcement fatigue
# - aria-live="assertive" should be reserved for critical alerts only
# - aria-atomic="false" on live regions causes partial announcements
```

### Pattern: Focus Management in SPAs

```python
# When auditing SPAs, check for:
# 1. Focus moved to new content after route change
# 2. Focus trap in modals with Escape key handler
# 3. Focus restoration after modal close
# 4. Inert background content during modal (inert attribute or aria-hidden)
```

### Pattern: Error Identification

```python
# Form validation errors should:
# - Be associated with the input via aria-describedby
# - Be announced via aria-live region
# - Be specified in the input's aria-invalid state
# - Have role="alert" on the error container
```

### Pattern: Accessible Names

```python
# Accessible name computation order:
# 1. aria-labelledby
# 2. aria-label
# 3. Native element text content
# 4. title attribute (last resort, inconsistent support)
# 5. aria-describedby (supplementary, not primary name)
```

---

---

## Remediation Playbook

### Playbook: Missing Alt Text

**Detection**: `img-missing-alt`, `img-alt-presentation`

**Impact**: Screen readers announce "image" with no context, or announce decorative content unnecessarily.

**Fix**:
```html
<!-- Before -->
<img src="chart.png">

<!-- After (informative) -->
<img src="chart.png" alt="Bar chart showing Q1 revenue of $1.2M, up 15% from Q4">

<!-- After (decorative) -->
<img src="divider.png" alt="" role="presentation">
```

**Effort**: 1-3 minutes per image.

### Playbook: Generic Links

**Detection**: `link-generic`

**Impact**: Screen reader users tabbing through links hear "Read more" repeatedly without context.

**Fix**:
```html
<!-- Before -->
<a href="/products">Read more</a>

<!-- After -->
<a href="/products">Read more about our product catalog</a>
```

**Effort**: 1-2 minutes per link.

### Playbook: Missing Form Labels

**Detection**: `form-no-label`

**Impact**: Screen reader users cannot determine the purpose of form inputs.

**Fix**:
```html
<!-- Before -->
<input type="email" placeholder="Enter your email">

<!-- After (preferred) -->
<label for="email">Email address</label>
<input type="email" id="email">

<!-- After (alternative) -->
<input type="email" aria-label="Email address">
```

**Effort**: 2-5 minutes per input.

### Playbook: Focus Indicator Removed

**Detection**: `focus-outline-removed`

**Impact**: Keyboard users cannot determine which element is currently focused.

**Fix**:
```css
/* Before */
button:focus { outline: none; }

/* After */
button:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

**Effort**: 1-5 minutes per stylesheet.

### Playbook: Incorrect Heading Structure

**Detection**: `heading-skip`, `multiple-h1`

**Impact**: Screen reader users navigating by headings miss content sections.

**Fix**:
```html
<!-- Before -->
<h1>Page Title</h1>
<h3>Section</h3>
<h1>Another Title</h1>

<!-- After -->
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

**Effort**: 5-15 minutes per page.

### Playbook: Keyboard Trap

**Detection**: `missing-aria-modal`, keyboard trap patterns

**Impact**: Keyboard users cannot exit a modal dialog.

**Fix**:
```html
<!-- Before -->
<div class="modal">
  <div class="modal-content">...</div>
</div>

<!-- After -->
<div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <!-- Focus trap implementation in JS -->
  <div class="modal-content">...</div>
</div>
```

**Effort**: 10-30 minutes per dialog (includes JS).

### Playbook: Insufficient Color Contrast

**Detection**: `color-contrast`

**Impact**: Users with low vision or color blindness cannot read text.

**Fix**:
```css
/* Before - 2.5:1 ratio */
.text { color: #767676; background: #ffffff; }

/* After - 4.7:1 ratio (WCAG AA) */
.text { color: #595959; background: #ffffff; }

/* For large text (18pt+): 3:1 minimum */
.heading { color: #767676; background: #ffffff; } /* 3.0:1 passes AA */
```

**Effort**: 2-10 minutes per color pair.

### Playbook: Missing Skip Link

**Detection**: `no-skip-link`

**Impact**: Keyboard users must tab through navigation on every page load.

**Fix**:
```html
<!-- Add as first focusable element in body -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  z-index: 100;
}
.skip-link:focus {
  top: 0;
}
</style>
```

**Effort**: 5-10 minutes per page.

---

---

## Testing Strategies

### Unit Testing Analyzers

```python
import pytest
from agents.accessibility.agent import (
    AccessibilityAgent,
    SemanticAnalyzer,
    AccessibilityIssue,
    IssueSeverity,
)

def test_missing_alt_detected():
    html = '<img src="photo.jpg">'
    analyzer = SemanticAnalyzer()
    # Requires DOMNode construction or integration test
    # Prefer integration via agent.audit_html()
    agent = AccessibilityAgent()
    result = agent.audit_html(html)
    assert any(i.category.value == "images" for i in result.issues)

def test_heading_hierarchy():
    html = '<h1>Title</h1><h3>Skip</h3>'
    agent = AccessibilityAgent()
    result = agent.audit_html(html)
    assert any("Heading level skipped" in i.description for i in result.issues)
```

### Integration Testing Full Pipeline

```python
from pathlib import Path
from agents.accessibility.agent import AccessibilityAgent, Config

def test_sample_page():
    html = Path("tests/fixtures/sample.html").read_text()
    agent = AccessibilityAgent(config=Config(generate_report=False))
    result = agent.audit_html(html)

    # Assertions on score distribution
    assert 0 <= result.score <= 100
    assert isinstance(result.issues, list)

    # Assert all severities represented
    severities = {i.severity for i in result.issues}
    assert all(s in severities for s in [
        IssueSeverity.CRITICAL,
        IssueSeverity.HIGH,
        IssueSeverity.MEDIUM,
        IssueSeverity.LOW,
    ])
```

### Snapshot Testing Reports

```python
import hashlib

def test_report_snapshot():
    html = "<html><head><title>Test</title></head><body><h1>Hi</h1></body></html>"
    agent = AccessibilityAgent()
    result = agent.audit_html(html)
    report = agent.generate_report(result, fmt="markdown")

    # Deterministic snapshot
    snapshot_hash = hashlib.sha256(report.encode()).hexdigest()
    assert snapshot_hash == "expected_hash_here"
```

---

---

## Migration Guides

### From axe-core CLI

```bash
# axe-core
npx axe https://example.com

# Accessibility Agent
python -m agents.accessibility.agent https://example.com --format json
```

### From WAVE API

```python
# WAVE returns JSON with different schema
# Map WAVE categories to agent's IssueSeverity:
# - Error -> CRITICAL
# - Contrast Error -> HIGH
# - Alert -> MEDIUM
# - Feature -> LOW
# - Structural -> MEDIUM
```

### From Pa11y

```python
# Pa11y JSON output
# Directly compatible with agent's JSON report schema
# Replace pa11y calls with agent.audit_html()
```

---

---

## Best Practices

### 1. Run Early and Often

Integrate the agent into:

- Local development (pre-commit hook or watch script).
- CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins).
- Pre-production deployment gates.

### 2. Prioritize by Severity

Use the built-in severity system:

```
CRITICAL > HIGH > MEDIUM > LOW
```

Fix CRITICAL issues before any other work.

### 3. Track Score Over Time

Enable `AuditHistory` and monitor trends:

```python
trend = agent.get_history()
scores = [h["score"] for h in trend]
# Plot scores to visualize accessibility debt
```

### 4. Use Multiple Formats

- HTML for stakeholders.
- Markdown for PR comments.
- JSON for automation.
- JUnit XML for CI gates.
- CSV for spreadsheets.

### 5. Train Your Team

- Share GROK.md with developers.
- Add `audit_html()` examples to onboarding docs.
- Run accessibility workshops with agent output.

### 6. Combine with Manual Testing

Automated audits catch ~30-40% of issues. Complement with:

- Screen reader testing (NVDA, JAWS, VoiceOver).
- Keyboard-only navigation testing.
- User testing with people with disabilities.

---

---

## Glossary

### A

- **ARIA**: Accessible Rich Internet Applications - W3C specification for enhancing HTML accessibility.
- **AT**: Assistive Technology - software/hardware used by people with disabilities.

### C

- **Contrast Ratio**: `(L1 + 0.05) / (L2 + 0.05)` where L is relative luminance.
- **CPA**: Cost Per Action/Acquisition - not directly related, but see `issue.score_penalty`.

### D

- **DOM**: Document Object Model - tree representation of HTML document.
- **Dynamically Generated Content**: Content rendered by JavaScript after initial page load.

### F

- **Focus**: The currently active UI element receiving keyboard input.
- **Focus Trap**: A situation where keyboard focus cannot move beyond a certain region.

### H

- **HTML Parser**: Converts HTML string to DOMNode tree.
- **Heading Hierarchy**: Proper nesting of h1-h6 elements.

### K

- **Keyboard Navigation**: Using Tab, Shift+Tab, Arrow keys, Enter, Escape to interact.

### L

- **Landmark**: ARIA region role identifying page structure.
- **Lighthouse**: Google's automated tool for page quality (includes accessibility audits).

### M

- **Marquee**: Deprecated HTML element - flagged by plugins.

### P

- **Plugin**: Custom rule extending the agent's capabilities.
- **Protanopia**: Red-blind color vision deficiency.

### R

- **Remediation**: The act of fixing an accessibility issue.
- **ROI**: Return on Investment - accessibility improvements have strong ROI through expanded audience.

### S

- **Screen Reader**: Software that reads screen content aloud (NVDA, JAWS, VoiceOver, TalkBack).
- **Semantic HTML**: Using correct HTML elements for their intended purpose.
- **Skip Link**: Link to bypass repetitive navigation and jump to main content.
- **SSRF**: Server-Side Request Forgery - relevant to `audit(url)` security.

### T

- **Tab Order**: Sequence in which elements receive focus when Tab is pressed.
- **Tabbing**: Navigating interactive elements via keyboard.

### W

- **WCAG**: Web Content Accessibility Guidelines.
- **WAI-ARIA**: W3C's ARIA specification.
- **WAVE**: Web Accessibility Evaluation Tool.

### X

- **XPath**: XML Path Language - selector syntax used to locate DOM nodes.

---

---

## Version History

- **v2.1.0** (2026-06-03)
  - Full rewrite with multi-standard support.
  - New analyzer architecture.
  - Multi-format reporting.
  - Plugin system.
  - Batch and async operations.
  - Comprehensive documentation.

- **v1.0.0** (2024-01-01)
  - Initial release.
  - Basic HTML parsing.
  - Simple issue detection.
  - Markdown reports.

---

---

*Accessibility Agent GROK.md - Built for the Awesome Grok Skills ecosystem.*

*Last updated: 2026-06-03*

*Maintained by the Accessibility Agent team and Grok community.*
