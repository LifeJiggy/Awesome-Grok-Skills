---
name: "multi-language"
category: "international-dev-tech"
version: "2.0.0"
tags: ["multi-language", "content", "management", "translation", "workflow"]
description: "Multi-language content management and translation workflow systems"
---

# Multi-Language

## Overview

The Multi-Language module provides content management capabilities for applications supporting multiple languages. It manages translated content versions, translation workflows, content synchronization across locales, and integration with translation management systems (TMS). The module supports both machine translation and human translation workflows with review cycles.

## Core Capabilities

- **Content Versioning**: Track content versions across languages
- **Translation Workflows**: Configure translation pipelines with review stages
- **Content Synchronization**: Keep content in sync across locales
- **Machine Translation**: Integration with MT providers (Google, DeepL, AWS)
- **Translation Memory**: Leverage TM for consistency and cost reduction
- **Glossary Management**: Maintain terminology consistency
- **Content Dashboard**: Monitor translation progress and coverage
- **Export/Import**: Support for XLIFF, PO, JSON, and other formats

## Usage Examples

### Content Management

```python
from multi_language import ContentManager, ContentItem

manager = ContentManager()

# Create content item
item = ContentItem(
    content_id="home-hero",
    content_type="html",
    source_locale="en-US",
    source_content="<h1>Welcome to Our Platform</h1>",
)

# Add translations
item.add_translation("es-ES", "<h1>Bienvenido a Nuestra Plataforma</h1>")
item.add_translation("ja-JP", "<h1>プラットフォームへようこそ</h1>")

manager.add_content(item)

# Get content for locale
content = manager.get_content("home-hero", "ja-JP")
print(f"Japanese content: {content}")
```

### Translation Workflow

```python
from multi_language import TranslationWorkflow, WorkflowStage

workflow = TranslationWorkflow(
    name="product-descriptions",
    stages=[
        WorkflowStage(name="translate", type="machine_translate", provider="deepl"),
        WorkflowStage(name="review", type="human_review", reviewer_pool=" translators"),
        WorkflowStage(name="approve", type="approval", approver="content-lead"),
    ],
)

# Submit content for translation
job = workflow.submit(
    content_id="product-123",
    target_locales=["es-ES", "fr-FR", "de-DE"],
    priority="high",
)

print(f"Translation Job: {job.job_id}")
print(f"Status: {job.status}")
print(f"Target Locales: {job.target_locales}")
```

### Glossary Management

```python
from multi_language import GlossaryManager

glossary = GlossaryManager()

# Add terms
glossary.add_term(
    term="cloud computing",
    translations={"es-ES": "computación en la nube", "fr-FR": "informatique en nuage"},
    domain="technology",
   禁止用法=["cloud"],
)

# Validate content against glossary
violations = glossary.validate("Computing in the cloud is essential", "es-ES")
print(f"Glossary violations: {violations}")
```

### Content Coverage Dashboard

```python
from multi_language import CoverageDashboard

dashboard = CoverageDashboard(manager)

# Get coverage stats
stats = dashboard.get_coverage("es-ES")
print(f"Spanish Coverage:")
print(f"  Total Items: {stats['total_items']}")
print(f"  Translated: {stats['translated']}")
print(f"  Coverage: {stats['coverage_pct']:.1f}%")
print(f"  Outdated: {stats['outdated']}")
```

## Best Practices

- **Content Segregation**: Separate UI strings from content for independent translation
- **Context Provision**: Provide context and screenshots for translators
- **Style Guides**: Maintain locale-specific style guides
- **Review Cycles**: Implement mandatory review for high-visibility content
- **Translation Memory**: Always use TM to maintain consistency
- **Terminology Management**: Enforce glossary compliance
- **Automated Testing**: Test locale switching and content display
- **Fallback Chains**: Implement graceful fallback to base locale

## Related Modules

- **localization-systems**: Technical localization infrastructure
- **cultural-adaptation**: Cultural adaptation beyond translation
- **content-management**: Content management integration

---

## Advanced Configuration

### TMS Integration Configuration

```python
tms_config = {
    "providers": {
        "smartling": {"api_key": "xxx", "project_id": "yyy"},
        "lokalise": {"api_key": "xxx", "project_id": "yyy"},
        "phrase": {"api_key": "xxx", "project_id": "yyy"},
    },
    "default_provider": "smartling",
    "fallback_provider": "lokalise",
    "sync_interval_minutes": 15,
}
```

### Translation Workflow Configuration

```python
workflow_config = {
    "default_workflow": {
        "stages": [
            {"name": "machine_translate", "provider": "deepl"},
            {"name": "human_review", "reviewer_pool": "translators"},
            {"name": "approval", "approver": "content-lead"},
        ],
        "parallel_stages": False,
        "auto_approve_threshold": 0.9,
    },
    "urgent_workflow": {
        "stages": [
            {"name": "human_translate", "reviewer_pool": "translators"},
            {"name": "approval", "approver": "content-lead"},
        ],
    },
}
```

### Machine Translation Configuration

