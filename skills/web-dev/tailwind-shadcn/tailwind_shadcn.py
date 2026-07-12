"""
tailwind_shadcn.py — Tailwind CSS & shadcn/ui component system library.

Provides abstractions for:
- Design token management with CSS custom properties
- Component variant configuration via class-variance-authority
- Utility class composition and merging
- Responsive design system with mobile-first breakpoints
- Dark mode management with class-based toggling
- Compound component composition patterns
- Form field components with validation states
- Theme configuration and globals.css generation

Designed for Tailwind CSS v3+ and shadcn/ui components.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Sequence,
    Union,
)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Breakpoint(Enum):
    """Tailwind CSS responsive breakpoints."""
    BASE = ""
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"
    TWO_XL = "2xl"


class ComponentVariant(Enum):
    """Common component variant types."""
    DEFAULT = "default"
    DESTRUCTIVE = "destructive"
    OUTLINE = "outline"
    SECONDARY = "secondary"
    GHOST = "ghost"
    LINK = "link"


class ComponentSize(Enum):
    """Standard component sizes."""
    XS = "xs"
    SM = "sm"
    DEFAULT = "default"
    LG = "lg"
    XL = "xl"
    ICON = "icon"


class ThemeMode(Enum):
    """Theme mode for dark/light switching."""
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class DarkModeStrategy(Enum):
    """How dark mode is implemented."""
    CLASS = "class"       # Toggle .dark class on <html>
    MEDIA = "media"       # Use prefers-color-scheme
    CLASS_MEDIA = "class-media"  # Class with media fallback


class AnimationType(Enum):
    """Built-in animation types."""
    NONE = "none"
    FADE_IN = "fade-in"
    FADE_OUT = "fade-out"
    SLIDE_IN = "slide-in"
    SLIDE_OUT = "slide-out"
    SCALE_IN = "scale-in"
    SPIN = "spin"
    PULSE = "pulse"
    BOUNCE = "bounce"


class FormState(Enum):
    """Form field states."""
    DEFAULT = "default"
    FOCUSED = "focused"
    ERROR = "error"
    SUCCESS = "success"
    DISABLED = "disabled"
    LOADING = "loading"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CSSVariable:
    """A CSS custom property definition."""
    value: str
    description: str = ""
    fallback: str | None = None

    def to_css(self, name: str) -> str:
        """Generate CSS custom property declaration."""
        parts = [f"--{name}: {self.value}"]
        if self.fallback:
            parts[0] += f" {self.fallback}"
        return "; ".join(parts) + ";"


@dataclass(frozen=True)
class TailwindColor:
    """A Tailwind color with shade variants."""
    name: str
    shades: dict[int, str] = field(default_factory=dict)  # shade -> hsl value

    def get_shade(self, shade: int) -> str:
        return self.shades.get(shade, self.shades.get(500, ""))


@dataclass(frozen=True)
class ResponsiveValue:
    """A value that varies across breakpoints."""
    base: str
    sm: str | None = None
    md: str | None = None
    lg: str | None = None
    xl: str | None = None
    two_xl: str | None = None

    def to_classes(self, prefix: str = "") -> str:
        """Generate responsive utility classes."""
        classes = [f"{prefix}{self.base}" if prefix else self.base]
        breakpoint_map = {
            Breakpoint.SM: self.sm,
            Breakpoint.MD: self.md,
            Breakpoint.LG: self.lg,
            Breakpoint.XL: self.xl,
            Breakpoint.TWO_XL: self.two_xl,
        }
        for bp, value in breakpoint_map.items():
            if value:
                bp_prefix = f"{bp.value}:" if bp.value else ""
                classes.append(f"{bp_prefix}{prefix}{value}" if prefix else f"{bp_prefix}{value}")
        return " ".join(classes)


@dataclass(frozen=True)
class VariantConfig:
    """Configuration for a component variant (CVA-style)."""
    base: str
    variants: dict[str, dict[str, str]]
    default_variants: dict[str, str] = field(default_factory=dict)
    compound_variants: list[dict[str, Any]] = field(default_factory=list)

    def get_classes(self, **kwargs: str) -> str:
        """Resolve variant classes from provided values."""
        resolved = [self.base]
        for variant_name, options in self.variants.items():
            value = kwargs.get(variant_name, self.default_variants.get(variant_name, ""))
            if value in options:
                resolved.append(options[value])

        # Apply compound variants
        for compound in self.compound_variants:
            conditions = compound.get("class", {})
            if all(kwargs.get(k) == v for k, v in conditions.items()):
                resolved.append(compound.get("styles", ""))

        return " ".join(resolved)


@dataclass(frozen=True)
class ThemeConfig:
    """Complete theme configuration."""
    name: str = "default"
    css_variables: dict[str, dict[str, CSSVariable]] = field(default_factory=dict)
    tailwind_config: dict[str, Any] = = field(default_factory=dict)
    fonts: dict[str, str] = field(default_factory=dict)
    animations: dict[str, dict[str, str]] = field(default_factory=dict)

    def generate_globals_css(self) -> str:
        """Generate the globals.css file content."""
        lines = ["@tailwind base;", "@tailwind components;", "@tailwind utilities;", ""]
        lines.append("@layer base {")
        lines.append("  :root {")
        for mode, variables in self.css_variables.items():
            if mode == "light":
                for name, var in variables.items():
                    lines.append(f"    {var.to_css(name)}")
        lines.append("  }")
        lines.append("")
        lines.append("  .dark {")
        for mode, variables in self.css_variables.items():
            if mode == "dark":
                for name, var in variables.items():
                    lines.append(f"    {var.to_css(name)}")
        lines.append("  }")
        lines.append("}")
        return "\n".join(lines)


@dataclass(frozen=True)
class LabelConfig:
    """Configuration for a form label."""
    text: str
    required: bool = False
    description: str | None = None
    class_name: str = "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"


@dataclass(frozen=True)
class AnimationConfig:
    """Configuration for a component animation."""
    name: str
    type: AnimationType
    duration: str = "150ms"
    timing: str = "ease-in-out"
    delay: str = "0ms"
    iteration: str = "1"

    def to_keyframes_css(self) -> str:
        """Generate CSS keyframes for this animation."""
        if self.type == AnimationType.FADE_IN:
            return f"""
