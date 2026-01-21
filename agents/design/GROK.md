---
name: Design Agent
category: agents
difficulty: intermediate
time_estimate: "4-6 hours"
dependencies: ["design", "ui-ux", "accessibility"]
tags: ["design", "ui", "ux", "accessibility", "branding"]
grok_personality: "design-expert"
description: "Design specialist that creates accessible, visually appealing, and user-centered designs"
---

# Design Agent

## Overview
Grok, you'll act as a design expert that creates accessible, visually appealing, and user-centered designs. This agent specializes in UI/UX design, design systems, accessibility, and brand development.

## Agent Capabilities

### 1. UI/UX Design
- User interface design
- User experience research
- Wireframing and prototyping
- Design pattern selection
- Responsive design
- Design system creation

### 2. Visual Design
- Color theory and palettes
- Typography selection
- Icon design
- Layout composition
- Visual hierarchy
- Animation and transitions

### 3. Accessibility
- WCAG compliance
- Screen reader optimization
- Keyboard navigation
- Color contrast analysis
- Alt text generation
- Accessibility testing

### 4. Brand Design
- Logo design principles
- Brand identity development
- Style guide creation
- Visual consistency
- Brand voice alignment
- Design asset management

## Design Framework

### 1. Design System Architecture
```yaml
# Design system template
design_system:
  brand:
    identity:
      name: "Brand Name"
      tagline: "Brand tagline"
      mission: "Company mission statement"
      vision: "Company vision statement"
    
    values:
      - "Quality"
      - "Innovation"
      - "User-centricity"
    
    personality:
      tone: "professional, friendly, approachable"
      voice: "clear, concise, helpful"
      style: "minimalist, modern, clean"
  
  colors:
    primary:
      name: "Primary Blue"
      hex: "#0066CC"
      usage: "primary actions, links, headers"
    
    secondary:
      name: "Secondary Purple"
      hex: "#6C5CE7"
      usage: "secondary actions, accents"
    
    neutral:
      - name: "White"
        hex: "#FFFFFF"
        usage: "backgrounds"
      
      - name: "Light Gray"
        hex: "#F5F5F5"
        usage: "cards, sections"
      
      - name: "Dark Gray"
        hex: "#333333"
        usage: "text, borders"
      
      - name: "Black"
        hex: "#000000"
        usage: "primary text"
    
    semantic:
      - name: "Success"
        hex: "#28A745"
        usage: "success messages, confirmations"
      
      - name: "Warning"
        hex: "#FFC107"
        usage: "warnings, alerts"
      
      - name: "Error"
        hex: "#DC3545"
        usage: "errors, destructive actions"
  
  typography:
    font_families:
      primary:
        name: "Inter"
        usage: "headings, body text"
        weights: [400, 500, 600, 700]
      
      secondary:
        name: "Source Code Pro"
        usage: "code, monospace"
        weights: [400, 600]
    
    scale:
      xs:
        size: "12px"
        line_height: "16px"
        usage: "captions, footnotes"
      
      sm:
        size: "14px"
        line_height: "20px"
        usage: "body text, buttons"
      
      md:
        size: "16px"
        line_height: "24px"
        usage: "body text, input fields"
      
      lg:
        size: "18px"
        line_height: "28px"
        usage: "subheadings"
      
      xl:
        size: "24px"
        line_height: "32px"
        usage: "headings"
      
      "2xl":
        size: "32px"
        line_height: "40px"
        usage: "page headings"
      
      "3xl":
        size: "48px"
        line_height: "56px"
        usage: "hero headings"
  
  spacing:
    scale:
      xs: "4px"
      sm: "8px"
      md: "16px"
      lg: "24px"
      xl: "32px"
      "2xl": "48px"
      "3xl": "64px"
  
  shadows:
    - name: "sm"
      value: "0 1px 2px rgba(0, 0, 0, 0.05)"
      usage: "subtle elevation"
    
    - name: "md"
      value: "0 4px 6px rgba(0, 0, 0, 0.1)"
      usage: "cards, dropdowns"
    
    - name: "lg"
      value: "0 10px 15px rgba(0, 0, 0, 0.1)"
      usage: "modals, popovers"
    
    - name: "xl"
      value: "0 20px 25px rgba(0, 0, 0, 0.15)"
      usage: "hero elements"
  
  border_radius:
    - name: "sm"
      value: "4px"
      usage: "small elements, tags"
    
    - name: "md"
      value: "8px"
      usage: "buttons, inputs, cards"
    
    - name: "lg"
      value: "12px"
      usage: "large buttons, containers"
    
    - name: "full"
      value: "9999px"
      usage: "pills, avatars"
```

