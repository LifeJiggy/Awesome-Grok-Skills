"""
Ground Stations Toolkit
Antenna tracking, signal processing, telemetry, Doppler, link budgets,
network coordination, rain fade, polarization.
"""

from __future__ import annotations

import math
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, List, Tuple, Dict, Any

import numpy as np


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AntennaMount(Enum):
    AZ_EL = "az_el"
    X_Y = "x_y"
    EQUATORIAL = "equatorial"
    POLAR = "polar"


class ModulationType(Enum):
    BPSK = "BPSK"
    QPSK = "QPSK"
    8PSK = "8PSK"
    16QAM = "16QAM"
    PCM_FM = "PCM/FM"


class CodingType(Enum):
    NONE = "none"
    CONVOLUTIONAL = "convolutional"
    REED_SOLOMON = "reed_solomon"
    LDPC = "ldpc"
    TURBO = "turbo"
    CONCATENATED = "concatenated"


class PolarizationType(Enum):
    LINEAR_H = "linear_h"
    LINEAR_V = "linear_v"
    CIRCULAR_LHCP = "lhcp"
    CIRCULAR_RHCP = "rhcp"
    RIGHT_HAND = "rhcp"
    LEFT_HAND = "lhcp"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class AntennaConfig:
    mount_type: AntennaMount = AntennaMount.AZ_EL
    aperture_m: float = 7.0
    frequency_ghz: float = 8.0
    gain_dbi: float = 48.0
    beamwidth_deg: float = 0.35
    max_slew_rate_deg_s: float = 2.0
    polarization: PolarizationType = PolarizationType.CIRCULAR_RHCP
    noise_temp_k: float = 30.0
    sidelobe_level_db: float = -20.0

    @property
    def wavelength_m(self) -> float:
        return 0.299792458 / self.frequency_ghz

    def gain_pattern(self, off_axis_angle_deg: float) -> float:
        """Antenna gain as function of off-axis angle (dB relative to boresight)."""
        if off_axis_angle_deg <= 0:
            return 0.0
        # First null approximation
        first_null = 1.22 * self.wavelength_m / self.aperture_m
        first_null_deg = math.degrees(first_null)
        if off_axis_angle_deg < first_null_deg:
            return -12.0 * (off_axis_angle_deg / first_null_deg) ** 2
        # Sidelobe region
        return self.sidelobe_level_db - 10.0 * math.log10(off_axis_angle_deg / first_null_deg)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["mount_type"] = self.mount_type.value
        d["polarization"] = self.polarization.value
        return d


@dataclass
class SatelliteState:
    time_s: float
    position_eci: List[float]  # [x, y, z] in meters
    velocity_eci: List[float]  # [vx, vy, vz] in m/s

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PointingResult:
    azimuth_deg: float
    elevation_deg: float
    range_km: float
    slew_rate_deg_s: float
    pointing_loss_db: float
    elevation_rate_deg_s: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ChainComponent:
    name: str
    gain_db: float = 0.0
    noise_figure_db: float = 0.0
    noise_temp_k: float = 0.0
    gain_dbi: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SignalChainResult:
    system_noise_temp_k: float
    system_noise_figure_db: float
    g_over_t_db: float
    total_gain_db: float
    carrier_to_noise_density: float  # C/N0 in dB-Hz
    components: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DopplerEntry:
    time_s: float
    doppler_shift_hz: float
    doppler_rate_hz_s: float
    range_rate_ms: float
    slant_range_km: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LinkMarginResult:
    eirp_dbw: float
    free_space_loss_db: float
    atmospheric_loss_db: float
    rain_loss_db: float
    pointing_loss_db: float
    polarization_loss_db: float
    received_power_dbw: float
    noise_power_dbw: float
    eb_n0_db: float
    required_eb_n0_db: float
    margin_db: float
    data_rate_mbps: float
    availability_pct: float
    ber: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PassSchedule:
    station_name: str
    satellite_name: str
    aos_time_s: float
    los_time_s: float
    max_elevation_deg: float
    duration_s: float
    max_doppler_shift_hz: float
    data_capacity_gb: float
    link_margin_db: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NetworkStatus:
    total_stations: int
    active_passes: int
    total_utilization_pct: float
    stations_status: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RainFadeResult:
    specific_attenuation_db_km: float
    effective_path_length_km: float
    total_attenuation_db: float
    availability_with_diversity_pct: float
    diversity_gain_db: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PolarizationResult:
    axial_ratio_db: float
    cross_polarization_isolation_db: float
    faraday_rotation_deg: float
    effective_polarization_loss_db: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Core Classes
