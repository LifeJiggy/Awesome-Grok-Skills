"""
Carbon Tracking Module
GHG emissions calculation, Scope 1/2/3 accounting, reduction tracking, and reporting.
"""

from __future__ import annotations

import json
import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class GHGProtocol(Enum):
    SCOPE_1 = "scope_1"
    SCOPE_2 = "scope_2"
    SCOPE_3 = "scope_3"


class Scope3Category(Enum):
    PURCHASED_GOODS = "purchased_goods_services"
    CAPITAL_GOODS = "capital_goods"
    FUEL_ENERGY = "fuel_energy_activities"
    TRANSPORTATION = "transportation_distribution"
    WASTE = "waste_operations"
    BUSINESS_TRAVEL = "business_travel"
    EMPLOYEE_COMMUTING = "employee_commuting"
    UPSTREAM_LEASING = "upstream_leased_assets"
    DOWNSTREAM_TRANSPORT = "downstream_transportation"
    PROCESSING = "processing_sold_products"
    USE_OF_SOLD = "use_of_sold_products"
    END_OF_LIFE = "end_of_life_treatment"
    DOWNSTREAM_LEASING = "downstream_leased_assets"
    FRANCHISES = "franchises"
    INVESTMENTS = "investments"


class OffsetType(Enum):
    REFORESTATION = "reforestation"
    AFFORESTATION = "afforestation"
    WIND = "wind_energy"
    SOLAR = "solar_energy"
    METHANE_CAPTURE = "methane_capture"
    COOKSTOVE = "cookstove"
    DIRECT_AIR_CAPTURE = "direct_air_capture"


class OffsetQuality(Enum):
    GOLD_STANDARD = "gold_standard"
    VERIFIED_CARBON_STANDARD = "vcs"
    CARBON_RESTORATION_CERT = "crc"
    ACR = "acr"
    OTHER = "other"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class EmissionsFactor:
    """Emissions factor record."""
    fuel_type: str
    region: str
    factor: float
    unit: str
    source: str = "EPA"
    year: int = 2024
    scope: GHGProtocol = GHGProtocol.SCOPE_1

    @property
    def factor_kg(self) -> float:
        if "kg" in self.unit:
            return self.factor
        elif "lb" in self.unit:
            return self.factor * 0.453592
        return self.factor


@dataclass
class EmissionsResult:
    """Emissions calculation result."""
    scope: GHGProtocol
    emissions_tonnes: float
    category: str = ""
    fuel_type: str = ""
    region: str = ""
    method: str = "direct"
    activity_data: float = 0.0
    emission_factor: float = 0.0
    uncertainty_pct: float = 5.0


@dataclass
class CarbonFootprint:
    """Total organizational carbon footprint."""
    org_name: str
    year: int = 2024
    scope1: float = 0.0
    scope2: float = 0.0
    scope3: float = 0.0
    offsets: float = 0.0
    scopes: List[EmissionsResult] = field(default_factory=list)

    def total_emissions(self) -> float:
        return self.scope1 + self.scope2 + self.scope3

    def net_emissions(self) -> float:
        return self.total_emissions() - self.offsets

    def add_scope(self, result: EmissionsResult) -> None:
        self.scopes.append(result)
        if result.scope == GHGProtocol.SCOPE_1:
            self.scope1 += result.emissions_tonnes
        elif result.scope == GHGProtocol.SCOPE_2:
            self.scope2 += result.emissions_tonnes
        elif result.scope == GHGProtocol.SCOPE_3:
            self.scope3 += result.emissions_tonnes


@dataclass
class ReductionProgress:
    """Emission reduction progress."""
    baseline_year: int
    baseline_emissions: float
    current_year: int
    current_emissions: float
    target_reduction_pct: float = 0.0
    reduction_pct: float = 0.0
    on_track: bool = False
    target_year: int = 2030


