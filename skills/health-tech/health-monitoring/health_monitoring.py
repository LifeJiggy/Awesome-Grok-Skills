"""
Health Monitoring - Wearable Data, Vital Signs, Anomaly Detection, Chronic Disease Management
Comprehensive module for continuous health monitoring and analytics.
"""

from __future__ import annotations

import hashlib
import json
import math
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class VitalType(Enum):
    """Types of vital sign measurements."""
    HEART_RATE = "heart_rate"
    HRV = "hrv"
    BLOOD_PRESSURE_SYSTOLIC = "bp_systolic"
    BLOOD_PRESSURE_DIASTOLIC = "bp_diastolic"
    OXYGEN_SATURATION = "spo2"
    BLOOD_GLUCOSE = "blood_glucose"
    BODY_TEMPERATURE = "body_temp"
    RESPIRATORY_RATE = "resp_rate"
    BODY_WEIGHT = "body_weight"
    STEPS = "steps"
    SLEEP_DURATION = "sleep_duration"
    SLEEP_DEEP = "sleep_deep"
    SLEEP_REM = "sleep_rem"
    CALORIES_BURNED = "calories"


class DeviceCategory(Enum):
    """Categories of health monitoring devices."""
    SMARTWATCH = "smartwatch"
    FITNESS_BAND = "fitness_band"
    CGM = "cgm"
    BLOOD_PRESSURE_MONITOR = "bp_monitor"
    SMART_SCALE = "smart_scale"
    PULSE_OXIMETER = "pulse_oximeter"
    SPIROMETER = "spirometer"
    ECG_MONITOR = "ecg_monitor"
    THERMOMETER = "thermometer"
    SMART_RING = "smart_ring"


class AnomalyType(Enum):
    """Classification of detected anomalies."""
    SPIKE = "spike"
    DROP = "drop"
    TREND_SHIFT = "trend_shift"
    ARRHYTHMIA = "arrhythmia"
    OUT_OF_RANGE = "out_of_range"
    MISSING_DATA = "missing_data"
    DEVICE_MALFUNCTION = "device_malfunction"


