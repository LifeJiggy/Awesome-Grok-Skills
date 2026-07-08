"""
Design Agent - UI/UX Design System Management
==============================================
Comprehensive design system management with component libraries,
accessibility checking, design tokens, prototyping, user research,
and Figma integration.

Author: Awesome Grok Skills
Version: 2.0.0
License: MIT
"""

from __future__ import annotations

import colorsys
import json
import logging
import re
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(handler)


# =============================================================================
# Enums
# =============================================================================

class ColorFormat(Enum):
    HEX = "hex"
    RGB = "rgb"
    HSL = "hsl"
    RGBA = "rgba"
    HSLA = "hsla"


class ComponentVariant(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    OUTLINE = "outline"
    GHOST = "ghost"
    LINK = "link"
    DESTRUCTIVE = "destructive"
    SUCCESS = "success"
    WARNING = "warning"


class ComponentSize(Enum):
    XS = "xs"
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"


class ComponentState(Enum):
    DEFAULT = "default"
    HOVER = "hover"
    ACTIVE = "active"
    FOCUS = "focus"
    DISABLED = "disabled"
    LOADING = "loading"
    ERROR = "error"
    SUCCESS = "success"


class AccessibilityLevel(Enum):
    A = "A"
    AA = "AA"
    AAA = "AAA"


class TokenType(Enum):
    COLOR = "color"
    TYPOGRAPHY = "typography"
    SPACING = "spacing"
    SHADOW = "shadow"
    BORDER = "border"
    MOTION = "motion"
    OPACITY = "opacity"
    BREAKPOINT = "breakpoint"
    Z_INDEX = "z-index"


class Platform(Enum):
    WEB = "web"
    IOS = "ios"
    ANDROID = "android"
    REACT_NATIVE = "react-native"
    FLUTTER = "flutter"


class ResearchMethod(Enum):
    USABILITY_TESTING = "usability_testing"
    INTERVIEW = "interview"
    SURVEY = "survey"
    A_B_TESTING = "a_b_testing"
    HEURISTIC_EVALUATION = "heuristic_evaluation"
    CARD_SORTING = "card_sorting"
    TREE_TESTING = "tree_testing"
    JOURNEY_MAPPING = "journey_mapping"


class FigmaNodeType(Enum):
    FRAME = "FRAME"
    GROUP = "GROUP"
    TEXT = "TEXT"
    RECTANGLE = "RECTANGLE"
    ELLIPSE = "ELLIPSE"
    VECTOR = "VECTOR"
    COMPONENT = "COMPONENT"
    COMPONENT_SET = "COMPONENT_SET"
    INSTANCE = "INSTANCE"


class OutputFormat(Enum):
    CSS = "css"
    SCSS = "scss"
    STYLED_COMPONENTS = "styled_components"
    TAILWIND = "tailwind"
    JSON = "json"
    YAML = "yaml"
    SWIFT_UI = "swift_ui"
    JETPACK_COMPOSE = "jetpack_compose"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ColorValue:
    name: str
    hex_value: str
    role: str = "primary"
    opacity: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_rgb(self) -> Tuple[int, int, int]:
        h = self.hex_value.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    def to_hsl(self) -> Tuple[float, float, float]:
        r, g, b = self.to_rgb()
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        return (round(h * 360, 2), round(s * 100, 2), round(l * 100, 2))

    def to_css(self, fmt: ColorFormat = ColorFormat.HEX) -> str:
        if fmt == ColorFormat.HEX:
            return self.hex_value
        r, g, b = self.to_rgb()
        if fmt == ColorFormat.RGB:
            return f"rgb({r}, {g}, {b})"
        h, s, l = self.to_hsl()
        if fmt == ColorFormat.HSL:
            return f"hsl({h}, {s}%, {l}%)"
        if fmt == ColorFormat.RGBA:
            return f"rgba({r}, {g}, {b}, {self.opacity})"
        if fmt == ColorFormat.HSLA:
            return f"hsla({h}, {s}%, {l}%, {self.opacity})"
        return self.hex_value

    def luminance(self) -> float:
        r, g, b = self.to_rgb()
        channels = []
        for c in [r / 255, g / 255, b / 255]:
            channels.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
        return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

    def contrast_ratio(self, other: "ColorValue") -> float:
        l1, l2 = self.luminance(), other.luminance()
        return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

    def is_light(self) -> bool:
        return self.luminance() > 0.179

    def is_dark(self) -> bool:
        return not self.is_light()


@dataclass
class TypographyValue:
    name: str
    font_family: str
    font_size: int
    font_weight: int = 400
    line_height: float = 1.5
    letter_spacing: float = 0.0
    text_transform: str = "none"
    text_decoration: str = "none"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_css(self) -> str:
        return (
            f"font-family: '{self.font_family}', sans-serif;\n"
            f"  font-size: {self.font_size}px;\n"
            f"  font-weight: {self.font_weight};\n"
            f"  line-height: {self.line_height};\n"
            f"  letter-spacing: {self.letter_spacing}em;"
        )

    def scale(self, factor: float) -> "TypographyValue":
        return TypographyValue(
            name=f"{self.name}_scaled", font_family=self.font_family,
            font_size=round(self.font_size * factor), font_weight=self.font_weight,
            line_height=self.line_height, letter_spacing=self.letter_spacing,
        )


@dataclass
class SpacingValue:
    name: str
    value: int
    unit: str = "px"
    scale_factor: float = 1.0

    def to_css(self) -> str:
        return f"{int(self.value * self.scale_factor)}{self.unit}"

    def to_rem(self, base: int = 16) -> str:
        return f"{round((self.value * self.scale_factor) / base, 4)}rem"


@dataclass
class ShadowValue:
    name: str
    x_offset: int = 0
    y_offset: int = 2
    blur_radius: int = 4
    spread_radius: int = 0
    color: str = "rgba(0, 0, 0, 0.1)"
    inset: bool = False

    def to_css(self) -> str:
        prefix = "inset " if self.inset else ""
        return (f"{prefix}{self.x_offset}px {self.y_offset}px "
                f"{self.blur_radius}px {self.spread_radius}px {self.color}")


@dataclass
class BorderValue:
    name: str
    width: int = 1
    style: str = "solid"
    color: str = "#E5E7EB"
    radius: int = 0

    def to_css(self) -> str:
        return f"{self.width}px {self.style} {self.color}"

    def to_css_radius(self) -> str:
        return f"{self.radius}px"


@dataclass
class DesignToken:
    name: str
    token_type: TokenType
    value: Any
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_css_variable(self) -> str:
        return f"--{self.name.replace('.', '-')}"


@dataclass
class ComponentProp:
    name: str
    prop_type: str
    default_value: Any = None
    required: bool = False
    description: str = ""
    options: List[Any] = field(default_factory=list)


@dataclass
class ComponentEvent:
    name: str
    description: str = ""
    payload_type: str = "void"
    payload_fields: Dict[str, str] = field(default_factory=dict)


@dataclass
class AccessibilityIssue:
    rule_id: str
    severity: str
    message: str
    element: str = ""
    line: int = 0
    column: int = 0
    wcag_level: AccessibilityLevel = AccessibilityLevel.AA
    fix_suggestion: str = ""
    impact: str = ""


@dataclass
class FigmaFile:
    file_id: str
    name: str
    last_modified: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    components: List[Dict[str, Any]] = field(default_factory=list)
    styles: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class DesignSystemExport:
    name: str
    version: str
    tokens: List[DesignToken] = field(default_factory=list)
    colors: List[ColorValue] = field(default_factory=list)
    typography: List[TypographyValue] = field(default_factory=list)
    spacing: List[SpacingValue] = field(default_factory=list)
    shadows: List[ShadowValue] = field(default_factory=list)
    borders: List[BorderValue] = field(default_factory=list)
    components: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "tokens": [
                {"name": t.name, "type": t.token_type.value,
                 "value": t.value, "description": t.description}
                for t in self.tokens
            ],
            "colors": [
                {"name": c.name, "hex": c.hex_value, "role": c.role}
                for c in self.colors
            ],
            "typography": [
                {"name": t.name, "font_family": t.font_family,
                 "font_size": t.font_size, "font_weight": t.font_weight}
                for t in self.typography
            ],
            "metadata": self.metadata,
        }


