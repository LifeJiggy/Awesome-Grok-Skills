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

The Localization Agent provides a complete internationalization and localization platform for product teams shipping software across languages and regions. It manages translation memory with fuzzy matching, locale-aware formatting, cultural adaptation, automated quality assurance, terminology consistency, and multi-market project orchestration.

---

## Core Principles

1. **Translation Memory is Leverage**: Never translate the same string twice — TM saves time and money.
2. **Cultural Adaptation > Translation**: Word-for-word is not enough — adapt for cultural context.
3. **Quality at Every Step**: QA checks run automatically — catch issues before they ship.
4. **Terminology Consistency**: Use the right terms everywhere — glossaries enforce consistency.
5. **Locale-Aware Formatting**: Numbers, dates, currencies must respect local conventions.

---

## Capabilities

### 1. Translation Memory Engine

Store and retrieve previous translations to maximize leverage and consistency.

```python
from agents.localization.agent import LocalizationAgent, MatchType

agent = LocalizationAgent()

# Add TM entries
agent.tm_engine.add_entry("Hello World", "Hola Mundo", "en", "es", "greeting")
agent.tm_engine.add_entry("Welcome back", "Bienvenido de nuevo", "en", "es", "greeting")
agent.tm_engine.add_entry("Thank you", "Gracias", "en", "es", "common")

# Find matches
matches = agent.tm_engine.find_matches("Hello World!", "en", "es")
# → [{"score": 0.95, "match_type": "fuzzy_95", "target": "Hola Mundo", "entry_id": "TM-XXX"}]

# Leverage analysis
leverage = agent.tm_engine.get_leverage_stats("en", "es", [
    "Hello World", "Welcome back", "Goodbye", "Thank you",
])
print(f"Leverage: {leverage['leverage_percent']}%")
# → Leverage: 50.0%
print(f"Cost savings: {leverage['cost_savings_estimate']}")
# → Cost savings: 50%

# Maintenance report
report = agent.tm_engine.maintenance_report()
print(f"Total entries: {report['total_entries']}")
# → Total entries: 100,000
```

**Match Types:**

| Type | Score | Cost | Description |
|------|-------|------|-------------|
| EXACT | 100% | 0% | Identical source text |
| FUZZY_95 | 95-99% | 10% | Near-identical, minimal editing |
| FUZZY_85 | 85-94% | 30% | Similar structure, light editing |
| FUZZY_75 | 75-84% | 50% | Partial match, moderate editing |
| MT | N/A | 60% | Machine translation + post-edit |
| NEW | 0% | 100% | No match, full translation |

**Leverage Formula:**
```
leverage = (exact_count + fuzzy_count × 0.75) / total_strings × 100%
```

**Fuzzy Match Algorithm (Jaccard Similarity):**
```
tokenize(text) → set of words (lowercased)
score = |intersection(words_a, words_b)| / |union(words_a, words_b)|

Example:
  "Hello World" vs "Hello World!" → {"hello", "world"} vs {"hello", "world", "!"}
  score = |{"hello", "world"}| / |{"hello", "world", "!"}| = 2/3 = 0.667
```

---

### 2. i18n Engineering

Configure locale-aware formatting, pseudo-localization, and RTL support.

```python
# Register locales
agent.i18n_engine.register_locale("es-ES", "es", "ES", currency="EUR", currency_symbol="€")
agent.i18n_engine.register_locale("ar-SA", "ar", "SA")  # RTL
agent.i18n_engine.register_locale("ja-JP", "ja", "JP", currency="JPY", currency_symbol="¥")

# Format numbers
agent.i18n_engine.format_number(1234.56, "es-ES")  # → "1.234,56"

# Format currency
agent.i18n_engine.format_currency(99.99, "es-ES")  # → "99,99 €"
agent.i18n_engine.format_currency(99.99, "ja-JP")  # → "¥99"

# Format dates
from datetime import datetime
agent.i18n_engine.format_date(datetime(2026, 12, 31), "es-ES")  # → "31/12/2026"
agent.i18n_engine.format_date(datetime(2026, 12, 31), "ja-JP")  # → "2026/12/31"

# RTL support check
rtl = agent.i18n_engine.check_rtl_support("ar-SA")
# → {"needs_rtl": True, "layout_flipping": True, "text_direction": "rtl"}

# Pseudo-localization for UI testing
pseudo = agent.i18n_engine.generate_pseudo_localization(
    {"hello": "Hello", "welcome": "Welcome"},
    target_locale="fr-FR",
)
# → {"hello": "¡Ĥéľļó", "welcome": "Ŵéľćőɱé"}
```

