"""
Green Computing Module
Energy-efficient algorithms, carbon-aware workload scheduling, DVFS optimization,
server power modeling, and Software Carbon Intensity (SCI) measurement.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums & Constants
# ---------------------------------------------------------------------------

class GridRegion(Enum):
    """Major grid regions with distinct carbon intensity profiles."""
    DE = "DE"          # Germany
    FR = "FR"          # France
    GB = "GB"          # Great Britain
    US_CAL_CISO = "US-CAL-CISO"  # California ISO
    US_PJ = "US-PJM"            # PJM Interconnection
    US_ERCOT = "US-ERCOT"        # Texas
    AU_EAST = "AU-NEM"           # Australia East
    JP = "JP"                     # Japan
    CN_NORTH = "CN-NORTH"        # China North


class DVFSGovernor(Enum):
    """CPU frequency scaling governors."""
    PERFORMANCE = "performance"
    POWERSAVE = "powersave"
    ONDEMAND = "ondemand"
    CONSERVATIVE = "conservative"
    SCHEDUTIL = "schedutil"


class WorkloadPriority(Enum):
    """Priority levels for carbon-aware scheduling."""
    CRITICAL = 0      # Must run now, no deferral allowed
    HIGH = 1          # Minimal deferral (max 1 hour)
    MEDIUM = 2        # Moderate deferral acceptable (up to 12 hours)
    LOW = 3           # Flexible deferral (up to 48 hours)
    BATCH = 4         # Fully deferrable (up to 1 week)


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class CarbonIntensityReading:
    """A single carbon intensity measurement for a grid region."""
    region: GridRegion
    timestamp: datetime
    gCO2_per_kWh: float
    renewable_percent: float
    source: str = "api"
    forecast: bool = False

    @property
    def carbon_free_energy_percent(self) -> float:
        return 100.0 - (self.gCO2_per_kWh / 900.0) * 100.0  # 900 = coal reference

    def __post_init__(self):
        if not 0 <= self.renewable_percent <= 100:
            raise ValueError(f"Renewable percent must be 0-100, got {self.renewable_percent}")
        if self.gCO2_per_kWh < 0:
            raise ValueError(f"Carbon intensity cannot be negative: {self.gCO2_per_kWh}")


@dataclass
class TimeWindow:
    """A time window for workload scheduling."""
    start: datetime
    end: datetime
    avg_gCO2_per_kWh: float
    renewable_fraction: float
    region: GridRegion

    @property
    def duration_hours(self) -> float:
        return (self.end - self.start).total_seconds() / 3600.0

    @property
    def carbon_savings_vs_average(self) -> float:
        baseline = 400.0  # Typical European average
        return max(0.0, baseline - self.avg_gCO2_per_kWh) / baseline * 100.0


@dataclass
class PowerEstimate:
    """Estimated power consumption breakdown."""
    cpu_watts: float
    memory_watts: float
    storage_watts: float
    network_watts: float
    cooling_overhead_watts: float = 0.0

    @property
    def total_watts(self) -> float:
        return self.cpu_watts + self.memory_watts + self.storage_watts + \
               self.network_watts + self.cooling_overhead_watts

    def with_pue(self, pue: float) -> float:
        """Apply Power Usage Effectiveness to get facility-level power."""
        return self.total_watts * pue


@dataclass
class SCIScore:
    """Software Carbon Intensity result."""
    gCO2eq: float
    functional_unit: str
    energy_kwh: float
    carbon_intensity_gCO2_per_kWh: float
    embodied_carbon_g: float
    time_span_hours: float

    @property
    def gCO2eq_per_unit(self) -> float:
        return self.gCO2eq

    @property
    def energy_per_unit(self) -> float:
        return self.energy_kwh


@dataclass
class DVFSState:
    """Current state of a CPU's DVFS configuration."""
    cpu_id: int
    governor: DVFSGovernor
    current_freq_mhz: int
    min_freq_mhz: int
    max_freq_mhz: int
    power_watts: float


# ---------------------------------------------------------------------------
# Carbon Intensity Client
# ---------------------------------------------------------------------------

