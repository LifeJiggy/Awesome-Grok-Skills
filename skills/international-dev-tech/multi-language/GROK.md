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
