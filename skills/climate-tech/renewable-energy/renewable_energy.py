"""
Renewable Energy Module
Solar, wind, storage, hydropower planning and economics.
"""

from __future__ import annotations

import logging
import math
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class StorageTechnology(Enum):
    LI_ION = "li_ion"
    LFP = "lfp"
    FLOW = "flow_batteries"
    PUMPED_HYDRO = "pumped_hydro"
    COMPRESSED_AIR = "compressed_air"
    HYDROGEN = "hydrogen"


class SolarTechnology(Enum):
    MONOCRYSTALLINE = "mono_si"
    POLYCRYSTALLINE = "poly_si"
    THIN_FILM = "thin_film"
    BIFACIAL = "bifacial"
    PEROVSKITE = "perovskite"


class WindTurbineClass(Enum):
    IEC_I = "class_1"
    IEC_II = "class_2"
    IEC_III = "class_3"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SolarResource:
    """Solar resource assessment."""
    ghi_kwh_m2: float = 0.0
    dni_kwh_m2: float = 0.0
    dhi_kwh_m2: float = 0.0
    peak_sun_hours: float = 0.0
    latitude: float = 0.0
    optimal_tilt: float = 0.0
    optimal_azimuth: float = 180.0


@dataclass
class SolarPerformance:
    """Solar system performance estimate."""
    annual_kwh: float = 0.0
    capacity_factor: float = 0.0
    performance_ratio: float = 0.0
    monthly_kwh: List[float] = field(default_factory=list)
    losses_breakdown: Dict[str, float] = field(default_factory=dict)


@dataclass
class WindResource:
    """Wind resource assessment."""
    mean_wind_speed_ms: float = 0.0
    power_density_w_m2: float = 0.0
    weibull_k: float = 2.0
    weibull_a: float = 0.0
    capacity_factor: float = 0.0
    turbulence_intensity: float = 0.0


@dataclass
class WindGeneration:
    """Wind generation estimate."""
    annual_mwh: float = 0.0
    capacity_factor: float = 0.0
    availability: float = 0.97
    wake_loss: float = 0.05
    electrical_loss: float = 0.02
    monthly_mwh: List[float] = field(default_factory=list)


@dataclass
class StorageCycle:
    """Battery cycle simulation."""
    efficiency: float = 0.0
    cycle_life: int = 0
    energy_throughput_kwh: float = 0.0
    degradation_per_cycle: float = 0.0


@dataclass
class StorageEconomics:
    """Storage economic analysis."""
    capex: float = 0.0
    annual_savings: float = 0.0
    payback_years: float = 0.0
    npv: float = 0.0
    irr: float = 0.0
    revenue_streams: Dict[str, float] = field(default_factory=dict)


@dataclass
class MicrogridSystem:
    """Optimized microgrid system."""
    solar_kw: float = 0.0
    storage_kwh: float = 0.0
    generator_kw: float = 0.0
    renewable_fraction: float = 0.0
    annual_cost: float = 0.0
    reliability_pct: float = 99.9
    annual_generation_kwh: float = 0.0
    annual_load_kwh: float = 0.0


@dataclass
class LCOEResult:
    """Levelized Cost of Energy."""
    lcoe: float = 0.0
    total_capex: float = 0.0
    total_opex: float = 0.0
    total_generation: float = 0.0


# ---------------------------------------------------------------------------
# Solar Planner
# ---------------------------------------------------------------------------