class AlertPriority(Enum):
    """Clinical alert priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class ChronicCondition(Enum):
    """Chronic conditions monitored via remote systems."""
    DIABETES_TYPE_1 = "diabetes_t1"
    DIABETES_TYPE_2 = "diabetes_t2"
    HEART_FAILURE = "heart_failure"
    HYPERTENSION = "hypertension"
    COPD = "copd"
    ASTHMA = "asthma"
    AFIB = "atrial_fibrillation"
    CHRONIC_KIDNEY_DISEASE = "ckd"


class TrendDirection(Enum):
    """Direction of a health metric trend."""
    RISING = "rising"
    FALLING = "falling"
    STABLE = "stable"
    VOLATILE = "volatile"


# ─── Dataclasses ──────────────────────────────────────────────────────────────

@dataclass
class VitalSignRange:
    """Normal range for a vital sign with alert thresholds."""
    vital_type: VitalType
    normal_min: float
    normal_max: float
    alert_low: float
    alert_high: float
    critical_low: float
    critical_high: float
    unit: str

    def classify(self, value: float) -> str:
        if value <= self.critical_low or value >= self.critical_high:
            return "critical"
        if value <= self.alert_low or value >= self.alert_high:
            return "alert"
        if value < self.normal_min or value > self.normal_max:
            return "borderline"
        return "normal"

    def deviation_score(self, value: float) -> float:
        """0.0 = normal, >1.0 = beyond alert threshold."""
        mid = (self.normal_min + self.normal_max) / 2
        half_range = (self.normal_max - self.normal_min) / 2
        if half_range == 0:
            return 0.0
        return abs(value - mid) / half_range


@dataclass
class VitalReading:
    """A single vital sign measurement."""
    reading_id: str
    patient_id: str
    vital_type: VitalType
    value: float
    timestamp: datetime
    device_id: str = ""
    device_category: DeviceCategory = DeviceCategory.SMARTWATCH
    context: str = ""
    quality_score: float = 1.0

    def is_valid(self) -> bool:
        return self.quality_score >= 0.5 and self.value >= 0


@dataclass
class DeviceInfo:
    """Registered health monitoring device."""
    device_id: str
    patient_id: str
    category: DeviceCategory
    manufacturer: str
    model: str
    firmware_version: str = ""
    last_sync: Optional[datetime] = None
    battery_level: float = 100.0
    is_active: bool = True

    def needs_sync(self, threshold_minutes: int = 60) -> bool:
        if not self.last_sync:
            return True
        elapsed = (datetime.utcnow() - self.last_sync).total_seconds() / 60
        return elapsed > threshold_minutes


@dataclass
class Anomaly:
    """A detected anomaly in health data."""
    anomaly_id: str
    patient_id: str
    vital_type: VitalType
    anomaly_type: AnomalyType
    reading_value: float
    expected_range: tuple[float, float]
    severity: AlertPriority
    detected_at: datetime = field(default_factory=datetime.utcnow)
    description: str = ""
    confirmed: bool = False

    def to_alert_dict(self) -> dict[str, Any]:
        return {
            "anomaly_id": self.anomaly_id,
            "vital_type": self.vital_type.value,
            "anomaly_type": self.anomaly_type.value,
            "severity": self.severity.value,
            "value": self.reading_value,
            "expected": f"{self.expected_range[0]}-{self.expected_range[1]}",
            "description": self.description,
            "timestamp": self.detected_at.isoformat(),
        }


@dataclass
class TrendAnalysis:
    """Result of trend analysis on a vital sign series."""
    vital_type: VitalType
    direction: TrendDirection
    slope: float
    r_squared: float
    mean: float
    std_dev: float
    min_value: float
    max_value: float
    sample_count: int
    period_start: datetime = field(default_factory=datetime.utcnow)
    period_end: datetime = field(default_factory=datetime.utcnow)

    def is_significant(self) -> bool:
        return self.r_squared > 0.5 and abs(self.slope) > 0.01


@dataclass
class ChronicDiseaseProtocol:
    """Monitoring protocol for a chronic condition."""
    condition: ChronicCondition
    patient_id: str
    target_vitals: list[VitalType] = field(default_factory=list)
    monitoring_frequency_hours: int = 24
    alert_thresholds: dict[str, float] = field(default_factory=dict)
    goals: dict[str, float] = field(default_factory=dict)
    clinician_id: str = ""
    enrolled_date: datetime = field(default_factory=datetime.utcnow)

    def get_checklist(self) -> list[dict[str, Any]]:
        checklist = []
        for vital in self.target_vitals:
            checklist.append({
                "vital": vital.value,
                "frequency": f"Every {self.monitoring_frequency_hours}h",
                "target": self.goals.get(vital.value, "N/A"),
            })
        return checklist


@dataclass
class PatientBaseline:
    """Patient-specific baseline for personalized monitoring."""
    patient_id: str
    vital_baselines: dict[VitalType, float] = field(default_factory=dict)
    vital_stds: dict[VitalType, float] = field(default_factory=dict)
    calculated_from: int = 0
    last_updated: datetime = field(default_factory=datetime.utcnow)

    def personalized_range(
        self, vital_type: VitalType, multiplier: float = 2.0
    ) -> Optional[tuple[float, float]]:
        base = self.vital_baselines.get(vital_type)
        std = self.vital_stds.get(vital_type)
        if base is None or std is None:
            return None
        return (base - multiplier * std, base + multiplier * std)


@dataclass
class DailySummary:
    """Summary of a patient's daily health data."""
    patient_id: str
    date: str
    total_readings: int = 0
    avg_heart_rate: float = 0.0
    avg_spo2: float = 0.0
    avg_glucose: float = 0.0
    steps: int = 0
    sleep_hours: float = 0.0
    anomalies_detected: int = 0
    alerts_triggered: int = 0


# ─── Vital Sign Ranges (Standard Adult) ──────────────────────────────────────