# ---------------------------------------------------------------------------

class AntennaTracker:
    """Antenna pointing and tracking geometry."""

    EARTH_RADIUS_M = 6371000.0
    SPEED_OF_LIGHT = 299792458.0

    def __init__(self, station_lat_deg: float, station_lon_deg: float, station_alt_m: float,
                 antenna: Optional[AntennaConfig] = None):
        self.lat = math.radians(station_lat_deg)
        self.lon = math.radians(station_lon_deg)
        self.alt = station_alt_m
        self.antenna = antenna or AntennaConfig()
        self._prev_pointing: Optional[PointingResult] = None

    def _eci_to_enu(self, sat_pos_eci: np.ndarray) -> np.ndarray:
        """Convert ECI position to East-North-Up relative to station."""
        # Station ECEF position (simplified, no rotation)
        R = self.EARTH_RADIUS_M + self.alt
        station_eci = R * np.array([
            math.cos(self.lat) * math.cos(self.lon),
            math.cos(self.lat) * math.sin(self.lon),
            math.sin(self.lat),
        ])
        dpos = sat_pos_eci - station_eci
        range_m = np.linalg.norm(dpos)

        # ENU rotation
        cos_lat, sin_lat = math.cos(self.lat), math.sin(self.lat)
        cos_lon, sin_lon = math.cos(self.lon), math.sin(self.lon)
        R_enu = np.array([
            [-sin_lon, cos_lon, 0],
            [-sin_lat * cos_lon, -sin_lat * sin_lon, cos_lat],
            [cos_lat * cos_lon, cos_lat * sin_lon, sin_lat],
        ])
        enu = R_enu @ dpos
        return enu

    def compute_pointing(self, sat_eci: List[float], prev_time_s: float = 0.0,
                         current_time_s: float = 0.0) -> PointingResult:
        """Compute azimuth, elevation, and slew rate for satellite tracking."""
        enu = self._eci_to_enu(np.array(sat_eci))
        east, north, up = enu

        # Azimuth and elevation
        horizontal_dist = math.sqrt(east ** 2 + north ** 2)
        azimuth = math.degrees(math.atan2(east, north))
        if azimuth < 0:
            azimuth += 360.0
        elevation = math.degrees(math.atan2(up, horizontal_dist))
        range_km = np.linalg.norm(enu) / 1000.0

        # Slew rate (simplified)
        slew_rate = 0.0
        elev_rate = 0.0
        if self._prev_pointing and current_time_s > prev_time_s:
            dt = current_time_s - prev_time_s
            if dt > 0:
                daz = azimuth - self._prev_pointing.azimuth_deg
                if daz > 180:
                    daz -= 360
                elif daz < -180:
                    daz += 360
                slew_rate = abs(daz / dt)
                elev_rate = abs((elevation - self._prev_pointing.elevation_deg) / dt)

        # Pointing loss
        pointing_loss = 10 ** (-self.antenna.get_pattern_loss_db(elevation) / 10) if hasattr(self.antenna, 'get_pattern_loss_db') else 0.125

        result = PointingResult(
            azimuth_deg=azimuth,
            elevation_deg=elevation,
            range_km=range_km,
            slew_rate_deg_s=slew_rate,
            pointing_loss_db=0.125,  # typical 0.1-0.2 dB for well-tracked antenna
            elevation_rate_deg_s=elev_rate,
        )
        self._prev_pointing = result
        return result

    def tracking_loop_simulation(
        self, trajectory: List[Tuple[float, List[float]]], dt_s: float = 0.1
    ) -> List[PointingResult]:
        """Simulate antenna tracking loop over a trajectory."""
        results = []
        for i, (t, sat_eci) in enumerate(trajectory):
            prev_t = trajectory[i-1][0] if i > 0 else 0.0
            result = self.compute_pointing(sat_eci, prev_t, t)
            results.append(result)
        return results

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lat_deg": math.degrees(self.lat),
            "lon_deg": math.degrees(self.lon),
            "alt_m": self.alt,
            "antenna": self.antenna.to_dict(),
        }


