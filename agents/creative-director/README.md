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
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Creative Director Agent is a Python-based system for managing end-to-end creative operations. It creates brand identities, designs visual assets, builds design systems, develops creative strategies, optimizes content, reviews creative work, estimates timelines, and manages campaigns from draft to launch.

**Key Capabilities:**
- Brand identity creation with deterministic palette generation (same input = same output)
- Visual asset design across multiple formats with accessibility compliance
- Design system construction with components, tokens, and guidelines
- Creative strategy development with positioning and messaging frameworks
- Content optimization for engagement and conversion
- Creative review with criteria-based scoring (composition, color, typography, brand, accessibility)
- Campaign management from draft through launch with status tracking
- Project time and cost estimation with confidence levels

**Ideal For:**
- Creative directors managing brand and campaign workflows
- Design teams building and maintaining design systems
- Marketing teams developing creative strategies
- Agencies handling multiple client brands

## Features

| Feature | Description |
|---------|-------------|
| Brand Identity | Logo concepts, 5-color palette, typography, voice, imagery style |
| Visual Assets | Image, video, illustration, icon, template design with specs |
| Design Systems | Components, states, variations, guidelines, tokens, versioning |
| Creative Strategy | Positioning, messaging, campaign ideas, success metrics |
| Content Optimization | Engagement and conversion optimization with A/B recommendations |
| Creative Review | 5-criteria scoring with strengths, weaknesses, recommendations |
| Timeline Estimation | Asset and campaign effort with hours, days, and cost |
| Campaign Management | Draft, launch, and track creative campaigns with status |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Creative Director Agent                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Brand   │  │ Visual   │  │ Design   │  │Creative  │   │
│  │Identity  │  │ Asset    │  │ System   │  │Strategy  │   │
│  │Designer  │  │Designer  │  │ Builder  │  │Advisor   │   │
│  │          │  │          │  │          │  │          │   │
│  │• Palette │  │• Multi   │  │• Comps   │  │• Position│   │
│  │• Type    │  │• Specs   │  │• Tokens  │  │• Message │   │
│  │• Logo    │  │• Mockups │  │• Rules   │  │• Ideas   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │           │
│  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐   │
│  │ Content  │  │Creative  │  │  Time    │  │  Design  │   │
│  │Optimizer │  │Reviewer  │  │Estimator │  │  Asset   │   │
│  │          │  │          │  │          │  │ Storage  │   │
│  │• Score   │  │• 5 areas │  │• Hours   │  │• JSON    │   │
│  │• A/B     │  │• Weights │  │• Cost    │  │• Version │   │
│  │• Alt     │  │• Verdict │  │• Team    │  │• Export  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Data Layer                         │   │
│  │  Brand Identities │ Design Systems │ Campaigns       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Basic Usage

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

# Design asset
asset = agent.design_visual_asset(
    brief={"name": "Hero Image", "type": "image", "description": "Launch hero"},
    system_id=system["system_id"],
)

# Review creative
review = agent.review_creative(asset_id=asset["asset_id"])
print(f"Score: {review['overall_score']}")
```

### Command Line

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

print(identity["colors"])       # 5-color palette with HEX, RGB, HSL
print(identity["typography"])   # 3 font families (heading, body, mono)
print(identity["logo_concept"]) # Logo concept with layout specs
print(identity["voice"])        # Voice guidelines with do/don't
print(identity["imagery_style"]) # Imagery style with treatment
```

### Visual Assets

```python
asset = agent.design_visual_asset(
    brief={"name": "Hero Image", "type": "image", "description": "Launch hero"},
    system_id=system["system_id"],
)

print(asset["formats"])           # ["jpg", "webp", "png"]
print(asset["specs"])             # Resolution, size, color profile
print(asset["principles_applied"]) # ["balance", "contrast", "hierarchy"]
print(asset["accessibility"])     # Contrast ratio, alt text recommendations
```

### Design Systems

```python
system = agent.build_design_system(brand="NovaBrand")

print(f"Components: {system['components_count']}")
print(f"Categories: {system['categories']}")
print(f"Tokens: {system['tokens']}")
print(f"Guidelines: {system['guidelines']}")
print(f"Version: {system['version']}")

# Export system
exported = agent.export_system(system["system_id"], format="css")
```