VITAL_RANGES: dict[VitalType, VitalSignRange] = {
    VitalType.HEART_RATE: VitalSignRange(
        VitalType.HEART_RATE, 60, 100, 50, 120, 40, 150, "bpm"
    ),
    VitalType.HRV: VitalSignRange(
        VitalType.HRV, 20, 100, 10, 150, 5, 200, "ms"
    ),
    VitalType.BLOOD_PRESSURE_SYSTOLIC: VitalSignRange(
        VitalType.BLOOD_PRESSURE_SYSTOLIC, 90, 120, 80, 160, 70, 180, "mmHg"
    ),
    VitalType.BLOOD_PRESSURE_DIASTOLIC: VitalSignRange(
        VitalType.BLOOD_PRESSURE_DIASTOLIC, 60, 80, 50, 100, 40, 110, "mmHg"
    ),
    VitalType.OXYGEN_SATURATION: VitalSignRange(
        VitalType.OXYGEN_SATURATION, 95, 100, 92, 100, 88, 100, "%"
    ),
    VitalType.BLOOD_GLUCOSE: VitalSignRange(
        VitalType.BLOOD_GLUCOSE, 70, 140, 54, 250, 40, 400, "mg/dL"
    ),
    VitalType.BODY_TEMPERATURE: VitalSignRange(
        VitalType.BODY_TEMPERATURE, 97.8, 99.1, 96.0, 100.4, 95.0, 101.3, "F"
    ),
    VitalType.RESPIRATORY_RATE: VitalSignRange(
        VitalType.RESPIRATORY_RATE, 12, 20, 8, 28, 6, 35, "/min"
    ),
    VitalType.BODY_WEIGHT: VitalSignRange(
        VitalType.BODY_WEIGHT, 100, 250, 80, 300, 60, 350, "lbs"
    ),
}


# ─── Core Services ────────────────────────────────────────────────────────────

class VitalSignMonitor:
    """Core vital sign tracking and validation engine."""

    def __init__(self) -> None:
        self._readings: dict[str, list[VitalReading]] = {}
        self._ranges = dict(VITAL_RANGES)

    def record_reading(self, reading: VitalReading) -> dict[str, Any]:
        """Record a vital sign reading and validate against normal ranges."""
        if not reading.is_valid():
            return {"status": "invalid", "reason": "Low quality or negative value"}

        if reading.patient_id not in self._readings:
            self._readings[reading.patient_id] = []
        self._readings[reading.patient_id].append(reading)

        vital_range = self._ranges.get(reading.vital_type)
        classification = vital_range.classify(reading.value) if vital_range else "unknown"
        deviation = vital_range.deviation_score(reading.value) if vital_range else 0.0

        return {
            "status": "recorded",
            "classification": classification,
            "deviation_score": round(deviation, 3),
            "range": f"{vital_range.normal_min}-{vital_range.normal_max}" if vital_range else "N/A",
            "unit": vital_range.unit if vital_range else "",
        }

    def get_readings(
        self,
        patient_id: str,
        vital_type: Optional[VitalType] = None,
        since: Optional[datetime] = None,
    ) -> list[VitalReading]:
        """Retrieve readings with optional filters."""
        readings = self._readings.get(patient_id, [])
        if vital_type:
            readings = [r for r in readings if r.vital_type == vital_type]
        if since:
            readings = [r for r in readings if r.timestamp >= since]
        return readings

    def get_latest(self, patient_id: str, vital_type: VitalType) -> Optional[VitalReading]:
        readings = [r for r in self._readings.get(patient_id, []) if r.vital_type == vital_type]
        return readings[-1] if readings else None

    def get_statistics(self, patient_id: str, vital_type: VitalType) -> dict[str, float]:
        readings = [r.value for r in self._readings.get(patient_id, []) if r.vital_type == vital_type]
        if not readings:
            return {}
        mean_val = sum(readings) / len(readings)
        variance = sum((x - mean_val) ** 2 for x in readings) / len(readings)
        return {
            "count": len(readings),
            "mean": round(mean_val, 2),
            "std_dev": round(math.sqrt(variance), 2),
            "min": min(readings),
            "max": max(readings),
        }


