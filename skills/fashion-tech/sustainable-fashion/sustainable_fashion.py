"""
Sustainable Fashion Module
Part of the fashion-tech skill domain

Provides carbon footprint calculation, material sustainability scoring,
circular economy management, supply chain traceability, and ESG reporting
for the fashion industry.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
import hashlib
import json
import statistics


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EmissionScope(Enum):
    SCOPE_1 = "scope_1_direct"
    SCOPE_2 = "scope_2_energy"
    SCOPE_3 = "scope_3_supply_chain"


class MaterialCategory(Enum):
    NATURAL = "natural"
    SYNTHETIC = "synthetic"
    RECYCLED = "recycled"
    BIOBASED = "biobased"
    CELLULOSIC = "cellulosic"


class CircularChannel(Enum):
    RESALE = "resale"
    RENTAL = "rental"
    REPAIR = "repair"
    RECYCLING = "recycling"
    UPCYCLING = "upcycling"
    COMPOSTING = "composting"


class TraceStage(Enum):
    RAW_MATERIAL = "raw_material"
    SPINNING = "spinning"
    WEAVING = "weaving"
    DYEING = "dyeing"
    CUT_MAKE_TRIM = "cut_make_trim"
    FINISHING = "finishing"
    WAREHOUSE = "warehouse"
    RETAIL = "retail"
    CONSUMER = "consumer"
    END_OF_LIFE = "end_of_life"


class ProgramType(Enum):
    TAKE_BACK = "take_back"
    RENTAL = "rental"
    REPAIR = "repair"
    RESALE = "resale"


class ItemCondition(Enum):
    NEW = "new"
    LIKE_NEW = "like_new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class ReportFramework(Enum):
    GRI = "gri"
    SASB = "sasb"
    EU_CSRD = "eu_csrd"
    CDP = "cdp"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class MaterialInput:
    """A material input for carbon footprint calculation."""
    material_type: str
    weight_kg: float
    origin: str
    certifications: List[str] = field(default_factory=list)


@dataclass
class CarbonFootprint:
    """Carbon footprint calculation result."""
    product_id: str
    total_kg_co2e: float
    breakdown: Dict[str, float]
    vs_category_avg: float
    data_quality: float
    methodology: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def rating(self) -> str:
        if self.total_kg_co2e < 5:
            return "A"
        if self.total_kg_co2e < 10:
            return "B"
        if self.total_kg_co2e < 20:
            return "C"
        if self.total_kg_co2e < 35:
            return "D"
        return "F"


@dataclass
class MaterialScore:
    """Sustainability score for a material."""
    name: str
    overall: int
    water_score: int
    carbon_score: int
    chemical_score: int
    biodiversity_score: int
    social_score: int
    certifications: List[str] = field(default_factory=list)


@dataclass
class CircularItem:
    """An item registered in a circular economy program."""
    item_id: str
    product_id: str
    condition: ItemCondition
    customer_id: str
    registered_date: str
    estimated_value: float = 0.0


@dataclass
class RoutingDecision:
    """Decision on how to route a returned circular item."""
    item_id: str
    channel: CircularChannel
    action: str
    resale_value: float
    estimated_lifespan_extension_months: int


@dataclass
class TraceRecord:
    """A single traceability record in the supply chain."""
    stage: TraceStage
    details: Dict[str, Any]
    certification: Optional[str]
    location: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TraceChain:
    """Complete traceability chain for a product."""
    product_id: str
    stages: List[TraceRecord]
    is_verified: bool
    origin: str
    blockchain_tx: Optional[str] = None


@dataclass
class ESGReport:
    """ESG sustainability report."""
    framework: ReportFramework
    reporting_period: str
    total_products_assessed: int
    avg_carbon_footprint: float
    circular_program_metrics: Dict[str, Any]
    compliance_status: str
    generated_date: str = field(default_factory=lambda: datetime.now().isoformat())


# ---------------------------------------------------------------------------
# Carbon Footprint Calculator
# ---------------------------------------------------------------------------

class CarbonFootprintCalculator:
    """Calculates product-level carbon footprints using LCA methodology."""

    # Emission factors (kg CO2e per unit)
    EMISSION_FACTORS = {
        "organic_cotton": 5.5,
        "conventional_cotton": 8.0,
        "recycled_polyester": 2.1,
        "virgin_polyester": 5.5,
        "nylon": 7.6,
        "recycled_nylon": 3.8,
        "wool": 17.0,
        "silk": 20.0,
        "linen": 1.7,
        "hemp": 1.6,
        "tencel": 1.5,
        "viscose": 4.5,
    }

    TRANSPORT_FACTORS = {
        "sea_freight": 0.01,    # kg CO2e per ton-km
        "air_freight": 0.50,
        "road_freight": 0.06,
        "rail_freight": 0.02,
    }

    def __init__(
        self,
        methodology: str = "GHG_PROTOCOL",
        boundaries: Optional[List[EmissionScope]] = None,
    ):
        self.methodology = methodology
        self.boundaries = boundaries or list(EmissionScope)

    def calculate_product(
        self,
        product_id: str,
        materials: List[Dict[str, Any]],
        manufacturing: Dict[str, Any],
        transport: Dict[str, Any],
        packaging: Optional[Dict[str, Any]] = None,
    ) -> CarbonFootprint:
        breakdown: Dict[str, float] = {}

        # Material emissions
        material_total = 0.0
        for mat in materials:
            factor = self.EMISSION_FACTORS.get(mat["type"], 5.0)
            material_total += factor * mat["weight_kg"]
        breakdown["materials"] = material_total

        # Manufacturing emissions
        energy_kwh = manufacturing.get("energy_kwh", 2.0)
        grid_factor = 0.5  # Simplified grid emission factor
        breakdown["manufacturing"] = energy_kwh * grid_factor

        # Transport emissions
        distance = transport.get("distance_km", 1000)
        mode = transport.get("mode", "sea_freight")
        tf = self.TRANSPORT_FACTORS.get(mode, 0.01)
        breakdown["transport"] = tf * distance * 0.001

        # Packaging
        if packaging:
            pkg_weight = packaging.get("weight_kg", 0.05)
            recycled = packaging.get("recycled_content", 0.0)
            breakdown["packaging"] = pkg_weight * 3.0 * (1 - recycled * 0.5)
        else:
            breakdown["packaging"] = 0.1

        total = sum(breakdown.values())
        category_avg = 12.5  # Industry average for dresses
        vs_avg = (total - category_avg) / category_avg

        return CarbonFootprint(
            product_id=product_id,
            total_kg_co2e=round(total, 2),
            breakdown={k: round(v, 2) for k, v in breakdown.items()},
            vs_category_avg=round(vs_avg, 2),
            data_quality=0.85,
            methodology=self.methodology,
        )


# ---------------------------------------------------------------------------
# Material Scorer
# ---------------------------------------------------------------------------

class MaterialScorer:
    """Scores materials on sustainability metrics."""

    MATERIAL_DATA = {
        "organic_cotton": {"overall": 72, "water": 60, "carbon": 75, "chemical": 85, "biodiversity": 65, "social": 70},
        "conventional_cotton": {"overall": 35, "water": 20, "carbon": 40, "chemical": 25, "biodiversity": 30, "social": 40},
        "recycled_polyester": {"overall": 68, "water": 80, "carbon": 70, "chemical": 65, "biodiversity": 55, "social": 60},
        "virgin_polyester": {"overall": 30, "water": 50, "carbon": 25, "chemical": 30, "biodiversity": 20, "social": 25},
        "linen": {"overall": 82, "water": 85, "carbon": 88, "chemical": 80, "biodiversity": 78, "social": 80},
        "hemp": {"overall": 85, "water": 90, "carbon": 90, "chemical": 82, "biodiversity": 80, "social": 78},
        "tencel": {"overall": 78, "water": 75, "carbon": 80, "chemical": 78, "biodiversity": 72, "social": 75},
    }

    def score(
        self,
        material: str,
        certifications: Optional[List[str]] = None,
        origin_country: str = "",
        process: str = "",
    ) -> MaterialScore:
        data = self.MATERIAL_DATA.get(material, {
            "overall": 50, "water": 50, "carbon": 50, "chemical": 50,
            "biodiversity": 50, "social": 50,
        })
        cert_bonus = len(certifications or []) * 3
        return MaterialScore(
            name=material,
            overall=min(data["overall"] + cert_bonus, 100),
            water_score=min(data["water"] + cert_bonus, 100),
            carbon_score=min(data["carbon"] + cert_bonus, 100),
            chemical_score=min(data["chemical"] + cert_bonus, 100),
            biodiversity_score=min(data["biodiversity"] + cert_bonus, 100),
            social_score=min(data["social"] + cert_bonus, 100),
            certifications=certifications or [],
        )

    def compare(self, materials: List[str]) -> List[MaterialScore]:
        return [self.score(m) for m in materials]


# ---------------------------------------------------------------------------
# Circular Economy Manager
# ---------------------------------------------------------------------------

class CircularEconomyManager:
    """Manages circular fashion programs (resale, rental, repair, take-back)."""

    def __init__(self, brand: str):
        self.brand = brand
        self._programs: Dict[str, Dict[str, Any]] = {}
        self._items: Dict[str, CircularItem] = {}
        self._routing_log: List[RoutingDecision] = []

    def create_program(
        self,
        program_type: ProgramType,
        incentive_type: str = "store_credit",
        credit_percentage: int = 15,
        accepted_conditions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        pid = f"PROG-{len(self._programs) + 1:04d}"
        program = {
            "program_id": pid,
            "type": program_type.value,
            "incentive": incentive_type,
            "credit_percentage": credit_percentage,
            "accepted_conditions": accepted_conditions or ["good", "fair"],
            "items_processed": 0,
            "active": True,
        }
        self._programs[pid] = program
        return program

    def register_return(
        self,
        product_id: str,
        condition: str,
        customer_id: str,
    ) -> CircularItem:
        item_id = f"CIR-{len(self._items) + 1:06d}"
        condition_enum = ItemCondition(condition)
        value_map = {
            ItemCondition.NEW: 45.0,
            ItemCondition.LIKE_NEW: 35.0,
            ItemCondition.GOOD: 25.0,
            ItemCondition.FAIR: 15.0,
            ItemCondition.POOR: 5.0,
        }
        item = CircularItem(
            item_id=item_id,
            product_id=product_id,
            condition=condition_enum,
            customer_id=customer_id,
            registered_date=datetime.now().isoformat(),
            estimated_value=value_map.get(condition_enum, 10.0),
        )
        self._items[item_id] = item
        return item

    def route_item(self, item: CircularItem) -> RoutingDecision:
        channel_map = {
            ItemCondition.NEW: CircularChannel.RESALE,
            ItemCondition.LIKE_NEW: CircularChannel.RESALE,
            ItemCondition.GOOD: CircularChannel.RENTAL,
            ItemCondition.FAIR: CircularChannel.REPAIR,
            ItemCondition.POOR: CircularChannel.RECYCLING,
        }
        channel = channel_map.get(item.condition, CircularChannel.RECYCLING)
        action_map = {
            CircularChannel.RESALE: "List on resale marketplace",
            CircularChannel.RENTAL: "Add to rental inventory",
            CircularChannel.REPAIR: "Route to repair workshop",
            CircularChannel.RECYCLING: "Send to textile recycling partner",
        }
        decision = RoutingDecision(
            item_id=item.item_id,
            channel=channel,
            action=action_map.get(channel, "Recycle"),
            resale_value=item.estimated_value,
            estimated_lifespan_extension_months={
                CircularChannel.RESALE: 12,
                CircularChannel.RENTAL: 24,
                CircularChannel.REPAIR: 18,
                CircularChannel.RECYCLING: 0,
            }.get(channel, 0),
        )
        self._routing_log.append(decision)
        return decision

    def get_program_stats(self) -> Dict[str, Any]:
        items = list(self._items.values())
        return {
            "total_items": len(items),
            "total_value": sum(i.estimated_value for i in items),
            "by_condition": {
                c.value: sum(1 for i in items if i.condition == c)
                for c in ItemCondition
            },
        }


# ---------------------------------------------------------------------------
# Traceability Tracker
# ---------------------------------------------------------------------------

class TraceabilityTracker:
    """Blockchain-backed supply chain traceability system."""

    def __init__(self, blockchain_enabled: bool = False):
        self.blockchain_enabled = blockchain_enabled
        self._chains: Dict[str, List[TraceRecord]] = {}
        self._tx_counter = 0

    def record(
        self,
        product_id: str,
        stage: str,
        details: Dict[str, Any],
        certification: Optional[str] = None,
        location: str = "",
    ) -> TraceRecord:
        record = TraceRecord(
            stage=TraceStage(stage),
            details=details,
            certification=certification,
            location=location,
        )
        self._chains.setdefault(product_id, []).append(record)
        if self.blockchain_enabled:
            self._tx_counter += 1
        return record

    def verify(self, product_id: str) -> TraceChain:
        stages = self._chains.get(product_id, [])
        expected_stages = {s.value for s in TraceStage}
        recorded_stages = {r.stage.value for r in stages}
        is_verified = expected_stages.issubset(recorded_stages)
        origin = stages[0].location if stages else "Unknown"

        tx = None
        if self.blockchain_enabled and stages:
            data = json.dumps([r.stage.value for r in stages])
            tx = hashlib.sha256(data.encode()).hexdigest()[:16]

        return TraceChain(
            product_id=product_id,
            stages=stages,
            is_verified=is_verified,
            origin=origin,
            blockchain_tx=tx,
        )


# ---------------------------------------------------------------------------
# ESG Reporter
# ---------------------------------------------------------------------------

class ESGReporter:
    """Generates ESG sustainability reports."""

    def __init__(self, brand: str, frameworks: Optional[List[ReportFramework]] = None):
        self.brand = brand
        self.frameworks = frameworks or [ReportFramework.GRI]

    def generate(
        self,
        products: List[CarbonFootprint],
        circular_stats: Dict[str, Any],
        reporting_period: str = "2025-Q4",
    ) -> ESGReport:
        avg_cf = statistics.mean([p.total_kg_co2e for p in products]) if products else 0
        compliant_count = sum(1 for p in products if p.rating in ("A", "B"))

        return ESGReport(
            framework=self.frameworks[0],
            reporting_period=reporting_period,
            total_products_assessed=len(products),
            avg_carbon_footprint=round(avg_cf, 2),
            circular_program_metrics=circular_stats,
            compliance_status=f"{compliant_count}/{len(products)} products meet targets",
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Sustainable Fashion Technology Demo")
    print("=" * 60)

    # Carbon footprint
    print("\n--- Carbon Footprint Calculation ---")
    calc = CarbonFootprintCalculator(methodology="GHG_PROTOCOL")
    fp = calc.calculate_product(
        product_id="DRESS-001",
        materials=[
            {"type": "organic_cotton", "weight_kg": 0.3, "origin": "India"},
            {"type": "recycled_polyester", "weight_kg": 0.1, "origin": "Taiwan"},
        ],
        manufacturing={"energy_kwh": 2.5, "country": "Vietnam"},
        transport={"distance_km": 12000, "mode": "sea_freight"},
        packaging={"weight_kg": 0.05, "recycled_content": 0.8},
    )
    print(f"  Product: {fp.product_id}")
    print(f"  Total: {fp.total_kg_co2e} kg CO2e ({fp.rating})")
    print(f"  Breakdown: {fp.breakdown}")
    print(f"  vs Category Avg: {fp.vs_category_avg:+.1%}")

    # Material scoring
    print("\n--- Material Sustainability Scoring ---")
    scorer = MaterialScorer()
    for mat in ["organic_cotton", "conventional_cotton", "linen", "hemp"]:
        score = scorer.score(mat, certifications=["GOTS"] if "organic" in mat else [])
        print(f"  {mat}: {score.overall}/100 (water={score.water_score}, carbon={score.carbon_score})")

    # Circular economy
    print("\n--- Circular Economy Program ---")
    circular = CircularEconomyManager(brand="EcoWear")
    prog = circular.create_program(ProgramType.TAKE_BACK, credit_percentage=15)
    print(f"  Program: {prog['program_id']} ({prog['type']})")

    item = circular.register_return("DRESS-001", "good", "CUST-12345")
    routing = circular.route_item(item)
    print(f"  Item {item.item_id}: condition={item.condition.value}, value=${item.estimated_value}")
    print(f"  Route: {routing.channel.value} - {routing.action}")

    # Traceability
    print("\n--- Supply Chain Traceability ---")
    tracker = TraceabilityTracker(blockchain_enabled=True)
    tracker.record("DRESS-001", "raw_material", {"farm": "Gujarat Farm"}, "GOTS", "India")
    tracker.record("DRESS-001", "spinning", {"mill": "EcoSpin"}, None, "India")
    tracker.record("DRESS-001", "dyeing", {"process": "low-water"}, "ZDHC", "Vietnam")
    chain = tracker.verify("DRESS-001")
    print(f"  Stages: {len(chain.stages)}, Verified: {chain.is_verified}")
    print(f"  Origin: {chain.origin}, Blockchain TX: {chain.blockchain_tx}")

    # ESG Report
    print("\n--- ESG Report ---")
    reporter = ESGReporter(brand="EcoWear")
    report = reporter.generate([fp], circular.get_program_stats())
    print(f"  Framework: {report.framework.value}")
    print(f"  Products assessed: {report.total_products_assessed}")
    print(f"  Avg carbon: {report.avg_carbon_footprint} kg CO2e")
    print(f"  Compliance: {report.compliance_status}")


if __name__ == "__main__":
    main()
