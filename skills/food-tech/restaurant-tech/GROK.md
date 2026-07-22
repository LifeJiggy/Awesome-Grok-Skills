---
name: "restaurant-tech"
category: "food-tech"
version: "2.0.0"
tags: ["food-tech", "restaurant-tech", "pos", "menu-engineering", "kitchen-management", "food-service"]
difficulty: "intermediate"
estimated_time: "35-50 minutes"
prerequisites: ["python", "restaurant-operations"]
---

# Restaurant Technology

## Overview

Restaurant technology encompasses the software systems powering modern food service operations: point-of-sale (POS) systems, kitchen display systems (KDS), menu engineering, online ordering, reservation management, inventory control, staff scheduling, and customer relationship management. This module provides a comprehensive framework for digitizing restaurant operations to improve efficiency, reduce waste, and enhance customer experience.

## Core Capabilities

- **POS Integration**: Modern cloud POS with order management, payment processing, split bills, and multi-location support
- **Menu Engineering**: Data-driven menu optimization using profitability matrix (profit vs popularity) and item performance analytics
- **Kitchen Display Systems**: Real-time order routing, preparation timing, and kitchen workflow optimization
- **Online Ordering**: Direct ordering platform with delivery zone management, order throttling, and integration with third-party aggregators
- **Reservation Management**: Table allocation, waitlist management, no-show prediction, and reservation-based CRM
- **Inventory Control**: Real-time ingredient tracking, par level management, waste logging, and automated purchasing suggestions
- **Staff Scheduling**: Labor cost optimization with demand-based scheduling, shift swapping, and overtime alerts
- **Customer Analytics**: Visit frequency, average check, menu preferences, and loyalty program management
- **Performance Dashboards**: Real-time KPIs including covers, average check, food cost %, labor cost %, and table turn time
- **Multi-Location Management**: Centralized reporting, menu management, and operational control across restaurant groups

## Usage Examples

### Menu Engineering Analysis

```python
from food_tech.restaurant_tech import MenuEngine, MenuCategory

engine = MenuEngine(
    analysis_period_days=90,
    cost_data_source="recipe_costs",
)

# Analyze menu performance
analysis = engine.analyze_menu(
    menu_items=[
        {"name": "Grilled Salmon", "price": 28.00, "cost": 8.40, "sold": 1200, "category": "entree"},
        {"name": "Caesar Salad", "price": 14.00, "cost": 3.50, "sold": 1800, "category": "starter"},
        {"name": "Filet Mignon", "price": 42.00, "cost": 16.80, "sold": 600, "category": "entree"},
        {"name": "Pasta Carbonara", "price": 18.00, "cost": 4.50, "sold": 950, "category": "entree"},
    ],
)

for item in analysis.items:
    quadrant = item.profitability_quadrant
    print(f"  {item.name}: {quadrant} "
          f"(profit=${item.profit_per_plate:.2f}, popularity={item.popularity_score:.0%})")
    if quadrant == "star":
        print(f"    -> Promote heavily, maintain quality")
    elif quadrant == "plowhorse":
        print(f"    -> Increase price or reduce cost")
    elif quadrant == "puzzle":
        print(f"    -> Improve marketing visibility")
    elif quadrant == "dog":
        print(f"    -> Consider removing from menu")
```

### Online Order Management

```python
from food_tech.restaurant_tech import OnlineOrdering, OrderSource

ordering = OnlineOrdering(
    restaurant_id="REST-001",
    delivery_zones=[
        {"name": "Zone A", "radius_km": 3, "delivery_fee": 3.99},
        {"name": "Zone B", "radius_km": 5, "delivery_fee": 5.99},
    ],
    max_concurrent_orders=25,
)

# Process incoming order
order = ordering.create_order(
    source=OrderSource.WEBSITE,
    items=[
        {"item_id": "SALMON", "quantity": 2, "customizations": {"side": "quinoa"}},
        {"item_id": "CAESAR", "quantity": 1, "customizations": {"dressing": "on_side"}},
    ],
    customer={"name": "Jane D.", "phone": "555-0123", "address": "123 Main St"},
    delivery_zone="Zone A",
)

print(f"Order: {order.order_id}")
print(f"Total: ${order.total:.2f}")
print(f"Est. delivery: {order.estimated_delivery_time}")
print(f"Kitchen ticket: {order.kitchen_ticket_id}")
```

