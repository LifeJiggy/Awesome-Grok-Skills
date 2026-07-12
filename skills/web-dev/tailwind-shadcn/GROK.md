---
name: "tailwind-shadcn"
category: "web-dev"
version: "1.0.0"
tags: ["web-dev", "tailwind", "shadcn", "css", "ui-components"]
---

# Tailwind CSS & shadcn/ui Component System

## Overview

Tailwind CSS is a utility-first CSS framework that provides atomic classes for rapid UI development without leaving your HTML or JSX. Instead of writing custom CSS, you compose utility classes directly on elements: `flex items-center justify-between p-4 rounded-lg bg-white shadow-md hover:shadow-lg transition-shadow`. This approach eliminates naming debates, reduces CSS bundle size through tree-shaking (unused utilities are purged), and creates a consistent visual language enforced by design tokens.

shadcn/ui is not a traditional component library — it's a collection of re-usable, accessible components built on Radix UI primitives and styled with Tailwind CSS. Unlike packages you install via npm, shadcn/ui components are copied into your project as source code, giving you full ownership and customization control. Each component is built with `class-variance-authority` (CVA) for variant management, `clsx` and `tailwind-merge` for conditional class composition, and follows a consistent pattern of `className` props, `asChild` composition, and forwardRef patterns.

The design system approach combines Tailwind's utility layer with shadcn/ui's component conventions: CSS custom properties for theming (colors, radius, spacing), Tailwind's `@layer` directives for component styles, and a `components.json` configuration that defines the component directory, alias paths, and styling preferences. Dark mode is handled through CSS class toggling (`.dark` class on `<html>`), with each component providing dark variants. The result is a fully typed, accessible, and deeply customizable UI system where every component is source code you own — not a black box dependency.

The theming system uses CSS custom properties defined in `globals.css` under `:root` and `.dark` selectors, with Tailwind's `theme.extend.colors` mapping these variables to utility classes. This creates a two-layer design token system: CSS variables for runtime theme switching and Tailwind's config for build-time optimization. Components reference these tokens through standard Tailwind classes, ensuring consistency while allowing per-component customization.

## Core Capabilities

- **Utility-first CSS composition** — Atomic classes for layout, spacing, typography, colors, and effects without custom CSS
- **Copy-paste component ownership** — shadcn/ui components as source code, not package dependencies
- **Variant management with CVA** — Class Variance Authority for type-safe component variants (size, color, intent)
- **Design token theming** — CSS custom properties for colors, radius, and spacing with dark mode support
- **Responsive design system** — Mobile-first breakpoints with Tailwind's responsive prefixes
- **Dark mode implementation** — Class-based dark mode with automatic variant application
- **Component composition patterns** — Radix UI primitives, `asChild` prop, compound components
- **Accessible form components** — Built-in label, error, and description patterns with ARIA compliance

## Usage Examples

### Theme Configuration

```python
from tailwind_shadcn import ThemeConfig, DesignTokens, CSSVariable

# Configure the design system tokens
theme = ThemeConfig(
    css_variables={
        "light": {
            "background": CSSVariable(value="0 0% 100%", description="White background"),
            "foreground": CSSVariable(value="222.2 84% 4.9%", description="Near-black text"),
            "primary": CSSVariable(value="222.2 47.4% 11.2%", description="Primary brand color"),
            "primary-foreground": CSSVariable(value="210 40% 98%", description="Text on primary"),
            "muted": CSSVariable(value="210 40% 96.1%", description="Muted background"),
            "muted-foreground": CSSVariable(value="215.4 16.3% 46.9%", description="Muted text"),
            "border": CSSVariable(value="214.3 31.8% 91.4%", description="Default border"),
            "input": CSSVariable(value="214.3 31.8% 91.4%", description="Input border"),
            "ring": CSSVariable(value="222.2 84% 4.9%", description="Focus ring"),
            "radius": CSSVariable(value="0.5rem", description="Border radius"),
        },
        "dark": {
            "background": CSSVariable(value="222.2 84% 4.9%", description="Dark background"),
            "foreground": CSSVariable(value="210 40% 98%", description="Light text"),
            "primary": CSSVariable(value="210 40% 98%", description="Primary on dark"),
            "primary-foreground": CSSVariable(value="222.2 47.4% 11.2%", description="Text on primary dark"),
            "muted": CSSVariable(value="217.2 32.6% 17.5%", description="Muted dark background"),
            "muted-foreground": CSSVariable(value="215 20.2% 65.1%", description="Muted dark text"),
            "border": CSSVariable(value="217.2 32.6% 17.5%", description="Border dark"),
            "input": CSSVariable(value="217.2 32.6% 17.5%", description="Input dark"),
            "ring": CSSVariable(value="212.7 26.8% 83.9%", description="Focus ring dark"),
        },
    },
    tailwind_config={
        "theme.extend.colors": {
            "border": "hsl(var(--border))",
            "input": "hsl(var(--input))",
            "ring": "hsl(var(--ring))",
            "background": "hsl(var(--background))",
            "foreground": "hsl(var(--foreground))",
            "primary": {"DEFAULT": "hsl(var(--primary))", "foreground": "hsl(var(--primary-foreground))"},
            "secondary": {"DEFAULT": "hsl(var(--secondary))", "foreground": "hsl(var(--secondary-foreground))"},
            "muted": {"DEFAULT": "hsl(var(--muted))", "foreground": "hsl(var(--muted-foreground))"},
        },
        "theme.extend.borderRadius": {
            "lg": "var(--radius)",
            "md": "calc(var(--radius) - 2px)",
            "sm": "calc(var(--radius) - 4px)",
        },
    },
)

print(theme.generate_globals_css())
```