### Creative Strategy

```python
strategy = agent.develop_creative_strategy(
    objective="launch",
    audience="tech professionals",
    channels=["web", "social", "email"],
    constraints={"timeline_weeks": 12, "budget": 10000},
)

print(strategy["positioning"])
print(strategy["key_messages"])
print(strategy["campaign_ideas"])
print(strategy["success_metrics"])
```

### Content Optimization

```python
optimized = agent.optimize_content(
    content={"headline": "New Feature Launch", "body": "We're excited to..."},
    channel="social",
    goal="engagement",
)

print(f"Score: {optimized['engagement_score']}")
for s in optimized["suggestions"]:
    print(f"  - {s}")
print(f"Alternatives: {optimized['alternative_versions']}")
```

### Creative Review

```python
review = agent.review_creative(asset_id=asset["asset_id"])

print(f"Score: {review['overall_score']}")
print(f"Verdict: {review['verdict']}")  # Approved, Needs Revision, Reject
print(f"Criteria Scores:")
for criteria, score in review["criteria_scores"].items():
    print(f"  {criteria}: {score}")
print(f"Strengths: {review['strengths']}")
print(f"Weaknesses: {review['weaknesses']}")
```

### Campaign Management

```python
campaign = agent.create_campaign(
    name="Spring Launch",
    objective="launch",
    target_audience="developers",
    channels=["social", "email"],
    budget=5000.0,
    duration_weeks=8,
)

print(f"Campaign ID: {campaign.campaign_id}")
print(f"Status: {campaign.status}")

# Launch
agent.launch_campaign(campaign.campaign_id)

# Check status
status = agent.get_status()
print(f"Active campaigns: {status['active_campaigns']}")
```

### Time Estimation

```python
estimate = agent.estimate_project(
    components=["logo", "hero_image", "social_templates", "email_template"],
    complexity="medium",
)

print(f"Hours: {estimate['total_hours']}")
print(f"Days: {estimate['total_days']}")
print(f"Cost: ${estimate['estimated_cost']}")
print(f"Breakdown:")
for component, hours in estimate["breakdown"].items():
    print(f"  {component}: {hours}h")
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

| Tone | Voice | Best For | Color Range |
|------|-------|----------|-------------|
| `professional` | Clear, factual | Enterprise, B2B | Blues (210-240) |
| `playful` | Energetic, witty | Consumer, youth | Warm (0-60) |
| `luxury` | Elegant, exclusive | Premium, fashion | Golds (30-60) |
| `minimalist` | Direct, clean | Tech, design | Any hue, low sat |
| `bold` | Confident, provocative | Disruption, DTC | Reds (340-20) |
| `friendly` | Warm, authentic | Community, support | Greens (80-160) |
| `technical` | Precise, structured | Engineering, SaaS | Cyans (180-260) |
| `warm` | Approachable, human | Health, family | Oranges (10-40) |
| `corporate` | Formal, established | Finance, legal | Navy (200-240) |
| `artisanal` | Handcrafted, authentic | Food, craft | Earth (20-60) |

## Asset Types

| Type | Description | Formats | Typical Use |
|------|-------------|---------|-------------|
| `logo` | Brand mark | SVG, PNG, JPG | Brand identity |
| `image` | Static visual | PNG, JPG, WEBP | Web, social |
| `video` | Motion content | MP4, MOV | Social, ads |
| `illustration` | Custom artwork | SVG, PNG | Web, editorial |
| `icon` | Glyph | SVG, PNG | UI, navigation |
| `template` | Design file | FIGMA, SKETCH | Design team |
| `motion_graphic` | Animation | MP4, GIF | Social, ads |
| `campaign_asset` | Marketing | Multiple | Campaigns |

## Design System Components

| Category | Variations | States |
|----------|-----------|--------|
| `button` | primary, secondary, tertiary, destructive, ghost | default, hover, focus, disabled, loading, error |
| `input` | default, error, success, disabled | default, focus, error, disabled, filled |
| `card` | default, outlined, elevated | default, hover, selected |
| `navigation` | top, side, bottom, mega | default, active, collapsed, mobile |
| `modal` | default, fullscreen, drawer | closed, opening, open, closing |
| `badge` | default, success, warning, error | default, pulse |

## Data Models

### Brand Identity
Complete brand system with deterministic 5-color palette, 3 typography families, logo concept, voice guidelines, and imagery style.

### Design System
Component library with design tokens (spacing, colors, typography), usage guidelines, version management, and multi-format export.

### Campaign
Creative campaign with objective, audience, channels, budget, duration, and status tracking (draft → active → completed → archived).

### Asset
Visual asset with format specs, design principles applied, accessibility notes, and version tracking.

## Configuration

```python
from agents.creative_director.agent import CreativeDirectorAgent, Config

