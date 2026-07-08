# Localization Agent

> Comprehensive localization platform covering translation memory, i18n engineering, cultural adaptation, quality assurance, terminology management, and project workflows.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Localization Agent manages the complete localization lifecycle — from string extraction and translation memory leverage through cultural adaptation, quality assurance, and multi-market deployment. Built for product teams shipping software across languages and regions with consistency, quality, and efficiency.

## Features

### Translation Memory
- Fuzzy matching with configurable thresholds
- Leverage analysis (exact, fuzzy, MT, new)
- Usage tracking and approval management
- Domain-specific TM partitioning
- Cost savings estimation

### i18n Engineering
- Locale configuration (date, number, currency formatting)
- Pseudo-localization for UI testing
- RTL language support
- Resource file management
- Missing key detection

### Cultural Adaptation
- Style guide management per language
- Cultural rules and禁忌 tracking
- Tone and formality control
- Content adaptation recommendations
- Brand voice enforcement

### Quality Assurance
- Automated QA checks (missing, placeholder, length, glossary)
- Severity-based issue tracking (CRITICAL → LOW)
- Auto-fix capabilities for some issues
- Pass rate calculation
- Glossary compliance verification

### Project Management
- Phase-based workflow (PLANNING → POST_LAUNCH)
- Progress tracking per language
- Deadline management
- Team coordination
- Portfolio overview

## Quick Start

### Installation

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Basic Usage

```python
from agents.localization.agent import LocalizationAgent, Language

agent = LocalizationAgent()

# Add TM entries
agent.tm_engine.add_entry("Hello World", "Hola Mundo", "en", "es")

# Find matches
matches = agent.tm_engine.find_matches("Hello World!", "en", "es")

# Register locale
agent.i18n_engine.register_locale("es-ES", "es", "ES", currency="EUR")

# Format
agent.i18n_engine.format_currency(99.99, "es-ES")  # → "99,99 €"

# Get dashboard
dashboard = agent.get_dashboard()
```

### Run the Demo

```bash
python agents/localization/agent.py
```

## Usage

### Translation Memory

```python
# Add entries
agent.tm_engine.add_entry("Thank you", "Gracias", "en", "es")
agent.tm_engine.add_entry("Goodbye", "Adiós", "en", "es")

# Find matches
matches = agent.tm_engine.find_matches("Thank you!", "en", "es")
# → [{"score": 0.95, "match_type": "fuzzy_95", "target": "Gracias"}]

# Leverage analysis
leverage = agent.tm_engine.get_leverage_stats("en", "es", [
    "Thank you", "Goodbye", "Hello", "Please",
])
```

### i18n Engineering

```python
# Register locales
agent.i18n_engine.register_locale("es-ES", "es", "ES", currency="EUR")
agent.i18n_engine.register_locale("ar-SA", "ar", "SA")  # RTL

# Format values
agent.i18n_engine.format_number(1234.56, "es-ES")   # → "1.234,56"
agent.i18n_engine.format_currency(99.99, "es-ES")    # → "99,99 €"

# Pseudo-localization
pseudo = agent.i18n_engine.generate_pseudo_localization(
    {"hello": "Hello", "welcome": "Welcome"},
    target_locale="fr-FR",
)
```

### Cultural Adaptation

```python
agent.cultural_engine.register_style_guide("es", tone="warm", formality="formal")
agent.cultural_engine.add_cultural_rule("ja", "honorifics", "Use keigo for B2B")

adaptation = agent.cultural_engine.adapt_content("Buy now", "en", "es-ES")
```

### Quality Assurance

```python
from agents.localization.agent import TranslationUnit

units = [
    TranslationUnit(unit_id="U1", key="greeting", source_text="Hello {name}",
                    target_language="es", translated_text="Hola {name}"),
    TranslationUnit(unit_id="U2", key="empty", source_text="Text",
                    target_language="es", translated_text=""),
]

qa = agent.qa_engine.run_full_qa(units)
# → {"total_issues": 1, "pass_rate": 50.0}
```

### Project Management

```python
project = agent.project_manager.create_project(
    name="Product Launch ES",
    source_language="en",
    target_languages=["es", "fr", "de"],
    total_strings=5000,
)

agent.project_manager.advance_phase(project.project_id)
agent.project_manager.update_progress(project.project_id, "es", translated=1000, reviewed=500, approved=400)
```

## API Reference

### TranslationMemoryEngine

| Method | Description |
|--------|-------------|
| `add_entry(source, target, src_lang, tgt_lang)` | Add TM entry |
| `find_matches(text, src_lang, tgt_lang)` | Find TM matches |
| `get_leverage_stats(src, tgt, texts)` | Analyze leverage |

### I18nEngine

| Method | Description |
|--------|-------------|
| `register_locale(locale, language, region)` | Register locale |
| `format_number(value, locale)` | Format number |
| `format_currency(value, locale)` | Format currency |
| `format_date(dt, locale)` | Format date |
| `generate_pseudo_localization(strings, locale)` | Generate pseudo-text |

### QualityAssuranceEngine

| Method | Description |
|--------|-------------|
| `check_missing_translations(units)` | Find missing translations |
| `check_placeholder_consistency(units)` | Verify placeholders |
| `check_length_limits(units, max_ratio)` | Check length limits |
| `check_glossary_compliance(units, glossary)` | Verify glossary terms |
| `run_full_qa(units, glossary)` | Run all QA checks |

### LocalizationProjectManager

| Method | Description |
|--------|-------------|
| `create_project(name, src, targets, **kw)` | Create project |
| `advance_phase(project_id)` | Advance to next phase |
| `update_progress(project_id, lang, trans, rev, app)` | Update progress |
| `get_project_status(project_id)` | Get project status |

## Examples

See the full demo in `agent.py`.

## Configuration

```python
agent = LocalizationAgent(config={"fuzzy_threshold": 0.80})
```

## Best Practices

1. **Build TM early** — leverage grows with every translation
2. **Use glossaries** — enforce consistent terminology
3. **Run QA before review** — catch mechanical issues first
4. **Adapt, don't just translate** — cultural context matters
5. **Pseudo-localize for testing** — find layout issues early
6. **Track leverage** — measure cost savings from TM

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Low TM leverage | Check source string changes, adjust threshold |
| QA pass rate low | Review systematic issues (placeholders, glossary) |
| Cultural issues missed | Add more locale-specific rules |
| Project behind schedule | Review phase bottlenecks, consider splitting work |

## License

MIT License - see LICENSE file for details.
