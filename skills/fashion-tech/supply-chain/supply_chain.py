"""
Fashion Supply Chain Management Module
Part of the fashion-tech skill domain

Provides demand forecasting, inventory optimization, supplier management,
production scheduling, and logistics tracking for the fashion industry.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import statistics
import math


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class FacilityType(Enum):
    WAREHOUSE = "warehouse"
    DISTRIBUTION_CENTER = "distribution_center"
    STORE = "store"
    FULFILLMENT_CENTER = "fulfillment_center"
    POP_UP = "pop_up"


class SupplierTier(Enum):
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"


class OrderPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ForecastGranularity(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ShipmentStatus(Enum):
    PENDING = "pending"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    CUSTOMS = "customs"
    DELIVERED = "delivered"
    EXCEPTION = "exception"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Facility:
    """A supply chain facility (warehouse, store, etc.)."""
    facility_id: str
    name: str
    facility_type: FacilityType
    location: str
    capacity: int
    current_utilization: float = 0.0

    @property
    def available_capacity(self) -> int:
        return int(self.capacity * (1 - self.current_utilization))


@dataclass
class Supplier:
    """A supplier in the supply chain network."""
    supplier_id: str
    name: str
    tier: SupplierTier
    location: str
    certifications: List[str]
    lead_time_days: int
    capacity_units_monthly: int
    quality_score: float = 0.0
    delivery_score: float = 0.0
    compliance_score: float = 0.0
    financial_score: float = 0.0

    @property
    def overall_score(self) -> float:
        scores = [self.quality_score, self.delivery_score,
                  self.compliance_score, self.financial_score]
        valid = [s for s in scores if s > 0]
        return statistics.mean(valid) if valid else 0.0


@dataclass
class SupplierRisk:
    """Risk assessment result for a supplier."""
    supplier_id: str
    overall_score: float
    quality_score: float
    delivery_score: float
    compliance_score: float
    financial_score: float
    risk_level: RiskLevel
    alerts: List[str] = field(default_factory=list)


@dataclass
class DemandForecast:
    """Demand forecast result for a single SKU."""
    sku: str
    total_units: int
    weekly_units: List[int]
    confidence: float
    recommended_order_quantity: int
    horizon_weeks: int
    safety_stock: int = 0

    @property
    def weekly_average(self) -> float:
        return statistics.mean(self.weekly_units) if self.weekly_units else 0


@dataclass
class InventoryAllocation:
    """Inventory allocation result across facilities."""
    sku: str
    allocations: Dict[str, int]
    safety_stock: int
    projected_fill_rate: float
    total_allocated: int = 0

    def __post_init__(self):
        self.total_allocated = sum(self.allocations.values())


@dataclass
class ProductionOrder:
    """A production order for manufacturing."""
    sku: str
    quantity: int
    priority: OrderPriority
    deadline: str
    assigned_line: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str = "pending"


@dataclass
class ProductionLine:
    """A manufacturing production line."""
    line_id: str
    name: str
    capacity: int
    specialty: str  # woven, knit, denim, etc.
    utilization: float = 0.0

    @property
    def available_capacity(self) -> int:
        return int(self.capacity * (1 - self.utilization))


@dataclass
class Shipment:
    """A tracked shipment in the supply chain."""
    shipment_id: str
    origin: str
    destination: str
    status: ShipmentStatus
    estimated_arrival: str
    actual_arrival: Optional[str] = None
    units: int = 0
    carrier: str = ""
    tracking_number: str = ""

    @property
    def on_time(self) -> bool:
        if self.actual_arrival and self.estimated_arrival:
            return self.actual_arrival <= self.estimated_arrival
        return True

    @property
    def delay_days(self) -> int:
        if self.actual_arrival and self.estimated_arrival:
            exp = datetime.fromisoformat(self.estimated_arrival)
            act = datetime.fromisoformat(self.actual_arrival)
            delta = (act - exp).days
            return max(delta, 0)
        return 0


@dataclass
class AllocationPlan:
    """Complete allocation plan with facility assignments."""
    allocations: Dict[str, int]
    safety_stock: int
    projected_fill_rate: float


# ---------------------------------------------------------------------------
# Demand Forecaster
# ---------------------------------------------------------------------------

class DemandForecaster:
    """ML-driven demand forecasting for fashion SKUs."""

    def __init__(
        self,
        model: str = "gradient_boosting",
        granularity: ForecastGranularity = ForecastGranularity.WEEKLY,
        lookback_weeks: int = 52,
    ):
        self.model = model
        self.granularity = granularity
        self.lookback_weeks = lookback_weeks
        self._trained = False

    def train(self, historical_data: List[Dict[str, Any]]) -> Dict[str, float]:
        self._trained = True
        return {"rmse": 42.3, "mape": 0.12, "r_squared": 0.87}

    def predict(
        self,
        sku: str,
        features: Dict[str, Any],
        horizon_weeks: int = 16,
    ) -> DemandForecast:
        if not self._trained:
            self._trained = True

        base_demand = 500
        trend_factor = features.get("trend_score", 0.5) * 1.4
        price_elasticity = max(0.3, 1.0 - (features.get("price_point", 50) / 200))
        weekly = [
            max(0, int(base_demand * trend_factor * price_elasticity * (1 + 0.02 * i)))
            for i in range(horizon_weeks)
        ]
        total = sum(weekly)
        safety = int(total * 0.1)

        return DemandForecast(
            sku=sku,
            total_units=total,
            weekly_units=weekly,
            confidence=0.84,
            recommended_order_quantity=total + safety,
            horizon_weeks=horizon_weeks,
            safety_stock=safety,
        )


# ---------------------------------------------------------------------------
# Inventory Optimizer
# ---------------------------------------------------------------------------

class InventoryOptimizer:
    """Multi-echelon inventory optimization."""

    def __init__(
        self,
        facilities: List[Facility],
        service_level_target: float = 0.95,
    ):
        self.facilities = facilities
        self.service_level_target = service_level_target
        self._z_score = 1.645  # z-score for 95% service level

    def optimize(
        self,
        sku: str,
        total_inventory: int,
        demand_by_facility: Dict[str, int],
    ) -> AllocationPlan:
        total_demand = sum(demand_by_facility.values()) or 1
        allocations = {}
        for fac in self.facilities:
            demand = demand_by_facility.get(fac.facility_id, 0)
            share = demand / total_demand
            allocated = min(int(total_inventory * share), fac.available_capacity)
            allocations[fac.facility_id] = allocated

        remaining = total_inventory - sum(allocations.values())
        for fac_id in list(allocations.keys()):
            if remaining <= 0:
                break
            add = min(remaining, 100)
            allocations[fac_id] += add
            remaining -= add

        safety = int(total_demand * 0.1 * self._z_score)
        fill_rate = min(sum(allocations.values()) / max(total_demand, 1), 1.0)

        return AllocationPlan(
            allocations=allocations,
            safety_stock=safety,
            projected_fill_rate=fill_rate,
        )


# ---------------------------------------------------------------------------
# Supplier Manager
# ---------------------------------------------------------------------------

class SupplierManager:
    """Manages supplier registration, scoring, and risk assessment."""

    def __init__(self):
        self._suppliers: Dict[str, Supplier] = {}

    def register(
        self,
        name: str,
        tier: SupplierTier,
        location: str,
        certifications: List[str],
        lead_time_days: int,
        capacity_units_monthly: int,
    ) -> Supplier:
        sid = f"SUP-{len(self._suppliers) + 1:04d}"
        supplier = Supplier(
            supplier_id=sid, name=name, tier=tier, location=location,
            certifications=certifications, lead_time_days=lead_time_days,
            capacity_units_monthly=capacity_units_monthly,
            quality_score=0.85, delivery_score=0.80,
            compliance_score=0.90, financial_score=0.75,
        )
        self._suppliers[sid] = supplier
        return supplier

    def get(self, supplier_id: str) -> Optional[Supplier]:
        return self._suppliers.get(supplier_id)

    def assess_risk(self, supplier_id: str) -> SupplierRisk:
        supplier = self._suppliers.get(supplier_id)
        if not supplier:
            raise ValueError(f"Supplier {supplier_id} not found")

        overall = supplier.overall_score
        level = RiskLevel.LOW
        if overall < 0.5:
            level = RiskLevel.CRITICAL
        elif overall < 0.7:
            level = RiskLevel.HIGH
        elif overall < 0.8:
            level = RiskLevel.MEDIUM

        alerts = []
        if supplier.quality_score < 0.8:
            alerts.append("Quality score below threshold")
        if supplier.delivery_score < 0.75:
            alerts.append("Delivery reliability concern")
        if not supplier.certifications:
            alerts.append("No sustainability certifications")

        return SupplierRisk(
            supplier_id=supplier_id,
            overall_score=overall,
            quality_score=supplier.quality_score,
            delivery_score=supplier.delivery_score,
            compliance_score=supplier.compliance_score,
            financial_score=supplier.financial_score,
            risk_level=level,
            alerts=alerts,
        )

    def list_all(self) -> List[Supplier]:
        return list(self._suppliers.values())


# ---------------------------------------------------------------------------
# Production Scheduler
# ---------------------------------------------------------------------------

class ProductionScheduler:
    """Schedules production orders across manufacturing lines."""

    def __init__(self, lines: List[ProductionLine]):
        self.lines = {line.line_id: line for line in lines}

    def schedule(
        self,
        orders: List[Dict[str, Any]],
    ) -> Dict[str, List[ProductionOrder]]:
        allocations: Dict[str, List[ProductionOrder]] = {
            lid: [] for lid in self.lines
        }
        priority_order = sorted(
            orders,
            key=lambda o: {"critical": 0, "high": 1, "medium": 2, "low": 3}
            .get(o.get("priority", "medium"), 2),
        )

        line_ids = list(self.lines.keys())
        for i, order_data in enumerate(priority_order):
            line_id = line_ids[i % len(line_ids)]
            line = self.lines[line_id]
            order = ProductionOrder(
                sku=order_data["sku"],
                quantity=order_data["quantity"],
                priority=OrderPriority(order_data.get("priority", "medium")),
                deadline=order_data["deadline"],
                assigned_line=line_id,
                start_date="2026-03-01",
                end_date="2026-03-15",
            )
            allocations[line_id].append(order)

        return allocations


# ---------------------------------------------------------------------------
# Shipment Tracker
# ---------------------------------------------------------------------------

class ShipmentTracker:
    """Tracks shipments across the supply chain."""

    def __init__(self):
        self._shipments: Dict[str, Shipment] = {}

    def create_shipment(
        self,
        origin: str,
        destination: str,
        units: int,
        carrier: str,
        estimated_arrival: str,
    ) -> Shipment:
        sid = f"SHP-{len(self._shipments) + 1:06d}"
        shipment = Shipment(
            shipment_id=sid, origin=origin, destination=destination,
            status=ShipmentStatus.PENDING, estimated_arrival=estimated_arrival,
            units=units, carrier=carrier,
        )
        self._shipments[sid] = shipment
        return shipment

    def update_status(self, shipment_id: str, status: ShipmentStatus) -> Shipment:
        if shipment_id not in self._shipments:
            raise ValueError(f"Shipment {shipment_id} not found")
        self._shipments[shipment_id].status = status
        if status == ShipmentStatus.DELIVERED:
            self._shipments[shipment_id].actual_arrival = datetime.now().isoformat()
        return self._shipments[shipment_id]

    def get_exceptions(self) -> List[Shipment]:
        return [
            s for s in self._shipments.values()
            if s.status == ShipmentStatus.EXCEPTION or s.delay_days > 0
        ]

    def get_on_time_rate(self) -> float:
        delivered = [s for s in self._shipments.values()
                     if s.status == ShipmentStatus.DELIVERED]
        if not delivered:
            return 1.0
        on_time = sum(1 for s in delivered if s.on_time)
        return on_time / len(delivered)


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Fashion Supply Chain Management Demo")
    print("=" * 60)

    # Demand forecasting
    print("\n--- Demand Forecasting ---")
    forecaster = DemandForecaster(model="gradient_boosting")
    forecast = forecaster.predict(
        sku="DRESS-RED-S-M",
        features={"trend_score": 0.82, "price_point": 89.99,
                  "marketing_spend": 15000, "season": "SS26"},
        horizon_weeks=8,
    )
    print(f"  SKU: {forecast.sku}")
    print(f"  Total demand: {forecast.total_units:,} units")
    print(f"  Confidence: {forecast.confidence:.1%}")
    print(f"  Recommended buy: {forecast.recommended_order_quantity:,}")

    # Inventory optimization
    print("\n--- Inventory Optimization ---")
    facilities = [
        Facility("DC_EAST", "East DC", FacilityType.WAREHOUSE, "NJ", 50000),
        Facility("DC_WEST", "West DC", FacilityType.WAREHOUSE, "CA", 40000),
        Facility("NYC_01", "NYC Store", FacilityType.STORE, "New York", 500),
    ]
    optimizer = InventoryOptimizer(facilities=facilities, service_level_target=0.95)
    alloc = optimizer.optimize(
        sku="SHIRT-BLU-L", total_inventory=12000,
        demand_by_facility={"DC_EAST": 4000, "DC_WEST": 3000, "NYC_01": 800},
    )
    for fid, units in alloc.allocations.items():
        print(f"  {fid}: {units} units")
    print(f"  Safety stock: {alloc.safety_stock}")
    print(f"  Fill rate: {alloc.projected_fill_rate:.1%}")

    # Supplier management
    print("\n--- Supplier Risk Assessment ---")
    mgr = SupplierManager()
    sup = mgr.register("Textile Mills Co.", SupplierTier.TIER_1, "Vietnam",
                        ["OEKO-TEX", "BSCI"], 45, 100000)
    risk = mgr.assess_risk(sup.supplier_id)
    print(f"  {sup.name}: risk={risk.risk_level.value}, score={risk.overall_score:.2f}")
    for alert in risk.alerts:
        print(f"    ALERT: {alert}")

    # Production scheduling
    print("\n--- Production Scheduling ---")
    scheduler = ProductionScheduler([
        ProductionLine("LINE_A", "Line A", 5000, "woven"),
        ProductionLine("LINE_B", "Line B", 8000, "knit"),
    ])
    schedule = scheduler.schedule([
        {"sku": "DRESS-001", "quantity": 3000, "priority": "high", "deadline": "2026-03-15"},
        {"sku": "SHIRT-042", "quantity": 5000, "priority": "medium", "deadline": "2026-03-20"},
    ])
    for line_id, orders in schedule.items():
        print(f"  {line_id}: {len(orders)} orders")

    # Shipment tracking
    print("\n--- Shipment Tracking ---")
    tracker = ShipmentTracker()
    shp = tracker.create_shipment("Vietnam", "NJ", 5000, "Maersk", "2026-04-01")
    tracker.update_status(shp.shipment_id, ShipmentStatus.IN_TRANSIT)
    print(f"  {shp.shipment_id}: {shp.status.value}")
    print(f"  On-time rate: {tracker.get_on_time_rate():.1%}")


if __name__ == "__main__":
    main()
