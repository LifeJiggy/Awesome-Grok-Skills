"""
Circular Economy Module
Material flow analysis, product lifecycle tracking, waste stream optimization,
recycling rate analytics, remanufacturing assessment, circular design scoring,
industrial symbiosis matching, and EPR tracking.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums & Constants
# ---------------------------------------------------------------------------

class MaterialType(Enum):
    """Material categories for flow analysis."""
    STEEL = "steel"
    ALUMINUM = "aluminum"
    COPPER = "copper"
    PLASTIC = "plastic"
    GLASS = "glass"
    PAPER = "paper"
    WOOD = "wood"
    RARE_EARTH = "rare_earth"
    CONCRETE = "concrete"
    ELECTRONICS = "electronics"
    TEXTILE = "textile"
    ORGANIC = "organic"


class EndOfLifePathway(Enum):
    """How a product reaches end of life."""
    REUSE = "reuse"
    REFURBISH = "refurbish"
    REMANUFACTURE = "remanufacture"
    RECYCLE = "recycle"
    ENERGY_RECOVERY = "energy_recovery"
    LANDFILL = "landfill"
    INCINERATION = "incineration"


class DesignScoreCategory(Enum):
    """Circular design scoring criteria."""
    DURABILITY = "durability"
    REPAIRABILITY = "repairability"
    RECYCLABILITY = "recyclability"
    RECYCLED_CONTENT = "recycled_content"
    TOXIC_FREE = "toxic_free"
    MODULARITY = "modularity"
    DISASSEMBLY_EASE = "disassembly_ease"
    MATERIAL_DIVERSITY = "material_diversity"


class ConditionGrade(Enum):
    """Product condition assessment grades."""
    LIKE_NEW = "like_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    SCRAP = "scrap"


class EPRJurisdiction(Enum):
    """Extended Producer Responsibility jurisdictions."""
    EU = "eu"
    USA_CALIFORNIA = "usa_california"
    USA_MAINE = "usa_maine"
    JAPAN = "japan"
    SOUTH_KOREA = "south_korea"
    CANADA = "canada"
    UK = "uk"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class MaterialInput:
    """A material input to a system."""
    material: str
    tonnes: float
    source: str  # primary_extraction, recycled, reused
    cost_per_tonne: float = 0.0
    region: str = ""

    @property
    def total_cost(self) -> float:
        return self.tonnes * self.cost_per_tonne

    @property
    def is_recycled_input(self) -> bool:
        return self.source.lower() in ("recycled", "reused", "secondary")


@dataclass
class MaterialOutput:
    """A material output from a system."""
    material: str
    tonnes: float
    destination: str  # market, recycler, landfill, export
    value_per_tonne: float = 0.0

    @property
    def total_value(self) -> float:
        return self.tonnes * self.value_per_tonne

    @property
    def is_circular_output(self) -> bool:
        return self.destination.lower() in ("recycler", "reuse", "remanufacture")


@dataclass
class ProcessStep:
    """A transformation process in the material flow."""
    name: str
    input_materials: list[str]
    output_materials: list[str]
    efficiency: float = 0.95  # Material efficiency (fraction of input preserved)
    energy_kwh_per_tonne: float = 0.0
    waste_generated_tonnes: float = 0.0


@dataclass
class MFAReport:
    """Results of a Material Flow Analysis."""
    system_name: str
    total_input_tonnes: float
    product_output_tonnes: float
    recycled_output_tonnes: float
    waste_to_landfill_tonnes: float
    circularity_rate: float
    material_efficiency: float
    recycled_input_fraction: float
    losses_by_process: dict[str, float]

    @property
    def landfill_diversion_rate(self) -> float:
        if self.total_input_tonnes <= 0:
            return 0.0
        return 1.0 - self.waste_to_landfill_tonnes / self.total_input_tonnes


@dataclass
class WasteStream:
    """A waste stream from a facility or process."""
    name: str
    material_type: str
    tonnes: float
    recyclable: bool
    value_per_tonne: float = 0.0
    disposal_cost_per_tonne: float = 0.0
    contamination_percent: float = 0.0

    @property
    def net_value(self) -> float:
        if self.recyclable:
            return self.tonnes * self.value_per_tonne
        return -self.tonnes * self.disposal_cost_per_tonne


@dataclass
class WasteOptimizationPlan:
    """Results of waste stream optimization."""
    diversion_rate: float
    net_revenue_usd: float
    landfill_reduction_tonnes: float
    total_waste_tonnes: float
    recommendations: list[str]
    by_stream: dict[str, float]


@dataclass
class LifecycleSummary:
    """Summary of a product's lifecycle environmental impact."""
    product_id: str
    total_co2_kg: float
    total_material_kg: float
    total_waste_kg: float
    end_of_life_recyclable_percent: float
    stages: list[dict]

    @property
    def co2_per_year(self) -> float:
        use_years = max(1, sum(s.get("duration_years", 1) for s in self.stages))
        return self.total_co2_kg / use_years