class SolarPlanner:
    """Solar PV system planning and performance estimation."""

    PV_EFFICIENCY = {
        SolarTechnology.MONOCRYSTALLINE: 0.20,
        SolarTechnology.POLYCRYSTALLINE: 0.17,
        SolarTechnology.THIN_FILM: 0.12,
        SolarTechnology.BIFACIAL: 0.21,
    }

    TEMPERATURE_COEFFICIENT = -0.004

    def __init__(
        self,
        location: Optional[Dict[str, float]] = None,
        system_capacity_kw: float = 100,
        technology: str = "mono_si",
        tilt_deg: Optional[float] = None,
        azimuth_deg: float = 180,
    ):
        self.location = location or {"lat": 35.0, "lon": -118.0}
        self.capacity_kw = system_capacity_kw
        self.tech = SolarTechnology(technology)
        self.tilt = tilt_deg if tilt_deg is not None else abs(self.location["lat"])
        self.azimuth = azimuth_deg

    def assess_resource(self) -> SolarResource:
        lat = abs(self.location["lat"])
        ghi = max(1800 - lat * 15, 800)
        dni = ghi * 1.3
        dhi = ghi * 0.45
        psh = ghi / 365
        optimal_tilt = lat * 0.76 + 3.1
        return SolarResource(
            ghi_kwh_m2=round(ghi, 1),
            dni_kwh_m2=round(dni, 1),
            dhi_kwh_m2=round(dhi, 1),
            peak_sun_hours=round(psh, 1),
            latitude=self.location["lat"],
            optimal_tilt=round(optimal_tilt, 1),
        )

    def estimate_performance(self) -> SolarPerformance:
        resource = self.assess_resource()
        efficiency = self.PV_EFFICIENCY.get(self.tech, 0.18)
        area_m2 = self.capacity_kw / (efficiency * 1.0)
        losses = {
            "temperature": 0.08,
            "soiling": 0.03,
            "mismatch": 0.02,
            "wiring": 0.02,
            "inverter": 0.03,
            "availability": 0.01,
        }
        total_loss = 1 - prod(losses.values())
        pr = 1 - sum(losses.values())
        annual = self.capacity_kw * resource.peak_sun_hours * 365 * pr
        cf = annual / (self.capacity_kw * 8760)
        monthly = [annual / 12 * (0.7 + 0.6 * math.sin(math.radians((m - 3) * 30))) for m in range(1, 13)]
        return SolarPerformance(
            annual_kwh=round(annual, 0),
            capacity_factor=round(cf, 3),
            performance_ratio=round(pr, 3),
            monthly_kwh=[round(m, 0) for m in monthly],
            losses_breakdown=losses,
        )

    def optimize_orientation(self) -> Dict[str, float]:
        resource = self.assess_resource()
        return {
            "optimal_tilt": resource.optimal_tilt,
            "optimal_azimuth": 180 if self.location["lat"] >= 0 else 0,
            "annual_gain_pct": 5.0,
        }


# ---------------------------------------------------------------------------
# Wind Planner
# ---------------------------------------------------------------------------

class WindPlanner:
    """Wind energy system planning."""

    AIR_DENSITY = 1.225

    def __init__(
        self,
        hub_height_m: float = 80,
        turbine_rating_kw: float = 3000,
        rotor_diameter_m: float = 120,
        cut_in_speed: float = 3.0,
        cut_out_speed: float = 25.0,
        rated_speed: float = 12.0,
    ):
        self.hub_height = hub_height_m
        self.rating = turbine_rating_kw
        self.rotor_d = rotor_diameter_m
        self.cut_in = cut_in_speed
        self.cut_out = cut_out_speed
        self.rated = rated_speed

    def assess_resource(
        self,
        wind_speed_ms: float = 7.5,
        weibull_k: float = 2.0,
    ) -> WindResource:
        weibull_a = wind_speed_ms / math.gamma(1 + 1 / weibull_k)
        area = math.pi * (self.rotor_d / 2) ** 2
        power_density = 0.5 * self.AIR_DENSITY * wind_speed_ms ** 3
        capacity_factor = self._capacity_factor(wind_speed_ms, weibull_k)
        return WindResource(
            mean_wind_speed_ms=wind_speed_ms,
            power_density_w_m2=round(power_density, 1),
            weibull_k=weibull_k,
            weibull_a=round(weibull_a, 2),
            capacity_factor=round(capacity_factor, 3),
            turbulence_intensity=0.12,
        )

    def estimate_generation(
        self,
        wind_speed_ms: float = 7.5,
        weibull_k: float = 2.0,
        availability: float = 0.97,
    ) -> WindGeneration:
        cf = self._capacity_factor(wind_speed_ms, weibull_k)
        annual_mwh = self.rating * cf * 8760 * availability / 1000
        monthly = [annual_mwh / 12 * (0.8 + 0.4 * math.sin(math.radians((m - 1) * 30 + 180))) for m in range(1, 13)]
        return WindGeneration(
            annual_mwh=round(annual_mwh, 1),
            capacity_factor=round(cf, 3),
            availability=availability,
            monthly_mwh=[round(m, 1) for m in monthly],
        )

    def _capacity_factor(self, wind_speed: float, k: float) -> float:
        a = wind_speed / math.gamma(1 + 1 / k)
        cf = min(0.6, 0.087 * wind_speed - 0.05)
        return max(cf, 0.15)

    def wake_loss(self, turbine_spacing_rotor_d: float = 7) -> float:
        return max(0.02, 0.3 / turbine_spacing_rotor_d)