### Reservation & Table Management

```python
from food_tech.restaurant_tech import ReservationSystem, TableConfig

system = ReservationSystem(
    tables=[
        TableConfig("T1", capacity=2, zone="patio"),
        TableConfig("T2", capacity=4, zone="main"),
        TableConfig("T3", capacity=4, zone="main"),
        TableConfig("T4", capacity=6, zone="private"),
        TableConfig("T5", capacity=8, zone="private"),
    ],
    reservation_duration_minutes=90,
    no_show_timeout_minutes=15,
)

# Make reservation
reservation = system.reserve(
    customer_name="John Smith",
    party_size=4,
    date_time="2026-07-15 19:00",
    preferences={"zone": "main", "occasion": "birthday"},
)

print(f"Reservation: {reservation.reservation_id}")
print(f"Table: {reservation.table_id}")
print(f"Confirmation: {reservation.confirmation_code}")

# Check availability
availability = system.check_availability(
    party_size=2, date_time="2026-07-15 20:00",
)
print(f"Tables available: {len(availability.tables)}")
```

### Performance Dashboard

```python
from food_tech.restaurant_tech import PerformanceDashboard

dashboard = PerformanceDashboard(restaurant_id="REST-001")

# Get real-time metrics
metrics = dashboard.get_realtime_metrics()
print(f"Today's Performance:")
print(f"  Covers: {metrics.covers}")
print(f"  Revenue: ${metrics.revenue:,.2f}")
print(f"  Avg Check: ${metrics.average_check:.2f}")
print(f"  Food Cost: {metrics.food_cost_pct:.1%}")
print(f"  Labor Cost: {metrics.labor_cost_pct:.1%}")
print(f"  Table Turn: {metrics.table_turn_time:.1f} min")
```

## Best Practices

- Use menu engineering quarterly analysis to keep the menu optimized; rotate seasonal items strategically
- Track food cost percentage by item, not just overall, to identify items dragging down margins
- Implement recipe-level costing with actual supplier prices updated monthly for accurate margins
- Use demand forecasting to schedule labor; understaffing during rush hurts service more than overstaffing costs
- Monitor online order throttling during peak hours to maintain kitchen capacity and food quality
- Track no-show rates and implement cancellation policies for high-demand time slots
- Log all waste with reason codes (overproduction, spoilage, mistake) for actionable waste reduction
- Train staff on upselling and suggestive selling techniques; track server-level revenue per cover
- Integrate POS, KDS, and inventory for real-time food cost tracking, not just end-of-month reconciliation
- Maintain separate dashboards for FOH (front of house) and BOH (back of house) operations

## Related Modules

- `food-tech/food-safety` - Kitchen food safety and temperature compliance
- `food-tech/nutrition-analysis` - Menu nutrition labeling and allergen management
- `food-tech/supply-chain` - Restaurant procurement and supplier management

## Advanced Configuration

### POS System Configuration

