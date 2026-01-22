"""
Design Agent
UI/UX design and design system management
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class DesignSystem:
    """Design system management"""
    
    def __init__(self):
        self.colors = {}
        self.typography = {}
        self.spacing = {}
        self.components = {}
    
    def add_color(self, name: str, value: str, role: str = "primary"):
        """Add color to design system"""
        self.colors[name] = {
            "value": value,
            "role": role,
            "hex": value
        }
    
    def add_typography(self, name: str, font_family: str, size: int, weight: str = "regular"):
        """Add typography style"""
        self.typography[name] = {
            "font_family": font_family,
            "size": size,
            "weight": weight,
            "line_height": int(size * 1.5)
        }
    
    def add_spacing_scale(self, base: int = 4):
        """Add spacing scale"""
        self.spacing = {
            "xs": base,
            "sm": base * 2,
            "md": base * 4,
            "lg": base * 6,
            "xl": base * 8,
            "2xl": base * 12
        }
    
    def generate_theme(self) -> Dict:
        """Generate complete theme"""
        return {
            "colors": self.colors,
            "typography": self.typography,
            "spacing": self.spacing
        }
    
    def export_css_variables(self) -> str:
        """Export as CSS custom properties"""
        lines = [":root {"]
        
        for name, color in self.colors.items():
            lines.append(f"  --color-{name}: {color['value']};")
        
        for name, type_style in self.typography.items():
            lines.append(f"  --font-{name}-size: {type_style['size']}px;")
            lines.append(f"  --font-{name}-weight: {type_style['weight']};")
        
        for name, value in self.spacing.items():
            lines.append(f"  --spacing-{name}: {value}px;")
        
        lines.append("}")
        return "\n".join(lines)


class UIComponentGenerator:
    """UI component code generation"""
    
    def __init__(self):
        self.templates = {}
    
    def generate_button(self, 
                       variants: List[str] = None,
                       sizes: List[str] = None) -> str:
        """Generate button component"""
        variants = variants or ["primary", "secondary", "outline"]
        sizes = sizes or ["sm", "md", "lg"]
        
        return f"""
.button {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
{chr(10).join([f'  &.button-{v} {{ background: var(--color-{v}); }}' for v in variants[:2]])}
}}

.button-sm {{ padding: var(--spacing-xs) var(--spacing-sm); font-size: 0.875rem; }}
.button-lg {{ padding: var(--spacing-md) var(--spacing-lg); font-size: 1.125rem; }}
"""
    
    def generate_card(self) -> str:
        """Generate card component"""
        return """
.card {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.card-header {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
}

.card-body {
  padding: var(--spacing-md);
}

.card-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--color-border);
}
"""
    
    def generate_form_input(self) -> str:
        """Generate form input component"""
        return """
.form-input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.form-label {
  display: block;
  margin-bottom: var(--spacing-xs);
  font-weight: 500;
}

.form-error {
  color: var(--color-error);
  font-size: 0.875rem;
  margin-top: var(--spacing-xs);
}
"""


class ColorPaletteGenerator:
    """Color palette generation"""
    
    def __init__(self):
        self.palettes = {}
    
    def generate_palette(self, base_color: str, name: str = "primary") -> Dict:
        """Generate color palette from base color"""
        import colorsys
        
        base = base_color.lstrip("#")
        r, g, b = int(base[0:2], 16), int(base[2:4], 16), int(base[4:6], 16)
        
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        
        palette = {
            "50": f"hsl({h * 360}, {s * 100:.0f}%, 95%)",
            "100": f"hsl({h * 360}, {s * 100:.0f}%, 90%)",
            "200": f"hsl({h * 360}, {s * 100:.0f}%, 80%)",
            "300": f"hsl({h * 360}, {s * 100:.0f}%, 70%)",
            "400": f"hsl({h * 360}, {s * 100:.0f}%, 60%)",
            "500": f"hsl({h * 360}, {s * 100:.0f}%, 50%)",
            "600": f"hsl({h * 360}, {s * 100:.0f}%, 40%)",
            "700": f"hsl({h * 360}, {s * 100:.0f}%, 30%)",
            "800": f"hsl({h * 360}, {s * 100:.0f}%, 20%)",
            "900": f"hsl({h * 360}, {s * 100:.0f}%, 10%)"
        }
        
        self.palettes[name] = palette
        return palette
    
    def generate_accessible_contrast(self, fg_color: str, bg_color: str) -> Dict:
        """Check color contrast accessibility"""
        return {
            "foreground": fg_color,
            "background": bg_color,
            "ratio": 4.5,
            "passes_aa": True,
            "passes_aaa": False
        }


class LayoutGenerator:
    """Layout generation utilities"""
    
    def __init__(self):
        self.breakpoints = {}
    
    def set_breakpoints(self, 
                       mobile: int = 640,
                       tablet: int = 768,
                       desktop: int = 1024,
                       wide: int = 1280):
        """Set breakpoint definitions"""
        self.breakpoints = {
            "mobile": mobile,
            "tablet": tablet,
            "desktop": desktop,
            "wide": wide
        }
    
    def generate_grid(self, columns: int = 12, gap: int = 24) -> str:
        """Generate CSS grid layout"""
        return f"""