# ---------------------------------------------------------------------------
# Storage Optimizer
# ---------------------------------------------------------------------------

class StorageOptimizer:
    """Energy storage system optimization."""

    CYCLE_LIFE = {
        StorageTechnology.LI_ION: 5000,
        StorageTechnology.LFP: 6000,
        StorageTechnology.FLOW: 15000,
        StorageTechnology.PUMPED_HYDRO: 50000,
    }

    EFFICIENCY = {
        StorageTechnology.LI_ION: 0.92,
        StorageTechnology.LFP: 0.95,
        StorageTechnology.FLOW: 0.80,
        StorageTechnology.PUMPED_HYDRO: 0.80,
    }

    def __init__(
        self,
        technology: str = "li_ion",
        capacity_kwh: float = 500,
        power_kw: float = 250,
    ):
        self.tech = StorageTechnology(technology)
        self.capacity = capacity_kwh
        self.power = power_kw

    def simulate_cycle(
        self,
        charge_rate: float = 0.5,
        discharge_rate: float = 0.8,
        depth_of_discharge: float = 0.8,
    ) -> StorageCycle:
        eff = self.EFFICIENCY.get(self.tech, 0.90)
        cycle_life = self.CYCLE_LIFE.get(self.tech, 5000)
        energy_throughput = self.capacity * depth_of_discharge * eff
        degradation = 1 / (cycle_life * depth_of_discharge)
        return StorageCycle(
            efficiency=round(eff, 3),
            cycle_life=cycle_life,
            energy_throughput_kwh=round(energy_throughput, 1),
            degradation_per_cycle=round(degradation, 6),
        )

    def calculate_economics(
        self,
        electricity_price: float = 0.12,
        demand_charge: float = 15.0,
        capex_per_kwh: float = 300,
        annual_maintenance_pct: float = 0.02,
        lifetime_years: int = 15,
    ) -> StorageEconomics:
        capex = self.capacity * capex_per_kwh
        daily_cycles = 1.0
        annual_energy = self.capacity * daily_cycles * 365 * 0.92
        energy_savings = annual_energy * electricity_price
        demand_savings = self.power * demand_charge * 12 * 0.3
        annual_savings = energy_savings + demand_savings
        annual_opex = capex * annual_maintenance_pct
        net_annual = annual_savings - annual_opex
        payback = capex / max(net_annual, 1)
        npv = sum(
            net_annual / (1.06 ** y) for y in range(1, lifetime_years + 1)
        ) - capex
        return StorageEconomics(
            capex=round(capex, 0),
            annual_savings=round(net_annual, 0),
            payback_years=round(payback, 1),
            npv=round(npv, 0),
            revenue_streams={
                "energy_arbitrage": round(energy_savings, 0),
                "demand_charge_reduction": round(demand_savings, 0),
            },
        )


# ---------------------------------------------------------------------------
# Economic Analyzer
# ---------------------------------------------------------------------------