@dataclass
class OffsetCredit:
    """Carbon offset credit."""
    credit_id: str
    vintage: int
    project_type: OffsetType
    quality: OffsetQuality
    quantity: int
    retired: bool = False
    retired_date: Optional[datetime] = None
    retirement_reason: str = ""


@dataclass
class GHGReport:
    """GHG Protocol report."""
    org_name: str
    year: int
    scope1_total: float
    scope2_total: float
    scope3_total: float
    total_emissions: float
    offsets: float
    net_emissions: float
    categories: Dict[str, float] = field(default_factory=dict)
    methodology: str = "GHG Protocol Corporate Standard"


# ---------------------------------------------------------------------------
# Emissions Factor Database
# ---------------------------------------------------------------------------

class EmissionsFactorDB:
    """GHG emissions factor database."""

    FACTORS: Dict[str, Dict[str, EmissionsFactor]] = {
        "natural_gas": {
            "US": EmissionsFactor("natural_gas", "US", 5.3, "kgCO2/therm", "EPA"),
            "EU": EmissionsFactor("natural_gas", "EU", 2.0, "kgCO2/m3", "EEA"),
        },
        "diesel": {
            "US": EmissionsFactor("diesel", "US", 10.18, "kgCO2/gallon", "EPA"),
            "EU": EmissionsFactor("diesel", "EU", 2.68, "kgCO2/liter", "EEA"),
        },
        "gasoline": {
            "US": EmissionsFactor("gasoline", "US", 8.89, "kgCO2/gallon", "EPA"),
            "EU": EmissionsFactor("gasoline", "EU", 2.31, "kgCO2/liter", "EEA"),
        },
        "electricity": {
            "US": EmissionsFactor("electricity", "US", 0.4, "kgCO2/kWh", "EPA"),
            "EU": EmissionsFactor("electricity", "EU", 0.23, "kgCO2/kWh", "EEA"),
            "CN": EmissionsFactor("electricity", "CN", 0.58, "kgCO2/kWh", "IEA"),
            "IN": EmissionsFactor("electricity", "IN", 0.71, "kgCO2/kWh", "IEA"),
        },
        "coal": {
            "US": EmissionsFactor("coal", "US", 9.5, "kgCO2/kg", "EPA"),
        },
        "lpg": {
            "US": EmissionsFactor("lpg", "US", 5.76, "kgCO2/gallon", "EPA"),
        },
    }

    def get_factor(
        self, fuel_type: str, region: str = "US", activity: str = "combustion"
    ) -> EmissionsFactor:
        fuel = self.FACTORS.get(fuel_type, {})
        return fuel.get(region, EmissionsFactor(fuel_type, region, 0.0, "unknown", "default"))


# ---------------------------------------------------------------------------
# GHG Calculator
# ---------------------------------------------------------------------------