@dataclass
class RemanufacturingScore:
    """Feasibility assessment for remanufacturing a product."""
    product_type: str
    feasibility_score: float
    recommendation: str
    economic_viability: bool
    technical_viability: bool
    estimated_profit_usd: float
    factors: dict[str, float]

    @property
    def grade(self) -> str:
        if self.feasibility_score >= 80:
            return "A - Highly Recommended"
        elif self.feasibility_score >= 60:
            return "B - Recommended"
        elif self.feasibility_score >= 40:
            return "C - Feasible with Improvements"
        elif self.feasibility_score >= 20:
            return "D - Marginal"
        return "F - Not Recommended"


@dataclass
class DesignScore:
    """Circular design score for a product."""
    product_name: str
    total_score: float
    category_scores: dict[str, float]
    rating: str
    recommendations: list[str]


@dataclass
class SymbiosisMatch:
    """A matched industrial symbiosis opportunity."""
    provider: str
    seeker: str
    material_type: str
    quantity: float
    unit: str
    distance_km: float
    annual_value_usd: float
    feasibility_score: float


@dataclass
class EPRObligation:
    """Extended Producer Responsibility obligation for a product."""
    product_id: str
    jurisdiction: EPRJurisdiction
    material_type: str
    weight_kg: float
    fee_per_kg: float
    reporting_deadline: str
    compliance_status: str = "pending"

    @property
    def total_fee(self) -> float:
        return self.weight_kg * self.fee_per_kg


# ---------------------------------------------------------------------------
# Material Flow Analyzer
# ---------------------------------------------------------------------------

class MaterialFlowAnalyzer:
    """
    Tracks and analyzes material flows through a system (factory, product,
    or economy) to calculate circularity metrics and identify losses.
    """

    def __init__(self, system: str = "System"):
        self.system_name = system
        self._inputs: list[MaterialInput] = []
        self._outputs: list[MaterialOutput] = []
        self._processes: list[ProcessStep] = []

    def add_input(self, material: str, tonnes: float, source: str, cost_per_tonne: float = 0.0) -> MaterialInput:
        """Record a material input."""
        inp = MaterialInput(material=material, tonnes=tonnes, source=source, cost_per_tonne=cost_per_tonne)
        self._inputs.append(inp)
        return inp

    def add_output(self, material: str, tonnes: float, destination: str, value_per_tonne: float = 0.0) -> MaterialOutput:
        """Record a material output."""
        out = MaterialOutput(material=material, tonnes=tonnes, destination=destination, value_per_tonne=value_per_tonne)
        self._outputs.append(out)
        return out

    def add_process(
        self,
        name: str,
        input_materials: list[str],
        output_materials: list[str],
        efficiency: float = 0.95,
        energy_kwh_per_tonne: float = 0.0
    ) -> ProcessStep:
        """Add a transformation process."""
        proc = ProcessStep(
            name=name,
            input_materials=input_materials,
            output_materials=output_materials,
            efficiency=efficiency,
            energy_kwh_per_tonne=energy_kwh_per_tonne
        )
        self._processes.append(proc)
        return proc

    def analyze(self) -> MFAReport:
        """Analyze material flows and calculate circularity metrics."""
        total_input = sum(i.tonnes for i in self._inputs)
        recycled_input = sum(i.tonnes for i in self._inputs if i.is_recycled_input)
        recycled_fraction = recycled_input / total_input if total_input > 0 else 0

        product_output = sum(o.tonnes for o in self._outputs if o.destination == "market")
        recycled_output = sum(o.tonnes for o in self._outputs if o.is_circular_output)
        waste_to_landfill = sum(o.tonnes for o in self._outputs if o.destination == "landfill")

        # Circularity rate (Ellen MacArthur definition simplified)
        if total_input > 0:
            circularity = (recycled_input + recycled_output) / (total_input + product_output) if (total_input + product_output) > 0 else 0
        else:
            circularity = 0.0

        # Material efficiency
        material_efficiency = product_output / total_input if total_input > 0 else 0

        # Losses by process
        losses = {}
        for proc in self._processes:
            total_proc_input = sum(
                i.tonnes for i in self._inputs if i.material in proc.input_materials
            )
            losses[proc.name] = round(total_proc_input * (1 - proc.efficiency), 2)

        return MFAReport(
            system_name=self.system_name,
            total_input_tonnes=round(total_input, 2),
            product_output_tonnes=round(product_output, 2),
            recycled_output_tonnes=round(recycled_output, 2),
            waste_to_landfill_tonnes=round(waste_to_landfill, 2),
            circularity_rate=round(min(1.0, circularity), 3),
            material_efficiency=round(min(1.0, material_efficiency), 3),
            recycled_input_fraction=round(recycled_fraction, 3),
            losses_by_process=losses
        )