class EconomicAnalyzer:
    """Energy project economic analysis."""

    def calculate_lcoe(
        self,
        capex: float,
        annual_opex: float,
        annual_generation_kwh: float,
        lifetime_years: int = 25,
        discount_rate: float = 0.06,
    ) -> float:
        total_cost = capex + sum(
            annual_opex / (1 + discount_rate) ** y
            for y in range(1, lifetime_years + 1)
        )
        total_energy = annual_generation_kwh * lifetime_years
        return round(total_cost / max(total_energy, 1), 4)

    def calculate_payback(
        self, capex: float, annual_savings: float
    ) -> float:
        return round(capex / max(annual_savings, 1), 1)

    def calculate_npv(
        self,
        capex: float,
        annual_cashflow: float,
        lifetime_years: int,
        discount_rate: float = 0.06,
    ) -> float:
        npv = sum(
            annual_cashflow / (1 + discount_rate) ** y
            for y in range(1, lifetime_years + 1)
        ) - capex
        return round(npv, 0)

    def sensitivity_analysis(
        self,
        base_lcoe: float,
        param_variations: Dict[str, float],
    ) -> Dict[str, float]:
        results = {}
        for param, variation in param_variations.items():
            new_lcoe = base_lcoe * (1 + variation)
            results[param] = round(new_lcoe, 4)
        return results


# ---------------------------------------------------------------------------
# Microgrid Designer
# ---------------------------------------------------------------------------

class MicrogridDesigner:
    """Design and optimize microgrid systems."""

    def optimize(
        self,
        load_kw: float = 500,
        solar_capacity_kw: float = 800,
        storage_kwh: float = 1000,
        grid_connection: bool = True,
    ) -> MicrogridSystem:
        annual_load = load_kw * 8760
        solar_planner = SolarPlanner(system_capacity_kw=solar_capacity_kw)
        perf = solar_planner.estimate_performance()
        annual_gen = perf.annual_kwh
        renewable_frac = min(annual_gen / max(annual_load, 1), 1.0)
        grid_cost = annual_load * 0.12 * (1 - renewable_frac)
        solar_cost = solar_capacity_kw * 1500 / 25
        storage_cost = storage_kwh * 300 / 15
        total_cost = grid_cost + solar_cost + storage_cost
        return MicrogridSystem(
            solar_kw=solar_capacity_kw,
            storage_kwh=storage_kwh,
            renewable_fraction=round(renewable_frac, 3),
            annual_cost=round(total_cost, 0),
            reliability_pct=99.9,
            annual_generation_kwh=round(annual_gen, 0),
            annual_load_kwh=round(annual_load, 0),
        )


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def prod(values):
    result = 1.0
    for v in values:
        result *= v
    return result


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Renewable Energy Demo")
    print("=" * 60)

    print("\n[1] Solar Planning")
    solar = SolarPlanner(location={"lat": 35, "lon": -118}, system_capacity_kw=100)
    res = solar.assess_resource()
    print(f"  GHI: {res.ghi_kwh_m2:.0f} kWh/m^2/yr")
    perf = solar.estimate_performance()
    print(f"  Generation: {perf.annual_kwh:,.0f} kWh")
    print(f"  Capacity factor: {perf.capacity_factor:.1%}")

    print("\n[2] Wind Planning")
    wind = WindPlanner(hub_height_m=80, turbine_rating_kw=3000)
    wr = wind.assess_resource(wind_speed_ms=7.5)
    print(f"  Power density: {wr.power_density_w_m2:.0f} W/m^2")
    gen = wind.estimate_generation(wind_speed_ms=7.5)
    print(f"  Annual: {gen.annual_mwh:,.0f} MWh")

    print("\n[3] Energy Storage")
    storage = StorageOptimizer("li_ion", 500, 250)
    cycle = storage.simulate_cycle(depth_of_discharge=0.8)
    print(f"  Efficiency: {cycle.efficiency:.1%}")
    print(f"  Cycle life: {cycle.cycle_life:,}")
    econ = storage.calculate_economics(electricity_price=0.12)
    print(f"  Payback: {econ.payback_years:.1f} years")

    print("\n[4] LCOE")
    analyzer = EconomicAnalyzer()
    lcoe = analyzer.calculate_lcoe(200000, 3000, 150000, 25, 0.06)
    print(f"  LCOE: ${lcoe:.3f}/kWh")

    print("\n[5] Microgrid")
    mg = MicrogridDesigner()
    system = mg.optimize(500, 800, 1000)
    print(f"  Renewable: {system.renewable_fraction:.1%}")
    print(f"  Cost: ${system.annual_cost:,.0f}/yr")

    print("\n" + "=" * 60)
    print("  Renewable energy demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
