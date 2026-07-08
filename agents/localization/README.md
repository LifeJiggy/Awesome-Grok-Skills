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
- [Architecture](#architecture)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [License](#license)

## Overview

The Localization Agent manages the complete localization lifecycle — from string extraction and translation memory leverage through cultural adaptation, quality assurance, and multi-market deployment. Built for product teams shipping software across languages and regions with consistency, quality, and efficiency.

Whether you're localizing a mobile app for 20 markets, translating documentation for enterprise clients, or adapting marketing content for different cultures, the Localization Agent provides the tools to manage your localization workflow efficiently.

## Features

### Translation Memory
- Fuzzy matching with configurable thresholds
- Leverage analysis (exact, fuzzy, MT, new)
- Usage tracking and approval management
- Domain-specific TM partitioning
- Cost savings estimation
- Maintenance reporting

### i18n Engineering
- Locale configuration (date, number, currency formatting)
- Pseudo-localization for UI testing
- RTL language support
- Resource file management
- Missing key detection
- Format conversion

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

### Terminology Management
- Glossary creation and management
- Forbidden term tracking
- Term search and discovery
- Category-based organization
- Multi-language support

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
print(f"Leverage: {leverage['leverage_percent']}%")

# Maintenance report
report = agent.tm_engine.maintenance_report()
print(f"Total entries: {report['total_entries']}")
```

### i18n Engineering

```python
# Register locales
agent.i18n_engine.register_locale("es-ES", "es", "ES", currency="EUR")
agent.i18n_engine.register_locale("ar-SA", "ar", "SA")  # RTL

# Format values
agent.i18n_engine.format_number(1234.56, "es-ES")   # → "1.234,56"
agent.i18n_engine.format_currency(99.99, "es-ES")    # → "99,99 €"
agent.i18n_engine.format_date(datetime(2026, 12, 31), "es-ES")  # → "31/12/2026"

# Pseudo-localization
pseudo = agent.i18n_engine.generate_pseudo_localization(
    {"hello": "Hello", "welcome": "Welcome"},
    target_locale="fr-FR",
)

# RTL check
rtl = agent.i18n_engine.check_rtl_support("ar-SA")
```

### Cultural Adaptation

```python
# Register style guide
agent.cultural_engine.register_style_guide("es", tone="warm", formality="formal")

# Add cultural rules
agent.cultural_engine.add_cultural_rule("ja", "honorifics", "Use keigo for B2B")
agent.cultural_engine.add_cultural_rule("de", "formality", "Use 'Sie' in business")

# Adapt content
adaptation = agent.cultural_engine.adapt_content("Buy now", "en", "es-ES")
print(f"Adaptations: {adaptation['adaptations_needed']}")
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
print(f"Issues: {qa['total_issues']}, Pass rate: {qa['pass_rate']}%")
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

status = agent.project_manager.get_project_status(project.project_id)
```

## API Reference

### TranslationMemoryEngine

| Method | Description |
|--------|-------------|
| `add_entry(source, target, src_lang, tgt_lang, domain)` | Add TM entry |
| `find_matches(text, src_lang, tgt_lang, limit)` | Find TM matches |
| `get_leverage_stats(src, tgt, texts)` | Analyze leverage |
| `maintenance_report()` | Get TM maintenance report |
| `update_entry(entry_id, **kwargs)` | Update TM entry |
| `delete_entry(entry_id)` | Delete TM entry |

### I18nEngine

| Method | Description |
|--------|-------------|
| `register_locale(locale, language, region, **kw)` | Register locale |
| `format_number(value, locale)` | Format number |
| `format_currency(value, locale)` | Format currency |
| `format_date(dt, locale)` | Format date |
| `generate_pseudo_localization(strings, locale)` | Generate pseudo-text |
| `check_rtl_support(locale)` | Check RTL support |
| `get_locale_config(locale)` | Get locale configuration |

### CulturalAdaptationEngine

| Method | Description |
|--------|-------------|
| `register_style_guide(language, tone, formality, rules)` | Register style guide |
| `add_cultural_rule(language, rule_type, rule)` | Add cultural rule |
| `adapt_content(text, source_lang, target_locale)` | Adapt content |
| `get_style_guide(language)` | Get style guide |
| `get_cultural_rules(language)` | Get cultural rules |

### QualityAssuranceEngine

| Method | Description |
|--------|-------------|
| `check_missing_translations(units)` | Find missing translations |
| `check_placeholder_consistency(units)` | Verify placeholders |
| `check_length_limits(units, max_ratio)` | Check length limits |
| `check_glossary_compliance(units, glossary)` | Verify glossary terms |
| `run_full_qa(units, glossary)` | Run all QA checks |
| `auto_fix_issues(issues)` | Auto-fix fixable issues |

### TerminologyManager

| Method | Description |
|--------|-------------|
| `add_term(source, target, src_lang, tgt_lang, **kw)` | Add term |
| `search_terms(query, language, category)` | Search terms |
| `get_forbidden_terms(language)` | Get forbidden terms |
| `update_term(term_id, **kwargs)` | Update term |
| `delete_term(term_id)` | Delete term |

### LocalizationProjectManager

| Method | Description |
|--------|-------------|
| `create_project(name, src, targets, **kw)` | Create project |
| `advance_phase(project_id)` | Advance to next phase |
| `update_progress(project_id, lang, trans, rev, app)` | Update progress |
| `get_project_status(project_id)` | Get project status |
| `get_portfolio_overview()` | Get all projects |

## Examples

### Full Localization Workflow

```python
from agents.localization.agent import LocalizationAgent, TranslationUnit, TerminologyEntry
from datetime import datetime

agent = LocalizationAgent()

# 1. Set up TM
agent.tm_engine.add_entry("Hello", "Hola", "en", "es", "greeting")
agent.tm_engine.add_entry("Thank you", "Gracias", "en", "es", "common")
agent.tm_engine.add_entry("Goodbye", "Adiós", "en", "es", "common")

# 2. Register locales
agent.i18n_engine.register_locale("es-ES", "es", "ES", currency="EUR")
agent.i18n_engine.register_locale("fr-FR", "fr", "FR", currency="EUR")

# 3. Set up terminology
agent.terminology_manager.add_term("button", "botón", "en", "es", category="ui")
agent.terminology_manager.add_term("submit", "enviar", "en", "es", category="ui")

# 4. Configure cultural rules
agent.cultural_engine.register_style_guide("es", tone="warm", formality="formal")

# 5. Create project
project = agent.project_manager.create_project(
    name="App Localization",
    source_language="en",
    target_languages=["es", "fr"],
    total_strings=1000,
    deadline=datetime(2026, 10, 1),
)

# 6. Process translations
units = [
    TranslationUnit(unit_id="U1", key="greeting", source_text="Hello {name}",
                    target_language="es", translated_text="Hola {name}"),
    TranslationUnit(unit_id="U2", key="thanks", source_text="Thank you",
                    target_language="es", translated_text="Gracias"),
]

# 7. Run QA
glossary = [
    TerminologyEntry(term_id="T1", source_term="button", target_term="botón",
                     source_language="en", target_language="es"),
]
qa = agent.qa_engine.run_full_qa(units, glossary)
print(f"QA: {qa['pass_rate']}% pass rate")

# 8. Get metrics
leverage = agent.tm_engine.get_leverage_stats("en", "es", ["Hello", "Thank you", "New string"])
print(f"TM Leverage: {leverage['leverage_percent']}%")
```

### Multi-Market Launch

```python
# Launch in 5 markets simultaneously
markets = {
    "es-ES": {"currency": "EUR", "tone": "formal"},
    "fr-FR": {"currency": "EUR", "tone": "formal"},
    "de-DE": {"currency": "EUR", "tone": "formal"},
    "ja-JP": {"currency": "JPY", "tone": "polite"},
    "ar-SA": {"currency": "SAR", "tone": "formal"},
}

# Register all locales
for locale, config in markets.items():
    lang, region = locale.split("-")
    agent.i18n_engine.register_locale(locale, lang, region, currency=config["currency"])

# Create multi-market project
project = agent.project_manager.create_project(
    name="Global Launch",
    source_language="en",
    target_languages=list(markets.keys()),
    total_strings=5000,
)

# Process each market
for locale in markets.keys():
    lang = locale.split("-")[0]
    agent.project_manager.update_progress(project.project_id, lang, translated=1000, reviewed=500)
```

## Configuration

```python
agent = LocalizationAgent(config={
    "fuzzy_threshold": 0.75,
    "max_character_ratio": 1.5,
    "default_source_language": "en",
    "qa_pass_rate_threshold": 95.0,
    "tm_max_entries": 1000000,
    "project_max_languages": 50,
    "style_guide_required": True,
    "glossary_enforcement": True,
})
```

### Configuration Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| fuzzy_threshold | 0.75 | Minimum fuzzy match score |
| max_character_ratio | 1.5 | Max target/source character ratio |
| default_source_language | en | Default source language |
| qa_pass_rate_threshold | 95.0 | Minimum QA pass rate |
| tm_max_entries | 1000000 | Maximum TM entries |
| project_max_languages | 50 | Maximum target languages |
| style_guide_required | True | Require style guides |
| glossary_enforcement | True | Enforce glossary terms |

## Architecture

For detailed architecture documentation, see [ARCHITECTURE.md](./ARCHITECTURE.md).

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Localization Agent                        │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│     TM      │    i18n     │  Cultural   │    Quality       │
│   Engine    │   Engine    │  Adaptation │  Assurance       │
├─────────────┼─────────────┼─────────────┼──────────────────┤
│ - Store     │ - Locale    │ - Style     │ - Missing        │
│ - Match     │ - Format    │ - Rules     │ - Placeholder    │
│ - Leverage  │ - Pseudo    │ - Adapt     │ - Length         │
│ - Maintain  │ - RTL       │ - Tone      │ - Glossary       │
├─────────────┴─────────────┴─────────────┴──────────────────┤
│                  Terminology Management                     │
│  - Glossary  - Forbidden  - Search  - Categories           │
├─────────────────────────────────────────────────────────────┤
│                  Project Management                         │
│  - Workflow  - Progress  - Deadlines  - Team                │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

### Translation Memory
1. **Build TM early** — leverage grows with every translation
2. **Use domain tags** — partition TM by content type
3. **Review fuzzy matches** — don't accept blindly
4. **Maintain TM regularly** — clean up outdated entries
5. **Monitor leverage** — track cost savings

### i18n Engineering
6. **Pseudo-localize for testing** — find layout issues early
7. **Test RTL layouts** — don't assume LTR
8. **Verify locale formatting** — numbers, dates, currencies
9. **Check character encoding** — UTF-8 everywhere
10. **Use resource files** — separate strings from code

### Cultural Adaptation
11. **Adapt, don't just translate** — cultural context matters
12. **Use native reviewers** — catch cultural issues
13. **Create style guides** — ensure consistency
14. **Respect local norms** — avoid cultural faux pas
15. **Test with local users** — validate adaptations

### Quality Assurance
16. **Run QA before review** — catch mechanical issues first
17. **Set quality thresholds** — enforce minimum standards
18. **Track QA metrics** — measure improvement over time
19. **Auto-fix when possible** — save reviewer time
20. **Review QA rules regularly** — keep checks relevant

### Project Management
21. **Plan phases carefully** — avoid bottlenecks
22. **Track progress daily** — catch delays early
23. **Communicate with team** — keep everyone aligned
24. **Set realistic deadlines** — account for review cycles
25. **Document decisions** — maintain project history

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Low TM leverage | Source strings changed, TM outdated | Update TM, adjust fuzzy threshold |
| QA pass rate low | Systematic issues, unclear guidelines | Review guidelines, train translators |
| Cultural issues missed | Incomplete rules, no native review | Add rules, involve native reviewers |
| Project behind schedule | Bottlenecks, capacity issues | Review workflow, adjust deadlines |
| Formatting issues | Locale misconfigured, wrong patterns | Verify locale settings, test formats |
| Integration problems | Missing strings, wrong format | Check extraction, validate format |
| Glossary non-compliance | Terms not enforced, unclear definitions | Enable enforcement, clarify definitions |

## FAQ

**Q: How does fuzzy matching work?**
A: The system uses Jaccard similarity to compare word sets between source strings. A score of 0.95 means 95% word overlap, requiring minimal editing.

**Q: What is pseudo-localization?**
A: Pseudo-localization expands and modifies source strings to simulate translated text. It helps identify UI layout issues before real translations exist.

**Q: How do I handle RTL languages?**
A: Register RTL locales (ar, he, fa, ur) and the system will configure appropriate text direction, layout flipping, and alignment.

**Q: Can I customize QA checks?**
A: Yes. The system supports configurable thresholds and custom check types via extension.

**Q: How do I measure localization ROI?**
A: Use the leverage analysis to calculate cost savings from TM matches. Higher leverage = lower translation costs.

**Q: What's the difference between translation and localization?**
A: Translation is word-for-word conversion. Localization includes cultural adaptation, formatting, and context-appropriate modifications.

## License

MIT License - see LICENSE file for details.