# ---------------------------------------------------------------------------
# Waste Stream Optimizer
# ---------------------------------------------------------------------------

class WasteOptimizer:
    """
    Analyzes waste streams and identifies optimization opportunities
    to maximize diversion, revenue, and minimize environmental impact.
    """

    def __init__(self, facility: str = "Facility"):
        self.facility = facility
        self._streams: list[WasteStream] = []

    def add_waste_stream(
        self,
        name: str,
        tonnes: float,
        recyclable: bool,
        value_per_tonne: float = 0.0,
        disposal_cost_per_tonne: float = 50.0,
        material_type: str = "mixed",
        contamination_percent: float = 0.0
    ) -> WasteStream:
        """Add a waste stream to the analysis."""
        stream = WasteStream(
            name=name,
            material_type=material_type,
            tonnes=tonnes,
            recyclable=recyclable,
            value_per_tonne=value_per_tonne,
            disposal_cost_per_tonne=disposal_cost_per_tonne,
            contamination_percent=contamination_percent
        )
        self._streams.append(stream)
        return stream

    def optimize(self) -> WasteOptimizationPlan:
        """Optimize waste streams for maximum diversion and value."""
        total_waste = sum(s.tonnes for s in self._streams)
        recyclable_tonnes = sum(s.tonnes for s in self._streams if s.recyclable)
        landfill_tonnes = sum(s.tonnes for s in self._streams if not s.recyclable)

        # Calculate economics
        recycling_revenue = sum(s.net_value for s in self._streams if s.recyclable)
        disposal_costs = sum(-s.net_value for s in self._streams if not s.recyclable)
        net_revenue = recycling_revenue - disposal_costs

        diversion_rate = recyclable_tonnes / total_waste if total_waste > 0 else 0

        # Generate recommendations
        recommendations = []
        for s in self._streams:
            if s.contamination_percent > 20:
                recommendations.append(
                    f"{s.name}: High contamination ({s.contamination_percent:.0f}%). "
                    f"Implement source separation to improve recyclate quality."
                )
            if not s.recyclable and s.tonnes > 10:
                recommendations.append(
                    f"{s.name}: {s.tonnes:.0f} tonnes going to landfill. "
                    f"Investigate alternative materials or take-back programs."
                )
        if diversion_rate < 0.7:
            recommendations.append(
                f"Overall diversion rate ({diversion_rate:.0%}) is below 70% target. "
                f"Prioritize the largest waste streams for recycling."
            )

        by_stream = {s.name: round(s.tonnes, 2) for s in self._streams}

        return WasteOptimizationPlan(
            diversion_rate=round(diversion_rate, 3),
            net_revenue_usd=round(net_revenue, 2),
            landfill_reduction_tonnes=round(recyclable_tonnes, 2),
            total_waste_tonnes=round(total_waste, 2),
            recommendations=recommendations,
            by_stream=by_stream
        )