class CarbonIntensityClient:
    """
    Fetches real-time and forecasted carbon intensity data from grid operators.
    Supports multiple regions and data sources.
    """

    # Typical carbon intensities by region (gCO2eq/kWh) — used as fallback
    REGION_DEFAULTS: dict[GridRegion, float] = {
        GridRegion.DE: 320.0,
        GridRegion.FR: 55.0,
        GridRegion.GB: 210.0,
        GridRegion.US_CAL_CISO: 280.0,
        GridRegion.US_PJ: 380.0,
        GridRegion.US_ERCOT: 420.0,
        GridRegion.AU_EAST: 650.0,
        GridRegion.JP: 480.0,
        GridRegion.CN_NORTH: 580.0,
    }

    def __init__(self, api_key: Optional[str] = None, cache_ttl_seconds: int = 300):
        self._api_key = api_key
        self._cache_ttl = cache_ttl_seconds
        self._cache: dict[GridRegion, tuple[float, CarbonIntensityReading]] = {}

    def get_current_intensity(self, region: GridRegion) -> CarbonIntensityReading:
        """Fetch the current carbon intensity for a grid region."""
        now = time.time()
        if region in self._cache:
            cached_time, cached_reading = self._cache[region]
            if now - cached_time < self._cache_ttl:
                return cached_reading

        reading = self._fetch_from_source(region)
        self._cache[region] = (now, reading)
        return reading

    def get_forecast(self, region: GridRegion, hours_ahead: int = 24) -> list[CarbonIntensityReading]:
        """Fetch carbon intensity forecast for the next N hours."""
        readings = []
        base = self.get_current_intensity(region)
        for h in range(hours_ahead):
            forecast_time = base.timestamp + timedelta(hours=h)
            # Simulate diurnal pattern: lower intensity during solar peak
            hour = forecast_time.hour
            solar_factor = math.cos((hour - 13) * math.pi / 12)  # Peak at 13:00
            wind_factor = 0.3 + 0.2 * math.sin(hour * math.pi / 6)
            variation = (solar_factor * 0.3 + wind_factor * 0.2) * base.gCO2_per_kWh
            forecasted_intensity = max(20.0, base.gCO2_per_kWh - variation)
            readings.append(CarbonIntensityReading(
                region=region,
                timestamp=forecast_time,
                gCO2_per_kWh=round(forecasted_intensity, 1),
                renewable_percent=min(100.0, max(0.0, 100 - forecasted_intensity / 9)),
                source="forecast",
                forecast=True
            ))
        return readings

    def compare_regions(self, regions: list[GridRegion]) -> list[CarbonIntensityReading]:
        """Compare carbon intensity across multiple regions."""
        readings = []
        for region in regions:
            readings.append(self.get_current_intensity(region))
        return sorted(readings, key=lambda r: r.gCO2_per_kWh)

    def _fetch_from_source(self, region: GridRegion) -> CarbonIntensityReading:
        """Fetch from external API or fall back to defaults."""
        # In production, this would call electricityMap, WattTime, or similar
        default = self.REGION_DEFAULTS.get(region, 400.0)
        return CarbonIntensityReading(
            region=region,
            timestamp=datetime.now(timezone.utc),
            gCO2_per_kWh=default + (hash(region.value) % 100 - 50),  # Simulated variation
            renewable_percent=max(0, min(100, 100 - default / 9)),
            source="default"
        )


# ---------------------------------------------------------------------------
# DVFS Controller
# ---------------------------------------------------------------------------

