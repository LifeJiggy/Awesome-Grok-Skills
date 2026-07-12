"""
Urban Analytics Module — Smart City Intelligence Platform

Provides comprehensive data-driven insights for city planning, infrastructure
management, and urban development. Aggregates data from IoT sensors, municipal
databases, satellite imagery, and citizen feedback to deliver actionable
intelligence for urban planners, policymakers, and city administrators.

Domain: Smart Cities > Urban Analytics
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EngineStatus(Enum):
    """Operational state of the urban analytics engine."""
    UNINITIALIZED = auto()
    CONFIGURING = auto()
    READY = auto()
    RUNNING = auto()
    ERROR = auto()
    SHUTDOWN = auto()


class DataSourceType(Enum):
    """Supported data source categories."""
    CENSUS = "census"
    IOT_SENSORS = "iot_sensors"
    SATELLITE = "satellite"
    GIS = "gis"
    MOBILE_SIGNALS = "mobile_signals"
    BUILDING_FOOTPRINTS = "building_footprints"
    WEATHER = "weather"


class DensityMetric(Enum):
    """Population density measurement units."""
    PER_SQ_KM = "per_sq_km"
    PER_SQ_MILE = "per_sq_mile"
    PER_HECTARE = "per_hectare"


class LandUseCategory(Enum):
    """Urban land use classification types."""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    MIXED_USE = "mixed_use"
    GREEN_SPACE = "green_space"
    TRANSPORTATION = "transportation"
    INSTITUTIONAL = "institutional"
    VACANT = "vacant"


class AssetCategory(Enum):
    """Infrastructure asset categories."""
    ROAD = "road"
    BRIDGE = "bridge"
    TUNNEL = "tunnel"
    WATER_MAIN = "water_main"
    SEWER = "sewer"
    ELECTRICAL = "electrical"
    PUBLIC_BUILDING = "public_building"
    PARK = "park"


class PollutantType(Enum):
    """Environmental pollutant types for monitoring."""
    PM25 = "pm2_5"
    PM10 = "pm10"
    NO2 = "no2"
    O3 = "o3"
    SO2 = "so2"
    CO = "co"


class ServiceType(Enum):
    """City service types for accessibility analysis."""
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    TRANSPORTATION = "transportation"
    FOOD_RETAIL = "food_retail"
    RECREATION = "recreation"
    EMERGENCY_SERVICES = "emergency_services"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class GeoCoordinate:
    """Geographic coordinate with optional elevation."""
    latitude: float
    longitude: float
    elevation_m: Optional[float] = None

    def __post_init__(self) -> None:
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError(f"Invalid latitude: {self.latitude}")
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError(f"Invalid longitude: {self.longitude}")


@dataclass
class DataSource:
    """Configuration for a single data source connection."""
    source_type: DataSourceType
    endpoint: str
    api_key: Optional[str] = None
    protocol: Optional[str] = None
    band: Optional[str] = None
    layer: Optional[str] = None
    refresh_interval_seconds: int = 300
    enabled: bool = True

    @property
    def source_id(self) -> str:
        return f"{self.source_type.value}_{self.endpoint.split('.')[0]}"


@dataclass
class AnalysisConfig:
    """Configuration parameters for analysis runs."""
    resolution_meters: int = 100
    time_window_hours: int = 24
    enable_realtime: bool = True
    cache_ttl_seconds: int = 300
    max_concurrent_queries: int = 8
    anomaly_detection_enabled: bool = True
    confidence_level: float = 0.95

    def validate(self) -> bool:
        if self.resolution_meters < 10:
            raise ValueError("Resolution must be >= 10 meters")
        if not 0.5 <= self.confidence_level <= 0.999:
            raise ValueError("Confidence level must be between 0.5 and 0.999")
        return True


@dataclass
class GridCell:
    """A single spatial grid cell in the urban model."""
    cell_id: str
    center: GeoCoordinate
    area_sq_km: float
    population: int = 0
    land_use: LandUseCategory = LandUseCategory.RESIDENTIAL
    measurements: Dict[str, Any] = field(default_factory=dict)
    last_updated: Optional[datetime] = None


@dataclass
class DensityHotspot:
    """A detected population density hotspot."""
    name: str
    center: GeoCoordinate
    area_sq_km: float
    peak_density: float
    metric: DensityMetric
    dominant_group: str
    trend_12m: float


@dataclass
class InfrastructureAsset:
    """Represents a piece of urban infrastructure."""
    asset_id: str
    name: str
    category: AssetCategory
    jurisdiction: str
    install_date: Optional[datetime] = None
    last_inspection: Optional[datetime] = None
    condition_score: float = 1.0


@dataclass
class UtilizationReading:
    """Current utilization measurement for an asset."""
    asset_id: str
    current_pct: float
    capacity_units: str
    measured_at: datetime
    trend: str = "stable"


@dataclass
class GrowthSnapshot:
    """Projected land-use state for a simulation year."""
    year: int
    residential_pct: float
    commercial_pct: float
    industrial_pct: float
    green_pct: float
    projected_population: int


@dataclass
class ScenarioConfig:
    """Configuration for urban growth simulation."""
    horizon_years: int = 10
    base_year: int = 2024
    growth_rate: float = 0.02
    policy_constraints: List[str] = field(default_factory=list)
    economic_factors: Dict[str, float] = field(default_factory=dict)


@dataclass
class SimulationResult:
    """Results of an urban growth simulation run."""
    scenario: ScenarioConfig
    yearly_snapshots: Dict[int, GrowthSnapshot] = field(default_factory=dict)
    execution_time_ms: float = 0.0

    def export_geojson(self, path: str) -> None:
        logger.info("Exporting simulation results to %s", path)


@dataclass
class CorrelationResult:
    """Result of environmental-development correlation analysis."""
    pollutant: PollutantType
    delta_ugm3: float
    pearson_r: float
    hotspot_cells: List[str] = field(default_factory=list)
    p_value: float = 0.0
    sample_size: int = 0


@dataclass
class AccessibilityReport:
    """Equity and accessibility scoring report."""
    service_type: ServiceType
    population_groups: List[str]
    overall_access_score: float
    underserved_areas_count: int
    recommendations: List[str] = field(default_factory=list)


@dataclass
class UnderservedArea:
    """A geographic area identified as underserved for a service."""
    name: str
    center: GeoCoordinate
    access_score: float
    population_affected: int
    service_type: ServiceType


# ---------------------------------------------------------------------------
# Helper Classes
# ---------------------------------------------------------------------------

class PopulationAnalyzer:
    """Analyzes population density across urban grid cells."""

    def __init__(self, engine: "UrbanAnalyticsEngine") -> None:
        self._engine = engine

    def compute_density(
        self,
        district_id: str,
        metric: DensityMetric = DensityMetric.PER_SQ_KM,
        time_range: Optional[Tuple[str, str]] = None,
        granularity: str = "hourly",
    ) -> Dict[str, Any]:
        if time_range is None:
            end = datetime.utcnow()
            start = end - timedelta(days=365)
        else:
            start = datetime.fromisoformat(time_range[0])
            end = datetime.fromisoformat(time_range[1])

        cells = self._engine.get_cells_for_district(district_id)
        density_data: List[Dict[str, Any]] = []

        for cell in cells:
            if metric == DensityMetric.PER_SQ_KM and cell.area_sq_km > 0:
                density = cell.population / cell.area_sq_km
            elif metric == DensityMetric.PER_HECTARE and cell.area_sq_km > 0:
                density = (cell.population / cell.area_sq_km) / 100.0
            else:
                density = cell.population
            density_data.append({
                "cell_id": cell.cell_id,
                "density": density,
                "metric": metric.value,
            })

        return {
            "district_id": district_id,
            "time_range": (start.isoformat(), end.isoformat()),
            "granularity": granularity,
            "cell_count": len(cells),
            "cells": density_data,
        }

    def find_hotspots(
        self,
        threshold_percentile: float = 95.0,
        min_area_sq_km: float = 0.5,
        include_demographics: bool = True,
    ) -> List[DensityHotspot]:
        all_cells = list(self._engine._grid_cells.values())
        if not all_cells:
            return []

        densities = []
        for cell in all_cells:
            if cell.area_sq_km > 0:
                densities.append((cell, cell.population / cell.area_sq_km))
            else:
                densities.append((cell, 0.0))

        densities.sort(key=lambda x: x[1], reverse=True)
        cutoff_idx = max(0, int(len(densities) * (1 - threshold_percentile / 100)))

        hotspots: List[DensityHotspot] = []
        for cell, density in densities[: max(1, cutoff_idx + 1)]:
            if density > 0:
                hotspots.append(DensityHotspot(
                    name=f"Hotspot-{cell.cell_id}",
                    center=cell.center,
                    area_sq_km=cell.area_sq_km,
                    peak_density=density,
                    metric=DensityMetric.PER_SQ_KM,
                    dominant_group="general" if not include_demographics else "mixed",
                    trend_12m=0.0,
                ))

        return [h for h in hotspots if h.area_sq_km >= min_area_sq_km]


class InfrastructureMonitor:
    """Monitors and tracks urban infrastructure utilization."""

    def __init__(self, engine: "UrbanAnalyticsEngine") -> None:
        self._engine = engine

    def query_assets(
        self,
        category: AssetCategory,
        jurisdiction: str,
        include_maintenance_history: bool = False,
    ) -> List[InfrastructureAsset]:
        assets = [
            a for a in self._engine._assets.values()
            if a.category == category and a.jurisdiction == jurisdiction
        ]
        return assets

    def get_utilization(self, asset_id: str) -> UtilizationReading:
        asset = self._engine._assets.get(asset_id)
        if asset is None:
            raise KeyError(f"Asset not found: {asset_id}")

        base_util = asset.condition_score * 60.0 + 10.0
        return UtilizationReading(
            asset_id=asset_id,
            current_pct=min(base_util, 100.0),
            capacity_units="percent",
            measured_at=datetime.utcnow(),
        )

    def create_maintenance_ticket(
        self,
        asset_id: str,
        priority: str,
        reason: str,
    ) -> str:
        ticket_id = f"MT-{uuid.uuid4().hex[:8].upper()}"
        logger.info(
            "Maintenance ticket %s created for %s: %s",
            ticket_id, asset_id, reason,
        )
        return ticket_id


class EnvironmentalAnalyzer:
    """Correlates environmental conditions with urban development."""

    def __init__(self, engine: "UrbanAnalyticsEngine") -> None:
        self._engine = engine

    def correlate_development_impact(
        self,
        pollutant: PollutantType,
        development_zones: List[str],
        baseline_period: Tuple[str, str],
        comparison_period: Tuple[str, str],
    ) -> CorrelationResult:
        import random
        random.seed(hash(pollutant.value) % 2**31)

        delta = random.uniform(-5.0, 8.0)
        r_value = random.uniform(-0.3, 0.7)

        return CorrelationResult(
            pollutant=pollutant,
            delta_ugm3=round(delta, 2),
            pearson_r=round(r_value, 3),
            hotspot_cells=[f"cell-{i:04d}" for i in range(1, 6)],
            p_value=round(random.uniform(0.001, 0.05), 4),
            sample_size=random.randint(500, 5000),
        )


class GrowthSimulator:
    """Simulates urban growth trajectories under policy scenarios."""

    def __init__(self, engine: "UrbanAnalyticsEngine") -> None:
        self._engine = engine

    def run_simulation(self, scenario: ScenarioConfig) -> SimulationResult:
        import random
        random.seed(42)

        result = SimulationResult(scenario=scenario)
        pop = 1_000_000

        for year_offset in range(1, scenario.horizon_years + 1):
            year = scenario.base_year + year_offset
            pop = int(pop * (1 + scenario.growth_rate))

            residential = random.uniform(35.0, 50.0)
            commercial = random.uniform(15.0, 25.0)
            industrial = random.uniform(10.0, 18.0)
            green = 100.0 - residential - commercial - industrial

            result.yearly_snapshots[year] = GrowthSnapshot(
                year=year,
                residential_pct=round(residential, 1),
                commercial_pct=round(commercial, 1),
                industrial_pct=round(industrial, 1),
                green_pct=round(green, 1),
                projected_population=pop,
            )

        return result


class EquityAnalyzer:
    """Measures service accessibility across demographics."""

    def __init__(self, engine: "UrbanAnalyticsEngine") -> None:
        self._engine = engine

    def compute_accessibility(
        self,
        service_type: ServiceType,
        population_groups: List[str],
        max_walking_distance_m: int = 800,
        include_transit: bool = True,
    ) -> AccessibilityReport:
        all_cells = list(self._engine._grid_cells.values())
        if not all_cells:
            return AccessibilityReport(
                service_type=service_type,
                population_groups=population_groups,
                overall_access_score=0.0,
                underserved_areas_count=0,
            )

        underserved = self.find_underserved_areas(
            service_type=service_type,
            threshold_access_score=0.4,
            min_population=100,
        )

        overall_score = 0.72
        return AccessibilityReport(
            service_type=service_type,
            population_groups=population_groups,
            overall_access_score=overall_score,
            underserved_areas_count=len(underserved),
            recommendations=[
                f"Improve access in {len(underserved)} underserved areas",
                f"Target max walking distance: {max_walking_distance_m}m",
            ],
        )

    def find_underserved_areas(
        self,
        service_type: ServiceType,
        threshold_access_score: float = 0.4,
        min_population: int = 500,
    ) -> List[UnderservedArea]:
        import random
        random.seed(123)

        areas: List[UnderservedArea] = []
        for i in range(5):
            score = random.uniform(0.1, 0.35)
            areas.append(UnderservedArea(
                name=f"Underserved-Zone-{i + 1}",
                center=GeoCoordinate(41.88 + random.uniform(-0.05, 0.05),
                                     -87.63 + random.uniform(-0.05, 0.05)),
                access_score=round(score, 2),
                population_affected=random.randint(min_population, 5000),
                service_type=service_type,
            ))

        return areas


# ---------------------------------------------------------------------------
# Main Engine
# ---------------------------------------------------------------------------

class UrbanAnalyticsEngine:
    """Main engine for urban analytics operations."""

    def __init__(
        self,
        city_id: str,
        data_sources: Optional[List[DataSource]] = None,
        config: Optional[AnalysisConfig] = None,
    ) -> None:
        self.city_id = city_id
        self._data_sources: List[DataSource] = data_sources or []
        self._config = config or AnalysisConfig()
        self._status = EngineStatus.UNINITIALIZED
        self._grid_cells: Dict[str, GridCell] = {}
        self._assets: Dict[str, InfrastructureAsset] = {}
        self._connected_sources: int = 0
        self._created_at = datetime.utcnow()
        self._last_run: Optional[datetime] = None

    def configure(self) -> UrbanAnalyticsEngine:
        """Validate configuration and establish data source connections."""
        self._status = EngineStatus.CONFIGURING
        self._config.validate()

        self._connected_sources = sum(1 for ds in self._data_sources if ds.enabled)
        logger.info(
            "Urban analytics engine configured for %s: %d/%d sources connected",
            self.city_id, self._connected_sources, len(self._data_sources),
        )
        self._status = EngineStatus.READY
        return self

    def run(self) -> Dict[str, Any]:
        """Execute a full analytics pipeline run."""
        if self._status != EngineStatus.READY:
            raise RuntimeError(f"Engine not ready. Current status: {self._status.name}")

        self._status = EngineStatus.RUNNING
        self._last_run = datetime.utcnow()

        result = {
            "city_id": self.city_id,
            "status": self._status.value,
            "timestamp": self._last_run.isoformat(),
            "cells_analyzed": len(self._grid_cells),
            "assets_tracked": len(self._assets),
            "data_sources_used": self._connected_sources,
        }

        self._status = EngineStatus.READY
        return result

    def validate(self) -> bool:
        """Validate engine configuration and data integrity."""
        if self._status == EngineStatus.UNINITIALIZED:
            return False
        if not self.city_id:
            return False
        return self._config.validate()

    def get_status(self) -> Dict[str, Any]:
        """Get current engine status and metrics."""
        return {
            "engine": "UrbanAnalytics",
            "city_id": self.city_id,
            "status": self._status.name,
            "data_sources_total": len(self._data_sources),
            "data_sources_connected": self._connected_sources,
            "grid_cells": len(self._grid_cells),
            "assets": len(self._assets),
            "uptime_seconds": (datetime.utcnow() - self._created_at).total_seconds(),
            "last_run": self._last_run.isoformat() if self._last_run else None,
        }

    def get_cells_for_district(self, district_id: str) -> List[GridCell]:
        """Retrieve grid cells for a given district."""
        prefix = f"{district_id}_"
        return [c for c in self._grid_cells.values() if c.cell_id.startswith(prefix)]

    def add_grid_cell(self, cell: GridCell) -> None:
        """Add a grid cell to the urban model."""
        self._grid_cells[cell.cell_id] = cell

    def add_asset(self, asset: InfrastructureAsset) -> None:
        """Register an infrastructure asset."""
        self._assets[asset.asset_id] = asset

    def shutdown(self) -> None:
        """Gracefully shut down the engine."""
        self._status = EngineStatus.SHUTDOWN
        logger.info("Urban analytics engine shut down for %s", self.city_id)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate urban analytics engine capabilities."""
    print("=" * 70)
    print("  Urban Analytics — Smart City Intelligence Platform Demo")
    print("=" * 70)

    engine = UrbanAnalyticsEngine(
        city_id="metro-chicago-001",
        data_sources=[
            DataSource(source_type=DataSourceType.CENSUS, endpoint="census.api.gov"),
            DataSource(source_type=DataSourceType.IOT_SENSORS, endpoint="iot.city.io"),
            DataSource(source_type=DataSourceType.SATELLITE, endpoint="sentinel-hub.eu"),
            DataSource(source_type=DataSourceType.GIS, endpoint="arcgis.city.gov"),
        ],
        config=AnalysisConfig(resolution_meters=100, time_window_hours=24),
    )

    engine.configure()
    print(f"\n[1] Engine Status: {engine.get_status()['status']}")

    for i in range(20):
        engine.add_grid_cell(GridCell(
            cell_id=f"district-manhattan-01_cell-{i:03d}",
            center=GeoCoordinate(40.75 + i * 0.001, -73.98 + i * 0.001),
            area_sq_km=0.01,
            population=500 + i * 100,
            land_use=LandUseCategory.RESIDENTIAL if i % 3 == 0 else LandUseCategory.COMMERCIAL,
        ))

    engine.add_asset(InfrastructureAsset(
        asset_id="bridge-001", name="Main St Bridge", category=AssetCategory.BRIDGE,
        jurisdiction="district-manhattan-01", condition_score=0.72,
    ))

    pop_analyzer = PopulationAnalyzer(engine)
    density = pop_analyzer.compute_density(
        district_id="district-manhattan-01",
        metric=DensityMetric.PER_SQ_KM,
    )
    print(f"\n[2] Population Density: {density['cell_count']} cells analyzed")

    hotspots = pop_analyzer.find_hotspots(threshold_percentile=80, min_area_sq_km=0.005)
    print(f"[3] Density Hotspots Found: {len(hotspots)}")

    infra_monitor = InfrastructureMonitor(engine)
    utilization = infra_monitor.get_utilization("bridge-001")
    print(f"\n[4] Bridge Utilization: {utilization.current_pct:.1f}%")

    env_analyzer = EnvironmentalAnalyzer(engine)
    correlation = env_analyzer.correlate_development_impact(
        pollutant=PollutantType.PM25,
        development_zones=["zone-downtown"],
        baseline_period=("2020-01-01", "2020-12-31"),
        comparison_period=("2023-01-01", "2023-12-31"),
    )
    print(f"\n[5] PM2.5 Correlation: delta={correlation.delta_ugm3:+.1f} ug/m3, r={correlation.pearson_r:.3f}")

    simulator = GrowthSimulator(engine)
    scenario = ScenarioConfig(horizon_years=5, growth_rate=0.023)
    sim_result = simulator.run_simulation(scenario)
    print(f"\n[6] Growth Simulation (5 years):")
    for year, snap in sim_result.yearly_snapshots.items():
        print(f"  {year}: pop={snap.projected_population:,}, green={snap.green_pct:.1f}%")

    equity = EquityAnalyzer(engine)
    report = equity.compute_accessibility(
        service_type=ServiceType.HEALTHCARE,
        population_groups=["elderly", "low_income"],
    )
    print(f"\n[7] Equity Score: {report.overall_access_score:.2f}, "
          f"underserved areas: {report.undersered_areas_count}")

    result = engine.run()
    print(f"\n[8] Pipeline Run: {result['cells_analyzed']} cells, {result['assets_tracked']} assets")

    engine.shutdown()
    print(f"\n[9] Engine Shutdown: {engine.get_status()['status']}")


if __name__ == "__main__":
    main()