```python
mt_config = {
    "providers": {
        "deepl": {"api_key": "xxx", "formality": "formal"},
        "google": {"api_key": "xxx", "model": "nmt"},
        "aws_translate": {"region": "us-east-1"},
    },
    "default_provider": "deepl",
    "quality_threshold": 0.8,
    "post_editing_enabled": True,
}
```

### Glossary Configuration

```python
glossary_config = {
    "strict_mode": True,
    "case_sensitive": False,
    "max_suggestions": 5,
    "domain_specific": True,
    "auto_add_terms": False,
}
```

### Content Sync Configuration

```python
sync_config = {
    "sync_strategy": "bidirectional",
    "conflict_resolution": "source_wins",
    "auto_sync": True,
    "sync_interval_minutes": 5,
    "batch_size": 100,
}
```

## Architecture Patterns

### Translation Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Source     │────▶│  String      │────▶│  Translation│
│  Content    │     │  Extraction  │     │  Queue      │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  MT     │           │  Human    │         │  QA       │
                    │  Engine │           │  Review   │         │  Check    │
                    └─────────┘           └───────────┘         └───────────┘
```

### Multi-Tenant Content Management

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Tenant     │────▶│  Content     │────▶│  Translation│
│  Config     │     │  Store       │     │  Manager    │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Cache  │           │  TMS      │         │  Deploy   │
                    │  Layer  │           │  Sync     │         │  Pipeline │
                    └─────────┘           └───────────┘         └───────────┘
```

### Version Control Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Content    │────▶│  Version     │────▶│  Translation│
│  Change     │     │  Control     │     │  Queue      │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  New    │           │  Update   │         │  Delete   │
                    │  Version│           │  Version  │         │  Version  │
                    └─────────┘           └───────────┘         └───────────┘
```

## Integration Guide

### CMS Integration

```python
def sync_cms_content(cms_provider, content_items):
    for item in content_items:
        # Extract translatable strings
        strings = extract_strings(item)

        # Submit to TMS
        tms_job = tms_api.create_job(
            source_content=strings,
            target_locales=item.target_locales,
            context=item.context,
        )

        # Track translation progress
        track_translation_progress(item.id, tms_job.id)
```

### CI/CD Integration

```python
def localization_ci_step():
    # Extract strings from code
    strings = extract_strings_from_code()

    # Check for missing translations
    missing = check_missing_translations(strings, target_locales)

    # Validate translations
    validation_results = validate_translations(strings)

    # Generate report
    return {
        "missing_count": len(missing),
        "validation_errors": validation_results.errors,
    }
```

### Webhook Integration

```python
def handle_tms_webhook(event):
    if event.type == "translation_complete":
        # Update content store
        content_store.update_translation(
            content_id=event.content_id,
            locale=event.locale,
            translation=event.translation,
        )

        # Trigger deployment
        deployment_pipeline.trigger(content_id=event.content_id)
```

### API Integration

```python
def translate_content(content_key, target_locale):
    # Get source content
    source = content_store.get(content_key, source_locale)

    # Check translation memory
    tm_match = translation_memory.find_match(source, target_locale)
    if tm_match and tm_match.score > 0.8:
        return tm_match.translation

    # Fall back to MT + human review
    mt_result = mt_engine.translate(source, target_locale)
    return {"translation": mt_result.text, "needs_review": True}
