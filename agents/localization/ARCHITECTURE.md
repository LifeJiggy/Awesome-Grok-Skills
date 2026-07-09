# Localization Agent Architecture

## Executive Summary

The Localization Agent is a comprehensive internationalization and localization platform that manages the complete lifecycle of shipping software across languages and regions. It provides translation memory management with fuzzy matching, i18n engineering with locale-aware formatting, cultural adaptation with style guide enforcement, automated quality assurance, terminology consistency, and multi-market project orchestration.

The platform is designed for product teams managing large-scale translation projects across 50+ languages, where consistency, quality, and efficiency are paramount.

## Design Principles

**Translation Memory First.** Every translated string is stored in the TM for future leverage.

**Quality is Automated.** Manual review catches nuance; automated QA catches mechanics.

**Locale-Aware Formatting.** Numbers, dates, currencies, and lists must respect local conventions.

**Terminology is Sacred.** Inconsistent terminology destroys user trust.

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                        Localization Agent                                         │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                   Translation Memory Layer                                  │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │  │
│  │  │TM Store  │ │Fuzzy     │ │Leverage  │ │TM        │ │Cost      │       │  │
│  │  │& Retrieval│ │Matching  │ │Analysis  │ │Maint.    │ │Savings   │       │  │
│  │  │          │ │(Jaccard) │ │          │ │          │ │Estimate  │       │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                   i18n Engineering Layer                                    │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │  │
│  │  │Locale    │ │Pseudo-   │ │Number/   │ │RTL       │ │Resource  │       │  │
│  │  │Config    │ │localize  │ │Date/Curr │ │Support   │ │File Mgmt │       │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                  Cultural Adaptation Layer                                  │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                     │  │
│  │  │Style     │ │Cultural  │ │Content   │ │Tone &    │                     │  │
│  │  │Guide     │ │Rules     │ │Adaptation│ │Formality │                     │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘                     │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                  Quality Assurance Layer                                    │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │  │
│  │  │Missing   │ │Placeholder│ │Length    │ │Glossary  │ │Style     │       │  │
│  │  │Translation│ │Check     │ │Check     │ │Compliance│ │Check     │       │  │
│  │  │(CRITICAL)│ │(HIGH)    │ │(MEDIUM)  │ │(HIGH)    │ │(MEDIUM)  │       │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                  Terminology Management Layer                               │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                                  │  │
│  │  │Glossary  │ │Termbase  │ │Forbidden │                                  │  │
│  │  │Manager   │ │Enforce   │ │Terms     │                                  │  │
│  │  └──────────┘ └──────────┘ └──────────┘                                  │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                  Project Management Layer                                   │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │  │
│  │  │Workflow  │ │Progress  │ │Deadline  │ │Team      │ │Portfolio │       │  │
│  │  │Orchestr. │ │Tracking  │ │Mgmt      │ │Coord.    │ │Overview  │       │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘       │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Translation Memory Engine

Stores previous translations and finds matches for new strings.

**Fuzzy Match Algorithm (Jaccard Similarity):**
```
tokenize(text) → set of words (lowercased)
score = |intersection(words_a, words_b)| / |union(words_a, words_b)|
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
leverage = (exact_count + fuzzy_count × 0.75) / total_strings × 100
cost_savings = leverage% (approximately)
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
```

**RTL Language Support:**
```
Languages requiring RTL: ar, he, fa, ur
  → HTML: <html dir="rtl" lang="ar">
  → CSS: logical properties (margin-inline-start vs margin-left)
  → Layout: mirrored navigation and icons
```