class AnomalyDetector:
    """Statistical anomaly detection for vital sign data."""

    def __init__(self, z_threshold: float = 3.0) -> None:
        self.z_threshold = z_threshold
        self._anomalies: dict[str, list[Anomaly]] = {}
        self._baselines: dict[str, PatientBaseline] = {}

    def set_baseline(self, patient_id: str, vital_type: VitalType, values: list[float]) -> None:
        """Calculate and set a patient baseline from historical data."""
        if len(values) < 2:
            return
        mean_val = sum(values) / len(values)
        std_val = math.sqrt(sum((x - mean_val) ** 2 for x in values) / len(values))

        if patient_id not in self._baselines:
            self._baselines[patient_id] = PatientBaseline(patient_id=patient_id)
        self._baselines[patient_id].vital_baselines[vital_type] = mean_val
        self._baselines[patient_id].vital_stds[vital_type] = std_val
        self._baselines[patient_id].calculated_from = len(values)

    def detect(self, reading: VitalReading) -> Optional[Anomaly]:
        """Check a single reading for anomalies against baseline."""
        baseline = self._baselines.get(reading.patient_id)
        if not baseline:
            return None

        base_val = baseline.vital_baselines.get(reading.vital_type)
        std_val = baseline.vital_stds.get(reading.vital_type)
        if base_val is None or std_val is None or std_val == 0:
            return None

        z_score = abs(reading.value - base_val) / std_val
        if z_score < self.z_threshold:
            return None

        vital_range = VITAL_RANGES.get(reading.vital_type)
        severity = AlertPriority.LOW
        if vital_range:
            cls = vital_range.classify(reading.value)
            if cls == "critical":
                severity = AlertPriority.CRITICAL
            elif cls == "alert":
                severity = AlertPriority.HIGH
            else:
                severity = AlertPriority.MEDIUM

        anomaly = Anomaly(
            anomaly_id=f"ANOM-{uuid.uuid4().hex[:8]}",
            patient_id=reading.patient_id,
            vital_type=reading.vital_type,
            anomaly_type=AnomalyType.SPIKE if reading.value > base_val else AnomalyType.DROP,
            reading_value=reading.value,
            expected_range=(base_val - self.z_threshold * std_val, base_val + self.z_threshold * std_val),
            severity=severity,
            description=f"Z-score={z_score:.2f}, value={reading.value}, baseline={base_val:.1f}±{std_val:.1f}",
        )

        self._anomalies.setdefault(reading.patient_id, []).append(anomaly)
        return anomaly

    def detect_batch(self, readings: list[VitalReading]) -> list[Anomaly]:
        """Detect anomalies across a batch of readings."""
        anomalies: list[Anomaly] = []
        for reading in readings:
            anomaly = self.detect(reading)
            if anomaly:
                anomalies.append(anomaly)
        return anomalies

    def get_anomalies(self, patient_id: str, since: Optional[datetime] = None) -> list[Anomaly]:
        anomalies = self._anomalies.get(patient_id, [])
        if since:
            anomalies = [a for a in anomalies if a.detected_at >= since]
        return anomalies


class TrendAnalyzer:
    """Analyzes trends in vital sign data over time."""

    def __init__(self, min_samples: int = 5) -> None:
        self.min_samples = min_samples

    def analyze(
        self, readings: list[VitalReading], vital_type: VitalType
    ) -> TrendAnalysis:
        """Perform linear regression trend analysis on a reading series."""
        filtered = [r for r in readings if r.vital_type == vital_type]
        if len(filtered) < self.min_samples:
            return TrendAnalysis(
                vital_type=vital_type,
                direction=TrendDirection.STABLE,
                slope=0.0, r_squared=0.0,
                mean=0.0, std_dev=0.0,
                min_value=0.0, max_value=0.0,
                sample_count=0,
            )

        values = [r.value for r in filtered]
        timestamps = [(r.timestamp - filtered[0].timestamp).total_seconds() for r in filtered]

        n = len(values)
        mean_x = sum(timestamps) / n
        mean_y = sum(values) / n

        ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(timestamps, values))
        ss_xx = sum((x - mean_x) ** 2 for x in timestamps)
        ss_yy = sum((y - mean_y) ** 2 for y in values)

        slope = ss_xy / ss_xx if ss_xx != 0 else 0.0
        r_squared = (ss_xy ** 2) / (ss_xx * ss_yy) if ss_xx > 0 and ss_yy > 0 else 0.0

        variance = sum((y - mean_y) ** 2 for y in values) / n

        if slope > 0.01 and r_squared > 0.5:
            direction = TrendDirection.RISING
        elif slope < -0.01 and r_squared > 0.5:
            direction = TrendDirection.FALLING
        elif math.sqrt(variance) > abs(mean_y) * 0.3:
            direction = TrendDirection.VOLATILE
        else:
            direction = TrendDirection.STABLE

        return TrendAnalysis(
            vital_type=vital_type,
            direction=direction,
            slope=round(slope, 6),
            r_squared=round(r_squared, 4),
            mean=round(mean_y, 2),
            std_dev=round(math.sqrt(variance), 2),
            min_value=min(values),
            max_value=max(values),
            sample_count=n,
            period_start=filtered[0].timestamp,
            period_end=filtered[-1].timestamp,
        )

    def detect_trend_shifts(
        self, readings: list[VitalReading], vital_type: VitalType, window_size: int = 10
    ) -> list[dict[str, Any]]:
        """Detect trend direction changes using sliding windows."""
        filtered = [r for r in readings if r.vital_type == vital_type]
        if len(filtered) < window_size * 2:
            return []

        shifts: list[dict[str, Any]] = []
        for i in range(window_size, len(filtered) - window_size):
            before = filtered[i - window_size:i]
            after = filtered[i:i + window_size]
            before_vals = [r.value for r in before]
            after_vals = [r.value for r in after]
            before_mean = sum(before_vals) / len(before_vals)
            after_mean = sum(after_vals) / len(after_vals)
            change_pct = ((after_mean - before_mean) / before_mean * 100) if before_mean != 0 else 0
            if abs(change_pct) > 15:
                shifts.append({
                    "timestamp": filtered[i].timestamp.isoformat(),
                    "change_percent": round(change_pct, 2),
                    "before_mean": round(before_mean, 2),
                    "after_mean": round(after_mean, 2),
                })
        return shifts


