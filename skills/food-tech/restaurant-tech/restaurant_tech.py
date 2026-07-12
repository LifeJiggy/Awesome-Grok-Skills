"""
Restaurant Technology Module
Part of the food-tech skill domain

Provides POS integration, menu engineering, online ordering,
reservation management, and performance analytics for restaurants.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid


class OrderSource(Enum):
    POS = "pos"
    WEBSITE = "website"
    MOBILE_APP = "mobile_app"
    AGGREGATOR = "aggregator"  # UberEats, DoorDash, etc.
    PHONE = "phone"


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProfitabilityQuadrant(Enum):
    STAR = "star"         # High profit, high popularity
    PLOWHORSE = "plowhorse"  # Low profit, high popularity
    PUZZLE = "puzzle"     # High profit, low popularity
    DOG = "dog"           # Low profit, low popularity


@dataclass
class MenuItem:
    item_id: str
    name: str
    price: float
    cost: float
    sold: int
    category: str
    profit_per_plate: float = 0.0
    popularity_score: float = 0.0
    profitability_quadrant: ProfitabilityQuadrant = ProfitabilityQuadrant.DOG

    def __post_init__(self):
        self.profit_per_plate = self.price - self.cost


@dataclass
class MenuAnalysis:
    items: List[MenuItem]
    total_revenue: float
    total_profit: float
    average_margin: float
    period_days: int


@dataclass
class OnlineOrder:
    order_id: str
    source: OrderSource
    items: List[Dict[str, Any]]
    customer: Dict[str, str]
    total: float
    status: OrderStatus
    delivery_zone: str = ""
    estimated_delivery_time: str = ""
    kitchen_ticket_id: str = ""
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TableConfig:
    table_id: str
    capacity: int
    zone: str
    status: str = "available"


@dataclass
class Reservation:
    reservation_id: str
    customer_name: str
    party_size: int
    date_time: str
    table_id: str
    confirmation_code: str
    preferences: Dict[str, str] = field(default_factory=dict)
    status: str = "confirmed"


@dataclass
class AvailabilityResult:
    available: bool
    tables: List[TableConfig]
    suggested_times: List[str]


@dataclass
class RealtimeMetrics:
    covers: int
    revenue: float
    average_check: float
    food_cost_pct: float
    labor_cost_pct: float
    table_turn_time: float
    online_order_count: int
    average_prep_time_minutes: float


class MenuEngine:
    """Data-driven menu optimization and analysis."""

    def __init__(self, analysis_period_days: int = 90,
                 cost_data_source: str = "recipe_costs"):
        self.period_days = analysis_period_days
        self.cost_source = cost_data_source

    def analyze_menu(self, menu_items: List[Dict[str, Any]]) -> MenuAnalysis:
        items = []
        total_sold = sum(m.get("sold", 0) for m in menu_items)
        avg_profit = 0

        for m in menu_items:
            profit = m["price"] - m["cost"]
            avg_profit += profit
            items.append(MenuItem(
                item_id=f"ITEM-{uuid.uuid4().hex[:6].upper()}",
                name=m["name"], price=m["price"], cost=m["cost"],
                sold=m["sold"], category=m.get("category", "other"),
                profit_per_plate=profit,
            ))

        avg_profit /= max(len(menu_items), 1)
        avg_popularity = total_sold / max(len(menu_items), 1)

        for item in items:
            item.popularity_score = item.sold / max(total_sold, 1)
            is_high_profit = item.profit_per_plate >= avg_profit
            is_high_pop = item.sold >= avg_popularity
            if is_high_profit and is_high_pop:
                item.profitability_quadrant = ProfitabilityQuadrant.STAR
            elif not is_high_profit and is_high_pop:
                item.profitability_quadrant = ProfitabilityQuadrant.PLOWHORSE
            elif is_high_profit and not is_high_pop:
                item.profitability_quadrant = ProfitabilityQuadrant.PUZZLE
            else:
                item.profitability_quadrant = ProfitabilityQuadrant.DOG

        total_rev = sum(m["price"] * m["sold"] for m in menu_items)
        total_profit = sum((m["price"] - m["cost"]) * m["sold"] for m in menu_items)

        return MenuAnalysis(
            items=items, total_revenue=total_rev,
            total_profit=total_profit,
            average_margin=total_profit / max(total_rev, 1),
            period_days=self.period_days,
        )


class OnlineOrdering:
    """Online ordering and delivery management."""

    def __init__(self, restaurant_id: str,
                 delivery_zones: Optional[List[Dict[str, Any]]] = None,
                 max_concurrent_orders: int = 25):
        self.restaurant_id = restaurant_id
        self.zones = delivery_zones or []
        self.max_orders = max_concurrent_orders
        self._orders: Dict[str, OnlineOrder] = {}

    def create_order(
        self, source: OrderSource, items: List[Dict[str, Any]],
        customer: Dict[str, str], delivery_zone: str = "",
    ) -> OnlineOrder:
        order_id = f"ORD-{uuid.uuid4().hex[:10].upper()}"
        total = sum(item.get("price", 15.0) * item.get("quantity", 1) for item in items)
        fee = next((z["delivery_fee"] for z in self.zones if z["name"] == delivery_zone), 0)
        total += fee

        order = OnlineOrder(
            order_id=order_id, source=source, items=items,
            customer=customer, total=round(total, 2),
            status=OrderStatus.CONFIRMED,
            delivery_zone=delivery_zone,
            estimated_delivery_time=(datetime.now() + timedelta(minutes=35)).strftime("%H:%M"),
            kitchen_ticket_id=f"TKT-{uuid.uuid4().hex[:6].upper()}",
        )
        self._orders[order_id] = order
        return order

    def update_status(self, order_id: str, status: OrderStatus) -> OnlineOrder:
        if order_id not in self._orders:
            raise ValueError(f"Order {order_id} not found")
        self._orders[order_id].status = status
        return self._orders[order_id]

    def get_active_orders(self) -> List[OnlineOrder]:
        active = {OrderStatus.PENDING, OrderStatus.CONFIRMED,
                  OrderStatus.PREPARING, OrderStatus.READY}
        return [o for o in self._orders.values() if o.status in active]


class ReservationSystem:
    """Restaurant reservation and table management."""

    def __init__(self, tables: Optional[List[TableConfig]] = None,
                 reservation_duration_minutes: int = 90,
                 no_show_timeout_minutes: int = 15):
        self.tables = {t.table_id: t for t in (tables or [])}
        self.duration = reservation_duration_minutes
        self.no_show_timeout = no_show_timeout_minutes
        self._reservations: Dict[str, Reservation] = {}

    def check_availability(self, party_size: int, date_time: str) -> AvailabilityResult:
        available = [t for t in self.tables.values()
                     if t.capacity >= party_size and t.status == "available"]
        return AvailabilityResult(
            available=len(available) > 0, tables=available,
            suggested_times=["18:00", "18:30", "19:00", "19:30", "20:00"],
        )

    def reserve(self, customer_name: str, party_size: int,
                date_time: str, preferences: Optional[Dict[str, str]] = None) -> Reservation:
        avail = self.check_availability(party_size, date_time)
        if not avail.available:
            raise ValueError("No tables available")

        table = min(avail.tables, key=lambda t: t.capacity)
        res_id = f"RES-{uuid.uuid4().hex[:8].upper()}"
        code = f"{uuid.uuid4().hex[:6].upper()}"

        reservation = Reservation(
            reservation_id=res_id, customer_name=customer_name,
            party_size=party_size, date_time=date_time,
            table_id=table.table_id, confirmation_code=code,
            preferences=preferences or {},
        )
        self._reservations[res_id] = reservation
        table.status = "reserved"
        return reservation

    def get_reservations(self, date: str = "") -> List[Reservation]:
        return list(self._reservations.values())


class PerformanceDashboard:
    """Real-time restaurant performance metrics."""

    def __init__(self, restaurant_id: str):
        self.restaurant_id = restaurant_id

    def get_realtime_metrics(self) -> RealtimeMetrics:
        return RealtimeMetrics(
            covers=187,
            revenue=8450.00,
            average_check=45.19,
            food_cost_pct=0.31,
            labor_cost_pct=0.28,
            table_turn_time=52.0,
            online_order_count=45,
            average_prep_time_minutes=18.5,
        )

    def get_hourly_breakdown(self) -> List[Dict[str, Any]]:
        return [
            {"hour": h, "covers": c, "revenue": r}
            for h, c, r in [("11:00", 35, 1500), ("12:00", 65, 3200),
                             ("13:00", 45, 2100), ("18:00", 20, 900)]
        ]


def main():
    print("=" * 60)
    print("  Restaurant Technology Demo")
    print("=" * 60)

    # Menu engineering
    print("\n--- Menu Engineering ---")
    engine = MenuEngine()
    analysis = engine.analyze_menu([
        {"name": "Grilled Salmon", "price": 28, "cost": 8.40, "sold": 1200, "category": "entree"},
        {"name": "Caesar Salad", "price": 14, "cost": 3.50, "sold": 1800, "category": "starter"},
        {"name": "Filet Mignon", "price": 42, "cost": 16.80, "sold": 600, "category": "entree"},
        {"name": "Pasta Carbonara", "price": 18, "cost": 4.50, "sold": 950, "category": "entree"},
    ])
    for item in analysis.items:
        print(f"  {item.name}: {item.profitability_quadrant.value} "
              f"(profit=${item.profit_per_plate:.2f})")
    print(f"  Revenue: ${analysis.total_revenue:,.0f}, Margin: {analysis.average_margin:.1%}")

    # Online ordering
    print("\n--- Online Ordering ---")
    ordering = OnlineOrdering("REST-001", [{"name": "Zone A", "delivery_fee": 3.99}])
    order = ordering.create_order(
        OrderSource.WEBSITE,
        [{"item_id": "SALMON", "quantity": 2, "price": 28}],
        {"name": "Jane D.", "phone": "555-0123"},
        "Zone A",
    )
    print(f"  Order: {order.order_id}, Total: ${order.total:.2f}")
    print(f"  Ticket: {order.kitchen_ticket_id}")

    # Reservations
    print("\n--- Reservation System ---")
    rs = ReservationSystem(tables=[
        TableConfig("T1", 2, "patio"), TableConfig("T2", 4, "main"),
        TableConfig("T3", 6, "private"),
    ])
    res = rs.reserve("John Smith", 4, "2026-07-15 19:00", {"occasion": "birthday"})
    print(f"  Reservation: {res.reservation_id}")
    print(f"  Table: {res.table_id}, Code: {res.confirmation_code}")

    # Dashboard
    print("\n--- Performance Dashboard ---")
    dash = PerformanceDashboard("REST-001")
    m = dash.get_realtime_metrics()
    print(f"  Covers: {m.covers}, Revenue: ${m.revenue:,.0f}")
    print(f"  Avg Check: ${m.average_check:.2f}, Food Cost: {m.food_cost_pct:.1%}")


if __name__ == "__main__":
    main()
