# Design Agent

> Comprehensive UI/UX design system management with component libraries,
> accessibility validation, design tokens, prototyping, user research,
> and multi-platform output generation.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![WCAG 2.1](https://img.shields.io/badge/WCAG-2.1%20AA-orange.svg)](https://www.w3.org/WAI/WCAG21/quickref/)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Design System Manager](#design-system-manager)
  - [Component Library](#component-library)
  - [Accessibility Checker](#accessibility-checker)
  - [Design Token Manager](#design-token-manager)
  - [Color Palette Manager](#color-palette-manager)
  - [Typography Manager](#typography-manager)
  - [Prototyping Engine](#prototyping-engine)
  - [User Research Manager](#user-research-manager)
  - [Figma Integration](#figma-integration)
  - [UI Component Generator](#ui-component-generator)
- [API Reference](#api-reference)
  - [DesignSystemManager](#designsystemmanager-api)
  - [ComponentLibrary](#componentlibrary-api)
  - [AccessibilityChecker](#accessibilitychecker-api)
  - [DesignTokenManager](#design-token-manager-api)
  - [ColorPaletteManager](#colorpalettemanager-api)
  - [TypographyManager](#typographymanager-api)
  - [PrototypingEngine](#prototypingengine-api)
  - [UserResearchManager](#userresearchmanager-api)
  - [FigmaIntegration](#figmaintegration-api)
  - [UIComponentGenerator](#uicomponentgenerator-api)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Design Agent is a comprehensive design system management platform built
entirely in Python with zero external dependencies. It provides tools for
creating, managing, validating, and exporting design systems across multiple
platforms (Web, iOS, Android).

### What It Does

- **Design System Management** — Create and manage colors, typography, spacing,
  shadows, borders, breakpoints, and z-indices with a single source of truth
- **Component Library** — Register UI components with props, events, slots,
  and generate production-ready CSS for each component
- **Accessibility Validation** — Check designs against WCAG 2.1 at A, AA, or AAA
  levels with detailed fix suggestions
- **Design Tokens** — W3C Design Token Format compatible management with
  alias resolution and multi-platform export (CSS, SCSS, JSON, Swift, Kotlin)
- **Color Theory** — Generate complementary, analogous, triadic,
  split-complementary, and tetradic color harmonies with shade scales
- **Typography** — Modular type scales (Major Third, Golden Ratio) with
  responsive CSS and font loading strategies
- **Prototyping** — Generate interactive HTML wireframes for common layouts
  (dashboard, login, landing, settings)
- **User Research** — Track participants, sessions, insights, and journey maps
- **Figma Integration** — Parse Figma data, extract design tokens, and generate
  platform-specific component code
- **Multi-Platform Output** — Export CSS, SCSS, React, SwiftUI, and Jetpack
  Compose from the same design system

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Zero dependencies | No external packages to manage, version, or audit |
| Dataclass-based models | Type-safe, self-documenting data structures |
| Observer pattern | Reactive workflows when design system changes |
| Strategy pattern | Clean multi-platform output without if/else chains |
| WCAG-first | Accessibility is checked by default, not as an afterthought |

---

## Features

### Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| Design System Manager | Central hub for all design decisions | Complete |
| Color Management | Add, remove, generate palettes, validate contrast | Complete |
| Typography Management | Font families, type scales, responsive CSS | Complete |
| Spacing System | Base-unit scaling, rem conversion | Complete |
| Shadow Tokens | Configurable box-shadow values | Complete |
| Border Tokens | Width, style, color, radius | Complete |
| Breakpoint System | Responsive breakpoints (sm, md, lg, xl, 2xl) | Complete |
| Z-Index Layers | Conflict-free z-index system | Complete |

### Component Features

| Feature | Description | Status |
|---------|-------------|--------|
| Button Component | 8 variants, 5 sizes, focus, disabled states | Complete |
| Card Component | Default, elevated, outlined variants | Complete |
| Input Component | With labels, helpers, error states | Complete |
| Modal Component | Overlay, header, body, footer | Complete |
| Toast Component | Success, error, warning, info variants | Complete |
| Navbar Component | Responsive with mobile toggle | Complete |
| Sidebar Component | Icon + label navigation | Complete |
| Table Component | Accessible with headers and captions | Complete |
| Tabs Component | ARIA tablist with keyboard navigation | Complete |
| Accordion Component | Expandable sections with ARIA | Complete |
| Breadcrumb Component | Accessible navigation trail | Complete |
| Pagination Component | Page navigation with ARIA | Complete |
| Dropdown Component | Select with label and options | Complete |

### Accessibility Features

| Feature | Description | Status |
|---------|-------------|--------|
| Color Contrast Check | WCAG 2.1 ratio calculation | Complete |
| HTML Validation | Semantic HTML, ARIA, labels | Complete |
| Palette Validation | All color combinations checked | Complete |
| WCAG Report | Summary with errors, warnings, passes | Complete |
| WCAG Levels | A, AA, AAA support | Complete |

### Token Features

| Feature | Description | Status |
|---------|-------------|--------|
| Token CRUD | Create, read, update, delete tokens | Complete |
| Token Groups | Organize tokens by category | Complete |
| Alias Resolution | Token references with chain support | Complete |
| CSS Export | `:root` custom properties | Complete |
| SCSS Export | `$variable` format | Complete |
| JSON Export | Structured token data | Complete |
| W3C Format | Design Token Community Group spec | Complete |
| Swift Export | `UIColor` extensions | Complete |
| Kotlin Export | Compose `Color` objects | Complete |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DESIGN AGENT                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │ DesignSystemManager │  │ DesignTokenManager   │              │
│  │ (Central Hub)       │──│ (W3C Tokens)         │              │
│  └─────────┬───────────┘  └─────────┬────────────┘              │
│            │                         │                           │
│  ┌─────────┴─────────────────────────┴────────────┐             │
│  │            Processing Layer                     │             │
│  │  ┌────────────┐ ┌──────────────┐ ┌───────────┐ │             │
│  │  │ Component  │ │ Accessibility│ │ Color     │ │             │
│  │  │ Library    │ │ Checker      │ │ Palette   │ │             │
│  │  └────────────┘ └──────────────┘ └───────────┘ │             │
│  │  ┌────────────┐ ┌──────────────┐ ┌───────────┐ │             │
│  │  │ Typography │ │ Prototyping  │ │ User      │ │             │
│  │  │ Manager    │ │ Engine       │ │ Research  │ │             │
│  │  └────────────┘ └──────────────┘ └───────────┘ │             │
│  └─────────────────────────────────────────────────┘            │
│            │                                                     │
│  ┌─────────┴─────────────────────────────────────┐              │
│  │            Output Layer                        │              │
│  │  CSS │ SCSS │ JSON │ React │ SwiftUI │ Compose │              │
│  └───────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Quick Start

### Minimal Setup (3 lines)

```python
from agents.design.agent import DesignSystemManager

ds = DesignSystemManager("My System")
ds.add_color("primary", "#3B82F6")
print(ds.export_css_variables())
```

### Complete Design System

```python
from agents.design.agent import DesignSystemManager

ds = DesignSystemManager("Acme Design System", "1.0.0", base_spacing=4)

# Colors
ds.add_color("primary", "#3B82F6", "brand")
ds.add_color("secondary", "#10B981", "brand")
ds.add_color("error", "#EF4444", "semantic")
ds.generate_palette("#3B82F6", "primary")

# Typography
ds.add_typography("heading", "Inter", 32, 700)
ds.add_typography("body", "Inter", 16, 400)

# Spacing & Layout
ds.generate_spacing_scale()
ds.set_breakpoints()
ds.set_z_indices()

# Export
print(ds.export_css_variables())
```

### Accessibility-First Workflow

```python
from agents.design.agent import (
    AccessibilityChecker, AccessibilityLevel, ColorValue
)

a11y = AccessibilityChecker(AccessibilityLevel.AA)

# Check contrast
fg = ColorValue("text", "#111827")
bg = ColorValue("surface", "#FFFFFF")
result = a11y.check_color_contrast(fg, bg, font_size=16)
print(result.message)  # "Contrast ratio 15.36:1 meets WCAG AA"

# Check HTML
issues = a11y.check_html(html_string)
for issue in issues:
    if issue.severity == "error":
        print(f"FIX: {issue.message} — {issue.fix_suggestion}")
```

---

## Installation

### From Repository

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
```

### Dependencies

**None.** The Design Agent uses only Python standard library modules:
- `colorsys` — Color space conversions
- `json` — Serialization
- `re` — Regular expressions
- `uuid` — Unique identifiers
- `logging` — Observability
- `dataclasses` — Data models
- `enum` — Type-safe enumerations
- `abc` — Abstract base classes
- `math` — Mathematical operations
- `datetime` — Timestamps
- `hashlib` — Hashing utilities
- `pathlib` — File path handling

### Python Version

Requires Python 3.10+ for:
- `match` statements (used in some patterns)
- Improved `dataclass` features
- Type hint syntax (`X | Y` union types)

---

## Usage

### Design System Manager

The central hub for all design decisions.

```python
from agents.design.agent import DesignSystemManager

ds = DesignSystemManager(
    name="Acme Design System",
    version="2.0.0",
    base_spacing=4,
    base_font_size=16
)

# Colors
ds.add_color("primary", "#3B82F6", "brand")
ds.add_color("secondary", "#10B981", "brand")
ds.add_color("error", "#EF4444", "semantic")
ds.add_color("warning", "#F59E0B", "semantic")
ds.add_color("surface", "#FFFFFF", "neutral")
ds.add_color("text", "#111827", "neutral")

# Generate 10-step shade palette
ds.generate_palette("#3B82F6", name="primary", steps=10)

# Typography
ds.add_typography("heading-1", "Inter", 32, font_weight=700)
ds.add_typography("heading-2", "Inter", 24, font_weight=600)
ds.add_typography("body", "Inter", 16, font_weight=400)
ds.add_typography("caption", "Inter", 12, font_weight=400)

# Generate modular type scale
ds.generate_type_scale(base_size=16, ratio=1.25)

# Spacing
ds.generate_spacing_scale()

# Breakpoints
ds.set_breakpoints(sm=640, md=768, lg=1024, xl=1280)

# Z-Index layers
ds.set_z_indices()

# Shadows
ds.add_shadow("sm", y=1, blur=2)
ds.add_shadow("md", y=4, blur=6)
ds.add_shadow("lg", y=10, blur=15)

# Borders
ds.add_border("default", width=1, style="solid", color="#E5E7EB")
ds.add_border("focus", width=2, style="solid", color="#3B82F6")

# Custom tokens
from agents.design.agent import TokenType
ds.add_token("animation.fast", TokenType.MOTION, "150ms ease")
ds.add_token("animation.normal", TokenType.MOTION, "250ms ease")

# Export
css = ds.export_css_variables()
json_data = ds.export_json()
theme = ds.generate_theme()
tokens = ds.export_design_tokens()

# Subscribe to changes
ds.subscribe(lambda sys: print(f"Updated: {sys.get_stats()}"))

# Get stats
stats = ds.get_stats()
```

### Component Library

Build and manage accessible UI components.

```python
from agents.design.agent import (
    ComponentLibrary, ComponentProp, ComponentEvent,
    ComponentVariant, ComponentSize
)

lib = ComponentLibrary(ds)

# Register a button
lib.register_component(
    name="Button",
    props=[
        ComponentProp("variant", "string", "primary",
                      options=["primary", "secondary", "outline", "ghost"]),
        ComponentProp("size", "string", "md",
                      options=["xs", "sm", "md", "lg", "xl"]),
        ComponentProp("disabled", "boolean", False),
        ComponentProp("loading", "boolean", False),
        ComponentProp("icon", "ReactNode", None),
    ],
    events=[
        ComponentEvent("onClick", "Click handler"),
        ComponentEvent("onFocus", "Focus handler"),
        ComponentEvent("onBlur", "Blur handler"),
    ],
    variants=list(ComponentVariant),
    sizes=list(ComponentSize),
)

# Generate CSS
button_css = lib.generate_button_css()
card_css = lib.generate_card_css()
input_css = lib.generate_input_css()
modal_css = lib.generate_modal_css()
toast_css = lib.generate_toast_css()

# List components
print(lib.list_components())  # ["Button"]

# Generate any registered component
css = lib.generate_component("Button")
```

### Accessibility Checker

Validate designs against WCAG 2.1.

```python
from agents.design.agent import AccessibilityChecker, AccessibilityLevel, ColorValue

# Initialize at AA level
a11y = AccessibilityChecker(AccessibilityLevel.AA)

# Check color contrast
fg = ColorValue("text", "#111827")
bg = ColorValue("surface", "#FFFFFF")
result = a11y.check_color_contrast(fg, bg, font_size=16)
# result.severity = "pass", result.message = "Contrast ratio 15.36:1 meets WCAG AA"

# Check large text (18pt+)
result = a11y.check_color_contrast(fg, bg, font_size=20, is_bold=True)

# Check HTML for issues
html = """
<html>
<body>
  <img src="photo.jpg">
  <input type="email">
  <button></button>
  <a href="/page"></a>
</body>
</html>
"""
issues = a11y.check_html(html)
# Returns issues for: missing alt, missing label, empty button,
# missing lang, empty link

# Check full color palette
colors = [
    ColorValue("primary", "#3B82F6"),
    ColorValue("secondary", "#10B981"),
    ColorValue("text", "#111827"),
    ColorValue("surface", "#FFFFFF"),
]
palette_issues = a11y.check_color_palette(colors)

# Generate report
report = a11y.generate_report()
# {
#   "level": "AA",
#   "total_issues": 4,
#   "errors": 3,
#   "warnings": 1,
#   "passes": 1,
#   "issues": [...]
# }

# Reset for next audit
a11y.reset()
```

### Design Token Manager

W3C-compatible token management with multi-platform export.

```python
from agents.design.agent import DesignTokenManager, TokenType

tm = DesignTokenManager("acme-tokens")

# Create tokens in groups
tm.create_token("color.primary", TokenType.COLOR, "#3B82F6",
                "Primary brand color", group="colors")
tm.create_token("color.secondary", TokenType.COLOR, "#10B981",
                group="colors")
tm.create_token("font.heading", TokenType.TYPOGRAPHY, "Inter, sans-serif",
                group="typography")
tm.create_token("spacing.unit", TokenType.SPACING, "4px", group="spacing")
tm.create_token("shadow.md", TokenType.SHADOW, "0 4px 6px rgba(0,0,0,0.1)",
                group="shadows")

# Create aliases
tm.create_alias("color.brand", "color.primary")
tm.create_alias("button.bg", "color.primary")

# Resolve aliases
token = tm.resolve_alias("color.brand")
print(token.value)  # "#3B82F6"

# Get tokens by group
color_tokens = tm.get_group("colors")

# Export to multiple formats
css = tm.export_css()
scss = tm.export_scss()
json_str = tm.export_json()
swift = tm.export_swift()
kotlin = tm.export_kotlin()
w3c = tm.export_w3c_format()

# Validate naming
errors = tm.validate()
# [] if all valid

# Merge managers
other = DesignTokenManager("extra")
other.create_token("extra.token", TokenType.COLOR, "#000")
tm.merge(other)
```

### Color Palette Generator

Generate color harmonies and shade scales.

```python
from agents.design.agent import ColorPaletteManager

cpm = ColorPaletteManager()

# Complementary harmony
comp = cpm.generate_harmony("#3B82F6", "complementary")
# {"base": ColorValue("#3B82F6"), "complement": ColorValue("#F6923B")}

# Analogous harmony
analog = cpm.generate_harmony("#3B82F6", "analogous")

# Triadic harmony
triad = cpm.generate_harmony("#3B82F6", "triadic")

# Split-complementary
split = cpm.generate_harmony("#3B82F6", "split-complementary")

# Tetradic (4-color)
tetradic = cpm.generate_harmony("#3B82F6", "tetradic")

# Shade scale (50-950)
shades = cpm.generate_shade_scale("#3B82F6", "blue", steps=11)
# {"blue-50": ..., "blue-100": ..., ..., "blue-950": ...}

# Get contrast suggestions
suggestions = cpm.get_contrast_suggestions("#9CA3AF", "#FFFFFF", 4.5)
# ["#6B7280", "#4B5563", "#374151"]

# Export palette
simple = cpm.export_palette("complementary")
```

### Typography Manager

Generate modular type scales and responsive typography.

```python
from agents.design.agent import TypographyManager

tpm = TypographyManager()

# Register fonts
tpm.register_font_family("Inter", ["Helvetica Neue", "Arial"])
tpm.register_font_family("Georgia", ["Times New Roman"])

# Major Third (1.25) scale
scale = tpm.generate_major_third_scale(16)
# {"2xs": 10px, "xs": 13px, "sm": 14px, "base": 16px,
#  "md": 20px, "lg": 25px, "xl": 31px, "2xl": 39px, ...}

# Golden Ratio (1.618) scale
golden = tpm.generate_golden_ratio_scale(16)

# Responsive CSS with clamp()
css = tpm.generate_responsive_css()

# @font-face declarations
font_face = tpm.generate_font_face_css()

# Font stack
stack = tpm.get_font_stack("Inter")
# "'Inter', 'Helvetica Neue', Arial, sans-serif"

# Export as JSON
json_str = tpm.export_type_scale_json()
```

### Prototyping Engine

Generate interactive HTML wireframes.

```python
from agents.design.agent import PrototypingEngine

proto = PrototypingEngine(ds)

# Generate wireframes
dashboard = proto.generate_wireframe("dashboard")
login = proto.generate_wireframe("login")
landing = proto.generate_wireframe("landing")
settings = proto.generate_wireframe("settings")

# Each is a complete, self-contained HTML file

# Register custom prototypes
proto.register_prototype("checkout", html="<html>...</html>",
                         description="E-commerce checkout")

# List and retrieve
protos = proto.list_prototypes()
html = proto.get_prototype("checkout")
```

### User Research Manager

Track research activities and insights.

```python
from agents.design.agent import UserResearchManager, ResearchMethod

urm = UserResearchManager()

# Add participants
p = urm.add_participant(demographics={"age_range": "25-34"})

# Log sessions
urm.log_session(
    participant_id=p.participant_id,
    method=ResearchMethod.USABILITY_TESTING,
    duration_minutes=45,
    notes="Tested checkout flow"
)

# Record insights
urm.add_insight(
    title="Discount code hidden on mobile",
    description="Users couldn't find discount input",
    category="usability",
    severity="high"
)

# Create journey maps
urm.create_journey_map("checkout", steps=[
    {"title": "View Cart", "emotion": "neutral"},
    {"title": "Checkout", "emotion": "anxious"},
])

# Generate report
report = urm.generate_report()

# Export journey map
text = urm.export_journey_map("checkout")
```

### Figma Integration

Parse Figma data and generate platform-specific code.

```python
from agents.design.agent import FigmaIntegration, Platform

figma = FigmaIntegration()

# Parse Figma colors (RGBA 0-1 → hex)
hex_val = figma.parse_figma_color({"r": 0.231, "g": 0.510, "b": 0.965})
# "#3b82f6"

# Parse Figma nodes
node = {"id": "1:1", "name": "Button", "type": "COMPONENT",
        "fills": [{"type": "SOLID", "color": {"r": 0.231, "g": 0.510, "b": 0.965}}]}
parsed = figma.parse_figma_node(node)

# Extract design tokens
tokens = figma.extract_design_tokens({"colors": {...}, "text_styles": {...}})

# Generate platform code
react = figma.generate_component_code(node, Platform.WEB)
swift = figma.generate_component_code(node, Platform.IOS)
compose = figma.generate_component_code(node, Platform.ANDROID)

# Sync styles
figma.sync_styles("file-id", style_data)
history = figma.get_sync_history()
```

### UI Component Generator

Generate accessible HTML components.

```python
from agents.design.agent import UIComponentGenerator

uigen = UIComponentGenerator(ds)

# Navbar
navbar = uigen.generate_navbar("Brand", ["Home", "About", "Contact"])

# Sidebar
sidebar = uigen.generate_sidebar([
    {"icon": "home", "label": "Dashboard", "href": "/dashboard"},
    {"icon": "chart", "label": "Analytics", "href": "/analytics"},
])

# Table
table = uigen.generate_table(["Name", "Email", "Role"], rows=5)

# Tabs (with ARIA)
tabs = uigen.generate_tabs(["Tab 1", "Tab 2", "Tab 3"])

# Accordion
accordion = uigen.generate_accordion([
    {"title": "Section 1", "content": "Content..."},
    {"title": "Section 2", "content": "Content..."},
])

# Breadcrumb
breadcrumb = uigen.generate_breadcrumb([
    {"label": "Home", "href": "/"},
    {"label": "Page", "href": ""},
])

# Pagination
pagination = uigen.generate_pagination(total_pages=10, current_page=1)

# Dropdown
dropdown = uigen.generate_dropdown("Country", ["US", "UK", "CA"])
```

---

## API Reference

### DesignSystemManager API

#### Constructor

```python
DesignSystemManager(
    name: str = "Default Design System",
    version: str = "1.0.0",
    base_spacing: int = 4,
    base_font_size: int = 16
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | `"Default Design System"` | System name |
| `version` | `str` | `"1.0.0"` | Semantic version |
| `base_spacing` | `int` | `4` | Base spacing unit in px |
| `base_font_size` | `int` | `16` | Base font size in px |

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `add_color(name, hex_value, role, opacity)` | `ColorValue` | Add a color |
| `get_color(name)` | `Optional[ColorValue]` | Get color by name |
| `remove_color(name)` | `bool` | Remove a color |
| `get_all_colors()` | `List[ColorValue]` | Get all colors |
| `generate_palette(base_color, name, steps)` | `Dict[str, ColorValue]` | Generate shade palette |
| `add_typography(name, family, size, weight, lh)` | `TypographyValue` | Add typography |
| `get_typography(name)` | `Optional[TypographyValue]` | Get typography |
| `generate_type_scale(base_size, ratio, family)` | `Dict[str, TypographyValue]` | Generate type scale |
| `add_spacing(name, value, unit)` | `SpacingValue` | Add spacing token |
| `generate_spacing_scale()` | `Dict[str, SpacingValue]` | Generate spacing scale |
| `add_shadow(name, x, y, blur, spread, color)` | `ShadowValue` | Add shadow |
| `add_border(name, width, style, color, radius)` | `BorderValue` | Add border |
| `set_breakpoints(sm, md, lg, xl, 2xl)` | `Dict[str, int]` | Set breakpoints |
| `set_z_indices(layers)` | `Dict[str, int]` | Set z-index layers |
| `add_token(name, type, value, description)` | `DesignToken` | Add custom token |
| `export_css_variables()` | `str` | Export as CSS |
| `export_json()` | `str` | Export as JSON |
| `export_design_tokens()` | `DesignSystemExport` | Export full system |
| `generate_theme()` | `Dict[str, Any]` | Generate theme dict |
| `subscribe(callback)` | `None` | Subscribe to changes |
| `get_stats()` | `Dict[str, int]` | Get summary stats |

### ComponentLibrary API

#### Constructor

```python
ComponentLibrary(design_system: DesignSystemManager)
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `register_component(name, props, events, slots, variants, sizes, states)` | `Dict` | Register component |
| `get_component(name)` | `Optional[Dict]` | Get component def |
| `list_components()` | `List[str]` | List all components |
| `generate_button_css(variants, sizes)` | `str` | Button CSS |
| `generate_card_css()` | `str` | Card CSS |
| `generate_input_css()` | `str` | Input CSS |
| `generate_modal_css()` | `str` | Modal CSS |
| `generate_toast_css()` | `str` | Toast CSS |
| `generate_component(name, platform)` | `str` | Generate any component |

### AccessibilityChecker API

#### Constructor

```python
AccessibilityChecker(level: AccessibilityLevel = AccessibilityLevel.AA)
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `check_color_contrast(fg, bg, font_size, is_bold)` | `AccessibilityIssue` | Check contrast |
| `check_html(html)` | `List[AccessibilityIssue]` | Check HTML |
| `check_color_palette(colors)` | `List[AccessibilityIssue]` | Check palette |
| `generate_report()` | `Dict[str, Any]` | Summary report |
| `reset()` | `None` | Clear issues |
| `get_rules()` | `Dict[str, str]` | Get rules |

### Design Token Manager API

#### Constructor

```python
DesignTokenManager(name: str = "design-tokens")
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `create_token(name, type, value, desc, group)` | `DesignToken` | Create token |
| `create_alias(alias, target)` | `None` | Create alias |
| `resolve_alias(name, depth)` | `DesignToken` | Resolve alias |
| `get_token(name)` | `Optional[DesignToken]` | Get token |
| `get_group(group)` | `List[DesignToken]` | Get group tokens |
| `export_w3c_format()` | `Dict` | W3C export |
| `export_css()` | `str` | CSS export |
| `export_scss()` | `str` | SCSS export |
| `export_json()` | `str` | JSON export |
| `export_swift()` | `str` | Swift export |
| `export_kotlin()` | `str` | Kotlin export |
| `validate()` | `List[str]` | Validate tokens |
| `merge(other)` | `None` | Merge managers |

### Color Palette Manager API

#### Constructor

```python
ColorPaletteManager()
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `generate_harmony(base_hex, harmony_type)` | `Dict[str, ColorValue]` | Generate harmony |
| `generate_shade_scale(base_hex, name, steps)` | `Dict[str, ColorValue]` | Generate shades |
| `get_contrast_suggestions(fg_hex, bg_hex, target)` | `List[str]` | Contrast fixes |
| `export_palette(name)` | `Dict[str, str]` | Export palette |

### Typography Manager API

#### Constructor

```python
TypographyManager()
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `register_font_family(name, fallbacks)` | `None` | Register font |
| `add_type_style(name, family, size, weight, lh, ls)` | `TypographyValue` | Add style |
| `generate_major_third_scale(base_size)` | `Dict[str, TypographyValue]` | Major Third scale |
| `generate_golden_ratio_scale(base_size)` | `Dict[str, TypographyValue]` | Golden Ratio scale |
| `generate_responsive_css()` | `str` | Responsive CSS |
| `generate_font_face_css()` | `str` | @font-face CSS |
| `get_font_stack(family)` | `str` | Font stack |
| `export_type_scale_json()` | `str` | JSON export |

### Prototyping Engine API

#### Constructor

```python
PrototypingEngine(design_system: DesignSystemManager)
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `generate_wireframe(layout)` | `str` | Generate wireframe |
| `register_prototype(name, html, description)` | `None` | Register prototype |
| `list_prototypes()` | `List[str]` | List prototypes |
| `get_prototype(name)` | `Optional[str]` | Get prototype HTML |

### User Research Manager API

#### Constructor

```python
UserResearchManager()
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `add_participant(id, demographics)` | `ResearchParticipant` | Add participant |
| `log_session(participant_id, method, duration, notes, tasks)` | `Dict` | Log session |
| `add_insight(title, desc, category, severity, sessions)` | `Dict` | Add insight |
| `create_journey_map(name, steps)` | `Dict` | Create journey map |
| `get_insights_by_category(category)` | `List[Dict]` | Filter insights |
| `get_insights_by_severity(severity)` | `List[Dict]` | Filter insights |
| `generate_report()` | `Dict[str, Any]` | Summary report |
| `export_journey_map(name)` | `str` | Export journey map |

### Figma Integration API

#### Constructor

```python
FigmaIntegration(access_token: Optional[str] = None)
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `parse_figma_color(figma_color)` | `str` | RGBA to hex |
| `parse_figma_node(node)` | `Dict[str, Any]` | Parse node tree |
| `register_file(file_id, name, pages, components)` | `FigmaFile` | Register file |
| `extract_design_tokens(figma_data)` | `Dict[str, DesignToken]` | Extract tokens |
| `generate_component_code(node, platform)` | `str` | Generate code |
| `sync_styles(file_id, style_data)` | `Dict` | Sync styles |
| `get_sync_history()` | `List[Dict]` | Sync history |

### UI Component Generator API

#### Constructor

```python
UIComponentGenerator(design_system: DesignSystemManager)
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `generate_navbar(brand, links, output)` | `str` | Navbar HTML |
| `generate_sidebar(items)` | `str` | Sidebar HTML |
| `generate_table(headers, rows)` | `str` | Table HTML |
| `generate_dropdown(label, options)` | `str` | Dropdown HTML |
| `generate_tabs(tabs)` | `str` | Tabs HTML |
| `generate_accordion(items)` | `str` | Accordion HTML |
| `generate_breadcrumb(items)` | `str` | Breadcrumb HTML |
| `generate_pagination(total_pages, current_page)` | `str` | Pagination HTML |

---

## Examples

### Example 1: Full Design System with CSS Export

```python
from agents.design.agent import DesignSystemManager

ds = DesignSystemManager("SaaS App", "1.0.0")

# Define complete color system
colors = {
    "primary": "#3B82F6",
    "secondary": "#8B5CF6",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#06B6D4",
    "text": "#111827",
    "text-secondary": "#6B7280",
    "surface": "#FFFFFF",
    "background": "#F9FAFB",
    "border": "#E5E7EB",
}

for name, hex_val in colors.items():
    role = "semantic" if name in ("success", "warning", "error", "info") else "neutral"
    if name in ("primary", "secondary"):
        role = "brand"
    ds.add_color(name, hex_val, role)

# Generate palettes for brand colors
ds.generate_palette("#3B82F6", "primary")
ds.generate_palette("#8B5CF6", "secondary")

# Typography
ds.add_typography("display", "Inter", 48, 800, 1.1)
ds.add_typography("h1", "Inter", 36, 700, 1.2)
ds.add_typography("h2", "Inter", 28, 600, 1.3)
ds.add_typography("h3", "Inter", 22, 600, 1.4)
ds.add_typography("body-lg", "Inter", 18, 400, 1.6)
ds.add_typography("body", "Inter", 16, 400, 1.5)
ds.add_typography("body-sm", "Inter", 14, 400, 1.5)
ds.add_typography("caption", "Inter", 12, 400, 1.4)

# Spacing
ds.generate_spacing_scale()

# Shadows
ds.add_shadow("xs", y=1, blur=2, color="rgba(0,0,0,0.05)")
ds.add_shadow("sm", y=1, blur=3, color="rgba(0,0,0,0.1)")
ds.add_shadow("md", y=4, blur=6, color="rgba(0,0,0,0.1)")
ds.add_shadow("lg", y=10, blur=15, color="rgba(0,0,0,0.1)")
ds.add_shadow("xl", y=20, blur=25, color="rgba(0,0,0,0.15)")

# Breakpoints
ds.set_breakpoints()

# Z-index
ds.set_z_indices()

# Export
print(ds.export_css_variables())
```

### Example 2: Accessibility Audit

```python
from agents.design.agent import AccessibilityChecker, AccessibilityLevel, ColorValue

a11y = AccessibilityChecker(AccessibilityLevel.AA)

# Test color combinations
combos = [
    ("text", "#111827", "surface", "#FFFFFF"),
    ("primary", "#3B82F6", "surface", "#FFFFFF"),
    ("text-secondary", "#6B7280", "surface", "#FFFFFF"),
    ("error", "#EF4444", "surface", "#FFFFFF"),
]

for name, fg_hex, bg_name, bg_hex in combos:
    fg = ColorValue(name, fg_hex)
    bg = ColorValue(bg_name, bg_hex)
    result = a11y.check_color_contrast(fg, bg, font_size=16)
    status = "PASS" if result.severity == "pass" else "FAIL"
    print(f"{name} on {bg_name}: {status} — {result.message}")

# Check page HTML
issues = a11y.check_html(page_html)
errors = [i for i in issues if i.severity == "error"]
print(f"\nFound {len(errors)} accessibility errors")
for e in errors:
    print(f"  - {e.rule_id}: {e.message}")
    print(f"    Fix: {e.fix_suggestion}")
```

### Example 3: Design Tokens to Multiple Platforms

```python
from agents.design.agent import DesignTokenManager, TokenType

tm = DesignTokenManager("cross-platform")

# Define tokens
tm.create_token("color.primary", TokenType.COLOR, "#3B82F6", group="colors")
tm.create_token("color.surface", TokenType.COLOR, "#FFFFFF", group="colors")
tm.create_token("font.body", TokenType.TYPOGRAPHY, "Inter, sans-serif", group="fonts")
tm.create_token("spacing.md", TokenType.SPACING, "16px", group="spacing")

# Export for web
css = tm.export_css()
print("=== Web (CSS) ===")
print(css)

# Export for iOS
swift = tm.export_swift()
print("\n=== iOS (Swift) ===")
print(swift)

# Export for Android
kotlin = tm.export_kotlin()
print("\n=== Android (Kotlin) ===")
print(kotlin)

# Export as W3C tokens
w3c = tm.export_w3c_format()
print("\n=== W3C Format ===")
import json
print(json.dumps(w3c, indent=2))
```

---

## Configuration

### DesignSystemManager Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `name` | `str` | `"Default Design System"` | System name |
| `version` | `str` | `"1.0.0"` | Version string |
| `base_spacing` | `int` | `4` | Base spacing unit (px) |
| `base_font_size` | `int` | `16` | Base font size (px) |

### AccessibilityChecker Levels

| Level | Contrast (Normal) | Contrast (Large) | Description |
|-------|-------------------|------------------|-------------|
| `A` | N/A | N/A | Minimum compliance |
| `AA` | 4.5:1 | 3.0:1 | Standard compliance |
| `AAA` | 7.0:1 | 4.5:1 | Enhanced compliance |

### Color Harmony Types

| Type | Colors | Description |
|------|--------|-------------|
| `complementary` | 2 | Opposite on color wheel |
| `analogous` | 3 | Adjacent on color wheel |
| `triadic` | 3 | Equally spaced (120°) |
| `split-complementary` | 3 | Base + 2 adjacent to complement |
| `tetradic` | 4 | Rectangle on color wheel |

### Export Formats

| Format | Platform | Method |
|--------|----------|--------|
| CSS | Web | `export_css_variables()` |
| SCSS | Web | `export_scss()` |
| JSON | Any | `export_json()` |
| W3C | Any | `export_w3c_format()` |
| Swift | iOS | `export_swift()` |
| Kotlin | Android | `export_kotlin()` |

---

## Best Practices

### 1. Start with Tokens

Always define design tokens before building components. Tokens are the
single source of truth and enable consistency across platforms.

```python
# Good: Token-first approach
tm = DesignTokenManager()
tm.create_token("color.primary", TokenType.COLOR, "#3B82F6")
# Components reference tokens, not hardcoded values

# Bad: Hardcoded values
ds.add_color("button-bg", "#3B82F6")  # What if primary changes?
```

### 2. Validate Accessibility Early

Run accessibility checks before exporting. Fix issues at the design level,
not in code.

```python
# Check before export
issues = a11y.check_html(generated_html)
errors = [i for i in issues if i.severity == "error"]
if errors:
    # Fix design, don't export broken designs
    raise ValueError(f"Accessibility errors: {len(errors)}")
```

### 3. Use Semantic Color Roles

Name colors by their purpose, not their value.

```python
# Good: Semantic naming
ds.add_color("primary", "#3B82F6", "brand")
ds.add_color("error", "#EF4444", "semantic")

# Bad: Value-based naming
ds.add_color("blue", "#3B82F6")
ds.add_color("red", "#EF4444")
```

### 4. Subscribe to Changes

Use the observer pattern to keep downstream artifacts in sync.

```python
ds.subscribe(lambda sys: regenerate_css_file(sys))
ds.subscribe(lambda sys: sync_to_figma(sys))
# Every change triggers regeneration
```

### 5. Version Your Design System

Track versions and use semantic versioning for breaking changes.

```python
ds = DesignSystemManager("Acme", "2.0.0")  # Major = breaking
# 1.x → 2.0: Renamed tokens, removed components
# 2.0 → 2.1: Added new tokens, non-breaking
```

---

## Troubleshooting

### Common Issues

**Invalid hex color error**
```
ValueError: Invalid hex color: #XYZ
```
Solution: Ensure hex colors start with `#` and contain 3 or 6 valid hex characters.

**Alias resolution recursion**
```
RecursionError: Alias resolution exceeded max depth
```
Solution: Check for circular aliases. The system limits depth to 10.

**Missing font in output**
```
Font stack shows only fallbacks
```
Solution: Register the font family first with `register_font_family()`.

**Empty CSS output**
```
:root { }
```
Solution: Ensure tokens/colors/typography are added before calling `export_css_variables()`.

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
# All operations log detailed information
```

---

## Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
python agents/design/agent.py  # Run demonstration
```

### Code Style

- Type hints on all public methods
- Docstrings for all public classes and methods
- Dataclasses for all data models
- Enums for all fixed sets of values
- Logging at module level

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