class GHGCalculator:
    """Calculate GHG emissions across scopes."""

    def __init__(self):
        self.db = EmissionsFactorDB()

    def calculate_scope1(
        self,
        fuel_type: str,
        quantity: float,
        unit: str = "therms",
        region: str = "US",
    ) -> EmissionsResult:
        factor = self.db.get_factor(fuel_type, region)
        if "therm" in unit.lower():
            emissions_kg = quantity * factor.factor
        elif "gallon" in unit.lower():
            emissions_kg = quantity * factor.factor
        elif "kg" in unit.lower():
            emissions_kg = quantity * factor.factor
        else:
            emissions_kg = quantity * factor.factor
        return EmissionsResult(
            scope=GHGProtocol.SCOPE_1,
            emissions_tonnes=round(emissions_kg / 1000, 4),
            category="fuel_combustion",
            fuel_type=fuel_type,
            region=region,
            activity_data=quantity,
            emission_factor=factor.factor,
        )

    def calculate_scope2(
        self,
        electricity_kwh: float,
        grid_factor: float = 0.4,
        method: str = "location",
        region: str = "US",
    ) -> EmissionsResult:
        emissions_kg = electricity_kwh * grid_factor
        return EmissionsResult(
            scope=GHGProtocol.SCOPE_2,
            emissions_tonnes=round(emissions_kg / 1000, 4),
            category="purchased_electricity",
            region=region,
            method=method,
            activity_data=electricity_kwh,
            emission_factor=grid_factor,
        )

    def calculate_scope3(
        self,
        category: str,
        distance_km: float = 0,
        passengers: int = 1,
        mode: str = "air",
        weight_tonnes: float = 0,
        spend_usd: float = 0,
    ) -> EmissionsResult:
        factors = {
            "air": 0.255,
            "rail": 0.041,
            "bus": 0.089,
            "car": 0.171,
            "truck": 0.096,
            "ship": 0.016,
        }
        factor = factors.get(mode, 0.1)
        emissions_kg = distance_km * passengers * factor
        return EmissionsResult(
            scope=GHGProtocol.SCOPE_3,
            emissions_tonnes=round(emissions_kg / 1000, 4),
            category=category,
            method="distance",
            activity_data=distance_km,
            emission_factor=factor,
        )


# ---------------------------------------------------------------------------
# Reduction Tracker
# ---------------------------------------------------------------------------

class ReductionTracker:
    """Track emissions reduction progress against targets."""

    def __init__(
        self,
        baseline_year: int = 2020,
        baseline_emissions: float = 50000,
        target_reduction_pct: float = 50,
        target_year: int = 2030,
    ):
        self.baseline_year = baseline_year
        self.baseline = baseline_emissions
        self.target_pct = target_reduction_pct
        self.target_year = target_year
        self._actuals: Dict[int, float] = {}

    def add_actual(self, year: int, emissions: float) -> None:
        self._actuals[year] = emissions

    def progress(self) -> ReductionProgress:
        current_year = max(self._actuals.keys()) if self._actuals else self.baseline_year
        current = self._actuals.get(current_year, self.baseline)
        reduction = (self.baseline - current) / max(self.baseline, 1) * 100
        years_left = self.target_year - current_year
        years_total = self.target_year - self.baseline_year
        expected = self.target_pct * (1 - years_left / max(years_total, 1))
        return ReductionProgress(
            baseline_year=self.baseline_year,
            baseline_emissions=self.baseline,
            current_year=current_year,
            current_emissions=current,
            target_reduction_pct=self.target_pct,
            reduction_pct=round(reduction, 1),
            on_track=reduction >= expected * 0.9,
            target_year=self.target_year,
        )

    def trajectory(self) -> List[Dict[str, float]]:
        trajectory: List[Dict[str, float]] = []
        for year in range(self.baseline_year, self.target_year + 1):
            if year in self._actuals:
                trajectory.append({"year": year, "emissions": self._actuals[year], "type": "actual"})
            else:
                progress = (year - self.baseline_year) / max(self.target_year - self.baseline_year, 1)
                projected = self.baseline * (1 - self.target_pct / 100 * progress)
                trajectory.append({"year": year, "emissions": round(projected, 1), "type": "projected"})
        return trajectory


# ---------------------------------------------------------------------------
# Offset Manager
# ---------------------------------------------------------------------------

class OffsetManager:
    """Manage carbon offset credits."""

    def __init__(self):
        self._credits: List[OffsetCredit] = []
        self._retired: List[OffsetCredit] = []

    def purchase(
        self,
        credits: int,
        vintage: int,
        project: str = "reforestation",
        quality: str = "gold_standard",
    ) -> OffsetCredit:
        credit = OffsetCredit(
            credit_id=f"OC-{secrets.token_hex(4).upper()}",
            vintage=vintage,
            project_type=OffsetType(project),
            quality=OffsetQuality(quality),
            quantity=credits,
        )
        self._credits.append(credit)
        return credit

    def retire(self, credits: int, reason: str = "") -> int:
        retired_count = 0
        for credit in self._credits:
            if credit.retired or retired_count >= credits:
                continue
            credit.retired = True
            credit.retired_date = datetime.now(timezone.utc)
            credit.retirement_reason = reason
            self._retired.append(credit)
            retired_count += credit.quantity
            if retired_count >= credits:
                break
        return retired_count

    def balance(self) -> int:
        return sum(c.quantity for c in self._credits if not c.retired)

    def total_retired(self) -> int:
        return sum(c.quantity for c in self._retired)