**Pseudo-Localization Algorithm:**
```
For each source string:
  1. Expand vowels: "Hello" → "Ĥéľľó"
  2. Add padding: "Hello" → "¡Ĥéľľó!"
  3. For RTL: add RTL marks

Purpose: Test UI layout with longer text before real translations exist
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

Ensures content is culturally appropriate.

**Style Guide Components:**
```python
guide = StyleGuide(
    language="ja",
    tone="polite",
    formality="formal",
    rules=[
        {"type": "pronoun", "rule": "Use keigo (honorific) in B2B"},
        {"type": "avoidance", "rule": "Never use direct refusal"},
    ],
    brand_voices={
        "product": "Friendly but professional",
        "marketing": "Aspirational and warm",
    },
)
```

**Cultural Rules by Language:**
| Language | Rule Type | Description |
|----------|-----------|-------------|
| ja | honorifics | Use keigo for B2B contexts |
| ja | avoidance | Avoid direct "no" |
| de | formality | Use "Sie" in business |
| de | precision | Technical compound words are standard |
| zh | numerology | Avoid number 4, prefer 8 |
| ar | religious | Avoid pork/alcohol references |
| br | informality | "Voce" acceptable in most contexts |
| ko | hierarchy | Respect age/status in language |

### Quality Assurance Engine

Runs automated checks before human review.

**QA Check Matrix:**
| Check Type | Severity | Auto-Fix | Detection Logic |
|-----------|----------|----------|-----------------|
| MISSING_TRANSLATION | CRITICAL | No | Empty target_text |
| PLACEHOLDER_MISMATCH | HIGH | Partial | {var} in source not in target |
| LENGTH_ISSUE | MEDIUM | No | len(target) > character_limit |
| GLOSSARY_VIOLATION | HIGH | No | Wrong term used |
| STYLE_VIOLATION | MEDIUM | No | Formality/tone mismatch |
| ENCODING_ERROR | CRITICAL | Yes | Invalid Unicode characters |
| PLURAL_FORM | HIGH | No | Missing plural variants |
| NUMERIC_FORMAT | MEDIUM | Yes | Wrong number formatting |
| PUNCTUATION | LOW | Yes | Trailing/leading punctuation mismatch |

**Severity Distribution:**
```
CRITICAL issues → Block release
HIGH issues     → Require fix before review
MEDIUM issues   → Fix before launch
LOW issues      → Track for next cycle
```

### Terminology Management

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
                  │ review    │
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

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Cache-Aside** | TM entries cached for fast lookup | TranslationMemoryEngine |
| **Pipeline** | QA checks as independent validators | QualityAssuranceEngine |
| **Strategy** | Multiple fuzzy matching algorithms | TranslationMemoryEngine |
| **Observer** | Phase transitions trigger notifications | ProjectManager |
| **Facade** | Unified API surface | LocalizationAgent |
| **Repository** | In-memory registries | All engines |

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

---

## Advanced i18n Patterns

### Pluralization Rules

```python
# ICU Message Format for plurals
plural_rules = {
    "en": {
        "one": "You have {count} new message",
        "other": "You have {count} new messages",
    },
    "ar": {
        "zero": "ليس لديك رسائل جديدة",
        "one": "لديك رسالة جديدة واحدة",
        "two": "لديك رسالتان جديدتان",
        "few": "لديك {count} رسائل جديدة",
        "many": "لديك {count} رسالة جديدة",
        "other": "لديك {count} رسالة جديدة",
    },
    "ja": {
        "other": "{count}件の新しいメッセージがあります",
    },
    "ru": {
        "one": "{count} новое сообщение",
        "few": "{count} новых сообщения",
        "many": "{count} новых сообщений",
        "other": "{count} новые сообщения",
    },
}
```

### Gender-Aware Translation

```python
# Gender-aware translations
gender_rules = {
    "de": {
        "user_greeting": {
            "male": "Willkommen, {name}!",
            "female": "Willkommen, {name}!",
            "neutral": "Willkommen, {name}!",
        },
        "task_assigned": {
            "male": "{name} hat eine neue Aufgabe",
            "female": "{name} hat eine neue Aufgabe",
            "neutral": "{name} hat eine neue Aufgabe",
        },
    },
    "fr": {
        "user_greeting": {
            "male": "Bienvenue, {name}!",
            "female": "Bienvenue, {name}!",
            "neutral": "Bienvenue, {name}!",
        },
    },
}
```

### Context-Aware Translation

```python
# Different translations based on context
context_translations = {
    "en": {
        "button.save": {
            "default": "Save",
            "dialog": "Save Changes",
            "toolbar": "Save Document",
            "settings": "Save Settings",
        },
    },
    "ja": {
        "button.save": {
            "default": "保存",
            "dialog": "変更を保存",
            "toolbar": "ドキュメントを保存",
            "settings": "設定を保存",
        },
    },
}
```

---

## Quality Metrics Dashboard

### Key Performance Indicators

```python
# Get localization quality dashboard
dashboard = agent.get_quality_dashboard()

print(f"Translation Quality Metrics:")
print(f"  Overall QA Pass Rate: {dashboard['qa_pass_rate']:.1f}%")
print(f"  Critical Issues: {dashboard['critical_issues']}")
print(f"  High Issues: {dashboard['high_issues']}")
print(f"  Medium Issues: {dashboard['medium_issues']}")
print(f"  Low Issues: {dashboard['low_issues']}")

print(f"\nTranslation Memory Stats:")
print(f"  Total Entries: {dashboard['tm_entries']:,}")
print(f"  Exact Matches: {dashboard['exact_matches']:,}")
print(f"  Fuzzy Matches: {dashboard['fuzzy_matches']:,}")
print(f"  New Translations: {dashboard['new_translations']:,}")
print(f"  Leverage: {dashboard['leverage_percent']:.1f}%")