```yaml
pos_system:
  restaurant_id: "REST-001"
  restaurant_name: "Bistro Excellence"
  locations:
    - id: "LOC-001"
      name: "Main Street"
      address: "123 Main Street, Downtown"
      timezone: "America/New_York"
      operating_hours:
        monday: { open: "11:00", close: "22:00" }
        tuesday: { open: "11:00", close: "22:00" }
        wednesday: { open: "11:00", close: "22:00" }
        thursday: { open: "11:00", close: "23:00" }
        friday: { open: "11:00", close: "23:00" }
        saturday: { open: "10:00", close: "23:00" }
        sunday: { open: "10:00", close: "21:00" }
        
  payment_methods:
    - type: "credit_card"
      processors: ["stripe", "square"]
      enabled: true
    - type: "cash"
      enabled: true
    - type: "mobile_pay"
      providers: ["apple_pay", "google_pay"]
      enabled: true
    - type: "gift_card"
      enabled: true
      
  tax_rates:
    - name: "State Tax"
      rate: 0.0625
      applies_to: ["all"]
    - name: "Local Tax"
      rate: 0.02
      applies_to: ["all"]
    - name: "Alcohol Tax"
      rate: 0.08
      applies_to: ["alcohol"]
```

### Menu Engineering Configuration

```yaml
menu_engineering:
  analysis_period_days: 90
  cost_data_source: "recipe_costs"
  
  profitability_matrix:
    high_profit_threshold: 0.65  # 65% margin
    high_popularity_threshold: 0.15  # 15% of sales
    
  categories:
    - name: "starters"
      display_order: 1
      description: "Appetizers and small plates"
      
    - name: "entrees"
      display_order: 2
      description: "Main courses"
      
    - name: "desserts"
      display_order: 3
      description: "Sweet endings"
      
    - name: "beverages"
      display_order: 4
      description: "Drinks and cocktails"
      
  modifiers:
    - name: "protein_upgrade"
      type: "choice"
      options:
        - name: "Standard"
          price_adjustment: 0
        - name: "Premium Cut"
          price_adjustment: 8.00
        - name: "Double Portion"
          price_adjustment: 12.00
          
    - name: "side_substitution"
      type: "choice"
      options:
        - name: "French Fries"
          price_adjustment: 0
        - name: "Sweet Potato Fries"
          price_adjustment: 2.00
        - name: "Garden Salad"
          price_adjustment: 1.50
```

### Kitchen Display System Configuration

```yaml
kitchen_display:
  stations:
    - id: "GRILL"
      name: "Grill Station"
      printers: ["KITCHEN-GRILL-01"]
      auto_fire_items: true
      timeout_minutes: 15
      
    - id: "SAUTE"
      name: "Sauté Station"
      printers: ["KITCHEN-SAUTE-01"]
      auto_fire_items: true
      timeout_minutes: 12
      
    - id: "GARDE"
      name: "Garde Manger"
      printers: ["KITCHEN-GARDE-01"]
      auto_fire_items: false
      timeout_minutes: 8
      
    - id: "PASTRY"
      name: "Pastry Station"
      printers: ["KITCHEN-PASTRY-01"]
      auto_fire_items: false
      timeout_minutes: 20
      
  routing_rules:
    - category: "steak"
      station: "GRILL"
      priority: "high"
      
    - category: "pasta"
      station: "SAUTE"
      priority: "normal"
      
    - category: "salad"
      station: "GARDE"
      priority: "normal"
      
    - category: "dessert"
      station: "PASTRY"
      priority: "normal"
      
  alerts:
    order_aging_threshold_minutes: 10
    expediting_threshold_minutes: 5
    notification_channels: ["display", "buzzer"]
```

### Online Ordering Configuration

```yaml
online_ordering:
  enabled: true
  channels:
    - type: "website"
      url: "https://bistroexcellence.com/order"
      commission_pct: 0
      
    - type: "mobile_app"
      platforms: ["ios", "android"]
      commission_pct: 0
      
    - type: "third_party"
      platforms:
        - name: "doordash"
          commission_pct: 25
        - name: "ubereats"
          commission_pct: 30
        - name: "grubhub"
          commission_pct: 27
          
  delivery_zones:
    - name: "Zone A"
      radius_km: 3
      delivery_fee: 3.99
      minimum_order: 20.00
      
    - name: "Zone B"
      radius_km: 5
      delivery_fee: 5.99
      minimum_order: 30.00
      
  order_throttling:
    max_concurrent_orders: 25
    throttle_threshold_pct: 80
    surge_multiplier: 1.5
    estimated_prep_time_minutes: 20
```