**Locale Formatting:**

| Locale | Number | Currency | Date | First Day |
|--------|--------|----------|------|-----------|
| en-US | 1,234.56 | $1,234.56 | 12/31/2026 | Sunday |
| es-ES | 1.234,56 | 1.234,56 € | 31/12/2026 | Monday |
| de-DE | 1.234,56 | 1.234,56 € | 31.12.2026 | Monday |
| ja-JP | 1,234.56 | ¥1,234 | 2026/12/31 | Sunday |
| ar-SA | ١٬٢٣٤٫٥٦ | ١٬٢٣٤٫٥٦ ر.س | 31/12/2026 | Saturday |
| zh-CN | 1,234.56 | ¥1,234.56 | 2026/12/31 | Monday |

**RTL Language Support:**
```
Languages requiring RTL: ar, he, fa, ur
  → HTML: <html dir="rtl" lang="ar">
  → CSS: logical properties (margin-inline-start vs margin-left)
  → Layout: mirrored navigation and icons
  → Text: right-aligned by default
```

**Pseudo-Localization Algorithm:**
```
For each source string:
  1. Expand vowels: "Hello" → "Ĥéľľó"
  2. Add padding: "Hello" → "¡Ĥéľľó!"
  3. For RTL: add RTL marks
  
Purpose: Test UI layout with longer, expanded text before real translations exist
```

---

### 3. Cultural Adaptation

Ensure content is culturally appropriate, not just linguistically correct.

```python
# Register style guide
agent.cultural_engine.register_style_guide(
    language="es",
    tone="warm",
    formality="formal",
    rules=[
        {"type": "pronoun", "rule": "Use 'usted' in B2B contexts"},
        {"type": "formality", "rule": "Avoid slang in business communications"},
        {"type": "address", "rule": "Use first name only for close colleagues"},
    ],
)

# Add cultural rules
agent.cultural_engine.add_cultural_rule("ja", "honorifics", "Use keigo for B2B")
agent.cultural_engine.add_cultural_rule("de", "formality", "Use 'Sie' in business")
agent.cultural_engine.add_cultural_rule("zh", "numerology", "Avoid number 4, prefer 8")
agent.cultural_engine.add_cultural_rule("ar", "religious", "Avoid pork/alcohol references")

# Adapt content
adaptation = agent.cultural_engine.adapt_content("Buy now", "en", "es-ES")
# → {
#   "original": "Buy now",
#   "target_locale": "es-ES",
#   "adaptations_needed": [
#     "Apply formal register",
#     "Cultural rule: Use usted in B2B"
#   ]
# }
```

**Style Guide Components:**

| Component | Description | Example |
|-----------|-------------|---------|
| tone | Emotional register | warm, professional, friendly |
| formality | Formality level | formal, informal, neutral |
| pronouns | Pronoun usage | usted (formal), tú (informal) |
| avoidance | Terms to avoid | slang, jargon, technical terms |
| brand_voice | Brand personality | friendly, authoritative, playful |

**Cultural Rules by Language:**

| Language | Rule Type | Description |
|----------|-----------|-------------|
| ja | honorifics | Use keigo for B2B contexts |
| ja | avoidance | Avoid direct "no" — use softer alternatives |
| de | formality | Use "Sie" in business communications |
| de | precision | Technical compound words are standard |
| zh | numerology | Avoid number 4, prefer 8 |
| ar | religious | Avoid pork/alcohol references |
| br | informality | "Voce" acceptable in most contexts |
| ko | hierarchy | Respect age/status in language |