class SignalChainAnalyzer:
    """Signal processing chain noise figure and SNR analysis."""

    K_BOLTZMANN = 1.380649e-23

    def __init__(self, frequency_ghz: float, bandwidth_mhz: float):
        self.frequency_ghz = frequency_ghz
        self.bandwidth_mhz = bandwidth_mhz
        self.bandwidth_hz = bandwidth_mhz * 1e6
        self.components: List[ChainComponent] = []

    def add_component(self, component: ChainComponent):
        self.components.append(component)

    def _noise_figure_cascade(self) -> Tuple[float, float]:
        """Friis noise figure cascade calculation."""
        # Convert first component gain to linear
        if not self.components:
            return 290.0, 0.0

        total_gain_linear = 1.0
        total_noise_temp = 0.0
        T0 = 290.0  # reference temperature

        for i, comp in enumerate(self.components):
            # Component noise temperature
            if comp.noise_temp_k > 0:
                T_comp = comp.noise_temp_k
            elif comp.noise_figure_db > 0:
                T_comp = T0 * (10 ** (comp.noise_figure_db / 10.0) - 1.0)
            else:
                T_comp = 0.0

            # Component gain (linear)
            if comp.gain_dbi > 0:
                G_comp = 10 ** (comp.gain_dbi / 10.0)
            else:
                G_comp = 10 ** (comp.gain_db / 10.0)

            # Friis formula
            total_noise_temp += T_comp / total_gain_linear
            total_gain_linear *= G_comp

        total_nf_db = 10.0 * math.log10(1.0 + total_noise_temp / T0) if total_noise_temp > 0 else 0.0
        return total_noise_temp, total_nf_db

    def compute(self) -> SignalChainResult:
        """Compute signal chain performance."""
        noise_temp, nf_db = self._noise_figure_cascade()

        # Total gain
        total_gain_db = sum(c.gain_db if c.gain_db != 0 else c.gain_dbi for c in self.components)

        # Antenna gain (first component typically)
        antenna_gain_dbi = self.components[0].gain_dbi if self.components else 0.0
        antenna_noise_temp = self.components[0].noise_temp_k if self.components else 290.0

        # System noise temperature (antenna + receiver)
        T_sys = antenna_noise_temp + noise_temp

        # G/T
        g_over_t = antenna_gain_dbi - 10 * math.log10(T_sys) if T_sys > 0 else 0.0

        # C/N0 for reference
        c_n0 = g_over_t + 10 * math.log10(self.bandwidth_hz) - 10 * math.log10(self.K_BOLTZMANN)

        return SignalChainResult(
            system_noise_temp_k=T_sys,
            system_noise_figure_db=nf_db,
            g_over_t_db=g_over_t,
            total_gain_db=total_gain_db,
            carrier_to_noise_density=c_n0,
            components=[c.to_dict() for c in self.components],
        )


class DopplerCompensator:
    """Doppler shift computation and compensation table generation."""

    SPEED_OF_LIGHT = 299792458.0
    EARTH_RADIUS_M = 6371000.0

    def __init__(self, frequency_hz: float):
        self.frequency_hz = frequency_hz

    def _doppler_shift(self, range_rate_ms: float) -> float:
        """Doppler frequency shift in Hz."""
        return -self.frequency_hz * range_rate_ms / self.SPEED_OF_LIGHT

    def compute_for_pass(
        self, sat_states: List[SatelliteState], ground_lat_deg: float, ground_lon_deg: float
    ) -> List[DopplerEntry]:
        """Compute Doppler shift for each satellite state."""
        lat_r = math.radians(ground_lat_deg)
        lon_r = math.radians(ground_lon_deg)
        R = self.EARTH_RADIUS_M
        gs_pos = R * np.array([
            math.cos(lat_r) * math.cos(lon_r),
            math.cos(lat_r) * math.sin(lon_r),
            math.sin(lat_r),
        ])

        entries = []
        prev_shift = 0.0
        prev_time = 0.0

        for state in sat_states:
            sat_pos = np.array(state.position_eci)
            sat_vel = np.array(state.velocity_eci)

            los = sat_pos - gs_pos
            range_m = np.linalg.norm(los)
            los_unit = los / range_m

            # Range rate (radial velocity)
            range_rate = np.dot(sat_vel, los_unit)
            doppler = self._doppler_shift(range_rate)

            # Doppler rate
            dt = state.time_s - prev_time if prev_time > 0 else 1.0
            doppler_rate = (doppler - prev_shift) / dt if dt > 0 else 0.0

            entries.append(DopplerEntry(
                time_s=state.time_s,
                doppler_shift_hz=doppler,
                doppler_rate_hz_s=doppler_rate,
                range_rate_ms=float(range_rate),
                slant_range_km=range_m / 1000.0,
            ))

            prev_shift = doppler
            prev_time = state.time_s

        return entries

    def generate_compensation_table(
        self, sat_states: List[SatelliteState], ground_lat: float, ground_lon: float,
        time_step_s: float = 1.0
    ) -> List[Dict[str, Any]]:
        """Generate frequency compensation table for receiver."""
        entries = self.compute_for_pass(sat_states, ground_lat, ground_lon)
        return [
            {
                "time_s": e.time_s,
                "doppler_shift_hz": e.doppler_shift_hz,
                "doppler_rate_hz_s": e.doppler_rate_hz_s,
                "compensation_freq_hz": -e.doppler_shift_hz,
            }
            for e in entries
        ]


