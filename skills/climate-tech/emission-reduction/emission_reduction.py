"""
Emission Reduction Module
Decarbonization pathways, MAC curves, carbon pricing, targets, and policy analysis.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Sector(Enum):
    POWER = "power"
    TRANSPORT = "transport"
    INDUSTRY = "industry"
    BUILDINGS = "buildings"
    AGRICULTURE = "agriculture"
    WASTE = "waste"
    LULUCF = "lulucf"


class PathwayType(Enum):
    NET_ZERO_2050 = "net_zero_2050"
    ONE_POINT_FIVE_C = "1.5C"
    TWO_C = "2C"
    CURRENT_POLICIES = "current_policies"


class PolicyInstrument(Enum):
    CARBON_TAX = "carbon_tax"
    ETS = "emissions_trading_system"
    REGULATION = "regulation"
    SUBSIDY = "subsidy"
    STANDARDS = "performance_standards"
    VOLUNTARY = "voluntary"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class MACMeasure:
    """Marginal Abatement Cost measure."""
    name: str
    reduction_tonnes: float
    cost_per_tonne: float
    sector: str = ""
    technology_readiness: float = 0.8
    co_benefits: List[str] = field(default_factory=list)
    implementation_time_years: int = 2


@dataclass
class DecarbonizationTrajectory:
    """Decarbonization pathway result."""
    baseline_emissions: float
    target_year: int
    target_reduction_pct: float
    total_cost: float = 0.0
    emissions_2030: float = 0.0
    emissions_2050: float = 0.0
    measures_applied: List[Dict[str, Any]] = field(default_factory=list)
    annual_reduction_rates: List[float] = field(default_factory=list)


@dataclass
class MACCRanking:
    """MACC curve ranking entry."""
    measure: str
    reduction: float
    cost: float
    cumulative_reduction: float = 0.0


@dataclass
class CarbonCost:
    """Carbon pricing cost result."""
    emissions: float
    carbon_price: float
    total_cost: float
    border_adjustment: float = 0.0
    net_cost: float = 0.0


@dataclass
class ScienceBasedTarget:
    """Science-based emission reduction target."""
    baseline_emissions: float
    baseline_year: int
    target_year: int
    required_reduction_pct: float
    annual_rate: float
    absolute_target: float
    pathway: str = "1.5C"
    scope_coverage: str = "scope_1_2_3"


@dataclass
class PolicyImpact:
    """Policy impact assessment."""
    policy_name: str
    abatement_potential: float = 0.0
    revenue: float = 0.0
    cost_to_business: float = 0.0
    gdp_impact_pct: float = 0.0
    employment_impact: int = 0
    co_benefits: List[str] = field(default_factory=list)


@dataclass
class ReductionMeasure:
    """Emission reduction measure."""
    name: str
    sector: str
    reduction_potential_tonnes: float
    cost_per_tonne: float
    implementation_years: int = 1
    technology_readiness: float = 0.8


# ---------------------------------------------------------------------------
# Decarbonization Pathway
# ---------------------------------------------------------------------------

class DecarbonizationPathway:
    """Model decarbonization pathways."""

    def __init__(
        self,
        baseline_emissions: float = 100000,
        target_year: int = 2050,
        target_reduction_pct: float = 100,
    ):
        self.baseline = baseline_emissions
        self.target_year = target_year
        self.target_pct = target_reduction_pct

    def model(
        self,
        measures: Optional[List[Dict[str, Any]]] = None,
        discount_rate: float = 0.06,
    ) -> DecarbonizationTrajectory:
        measures = measures or []
        total_reduction_pct = sum(m.get("reduction_pct", 0) for m in measures)
        total_reduction_pct = min(total_reduction_pct, self.target_pct)
        residual = self.baseline * (1 - total_reduction_pct / 100)
        years_to_target = self.target_year - 2024
        annual_rate = total_reduction_pct / max(years_to_target, 1) / 100

        total_cost = 0.0
        applied = []
        for m in measures:
            reduction = self.baseline * m.get("reduction_pct", 0) / 100
            cost = reduction * m.get("cost_per_tonne", 50)
            total_cost += cost
            applied.append({
                "name": m.get("name", "unknown"),
                "reduction_tonnes": round(reduction, 0),
                "cost": round(cost, 0),
            })

        em_2030 = self.baseline * (1 - annual_rate * 6)
        em_2050 = max(residual, 0)
        return DecarbonizationTrajectory(
            baseline_emissions=self.baseline,
            target_year=self.target_year,
            target_reduction_pct=self.target_pct,
            total_cost=round(total_cost, 0),
            emissions_2030=round(max(em_2030, 0), 0),
            emissions_2050=round(em_2050, 0),
            measures_applied=applied,
            annual_reduction_rates=[round(annual_rate * 100, 2)],
        )

    def interpolate_year(self, year: int, trajectory: DecarbonizationTrajectory) -> float:
        progress = (year - 2024) / max(self.target_year - 2024, 1)
        progress = min(max(progress, 0), 1)
        return self.baseline * (1 - trajectory.target_reduction_pct / 100 * progress)


# ---------------------------------------------------------------------------
# MAC Curve
# ---------------------------------------------------------------------------

class MACCurve:
    """Marginal Abatement Cost Curve."""

    def __init__(self):
        self._measures: List[MACMeasure] = []

    def add_measure(
        self,
        name: str,
        reduction: float,
        cost_per_tonne: float,
        sector: str = "",
    ) -> None:
        self._measures.append(MACMeasure(
            name=name,
            reduction_tonnes=reduction,
            cost_per_tonne=cost_per_tonne,
            sector=sector,
        ))

    def rank_measures(self) -> List[Dict[str, Any]]:
        sorted_m = sorted(self._measures, key=lambda m: m.cost_per_tonne)
        cumulative = 0.0
        ranking: List[Dict[str, Any]] = []
        for m in sorted_m:
            cumulative += m.reduction_tonnes
            ranking.append({
                "measure": m.name,
                "reduction": m.reduction_tonnes,
                "cost": m.cost_per_tonne,
                "cumulative": round(cumulative, 0),
                "sector": m.sector,
            })
        return ranking

    def total_reduction(self) -> float:
        return sum(m.reduction_tonnes for m in self._measures)

    def total_cost(self) -> float:
        return sum(m.reduction_tonnes * m.cost_per_tonne for m in self._measures)

    def below_threshold(self, cost_threshold: float = 0) -> List[MACMeasure]:
        return [m for m in self._measures if m.cost_per_tonne <= cost_threshold]

    def cost_effective_portfolio(self, budget: float) -> List[MACMeasure]:
        sorted_m = sorted(self._measures, key=lambda m: m.cost_per_tonne)
        portfolio: List[MACMeasure] = []
        remaining = budget
        for m in sorted_m:
            cost = m.reduction_tonnes * m.cost_per_tonne
            if cost <= remaining:
                portfolio.append(m)
                remaining -= cost
        return portfolio


# ---------------------------------------------------------------------------
# Carbon Pricing Model
# ---------------------------------------------------------------------------

class CarbonPricingModel:
    """Carbon pricing and cost modeling."""

    def calculate_carbon_cost(
        self,
        emissions: float,
        carbon_price: float = 50,
        border_adjustment: bool = False,
        border_rate: float = 0.1,
    ) -> CarbonCost:
        base_cost = emissions * carbon_price
        bat = base_cost * border_rate if border_adjustment else 0
        return CarbonCost(
            emissions=emissions,
            carbon_price=carbon_price,
            total_cost=round(base_cost, 0),
            border_adjustment=round(bat, 0),
            net_cost=round(base_cost + bat, 0),
        )

    def breakeven_analysis(
        self,
        abatement_cost: float,
        carbon_price: float,
    ) -> Dict[str, float]:
        if carbon_price <= 0:
            return {"breakeven_price": abatement_cost, "years_to_breakeven": 999}
        years = abatement_cost / carbon_price
        return {
            "breakeven_price": abatement_cost,
            "years_to_breakeven": round(years, 1),
        }

    def carbon_border_adjustment(
        self,
        import_value: float,
        embedded_emissions_tonnes: float,
        domestic_carbon_price: float,
    ) -> float:
        return embedded_emissions_tonnes * domestic_carbon_price

    def shadow_carbon_price(
        self,
        investment_cost: float,
        annual_emissions: float,
        project_lifetime: int = 20,
    ) -> float:
        if annual_emissions <= 0:
            return 0.0
        return investment_cost / (annual_emissions * project_lifetime)


# ---------------------------------------------------------------------------
# Target Setter
# ---------------------------------------------------------------------------

class TargetSetter:
    """Set science-based emission reduction targets."""

    PATHWAY_TARGETS = {
        "1.5C": {"2030": 42, "2040": 72, "2050": 100},
        "2C": {"2030": 25, "2040": 55, "2050": 90},
        "well_below_2C": {"2030": 30, "2040": 60, "2050": 95},
    }

    def set_target(
        self,
        baseline_emissions: float,
        baseline_year: int = 2020,
        target_year: int = 2030,
        sector: str = "cross_sector",
        pathway: str = "1.5C",
    ) -> ScienceBasedTarget:
        pathway_targets = self.PATHWAY_TARGETS.get(pathway, self.PATHWAY_TARGETS["1.5C"])
        target_str = str(min(target_year, 2050))
        for year_key in sorted(pathway_targets.keys()):
            if int(year_key) >= target_year:
                target_str = year_key
                break
        required_pct = pathway_targets.get(target_str, 50)
        years = target_year - baseline_year
        annual_rate = required_pct / max(years, 1)
        absolute_target = baseline_emissions * (1 - required_pct / 100)
        return ScienceBasedTarget(
            baseline_emissions=baseline_emissions,
            baseline_year=baseline_year,
            target_year=target_year,
            required_reduction_pct=required_pct,
            annual_rate=round(annual_rate, 2),
            absolute_target=round(absolute_target, 0),
            pathway=pathway,
        )

    def intermediate_milestones(
        self,
        baseline: float,
        target_reduction_pct: float,
        target_year: int = 2050,
    ) -> List[Dict[str, float]]:
        milestones: List[Dict[str, float]] = []
        for year in range(2025, target_year + 1, 5):
            progress = (year - 2024) / (target_year - 2024)
            reduction = target_reduction_pct * progress
            emissions = baseline * (1 - reduction / 100)
            milestones.append({
                "year": year,
                "reduction_pct": round(reduction, 1),
                "emissions": round(emissions, 0),
            })
        return milestones


# ---------------------------------------------------------------------------
# Policy Analyzer
# ---------------------------------------------------------------------------

class PolicyAnalyzer:
    """Analyze climate policy impacts."""

    def assess_policy(
        self,
        policy_name: str,
        carbon_price: float = 0,
        coverage_pct: float = 100,
        revenue_use: str = "general",
        sector: str = "cross_sector",
    ) -> PolicyImpact:
        baseline_emissions = 100000
        abatement_rate = min(carbon_price / 200, 0.5) * coverage_pct / 100
        abatement = baseline_emissions * abatement_rate
        revenue = abatement * carbon_price
        gdp_impact = -carbon_price * 0.00001 * coverage_pct
        employment = int(abatement * 0.005)
        co_benefits = ["reduced_air_pollution", "health_improvements", "energy_security"]
        if revenue_use == "dividend":
            co_benefits.append("progressive_benefit")
        return PolicyImpact(
            policy_name=policy_name,
            abatement_potential=round(abatement, 0),
            revenue=round(revenue, 0),
            gdp_impact_pct=round(gdp_impact, 3),
            employment_impact=employment,
            co_benefits=co_benefits,
        )

    def compare_policies(
        self, policies: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        results = []
        for p in policies:
            impact = self.assess_policy(**p)
            results.append({
                "policy": impact.policy_name,
                "abatement": impact.abatement_potential,
                "cost_efficiency": impact.revenue / max(impact.abatement_potential, 1),
            })
        return sorted(results, key=lambda x: x["cost_efficiency"])


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Emission Reduction Demo")
    print("=" * 60)

    print("\n[1] Decarbonization Pathway")
    pathway = DecarbonizationPathway(100000, 2050, 100)
    traj = pathway.model(measures=[
        {"name": "renewables", "reduction_pct": 30, "cost_per_tonne": 50},
        {"name": "efficiency", "reduction_pct": 15, "cost_per_tonne": 20},
        {"name": "electrification", "reduction_pct": 25, "cost_per_tonne": 80},
    ])
    print(f"  Total cost: ${traj.total_cost:,.0f}")
    print(f"  2030: {traj.emissions_2030:,.0f} tCO2e")
    print(f"  2050: {traj.emissions_2050:,.0f} tCO2e")

    print("\n[2] MAC Curve")
    macc = MACCurve()
    macc.add_measure("LED lighting", 5000, -20, "buildings")
    macc.add_measure("Solar PV", 25000, 30, "power")
    macc.add_measure("Heat pumps", 15000, 50, "buildings")
    ranking = macc.rank_measures()
    for m in ranking:
        print(f"  {m['measure']}: {m['reduction']:,.0f} t @ ${m['cost']:.0f}/t")

    print("\n[3] Carbon Pricing")
    pricing = CarbonPricingModel()
    cost = pricing.calculate_carbon_cost(50000, 75, border_adjustment=True)
    print(f"  Cost: ${cost.net_cost:,.0f}")

    print("\n[4] Science-Based Targets")
    setter = TargetSetter()
    target = setter.set_target(100000, 2020, 2030, pathway="1.5C")
    print(f"  Required: {target.required_reduction_pct:.0f}%")
    print(f"  Annual rate: {target.annual_rate:.1f}%")
    milestones = setter.intermediate_milestones(100000, 100)
    for m in milestones:
        print(f"    {m['year']}: {m['reduction_pct']:.0f}% ({m['emissions']:,.0f} t)")

    print("\n[5] Policy Analysis")
    analyzer = PolicyAnalyzer()
    impact = analyzer.assess_policy("Carbon Tax", carbon_price=50, coverage_pct=80)
    print(f"  Abatement: {impact.abatement_potential:,.0f} tCO2e")
    print(f"  Revenue: ${impact.revenue:,.0f}")

    print("\n" + "=" * 60)
    print("  Emission reduction demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
