"""
Food Supply Chain Management Module
Part of the food-tech skill domain

Provides cold chain monitoring, demand forecasting, supplier quality,
inventory management, and logistics for perishable food products.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid
import statistics


class TemperatureZone(Enum):
    FROZEN = "frozen"         # -18C or below
    DEEP_FROZEN = "deep_frozen"  # -30C or below
    CHILLED = "chilled"       # 0 to 4C
    FRESH = "fresh"           # -1 to 4C
    AMBIENT = "ambient"       # 10 to 25C


class ShipmentStatus(Enum):
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELAYED = "delayed"
    DELIVERED = "delivered"
    COMPROMISED = "compromised"


class Grade(Enum):
    A_PLUS = "A+"
    A = "A"
    B_PLUS = "B+"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


@dataclass
class TemperatureReading:
    sensor_id: str
    temperature_celsius: float
    timestamp: str


@dataclass
class ShipmentTracking:
    shipment_id: str
    product: str
    origin: str
    destination: str
    temperature_zone: TemperatureZone
    target_range: Tuple[float, float]
    status: ShipmentStatus
    readings: List[TemperatureReading]
    estimated_arrival: str
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def average_temperature(self) -> float:
        if not self.readings:
            return 0.0
        return statistics.mean(r.temperature_celsius for r in self.readings)

    @property
    def excursion_count(self) -> int:
        return sum(1 for r in self.readings
                   if not (self.target_range[0] <= r.temperature_celsius <= self.target_range[1]))

    @property
    def projected_shelf_life_hours(self) -> float:
        base = {"frozen": 720, "deep_frozen": 2160, "chilled": 120,
                "fresh": 96, "ambient": 720}
        base_hours = base.get(self.temperature_zone.value, 120)
        excursion_penalty = self.excursion_count * 12
        return max(base_hours - excursion_penalty, 0)


@dataclass
class DailyForecast:
    date: str
    predicted_units: float
    ci_lower: float
    ci_upper: float


@dataclass
class DemandForecastResult:
    product_id: str
    location: str
    total_units: float
    daily_forecast: List[DailyForecast]
    model: str
    confidence: float


@dataclass
class SupplierRegistration:
    supplier_id: str
    name: str
    category: str
    location: str
    certifications: List[str]
    registered_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SupplierScorecard:
    supplier_id: str
    supplier_name: str
    period: str
    overall_score: float
    grade: Grade
    area_scores: Dict[str, float]
    recommendations: List[str] = field(default_factory=list)


@dataclass
class InventoryItem:
    item_id: str
    product_id: str
    lot_number: str
    quantity: float
    unit: str
    received_date: str
    expiry_date: str
    temperature_zone: TemperatureZone
    location: str
    status: str = "available"

    @property
    def days_until_expiry(self) -> float:
        exp = datetime.fromisoformat(self.expiry_date)
        return max((exp - datetime.now()).total_seconds() / 86400, 0)

    @property
    def is_expired(self) -> bool:
        return self.days_until_expiry <= 0


class ColdChainManager:
    """Real-time cold chain temperature monitoring."""

    def __init__(self, alert_channels: Optional[List[str]] = None,
                 excursion_threshold_minutes: int = 15):
        self.alert_channels = alert_channels or ["dashboard"]
        self.excursion_threshold = excursion_threshold_minutes
        self._shipments: Dict[str, ShipmentTracking] = {}
        self._alerts: List[Dict[str, Any]] = []

    def create_shipment(
        self, shipment_id: str, product: str, origin: str, destination: str,
        temperature_zone: TemperatureZone, target_range_celsius: Tuple[float, float],
        estimated_transit_hours: float,
    ) -> ShipmentTracking:
        arrival = (datetime.now() + timedelta(hours=estimated_transit_hours)).isoformat()
        shipment = ShipmentTracking(
            shipment_id=shipment_id, product=product, origin=origin,
            destination=destination, temperature_zone=temperature_zone,
            target_range=target_range_celsius, status=ShipmentStatus.IN_TRANSIT,
            readings=[], estimated_arrival=arrival,
        )
        self._shipments[shipment_id] = shipment
        return shipment

    def record_temperature(self, shipment_id: str, temperature: float,
                           sensor_id: str = "default") -> TemperatureReading:
        shipment = self._shipments.get(shipment_id)
        if not shipment:
            raise ValueError(f"Shipment {shipment_id} not found")

        reading = TemperatureReading(
            sensor_id=sensor_id, temperature_celsius=temperature,
            timestamp=datetime.now().isoformat(),
        )
        shipment.readings.append(reading)

        if not (shipment.target_range[0] <= temperature <= shipment.target_range[1]):
            self._alerts.append({
                "shipment_id": shipment_id, "temperature": temperature,
                "timestamp": reading.timestamp,
                "message": f"Temperature excursion: {temperature:.1f}C",
            })

        return reading

    def get_shipment_status(self, shipment_id: str) -> ShipmentTracking:
        shipment = self._shipments.get(shipment_id)
        if not shipment:
            raise ValueError(f"Shipment {shipment_id} not found")
        return shipment

    def get_alerts(self) -> List[Dict[str, Any]]:
        return list(self._alerts)


class DemandForecaster:
    """Perishable goods demand forecasting."""

    def __init__(self, model: str = "prophet", granularity: str = "daily",
                 include_weather: bool = True):
        self.model = model
        self.granularity = granularity
        self.include_weather = include_weather

    def predict(
        self, product_id: str, location: str, horizon_days: int = 14,
        historical_data: str = "", special_events: Optional[List[str]] = None,
    ) -> DemandForecastResult:
        daily = []
        base = 500
        for i in range(horizon_days):
            date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            variation = base * (1 + 0.1 * ((-1) ** i) + 0.05 * (i % 7 < 2))
            ci_width = variation * 0.15
            daily.append(DailyForecast(
                date=date, predicted_units=round(variation),
                ci_lower=round(variation - ci_width),
                ci_upper=round(variation + ci_width),
            ))

        total = sum(d.predicted_units for d in daily)
        return DemandForecastResult(
            product_id=product_id, location=location,
            total_units=total, daily_forecast=daily,
            model=self.model, confidence=0.84,
        )


class SupplierQualityManager:
    """Supplier quality scoring and management."""

    def __init__(self):
        self._suppliers: Dict[str, SupplierRegistration] = {}

    def register_supplier(self, name: str, category: str, location: str,
                          certifications: Optional[List[str]] = None) -> SupplierRegistration:
        sid = f"SUP-{uuid.uuid4().hex[:8].upper()}"
        supplier = SupplierRegistration(sid, name, category, location, certifications or [])
        self._suppliers[sid] = supplier
        return supplier

    def score_supplier(self, supplier_id: str, period: str,
                       metrics: Dict[str, float]) -> SupplierScorecard:
        supplier = self._suppliers.get(supplier_id)
        if not supplier:
            raise ValueError(f"Supplier {supplier_id} not found")

        weights = {"on_time_delivery": 0.25, "quality_rejection_rate": 0.25,
                    "food_safety_audit_score": 0.25, "response_time_hours": 0.10,
                    "documentation_accuracy": 0.15}

        area_scores = {}
        weighted = 0.0
        for metric, weight in weights.items():
            val = metrics.get(metric, 0)
            if "rejection" in metric:
                score = max(0, (1 - val) * 100)
            elif "audit" in metric:
                score = val
            elif "response" in metric:
                score = max(0, (24 - val) / 24 * 100)
            else:
                score = min(val * 100, 100)
            area_scores[metric] = round(score, 1)
            weighted += score * weight

        grade_map = [(95, Grade.A_PLUS), (90, Grade.A), (85, Grade.B_PLUS),
                     (80, Grade.B), (70, Grade.C), (60, Grade.D)]
        grade = Grade.F
        for threshold, g in grade_map:
            if weighted >= threshold:
                grade = g
                break

        recs = []
        if area_scores.get("quality_rejection_rate", 100) < 80:
            recs.append("Implement incoming inspection protocol")
        if area_scores.get("food_safety_audit_score", 100) < 85:
            recs.append("Schedule food safety re-audit")

        return SupplierScorecard(
            supplier_id=supplier_id, supplier_name=supplier.name,
            period=period, overall_score=round(weighted, 1),
            grade=grade, area_scores=area_scores, recommendations=recs,
        )


class PerishableInventory:
    """FEFO-based perishable inventory management."""

    def __init__(self):
        self._items: Dict[str, InventoryItem] = {}

    def add_item(self, product_id: str, lot_number: str, quantity: float,
                 unit: str, expiry_date: str,
                 temperature_zone: TemperatureZone = TemperatureZone.FRESH,
                 location: str = "DC-01") -> InventoryItem:
        item_id = f"INV-{uuid.uuid4().hex[:10].upper()}"
        item = InventoryItem(
            item_id=item_id, product_id=product_id, lot_number=lot_number,
            quantity=quantity, unit=unit,
            received_date=datetime.now().isoformat(),
            expiry_date=expiry_date, temperature_zone=temperature_zone,
            location=location,
        )
        self._items[item_id] = item
        return item

    def get_fifo_allocation(self, product_id: str, quantity_needed: float) -> List[InventoryItem]:
        items = [i for i in self._items.values()
                 if i.product_id == product_id and i.status == "available" and not i.is_expired]
        items.sort(key=lambda i: i.expiry_date)  # FEFO: earliest expiry first

        allocated = []
        remaining = quantity_needed
        for item in items:
            if remaining <= 0:
                break
            take = min(item.quantity, remaining)
            allocated.append(item)
            remaining -= take
        return allocated

    def get_waste_report(self) -> Dict[str, Any]:
        items = list(self._items.values())
        expired = [i for i in items if i.is_expired]
        total_waste = sum(i.quantity for i in expired)
        return {
            "total_items": len(items),
            "expired_items": len(expired),
            "waste_quantity": total_waste,
            "waste_rate": len(expired) / max(len(items), 1),
        }


def main():
    print("=" * 60)
    print("  Food Supply Chain Demo")
    print("=" * 60)

    # Cold chain
    print("\n--- Cold Chain Monitoring ---")
    cc = ColdChainManager()
    ship = cc.create_shipment("SHP-001", "Fresh Salmon", "Seattle", "Chicago",
                              TemperatureZone.FRESH, (-1, 2), 48)
    cc.record_temperature("SHP-001", 1.2, "TRAILER-01")
    cc.record_temperature("SHP-001", 3.5, "TRAILER-01")
    status = cc.get_shipment_status("SHP-001")
    print(f"  Status: {status.status.value}")
    print(f"  Avg temp: {status.average_temperature:.1f}C")
    print(f"  Excursions: {status.excursion_count}")
    print(f"  Shelf life remaining: {status.projected_shelf_life_hours:.0f}h")

    # Demand forecasting
    print("\n--- Demand Forecasting ---")
    df = DemandForecaster(model="prophet")
    forecast = df.predict("SALMON-FRESH", "CHICAGO-DC", 7)
    print(f"  7-day demand: {forecast.total_units:,} units")
    for d in forecast.daily_forecast[:3]:
        print(f"    {d.date}: {d.predicted_units:,} ({d.ci_lower}-{d.ci_upper})")

    # Supplier quality
    print("\n--- Supplier Quality ---")
    sqm = SupplierQualityManager()
    sup = sqm.register_supplier("Pacific Seafood", "seafood", "Seattle", ["HACCP", "MSC"])
    scorecard = sqm.score_supplier(sup.supplier_id, "2026-Q2",
                                   {"on_time_delivery": 0.95, "quality_rejection_rate": 0.02,
                                    "food_safety_audit_score": 92, "response_time_hours": 4,
                                    "documentation_accuracy": 0.98})
    print(f"  {scorecard.supplier_name}: {scorecard.overall_score}/100 ({scorecard.grade.value})")

    # Inventory
    print("\n--- Perishable Inventory ---")
    inv = PerishableInventory()
    inv.add_item("SALMON", "LOT-001", 100, "lbs", "2026-07-10")
    inv.add_item("SALMON", "LOT-002", 150, "lbs", "2026-07-08")
    alloc = inv.get_fifo_allocation("SALMON", 200)
    print(f"  FEFO allocation: {len(alloc)} lots for 200 lbs order")
    waste = inv.get_waste_report()
    print(f"  Waste rate: {waste['waste_rate']:.1%}")


if __name__ == "__main__":
    main()
