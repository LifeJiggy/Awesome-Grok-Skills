"""
Carbon Tracking Module
Scope 1/2/3 emissions calculation, GHG Protocol compliance, carbon credit
management, reduction target tracking, and carbon accounting API integration.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums & Constants
# ---------------------------------------------------------------------------

class Scope3Category(Enum):
    """GHG Protocol Scope 3 emission categories (15 total)."""
    PURCHASED_GOODS = 1
    CAPITAL_GOODS = 2
    FUEL_AND_ENERGY = 3
    UPSTREAM_TRANSPORT = 4
    WASTE_FROM_OPS = 5
    BUSINESS_TRAVEL = 6
    EMPLOYEE_COMMUTING = 7
    UPSTREAM_LEASED = 8
    DOWNSTREAM_TRANSPORT = 9
    PROCESSING_OF_SOLD = 10
    USE_OF_SOLD = 11
    END_OF_LIFE = 12
    DOWNSTREAM_LEASED = 13
    FRANCHISES = 14
    INVESTMENTS = 15


class Scope3Method(Enum):
    """Calculation methods for Scope 3 emissions."""
    ACTIVITY_BASED = "activity_based"
    SPEND_BASED = "spend_based"
    AVERAGE_DATA = "average_data"
    SUPPLIER_SPECIFIC = "supplier_specific"
    HYBRID = "hybrid"


class EmissionBoundary(Enum):
    """Organizational boundary methods per GHG Protocol."""
    OPERATIONAL_CONTROL = "operational_control"
    EQUITY_SHARE = "equity_share"
    FINANCIAL_CONTROL = "financial_control"


class Scope2Method(Enum):
    """Scope 2 calculation methods."""
    LOCATION_BASED = "location_based"
    MARKET_BASED = "market_based"


class CarbonCreditStandard(Enum):
    """Carbon credit registries and standards."""
    VERRA_VCS = "verra_vcs"
    GOLD_STANDARD = "gold_standard"
    ACR = "acr"
    CAR = "car"
    PLAN_VIVO = "plan_vivo"
    CDM = "cdm"


class DataQuality(Enum):
    """GHG Protocol data quality levels (1=best, 5=worst)."""
    SUPPLIER_SPECIFIC = 1
    ACTIVITY_BASED = 2
    AVERAGE_DATA = 3
    SPEND_BASED = 4
    ESTIMATE = 5


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class EmissionRecord:
    """A single emission calculation record."""
    scope: int
    category: str
    source: str
    activity_data: float
    unit: str
    emission_factor: float
    factor_unit: str
    emissions_kgCO2e: float
    data_quality: str = "activity_based"
    source_dataset: str = ""
    region: str = ""
    year: int = 2025

    @property
    def emissions_tonnes(self) -> float:
        return self.emissions_kgCO2e / 1000.0


@dataclass
class CarbonCredit:
    """A carbon credit from a specific project and registry."""
    credits: float
    standard: CarbonCreditStandard
    project: str
    vintage: int
    price_per_tonne: float
    registry_id: str
    purchase_date: str = ""
    retired: bool = False
    retired_date: str = ""
    retired_for: str = ""

    @property
    def total_cost(self) -> float:
        return self.credits * self.price_per_tonne

    @property
    def is_retired(self) -> bool:
        return self.retired


@dataclass
class RetirementRecord:
    """Record of a carbon credit retirement."""
    credits: float
    standard: CarbonCreditStandard
    project: str
    vintage: int
    registry_id: str
    retired_for: str
    retirement_date: str
    reason: str


@dataclass
class ReductionProgress:
    """Progress toward an emissions reduction target."""
    base_year: int
    base_emissions_tonnes: float
    target_year: int
    target_reduction_percent: float
    current_year: int
    current_emissions_tonnes: float

    @property
    def target_emissions_tonnes(self) -> float:
        return self.base_emissions_tonnes * (1 - self.target_reduction_percent / 100)

    @property
    def percent_reduced(self) -> float:
        if self.base_emissions_tonnes <= 0:
            return 0.0
        reduction = self.base_emissions_tonnes - self.current_emissions_tonnes
        return max(0.0, reduction / self.base_emissions_tonnes * 100)

    @property
    def on_track(self) -> bool:
        years_elapsed = self.current_year - self.base_year
        years_total = self.target_year - self.base_year
        if years_total <= 0 or years_elapsed <= 0:
            return True
        expected_reduction = self.target_reduction_percent * (years_elapsed / years_total)
        return self.percent_reduced >= expected_reduction * 0.9  # 10% tolerance

    @property
    def annual_reduction_needed_tonnes(self) -> float:
        years_remaining = max(1, self.target_year - self.current_year)
        remaining_reduction = self.current_emissions_tonnes - self.target_emissions_tonnes
        return max(0.0, remaining_reduction / years_remaining)


@dataclass
class GHGReport:
    """Complete GHG emissions report."""
    reporting_entity: str
    fiscal_year: int
    scope1_total_tonnes: float
    scope2_total_tonnes: float
    scope2_market_total_tonnes: float
    scope3_total_tonnes: float
    scope3_by_category: dict[int, float]
    grand_total_tonnes: float
    records: list[EmissionRecord]
    boundary: EmissionBoundary = EmissionBoundary.OPERATIONAL_CONTROL

    @property
    def scope1_percent(self) -> float:
        if self.grand_total_tonnes <= 0:
            return 0.0
        return self.scope1_total_tonnes / self.grand_total_tonnes * 100

    @property
    def intensity_per_revenue(self) -> float:
        return self.grand_total_tonnes  # Caller divides by revenue


# ---------------------------------------------------------------------------
# Emission Factor Database
# ---------------------------------------------------------------------------

class EmissionFactorDB:
    """
    Database of emission factors from EPA, DEFRA, IEA, and IPCC sources.
    Provides lookup by source type, region, and year.
    """

    # Default emission factors (kgCO2e per unit)
    FACTORS = {
        "natural_gas_therm": 5.301,
        "natural_gas_m3": 2.021,
        "diesel_gallon": 10.21,
        "gasoline_gallon": 8.887,
        "propane_gallon": 5.724,
        "coal_short_ton": 2088.0,
        "electricity_us_kwh": 0.417,
        "electricity_eu_kwh": 0.296,
        "electricity_cn_kwh": 0.581,
        "electricity_uk_kwh": 0.233,
        "flight_short_haul_km": 0.255,
        "flight_long_haul_km": 0.195,
        "car_km": 0.171,
        "bus_km": 0.089,
        "train_km": 0.041,
        "ship_freight_tkm": 0.016,
    }

    def __init__(self):
        self._custom_factors: dict[str, float] = {}

    def lookup(self, key: str) -> float:
        """Look up an emission factor by key."""
        if key in self._custom_factors:
            return self._custom_factors[key]
        if key in self.FACTORS:
            return self.FACTORS[key]
        raise KeyError(f"Emission factor '{key}' not found. Available: {list(self.FACTORS.keys())[:5]}...")

    def add_factor(self, key: str, value: float, source: str = "custom") -> None:
        """Add a custom emission factor."""
        if value < 0:
            raise ValueError("Emission factor cannot be negative")
        self._custom_factors[key] = value

    def available_factors(self) -> list[str]:
        """List all available emission factor keys."""
        return sorted(set(list(self.FACTORS.keys()) + list(self._custom_factors.keys())))


# ---------------------------------------------------------------------------
# GHG Calculator
# ---------------------------------------------------------------------------

class GHGCalculator:
    """
    Full GHG Protocol calculator supporting Scope 1, 2, and 3 emissions.
    Supports multiple boundary methods and calculation approaches.
    """

    def __init__(
        self,
        fiscal_year: int = 2025,
        reporting_entity: str = "",
        boundary: EmissionBoundary = EmissionBoundary.OPERATIONAL_CONTROL
    ):
        self.fiscal_year = fiscal_year
        self.reporting_entity = reporting_entity
        self.boundary = boundary
        self._records: list[EmissionRecord] = []
        self._factor_db = EmissionFactorDB()

    def add_scope1(
        self,
        category: str,
        source: str,
        activity_data: float,
        unit: str,
        emission_factor: float,
        source_dataset: str = "",
        region: str = "US"
    ) -> EmissionRecord:
        """Add a Scope 1 (direct) emission record."""
        emissions = activity_data * emission_factor
        record = EmissionRecord(
            scope=1,
            category=category,
            source=source,
            activity_data=activity_data,
            unit=unit,
            emission_factor=emission_factor,
            factor_unit=f"kgCO2e/{unit}",
            emissions_kgCO2e=emissions,
            source_dataset=source_dataset,
            region=region,
            year=self.fiscal_year
        )
        self._records.append(record)
        return record

    def add_scope2(
        self,
        category: str,
        source: str,
        activity_data: float,
        unit: str,
        grid_emission_factor: float,
        method: str = "location_based",
        source_dataset: str = "",
        region: str = "US",
        market_factor: Optional[float] = None
    ) -> EmissionRecord:
        """Add a Scope 2 (indirect electricity) emission record."""
        emissions = activity_data * grid_emission_factor
        record = EmissionRecord(
            scope=2,
            category=category,
            source=source,
            activity_data=activity_data,
            unit=unit,
            emission_factor=grid_emission_factor,
            factor_unit=f"kgCO2e/{unit}",
            emissions_kgCO2e=emissions,
            data_quality=method,
            source_dataset=source_dataset,
            region=region,
            year=self.fiscal_year
        )
        self._records.append(record)
        return record

    def add_scope3(
        self,
        category: Scope3Category,
        source: str,
        activity_data: float = 0.0,
        unit: str = "",
        emission_factor: float = 0.0,
        spend_usd: float = 0.0,
        spend_factor: float = 0.0,
        data_quality: str = "activity_based",
        region: str = "US"
    ) -> EmissionRecord:
        """Add a Scope 3 (value chain) emission record."""
        if activity_data > 0 and emission_factor > 0:
            emissions = activity_data * emission_factor
        elif spend_usd > 0 and spend_factor > 0:
            emissions = spend_usd * spend_factor
            unit = "USD"
        else:
            raise ValueError("Provide either (activity_data + emission_factor) or (spend_usd + spend_factor)")

        record = EmissionRecord(
            scope=3,
            category=f"category_{category.value}",
            source=source,
            activity_data=activity_data if activity_data > 0 else spend_usd,
            unit=unit,
            emission_factor=emission_factor if emission_factor > 0 else spend_factor,
            factor_unit=f"kgCO2e/{unit}",
            emissions_kgCO2e=emissions,
            data_quality=data_quality,
            region=region,
            year=self.fiscal_year
        )
        self._records.append(record)
        return record

    def generate_report(self) -> GHGReport:
        """Generate a complete GHG emissions report."""
        scope1 = sum(r.emissions_kgCO2e for r in self._records if r.scope == 1)
        scope2 = sum(r.emissions_kgCO2e for r in self._records if r.scope == 2)
        scope3 = sum(r.emissions_kgCO2e for r in self._records if r.scope == 3)

        scope3_by_cat: dict[int, float] = {}
        for r in self._records:
            if r.scope == 3:
                cat_num = int(r.category.replace("category_", ""))
                scope3_by_cat[cat_num] = scope3_by_cat.get(cat_num, 0) + r.emissions_kgCO2e

        total = scope1 + scope2 + scope3

        return GHGReport(
            reporting_entity=self.reporting_entity,
            fiscal_year=self.fiscal_year,
            scope1_total_tonnes=round(scope1 / 1000, 2),
            scope2_total_tonnes=round(scope2 / 1000, 2),
            scope2_market_total_tonnes=round(scope2 / 1000, 2),  # Simplified
            scope3_total_tonnes=round(scope3 / 1000, 2),
            scope3_by_category={k: round(v / 1000, 2) for k, v in scope3_by_cat.items()},
            grand_total_tonnes=round(total / 1000, 2),
            records=self._records,
            boundary=self.boundary
        )


# ---------------------------------------------------------------------------
# Carbon Credit Registry
# ---------------------------------------------------------------------------

class CarbonCreditRegistry:
    """
    Manages carbon credit purchases, inventory, and retirements across
    multiple standards and registries.
    """

    def __init__(self):
        self._credits: list[CarbonCredit] = []
        self._retirements: list[RetirementRecord] = []

    def purchase(
        self,
        credits: float,
        standard: str,
        project: str,
        vintage: int,
        price_per_tonne: float,
        registry_id: str
    ) -> CarbonCredit:
        """Record a carbon credit purchase."""
        if credits <= 0:
            raise ValueError("Credits must be positive")
        if price_per_tonne < 0:
            raise ValueError("Price cannot be negative")

        credit = CarbonCredit(
            credits=credits,
            standard=CarbonCreditStandard(standard),
            project=project,
            vintage=vintage,
            price_per_tonne=price_per_tonne,
            registry_id=registry_id,
            purchase_date=date.today().isoformat()
        )
        self._credits.append(credit)
        return credit

    def retire(
        self,
        credits: float,
        standard: str,
        retired_for: str,
        reason: str = "offset"
    ) -> RetirementRecord:
        """Retire credits against emissions (FIFO by vintage)."""
        available = [c for c in self._credits
                     if c.standard.value == standard and not c.retired]
        if not available:
            raise ValueError(f"No unretired {standard} credits available")

        # Sort by vintage (oldest first)
        available.sort(key=lambda c: c.vintage)

        remaining = credits
        retired_credits = []
        for credit in available:
            if remaining <= 0:
                break
            retire_amount = min(remaining, credit.credits)
            credit.credits -= retire_amount
            remaining -= retire_amount
            retired_credits.append((credit, retire_amount))

        if remaining > 0:
            raise ValueError(f"Insufficient {standard} credits: needed {credits}, available {credits - remaining}")

        # Create retirement record for the first credit (simplified)
        first_credit = retired_credits[0][0]
        record = RetirementRecord(
            credits=credits,
            standard=CarbonCreditStandard(standard),
            project=first_credit.project,
            vintage=first_credit.vintage,
            registry_id=first_credit.registry_id,
            retired_for=retired_for,
            retirement_date=date.today().isoformat(),
            reason=reason
        )
        self._retirements.append(record)

        # Mark fully depleted credits as retired
        for credit, amount in retired_credits:
            if credit.credits <= 0.001:
                credit.retired = True
                credit.retired_date = date.today().isoformat()
                credit.retired_for = retired_for

        return record

    def balance(self, standard: Optional[str] = None) -> float:
        """Get total unretired credit balance."""
        credits = self._credits
        if standard:
            credits = [c for c in credits if c.standard.value == standard]
        return sum(c.credits for c in credits if not c.retired)

    def portfolio_summary(self) -> dict:
        """Summary of credit portfolio."""
        by_standard = {}
        total_cost = 0.0
        for credit in self._credits:
            std = credit.standard.value
            if std not in by_standard:
                by_standard[std] = {"purchased": 0, "retired": 0, "balance": 0}
            by_standard[std]["purchased"] += credit.credits
            if credit.retired:
                by_standard[std]["retired"] += credit.credits
            else:
                by_standard[std]["balance"] += credit.credits
            total_cost += credit.total_cost

        return {
            "by_standard": by_standard,
            "total_purchased": sum(c["purchased"] for c in by_standard.values()),
            "total_retired": sum(c["retired"] for c in by_standard.values()),
            "total_balance": sum(c["balance"] for c in by_standard.values()),
            "total_cost_usd": round(total_cost, 2),
            "retirement_count": len(self._retirements)
        }


# ---------------------------------------------------------------------------
# Reduction Target Tracker
# ---------------------------------------------------------------------------

class ReductionTracker:
    """
    Tracks emissions reduction progress against science-based or custom targets.
    Supports SBTi 1.5°C and well-below 2°C pathways.
    """

    def __init__(
        self,
        base_year: int = 2020,
        base_emissions_tonnes: float = 50000.0,
        target_reduction_percent: float = 50.0,
        target_year: int = 2030
    ):
        self.base_year = base_year
        self.base_emissions = base_emissions_tonnes
        self.target_reduction = target_reduction_percent
        self.target_year = target_year
        self._annual_data: dict[int, float] = {}

    def record_annual_emissions(self, year: int, emissions_tonnes: float) -> None:
        """Record annual emissions for a given year."""
        if year < self.base_year:
            raise ValueError(f"Year {year} is before base year {self.base_year}")
        self._annual_data[year] = emissions_tonnes

    def calculate_progress(self, current_year: int, current_emissions: float) -> ReductionProgress:
        """Calculate progress toward the reduction target."""
        return ReductionProgress(
            base_year=self.base_year,
            base_emissions_tonnes=self.base_emissions,
            target_year=self.target_year,
            target_reduction_percent=self.target_reduction,
            current_year=current_year,
            current_emissions_tonnes=current_emissions
        )

    def sbti_pathway(self, year: int) -> float:
        """Calculate expected emissions at a given year under SBTi linear pathway."""
        if year <= self.base_year:
            return self.base_emissions
        if year >= self.target_year:
            return self.base_emissions * (1 - self.target_reduction / 100)

        years_fraction = (year - self.base_year) / (self.target_year - self.base_year)
        return self.base_emissions * (1 - self.target_reduction / 100 * years_fraction)

    def historical_trend(self) -> dict:
        """Analyze historical emissions trend."""
        if len(self._annual_data) < 2:
            return {"trend": "insufficient_data", "years": len(self._annual_data)}

        years = sorted(self._annual_data.keys())
        first_val = self._annual_data[years[0]]
        last_val = self._annual_data[years[-1]]
        total_change = (last_val - first_val) / first_val * 100 if first_val > 0 else 0

        return {
            "trend": "decreasing" if last_val < first_val else "increasing",
            "years": len(years),
            "first_year": years[0],
            "last_year": years[-1],
            "total_change_percent": round(total_change, 1),
            "annual_data": {str(y): round(v, 1) for y, v in self._annual_data.items()}
        }

    def projection(self, current_year: int, current_emissions: float, annual_reduction_rate: float) -> dict:
        """Project future emissions given a constant annual reduction rate."""
        projections = {}
        emissions = current_emissions
        for year in range(current_year + 1, self.target_year + 1):
            emissions *= (1 - annual_reduction_rate / 100)
            projections[year] = round(emissions, 1)

        target = self.sbti_pathway(self.target_year)
        meets_target = emissions <= target * 1.05  # 5% tolerance

        return {
            "projections": projections,
            "projected_end_emissions": round(emissions, 1),
            "sbti_target_emissions": round(target, 1),
            "meets_target": meets_target,
            "required_rate": round(
                (current_emissions - target) / current_emissions * 100 /
                max(1, self.target_year - current_year), 2
            )
        }


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main():
    """Demonstrate Carbon Tracking capabilities."""
    print("=" * 60)
    print("Carbon Tracking Module Demo")
    print("=" * 60)

    # 1. GHG Emissions Calculation
    print("\n--- GHG Emissions Calculation ---")
    calc = GHGCalculator(fiscal_year=2025, reporting_entity="Acme Corp")

    # Scope 1
    calc.add_scope1("stationary_combustion", "Natural gas boilers", 50000, "therms", 5.301)
    calc.add_scope1("mobile_combustion", "Company fleet", 1200000, "miles", 0.352)
    calc.add_scope1("process_emissions", "Chemical processes", 2000, "tonnes", 1.5)

    # Scope 2
    calc.add_scope2("purchased_electricity", "US operations", 8500000, "kWh", 0.417)
    calc.add_scope2("purchased_steam", "District heating", 500, "MWh", 100.0)

    # Scope 3
    calc.add_scope3(Scope3Category.PURCHASED_GOODS, "Raw materials",
                    spend_usd=12_000_000, spend_factor=0.45)
    calc.add_scope3(Scope3Category.BUSINESS_TRAVEL, "Air travel",
                    activity_data=250000, unit="passenger-miles", emission_factor=0.255)
    calc.add_scope3(Scope3Category.UPSTREAM_TRANSPORT, "Inbound freight",
                    activity_data=500000, unit="tonne-km", emission_factor=0.016)

    report = calc.generate_report()
    print(f"  Scope 1: {report.scope1_total_tonnes:>10,.1f} tCO2e ({report.scope1_percent:.1f}%)")
    print(f"  Scope 2: {report.scope2_total_tonnes:>10,.1f} tCO2e")
    print(f"  Scope 3: {report.scope3_total_tonnes:>10,.1f} tCO2e")
    print(f"  Total:   {report.grand_total_tonnes:>10,.1f} tCO2e")

    # 2. Carbon Credit Management
    print("\n--- Carbon Credit Portfolio ---")
    registry = CarbonCreditRegistry()
    registry.purchase(5000, "verra_vcs", "wind_farm_india", 2024, 12.50, "VCS-2024-1234")
    registry.purchase(2000, "gold_standard", "cookstoves_kenya", 2024, 18.00, "GS-2024-5678")
    registry.purchase(3000, "verra_vcs", "reforestation_brazil", 2023, 15.00, "VCS-2023-9012")

    retirement = registry.retire(3000, "verra_vcs", "Acme Corp FY2025")
    print(f"  Retired: {retirement.credits} credits from {retirement.project}")
    summary = registry.portfolio_summary()
    print(f"  Total balance: {summary['total_balance']:,.0f} credits")
    print(f"  Total cost: ${summary['total_cost_usd']:,.2f}")
    print(f"  Verra balance: {summary['by_standard']['verra_vcs']['balance']:,.0f}")

    # 3. Reduction Target Tracking
    print("\n--- Reduction Target Tracker ---")
    tracker = ReductionTracker(base_year=2020, base_emissions_tonnes=50000,
                                target_reduction_percent=50, target_year=2030)
    tracker.record_annual_emissions(2020, 50000)
    tracker.record_annual_emissions(2021, 47500)
    tracker.record_annual_emissions(2022, 44000)
    tracker.record_annual_emissions(2023, 41000)
    tracker.record_annual_emissions(2024, 38500)

    progress = tracker.calculate_progress(current_year=2025, current_emissions=38000)
    print(f"  Base: {progress.base_emissions_tonnes:,.0f} tCO2e ({progress.base_year})")
    print(f"  Current: {progress.current_emissions_tonnes:,.0f} tCO2e ({progress.current_year})")
    print(f"  Target: {progress.target_emissions_tonnes:,.0f} tCO2e ({progress.target_year})")
    print(f"  Reduced: {progress.percent_reduced:.1f}%")
    print(f"  On track: {progress.on_track}")
    print(f"  Annual reduction needed: {progress.annual_reduction_needed_tonnes:.0f} tCO2e")

    # Projection
    proj = tracker.projection(2025, 38000, 5.0)
    print(f"  At 5%/yr reduction -> {proj['projected_end_emissions']:,.0f} tCO2e by {tracker.target_year}")
    print(f"  Meets SBTi target: {proj['meets_target']}")

    # 4. Emission Factor DB
    print("\n--- Emission Factor Database ---")
    db = EmissionFactorDB()
    for key in ["natural_gas_therm", "electricity_us_kwh", "flight_short_haul_km"]:
        print(f"  {key}: {db.lookup(key)} kgCO2e/unit")

    print("\n" + "=" * 60)
    print("Demo complete.")


if __name__ == "__main__":
    main()
