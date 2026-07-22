---
name: "localization-systems"
category: "international-dev-tech"
version: "2.0.0"
tags: ["localization", "i18n", "l10n", "translation", "internationalization"]
description: "Software localization and internationalization systems for global applications"
---

# Localization Systems

## Overview

The Localization Systems module provides comprehensive tools for internationalizing and localizing software applications. It supports string translation management, locale detection, pluralization rules, right-to-left (RTL) layouts, date/number formatting, and integration with translation management systems (TMS). The module enables developers to build applications that adapt to any language, region, or cultural convention.

## Core Capabilities

- **String Management**: Organize translatable strings with context and metadata
- **Locale Detection**: Automatic user locale detection from browser, IP, or preferences
- **Pluralization**: Handle complex plural rules across languages (CLDR)
- **Date/Time Formatting**: Locale-aware date and time formatting
- **Number Formatting**: Currency, percentage, and decimal formatting by locale
- **RTL Support**: Right-to-left layout adaptation for Arabic, Hebrew, etc.
- **Translation Workflow**: Integration with translation management systems
- **Pseudo-Localization**: Generate test translations for UI validation

## Usage Examples

### String Translation

```python
from localization_systems import LocalizationManager, TranslationKey

manager = LocalizationManager(default_locale="en-US")

# Add translations
manager.add_translation("en-US", "welcome_message", "Welcome, {name}!")
manager.add_translation("es-ES", "welcome_message", "¡Bienvenido, {name}!")
manager.add_translation("ja-JP", "welcome_message", "ようこそ、{name}さん！")

# Get translation
message = manager.translate(
    key="welcome_message",
    locale="es-ES",
    variables={"name": "Carlos"},
)
print(message)  # ¡Bienvenido, Carlos!
```

### Pluralization

```python
from localization_systems import PluralizationRules

rules = PluralizationRules()

# English pluralization
en_forms = rules.get_forms("en", count=5)
print(f"English: {en_forms}")  # ['other']

# Russian pluralization (complex rules)
ru_forms = rules.get_forms("ru", count=5)
print(f"Russian: {ru_forms}")  # ['one', 'few', 'many', 'other']

# Get correct plural form
form = rules.get_plural_form("en", count=1)
print(f"Form: {form}")  # 'one'
```

### Locale Formatting

```python
from localization_systems import LocaleFormatter

formatter = LocaleFormatter()

# Format date
date_str = formatter.format_date(
    date="2024-01-15T14:30:00Z",
    locale="de-DE",
    format="long",
)
print(f"German date: {date_str}")  # 15. Januar 2024

# Format currency
currency = formatter.format_currency(
    amount=1234.56,
    locale="ja-JP",
    currency="JPY",
)
print(f"Japanese currency: {currency}")  # ¥1,235

# Format number
number = formatter.format_number(
    value=1234567.89,
    locale="fr-FR",
)
print(f"French number: {number}")  # 1 234 567,89
```

### RTL Layout Detection

```python
from localization_systems import LayoutDetector

detector = LayoutDetector()

# Check if locale requires RTL
is_rtl = detector.is_rtl("ar-SA")
print(f"Arabic RTL: {is_rtl}")  # True

is_rtl = detector.is_rtl("en-US")
print(f"English RTL: {is_rtl}")  # False

# Get text direction
direction = detector.get_direction("he-IL")
print(f"Hebrew direction: {direction}")  # 'rtl'
```

## Best Practices

- **Use Resource Files**: Store translations in structured resource files (JSON, XLIFF, PO)
- **Context Matters**: Provide context for translators to ensure accurate translations
- **Test Pseudo-Localization**: Use pseudo-loc to test UI layout before real translations
- **Handle Plurals**: Always use pluralization functions, not string concatenation
- **Locale Fallback**: Implement fallback chains (e.g., fr-CA -> fr -> en)
- **Unicode Support**: Ensure full Unicode support throughout the application
- **RTL Testing**: Test layouts with RTL languages early in development
- **Translation Memory**: Use TM to maintain consistency across translations

## Related Modules