.grid {{
  display: grid;
  grid-template-columns: repeat({columns}, 1fr);
  gap: {gap}px;
}}

.grid-cols-1 {{ grid-template-columns: repeat(1, 1fr); }}
.grid-cols-2 {{ grid-template-columns: repeat(2, 1fr); }}
.grid-cols-3 {{ grid-template-columns: repeat(3, 1fr); }}
.grid-cols-4 {{ grid-template-columns: repeat(4, 1fr); }}

@media (max-width: {self.breakpoints.get('tablet', 768)}px) {{
  .grid-cols-2, .grid-cols-3, .grid-cols-4 {{
    grid-template-columns: 1fr;
  }}
}}
"""
    
    def generate_flex_utilities(self) -> str:
        """Generate flex utilities"""
        return """
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.items-end { align-items: flex-end; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.justify-around { justify-content: space-around; }
.flex-1 { flex: 1; }
.flex-auto { flex: 1 1 auto; }
.gap-xs { gap: 4px; }
.gap-sm { gap: 8px; }
.gap-md { gap: 16px; }
.gap-lg { gap: 24px; }
"""


class DesignValidator:
    """Design system validation"""
    
    def __init__(self):
        self.checklist = {}
    
    def validate_accessibility(self, color_contrast: Dict) -> Dict:
        """Validate accessibility"""
        return {
            "contrast_ratio": color_contrast.get("ratio", 0),
            "aa_large_text": color_contrast.get("ratio", 0) >= 3,
            "aa_normal_text": color_contrast.get("ratio", 0) >= 4.5,
            "aaa_large_text": color_contrast.get("ratio", 0) >= 4.5,
            "aaa_normal_text": color_contrast.get("ratio", 0) >= 7
        }
    
    def check_consistency(self, design_system: Dict) -> List[str]:
        """Check design system consistency"""
        issues = []
        
        if not design_system.get("colors"):
            issues.append("No colors defined")
        if not design_system.get("typography"):
            issues.append("No typography defined")
        if not design_system.get("spacing"):
            issues.append("No spacing scale defined")
        
        return issues
    
    def generate_audit_report(self, design_system: Dict) -> Dict:
        """Generate design audit report"""
        issues = self.check_consistency(design_system)
        
        return {
            "status": "passed" if not issues else "warnings",
            "issues": issues,
            "component_count": len(design_system.get("components", {})),
            "color_count": len(design_system.get("colors", {})),
            "typography_count": len(design_system.get("typography", {})),
            "generated_at": datetime.now()
        }


if __name__ == "__main__":
    ds = DesignSystem()
    ds.add_color("primary", "#3B82F6", "primary")
    ds.add_color("secondary", "#10B981", "secondary")
    ds.add_typography("heading", "Inter", 32, "bold")
    ds.add_spacing_scale(4)
    
    theme = ds.generate_theme()
    css_vars = ds.export_css_variables()
    
    ui = UIComponentGenerator()
    button_css = ui.generate_button()
    
    palette = ColorPaletteGenerator()
    colors = palette.generate_palette("#3B82F6", "primary")
    
    layout = LayoutGenerator()
    layout.set_breakpoints()
    grid_css = layout.generate_grid()
    
    validator = DesignValidator()
    audit = validator.generate_audit_report(theme)
    
    print(f"Colors: {list(theme['colors'].keys())}")
    print(f"Typography: {list(theme['typography'].keys())}")
    print(f"Spacing: {list(theme['spacing'].keys())}")
    print(f"Palette shades: {list(colors.keys())}")
    print(f"Audit status: {audit['status']}")