config = Config(
    tone="professional",
    industry="technology",
    default_formats=["png", "jpg", "webp"],
    design_grid_columns=12,
    max_width_px=1200,
    accessibility_level="AA",  # WCAG 2.1 AA
    spacing_unit=8,  # 8px grid
    border_radius=8,
)
agent = CreativeDirectorAgent(config=config)
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `tone` | `"professional"` | Default brand tone |
| `industry` | `"technology"` | Default industry context |
| `default_formats` | `["png", "jpg"]` | Default export formats |
| `design_grid_columns` | `12` | Grid system columns |
| `max_width_px` | `1200` | Maximum asset width |
| `accessibility_level` | `"AA"` | WCAG compliance level |
| `spacing_unit` | `8` | Base spacing unit (px) |
| `border_radius` | `8` | Default border radius (px) |

## Examples

### Complete Brand Launch

```python
from agents.creative_director.agent import CreativeDirectorAgent

agent = CreativeDirectorAgent()

# 1. Create brand identity
identity = agent.create_brand_identity("AcmeTech", "technology", "technical")

# 2. Build design system
system = agent.build_design_system("AcmeTech")

# 3. Develop strategy
strategy = agent.develop_creative_strategy(
    objective="launch",
    audience="developers",
    channels=["web", "social"],
)

# 4. Create assets
hero = agent.design_visual_asset(
    {"name": "Hero", "type": "image", "description": "Product hero"},
    system["system_id"],
)

# 5. Review
review = agent.review_creative(hero["asset_id"])
if review["overall_score"] >= 80:
    print("Asset approved for launch!")

# 6. Launch campaign
campaign = agent.create_campaign(
    "Acme Launch", "launch", "developers",
    ["social", "email"], 10000.0, 12,
)
agent.launch_campaign(campaign.campaign_id)
```

## Best Practices

1. **Start with Strategy** — Define positioning and messaging before designing any assets
2. **Maintain Consistency** — Use the design system for all touchpoints; never go rogue
3. **Design for Accessibility** — WCAG 2.1 AA compliance minimum; AAA when possible
4. **Document Everything** — Brand guidelines prevent drift; version control prevents chaos
5. **Iterate Based on Data** — Use performance metrics to refine creative; gut feel isn't enough
6. **Collaborate Early** — Involve stakeholders in brand development; buy-in prevents rework
7. **Version Control** — Track design system versions; know what's deployed where
8. **Budget for Review** — Creative review takes time; don't skip it under deadline pressure
9. **Test Across Platforms** — What looks great on desktop may fail on mobile
10. **Build Reusable Components** — One well-designed button template beats 50 one-off buttons

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Colors inconsistent | Verify deterministic palette generation; same brand name = same colors |
| Components not rendering | Check token names match CSS custom property definitions exactly |
| Campaign launch fails | Verify campaign_id exists and current status allows the transition |
| Review score low | Address weakest criteria first; focus on quick wins before deep fixes |
| Timeline aggressive | Increase complexity estimate; add 20% buffer for revisions |
| Brand identity generic | Add industry-specific elements; research competitor visual language |
| Accessibility fails | Adjust palette for WCAG AA contrast ratios (4.5:1 text, 3:1 large text) |
| Export fails | Verify design system has data for requested format; check version |

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams and component details
- `GROK.md` — Agent instructions, identity, and API reference
- `README.md` — This file

## Contributing

1. Add new brand tone options with expanded color ranges
2. Enhance asset format support (WebP, AVIF, Lottie)
3. Add new component templates (table, form, tooltip, toast)
4. Improve review criteria with industry-specific benchmarks
5. Add Figma/Sketch plugin integration
6. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.