- **multi-language**: Multi-language content management
- **cultural-adaptation**: Cultural adaptation beyond translation
- **global-compliance**: Regulatory requirements by locale

---

## Advanced Configuration

### CLDR Data Configuration

```python
cldr_config = {
    "version": "44.0",
    "locales": ["en", "es", "fr", "de", "ja", "zh", "ar", "he"],
    "features": ["plurals", "currencies", "calendars", "timezones"],
    "custom_rules": True,
}
```

### Fallback Chain Configuration

```python
fallback_config = {
    "en-US": ["en", "en-GB", "root"],
    "fr-CA": ["fr", "fr-FR", "root"],
    "pt-BR": ["pt", "pt-PT", "root"],
    "zh-Hans-CN": ["zh-Hans", "zh", "root"],
    "default": ["en", "root"],
}
```

### Translation Memory Configuration

```python
tm_config = {
    "provider": "smartling",
    "match_threshold": 75,
    "context_weight": 0.3,
    "exact_match_bonus": 0.2,
    "max_results": 10,
    "enable_machine_post_editing": True,
}
```

### Pseudo-Localization Configuration

```python
pseudoloc_config = {
    "expansion_factor": 1.3,
    "prefix": "[",
    "suffix": "]",
    "character_replacement": True,
    "bracket_markers": True,
    "test_scripts": ["Latn", "Cyrl", "Arab"],
}
```

### Resource File Configuration

```python
resource_config = {
    "default_format": "json",
    "supported_formats": ["json", "xliff", "po", "properties", "yaml"],
    "key_separator": ".",
    "flatten_nested": False,
    "include_metadata": True,
}
```

## Architecture Patterns

### Localization Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Source     │────▶│  Extraction  │────▶│  Translation│
│  Strings    │     │  Engine      │     │  Management │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  MT     │           │  Human    │         │  QA       │
                    │  Engine │           │  Review   │         │  Check    │
                    └─────────┘           └───────────┘         └───────────┘
```

### Multi-Tenant Localization

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Tenant     │────▶│  Locale      │────▶│  Content    │
│  Config     │     │  Resolver    │     │  Delivery   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Cache  │           │  Fallback │         │  CDN      │
                    │  Layer  │           │  Chain    │         │  Edge     │
                    └─────────┘           └───────────┘         └───────────┘
```

### Event-Driven Translation Updates

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  String     │────▶│  Event       │────▶│  Translation│
│  Change     │     │  Bus         │     │  Queue      │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  MT     │           │  Human    │         │  Deploy   │
                    │  Queue  │           │  Queue    │         │  Pipeline │
                    └─────────┘           └───────────┘         └───────────┘
```

## Integration Guide

### TMS Integration

```python
def integrate_with_tms(content_items):
    for item in content_items:
        tms_api.create_job(
            source_content=item.source_content,
            target_locales=item.target_locales,
            context=item.context,
            priority=item.priority,
        )
```

### CI/CD Integration

```python
def localization_ci_step():
    # Extract strings
    strings = extract_strings_from_code()

    # Check for missing translations
    missing = check_missing_translations(strings, target_locales)

    # Validate pseudo-loc
    pseudoloc_results = validate_pseudo_localization(strings)

    return {"missing": missing, "pseudoloc": pseudoloc_results}
```

### Content Delivery Integration

```python
def deliver_localized_content(locale, content_key):
    # Check cache
    cached = cache.get(f"{locale}:{content_key}")
    if cached:
        return cached

    # Fallback chain
    content = None
    for fallback_locale in get_fallback_chain(locale):
        content = content_store.get(fallback_locale, content_key)
        if content:
            break

    # Cache and return
    cache.set(f"{locale}:{content_key}", content, ttl=300)
    return content
```

### MT Provider Integration

```python
def translate_with_mt(source_text, target_locale, provider="deepl"):
    result = mt_providers[provider].translate(
        text=source_text,
        target_lang=target_locale,
        formality="formal",
        preserve_formatting=True,
    )
    return {"translation": result.text, "confidence": result.confidence}