# ---------------------------------------------------------------------------
# Product Lifecycle Tracker
# ---------------------------------------------------------------------------

class LifecycleTracker:
    """Tracks material and environmental flows through a product's lifecycle."""

    def __init__(self, product_id: str = ""):
        self.product_id = product_id
        self._stages: list[dict] = []

    def add_stage(
        self,
        stage_name: str,
        materials: dict[str, float] | None = None,
        co2_kg: float = 0.0,
        waste_generated_kg: float = 0.0,
        duration_years: float = 0.0,
        recyclable_percent: float = 0.0,
        maintenance_kg: float = 0.0
    ) -> None:
        """Add a lifecycle stage with its impacts."""
        self._stages.append({
            "stage": stage_name,
            "materials": materials or {},
            "co2_kg": co2_kg,
            "waste_kg": waste_generated_kg,
            "duration_years": duration_years,
            "recyclable_percent": recyclable_percent,
            "maintenance_kg": maintenance_kg
        })

    def summarize(self) -> LifecycleSummary:
        """Generate lifecycle impact summary."""
        total_co2 = sum(s["co2_kg"] for s in self._stages)
        total_material = sum(sum(s["materials"].values()) for s in self._stages)
        total_waste = sum(s["waste_kg"] + s["maintenance_kg"] for s in self._stages)
        eol_recyclable = next(
            (s["recyclable_percent"] for s in self._stages if s["recyclable_percent"] > 0),
            0.0
        )

        return LifecycleSummary(
            product_id=self.product_id,
            total_co2_kg=round(total_co2, 2),
            total_material_kg=round(total_material, 2),
            total_waste_kg=round(total_waste, 2),
            end_of_life_recyclable_percent=round(eol_recyclable, 1),
            stages=self._stages
        )


# ---------------------------------------------------------------------------
# Remanufacturing Assessor
# ---------------------------------------------------------------------------

class RemanufacturingAssessor:
    """Evaluates products for remanufacturing feasibility."""

    # Scoring weights
    WEIGHTS = {
        "economic": 35.0,
        "technical": 30.0,
        "environmental": 20.0,
        "logistical": 15.0
    }

    def assess(
        self,
        product_type: str,
        age_years: float,
        condition: str,
        material_value_usd: float,
        remanufacturing_cost_usd: float,
        new_product_cost_usd: float,
        return_rate_percent: float = 30.0,
        disassembly_difficulty: str = "moderate"
    ) -> RemanufacturingScore:
        """Assess remanufacturing feasibility."""
        # Economic score
        cost_ratio = remanufacturing_cost_usd / new_product_cost_usd if new_product_cost_usd > 0 else 1.0
        economic = max(0, min(100, (1 - cost_ratio) * 100 + (return_rate_percent - 20)))

        # Technical score (condition-based)
        condition_scores = {
            "like_new": 95, "good": 75, "fair": 50, "poor": 25, "scrap": 5
        }
        difficulty_scores = {"easy": 100, "moderate": 70, "difficult": 40, "impossible": 10}
        technical = (condition_scores.get(condition, 50) + difficulty_scores.get(disassembly_difficulty, 50)) / 2

        # Environmental score (based on material value recovery)
        env_score = min(100, material_value_usd / new_product_cost_usd * 200) if new_product_cost_usd > 0 else 50

        # Logistical score (age and return rate)
        log_score = max(0, 100 - age_years * 10) * (return_rate_percent / 100)

        # Weighted total
        total = (
            economic * self.WEIGHTS["economic"] / 100 +
            technical * self.WEIGHTS["technical"] / 100 +
            env_score * self.WEIGHTS["environmental"] / 100 +
            log_score * self.WEIGHTS["logistical"] / 100
        )

        profit = new_product_cost_usd - remanufacturing_cost_usd
        viable = total >= 50 and profit > 0

        recommendation = (
            "Strongly recommended" if total >= 75 else
            "Recommended" if total >= 55 else
            "Feasible with improvements" if total >= 35 else
            "Marginal" if total >= 20 else
            "Not recommended"
        )

        return RemanufacturingScore(
            product_type=product_type,
            feasibility_score=round(total, 1),
            recommendation=recommendation,
            economic_viability=profit > 0,
            technical_viability=technical >= 50,
            estimated_profit_usd=round(profit, 2),
            factors={
                "economic": round(economic, 1),
                "technical": round(technical, 1),
                "environmental": round(env_score, 1),
                "logistical": round(log_score, 1)
            }
        )


