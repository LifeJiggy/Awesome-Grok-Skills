# Creative Director Agent

Creative strategy, brand campaigns, design direction, team leadership, client relations, and portfolio management for end-to-end creative operations.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Brand Identity](#brand-identity)
  - [Visual Assets](#visual-assets)
  - [Design Systems](#design-systems)
  - [Creative Strategy](#creative-strategy)
  - [Content Optimization](#content-optimization)
  - [Creative Review](#creative-review)
  - [Campaign Management](#campaign-management)
  - [Time Estimation](#time-estimation)
- [API Reference](#api-reference)
- [Brand Tones](#brand-tones)
- [Asset Types](#asset-types)
- [Design System Components](#design-system-components)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Creative Director Agent is a Python-based system for managing end-to-end creative operations. It creates brand identities, designs visual assets, builds design systems, develops creative strategies, optimizes content, reviews creative work, estimates timelines, and manages campaigns.

**Key Capabilities:**
- Brand identity creation with deterministic palette generation
- Visual asset design across multiple formats
- Design system construction with components and tokens
- Creative strategy development with positioning and messaging
- Content optimization for engagement and conversion
- Creative review with criteria-based scoring
- Campaign management from draft to launch
- Project time and cost estimation

## Features

| Feature | Description |
|---------|-------------|
| Brand Identity | Logo, colors, typography, voice, imagery style |
| Visual Assets | Image, video, illustration, icon, template design |
| Design Systems | Components, states, variations, guidelines, tokens |
| Creative Strategy | Positioning, messaging, campaign ideas, metrics |
| Content Optimization | Engagement and conversion optimization |
| Creative Review | Criteria-based scoring with recommendations |
| Timeline Estimation | Asset and campaign effort estimation |
| Campaign Management | Draft, launch, and track creative campaigns |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Creative Director Agent                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │  Brand   │ │ Visual   │ │ Design   │ │Creative  │     │
│  │Identity  │ │ Asset    │ │ System   │ │Strategy  │     │
│  │Designer  │ │Designer  │ │ Builder  │ │Advisor   │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
│       │            │            │            │             │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐     │
│  │ Content  │ │Creative  │ │  Time    │ │  Design  │     │
│  │Optimizer │ │Reviewer  │ │Estimator │ │  Asset   │     │
│  │          │ │          │ │          │ │ Storage  │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agents.creative_director.agent import CreativeDirectorAgent

agent = CreativeDirectorAgent()

# Create brand identity
identity = agent.create_brand_identity(
    brand="NovaBrand",
    industry="technology",
    tone="bold",
)

# Build design system
system = agent.build_design_system(brand="NovaBrand")

# Develop strategy
strategy = agent.develop_creative_strategy(
    objective="launch",
    audience="developers",
    channels=["web", "social"],
)

# Create campaign
campaign = agent.create_campaign(
    name="Nova Launch",
    objective="launch",
    target_audience="developers",
    channels=["social"],
    budget=8000.0,
    duration_weeks=12,
)
```

```bash
python agents/creative-director/agent.py
```

## Usage

### Brand Identity

```python
identity = agent.create_brand_identity(
    brand="NovaBrand",
    industry="technology",
    tone="bold",
)

print(identity["colors"])       # 5-color palette
print(identity["typography"])   # 3 font families
print(identity["logo_concept"]) # Logo concept details
print(identity["voice"])        # Voice guidelines
```

### Visual Assets

```python
asset = agent.design_visual_asset(
    brief={"name": "Hero Image", "type": "image", "description": "Launch hero"},
    system_id=system["system_id"],
)

print(asset["formats"])           # jpg, webp, png
print(asset["specs"])             # Format-specific specs
print(asset["principles_applied"]) # Design principles
```

### Design Systems

```python
system = agent.build_design_system(brand="NovaBrand")

print(f"Components: {system['components_count']}")
print(f"Categories: {system['categories']}")
print(f"Guidelines: {system['guidelines']}")
```

### Creative Strategy

```python
strategy = agent.develop_creative_strategy(
    objective="launch",
    audience="tech professionals",
    channels=["web", "social"],
    constraints={"timeline_weeks": 12, "budget": 10000},
)

print(strategy["positioning"])
print(strategy["campaign_ideas"])
print(strategy["success_metrics"])
```

### Content Optimization

```python
optimized = agent.optimize_content(
    content={"headline": "New Feature Launch"},
    channel="social",
    goal="engagement",
)

print(f"Score: {optimized['engagement_score']}")
for s in optimized["suggestions"]:
    print(f"  - {s}")
```

### Creative Review

```python
review = agent.review_creative(asset_id=asset["asset_id"])

print(f"Score: {review['overall_score']}")
print(f"Verdict: {review['verdict']}")
print(f"Strengths: {review['strengths']}")
print(f"Weaknesses: {review['weaknesses']}")
```

### Campaign Management

```python
campaign = agent.create_campaign(
    name="Spring Launch",
    objective="launch",
    target_audience="developers",
    channels=["social"],
    budget=5000.0,
    duration_weeks=8,
)

agent.launch_campaign(campaign.campaign_id)
```

### Time Estimation

```python
estimate = agent.estimate_project(
    components=["logo", "hero_image", "social_templates"],
    complexity="medium",
)

print(f"Hours: {estimate['total_hours']}")
print(f"Days: {estimate['total_days']}")
print(f"Cost: ${estimate['estimated_cost']}")
```

## API Reference

### CreativeDirectorAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_brand_identity()` | brand, industry, tone | Brand identity dict |
| `design_visual_asset()` | brief, system_id | Asset dict |
| `build_design_system()` | brand, system_id | Design system dict |
| `develop_creative_strategy()` | objective, audience, channels, constraints | Strategy dict |
| `optimize_content()` | content, channel, goal | Optimized content dict |
| `review_creative()` | asset_id | Review dict |
| `estimate_project()` | components, complexity | Estimate dict |
| `create_campaign()` | name, objective, target_audience, channels, budget, duration_weeks | Campaign object |
| `launch_campaign()` | campaign_id | Launch dict |
| `get_status()` | — | Agent status dict |
| `export_system()` | system_id, format | Export dict |

## Brand Tones

| Tone | Voice | Best For |
|------|-------|----------|
| `professional` | Clear, factual | Enterprise, B2B |
| `playful` | Energetic, witty | Consumer, youth |
| `luxury` | Elegant, exclusive | Premium, fashion |
| `minimalist` | Direct, clean | Tech, design |
| `bold` | Confident, provocative | Disruption, DTC |
| `friendly` | Warm, authentic | Community, support |
| `technical` | Precise, structured | Engineering, SaaS |
| `warm` | Approachable, human | Health, family |
| `corporate` | Formal, established | Finance, legal |
| `artisanal` | Handcrafted, authentic | Food, craft |

## Asset Types

| Type | Description | Formats |
|------|-------------|---------|
| `logo` | Brand mark | SVG, PNG, JPG |
| `image` | Static visual | PNG, JPG, WEBP |
| `video` | Motion content | MP4, MOV |
| `illustration` | Custom artwork | SVG, PNG |
| `icon` | Glyph | SVG, PNG |
| `template` | Design file | FIGMA, SKETCH |
| `motion_graphic` | Animation | MP4, GIF |
| `campaign_asset` | Marketing | Multiple |

## Design System Components

| Category | Variations | States |
|----------|-----------|--------|
| `button` | primary, secondary, tertiary, destructive, ghost | default, hover, focus, disabled, loading, error |
| `input` | default, error, success, disabled | default, focus, error, disabled, filled |
| `card` | default, outlined, elevated | default, hover, selected |
| `navigation` | top, side, bottom, mega | default, active, collapsed, mobile |

## Data Models

### Brand Identity
Complete brand system with colors, typography, logo concept, voice, and imagery style.

### Design System
Component library with tokens, guidelines, and version management.

### Campaign
Creative campaign with objective, audience, channels, budget, and status tracking.

### Asset
Visual asset with formats, specs, design principles, and accessibility notes.

## Configuration

```python
from agents.creative_director.agent import Config

config = Config(
    tone="professional",
    industry="technology",
    default_formats=["png", "jpg"],
    design_grid_columns=12,
    max_width_px=1200,
    accessibility_level="AA",
)
agent = CreativeDirectorAgent(config=config)
```

## Best Practices

1. **Start with Strategy** — Define positioning before designing
2. **Maintain Consistency** — Use the design system for all touchpoints
3. **Design for Accessibility** — WCAG 2.1 AA compliance minimum
4. **Document Everything** — Brand guidelines prevent drift
5. **Iterate Based on Data** — Use performance metrics to refine
6. **Collaborate Early** — Involve stakeholders in brand development
7. **Version Control** — Track design system versions

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Colors inconsistent | Verify deterministic palette generation |
| Components not rendering | Check token names match CSS custom properties |
| Campaign launch fails | Verify campaign_id and status transitions |
| Review score low | Address weakest criteria first |
| Timeline aggressive | Increase complexity estimate |
| Brand identity generic | Add industry-specific elements |

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file

## Contributing

1. Add new brand tone options
2. Enhance asset format support
3. Add new component templates
4. Improve review criteria
5. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.