class LinkMarginAnalyzer:
    """End-to-end link margin computation."""

    K_BOLTZMANN = 1.380649e-23
    SPEED_OF_LIGHT = 299792458.0

    def __init__(
        self,
        frequency_ghz: float,
        data_rate_mbps: float,
        modulation: str = "QPSK",
        coding_rate: float = 0.75,
        satellite_eirp_dbw: float = 20.0,
        satellite_antenna_gain_dbi: float = 18.0,
        ground_antenna_gain_dbi: float = 48.0,
        ground_noise_temp_k: float = 50.0,
    ):
        self.freq_ghz = frequency_ghz
        self.freq_hz = frequency_ghz * 1e9
        self.data_rate_mbps = data_rate_mbps
        self.data_rate_bps = data_rate_mbps * 1e6
        self.modulation = modulation
        self.coding_rate = coding_rate
        self.eirp = satellite_eirp_dbw
        self.sat_gain = satellite_antenna_gain_dbi
        self.gs_gain = ground_antenna_gain_dbi
        self.gs_noise_temp = ground_noise_temp_k

    def _free_space_loss(self, distance_km: float) -> float:
        """FSPL in dB."""
        distance_m = distance_km * 1000.0
        wavelength = self.SPEED_OF_LIGHT / self.freq_hz
        return 20.0 * math.log10(4.0 * math.pi * distance_m / wavelength)

    def _atmospheric_loss(self, elevation_deg: float) -> float:
        """ITU-R P.676 atmospheric absorption (dB)."""
        slant_factor = 1.0 / math.sin(math.radians(max(elevation_deg, 5.0)))
        # Empirical model for O2 and H2O absorption
        base_loss = 0.04 + 0.01 * self.freq_ghz
        return base_loss * slant_factor

    def _rain_loss(self, elevation_deg: float, rain_rate_mm_hr: float) -> float:
        """ITU-R P.618 rain attenuation (dB)."""
        if rain_rate_mm_hr <= 0:
            return 0.0
        k = 0.00012 * self.freq_ghz ** 1.5
        alpha = 1.15
        gamma_r = k * rain_rate_mm_hr ** alpha
        slant_path = 5.0 / math.sin(math.radians(max(elevation_deg, 5.0)))
        return gamma_r * slant_path

    def _coding_gain(self) -> float:
        """Coding gain for specified coding scheme."""
        gains = {
            "none": 0.0,
            "convolutional": 5.0,
            "reed_solomon": 2.0,
            "ldpc": 10.0,
            "turbo": 10.5,
            "concatenated": 7.0,
        }
        return gains.get(self.modulation.lower(), 0.0) * self.coding_rate

    def _modulation_required_eb_n0(self) -> float:
        """Required Eb/N0 for target BER (1e-6) with modulation."""
        required = {
            "BPSK": 10.5,
            "QPSK": 10.5,
            "8PSK": 14.0,
            "16QAM": 14.5,
            "PCM/FM": 11.0,
        }
        return required.get(self.modulation, 10.5)

    def compute_link_margin(
        self,
        range_km: float,
        elevation_deg: float,
        rain_rate_mm_hr: float = 0.0,
        pointing_loss_db: float = 0.5,
        polarization_loss_db: float = 0.3,
        implementation_margin_db: float = 2.0,
    ) -> LinkMarginResult:
        """Compute end-to-end link margin."""
        # Losses
        fspl = self._free_space_loss(range_km)
        atm_loss = self._atmospheric_loss(elevation_deg)
        rain_loss = self._rain_loss(elevation_deg, rain_rate_mm_hr)

        # Total loss
        total_loss = fspl + atm_loss + rain_loss + pointing_loss_db + polarization_loss_db

        # Received power
        rx_power = self.eirp - total_loss + self.gs_gain

        # Noise power
        T_sys = self.gs_noise_temp + 290.0  # simplified
        noise_power = 10 * math.log10(self.K_BOLTZMANN * T_sys * self.data_rate_bps)

        # Eb/N0
        eb_n0 = rx_power - noise_power + 10 * math.log10(self.data_rate_bps) - 10 * math.log10(self.freq_hz)

        # Required Eb/N0 with coding gain
        required_ebn0 = self._modulation_required_eb_n0() - self._coding_gain() + implementation_margin_db

        margin = eb_n0 - required_ebn0

        # BER approximation
        eb_n0_linear = 10 ** (eb_n0 / 10.0)
        ber = 0.5 * math.erfc(math.sqrt(eb_n0_linear))

        # Availability (simplified)
        availability = 99.9 if rain_rate_mm_hr < 5 else (99.5 if rain_rate_mm_hr < 25 else 99.0)

        return LinkMarginResult(
            eirp_dbw=self.eirp,
            free_space_loss_db=fspl,
            atmospheric_loss_db=atm_loss,
            rain_loss_db=rain_loss,
            pointing_loss_db=pointing_loss_db,
            polarization_loss_db=polarization_loss_db,
            received_power_dbw=rx_power,
            noise_power_dbw=noise_power,
            eb_n0_db=eb_n0,
            required_eb_n0_db=required_ebn0,
            margin_db=margin,
            data_rate_mbps=self.data_rate_mbps,
            availability_pct=availability,
            ber=ber,
        )


