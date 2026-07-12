"""
Proximity Sensing Module — BLE beacon ranging, UWB positioning, RFID/NFC detection,
zone management, presence detection, and multi-source fusion for indoor proximity.
"""

from __future__ import annotations

import json
import math
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RangingMode(Enum):
    IMMEDIATE = "immediate"   # < 0.5m
    NEAR = "near"             # 0.5 - 3m
    FAR = "far"               # 3 - 70m
    OUT_OF_RANGE = "out_of_range"


class BeaconType(Enum):
    IBEACON = "ibeacon"
    EDDYSTONE = "eddystone"
    CUSTOM = "custom"


class TagType(Enum):
    ASSET = "asset"
    PERSON = "person"
    VEHICLE = "vehicle"
    EQUIPMENT = "equipment"


class ProximityEventType(Enum):
    ZONE_ENTER = "zone_enter"
    ZONE_EXIT = "zone_exit"
    DEVICE_DETECTED = "device_detected"
    DEVICE_LOST = "device_lost"
    DISTANCE_CHANGE = "distance_change"
    BATTERY_LOW = "battery_low"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Beacon:
    """A BLE beacon device."""
    beacon_id: str
    uuid: str
    major: int = 0
    minor: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    tx_power_dbm: int = -59
    beacon_type: BeaconType = BeaconType.IBEACON
    battery_pct: float = 100.0
    advertising_interval_ms: int = 1000
    firmware_version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "beacon_id": self.beacon_id,
            "uuid": self.uuid,
            "major": self.major,
            "minor": self.minor,
            "tx_power": self.tx_power_dbm,
        }


@dataclass
class UWBTag:
    """An Ultra-Wideband positioning tag."""
    tag_id: str
    tag_type: TagType = TagType.ASSET
    location: Tuple[float, float] = (0.0, 0.0)
    battery_pct: float = 100.0
    is_moving: bool = False
    last_update: str = ""
    firmware_version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tag_id": self.tag_id,
            "type": self.tag_type.value,
            "location": self.location,
            "battery": self.battery_pct,
        }


@dataclass
class RFIDTag:
    """An RFID/NFC tag."""
    tag_id: str
    tag_type: TagType = TagType.ASSET
    epc: str = ""  # Electronic Product Code
    last_read: str = ""
    read_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {"tag_id": self.tag_id, "epc": self.epc, "reads": self.read_count}


@dataclass
class Zone:
    """A proximity zone with entry/exit actions."""
    zone_id: str
    name: str
    center: Tuple[float, float] = (0.0, 0.0)
    radius_m: float = 5.0
    ranging_mode: RangingMode = RangingMode.NEAR
    on_enter: Optional[str] = None
    on_exit: Optional[str] = None
    max_occupancy: int = 0
    current_occupancy: int = 0

    def contains_point(self, x: float, y: float) -> bool:
        dx = x - self.center[0]
        dy = y - self.center[1]
        return math.sqrt(dx * dx + dy * dy) <= self.radius_m

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "center": self.center,
            "radius_m": self.radius_m,
            "occupancy": self.current_occupancy,
        }


@dataclass
class ProximityEvent:
    """A proximity detection event."""
    event_id: str
    event_type: ProximityEventType
    device_id: str
    distance_m: float
    rssi_dbm: float
    ranging_mode: RangingMode
    zone: Optional[str] = None
    confidence: float = 0.9
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "type": self.event_type.value,
            "device_id": self.device_id,
            "distance_m": round(self.distance_m, 2),
            "rssi": self.rssi_dbm,
            "zone": self.zone,
        }


@dataclass
class RangingResult:
    """Result of a ranging measurement."""
    device_id: str
    distance_m: float
    rssi_dbm: float
    ranging_mode: RangingMode
    accuracy_m: float
    measurement_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ProximityProfile:
    """A proximity detection profile with rules."""
    profile_id: str
    name: str
    ranging_interval_ms: int = 1000
    rssi_filter_threshold: int = -90
    hysteresis_m: float = 0.5
    zones: List[Zone] = field(default_factory=list)
    enabled: bool = True