# ---------------------------------------------------------------------------
# Circular Design Scorer
# ---------------------------------------------------------------------------

class CircularDesignScorer:
    """Scores products against circularity design criteria."""

    WEIGHTS = {
        "durability": 15.0,
        "repairability": 20.0,
        "recyclability": 20.0,
        "recycled_content": 15.0,
        "toxic_free": 15.0,
        "modularity": 10.0,
        "disassembly_ease": 5.0
    }

    def score_product(self, product: dict) -> DesignScore:
        """Score a product against circular design criteria."""
        category_scores = {}
        for category, weight in self.WEIGHTS.items():
            raw_score = product.get(category, 50)  # Default to 50 if not specified
            category_scores[category] = round(min(100, max(0, raw_score)), 1)

        total = sum(
            category_scores[cat] * self.WEIGHTS[cat] / 100
            for cat in self.WEIGHTS
        )

        # Rating
        if total >= 80:
            rating = "Platinum (C2C Certified)"
        elif total >= 65:
            rating = "Gold"
        elif total >= 50:
            rating = "Silver"
        elif total >= 35:
            rating = "Bronze"
        else:
            rating = "Below Standard"

        # Recommendations for weak areas
        recommendations = []
        for cat, score in category_scores.items():
            if score < 40:
                recommendations.append(
                    f"{cat.replace('_', ' ').title()} is weak ({score:.0f}/100). "
                    f"Prioritize improvement in this area."
                )

        return DesignScore(
            product_name=product.get("name", "Unknown"),
            total_score=round(total, 1),
            category_scores=category_scores,
            rating=rating,
            recommendations=recommendations
        )


# ---------------------------------------------------------------------------
# Industrial Symbiosis Matcher
# ---------------------------------------------------------------------------

class SymbiosisMatcher:
    """Matches waste stream providers with resource seekers."""

    def __init__(self):
        self._providers: list[dict] = []
        self._seekers: list[dict] = []

    def add_provider(self, name: str, waste_type: str, quantity: float, location: str, unit: str = "tonnes") -> None:
        self._providers.append({"name": name, "type": waste_type, "quantity": quantity,
                                "location": location, "unit": unit})

    def add_seeker(self, name: str, need_type: str, quantity: float, location: str, unit: str = "tonnes") -> None:
        self._seekers.append({"name": name, "type": need_type, "quantity": quantity,
                              "location": location, "unit": unit})

    def find_matches(self) -> list[SymbiosisMatch]:
        """Find matching provider-seeker pairs."""
        matches = []
        for provider in self._providers:
            for seeker in self._seekers:
                if provider["type"] == seeker["type"]:
                    matched_qty = min(provider["quantity"], seeker["quantity"])
                    distance = abs(hash(provider["location"]) % 50)  # Simplified distance

                    # Feasibility based on quantity match and distance
                    qty_match = matched_qty / max(provider["quantity"], seeker["quantity"])
                    distance_score = max(0, 100 - distance * 2)
                    feasibility = (qty_match * 60 + distance_score * 0.4)

                    # Rough value estimate
                    value = matched_qty * 50  # $50/tonne average

                    matches.append(SymbiosisMatch(
                        provider=provider["name"],
                        seeker=seeker["name"],
                        material_type=provider["type"],
                        quantity=round(matched_qty, 2),
                        unit=provider["unit"],
                        distance_km=distance,
                        annual_value_usd=round(value, 2),
                        feasibility_score=round(feasibility, 1)
                    ))

        return sorted(matches, key=lambda m: m.feasibility_score, reverse=True)


# ---------------------------------------------------------------------------
# EPR Tracker
# ---------------------------------------------------------------------------