class ChronicDiseaseManager:
    """Manages monitoring protocols for chronic conditions."""

    PROTOCOL_TEMPLATES: dict[ChronicCondition, dict[str, Any]] = {
        ChronicCondition.DIABETES_TYPE_2: {
            "vitals": [VitalType.BLOOD_GLUCOSE, VitalType.BODY_WEIGHT, VitalType.BLOOD_PRESSURE_SYSTOLIC],
            "frequency_hours": 4,
            "goals": {
                "blood_glucose_fasting": 80,
                "blood_glucose_postprandial": 140,
                "hba1c": 7.0,
                "bp_systolic": 130,
            },
        },
        ChronicCondition.HEART_FAILURE: {
            "vitals": [VitalType.BODY_WEIGHT, VitalType.BLOOD_PRESSURE_SYSTOLIC, VitalType.HEART_RATE, VitalType.OXYGEN_SATURATION],
            "frequency_hours": 12,
            "goals": {
                "daily_weight_change_max": 2.0,
                "bp_systolic_target": 120,
                "hr_target": 70,
                "spo2_target": 95,
            },
        },
        ChronicCondition.HYPERTENSION: {
            "vitals": [VitalType.BLOOD_PRESSURE_SYSTOLIC, VitalType.BLOOD_PRESSURE_DIASTOLIC, VitalType.HEART_RATE],
            "frequency_hours": 12,
            "goals": {
                "bp_systolic": 130,
                "bp_diastolic": 80,
            },
        },
        ChronicCondition.COPD: {
            "vitals": [VitalType.OXYGEN_SATURATION, VitalType.RESPIRATORY_RATE, VitalType.HEART_RATE],
            "frequency_hours": 24,
            "goals": {
                "spo2_target": 92,
                "resp_rate_max": 20,
            },
        },
    }

    def __init__(self) -> None:
        self._protocols: dict[str, ChronicDiseaseProtocol] = {}

    def enroll_patient(
        self, patient_id: str, condition: ChronicCondition, clinician_id: str
    ) -> ChronicDiseaseProtocol:
        """Enroll a patient in a chronic disease monitoring protocol."""
        template = self.PROTOCOL_TEMPLATES.get(condition, {})
        protocol = ChronicDiseaseProtocol(
            condition=condition,
            patient_id=patient_id,
            target_vitals=template.get("vitals", []),
            monitoring_frequency_hours=template.get("frequency_hours", 24),
            goals=template.get("goals", {}),
            clinician_id=clinician_id,
        )
        key = f"{patient_id}-{condition.value}"
        self._protocols[key] = protocol
        return protocol

    def get_protocol(self, patient_id: str, condition: ChronicCondition) -> Optional[ChronicDiseaseProtocol]:
        return self._protocols.get(f"{patient_id}-{condition.value}")

    def evaluate_readings(
        self, patient_id: str, condition: ChronicCondition, readings: list[VitalReading]
    ) -> dict[str, Any]:
        """Evaluate readings against protocol goals."""
        protocol = self.get_protocol(patient_id, condition)
        if not protocol:
            return {"error": "Patient not enrolled"}

        results: list[dict[str, Any]] = []
        for reading in readings:
            if reading.vital_type in protocol.target_vitals:
                target = protocol.goals.get(reading.vital_type.value, None)
                in_range = True
                if target is not None:
                    in_range = abs(reading.value - target) / target < 0.2 if target != 0 else True
                results.append({
                    "vital": reading.vital_type.value,
                    "value": reading.value,
                    "target": target,
                    "in_range": in_range,
                })

        total = len(results)
        in_range_count = sum(1 for r in results if r["in_range"])
        return {
            "condition": condition.value,
            "total_measurements": total,
            "in_range": in_range_count,
            "compliance_rate": (in_range_count / total * 100) if total > 0 else 0,
            "details": results,
        }

    def get_active_protocols(self, patient_id: str) -> list[ChronicDiseaseProtocol]:
        return [p for k, p in self._protocols.items() if k.startswith(patient_id)]