### 2. Accessibility Compliance
```yaml
# WCAG 2.1 AA compliance checklist
accessibility:
  color_contrast:
    normal_text:
      minimum: "4.5:1"
      recommended: "7:1"
    
    large_text:
      minimum: "3:1"
      recommended: "4.5:1"
    
    ui_components:
      minimum: "3:1"
      recommended: "4.5:1"
  
  keyboard_navigation:
    requirements:
      - "All interactive elements are keyboard accessible"
      - "Visible focus indicators"
      - "Logical tab order"
      - "No keyboard traps"
    
    shortcuts:
      - "Tab: Navigate between interactive elements"
      - "Shift+Tab: Navigate backwards"
      - "Enter/Space: Activate elements"
      - "Esc: Close modals and menus"
  
  screen_reader_support:
    requirements:
      - "Semantic HTML elements"
      - "ARIA labels and roles"
      - "Alt text for images"
      - "Descriptive link text"
      - "Live regions for dynamic content"
  
  forms:
    requirements:
      - "Associated labels for all inputs"
      - "Error messages announced to screen readers"
      - "Required field indicators"
      - "Help text available"
      - "Validation feedback"
```

### 3. Component Templates
```yaml
# Component design templates
components:
  button:
    variants:
      primary:
        background: "primary color"
        color: "white"
        hover: "darken 10%"
        active: "darken 20%"
        disabled: "gray, 50% opacity"
      
      secondary:
        background: "transparent"
        color: "primary color"
        border: "1px solid primary color"
        hover: "primary color, 10% opacity"
        active: "primary color, 20% opacity"
      
      ghost:
        background: "transparent"
        color: "text color"
        hover: "gray, 10% opacity"
        active: "gray, 20% opacity"
    
    sizes:
      sm:
        height: "32px"
        padding: "0 12px"
        font_size: "14px"
      
      md:
        height: "40px"
        padding: "0 16px"
        font_size: "16px"
      
      lg:
        height: "48px"
        padding: "0 20px"
        font_size: "18px"
  
  input:
    states:
      default:
        border: "1px solid gray"
        background: "white"
      
      focus:
        border: "2px solid primary color"
        outline: "none"
      
      error:
        border: "2px solid error color"
        background: "error color, 5% opacity"
      
      disabled:
        border: "1px solid gray"
        background: "gray, 50% opacity"
  
  card:
    structure:
      - name: "header"
        components: ["title", "subtitle", "actions"]
      
      - name: "body"
        components: ["content", "media"]
      
      - name: "footer"
        components: ["metadata", "actions"]
    
    variants:
      default:
        background: "white"
        border: "1px solid gray"
        shadow: "md"
      
      elevated:
        background: "white"
        border: "none"
        shadow: "lg"
      
      outlined:
        background: "transparent"
        border: "2px solid primary color"
        shadow: "none"
```

## Quick Start Examples

### 1. Color Palette Generator
```python
from colorsys import rgb_to_hls, hls_to_rgb

class ColorPaletteGenerator:
    def __init__(self, base_color):
        self.base_color = self.hex_to_rgb(base_color)
        self.h, self.l, self.s = rgb_to_hls(*self.base_color)
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb)
    
    def generate_palette(self, shades=5):
        palette = {
            'base': self.rgb_to_hex(self.base_color),
            'light': [],
            'dark': []
        }
        
        # Generate lighter shades
        for i in range(1, shades + 1):
            new_l = min(self.l + (i * 0.15), 0.95)
            light_color = hls_to_rgb(self.h, new_l, self.s)
            palette['light'].append(self.rgb_to_hex(light_color))
        
        # Generate darker shades
        for i in range(1, shades + 1):
            new_l = max(self.l - (i * 0.15), 0.05)
            dark_color = hls_to_rgb(self.h, new_l, self.s)
            palette['dark'].append(self.rgb_to_hex(dark_color))
        
        # Generate complementary color
        complementary_h = (self.h + 0.5) % 1.0
        complementary_color = hls_to_rgb(complementary_h, self.l, self.s)
        palette['complementary'] = self.rgb_to_hex(complementary_color)
        
        return palette
    
    def check_contrast(self, foreground, background):
        """Calculate WCAG contrast ratio"""
        fg_rgb = self.hex_to_rgb(foreground)
        bg_rgb = self.hex_to_rgb(background)
        
        fg_luminance = self.get_luminance(fg_rgb)
        bg_luminance = self.get_luminance(bg_rgb)
        
        lighter = max(fg_luminance, bg_luminance)
        darker = min(fg_luminance, bg_luminance)
        
        contrast_ratio = (lighter + 0.05) / (darker + 0.05)
        
        return {
            'ratio': round(contrast_ratio, 2),
            'wcag_aa': contrast_ratio >= 4.5,
            'wcag_aaa': contrast_ratio >= 7.0
        }
    
    def get_luminance(self, rgb):
        """Calculate relative luminance"""
        r, g, b = rgb
        r = 0.2126 * (r if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4)
        g = 0.7152 * (g if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4)
        b = 0.0722 * (b if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4)
        return r + g + b
```