class DVFSController:
    """
    Dynamic Voltage and Frequency Scaling controller for CPU power management.
    Adjusts CPU frequency to balance performance and energy consumption.
    """

    # Power model constants (approximate linear model)
    BASE_POWER_PER_MHZ = 0.05   # Watts per MHz (baseline)
    IDLE_POWER_OFFSET = 30.0    # Watts when CPU is idle at min frequency

    def __init__(self, cpu_id: int = 0, min_freq_mhz: int = 800, max_freq_mhz: int = 4500):
        self._cpu_id = cpu_id
        self._min_freq = min_freq_mhz
        self._max_freq = max_freq_mhz
        self._current_freq = max_freq_mhz
        self._governor = DVFSGovernor.SCHEDUTIL

    @property
    def cpu_id(self) -> int:
        return self._cpu_id

    @property
    def current_state(self) -> DVFSState:
        return DVFSState(
            cpu_id=self._cpu_id,
            governor=self._governor,
            current_freq_mhz=self._current_freq,
            min_freq_mhz=self._min_freq,
            max_freq_mhz=self._max_freq,
            power_watts=self.estimate_power_watts()
        )

    def set_governor(self, governor: str) -> None:
        """Set the CPU frequency scaling governor."""
        self._governor = DVFSGovernor(governor)

    def set_frequency_mhz(self, freq_mhz: int) -> None:
        """Set the CPU frequency in MHz."""
        if not self._min_freq <= freq_mhz <= self._max_freq:
            raise ValueError(
                f"Frequency {freq_mhz}MHz outside range "
                f"[{self._min_freq}, {self._max_freq}]"
            )
        self._current_freq = freq_mhz

    def estimate_power_watts(self, utilization: float = 0.5) -> float:
        """Estimate power consumption at current frequency and given utilization."""
        freq_ratio = self._current_freq / self._max_freq
        dynamic_power = self.BASE_POWER_PER_MHZ * self._current_freq * utilization
        static_power = self.IDLE_POWER_OFFSET * freq_ratio
        return round(dynamic_power + static_power, 2)

    def optimal_freq_for_budget(self, power_budget_watts: float, utilization: float = 0.5) -> int:
        """Find the highest frequency that stays within a power budget."""
        target_dynamic = power_budget_watts - self.IDLE_POWER_OFFSET * (self._current_freq / self._max_freq)
        if target_dynamic <= 0:
            return self._min_freq
        max_safe_freq = int(target_dynamic / (self.BASE_POWER_PER_MHZ * utilization))
        return max(self._min_freq, min(self._max_freq, max_safe_freq))

    def powersave_for_batch(self) -> None:
        """Configure for batch processing with maximum power savings."""
        self._governor = DVFSGovernor.POWERSAVE
        self._current_freq = self._min_freq

    def performance_for_interactive(self) -> None:
        """Configure for interactive workloads with maximum performance."""
        self._governor = DVFSGovernor.PERFORMANCE
        self._current_freq = self._max_freq

    def power_savings_summary(self, hours_running: float = 1.0) -> dict:
        """Calculate power savings compared to running at max frequency."""
        power_at_max = self.IDLE_POWER_OFFSET + self.BASE_POWER_PER_MHZ * self._max_freq
        power_at_current = self.estimate_power_watts()
        saved_watts = power_at_max - power_at_current
        energy_saved_wh = saved_watts * hours_running
        carbon_saved_g = energy_saved_wh * 0.0004  # ~400g CO2/kWh average
        return {
            "power_saved_watts": round(saved_watts, 2),
            "energy_saved_wh": round(energy_saved_wh, 2),
            "carbon_saved_grams": round(carbon_saved_g, 3),
            "percent_reduction": round(saved_watts / power_at_max * 100, 1)
        }


# ---------------------------------------------------------------------------
# Server Power Model
# ---------------------------------------------------------------------------