# ---------------------------------------------------------------------------
# Report Generator
# ---------------------------------------------------------------------------

class ReportGenerator:
    """Generate GHG emissions reports."""

    def generate_ghg_protocol(
        self, footprint: CarbonFootprint, year: int = 2024
    ) -> GHGReport:
        categories: Dict[str, float] = {}
        for scope in footprint.scopes:
            categories[f"{scope.scope.value}_{scope.category}"] = scope.emissions_tonnes
        return GHGReport(
            org_name=footprint.org_name,
            year=year,
            scope1_total=round(footprint.scope1, 2),
            scope2_total=round(footprint.scope2, 2),
            scope3_total=round(footprint.scope3, 2),
            total_emissions=round(footprint.total_emissions(), 2),
            offsets=round(footprint.offsets, 2),
            net_emissions=round(footprint.net_emissions(), 2),
            categories=categories,
        )

    def export_json(self, report: GHGReport, path: str) -> str:
        data = {
            "org": report.org_name,
            "year": report.year,
            "scope1": report.scope1_total,
            "scope2": report.scope2_total,
            "scope3": report.scope3_total,
            "total": report.total_emissions,
            "offsets": report.offsets,
            "net": report.net_emissions,
        }
        return json.dumps(data, indent=2)


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Carbon Tracking Demo")
    print("=" * 60)

    calc = GHGCalculator()
    print("\n[1] Scope 1 Emissions")
    s1 = calc.calculate_scope1("natural_gas", 10000, "therms", "US")
    print(f"  Natural gas: {s1.emissions_tonnes:.2f} tCO2e")

    print("\n[2] Scope 2 Emissions")
    s2 = calc.calculate_scope2(500000, 0.4, "market")
    print(f"  Electricity: {s2.emissions_tonnes:.2f} tCO2e")

    print("\n[3] Scope 3 Emissions")
    s3 = calc.calculate_scope3("business_travel", 100000, 50, "air")
    print(f"  Business travel: {s3.emissions_tonnes:.2f} tCO2e")

    print("\n[4] Carbon Footprint")
    fp = CarbonFootprint(org_name="TechCorp")
    fp.add_scope(s1)
    fp.add_scope(s2)
    fp.add_scope(s3)
    print(f"  Total: {fp.total_emissions():.2f} tCO2e")
    print(f"  Scope breakdown: 1={fp.scope1:.0f}, 2={fp.scope2:.0f}, 3={fp.scope3:.0f}")

    print("\n[5] Reduction Tracking")
    tracker = ReductionTracker(baseline_year=2020, baseline_emissions=50000)
    tracker.add_actual(2024, 42000)
    prog = tracker.progress()
    print(f"  Reduction: {prog.reduction_pct:.1f}%")
    print(f"  On track: {prog.on_track}")

    print("\n[6] Offsets")
    offsets = OffsetManager()
    offsets.purchase(1000, 2024, "reforestation")
    offsets.retire(500, "Scope 1 neutralization")
    print(f"  Balance: {offsets.balance()}")
    print(f"  Retired: {offsets.total_retired()}")

    print("\n[7] Reporting")
    reporter = ReportGenerator()
    report = reporter.generate_ghg_protocol(fp, 2024)
    print(f"  Net emissions: {report.net_emissions:.2f} tCO2e")

    print("\n" + "=" * 60)
    print("  Carbon tracking demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