### Button Component with Variants

```python
from tailwind_shadcn import ComponentVariant, VariantConfig

# Define Button variants using CVA
button_variants = VariantConfig(
    base="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
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
```

### Card Component Composition

```python
from tailwind_shadcn import CompoundComponent

class Card(CompoundComponent):
    """Card container with header, content, and footer slots."""

    root_classes = "rounded-lg border bg-card text-card-foreground shadow-sm"

    class Header:
        classes = "flex flex-col space-y-1.5 p-6"

    class Title:
        classes = "text-2xl font-semibold leading-none tracking-tight"

    class Description:
        classes = "text-sm text-muted-foreground"

    class Content:
        classes = "p-6 pt-0"

    class Footer:
        classes = "flex items-center p-6 pt-0"
```

### Responsive Utility Builder

```python
from tailwind_shadcn import ResponsiveBuilder

# Build responsive utility classes
builder = ResponsiveBuilder()
builder.add("padding", {
    "base": "p-4",
    "sm": "sm:p-6",
    "md": "md:p-8",
    "lg": "lg:p-12",
})
builder.add("grid", {
    "base": "grid-cols-1",
    "sm": "sm:grid-cols-2",
    "md": "md:grid-cols-3",
    "lg": "lg:grid-cols-4",
})
print(builder.build())  # "p-4 sm:p-6 md:p-8 lg:p-12 grid grid-cols-1 sm:grid-cols-2 ..."
```

### Dark Mode Toggle

```python
from tailwind_shadcn import DarkModeManager

manager = DarkModeManager(strategy="class")

# Generate the theme toggle script
toggle_script = manager.generate_toggle_script()
# Generates: document.documentElement.classList.toggle('dark')

# Generate theme-aware component classes
badge_classes = manager.theme_classes(
    light="bg-gray-100 text-gray-900",
    dark="bg-gray-800 text-gray-100",
)
```

### Form Component with Validation

```python
from tailwind_shadcn import FormField, InputVariant, LabelConfig

# Form field with error state
form_field = FormField(
    label=LabelConfig(text="Email Address", required=True),
    input_variant=InputVariant.DEFAULT,
    error_message="Please enter a valid email address",
    description="We'll never share your email with anyone.",
)

# Generate the HTML with proper ARIA attributes
html = form_field.render(
    input_props={"type": "email", "placeholder": "you@example.com"},
    error=True,
)
```

### Utility Class Compositor

```python
from tailwind_shadcn import ClassComposer

composer = ClassComposer()

# Compose classes with conditional logic
classes = composer.compose(
    "flex items-center gap-2",              # Always included
    {"bg-red-500": has_error, "bg-green-500": has_success},  # Conditional
    f"text-{size}-sm" if small else f"text-{size}-md",       # Dynamic
    "dark:bg-gray-800",                     # Always included
)

# Merge with tailwind-merge (deduplicates conflicting classes)
merged = composer.merge("p-4 p-8")  # -> "p-8"
```

### Component Library Index Generator

```python
from tailwind_shadcn import ComponentIndex

index = ComponentIndex(components_dir="src/components/ui")

# Auto-discover components and generate exports
exports = index.generate_exports()
# Generates barrel export file with all components

# Generate component documentation
docs = index.generate_docs()
# Generates usage examples for each component
```

## Best Practices

1. **Use `cn()` for class composition** — Always use the `cn()` helper (which wraps `clsx` + `tailwind-merge`) for conditional classes. This prevents conflicts and deduplicates utilities: `cn("p-4", isActive && "bg-blue-500", className)`.

2. **Customize at the theme level, not the component level** — Use CSS custom properties in `globals.css` for theme-wide changes. Override component-specific styles with Tailwind's `@apply` or className props, not by modifying the component source.

3. **Follow the variant pattern** — Use `class-variance-authority` for component variants instead of conditional strings. This keeps variants type-safe, discoverable, and composable.

4. **Keep components focused** — Each shadcn/ui component does one thing well. Compose them in your pages rather than creating mega-components. A Card is a Card; your page composes Card.Header, Card.Content, and Card.Footer.

5. **Use semantic color tokens** — Reference `bg-primary`, `text-muted-foreground`, `border-border` instead of raw colors like `bg-blue-500`. Semantic tokens automatically adapt to dark mode and theme changes.

6. **Mobile-first responsive design** — Always start with base styles for mobile and add `sm:`, `md:`, `lg:` prefixes for larger screens. This ensures your layout works on all devices by default.

7. **Accessibility is built-in** — shadcn/ui components include ARIA attributes, keyboard navigation, and focus management. Don't strip these when customizing. Test with screen readers.

8. **Tree-shake aggressively** — Tailwind purges unused utilities. Only include classes you actually use. For dynamic classes, safelist them in `tailwind.config.js` or use complete class names in templates.

## Related Modules

- **nextjs-fullstack** — Integrating Tailwind and shadcn/ui in Next.js App Router
- **server-components** — Using shadcn/ui components in React Server Components
- **edge-runtime** — CSS-in-JS considerations at the edge
- **supabase-auth** — Auth form UI patterns with shadcn/ui components