```

## Performance Optimization

### Caching Strategy

```python
cache_config = {
    "translations_ttl": 300,
    "locale_config_ttl": 3600,
    "plurals_ttl": 86400,
    "cache_backend": "redis",
    "cache_prefix": "l10n",
}
```

### Batch Processing

```python
batch_config = {
    "translation_batch_size": 100,
    "extraction_batch_size": 500,
    "parallel_workers": 4,
    "timeout_seconds": 300,
}
```

### CDN Optimization

```python
cdn_config = {
    "edge_locations": ["us-east-1", "eu-west-1", "ap-southeast-1"],
    "cache_ttl": 86400,
    "gzip_enabled": True,
    "brotli_enabled": True,
}
```

### Database Optimization

```python
db_config = {
    "indexing": ["locale", "key", "updated_at"],
    "connection_pool_size": 20,
    "read_replicas": 2,
    "query_timeout": 10,
}
```

## Security Considerations

### Data Protection

```python
security_config = {
    "encryption_at_rest": True,
    "encryption_in_transit": True,
    "sensitive_fields_masked": True,
    "access_logging": True,
    "data_retention_days": 365,
}
```

### Access Control

```python
access_control = {
    "rbac_enabled": True,
    "roles": {
        "translator": ["read_strings", "submit_translations"],
        "reviewer": ["read_strings", "approve_translations"],
        "admin": ["manage_strings", "configure_tms", "view_audit_logs"],
    },
    "mfa_required": True,
}
```

### API Security

```python
api_security = {
    "rate_limiting": 1000,
    "api_key_rotation_days": 90,
    "ip_whitelist": ["10.0.0.0/8"],
    "webhook_signature_verification": True,
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing translations | String not added to TMS | Add string to translation queue |
| RTL layout broken | CSS not adapted | Add RTL-specific CSS rules |
| Pluralization error | Wrong CLDR rules | Update CLDR data |
| Encoding issues | Non-UTF-8 source files | Convert to UTF-8 |
| Fallback not working | Chain misconfigured | Verify fallback chain |
| Cache stale | TTL too long | Reduce cache TTL |

### Debug Commands

```bash
# Check translation status
l10n-cli status --locale es-ES

# Validate pseudo-loc
l10n-cli pseudoloc --validate

# Check missing translations
l10n-cli missing --locale fr-FR

# Test fallback chain
l10n-cli fallback --locale fr-CA
```

## API Reference

### LocalizationManager

```python
class LocalizationManager:
    def __init__(self, default_locale: str):
        """Initialize localization manager."""

    def add_translation(self, locale: str, key: str, value: str) -> None:
        """Add translation string."""

    def translate(self, key: str, locale: str, variables: dict = None) -> str:
        """Get translated string."""

    def get_missing(self, locale: str) -> List[str]:
        """Get missing translation keys."""
```

### PluralizationRules

```python
class PluralizationRules:
    def __init__(self):
        """Initialize with CLDR rules."""

    def get_forms(self, locale: str, count: int) -> List[str]:
        """Get applicable plural forms."""

    def get_plural_form(self, locale: str, count: int) -> str:
        """Get correct plural form for count."""
```

### LocaleFormatter

```python
class LocaleFormatter:
    def __init__(self):
        """Initialize locale formatter."""

    def format_date(self, date: str, locale: str, format: str = "medium") -> str:
        """Format date for locale."""

    def format_currency(self, amount: float, locale: str, currency: str) -> str:
        """Format currency for locale."""

    def format_number(self, value: float, locale: str) -> str:
        """Format number for locale."""
```

### LayoutDetector

```python
class LayoutDetector:
    def __init__(self):
        """Initialize layout detector."""

    def is_rtl(self, locale: str) -> bool:
        """Check if locale is RTL."""

    def get_direction(self, locale: str) -> str:
        """Get text direction for locale."""
```

## Data Models

### Translation

```python
@dataclass
class Translation:
    key: str
    locale: str
    value: str
    context: str = None
    created_at: datetime = None
    updated_at: datetime = None
    translator: str = None
```

### LocaleConfig

```python
@dataclass
class LocaleConfig:
    locale: str
    language: str
    region: str
    direction: str
    fallback_chain: List[str]
    plural_rules: str
    date_format: str
    number_format: str
```

### PluralRule

```python
@dataclass
class PluralRule:
    locale: str
    cardinal_rules: Dict[str, str]
    ordinal_rules: Dict[str, str]
    range_rules: Dict[str, str]
```

### TranslationJob

```python
@dataclass
class TranslationJob:
    job_id: str
    source_locale: str
    target_locales: List[str]
    content_keys: List[str]
    status: str
    created_at: datetime
    completed_at: datetime = None
```

## Deployment Guide

### Initial Setup

```bash
# Initialize localization system
l10n-cli init

# Import source strings
l10n-cli import --source en-US --file strings.json

# Configure TMS integration
l10n-cli configure-tms --provider smartling --api-key xxx
```

### Production Deployment

```bash
# Deploy translation artifacts
l10n-cli deploy --locale all --environment production

# Verify deployment
l10n-cli verify --locale es-ES
```

## Monitoring & Observability

### Key Metrics

```python
metrics_config = {
    "translation_coverage": "gauge",
    "missing_translations": "gauge",
    "translation_latency": "histogram",
    "api_request_count": "counter",
    "cache_hit_rate": "gauge",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Localization Dashboard",
    "panels": [
        "coverage_by_locale",
        "translation_progress",
        "missing_strings",
        "cache_performance",
    ],
}
```

## Testing Strategy

### Pseudo-Localization Testing

```python
def test_pseudoloc():
    results = pseudoloc.validate_all_strings()
    assert results.ui_overflow == 0
    assert results.encoding_errors == 0
```

### RTL Layout Testing

```python
def test_rtl_layout():
    for locale in ["ar-SA", "he-IL", "fa-IR"]:
        layout = render_page(locale)
        assert layout.direction == "rtl"
        assert layout.mirrored == True
```

### Integration Tests

```python
def test_translation_workflow():
    key = "test.string"
    manager.add_translation("en-US", key, "Hello {name}")
    result = manager.translate(key, "es-ES", {"name": "Carlos"})
    assert result is not None
```

## Versioning & Migration

### String Versioning

```python
version_config = {
    "strategy": "semantic",
    "backward_compatibility": True,
    "deprecation_period_days": 90,
}
```

### TMS Migration

```python
migration_steps = {
    "export_strings": "Export from current TMS",
    "transform_format": "Convert to new format",
    "import_strings": "Import to new TMS",
    "validate_translations": "Verify all translations imported",
    "update_integrations": "Update CI/CD and app integrations",
}
```

## Glossary

| Term | Definition |
|------|------------|
| **i18n** | Internationalization - designing for multiple locales |
| **L10n** | Localization - adapting for specific locale |
| **CLDR** | Common Locale Data Repository |
| **TMS** | Translation Management System |
| **TM** | Translation Memory |
| **MT** | Machine Translation |
| **Pseudo-Localization** | Test translation for UI validation |
| **RTL** | Right-to-Left text direction |
| **Locale** | Language-region combination (e.g., en-US) |
| **Fallback Chain** | Order of locales to try for missing translations |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with TMS integration |
| 1.5.0 | 2024-11-01 | Added pseudo-localization |
| 1.4.0 | 2024-09-15 | Enhanced RTL support |
| 1.3.0 | 2024-07-20 | Pluralization improvements |
| 1.2.0 | 2024-05-10 | Translation memory integration |
| 1.1.0 | 2024-03-01 | Locale detection enhancements |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow Unicode standards
2. Test with pseudo-loc before real translations
3. Document string context for translators
4. Validate RTL layouts
5. Update CLDR data regularly
6. Test fallback chains

## String Extraction Automation

### Source Code String Extraction

```python
from localization_systems import StringExtractor

extractor = StringExtractor()

# Extract strings from source code
strings = extractor.extract(
    source_paths=["src/", "components/"],
    patterns=["t()", "i18n.translate()", "$t()"],
    output_format="json",
)

print(f"Extracted {len(strings)} translatable strings")
print(f"  New: {strings.new_count}")
print(f"  Existing: {strings.existing_count}")
print(f"  Missing: {strings.missing_count}")
```

## License

MIT License. See LICENSE file for full terms.