class EPRTracker:
    """Manages Extended Producer Responsibility obligations."""

    # EPR fee rates (EUR/kg) by material type
    DEFAULT_FEES = {
        "plastic": 0.85,
        "aluminum": 0.12,
        "steel": 0.08,
        "glass": 0.05,
        "paper": 0.03,
        "electronics": 2.50,
        "batteries": 4.00,
        "textiles": 0.20,
    }

    def __init__(self):
        self._obligations: list[EPRObligation] = []
        self._reporting: list[dict] = []

    def register_obligation(
        self,
        product_id: str,
        jurisdiction: str,
        material_type: str,
        weight_kg: float,
        fee_per_kg: Optional[float] = None
    ) -> EPRObligation:
        """Register an EPR obligation for a product."""
        fee = fee_per_kg if fee_per_kg is not None else self.DEFAULT_FEES.get(material_type, 0.50)
        obligation = EPRObligation(
            product_id=product_id,
            jurisdiction=EPRJurisdiction(jurisdiction),
            material_type=material_type,
            weight_kg=weight_kg,
            fee_per_kg=fee,
            reporting_deadline="2026-03-31"
        )
        self._obligations.append(obligation)
        return obligation

    def total_fees(self, jurisdiction: Optional[str] = None) -> float:
        """Calculate total EPR fees."""
        obs = self._obligations
        if jurisdiction:
            obs = [o for o in obs if o.jurisdiction.value == jurisdiction]
        return sum(o.total_fee for o in obs)

    def compliance_summary(self) -> dict:
        """Summary of EPR compliance status."""
        by_jurisdiction = {}
        for obs in self._obligations:
            j = obs.jurisdiction.value
            if j not in by_jurisdiction:
                by_jurisdiction[j] = {"obligations": 0, "total_fee": 0.0, "weight_kg": 0.0}
            by_jurisdiction[j]["obligations"] += 1
            by_jurisdiction[j]["total_fee"] += obs.total_fee
            by_jurisdiction[j]["weight_kg"] += obs.weight_kg

        return {
            "total_obligations": len(self._obligations),
            "total_fees_usd": round(self.total_fees(), 2),
            "total_weight_kg": round(sum(o.weight_kg for o in self._obligations), 2),
            "by_jurisdiction": {
                k: {kk: round(vv, 2) if isinstance(vv, float) else vv
                    for kk, vv in v.items()}
                for k, v in by_jurisdiction.items()
            }
        }


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main():
    """Demonstrate Circular Economy module capabilities."""
    print("=" * 60)
    print("Circular Economy Module Demo")
    print("=" * 60)

    # 1. Material Flow Analysis
    print("\n--- Material Flow Analysis ---")
    mfa = MaterialFlowAnalyzer("Widget Manufacturing")
    mfa.add_input("steel", 500, "primary_extraction", 800)
    mfa.add_input("aluminum", 120, "primary_extraction", 2200)
    mfa.add_input("plastic", 80, "recycled", 600)
    mfa.add_process("stamping", ["steel"], ["steel_parts", "steel_scrap"], efficiency=0.81)
    mfa.add_process("assembly", ["steel_parts", "aluminum", "plastic"], ["widget"], efficiency=0.95)
    mfa.add_output("widget", 400, "market", 5000)
    mfa.add_output("steel_scrap", 95, "recycler", 150)
    mfa.add_output("aluminum_scrap", 18, "recycler", 1200)
    mfa.add_output("waste", 12, "landfill")

    report = mfa.analyze()
    print(f"  Total input: {report.total_input_tonnes:.0f} tonnes")
    print(f"  Product output: {report.product_output_tonnes:.0f} tonnes")
    print(f"  Recycled output: {report.recycled_output_tonnes:.0f} tonnes")
    print(f"  Circularity rate: {report.circularity_rate:.1%}")
    print(f"  Material efficiency: {report.material_efficiency:.1%}")
    print(f"  Recycled input: {report.recycled_input_fraction:.1%}")

    # 2. Waste Stream Optimization
    print("\n--- Waste Stream Optimization ---")
    optimizer = WasteOptimizer("Assembly Plant")
    optimizer.add_waste_stream("steel_scrap", 95, True, 150, material_type="steel")
    optimizer.add_waste_stream("plastic_waste", 25, True, 80, material_type="plastic", contamination_percent=15)
    optimizer.add_waste_stream("mixed_metal", 12, True, 200)
    optimizer.add_waste_stream("packaging", 15, True, 20)
    optimizer.add_waste_stream("hazardous", 3, False, disposal_cost_per_tonne=500)

    plan = optimizer.optimize()
    print(f"  Diversion rate: {plan.diversion_rate:.1%}")
    print(f"  Net revenue: ${plan.net_revenue_usd:,.2f}")
    print(f"  Landfill reduction: {plan.landfill_reduction_tonnes:.1f} tonnes")
    for rec in plan.recommendations[:2]:
        print(f"  > {rec}")

    # 3. Product Lifecycle
    print("\n--- Product Lifecycle ---")
    tracker = LifecycleTracker("WIDGET-100")
    tracker.add_stage("extraction", {"steel": 12.5, "aluminum": 3.0, "plastic": 2.0}, co2_kg=45.0)
    tracker.add_stage("manufacturing", co2_kg=15.0, waste_generated_kg=1.8)
    tracker.add_stage("use", duration_years=5, co2_kg=2.0, maintenance_kg=0.5)
    tracker.add_stage("end_of_life", recyclable_percent=78.0, co2_kg=3.0)
    lifecycle = tracker.summarize()
    print(f"  Total CO2: {lifecycle.total_co2_kg:.1f} kg")
    print(f"  Total material: {lifecycle.total_material_kg:.1f} kg")
    print(f"  Recyclability: {lifecycle.end_of_life_recyclable_percent:.0f}%")

    # 4. Remanufacturing Assessment
    print("\n--- Remanufacturing Assessment ---")
    assessor = RemanufacturingAssessor()
    score = assessor.assess(
        product_type="industrial_pump", age_years=3, condition="good",
        material_value_usd=120, remanufacturing_cost_usd=85, new_product_cost_usd=450
    )
    print(f"  Score: {score.feasibility_score:.1f}/100 ({score.grade})")
    print(f"  Profit: ${score.estimated_profit_usd:.2f}")
    print(f"  Viable: economic={score.economic_viability}, technical={score.technical_viability}")

    # 5. Circular Design Scoring
    print("\n--- Circular Design Scoring ---")
    scorer = CircularDesignScorer()
    design_scores = [
        {"name": "Product A", "durability": 85, "repairability": 90, "recyclability": 80,
         "recycled_content": 40, "toxic_free": 95, "modularity": 75, "disassembly_ease": 85},
        {"name": "Product B", "durability": 50, "repairability": 30, "recyclability": 60,
         "recycled_content": 20, "toxic_free": 70, "modularity": 40, "disassembly_ease": 35},
    ]
    for product in design_scores:
        ds = scorer.score_product(product)
        print(f"  {ds.product_name}: {ds.total_score:.1f}/100 ({ds.rating})")

    # 6. Industrial Symbiosis
    print("\n--- Industrial Symbiosis Matching ---")
    matcher = SymbiosisMatcher()
    matcher.add_provider("Steel Mill", "waste_heat", 500, "Industrial Zone A", "MWh")
    matcher.add_provider("Chemical Plant", "steam", 300, "Industrial Zone A", "tonnes")
    matcher.add_seeker("Food Processor", "waste_heat", 200, "Industrial Zone A", "MWh")
    matcher.add_seeker("Paper Mill", "steam", 250, "Industrial Zone A", "tonnes")
    matches = matcher.find_matches()
    for m in matches:
        print(f"  {m.provider} -> {m.seeker}: {m.material_type} ({m.quantity} {m.unit}) "
              f"[score: {m.feasibility_score:.0f}]")

    # 7. EPR Tracking
    print("\n--- EPR Compliance ---")
    epr = EPRTracker()
    epr.register_obligation("PROD-001", "eu", "plastic", 15.0)
    epr.register_obligation("PROD-002", "eu", "electronics", 5.0)
    epr.register_obligation("PROD-003", "usa_california", "electronics", 3.0)
    summary = epr.compliance_summary()
    print(f"  Total obligations: {summary['total_obligations']}")
    print(f"  Total fees: ${summary['total_fees_usd']:.2f}")
    for j, data in summary['by_jurisdiction'].items():
        print(f"  {j}: {data['obligations']} products, ${data['total_fee']:.2f}")

    print("\n" + "=" * 60)
    print("Demo complete.")


if __name__ == "__main__":
    main()
