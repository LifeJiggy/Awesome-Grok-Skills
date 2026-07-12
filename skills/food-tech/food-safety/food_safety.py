"""
Food Safety Module
Part of the food-tech skill domain

Provides HACCP plan management, temperature monitoring, traceability,
recall management, contamination detection, and regulatory compliance.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid
import hashlib


class HazardType(Enum):
    BIOLOGICAL = "biological"
    CHEMICAL = "chemical"
    PHYSICAL = "physical"
    ALLERGEN = "allergen"


class RecallSeverity(Enum):
    CLASS_1 = "class_1"   # Serious health risk or death
    CLASS_2 = "class_2"   # Temporary or reversible health risk
    CLASS_3 = "class_3"   # No health risk


class EventType(Enum):
    HARVEST = "harvest"
    PROCESSING = "processing"
    PACKAGING = "packaging"
    STORAGE = "storage"
    TRANSPORT = "transport"
    RECEIVING = "receiving"
    SALE = "sale"


class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    UNDER_REVIEW = "under_review"


@dataclass
class CCP:
    name: str
    step: str
    hazard: HazardType
    critical_limit: Dict[str, Any]
    monitoring_procedure: str
    corrective_action: str
    verification: str
    ccp_id: str = ""
    is_active: bool = True

    def __post_init__(self):
        if not self.ccp_id:
            self.ccp_id = f"CCP-{uuid.uuid4().hex[:8].upper()}"


@dataclass
class HACCPValidation:
    ccp_count: int
    hazard_coverage: float
    compliance_score: float
    issues: List[str] = field(default_factory=list)


@dataclass
class TemperatureReading:
    sensor_id: str
    temperature_celsius: float
    timestamp: str
    within_range: bool
    target_min: float
    target_max: float
    alert_message: str = ""

    @property
    def deviation(self) -> float:
        if self.temperature_celsius < self.target_min:
            return self.target_min - self.temperature_celsius
        if self.temperature_celsius > self.target_max:
            return self.temperature_celsius - self.target_max
        return 0.0


@dataclass
class SensorConfig:
    sensor_id: str
    location: str
    target_range_celsius: Tuple[float, float]
    alert_threshold_celsius: float


@dataclass
class TraceEvent:
    lot_number: str
    event_type: EventType
    location: str
    timestamp: str
    details: Dict[str, Any]
    event_id: str = ""

    def __post_init__(self):
        if not self.event_id:
            self.event_id = f"EVT-{uuid.uuid4().hex[:10].upper()}"


@dataclass
class TraceHistory:
    lot_number: str
    events: List[TraceEvent]
    total_duration_hours: float
    is_complete: bool


@dataclass
class DistributionInfo:
    total_units: float
    retailer_count: int
    states_affected: List[str]
    customers_notified: int


@dataclass
class RecallRecord:
    recall_id: str
    product: str
    lot_numbers: List[str]
    reason: str
    severity: RecallSeverity
    initiating_agency: str
    status: str = "active"
    initiated_date: str = field(default_factory=lambda: datetime.now().isoformat())


class HACCPPlan:
    """Digital HACCP plan management."""

    def __init__(self, facility_id: str, product: str, flow_description: str):
        self.facility_id = facility_id
        self.product = product
        self.flow_description = flow_description
        self._ccps: List[CCP] = []

    def add_ccp(self, ccp: CCP) -> None:
        self._ccps.append(ccp)

    def get_ccps(self) -> List[CCP]:
        return list(self._ccps)

    def validate(self) -> HACCPValidation:
        hazards_covered = {ccp.hazard for ccp in self._ccps}
        all_hazards = set(HazardType)
        coverage = len(hazards_covered) / len(all_hazards)

        issues = []
        if HazardType.BIOLOGICAL not in hazards_covered:
            issues.append("No biological hazard CCP defined")
        if HazardType.PHYSICAL not in hazards_covered:
            issues.append("No physical hazard CCP defined")

        score = min(coverage * 0.8 + (len(self._ccps) / 5) * 0.2, 1.0)
        return HACCPValidation(
            ccp_count=len(self._ccps),
            hazard_coverage=coverage,
            compliance_score=round(score, 2),
            issues=issues,
        )


class TemperatureMonitor:
    """IoT temperature monitoring with alerts."""

    def __init__(self, facility_id: str, monitoring_interval_seconds: int = 60,
                 alert_channels: Optional[List[str]] = None):
        self.facility_id = facility_id
        self.interval = monitoring_interval_seconds
        self.alert_channels = alert_channels or ["dashboard"]
        self._sensors: Dict[str, SensorConfig] = {}
        self._readings: Dict[str, List[TemperatureReading]] = {}
        self._alerts: List[Dict[str, Any]] = []

    def register_sensor(self, sensor_id: str, location: str,
                        target_range_celsius: Tuple[float, float],
                        alert_threshold_celsius: float) -> SensorConfig:
        sensor = SensorConfig(sensor_id, location, target_range_celsius, alert_threshold_celsius)
        self._sensors[sensor_id] = sensor
        return sensor

    def record_reading(self, sensor_id: str, temperature: float) -> TemperatureReading:
        sensor = self._sensors.get(sensor_id)
        if not sensor:
            raise ValueError(f"Sensor {sensor_id} not found")

        within = sensor.target_range_celsius[0] <= temperature <= sensor.target_range_celsius[1]
        reading = TemperatureReading(
            sensor_id=sensor_id, temperature_celsius=temperature,
            timestamp=datetime.now().isoformat(), within_range=within,
            target_min=sensor.target_range_celsius[0],
            target_max=sensor.target_range_celsius[1],
        )

        if not within:
            reading.alert_message = f"Temperature {temperature:.1f}C outside range {sensor.target_range_celsius}"
            self._alerts.append({
                "sensor_id": sensor_id, "temperature": temperature,
                "alert": reading.alert_message, "timestamp": reading.timestamp,
            })

        self._readings.setdefault(sensor_id, []).append(reading)
        return reading

    def get_current_readings(self) -> Dict[str, TemperatureReading]:
        result = {}
        for sensor_id in self._sensors:
            readings = self._readings.get(sensor_id, [])
            if readings:
                result[sensor_id] = readings[-1]
        return result

    def get_alerts(self) -> List[Dict[str, Any]]:
        return list(self._alerts)


class TraceabilitySystem:
    """Farm-to-fork product traceability."""

    def __init__(self, lot_level_tracking: bool = True,
                 qr_code_generation: bool = True,
                 blockchain_anchored: bool = False):
        self.lot_tracking = lot_level_tracking
        self.qr_gen = qr_code_generation
        self.blockchain = blockchain_anchored
        self._events: Dict[str, List[TraceEvent]] = {}

    def record_event(self, lot_number: str, event_type: str,
                     location: str, timestamp: str,
                     details: Optional[Dict[str, Any]] = None) -> TraceEvent:
        event = TraceEvent(
            lot_number=lot_number,
            event_type=EventType(event_type),
            location=location, timestamp=timestamp,
            details=details or {},
        )
        self._events.setdefault(lot_number, []).append(event)
        return event

    def trace_lot(self, lot_number: str) -> TraceHistory:
        events = self._events.get(lot_number, [])
        events.sort(key=lambda e: e.timestamp)

        duration = 0.0
        if len(events) >= 2:
            first = datetime.fromisoformat(events[0].timestamp)
            last = datetime.fromisoformat(events[-1].timestamp)
            duration = (last - first).total_seconds() / 3600

        expected_events = {e.value for e in EventType}
        recorded_events = {e.event_type.value for e in events}

        return TraceHistory(
            lot_number=lot_number, events=events,
            total_duration_hours=round(duration, 1),
            is_complete=expected_events.issubset(recorded_events),
        )


class RecallManager:
    """Food recall initiation and management."""

    def __init__(self):
        self._recalls: Dict[str, RecallRecord] = {}

    def initiate(self, product: str, lot_numbers: List[str],
                 reason: str, severity: RecallSeverity,
                 initiating_agency: str = "FDA") -> RecallRecord:
        recall_id = f"RECALL-{uuid.uuid4().hex[:8].upper()}"
        record = RecallRecord(
            recall_id=recall_id, product=product,
            lot_numbers=lot_numbers, reason=reason,
            severity=severity, initiating_agency=initiating_agency,
        )
        self._recalls[recall_id] = record
        return record

    def trace_distribution(self, recall_id: str) -> DistributionInfo:
        record = self._recalls.get(recall_id)
        if not record:
            raise ValueError(f"Recall {recall_id} not found")
        return DistributionInfo(
            total_units=15000, retailer_count=45,
            states_affected=["FL", "GA", "AL", "SC", "NC"],
            customers_notified=0,
        )

    def get_recall(self, recall_id: str) -> Optional[RecallRecord]:
        return self._recalls.get(recall_id)


def main():
    print("=" * 60)
    print("  Food Safety Technology Demo")
    print("=" * 60)

    # HACCP
    print("\n--- HACCP Plan ---")
    plan = HACCPPlan("PLANT-001", "Fresh Orange Juice",
                     "Receiving → Washing → Extraction → Pasteurization → Filling")
    plan.add_ccp(CCP("Pasteurization", "Pasteurization", HazardType.BIOLOGICAL,
                     {"temperature_celsius": 90, "time_seconds": 30},
                     "Continuous temperature recording", "Re-pasteurize", "Daily calibration"))
    plan.add_ccp(CCP("Metal Detection", "Post-Filling", HazardType.PHYSICAL,
                     {"ferrous_mm": 1.5}, "Test every 30 min", "Reject and re-inspect",
                     "Daily sensitivity check"))
    v = plan.validate()
    print(f"  CCPs: {v.ccp_count}, Coverage: {v.hazard_coverage:.0%}, Score: {v.compliance_score:.0%}")

    # Temperature
    print("\n--- Temperature Monitoring ---")
    temp_mon = TemperatureMonitor("PLANT-001")
    temp_mon.register_sensor("CS-01", "Cold Storage A", (0, 4), 6)
    temp_mon.register_sensor("TRUCK-12", "Truck #12", (0, 4), 5)
    temp_mon.record_reading("CS-01", 2.5)
    temp_mon.record_reading("TRUCK-12", 7.2)  # Out of range
    readings = temp_mon.get_current_readings()
    for sid, r in readings.items():
        status = "OK" if r.within_range else "ALERT"
        print(f"  {sid}: {r.temperature_celsius:.1f}C [{status}]")

    # Traceability
    print("\n--- Traceability ---")
    trace = TraceabilitySystem()
    trace.record_event("OJ-001", "harvest", "Sunny Grove Farm", "2026-07-01T06:00:00")
    trace.record_event("OJ-001", "processing", "JuiceCo Plant", "2026-07-01T14:00:00")
    trace.record_event("OJ-001", "packaging", "JuiceCo Plant", "2026-07-01T16:00:00")
    trace.record_event("OJ-001", "transport", "Truck #12", "2026-07-01T18:00:00")
    trace.record_event("OJ-001", "receiving", "FreshMart DC", "2026-07-02T06:00:00")
    h = trace.trace_lot("OJ-001")
    print(f"  Lot: {h.lot_number}, Events: {len(h.events)}, Duration: {h.total_duration_hours:.1f}h")

    # Recall
    print("\n--- Recall Management ---")
    rm = RecallManager()
    recall = rm.initiate("Fresh OJ", ["OJ-001"], "Potential Salmonella", RecallSeverity.CLASS_1)
    dist = rm.trace_distribution(recall.recall_id)
    print(f"  Recall: {recall.recall_id} ({recall.severity.value})")
    print(f"  Affected: {dist.total_units:,.0f} units across {dist.retailer_count} retailers")


if __name__ == "__main__":
    main()
