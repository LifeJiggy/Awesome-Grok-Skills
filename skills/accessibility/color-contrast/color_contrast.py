"""
Color Contrast Module — WCAG contrast ratio calculation, color blindness simulation,
design token validation, and CSS analysis for accessibility compliance.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TextSize(Enum):
    """WCAG text size classification."""
    NORMAL = "normal"
    LARGE = "large"
    ENHANCED = "enhanced"


class BlindnessType(Enum):
    """Types of color vision deficiency."""
    PROTANOPIA = "protanopia"
    DEUTERANOPIA = "deuteranopia"
    TRITANOPIA = "tritanopia"
    PROTANOMALY = "protanomaly"
    DEUTERANOMALY = "deuteranomaly"
    TRITANOMALY = "tritanomaly"
    ACHROMATOPSIA = "achromatopsia"
    ACHROMATOMALY = "achromatomaly"


class ComplianceStatus(Enum):
    """WCAG compliance result."""
    PASS = "pass"
    FAIL = "fail"
    NA = "not_applicable"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class RGBColor:
    """RGB color representation."""
    r: int
    g: int
    b: int
    alpha: float = 1.0

    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)

    @classmethod
    def from_hex(cls, hex_str: str) -> RGBColor:
        hex_str = hex_str.lstrip("#")
        if len(hex_str) == 3:
            hex_str = "".join(c * 2 for c in hex_str)
        if len(hex_str) == 8:
            r, g, b, a = (
                int(hex_str[0:2], 16),
                int(hex_str[2:4], 16),
                int(hex_str[4:6], 16),
                int(hex_str[6:8], 16) / 255,
            )
            return cls(r=r, g=g, b=b, alpha=a)
        r, g, b = (
            int(hex_str[0:2], 16),
            int(hex_str[2:4], 16),
            int(hex_str[4:6], 16),
        )
        return cls(r=r, g=g, b=b)

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int, alpha: float = 1.0) -> RGBColor:
        return cls(r=max(0, min(255, r)), g=max(0, min(255, g)), b=max(0, min(255, b)), alpha=alpha)

    def __str__(self) -> str:
        return self.to_hex()


@dataclass
class ContrastResult:
    """Result of a contrast ratio check."""
    foreground: RGBColor
    background: RGBColor
    ratio: float
    text_size: TextSize
    wcag_aaa_normal: ComplianceStatus
    wcag_aaa_large: ComplianceStatus
    wcag_aa_normal: ComplianceStatus
    wcag_aa_large: ComplianceStatus
    wcag_aa_non_text: ComplianceStatus
    required_ratio: float
    luminance_fg: float = 0.0
    luminance_bg: float = 0.0

    @property
    def passes(self) -> bool:
        if self.text_size == TextSize.NORMAL:
            return self.wcag_aa_normal == ComplianceStatus.PASS
        return self.wcag_aa_large == ComplianceStatus.PASS

    def to_dict(self) -> Dict[str, Any]:
        return {
            "foreground": self.foreground.to_hex(),
            "background": self.background.to_hex(),
            "ratio": round(self.ratio, 2),
            "text_size": self.text_size.value,
            "wcag_aa_normal": self.wcag_aa_normal.value,
            "wcag_aa_large": self.wcag_aa_large.value,
            "wcag_aaa_normal": self.wcag_aaa_normal.value,
            "wcag_aaa_large": self.wcag_aaa_large.value,
            "required_ratio": self.required_ratio,
        }


@dataclass
class ContrastViolation:
    """A contrast ratio violation found in CSS or design tokens."""
    selector: str
    foreground: str
    background: str
    ratio: float
    required_ratio: float
    text_size: TextSize
    line_number: Optional[int] = None
    file_path: Optional[str] = None
    suggestion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "selector": self.selector,
            "foreground": self.foreground,
            "background": self.background,
            "ratio": round(self.ratio, 2),
            "required_ratio": self.required_ratio,
            "line_number": self.line_number,
        }


@dataclass
class BlindnessSimulation:
    """Result of color blindness simulation."""
    original: RGBColor
    simulated: RGBColor
    blindness_type: BlindnessType

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original": self.original.to_hex(),
            "simulated": self.simulated.to_hex(),
            "blindness_type": self.blindness_type.value,
        }


@dataclass
class DesignTokenReport:
    """Report from design token contrast validation."""
    total_checked: int = 0
    violation_count: int = 0
    violations: List[ContrastViolation] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_checked": self.total_checked,
            "violation_count": self.violation_count,
            "violations": [v.to_dict() for v in self.violations],
            "timestamp": self.timestamp,
        }


# ---------------------------------------------------------------------------
# Core contrast analyzer
# ---------------------------------------------------------------------------

class ContrastAnalyzer:
    """
    WCAG contrast ratio analyzer with color blindness simulation and
    batch processing capabilities.
    """

    # WCAG 2.1 threshold ratios
    THRESHOLDS = {
        "aa_normal": 4.5,
        "aa_large": 3.0,
        "aa_non_text": 3.0,
        "aaa_normal": 7.0,
        "aaa_large": 4.5,
    }

    def __init__(self, precision: int = 2):
        self.precision = precision
        self._color_blindness = ColorBlindnessSimulator()

    @staticmethod
    def _relative_luminance(color: RGBColor) -> float:
        """Calculate relative luminance per WCAG 2.1 definition."""
        def linearize(c: int) -> float:
            srgb = c / 255.0
            return srgb / 12.92 if srgb <= 0.04045 else ((srgb + 0.055) / 1.055) ** 2.4

        r = linearize(color.r)
        g = linearize(color.g)
        b = linearize(color.b)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _contrast_ratio(self, fg: RGBColor, bg: RGBColor) -> float:
        """Calculate contrast ratio between two colors."""
        l1 = self._relative_luminance(fg)
        l2 = self._relative_luminance(bg)
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    def _determine_text_size(
        self, font_size_px: float = 16.0, font_weight: int = 400
    ) -> TextSize:
        """Determine WCAG text size classification."""
        is_bold = font_weight >= 700
        if font_size_px >= 24 or (font_size_px >= 18.66 and is_bold):
            return TextSize.LARGE
        return TextSize.NORMAL

    def check_contrast(
        self,
        foreground: str,
        background: str,
        text_size: TextSize = TextSize.NORMAL,
        font_size_px: float = 16.0,
        font_weight: int = 400,
    ) -> ContrastResult:
        """Check contrast ratio for a foreground/background color pair."""
        fg = RGBColor.from_hex(foreground)
        bg = RGBColor.from_hex(background)

        if font_size_px != 16.0 or font_weight != 400:
            text_size = self._determine_text_size(font_size_px, font_weight)

        ratio = self._contrast_ratio(fg, bg)
        luminance_fg = self._relative_luminance(fg)
        luminance_bg = self._relative_luminance(bg)

        thresholds = self.THRESHOLDS
        aa_threshold = thresholds["aa_large"] if text_size == TextSize.LARGE else thresholds["aa_normal"]
        aaa_threshold = thresholds["aaa_large"] if text_size == TextSize.LARGE else thresholds["aaa_normal"]

        return ContrastResult(
            foreground=fg,
            background=bg,
            ratio=round(ratio, self.precision),
            text_size=text_size,
            wcag_aa_normal=self._status(ratio, thresholds["aa_normal"]),
            wcag_aa_large=self._status(ratio, thresholds["aa_large"]),
            wcag_aa_non_text=self._status(ratio, thresholds["aa_non_text"]),
            wcag_aaa_normal=self._status(ratio, thresholds["aaa_normal"]),
            wcag_aaa_large=self._status(ratio, thresholds["aaa_large"]),
            required_ratio=aa_threshold,
            luminance_fg=round(luminance_fg, 6),
            luminance_bg=round(luminance_bg, 6),
        )

    def _status(self, ratio: float, threshold: float) -> ComplianceStatus:
        return ComplianceStatus.PASS if ratio >= threshold else ComplianceStatus.FAIL

    def suggest_improvement(
        self, foreground: str, background: str, target_ratio: float = 4.5
    ) -> List[str]:
        """Suggest color adjustments to meet a target contrast ratio."""
        fg = RGBColor.from_hex(foreground)
        bg = RGBColor.from_hex(background)
        current = self._contrast_ratio(fg, bg)
        if current >= target_ratio:
            return [f"Current ratio {current:.2f}:1 already meets {target_ratio}:1"]

        suggestions = []
        # Darken foreground
        for step in range(10, 0, -1):
            darker_fg = RGBColor.from_rgb(
                max(0, fg.r - step * 25),
                max(0, fg.g - step * 25),
                max(0, fg.b - step * 25),
            )
            ratio = self._contrast_ratio(darker_fg, bg)
            if ratio >= target_ratio:
                suggestions.append(f"Darken foreground to {darker_fg.to_hex()} (ratio: {ratio:.2f}:1)")
                break

        # Lighten background
        for step in range(10, 0, -1):
            lighter_bg = RGBColor.from_rgb(
                min(255, bg.r + step * 25),
                min(255, bg.g + step * 25),
                min(255, bg.b + step * 25),
            )
            ratio = self._contrast_ratio(fg, lighter_bg)
            if ratio >= target_ratio:
                suggestions.append(f"Lighten background to {lighter_bg.to_hex()} (ratio: {ratio:.2f}:1)")
                break

        return suggestions or [f"Unable to auto-suggest; consider changing both colors"]

    def check_batch(
        self, color_pairs: List[Tuple[str, str]], text_size: TextSize = TextSize.NORMAL
    ) -> List[ContrastResult]:
        """Check contrast for multiple color pairs."""
        return [self.check_contrast(fg, bg, text_size) for fg, bg in color_pairs]


# ---------------------------------------------------------------------------
# Color blindness simulation
# ---------------------------------------------------------------------------

class ColorBlindnessSimulator:
    """Simulates color vision deficiencies using Brettel et al. algorithm matrices."""

    # Transformation matrices (approximate) for each blindness type
    MATRICES: Dict[BlindnessType, List[List[float]]] = {
        BlindnessType.PROTANOPIA: [
            [0.152286, 1.052583, -0.204868],
            [0.114503, 0.786281, 0.099216],
            [-0.003882, -0.048116, 1.051998],
        ],
        BlindnessType.DEUTERANOPIA: [
            [0.367322, 0.860646, -0.227968],
            [0.280085, 0.672501, 0.047413],
            [-0.011820, 0.042940, 0.968881],
        ],
        BlindnessType.TRITANOPIA: [
            [1.255528, -0.076749, -0.178779],
            [-0.078411, 0.930809, 0.147602],
            [0.004733, 0.691367, 0.303900],
        ],
        BlindnessType.PROTANOMALY: [
            [0.458064, 0.679578, -0.137642],
            [0.092785, 0.846313, 0.060902],
            [-0.007494, -0.016807, 1.024301],
        ],
        BlindnessType.DEUTERANOMALY: [
            [0.547494, 0.607765, -0.155259],
            [0.181692, 0.781742, 0.036566],
            [-0.010410, 0.027275, 0.983136],
        ],
        BlindnessType.TRITANOMALY: [
            [1.017277, 0.027029, -0.044306],
            [-0.006113, 0.958479, 0.047634],
            [0.006379, 0.248708, 0.744913],
        ],
        BlindnessType.ACHROMATOPSIA: [
            [0.299, 0.587, 0.114],
            [0.299, 0.587, 0.114],
            [0.299, 0.587, 0.114],
        ],
        BlindnessType.ACHROMATOMALY: [
            [0.444549, 0.545832, 0.009619],
            [0.149895, 0.790768, 0.059337],
            [0.020497, 0.124339, 0.855164],
        ],
    }

    def simulate(self, color: RGBColor, blindness_type: BlindnessType) -> RGBColor:
        """Simulate how a color appears to someone with a specific color vision deficiency."""
        matrix = self.MATRICES[blindness_type]
        r = matrix[0][0] * color.r + matrix[0][1] * color.g + matrix[0][2] * color.b
        g = matrix[1][0] * color.r + matrix[1][1] * color.g + matrix[1][2] * color.b
        b = matrix[2][0] * color.r + matrix[2][1] * color.g + matrix[2][2] * color.b
        return RGBColor.from_rgb(int(max(0, min(255, r))), int(max(0, min(255, g))), int(max(0, min(255, b))))

    def simulate_all(self, color_hex: str) -> Dict[BlindnessType, RGBColor]:
        """Simulate a color across all blindness types."""
        color = RGBColor.from_hex(color_hex)
        return {bt: self.simulate(color, bt) for bt in BlindnessType}

    def simulate_pair(
        self, fg_hex: str, bg_hex: str, blindness_type: BlindnessType
    ) -> Tuple[RGBColor, RGBColor, float]:
        """Simulate a color pair and compute resulting contrast ratio."""
        fg = RGBColor.from_hex(fg_hex)
        bg = RGBColor.from_hex(bg_hex)
        sim_fg = self.simulate(fg, blindness_type)
        sim_bg = self.simulate(bg, blindness_type)

        def lum(c: RGBColor) -> float:
            def lin(v: int) -> float:
                s = v / 255.0
                return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4
            return 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b)

        l1 = lum(sim_fg)
        l2 = lum(sim_bg)
        ratio = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
        return sim_fg, sim_bg, round(ratio, 2)


# ---------------------------------------------------------------------------
# CSS analyzer
# ---------------------------------------------------------------------------

class CSSAnalyzer:
    """Analyzes CSS files for color contrast violations."""

    COLOR_PATTERN = re.compile(
        r"(?:color|background-color|background)\s*:\s*"
        r"(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|[a-z]+)"
    )
    SELECTOR_PATTERN = re.compile(r"([.#][\w-]+|[\w]+)\s*\{")
    CSS_COLOR_NAMES = {
        "white": "#ffffff", "black": "#000000", "red": "#ff0000",
        "green": "#008000", "blue": "#0000ff", "yellow": "#ffff00",
        "gray": "#808080", "grey": "#808080", "orange": "#ffa500",
        "purple": "#800080", "navy": "#000080", "teal": "#008080",
    }

    def __init__(self, css_path: str):
        self.css_path = css_path
        self._analyzer = ContrastAnalyzer()

    def _parse_color(self, color_str: str) -> str:
        """Normalize a CSS color string to hex."""
        color_str = color_str.strip().lower()
        if color_str.startswith("#"):
            return color_str
        if color_str in self.CSS_COLOR_NAMES:
            return self.CSS_COLOR_NAMES[color_str]
        match = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", color_str)
        if match:
            r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
            return RGBColor.from_rgb(r, g, b).to_hex()
        return color_str

    def find_contrast_violations(self) -> List[ContrastViolation]:
        """Scan CSS file for contrast violations."""
        violations: List[ContrastViolation] = []
        try:
            content = Path(self.css_path).read_text(encoding="utf-8")
        except FileNotFoundError:
            return violations

        current_selector = "unknown"
        colors_found: Dict[str, str] = {}
        line_number = 0

        for line in content.split("\n"):
            line_number += 1
            line = line.strip()

            selector_match = self.SELECTOR_PATTERN.search(line)
            if selector_match:
                current_selector = selector_match.group(0).strip()

            color_match = self.COLOR_PATTERN.search(line)
            if color_match:
                prop = color_match.group(0)
                if "background" in prop:
                    colors_found["background"] = self._parse_color(
                        color_match.group(1)
                    )
                else:
                    colors_found["foreground"] = self._parse_color(
                        color_match.group(1)
                    )

            if "foreground" in colors_found and "background" in colors_found:
                fg = colors_found["foreground"]
                bg = colors_found["background"]
                try:
                    result = self._analyzer.check_contrast(fg, bg)
                    if not result.passes:
                        violations.append(
                            ContrastViolation(
                                selector=current_selector,
                                foreground=fg,
                                background=bg,
                                ratio=result.ratio,
                                required_ratio=result.required_ratio,
                                text_size=result.text_size,
                                line_number=line_number,
                                file_path=self.css_path,
                            )
                        )
                except ValueError:
                    pass
                colors_found.clear()

        return violations


# ---------------------------------------------------------------------------
# Design token validator
# ---------------------------------------------------------------------------

class DesignTokenValidator:
    """Validates color contrast in design token files (JSON format)."""

    def __init__(self, token_path: str):
        self.token_path = token_path
        self._analyzer = ContrastAnalyzer()

    def validate(self) -> DesignTokenReport:
        """Validate all color token pairs in the token file."""
        report = DesignTokenReport()
        try:
            data = json.loads(Path(self.token_path).read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return report

        tokens = data.get("tokens", data)
        color_pairs = self._extract_color_pairs(tokens)

        for pair_name, fg, bg in color_pairs:
            report.total_checked += 1
            try:
                result = self._analyzer.check_contrast(fg, bg)
                if not result.passes:
                    report.violations.append(
                        ContrastViolation(
                            selector=pair_name,
                            foreground=fg,
                            background=bg,
                            ratio=result.ratio,
                            required_ratio=result.required_ratio,
                            text_size=result.text_size,
                            file_path=self.token_path,
                        )
                    )
                    report.violation_count += 1
            except ValueError:
                pass

        return report

    def _extract_color_pairs(
        self, tokens: Dict[str, Any], prefix: str = ""
    ) -> List[Tuple[str, str, str]]:
        """Recursively extract foreground/background color pairs from token tree."""
        pairs: List[Tuple[str, str, str]] = []
        fg_keys = {"foreground", "fg", "text", "color"}
        bg_keys = {"background", "bg"}

        for key, value in tokens.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                pairs.extend(self._extract_color_pairs(value, full_key))
            elif isinstance(value, str) and value.startswith("#"):
                pass

        fg_color = None
        bg_color = None
        for key, value in tokens.items():
            if key in fg_keys and isinstance(value, str):
                fg_color = value
            elif key in bg_keys and isinstance(value, str):
                bg_color = value

        if fg_color and bg_color:
            pairs.append((prefix, fg_color, bg_color))

        return pairs


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the color contrast analysis toolkit."""
    analyzer = ContrastAnalyzer()
    simulator = ColorBlindnessSimulator()

    print("Color Contrast Analysis")
    print("=" * 60)

    # Check individual color pairs
    pairs = [
        ("#767676", "#FFFFFF", "Gray on white (classic fail)"),
        ("#000000", "#FFFFFF", "Black on white (always pass)"),
        ("#1E40AF", "#FFFFFF", "Blue on white"),
        ("#6B7280", "#F3F4F6", "Muted gray on light gray"),
    ]

    for fg, bg, desc in pairs:
        result = analyzer.check_contrast(fg, bg)
        status = "PASS" if result.passes else "FAIL"
        print(f"\n[{status}] {desc}")
        print(f"  {fg} on {bg} = {result.ratio}:1 (need {result.required_ratio}:1)")
        print(f"  AA normal: {result.wcag_aa_normal.value}, AA large: {result.wcag_aa_large.value}")
        print(f"  AAA normal: {result.wcag_aaa_normal.value}")

    # Color blindness simulation
    print("\n\nColor Blindness Simulation")
    print("=" * 60)
    test_color = "#FF6600"
    results = simulator.simulate_all(test_color)
    for bt, color in results.items():
        print(f"  {bt.value:20s}: {test_color} → {color.to_hex()}")

    # Simulate a pair
    sim_fg, sim_bg, sim_ratio = simulator.simulate_pair(
        "#FF0000", "#00FF00", BlindnessType.DEUTERANOPIA
    )
    print(f"\nDeuteranopia: #FF0000/#00FF00 → {sim_fg}/{sim_bg} = {sim_ratio}:1")

    # Suggestions
    print("\n\nImprovement Suggestions")
    print("=" * 60)
    suggestions = analyzer.suggest_improvement("#767676", "#FFFFFF", target_ratio=4.5)
    for s in suggestions:
        print(f"  {s}")


if __name__ == "__main__":
    main()