class PowerModel:
    """
    Estimates server power consumption using an empirical model.
    Based on CPU, memory, storage, and network utilization.
    """

    def __init__(
        self,
        idle_power_watts: float = 85.0,
        max_power_watts: float = 350.0,
        cpu_tdp: float = 170.0,
        memory_watts: float = 24.0,
        storage_watts: float = 12.0,
        network_watts: float = 8.0,
        pue: float = 1.2
    ):
        self.idle_power = idle_power_watts
        self.max_power = max_power_watts
        self.cpu_tdp = cpu_tdp
        self.memory_base = memory_watts
        self.storage_base = storage_watts
        self.network_base = network_watts
        self.pue = pue

    def estimate(
        self,
        cpu_utilization: float = 0.0,
        memory_utilization: float = 0.0,
        disk_utilization: float = 0.0,
        network_utilization: float = 0.0
    ) -> PowerEstimate:
        """Estimate power consumption at given utilization levels."""
        cpu_watts = self.cpu_tdp * (0.1 + 0.9 * cpu_utilization)  # 10% base + 90% scaled
        mem_watts = self.memory_base * (0.5 + 0.5 * memory_utilization)
        stor_watts = self.storage_base * (0.3 + 0.7 * disk_utilization)
        net_watts = self.network_base * (0.2 + 0.8 * network_utilization)
        cooling = (cpu_watts + mem_watts) * (self.pue - 1.0)

        return PowerEstimate(
            cpu_watts=round(cpu_watts, 2),
            memory_watts=round(mem_watts, 2),
            storage_watts=round(stor_watts, 2),
            network_watts=round(net_watts, 2),
            cooling_overhead_watts=round(cooling, 2)
        )

    def annual_cost_estimate(self, hours_per_year: float = 8760.0, electricity_rate: float = 0.10) -> dict:
        """Estimate annual power cost at average utilization."""
        avg_estimate = self.estimate(cpu_utilization=0.4, memory_utilization=0.5)
        energy_kwh = avg_estimate.total_watts * self.pue * hours_per_year / 1000.0
        cost = energy_kwh * electricity_rate
        carbon_kg = energy_kwh * 0.4  # ~400g CO2/kWh average
        return {
            "energy_kwh": round(energy_kwh, 1),
            "cost_usd": round(cost, 2),
            "carbon_kg": round(carbon_kg, 1),
            "pue_adjusted_watts": round(avg_estimate.total_watts * self.pue, 1)
        }


# ---------------------------------------------------------------------------
# Software Carbon Intensity (SCI) Calculator
# ---------------------------------------------------------------------------

class SCICalculator:
    """
    Implements the Green Software Foundation's SCI specification.
    SCI = (Operational Energy * Carbon Intensity + Embodied Carbon) / Functional Unit
    """

    def __init__(
        self,
        energy_measurements: list[float],
        carbon_intensity: float,
        embodied_carbon_g: float = 0.0,
        expected_lifespan_hours: float = 43800.0  # 5 years
    ):
        if not energy_measurements:
            raise ValueError("Energy measurements list cannot be empty")
        self.energy_measurements = energy_measurements
        self.carbon_intensity = carbon_intensity
        self.embodied_carbon_g = embodied_carbon_g
        self.expected_lifespan_hours = expected_lifespan_hours

    @property
    def avg_energy_kwh(self) -> float:
        return sum(self.energy_measurements) / len(self.energy_measurements)

    @property
    def total_energy_kwh(self) -> float:
        return sum(self.energy_measurements)

    def compute(self, functional_unit: str, total_units: int = 1) -> SCIScore:
        """Compute the SCI score for a given functional unit."""
        if total_units <= 0:
            raise ValueError("Total units must be positive")

        avg_energy = self.avg_energy_kwh
        operational_carbon_g = avg_energy * self.carbon_intensity * total_units

        # Amortize embodied carbon across expected lifespan and total units
        time_ratio = len(self.energy_measurements) / max(self.expected_lifespan_hours, 1)
        embodied_per_unit = self.embodied_carbon_g * time_ratio / total_units

        total_carbon = operational_carbon_g + embodied_per_unit
        per_unit = total_carbon / total_units if total_units > 0 else total_carbon

        return SCIScore(
            gCO2eq=round(per_unit, 8),
            functional_unit=functional_unit,
            energy_kwh=round(avg_energy, 8),
            carbon_intensity_gCO2_per_kWh=self.carbon_intensity,
            embodied_carbon_g=round(embodied_per_unit, 6),
            time_span_hours=len(self.energy_measurements)
        )


# ---------------------------------------------------------------------------
# Workload Scheduler (Carbon-Aware)
# ---------------------------------------------------------------------------

@dataclass
class ScheduledWorkload:
    """A workload with its scheduling metadata."""
    workload_id: str
    duration_hours: float
    priority: WorkloadPriority
    preferred_region: GridRegion
    flexible: bool = True
    energy_kwh_per_hour: float = 0.5


@dataclass
class MigrationPlan:
    """A recommended workload migration."""
    workload_id: str
    from_cluster: str
    to_cluster: str
    carbon_saved_grams: float
    delay_hours: float
    reason: str


