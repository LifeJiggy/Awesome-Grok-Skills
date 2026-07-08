# Localization Agent Architecture

## Executive Summary

The Localization Agent is a comprehensive internationalization and localization platform that manages the complete lifecycle of shipping software across languages and regions. It provides translation memory management with fuzzy matching, i18n engineering with locale-aware formatting, cultural adaptation with style guide enforcement, automated quality assurance, terminology consistency, and multi-market project orchestration.

The platform is designed for product teams managing large-scale translation projects across 50+ languages, where consistency, quality, and efficiency are paramount. It supports the full workflow from string extraction through translation, review, QA, integration, and launch.

## Design Principles

**Translation Memory First.** Every translated string is stored in the TM for future leverage. The system aggressively matches new strings against existing translations, reducing cost and improving consistency.

**Quality is Automated.** Manual review catches nuance; automated QA catches mechanics. The system runs placeholder checks, glossary compliance, length limits, and encoding validation before human reviewers see the text.

**Locale-Aware Formatting.** Numbers, dates, currencies, and lists must respect local conventions. The system provides locale configuration for formatting and validates that translations preserve format placeholders.

**Terminology is Sacred.** Inconsistent terminology destroys user trust. The glossary system enforces correct terms and flags forbidden alternatives.

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                        Localization Agent                                         │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                   Translation Memory Layer                                  │  │
│  │                                                                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │  │
│  │  │TM Store  │ │Fuzzy     │ │Leverage  │ │TM        │ │Cost      │       │  │
│  │  │& Retrieval│ │Matching  │ │Analysis  │ │Maint.    │ │Savings   │       │  │
│  │  │          │ │(Jaccard) │ │          │ │          │ │Estimate  │       │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                   i18n Engineering Layer                                    │  │
│  │                                                                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │  │
│  │  │Locale    │ │Pseudo-   │ │Number/   │ │RTL       │ │Resource  │       │  │
│  │  │Config    │ │localize  │ │Date/Curr │ │Support   │ │File Mgmt │       │  │
│  │  │          │ │          │ │Format    │ │          │ │          │       │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                  Cultural Adaptation Layer                                  │  │
│  │                                                                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                     │  │
│  │  │Style     │ │Cultural  │ │Content   │ │Tone &    │                     │  │
│  │  │Guide     │ │Rules     │ │Adaptation│ │Formality │                     │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘                     │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                  Quality Assurance Layer                                    │  │
│  │                                                                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │  │
│  │  │Missing   │ │Placeholder│ │Length    │ │Glossary  │ │Style     │       │  │
│  │  │Translation│ │Check     │ │Check     │ │Compliance│ │Check     │       │  │
│  │  │(CRITICAL)│ │(HIGH)    │ │(MEDIUM)  │ │(HIGH)    │ │(MEDIUM)  │       │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                  Terminology Management Layer                               │  │
│  │                                                                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                                  │  │
│  │  │Glossary  │ │Termbase  │ │Forbidden │                                  │  │
│  │  │Manager   │ │Enforce   │ │Terms     │                                  │  │
│  │  └──────────┘ └──────────┘ └──────────┘                                  │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                  Project Management Layer                                   │  │
│  │                                                                            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │  │
│  │  │Workflow  │ │Progress  │ │Deadline  │ │Team      │ │Portfolio │       │  │
│  │  │Orchestr. │ │Tracking  │ │Mgmt      │ │Coord.    │ │Overview  │       │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Translation Memory Engine

Stores previous translations and finds matches for new strings to maximize leverage and consistency.

**Fuzzy Match Algorithm (Jaccard Similarity):**
```
tokenize(text) → set of words (lowercased)
score = |intersection(words_a, words_b)| / |union(words_a, words_b)|

Example:
  "Hello World" vs "Hello World!" → {"hello", "world"} vs {"hello", "world", "!"}
  score = |{"hello", "world"}| / |{"hello", "world", "!"}| = 2/3 = 0.667
```

**Match Type Classification:**
| Match Type | Score Range | Cost Multiplier | Post-Editing Effort |
|-----------|-------------|-----------------|-------------------|
| EXACT | 100% | 0% (free) | None |
| FUZZY_95 | 95-99% | 10% | Minimal |
| FUZZY_85 | 85-94% | 30% | Light editing |
| FUZZY_75 | 75-84% | 50% | Moderate editing |
| MT | N/A | 60% | Full post-edit |
| NEW | 0% | 100% | Full translation |