class GroundStationNetwork:
    """Multi-station network coordination and handover."""

    def __init__(self):
        self.stations: List[Dict[str, Any]] = []
        self.active_passes: List[PassSchedule] = []

    def add_station(self, name: str, lat_deg: float, lon_deg: float, alt_m: float,
                    bandwidth_mbps: float = 150.0):
        self.stations.append({
            "name": name,
            "lat_deg": lat_deg,
            "lon_deg": lon_deg,
            "alt_m": alt_m,
            "bandwidth_mbps": bandwidth_mbps,
            "status": "available",
            "current_load_pct": 0.0,
        })

    def schedule_pass(self, station_name: str, satellite_name: str,
                      aos_s: float, los_s: float, max_elev: float,
                      doppler_shift: float, data_gb: float, margin_db: float) -> PassSchedule:
        """Schedule a pass on a station."""
        ps = PassSchedule(
            station_name=station_name,
            satellite_name=satellite_name,
            aos_time_s=aos_s,
            los_time_s=los_s,
            max_elevation_deg=max_elev,
            duration_s=los_s - aos_s,
            max_doppler_shift_hz=doppler_shift,
            data_capacity_gb=data_gb,
            link_margin_db=margin_db,
        )
        self.active_passes.append(ps)
        return ps

    def detect_handovers(self, satellite_name: str) -> List[Dict[str, Any]]:
        """Detect handover opportunities between stations for a satellite."""
        sat_passes = sorted(
            [p for p in self.active_passes if p.satellite_name == satellite_name],
            key=lambda p: p.aos_time_s,
        )
        handovers = []
        for i in range(len(sat_passes) - 1):
            current = sat_passes[i]
            next_pass = sat_passes[i + 1]
            gap = next_pass.aos_time_s - current.los_time_s
            handovers.append({
                "from_station": current.station_name,
                "to_station": next_pass.station_name,
                "gap_s": gap,
                "seamless": gap < 30.0,
            })
        return handovers

    def load_balance(self) -> Dict[str, float]:
        """Compute station utilization for load balancing."""
        station_usage: Dict[str, float] = {s["name"]: 0.0 for s in self.stations}
        for ps in self.active_passes:
            station_usage[ps.station_name] = station_usage.get(ps.station_name, 0.0) + ps.duration_s
        total_time = 86400.0  # 24 hours
        return {name: usage / total_time * 100 for name, usage in station_usage.items()}

    def failover_plan(self, failed_station: str) -> List[Dict[str, Any]]:
        """Generate failover plan when a station goes down."""
        affected_passes = [p for p in self.active_passes if p.station_name == failed_station]
        failover = []
        for ps in affected_passes:
            # Find alternative station with best elevation
            best_alt = -90.0
            best_station = None
            for s in self.stations:
                if s["name"] != failed_station and s["status"] == "available":
                    # Simplified: pick by latitude proximity
                    lat_diff = abs(s["lat_deg"] - 40.0)  # placeholder
                    if lat_diff < 30:
                        best_station = s["name"]
                        break
            if best_station:
                failover.append({
                    "pass": ps.to_dict(),
                    "failover_to": best_station,
                    "estimated_margin_loss_db": 3.0,
                })
        return failover

    def get_status(self) -> NetworkStatus:
        """Get network status summary."""
        utilization = self.load_balance()
        return NetworkStatus(
            total_stations=len(self.stations),
            active_passes=len(self.active_passes),
            total_utilization_pct=sum(utilization.values()) / max(len(utilization), 1),
            stations_status=[
                {"name": s["name"], "status": s["status"],
                 "utilization_pct": utilization.get(s["name"], 0.0)}
                for s in self.stations
            ],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stations": self.stations,
            "active_passes": len(self.active_passes),
        }