## Architecture Patterns

### Event-Driven Restaurant Operations

```python
class RestaurantEventProcessor:
    def __init__(self, event_store, notification_service):
        self.event_store = event_store
        self.notifier = notification_service
    
    async def process_event(self, event: RestaurantEvent):
        # Store event
        await self.event_store.store(event)
        
        # Route to appropriate handlers
        handlers = {
            "order_placed": self.handle_order_placed,
            "order_ready": self.handle_order_ready,
            "reservation_made": self.handle_reservation_made,
            "payment_processed": self.handle_payment_processed,
        }
        
        handler = handlers.get(event.event_type)
        if handler:
            await handler(event)
    
    async def handle_order_placed(self, event: OrderEvent):
        # Notify kitchen
        await self.notifier.notify_kitchen(event.order)
        
        # Update inventory
        await self.update_inventory(event.order)
        
        # Track metrics
        await self.track_metrics(event.order)
```

### Menu Optimization Algorithm

```python
class MenuOptimizationAlgorithm:
    def __init__(self, sales_data, cost_data):
        self.sales = sales_data
        self.costs = cost_data
    
    async def optimize_menu(self, menu_items: List[MenuItem]) -> MenuOptimization:
        # Calculate profitability metrics
        for item in menu_items:
            item.profit_margin = await self.calculate_profit_margin(item)
            item.popularity_score = await self.calculate_popularity(item)
        
        # Classify items into quadrants
        classified = self.classify_items(menu_items)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(classified)
        
        return MenuOptimization(
            items=classified,
            recommendations=recommendations,
            projected_impact=self.calculate_impact(recommendations),
        )
```

### Kitchen Workflow Management

```python
class KitchenWorkflowManager:
    def __init__(self, station_registry, timer_service):
        self.stations = station_registry
        self.timers = timer_service
    
    async def route_order(self, order: Order) -> KitchenTicket:
        # Create kitchen ticket
        ticket = KitchenTicket(
            order_id=order.id,
            items=[],
            created_at=datetime.utcnow(),
        )
        
        # Route items to stations
        for item in order.items:
            station = await self.find_station(item)
            ticket.items.append(TicketItem(
                item=item,
                station=station.id,
                priority=item.priority,
                estimated_time=item.prep_time,
            ))
        
        # Start timers
        await self.timers.start_ticket(ticket)
        
        return ticket
    
    async def update_item_status(self, ticket_id: str, item_id: str, status: str):
        # Update item status
        await self.update_item(ticket_id, item_id, status)
        
        # Check if order is complete
        ticket = await self.get_ticket(ticket_id)
        if all(item.status == "ready" for item in ticket.items):
            await self.notify_order_ready(ticket)
```

### Reservation Optimization

```python
class ReservationOptimizer:
    def __init__(self, table_registry, predictive_model):
        self.tables = table_registry
        self.model = predictive_model
    
    async def optimize_seating(self, reservation: Reservation) -> SeatingRecommendation:
        # Get available tables
        available = await self.get_available_tables(
            reservation.party_size,
            reservation.date_time,
        )
        
        # Score each table
        scored_tables = []
        for table in available:
            score = await self.score_table(table, reservation)
            scored_tables.append((table, score))
        
        # Sort by score
        scored_tables.sort(key=lambda x: x[1], reverse=True)
        
        # Return best recommendation
        best_table, best_score = scored_tables[0]
        
        return SeatingRecommendation(
            table=best_table,
            score=best_score,
            alternatives=[t for t, s in scored_tables[1:4]],
        )
```

## Integration Guide

### POS System Integration