---

### 4. Quality Assurance

Run automated checks to catch mechanical errors before human review.

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
# → {
#   "total_issues": 5,
#   "by_severity": {"critical": 1, "high": 2, "medium": 1, "low": 1},
#   "pass_rate": 50.0,
#   "issues": [...]
# }
```

**QA Check Types:**

| Check | Severity | Auto-Fix | Description |
|-------|----------|----------|-------------|
| MISSING_TRANSLATION | CRITICAL | No | Empty target text |
| PLACEHOLDER_MISMATCH | HIGH | Partial | {var} in source not in target |
| LENGTH_ISSUE | MEDIUM | No | Over character limit |
| GLOSSARY_VIOLATION | HIGH | No | Wrong term used |
| STYLE_VIOLATION | MEDIUM | No | Formality/tone mismatch |
| ENCODING_ERROR | CRITICAL | Yes | Invalid Unicode |
| PLURAL_FORM | HIGH | Missing plural variants |
| NUMERIC_FORMAT | MEDIUM | Yes | Wrong number formatting |
| PUNCTUATION | LOW | Yes | Punctuation mismatch |

**QA Pass Rate Calculation:**
```
pass_rate = (1 - total_issues / total_units) × 100%
```

**Severity Distribution:**
```
CRITICAL issues → Block release
HIGH issues     → Require fix before review
MEDIUM issues   → Fix before launch
LOW issues      → Track for next cycle
```

---

### 5. Terminology Management

Enforce consistent terminology across all translations.

```python
# Add terminology
agent.terminology_manager.add_term(
    source_term="cloud",
    target_term="nube",
    source_language="en",
    target_language="es",
    category="technical",
    definition="Remote computing resources accessed via internet",
)

# Search terms
terms = agent.terminology_manager.search_terms(
    query="cloud",
    language="es",
    category="technical",
)

# Get forbidden terms
forbidden = agent.terminology_manager.get_forbidden_terms("es")
# → [{"term": "nub", "reason": "Common misspelling"}]
```

**Terminology Entry Fields:**

| Field | Description |
|-------|-------------|
| source_term | Term in source language |
| target_term | Approved translation |
| source_language | Source language code |
| target_language | Target language code |
| category | Term category (technical, legal, marketing) |
| definition | Clarifying definition |
| context | Usage context |
| forbidden | Whether term is forbidden |

---

### 6. Project Management

Orchestrate the complete localization workflow across languages.

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
agent.project_manager.update_progress(
    project.project_id, "es",
    translated=1000, reviewed=500, approved=400,
)

# Get status
status = agent.project_manager.get_project_status(project.project_id)
# → {
#   "project_id": "PROJ-XXX",
#   "overall_progress": 8.0,
#   "phase": "extraction",
#   "days_remaining": 57,
#   "by_language": {"es": 20.0, "fr": 0.0, "de": 0.0}
# }
```

**Project Phases:**
```
PLANNING → EXTRACTION → TRANSLATION → REVIEW → QA → INTEGRATION → LAUNCH → POST_LAUNCH
```

**Workflow Steps:**

| Step | Description | Input | Output |
|------|-------------|-------|--------|
| EXTRACT | Pull translatable strings | Source code | Resource files |
| TRANSLATE | Translate with TM leverage | Source strings | Translated strings |
| REVIEW | Linguistic review by native | Translations | Reviewed translations |
| PROOFREAD | Final quality pass | Reviewed | Proofread translations |
| QA_CHECK | Automated quality checks | Translations | QA report |
| INTEGRATE | Merge into codebase | Translations | Updated code |
| PUBLISH | Deploy to production | Code | Live product |

---

## Data Models

### TranslationUnit