**Leverage Calculation:**
```
For each source string:
  matches = find_matches(source_text, src_lang, tgt_lang, limit=1)
  if matches[0].score >= 0.95:
    exact_count += 1
  elif matches[0].score >= 0.75:
    fuzzy_count += 1
  else:
    new_count += 1

leverage = (exact_count + fuzzy_count × 0.75) / total_strings × 100
cost_savings = leverage% (approximately)
```

**TM Maintenance Report:**
```python
report = tm_engine.maintenance_report()
# Returns:
# - total_entries: 100,000
# - approved_entries: 90,000
# - pending_review: 10,000
# - by_language_pair: {"en-es": 30000, "en-fr": 25000, ...}
# - by_domain: {"greeting": 5000, "technical": 15000, ...}
# - utilization_rate: 45.0 (avg uses per entry)
```

**TM Data Model:**

| Field | Type | Description |
|-------|------|-------------|
| entry_id | str | Unique identifier |
| source_text | str | Source text |
| target_text | str | Translation |
| source_language | str | Source language code |
| target_language | str | Target language code |
| domain | str | Content domain |
| approved | bool | Entry approved |
| usage_count | int | Times leveraged |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

### i18n Engineering Engine

Handles locale configuration, pseudo-localization, and locale-aware formatting.

**Locale Configuration Model:**
```
locale: "es-ES"
  language: "es"
  region: "ES"
  direction: LTR
  date_format: "DD/MM/YYYY"
  time_format: "HH:mm"
  number_format: "1.234,56"
  currency_code: "EUR"
  currency_symbol: "€"
  decimal_separator: ","
  thousands_separator: "."
  first_day_of_week: 1 (Monday)
  plural_rules: "spanish"
```

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

**Format Handling by Locale:**
| Locale | Number | Currency | Date | First Day |
|--------|--------|----------|------|-----------|
| en-US | 1,234.56 | $1,234.56 | 12/31/2026 | Sunday |
| es-ES | 1.234,56 | 1.234,56 € | 31/12/2026 | Monday |
| de-DE | 1.234,56 | 1.234,56 € | 31.12.2026 | Monday |
| ja-JP | 1,234.56 | ¥1,234 | 2026/12/31 | Sunday |
| ar-SA | ١٬٢٣٤٫٥٦ | ١٬٢٣٤٫٥٦ ر.س | 31/12/2026 | Saturday |
| zh-CN | 1,234.56 | ¥1,234.56 | 2026/12/31 | Monday |

### Cultural Adaptation Engine

Ensures content is culturally appropriate, not just linguistically correct.

**Style Guide Components:**
```python
guide = StyleGuide(
    language="ja",
    tone="polite",
    formality="formal",
    rules=[
        {"type": "pronoun", "rule": "Use keigo (honorific) in B2B"},
        {"type": "avoidance", "rule": "Never use direct refusal"},
        {"type": "seasonal", "rule": "Seasonal references appreciated"},
    ],
    brand_voices={
        "product": "Friendly but professional",
        "marketing": "Aspirational and warm",
        "support": "Patient and helpful",
    },
)
```

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

### Quality Assurance Engine

Runs automated checks before human review to catch mechanical errors.

**QA Check Matrix:**
| Check Type | Severity | Auto-Fix | Detection Logic |
|-----------|----------|----------|-----------------|
| MISSING_TRANSLATION | CRITICAL | No | Empty target_text |
| PLACEHOLDER_MISMATCH | HIGH | Partial | {var} in source not in target |
| LENGTH_ISSUE | MEDIUM | No | len(target) > character_limit |
| GLOSSARY_VIOLATION | HIGH | No | Wrong term used for glossary match |
| STYLE_VIOLATION | MEDIUM | No | Formality/tone mismatch |
| ENCODING_ERROR | CRITICAL | Yes | Invalid Unicode characters |
| PLURAL_FORM | HIGH | Missing plural variants |
| NUMERIC_FORMAT | MEDIUM | Yes | Wrong number formatting |
| PUNCTUATION | LOW | Yes | Trailing/leading punctuation mismatch |

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

### Terminology Management

Enforces consistent terminology across all translations.

**Glossary Entry Model:**

