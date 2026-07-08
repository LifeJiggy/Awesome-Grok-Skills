---
name: "Localization Agent"
version: "2.0.0"
description: "Comprehensive localization platform covering translation memory, i18n engineering, cultural adaptation, quality assurance, terminology management, and project workflows"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["localization", "i18n", "l10n", "translation", "cultural-adaptation", "quality-assurance", "terminology", "multi-language"]
category: "localization"
personality: "localization-manager"
use_cases: ["translation-management", "i18n-engineering", "cultural-adaptation", "quality-assurance", "terminology-management", "project-orchestration"]
complexity: "advanced"
dependencies: ["python>=3.8"]
---

# Localization Agent

> Ship software globally with consistent quality, cultural relevance, and efficient translation workflows.

## Core Principles

1. **Translation Memory is Leverage**: Never translate the same string twice — TM saves time and money.
2. **Cultural Adaptation > Translation**: Word-for-word is not enough — adapt for cultural context.
3. **Quality at Every Step**: QA checks run automatically — catch issues before they ship.
4. **Terminology Consistency**: Use the right terms everywhere — glossaries enforce consistency.
5. **Locale-Aware Formatting**: Numbers, dates, currencies must respect local conventions.

## Capabilities

### Translation Memory Engine

```python
from agents.localization.agent import LocalizationAgent, MatchType

agent = LocalizationAgent()

# Add TM entries
agent.tm_engine.add_entry("Hello World", "Hola Mundo", "en", "es", "greeting")
agent.tm_engine.add_entry("Welcome back", "Bienvenido de nuevo", "en", "es", "greeting")

# Find matches
matches = agent.tm_engine.find_matches("Hello World!", "en", "es")
# → [{"score": 0.95, "match_type": "fuzzy_95", "target": "Hola Mundo"}]

# Leverage analysis
leverage = agent.tm_engine.get_leverage_stats("en", "es", [
    "Hello World", "Welcome back", "Goodbye", "Thank you",
])
# → {"leverage_percent": 50.0, "cost_savings_estimate": "50%"}
```

**Match Types:**
| Type | Score | Cost | Description |
|------|-------|------|-------------|
| EXACT | 100% | 0% | Identical source |
| FUZZY_95 | 95-99% | 10% | Near-identical |
| FUZZY_85 | 85-94% | 30% | Similar structure |
| FUZZY_75 | 75-84% | 50% | Partial match |
| MT | N/A | 60% | Machine translation |
| NEW | 0% | 100% | No match |

**Leverage Formula:**
```
leverage = (exact + fuzzy × 0.75) / total × 100%
```

### i18n Engineering

```python
# Register locales
agent.i18n_engine.register_locale("es-ES", "es", "ES", currency="EUR", currency_symbol="€")
agent.i18n_engine.register_locale("ar-SA", "ar", "SA")  # RTL

# Format numbers
agent.i18n_engine.format_number(1234.56, "es-ES")  # → "1.234,56"

# Format currency
agent.i18n_engine.format_currency(99.99, "es-ES")  # → "99,99 €"

# Format dates
from datetime import datetime
agent.i18n_engine.format_date(datetime(2026, 12, 31), "es-ES")  # → "31/12/2026"

# RTL support check
rtl = agent.i18n_engine.check_rtl_support("ar-SA")
# → {"needs_rtl": True, "layout_flipping": True}

# Pseudo-localization for UI testing
pseudo = agent.i18n_engine.generate_pseudo_localization(
    {"hello": "Hello", "welcome": "Welcome"},
    target_locale="fr-FR",
)
# → {"hello": "¡Ĥéľļó", "welcome": "Ŵéľćőɱé"}
```

**Locale Formatting:**
| Locale | Number | Currency | Date |
|--------|--------|----------|------|
| en-US | 1,234.56 | $1,234.56 | 12/31/2026 |
| es-ES | 1.234,56 | 1.234,56 € | 31/12/2026 |
| de-DE | 1.234,56 | 1.234,56 € | 31.12.2026 |
| ar-SA | ١٬٢٣٤٫٥٦ | ١٬٢٣٤٫٥٦ ر.س | 31/12/2026 |

### Cultural Adaptation

```python
# Register style guide
agent.cultural_engine.register_style_guide(
    language="es",
    tone="warm",
    formality="formal",
    rules=[
        {"type": "pronoun", "rule": "Use 'usted' in B2B contexts"},
        {"type": "formality", "rule": "Avoid slang in business communications"},
    ],
)

# Add cultural rules
agent.cultural_engine.add_cultural_rule("ja", "honorifics", "Use keigo for B2B")
agent.cultural_engine.add_cultural_rule("de", "formality", "Use 'Sie' in business")

# Adapt content
adaptation = agent.cultural_engine.adapt_content("Buy now", "en", "es-ES")
# → {"adaptations_needed": ["Apply formal register", "Cultural rule: Use usted in B2B"]}
```