print(f"\nProject Status:")
for project in dashboard['projects']:
    print(f"  {project['name']}: {project['progress']:.1f}% complete")
    print(f"    Languages: {', '.join(project['languages'])}")
    print(f"    Deadline: {project['deadline']}")
    print(f"    Days Remaining: {project['days_remaining']}")
```

---

## Testing Strategy

### Unit Test Coverage

```python
# Translation Memory Tests
class TestTranslationMemory:
    def test_exact_match(self):
        tm = TranslationMemoryEngine()
        tm.add_entry("Hello", "Hola", "en", "es")
        matches = tm.find_matches("Hello", "en", "es")
        assert len(matches) == 1
        assert matches[0].score == 1.0
        assert matches[0].match_type == "EXACT"

    def test_fuzzy_match(self):
        tm = TranslationMemoryEngine()
        tm.add_entry("Hello World", "Hola Mundo", "en", "es")
        matches = tm.find_matches("Hello Worlds", "en", "es")
        assert len(matches) == 1
        assert 0.8 <= matches[0].score <= 1.0

    def test_leverage_calculation(self):
        tm = TranslationMemoryEngine()
        tm.add_entry("Hello", "Hola", "en", "es")
        tm.add_entry("Goodbye", "Adios", "en", "es")
        leverage = tm.get_leverage_stats("en", "es", ["Hello", "New"])
        assert leverage["leverage_percent"] == 50.0
```

### Integration Tests

```python
class TestLocalizationWorkflow:
    def test_full_localization_flow(self):
        agent = LocalizationAgent()

        # Set up TM
        agent.tm_engine.add_entry("Hello", "Hola", "en", "es")

        # Register locale
        agent.i18n_engine.register_locale("es-ES", "es", "ES", currency="EUR")

        # Create project
        project = agent.project_manager.create_project(
            name="Test Project",
            source_language="en",
            target_languages=["es"],
            total_strings=10,
        )

        # Process translations
        units = [
            TranslationUnit("U1", "greeting", "Hello {name}", "es", "Hola {name}"),
            TranslationUnit("U2", "farewell", "Goodbye", "es", "Adios"),
        ]

        # Run QA
        qa = agent.qa_engine.run_full_qa(units)
        assert qa["pass_rate"] == 100.0

        # Update progress
        agent.project_manager.update_progress(project.project_id, "es", translated=10, reviewed=10, approved=10)

        # Verify completion
        status = agent.project_manager.get_project_status(project.project_id)
        assert status["progress"] == 100.0
```

---

## Advanced Configuration

### Custom Locale Configurations

```python
# Define custom locale configurations
custom_locales = {
    "pt-BR": {
        "language": "pt",
        "region": "BR",
        "direction": "LTR",
        "date_format": "DD/MM/YYYY",
        "time_format": "HH:mm",
        "number_format": "1.234,56",
        "currency_code": "BRL",
        "currency_symbol": "R$",
        "decimal_separator": ",",
        "thousands_separator": ".",
        "first_day_of_week": 0,  # Sunday
        "plural_rules": "portuguese",
    },
    "ko-KR": {
        "language": "ko",
        "region": "KR",
        "direction": "LTR",
        "date_format": "YYYY-MM-DD",
        "time_format": "HH:mm",
        "number_format": "1,234.56",
        "currency_code": "KRW",
        "currency_symbol": "₩",
        "decimal_separator": ".",
        "thousands_separator": ",",
        "first_day_of_week": 0,  # Sunday
        "plural_rules": "korean",
    },
    "th-TH": {
        "language": "th",
        "region": "TH",
        "direction": "LTR",
        "date_format": "DD/MM/YYYY",
        "time_format": "HH:mm",
        "number_format": "1,234.56",
        "currency_code": "THB",
        "currency_symbol": "฿",
        "decimal_separator": ".",
        "thousands_separator": ",",
        "first_day_of_week": 0,  # Sunday
        "plural_rules": "thai",
    },
}

# Register custom locales
for locale_code, config in custom_locales.items():
    agent.i18n_engine.register_locale(locale_code, **config)
```

### Translation Memory Optimization

```python
# Optimize TM for better performance
optimization_config = {
    "deduplication": {
        "enabled": True,
        "similarity_threshold": 0.95,
        "strategy": "keep_approved",
    },
    "consolidation": {
        "enabled": True,
        "min_usage_count": 10,
        "consolidate_similar": True,
    },
    "cleanup": {
        "enabled": True,
        "remove_outdated_days": 365,
        "remove_low_quality": True,
        "quality_threshold": 0.7,
    },
    "indexing": {
        "enabled": True,
        "index_fields": ["source_text", "target_text", "domain"],
        "update_interval_hours": 24,
    },
}