class WorkloadScheduler:
    """
    Carbon-aware workload scheduler that finds optimal execution windows
    based on grid carbon intensity forecasts.
    """

    def __init__(self, region: GridRegion = GridRegion.DE):
        self._region = region
        self._carbon_client = CarbonIntensityClient()
        self._workloads: list[ScheduledWorkload] = []

    def find_low_carbon_window(
        self,
        task_duration_hours: float,
        max_delay_hours: float = 24.0
    ) -> TimeWindow:
        """Find the time window with lowest carbon intensity for a task."""
        forecast = self._carbon_client.get_forecast(self._region, hours_ahead=int(max_delay_hours) + 1)

        best_window: Optional[TimeWindow] = None
        best_intensity = float("inf")

        for i in range(len(forecast)):
            end_idx = min(i + int(task_duration_hours), len(forecast))
            if end_idx - i < 1:
                continue
            window_readings = forecast[i:end_idx]
            avg_intensity = sum(r.gCO2_per_kWh for r in window_readings) / len(window_readings)
            avg_renewable = sum(r.renewable_percent for r in window_readings) / len(window_readings)

            if avg_intensity < best_intensity:
                best_intensity = avg_intensity
                best_window = TimeWindow(
                    start=window_readings[0].timestamp,
                    end=window_readings[-1].timestamp,
                    avg_gCO2_per_kWh=round(avg_intensity, 1),
                    renewable_fraction=round(avg_renewable / 100, 3),
                    region=self._region
                )

        return best_window or TimeWindow(
            start=datetime.now(timezone.utc),
            end=datetime.now(timezone.utc) + timedelta(hours=task_duration_hours),
            avg_gCO2_per_kWh=0.0,
            renewable_fraction=0.0,
            region=self._region
        )

    def plan_migration(self, workload_id: str, current_cluster: str, priority: str, max_migrations_per_day: int = 2) -> MigrationPlan:
        """Plan a workload migration to a lower-carbon region."""
        regions = [GridRegion.DE, GridRegion.FR, GridRegion.GB, GridRegion.US_CAL_CISO]
        comparison = self._carbon_client.compare_regions(regions)

        current_reading = self._carbon_client.get_current_intensity(self._region)
        if len(comparison) < 2:
            raise ValueError("Need at least 2 regions for migration comparison")

        best = comparison[0]
        worst = comparison[-1]

        return MigrationPlan(
            workload_id=workload_id,
            from_cluster=current_cluster,
            to_cluster=f"region-{best.region.value}",
            carbon_saved_grams=round((current_reading.gCO2_per_kWh - best.gCO2_per_kWh) * 0.5, 2),
            delay_hours=0.0,
            reason=f"Region {best.region.value} has {best.gCO2_per_kWh:.0f} gCO2eq/kWh vs current {current_reading.gCO2_per_kWh:.0f}"
        )


# ---------------------------------------------------------------------------
# Green Metrics Dashboard
# ---------------------------------------------------------------------------