| Field | Type | Description |
|-------|------|-------------|
| term_id | str | Unique identifier |
| source_term | str | Term in source language |
| target_term | str | Approved translation |
| source_language | str | Source language code |
| target_language | str | Target language code |
| category | str | Term category |
| definition | str | Clarifying definition |
| context | str | Usage context |
| forbidden | bool | Whether term is forbidden |

### Project Management

Orchestrates the complete localization workflow across languages.

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

**Progress Tracking:**
```python
status = project_manager.get_project_status(project_id)
# Returns:
# - overall_progress: 65.0%
# - translated: 3250/5000
# - reviewed: 2500/5000
# - approved: 2000/5000
# - days_remaining: 45
```

## Data Flow

### Translation Workflow

```
1. Source strings extracted from codebase
2. TM lookup → exact/fuzzy matches found
3. Matched strings auto-populated (with leverage %)
4. Untranslated strings → translator queue
5. Translator works with TM suggestions
6. Translation submitted → review queue
7. Reviewer approves/edits
8. QA checks run automatically
9. Issues flagged and fixed
10. Translations merged into codebase
11. Build verified
12. Deployed to production
```

### Quality Assurance Flow

```
Translated units → QA Engine
                        │
          ┌─────────────┼─────────────┐
          │             │             │
    ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
    │ Missing   │ │Placeholder│ │ Length    │
    │ Check     │ │ Check     │ │ Check     │
    └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
          │             │             │
    ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
    │ Glossary  │ │ Style     │ │ Encoding  │
    │ Check     │ │ Check     │ │ Check     │
    └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
          │             │             │
          └─────────────┼─────────────┘
                        │
                  ┌─────▼─────┐
                  │ Issues    │
                  │ Collected │
                  └─────┬─────┘
                        │
                  ┌─────▼─────┐
                  │ Prioritize│
                  │ by Severity│
                  └─────┬─────┘
                        │
                  ┌─────▼─────┐
                  │ Auto-fix  │
                  │ where     │
                  │ possible  │
                  └─────┬─────┘
                        │
                  ┌─────▼─────┐
                  │ Manual    │
                  │ review for│
                  │ rest      │
                  └───────────┘
```

## Security

- Translation data confidentiality per language pair
- Access control per project and language
- Audit trail for TM modifications
- Secure handling of proprietary source strings
- Locale data integrity validation
- Encrypted storage for sensitive content

## Scalability

| Metric | Capacity |
|--------|----------|
| TM entries | 1M+ with sub-100ms lookup |
| Concurrent projects | 100+ |
| Languages supported | 50+ |
| QA checks per batch | 10K+ units |
| String management | 100K+ per project |
| Concurrent translators | Unlimited (stateless) |

## Performance Targets

| Metric | Target |
|--------|--------|
| TM fuzzy match lookup | < 50ms per 10K entries |
| Pseudo-localization gen | < 10ms per 100 strings |
| QA check (1K units) | < 500ms |
| Format conversion | < 5ms per value |
| Project status update | < 100ms |
| Leverage analysis | < 200ms for 10K strings |
| Missing key detection | < 100ms per locale pair |

## Design Patterns

### Cache-Aside Pattern
TM entries are cached for fast lookup, with cache invalidation on updates.

### Pipeline Pattern
QA checks run as a pipeline of independent validators, each handling a specific check type.

### Strategy Pattern
Multiple fuzzy matching strategies can be swapped based on content type and language.

### Observer Pattern
Project phase transitions trigger notifications to team members and downstream systems.

## Configuration Reference

```yaml
translation_memory:
  max_entries: 1000000
  fuzzy_threshold: 0.75
  cache_size: 100000
  maintenance_schedule: "weekly"

i18n_engine:
  default_source_language: "en"
  pseudo_localization_enabled: true
  rtl_languages: ["ar", "he", "fa", "ur"]
  max_locale_configs: 100

quality_assurance:
  pass_rate_threshold: 95.0
  auto_fix_enabled: true
  max_batch_size: 10000
  check_timeout_seconds: 300

terminology:
  enforcement_enabled: true
  forbidden_term_alerts: true
  max_terms_per_language: 50000

project_management:
  max_concurrent_projects: 100
  max_languages_per_project: 50
  deadline_reminder_days: [30, 14, 7, 3, 1]
  progress_update_frequency: "daily"
```