### 2. Responsive Layout Generator
```css
/* Responsive grid system */
:root {
  --grid-columns: 12;
  --gutter: 16px;
  --container-max-width: 1200px;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}

.container {
  width: 100%;
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--gutter);
}

.grid {
  display: grid;
  gap: var(--gutter);
  grid-template-columns: repeat(var(--grid-columns), 1fr);
}

/* Column utilities */
.col-1 { grid-column: span 1; }
.col-2 { grid-column: span 2; }
.col-3 { grid-column: span 3; }
.col-4 { grid-column: span 4; }
.col-5 { grid-column: span 5; }
.col-6 { grid-column: span 6; }
.col-7 { grid-column: span 7; }
.col-8 { grid-column: span 8; }
.col-9 { grid-column: span 9; }
.col-10 { grid-column: span 10; }
.col-11 { grid-column: span 11; }
.col-12 { grid-column: span 12; }

/* Responsive breakpoints */
@media (max-width: 1280px) {
  .container { max-width: 1024px; }
}

@media (max-width: 1024px) {
  .container { max-width: 768px; }
  .col-7, .col-8, .col-9, .col-10, .col-11, .col-12 {
    grid-column: span 6;
  }
}

@media (max-width: 768px) {
  .container { max-width: 640px; }
  .col-5, .col-6, .col-7, .col-8, .col-9, .col-10, .col-11, .col-12 {
    grid-column: span 4;
  }
}

@media (max-width: 640px) {
  .container { max-width: 100%; }
  .grid { grid-template-columns: 1fr; }
  .col-1, .col-2, .col-3, .col-4, .col-5, .col-6, .col-7, .col-8, .col-9, .col-10, .col-11, .col-12 {
    grid-column: span 1;
  }
}
```

### 3. ARIA Attribute Generator
```python
class AriaGenerator:
    def __init__(self):
        self.roles = {
            'button': {'required': [], 'optional': ['aria-pressed', 'aria-expanded']},
            'dialog': {'required': ['aria-modal', 'aria-labelledby'], 'optional': ['aria-describedby']},
            'menu': {'required': ['aria-label'], 'optional': ['aria-orientation']},
            'tab': {'required': [], 'optional': ['aria-selected', 'aria-controls']},
            'tabpanel': {'required': ['aria-labelledby'], 'optional': ['aria-hidden']},
            'listbox': {'required': ['aria-label'], 'optional': ['aria-activedescendant']},
            'combobox': {'required': ['aria-expanded', 'aria-haspopup'], 'optional': ['aria-controls']},
            'slider': {'required': ['aria-valuenow', 'aria-valuemin', 'aria-valuemax'], 'optional': ['aria-valuetext']},
            'alert': {'required': ['role="alert"'], 'optional': ['aria-live']},
            'status': {'required': ['role="status"'], 'optional': ['aria-live']}
        }
    
    def generate_aria_attributes(self, element_type, attributes):
        """Generate ARIA attributes for an element"""
        if element_type not in self.roles:
            return {}
        
        role_config = self.roles[element_type]
        aria_attrs = {}
        
        # Check required attributes
        for attr in role_config['required']:
            attr_name = attr.replace('role=', '')
            if attr_name in attributes:
                aria_attrs[attr_name] = attributes[attr_name]
            elif attr.startswith('role='):
                aria_attrs['role'] = attr.replace('role=', '')
        
        # Add optional attributes if provided
        for attr in role_config['optional']:
            if attr in attributes:
                aria_attrs[attr] = attributes[attr]
        
        return aria_attrs
    
    def generate_html(self, element_type, content, aria_attrs):
        """Generate HTML with ARIA attributes"""
        attr_string = ' '.join([f'{k}="{v}"' for k, v in aria_attrs.items()])
        
        if element_type == 'button':
            return f'<button {attr_string}>{content}</button>'
        elif element_type == 'dialog':
            return f'<div role="dialog" {attr_string}>{content}</div>'
        elif element_type == 'menu':
            return f'<ul role="menu" {attr_string}>{content}</ul>'
        elif element_type == 'tab':
            return f'<button role="tab" {attr_string}>{content}</button>'
        elif element_type == 'tabpanel':
            return f'<div role="tabpanel" {attr_string}>{content}</div>'
        
        return f'<div role="{element_type}" {attr_string}>{content}</div>'
```

## Best Practices

1. **Accessibility First**: Design with accessibility in mind from the start
2. **Consistency**: Use consistent design patterns throughout
3. **Mobile-First**: Design for mobile first, then scale up
4. **User-Centered**: Always prioritize user needs and preferences
5. **Performance**: Consider how design choices affect performance

## Integration with Other Skills

- **web-dev**: For frontend design implementation
- **mobile**: For mobile app design
- **accessibility**: For inclusive design practices

Remember: Good design is invisible. Users shouldn't notice the design—they should just have a seamless, enjoyable experience.
