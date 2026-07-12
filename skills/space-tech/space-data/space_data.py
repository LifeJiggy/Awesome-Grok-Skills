"""
Space Data Processing Module
Part of the space-tech skill domain

Comprehensive toolkit for space weather processing, Earth observation pipelines,
satellite telemetry analysis, space debris cataloguing, ephemeris processing,
remote sensing image analysis, satellite data compression, and space situational
awareness data fusion.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DataFormat(Enum):
    """Supported space data file formats."""
    TLE = "tle"
    CDF = "cdf"
    FITS = "fits"
    GEOTIFF = "geotiff"
    HDF5 = "hdf5"
    CCSDS_PACKET = "ccsds_packet"
    SPICE_SPK = "spk"
    SPICE_FK = "fk"
    RINEX = "rinex"
    JSON = "json"


class ProcessingStage(Enum):
    """Pipeline processing stages for Earth observation data."""
    INGEST = auto()
    RADIOMETRIC_CALIBRATION = auto()
    ATMOSPHERIC_CORRECTION = auto()
    GEOMETRIC_CORRECTION = auto()
    ORTHORECTIFICATION = auto()
    MOSAICKING = auto()
    CLASSIFICATION = auto()
    EXPORT = auto()


class WeatherSeverity(Enum):
    """Space weather storm severity scale (NOAA G-scale)."""
    G0_NONE = 0
    G1_MINOR = 1
    G2_MODERATE = 2
    G3_STRONG = 3
    G4_SEVERE = 4
    G5_EXTREME = 5


class DebrisOrbitRegime(Enum):
    """Orbital regime classification for space objects."""
    LEO = "low_earth_orbit"        # < 2000 km
    MEO = "medium_earth_orbit"     # 2000–35786 km
    GEO = "geostationary"          # ~35786 km
    HEO = "high_earth_orbit"       # elliptical > MEO
    CISLUNAR = "cislunar"          # beyond GEO
    DEEP_SPACE = "deep_space"      # heliocentric


class CompressionType(Enum):
    """On-board data compression algorithms."""
    NONE = "none"
    LOSSLESS_CCSDS_121 = "ccsds_121_bzip"
    LOSSLESS_CCSDS_123 = "ccsds_123_predictive"
    WAVELET = "wavelet"
    JPEG2000 = "jpeg2000"
    LZMA = "lzma"


class AnomalyDetectionMethod(Enum):
    """Statistical anomaly detection methods for telemetry."""
    CUSUM = "cusum"
    EWMA = "ewma"
    ZSCORE = "zscore"
    IQR = "iqr"
    ISOLATION_FOREST = "isolation_forest"


class CoordinateFrame(Enum):
    """Reference coordinate frames for ephemeris processing."""
    ECI = "earth_centered_inertial"
    ECEF = "earth_centered_earth_fixed"
    LVLH = "local_vertical_local_horizontal"
    SEZ = "south_east_zenith"
    GEOCENTRIC = "geocentric"


class SensorType(Enum):
    """Types of SSA tracking sensors."""
    RADAR = "radar"
    OPTICAL = "optical"
    RF_PASSIVE = "rf_passive"
    LIDAR = "lidar"
    IR = "infrared"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class SpaceWeatherData:
    """Real-time or archival space weather measurement."""
    timestamp: datetime
    solar_wind_speed_kms: float
    solar_wind_density_pcc: float
    imf_bt_nt: float
    imf_bz_nt: float
    proton_flux_gev: float
    electron_flux_mev: float
    kp_index: float
    dst_index_nt: float
    f107_flux_sfu: float
    ap_index: Optional[float] = None

    @property
    def is_storm(self) -> bool:
        return self.kp_index >= 5.0 or self.dst_index_nt <= -50.0

    @property
    def bz_southward(self) -> bool:
        return self.imf_bz_nt < 0.0


@dataclass
class StormClassification:
    """Result of space weather storm classification."""
    severity: WeatherSeverity
    estimated_dst_nt: float
    radiation_dose_rate_mrad_hr: float
    mission_impact_level: str
    onset_time: Optional[datetime] = None
    recovery_time_hours: Optional[float] = None
    recommendations: List[str] = field(default_factory=list)


@dataclass
class SolarWindData:
    """Abbreviated solar wind measurement for quick processing."""
    speed_kms: float
    density_pcc: float
    imf_bt_nt: float
    imf_bz_nt: float
    temperature_k: float


@dataclass
class EOImageMetadata:
    """Metadata for an Earth observation image product."""
    scene_id: str
    sensor_name: str
    acquisition_time: datetime
    center_lat_deg: float
    center_lon_deg: float
    cloud_cover_pct: float
    sun_elevation_deg: float
    bands: int
    resolution_m: float
    swath_width_km: float
    processing_level: str = "L1B"


@dataclass
class EOProcessingResult:
    """Output from an Earth observation pipeline run."""
    output_path: str
    output_format: str
    cloud_cover_pct: float
    processing_time_s: float
    bands_processed: int
    pixel_count: int
    statistics: Dict[str, float] = field(default_factory=dict)


@dataclass
class SensorConfig:
    """Configuration for an Earth observation sensor model."""
    sensor_type: str
    bands: int
    resolution_m: float
    snr_db: float
    swath_width_km: float
    bit_depth: int = 12
    quantum_efficiency: float = 0.85


@dataclass
class DebrisObject:
    """A tracked space debris object."""
    catalog_number: int
    name: str
    epoch: datetime
    sma_km: float
    eccentricity: float
    inclination_deg: float
    raan_deg: float
    arg_perigee_deg: float
    mean_anomaly_deg: float
    ballistic_coefficient: Optional[float] = None
    cross_section_m2: Optional[float] = None
    mass_kg: Optional[float] = None

    @property
    def orbital_regime(self) -> DebrisOrbitRegime:
        if self.sma_km < 2000.0:
            return DebrisOrbitRegime.LEO
        elif self.sma_km < 35786.0:
            return DebrisOrbitRegime.MEO
        elif self.sma_km < 42164.0:
            return DebrisOrbitRegime.GEO
        else:
            return DebrisOrbitRegime.DEEP_SPACE

    @property
    def orbital_period_minutes(self) -> float:
        mu = 398600.4418  # km^3/s^2
        return 2.0 * math.pi * math.sqrt(self.sma_km ** 3 / mu) / 60.0

    @property
    def perigee_km(self) -> float:
        return self.sma_km * (1.0 - self.eccentricity)

    @property
    def apogee_km(self) -> float:
        return self.sma_km * (1.0 + self.eccentricity)


@dataclass
class ConjunctionEvent:
    """A predicted close approach between two space objects."""
    primary_catalog_number: int
    secondary_catalog_number: int
    time: datetime
    miss_distance_km: float
    probability_of_collision: float
    relative_velocity_kms: float
    miss_distance_sigma: float = 0.0


@dataclass
class TLE:
    """Two-Line Element set."""
    line1: str
    line2: str
    catalog_number: int = 0
    name: str = ""

    def __post_init__(self):
        if not self.catalog_number and len(self.line1) >= 7:
            try:
                self.catalog_number = int(self.line1[2:7].strip())
            except ValueError:
                self.catalog_number = 0


@dataclass
class TelemetryParameter:
    """A single telemetry parameter reading."""
    name: str
    value: float
    unit: str = ""
    limits: Tuple[float, float] = (-float("inf"), float("inf"))
    timestamp: Optional[datetime] = None

    @property
    def is_out_of_limits(self) -> bool:
        return self.value < self.limits[0] or self.value > self.limits[1]

    @property
    def limit_margin_pct(self) -> float:
        span = self.limits[1] - self.limits[0]
        if span <= 0:
            return 0.0
        center = (self.limits[0] + self.limits[1]) / 2.0
        return (1.0 - abs(self.value - center) / (span / 2.0)) * 100.0


@dataclass
class AnomalyEvent:
    """Detected anomaly in telemetry data."""
    parameter_name: str
    value: float
    unit: str
    deviation_sigma: float
    detection_method: AnomalyDetectionMethod
    timestamp: Optional[datetime] = None
    severity: str = "warning"


@dataclass
class EphemerisState:
    """A position-velocity state at a given epoch."""
    epoch: datetime
    position_eci_m: Tuple[float, float, float]
    velocity_eci_mps: Tuple[float, float, float]
    frame: CoordinateFrame = CoordinateFrame.ECI

    @property
    def radius_m(self) -> float:
        return math.sqrt(sum(c ** 2 for c in self.position_eci_m))

    @property
    def speed_mps(self) -> float:
        return math.sqrt(sum(c ** 2 for c in self.velocity_eci_mps))


@dataclass
class SSATrackAssociation:
    """Result of associating an observation with a cataloged object."""
    sensor_id: str
    sensor_type: SensorType
    catalog_number: int
    observation_time: datetime
    mahalanobis_distance: float
    innovation_vector: Tuple[float, float, float]
    is_associated: bool


@dataclass
class CompressionResult:
    """Result of on-board data compression modeling."""
    algorithm: CompressionType
    original_size_bytes: int
    compressed_size_bytes: int
    compression_ratio: float
    compression_time_ms: float
    data_type: str = "unknown"

    @property
    def space_saving_pct(self) -> float:
        if self.original_size_bytes == 0:
            return 0.0
        return (1.0 - self.compressed_size_bytes / self.original_size_bytes) * 100.0


@dataclass
class SpaceWeatherConfig:
    """Configuration for the space weather processor."""
    noaa_swpc_base_url: str = "https://services.swpc.noaa.gov"
    kp_threshold_storm: float = 5.0
    dst_threshold_storm: float = -50.0
    radiation_dose_limit_mrad_hr: float = 10.0
    data_quality_flags: List[str] = field(default_factory=lambda: ["valid", "interpolated", "estimated"])
    default_data_quality: str = "valid"


@dataclass
class DebrisCatalogConfig:
    """Configuration for the debris catalog subsystem."""
    tle_source: str = "celestrak"
    propagation_model: str = "sgp4"
    conjunction_screening_distance_km: float = 10.0
    probability_of_collision_threshold: float = 1e-4
    max_propagation_days: float = 7.0
    drag_coefficient: float = 2.2
    reference_area_m2: float = 1.0


# ---------------------------------------------------------------------------
# Space Weather Processor
# ---------------------------------------------------------------------------

class SpaceWeatherProcessor:
    """Processes space weather data from NOAA SWPC and other sources."""

    def __init__(self, config: Optional[SpaceWeatherConfig] = None):
        self.config = config or SpaceWeatherConfig()
        self._history: List[SpaceWeatherData] = []
        self._storm_history: List[StormClassification] = []

    def ingest(self, data: SpaceWeatherData) -> None:
        self._history.append(data)

    def classify_storm(
        self, solar_wind: SolarWindData, kp_index: float
    ) -> StormClassification:
        if kp_index < 4.0:
            severity = WeatherSeverity.G0_NONE
        elif kp_index < 5.0:
            severity = WeatherSeverity.G1_MINOR
        elif kp_index < 6.0:
            severity = WeatherSeverity.G2_MODERATE
        elif kp_index < 7.0:
            severity = WeatherSeverity.G3_STRONG
        elif kp_index < 8.0:
            severity = WeatherSeverity.G4_SEVERE
        else:
            severity = WeatherSeverity.G5_EXTREME

        estimated_dst = -10.0 * (solar_wind.speed_kms / 100.0) ** 2
        if solar_wind.imf_bz_nt < 0.0:
            estimated_dst *= 1.5
        dose_rate = 0.5 + 0.02 * kp_index + 0.001 * solar_wind.proton_flux_gev

        impact = "nominal"
        if severity.value >= 3:
            impact = "significant"
        elif severity.value >= 1:
            impact = "minor"

        result = StormClassification(
            severity=severity,
            estimated_dst_nt=estimated_dst,
            radiation_dose_rate_mrad_hr=dose_rate,
            mission_impact_level=impact,
            recommendations=self._storm_recommendations(severity),
        )
        self._storm_history.append(result)
        return result

    def _storm_recommendations(self, severity: WeatherSeverity) -> List[str]:
        recs: List[str] = []
        if severity.value >= 1:
            recs.append("Increase telemetry monitoring frequency")
        if severity.value >= 2:
            recs.append("Suspend non-essential payload operations")
        if severity.value >= 3:
            recs.append("Enter safe-hold mode for sensitive instruments")
        if severity.value >= 4:
            recs.append("Activate radiation-hardened backup systems")
        if severity.value >= 5:
            recs.append("Full spacecraft safe-mode recommended")
        return recs

    def estimate_radiation_dose(
        self, energy_mev: float, shielding_mm_al: float, duration_hours: float
    ) -> float:
        flux = 1e6 * math.exp(-energy_mev / 10.0)
        dose = flux * 1e-9 * (1.0 / (1.0 + shielding_mm_al / 10.0)) * duration_hours
        return dose

    def kp_to_ap(self, kp: float) -> float:
        ap_table = {0: 0, 1: 4, 2: 7, 3: 15, 4: 27, 5: 48,
                     6: 80, 7: 132, 8: 187, 9: 253}
        idx = min(int(kp), 9)
        return float(ap_table.get(idx, 0))


# ---------------------------------------------------------------------------
# Earth Observation Pipeline
# ---------------------------------------------------------------------------

class EOPipeline:
    """Earth observation data processing pipeline."""

    def __init__(self, sensor: SensorConfig):
        self.sensor = sensor
        self._stage_times: Dict[str, float] = {}

    def process(
        self,
        raw_data_path: str,
        output_format: str = "GeoTIFF",
        atmospheric_correction: bool = True,
        orthorectify: bool = True,
    ) -> EOProcessingResult:
        start = datetime.now()

        stages = [
            ProcessingStage.INGEST,
            ProcessingStage.RADIOMETRIC_CALIBRATION,
        ]
        if atmospheric_correction:
            stages.append(ProcessingStage.ATMOSPHERIC_CORRECTION)
        if orthorectify:
            stages.extend([
                ProcessingStage.GEOMETRIC_CORRECTION,
                ProcessingStage.ORTHORECTIFICATION,
            ])
        stages.append(ProcessingStage.EXPORT)

        pixel_count = 0
        cloud_cover = 0.0
        for stage in stages:
            stage_result = self._execute_stage(stage, raw_data_path)
            pixel_count = stage_result.get("pixels", pixel_count)
            cloud_cover = stage_result.get("cloud_cover", cloud_cover)

        elapsed = (datetime.now() - start).total_seconds()
        output = raw_data_path.replace(".raw", f".{output_format.lower()}")

        return EOProcessingResult(
            output_path=output,
            output_format=output_format,
            cloud_cover_pct=cloud_cover,
            processing_time_s=elapsed,
            bands_processed=self.sensor.bands,
            pixel_count=pixel_count,
        )

    def _execute_stage(self, stage: ProcessingStage, path: str) -> Dict[str, Any]:
        if stage == ProcessingStage.INGEST:
            return {"pixels": 1024 * 1024, "cloud_cover": 12.5}
        elif stage == ProcessingStage.ATMOSPHERIC_CORRECTION:
            return {"reflectance_offset": 0.02}
        return {}

    def compute_ndvi(self, red_band: List[float], nir_band: List[float]) -> List[float]:
        ndvi_values: List[float] = []
        for r, n in zip(red_band, nir_band):
            denom = r + n
            if denom == 0:
                ndvi_values.append(0.0)
            else:
                ndvi_values.append((n - r) / denom)
        return ndvi_values


# ---------------------------------------------------------------------------
# Debris Catalog
# ---------------------------------------------------------------------------

class DebrisCatalog:
    """Space debris catalog processing and conjunction screening."""

    def __init__(self, config: Optional[DebrisCatalogConfig] = None):
        self.config = config or DebrisCatalogConfig()
        self._objects: List[DebrisObject] = []
        self._conjunctions: List[ConjunctionEvent] = []

    def load_tle_file(self, filepath: str) -> int:
        count = 0
        try:
            with open(filepath, "r") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
            i = 0
            while i < len(lines) - 1:
                if lines[i].startswith("1 ") and lines[i + 1].startswith("2 "):
                    tle = TLE(line1=lines[i], line2=lines[i + 1])
                    obj = self._parse_tle_to_object(tle)
                    if obj:
                        self._objects.append(obj)
                        count += 1
                    i += 2
                else:
                    i += 1
        except FileNotFoundError:
            pass
        return count

    def add_object(self, obj: DebrisObject) -> None:
        self._objects.append(obj)

    def _parse_tle_to_object(self, tle: TLE) -> Optional[DebrisObject]:
        try:
            epoch_year = int(tle.line1[18:20])
            epoch_day = float(tle.line1[20:32])
            year = 2000 + epoch_year if epoch_year < 57 else 1900 + epoch_year
            epoch = datetime(year, 1, 1) + timedelta(days=epoch_day - 1)

            sma = float(tle.line2[52:63]) / 10.0
            ecc_str = "0." + tle.line2[26:33]
            ecc = float(ecc_str)
            inc = float(tle.line2[8:16])
            raan = float(tle.line2[17:25])
            argp = float(tle.line2[34:42])
            ma = float(tle.line2[43:51])

            return DebrisObject(
                catalog_number=tle.catalog_number,
                name=tle.name,
                epoch=epoch,
                sma_km=sma,
                eccentricity=ecc,
                inclination_deg=inc,
                raan_deg=raan,
                arg_perigee_deg=argp,
                mean_anomaly_deg=ma,
            )
        except (ValueError, IndexError):
            return None

    def screen_conjunctions(
        self,
        target_sma: float,
        target_inc_deg: float,
        time_window_days: float = 7.0,
        distance_threshold_km: float = 10.0,
    ) -> List[ConjunctionEvent]:
        results: List[ConjunctionEvent] = []
        for obj in self._objects:
            sma_diff = abs(obj.sma_km - target_sma)
            inc_diff = abs(obj.inclination_deg - target_inc_deg)
            if sma_diff < distance_threshold_km * 2 and inc_diff < 5.0:
                miss = sma_diff * math.sin(math.radians(inc_diff))
                if miss < distance_threshold_km:
                    poc = self._estimate_poc(miss, obj)
                    event = ConjunctionEvent(
                        primary_catalog_number=0,
                        secondary_catalog_number=obj.catalog_number,
                        time=datetime.now(),
                        miss_distance_km=miss,
                        probability_of_collision=poc,
                        relative_velocity_kms=10.0,
                    )
                    results.append(event)
        results.sort(key=lambda c: c.probability_of_collision, reverse=True)
        self._conjunctions.extend(results)
        return results

    def _estimate_poc(self, miss_km: float, obj: DebrisObject) -> float:
        sigma = 0.5  # km combined position uncertainty
        area = obj.cross_section_m2 or 10.0
        r_eff = math.sqrt(area / math.pi) / 1000.0
        return math.exp(-0.5 * (miss_km / sigma) ** 2) * (r_eff / sigma) ** 2

    @property
    def object_count(self) -> int:
        return len(self._objects)

    @property
    def conjunction_count(self) -> int:
        return len(self._conjunctions)


# ---------------------------------------------------------------------------
# Telemetry Analyzer
# ---------------------------------------------------------------------------

class TelemetryAnalyzer:
    """Satellite telemetry analysis and anomaly detection."""

    def __init__(self):
        self._history: Dict[str, List[float]] = {}
        self._anomalies: List[AnomalyEvent] = []

    def ingest(self, params: List[TelemetryParameter]) -> None:
        for p in params:
            self._history.setdefault(p.name, []).append(p.value)

    def detect_anomalies(
        self,
        params: List[TelemetryParameter],
        method: str = "cusum",
        threshold_sigma: float = 3.0,
    ) -> List[AnomalyEvent]:
        method_enum = AnomalyDetectionMethod(method)
        results: List[AnomalyEvent] = []
        for p in params:
            hist = self._history.get(p.name, [])
            if len(hist) < 5:
                continue

            if method_enum == AnomalyDetectionMethod.ZSCORE:
                dev = self._zscore_deviation(hist, p.value)
            elif method_enum == AnomalyDetectionMethod.IQR:
                dev = self._iqr_deviation(hist, p.value)
            else:
                dev = self._cusum_deviation(hist, p.value)

            if abs(dev) > threshold_sigma:
                event = AnomalyEvent(
                    parameter_name=p.name,
                    value=p.value,
                    unit=p.unit,
                    deviation_sigma=abs(dev),
                    detection_method=method_enum,
                    timestamp=p.timestamp or datetime.now(),
                    severity="critical" if abs(dev) > 5.0 else "warning",
                )
                results.append(event)
                self._anomalies.append(event)
        return results

    def _zscore_deviation(self, history: List[float], value: float) -> float:
        mean = sum(history) / len(history)
        var = sum((x - mean) ** 2 for x in history) / len(history)
        std = math.sqrt(var) if var > 0 else 1.0
        return (value - mean) / std

    def _iqr_deviation(self, history: List[float], value: float) -> float:
        sorted_h = sorted(history)
        n = len(sorted_h)
        q1 = sorted_h[n // 4]
        q3 = sorted_h[3 * n // 4]
        iqr = q3 - q1
        if iqr == 0:
            return 0.0
        median = sorted_h[n // 2]
        return (value - median) / (iqr * 0.7413)

    def _cusum_deviation(self, history: List[float], value: float) -> float:
        mean = sum(history) / len(history)
        threshold = 4.0
        cusum_pos = 0.0
        cusum_neg = 0.0
        for v in history[-20:]:
            cusum_pos = max(0, cusum_pos + (v - mean) - threshold / 2)
            cusum_neg = max(0, cusum_neg - (v - mean) - threshold / 2)
        delta = value - mean
        return delta / (math.sqrt(sum((x - mean) ** 2 for x in history) / len(history)) + 1e-10)

    def compute_trend(self, param_name: str) -> Optional[float]:
        hist = self._history.get(param_name, [])
        if len(hist) < 2:
            return None
        n = len(hist)
        x_mean = (n - 1) / 2.0
        y_mean = sum(hist) / n
        num = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(hist))
        den = sum((i - x_mean) ** 2 for i in range(n))
        return num / den if den > 0 else 0.0


# ---------------------------------------------------------------------------
# Ephemeris Processor
# ---------------------------------------------------------------------------

class EphemerisProcessor:
    """Ephemeris data processing and coordinate frame transformations."""

    MU_EARTH_M3_S2 = 398600.4418  # km^3/s^2
    R_EARTH_M = 6371000.0

    def __init__(self):
        self._states: List[EphemerisState] = []

    def add_state(self, state: EphemerisState) -> None:
        self._states.append(state)

    def interpolate(self, target_time: datetime) -> Optional[EphemerisState]:
        if len(self._states) < 2:
            return self._states[0] if self._states else None
        for i in range(len(self._states) - 1):
            t0 = self._states[i].epoch
            t1 = self._states[i + 1].epoch
            if t0 <= target_time <= t1:
                frac = (target_time - t0).total_seconds() / max((t1 - t0).total_seconds(), 1e-10)
                s0, s1 = self._states[i], self._states[i + 1]
                pos = tuple(s0.position_eci_m[j] + frac * (s1.position_eci_m[j] - s0.position_eci_m[j]) for j in range(3))
                vel = tuple(s0.velocity_eci_mps[j] + frac * (s1.velocity_eci_mps[j] - s0.velocity_eci_mps[j]) for j in range(3))
                return EphemerisState(epoch=target_time, position_eci_m=pos, velocity_eci_mps=vel)
        return None

    def propagate_keplerian(
        self,
        state: EphemerisState,
        delta_s: float,
    ) -> EphemerisState:
        r = list(state.position_eci_m)
        v = list(state.velocity_eci_mps)
        r_mag = math.sqrt(sum(c ** 2 for c in r))
        v_mag = math.sqrt(sum(c ** 2 for c in v))
        mu = self.MU_EARTH_M3_S2 / 1e9  # m^3/s^2

        steps = max(int(abs(delta_s) / 60.0), 1)
        dt = delta_s / steps
        for _ in range(steps):
            a_mag = mu / r_mag ** 2
            r_unit = [r[j] / r_mag for j in range(3)]
            acc = [-a_mag * r_unit[j] for j in range(3)]
            for j in range(3):
                v[j] += acc[j] * dt
                r[j] += v[j] * dt
            r_mag = math.sqrt(sum(c ** 2 for j, c in enumerate(r)))
        return EphemerisState(
            epoch=state.epoch + timedelta(seconds=delta_s),
            position_eci_m=tuple(r),
            velocity_eci_mps=tuple(v),
        )

    def eci_to_ecef(self, state: EphemerisState, gmst_rad: float) -> Tuple[float, float, float]:
        x, y, z = state.position_eci_m
        cos_g = math.cos(gmst_rad)
        sin_g = math.sin(gmst_rad)
        x_ecef = cos_g * x + sin_g * y
        y_ecef = -sin_g * x + cos_g * y
        return (x_ecef, y_ecef, z)

    def eci_to_sez(self, state: EphemerisState, lat_rad: float, lon_rad: float) -> Tuple[float, float, float]:
        gmst = lon_rad
        ecef = self.eci_to_ecef(state, gmst)
        cos_lat = math.cos(lat_rad)
        sin_lat = math.sin(lat_rad)
        x, y, z = ecef
        south = -sin_lat * x + cos_lat * z
        east = y
        zenith = cos_lat * x + sin_lat * z
        return (south, east, zenith)

    @property
    def state_count(self) -> int:
        return len(self._states)


# ---------------------------------------------------------------------------
# SSA Data Fusion Engine
# ---------------------------------------------------------------------------

class SSADataFusion:
    """Multi-sensor space situational awareness data fusion."""

    MAHALANOBIS_THRESHOLD = 3.0

    def __init__(self):
        self._catalog: Dict[int, EphemerisState] = {}
        self._sensor_biases: Dict[str, Tuple[float, float, float]] = {}
        self._associations: List[SSATrackAssociation] = []

    def register_sensor_bias(self, sensor_id: str, bias_rad: Tuple[float, float, float]) -> None:
        self._sensor_biases[sensor_id] = bias_rad

    def associate_observation(
        self,
        sensor_id: str,
        sensor_type: SensorType,
        observation_time: datetime,
        measured_position: Tuple[float, float, float],
        measurement_covariance: Tuple[float, float, float],
    ) -> Optional[SSATrackAssociation]:
        best_dist = float("inf")
        best_cat_num = -1
        best_innovation = (0.0, 0.0, 0.0)

        bias = self._sensor_biases.get(sensor_id, (0.0, 0.0, 0.0))
        corrected = tuple(measured_position[j] - bias[j] for j in range(3))

        for cat_num, ref_state in self._catalog.items():
            if abs((observation_time - ref_state.epoch).total_seconds()) > 300:
                continue
            innovation = tuple(corrected[j] - ref_state.position_eci_m[j] for j in range(3))
            inn_sq = sum(innovation[j] ** 2 / max(measurement_covariance[j] ** 2, 1.0) for j in range(3))
            dist = math.sqrt(inn_sq)
            if dist < best_dist:
                best_dist = dist
                best_cat_num = cat_num
                best_innovation = innovation

        is_associated = best_dist < self.MAHALANOBIS_THRESHOLD
        assoc = SSATrackAssociation(
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            catalog_number=best_cat_num if is_associated else -1,
            observation_time=observation_time,
            mahalanobis_distance=best_dist,
            innovation_vector=best_innovation,
            is_associated=is_associated,
        )
        self._associations.append(assoc)
        return assoc

    def update_catalog(self, cat_num: int, state: EphemerisState) -> None:
        existing = self._catalog.get(cat_num)
        if existing is None or state.epoch >= existing.epoch:
            self._catalog[cat_num] = state

    def catalog_size(self) -> int:
        return len(self._catalog)

    def association_rate(self) -> float:
        if not self._associations:
            return 0.0
        return sum(1 for a in self._associations if a.is_associated) / len(self._associations)


# ---------------------------------------------------------------------------
# Compression Modeler
# ---------------------------------------------------------------------------

class CompressionModeler:
    """Models on-board data compression for spacecraft data."""

    def estimate_ratio(
        self,
        data_type: str,
        algorithm: CompressionType,
        data_size_bytes: int,
    ) -> CompressionResult:
        ratio_map: Dict[str, Dict[CompressionType, float]] = {
            "imagery": {
                CompressionType.NONE: 1.0,
                CompressionType.WAVELET: 0.25,
                CompressionType.JPEG2000: 0.20,
                CompressionType.LZMA: 0.45,
                CompressionType.LOSSLESS_CCSDS_123: 0.55,
            },
            "telemetry": {
                CompressionType.NONE: 1.0,
                CompressionType.LOSSLESS_CCSDS_121: 0.60,
                CompressionType.LOSSLESS_CCSDS_123: 0.50,
                CompressionType.LZMA: 0.40,
            },
            "science": {
                CompressionType.NONE: 1.0,
                CompressionType.WAVELET: 0.30,
                CompressionType.LOSSLESS_CCSDS_123: 0.50,
                CompressionType.JPEG2000: 0.22,
            },
        }
        rates = ratio_map.get(data_type, ratio_map["telemetry"])
        ratio = rates.get(algorithm, 0.5)
        compressed = int(data_size_bytes * ratio)
        time_ms = data_size_bytes / (500 * 1024) * 1000
        return CompressionResult(
            algorithm=algorithm,
            original_size_bytes=data_size_bytes,
            compressed_size_bytes=compressed,
            compression_ratio=1.0 / ratio if ratio > 0 else 0.0,
            compression_time_ms=time_ms,
            data_type=data_type,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("Space Data Processing Module — Demo")
    print("=" * 60)

    # Space weather
    swp = SpaceWeatherProcessor()
    sw = SolarWindData(speed_kms=550.0, density_pcc=8.0, imf_bt_nt=12.0, imf_bz_nt=-15.0, temperature_k=200000.0)
    storm = swp.classify_storm(sw, kp_index=7.0)
    print(f"\n[Space Weather] Storm: {storm.severity.name}, Dst est: {storm.estimated_dst_nt:.0f} nT")
    print(f"  Impact: {storm.mission_impact_level}")
    for rec in storm.recommendations:
        print(f"  - {rec}")

    # Earth observation
    sensor = SensorConfig(sensor_type="optical", bands=4, resolution_m=10.0, snr_db=45.0, swath_width_km=290.0)
    pipeline = EOPipeline(sensor)
    result = pipeline.process("/data/scene_001.raw")
    print(f"\n[EO Pipeline] Output: {result.output_path}, pixels: {result.pixel_count:,}")

    # Debris catalog
    catalog = DebrisCatalog()
    obj = DebrisObject(
        catalog_number=99999, name="DEBRIS-TEST", epoch=datetime.now(),
        sma_km=6871.0, eccentricity=0.001, inclination_deg=97.4,
        raan_deg=45.0, arg_perigee_deg=0.0, mean_anomaly_deg=120.0,
        cross_section_m2=10.0,
    )
    catalog.add_object(obj)
    print(f"\n[Debris] Objects: {catalog.object_count}, Regime: {obj.orbital_regime.value}")

    # Telemetry
    analyzer = TelemetryAnalyzer()
    params = [
        TelemetryParameter("battery_voltage", 27.5, "V", (26.0, 30.0)),
        TelemetryParameter("cpu_temp", 55.0, "C", (-10.0, 60.0)),
    ]
    anomalies = analyzer.detect_anomalies(params)
    print(f"\n[Telemetry] Anomalies: {len(anomalies)}")
    for a in anomalies:
        print(f"  {a.parameter_name}: {a.value} ({a.deviation_sigma:.1f}σ)")

    # Ephemeris
    eph = EphemerisProcessor()
    state = EphemerisState(
        epoch=datetime.now(), position_eci_m=(6871000.0, 0.0, 0.0),
        velocity_eci_mps=(0.0, 7500.0, 0.0),
    )
    propagated = eph.propagate_keplerian(state, 3600.0)
    print(f"\n[Ephemeris] Propagated radius: {propagated.radius_m / 1000:.1f} km")

    # SSA Fusion
    ssa = SSADataFusion()
    ssa.update_catalog(1, state)
    obs = ssa.associate_observation("SENSOR-1", SensorType.RADAR, datetime.now(), (6871500.0, 100.0, 50.0), (100.0, 100.0, 100.0))
    print(f"\n[SSA] Catalog: {ssa.catalog_size()}, Associated: {obs.is_associated if obs else 'N/A'}")

    # Compression
    comp = CompressionModeler()
    res = comp.estimate_ratio("imagery", CompressionType.JPEG2000, 10 * 1024 * 1024)
    print(f"\n[Compression] Ratio: {res.compression_ratio:.1f}:1, Saving: {res.space_saving_pct:.0f}%")

    print("\n" + "=" * 60)
    print("Demo complete.")


if __name__ == "__main__":
    main()