```python
class POSIntegration:
    def __init__(self, pos_api_url: str, api_key: str):
        self.api_url = pos_api_url
        self.api_key = api_key
    
    async def sync_menu(self, menu: Menu) -> SyncResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/menu/sync",
                headers=headers,
                json=menu.to_dict(),
            )
        
        return self.parse_sync_result(response.json())
    
    async def get_sales_data(self, date_range: Tuple[date, date]) -> SalesData:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        params = {
            "start_date": date_range[0].isoformat(),
            "end_date": date_range[1].isoformat(),
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/sales",
                headers=headers,
                params=params,
            )
        
        return self.parse_sales_data(response.json())
```

### Delivery Platform Integration

```python
class DeliveryPlatformIntegration:
    def __init__(self, platform: str, credentials: dict):
        self.platform = platform
        self.credentials = credentials
    
    async def receive_order(self, order_data: dict) -> Order:
        # Validate order
        validation = await self.validate_order(order_data)
        if not validation.is_valid:
            raise OrderValidationError(validation.errors)
        
        # Transform to internal format
        order = self.transform_order(order_data)
        
        # Send to kitchen
        await self.send_to_kitchen(order)
        
        return order
    
    async def update_order_status(self, order_id: str, status: str):
        # Update platform status
        await self.update_platform_status(order_id, status)
        
        # Notify customer
        await self.notify_customer(order_id, status)
```

### Reservation Platform Integration

```python
class ReservationPlatformIntegration:
    def __init__(self, platform: str, api_key: str):
        self.platform = platform
        self.api_key = api_key
    
    async def sync_reservations(self, date: date) -> SyncResult:
        # Get reservations from platform
        reservations = await self.fetch_reservations(date)
        
        # Sync to internal system
        synced = 0
        errors = []
        
        for reservation in reservations:
            try:
                await self.internal_system.sync_reservation(reservation)
                synced += 1
            except Exception as e:
                errors.append({"reservation_id": reservation.id, "error": str(e)})
        
        return SyncResult(synced=synced, errors=errors)
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_orders_restaurant_date ON orders (restaurant_id, created_at DESC);
CREATE INDEX idx_orders_status ON orders (status, created_at);
CREATE INDEX idx_menu_items_restaurant ON menu_items (restaurant_id, category);
CREATE INDEX idx_reservations_date_time ON reservations (date_time, party_size);

-- Create materialized view for daily sales
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT 
    restaurant_id,
    DATE(created_at) as sale_date,
    COUNT(*) as order_count,
    SUM(total) as revenue,
    AVG(total) as average_check
FROM orders
WHERE status = 'completed'
GROUP BY restaurant_id, DATE(created_at);
```

### Caching Strategy

```python
class RestaurantCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes
    
    async def get_menu(self, restaurant_id: str) -> Optional[Menu]:
        cache_key = f"menu:{restaurant_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return Menu.from_json(cached)
        return None
    
    async def cache_menu(self, restaurant_id: str, menu: Menu):
        cache_key = f"menu:{restaurant_id}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            menu.to_json()
        )
```

### Real-Time Updates

```python
class RealTimeUpdateService:
    def __init__(self, websocket_manager):
        self.ws_manager = websocket_manager
    
    async def broadcast_order_update(self, order: Order):
        # Notify kitchen
        await self.ws_manager.send_to_room(
            f"kitchen:{order.restaurant_id}",
            {"type": "order_update", "order": order.to_dict()}
        )
        
        # Notify servers
        await self.ws_manager.send_to_room(
            f"servers:{order.restaurant_id}",
            {"type": "order_update", "order": order.to_dict()}
        )
    
    async def broadcast_table_update(self, table: Table):
        await self.ws_manager.send_to_room(
            f"floor:{table.restaurant_id}",
            {"type": "table_update", "table": table.to_dict()}
        )
```

## Security Considerations

### Payment Security

