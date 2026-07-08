# Design Agent Architecture

## Table of Contents

1. [System Overview](#system-overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Deep Dives](#component-deep-dives)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Tech Stack](#tech-stack)
7. [Token Management Architecture](#token-management-architecture)
8. [Accessibility Architecture](#accessibility-architecture)
9. [Multi-Platform Output](#multi-platform-output)
10. [Security Considerations](#security-considerations)
11. [Scalability Patterns](#scalability-patterns)
12. [Testing Strategy](#testing-strategy)
13. [Deployment Architecture](#deployment-architecture)

---

## System Overview

The Design Agent is a comprehensive design system management platform that orchestrates
color systems, typography, spacing, component libraries, accessibility validation,
prototyping, user research, and multi-platform code generation.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DESIGN AGENT                                 │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │   Design      │  │   Token      │  │   Component              │  │
│  │   System      │  │   Manager    │  │   Library                │  │
│  │   Manager     │  │              │  │                          │  │
│  └──────┬───────┘  └──────┬───────┘  └────────────┬─────────────┘  │
│         │                 │                        │                │
│  ┌──────┴─────────────────┴────────────────────────┴─────────────┐  │
│  │                    CORE ORCHESTRATION LAYER                    │  │
│  └──────┬─────────────────┬────────────────────────┬─────────────┘  │
│         │                 │                        │                │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌────────────┴─────────────┐  │
│  │  Accessibility│  │  Prototyping │  │  User Research            │  │
│  │  Checker      │  │  Engine      │  │  Manager                  │  │
│  └──────┬───────┘  └──────┬───────┘  └────────────┬─────────────┘  │
│         │                 │                        │                │
│  ┌──────┴─────────────────┴────────────────────────┴─────────────┐  │
│  │                    OUTPUT GENERATION LAYER                     │  │
│  │  CSS Variables │ SCSS │ Tailwind │ React │ SwiftUI │ Compose  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## High-Level Architecture

### Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                      │
│  ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │ CSS     │ │ React    │ │ SwiftUI  │ │ Compose    │  │
│  │ Output  │ │ Output   │ │ Output   │ │ Output     │  │
│  └─────────┘ └──────────┘ └──────────┘ └────────────┘  │
├─────────────────────────────────────────────────────────┤
│                  PROCESSING LAYER                        │
│  ┌──────────────────┐  ┌─────────────────────────────┐  │
│  │ Component        │  │ Accessibility               │  │
│  │ Generator        │  │ Checker                     │  │
│  └──────────────────┘  └─────────────────────────────┘  │
│  ┌──────────────────┐  ┌─────────────────────────────┐  │
│  │ Prototyping      │  │ User Research               │  │
│  │ Engine           │  │ Manager                     │  │
│  └──────────────────┘  └─────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                  DOMAIN LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Design       │  │ Token        │  │ Color        │  │
│  │ System       │  │ Manager      │  │ Palette      │  │
│  │ Manager      │  │              │  │ Manager      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │ Typography   │  │ Figma        │                    │
│  │ Manager      │  │ Integration  │                    │
│  └──────────────┘  └──────────────┘                    │
├─────────────────────────────────────────────────────────┤
│                  FOUNDATION LAYER                        │
│  ┌─────────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ Data Classes│ │ Enums    │ │ Logging  │ │ Utils  │ │
│  └─────────────┘ └──────────┘ └──────────┘ └────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Component Interaction Map

```
DesignSystemManager ──────┬──────────────────────────────────────┐
       │                  │                                      │
       ├──► ColorValue ───┤──► AccessibilityChecker              │
       ├──► TypographyValue┤                                      │
       ├──► SpacingValue  │──► ColorPaletteManager               │
       ├──► ShadowValue   │                                      │
       ├──► BorderValue   │──► TypographyManager                 │
       │                  │                                      │
       ▼                  ▼                                      ▼
  ComponentLibrary   DesignTokenManager ──────► FigmaIntegration
       │                  │
       ├──► Button CSS    ├──► CSS Variables
       ├──► Card CSS      ├──► SCSS Variables
       ├──► Input CSS     ├──► JSON Tokens
       ├──► Modal CSS     ├──► Swift Tokens
       └──► Toast CSS     └──► Kotlin Tokens
                                 │
  PrototypingEngine ◄────────────┘
       │
       ├──► Dashboard Wireframe
       ├──► Login Wireframe
       ├──► Landing Wireframe
       └──► Settings Wireframe

  UserResearchManager
       │
       ├──► Participants
       ├──► Sessions
       ├──► Insights
       └──► Journey Maps
```

---

## Component Deep Dives

### 1. DesignSystemManager

The central hub that owns all design tokens, colors, typography, spacing,
and generates exportable formats.

```
┌─────────────────────────────────────────────────┐
│              DesignSystemManager                 │
├─────────────────────────────────────────────────┤
│ - name: str                                      │
│ - version: str                                   │
│ - base_spacing: int                              │
│ - base_font_size: int                            │
│ - _colors: Dict[str, ColorValue]                 │
│ - _typography: Dict[str, TypographyValue]        │
│ - _spacing: Dict[str, SpacingValue]              │
│ - _shadows: Dict[str, ShadowValue]               │
│ - _borders: Dict[str, BorderValue]               │
│ - _tokens: Dict[str, DesignToken]                │
│ - _breakpoints: Dict[str, int]                   │
│ - _z_indices: Dict[str, int]                     │
│ - _listeners: List[Callable]                     │
├─────────────────────────────────────────────────┤
│ + add_color(name, hex, role) → ColorValue        │
│ + get_color(name) → Optional[ColorValue]         │
│ + generate_palette(base, name, steps) → Dict     │
│ + add_typography(name, family, size, ...) → ...  │
│ + generate_type_scale(base, ratio, family)       │
│ + add_spacing(name, value, unit) → SpacingValue  │
│ + generate_spacing_scale() → Dict                │
│ + add_shadow(name, x, y, blur, spread, color)    │
│ + add_border(name, width, style, color, radius)  │
│ + set_breakpoints(sm, md, lg, xl, 2xl)          │
│ + set_z_indices(layers) → Dict                   │
│ + add_token(name, type, value, desc)             │
│ + export_css_variables() → str                   │
│ + export_json() → str                            │
│ + export_design_tokens() → DesignSystemExport    │
│ + generate_theme() → Dict                        │
│ + subscribe(callback) → None                     │
│ + get_stats() → Dict                             │
└─────────────────────────────────────────────────┘
```

**Key Responsibilities:**
- Owns the single source of truth for all design decisions
- Manages observer pattern for reactive updates
- Generates CSS custom properties, JSON, and DesignToken export format
- Validates color hex values on input
- Tracks creation and modification timestamps

### 2. ComponentLibrary

Manages a registry of UI components with full prop/event/slot definitions
and generates CSS for each component.

```
┌─────────────────────────────────────────────────┐
│              ComponentLibrary                    │
├─────────────────────────────────────────────────┤
│ - _ds: DesignSystemManager                       │
│ - _components: Dict[str, Dict[str, Any]]         │
│ - _component_count: int                          │
├─────────────────────────────────────────────────┤
│ + register_component(name, props, events, ...)   │
│ + get_component(name) → Optional[Dict]           │
│ + list_components() → List[str]                  │
│ + generate_button_css(variants, sizes) → str     │
│ + generate_card_css() → str                      │
│ + generate_input_css() → str                     │
│ + generate_modal_css() → str                     │
│ + generate_toast_css() → str                     │
│ + generate_component(name, platform) → str       │
└─────────────────────────────────────────────────┘
```

**Component Variant System:**
```
                    ┌─── primary ──┐
                    │              │
              ┌─── secondary ──┐  │
              │               │  │
        ┌─── outline ──┐     │  │
        │              │     │  │
  ┌─── ghost ──┐      │     │  │
  │            │      │     │  │
Button ────────┼──────┼─────┼──┘
  │            │      │     │
  └─── link ───┘      │     │
        │              │     │
        └─── destructive┘     │
              │               │
              └─── success ───┘
                    │
                    └─── warning ─┘
```

### 3. AccessibilityChecker

Validates design output against WCAG 2.1 guidelines at A, AA, or AAA levels.

```
┌─────────────────────────────────────────────────┐
│            AccessibilityChecker                  │
├─────────────────────────────────────────────────┤
│ - level: AccessibilityLevel                      │
│ - _issues: List[AccessibilityIssue]              │
│ - _rules: Dict[str, str]                         │
├─────────────────────────────────────────────────┤
│ WCAG_AA_NORMAL = 4.5:1                           │
│ WCAG_AA_LARGE = 3.0:1                            │
│ WCAG_AAA_NORMAL = 7.0:1                          │
│ WCAG_AAA_LARGE = 4.5:1                           │
├─────────────────────────────────────────────────┤
│ + check_color_contrast(fg, bg, size, bold)       │
│ + check_html(html) → List[AccessibilityIssue]    │
│ + check_color_palette(colors) → List[Issues]     │
│ + generate_report() → Dict                       │
│ + reset() → None                                 │
│ + get_rules() → Dict                             │
└─────────────────────────────────────────────────┘
```

**Accessibility Validation Flow:**
```
Input (HTML/Colors/Components)
         │
         ▼
┌─────────────────────┐
│   Parse Input        │
│   (HTML → DOM, etc.) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐     ┌──────────────────┐
│  Color Contrast     │────►│ WCAG Ratio Calc  │
│  Check              │     │ (Luminance-based) │
└──────────┬──────────┘     └──────────────────┘
           │
           ▼
┌─────────────────────┐     ┌──────────────────┐
│  Semantic HTML      │────►│ ARIA Validation  │
│  Validation         │     │ Label/Role Check  │
└──────────┬──────────┘     └──────────────────┘
           │
           ▼
┌─────────────────────┐     ┌──────────────────┐
│  Keyboard           │────►│ Tab Order, Focus  │
│  Navigation Check   │     │ Trap Detection    │
└──────────┬──────────┘     └──────────────────┘
           │
           ▼
┌─────────────────────┐
│  Issue Collection   │
│  & Report Generation│
└─────────────────────┘
```

### 4. DesignTokenManager

W3C Design Token Format compatible token management with alias resolution,
multi-platform export, and validation.

```
┌─────────────────────────────────────────────────┐
│           DesignTokenManager                     │
├─────────────────────────────────────────────────┤
│ - name: str                                      │
│ - _tokens: Dict[str, DesignToken]                │
│ - _token_groups: Dict[str, List[str]]            │
│ - _aliases: Dict[str, str]                       │
├─────────────────────────────────────────────────┤
│ + create_token(name, type, value, desc, group)   │
│ + create_alias(alias, target) → None             │
│ + resolve_alias(name, depth) → DesignToken       │
│ + get_token(name) → Optional[DesignToken]        │
│ + get_group(group) → List[DesignToken]           │
│ + export_w3c_format() → Dict                     │
│ + export_css() → str                             │
│ + export_scss() → str                            │
│ + export_json() → str                            │
│ + export_swift() → str                           │
│ + export_kotlin() → str                          │
│ + validate() → List[str]                         │
│ + merge(other) → None                            │
└─────────────────────────────────────────────────┘
```

**Token Resolution Chain:**
```
color.brand
    │
    ├──► _aliases["color.brand"] = "color.primary"
    │
    ▼
color.primary
    │
    ├──► _tokens["color.primary"] = DesignToken(value="#3B82F6")
    │
    ▼
Return Token(#3B82F6)

Aliases can chain:
  color.brand → color.primary → color.blue.500 → #3B82F6
```

### 5. ColorPaletteManager

Generates color harmonies (complementary, analogous, triadic, etc.)
and shade scales with contrast-aware suggestions.

```
┌─────────────────────────────────────────────────┐
│          ColorPaletteManager                     │
├─────────────────────────────────────────────────┤
│ - _palettes: Dict[str, Dict[str, ColorValue]]    │
│ - _harmony_cache: Dict[str, List[str]]           │
├─────────────────────────────────────────────────┤
│ + generate_harmony(base, type) → Dict            │
│ + generate_shade_scale(base, name, steps) → Dict │
│ + get_contrast_suggestions(fg, bg, target)       │
│ + export_palette(name) → Dict[str, str]          │
└─────────────────────────────────────────────────┘
```

**Harmony Types:**
```
Complementary:     Analogous:        Triadic:
      ●                 ●               ●
     /                 / \             / \
    ○                 ●   ●           ●   ●
                                              
Split-Comp:        Tetradic:
      ●               ●   ●
     / \              │   │
    ●   ●             ●───●
```

---

## Data Flow

### Design System Creation Flow

```
User Request
    │
    ▼
┌───────────────────┐
│ Initialize        │
│ DesignSystemMgr   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐     ┌──────────────────────┐
│ Define Colors     │────►│ Validate Hex Format   │
│ add_color()       │     │ Register in Dict      │
└────────┬──────────┘     └──────────────────────┘
         │
         ▼
┌───────────────────┐     ┌──────────────────────┐
│ Define Typography │────►│ Scale Calculation     │
│ add_typography()  │     │ Line Height Derive    │
└────────┬──────────┘     └──────────────────────┘
         │
         ▼
┌───────────────────┐     ┌──────────────────────┐
│ Define Spacing    │────►│ Base Unit Scale       │
│ add_spacing()     │     │ Rem Conversion        │
└────────┬──────────┘     └──────────────────────┘
         │
         ▼
┌───────────────────┐
│ Set Breakpoints   │
│ Set Z-Indices     │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐     ┌──────────────────────┐
│ Export            │────►│ CSS / JSON / Tokens   │
│ export_*()        │     │ Swift / Kotlin        │
└───────────────────┘     └──────────────────────┘
```

### Token Export Pipeline

```
DesignTokenManager
         │
         ├──► export_css()    ──► ":root { --token: value; }"
         │
         ├──► export_scss()   ──► "$token: value;"
         │
         ├──► export_json()   ──► '{ "token": { "type": "...", "value": "..." } }'
         │
         ├──► export_swift()  ──► "extension UIColor { static let token = ... }"
         │
         ├──► export_kotlin() ──► "object AppColors { val token = Color(...) }"
         │
         └──► export_w3c_format() ──► { "$type": "...", "$value": "..." }
```

### Accessibility Check Flow

```
HTML/Color Input
    │
    ▼
┌──────────────────┐
│ Check 1:         │
│ Color Contrast   │──── Compute WCAG ratio
│ (Luminance)      │     Compare to threshold
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Check 2:         │
│ Semantic HTML    │──── Verify <html lang>
│                  │     Verify landmarks
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Check 3:         │
│ ARIA Attributes  │──── Validate roles
│                  │     Check required props
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Check 4:         │
│ Form Labels      │──── Match <label> to <input>
│                  │     Check aria-label
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Check 5:         │
│ Keyboard         │──── Tab order
│ Navigation       │     Focus indicators
└────────┬─────────┘     No keyboard traps
         │
         ▼
┌──────────────────┐
│ Aggregate        │
│ Issues & Report  │
└──────────────────┘
```

---

## Design Patterns

### 1. Observer Pattern

Used by `DesignSystemManager` to notify listeners when the design system changes.

```python
class DesignSystemManager:
    def __init__(self):
        self._listeners: List[Callable] = []

    def subscribe(self, callback: Callable) -> None:
        """Register a change listener."""
        self._listeners.append(callback)

    def _touch(self) -> None:
        """Notify all listeners of a change."""
        self._updated_at = datetime.now()
        for listener in self._listeners:
            listener(self)

# Usage:
ds = DesignSystemManager()
ds.subscribe(lambda sys: print(f"System updated: {sys.name}"))
ds.add_color("primary", "#3B82F6")  # Triggers listener
```

**Why:** Enables reactive workflows — when colors change, downstream
components can auto-regenerate without explicit polling.

### 2. Strategy Pattern

Used for multi-platform output generation in `UIComponentGenerator`.

```python
class OutputStrategy(ABC):
    @abstractmethod
    def generate(self, component: Dict) -> str: ...

class CSSOutputStrategy(OutputStrategy):
    def generate(self, component: Dict) -> str:
        return f".{component['name']} {{ ... }}"

class ReactOutputStrategy(OutputStrategy):
    def generate(self, component: Dict) -> str:
        return f"export const {component['name']} = () => {{ ... }}"

class SwiftUIOutputStrategy(OutputStrategy):
    def generate(self, component: Dict) -> str:
        return f"struct {component['name']}View: View {{ ... }}"
```

**Why:** Each platform has fundamentally different output syntax.
Strategy pattern avoids giant if/else chains and makes adding new platforms trivial.

### 3. Factory Pattern

Used in `PrototypingEngine` to create wireframes by layout name.

```python
class PrototypingEngine:
    def generate_wireframe(self, layout: str) -> str:
        wireframes = {
            "dashboard": self._dashboard_wireframe(),
            "login": self._login_wireframe(),
            "landing": self._landing_wireframe(),
            "settings": self._settings_wireframe(),
        }
        return wireframes.get(layout, self._dashboard_wireframe())
```

**Why:** New wireframe types can be added without changing the public API.
The factory method maps layout names to generation functions.

### 4. Composite Pattern

Used for component hierarchies — components contain sub-components
(slots, children) with uniform interfaces.

```python
@dataclass
class ComponentSlot:
    name: str
    required: bool = False
    default_content: str = ""

# A Card component composes Header, Body, Footer slots
# Each slot is itself a renderable unit
card = ComponentLibrary.register_component(
    "Card",
    slots=[
        ComponentSlot("header", required=True),
        ComponentSlot("body", required=True),
        ComponentSlot("footer", required=False),
    ]
)
```

**Why:** UI components are inherently hierarchical. Composite pattern
lets you treat individual elements and compositions uniformly.

### 5. Builder Pattern

Used in `DesignSystemManager` for progressive system construction.

```python
ds = (DesignSystemManager("My System")
    .add_color("primary", "#3B82F6")
    .add_color("secondary", "#10B981")
    .add_typography("heading", "Inter", 32)
    .generate_spacing_scale()
    .set_breakpoints())
```

**Why:** Design systems are built incrementally. Builder pattern
enables fluent, readable construction without massive constructor args.

### 6. Adapter Pattern

Used in `FigmaIntegration` to convert Figma-specific data formats
into the design system's internal model.

```python
class FigmaIntegration:
    def parse_figma_color(self, figma_color: Dict[str, float]) -> str:
        """Adapt Figma RGBA (0-1) to standard hex."""
        r = int(figma_color.get("r", 0) * 255)
        g = int(figma_color.get("g", 0) * 255)
        b = int(figma_color.get("b", 0) * 255)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def parse_figma_node(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt Figma node tree to simplified internal format."""
        ...
```

**Why:** External tools (Figma) use their own data formats.
Adapter pattern keeps the core system format-agnostic.

### 7. Template Method Pattern

Used in `DesignOutput` abstract base class.

```python
class DesignOutput(ABC):
    @abstractmethod
    def generate(self, design_system: DesignSystemManager) -> str:
        ...

    @abstractmethod
    def get_format(self) -> OutputFormat:
        ...

class CSSOutput(DesignOutput):
    def generate(self, ds: DesignSystemManager) -> str:
        return ds.export_css_variables()

    def get_format(self) -> OutputFormat:
        return OutputFormat.CSS
```

**Why:** Enforces a contract for all output generators while letting
each subclass implement format-specific logic.

---

## Tech Stack

### Core Dependencies

```
┌─────────────────────────────────────────────┐
│ Python 3.10+                                 │
├─────────────────────────────────────────────┤
│ Standard Library:                            │
│   ├── colorsys (color manipulation)          │
│   ├── json (serialization)                   │
│   ├── re (regex parsing)                     │
│   ├── uuid (unique IDs)                      │
│   ├── logging (observability)                │
│   ├── dataclasses (data models)              │
│   ├── enum (type safety)                     │
│   ├── abc (abstract contracts)               │
│   ├── math (calculations)                    │
│   ├── hashlib (hashing)                      │
│   └── datetime (timestamps)                  │
├─────────────────────────────────────────────┤
│ Zero external dependencies — fully self-     │
│ contained within Python standard library.    │
└─────────────────────────────────────────────┘
```

### Output Format Support

| Format       | Target        | Extension     | Status  |
|-------------|---------------|---------------|---------|
| CSS         | Web           | `.css`         | Active  |
| SCSS        | Web           | `.scss`        | Active  |
| JSON        | Any           | `.json`        | Active  |
| W3C Tokens  | Any           | `.json`        | Active  |
| Swift       | iOS           | `.swift`       | Active  |
| Kotlin      | Android       | `.kt`          | Active  |

### Platform Support

| Platform       | Output Type      | Generator              |
|---------------|------------------|------------------------|
| Web           | CSS/SCSS         | `export_css_variables` |
| React         | JSX/TSX          | `generate_react_*`     |
| React Native  | StyleSheet       | `generate_rn_*`        |
| iOS (SwiftUI) | Swift            | `export_swift`         |
| Android       | Compose          | `export_kotlin`        |
| Flutter       | Dart             | `generate_dart_*`      |

---

## Token Management Architecture

### Token Types and Hierarchy

```
Design Tokens
├── Primitive Tokens (raw values)
│   ├── color.blue.500: #3B82F6
│   ├── font.size.base: 16px
│   └── spacing.unit: 4px
│
├── Semantic Tokens (purpose-based)
│   ├── color.primary: {color.blue.500}
│   ├── color.error: {color.red.500}
│   ├── font.heading: {font.inter.bold}
│   └── spacing.component.padding: {spacing.4}
│
└── Component Tokens (component-specific)
    ├── button.background: {color.primary}
    ├── button.padding: {spacing.component.padding}
    ├── input.border: {color.border.default}
    └── card.shadow: {shadow.md}
```

### W3C Design Token Format

```json
{
  "color": {
    "$description": "Color tokens",
    "primary": {
      "$type": "color",
      "$value": "#3B82F6",
      "$description": "Primary brand color"
    },
    "error": {
      "$type": "color",
      "$value": "#EF4444"
    }
  },
  "spacing": {
    "unit": {
      "$type": "spacing",
      "$value": "4px"
    },
    "component-padding": {
      "$type": "spacing",
      "$value": "{spacing.unit} * 4"
    }
  }
}
```

### Token Resolution Algorithm

```
resolve("color.brand"):
  1. Check _aliases → found "color.primary"
  2. resolve("color.primary"):
     a. Check _aliases → not found
     b. Check _tokens → found DesignToken(value="#3B82F6")
     c. Return token
  3. Return resolved token

Guard: max depth = 10 (prevents infinite alias loops)
```

---

## Accessibility Architecture

### WCAG 2.1 Compliance Matrix

```
Level A (Minimum):
  ✅ 1.1.1  Non-text Content (alt text)
  ✅ 1.3.1  Info and Relationships (semantic HTML)
  ✅ 1.4.1  Use of Color (not sole indicator)
  ✅ 2.1.1  Keyboard accessible
  ✅ 2.4.1  Bypass Blocks (skip nav)
  ✅ 2.4.2  Page Titled
  ✅ 3.1.1  Language of Page
  ✅ 4.1.2  Name, Role, Value (ARIA)

Level AA (Target):
  ✅ 1.4.3  Contrast Minimum (4.5:1)
  ✅ 1.4.4  Resize Text (200%)
  ✅ 1.4.5  Images of Text
  ✅ 2.4.5  Multiple Ways
  ✅ 2.4.6  Headings and Labels
  ✅ 2.4.7  Focus Visible
  ✅ 3.2.4  Consistent Identification

Level AAA (Enhanced):
  ✅ 1.4.6  Contrast Enhanced (7:1)
  ✅ 1.4.8  Visual Presentation
  ✅ 2.4.10  Section Headings
```

### Contrast Ratio Calculation

```
Relative Luminance (L):
  For each RGB channel (sRGB 0-1):
    if value <= 0.03928:
      linear = value / 12.92
    else:
      linear = ((value + 0.055) / 1.055) ^ 2.4

  L = 0.2126 * R + 0.7152 * G + 0.0722 * B

Contrast Ratio:
  ratio = (L1 + 0.05) / (L2 + 0.05)
  where L1 = lighter, L2 = darker

Thresholds:
  WCAG AA Normal Text:  ≥ 4.5:1
  WCAG AA Large Text:   ≥ 3.0:1
  WCAG AAA Normal Text: ≥ 7.0:1
  WCAG AAA Large Text:  ≥ 4.5:1
  Large text: ≥ 18pt or ≥ 14pt bold
```

---

## Multi-Platform Output

### Output Generation Pipeline

```
DesignSystemManager
         │
         ▼
┌────────────────────┐
│ Export Strategy     │
│ Selection           │
└────────┬───────────┘
         │
    ┌────┴────┬────────┬──────────┬──────────┐
    ▼         ▼        ▼          ▼          ▼
  CSS      SCSS     JSON      Swift     Kotlin
    │         │        │          │          │
    ▼         ▼        ▼          ▼          ▼
  Variables  Variables Tokens    UIColor   Compose
  (:root)   ($var)    (dict)    Extension  Theme
```

### Platform-Specific Adaptations

**Web (CSS):**
```css
:root {
  --color-primary: #3B82F6;
  --font-heading-size: 32px;
  --spacing-md: 16px;
}
```

**iOS (Swift):**
```swift
extension UIColor {
    static let primary = UIColor(hex: "#3B82F6")
}
```

**Android (Kotlin Compose):**
```kotlin
object AppColors {
    val primary = Color(0xFF3B82F6)
}
```

---

## Security Considerations

### Input Validation

```
┌─────────────────────────────────────────────────┐
│ Input Validation Points                          │
├─────────────────────────────────────────────────┤
│                                                  │
│ 1. Color Hex Format                              │
│    Pattern: /^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$/│
│    Reject: Non-hex characters, wrong length      │
│                                                  │
│ 2. Token Names                                   │
│    Pattern: /^[a-z0-9][a-z0-9.\-]*$/             │
│    Reject: Uplift, spaces, special chars         │
│                                                  │
│ 3. Numeric Ranges                                │
│    Font size: 8-200px                            │
│    Spacing: 0-512px                              │
│    Opacity: 0.0-1.0                              │
│    Contrast ratio: computed, not input           │
│                                                  │
│ 4. HTML Output (XSS Prevention)                  │
│    All user content escaped before embedding     │
│    No eval() or exec() on user input             │
│    Component content uses text nodes, not innerHTML│
└─────────────────────────────────────────────────┘
```

### Data Protection

- Design tokens may contain brand-sensitive color values
- Figma access tokens should never be logged or exported
- Export functions do not include API keys or secrets
- All file I/O uses explicit path validation

### Dependency Policy

- Zero external dependencies (standard library only)
- No network calls from core logic
- Figma integration uses explicit token injection (no ambient credentials)

---

## Scalability Patterns

### Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| add_color | O(1) | Dict insertion |
| export_css_variables | O(n) | n = total tokens |
| generate_palette | O(steps) | Fixed steps per call |
| check_color_contrast | O(1) | Pure computation |
| check_html | O(m) | m = HTML length |
| resolve_alias | O(d) | d = alias chain depth |
| export_w3c_format | O(n) | n = total tokens |

### Memory Management

- All data is in-memory dictionaries (no database required)
- Tokens are lightweight dataclass instances
- Palette caches avoid regeneration
- Observer list is the only unbounded growth point (mitigated by explicit subscribe/unsubscribe)

### Scaling Strategies

```
Single-Process (Current):
  ┌──────────────────────────┐
  │ Design System Manager    │
  │ In-Memory State          │
  │ Synchronous Operations   │
  └──────────────────────────┘

Horizontal (Future):
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │ Worker 1 │  │ Worker 2 │  │ Worker 3 │
  │ (Colors) │  │ (Tokens) │  │ (Export) │
  └────┬─────┘  └────┬─────┘  └────┬─────┘
       │              │              │
       └──────────────┼──────────────┘
                      ▼
              ┌──────────────┐
              │ Shared State │
              │ (Redis/DB)   │
              └──────────────┘
```

### Caching Strategy

- Palette shade scales are cached after generation
- Alias resolution is computed on-demand (no pre-cache)
- CSS output is generated fresh each call (cheap operation)
- Figma sync history is append-only

---

## Testing Strategy

### Test Pyramid

```
           ╱╲
          ╱  ╲
         ╱ E2E╲         (Full workflow tests)
        ╱──────╲
       ╱        ╲
      ╱Integration╲     (Cross-component tests)
     ╱──────────────╲
    ╱                ╲
   ╱   Unit Tests     ╲  (Per-class tests)
  ╱────────────────────╲
```

### Unit Test Coverage

| Component | Key Tests |
|-----------|-----------|
| ColorValue | hex→RGB, hex→HSL, luminance, contrast ratio |
| TypographyValue | CSS generation, scaling |
| DesignSystemManager | add/get/remove colors, palette gen, CSS export |
| ComponentLibrary | Component registration, CSS generation |
| AccessibilityChecker | Contrast checks, HTML validation, report gen |
| DesignTokenManager | Token CRUD, alias resolution, merge, validation |
| ColorPaletteManager | All harmony types, shade scale, suggestions |
| TypographyManager | Type scales, font stacks, responsive CSS |
| FigmaIntegration | Color parsing, node parsing, token extraction |
| UserResearchManager | Participant CRUD, session logging, reporting |

### Integration Tests

- Design system → CSS export roundtrip
- Token manager → Figma sync → token extraction
- Accessibility check → report generation
- Component library → full CSS output validation

---

## Deployment Architecture

### Standalone Mode

```
┌──────────────────────────────┐
│ Python Script                │
│   └── agent.py               │
│       └── main()             │
│           ├── Design System  │
│           ├── Components     │
│           ├── Accessibility  │
│           └── Export         │
└──────────────────────────────┘
```

### As a Library

```python
from agents.design.agent import (
    DesignSystemManager,
    ComponentLibrary,
    AccessibilityChecker,
    DesignTokenManager,
)

ds = DesignSystemManager("My System")
ds.add_color("primary", "#3B82F6")

lib = ComponentLibrary(ds)
css = lib.generate_button_css()

a11y = AccessibilityChecker()
report = a11y.check_html(html_string)
```

### CI/CD Integration

```
┌────────┐     ┌────────────┐     ┌──────────────┐
│ Commit │────►│ Run Tests  │────►│ Validate     │
│        │     │            │     │ A11y Report  │
└────────┘     └────────────┘     └──────┬───────┘
                                         │
                                    Pass │ Fail
                                         │
                              ┌──────────┴──────────┐
                              ▼                     ▼
                     ┌──────────────┐     ┌──────────────┐
                     │ Build Export │     │ Block Merge  │
                     │ (CSS, Tokens)│     │ Fix Issues   │
                     └──────────────┘     └──────────────┘
```

---

## Appendix: File Structure

```
agents/design/
├── agent.py           # Core implementation (all classes)
├── ARCHITECTURE.md    # This document
├── GROK.md            # Agent identity and capabilities
└── README.md          # User-facing documentation
```

## Appendix: Class Relationship Diagram

```
DesignSystemManager ◄────────────────── ComponentLibrary
       │                                        │
       ├── ColorValue                           ├── Button CSS
       ├── TypographyValue                      ├── Card CSS
       ├── SpacingValue                         ├── Input CSS
       ├── ShadowValue                          ├── Modal CSS
       ├── BorderValue                          └── Toast CSS
       │
       ├── DesignTokenManager ◄──── FigmaIntegration
       │         │                       │
       │         ├── Token CRUD          ├── parse_figma_color()
       │         ├── Alias Resolution    ├── parse_figma_node()
       │         ├── CSS Export          ├── extract_design_tokens()
       │         ├── SCSS Export         └── generate_component_code()
       │         ├── JSON Export
       │         ├── Swift Export        UserResearchManager
       │         └── Kotlin Export              │
       │                                       ├── Participants
       ├── ColorPaletteManager                  ├── Sessions
       │         │                              ├── Insights
       │         ├── Harmony Generation         └── Journey Maps
       │         ├── Shade Scale
       │         └── Contrast Suggestions       AccessibilityChecker
       │                                              │
       ├── TypographyManager                         ├── WCAG Checks
       │         │                                    ├── HTML Validation
       │         ├── Type Scales                     ├── Contrast Analysis
       │         ├── Font Stacks                     └── Report Generation
       │         └── Responsive CSS
       │
       └── PrototypingEngine
                 │
                 ├── Dashboard Wireframe
                 ├── Login Wireframe
                 ├── Landing Wireframe
                 └── Settings Wireframe
```