class RainFadeMitigator:
    """Rain fade analysis and mitigation strategy."""

    def __init__(self, frequency_ghz: float, site_altitude_m: float = 0.0):
        self.freq_ghz = frequency_ghz
        self.site_alt = site_altitude_m

    def specific_attenuation(self, rain_rate_mm_hr: float) -> float:
        """ITU-R P.838 specific attenuation (dB/km)."""
        k = 0.00012 * self.freq_ghz ** 1.5
        alpha = 1.15
        return k * rain_rate_mm_hr ** alpha

    def effective_path_length(self, elevation_deg: float, rain_rate_mm_hr: float) -> float:
        """ITU-R P.618 effective path length through rain."""
        slant_path = 5.0 / math.sin(math.radians(max(elevation_deg, 5.0)))
        # Reduction factor for non-uniform rain
        reduction = 1.0 - 0.3 / (1.0 + 0.01 * rain_rate_mm_hr)
        return slant_path * reduction

    def rain_attenuation(self, elevation_deg: float, rain_rate_mm_hr: float) -> RainFadeResult:
        """Compute rain fade for given conditions."""
        gamma = self.specific_attenuation(rain_rate_mm_hr)
        leff = self.effective_path_length(elevation_deg, rain_rate_mm_hr)
        total_atten = gamma * leff

        # Site diversity gain (simplified)
        diversity_gain = 0.0
        availability_with_diversity = 99.9
        if total_atten > 5.0:
            diversity_gain = min(6.0, total_atten * 0.3)
            availability_with_diversity = 99.95

        return RainFadeResult(
            specific_attenuation_db_km=gamma,
            effective_path_length_km=leff,
            total_attenuation_db=total_atten,
            availability_with_diversity_pct=availability_with_diversity,
            diversity_gain_db=diversity_gain,
        )

    def acm_thresholds(self) -> List[Dict[str, Any]]:
        """Adaptive coding and modulation thresholds."""
        return [
            {"rain_rate_mm_hr": 0, "modulation": "8PSK", "coding_rate": 0.85, "data_rate_factor": 1.0},
            {"rain_rate_mm_hr": 5, "modulation": "QPSK", "coding_rate": 0.75, "data_rate_factor": 0.8},
            {"rain_rate_mm_hr": 12, "modulation": "QPSK", "coding_rate": 0.5, "data_rate_factor": 0.5},
            {"rain_rate_mm_hr": 25, "modulation": "BPSK", "coding_rate": 0.5, "data_rate_factor": 0.3},
            {"rain_rate_mm_hr": 50, "modulation": "BPSK", "coding_rate": 1/3, "data_rate_factor": 0.15},
        ]

    def to_dict(self) -> Dict[str, Any]:
        return {"frequency_ghz": self.freq_ghz, "site_altitude_m": self.site_alt}