```python
class PaymentSecurity:
    def __init__(self, pci_compliance_level: str):
        self.pci_level = pci_compliance_level
    
    def tokenize_card(self, card_number: str) -> str:
        """Tokenize card number for PCI compliance"""
        # Use payment processor's tokenization
        token = payment_processor.tokenize(card_number)
        return token
    
    def mask_card_number(self, card_number: str) -> str:
        """Mask card number for display"""
        return f"****-****-****-{card_number[-4:]}"
```

### Data Encryption

```python
from cryptography.fernet import Fernet

class RestaurantDataEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_customer_data(self, data: str) -> str:
        """Encrypt sensitive customer data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_customer_data(self, encrypted: str) -> str:
        """Decrypt sensitive customer data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class RestaurantAccessControl:
    def __init__(self):
        self.permissions = {}
        self.roles = {}
    
    def check_permission(self, user_id: str, action: str) -> bool:
        user_roles = self.roles.get(user_id, [])
        for role in user_roles:
            role_permissions = self.permissions.get(role, [])
            if action in role_permissions:
                return True
        return False
    
    def grant_role(self, user_id: str, role: str):
        if user_id not in self.roles:
            self.roles[user_id] = []
        self.roles[user_id].append(role)
```

## Troubleshooting Guide

### Common Issues

**Issue: High order error rate**
```python
async def diagnose_order_errors(restaurant_id: str, date_range: Tuple[date, date]):
    orders = await get_orders(restaurant_id, date_range)
    
    errors = [o for o in orders if o.status == "error"]
    
    print(f"Restaurant {restaurant_id}:")
    print(f"  Total orders: {len(orders)}")
    print(f"  Errors: {len(errors)}")
    print(f"  Error rate: {len(errors)/len(orders):.1%}")
    
    # Analyze error types
    error_types = defaultdict(int)
    for error in errors:
        error_types[error.error_type] += 1
    
    for error_type, count in error_types.items():
        print(f"  {error_type}: {count}")
```

**Issue: Low table utilization**
```python
async def analyze_table_utilization(restaurant_id: str, date: date):
    tables = await get_tables(restaurant_id)
    reservations = await get_reservations(restaurant_id, date)
    
    print(f"Table utilization for {date}:")
    for table in tables:
        table_reservations = [r for r in reservations if r.table_id == table.id]
        
        total_reserved_minutes = sum(
            r.duration_minutes for r in table_reservations
        )
        
        utilization = total_reserved_minutes / (12 * 60)  # 12-hour day
        
        print(f"  {table.id} ({table.capacity} seats): {utilization:.1%}")
```

**Issue: Kitchen bottlenecks**
```python
async def identify_kitchen_bottlenecks(restaurant_id: str, date: date):
    tickets = await get_kitchen_tickets(restaurant_id, date)
    
    # Analyze by station
    station_times = defaultdict(list)
    for ticket in tickets:
        for item in ticket.items:
            station_times[item.station].append(item.actual_time)
    
    print(f"Kitchen performance for {date}:")
    for station, times in station_times.items():
        avg_time = sum(times) / len(times)
        max_time = max(times)
        
        print(f"  {station}: avg={avg_time:.1f}min, max={max_time:.1f}min")
        
        if avg_time > 10:
            print(f"    WARNING: Station above target time")
```

## API Reference

### Menu Management API

```python
# Get menu
GET /api/v1/menu
Response:
{
    "restaurant_id": "REST-001",
    "categories": [
        {
            "name": "entrees",
            "items": [
                {
                    "id": "SALMON",
                    "name": "Grilled Salmon",
                    "price": 28.00,
                    "cost": 8.40,
                    "description": "Fresh Atlantic salmon with quinoa",
                    "allergens": ["fish"]
                }
            ]
        }
    ]
}

# Update menu item
PUT /api/v1/menu/items/{item_id}
Request:
{
    "name": "Grilled Salmon",
    "price": 29.00,
    "description": "Fresh Atlantic salmon with quinoa and seasonal vegetables"
}
```

