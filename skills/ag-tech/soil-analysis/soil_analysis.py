"""
Soil Analysis Module — Laboratory result interpretation, nutrient recommendations,
pH management, soil health assessment, and multi-year trend analysis.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class NutrientStatus(Enum):
    DEFICIENT = "deficient"
    LOW = "low"
    OPTIMAL = "optimal"
    HIGH = "high"
    VERY_HIGH = "very_high"


class SoilTexture(Enum):
    SAND = "sand"
    LOAMY_SAND = "loamy_sand"
    SANDY_LOAM = "sandy_loam"
    LOAM = "loam"
    SILT_LOAM = "silt_loam"
    SILT = "silt"
    CLAY_LOAM = "clay_loam"
    CLAY = "clay"


class ExtractionMethod(Enum):
    MEHLICH3 = "mehlich_3"
    BRAY1 = "bray_1"
    AMMONIUM_ACETATE = "ammonium_acetate"
    DTPA = "dtpa"
    OLSEN = "olsen"


class CropType(Enum):
    CORN = "corn"
    SOYBEANS = "soybeans"
    WHEAT = "wheat"
    COTTON = "cotton"
    RICE = "rice"
    ALFALFA = "alfalfa"
    GRASS_HAY = "grass_hay"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SoilSample:
    """A complete soil sample with laboratory analysis results."""
    sample_id: str
    latitude: float = 0.0
    longitude: float = 0.0
    depth_inches: float = 8.0
    collection_date: str = ""
    lab_name: str = ""
    extraction_method: ExtractionMethod = ExtractionMethod.MEHLICH3

    # Primary nutrients
    nitrogen_ppm: float = 0.0
    phosphorus_ppm: float = 0.0
    potassium_ppm: float = 0.0
    sulfur_ppm: float = 0.0

    # pH and buffer
    ph: float = 7.0
    buffer_ph: float = 7.0

    # Secondary nutrients and micronutrients
    calcium_ppm: float = 0.0
    magnesium_ppm: float = 0.0
    sodium_ppm: float = 0.0
    zinc_ppm: float = 0.0
    manganese_ppm: float = 0.0
    iron_ppm: float = 0.0
    copper_ppm: float = 0.0
    boron_ppm: float = 0.0

    # Soil properties
    organic_matter_pct: float = 0.0
    cec: float = 0.0  # meq/100g
    base_saturation_pct: float = 0.0

    @property
    def p_status(self) -> str:
        if self.phosphorus_ppm < 15:
            return "deficient"
        elif self.phosphorus_ppm < 30:
            return "low"
        elif self.phosphorus_ppm < 60:
            return "optimal"
        elif self.phosphorus_ppm < 100:
            return "high"
        return "very_high"

    @property
    def k_status(self) -> str:
        if self.potassium_ppm < 80:
            return "deficient"
        elif self.potassium_ppm < 130:
            return "low"
        elif self.potassium_ppm < 200:
            return "optimal"
        elif self.potassium_ppm < 300:
            return "high"
        return "very_high"

    @property
    def om_status(self) -> str:
        if self.organic_matter_pct < 1.5:
            return "very_low"
        elif self.organic_matter_pct < 2.5:
            return "low"
        elif self.organic_matter_pct < 4.0:
            return "optimal"
        elif self.organic_matter_pct < 6.0:
            return "high"
        return "very_high"

    @property
    def base_saturation(self) -> float:
        if self.cec > 0:
            total_bases = self.calcium_ppm / 200.4 + self.magnesium_ppm / 121.5 + self.sodium_ppm / 229.9
            return round((total_bases / self.cec) * 100, 1)
        return 0.0

    @property
    def mg_ca_ratio(self) -> float:
        if self.magnesium_ppm > 0:
            return round(self.calcium_ppm / self.magnesium_ppm, 1)
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "ph": round(self.ph, 1),
            "nitrogen": round(self.nitrogen_ppm, 1),
            "phosphorus": round(self.phosphorus_ppm, 1),
            "potassium": round(self.potassium_ppm, 1),
            "organic_matter": round(self.organic_matter_pct, 1),
            "cec": round(self.cec, 1),
            "p_status": self.p_status,
            "k_status": self.k_status,
        }


@dataclass
class NutrientRec:
    """Nutrient recommendation for a specific field and crop."""
    nitrogen_lb_ac: float = 0.0
    phosphorus_lb_ac: float = 0.0
    potassium_lb_ac: float = 0.0
    sulfur_lb_ac: float = 0.0
    lime_tons_ac: float = 0.0
    zinc_lb_ac: float = 0.0
    manganese_lb_ac: float = 0.0
    boron_lb_ac: float = 0.0
    product: str = ""
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nitrogen": round(self.nitrogen_lb_ac, 1),
            "phosphorus_p2o5": round(self.phosphorus_lb_ac, 1),
            "potassium_k2o": round(self.potassium_lb_ac, 1),
            "sulfur": round(self.sulfur_lb_ac, 1),
            "lime_tons": round(self.lime_tons_ac, 2),
            "notes": self.notes,
        }


@dataclass
class LimeResult:
    """Lime requirement calculation result."""
    tons_per_acre: float
    product: str
    ecce: float  # effective calcium carbonate equivalent
    fineness_pct: float
    neutralizing_power: float
    equivalent_calcitic: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tons_per_acre": round(self.tons_per_acre, 2),
            "product": self.product,
            "ecce": round(self.ecce, 1),
        }


@dataclass
class SoilHealthScore:
    """Soil health assessment score."""
    total_score: float
    chemical_score: float
    physical_score: float
    biological_score: float
    components: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)

    @property
    def grade(self) -> str:
        if self.total_score >= 80:
            return "A (Excellent)"
        elif self.total_score >= 65:
            return "B (Good)"
        elif self.total_score >= 50:
            return "C (Fair)"
        elif self.total_score >= 35:
            return "D (Poor)"
        return "F (Very Poor)"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_score": round(self.total_score, 1),
            "grade": self.grade,
            "chemical": round(self.chemical_score, 1),
            "physical": round(self.physical_score, 1),
            "biological": round(self.biological_score, 1),
            "components": {k: round(v, 1) for k, v in self.components.items()},
        }


@dataclass
class TrendData:
    """Year-over-year soil test trend for a parameter."""
    parameter: str
    year_values: Dict[str, float] = field(default_factory=dict)

    @property
    def trend_direction(self) -> str:
        values = list(self.year_values.values())
        if len(values) < 2:
            return "insufficient_data"
        recent = values[-1]
        previous = values[-2]
        diff = recent - previous
        if abs(diff) < 0.5:
            return "stable"
        return "increasing" if diff > 0 else "decreasing"

    @property
    def total_change(self) -> float:
        values = list(self.year_values.values())
        if len(values) < 2:
            return 0.0
        return values[-1] - values[0]


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class SoilTestLab:
    """Load and manage soil test laboratory results."""

    def __init__(self):
        self.samples: List[SoilSample] = []

    @classmethod
    def from_file(cls, filepath: str) -> SoilTestLab:
        lab = cls()
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sample = SoilSample(
                        sample_id=row.get("sample_id", f"S{len(lab.samples)+1}"),
                        latitude=float(row.get("latitude", 0)),
                        longitude=float(row.get("longitude", 0)),
                        depth_inches=float(row.get("depth", 8)),
                        ph=float(row.get("ph", 7.0)),
                        buffer_ph=float(row.get("buffer_ph", 6.8)),
                        nitrogen_ppm=float(row.get("nitrogen", 0)),
                        phosphorus_ppm=float(row.get("phosphorus", 0)),
                        potassium_ppm=float(row.get("potassium", 0)),
                        sulfur_ppm=float(row.get("sulfur", 0)),
                        calcium_ppm=float(row.get("calcium", 0)),
                        magnesium_ppm=float(row.get("magnesium", 0)),
                        sodium_ppm=float(row.get("sodium", 0)),
                        zinc_ppm=float(row.get("zinc", 0)),
                        manganese_ppm=float(row.get("manganese", 0)),
                        iron_ppm=float(row.get("iron", 0)),
                        copper_ppm=float(row.get("copper", 0)),
                        boron_ppm=float(row.get("boron", 0)),
                        organic_matter_pct=float(row.get("organic_matter", 0)),
                        cec=float(row.get("cec", 15)),
                    )
                    lab.samples.append(sample)
        except FileNotFoundError:
            pass
        return lab

    @classmethod
    def from_dicts(cls, data: List[Dict[str, Any]]) -> SoilTestLab:
        lab = cls()
        for d in data:
            lab.samples.append(SoilSample(
                sample_id=d.get("sample_id", ""),
                ph=d.get("ph", 7.0),
                buffer_ph=d.get("buffer_ph", 6.8),
                nitrogen_ppm=d.get("nitrogen", 0),
                phosphorus_ppm=d.get("phosphorus", 0),
                potassium_ppm=d.get("potassium", 0),
                sulfur_ppm=d.get("sulfur", 0),
                calcium_ppm=d.get("calcium", 0),
                magnesium_ppm=d.get("magnesium", 0),
                organic_matter_pct=d.get("organic_matter", 0),
                cec=d.get("cec", 15),
                zinc_ppm=d.get("zinc", 0),
                manganese_ppm=d.get("manganese", 0),
                boron_ppm=d.get("boron", 0),
            ))
        return lab

    def get_summary(self) -> Dict[str, Any]:
        if not self.samples:
            return {"count": 0}
        ph_vals = [s.ph for s in self.samples]
        p_vals = [s.phosphorus_ppm for s in self.samples]
        k_vals = [s.potassium_ppm for s in self.samples]
        om_vals = [s.organic_matter_pct for s in self.samples]
        return {
            "count": len(self.samples),
            "ph_avg": round(sum(ph_vals) / len(ph_vals), 1),
            "p_avg": round(sum(p_vals) / len(p_vals), 1),
            "k_avg": round(sum(k_vals) / len(k_vals), 1),
            "om_avg": round(sum(om_vals) / len(om_vals), 1),
        }


class NutrientRecommendation:
    """Calculate nutrient recommendations based on soil test and crop."""

    # Corn nutrient removal rates (lb per bu)
    CORN_REMOVAL = {"nitrogen": 0.8, "phosphorus": 0.37, "potassium": 0.27, "sulfur": 0.12}

    def __init__(self, crop: str = "corn", target_yield: float = 180):
        self.crop = crop.lower()
        self.target_yield = target_yield

    def calculate(self, sample: SoilSample) -> NutrientRec:
        rec = NutrientRec()
        removal = self.CORN_REMOVAL if self.crop == "corn" else self.CORN_REMOVAL

        # Nitrogen
        crop_needs = self.target_yield * removal["nitrogen"]
        soil_credit = sample.nitrogen_ppm * 0.5
        organic_credit = sample.organic_matter_pct * 20 * 0.04  # ~4% mineralization
        rec.nitrogen_lb_ac = max(0, crop_needs - soil_credit - organic_credit)

        # Phosphorus (build and maintain)
        if sample.phosphorus_ppm < 25:
            rec.phosphorus_lb_ac = max(0, self.target_yield * removal["phosphorus"] - sample.phosphorus_ppm * 0.5)
            rec.notes.append("Building P level — apply extra 30 lb P2O5/ac")
        elif sample.phosphorus_ppm > 100:
            rec.phosphorus_lb_ac = 0
            rec.notes.append("P level very high — skip P application this year")
        else:
            rec.phosphorus_lb_ac = self.target_yield * removal["phosphorus"]

        # Potassium
        if sample.potassium_ppm < 120:
            rec.potassium_lb_ac = max(0, self.target_yield * removal["potassium"] * 1.2)
            rec.notes.append("Building K level — apply 20% above removal rate")
        else:
            rec.potassium_lb_ac = self.target_yield * removal["potassium"]

        # Sulfur
        rec.sulfur_lb_ac = max(0, self.target_yield * removal["sulfur"] - sample.sulfur_ppm * 0.2)

        # Lime
        if sample.ph < 6.0:
            rec.lime_tons_ac = (6.5 - sample.ph) * 0.5  # simplified
            rec.notes.append(f"Current pH {sample.ph:.1f} — target 6.5")
            rec.product = "Agricultural Limestone"

        # Micronutrients
        if sample.zinc_ppm < 1.0:
            rec.zinc_lb_ac = 2.0
        if sample.manganese_ppm < 5.0:
            rec.manganese_lb_ac = 1.0
        if sample.boron_ppm < 0.5:
            rec.boron_lb_ac = 0.5

        return rec


class pHManager:
    """Calculate lime requirements and pH adjustments."""

    LIME_FACTORS = {
        "sand": 0.60, "loamy_sand": 0.70, "sandy_loam": 0.80,
        "loam": 1.00, "silt_loam": 1.10, "silt": 1.20,
        "clay_loam": 1.30, "clay": 1.50,
    }

    def calculate_lime(
        self,
        current_ph: float,
        target_ph: float,
        buffer_ph: float,
        soil_type: str = "silt_loam",
    ) -> LimeResult:
        ph_diff = target_ph - current_ph
        base_rate = ph_diff * 1.5  # tons per acre per pH unit
        soil_factor = self.LIME_FACTORS.get(soil_type, 1.0)
        adjusted_rate = base_rate / soil_factor
        ecce = 90.0
        fineness = 60.0

        return LimeResult(
            tons_per_acre=max(0, adjusted_rate),
            product="Agricultural Limestone (calcitic)",
            ecce=ecce,
            fineness_pct=fineness,
            neutralizing_power=ecce * fineness / 100,
            equivalent_calcitic=adjusted_rate,
        )

    def calculate_acidifier(
        self, current_ph: float, target_ph: float, soil_type: str = "silt_loam"
    ) -> float:
        ph_diff = current_ph - target_ph
        element_sulfur_rate = ph_diff * 0.6
        return max(0, element_sulfur_rate)


class SoilHealthIndex:
    """Evaluate soil health across chemical, physical, and biological dimensions."""

    def evaluate(
        self,
        organic_matter_pct: float = 0.0,
        ph: float = 7.0,
        cec: float = 15.0,
        microbial_activity: float = 0.5,
        aggregate_stability: float = 50.0,
        infiltration_rate: float = 1.0,
        bulk_density: float = 1.3,
        **kwargs: Any,
    ) -> SoilHealthScore:
        components: Dict[str, float] = {}

        # Chemical (40% of total)
        ph_score = max(0, 100 - abs(ph - 6.5) * 30)
        om_score = min(100, organic_matter_pct / 4.0 * 100)
        cec_score = min(100, cec / 25.0 * 100)
        chemical = (ph_score + om_score + cec_score) / 3
        components["ph"] = ph_score
        components["organic_matter"] = om_score
        components["cec"] = cec_score

        # Physical (30% of total)
        agg_score = aggregate_stability
        infil_score = min(100, infiltration_rate / 2.0 * 100)
        bd_score = max(0, 100 - abs(bulk_density - 1.3) * 100)
        physical = (agg_score + infil_score + bd_score) / 3
        components["aggregate_stability"] = agg_score
        components["infiltration"] = infil_score
        components["bulk_density"] = bd_score

        # Biological (30% of total)
        bio_score = microbial_activity * 100
        components["microbial_activity"] = bio_score
        biological = bio_score

        total = chemical * 0.4 + physical * 0.3 + biological * 0.3

        recommendations = []
        if ph_score < 60:
            recommendations.append("Adjust pH toward 6.5 with lime or acidifier")
        if om_score < 50:
            recommendations.append("Increase organic matter with cover crops and residue management")
        if aggregate_stability < 50:
            recommendations.append("Improve aggregate stability with reduced tillage and organic amendments")
        if microbial_activity < 0.5:
            recommendations.append("Boost microbial activity with diverse cover crop mixes")

        return SoilHealthScore(
            total_score=total,
            chemical_score=chemical,
            physical_score=physical,
            biological_score=biological,
            components=components,
            recommendations=recommendations,
        )


class TrendAnalyzer:
    """Track soil test trends over multiple years."""

    def __init__(self):
        self._yearly_data: Dict[str, Dict[str, float]] = {}

    def add_year(self, year: str, sample: SoilSample) -> None:
        self._yearly_data[year] = {
            "ph": sample.ph,
            "phosphorus": sample.phosphorus_ppm,
            "potassium": sample.potassium_ppm,
            "organic_matter": sample.organic_matter_pct,
            "cec": sample.cec,
        }

    def get_trend(self, parameter: str) -> TrendData:
        trend = TrendData(parameter=parameter)
        for year, data in sorted(self._yearly_data.items()):
            if parameter in data:
                trend.year_values[year] = data[parameter]
        return trend

    def generate_report(self) -> Dict[str, Any]:
        report = {}
        for param in ["ph", "phosphorus", "potassium", "organic_matter"]:
            trend = self.get_trend(param)
            report[param] = {
                "direction": trend.trend_direction,
                "total_change": round(trend.total_change, 2),
                "values": trend.year_values,
            }
        return report


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the soil analysis toolkit."""
    print("Soil Analysis Toolkit")
    print("=" * 60)

    # Create sample data
    lab = SoilTestLab.from_dicts([
        {"sample_id": "S001", "ph": 5.8, "buffer_ph": 6.8, "nitrogen": 35,
         "phosphorus": 18, "potassium": 145, "organic_matter": 3.2, "cec": 18,
         "zinc": 1.5, "manganese": 8, "boron": 0.6},
        {"sample_id": "S002", "ph": 6.4, "buffer_ph": 6.9, "nitrogen": 52,
         "phosphorus": 42, "potassium": 210, "organic_matter": 4.1, "cec": 22,
         "zinc": 0.8, "manganese": 12, "boron": 0.3},
        {"sample_id": "S003", "ph": 7.1, "buffer_ph": 7.2, "nitrogen": 28,
         "phosphorus": 65, "potassium": 95, "organic_matter": 2.5, "cec": 14,
         "zinc": 2.1, "manganese": 5, "boron": 0.8},
    ])

    summary = lab.get_summary()
    print(f"\nLab Summary ({summary['count']} samples):")
    print(f"  pH avg: {summary['ph_avg']}, P avg: {summary['p_avg']}ppm, K avg: {summary['k_avg']}ppm")

    # Nutrient recommendations
    print("\n--- Nutrient Recommendations (Corn @ 180 bu/ac) ---")
    recommender = NutrientRecommendation(crop="corn", target_yield=180)
    for sample in lab.samples:
        rec = recommender.calculate(sample)
        print(f"\n  {sample.sample_id}:")
        print(f"    N: {rec.nitrogen_lb_ac:.0f} lb/ac")
        print(f"    P2O5: {rec.phosphorus_lb_ac:.0f} lb/ac")
        print(f"    K2O: {rec.potassium_lb_ac:.0f} lb/ac")
        print(f"    Lime: {rec.lime_tons_ac:.2f} tons/ac")
        for note in rec.notes:
            print(f"    Note: {note}")

    # pH management
    print("\n--- pH Management ---")
    ph_mgr = pHManager()
    lime = ph_mgr.calculate_lime(5.8, 6.5, 6.8, "silt_loam")
    print(f"  Lime needed: {lime.tons_per_acre:.2f} tons/ac ({lime.product})")

    # Soil health
    print("\n--- Soil Health Assessment ---")
    health = SoilHealthIndex()
    score = health.evaluate(
        organic_matter_pct=3.5, ph=6.5, cec=18.0,
        microbial_activity=0.75, aggregate_stability=65, infiltration_rate=1.5,
    )
    print(f"  Score: {score.total_score:.0f}/100 ({score.grade})")
    print(f"  Chemical: {score.chemical_score:.0f}, Physical: {score.physical_score:.0f}, Biological: {score.biological_score:.0f}")


if __name__ == "__main__":
    main()