class PolarizationAnalyzer:
    """Polarization tracking and Faraday rotation analysis."""

    def __init__(self, frequency_ghz: float, polarization: PolarizationType):
        self.freq_ghz = frequency_ghz
        self.polarization = polarization

    def faraday_rotation(self, total_electron_content: float, magnetic_field_tesla: float = 3e-5) -> float:
        """Faraday rotation angle (degrees) for linear polarization through ionosphere."""
        freq_hz = self.freq_ghz * 1e9
        # Simplified formula: rotation ∝ TEC / f^2
        rotation_rad = 2.62e-13 * magnetic_field_tesla * total_electron_content / (freq_hz ** 2)
        return math.degrees(rotation_rad)

    def axial_ratio_analysis(self, off_axis_angle_deg: float = 0.0) -> float:
        """Circular polarization axial ratio (dB) as function of off-axis angle."""
        # Typical feed: axial ratio degrades off-axis
        return 0.5 + 0.1 * off_axis_angle_deg

    def cross_polarization_isolation(
        self, xpd_ideal_db: float = 30.0, pointing_error_deg: float = 0.05
    ) -> float:
        """Cross-polarization isolation accounting for pointing error."""
        # XPD degrades with pointing error
        xpd_loss = 10 * math.log10(1 + 10 ** (pointing_error_deg * 10))
        return xpd_ideal_db - xpd_loss

    def polarization_loss(self, intended: PolarizationType, actual_angle_deg: float = 0.0) -> float:
        """Polarization mismatch loss (dB)."""
        if intended in [PolarizationType.CIRCULAR_RHCP, PolarizationType.CIRCULAR_LHCP,
                        PolarizationType.RIGHT_HAND, PolarizationType.LEFT_HAND]:
            # Circular: loss due to axial ratio
            return 0.0  # ideal circular has no loss
        else:
            # Linear: cos^2 loss
            return -20.0 * math.log10(max(abs(math.cos(math.radians(actual_angle_deg))), 0.01))

    def compute(
        self, tec: float = 1e18, pointing_error_deg: float = 0.05
    ) -> PolarizationResult:
        """Full polarization analysis."""
        faraday = self.faraday_rotation(tec)
        axial = self.axial_ratio_analysis()
        xpi = self.cross_polarization_isolation(pointing_error_deg=pointing_error_deg)
        pol_loss = self.polarization_loss(self.polarization, pointing_error_deg)

        return PolarizationResult(
            axial_ratio_db=axial,
            cross_polarization_isolation_db=xpi,
            faraday_rotation_deg=faraday,
            effective_polarization_loss_db=abs(pol_loss),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"frequency_ghz": self.freq_ghz, "polarization": self.polarization.value}


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main():
    """Demonstrate the ground stations toolkit."""
    print("=" * 70)
    print("GROUND STATIONS TOOLKIT — DEMONSTRATION")
    print("=" * 70)

    # 1. Antenna Tracking
    print("\n--- Antenna Tracking ---")
    tracker = AntennaTracker(
        station_lat_deg=40.0, station_lon_deg=-75.0, station_alt_m=100.0,
        antenna=AntennaConfig(aperture_m=7.0, frequency_ghz=8.0, gain_dbi=48.0),
    )
    sat_eci = [1200000.0, -4500000.0, 4200000.0]
    pointing = tracker.compute_pointing(sat_eci)
    print(f"Az: {pointing.azimuth_deg:.2f}°, El: {pointing.elevation_deg:.2f}°")
    print(f"Range: {pointing.range_km:.1f} km, Pointing loss: {pointing.pointing_loss_db:.3f} dB")

    # 2. Signal Processing Chain
    print("\n--- Signal Processing Chain ---")
    chain = SignalChainAnalyzer(frequency_ghz=8.15, bandwidth_mhz=50.0)
    chain.add_component(ChainComponent("Antenna", gain_dbi=48.0, noise_temp_k=30.0))
    chain.add_component(ChainComponent("Feeder", gain_db=-0.5, noise_figure_db=0.3))
    chain.add_component(ChainComponent("LNA", gain_db=55.0, noise_figure_db=0.8))
    chain.add_component(ChainComponent("Mixer", gain_db=-6.0, noise_figure_db=8.0))
    chain.add_component(ChainComponent("IF Amp", gain_db=30.0, noise_figure_db=3.0))
    sig_result = chain.compute()
    print(f"T_sys: {sig_result.system_noise_temp_k:.1f} K")
    print(f"G/T: {sig_result.g_over_t_db:.2f} dB/K, NF: {sig_result.system_noise_figure_db:.2f} dB")

    # 3. Doppler
    print("\n--- Doppler Compensation ---")
    doppler = DopplerCompensator(frequency_hz=8150e6)
    sat_states = [
        SatelliteState(0, [7000000, 0, 0], [0, 7500, 0]),
        SatelliteState(10, [7000000, 75000, 0], [-100, 7500, 0]),
        SatelliteState(60, [7000000, 450000, 0], [-500, 7300, 0]),
    ]
    table = doppler.generate_compensation_table(sat_states, 40.0, -75.0)
    for entry in table:
        print(f"  T+{entry['time_s']:5.0f}s: Δf={entry['doppler_shift_hz']:.1f} Hz, "
              f"comp={entry['compensation_freq_hz']:.1f} Hz")

    # 4. Link Margin
    print("\n--- Link Margin Analysis ---")
    link = LinkMarginAnalyzer(
        frequency_ghz=8.15, data_rate_mbps=150.0, modulation="QPSK", coding_rate=0.75,
        satellite_eirp_dbw=20.0, ground_antenna_gain_dbi=48.0, ground_noise_temp_k=50.0,
    )
    lm = link.compute_link_margin(range_km=900, elevation_deg=45.0, rain_rate_mm_hr=12.0)
    print(f"Link margin: {lm.margin_db:.2f} dB, Eb/N0: {lm.eb_n0_db:.1f} dB")
    print(f"Availability: {lm.availability_pct:.2f}%, BER: {lm.ber:.2e}")

    # 5. Ground Station Network
    print("\n--- Ground Station Network ---")
    network = GroundStationNetwork()
    network.add_station("Kourou", 5.2, -52.7, 10.0)
    network.add_station("Svalbard", 78.2, 15.4, 500.0)
    network.add_station("Punchbowl", -34.0, 138.7, 50.0)
    network.schedule_pass("Kourou", "SAT-A", 0, 600, 45.0, 50000, 1.2, 8.5)
    network.schedule_pass("Svalbard", "SAT-A", 700, 1400, 35.0, 45000, 0.9, 7.2)
    network.schedule_pass("Kourou", "SAT-B", 200, 800, 40.0, 48000, 1.0, 8.0)

    status = network.get_status()
    print(f"Stations: {status.total_stations}, Active passes: {status.active_passes}")
    print(f"Utilization: {status.total_utilization_pct:.1f}%")

    handovers = network.detect_handovers("SAT-A")
    print(f"Handovers for SAT-A: {len(handovers)}")
    for h in handovers:
        print(f"  {h['from_station']} → {h['to_station']}: gap={h['gap_s']:.0f}s, seamless={h['seamless']}")

    # 6. Rain Fade
    print("\n--- Rain Fade Mitigation ---")
    rfm = RainFadeMitigator(frequency_ghz=8.15)
    rf_result = rfm.rain_attenuation(elevation_deg=45.0, rain_rate_mm_hr=25.0)
    print(f"Rain attenuation: {rf_result.total_attenuation_db:.2f} dB")
    print(f"Specific atten: {rf_result.specific_attenuation_db_km:.4f} dB/km")
    print(f"Diversity gain: {rf_result.diversity_gain_db:.2f} dB")

    acm = rfm.acm_thresholds()
    print(f"ACM thresholds: {len(acm)} levels")

    # 7. Polarization
    print("\n--- Polarization Analysis ---")
    pol = PolarizationAnalyzer(frequency_ghz=8.15, polarization=PolarizationType.CIRCULAR_RHCP)
    pol_result = pol.compute(tec=1e18, pointing_error_deg=0.05)
    print(f"Axial ratio: {pol_result.axial_ratio_db:.2f} dB")
    print(f"XPI: {pol_result.cross_polarization_isolation_db:.1f} dB")
    print(f"Faraday rotation: {pol_result.faraday_rotation_deg:.4f}°")

    # Serialization
    print("\n--- Serialization ---")
    d = chain.compute()
    print(f"Signal chain serialized: {len(d.components)} components")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
