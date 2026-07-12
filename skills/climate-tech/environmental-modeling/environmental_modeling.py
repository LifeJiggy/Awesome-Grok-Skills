"""
Environmental Modeling Module
Species distribution, population dynamics, carbon cycle, biodiversity, and land-use change modeling.
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

class EcosystemType(Enum):
    TROPICAL_FOREST = "tropical_forest"
    TEMPERATE_FOREST = "temperate_forest"
    BOREAL_FOREST = "boreal_forest"
    GRASSLAND = "grassland"
    DESERT = "desert"
    TUNDRA = "tundra"
    WETLAND = "wetland"
    MARINE = "marine"
    CORAL_REEF = "coral_reef"
    MANGROVE = "mangrove"


class ClimateScenario(Enum):
    SSP1_26 = "SSP1-2.6"
    SSP2_45 = "SSP2-4.5"
    SSP3_70 = "SSP3-7.0"
    SSP5_85 = "SSP5-8.5"


class LandUseType(Enum):
    FOREST = "forest"
    GRASSLAND = "grassland"
    CROPLAND = "cropland"
    URBAN = "urban"
    WATER = "water"
    BARREN = "barren"
    WETLAND = "wetland"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class HabitatSuitability:
    """Species distribution model result."""
    species: str
    current_area_km2: float
    future_area_km2: float
    area_change_pct: float
    suitable_pixels: int = 0
    climate_scenario: str = ""
    future_year: int = 2050
    confidence: float = 0.0


@dataclass
class PopulationProjection:
    """Population dynamics projection."""
    species: str
    initial_population: int
    final_population: int
    trajectory: List[int] = field(default_factory=list)
    extinction_probability: float = 0.0
    time_to_extinction: Optional[int] = None
    years: int = 50


@dataclass
class CarbonExchange:
    """Annual carbon exchange result."""
    ecosystem_type: str
    area_hectares: float
    gross_primary_production: float = 0.0
    ecosystem_respiration: float = 0.0
    nee_tonnes: float = 0.0
    sequestration_tonnes: float = 0.0
    soil_carbon_change: float = 0.0
    biomass_carbon_change: float = 0.0


@dataclass
class BiodiversityMetrics:
    """Biodiversity index results."""
    shannon_wiener: float = 0.0
    simpson_diversity: float = 0.0
    simpson_reciprocal: float = 0.0
    species_richness: int = 0
    evenness: float = 0.0
    pielou_evenness: float = 0.0


@dataclass
class LandUseProjection:
    """Land-use change projection."""
    area_km2: float
    years: int
    current: Dict[str, float] = field(default_factory=dict)
    projected: Dict[str, float] = field(default_factory=dict)
    forest_loss_km2: float = 0.0
    urban_km2: float = 0.0
    fragmentation_index: float = 0.0


@dataclass
class EcologicalFootprint:
    """Ecological footprint assessment."""
    carbon_footprint: float = 0.0
    cropland_footprint: float = 0.0
    grazing_footprint: float = 0.0
    forest_footprint: float = 0.0
    fishing_footprint: float = 0.0
    built_up_footprint: float = 0.0
    total_footprint: float = 0.0
    biocapacity: float = 0.0
    deficit: float = 0.0


# ---------------------------------------------------------------------------
# Species Distribution Model
# ---------------------------------------------------------------------------

class SpeciesDistributor:
    """Model species habitat suitability."""

    CLIMATE_SENSITIVITY = {
        "Panthera tigris": {"temp_sensitivity": -0.15, "precip_sensitivity": 0.1},
        "Ursus arctos": {"temp_sensitivity": -0.08, "precip_sensitivity": 0.05},
        "Delphinapterus leucas": {"temp_sensitivity": -0.25, "precip_sensitivity": 0.02},
    }

    SCENARIO_WARMING = {
        ClimateScenario.SSP1_26: {2050: 1.5, 2100: 1.8},
        ClimateScenario.SSP2_45: {2050: 2.0, 2100: 2.7},
        ClimateScenario.SSP3_70: {2050: 2.5, 2100: 3.6},
        ClimateScenario.SSP5_85: {2050: 2.8, 2100: 4.4},
    }

    def model_habitat(
        self,
        species: str,
        climate_scenario: str = "SSP2-4.5",
        current_range: Optional[Dict[str, float]] = None,
        future_year: int = 2050,
    ) -> HabitatSuitability:
        current_range = current_range or {"lat_min": 0, "lat_max": 30, "lon_min": 70, "lon_max": 120}
        lat_span = current_range["lat_max"] - current_range["lat_min"]
        lon_span = current_range["lon_max"] - current_range["lon_min"]
        current_area = lat_span * lon_span * 111 * 111 * math.cos(math.radians(15))

        sensitivity = self.CLIMATE_SENSITIVITY.get(species, {"temp_sensitivity": -0.1, "precip_sensitivity": 0.05})
        scenario = ClimateScenario(climate_scenario)
        warming = self.SCENARIO_WARMING.get(scenario, {}).get(future_year, 2.0)

        temp_effect = 1 + sensitivity["temp_sensitivity"] * warming
        future_area = current_area * max(temp_effect, 0.1)
        change_pct = (future_area - current_area) / max(current_area, 1) * 100

        return HabitatSuitability(
            species=species,
            current_area_km2=round(current_area, 1),
            future_area_km2=round(future_area, 1),
            area_change_pct=round(change_pct, 1),
            climate_scenario=climate_scenario,
            future_year=future_year,
            confidence=0.75,
        )


# ---------------------------------------------------------------------------
# Population Model
# ---------------------------------------------------------------------------

class PopulationModel:
    """Population dynamics modeling."""

    def __init__(
        self,
        species: str,
        initial_population: int,
        carrying_capacity: int,
        growth_rate: float = 0.1,
        mortality_rate: float = 0.05,
        stochastic: bool = True,
    ):
        self.species = species
        self.initial = initial_population
        self.K = carrying_capacity
        self.r = growth_rate
        self.m = mortality_rate
        self.stochastic = stochastic
        self._rng = random.Random(42)

    def project(self, years: int = 50, simulations: int = 100) -> PopulationProjection:
        trajectory = self._single_run(years)
        ext_count = 0
        for _ in range(simulations):
            run = self._single_run(years)
            if run[-1] <= 0:
                ext_count += 1
        ext_prob = ext_count / simulations
        final = trajectory[-1] if trajectory else 0
        time_ext = None
        for i, pop in enumerate(trajectory):
            if pop <= 0:
                time_ext = i
                break
        return PopulationProjection(
            species=self.species,
            initial_population=self.initial,
            final_population=max(final, 0),
            trajectory=trajectory,
            extinction_probability=ext_prob,
            time_to_extinction=time_ext,
            years=years,
        )

    def _single_run(self, years: int) -> List[int]:
        pop = self.initial
        trajectory: List[int] = [pop]
        for _ in range(years):
            if pop <= 0:
                trajectory.append(0)
                continue
            growth = self.r * pop * (1 - pop / self.K)
            deaths = self.m * pop
            net = growth - deaths
            if self.stochastic:
                net = self._rng.gauss(net, abs(net) * 0.1)
            pop = max(0, int(pop + net))
            trajectory.append(pop)
        return trajectory

    def viability_analysis(self, min_viable: int = 50) -> Dict[str, Any]:
        runs = [self._single_run(100) for _ in range(200)]
        survival = sum(1 for run in runs if run[-1] >= min_viable) / len(runs)
        return {
            "viability_probability": survival,
            "min_viable_population": min_viable,
            "recommended_population": int(min_viable * 3),
        }


# ---------------------------------------------------------------------------
# Carbon Cycle Model
# ---------------------------------------------------------------------------

class CarbonCycleModel:
    """Carbon cycle modeling for ecosystems."""

    ECOSYSTEM_PARAMS = {
        EcosystemType.TROPICAL_FOREST: {"gpp": 20.0, "resp": 18.0, "soil_c": 120, "biomass_c": 250},
        EcosystemType.TEMPERATE_FOREST: {"gpp": 14.0, "resp": 12.5, "soil_c": 180, "biomass_c": 180},
        EcosystemType.BOREAL_FOREST: {"gpp": 8.0, "resp": 7.0, "soil_c": 200, "biomass_c": 100},
        EcosystemType.GRASSLAND: {"gpp": 10.0, "resp": 9.5, "soil_c": 150, "biomass_c": 15},
        EcosystemType.WETLAND: {"gpp": 12.0, "resp": 10.0, "soil_c": 300, "biomass_c": 50},
    }

    def __init__(
        self,
        ecosystem_type: str,
        area_hectares: float,
        soil_depth_m: float = 1.0,
    ):
        self.ecosystem = EcosystemType(ecosystem_type)
        self.area = area_hectares
        self.soil_depth = soil_depth_m
        self.params = self.ECOSYSTEM_PARAMS.get(self.ecosystem, {"gpp": 10, "resp": 9, "soil_c": 150, "biomass_c": 50})

    def annual_exchange(self) -> CarbonExchange:
        gpp = self.params["gpp"] * self.area / 10000
        resp = self.params["resp"] * self.area / 10000
        nee = resp - gpp
        sequestration = -nee
        soil_change = sequestration * 0.3
        biomass_change = sequestration * 0.7
        return CarbonExchange(
            ecosystem_type=self.ecosystem.value,
            area_hectares=self.area,
            gross_primary_production=round(gpp, 2),
            ecosystem_respiration=round(resp, 2),
            nee_tonnes=round(nee, 2),
            sequestration_tonnes=round(sequestration, 2),
            soil_carbon_change=round(soil_change, 2),
            biomass_carbon_change=round(biomass_change, 2),
        )

    def carbon_sequestration_potential(self, years: int = 30) -> Dict[str, float]:
        annual = self.annual_exchange()
        total = annual.sequestration_tonnes * years
        value_per_tonne = 50
        return {
            "total_sequestration_tonnes": round(total, 1),
            "value_usd": round(total * value_per_tonne, 2),
            "annual_rate": round(annual.sequestration_tonnes, 2),
        }


# ---------------------------------------------------------------------------
# Biodiversity Calculator
# ---------------------------------------------------------------------------

class BiodiversityCalculator:
    """Calculate biodiversity indices."""

    def shannon_wiener(self, abundances: List[int]) -> float:
        total = sum(abundances)
        if total == 0:
            return 0.0
        h = 0.0
        for n in abundances:
            if n > 0:
                p = n / total
                h -= p * math.log(p)
        return h

    def simpson_diversity(self, abundances: List[int]) -> float:
        total = sum(abundances)
        if total == 0:
            return 0.0
        D = sum(n * (n - 1) for n in abundances) / (total * (total - 1))
        return 1 - D

    def simpson_reciprocal(self, abundances: List[int]) -> float:
        D = self.simpson_diversity(abundances)
        return 1 / max(1 - D, 0.001)

    def pielou_evenness(self, abundances: List[int]) -> float:
        S = sum(1 for n in abundances if n > 0)
        if S <= 1:
            return 0.0
        H = self.shannon_wiener(abundances)
        return H / math.log(S)

    def species_area_relationship(
        self, areas: List[float], species_counts: List[int]
    ) -> Dict[str, float]:
        log_a = [math.log(a) for a in areas]
        log_s = [math.log(max(s, 1)) for s in species_counts]
        n = len(areas)
        if n < 2:
            return {"z": 0.25, "c": 10.0}
        mean_x = sum(log_a) / n
        mean_y = sum(log_s) / n
        ss_xx = sum((x - mean_x) ** 2 for x in log_a)
        ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_a, log_s))
        z = ss_xy / max(ss_xx, 1e-10)
        c = math.exp(mean_y - z * mean_x)
        return {"z": round(z, 3), "c": round(c, 3)}

    def calculate_all(self, abundances: List[int]) -> BiodiversityMetrics:
        S = sum(1 for n in abundances if n > 0)
        H = self.shannon_wiener(abundances)
        D = self.simpson_diversity(abundances)
        E = self.pielou_evenness(abundances)
        return BiodiversityMetrics(
            shannon_wiener=round(H, 4),
            simpson_diversity=round(D, 4),
            simpson_reciprocal=round(self.simpson_reciprocal(abundances), 4),
            species_richness=S,
            evenness=round(E, 4),
            pielou_evenness=round(E, 4),
        )


# ---------------------------------------------------------------------------
# Land Use Model
# ---------------------------------------------------------------------------

class LandUseModel:
    """Land-use change projection model."""

    def __init__(self, area_km2: float = 100):
        self.area = area_km2
        self.current = {
            LandUseType.FOREST.value: area_km2 * 0.4,
            LandUseType.GRASSLAND.value: area_km2 * 0.25,
            LandUseType.CROPLAND.value: area_km2 * 0.2,
            LandUseType.URBAN.value: area_km2 * 0.05,
            LandUseType.WATER.value: area_km2 * 0.05,
            LandUseType.BARREN.value: area_km2 * 0.05,
        }

    def project_change(
        self,
        years: int = 20,
        urban_growth_rate: float = 0.03,
        deforestation_rate: float = 0.01,
    ) -> LandUseProjection:
        projected = dict(self.current)
        forest_loss = 0.0
        for year in range(years):
            urban_growth = projected.get(LandUseType.URBAN.value, 0) * urban_growth_rate
            forest_loss_yr = projected.get(LandUseType.FOREST.value, 0) * deforestation_rate
            projected[LandUseType.URBAN.value] = projected.get(LandUseType.URBAN.value, 0) + urban_growth
            projected[LandUseType.FOREST.value] = projected.get(LandUseType.FOREST.value, 0) - forest_loss_yr
            forest_loss += forest_loss_yr

        return LandUseProjection(
            area_km2=self.area,
            years=years,
            current=self.current,
            projected=projected,
            forest_loss_km2=round(forest_loss, 2),
            urban_km2=round(projected.get(LandUseType.URBAN.value, 0), 2),
            fragmentation_index=round(self._fragmentation(projected), 3),
        )

    def _fragmentation(self, land_use: Dict[str, float]) -> float:
        total = sum(land_use.values())
        if total == 0:
            return 0.0
        probs = [v / total for v in land_use.values()]
        H = -sum(p * math.log(p) for p in probs if p > 0)
        max_H = math.log(len(probs))
        return 1 - H / max(max_H, 1)

    def ecological_footprint(self) -> EcologicalFootprint:
        urban = self.current.get(LandUseType.URBAN.value, 0)
        forest = self.current.get(LandUseType.FOREST.value, 0)
        cropland = self.current.get(LandUseType.CROPLAND.value, 0)
        return EcologicalFootprint(
            carbon_footprint=urban * 0.5,
            cropland_footprint=cropland * 0.3,
            forest_footprint=forest * 0.1,
            total_footprint=urban * 0.5 + cropland * 0.3 + forest * 0.1,
            biocapacity=self.area * 0.4,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Environmental Modeling Demo")
    print("=" * 60)

    print("\n[1] Species Distribution")
    dist = SpeciesDistributor()
    suit = dist.model_habitat("Panthera tigris", "SSP2-4.5", future_year=2050)
    print(f"  Current: {suit.current_area_km2:,.0f} km^2")
    print(f"  Future: {suit.future_area_km2:,.0f} km^2")
    print(f"  Change: {suit.area_change_pct:.1f}%")

    print("\n[2] Population Dynamics")
    pop = PopulationModel("wolf", 50, 200, growth_rate=0.15, mortality_rate=0.08)
    proj = pop.project(years=50)
    print(f"  Final pop: {proj.final_population}")
    print(f"  Extinction prob: {proj.extinction_probability:.1%}")

    print("\n[3] Carbon Cycle")
    carbon = CarbonCycleModel("temperate_forest", 1000)
    exchange = carbon.annual_exchange()
    print(f"  GPP: {exchange.gross_primary_production:.1f} tC/yr")
    print(f"  Sequestration: {exchange.sequestration_tonnes:.1f} tC/yr")

    print("\n[4] Biodiversity")
    bio = BiodiversityCalculator()
    metrics = bio.calculate_all([10, 20, 30, 40, 5])
    print(f"  Shannon: {metrics.shannon_wiener:.3f}")
    print(f"  Simpson: {metrics.simpson_diversity:.3f}")
    print(f"  Richness: {metrics.species_richness}")

    print("\n[5] Land Use Change")
    land = LandUseModel(100)
    proj = land.project_change(years=20, urban_growth_rate=0.03)
    print(f"  Urban: {proj.urban_km2:.1f} km^2")
    print(f"  Forest loss: {proj.forest_loss_km2:.1f} km^2")

    print("\n" + "=" * 60)
    print("  Environmental modeling demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