class GreenMetricsDashboard:
    """Collects and aggregates green computing metrics over time."""

    def __init__(self):
        self._readings: list[dict] = []

    def record(self, timestamp: datetime, energy_kwh: float, carbon_g: float, pue: float = 1.0) -> None:
        """Record a single energy/carbon measurement."""
        self._readings.append({
            "timestamp": timestamp.isoformat(),
            "energy_kwh": energy_kwh,
            "carbon_g": carbon_g,
            "pue": pue,
            "carbon_per_kwh": carbon_g / max(energy_kwh, 0.0001)
        })

    def summary(self) -> dict:
        """Aggregate all recorded metrics into a summary."""
        if not self._readings:
            return {"total_energy_kwh": 0, "total_carbon_g": 0, "avg_pue": 1.0, "readings_count": 0}

        total_energy = sum(r["energy_kwh"] for r in self._readings)
        total_carbon = sum(r["carbon_g"] for r in self._readings)
        avg_pue = sum(r["pue"] for r in self._readings) / len(self._readings)

        return {
            "total_energy_kwh": round(total_energy, 4),
            "total_carbon_g": round(total_carbon, 2),
            "avg_carbon_per_kwh": round(total_carbon / max(total_energy, 0.0001), 2),
            "avg_pue": round(avg_pue, 2),
            "readings_count": len(self._readings),
            "period_start": self._readings[0]["timestamp"],
            "period_end": self._readings[-1]["timestamp"]
        }


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main():
    """Demonstrate green computing capabilities."""
    print("=" * 60)
    print("Green Computing Module Demo")
    print("=" * 60)

    # 1. Carbon Intensity
    print("\n--- Carbon Intensity ---")
    client = CarbonIntensityClient()
    for region in [GridRegion.DE, GridRegion.FR, GridRegion.US_CAL_CISO]:
        reading = client.get_current_intensity(region)
        print(f"  {region.value}: {reading.gCO2_per_kWh:.0f} gCO2eq/kWh, "
              f"{reading.renewable_percent:.0f}% renewable")

    # 2. DVFS
    print("\n--- DVFS Optimization ---")
    dvfs = DVFSController(cpu_id=0)
    for freq in [4500, 3000, 2000, 1200, 800]:
        dvfs.set_frequency_mhz(freq)
        power = dvfs.estimate_power_watts(utilization=0.5)
        print(f"  {freq}MHz: {power:.1f}W")
    savings = dvfs.power_savings_summary(hours_running=24)
    print(f"  Daily savings at min freq: {savings['power_saved_watts']:.1f}W, "
          f"{savings['carbon_saved_grams']:.2f}g CO2")

    # 3. Power Model
    print("\n--- Server Power Model ---")
    model = PowerModel(idle_power_watts=85, max_power_watts=350)
    for util in [0.1, 0.5, 1.0]:
        est = model.estimate(cpu_utilization=util)
        print(f"  CPU {util*100:.0f}%: {est.total_watts:.1f}W total, "
              f"PUE-adjusted: {est.with_pue(1.2):.1f}W")
    annual = model.annual_cost_estimate()
    print(f"  Annual: {annual['energy_kwh']:.0f} kWh, ${annual['cost_usd']:.0f}, "
          f"{annual['carbon_kg']:.0f} kg CO2")

    # 4. SCI Calculator
    print("\n--- Software Carbon Intensity ---")
    calc = SCICalculator(
        energy_measurements=[0.005, 0.004, 0.006, 0.003],
        carbon_intensity=250.0,
        embodied_carbon_g=1200.0
    )
    score = calc.compute(functional_unit="per-request", total_units=100000)
    print(f"  SCI: {score.gCO2eq:.6f} gCO2eq/request")
    print(f"  Energy: {score.energy_kwh:.6f} kWh/request")

    # 5. Workload Scheduler
    print("\n--- Carbon-Aware Scheduling ---")
    scheduler = WorkloadScheduler(region=GridRegion.DE)
    window = scheduler.find_low_carbon_window(task_duration_hours=4, max_delay_hours=12)
    print(f"  Best window: {window.start.strftime('%H:%M')} - {window.end.strftime('%H:%M')}")
    print(f"  Avg intensity: {window.avg_gCO2_per_kWh:.0f} gCO2eq/kWh")
    print(f"  Savings vs average: {window.carbon_savings_vs_average:.1f}%")

    # 6. Dashboard
    print("\n--- Green Metrics Dashboard ---")
    dashboard = GreenMetricsDashboard()
    now = datetime.now(timezone.utc)
    for i in range(8):
        dashboard.record(
            timestamp=now + timedelta(hours=i),
            energy_kwh=0.5 + (i % 3) * 0.1,
            carbon_g=150 + (i % 3) * 30,
            pue=1.15 + (i % 2) * 0.05
        )
    summary = dashboard.summary()
    print(f"  Total energy: {summary['total_energy_kwh']:.1f} kWh")
    print(f"  Total carbon: {summary['total_carbon_g']:.0f} g CO2")
    print(f"  Avg PUE: {summary['avg_pue']:.2f}")
    print(f"  Readings: {summary['readings_count']}")

    print("\n" + "=" * 60)
    print("Demo complete.")


if __name__ == "__main__":
    main()