# Run TM optimization
results = agent.tm_engine.optimize(optimization_config)
print(f"Optimization Results:")
print(f"  Duplicates Removed: {results['duplicates_removed']}")
print(f"  Entries Consolidated: {results['entries_consolidated']}")
print(f"  Outdated Entries Removed: {results['outdated_removed']}")
print(f"  Index Rebuilt: {results['index_rebuilt']}")
print(f"  Performance Improvement: {results['performance_improvement']:.1f}%")
```

---

## Advanced Translation Features

### Context-Aware Translation

```python
# Different translations based on context
context_translations = {
    "en": {
        "button.save": {
            "default": "Save",
            "dialog": "Save Changes",
            "toolbar": "Save Document",
            "settings": "Save Settings",
        },
    },
    "ja": {
        "button.save": {
            "default": "保存",
            "dialog": "変更を保存",
            "toolbar": "ドキュメントを保存",
            "settings": "設定を保存",
        },
    },
}
```

### Pluralization Rules

```python
# ICU Message Format for plurals
plural_rules = {
    "en": {
        "one": "You have {count} new message",
        "other": "You have {count} new messages",
    },
    "ar": {
        "zero": "ليس لديك رسائل جديدة",
        "one": "لديك رسالة جديدة واحدة",
        "two": "لديك رسالتان جديدتان",
        "few": "لديك {count} رسائل جديدة",
        "many": "لديك {count} رسالة جديدة",
        "other": "لديك {count} رسالة جديدة",
    },
    "ja": {
        "other": "{count}件の新しいメッセージがあります",
    },
}
```

### Gender-Aware Translation

```python
# Gender-aware translations
gender_rules = {
    "de": {
        "user_greeting": {
            "male": "Willkommen, {name}!",
            "female": "Willkommen, {name}!",
            "neutral": "Willkommen, {name}!",
        },
    },
    "fr": {
        "user_greeting": {
            "male": "Bienvenue, {name}!",
            "female": "Bienvenue, {name}!",
            "neutral": "Bienvenue, {name}!",
        },
    },
}
```

### String Interpolation Patterns

```python
# Handle various interpolation patterns
interpolation_patterns = {
    "named": "Hello {name}, you have {count} messages",
    "positional": "Hello {0}, you have {1} messages",
    "icu": "{gender, select, male{He} female{She} other{They}} has {count, plural, one{# message} other{# messages}}",
    "python": "Hello %(name)s, you have %(count)d messages",
    "sprintf": "Hello %s, you have %d messages",
}
```

---

## Advanced Translation Features

### Context-Aware Translation

```python
# Different translations based on context
context_translations = {
    "en": {
        "button.save": {
            "default": "Save",
            "dialog": "Save Changes",
            "toolbar": "Save Document",
            "settings": "Save Settings",
        },
    },
    "ja": {
        "button.save": {
            "default": "保存",
            "dialog": "変更を保存",
            "toolbar": "ドキュメントを保存",
            "settings": "設定を保存",
        },
    },
}
```

### Pluralization Rules

```python
# ICU Message Format for plurals
plural_rules = {
    "en": {
        "one": "You have {count} new message",
        "other": "You have {count} new messages",
    },
    "ar": {
        "zero": "ليس لديك رسائل جديدة",
        "one": "لديك رسالة جديدة واحدة",
        "two": "لديك رسالتان جديدتان",
        "few": "لديك {count} رسائل جديدة",
        "many": "لديك {count} رسالة جديدة",
        "other": "لديك {count} رسالة جديدة",
    },
    "ja": {
        "other": "{count}件の新しいメッセージがあります",
    },
}
```

### Gender-Aware Translation

```python
# Gender-aware translations
gender_rules = {
    "de": {
        "user_greeting": {
            "male": "Willkommen, {name}!",
            "female": "Willkommen, {name}!",
            "neutral": "Willkommen, {name}!",
        },
    },
    "fr": {
        "user_greeting": {
            "male": "Bienvenue, {name}!",
            "female": "Bienvenue, {name}!",
            "neutral": "Bienvenue, {name}!",
        },
    },
}
```

### String Interpolation Patterns

```python
# Handle various interpolation patterns
interpolation_patterns = {
    "named": "Hello {name}, you have {count} messages",
    "positional": "Hello {0}, you have {1} messages",
    "icu": "{gender, select, male{He} female{She} other{They}} has {count, plural, one{# message} other{# messages}}",
    "python": "Hello %(name)s, you have %(count)d messages",
    "sprintf": "Hello %s, you have %d messages",
}
```
```