### Order Management API

```python
# Create order
POST /api/v1/orders
Request:
{
    "restaurant_id": "REST-001",
    "items": [
        {"item_id": "SALMON", "quantity": 2, "customizations": {"side": "quinoa"}}
    ],
    "table_id": "T3"
}

Response:
{
    "order_id": "ORD-001",
    "total": 56.00,
    "status": "confirmed",
    "estimated_ready_time": "2026-07-01T19:30:00Z"
}

# Update order status
PATCH /api/v1/orders/{order_id}
Request:
{
    "status": "ready"
}
```

### Reservation API

```python
# Create reservation
POST /api/v1/reservations
Request:
{
    "customer_name": "John Smith",
    "party_size": 4,
    "date_time": "2026-07-15T19:00:00",
    "preferences": {"zone": "main"}
}

Response:
{
    "reservation_id": "RES-001",
    "table_id": "T2",
    "confirmation_code": "ABC123",
    "date_time": "2026-07-15T19:00:00"
}

# Check availability
GET /api/v1/reservations/availability
Query Parameters:
  - party_size: 4
  - date_time: 2026-07-15T19:00:00

Response:
{
    "available": true,
    "tables": ["T2", "T3"],
    "suggested_times": ["18:30", "19:00", "19:30"]
}
```

## Data Models

### Order Model

```python
class Order:
    order_id: str
    restaurant_id: str
    table_id: Optional[str]
    items: List[OrderItem]
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    status: OrderStatus
    source: OrderSource
    customer: Optional[Customer]
    created_at: datetime
    updated_at: datetime
```

### Menu Item Model

```python
class MenuItem:
    item_id: str
    restaurant_id: str
    name: str
    description: str
    category: str
    price: Decimal
    cost: Decimal
    allergens: List[str]
    modifiers: List[Modifier]
    is_available: bool
    prep_time_minutes: int
    calories: Optional[int]
    image_url: Optional[str]
```

### Reservation Model

```python
class Reservation:
    reservation_id: str
    restaurant_id: str
    customer_name: str
    party_size: int
    table_id: Optional[str]
    date_time: datetime
    duration_minutes: int
    status: ReservationStatus
    confirmation_code: str
    preferences: Dict[str, Any]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: restaurant-tech-service
  namespace: restaurant-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: restaurant-tech-service
  template:
    metadata:
      labels:
        app: restaurant-tech-service
    spec:
      containers:
      - name: restaurant-tech
        image: your-registry/restaurant-tech-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8443
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8443
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Database Migration

```bash
# Run migrations
alembic upgrade head

# Verify migration status
alembic current

# Rollback if needed
alembic downgrade -1
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Order metrics
orders_counter = Counter(
    'restaurant_orders_total',
    'Total orders',
    ['restaurant_id', 'source', 'status']
)

order_duration = Histogram(
    'restaurant_order_duration_seconds',
    'Order processing duration',
    ['restaurant_id'],
    buckets=[300, 600, 900, 1800, 3600]
)

# Reservation metrics
reservations_counter = Counter(
    'restaurant_reservations_total',
    'Total reservations',
    ['restaurant_id', 'status']
)

