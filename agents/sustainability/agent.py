#!/usr/bin/env python3
"""
Grok Sustainability Agent
Comprehensive sustainability management platform covering carbon tracking,
ESG reporting, circular economy, green supply chain, and regulatory compliance.
"""

from __future__ import annotations

import logging
import math
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import (
    Any,
    Dict,
    Generator,
    List,
    NamedTuple,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SustainabilityCategory(Enum):
    ENERGY = "energy"
    WATER = "water"
    WASTE = "waste"
    TRANSPORTATION = "transportation"
    SUPPLY_CHAIN = "supply_chain"
    BUILDING = "building"
    PRODUCT = "product"
    BIODIVERSITY = "biodiversity"
    SOCIAL_IMPACT = "social_impact"
    GOVERNANCE = "governance"


class CarbonScope(Enum):
    SCOPE_1 = "scope_1"  # Direct emissions
    SCOPE_2 = "scope_2"  # Indirect from purchased energy
    SCOPE_3 = "scope_3"  # Value chain emissions


class InitiativeStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class ComplianceFramework(Enum):
    GRI = "gri"                    # Global Reporting Initiative
    SASB = "sasb"                  # Sustainability Accounting Standards Board
    CDP = "cdp"                    # Carbon Disclosure Project
    TCFD = "tcfd"                  # Task Force on Climate-related Financial Disclosures
    EU_CSRD = "eu_csrd"            # EU Corporate Sustainability Reporting Directive
    ISSB = "issb"                  # International Sustainability Standards Board
    ISO_14001 = "iso_14001"       # Environmental Management System
    UN_SDGS = "un_sdgs"           # UN Sustainable Development Goals


class CertificationType(Enum):
    ISO_14001 = "iso_14001"
    ISO_50001 = "iso_50001"
    LEED = "leed"
    ENERGY_STAR = "energy_star"
    B_CORP = "b_corp"
    CARBON_NEUTRAL = "carbon_neutral"
    SCIENCE_BASED_TARGETS = "science_based_targets"


class CircularEconomyPhase(Enum):
    DESIGN = "design"
    PRODUCTION = "production"
    USE = "use"
    COLLECTION = "collection"
    RECYCLING = "recycling"
    REMANUFACTURING = "remanufacturing"


class SupplyChainTier(Enum):
    TIER_1 = "tier_1"  # Direct suppliers
    TIER_2 = "tier_2"  # Suppliers' suppliers
    TIER_3 = "tier_3"  # Raw material suppliers
    TIER_4 = "tier_4"  # Extraction/processing


class ReportingPeriod(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"


class StakeholderType(Enum):
    INVESTORS = "investors"
    CUSTOMERS = "customers"
    EMPLOYEES = "employees"
    REGULATORS = "regulators"
    COMMUNITY = "community"
    SUPPLIERS = "suppliers"


class GoalPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ESGRating(Enum):
    AAA = "AAA"
    AA = "AA"
    A = "A"
    BBB = "BBB"
    BB = "BB"
    B = "B"
    CCC = "CCC"


class EnergySource(Enum):
    SOLAR = "solar"
    WIND = "wind"
    HYDRO = "hydro"
    NUCLEAR = "nuclear"
    NATURAL_GAS = "natural_gas"
    COAL = "coal"
    BIOMASS = "biomass"
    GEOTHERMAL = "geothermal"
    HYDROGEN = "hydrogen"


class WasteType(Enum):
    LANDFILL = "landfill"
    RECYCLABLE = "recyclable"
    ORGANIC = "organic"
    HAZARDOUS = "hazardous"
    ELECTRONIC = "electronic"
    CONSTRUCTION = "construction"
    CHEMICAL = "chemical"


class WaterSource(Enum):
    MUNICIPAL = "municipal"
    WELL = "well"
    RIVER = "river"
    RAINWATER = "rainwater"
    RECYCLED = "recycled"


class TransportMode(Enum):
    ROAD = "road"
    RAIL = "rail"
    SEA = "sea"
    AIR = "air"
    PIPELINE = "pipeline"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class EmissionRecord:
    """Carbon emission record."""
    record_id: str
    category: SustainabilityCategory
    scope: CarbonScope
    source: str
    amount: float
    unit: str
    date: datetime
    location: str
    verified: bool = False
    activity_data: Dict[str, Any] = field(default_factory=dict)
    reduction_offset: float = 0.0
    notes: str = ""

    @property
    def net_emission(self) -> float:
        return max(0, self.amount - self.reduction_offset)

    @property
    def is_verified(self) -> bool:
        return self.verified


@dataclass
class SustainabilityGoal:
    """Sustainability target/goal."""
    goal_id: str
    name: str
    description: str
    category: SustainabilityCategory
    baseline_value: float
    target_value: float
    baseline_year: int
    target_year: int
    current_value: float = 0.0
    status: str = "active"
    priority: GoalPriority = GoalPriority.MEDIUM
    owner: str = ""
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def progress_pct(self) -> float:
        if self.baseline_value == self.target_value:
            return 100.0
        total_change = self.target_value - self.baseline_value
        current_change = self.current_value - self.baseline_value
        return min(100.0, max(0.0, (current_change / total_change) * 100))

    @property
    def years_remaining(self) -> int:
        return max(0, self.target_year - datetime.utcnow().year)

    @property
    def is_on_track(self) -> bool:
        total_years = self.target_year - self.baseline_year
        elapsed_years = datetime.utcnow().year - self.baseline_year
        expected_progress = (elapsed_years / total_years) * 100
        return self.progress_pct >= expected_progress * 0.9


@dataclass
class GreenInitiative:
    """Sustainability initiative/project."""
    initiative_id: str
    name: str
    description: str
    category: SustainabilityCategory
    status: InitiativeStatus
    start_date: datetime
    expected_completion: datetime
    investment: float
    projected_savings: Dict[str, float]
    carbon_reduction: float
    metrics: Dict[str, Any] = field(default_factory=dict)
    owner: str = ""
    stakeholders: List[str] = field(default_factory=list)
    risk_level: str = "medium"
    roi_calculated: bool = False

    @property
    def actual_completion_pct(self) -> float:
        return self.metrics.get("progress", 0)

    @property
    def is_overdue(self) -> bool:
        return datetime.utcnow() > self.expected_completion and self.status != InitiativeStatus.COMPLETED


@dataclass
class Supplier:
    """Supply chain supplier record."""
    supplier_id: str
    name: str
    tier: SupplyChainTier
    location: str
    category: str
    sustainability_score: float = 0.0
    certifications: List[str] = field(default_factory=list)
    carbon_footprint: float = 0.0
    last_audit_date: Optional[datetime] = None
    audit_score: float = 0.0
    compliance_status: str = "pending"
    contact_email: str = ""
    risk_level: str = "medium"

    @property
    def is_compliant(self) -> bool:
        return self.compliance_status == "compliant"

    @property
    def audit_age_days(self) -> Optional[int]:
        if not self.last_audit_date:
            return None
        return (datetime.utcnow() - self.last_audit_date).days


@dataclass
class CircularProduct:
    """Product circular economy tracking."""
    product_id: str
    name: str
    category: str
    material_composition: Dict[str, float]
    recyclable_pct: float
    recycled_content_pct: float
    carbon_footprint: float
    design_for_disassembly: bool = False
    take_back_program: bool = False
    remanufacturing_possible: bool = False
    end_of_life_options: List[str] = field(default_factory=list)

    @property
    def circularity_score(self) -> float:
        score = self.recycled_content_pct * 0.3
        score += self.recyclable_pct * 0.3
        score += (100 if self.design_for_disassembly else 0) * 0.2
        score += (100 if self.take_back_program else 0) * 0.1
        score += (100 if self.remanufacturing_possible else 0) * 0.1
        return score


@dataclass
class WaterUsage:
    """Water consumption record."""
    usage_id: str
    location: str
    source: WaterSource
    volume_m3: float
    date: datetime
    process: str = ""
    recycled_pct: float = 0.0
    cost: float = 0.0

    @property
    def net_consumption(self) -> float:
        return self.volume_m3 * (1 - self.recycled_pct / 100)


@dataclass
class EnergyRecord:
    """Energy consumption record."""
    record_id: str
    location: str
    source: EnergySource
    kwh: float
    date: datetime
    cost: float = 0.0
    carbon_factor: float = 0.0
    renewable_pct: float = 0.0

    @property
    def carbon_emissions(self) -> float:
        return self.kwh * self.carbon_factor


@dataclass
class WasteRecord:
    """Waste generation record."""
    record_id: str
    location: str
    waste_type: WasteType
    weight_kg: float
    date: datetime
    disposal_method: str = ""
    recycled_pct: float = 0.0
    cost: float = 0.0

    @property
    def landfill_diverted(self) -> float:
        return self.weight_kg * (self.recycled_pct / 100)


@dataclass
class ESGScore:
    """ESG scoring record."""
    score_id: str
    date: datetime
    environmental_score: float
    social_score: float
    governance_score: float
    overall_score: float
    rating: ESGRating
    methodology: str = ""
    benchmark: str = ""

    @property
    def category_breakdown(self) -> Dict[str, float]:
        return {
            "environmental": self.environmental_score,
            "social": self.social_score,
            "governance": self.governance_score,
        }


@dataclass
class ComplianceRecord:
    """Regulatory compliance tracking."""
    record_id: str
    framework: ComplianceFramework
    requirement: str
    status: str = "pending"
    due_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    evidence_url: str = ""
    notes: str = ""
    responsible_party: str = ""

    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status != "compliant"


@dataclass
class CarbonOffset:
    """Carbon offset/credit record."""
    offset_id: str
    project_name: str
    project_type: str
    tonnes_co2: float
    purchase_date: datetime
    vintage_year: int
    certification: str = ""
    cost_per_tonne: float = 0.0
    retired: bool = False

    @property
    def total_cost(self) -> float:
        return self.tonnes_co2 * self.cost_per_tonne


@dataclass
class StakeholderReport:
    """Stakeholder-specific report."""
    report_id: str
    stakeholder: StakeholderType
    period: ReportingPeriod
    start_date: datetime
    end_date: datetime
    sections: List[Dict[str, Any]] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.utcnow)
    executive_summary: str = ""


@dataclass
class SDGAlignment:
    """UN SDG alignment tracking."""
    sdg_number: int
    sdg_name: str
    target_value: float
    current_value: float
    contribution_pct: float = 0.0
    initiatives: List[str] = field(default_factory=list)

    @property
    def progress(self) -> float:
        if self.target_value == 0:
            return 0.0
        return min(100.0, (self.current_value / self.target_value) * 100)


# ---------------------------------------------------------------------------
# Carbon Calculator
# ---------------------------------------------------------------------------

class CarbonCalculator:
    """Carbon emission calculation engine."""

    def __init__(self) -> None:
        self.emission_factors: Dict[str, Dict[str, float]] = {
            "electricity": {"factor": 0.42, "unit": "kg CO2e/kWh"},
            "natural_gas": {"factor": 2.0, "unit": "kg CO2e/m³"},
            "gasoline": {"factor": 2.31, "unit": "kg CO2e/L"},
            "diesel": {"factor": 2.68, "unit": "kg CO2e/L"},
            "lpg": {"factor": 1.56, "unit": "kg CO2e/L"},
            "flight_short": {"factor": 0.255, "unit": "kg CO2e/km"},
            "flight_long": {"factor": 0.195, "unit": "kg CO2e/km"},
            "flight_intl": {"factor": 0.150, "unit": "kg CO2e/km"},
            "shipping": {"factor": 0.5, "unit": "kg CO2e/tonne-km"},
            "rail": {"factor": 0.041, "unit": "kg CO2e/passenger-km"},
            "bus": {"factor": 0.089, "unit": "kg CO2e/passenger-km"},
            "car": {"factor": 0.12, "unit": "kg CO2e/km"},
            "ev": {"factor": 0.05, "unit": "kg CO2e/km"},
            "waste_landfill": {"factor": 0.58, "unit": "kg CO2e/kg"},
            "waste_recycled": {"factor": 0.02, "unit": "kg CO2e/kg"},
            "waste_composted": {"factor": 0.01, "unit": "kg CO2e/kg"},
            "water": {"factor": 0.344, "unit": "kg CO2e/m³"},
            "refrigerant_r410a": {"factor": 2088, "unit": "kg CO2e/kg"},
            "refrigerant_r134a": {"factor": 1430, "unit": "kg CO2e/kg"},
        }
        self.grid_factors: Dict[str, float] = {
            "US_average": 0.42,
            "EU_average": 0.30,
            "UK": 0.23,
            "Germany": 0.35,
            "France": 0.06,
            "China": 0.58,
            "India": 0.71,
            "Japan": 0.47,
            "Canada": 0.12,
            "Australia": 0.63,
        }
        self.scope3_categories: Dict[int, str] = {
            1: "Purchased Goods and Services",
            2: "Capital Goods",
            3: "Fuel and Energy Related Activities",
            4: "Upstream Transportation",
            5: "Waste Generated in Operations",
            6: "Business Travel",
            7: "Employee Commuting",
            8: "Upstream Leased Assets",
            9: "Downstream Transportation",
            10: "Processing of Sold Products",
            11: "Use of Sold Products",
            12: "End-of-life Treatment",
            13: "Downstream Leased Assets",
            14: "Franchises",
            15: "Investments",
        }

    def calculate_emission(self, source: str, quantity: float, region: str = "US_average") -> Dict[str, Any]:
        """Calculate emission for given source and quantity."""
        factor_data = self.emission_factors.get(source.lower())
        if not factor_data:
            return {"error": f"Unknown source: {source}"}

        emission = quantity * factor_data["factor"]
        return {
            "source": source,
            "quantity": quantity,
            "emission_kg": round(emission, 4),
            "emission_tonnes": round(emission / 1000, 6),
            "unit": factor_data["unit"],
            "factor": factor_data["factor"],
        }

    def calculate_from_activity(self, activity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emissions from activity data."""
        calculators = {
            "electricity": self._calc_electricity,
            "transportation": self._calc_transport,
            "heating": self._calc_heating,
            "cooling": self._calc_cooling,
            "waste": self._calc_waste,
            "water": self._calc_water,
            "business_travel": self._calc_business_travel,
            "employee_commute": self._calc_employee_commute,
            "supply_chain": self._calc_supply_chain,
            "refrigerants": self._calc_refrigerants,
        }

        calc = calculators.get(activity_type.lower())
        if not calc:
            return {"error": f"Unknown activity type: {activity_type}"}

        return calc(data)

    def _calc_electricity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate electricity-related emissions."""
        kwh = data.get("kwh", 0)
        region = data.get("region", "US_average")
        grid_factor = self.grid_factors.get(region, 0.42)
        renewable_pct = data.get("renewable_pct", 0)

        emission = kwh * grid_factor * (1 - renewable_pct / 100)
        return {
            "emission_kg": round(emission, 4),
            "breakdown": {
                "kwh": kwh,
                "grid_factor": grid_factor,
                "region": region,
                "renewable_offset_pct": renewable_pct,
            },
        }

    def _calc_transport(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate transportation emissions."""
        distance_km = data.get("distance_km", 0)
        mode = data.get("mode", "car")
        passengers = data.get("passengers", 1)
        load_tonnes = data.get("load_tonnes", 0)

        factors = {
            "car": 0.12,
            "ev": 0.05,
            "bus": 0.089,
            "rail": 0.041,
            "flight_short": 0.255,
            "flight_long": 0.195,
            "flight_intl": 0.150,
            "shipping": 0.5,
        }

        factor = factors.get(mode.lower(), 0.12)
        if mode.lower() in ("shipping",) and load_tonnes > 0:
            emission = load_tonnes * distance_km * factor
        else:
            emission = (distance_km * factor) / max(1, passengers)

        return {
            "emission_kg": round(emission, 4),
            "breakdown": {
                "distance_km": distance_km,
                "mode": mode,
                "passengers": passengers,
                "factor": factor,
            },
        }

    def _calc_heating(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate heating-related emissions."""
        fuel_type = data.get("fuel_type", "natural_gas")
        amount = data.get("amount", 0)

        factor = self.emission_factors.get(fuel_type, {}).get("factor", 2.0)
        emission = amount * factor
        return {
            "emission_kg": round(emission, 4),
            "breakdown": {"fuel_type": fuel_type, "amount": amount, "factor": factor},
        }

    def _calc_cooling(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate cooling/HVAC emissions."""
        kwh = data.get("kwh", 0)
        refrigerant_leak_kg = data.get("refrigerant_leak_kg", 0)
        refrigerant_type = data.get("refrigerant_type", "r410a")

        electricity_emission = kwh * 0.42
        factor = self.emission_factors.get(f"refrigerant_{refrigerant_type.lower()}", {}).get("factor", 2088)
        refrigerant_emission = refrigerant_leak_kg * factor

        return {
            "emission_kg": round(electricity_emission + refrigerant_emission, 4),
            "breakdown": {
                "electricity_kg": electricity_emission,
                "refrigerant_kg": refrigerant_emission,
            },
        }

    def _calc_waste(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate waste emissions."""
        waste_type = data.get("waste_type", "landfill")
        weight_kg = data.get("weight_kg", 0)

        factor = self.emission_factors.get(f"waste_{waste_type}", {}).get("factor", 0.58)
        emission = weight_kg * factor
        return {
            "emission_kg": round(emission, 4),
            "breakdown": {"waste_type": waste_type, "weight_kg": weight_kg},
        }

    def _calc_water(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate water-related emissions."""
        volume_m3 = data.get("volume_m3", 0)
        emission = volume_m3 * self.emission_factors["water"]["factor"]
        return {
            "emission_kg": round(emission, 4),
            "breakdown": {"volume_m3": volume_m3},
        }

    def _calc_business_travel(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate business travel emissions."""
        flights = data.get("flights", 0)
        hotel_nights = data.get("hotel_nights", 0)
        car_rental_km = data.get("car_rental_km", 0)

        flight_emission = flights * 250 * 0.255
        hotel_emission = hotel_nights * 20
        car_emission = car_rental_km * 0.12

        return {
            "emission_kg": round(flight_emission + hotel_emission + car_emission, 4),
            "breakdown": {
                "flights_kg": flight_emission,
                "hotels_kg": hotel_emission,
                "car_kg": car_emission,
            },
        }

    def _calc_employee_commute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate employee commuting emissions."""
        employees = data.get("employees", 0)
        avg_distance_km = data.get("avg_distance_km", 20)
        work_days = data.get("work_days", 220)
        mode = data.get("mode", "car")

        factor = self.emission_factors.get(mode, {}).get("factor", 0.12)
        emission = employees * avg_distance_km * 2 * work_days * factor

        return {
            "emission_kg": round(emission, 4),
            "breakdown": {
                "employees": employees,
                "avg_distance_km": avg_distance_km,
                "work_days": work_days,
            },
        }

    def _calc_supply_chain(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate supply chain emissions (simplified)."""
        procurement_cost = data.get("procurement_cost", 0)
        emission_intensity = data.get("emission_intensity", 0.5)
        emission = procurement_cost * emission_intensity

        return {
            "emission_kg": round(emission, 4),
            "breakdown": {"procurement_cost": procurement_cost, "intensity": emission_intensity},
        }

    def _calc_refrigerants(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate refrigerant emissions."""
        leak_kg = data.get("leak_kg", 0)
        refrigerant_type = data.get("refrigerant_type", "r410a")
        factor = self.emission_factors.get(f"refrigerant_{refrigerant_type.lower()}", {}).get("factor", 2088)
        emission = leak_kg * factor

        return {
            "emission_kg": round(emission, 4),
            "breakdown": {"refrigerant": refrigerant_type, "leak_kg": leak_kg},
        }

    def calculate_total_footprint(self, records: List[EmissionRecord]) -> Dict[str, Any]:
        """Calculate total carbon footprint from emission records."""
        total = 0.0
        by_scope: Dict[str, float] = defaultdict(float)
        by_category: Dict[str, float] = defaultdict(float)
        by_month: Dict[str, float] = defaultdict(float)

        for record in records:
            net = record.net_emission
            total += net
            by_scope[record.scope.value] += net
            by_category[record.category.value] += net
            month_key = record.date.strftime("%Y-%m")
            by_month[month_key] += net

        return {
            "total_emission_kg": round(total, 2),
            "total_emission_tonnes": round(total / 1000, 3),
            "by_scope": dict(by_scope),
            "by_category": dict(by_category),
            "by_month": dict(by_month),
            "record_count": len(records),
        }


# ---------------------------------------------------------------------------
# Goal Tracker
# ---------------------------------------------------------------------------

class GoalTracker:
    """Tracks sustainability goals and targets."""

    def __init__(self) -> None:
        self.goals: Dict[str, SustainabilityGoal] = {}
        self.history: List[Dict[str, Any]] = []
        self._counter = 0

    def create_goal(
        self,
        name: str,
        description: str,
        category: SustainabilityCategory,
        baseline_value: float,
        target_value: float,
        target_year: int,
        priority: GoalPriority = GoalPriority.MEDIUM,
        owner: str = "",
    ) -> SustainabilityGoal:
        """Create sustainability goal."""
        self._counter += 1
        goal = SustainabilityGoal(
            goal_id=f"GOAL-{self._counter:05d}",
            name=name,
            description=description,
            category=category,
            baseline_value=baseline_value,
            target_value=target_value,
            baseline_year=datetime.utcnow().year,
            target_year=target_year,
            current_value=baseline_value,
            priority=priority,
            owner=owner,
        )
        self.goals[goal.goal_id] = goal
        logger.info("Goal created: %s (%s)", name, goal.goal_id)
        return goal

    def update_progress(self, goal_id: str, current_value: float) -> Optional[SustainabilityGoal]:
        """Update goal progress."""
        if goal_id not in self.goals:
            logger.warning("Goal not found: %s", goal_id)
            return None

        goal = self.goals[goal_id]
        goal.current_value = current_value
        goal.updated_at = datetime.utcnow()

        if current_value <= goal.target_value:
            goal.status = "achieved"
        elif datetime.utcnow().year > goal.target_year:
            goal.status = "missed"

        self.history.append({
            "goal_id": goal_id,
            "value": current_value,
            "timestamp": datetime.utcnow().isoformat(),
        })

        return goal

    def calculate_goal_status(self, goal_id: str) -> Dict[str, Any]:
        """Calculate detailed goal status."""
        goal = self.goals.get(goal_id)
        if not goal:
            return {"error": "Goal not found"}

        total_years = goal.target_year - goal.baseline_year
        elapsed_years = datetime.utcnow().year - goal.baseline_year
        expected_progress = (elapsed_years / total_years) * 100 if total_years > 0 else 100
        actual_progress = goal.progress_pct

        return {
            "goal_id": goal.goal_id,
            "goal_name": goal.name,
            "expected_progress": round(expected_progress, 1),
            "actual_progress": round(actual_progress, 1),
            "variance": round(actual_progress - expected_progress, 1),
            "on_track": actual_progress >= expected_progress * 0.9,
            "years_remaining": goal.years_remaining,
            "status": goal.status,
        }

    def get_overall_progress(self) -> Dict[str, Any]:
        """Get overall goal progress summary."""
        on_track = 0
        at_risk = 0
        behind = 0
        achieved = 0

        for goal in self.goals.values():
            status = self.calculate_goal_status(goal.goal_id)
            if goal.status == "achieved":
                achieved += 1
            elif status.get("on_track", False):
                on_track += 1
            elif status.get("variance", 0) > -20:
                at_risk += 1
            else:
                behind += 1

        total = len(self.goals)
        return {
            "total_goals": total,
            "on_track": on_track,
            "at_risk": at_risk,
            "behind": behind,
            "achieved": achieved,
            "success_rate": round(achieved / total * 100, 1) if total > 0 else 0,
        }

    def get_goals_by_category(self, category: SustainabilityCategory) -> List[SustainabilityGoal]:
        """Get goals filtered by category."""
        return [g for g in self.goals.values() if g.category == category]

    def get_overdue_milestones(self) -> List[Dict[str, Any]]:
        """Get overdue milestones across all goals."""
        overdue = []
        for goal in self.goals.values():
            for milestone in goal.milestones:
                due = milestone.get("due_date")
                if isinstance(due, datetime) and datetime.utcnow() > due and not milestone.get("completed"):
                    overdue.append({
                        "goal_id": goal.goal_id,
                        "milestone": milestone,
                        "days_overdue": (datetime.utcnow() - due).days,
                    })
        return overdue


# ---------------------------------------------------------------------------
# Initiative Manager
# ---------------------------------------------------------------------------

class InitiativeManager:
    """Manages sustainability initiatives and projects."""

    def __init__(self) -> None:
        self.initiatives: Dict[str, GreenInitiative] = {}
        self._counter = 0

    def create_initiative(
        self,
        name: str,
        description: str,
        category: SustainabilityCategory,
        investment: float,
        expected_savings: Dict[str, float],
        carbon_reduction: float,
        timeline_months: int = 12,
        owner: str = "",
    ) -> GreenInitiative:
        """Create green initiative."""
        start = datetime.utcnow()
        completion = start + timedelta(days=30 * timeline_months)

        self._counter += 1
        initiative = GreenInitiative(
            initiative_id=f"INI-{self._counter:05d}",
            name=name,
            description=description,
            category=category,
            status=InitiativeStatus.PLANNED,
            start_date=start,
            expected_completion=completion,
            investment=investment,
            projected_savings=expected_savings,
            carbon_reduction=carbon_reduction,
            owner=owner,
        )
        self.initiatives[initiative.initiative_id] = initiative
        logger.info("Initiative created: %s (%s)", name, initiative.initiative_id)
        return initiative

    def update_initiative(self, initiative_id: str, progress: float, status: Optional[InitiativeStatus] = None) -> Optional[GreenInitiative]:
        """Update initiative progress."""
        if initiative_id not in self.initiatives:
            return None

        initiative = self.initiatives[initiative_id]
        initiative.metrics["progress"] = min(100, max(0, progress))
        initiative.updated_at = datetime.utcnow()

        if status:
            initiative.status = status
        elif progress >= 100:
            initiative.status = InitiativeStatus.COMPLETED
        elif progress > 0:
            initiative.status = InitiativeStatus.IN_PROGRESS

        return initiative

    def calculate_roi(self, initiative_id: str) -> Dict[str, Any]:
        """Calculate initiative ROI."""
        initiative = self.initiatives.get(initiative_id)
        if not initiative:
            return {"error": "Initiative not found"}

        annual_savings = initiative.projected_savings.get("annual", 0)
        payback_period = initiative.investment / annual_savings if annual_savings > 0 else float("inf")
        roi_5_year = ((annual_savings * 5) - initiative.investment) / initiative.investment * 100 if initiative.investment > 0 else 0

        return {
            "initiative_id": initiative.initiative_id,
            "initiative_name": initiative.name,
            "investment": initiative.investment,
            "annual_savings": annual_savings,
            "payback_years": round(payback_period, 1),
            "roi_5_year_pct": round(roi_5_year, 1),
            "carbon_reduction_tonnes": initiative.carbon_reduction,
            "cost_per_tonne_abated": round(initiative.investment / initiative.carbon_reduction, 2) if initiative.carbon_reduction > 0 else 0,
        }

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get initiative portfolio summary."""
        total_investment = sum(i.investment for i in self.initiatives.values())
        total_carbon = sum(i.carbon_reduction for i in self.initiatives.values())
        total_savings = sum(i.projected_savings.get("annual", 0) for i in self.initiatives.values())

        by_status: Dict[str, int] = defaultdict(int)
        by_category: Dict[str, int] = defaultdict(int)
        for ini in self.initiatives.values():
            by_status[ini.status.value] += 1
            by_category[ini.category.value] += 1

        return {
            "total_initiatives": len(self.initiatives),
            "total_investment": total_investment,
            "projected_annual_savings": total_savings,
            "total_carbon_reduction_tonnes": total_carbon,
            "by_status": dict(by_status),
            "by_category": dict(by_category),
            "avg_cost_per_tonne": round(total_investment / total_carbon, 2) if total_carbon > 0 else 0,
        }

    def get_overdue_initiatives(self) -> List[GreenInitiative]:
        """Get initiatives that are overdue."""
        return [i for i in self.initiatives.values() if i.is_overdue]

    def get_initiatives_by_category(self, category: SustainabilityCategory) -> List[GreenInitiative]:
        """Get initiatives filtered by category."""
        return [i for i in self.initiatives.values() if i.category == category]


# ---------------------------------------------------------------------------
# Supply Chain Manager
# ---------------------------------------------------------------------------

class SupplyChainManager:
    """Manages green supply chain and supplier sustainability."""

    def __init__(self) -> None:
        self.suppliers: Dict[str, Supplier] = {}
        self.audit_history: List[Dict[str, Any]] = []
        self._counter = 0

    def add_supplier(
        self,
        name: str,
        tier: SupplyChainTier,
        location: str,
        category: str,
        **kwargs: Any,
    ) -> Supplier:
        """Add supplier to tracking."""
        self._counter += 1
        supplier = Supplier(
            supplier_id=f"SUP-{self._counter:05d}",
            name=name,
            tier=tier,
            location=location,
            category=category,
            **kwargs,
        )
        self.suppliers[supplier.supplier_id] = supplier
        return supplier

    def calculate_supplier_score(self, supplier_id: str) -> Dict[str, Any]:
        """Calculate comprehensive supplier sustainability score."""
        supplier = self.suppliers.get(supplier_id)
        if not supplier:
            return {"error": "Supplier not found"}

        weights = {
            "certifications": 0.25,
            "carbon_footprint": 0.20,
            "audit_score": 0.30,
            "compliance": 0.15,
            "location_risk": 0.10,
        }

        cert_score = min(100, len(supplier.certifications) * 20)
        carbon_score = max(0, 100 - (supplier.carbon_footprint / 10))
        audit_score = supplier.audit_score
        compliance_score = 100 if supplier.is_compliant else 0
        location_risk = 80 if supplier.location in ["China", "India"] else 90

        overall = (
            cert_score * weights["certifications"]
            + carbon_score * weights["carbon_footprint"]
            + audit_score * weights["audit_score"]
            + compliance_score * weights["compliance"]
            + location_risk * weights["location_risk"]
        )

        return {
            "supplier_id": supplier_id,
            "overall_score": round(overall, 1),
            "breakdown": {
                "certifications": round(cert_score, 1),
                "carbon_footprint": round(carbon_score, 1),
                "audit_score": round(audit_score, 1),
                "compliance": round(compliance_score, 1),
            },
        }

    def get_suppliers_by_tier(self, tier: SupplyChainTier) -> List[Supplier]:
        """Get suppliers filtered by tier."""
        return [s for s in self.suppliers.values() if s.tier == tier]

    def get_non_compliant_suppliers(self) -> List[Supplier]:
        """Get suppliers that are not compliant."""
        return [s for s in self.suppliers.values() if not s.is_compliant]

    def get_suppliers_needing_audit(self, days: int = 365) -> List[Supplier]:
        """Get suppliers that need audit within specified days."""
        cutoff = datetime.utcnow() + timedelta(days=days)
        return [
            s for s in self.suppliers.values()
            if not s.last_audit_date or s.last_audit_date > cutoff
        ]

    def get_supply_chain_summary(self) -> Dict[str, Any]:
        """Get supply chain sustainability summary."""
        total_suppliers = len(self.suppliers)
        by_tier: Dict[str, int] = defaultdict(int)
        by_compliance: Dict[str, int] = defaultdict(int)
        total_carbon = 0.0

        for s in self.suppliers.values():
            by_tier[s.tier.value] += 1
            by_compliance[s.compliance_status] += 1
            total_carbon += s.carbon_footprint

        avg_score = statistics.mean([
            self.calculate_supplier_score(s.supplier_id).get("overall_score", 0)
            for s in self.suppliers.values()
        ]) if self.suppliers else 0

        return {
            "total_suppliers": total_suppliers,
            "by_tier": dict(by_tier),
            "by_compliance": dict(by_compliance),
            "total_carbon_footprint": total_carbon,
            "average_sustainability_score": round(avg_score, 1),
            "non_compliant_count": len(self.get_non_compliant_suppliers()),
        }


# ---------------------------------------------------------------------------
# Circular Economy Manager
# ---------------------------------------------------------------------------

class CircularEconomyManager:
    """Manages circular economy tracking for products."""

    def __init__(self) -> None:
        self.products: Dict[str, CircularProduct] = {}
        self._counter = 0

    def add_product(
        self,
        name: str,
        category: str,
        material_composition: Dict[str, float],
        recyclable_pct: float,
        recycled_content_pct: float,
        carbon_footprint: float,
        **kwargs: Any,
    ) -> CircularProduct:
        """Add product for circular economy tracking."""
        self._counter += 1
        product = CircularProduct(
            product_id=f"PROD-{self._counter:05d}",
            name=name,
            category=category,
            material_composition=material_composition,
            recyclable_pct=recyclable_pct,
            recycled_content_pct=recycled_content_pct,
            carbon_footprint=carbon_footprint,
            **kwargs,
        )
        self.products[product.product_id] = product
        return product

    def calculate_circularity_score(self, product_id: str) -> Dict[str, Any]:
        """Calculate circularity score for product."""
        product = self.products.get(product_id)
        if not product:
            return {"error": "Product not found"}

        return {
            "product_id": product_id,
            "product_name": product.name,
            "circularity_score": round(product.circularity_score, 1),
            "recyclable_pct": product.recyclable_pct,
            "recycled_content_pct": product.recycled_content_pct,
            "design_for_disassembly": product.design_for_disassembly,
            "take_back_program": product.take_back_program,
            "remanufacturing_possible": product.remanufacturing_possible,
        }

    def get_products_by_category(self, category: str) -> List[CircularProduct]:
        """Get products filtered by category."""
        return [p for p in self.products.values() if p.category.lower() == category.lower()]

    def get_portfolio_circularity(self) -> Dict[str, Any]:
        """Get portfolio-wide circularity metrics."""
        if not self.products:
            return {"avg_circularity_score": 0, "total_products": 0}

        scores = [p.circularity_score for p in self.products.values()]
        avg_recyclable = statistics.mean([p.recyclable_pct for p in self.products.values()])
        avg_recycled_content = statistics.mean([p.recycled_content_pct for p in self.products.values()])
        dfa_count = sum(1 for p in self.products.values() if p.design_for_disassembly)
        takeback_count = sum(1 for p in self.products.values() if p.take_back_program)

        return {
            "total_products": len(self.products),
            "avg_circularity_score": round(statistics.mean(scores), 1),
            "avg_recyclable_pct": round(avg_recyclable, 1),
            "avg_recycled_content_pct": round(avg_recycled_content, 1),
            "design_for_disassembly_pct": round(dfa_count / len(self.products) * 100, 1),
            "take_back_program_pct": round(takeback_count / len(self.products) * 100, 1),
        }


# ---------------------------------------------------------------------------
# Water & Waste Manager
# ---------------------------------------------------------------------------

class ResourceUsageManager:
    """Manages water and waste tracking."""

    def __init__(self) -> None:
        self.water_records: List[WaterUsage] = []
        self.waste_records: List[WasteRecord] = []
        self.energy_records: List[EnergyRecord] = []
        self._water_counter = 0
        self._waste_counter = 0
        self._energy_counter = 0

    def add_water_usage(
        self, location: str, source: WaterSource, volume_m3: float,
        date: datetime, **kwargs: Any,
    ) -> WaterUsage:
        """Add water usage record."""
        self._water_counter += 1
        record = WaterUsage(
            usage_id=f"WTR-{self._water_counter:05d}",
            location=location,
            source=source,
            volume_m3=volume_m3,
            date=date,
            **kwargs,
        )
        self.water_records.append(record)
        return record

    def add_waste_record(
        self, location: str, waste_type: WasteType, weight_kg: float,
        date: datetime, **kwargs: Any,
    ) -> WasteRecord:
        """Add waste record."""
        self._waste_counter += 1
        record = WasteRecord(
            record_id=f"WST-{self._waste_counter:05d}",
            location=location,
            waste_type=waste_type,
            weight_kg=weight_kg,
            date=date,
            **kwargs,
        )
        self.waste_records.append(record)
        return record

    def add_energy_record(
        self, location: str, source: EnergySource, kwh: float,
        date: datetime, **kwargs: Any,
    ) -> EnergyRecord:
        """Add energy record."""
        self._energy_counter += 1
        record = EnergyRecord(
            record_id=f"ENR-{self._energy_counter:05d}",
            location=location,
            source=source,
            kwh=kwh,
            date=date,
            **kwargs,
        )
        self.energy_records.append(record)
        return record

    def get_water_summary(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get water usage summary."""
        records = self.water_records
        if start_date:
            records = [r for r in records if r.date >= start_date]
        if end_date:
            records = [r for r in records if r.date <= end_date]

        total_volume = sum(r.volume_m3 for r in records)
        total_recycled = sum(r.net_consumption for r in records)
        total_cost = sum(r.cost for r in records)

        by_source: Dict[str, float] = defaultdict(float)
        for r in records:
            by_source[r.source.value] += r.volume_m3

        return {
            "total_volume_m3": round(total_volume, 2),
            "net_consumption_m3": round(total_recycled, 2),
            "recycled_volume_m3": round(total_volume - total_recycled, 2),
            "total_cost": round(total_cost, 2),
            "by_source": dict(by_source),
            "record_count": len(records),
        }

    def get_waste_summary(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get waste summary."""
        records = self.waste_records
        if start_date:
            records = [r for r in records if r.date >= start_date]
        if end_date:
            records = [r for r in records if r.date <= end_date]

        total_weight = sum(r.weight_kg for r in records)
        total_recycled = sum(r.landfill_diverted for r in records)
        total_cost = sum(r.cost for r in records)

        by_type: Dict[str, float] = defaultdict(float)
        for r in records:
            by_type[r.waste_type.value] += r.weight_kg

        return {
            "total_weight_kg": round(total_weight, 2),
            "recycled_kg": round(total_recycled, 2),
            "landfill_kg": round(total_weight - total_recycled, 2),
            "diversion_rate_pct": round(total_recycled / total_weight * 100, 1) if total_weight > 0 else 0,
            "total_cost": round(total_cost, 2),
            "by_type": dict(by_type),
            "record_count": len(records),
        }

    def get_energy_summary(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get energy usage summary."""
        records = self.energy_records
        if start_date:
            records = [r for r in records if r.date >= start_date]
        if end_date:
            records = [r for r in records if r.date <= end_date]

        total_kwh = sum(r.kwh for r in records)
        total_emissions = sum(r.carbon_emissions for r in records)
        total_cost = sum(r.cost for r in records)
        renewable_kwh = sum(r.kwh * r.renewable_pct / 100 for r in records)

        by_source: Dict[str, float] = defaultdict(float)
        for r in records:
            by_source[r.source.value] += r.kwh

        return {
            "total_kwh": round(total_kwh, 2),
            "renewable_kwh": round(renewable_kwh, 2),
            "renewable_pct": round(renewable_kwh / total_kwh * 100, 1) if total_kwh > 0 else 0,
            "total_emissions_kg": round(total_emissions, 2),
            "total_cost": round(total_cost, 2),
            "by_source": dict(by_source),
            "record_count": len(records),
        }


# ---------------------------------------------------------------------------
# Compliance Manager
# ---------------------------------------------------------------------------

class ComplianceManager:
    """Manages sustainability regulatory compliance."""

    def __init__(self) -> None:
        self.records: Dict[str, ComplianceRecord] = {}
        self.certifications: Dict[str, Dict[str, Any]] = {}
        self._counter = 0

    def add_requirement(
        self,
        framework: ComplianceFramework,
        requirement: str,
        due_date: Optional[datetime] = None,
        responsible_party: str = "",
    ) -> ComplianceRecord:
        """Add compliance requirement."""
        self._counter += 1
        record = ComplianceRecord(
            record_id=f"COMP-{self._counter:05d}",
            framework=framework,
            requirement=requirement,
            due_date=due_date,
            responsible_party=responsible_party,
        )
        self.records[record.record_id] = record
        return record

    def update_status(self, record_id: str, status: str) -> bool:
        """Update compliance status."""
        if record_id not in self.records:
            return False

        self.records[record_id].status = status
        if status == "compliant":
            self.records[record_id].completion_date = datetime.utcnow()
        return True

    def add_certification(self, name: str, certification_type: CertificationType, expiry: Optional[datetime] = None) -> None:
        """Add organization certification."""
        self.certifications[name] = {
            "type": certification_type.value,
            "obtained_date": datetime.utcnow(),
            "expiry_date": expiry,
            "status": "active",
        }

    def get_overdue_requirements(self) -> List[ComplianceRecord]:
        """Get overdue compliance requirements."""
        return [r for r in self.records.values() if r.is_overdue]

    def get_compliance_by_framework(self, framework: ComplianceFramework) -> List[ComplianceRecord]:
        """Get compliance records by framework."""
        return [r for r in self.records.values() if r.framework == framework]

    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get compliance summary."""
        by_status: Dict[str, int] = defaultdict(int)
        by_framework: Dict[str, int] = defaultdict(int)

        for record in self.records.values():
            by_status[record.status] += 1
            by_framework[record.framework.value] += 1

        total = len(self.records)
        compliant = by_status.get("compliant", 0)

        return {
            "total_requirements": total,
            "compliant": compliant,
            "compliance_rate_pct": round(compliant / total * 100, 1) if total > 0 else 0,
            "overdue": len(self.get_overdue_requirements()),
            "by_status": dict(by_status),
            "by_framework": dict(by_framework),
            "active_certifications": len(self.certifications),
        }


# ---------------------------------------------------------------------------
# ESG Reporter
# ---------------------------------------------------------------------------

class ESGReporter:
    """Generates ESG reports and scores."""

    def __init__(
        self,
        carbon_calc: CarbonCalculator,
        goal_tracker: GoalTracker,
        initiative_manager: InitiativeManager,
        supply_chain: SupplyChainManager,
    ) -> None:
        self.carbon = carbon_calc
        self.goals = goal_tracker
        self.initiatives = initiative_manager
        self.supply_chain = supply_chain

    def calculate_esg_score(self) -> ESGScore:
        """Calculate overall ESG score."""
        env_score = self._calculate_environmental_score()
        social_score = self._calculate_social_score()
        gov_score = self._calculate_governance_score()
        overall = env_score * 0.4 + social_score * 0.3 + gov_score * 0.3

        rating = self._score_to_rating(overall)

        return ESGScore(
            score_id=f"ESG-{datetime.utcnow().strftime('%Y%m%d')}",
            date=datetime.utcnow(),
            environmental_score=env_score,
            social_score=social_score,
            governance_score=gov_score,
            overall_score=overall,
            rating=rating,
        )

    def _calculate_environmental_score(self) -> float:
        """Calculate environmental component score."""
        base = 70.0

        goal_status = self.goals.get_overall_progress()
        base += goal_status.get("success_rate", 0) * 0.2

        portfolio = self.initiatives.get_portfolio_summary()
        if portfolio["total_carbon_reduction_tonnes"] > 100:
            base += 5

        return min(100.0, base)

    def _calculate_social_score(self) -> float:
        """Calculate social component score."""
        return 75.0

    def _calculate_governance_score(self) -> float:
        """Calculate governance component score."""
        return 80.0

    def _score_to_rating(self, score: float) -> ESGRating:
        """Convert numeric score to ESG rating."""
        if score >= 90:
            return ESGRating.AAA
        elif score >= 80:
            return ESGRating.AA
        elif score >= 70:
            return ESGRating.A
        elif score >= 60:
            return ESGRating.BBB
        elif score >= 50:
            return ESGRating.BB
        elif score >= 40:
            return ESGRating.B
        return ESGRating.CCC

    def generate_stakeholder_report(self, stakeholder: StakeholderType, start_date: datetime, end_date: datetime) -> StakeholderReport:
        """Generate stakeholder-specific report."""
        sections = []

        if stakeholder == StakeholderType.INVESTORS:
            sections.append({"title": "ESG Performance", "content": "Detailed ESG metrics and trends"})
            sections.append({"title": "Risk Assessment", "content": "Climate and sustainability risks"})
        elif stakeholder == StakeholderType.CUSTOMERS:
            sections.append({"title": "Product Sustainability", "content": "Green product metrics"})
            sections.append({"title": "Carbon Footprint", "content": "Supply chain transparency"})
        elif stakeholder == StakeholderType.REGULATORS:
            sections.append({"title": "Compliance Status", "content": "Regulatory compliance details"})
            sections.append({"title": "Emissions Report", "content": "Verified emissions data"})

        return StakeholderReport(
            report_id=f"RPT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            stakeholder=stakeholder,
            period=ReportingPeriod.ANNUALLY,
            start_date=start_date,
            end_date=end_date,
            sections=sections,
        )

    def generate_footprint_report(self, records: List[EmissionRecord]) -> Dict[str, Any]:
        """Generate carbon footprint report."""
        footprint = self.carbon.calculate_total_footprint(records)
        return {
            "report_date": datetime.utcnow().isoformat(),
            "period": f"{records[0].date.date()} to {records[-1].date.date()}" if records else "N/A",
            "total_emissions_tonnes": footprint["total_emission_tonnes"],
            "by_scope": footprint["by_scope"],
            "by_category": footprint["by_category"],
            "intensity_metrics": self._calculate_intensity_metrics(footprint),
        }

    def _calculate_intensity_metrics(self, footprint: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emission intensity metrics."""
        total_tonnes = footprint["total_emission_tonnes"]
        return {
            "emissions_per_employee": round(total_tonnes * 1000 / 100, 2),
            "emissions_per_revenue_million": round(total_tonnes * 1000 / 10, 2),
            "emissions_per_unit_produced": round(total_tonnes * 1000 / 10000, 4),
        }


# ---------------------------------------------------------------------------
# Sustainability Agent (Main)
# ---------------------------------------------------------------------------

class SustainabilityAgent:
    """Main sustainability management agent."""

    def __init__(self) -> None:
        self.carbon = CarbonCalculator()
        self.goals = GoalTracker()
        self.initiatives = InitiativeManager()
        self.supply_chain = SupplyChainManager()
        self.circular_economy = CircularEconomyManager()
        self.resources = ResourceUsageManager()
        self.compliance = ComplianceManager()
        self.reporter = ESGReporter(self.carbon, self.goals, self.initiatives, self.supply_chain)
        self.emission_records: List[EmissionRecord] = []
        self._record_counter = 0

    def track_emission(
        self,
        category: SustainabilityCategory,
        scope: CarbonScope,
        source: str,
        amount: float,
        unit: str,
        date: Optional[datetime] = None,
        location: str = "HQ",
        verified: bool = False,
    ) -> EmissionRecord:
        """Track emission record."""
        self._record_counter += 1
        record = EmissionRecord(
            record_id=f"EMI-{self._record_counter:05d}",
            category=category,
            scope=scope,
            source=source,
            amount=amount,
            unit=unit,
            date=date or datetime.utcnow(),
            location=location,
            verified=verified,
        )
        self.emission_records.append(record)
        logger.info("Emission tracked: %s %s %s (%s)", amount, unit, source, record.record_id)
        return record

    def set_sustainability_goal(
        self,
        name: str,
        description: str,
        category: SustainabilityCategory,
        baseline: float,
        target: float,
        target_year: int,
        priority: GoalPriority = GoalPriority.MEDIUM,
    ) -> Dict[str, Any]:
        """Set sustainability goal."""
        goal = self.goals.create_goal(
            name=name,
            description=description,
            category=category,
            baseline_value=baseline,
            target_value=target,
            target_year=target_year,
            priority=priority,
        )
        return {
            "goal_id": goal.goal_id,
            "name": goal.name,
            "target": f"{target} by {target_year}",
        }

    def calculate_carbon_footprint(self, activities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate carbon footprint from activities."""
        total_emission = 0.0
        breakdown: Dict[str, float] = defaultdict(float)

        for activity in activities:
            result = self.carbon.calculate_from_activity(activity["type"], activity["data"])
            if "emission_kg" in result:
                total_emission += result["emission_kg"]
                breakdown[activity["type"]] += result["emission_kg"]

        return {
            "total_emission_kg": round(total_emission, 2),
            "total_emission_tonnes": round(total_emission / 1000, 3),
            "breakdown": dict(breakdown),
            "offset_cost_usd": round(total_emission * 0.02, 2),
        }

    def get_sustainability_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive sustainability dashboard."""
        esg = self.reporter.calculate_esg_score()
        goal_progress = self.goals.get_overall_progress()
        initiative_portfolio = self.initiatives.get_portfolio_summary()
        supply_chain_summary = self.supply_chain.get_supply_chain_summary()
        resource_summary = {
            "water": self.resources.get_water_summary(),
            "waste": self.resources.get_waste_summary(),
            "energy": self.resources.get_energy_summary(),
        }
        compliance_summary = self.compliance.get_compliance_summary()

        return {
            "esg_score": {
                "overall": esg.overall_score,
                "rating": esg.rating.value,
                "environmental": esg.environmental_score,
                "social": esg.social_score,
                "governance": esg.governance_score,
            },
            "goals": goal_progress,
            "initiatives": initiative_portfolio,
            "supply_chain": supply_chain_summary,
            "resources": resource_summary,
            "compliance": compliance_summary,
            "quick_wins": [
                "Switch to LED lighting - saves 40% on energy costs",
                "Implement paperless office - reduces 5 tonnes CO2 annually",
                "Optimize HVAC schedule - saves 15% energy",
                "Install smart meters for real-time monitoring",
                "Set up recycling stations in all offices",
            ],
        }

    def generate_annual_report(self) -> Dict[str, Any]:
        """Generate comprehensive annual sustainability report."""
        footprint = self.carbon.calculate_total_footprint(self.emission_records)
        esg = self.reporter.calculate_esg_score()

        return {
            "report_type": "Annual Sustainability Report",
            "generated_at": datetime.utcnow().isoformat(),
            "executive_summary": "Organization demonstrates strong commitment to sustainability with measurable progress across environmental, social, and governance dimensions.",
            "carbon_footprint": footprint,
            "esg_score": {
                "overall": esg.overall_score,
                "rating": esg.rating.value,
            },
            "goals_status": self.goals.get_overall_progress(),
            "initiative_highlights": self.initiatives.get_portfolio_summary(),
            "supply_chain_sustainability": self.supply_chain.get_supply_chain_summary(),
            "circular_economy": self.circular_economy.get_portfolio_circularity(),
            "compliance_status": self.compliance.get_compliance_summary(),
            "sdg_alignment": self._get_sdg_alignment(),
            "targets_next_year": [
                "Reduce Scope 1+2 emissions by 15%",
                "Achieve 90% supplier compliance",
                "Launch 3 new circular economy initiatives",
                "Obtain ISO 14001 certification",
            ],
        }

    def _get_sdg_alignment(self) -> List[Dict[str, Any]]:
        """Get UN SDG alignment."""
        sdgs = [
            {"sdg": 7, "name": "Affordable and Clean Energy", "progress": 65},
            {"sdg": 12, "name": "Responsible Consumption and Production", "progress": 55},
            {"sdg": 13, "name": "Climate Action", "progress": 70},
            {"sdg": 6, "name": "Clean Water and Sanitation", "progress": 80},
            {"sdg": 15, "name": "Life on Land", "progress": 45},
        ]
        return sdgs


# ---------------------------------------------------------------------------
# Main Demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)
    print("=" * 70)
    print("Sustainability Agent - Comprehensive Demo")
    print("=" * 70)

    agent = SustainabilityAgent()

    # Track emissions
    agent.track_emission(
        SustainabilityCategory.ENERGY, CarbonScope.SCOPE_1,
        "Natural Gas", 5000, "m³", location="HQ"
    )
    agent.track_emission(
        SustainabilityCategory.ENERGY, CarbonScope.SCOPE_2,
        "Electricity", 100000, "kWh", location="HQ"
    )
    agent.track_emission(
        SustainabilityCategory.TRANSPORTATION, CarbonScope.SCOPE_3,
        "Business Travel", 50000, "km", location="Multiple"
    )

    # Set goals
    agent.set_sustainability_goal(
        "Net Zero by 2030",
        "Achieve net-zero carbon emissions",
        SustainabilityCategory.ENERGY,
        baseline=5000,
        target=0,
        target_year=2030,
    )

    # Create initiatives
    agent.initiatives.create_initiative(
        "Solar Panel Installation",
        "Install solar panels on HQ roof",
        SustainabilityCategory.ENERGY,
        investment=150000,
        expected_savings={"annual": 25000},
        carbon_reduction=120,
        timeline_months=6,
    )

    # Add suppliers
    agent.supply_chain.add_supplier(
        "Green Materials Co",
        SupplyChainTier.TIER_1,
        "Germany",
        "Raw Materials",
        sustainability_score=85,
        certifications=["ISO 14001", "FSC"],
        carbon_footprint=50,
    )

    # Add products
    agent.circular_economy.add_product(
        "EcoWidget",
        "Consumer Electronics",
        {"aluminum": 40, "plastic": 30, "glass": 30},
        recyclable_pct=85,
        recycled_content_pct=25,
        carbon_footprint=12.5,
        design_for_disassembly=True,
        take_back_program=True,
    )

    # Resource tracking
    agent.resources.add_water_usage("HQ", WaterSource.MUNICIPAL, 500, datetime.utcnow())
    agent.resources.add_waste_record("HQ", WasteType.RECYCLABLE, 200, datetime.utcnow(), recycled_pct=95)
    agent.resources.add_energy_record("HQ", EnergySource.SOLAR, 5000, datetime.utcnow(), renewable_pct=100)

    # Compliance
    agent.compliance.add_requirement(
        ComplianceFramework.EU_CSRD,
        "Annual sustainability reporting",
        due_date=datetime(2025, 12, 31),
    )

    # Generate dashboard
    dashboard = agent.get_sustainability_dashboard()
    print(f"\nDashboard: {dashboard['esg_score']}")

    # Generate annual report
    report = agent.generate_annual_report()
    print(f"\nAnnual Report - Carbon: {report['carbon_footprint']['total_emission_tonnes']} tonnes")

    print("\n" + "=" * 70)
    print("Sustainability Agent demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