```

## Performance Optimization

### Caching Strategy

```python
cache_config = {
    "translations_ttl": 300,
    "glossary_ttl": 3600,
    "tm_ttl": 86400,
    "cache_backend": "redis",
    "cache_prefix": "ml",
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

### Database Optimization

```python
db_config = {
    "indexing": ["content_key", "locale", "updated_at"],
    "connection_pool_size": 20,
    "read_replicas": 2,
    "query_timeout": 10,
}
```

### API Optimization

```python
api_config = {
    "response_timeout": 10,
    "retry_count": 3,
    "circuit_breaker": True,
    "rate_limiting": 500,
}
```

## Security Considerations

### Data Protection

```python
security_config = {
    "encryption_at_rest": True,
    "encryption_in_transit": True,
    "sensitive_content_masked": True,
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
        "admin": ["manage_strings", "configure_tms"],
    },
    "mfa_required": True,
}
```

### API Security

```python
api_security = {
    "api_key_required": True,
    "rate_limiting": 500,
    "ip_whitelist": ["10.0.0.0/8"],
    "webhook_signature_verification": True,
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing translations | String not in TMS | Add to translation queue |
| Sync conflict | Concurrent edits | Use conflict resolution rules |
| MT quality poor | Source text unclear | Improve source text |
| Glossary violation | Term not in glossary | Add term to glossary |
| Version mismatch | Content updated | Trigger retranslation |
| Deployment failed | TMS sync error | Check TMS connectivity |

### Debug Commands

```bash
# Check translation status
ml-cli status --content-key home-hero

# Validate translations
ml-cli validate --locale es-ES

# Sync content
ml-cli sync --content-key home-hero

# Check glossary
ml-cli glossary --term "cloud computing"
```

## API Reference

### ContentManager

```python
class ContentManager:
    def __init__(self):
        """Initialize content manager."""

    def add_content(self, item: ContentItem) -> None:
        """Add content item."""

    def get_content(self, content_id: str, locale: str) -> str:
        """Get content for locale."""

    def update_content(self, content_id: str, locale: str, content: str) -> None:
        """Update content."""
```

### TranslationWorkflow

```python
class TranslationWorkflow:
    def __init__(self, name: str, stages: List[WorkflowStage]):
        """Initialize workflow."""

    def submit(self, content_id: str, target_locales: List[str], priority: str) -> TranslationJob:
        """Submit for translation."""

    def get_status(self, job_id: str) -> JobStatus:
        """Get job status."""
```

### GlossaryManager

```python
class GlossaryManager:
    def __init__(self):
        """Initialize glossary manager."""

    def add_term(self, term: str, translations: Dict[str, str], domain: str) -> None:
        """Add glossary term."""

    def validate(self, content: str, locale: str) -> List[GlossaryViolation]:
        """Validate content against glossary."""
```

### CoverageDashboard

```python
class CoverageDashboard:
    def __init__(self, content_manager: ContentManager):
        """Initialize dashboard."""

    def get_coverage(self, locale: str) -> CoverageStats:
        """Get coverage statistics."""

    def get_missing(self, locale: str) -> List[str]:
        """Get missing translations."""
```

## Data Models

### ContentItem

```python
@dataclass
class ContentItem:
    content_id: str
    content_type: str
    source_locale: str
    source_content: str
    translations: Dict[str, str] = None
    metadata: Dict[str, Any] = None
```

### TranslationJob

```python
@dataclass
class TranslationJob:
    job_id: str
    content_id: str
    source_locale: str
    target_locales: List[str]
    status: str
    created_at: datetime
    completed_at: datetime = None
```

### WorkflowStage

```python
@dataclass
class WorkflowStage:
    name: str
    type: str
    provider: str = None
    reviewer_pool: str = None
    approver: str = None
```

### GlossaryTerm

```python
@dataclass
class GlossaryTerm:
    term: str
    translations: Dict[str, str]
    domain: str
    forbidden_variations: List[str] = None
```

### CoverageStats

```python
@dataclass
class CoverageStats:
    locale: str
    total_items: int
    translated: int
    coverage_pct: float
    outdated: int
```

## Deployment Guide

### Initial Setup

```bash
# Initialize multi-language system
ml-cli init

# Configure TMS
ml-cli configure-tms --provider smartling --api-key xxx

# Import glossary
ml-cli import-glossary --file glossary.csv
```

### Production Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/multi-language-service.yaml

# Verify deployment
kubectl rollout status deployment/multi-language-service
```

## Monitoring & Observability

### Key Metrics

```python
metrics_config = {
    "translation_coverage": "gauge",
    "translation_progress": "gauge",
    "glossary_compliance": "gauge",
    "sync_latency": "histogram",
    "api_request_count": "counter",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Multi-Language Dashboard",
    "panels": [
        "coverage_by_locale",
        "translation_progress",
        "glossary_violations",
        "sync_status",
    ],
}
```

## Testing Strategy

### Unit Tests

```python
def test_content_translation():
    manager = ContentManager()
    item = ContentItem("test", "html", "en-US", "<h1>Hello</h1>")
    manager.add_content(item)
    content = manager.get_content("test", "es-ES")
    assert content is not None
```

### Integration Tests

```python
def test_translation_workflow():
    workflow = TranslationWorkflow("test", mock_stages)
    job = workflow.submit("test-content", ["es-ES"], "high")
    assert job.status == "submitted"
```

## Versioning & Migration

### Content Versioning

```python
version_config = {
    "strategy": "semantic",
    "backward_compatibility": True,
    "deprecation_period_days": 90,
}
```

## Glossary

| Term | Definition |
|------|------------|
| **TMS** | Translation Management System |
| **TM** | Translation Memory |
| **MT** | Machine Translation |
| **Glossary** | Terminology database |
| **String** | Translatable text unit |
| **Locale** | Language-region combination |
| **Coverage** | Percentage of translated content |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with TMS integration |
| 1.5.0 | 2024-11-01 | Added glossary management |
| 1.4.0 | 2024-09-15 | Enhanced workflow support |
| 1.3.0 | 2024-07-20 | MT integration improvements |
| 1.2.0 | 2024-05-10 | Content sync features |
| 1.1.0 | 2024-03-01 | Coverage dashboard |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow translation best practices
2. Maintain glossary consistency
3. Test with multiple locales
4. Document content context
5. Review translations carefully

## Content Quality Metrics

### Translation Quality Score

```python
from multi_language import QualityScorer

scorer = QualityScorer()

# Score translation quality
quality = scorer.score(
    content_id="home-hero",
    target_locale="es-ES",
    metrics=["fluency", "terminology", "consistency", "cultural_fit"],
)

print(f"Translation Quality:")
print(f"  Overall: {quality.overall_score:.1%}")
print(f"  Fluency: {quality.fluency:.1%}")
print(f"  Terminology: {quality.terminology:.1%}")
print(f"  Consistency: {quality.consistency:.1%}")
print(f"  Cultural Fit: {quality.cultural_fit:.1%}")
```

## License

MIT License. See LICENSE file for full terms.
