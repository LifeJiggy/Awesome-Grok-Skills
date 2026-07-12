"""
Agricultural Supply Chain Module — Farm-to-fork traceability, cold chain monitoring,
logistics optimization, inventory management, and blockchain provenance tracking.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EventType(Enum):
    HARVEST = "harvest"
    WASH_PACK = "wash_pack"
    STORAGE = "storage"
    TRANSPORT = "transport"
    RECEIVE = "receive"
    PROCESS = "process"
    SHIP = "ship"
    RETAIL = "retail"
    CONSUME = "consume"
    RECALL = "recall"


class QualityGrade(Enum):
    USDA_EXTRA_FANCY = "USDA Extra Fancy"
    USDA_FANCY = "USDA Fancy"
    USDA_1 = "USDA #1"
    USDA_2 = "USDA #2"
    USDA_3 = "USDA #3"
    REJECT = "Reject"


class ColdChainStatus(Enum):
    NOMINAL = "nominal"
    WARNING = "warning"
    CRITICAL = "critical"
    FAILURE = "failure"


class InventoryRotation(Enum):
    FIFO = "fifo"
    FEFO = "fefo"
    LIFO = "lifo"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Lot:
    """A traceable production lot."""
    lot_id: str
    crop: str
    variety: str
    field_id: str
    harvest_date: str
    quantity_lbs: float
    grade: str
    organic_certified: bool = False
    harvest_crew: str = ""
    packing_facility: str = ""
    qr_code_url: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    shelf_life_days: int = 14
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, crop: str, variety: str, field_id: str, harvest_date: str,
               quantity_lbs: float, grade: str = "USDA #1",
               organic_certified: bool = False, **kwargs: Any) -> Lot:
        lot_id = f"LOT-{uuid.uuid4().hex[:8].upper()}"
        return cls(
            lot_id=lot_id, crop=crop, variety=variety, field_id=field_id,
            harvest_date=harvest_date, quantity_lbs=quantity_lbs, grade=grade,
            organic_certified=organic_certified,
            qr_code_url=f"https://trace.example.com/lot/{lot_id}",
            **kwargs,
        )

    @property
    def expiry_date(self) -> str:
        harvest = datetime.fromisoformat(self.harvest_date)
        return (harvest + timedelta(days=self.shelf_life_days)).isoformat()

    @property
    def days_until_expiry(self) -> int:
        expiry = datetime.fromisoformat(self.expiry_date)
        now = datetime.now(timezone.utc)
        return max(0, (expiry - now.replace(tzinfo=None)).days)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lot_id": self.lot_id,
            "crop": self.crop,
            "variety": self.variety,
            "field_id": self.field_id,
            "harvest_date": self.harvest_date,
            "quantity_lbs": round(self.quantity_lbs, 1),
            "grade": self.grade,
            "organic": self.organic_certified,
            "expiry": self.expiry_date,
        }


@dataclass
class TraceEvent:
    """A single event in the supply chain traceability record."""
    event_id: str
    lot_id: str
    event_type: EventType
    location: str
    description: str
    responsible_party: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    temperature_f: Optional[float] = None
    humidity_pct: Optional[float] = None
    verified: bool = False
    blockchain_hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "lot_id": self.lot_id,
            "type": self.event_type.value,
            "location": self.location,
            "description": self.description,
            "timestamp": self.timestamp,
            "temperature": self.temperature_f,
        }


@dataclass
class ColdChainReading:
    """A temperature/humidity reading during cold chain monitoring."""
    sensor_id: str
    lot_id: str
    temperature_f: float
    humidity_pct: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ethylene_ppm: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensor": self.sensor_id,
            "temp_f": round(self.temperature_f, 1),
            "humidity": round(self.humidity_pct, 1),
            "timestamp": self.timestamp,
        }


@dataclass
class ColdChainStatusResult:
    """Current cold chain status for a monitored lot."""
    lot_id: str
    status: ColdChainStatus
    current_temp_f: float
    min_temp_f: float
    max_temp_f: float
    avg_temp_f: float
    time_out_of_range_min: float
    readings_count: int
    alerts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lot_id": self.lot_id,
            "status": self.status.value,
            "current_temp": round(self.current_temp_f, 1),
            "min_temp": round(self.min_temp_f, 1),
            "max_temp": round(self.max_temp_f, 1),
            "alerts": self.alerts,
        }


@dataclass
class RouteStop:
    """A stop on an optimized delivery route."""
    order: int
    location: str
    latitude: float = 0.0
    longitude: float = 0.0
    load_lbs: float = 0.0
    estimated_arrival: str = ""
    service_time_min: float = 30.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "order": self.order,
            "location": self.location,
            "load_lbs": round(self.load_lbs, 0),
            "eta": self.estimated_arrival,
        }


@dataclass
class OptimizedRoute:
    """An optimized delivery route."""
    route_id: str
    origin: str
    stops: List[RouteStop] = field(default_factory=list)
    total_miles: float = 0.0
    estimated_hours: float = 0.0
    fuel_cost: float = 0.0
    total_load_lbs: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route_id": self.route_id,
            "origin": self.origin,
            "stops": len(self.stops),
            "total_miles": round(self.total_miles, 1),
            "estimated_hours": round(self.estimated_hours, 1),
            "fuel_cost": round(self.fuel_cost, 2),
        }


@dataclass
class InventoryItem:
    """A lot tracked in inventory."""
    lot: Lot
    quantity_lbs: float
    location: str = "warehouse"
    received_date: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    rotation_priority: float = 0.0  # for FEFO sorting

    @property
    def days_in_inventory(self) -> int:
        received = datetime.fromisoformat(self.received_date)
        return (datetime.now(timezone.utc) - received.replace(tzinfo=None)).days

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lot_id": self.lot.lot_id,
            "quantity_lbs": round(self.quantity_lbs, 1),
            "days_in_stock": self.days_in_inventory,
            "days_to_expiry": self.lot.days_until_expiry,
        }


@dataclass
class BlockchainRecord:
    """An immutable blockchain provenance record."""
    record_id: str
    lot_id: str
    event_type: str
    data_hash: str
    previous_hash: str
    timestamp: str
    block_number: int
    verified: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "lot_id": self.lot_id,
            "block": self.block_number,
            "hash": self.data_hash[:16] + "...",
            "verified": self.verified,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class Traceability:
    """Farm-to-fork traceability system with chain of custody tracking."""

    def __init__(self):
        self._events: Dict[str, List[TraceEvent]] = {}
        self._blockchain: List[BlockchainRecord] = []
        self._block_number = 0

    def record_event(
        self,
        lot_id: str,
        event_type: str,
        location: str,
        description: str,
        responsible_party: str = "",
        temperature_f: Optional[float] = None,
    ) -> TraceEvent:
        event = TraceEvent(
            event_id=f"EVT-{uuid.uuid4().hex[:8].upper()}",
            lot_id=lot_id,
            event_type=EventType(event_type),
            location=location,
            description=description,
            responsible_party=responsible_party,
            temperature_f=temperature_f,
        )
        if lot_id not in self._events:
            self._events[lot_id] = []
        self._events[lot_id].append(event)

        # Create blockchain record
        data_str = json.dumps(event.to_dict(), sort_keys=True)
        data_hash = hashlib.sha256(data_str.encode()).hexdigest()
        prev_hash = self._blockchain[-1].data_hash if self._blockchain else "0" * 64
        self._block_number += 1
        record = BlockchainRecord(
            record_id=f"BLK-{self._block_number}",
            lot_id=lot_id,
            event_type=event_type,
            data_hash=data_hash,
            previous_hash=prev_hash,
            timestamp=event.timestamp,
            block_number=self._block_number,
        )
        self._blockchain.append(record)
        event.blockchain_hash = data_hash
        event.verified = True
        return event

    def get_full_history(self, lot_id: str) -> List[TraceEvent]:
        return self._events.get(lot_id, [])

    def verify_chain(self) -> bool:
        """Verify blockchain integrity."""
        for i in range(1, len(self._blockchain)):
            if self._blockchain[i].previous_hash != self._blockchain[i - 1].data_hash:
                return False
        return True

    def get_chain_length(self) -> int:
        return len(self._blockchain)


class ColdChain:
    """Monitor and validate cold chain conditions during transport and storage."""

    def __init__(self, max_temp_f: float = 41.0, min_temp_f: float = 32.0,
                 warning_buffer_f: float = 2.0):
        self.max_temp_f = max_temp_f
        self.min_temp_f = min_temp_f
        self.warning_buffer_f = warning_buffer_f
        self._monitoring: Dict[str, List[ColdChainReading]] = {}

    def start_monitoring(self, lot_id: str, sensor_id: str = "",
                         max_temp_f: float = 41.0) -> None:
        self.max_temp_f = max_temp_f
        self._monitoring[lot_id] = []

    def add_reading(self, reading: ColdChainReading) -> Optional[str]:
        """Add a reading and return alert message if out of range."""
        if reading.lot_id not in self._monitoring:
            self._monitoring[reading.lot_id] = []
        self._monitoring[reading.lot_id].append(reading)

        if reading.temperature_f > self.max_temp_f:
            return f"CRITICAL: Temperature {reading.temperature_f}°F exceeds max {self.max_temp_f}°F"
        elif reading.temperature_f > self.max_temp_f - self.warning_buffer_f:
            return f"WARNING: Temperature {reading.temperature_f}°F approaching limit"
        elif reading.temperature_f < self.min_temp_f:
            return f"WARNING: Temperature {reading.temperature_f}°F below minimum {self.min_temp_f}°F"
        return None

    def check_status(self, lot_id: str) -> ColdChainStatusResult:
        readings = self._monitoring.get(lot_id, [])
        if not readings:
            return ColdChainStatusResult(
                lot_id=lot_id, status=ColdChainStatus.NOMINAL,
                current_temp_f=0, min_temp_f=0, max_temp_f=0, avg_temp_f=0,
                time_out_of_range_min=0, readings_count=0,
            )

        temps = [r.temperature_f for r in readings]
        out_of_range = sum(1 for t in temps if t > self.max_temp_f or t < self.min_temp_f)

        status = ColdChainStatus.NOMINAL
        if out_of_range > len(temps) * 0.1:
            status = ColdChainStatus.CRITICAL
        elif out_of_range > 0:
            status = ColdChainStatus.WARNING

        return ColdChainStatusResult(
            lot_id=lot_id,
            status=status,
            current_temp_f=temps[-1],
            min_temp_f=min(temps),
            max_temp_f=max(temps),
            avg_temp_f=sum(temps) / len(temps),
            time_out_of_range_min=out_of_range * 5,
            readings_count=len(readings),
        )


class LogisticsOptimizer:
    """Optimize delivery routes for agricultural supply chain logistics."""

    COST_PER_MILE = 1.85
    AVG_SPEED_MPH = 55.0

    def optimize_route(
        self,
        origin: str,
        destinations: List[str],
        vehicle_capacity_lbs: float = 40000,
    ) -> OptimizedRoute:
        """Generate an optimized delivery route (nearest-neighbor heuristic)."""
        route = OptimizedRoute(
            route_id=f"ROUTE-{uuid.uuid4().hex[:8].upper()}",
            origin=origin,
        )

        current_miles = 0.0
        for i, dest in enumerate(destinations):
            segment_miles = 50 + i * 30  # simplified distance estimation
            current_miles += segment_miles
            hours = current_miles / self.AVG_SPEED_MPH
            arrival_time = datetime.now(timezone.utc) + timedelta(hours=hours)

            route.stops.append(RouteStop(
                order=i + 1,
                location=dest,
                load_lbs=vehicle_capacity_lbs / len(destinations),
                estimated_arrival=arrival_time.strftime("%Y-%m-%d %H:%M"),
            ))

        route.total_miles = current_miles
        route.estimated_hours = current_miles / self.AVG_SPEED_MPH
        route.fuel_cost = route.total_miles * self.COST_PER_MILE
        route.total_load_lbs = vehicle_capacity_lbs
        return route


class InventoryManager:
    """Manage lot-based agricultural inventory with rotation strategies."""

    def __init__(self, rotation: InventoryRotation = InventoryRotation.FEFO):
        self.rotation = rotation
        self._items: List[InventoryItem] = []

    def receive(self, lot: Lot, quantity_lbs: Optional[float] = None,
                location: str = "warehouse") -> InventoryItem:
        qty = quantity_lbs or lot.quantity_lbs
        item = InventoryItem(lot=lot, quantity_lbs=qty, location=location)
        self._items.append(item)
        return item

    def ship(self, lot_id: str, quantity_lbs: float) -> Optional[InventoryItem]:
        """Ship quantity from a lot (FIFO/FEFO order)."""
        candidates = [i for i in self._items if i.lot.lot_id == lot_id and i.quantity_lbs > 0]
        if not candidates:
            return None

        if self.rotation == InventoryRotation.FEFO:
            candidates.sort(key=lambda x: x.lot.days_until_expiry)
        elif self.rotation == InventoryRotation.FIFO:
            candidates.sort(key=lambda x: x.received_date)

        item = candidates[0]
        ship_qty = min(quantity_lbs, item.quantity_lbs)
        item.quantity_lbs -= ship_qty
        if item.quantity_lbs <= 0:
            self._items.remove(item)
        return item

    @property
    def total_lbs(self) -> float:
        return sum(i.quantity_lbs for i in self._items)

    @property
    def lot_count(self) -> int:
        return len([i for i in self._items if i.quantity_lbs > 0])

    @property
    def expiring_lots_count(self) -> int:
        return sum(1 for i in self._items if i.lot.days_until_expiry <= 3)

    def get_inventory(self) -> List[Dict[str, Any]]:
        return [i.to_dict() for i in self._items if i.quantity_lbs > 0]

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_lbs": round(self.total_lbs, 1),
            "lot_count": self.lot_count,
            "expiring_soon": self.expiring_lots_count,
            "rotation": self.rotation.value,
        }


class BlockchainProvenance:
    """Blockchain-based provenance tracking for agricultural certifications."""

    def __init__(self):
        self._records: List[BlockchainRecord] = []
        self._block_number = 0

    def record_certification(self, lot_id: str, cert_type: str,
                             details: Dict[str, Any]) -> BlockchainRecord:
        data_str = json.dumps({"lot_id": lot_id, "cert": cert_type, "details": details}, sort_keys=True)
        data_hash = hashlib.sha256(data_str.encode()).hexdigest()
        prev_hash = self._records[-1].data_hash if self._records else "0" * 64
        self._block_number += 1

        record = BlockchainRecord(
            record_id=f"CERT-{self._block_number}",
            lot_id=lot_id,
            event_type=f"certification_{cert_type}",
            data_hash=data_hash,
            previous_hash=prev_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
            block_number=self._block_number,
        )
        self._records.append(record)
        return record

    def verify_lot(self, lot_id: str) -> List[BlockchainRecord]:
        return [r for r in self._records if r.lot_id == lot_id]

    def verify_chain_integrity(self) -> bool:
        for i in range(1, len(self._records)):
            if self._records[i].previous_hash != self._records[i - 1].data_hash:
                return False
        return True


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the agricultural supply chain toolkit."""
    print("Agricultural Supply Chain Management")
    print("=" * 60)

    # Create lot
    lot = Lot.create(
        crop="tomatoes", variety="Roma", field_id="FIELD-001",
        harvest_date="2024-07-15", quantity_lbs=5000, grade="USDA #1",
        organic_certified=True,
    )
    print(f"\nLot: {lot.lot_id}")
    print(f"  {lot.quantity_lbs} lbs {lot.variety} {lot.crop}")
    print(f"  Expiry: {lot.expiry_date}")

    # Traceability
    trace = Traceability()
    trace.record_event(lot.lot_id, "harvest", "Field-001", "Harvested by Team-A", temperature_f=85)
    trace.record_event(lot.lot_id, "wash_pack", "Pack-001", "Washed and packed", temperature_f=38)
    trace.record_event(lot.lot_id, "storage", "Cooler-01", "Stored at 38°F", temperature_f=38)
    trace.record_event(lot.lot_id, "transport", "Truck-4521", "Loaded for DC", temperature_f=36)
    trace.record_event(lot.lot_id, "receive", "DC-Chicago", "Received and inspected", temperature_f=37)

    history = trace.get_full_history(lot.lot_id)
    print(f"\nTraceability ({len(history)} events, chain: {trace.get_chain_length()} blocks):")
    for e in history:
        temp = f" ({e.temperature_f}°F)" if e.temperature_f else ""
        print(f"  {e.event_type.value:10s} @ {e.location:12s}{temp} — {e.description}")
    print(f"  Chain integrity: {'VALID' if trace.verify_chain() else 'BROKEN'}")

    # Cold chain
    print("\n--- Cold Chain Monitoring ---")
    cold = ColdChain()
    cold.start_monitoring(lot.lot_id, sensor_id="TEMP-001")
    for temp in [38, 39, 40, 42, 43, 41, 39, 37]:
        alert = cold.add_reading(ColdChainReading(
            sensor_id="TEMP-001", lot_id=lot.lot_id,
            temperature_f=temp, humidity_pct=90,
        ))
        if alert:
            print(f"  ALERT: {alert}")
    status = cold.check_status(lot.lot_id)
    print(f"  Status: {status.status.value}, Range: {status.min_temp_f}-{status.max_temp_f}°F")

    # Inventory
    print("\n--- Inventory Management ---")
    inv = InventoryManager(rotation=InventoryRotation.FEFO)
    inv.receive(lot)
    inv.receive(Lot.create("tomatoes", "Beefsteak", "FIELD-002", "2024-07-10", 3000, "USDA #1"))
    print(f"  Total: {inv.total_lbs:.0f} lbs in {inv.lot_count} lots")
    inv.ship(lot.lot_id, 1000)
    print(f"  After shipping 1000 lbs: {inv.total_lbs:.0f} lbs remaining")

    # Blockchain
    print("\n--- Blockchain Provenance ---")
    bc = BlockchainProvenance()
    bc.record_certification(lot.lot_id, "organic", {"certifier": "USDA NOP", "expires": "2025-01-01"})
    bc.record_certification(lot.lot_id, "fair_trade", {"certifier": "Fair Trade USA"})
    certs = bc.verify_lot(lot.lot_id)
    print(f"  {len(certs)} certification records for {lot.lot_id}")
    print(f"  Chain valid: {bc.verify_chain_integrity()}")


if __name__ == "__main__":
    main()