# =============================================================================
# Abstract Base Classes
# =============================================================================

class DesignOutput(ABC):
    @abstractmethod
    def generate(self, design_system: "DesignSystemManager") -> str: ...

    @abstractmethod
    def get_format(self) -> OutputFormat: ...


class Validator(ABC):
    @abstractmethod
    def validate(self, data: Any) -> List[AccessibilityIssue]: ...

    @abstractmethod
    def get_rules(self) -> Dict[str, str]: ...


# =============================================================================
# Core Design System Manager
# =============================================================================

class DesignSystemManager:
    """Central manager for the entire design system."""

    def __init__(
        self, name: str = "Default Design System", version: str = "1.0.0",
        base_spacing: int = 4, base_font_size: int = 16,
    ):
        self.name = name
        self.version = version
        self.base_spacing = base_spacing
        self.base_font_size = base_font_size
        self._colors: Dict[str, ColorValue] = {}
        self._typography: Dict[str, TypographyValue] = {}
        self._spacing: Dict[str, SpacingValue] = {}
        self._shadows: Dict[str, ShadowValue] = {}
        self._borders: Dict[str, BorderValue] = {}
        self._tokens: Dict[str, DesignToken] = {}
        self._breakpoints: Dict[str, int] = {}
        self._z_indices: Dict[str, int] = {}
        self._listeners: List[Callable] = []
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        logger.info(f"Initialized DesignSystemManager: {name} v{version}")

    # -- Color Management --

    def add_color(self, name: str, hex_value: str, role: str = "primary",
                  opacity: float = 1.0) -> ColorValue:
        if not re.match(r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$", hex_value):
            raise ValueError(f"Invalid hex color: {hex_value}")
        color = ColorValue(name=name, hex_value=hex_value, role=role, opacity=opacity)
        self._colors[name] = color
        self._touch()
        return color

    def get_color(self, name: str) -> Optional[ColorValue]:
        return self._colors.get(name)

    def remove_color(self, name: str) -> bool:
        if name in self._colors:
            del self._colors[name]
            self._touch()
            return True
        return False

    def get_all_colors(self) -> List[ColorValue]:
        return list(self._colors.values())

    def generate_palette(self, base_color: str, name: str = "primary",
                         steps: int = 10) -> Dict[str, ColorValue]:
        base = base_color.lstrip("#")
        r, g, b = int(base[0:2], 16), int(base[2:4], 16), int(base[4:6], 16)
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        palette: Dict[str, ColorValue] = {}
        shade_labels = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
        for i, label in enumerate(shade_labels[:steps]):
            lightness = max(0.05, min(0.95, 0.95 - i * 0.09))
            rgb = colorsys.hls_to_rgb(h, lightness, s)
            hex_val = "#{:02x}{:02x}{:02x}".format(
                int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            palette[f"{name}-{label}"] = self.add_color(f"{name}-{label}", hex_val, name)
        return palette

    # -- Typography Management --

    def add_typography(self, name: str, font_family: str, font_size: int,
                       font_weight: int = 400, line_height: float = 1.5) -> TypographyValue:
        typo = TypographyValue(name=name, font_family=font_family, font_size=font_size,
                               font_weight=font_weight, line_height=line_height)
        self._typography[name] = typo
        self._touch()
        return typo

    def get_typography(self, name: str) -> Optional[TypographyValue]:
        return self._typography.get(name)

    def generate_type_scale(self, base_size: int = 16, ratio: float = 1.25,
                            family: str = "Inter") -> Dict[str, TypographyValue]:
        names = ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl"]
        scale: Dict[str, TypographyValue] = {}
        for i, name in enumerate(names):
            size = round(base_size * (ratio ** (i - 2)))
            scale[name] = self.add_typography(name, family, size)
        return scale

    # -- Spacing Management --

    def add_spacing(self, name: str, value: int, unit: str = "px") -> SpacingValue:
        spacing = SpacingValue(name=name, value=value, unit=unit)
        self._spacing[name] = spacing
        self._touch()
        return spacing

    def generate_spacing_scale(self) -> Dict[str, SpacingValue]:
        multipliers = {
            "0": 0, "0.5": 0.5, "1": 1, "1.5": 1.5, "2": 2, "3": 3,
            "4": 4, "5": 5, "6": 6, "8": 8, "10": 10, "12": 12,
            "16": 16, "20": 20, "24": 24,
        }
        scale = {}
        for key, mult in multipliers.items():
            name = f"spacing-{key}"
            scale[name] = self.add_spacing(name, int(self.base_spacing * mult))
        return scale

    # -- Shadow Management --

    def add_shadow(self, name: str, x: int = 0, y: int = 2, blur: int = 4,
                   spread: int = 0, color: str = "rgba(0, 0, 0, 0.1)") -> ShadowValue:
        shadow = ShadowValue(name=name, x_offset=x, y_offset=y,
                             blur_radius=blur, spread_radius=spread, color=color)
        self._shadows[name] = shadow
        self._touch()
        return shadow

    # -- Border Management --

    def add_border(self, name: str, width: int = 1, style: str = "solid",
                   color: str = "#E5E7EB", radius: int = 0) -> BorderValue:
        border = BorderValue(name=name, width=width, style=style,
                             color=color, radius=radius)
        self._borders[name] = border
        self._touch()
        return border

    # -- Breakpoint Management --

    def set_breakpoints(self, sm: int = 640, md: int = 768, lg: int = 1024,
                        xl: int = 1280, xxl: int = 1536) -> Dict[str, int]:
        self._breakpoints = {"sm": sm, "md": md, "lg": lg, "xl": xl, "2xl": xxl}
        self._touch()
        return self._breakpoints

    # -- Z-Index Management --

    def set_z_indices(self, layers: Optional[Dict[str, int]] = None) -> Dict[str, int]:
        if layers is None:
            layers = {
                "base": 0, "dropdown": 1000, "sticky": 1100, "overlay": 1300,
                "modal": 1400, "popover": 1500, "toast": 1700, "tooltip": 1800,
            }
        self._z_indices = layers
        self._touch()
        return self._z_indices

    # -- Token Management --

    def add_token(self, name: str, token_type: TokenType, value: Any,
                  description: str = "") -> DesignToken:
        token = DesignToken(name=name, token_type=token_type,
                            value=value, description=description)
        self._tokens[name] = token
        self._touch()
        return token

    # -- Export --

    def export_css_variables(self) -> str:
        lines = [":root {"]
        for color in self._colors.values():
            lines.append(f"  --color-{color.name}: {color.hex_value};")
        for typo in self._typography.values():
            lines.append(f"  --font-{typo.name}-family: '{typo.font_family}', sans-serif;")
            lines.append(f"  --font-{typo.name}-size: {typo.font_size}px;")
            lines.append(f"  --font-{typo.name}-weight: {typo.font_weight};")
        for spacing in self._spacing.values():
            lines.append(f"  --{spacing.name}: {spacing.to_css()};")
        for shadow in self._shadows.values():
            lines.append(f"  --shadow-{shadow.name}: {shadow.to_css()};")
        for name, bp in self._breakpoints.items():
            lines.append(f"  --breakpoint-{name}: {bp}px;")
        for name, z in self._z_indices.items():
            lines.append(f"  --z-{name}: {z};")
        lines.append("}")
        return "\n".join(lines)

    def export_json(self) -> str:
        data = {
            "name": self.name,
            "version": self.version,
            "colors": {
                n: {"hex": c.hex_value, "role": c.role, "rgb": c.to_rgb()}
                for n, c in self._colors.items()
            },
            "typography": {
                n: {"font_family": t.font_family, "font_size": t.font_size,
                    "font_weight": t.font_weight}
                for n, t in self._typography.items()
            },
            "spacing": {n: s.value for n, s in self._spacing.items()},
            "shadows": {n: s.to_css() for n, s in self._shadows.items()},
            "breakpoints": self._breakpoints,
            "z_indices": self._z_indices,
        }
        return json.dumps(data, indent=2)

    def export_design_tokens(self) -> DesignSystemExport:
        return DesignSystemExport(
            name=self.name, version=self.version,
            tokens=list(self._tokens.values()),
            colors=list(self._colors.values()),
            typography=list(self._typography.values()),
            spacing=list(self._spacing.values()),
            shadows=list(self._shadows.values()),
            borders=list(self._borders.values()),
            metadata={"breakpoints": self._breakpoints, "z_indices": self._z_indices,
                      "created_at": self._created_at.isoformat(),
                      "updated_at": self._updated_at.isoformat()},
        )

    def generate_theme(self) -> Dict[str, Any]:
        return {
            "colors": {n: {"value": c.hex_value, "role": c.role}
                       for n, c in self._colors.items()},
            "typography": {n: {"family": t.font_family, "size": t.font_size,
                               "weight": t.font_weight}
                           for n, t in self._typography.items()},
            "spacing": {n: s.value for n, s in self._spacing.items()},
            "shadows": {n: s.to_css() for n, s in self._shadows.items()},
        }

    def subscribe(self, callback: Callable) -> None:
        self._listeners.append(callback)

    def _touch(self) -> None:
        self._updated_at = datetime.now()
        for listener in self._listeners:
            try:
                listener(self)
            except Exception as e:
                logger.error(f"Listener error: {e}")

    def get_stats(self) -> Dict[str, int]:
        return {
            "colors": len(self._colors), "typography": len(self._typography),
            "spacing": len(self._spacing), "shadows": len(self._shadows),
            "borders": len(self._borders), "tokens": len(self._tokens),
            "breakpoints": len(self._breakpoints), "z_indices": len(self._z_indices),
        }


# =============================================================================
# Component Library
# =============================================================================

class ComponentLibrary:
    """Manages reusable UI components with variants, states, and props."""

    def __init__(self, design_system: DesignSystemManager):
        self._ds = design_system
        self._components: Dict[str, Dict[str, Any]] = {}
        logger.info("ComponentLibrary initialized")

    def register_component(
        self, name: str, props: Optional[List[ComponentProp]] = None,
        events: Optional[List[ComponentEvent]] = None,
        variants: Optional[List[ComponentVariant]] = None,
        sizes: Optional[List[ComponentSize]] = None,
    ) -> Dict[str, Any]:
        component = {
            "name": name,
            "props": props or [],
            "events": events or [],
            "variants": [v.value for v in (variants or [ComponentVariant.PRIMARY])],
            "sizes": [s.value for s in (sizes or [ComponentSize.MD])],
            "created_at": datetime.now().isoformat(),
            "id": str(uuid.uuid4())[:8],
        }
        self._components[name] = component
        logger.info(f"Registered component: {name}")
        return component

    def get_component(self, name: str) -> Optional[Dict[str, Any]]:
        return self._components.get(name)

    def list_components(self) -> List[str]:
        return list(self._components.keys())

    def generate_button_css(
        self, variants: Optional[List[ComponentVariant]] = None,
        sizes: Optional[List[ComponentSize]] = None,
    ) -> str:
        if variants is None:
            variants = list(ComponentVariant)
        if sizes is None:
            sizes = list(ComponentSize)

        size_map = {
            ComponentSize.XS: ("28px", "0 8px", "12px"),
            ComponentSize.SM: ("32px", "0 12px", "14px"),
            ComponentSize.MD: ("40px", "0 16px", "16px"),
            ComponentSize.LG: ("48px", "0 20px", "18px"),
            ComponentSize.XL: ("56px", "0 24px", "20px"),
        }
        variant_css = {
            ComponentVariant.PRIMARY: "background: var(--color-primary, #3B82F6); color: white;",
            ComponentVariant.SECONDARY: "background: var(--color-secondary, #6B7280); color: white;",
            ComponentVariant.OUTLINE: "background: transparent; color: var(--color-primary); border: 2px solid var(--color-primary);",
            ComponentVariant.GHOST: "background: transparent; color: var(--color-text);",
            ComponentVariant.LINK: "background: transparent; color: var(--color-primary); text-decoration: underline;",
            ComponentVariant.DESTRUCTIVE: "background: var(--color-error, #EF4444); color: white;",
            ComponentVariant.SUCCESS: "background: var(--color-success, #10B981); color: white;",
            ComponentVariant.WARNING: "background: var(--color-warning, #F59E0B); color: white;",
        }

        css = [
            ".btn { display: inline-flex; align-items: center; justify-content: center;",
            "  font-weight: 500; border-radius: var(--radius-md, 8px); cursor: pointer;",
            "  transition: all 0.2s ease; outline: none; user-select: none; }",
            ".btn:focus-visible { box-shadow: 0 0 0 3px var(--color-focus, rgba(59,130,246,0.5)); }",
            ".btn:disabled { opacity: 0.5; cursor: not-allowed; pointer-events: none; }",
        ]

        for size in sizes:
            height, padding, font_size = size_map[size]
            css.append(f".btn-{size.value} {{ height: {height}; padding: {padding}; font-size: {font_size}; }}")

        for variant in variants:
            css.append(f".btn-{variant.value} {{ {variant_css.get(variant, '')} }}")

        return "\n".join(css)

    def generate_card_css(self) -> str:
        return (
            ".card { background: var(--color-surface, white); border-radius: var(--radius-lg, 12px);"
            " box-shadow: var(--shadow-sm); overflow: hidden; transition: box-shadow 0.2s; }\n"
            ".card:hover { box-shadow: var(--shadow-md); }\n"
            ".card__header { padding: var(--spacing-4); border-bottom: 1px solid var(--color-border); }\n"
            ".card__body { padding: var(--spacing-4); }\n"
            ".card__footer { padding: var(--spacing-4); border-top: 1px solid var(--color-border);"
            " display: flex; justify-content: flex-end; gap: var(--spacing-2); }"
        )

    def generate_input_css(self) -> str:
        return (
            ".input { width: 100%; padding: var(--spacing-sm) var(--spacing-md);"
            " border: 1px solid var(--color-border); border-radius: var(--radius-md);"
            " font-size: 1rem; color: var(--color-text); background: var(--color-surface);"
            " transition: border-color 0.2s, box-shadow 0.2s; }\n"
            ".input:focus { outline: none; border-color: var(--color-primary);"
            " box-shadow: 0 0 0 3px var(--color-focus); }\n"
            ".input:disabled { background: var(--color-disabled); cursor: not-allowed; }\n"
            ".input--error { border-color: var(--color-error); }\n"
            ".input-label { display: block; margin-bottom: var(--spacing-1); font-weight: 500; }"
        )

    def generate_component(self, name: str, platform: Platform = Platform.WEB) -> str:
        generators = {
            "button": self.generate_button_css,
            "card": self.generate_card_css,
            "input": self.generate_input_css,
        }
        generator = generators.get(name.lower())
        if generator:
            return generator()
        return f"/* No generator for {name} */"


# =============================================================================
# Accessibility Checker
# =============================================================================

class AccessibilityChecker:
    """WCAG 2.1 accessibility checker for colors, HTML, and components."""

    WCAG_AA_NORMAL = 4.5
    WCAG_AA_LARGE = 3.0
    WCAG_AAA_NORMAL = 7.0
    WCAG_AAA_LARGE = 4.5
    LARGE_TEXT_THRESHOLD = 18

    def __init__(self, level: AccessibilityLevel = AccessibilityLevel.AA):
        self.level = level
        self._issues: List[AccessibilityIssue] = []
        self._rules = self._load_rules()
        logger.info(f"AccessibilityChecker initialized at WCAG {level.value}")

    def _load_rules(self) -> Dict[str, str]:
        return {
            "color-contrast": "Text must meet minimum contrast ratio",
            "missing-alt": "Images must have alt text",
            "missing-label": "Form inputs must have associated labels",
            "missing-lang": "Document must have lang attribute",
            "heading-order": "Headings must be in sequential order",
            "link-name": "Links must have discernible text",
            "button-name": "Buttons must have discernible text",
            "aria-required": "Required fields must use aria-required",
            "focus-visible": "Interactive elements must have visible focus",
            "tab-order": "Tab order must be logical and sequential",
            "skip-nav": "Page must provide skip navigation",
            "landmark": "Page must use landmark regions",
            "table-header": "Tables must have header cells",
            "video-caption": "Videos must have captions",
            "color-only": "Information must not be conveyed by color alone",
        }

    def check_color_contrast(
        self, foreground: ColorValue, background: ColorValue,
        font_size: int = 16, is_bold: bool = False,
    ) -> AccessibilityIssue:
        ratio = foreground.contrast_ratio(background)
        is_large = font_size >= self.LARGE_TEXT_THRESHOLD or is_bold
        if is_large:
            min_ratio = self.WCAG_AA_LARGE if self.level == AccessibilityLevel.AA else self.WCAG_AAA_LARGE
        else:
            min_ratio = self.WCAG_AA_NORMAL if self.level == AccessibilityLevel.AA else self.WCAG_AAA_NORMAL

        if ratio < min_ratio:
            return AccessibilityIssue(
                rule_id="color-contrast", severity="error",
                message=f"Contrast ratio {ratio:.2f}:1 is below minimum {min_ratio}:1",
                wcag_level=self.level,
                fix_suggestion="Increase contrast by darkening text or lightening background",
                impact="Low-vision users may not be able to read the text",
            )
        return AccessibilityIssue(
            rule_id="color-contrast", severity="pass",
            message=f"Contrast ratio {ratio:.2f}:1 meets WCAG {self.level.value}",
            wcag_level=self.level,
        )

    def check_html(self, html: str) -> List[AccessibilityIssue]:
        issues: List[AccessibilityIssue] = []

        for match in re.finditer(r"<img[^>]*?>", html, re.IGNORECASE):
            tag = match.group()
            if "alt=" not in tag.lower():
                issues.append(AccessibilityIssue(
                    rule_id="missing-alt", severity="error",
                    message="Image is missing alt attribute", element=tag[:100],
                    fix_suggestion="Add descriptive alt text to the image",
                ))

        for match in re.finditer(r"<input[^>]*?>", html, re.IGNORECASE):
            tag = match.group()
            if "type=\"hidden\"" in tag.lower():
                continue
            if "aria-label" not in tag.lower() and "aria-labelledby" not in tag.lower():
                id_match = re.search(r'id=["\']([^"\']+)["\']', tag)
                if not id_match or f'for="{id_match.group(1)}"' not in html.lower():
                    issues.append(AccessibilityIssue(
                        rule_id="missing-label", severity="error",
                        message="Form input is missing an associated label",
                        element=tag[:100],
                        fix_suggestion="Add a <label> element or aria-label attribute",
                    ))

        if "<html" in html.lower() and "lang=" not in html.lower():
            issues.append(AccessibilityIssue(
                rule_id="missing-lang", severity="error",
                message="HTML element is missing lang attribute",
                fix_suggestion="Add lang attribute to <html> element",
            ))

        for match in re.finditer(r"<button[^>]*?>(.*?)</button>", html,
                                  re.IGNORECASE | re.DOTALL):
            content = match.group(1).strip()
            tag = match.group(0)
            if not content and "aria-label" not in tag.lower():
                issues.append(AccessibilityIssue(
                    rule_id="button-name", severity="error",
                    message="Button has no accessible name", element=tag[:100],
                    fix_suggestion="Add text content or aria-label to the button",
                ))

        self._issues.extend(issues)
        return issues

    def check_color_palette(self, colors: List[ColorValue]) -> List[AccessibilityIssue]:
        issues = []
        for i, fg in enumerate(colors):
            for j, bg in enumerate(colors):
                if i != j:
                    ratio = fg.contrast_ratio(bg)
                    if ratio < self.WCAG_AA_NORMAL and fg.is_light() != bg.is_light():
                        issues.append(AccessibilityIssue(
                            rule_id="color-contrast", severity="warning",
                            message=f"Low contrast between {fg.name} and {bg.name}: {ratio:.2f}:1",
                            fix_suggestion=f"Adjust {fg.name} or {bg.name} to achieve at least 4.5:1 ratio",
                        ))
        self._issues.extend(issues)
        return issues

    def generate_report(self) -> Dict[str, Any]:
        errors = sum(1 for i in self._issues if i.severity == "error")
        warnings = sum(1 for i in self._issues if i.severity == "warning")
        passes = sum(1 for i in self._issues if i.severity == "pass")
        return {
            "level": self.level.value, "total_issues": len(self._issues),
            "errors": errors, "warnings": warnings, "passes": passes,
            "issues": [
                {"rule": i.rule_id, "severity": i.severity,
                 "message": i.message, "fix": i.fix_suggestion}
                for i in self._issues
            ],
            "generated_at": datetime.now().isoformat(),
        }

    def reset(self) -> None:
        self._issues.clear()


# =============================================================================
# Design Token Manager
# =============================================================================

class DesignTokenManager:
    """W3C Design Token Format compatible token management."""

    def __init__(self, name: str = "design-tokens"):
        self.name = name
        self._tokens: Dict[str, DesignToken] = {}
        self._token_groups: Dict[str, List[str]] = {}
        self._aliases: Dict[str, str] = {}
        logger.info(f"DesignTokenManager initialized: {name}")

    def create_token(self, name: str, token_type: TokenType, value: Any,
                     description: str = "", group: str = "default") -> DesignToken:
        token = DesignToken(name=name, token_type=token_type,
                            value=value, description=description)
        self._tokens[name] = token
        self._token_groups.setdefault(group, []).append(name)
        return token

    def create_alias(self, alias_name: str, target_name: str) -> None:
        if target_name not in self._tokens:
            raise ValueError(f"Target token '{target_name}' does not exist")
        self._aliases[alias_name] = target_name

    def resolve_alias(self, name: str, depth: int = 10) -> Optional[DesignToken]:
        if depth <= 0:
            raise RecursionError(f"Alias resolution exceeded max depth for: {name}")
        target = self._aliases.get(name)
        if target:
            return self.resolve_alias(target, depth - 1)
        return self._tokens.get(name)

    def get_token(self, name: str) -> Optional[DesignToken]:
        token = self._tokens.get(name)
        if token is None and name in self._aliases:
            return self.resolve_alias(name)
        return token

    def get_group(self, group: str) -> List[DesignToken]:
        names = self._token_groups.get(group, [])
        return [self._tokens[n] for n in names if n in self._tokens]

    def export_w3c_format(self) -> Dict[str, Any]:
        output: Dict[str, Any] = {}
        for name, token in self._tokens.items():
            group = "default"
            for g, names in self._token_groups.items():
                if name in names:
                    group = g
                    break
            output.setdefault(group, {})[name] = {
                "$type": token.token_type.value,
                "$value": token.value,
                "$description": token.description,
            }
        return output

    def export_css(self) -> str:
        lines = []
        for group, names in self._token_groups.items():
            lines.append(f"/* {group} */")
            for name in names:
                token = self._tokens.get(name)
                if token:
                    lines.append(f"  --{name.replace('.', '-')}: {token.value};")
            lines.append("")
        return ":root {\n" + "\n".join(lines) + "}"

    def export_scss(self) -> str:
        lines = [f"${name.replace('.', '-')}: {token.value};"
                 for name, token in self._tokens.items()]
        return "\n".join(lines)

    def export_json(self) -> str:
        data = {name: {"type": token.token_type.value, "value": token.value,
                        "description": token.description}
                for name, token in self._tokens.items()}
        return json.dumps(data, indent=2)

    def export_swift(self) -> str:
        lines = ["import UIKit", "", "extension UIColor {"]
        for name, token in self._tokens.items():
            if token.token_type == TokenType.COLOR:
                swift_name = name.replace("-", "_").replace(".", "_")
                lines.append(f"    static let {swift_name} = UIColor(hex: \"{token.value}\")")
        lines.append("}")
        return "\n".join(lines)

    def export_kotlin(self) -> str:
        lines = ["package com.app.theme", "", "import androidx.compose.ui.graphics.Color", "",
                 "object AppColors {"]
        for name, token in self._tokens.items():
            if token.token_type == TokenType.COLOR:
                kotlin_name = name.replace("-", "_").replace(".", "_")
                hex_val = token.value.replace("#", "0xFF")
                lines.append(f"    val {kotlin_name} = Color({hex_val})")
        lines.append("}")
        return "\n".join(lines)

    def validate(self) -> List[str]:
        errors = []
        name_pattern = re.compile(r"^[a-z0-9][a-z0-9.\-]*$")
        for name in self._tokens:
            if not name_pattern.match(name):
                errors.append(f"Invalid token name: '{name}'")
        for alias, target in self._aliases.items():
            if target not in self._tokens:
                errors.append(f"Alias '{alias}' points to non-existent token '{target}'")
        return errors

    def merge(self, other: "DesignTokenManager") -> None:
        for name, token in other._tokens.items():
            self._tokens[name] = token
        for group, names in other._token_groups.items():
            self._token_groups.setdefault(group, []).extend(names)
        self._aliases.update(other._aliases)


# =============================================================================
# Color Palette Manager
# =============================================================================

class ColorPaletteManager:
    """Advanced color palette generation with harmony theory."""

    def __init__(self):
        self._palettes: Dict[str, Dict[str, ColorValue]] = {}
        self._harmony_cache: Dict[str, List[str]] = {}

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        h = hex_color.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
        return "#{:02x}{:02x}{:02x}".format(
            max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

    def _rotate_hue(self, h: float, degrees: float) -> float:
        return (h + degrees / 360) % 1.0

    def generate_harmony(self, base_hex: str,
                         harmony_type: str = "complementary") -> Dict[str, ColorValue]:
        r, g, b = self._hex_to_rgb(base_hex)
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

        offsets = {
            "complementary": [("base", 0), ("complement", 180)],
            "analogous": [("base", 0), ("analogous-1", -30), ("analogous-2", 30)],
            "triadic": [("base", 0), ("triadic-1", 120), ("triadic-2", 240)],
            "split-complementary": [("base", 0), ("split-1", 150), ("split-2", 210)],
            "tetradic": [("base", 0), ("t-1", 90), ("t-2", 180), ("t-3", 270)],
        }

        palette = {}
        for name, deg in offsets.get(harmony_type, [("base", 0)]):
            new_h = self._rotate_hue(h, deg)
            rgb = colorsys.hls_to_rgb(new_h, l, s)
            hex_val = self._rgb_to_hex(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            palette[name] = ColorValue(name=name, hex_value=hex_val, role="harmony")

        cache_key = f"{base_hex}_{harmony_type}"
        self._harmony_cache[cache_key] = [p.hex_value for p in palette.values()]
        self._palettes[cache_key] = palette
        return palette

    def generate_shade_scale(self, base_hex: str, name: str = "primary",
                             steps: int = 11) -> Dict[str, ColorValue]:
        r, g, b = self._hex_to_rgb(base_hex)
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        labels = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
        scale = {}
        for i, label in enumerate(labels[:steps]):
            t = i / (steps - 1)
            lightness = 0.97 - t * 0.92
            adjusted_s = max(0.1, min(1.0, s * (1.0 - 0.3 * abs(t - 0.5))))
            rgb = colorsys.hls_to_rgb(h, lightness, adjusted_s)
            hex_val = self._rgb_to_hex(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            scale[f"{name}-{label}"] = ColorValue(name=f"{name}-{label}",
                                                   hex_value=hex_val, role=name)
        self._palettes[f"{name}_scale"] = scale
        return scale

    def get_contrast_suggestions(self, fg_hex: str, bg_hex: str,
                                 target_ratio: float = 4.5) -> List[str]:
        fg_r, fg_g, fg_b = self._hex_to_rgb(fg_hex)
        bg_color = ColorValue(name="bg", hex_value=bg_hex)
        suggestions = []
        for delta in range(-50, 51, 5):
            h, l, s = colorsys.rgb_to_hls(fg_r / 255, fg_g / 255, fg_b / 255)
            new_l = max(0, min(1, l + delta / 100))
            rgb = colorsys.hls_to_rgb(h, new_l, s)
            hex_val = self._rgb_to_hex(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            test_color = ColorValue(name="test", hex_value=hex_val)
            if test_color.contrast_ratio(bg_color) >= target_ratio:
                suggestions.append(hex_val)
                if len(suggestions) >= 3:
                    break
        return suggestions

    def export_palette(self, palette_name: str) -> Dict[str, str]:
        palette = self._palettes.get(palette_name, {})
        return {name: color.hex_value for name, color in palette.items()}


# =============================================================================
# Typography Manager
# =============================================================================

class TypographyManager:
    """Manages typography with font stacks, type scales, and responsive CSS."""

    def __init__(self):
        self._font_families: Dict[str, List[str]] = {}
        self._type_styles: Dict[str, TypographyValue] = {}

    def register_font_family(self, name: str, fallbacks: Optional[List[str]] = None) -> None:
        self._font_families[name] = [name] + (fallbacks or ["sans-serif"])

    def add_type_style(self, name: str, font_family: str, font_size: int,
                       font_weight: int = 400, line_height: float = 1.5,
                       letter_spacing: float = 0.0) -> TypographyValue:
        style = TypographyValue(name=name, font_family=font_family, font_size=font_size,
                                font_weight=font_weight, line_height=line_height,
                                letter_spacing=letter_spacing)
        self._type_styles[name] = style
        return style

    def generate_major_third_scale(self, base_size: int = 16) -> Dict[str, TypographyValue]:
        ratio = 1.25
        names = [("2xs", -4), ("xs", -3), ("sm", -2), ("base", -1),
                 ("md", 0), ("lg", 1), ("xl", 2), ("2xl", 3), ("3xl", 4), ("4xl", 5)]
        scale = {}
        for name, step in names:
            size = round(base_size * (ratio ** step))
            scale[name] = self.add_type_style(name, "Inter", size)
        return scale

    def generate_golden_ratio_scale(self, base_size: int = 16) -> Dict[str, TypographyValue]:
        ratio = 1.618
        names = [("xs", -2), ("sm", -1), ("base", 0), ("lg", 1),
                 ("xl", 2), ("2xl", 3), ("3xl", 4)]
        scale = {}
        for name, step in names:
            size = round(base_size * (ratio ** step))
            scale[name] = self.add_type_style(name, "Georgia", size)
        return scale

    def generate_responsive_css(self) -> str:
        lines = [".typography-responsive {"]
        for name, style in self._type_styles.items():
            min_size = max(12, style.font_size - 4)
            max_size = style.font_size + 4
            preferred = round(style.font_size / 16, 4)
            lines.append(f"  --font-{name}: clamp({min_size}px, {preferred}vw + {min_size}px, {max_size}px);")
        lines.append("}")
        return "\n".join(lines)

    def generate_font_face_css(self) -> str:
        lines = []
        for family in self._font_families:
            lines.append(
                f"@font-face {{ font-family: '{family}';"
                f" src: url('/fonts/{family.lower()}-regular.woff2') format('woff2');"
                f" font-weight: 400; font-style: normal; font-display: swap; }}\n"
                f"@font-face {{ font-family: '{family}';"
                f" src: url('/fonts/{family.lower()}-bold.woff2') format('woff2');"
                f" font-weight: 700; font-style: normal; font-display: swap; }}")
        return "\n\n".join(lines)

    def get_font_stack(self, family: str) -> str:
        fallbacks = self._font_families.get(family, [family, "sans-serif"])
        return ", ".join(f"'{f}'" for f in fallbacks)

    def export_type_scale_json(self) -> str:
        data = {name: {"font_family": s.font_family, "font_size": s.font_size,
                        "font_weight": s.font_weight, "line_height": s.line_height}
                for name, s in self._type_styles.items()}
        return json.dumps(data, indent=2)


# =============================================================================
# Prototyping Engine
# =============================================================================

class PrototypingEngine:
    """Generates interactive HTML prototypes from design specifications."""

    def __init__(self, design_system: DesignSystemManager):
        self._ds = design_system
        self._prototypes: Dict[str, Dict[str, Any]] = {}

    def generate_wireframe(self, layout: str = "dashboard") -> str:
        wireframes = {
            "dashboard": self._dashboard_wireframe(),
            "login": self._login_wireframe(),
            "landing": self._landing_wireframe(),
            "settings": self._settings_wireframe(),
        }
        return wireframes.get(layout, self._dashboard_wireframe())

    def _dashboard_wireframe(self) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Wireframe</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, sans-serif; background: #F3F4F6; }
    .sidebar { position: fixed; left: 0; top: 0; bottom: 0; width: 240px;
               background: #1F2937; color: white; padding: 16px; }
    .sidebar__item { padding: 8px 12px; border-radius: 6px; margin-bottom: 4px; cursor: pointer; }
    .sidebar__item:hover { background: rgba(255,255,255,0.1); }
    .main { margin-left: 240px; padding: 24px; }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
    .card { background: white; border-radius: 8px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
    .stat { text-align: center; }
    .stat__value { font-size: 2rem; font-weight: 700; color: #111827; }
    .stat__label { font-size: 0.875rem; color: #6B7280; }
  </style>
</head>
<body>
  <aside class="sidebar">
    <h2 style="margin-bottom:24px">Brand</h2>
    <div class="sidebar__item">Dashboard</div>
    <div class="sidebar__item">Analytics</div>
    <div class="sidebar__item">Users</div>
    <div class="sidebar__item">Settings</div>
  </aside>
  <main class="main">
    <div class="header">
      <h1>Dashboard</h1>
      <div style="width:32px;height:32px;border-radius:50%;background:#D1D5DB"></div>
    </div>
    <div class="grid">
      <div class="card stat"><div class="stat__value">1,234</div><div class="stat__label">Users</div></div>
      <div class="card stat"><div class="stat__value">$5,678</div><div class="stat__label">Revenue</div></div>
      <div class="card stat"><div class="stat__value">89%</div><div class="stat__label">Retention</div></div>
      <div class="card stat"><div class="stat__value">42</div><div class="stat__label">Tickets</div></div>
    </div>
    <div class="card" style="margin-top:16px;height:300px">
      <p style="color:#9CA3AF">Chart placeholder</p>
    </div>
  </main>
</body>
</html>"""

    def _login_wireframe(self) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login Wireframe</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, sans-serif; display: flex; align-items: center;
           justify-content: center; min-height: 100vh; background: #F3F4F6; }
    .login-card { background: white; border-radius: 12px; padding: 40px; width: 100%;
                  max-width: 400px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .form-group { margin-bottom: 16px; }
    .form-label { display: block; margin-bottom: 4px; font-size: 0.875rem; font-weight: 500; }
    .form-input { width: 100%; padding: 10px 12px; border: 1px solid #D1D5DB;
                  border-radius: 6px; font-size: 1rem; }
    .btn { width: 100%; padding: 10px; background: #3B82F6; color: white; border: none;
           border-radius: 6px; font-size: 1rem; font-weight: 500; cursor: pointer; }
    .btn:hover { background: #2563EB; }
    .link { text-align: center; margin-top: 12px; font-size: 0.875rem; }
    .link a { color: #3B82F6; text-decoration: none; }
  </style>
</head>
<body>
  <div class="login-card">
    <h1 style="text-align:center;margin-bottom:24px">Sign In</h1>
    <div class="form-group">
      <label class="form-label">Email</label>
      <input class="form-input" type="email" placeholder="you@example.com">
    </div>
    <div class="form-group">
      <label class="form-label">Password</label>
      <input class="form-input" type="password" placeholder="Enter password">
    </div>
    <button class="btn">Sign In</button>
    <div class="link"><a href="#">Forgot password?</a></div>
  </div>
</body>
</html>"""

    def _landing_wireframe(self) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Landing Page Wireframe</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, sans-serif; }
    .nav { display: flex; justify-content: space-between; align-items: center; padding: 16px 48px; background: white; }
    .nav__links { display: flex; gap: 24px; }
    .hero { text-align: center; padding: 80px 48px; background: #EFF6FF; }
    .hero h1 { font-size: 3rem; margin-bottom: 16px; color: #111827; }
    .hero p { font-size: 1.25rem; color: #6B7280; max-width: 600px; margin: 0 auto 24px; }
    .btn-primary { display: inline-block; padding: 12px 32px; background: #3B82F6;
                   color: white; border-radius: 8px; text-decoration: none; font-weight: 500; }
    .features { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; padding: 64px 48px; max-width: 1200px; margin: 0 auto; }
    .feature { text-align: center; }
    .feature__icon { width: 48px; height: 48px; margin: 0 auto 16px; background: #DBEAFE; border-radius: 12px; }
    footer { text-align: center; padding: 32px; color: #9CA3AF; }
  </style>
</head>
<body>
  <nav class="nav">
    <strong>Brand</strong>
    <div class="nav__links"><a href="#">Features</a><a href="#">Pricing</a><a href="#">About</a></div>
  </nav>
  <section class="hero">
    <h1>Build Something Amazing</h1>
    <p>The platform that helps you ship faster and better.</p>
    <a href="#" class="btn-primary">Get Started</a>
  </section>
  <section class="features">
    <div class="feature"><div class="feature__icon"></div><h3>Fast</h3><p>Lightning-fast performance.</p></div>
    <div class="feature"><div class="feature__icon"></div><h3>Secure</h3><p>Enterprise-grade security.</p></div>
    <div class="feature"><div class="feature__icon"></div><h3>Simple</h3><p>Intuitive user experience.</p></div>
  </section>
  <footer>&copy; 2024 Brand. All rights reserved.</footer>
</body>
</html>"""

    def _settings_wireframe(self) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Settings Wireframe</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, sans-serif; background: #F9FAFB; }
    .settings { max-width: 720px; margin: 40px auto; padding: 0 24px; }
    .settings h1 { margin-bottom: 32px; }
    .section { background: white; border-radius: 8px; padding: 24px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .section h2 { font-size: 1.125rem; margin-bottom: 16px; }
    .field { margin-bottom: 16px; }
    .field label { display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 4px; }
    .field input, .field select { width: 100%; padding: 8px 12px; border: 1px solid #D1D5DB; border-radius: 6px; }
    .field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .toggle { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #F3F4F6; }
    .btn-save { padding: 10px 24px; background: #3B82F6; color: white; border: none; border-radius: 6px; cursor: pointer; }
  </style>
</head>
<body>
  <div class="settings">
    <h1>Settings</h1>
    <div class="section">
      <h2>Profile</h2>
      <div class="field-row">
        <div class="field"><label>First Name</label><input type="text"></div>
        <div class="field"><label>Last Name</label><input type="text"></div>
      </div>
      <div class="field"><label>Email</label><input type="email"></div>
    </div>
    <div class="section">
      <h2>Preferences</h2>
      <div class="toggle"><span>Email Notifications</span></div>
      <div class="toggle"><span>Dark Mode</span></div>
    </div>
    <button class="btn-save">Save Changes</button>
  </div>
</body>
</html>"""

    def register_prototype(self, name: str, html: str, description: str = "") -> None:
        self._prototypes[name] = {
            "html": html, "description": description,
            "created_at": datetime.now().isoformat(),
        }

    def list_prototypes(self) -> List[str]:
        return list(self._prototypes.keys())

    def get_prototype(self, name: str) -> Optional[str]:
        proto = self._prototypes.get(name)
        return proto["html"] if proto else None


# =============================================================================
# User Research Manager
# =============================================================================

class UserResearchManager:
    """Manages user research sessions, participants, insights, and journey maps."""

    def __init__(self):
        self._participants: Dict[str, Dict[str, Any]] = {}
        self._sessions: List[Dict[str, Any]] = []
        self._insights: List[Dict[str, Any]] = []
        self._journeys: Dict[str, List[Dict[str, Any]]] = {}

    def add_participant(self, participant_id: Optional[str] = None,
                        demographics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pid = participant_id or str(uuid.uuid4())[:8]
        participant = {
            "participant_id": pid,
            "demographics": demographics or {},
            "sessions": [],
            "consent_date": datetime.now().isoformat(),
        }
        self._participants[pid] = participant
        return participant

    def log_session(self, participant_id: str, method: ResearchMethod,
                    duration_minutes: int, notes: str = "",
                    tasks: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        if participant_id not in self._participants:
            raise ValueError(f"Participant {participant_id} not found")
        session = {
            "session_id": str(uuid.uuid4())[:8],
            "participant_id": participant_id,
            "method": method.value,
            "duration_minutes": duration_minutes,
            "notes": notes,
            "tasks": tasks or [],
            "completed_at": datetime.now().isoformat(),
        }
        self._sessions.append(session)
        self._participants[participant_id]["sessions"].append(session)
        return session

    def add_insight(self, title: str, description: str, category: str = "usability",
                    severity: str = "medium",
                    source_session_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        insight = {
            "insight_id": str(uuid.uuid4())[:8],
            "title": title, "description": description,
            "category": category, "severity": severity,
            "source_sessions": source_session_ids or [],
            "created_at": datetime.now().isoformat(),
        }
        self._insights.append(insight)
        return insight

    def create_journey_map(self, journey_name: str,
                           steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        self._journeys[journey_name] = steps
        return {"name": journey_name, "steps": steps,
                "created_at": datetime.now().isoformat()}

    def get_insights_by_category(self, category: str) -> List[Dict[str, Any]]:
        return [i for i in self._insights if i["category"] == category]

    def get_insights_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        return [i for i in self._insights if i["severity"] == severity]

    def generate_report(self) -> Dict[str, Any]:
        sessions_by_method: Dict[str, int] = {}
        for s in self._sessions:
            m = s.get("method", "unknown")
            sessions_by_method[m] = sessions_by_method.get(m, 0) + 1
        insights_by_severity: Dict[str, int] = {}
        for i in self._insights:
            sev = i.get("severity", "unknown")
            insights_by_severity[sev] = insights_by_severity.get(sev, 0) + 1
        return {
            "total_participants": len(self._participants),
            "total_sessions": len(self._sessions),
            "total_insights": len(self._insights),
            "sessions_by_method": sessions_by_method,
            "insights_by_severity": insights_by_severity,
            "generated_at": datetime.now().isoformat(),
        }

    def export_journey_map(self, journey_name: str) -> str:
        steps = self._journeys.get(journey_name, [])
        if not steps:
            return f"No journey map found: {journey_name}"
        lines = [f"Journey Map: {journey_name}", "=" * 40]
        for idx, step in enumerate(steps, 1):
            lines.append(f"\nStep {idx}: {step.get('title', 'Untitled')}")
            lines.append(f"  Action: {step.get('action', 'N/A')}")
            lines.append(f"  Emotion: {step.get('emotion', 'neutral')}")
            lines.append(f"  Pain Point: {step.get('pain_point', 'None')}")
        return "\n".join(lines)


# =============================================================================
# Figma Integration
# =============================================================================

class FigmaIntegration:
    """Integration layer for Figma API — color parsing, token extraction, code generation."""

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token
        self._files: Dict[str, FigmaFile] = {}
        self._sync_history: List[Dict[str, Any]] = []

    def parse_figma_color(self, figma_color: Dict[str, float]) -> str:
        r = int(figma_color.get("r", 0) * 255)
        g = int(figma_color.get("g", 0) * 255)
        b = int(figma_color.get("b", 0) * 255)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def parse_figma_node(self, node: Dict[str, Any]) -> Dict[str, Any]:
        parsed = {
            "id": node.get("id", ""),
            "name": node.get("name", ""),
            "type": node.get("type", ""),
            "visible": node.get("visible", True),
        }
        if node.get("type") == "TEXT":
            style = node.get("style", {})
            parsed.update({
                "text": node.get("characters", ""),
                "font_family": style.get("fontFamily", ""),
                "font_size": style.get("fontSize", 16),
                "font_weight": style.get("fontWeight", 400),
            })
        if "fills" in node:
            fills = node["fills"]
            if fills and isinstance(fills, list) and fills[0].get("type") == "SOLID":
                parsed["color"] = self.parse_figma_color(fills[0].get("color", {}))
        if "children" in node:
            parsed["children"] = [self.parse_figma_node(c) for c in node["children"]]
        return parsed

    def register_file(self, file_id: str, name: str,
                      pages: Optional[List[Dict[str, Any]]] = None,
                      components: Optional[List[Dict[str, Any]]] = None) -> FigmaFile:
        figma_file = FigmaFile(file_id=file_id, name=name,
                               last_modified=datetime.now().isoformat(),
                               pages=pages or [], components=components or [])
        self._files[file_id] = figma_file
        return figma_file

    def extract_design_tokens(self, figma_data: Dict[str, Any]) -> Dict[str, DesignToken]:
        tokens: Dict[str, DesignToken] = {}
        if "colors" in figma_data:
            for name, color_data in figma_data["colors"].items():
                tokens[name] = DesignToken(
                    name=name, token_type=TokenType.COLOR,
                    value=self.parse_figma_color(color_data),
                    description="Extracted from Figma")
        if "text_styles" in figma_data:
            for name, style in figma_data["text_styles"].items():
                tokens[name] = DesignToken(
                    name=name, token_type=TokenType.TYPOGRAPHY,
                    value={"font_family": style.get("fontFamily", ""),
                           "font_size": style.get("fontSize", 16),
                           "font_weight": style.get("fontWeight", 400)})
        return tokens

    def generate_component_code(self, figma_node: Dict[str, Any],
                                platform: Platform = Platform.WEB) -> str:
        parsed = self.parse_figma_node(figma_node)
        if platform == Platform.WEB:
            return self._generate_react(parsed)
        if platform == Platform.IOS:
            return self._generate_swiftui(parsed)
        if platform == Platform.ANDROID:
            return self._generate_compose(parsed)
        return f"<!-- Unsupported platform: {platform.value} -->"

    def _generate_react(self, parsed: Dict[str, Any]) -> str:
        name = parsed.get("name", "Component").replace(" ", "")
        children = parsed.get("children", [])
        props = ["  text?: string;"] if any(c.get("type") == "TEXT" for c in children) else []
        props_str = "\n".join(props)
        return f"""import React from 'react';

interface {name}Props {{
{props_str}
  className?: string;
  children?: React.ReactNode;
}}

export const {name}: React.FC<{name}Props> = ({{ className, children, ...props }}) => {{
  return (
    <div className={{className}} {{...props}}>
      {{children}}
    </div>
  );
}};

export default {name};"""

    def _generate_swiftui(self, parsed: Dict[str, Any]) -> str:
        name = parsed.get("name", "Component").replace(" ", "")
        return f"""import SwiftUI

struct {name}View: View {{
    var body: some View {{
        VStack(alignment: .leading, spacing: 16) {{
            Text("{name}").font(.headline)
        }}
        .padding()
    }}
}}

struct {name}View_Previews: PreviewProvider {{
    static var previews: some View {{ {name}View() }}
}}"""

    def _generate_compose(self, parsed: Dict[str, Any]) -> str:
        name = parsed.get("name", "Component").replace(" ", "")
        return f"""import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun {name}(modifier: Modifier = Modifier) {{
    Column(
        modifier = modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {{
        Text(text = "{name}", style = MaterialTheme.typography.headlineMedium)
    }}
}}"""

    def sync_styles(self, file_id: str, style_data: Dict[str, Any]) -> Dict[str, Any]:
        tokens = self.extract_design_tokens(style_data)
        record = {"file_id": file_id, "tokens_synced": len(tokens),
                  "synced_at": datetime.now().isoformat()}
        self._sync_history.append(record)
        return record

    def get_sync_history(self) -> List[Dict[str, Any]]:
        return self._sync_history
