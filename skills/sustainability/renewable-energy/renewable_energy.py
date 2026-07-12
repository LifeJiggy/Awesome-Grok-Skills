"""
Renewable Energy Module
Solar irradiance forecasting, wind power prediction, battery storage optimization,
grid balancing, energy trading, microgrid management, and REC tracking.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta, timezone
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums & Constants
# ---------------------------------------------------------------------------

class EnergySource(Enum):
    """Types of renewable energy sources."""
    SOLAR_PV = "solar_pv"
    SOLAR_THERMAL = "solar_thermal"
    ONSHORE_WIND = "onshore_wind"
    OFFSHORE_WIND = "offshore_wind"
    HYDROPOWER = "hydropower"
    GEOTHERMAL = "geothermal"
    BIOMASS = "biomass"


class BatteryChemistry(Enum):
    """Battery technology types."""
    LFP = "lfp"            # Lithium Iron Phosphate
    NMC = "nmc"            # Nickel Manganese Cobalt
    NCA = "nca"            # Nickel Cobalt Aluminum
    LTO = "lto"            # Lithium Titanate
    SODIUM_ION = "sodium_ion"
    FLOW = "flow"          # Vanadium Redox Flow


class GridMode(Enum):
    """Microgrid operating modes."""
    GRID_CONNECTED = "grid_connected"
    ISLANDED = "islanded"
    GRID_FOLLOWING = "grid_following"
    GRID_FORMING = "grid_forming"


class MarketType(Enum):
    """Energy market types."""
    DAY_AHEAD = "day_ahead"
    INTRADAY = "intraday"
    REAL_TIME = "real_time"
    ANCILLARY = "ancillary"
    CAPACITY = "capacity"


class BatteryAction(Enum):
    """Battery dispatch actions."""
    CHARGE = "charge"
    DISCHARGE = "discharge"
    IDLE = "idle"
    FLOAT = "float"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SolarForecast:
    """Solar generation forecast for a time period."""
    time: datetime
    power_kw: float
    irradiance_w_m2: float
    capacity_factor: float
    temperature_c: float
    clipped: bool = False

    @property
    def energy_kwh(self) -> float:
        return self.power_kw  # Per-hour resolution


@dataclass
class WindForecast:
    """Wind power forecast."""
    time: datetime
    power_kw: float
    wind_speed_ms: float
    wind_direction_deg: float
    capacity_factor: float
    air_density_kg_m3: float = 1.225
    wake_losses_percent: float = 0.0

    @property
    def net_power_kw(self) -> float:
        return self.power_kw * (1 - self.wake_losses_percent / 100)


@dataclass
class BatterySchedule:
    """Single hour battery dispatch instruction."""
    hour: int
    action: BatteryAction
    power_kw: float
    soc_start: float
    soc_end: float
    revenue_usd: float = 0.0
    degradation_cost_usd: float = 0.0

    @property
    def net_revenue(self) -> float:
        return self.revenue_usd - self.degradation_cost_usd


@dataclass
class MicrogridDispatch:
    """Dispatch result for a microgrid optimization."""
    solar_used_kw: float
    battery_action: BatteryAction
    battery_power_kw: float
    grid_import_kw: float
    grid_export_kw: float
    load_served_kw: float
    total_cost_usd: float
    renewable_fraction: float


@dataclass
class RECCertificate:
    """A Renewable Energy Certificate."""
    id: str
    source: EnergySource
    vintage: int
    region: str
    mwh: float
    retired: bool = False
    retirement_reason: str = ""
    issue_date: str = ""

    @property
    def is_available(self) -> bool:
        return not self.retired


@dataclass
class EnergyBid:
    """A bid in an energy market."""
    hour: int
    quantity_kwh: float
    price_cents: float
    bid_type: str = "sell"  # buy or sell
    cleared: bool = False


@dataclass
class PowerCurve:
    """Wind turbine power curve parameters."""
    cut_in_speed_ms: float = 3.5
    rated_speed_ms: float = 12.0
    cut_out_speed_ms: float = 25.0
    rated_power_kw: float = 3000.0
    hub_height_m: float = 100.0
    rotor_diameter_m: float = 112.0

    def power_at_speed(self, wind_speed_ms: float, air_density: float = 1.225) -> float:
        """Calculate power output at a given wind speed."""
        if wind_speed_ms < self.cut_in_speed_ms or wind_speed_ms >= self.cut_out_speed_ms:
            return 0.0
        if wind_speed_ms >= self.rated_speed_ms:
            return self.rated_power_kw
        # Cubic relationship between cut-in and rated speed
        ratio = (wind_speed_ms - self.cut_in_speed_ms) / \
                (self.rated_speed_ms - self.cut_in_speed_ms)
        return self.rated_power_kw * (ratio ** 3) * (air_density / 1.225)


# ---------------------------------------------------------------------------
# Solar Forecaster
# ---------------------------------------------------------------------------

class SolarForecaster:
    """
    Forecasts solar PV generation using physical models and weather data.
    Includes plane-of-array irradiance, temperature effects, and inverter clipping.
    """

    # Standard test conditions
    STC_IRRADIANCE = 1000.0  # W/m²
    STC_TEMPERATURE = 25.0   # °C
    TEMP_COEFF_POWER = -0.004  # %/°C (typical for crystalline silicon)

    def __init__(
        self,
        system_capacity_kw: float,
        tilt_degrees: float,
        azimuth_degrees: float,
        latitude: float,
        longitude: float,
        dc_ac_ratio: float = 1.2,
        module_efficiency: float = 0.20
    ):
        self.capacity_kw = system_capacity_kw
        self.tilt_rad = math.radians(tilt_degrees)
        self.azimuth_rad = math.radians(azimuth_degrees)
        self.latitude = latitude
        self.longitude = longitude
        self.dc_ac_ratio = dc_ac_ratio
        self.module_efficiency = module_efficiency
        self.dc_capacity_kw = system_capacity_kw * dc_ac_ratio

    def forecast_next_24h(self, temperature_c: float = 25.0) -> list[SolarForecast]:
        """Generate a 24-hour solar generation forecast."""
        forecasts = []
        now = datetime.now(timezone.utc)
        base_irradiance = self._peak_irradiance_for_latitude()

        for hour in range(24):
            t = now + timedelta(hours=hour)
            solar_hour = (t.hour - 12) * math.pi / 12  # Radians from solar noon

            # Irradiance follows cosine of solar angle
            if abs(solar_hour) > math.pi / 2:
                ghi = 0.0
            else:
                ghi = base_irradiance * math.cos(solar_hour)

            # Apply tilt and orientation factor
            poa = ghi * self._tilt_orientation_factor(solar_hour)

            # Temperature derating
            cell_temp = temperature_c + (poa / 800) * 25  # Heated above ambient
            temp_factor = 1.0 + self.TEMP_COEFF_POWER * (cell_temp - self.STC_TEMPERATURE)

            # DC power before clipping
            dc_power = self.dc_capacity_kw * (poa / self.STC_IRRADIANCE) * temp_factor
            dc_power = max(0.0, dc_power)

            # Inverter clipping
            clipped = dc_power > self.capacity_kw
            ac_power = min(dc_power, self.capacity_kw)

            cf = ac_power / self.capacity_kw if self.capacity_kw > 0 else 0.0

            forecasts.append(SolarForecast(
                time=t,
                power_kw=round(ac_power, 2),
                irradiance_w_m2=round(poa, 1),
                capacity_factor=round(min(1.0, cf), 3),
                temperature_c=round(cell_temp, 1),
                clipped=clipped
            ))

        return forecasts

    def _peak_irradiance_for_latitude(self) -> float:
        """Estimate peak irradiance based on latitude."""
        # Simple model: peak decreases slightly with latitude
        return 900.0 - abs(self.latitude) * 2.0

    def _tilt_orientation_factor(self, solar_hour_rad: float) -> float:
        """Factor for panel tilt and orientation relative to sun position."""
        cos_tilt = math.cos(self.tilt_rad)
        # Simplified: assume south-facing (azimuth ~180°)
        return 0.7 + 0.3 * cos_tilt * math.cos(solar_hour_rad)


# ---------------------------------------------------------------------------
# Wind Forecaster
# ---------------------------------------------------------------------------

class WindForecaster:
    """
    Forecasts wind power generation using power curve modeling with
    wake effects and air density corrections.
    """

    def __init__(
        self,
        turbine_rated_power_kw: float = 3000.0,
        hub_height_m: float = 100.0,
        rotor_diameter_m: float = 112.0,
        cut_in_ms: float = 3.5,
        rated_ms: float = 12.0,
        cut_out_ms: float = 25.0
    ):
        self.rated_power_kw = turbine_rated_power_kw
        self.hub_height_m = hub_height_m
        self.rotor_diameter_m = rotor_diameter_m
        self.power_curve = PowerCurve(
            cut_in_speed_ms=cut_in_ms,
            rated_speed_ms=rated_ms,
            cut_out_speed_ms=cut_out_ms,
            rated_power_kw=turbine_rated_power_kw,
            hub_height_m=hub_height_m,
            rotor_diameter_m=rotor_diameter_m
        )

    def predict(
        self,
        wind_speed_ms: float,
        wind_direction_deg: float,
        air_density_kg_m3: float = 1.225,
        turbulence_intensity: float = 0.10,
        hours: int = 1
    ) -> WindForecast:
        """Predict wind power output for given conditions."""
        # Adjust wind speed for hub height using power law
        hub_speed = self._wind_shear_adjustment(wind_speed_ms, measurement_height=10.0)

        # Calculate power from curve
        power = self.power_curve.power_at_speed(hub_speed, air_density_kg_m3)

        # Turbulence penalty (rough estimate)
        turbulence_penalty = 1.0 - turbulence_intensity * 0.5
        power *= turbulence_penalty

        cf = power / self.rated_power_kw if self.rated_power_kw > 0 else 0.0

        return WindForecast(
            time=datetime.now(timezone.utc),
            power_kw=round(power, 2),
            wind_speed_ms=round(hub_speed, 2),
            wind_direction_deg=wind_direction_deg,
            capacity_factor=round(min(1.0, max(0.0, cf)), 3),
            air_density_kg_m3=air_density_kg_m3,
            wake_losses_percent=round(turbulence_intensity * 50, 1)
        )

    def predict_farm(
        self,
        turbine_count: int,
        wind_speed_ms: float,
        wind_direction_deg: float,
        air_density_kg_m3: float = 1.225,
        spacing_rotor_diameters: float = 7.0
    ) -> dict:
        """Predict farm-level output accounting for wake losses."""
        # Jensen wake model (simplified)
        wake_loss_factor = 1.0 - (2 / (1 + spacing_rotor_diameters)) ** 2 * 0.3
        single = self.predict(wind_speed_ms, wind_direction_deg, air_density_kg_m3)
        farm_power = single.power_kw * turbine_count * wake_loss_factor
        farm_cf = farm_power / (self.rated_power_kw * turbine_count) if turbine_count > 0 else 0

        return {
            "turbine_count": turbine_count,
            "single_turbine_kw": single.power_kw,
            "farm_total_kw": round(farm_power, 2),
            "farm_capacity_factor": round(min(1.0, max(0.0, farm_cf)), 3),
            "wake_losses_percent": round((1 - wake_loss_factor) * 100, 1),
            "annual_energy_mwh": round(farm_power * 8760 / 1000, 0)
        }

    def _wind_shear_adjustment(self, speed_ms: float, measurement_height: float) -> float:
        """Adjust wind speed from measurement height to hub height."""
        alpha = 0.14  # Wind shear exponent (open terrain)
        return speed_ms * (self.hub_height_m / measurement_height) ** alpha


# ---------------------------------------------------------------------------
# Battery Storage Optimizer
# ---------------------------------------------------------------------------

class BatteryOptimizer:
    """
    Optimizes battery storage dispatch for energy arbitrage, peak shaving,
    and ancillary services with degradation-aware scheduling.
    """

    # LFP chemistry defaults
    DEFAULT_CYCLE_DEGRADATION = 0.0002   # 0.02% per full cycle
    DEFAULT_CALENDAR_DEGRADATION = 0.001  # 0.1% per month
    REPLACEMENT_COST_PER_KWH = 350.0     # USD

    def __init__(
        self,
        capacity_kwh: float = 1000.0,
        max_charge_kw: float = 250.0,
        max_discharge_kw: float = 250.0,
        round_trip_efficiency: float = 0.92,
        degradation_per_cycle: float = 0.0002,
        min_soc: float = 0.1,
        max_soc: float = 0.95,
        chemistry: BatteryChemistry = BatteryChemistry.LFP
    ):
        self.capacity_kwh = capacity_kwh
        self.max_charge_kw = max_charge_kw
        self.max_discharge_kw = max_discharge_kw
        self.rte = round_trip_efficiency
        self.degradation_per_cycle = degradation_per_cycle
        self.min_soc = min_soc
        self.max_soc = max_soc
        self.chemistry = chemistry

    def optimize_for_arbitrage(
        self,
        prices: list[float],
        current_soc: float = 0.5
    ) -> list[BatterySchedule]:
        """Optimize charge/discharge schedule for energy price arbitrage."""
        if len(prices) != 24:
            raise ValueError("Prices must be a 24-hour array")

        schedule = []
        soc = current_soc
        avg_price = sum(prices) / len(prices)

        for hour, price in enumerate(prices):
            charge_cost = price / (self.rte * 100)  # Cost to charge $/kWh
            discharge_revenue = price / 100  # Revenue from discharge $/kWh

            # Degradation cost per kWh throughput
            degradation_cost = self.degradation_per_cycle * self.REPLACEMENT_COST_PER_KWH / self.capacity_kwh

            # Decision logic
            if price < avg_price * 0.8 and soc < self.max_soc:
                # Low price: charge
                max_charge_kwh = (self.max_soc - soc) * self.capacity_kwh
                charge_kwh = min(max_charge_kwh, self.max_charge_kw)
                soc_delta = charge_kwh / self.capacity_kwh
                new_soc = min(self.max_soc, soc + soc_delta)
                cost = charge_kwh * charge_cost + charge_kwh * degradation_cost
                schedule.append(BatterySchedule(
                    hour=hour, action=BatteryAction.CHARGE,
                    power_kw=round(charge_kwh, 2),
                    soc_start=round(soc, 3), soc_end=round(new_soc, 3),
                    revenue_usd=0.0, degradation_cost_usd=round(cost, 4)
                ))
                soc = new_soc
            elif price > avg_price * 1.2 and soc > self.min_soc:
                # High price: discharge
                max_discharge_kwh = (soc - self.min_soc) * self.capacity_kwh
                discharge_kwh = min(max_discharge_kwh, self.max_discharge_kw)
                soc_delta = discharge_kwh / self.capacity_kwh
                new_soc = max(self.min_soc, soc - soc_delta)
                revenue = discharge_kwh * discharge_revenue
                deg_cost = discharge_kwh * degradation_cost
                schedule.append(BatterySchedule(
                    hour=hour, action=BatteryAction.DISCHARGE,
                    power_kw=round(discharge_kwh, 2),
                    soc_start=round(soc, 3), soc_end=round(new_soc, 3),
                    revenue_usd=round(revenue, 4),
                    degradation_cost_usd=round(deg_cost, 4)
                ))
                soc = new_soc
            else:
                schedule.append(BatterySchedule(
                    hour=hour, action=BatteryAction.IDLE,
                    power_kw=0.0, soc_start=round(soc, 3), soc_end=round(soc, 3)
                ))

        return schedule

    def peak_shaving_schedule(
        self,
        load_profile_kw: list[float],
        peak_threshold_kw: float,
        current_soc: float = 0.5
    ) -> list[BatterySchedule]:
        """Optimize battery for peak load shaving."""
        schedule = []
        soc = current_soc

        for hour, load in enumerate(load_profile_kw):
            if load > peak_threshold_kw and soc > self.min_soc:
                # Discharge to shave peak
                excess = load - peak_threshold_kw
                discharge_kwh = min(excess, self.max_discharge_kw,
                                    (soc - self.min_soc) * self.capacity_kwh)
                soc_delta = discharge_kwh / self.capacity_kwh
                new_soc = max(self.min_soc, soc - soc_delta)
                schedule.append(BatterySchedule(
                    hour=hour, action=BatteryAction.DISCHARGE,
                    power_kw=round(discharge_kwh, 2),
                    soc_start=round(soc, 3), soc_end=round(new_soc, 3)
                ))
                soc = new_soc
            elif load < peak_threshold_kw * 0.6 and soc < self.max_soc:
                # Charge during off-peak
                charge_kwh = min(self.max_charge_kw,
                                 (self.max_soc - soc) * self.capacity_kwh)
                soc_delta = charge_kwh / self.capacity_kwh
                new_soc = min(self.max_soc, soc + soc_delta)
                schedule.append(BatterySchedule(
                    hour=hour, action=BatteryAction.CHARGE,
                    power_kw=round(charge_kwh, 2),
                    soc_start=round(soc, 3), soc_end=round(new_soc, 3)
                ))
                soc = new_soc
            else:
                schedule.append(BatterySchedule(
                    hour=hour, action=BatteryAction.IDLE,
                    power_kw=0.0, soc_start=round(soc, 3), soc_end=round(soc, 3)
                ))

        return schedule

    def health_report(self, cycles_completed: float, months_online: float) -> dict:
        """Generate battery health and remaining life report."""
        cycle_degradation = cycles_completed * self.degradation_per_cycle
        calendar_degradation = months_online * self.DEFAULT_CALENDAR_DEGRADATION
        total_degradation = min(0.8, cycle_degradation + calendar_degradation)  # Cap at 80% loss
        remaining_capacity = 1.0 - total_degradation
        remaining_cycles = (0.8 - remaining_capacity) / self.degradation_per_cycle
        replacement_cost = self.capacity_kwh * self.REPLACEMENT_COST_PER_KWH

        return {
            "remaining_capacity_percent": round(remaining_capacity * 100, 1),
            "cycle_degradation_percent": round(cycle_degradation * 100, 2),
            "calendar_degradation_percent": round(calendar_degradation * 100, 2),
            "estimated_remaining_cycles": max(0, round(remaining_cycles, 0)),
            "replacement_cost_usd": round(replacement_cost, 0),
            "eol_threshold_percent": 80.0,
            "status": "healthy" if remaining_capacity > 0.8 else "degraded" if remaining_capacity > 0.6 else "critical"
        }


# ---------------------------------------------------------------------------
# Microgrid Manager
# ---------------------------------------------------------------------------

class MicrogridManager:
    """Manages a microgrid with solar, battery, and load resources."""

    def __init__(self, name: str = "Microgrid"):
        self.name = name
        self._solar_capacity_kw = 0.0
        self._battery_capacity_kwh = 0.0
        self._battery_max_kw = 0.0
        self._load_typical_kw = 0.0
        self._load_critical_kw = 0.0

    def add_solar(self, capacity_kw: float) -> None:
        self._solar_capacity_kw += capacity_kw

    def add_battery(self, capacity_kwh: float, max_power_kw: float) -> None:
        self._battery_capacity_kwh += capacity_kwh
        self._battery_max_kw += max_power_kw

    def add_load(self, typical_kw: float, critical_kw: float) -> None:
        self._load_typical_kw += typical_kw
        self._load_critical_kw += critical_kw

    def optimize_dispatch(
        self,
        solar_forecast_kw: float,
        grid_price_cents: float,
        battery_soc: float = 0.5,
        mode: str = "grid_connected",
        grid_export_limit_kw: float = 200.0,
        grid_import_limit_kw: float = 500.0
    ) -> MicrogridDispatch:
        """Optimize dispatch for the current time step."""
        load = self._load_typical_kw

        # Priority: solar first, then battery, then grid
        solar_used = min(solar_forecast_kw, load)
        remaining_load = load - solar_used

        battery_action = BatteryAction.IDLE
        battery_power = 0.0

        if remaining_load > 0 and battery_soc > 0.2:
            # Discharge battery
            battery_power = min(remaining_load, self._battery_max_kw,
                                (battery_soc - 0.1) * self._battery_capacity_kwh)
            battery_action = BatteryAction.DISCHARGE
            remaining_load -= battery_power
        elif solar_forecast_kw > load and battery_soc < 0.9:
            # Excess solar: charge battery
            excess = solar_forecast_kw - load
            battery_power = min(excess, self._battery_max_kw,
                                (0.95 - battery_soc) * self._battery_capacity_kwh)
            battery_action = BatteryAction.CHARGE

        grid_import = max(0, remaining_load)
        grid_export = max(0, solar_forecast_kw - load - battery_power if battery_action == BatteryAction.CHARGE else 0)

        # Apply grid limits
        grid_import = min(grid_import, grid_import_limit_kw)
        grid_export = min(grid_export, grid_export_limit_kw)

        # Calculate renewable fraction
        total_served = load
        renewable = solar_used + (battery_power if battery_action == BatteryAction.DISCHARGE else 0)
        ren_fraction = renewable / total_served if total_served > 0 else 0

        # Cost
        import_cost = grid_import * grid_price_cents / 100
        export_revenue = grid_export * grid_price_cents / 100 * 0.8  # Feed-in tariff

        return MicrogridDispatch(
            solar_used_kw=round(solar_used, 2),
            battery_action=battery_action,
            battery_power_kw=round(battery_power, 2),
            grid_import_kw=round(grid_import, 2),
            grid_export_kw=round(grid_export, 2),
            load_served_kw=round(load, 2),
            total_cost_usd=round(import_cost - export_revenue, 4),
            renewable_fraction=round(min(1.0, ren_fraction), 3)
        )


# ---------------------------------------------------------------------------
# REC Tracker
# ---------------------------------------------------------------------------

class RECTracker:
    """Tracks Renewable Energy Certificates through issuance, transfer, and retirement."""

    def __init__(self):
        self._certificates: list[RECCertificate] = []
        self._counter = 0

    def issue(self, certificates: float, source: str, vintage: int, region: str) -> list[RECCertificate]:
        """Issue new RECs."""
        issued = []
        for _ in range(int(certificates)):
            self._counter += 1
            cert = RECCertificate(
                id=f"REC-{self._counter:06d}",
                source=EnergySource(source),
                vintage=vintage,
                region=region,
                mwh=1.0,
                issue_date=date.today().isoformat() if hasattr(date, 'today') else datetime.now().strftime("%Y-%m-%d")
            )
            self._certificates.append(cert)
            issued.append(cert)
        return issued

    def retire(self, certificates: int, reason: str = "") -> dict:
        """Retire RECs (oldest vintage first)."""
        available = [c for c in self._certificates if c.is_available]
        available.sort(key=lambda c: c.vintage)

        retired = 0
        for cert in available[:certificates]:
            cert.retired = True
            cert.retirement_reason = reason
            retired += 1

        return {
            "retired": retired,
            "remaining": self.balance(),
            "reason": reason
        }

    def balance(self, source: Optional[str] = None) -> float:
        """Get total unretired REC balance."""
        available = [c for c in self._certificates if c.is_available]
        if source:
            available = [c for c in available if c.source.value == source]
        return sum(c.mwh for c in available)

    def portfolio_summary(self) -> dict:
        """Summary of REC portfolio."""
        total = len(self._certificates)
        retired = sum(1 for c in self._certificates if c.retired)
        by_source = {}
        for cert in self._certificates:
            src = cert.source.value
            if src not in by_source:
                by_source[src] = {"total": 0, "available": 0, "retired": 0}
            by_source[src]["total"] += 1
            if cert.retired:
                by_source[src]["retired"] += 1
            else:
                by_source[src]["available"] += 1

        return {
            "total_certificates": total,
            "retired": retired,
            "available": total - retired,
            "by_source": by_source
        }


# ---------------------------------------------------------------------------
# Energy Trader
# ---------------------------------------------------------------------------

class EnergyTrader:
    """Generates market bids for energy trading based on forecasts and prices."""

    def __init__(self, market: str = "PJM"):
        self.market = market

    def generate_day_ahead_bids(
        self,
        generation_forecast_kwh: list[float],
        price_forecast_cents: list[float],
        min_price_cents: float = 2.0,
        risk_margin: float = 0.9
    ) -> list[EnergyBid]:
        """Generate day-ahead market bids."""
        if len(generation_forecast_kwh) != len(price_forecast_cents):
            raise ValueError("Forecast arrays must have equal length")

        bids = []
        for hour, (gen, price) in enumerate(zip(generation_forecast_kwh, price_forecast_cents)):
            if price >= min_price_cents:
                # Apply risk margin: bid slightly less than forecast
                bid_quantity = gen * risk_margin
                bids.append(EnergyBid(
                    hour=hour,
                    quantity_kwh=round(bid_quantity, 2),
                    price_cents=round(price, 2),
                    bid_type="sell"
                ))

        return bids

    def calculate_settlement(self, bids: list[EnergyBid], actual_generation_kwh: list[float]) -> dict:
        """Calculate settlement from bid execution and actual generation."""
        total_bid_volume = sum(b.quantity_kwh for b in bids if b.bid_type == "sell")
        total_revenue = sum(b.quantity_kwh * b.price_cents / 100 for b in bids if b.bid_type == "sell")
        total_actual = sum(actual_generation_kwh[:len(bids)])

        # Imbalance calculation
        imbalance = total_actual - total_bid_volume
        imbalance_penalty_cents = 5.0  # Typical imbalance penalty

        return {
            "total_bid_volume_kwh": round(total_bid_volume, 2),
            "total_actual_generation_kwh": round(total_actual, 2),
            "imbalance_kwh": round(imbalance, 2),
            "base_revenue_usd": round(total_revenue, 2),
            "imbalance_cost_usd": round(max(0, abs(imbalance)) * imbalance_penalty_cents / 100, 2),
            "net_revenue_usd": round(total_revenue - max(0, abs(imbalance)) * imbalance_penalty_cents / 100, 2)
        }


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main():
    """Demonstrate Renewable Energy module capabilities."""
    print("=" * 60)
    print("Renewable Energy Module Demo")
    print("=" * 60)

    # 1. Solar Forecasting
    print("\n--- Solar Irradiance Forecast ---")
    solar = SolarForecaster(
        system_capacity_kw=500, tilt_degrees=30, azimuth_degrees=180,
        latitude=37.77, longitude=-122.42
    )
    forecast = solar.forecast_next_24h(temperature_c=25.0)
    peak = max(forecast, key=lambda f: f.power_kw)
    total_energy = sum(f.energy_kwh for f in forecast)
    print(f"  Peak output: {peak.power_kw:.1f} kW at {peak.time.strftime('%H:%M')}")
    print(f"  Daily generation: {total_energy:.1f} kWh")
    clipped = sum(1 for f in forecast if f.clipped)
    print(f"  Clipped hours: {clipped}")

    # 2. Wind Power Prediction
    print("\n--- Wind Power Prediction ---")
    wind = WindForecaster(turbine_rated_power_kw=3000, hub_height_m=100)
    single = wind.predict(wind_speed_ms=8.5, wind_direction_deg=225)
    print(f"  Single turbine: {single.power_kw:.0f} kW ({single.capacity_factor:.0%} CF)")
    farm = wind.predict_farm(turbine_count=20, wind_speed_ms=8.5, wind_direction_deg=225)
    print(f"  Farm (20 turbines): {farm['farm_total_kw']:.0f} kW")
    print(f"  Wake losses: {farm['wake_losses_percent']:.1f}%")
    print(f"  Annual energy: {farm['annual_energy_mwh']:.0f} MWh")

    # 3. Battery Optimization
    print("\n--- Battery Storage Optimization ---")
    battery = BatteryOptimizer(capacity_kwh=1000, max_charge_kw=250, max_discharge_kw=250)
    prices = [45, 42, 38, 35, 33, 30, 28, 32, 48, 65, 85, 95,
              110, 120, 95, 75, 60, 55, 70, 85, 100, 90, 70, 50]
    schedule = battery.optimize_for_arbitrage(prices, current_soc=0.5)
    total_revenue = sum(s.net_revenue for s in schedule)
    charge_hours = sum(1 for s in schedule if s.action == BatteryAction.CHARGE)
    discharge_hours = sum(1 for s in schedule if s.action == BatteryAction.DISCHARGE)
    print(f"  Arbitrage revenue: ${total_revenue:.2f}")
    print(f"  Charge hours: {charge_hours}, Discharge hours: {discharge_hours}")

    # Battery health
    health = battery.health_report(cycles_completed=1500, months_online=36)
    print(f"  Remaining capacity: {health['remaining_capacity_percent']}%")
    print(f"  Status: {health['status']}")

    # 4. Microgrid
    print("\n--- Microgrid Dispatch ---")
    microgrid = MicrogridManager("Campus")
    microgrid.add_solar(200)
    microgrid.add_battery(500, 125)
    microgrid.add_load(180, 50)
    dispatch = microgrid.optimize_dispatch(solar_forecast_kw=150, grid_price_cents=12.0)
    print(f"  Solar used: {dispatch.solar_used_kw:.0f} kW")
    print(f"  Battery: {dispatch.battery_action.value} {dispatch.battery_power_kw:.0f} kW")
    print(f"  Grid import: {dispatch.grid_import_kw:.0f} kW")
    print(f"  Renewable fraction: {dispatch.renewable_fraction:.0%}")

    # 5. REC Tracking
    print("\n--- REC Portfolio ---")
    recs = RECTracker()
    recs.issue(100, "solar_pv", 2025, "US-CA")
    recs.issue(50, "onshore_wind", 2025, "US-TX")
    recs.retire(30, "Scope 2 compliance")
    summary = recs.portfolio_summary()
    print(f"  Total: {summary['total_certificates']}, Available: {summary['available']}")
    print(f"  Solar available: {summary['by_source']['solar_pv']['available']}")

    # 6. Energy Trading
    print("\n--- Day-Ahead Bidding ---")
    trader = EnergyTrader("PJM")
    bids = trader.generate_day_ahead_bids(
        generation_forecast_kwh=[100]*6 + [150]*6 + [200]*6 + [100]*6,
        price_forecast_cents=[3.5, 3.2, 3.0, 2.8, 3.1, 4.5,
                              6.0, 5.5, 5.0, 4.8, 4.5, 4.2,
                              4.0, 3.8, 3.5, 3.3, 3.2, 4.0,
                              6.5, 8.0, 9.5, 7.0, 5.0, 3.8]
    )
    total_volume = sum(b.quantity_kwh for b in bids)
    total_value = sum(b.quantity_kwh * b.price_cents / 100 for b in bids)
    print(f"  Bid volume: {total_volume:,.0f} kWh")
    print(f"  Bid value: ${total_value:,.2f}")

    print("\n" + "=" * 60)
    print("Demo complete.")


if __name__ == "__main__":
    main()
