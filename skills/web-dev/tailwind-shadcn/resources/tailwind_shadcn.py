"""
Tailwind CSS Pipeline
Tailwind and shadcn/ui patterns
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ComponentConfig:
    name: str
    component_type: str
    variants: List[str] = None
    sizes: List[str] = None
    colors: Dict = None
    responsive: bool = True
    
    def __post_init__(self):
        if self.variants is None:
            self.variants = ["default", "destructive", "outline", "secondary", "ghost"]
        if self.sizes is None:
            self.sizes = ["sm", "md", "lg", "xl"]
        if self.colors is None:
            self.colors = {"primary": "blue", "secondary": "gray"}


class TailwindConfigGenerator:
    """Tailwind configuration generator"""
    
    @staticmethod
    def generate_config(theme_name: str = "my-app",
                       colors: Dict = None,
                       fonts: List[str] = None) -> str:
        """Generate tailwind.config.js"""
        theme_colors = colors or {
            "background": "hsl(var(--background))",
            "foreground": "hsl(var(--foreground))",
            "primary": {
                "DEFAULT": "hsl(var(--primary))",
                "foreground": "hsl(var(--primary-foreground))"
            },
            "secondary": {
                "DEFAULT": "hsl(var(--secondary))",
                "foreground": "hsl(var(--secondary-foreground))"
            },
            "muted": {
                "DEFAULT": "hsl(var(--muted))",
                "foreground": "hsl(var(--muted-foreground))"
            },
            "accent": {
                "DEFAULT": "hsl(var(--accent))",
                "foreground": "hsl(var(--accent-foreground))"
            },
            "destructive": {
                "DEFAULT": "hsl(var(--destructive))",
                "foreground": "hsl(var(--destructive-foreground))"
            },
            "card": {
                "DEFAULT": "hsl(var(--card))",
                "foreground": "hsl(var(--card-foreground))"
            },
            "border": "hsl(var(--border))",
            "input": "hsl(var(--input))",
            "ring": "hsl(var(--ring))"
        }
        
        theme_fonts = fonts or ["Inter", "system-ui", "sans-serif"]
        
        return f"""
/** @type {{import('tailwindcss').Config}} */
export default {{
  darkMode: ["class"],
  content: [
    "./pages/**/*.{{ts,tsx}}",
    "./components/**/*.{{ts,tsx}}",
    "./app/**/*.{{ts,tsx}}",
    "./src/**/*.{{ts,tsx}}",
  ],
  theme: {{
    container: {{
      center: true,
      padding: "2rem",
      screens: {{
        "2xl": "1400px",
      }},
    }},
    extend: {{
      colors: {theme_colors},
      fontFamily: {{
        sans: ["{theme_fonts[0]}", ...fontFamily.sans],
        mono: [fontFamily.mono],
      }},
      borderRadius: {{
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      }},
      keyframes: {{
        "accordion-down": {{
          from: {{ height: 0 }},
          to: {{ height: "var(--radix-accordion-content-height)" }},
        }},
        "accordion-up": {{
          from: {{ height: "var(--radix-accordion-content-height)" }},
          to: {{ height: 0 }},
        }},
        "fade-in": {{
          from: {{ opacity: 0 }},
          to: {{ opacity: 1 }},
        }},
        "slide-in-from-top": {{
          from: {{ transform: "translateY(-100%)" }},
          to: {{ transform: "translateY(0)" }},
        }},
      }},
      animation: {{
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-in": "fade-in 0.3s ease-out",
      }},
    }},
  }},
  plugins: [require("tailwindcss-animate"), require("@tailwindcss/typography")],
}};
"""
    
    @staticmethod
    def generate_globals_css(colors: Dict = None) -> str:
        """Generate globals.css with CSS variables"""
        return """
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
    font-feature-settings: "rlig" 1, "calt" 1;
  }
}
"""


class ShadcnComponentGenerator:
    """shadcn/ui component generator"""
    
    @staticmethod
    def generate_button(config: ComponentConfig) -> str:
        """Generate Button component"""
        variants = ", ".join([f'"{v}"' for v in config.variants])
        sizes = ", ".join([f'"{s}"' for s in config.sizes])
        
        return f"""
import * as React from "react"
import {{ cva, type VariantProps }} from "class-variance-authority"
import {{ cn }} from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {{
    variants: {{
      variant: {{
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      }},
      size: {{
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      }},
    }},
    defaultVariants: {{
      variant: "default",
      size: "default",
    }},
  }}
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {{
  asChild?: boolean
}}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({{ className, variant, size, asChild = false, ...props }}, ref) => {{
    return (
      <button
        className={{ cn(buttonVariants({{ variant, size, className }})) }}
        ref={{ref}}
        {{...props}}
      />
    )
  }}
)
Button.displayName = "Button"

export {{ Button, buttonVariants }}
"""
    
    @staticmethod
    def generate_input() -> str:
        """Generate Input component"""
        return """
