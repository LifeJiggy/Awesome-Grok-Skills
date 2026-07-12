"""
Cultural Adaptation Module
Cultural adaptation of UI, content, and experiences for global markets
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class HolidayType(Enum):
    PUBLIC = "public"
    BANK = "bank"
    OBSERVANCE = "observance"
    SEASONAL = "seasonal"

class ContentType(Enum):
    MARKETING = "marketing"
    LEGAL = "legal"
    UI = "ui"
    SUPPORT = "support"

@dataclass
class ColorSymbolism:
    color: str = ""
    country_code: str = ""
    meaning: str = ""
    positive: List[str] = field(default_factory=list)
    negative: List[str] = field(default_factory=list)
    usage_recommendation: str = ""

@dataclass
class ToneAdaptation:
    content: str = ""
    source_culture: str = ""
    target_culture: str = ""
    changes: List[str] = field(default_factory=list)
    cultural_notes: List[str] = field(default_factory=list)

@dataclass
class CulturalRisk:
    market: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    description: str = ""
    recommendation: str = ""

@dataclass
class Holiday:
    date: str = ""
    name: str = ""
    country_code: str = ""
    type: HolidayType = HolidayType.PUBLIC
    business_impact: str = ""
    is_recurring: bool = True

@dataclass
class LayoutPreference:
    country_code: str = ""
    text_direction: str = "ltr"
    text_expansion_factor: float = 1.0
    prefers_left_alignment: bool = True
    date_format: str = "MM/DD/YYYY"
    number_format: str = "1,234.56"

COLOR_DATABASE = {
    ("red", "CN"): ColorSymbolism("red", "CN", "Luck and prosperity", ["good fortune", "joy", "celebration"], ["danger", "warning"], "Use for celebrations and positive messaging"),
    ("red", "US"): ColorSymbolism("red", "US", "Passion and urgency", ["love", "excitement", "sale"], ["danger", "error"], "Effective for CTAs and urgency"),
    ("white", "JP"): ColorSymbolism("white", "JP", "Purity and mourning", ["purity", "cleanliness"], ["death", "funeral"], "Use carefully; associated with mourning"),
    ("white", "US"): ColorSymbolism("white", "US", "Cleanliness and simplicity", ["purity", "clean", "minimal"], ["sterile"], "Safe for backgrounds and clean design"),
    ("green", "SA"): ColorSymbolism("green", "SA", "Islam and nature", ["paradise", "nature", "islam"], [], "Respectful color; use thoughtfully"),
    ("yellow", "FR"): ColorSymbolism("yellow", "FR", "Jealousy and caution", ["warmth"], ["jealousy", "caution"], "Use sparingly; can convey negative emotions"),
}

TONE_DATABASE = {
    ("US", "JP"): {"formality": "high", "directness": "low", "humor": "avoid", "notes": ["Use honorific language", "Avoid direct commands", "Be indirect in requests"]},
    ("US", "DE"): {"formality": "medium", "directness": "high", "humor": "avoid", "notes": ["Be direct and factual", "Avoid superlatives", "Focus on technical details"]},
    ("US", "BR"): {"formality": "low", "directness": "medium", "humor": "allow", "notes": ["Use warm, friendly tone", "Relationship-building is important", "Emojis acceptable"]},
}

HOLIDAYS_DB = {
    "JP": [Holiday(date="2024-01-01", name="New Year's Day", country_code="JP", type=HolidayType.PUBLIC, business_impact="offices closed"), Holiday(date="2024-01-08", name="Coming of Age Day", country_code="JP", type=HolidayType.PUBLIC, business_impact="offices closed")],
    "US": [Holiday(date="2024-01-01", name="New Year's Day", country_code="US", type=HolidayType.PUBLIC, business_impact="offices closed"), Holiday(date="2024-07-04", name="Independence Day", country_code="US", type=HolidayType.PUBLIC, business_impact="offices closed")],
    "DE": [Holiday(date="2024-01-01", name="New Year's Day", country_code="DE", type=HolidayType.PUBLIC, business_impact="offices closed"), Holiday(date="2024-10-03", name="German Unity Day", country_code="DE", type=HolidayType.PUBLIC, business_impact="offices closed")],
}

LAYOUT_PREFS = {
    "US": LayoutPreference("US", "ltr", 1.0, True, "MM/DD/YYYY", "1,234.56"),
    "DE": LayoutPreference("DE", "ltr", 1.1, True, "DD.MM.YYYY", "1.234,56"),
    "JP": LayoutPreference("JP", "ltr", 0.9, True, "YYYY年MM月DD日", "1,234.56"),
    "SA": LayoutPreference("SA", "rtl", 1.0, False, "DD/MM/YYYY", "1٬234٫56"),
}

class CulturalAdvisor:
    def get_color_symbolism(self, color: str, country_code: str) -> Optional[ColorSymbolism]:
        return COLOR_DATABASE.get((color, country_code))

    def get_layout_preference(self, country_code: str) -> Optional[LayoutPreference]:
        return LAYOUT_PREFS.get(country_code)

class ToneAdapter:
    def adapt(self, content: str, source_culture: str, target_culture: str, content_type: ContentType = ContentType.MARKETING) -> ToneAdaptation:
        tone_rules = TONE_DATABASE.get((source_culture, target_culture), {})
        adapted = content
        changes = []
        notes = tone_rules.get("notes", [])
        if tone_rules.get("formality") == "high":
            adapted = adapted.replace("!", ".").replace("Buy", "Please consider purchasing")
            changes.append("Increased formality")
        return ToneAdaptation(content=adapted, source_culture=source_culture, target_culture=target_culture, changes=changes, cultural_notes=notes)

class CulturalRiskAssessor:
    HIGH_RISK_PHRASES = {"disrupt", "revolutionary", "destroy", "crush", "dominate"}
    def assess(self, content: str, target_markets: List[str]) -> List[CulturalRisk]:
        risks = []
        content_lower = content.lower()
        for market in target_markets:
            for phrase in self.HIGH_RISK_PHRASES:
                if phrase in content_lower:
                    risks.append(CulturalRisk(market=market, risk_level=RiskLevel.MEDIUM, description=f"Aggressive language '{phrase}' may not resonate", recommendation="Consider softer alternative"))
        return risks

class HolidayCalendar:
    def get_holidays(self, country_code: str, year: int = 2024, include_observances: bool = True) -> List[Holiday]:
        holidays = HOLIDAYS_DB.get(country_code, [])
        return [h for h in holidays if h.date.startswith(str(year))]

def main() -> None:
    print("=" * 60)
    print("  Cultural Adaptation Module — Demo")
    print("=" * 60)

    advisor = CulturalAdvisor()
    red = advisor.get_color_symbolism("red", "CN")
    if red:
        print(f"\n[+] Red in China: {red.meaning}")
        print(f"    Positive: {red.positive}")
        print(f"    Usage: {red.usage_recommendation}")

    adapter = ToneAdapter()
    adapted = adapter.adapt("Buy now and save 50%!", "US", "JP")
    print(f"\n[+] Tone Adaptation:")
    print(f"    Original: Buy now and save 50%!")
    print(f"    Adapted: {adapted.content}")
    print(f"    Notes: {adapted.cultural_notes}")

    assessor = CulturalRiskAssessor()
    risks = assessor.assess("Our revolutionary product will disrupt the market!", ["JP", "DE"])
    print(f"\n[+] Cultural Risks: {len(risks)} found")
    for risk in risks:
        print(f"    {risk.market}: {risk.description}")

    calendar = HolidayCalendar()
    holidays = calendar.get_holidays("JP", 2024)
    print(f"\n[+] Japan Holidays: {len(holidays)}")
    for h in holidays[:3]:
        print(f"    {h.date}: {h.name}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