@dataclass
class ContactTrace:
    """A privacy-preserved contact tracing record."""
    trace_id: str
    rolling_id: str  # Rotating pseudonymous identifier
    proximity_distance_m: float
    duration_seconds: float
    timestamp_start: str
    timestamp_end: str
    risk_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "rolling_id": self.rolling_id[:8] + "...",
            "distance_m": round(self.proximity_distance_m, 1),
            "duration_s": round(self.duration_seconds, 0),
            "risk_score": round(self.risk_score, 2),
        }


@dataclass
class ProximitySummary:
    """Summary of proximity sensing activity."""
    total_devices_detected: int = 0
    zones_active: int = 0
    events_count: int = 0
    average_distance_m: float = 0.0
    coverage_pct: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "devices": self.total_devices_detected,
            "zones": self.zones_active,
            "events": self.events_count,
            "avg_distance_m": round(self.average_distance_m, 2),
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class ProximityManager:
    """Main proximity sensing manager coordinating beacons, tags, and zones."""

    # Path loss model parameters for RSSI-to-distance conversion
    PATH_LOSS_EXPONENT = 2.5
    REFERENCE_DISTANCE_M = 1.0

    def __init__(self):
        self._beacons: Dict[str, Beacon] = {}
        self._uwb_tags: Dict[str, UWBTag] = {}
        self._rfid_tags: Dict[str, RFIDTag] = {}
        self._zones: Dict[str, Zone] = {}
        self._events: List[ProximityEvent] = []
        self._ranging_results: Dict[str, List[RangingResult]] = {}
        self._contact_traces: List[ContactTrace] = []
        self._event_handlers: Dict[ProximityEventType, List[Callable]] = {}

    def register_beacon(self, beacon: Beacon) -> None:
        self._beacons[beacon.beacon_id] = beacon

    def register_uwb_tag(self, tag: UWBTag) -> None:
        self._uwb_tags[tag.tag_id] = tag

    def register_rfid_tag(self, tag: RFIDTag) -> None:
        self._rfid_tags[tag.tag_id] = tag

    def add_zone(self, zone: Zone) -> None:
        self._zones[zone.zone_id] = zone

    def on_event(self, event_type: ProximityEventType, callback: Callable) -> None:
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(callback)

    def rssi_to_distance(self, rssi_dbm: int, tx_power_dbm: int = -59) -> float:
        """Convert RSSI to estimated distance using path loss model."""
        if rssi_dbm == 0:
            return -1.0
        ratio = (tx_power_dbm - rssi_dbm) / (10 * self.PATH_LOSS_EXPONENT)
        return round(self.REFERENCE_DISTANCE_M * (10 ** ratio), 2)

    def classify_range(self, distance_m: float) -> RangingMode:
        if distance_m < 0.5:
            return RangingMode.IMMEDIATE
        elif distance_m < 3.0:
            return RangingMode.NEAR
        elif distance_m < 70.0:
            return RangingMode.FAR
        return RangingMode.OUT_OF_RANGE

    def scan(self, duration_s: float = 5.0) -> List[ProximityEvent]:
        """Perform a proximity scan and return events."""
        events = []
        scan_end = time.time() + duration_s

        while time.time() < scan_end:
            for beacon_id, beacon in self._beacons.items():
                # Simulate RSSI reading
                rssi = beacon.tx_power_dbm - 40
                distance = self.rssi_to_distance(rssi, beacon.tx_power_dbm)
                mode = self.classify_range(distance)

                # Check zone containment
                zone_name = None
                for zone in self._zones.values():
                    if zone.contains_point(beacon.latitude + distance * 0.00001, beacon.longitude):
                        zone_name = zone.zone_id

                event = ProximityEvent(
                    event_id=f"PX-{uuid.uuid4().hex[:8].upper()}",
                    event_type=ProximityEventType.DEVICE_DETECTED,
                    device_id=beacon_id,
                    distance_m=distance,
                    rssi_dbm=rssi,
                    ranging_mode=mode,
                    zone=zone_name,
                )
                events.append(event)
                self._events.append(event)

                # Store ranging result
                if beacon_id not in self._ranging_results:
                    self._ranging_results[beacon_id] = []
                self._ranging_results[beacon_id].append(RangingResult(
                    device_id=beacon_id,
                    distance_m=distance,
                    rssi_dbm=rssi,
                    ranging_mode=mode,
                    accuracy_m=distance * 0.3,
                ))

                # Fire handlers
                for handler in self._event_handlers.get(ProximityEventType.DEVICE_DETECTED, []):
                    handler(event)

            time.sleep(0.1)

        return events

    def get_nearby_devices(self, max_distance_m: float = 5.0) -> List[Dict[str, Any]]:
        nearby = []
        for device_id, results in self._ranging_results.items():
            if results:
                latest = results[-1]
                if latest.distance_m <= max_distance_m:
                    nearby.append({
                        "device_id": device_id,
                        "distance_m": latest.distance_m,
                        "ranging_mode": latest.ranging_mode.value,
                        "accuracy_m": latest.accuracy_m,
                    })
        return sorted(nearby, key=lambda d: d["distance_m"])

    def get_zone_occupancy(self) -> Dict[str, int]:
        return {z.zone_id: z.current_occupancy for z in self._zones.values()}

    def get_summary(self) -> ProximitySummary:
        total_devices = len(self._ranging_results)
        distances = [r[-1].distance_m for r in self._ranging_results.values() if r]
        avg_dist = sum(distances) / len(distances) if distances else 0
        return ProximitySummary(
            total_devices_detected=total_devices,
            zones_active=len(self._zones),
            events_count=len(self._events),
            average_distance_m=avg_dist,
        )

    def generate_contact_trace(
        self, device_id: str, distance_m: float, duration_s: float
    ) -> ContactTrace:
        risk = 0.0
        if distance_m < 2.0 and duration_s > 600:
            risk = 0.8
        elif distance_m < 2.0 and duration_s > 300:
            risk = 0.5
        elif distance_m < 5.0 and duration_s > 900:
            risk = 0.3

        trace = ContactTrace(
            trace_id=f"CT-{uuid.uuid4().hex[:8].upper()}",
            rolling_id=uuid.uuid4().hex[:16],
            proximity_distance_m=distance_m,
            duration_seconds=duration_s,
            timestamp_start=datetime.now(timezone.utc).isoformat(),
            timestamp_end=datetime.now(timezone.utc).isoformat(),
            risk_score=risk,
        )
        self._contact_traces.append(trace)
        return trace

    def export_events(self, path: str) -> None:
        data = [e.to_dict() for e in self._events]
        Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the proximity sensing platform."""
    print("Proximity Sensing Platform")
    print("=" * 60)

    manager = ProximityManager()

    # Register beacons
    for i, (bid, uuid_str) in enumerate([
        ("entrance", "E2C56DB5-DFFB-48D2-B060-D0F5A71096E0"),
        ("lobby", "FDA50693-A4E2-4FB1-AFCF-C6EB07647825"),
        ("office", "74278BDA-B644-4520-8F3C-0AF797BE98D5"),
    ]):
        manager.register_beacon(Beacon(
            beacon_id=bid, uuid=uuid_str, major=1, minor=i + 1,
            latitude=i * 5.0, longitude=0.0, tx_power_dbm=-59,
        ))

    # Register UWB tags
    manager.register_uwb_tag(UWBTag(tag_id="cart-01", tag_type=TagType.ASSET, location=(3.0, 4.0)))
    manager.register_uwb_tag(UWBTag(tag_id="cart-02", tag_type=TagType.ASSET, location=(7.0, 2.0)))

    # Add zones
    manager.add_zone(Zone(zone_id="entrance", name="Entrance", center=(0, 0), radius_m=3.0))
    manager.add_zone(Zone(zone_id="lobby", name="Lobby", center=(5, 0), radius_m=5.0))

    # Scan
    events = manager.scan(duration_s=1.0)
    print(f"\nScanned {len(events)} proximity events:")
    for e in events[:5]:
        print(f"  {e.device_id}: {e.distance_m}m ({e.ranging_mode.value}) zone={e.zone}")

    # Nearby
    nearby = manager.get_nearby_devices(max_distance_m=50)
    print(f"\nNearby devices: {len(nearby)}")
    for d in nearby[:5]:
        print(f"  {d['device_id']}: {d['distance_m']:.1f}m ({d['ranging_mode']})")

    # Contact trace
    trace = manager.generate_contact_trace("cart-01", 1.5, 600)
    print(f"\nContact trace: risk={trace.risk_score:.1f}, distance={trace.proximity_distance_m}m")

    summary = manager.get_summary()
    print(f"\nSummary: {summary.total_devices_detected} devices, {summary.events_count} events")


if __name__ == "__main__":
    main()