import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
"""
    
    @staticmethod
    def generate_card() -> str:
        """Generate Card component"""
        return """
import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border bg-card text-card-foreground shadow-sm",
      className
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-2xl font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
"""
    
    @staticmethod
    def generate_utils() -> str:
        """Generate utility function"""
        return """
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatCurrency(amount: number, currency = "USD"): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(amount)
}

export function formatDate(date: Date | string): string {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
  }).format(new Date(date))
}

export function truncate(str: string, length: number): string {
  if (str.length <= length) return str;
  return str.slice(0, length) + "...";
}

export function generateId(): string {
  return Math.random().toString(36).substring(2, 9);
}
"""


class ResponsiveDesignGenerator:
    """Responsive design utilities"""
    
    @staticmethod
    def generate_breakpoints() -> Dict:
        """Define responsive breakpoints"""
        return {
            "sm": "640px",
            "md": "768px",
            "lg": "1024px",
            "xl": "1280px",
            "2xl": "1536px"
        }
    
    @staticmethod
    def generate_container_config() -> str:
        """Generate responsive container config"""
        return """
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media (min-width: 640px) {
  .container {
    max-width: 640px;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}

@media (min-width: 1536px) {
  .container {
    max-width: 1536px;
  }
}
"""
    
    @staticmethod
    def generate_hide_show_utilities() -> str:
        """Generate responsive hide/show utilities"""
        return """
.hide {
  display: none;
}

@media (min-width: 640px) {
  .sm\:hide {
    display: none;
  }
  .sm\:block {
    display: block;
  }
  .sm\:inline {
    display: inline;
  }
  .sm\:flex {
    display: flex;
  }
}

@media (min-width: 768px) {
  .md\:hide {
    display: none;
  }
  .md\:block {
    display: block;
  }
  .md\:inline {
    display: inline;
  }
  .md\:flex {
    display: flex;
  }
}

@media (min-width: 1024px) {
  .lg\:hide {
    display: none;
  }
  .lg\:block {
    display: block;
  }
  .lg\:inline {
    display: inline;
  }
  .lg\:flex {
    display: flex;
  }
}

@media (min-width: 1280px) {
  .xl\:hide {
    display: none;
  }
  .xl\:block {
    display: block;
  }
  .xl\:inline {
    display: inline;
  }
  .xl\:flex {
    display: flex;
  }
}
"""


class AnimationGenerator:
    """Tailwind animation utilities"""
    
    @staticmethod
    def generate_animations() -> str:
        """Generate custom animations"""
        return """
@layer utilities {
  .animate-in {
    animation: animate-in 0.3s ease-out;
  }
  
  .animate-out {
    animation: animate-out 0.2s ease-in;
  }
  
  .animate-spin {
    animation: spin 1s linear infinite;
  }
  
  .animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }
  
  .animate-bounce {
    animation: bounce 1s infinite;
  }
  
  @keyframes animate-in {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  @keyframes animate-out {
    from {
      opacity: 1;
      transform: scale(1);
    }
    to {
      opacity: 0;
      transform: scale(0.95);
    }
  }
  
  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }
  
  @keyframes bounce {
    0%, 100% {
      transform: translateY(-25%);
      animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
    }
    50% {
      transform: translateY(0);
      animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
    }
  }
  
  .transition-all {
    transition-property: all;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
  }
  
  .transition-colors {
    transition-property: color, background-color, border-color, text-decoration-color, fill, stroke;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
  }
  
  .transition-opacity {
    transition-property: opacity;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
  }
  
  .transition-transform {
    transition-property: transform;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
  }
}
"""


if __name__ == "__main__":
    tailwind_gen = TailwindConfigGenerator()
    shadcn_gen = ShadcnComponentGenerator()
    responsive_gen = ResponsiveDesignGenerator()
    animation_gen = AnimationGenerator()
    
    tailwind_config = tailwind_gen.generate_config()
    globals_css = tailwind_gen.generate_globals_css()
    
    button_component = shadcn_gen.generate_button(ComponentConfig(name="Button", component_type="button"))
    input_component = shadcn_gen.generate_input()
    card_component = shadcn_gen.generate_card()
    utils_component = shadcn_gen.generate_utils()
    
    breakpoints = responsive_gen.generate_breakpoints()
    container_config = responsive_gen.generate_container_config()
    
    animations = animation_gen.generate_animations()
    
    print(f"Tailwind config: {len(tailwind_config)} chars")
    print(f"Globals CSS: {len(globals_css)} chars")
    print(f"Button component: {len(button_component)} chars")
    print(f"Input component: {len(input_component)} chars")
    print(f"Card component: {len(card_component)} chars")
    print(f"Utils component: {len(utils_component)} chars")
    print(f"Breakpoints: {list(breakpoints.keys())}")
    print(f"Animations: {len(animations)} chars")