class DailySummaryGenerator:
    """Generates daily health summaries from readings."""

    def __init__(self, monitor: VitalSignMonitor) -> None:
        self.monitor = monitor

    def generate(self, patient_id: str, date: str) -> DailySummary:
        """Generate a daily summary for a patient."""
        dt = datetime.fromisoformat(date)
        next_day = dt + timedelta(days=1)

        all_readings = self.monitor.get_readings(patient_id)
        day_readings = [r for r in all_readings if dt <= r.timestamp < next_day]

        hr_values = [r.value for r in day_readings if r.vital_type == VitalType.HEART_RATE]
        spo2_values = [r.value for r in day_readings if r.vital_type == VitalType.OXYGEN_SATURATION]
        glucose_values = [r.value for r in day_readings if r.vital_type == VitalType.BLOOD_GLUCOSE]
        steps_readings = [r.value for r in day_readings if r.vital_type == VitalType.STEPS]

        return DailySummary(
            patient_id=patient_id,
            date=date,
            total_readings=len(day_readings),
            avg_heart_rate=sum(hr_values) / len(hr_values) if hr_values else 0,
            avg_spo2=sum(spo2_values) / len(spo2_values) if spo2_values else 0,
            avg_glucose=sum(glucose_values) / len(glucose_values) if glucose_values else 0,
            steps=int(sum(steps_readings)),
        )