# Table metrics
table_utilization = Gauge(
    'restaurant_table_utilization',
    'Table utilization percentage',
    ['restaurant_id', 'table_id']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Restaurant Operations",
    "panels": [
      {
        "title": "Order Volume",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(restaurant_orders_total[5m])",
            "legendFormat": "{{source}} - {{status}}"
          }
        ]
      },
      {
        "title": "Table Utilization",
        "type": "gauge",
        "targets": [
          {
            "expr": "restaurant_table_utilization",
            "legendFormat": "{{table_id}}"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
groups:
- name: restaurant_alerts
  rules:
  - alert: HighOrderErrorRate
    expr: rate(restaurant_orders_total{status="error"}[5m]) / rate(restaurant_orders_total[5m]) > 0.1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Order error rate exceeds 10%"
      
  - alert: LowTableUtilization
    expr: restaurant_table_utilization < 0.3
    for: 30m
    labels:
      severity: info
    annotations:
      summary: "Table utilization below 30%"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from decimal import Decimal

class TestMenuEngineering:
    def test_calculate_profit_margin(self, menu_engine):
        item = MenuItem(
            item_id="SALMON",
            name="Grilled Salmon",
            price=Decimal("28.00"),
            cost=Decimal("8.40"),
        )
        
        margin = menu_engine.calculate_profit_margin(item)
        
        assert margin == 0.70  # 70% margin
    
    def test_classify_menu_item(self, menu_engine):
        item = MenuItem(
            item_id="SALMON",
            name="Grilled Salmon",
            profit_margin=0.70,
            popularity_score=0.20,
        )
        
        quadrant = menu_engine.classify_item(item)
        
        assert quadrant == "star"  # High profit, high popularity
```

### Integration Tests

```python
class TestEndToEndRestaurant:
    async def test_order_flow(self, restaurant_system):
        # Create order
        order = await restaurant_system.create_order(
            restaurant_id="REST-001",
            items=[{"item_id": "SALMON", "quantity": 2}],
            table_id="T3",
        )
        
        assert order.status == "confirmed"
        
        # Update status
        await restaurant_system.update_order_status(order.order_id, "preparing")
        
        # Verify status changed
        updated_order = await restaurant_system.get_order(order.order_id)
        assert updated_order.status == "preparing"
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class RestaurantUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def create_order(self):
        self.client.post("/api/v1/orders", json={
            "restaurant_id": "REST-001",
            "items": [{"item_id": "SALMON", "quantity": 2}],
        })
    
    @task(5)
    def create_reservation(self):
        self.client.post("/api/v1/reservations", json={
            "customer_name": f"Customer-{self.customer_counter}",
            "party_size": 4,
            "date_time": "2026-07-15T19:00:00",
        })
        self.customer_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/orders", methods=["POST"])
@app.route("/api/v2/orders", methods=["POST"])
async def create_order():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await create_order_v2()
    return await create_order_v1()
```

### Database Migration Strategy

```bash
# Forward migration
alembic upgrade head

# Specific version
alembic upgrade ae1027a6555

# Downgrade
alembic downgrade -1
```

## Glossary

- **BOH**: Back of House - kitchen and preparation areas
- **Covers**: Number of guests served
- **FIFO**: First In, First Out - inventory management method
- **FOH**: Front of House - dining room and customer service areas
- **KDS**: Kitchen Display System - digital order display in kitchen
- **POS**: Point of Sale - system for processing transactions
- **Par Level**: Minimum inventory level needed to meet demand
- **Table Turn Time**: Time from seating to payment for a table
- **Food Cost Percentage**: Cost of food sold divided by revenue
- **Labor Cost Percentage**: Labor costs divided by revenue

## Changelog

### Version 2.0.0 (2026-07-01)
- Added multi-location management
- Implemented demand forecasting for labor scheduling
- Enhanced kitchen display with station routing
- Added real-time inventory tracking

### Version 1.5.0 (2026-01-15)
- Added online ordering integration
- Implemented reservation optimization
- Enhanced menu engineering analytics

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic POS integration
- Menu management

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def create_order(
    restaurant_id: str,
    items: List[OrderItem],
    table_id: Optional[str],
) -> Order:
    """Create a new order.
    
    Args:
        restaurant_id: Restaurant identifier.
        items: Order items.
        table_id: Optional table assignment.
    
    Returns:
        Created order.
    
    Raises:
        OrderError: If order creation fails.
    """
    pass
```

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from team lead
6. Address review comments
7. Merge after approval

## License

MIT License

Copyright (c) 2026 Restaurant Technology Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