| Field | Type | Description |
|-------|------|-------------|
| unit_id | str | Unique identifier |
| key | str | String key |
| source_text | str | Source language text |
| target_language | str | Target language code |
| translated_text | str | Target language text |
| status | TranslationStatus | PENDING, IN_PROGRESS, REVIEW, APPROVED, PUBLISHED |
| match_type | MatchType | EXACT, FUZZY_XX, MT, NEW |
| translator | str | Assigned translator |
| reviewer | str | Assigned reviewer |

### TranslationMemoryEntry

| Field | Type | Description |
|-------|------|-------------|
| entry_id | str | Unique identifier |
| source_text | str | Source text |
| target_text | str | Translation |
| source_language | str | Source language code |
| target_language | str | Target language code |
| approved | bool | TM entry approved |
| usage_count | int | Times used |
| domain | str | Domain/category |

### QAIssue

| Field | Type | Description |
|-------|------|-------------|
| issue_id | str | Unique identifier |
| unit_id | str | Related translation unit |
| check_type | QACheckType | MISSING, PLACEHOLDER, LENGTH, etc. |
| severity | QASeverity | CRITICAL, HIGH, MEDIUM, LOW |
| message | str | Issue description |
| auto_fixable | bool | Can be auto-fixed |
| suggestion | str | Suggested fix |

### LocaleConfiguration

| Field | Type | Description |
|-------|------|-------------|
| locale_code | str | Locale identifier (es-ES) |
| language | str | Language code (es) |
| region | str | Region code (ES) |
| direction | str | LTR or RTL |
| date_format | str | Date format pattern |
| time_format | str | Time format pattern |
| number_format | str | Number format pattern |
| currency_code | str | Currency code (EUR) |
| currency_symbol | str | Currency symbol (€) |
| decimal_separator | str | Decimal separator (.) |
| thousands_separator | str | Thousands separator (,) |
| first_day_of_week | int | 0=Sunday, 1=Monday |

---

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
- [ ] Set up CI/CD integration
- [ ] Configure monitoring

### Translation Workflow
- [ ] TM leverage analysis complete
- [ ] Untranslated strings identified
- [ ] Translation assigned to linguists
- [ ] Translations submitted
- [ ] Review completed
- [ ] QA checks passed
- [ ] Glossary compliance verified
- [ ] Integrations tested
- [ ] Build verified
- [ ] Ready for deployment

### Pre-Launch QA
- [ ] All strings translated
- [ ] QA pass rate >= 95%
- [ ] No critical issues
- [ ] Placeholder consistency verified
- [ ] Character limits respected
- [ ] RTL layout tested
- [ ] Date/number formatting verified
- [ ] Cultural adaptation reviewed
- [ ] Glossary compliance verified
- [ ] Pseudo-localization tested

### Post-Launch
- [ ] Monitor user feedback
- [ ] Track translation quality metrics
- [ ] Update TM with corrections
- [ ] Review glossary additions
- [ ] Document lessons learned
- [ ] Plan next iteration

---

## Troubleshooting

### Low TM Leverage
- Check if source strings have changed significantly
- Verify TM contains relevant entries
- Consider fuzzy match threshold adjustment
- Review TM domain assignment
- Check for source string variations
- Verify TM language pair coverage

### QA Pass Rate Too Low
- Check for systematic issues (placeholders, glossary)
- Review translator training needs
- Verify style guide clarity
- Check source string quality
- Review QA check configuration
- Validate character limit settings

### Cultural Issues Not Caught
- Review cultural rule coverage
- Add more locale-specific rules
- Involve native reviewers earlier
- Check style guide completeness
- Review cultural rule accuracy
- Add regional variants

### Project Behind Schedule
- Review phase transition bottlenecks
- Check team capacity and workload
- Consider splitting work by language
- Adjust deadlines if needed
- Review TM leverage improvements
- Consider MT for initial drafts

### Formatting Issues
- Verify locale configuration
- Check date/number format patterns
- Validate currency settings
- Review RTL support
- Test pseudo-localization
- Verify character encoding

### Integration Problems
- Check string extraction completeness
- Verify resource file format
- Review build integration
- Test deployment process
- Validate string keys
- Check for missing translations

---

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