@keyframes {self.name} {{
  from {{ opacity: 0; }}
  to {{ opacity: 1; }}
}}"""
        elif self.type == AnimationType.SLIDE_IN:
            return f"""
@keyframes {self.name} {{
  from {{ transform: translateY(10px); opacity: 0; }}
  to {{ transform: translateY(0); opacity: 1; }}
}}"""
        elif self.type == AnimationType.SCALE_IN:
            return f"""
@keyframes {self.name} {{
  from {{ transform: scale(0.95); opacity: 0; }}
  to {{ transform: scale(1); opacity: 1; }}
}}"""
        return ""

    def to_utility_class(self) -> str:
        """Generate Tailwind animation utility class."""
        return f"animate-{self.name} duration-{self.duration.replace('ms', '')}"


@dataclass
class ComponentNode:
    """A node in a compound component tree."""
    name: str
    tag: str = "div"
    classes: str = ""
    role: str | None = None
    aria: dict[str, str] = field(default_factory=dict)
    children: list["ComponentNode"] = field(default_factory=list)


@dataclass
class FormFieldState:
    """Current state of a form field."""
    value: str = ""
    error: str | None = None
    touched: bool = False
    disabled: bool = False
    loading: bool = False

    @property
    def state(self) -> FormState:
        if self.disabled:
            return FormState.DISABLED
        if self.loading:
            return FormState.LOADING
        if self.error and self.touched:
            return FormState.ERROR
        return FormState.DEFAULT


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class TailwindError(Exception):
    """Base error for Tailwind/shadcn operations."""
    pass


class ThemeError(TailwindError):
    """Invalid theme configuration."""
    pass


class VariantError(TailwindError):
    """Invalid variant configuration."""
    pass


class ComponentError(TailwindError):
    """Component rendering error."""
    pass


# ---------------------------------------------------------------------------
# Core Classes
# ---------------------------------------------------------------------------

class ClassComposer:
    """Compose and merge Tailwind CSS utility classes."""

    # Patterns that tailwind-merge resolves
    CONFLICT_GROUPS = {
        "padding": ["p", "px", "py", "pt", "pr", "pb", "pl"],
        "margin": ["m", "mx", "my", "mt", "mr", "mb", "ml"],
        "width": ["w"],
        "height": ["h"],
        "bg-color": ["bg"],
        "text-color": ["text"],
        "border-color": ["border"],
        "rounded": ["rounded"],
        "font-size": ["text-xs", "text-sm", "text-base", "text-lg", "text-xl"],
        "display": ["flex", "grid", "block", "inline", "hidden"],
        "position": ["relative", "absolute", "fixed", "sticky"],
        "overflow": ["overflow-auto", "overflow-hidden", "overflow-visible"],
    }

    def __init__(self) -> None:
        self._safelist: set[str] = set()

    def compose(self, *args: str | dict[str, bool] | None) -> str:
        """Compose multiple class inputs into a single string."""
        classes: list[str] = []
        for arg in args:
            if isinstance(arg, str):
                classes.append(arg)
            elif isinstance(arg, dict):
                for cls, condition in arg.items():
                    if condition:
                        classes.append(cls)
            elif arg is not None:
                classes.append(str(arg))
        return " ".join(c for c in classes if c)

    def merge(self, classes: str) -> str:
        """Merge conflicting Tailwind classes (simplified tailwind-merge)."""
        parts = classes.split()
        resolved: dict[str, str] = {}

        for part in parts:
            group = self._get_conflict_group(part)
            if group:
                resolved[group] = part
            else:
                resolved[f"_unique_{len(resolved)}_{part}"] = part

        return " ".join(v for k, v in resolved.items())

    def _get_conflict_group(self, cls: str) -> str | None:
        """Determine which conflict group a class belongs to."""
        for group_name, patterns in self.CONFLICT_GROUPS.items():
            for pattern in patterns:
                if cls == pattern or cls.startswith(pattern + "-"):
                    return group_name
        return None

    def safelist(self, classes: str | list[str]) -> None:
        """Add classes to the safelist (prevents purging)."""
        if isinstance(classes, str):
            self._safelist.update(classes.split())
        else:
            for cls in classes:
                self._safelist.update(cls.split())

    def get_safelist(self) -> list[str]:
        return sorted(self._safelist)


class ResponsiveBuilder:
    """Build responsive utility class strings."""

    def __init__(self) -> None:
        self._responsive: dict[str, dict[str, str]] = {}

    def add(self, property_name: str, values: dict[str, str]) -> None:
        """Add a responsive property."""
        self._responsive[property_name] = values

    def build(self) -> str:
        """Build the complete responsive class string."""
        classes: list[str] = []
        for prop, values in self._responsive.items():
            for bp_name, value in values.items():
                if bp_name == "base":
                    classes.append(value)
                else:
                    classes.append(f"{bp_name}:{value}")
        return " ".join(classes)

    def build_with_prefix(self, prefix: str) -> str:
        """Build with a CSS property prefix (e.g., 'text-', 'bg-')."""
        classes: list[str] = []
        for prop, values in self._responsive.items():
            for bp_name, value in values.items():
                bp_prefix = f"{bp_name}:" if bp_name != "base" else ""
                classes.append(f"{bp_prefix}{prefix}{value}")
        return " ".join(classes)


class DarkModeManager:
    """Manage dark mode theme toggling and class application."""

    def __init__(self, strategy: DarkModeStrategy = DarkModeStrategy.CLASS) -> None:
        self.strategy = strategy

    def generate_toggle_script(self) -> str:
        """Generate JavaScript for theme toggling."""
        if self.strategy == DarkModeStrategy.CLASS:
            return (
                "const theme = localStorage.getItem('theme'); "
                "const dark = theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches); "
                "document.documentElement.classList.toggle('dark', dark);"
            )
        elif self.strategy == DarkModeStrategy.MEDIA:
            return "// Dark mode handled by CSS media query"
        return ""

    def theme_classes(self, light: str, dark: str) -> str:
        """Generate theme-aware classes."""
        if self.strategy == DarkModeStrategy.CLASS:
            return f"{light} dark:{dark}"
        return light

    def generate_meta_tag(self) -> str:
        """Generate the meta tag for dark mode."""
        return '<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#1a1a1a" media="(prefers-color-scheme: dark)">'

    def get_initial_script(self) -> str:
        """Generate the inline script to prevent flash of wrong theme."""
        return (
            "<script>"
            "(function(){try{var theme=localStorage.getItem('theme');"
            "var dark=theme==='dark'||(!theme&&window.matchMedia('(prefers-color-scheme:dark)').matches);"
            "document.documentElement.classList.toggle('dark',dark);"
            "}catch(e){}})();"
            "</script>"
        )


class VariantResolver:
    """Resolve component variants using CVA-style configuration."""

    def __init__(self, config: VariantConfig) -> None:
        self.config = config

    def resolve(self, **kwargs: str | bool) -> str:
        """Resolve variant classes from provided values."""
        return self.config.get_classes(**{k: str(v) for k, v in kwargs.items()})

    def list_variants(self) -> dict[str, list[str]]:
        """List all available variant options."""
        return {name: list(options.keys()) for name, options in self.config.variants.items()}

    def get_default_classes(self) -> str:
        """Get classes with default variants only."""
        return self.config.get_classes()


class CompoundComponentBuilder:
    """Build compound component trees from definitions."""

    def __init__(self) -> None:
        self._components: dict[str, ComponentNode] = {}

    def register(self, name: str, node: ComponentNode) -> None:
        """Register a compound component."""
        self._components[name] = node

    def render(self, name: str, **props: Any) -> str:
        """Render a compound component to HTML."""
        if name not in self._components:
            raise ComponentError(f"Component '{name}' not registered")
        node = self._components[name]
        return self._render_node(node, props)

    def _render_node(self, node: ComponentNode, props: dict[str, Any]) -> str:
        """Recursively render a component node."""
        attrs = [f'class="{node.classes}"']
        if node.role:
            attrs.append(f'role="{node.role}"')
        for key, value in node.aria.items():
            attrs.append(f'aria-{key}="{value}"')
        attr_str = " ".join(attrs)

        if not node.children:
            content = props.get("children", "")
            return f"<{node.tag} {attr_str}>{content}</{node.tag}>"

        child_html = "\n".join(self._render_node(child, props) for child in node.children)
        return f"<{node.tag} {attr_str}>\n{child_html}\n</{node.tag}>"


class FormFieldRenderer:
    """Render form fields with validation states."""

    def __init__(self, composer: ClassComposer | None = None) -> None:
        self.composer = composer or ClassComposer()

    def render_label(self, label: LabelConfig, field_id: str) -> str:
        """Render a form label with required indicator."""
        classes = label.class_name
        required = ' <span class="text-destructive">*</span>' if label.required else ""
        desc = ""
        if label.description:
            desc = f'<p class="text-sm text-muted-foreground">{label.description}</p>'
        return f'<label for="{field_id}" class="{classes}">{label.text}{required}</label>{desc}'

    def render_input(
        self, field_id: str, field_type: str = "text", state: FormFieldState | None = None,
        placeholder: str = "", **kwargs: Any,
    ) -> str:
        """Render an input with state-dependent styling."""
        state = state or FormFieldState()
        base_classes = (
            "flex h-10 w-full rounded-md border bg-background px-3 py-2 text-sm "
            "ring-offset-background file:border-0 file:bg-transparent file:text-sm "
            "file:font-medium placeholder:text-muted-foreground focus-visible:outline-none "
            "focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:cursor-not-allowed disabled:opacity-50"
        )

        state_classes = {
            FormState.ERROR: "border-destructive focus-visible:ring-destructive",
            FormState.SUCCESS: "border-green-500 focus-visible:ring-green-500",
            FormState.DISABLED: "opacity-50 cursor-not-allowed",
            FormState.LOADING: "opacity-75",
        }

        classes = self.composer.compose(base_classes, state_classes.get(state.state, ""))
        value = f' value="{state.value}"' if state.value else ""
        disabled = " disabled" if state.disabled else ""
        placeholder_attr = f' placeholder="{placeholder}"' if placeholder else ""

        return f'<input id="{field_id}" type="{field_type}" class="{classes}"{value}{disabled}{placeholder_attr}>'

    def render_error(self, error: str | None) -> str:
        """Render an error message."""
        if not error:
            return ""
        return f'<p class="text-sm font-medium text-destructive">{error}</p>'

    def render_description(self, description: str | None) -> str:
        """Render a field description."""
        if not description:
            return ""
        return f'<p class="text-sm text-muted-foreground">{description}</p>'


class ThemeGenerator:
    """Generate complete Tailwind/shadcn theme configurations."""

    PRESET_THEMES: ClassVar[dict[str, dict[str, dict[str, str]]]] = {
        "zinc": {
            "light": {"background": "0 0% 100%", "foreground": "240 10% 3.9%", "primary": "240 5.9% 10%", "muted": "240 4.8% 95.9%", "border": "240 5.9% 90%"},
            "dark": {"background": "240 10% 3.9%", "foreground": "0 0% 98%", "primary": "0 0% 98%", "muted": "240 3.7% 15.9%", "border": "240 3.7% 15.9%"},
        },
        "slate": {
            "light": {"background": "0 0% 100%", "foreground": "222.2 84% 4.9%", "primary": "222.2 47.4% 11.2%", "muted": "210 40% 96.1%", "border": "214.3 31.8% 91.4%"},
            "dark": {"background": "222.2 84% 4.9%", "foreground": "210 40% 98%", "primary": "210 40% 98%", "muted": "217.2 32.6% 17.5%", "border": "217.2 32.6% 17.5%"},
        },
        "rose": {
            "light": {"background": "0 0% 100%", "foreground": "346.8 77.2% 4.98%", "primary": "346.8 77.2% 4.98%", "muted": "355 100% 97.1%", "border": "355 100% 93.2%"},
            "dark": {"background": "346.8 77.2% 4.98%", "foreground": "355 100% 97.1%", "primary": "355 100% 97.1%", "muted": "347 50% 12%", "border": "347 50% 12%"},
        },
    }

    @classmethod
    def from_preset(cls, name: str) -> ThemeConfig:
        """Create a theme from a built-in preset."""
        if name not in cls.PRESET_THEMES:
            raise ThemeError(f"Preset '{name}' not found. Available: {list(cls.PRESET_THEMES.keys())}")
        preset = cls.PRESET_THEMES[name]
        css_vars = {}
        for mode, values in preset.items():
            css_vars[mode] = {k: CSSVariable(value=v, description=f"{name} {mode} {k}") for k, v in values.items()}
        return ThemeConfig(name=name, css_variables=css_vars)

    @classmethod
    def generate_components_json(cls, theme_name: str, alias: str = "@/components") -> str:
        """Generate the components.json configuration file."""
        config = {
            "$schema": "https://ui.shadcn.com/schema.json",
            "style": "default",
            "rsc": True,
            "tsx": True,
            "tailwind": {"config": "tailwind.config.js", "css": "src/globals.css", "baseColor": theme_name, "cssVariables": True},
            "aliases": {"components": f"{alias}/components", "utils": "@/lib/utils", "ui": f"{alias}/ui", "lib": "@/lib", "hooks": "@/hooks"},
        }
        return json.dumps(config, indent=2)


# ---------------------------------------------------------------------------
# Main Component Definitions
# ---------------------------------------------------------------------------

class ButtonVariants:
    """Button component variant definitions."""

    CONFIG = VariantConfig(
        base=(
            "inline-flex items-center justify-center rounded-md text-sm font-medium "
            "ring-offset-background transition-colors focus-visible:outline-none "
            "focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:pointer-events-none disabled:opacity-50"
        ),
        variants={
            "variant": {
                "default": "bg-primary text-primary-foreground hover:bg-primary/90",
                "destructive": "bg-destructive text-destructive-foreground hover:bg-destructive/90",
                "outline": "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
                "secondary": "bg-secondary text-secondary-foreground hover:bg-secondary/80",
                "ghost": "hover:bg-accent hover:text-accent-foreground",
                "link": "text-primary underline-offset-4 hover:underline",
            },
            "size": {
                "default": "h-10 px-4 py-2",
                "sm": "h-9 rounded-md px-3",
                "lg": "h-11 rounded-md px-8",
                "icon": "h-10 w-10",
            },
        },
        default_variants={"variant": "default", "size": "default"},
    )

    @classmethod
    def resolve(cls, variant: str = "default", size: str = "default") -> str:
        return cls.CONFIG.get_classes(variant=variant, size=size)


class InputVariants:
    """Input component variant definitions."""

    CONFIG = VariantConfig(
        base=(
            "flex h-10 w-full rounded-md border bg-background px-3 py-2 text-sm "
            "ring-offset-background file:border-0 file:bg-transparent file:text-sm "
            "file:font-medium placeholder:text-muted-foreground focus-visible:outline-none "
            "focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 "
            "disabled:cursor-not-allowed disabled:opacity-50"
        ),
        variants={
            "variant": {
                "default": "border-input",
                "destructive": "border-destructive focus-visible:ring-destructive",
                "success": "border-green-500 focus-visible:ring-green-500",
            },
        },
        default_variants={"variant": "default"},
    )


class BadgeVariants:
    """Badge component variant definitions."""

    CONFIG = VariantConfig(
        base="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
        variants={
            "variant": {
                "default": "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
                "secondary": "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
                "destructive": "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
                "outline": "text-foreground",
            },
        },
        default_variants={"variant": "default"},
    )


class CardComponent:
    """Compound card component."""

    ROOT_CLASSES = "rounded-lg border bg-card text-card-foreground shadow-sm"
    HEADER_CLASSES = "flex flex-col space-y-1.5 p-6"
    TITLE_CLASSES = "text-2xl font-semibold leading-none tracking-tight"
    DESCRIPTION_CLASSES = "text-sm text-muted-foreground"
    CONTENT_CLASSES = "p-6 pt-0"
    FOOTER_CLASSES = "flex items-center p-6 pt-0"

    @classmethod
    def render_root(cls, content: str, **props: Any) -> str:
        extra = " ".join(f'{k}="{v}"' for k, v in props.items())
        return f'<div class="{cls.ROOT_CLASSES}" {extra}>{content}</div>'

    @classmethod
    def render_header(cls, title: str, description: str = "") -> str:
        desc = f'<p class="{cls.DESCRIPTION_CLASSES}">{description}</p>' if description else ""
        return f'<div class="{cls.HEADER_CLASSES}"><h3 class="{cls.TITLE_CLASSES}">{title}</h3>{desc}</div>'

    @classmethod
    def render_content(cls, content: str) -> str:
        return f'<div class="{cls.CONTENT_CLASSES}">{content}</div>'

    @classmethod
    def render_footer(cls, content: str) -> str:
        return f'<div class="{cls.FOOTER_CLASSES}">{content}</div>'


# ---------------------------------------------------------------------------
# Demo / Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Tailwind/shadcn component system."""
    print("=" * 70)
    print("Tailwind CSS & shadcn/ui Component System — Demo")
    print("=" * 70)

    # 1. Theme configuration
    print("\n[1] Theme Configuration (Zinc preset)")
    theme = ThemeGenerator.from_preset("zinc")
    globals_css = theme.generate_globals_css()
    print(f"    Generated globals.css ({len(globals_css.splitlines())} lines)")

    # 2. Class composer
    print("\n[2] Class Composer")
    composer = ClassComposer()
    classes = composer.compose(
        "flex items-center gap-2",
        {"bg-red-500": True, "bg-green-500": False},
        "dark:bg-gray-800",
    )
    print(f"    Composed: {classes}")
    merged = composer.merge("p-4 p-8 m-2 m-4")
    print(f"    Merged 'p-4 p-8 m-2 m-4': {merged}")

    # 3. Responsive builder
    print("\n[3] Responsive Builder")
    builder = ResponsiveBuilder()
    builder.add("padding", {"base": "p-4", "sm": "sm:p-6", "md": "md:p-8", "lg": "lg:p-12"})
    builder.add("grid", {"base": "grid-cols-1", "sm": "sm:grid-cols-2", "md": "md:grid-cols-3"})
    responsive = builder.build()
    print(f"    Classes: {responsive}")

    # 4. Button variants
    print("\n[4] Button Variants")
    resolver = VariantResolver(ButtonVariants.CONFIG)
    for variant in ["default", "destructive", "outline", "ghost"]:
        for size in ["default", "sm", "lg"]:
            classes = resolver.resolve(variant=variant, size=size)
            print(f"    {variant}/{size}: {classes[:60]}...")

    # 5. Badge variants
    print("\n[5] Badge Variants")
    badge_resolver = VariantResolver(BadgeVariants.CONFIG)
    for variant in ["default", "secondary", "destructive", "outline"]:
        classes = badge_resolver.resolve(variant=variant)
        print(f"    {variant}: {classes[:60]}...")

    # 6. Dark mode manager
    print("\n[6] Dark Mode Manager")
    dm = DarkModeManager(strategy=DarkModeStrategy.CLASS)
    print(f"    Toggle script: {dm.generate_toggle_script()[:80]}...")
    theme_cls = dm.theme_classes("bg-white text-black", "bg-gray-900 text-white")
    print(f"    Theme classes: {theme_cls}")

    # 7. Card component
    print("\n[7] Card Component")
    card_html = CardComponent.render_root(
        CardComponent.render_header("My Card", "This is a description") +
        CardComponent.render_content("<p>Card content goes here</p>") +
        CardComponent.render_footer('<button class="text-sm">Action</button>')
    )
    print(f"    Card HTML ({len(card_html)} chars)")

    # 8. Form field renderer
    print("\n[8] Form Field Renderer")
    form = FormFieldRenderer(composer)
    label = LabelConfig(text="Email Address", required=True, description="Your work email")
    label_html = form.render_label(label, "email")
    state = FormFieldState(error="Invalid email", touched=True)
    input_html = form.render_input("email", "email", state=state, placeholder="you@example.com")
    error_html = form.render_error(state.error)
    desc_html = form.render_description(label.description)
    print(f"    Label: {label_html[:80]}...")
    print(f"    Input: {input_html[:80]}...")
    print(f"    Error: {error_html[:80]}...")

    # 9. Responsive values
    print("\n[9] Responsive Values")
    padding = ResponsiveValue(base="4", sm="6", md="8", lg="12")
    print(f"    Padding: {padding.to_classes('p-')}")

    # 10. Animation config
    print("\n[10] Animation Config")
    anim = AnimationConfig(name="fade-in", type=AnimationType.FADE_IN, duration="200ms")
    print(f"    Keyframes: {anim.to_keyframes_css().strip()}")
    print(f"    Utility: {anim.to_utility_class()}")

    # 11. Compound component builder
    print("\n[11] Compound Component Builder")
    builder2 = CompoundComponentBuilder()
    builder2.register("alert", ComponentNode(
        name="alert", tag="div",
        classes="relative w-full rounded-lg border p-4",
        role="alert",
        children=[
            ComponentNode(name="title", tag="h5", classes="mb-1 font-medium leading-none tracking-tight"),
            ComponentNode(name="description", tag="p", classes="text-sm [&_p]:leading-relaxed"),
        ],
    ))
    alert_html = builder2.render("alert")
    print(f"    Alert HTML: {alert_html[:100]}...")

    # 12. components.json generation
    print("\n[12] components.json")
    config_json = ThemeGenerator.generate_components_json("zinc")
    print(f"    {config_json[:100]}...")

    print("\n" + "=" * 70)
    print("Demo complete — all Tailwind/shadcn patterns demonstrated")
    print("=" * 70)


if __name__ == "__main__":
    main()