# ─── Demo ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate health monitoring capabilities."""
    print("=" * 70)
    print("HEALTH MONITORING DEMONSTRATION")
    print("=" * 70)

    # 1. Vital Sign Monitoring
    print("\n── 1. VITAL SIGN MONITORING ──")
    monitor = VitalSignMonitor()
    patient_id = "PAT-5001"
    now = datetime.utcnow()

    readings = [
        VitalReading("R-001", patient_id, VitalType.HEART_RATE, 78, now),
        VitalReading("R-002", patient_id, VitalType.HEART_RATE, 82, now + timedelta(minutes=5)),
        VitalReading("R-003", patient_id, VitalType.HEART_RATE, 85, now + timedelta(minutes=10)),
        VitalReading("R-004", patient_id, VitalType.OXYGEN_SATURATION, 97, now),
        VitalReading("R-005", patient_id, VitalType.BLOOD_GLUCOSE, 125, now),
        VitalReading("R-006", patient_id, VitalType.BLOOD_PRESSURE_SYSTOLIC, 135, now),
        VitalReading("R-007", patient_id, VitalType.BLOOD_PRESSURE_DIASTOLIC, 85, now),
    ]

    for reading in readings:
        result = monitor.record_reading(reading)
        print(f"  {reading.vital_type.value}={reading.value}: {result['classification']} (dev={result['deviation_score']})")

    stats = monitor.get_statistics(patient_id, VitalType.HEART_RATE)
    print(f"  HR Stats: {json.dumps(stats, indent=4)}")

    # 2. Anomaly Detection
    print("\n── 2. ANOMALY DETECTION ──")
    detector = AnomalyDetector(z_threshold=2.5)

    baseline_values = [78, 80, 75, 82, 77, 79, 81, 76, 80, 78, 79, 83, 77, 80]
    detector.set_baseline(patient_id, VitalType.HEART_RATE, baseline_values)
    print(f"  Baseline set from {len(baseline_values)} samples")

    test_readings = [
        VitalReading("T-001", patient_id, VitalType.HEART_RATE, 78, now),
        VitalReading("T-002", patient_id, VitalType.HEART_RATE, 145, now + timedelta(minutes=1)),
        VitalReading("T-003", patient_id, VitalType.HEART_RATE, 42, now + timedelta(minutes=2)),
        VitalReading("T-004", patient_id, VitalType.HEART_RATE, 81, now + timedelta(minutes=3)),
    ]

    for reading in test_readings:
        anomaly = detector.detect(reading)
        if anomaly:
            print(f"  ANOMALY: {anomaly.anomaly_type.value} | {anomaly.description}")
        else:
            print(f"  Normal: HR={reading.value}")

    all_anomalies = detector.get_anomalies(patient_id)
    print(f"  Total anomalies detected: {len(all_anomalies)}")

    # 3. Trend Analysis
    print("\n── 3. TREND ANALYSIS ──")
    trend_analyzer = TrendAnalyzer(min_samples=3)

    trend_readings = [
        VitalReading(f"TR-{i}", patient_id, VitalType.BLOOD_GLUCOSE,
                     100 + i * 5 + (i % 3) * 3, now + timedelta(hours=i))
        for i in range(12)
    ]

    trend = trend_analyzer.analyze(trend_readings, VitalType.BLOOD_GLUCOSE)
    print(f"  Glucose Trend: {trend.direction.value} (slope={trend.slope}, R²={trend.r_squared})")
    print(f"  Mean: {trend.mean}, StdDev: {trend.std_dev}, Range: {trend.min_value}-{trend.max_value}")

    shifts = trend_analyzer.detect_trend_shifts(trend_readings, VitalType.BLOOD_GLUCOSE, window_size=3)
    print(f"  Trend shifts detected: {len(shifts)}")

    # 4. Chronic Disease Management
    print("\n── 4. CHRONIC DISEASE MANAGEMENT ──")
    cdm = ChronicDiseaseManager()
    protocol = cdm.enroll_patient(patient_id, ChronicCondition.DIABETES_TYPE_2, "DR-CHEN")
    print(f"  Enrolled in: {protocol.condition.value}")
    print(f"  Monitoring frequency: Every {protocol.monitoring_frequency_hours}h")
    print(f"  Goals: {json.dumps(protocol.goals, indent=4)}")

    checklist = protocol.get_checklist()
    print(f"  Daily checklist:")
    for item in checklist:
        print(f"    - {item['vital']}: {item['frequency']} (target: {item['target']})")

    eval_readings = [
        VitalReading("E-001", patient_id, VitalType.BLOOD_GLUCOSE, 135, now),
        VitalReading("E-002", patient_id, VitalType.BLOOD_GLUCOSE, 165, now + timedelta(hours=4)),
        VitalReading("E-003", patient_id, VitalType.BLOOD_PRESSURE_SYSTOLIC, 128, now),
        VitalReading("E-004", patient_id, VitalType.BODY_WEIGHT, 185, now),
    ]
    evaluation = cdm.evaluate_readings(patient_id, ChronicCondition.DIABETES_TYPE_2, eval_readings)
    print(f"  Compliance rate: {evaluation.get('compliance_rate', 0):.1f}%")

    active = cdm.get_active_protocols(patient_id)
    print(f"  Active protocols: {[p.condition.value for p in active]}")

    # 5. Daily Summary
    print("\n── 5. DAILY SUMMARY ──")
    gen = DailySummaryGenerator(monitor)
    summary = gen.generate(patient_id, now.strftime("%Y-%m-%d"))
    print(f"  Date: {summary.date}")
    print(f"  Total readings: {summary.total_readings}")
    print(f"  Avg HR: {summary.avg_heart_rate:.1f} bpm")
    print(f"  Avg SpO2: {summary.avg_spo2:.1f}%")
    print(f"  Avg Glucose: {summary.avg_glucose:.1f} mg/dL")

    print("\n" + "=" * 70)
    print("HEALTH MONITORING DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