### Quality Assurance

```python
from agents.localization.agent import TranslationUnit, TerminologyEntry

units = [
    TranslationUnit(
        unit_id="U1", key="greeting", source_text="Hello {name}",
        target_language="es", translated_text="Hola {name}",
    ),
    TranslationUnit(
        unit_id="U2", key="farewell", source_text="Goodbye",
        target_language="es", translated_text="",
    ),
    TranslationUnit(
        unit_id="U3", key="button", source_text="Click here to continue",
        target_language="es", translated_text="Haga clic aquí para continuar y seguir adelante y avanzar más",
    ),
]

glossary = [
    TerminologyEntry(
        term_id="T1", source_term="button", target_term="botón",
        source_language="en", target_language="es",
    ),
]

# Run full QA
qa = agent.qa_engine.run_full_qa(units, glossary)
# → {"total_issues": 5, "by_severity": {"critical": 1, "high": 2, "medium": 1, "low": 1}, "pass_rate": 50.0}
```

**QA Check Types:**
| Check | Severity | Auto-Fix | Description |
|-------|----------|----------|-------------|
| MISSING_TRANSLATION | CRITICAL | No | Empty target |
| PLACEHOLDER_MISMATCH | HIGH | Partial | {var} missing |
| LENGTH_ISSUE | MEDIUM | No | Over character limit |
| GLOSSARY_VIOLATION | HIGH | No | Wrong term used |
| STYLE_VIOLATION | MEDIUM | No | Tone mismatch |

### Project Management

```python
project = agent.project_manager.create_project(
    name="Product Launch ES",
    source_language="en",
    target_languages=["es", "fr", "de"],
    total_strings=5000,
    team=["translator-es", "reviewer-es", "translator-fr"],
    deadline=datetime(2026, 9, 1),
)

# Advance through phases
agent.project_manager.advance_phase(project.project_id)

# Update progress
agent.project_manager.update_progress(project.project_id, "es", translated=1000, reviewed=500, approved=400)

# Get status
status = agent.project_manager.get_project_status(project.project_id)
# → {"overall_progress": 8.0, "phase": "extraction", "days_remaining": 57}
```

**Project Phases:**
```
PLANNING → EXTRACTION → TRANSLATION → REVIEW → QA → INTEGRATION → LAUNCH → POST_LAUNCH
```

## Data Models

### TranslationUnit
| Field | Type | Description |
|-------|------|-------------|
| unit_id | str | Unique identifier |
| key | str | String key |
| source_text | str | Source language text |
| translated_text | str | Target language text |
| status | TranslationStatus | PENDING → PUBLISHED |
| match_type | MatchType | EXACT, FUZZY_XX, MT, NEW |

### TranslationMemoryEntry
| Field | Type | Description |
|-------|------|-------------|
| entry_id | str | Unique identifier |
| source_text | str | Source text |
| target_text | str | Translation |
| approved | bool | TM entry approved |
| usage_count | int | Times used |

### QAIssue
| Field | Type | Description |
|-------|------|-------------|
| issue_id | str | Unique identifier |
| check_type | QACheckType | MISSING, PLACEHOLDER, LENGTH, etc. |
| severity | QASeverity | CRITICAL, HIGH, MEDIUM, LOW |
| auto_fixable | bool | Can be auto-fixed |

## Checklists

### Localization Project Setup
- [ ] Define source and target languages
- [ ] Extract translatable strings
- [ ] Set up translation memory
- [ ] Load glossary/terminology
- [ ] Configure style guides
- [ ] Set quality thresholds
- [ ] Define workflow steps
- [ ] Assign team members

### Translation Workflow
- [ ] TM leverage analysis complete
- [ ] Untranslated strings identified
- [ ] Translation assigned to linguists
- [ ] Translations submitted
- [ ] Review completed
- [ ] QA checks passed
- [ ] Glossary compliance verified
- [ ] Integrations tested

### Pre-Launch QA
- [ ] All strings translated
- [ ] QA pass rate >= 95%
- [ ] No critical issues
- [ ] Placeholder consistency verified
- [ ] Character limits respected
- [ ] RTL layout tested
- [ ] Date/number formatting verified
- [ ] Cultural adaptation reviewed

## Troubleshooting

### Low TM Leverage
- Check if source strings have changed significantly
- Verify TM contains relevant entries
- Consider fuzzy match threshold adjustment
- Review TM domain assignment

### QA Pass Rate Too Low
- Check for systematic issues (placeholders, glossary)
- Review translator training needs
- Verify style guide clarity
- Check source string quality

### Cultural Issues Not Caught
- Review cultural rule coverage
- Add more locale-specific rules
- Involve native reviewers earlier
- Check style guide completeness

### Project Behind Schedule
- Review phase transition bottlenecks
- Check team capacity and workload
- Consider splitting work by language
- Adjust deadlines if needed
