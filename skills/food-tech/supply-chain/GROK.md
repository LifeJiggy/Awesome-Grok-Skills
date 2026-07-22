---
name: "supply-chain"
category: "food-tech"
version: "2.0.0"
tags: ["food-tech", "supply-chain", "cold-chain", "logistics", "inventory", "procurement"]
difficulty: "intermediate"
estimated_time: "40-55 minutes"
prerequisites: ["python", "supply-chain-fundamentals"]
---

# Food Supply Chain Management

## Overview

Food supply chain management addresses the unique challenges of perishable goods logistics: temperature-controlled supply chains (cold chain), shelf-life management, demand forecasting for fresh products, supplier quality management, and regulatory compliance for food transport. This module provides tools for end-to-end food supply chain visibility from farm procurement through distribution to retail and food service endpoints.

## Core Capabilities

- **Cold Chain Management**: Real-time temperature monitoring throughout the supply chain with IoT sensor integration and excursion alerting
- **Shelf-Life Tracking**: Dynamic shelf-life prediction based on actual temperature history, not static expiration dates
- **Demand Forecasting**: ML-driven demand prediction for perishable goods considering seasonality, weather, events, and promotional calendars
- **Procurement Optimization**: Supplier selection, contract management, and automated purchasing for raw materials and ingredients
- **Warehouse Management**: Food-grade warehouse operations including FIFO/FEFO enforcement, lot tracking, and quality hold management
- **Route Optimization**: Multi-stop delivery route planning for perishable goods with time window and temperature constraints
- **Inventory Management**: Perishable inventory management with first-expiry-first-out (FEFO) logic and waste reduction analytics
- **Supplier Quality Management**: Supplier scorecards, audit management, and corrective action tracking
- **Cost Analysis**: landed cost calculation including procurement, transport, storage, and waste costs
- **Sustainability Metrics**: Carbon footprint tracking, food waste measurement, and sustainable sourcing analytics

## Usage Examples

### Cold Chain Monitoring

```python
from food_tech.supply_chain import ColdChainManager, TemperatureZone

chain = ColdChainManager(
    alert_channels=["sms", "email", "dashboard"],
    excursion_threshold_minutes=15,
)

# Track a shipment
shipment = chain.create_shipment(
    shipment_id="SHP-2026-07-001",
    product="Fresh Salmon",
    origin="Seattle, WA",
    destination="Chicago, IL",
    temperature_zone=TemperatureZone.FRESH,
    target_range_celsius=(-1, 2),
    estimated_transit_hours=48,
)

# Record temperature readings
chain.record_temperature("SHP-2026-07-001", 1.2, sensor_id="TRAILER-01")
chain.record_temperature("SHP-2026-07-001", 3.5, sensor_id="TRAILER-01")  # Warning

status = chain.get_shipment_status("SHP-2026-07-001")
print(f"Status: {status.current_status}")
print(f"Avg Temp: {status.average_temperature:.1f}C")
print(f"Excursions: {status.excursion_count}")
print(f"Remaining shelf life: {status.projected_shelf_life_hours:.1f} hours")
```

### Demand Forecasting

```python
from food_tech.supply_chain import DemandForecaster

forecaster = DemandForecaster(
    model="prophet",
    granularity="daily",
    include_weather=True,
)

# Generate forecast
forecast = forecaster.predict(
    product_id="SALMON-ATLANTIC-FRESH",
    location="CHICAGO-DC",
    horizon_days=14,
    historical_data="sales_2025.csv",
    special_events=["4th_of_july", "labor_day"],
)

print(f"14-day demand: {forecast.total_units:,} lbs")
for day in forecast.daily_forecast[:7]:
    print(f"  {day.date}: {day.predicted_units:,} lbs "
          f"(range: {day.ci_lower:,}-{day.ci_upper:,})")
```

### Supplier Quality Scorecard

```python
from food_tech.supply_chain import SupplierQualityManager

sqm = SupplierQualityManager()

# Register supplier
supplier = sqm.register_supplier(
    name="Pacific Seafood Co.",
    category="fresh_seafood",
    location="Seattle, WA",
    certifications=["HACCP", "MSC", "SQF"],
)

# Score supplier
scorecard = sqm.score_supplier(
    supplier_id=supplier.supplier_id,
    period="2026-Q2",
    metrics={
        "on_time_delivery": 0.95,
        "quality_rejection_rate": 0.02,
        "food_safety_audit_score": 92,
        "response_time_hours": 4,
        "documentation_accuracy": 0.98,
    },
)

print(f"Supplier: {scorecard.supplier_name}")
print(f"Overall Score: {scorecard.overall_score:.1f}/100")
print(f"Grade: {scorecard.grade}")
for area, s in scorecard.area_scores.items():
    print(f"  {area}: {s:.1f}/100")
```

## Best Practices

- Implement FEFO (First Expired First Out) rather than FIFO for perishable inventory management
- Use dynamic shelf-life models based on actual time-temperature history rather than static date codes
- Monitor cold chain continuously; a 15-minute temperature excursion can reduce shelf life by 30%+
- Maintain supplier diversification; no single supplier should represent >40% of critical ingredient supply
- Forecast demand at the SKU-location-day level for perishables to minimize waste and stockouts
- Track food waste metrics (shrink rate) by category and implement waste reduction programs
- Conduct mock recall exercises quarterly to validate traceability system effectiveness
- Use landed cost analysis including waste to make true cost-of-goods decisions
- Negotiate vendor-managed inventory (VMI) agreements for high-volume staple items
- Implement automated reorder points based on lead time variability, not just average lead time

## Related Modules

- `food-tech/food-safety` - HACCP, temperature compliance, and traceability
- `food-tech/agriculture-data` - Farm-level data for procurement
- `food-tech/restaurant-tech` - Restaurant supply chain operations
- `food-tech/nutrition-analysis` - Product composition for procurement decisions

## Advanced Configuration

### Cold Chain Configuration

```yaml
cold_chain:
  temperature_zones:
    frozen:
      name: "Frozen"
      target_range_celsius: [-25, -18]
      alert_threshold_celsius: -15
      shelf_life_extension_hours: 0
      
    deep_frozen:
      name: "Deep Frozen"
      target_range_celsius: [-35, -28]
      alert_threshold_celsius: -25
      shelf_life_extension_hours: 0
      
    fresh:
      name: "Fresh"
      target_range_celsius: [-1, 4]
      alert_threshold_celsius: 5
      shelf_life_extension_hours: -12
      
    chilled:
      name: "Chilled"
      target_range_celsius: [0, 4]
      alert_threshold_celsius: 5
      shelf_life_extension_hours: -6
      
  monitoring:
    sensors:
      - type: "iot_wireless"
        protocol: "bluetooth_le"
        battery_life_days: 365
        accuracy_celsius: 0.5
        
      - type: "gps_tracker"
        features: ["temperature", "location", "humidity"]
        reporting_interval_minutes: 5
        
    alerts:
      channels:
        - type: "sms"
          recipients: ["+1-555-0101", "+1-555-0102"]
        - type: "email"
          recipients: ["ops@company.com", "quality@company.com"]
        - type: "webhook"
          url: "https://alerts.company.com/cold-chain"
          
      escalation:
        enabled: true
        escalation_time_minutes: 15
        escalation_contacts: ["+1-555-0103"]
```

### Demand Forecasting Configuration

```yaml
demand_forecasting:
  model:
    type: "prophet"
    seasonality:
      yearly: true
      weekly: true
      daily: false
    holidays:
      enabled: true
      country: "US"
      additional_holidays:
        - "super_bowl_sunday"
        - "memorial_day"
        - "independence_day"
        - "labor_day"
        - "thanksgiving"
        - "christmas"
        
  external_factors:
    weather:
      enabled: true
      api_key: "${WEATHER_API_KEY}"
      forecast_days: 7
      
    events:
      enabled: true
      sources:
        - "eventbrite"
        - "sports_schedules"
        
    promotions:
      enabled: true
      data_source: "pos_system"
      
  granularity:
    time_level: "daily"
    product_level: "sku"
    location_level: "store"
    
  accuracy_targets:
    mape_threshold: 15  # Mean Absolute Percentage Error
    bias_threshold: 5   # Forecast Bias
```

### Supplier Management Configuration

```yaml
supplier_management:
  qualification:
    required_certifications:
      - "HACCP"
      - "SQF"
      - "GFSI"
      
    audit_frequency_days: 365
    performance_review_days: 90
    
  scoring:
    weights:
      quality: 0.35
      delivery: 0.30
      cost: 0.20
      responsiveness: 0.15
      
    grades:
      A:
        min_score: 90
        benefits: ["preferred_supplier", "longer_contracts"]
      B:
        min_score: 75
        benefits: ["standard_terms"]
      C:
        min_score: 60
        benefits: ["probationary_status"]
      F:
        max_score: 59
        actions: ["improvement_plan", "potential_disqualification"]
        
  risk_management:
    diversification_rules:
      max_single_supplier_pct: 40
      min_suppliers_per_category: 2
      
    monitoring:
      financial_health: true
      geopolitical_risk: true
      weather_disruption: true
```

## Architecture Patterns

### Event-Driven Supply Chain

```python
class SupplyChainEventProcessor:
    def __init__(self, event_store, notification_service):
        self.event_store = event_store
        self.notifier = notification_service
    
    async def process_event(self, event: SupplyChainEvent):
        # Store event
        await self.event_store.store(event)
        
        # Route to appropriate handlers
        handlers = {
            "shipment_created": self.handle_shipment_created,
            "temperature_excursion": self.handle_temperature_excursion,
            "delivery_completed": self.handle_delivery_completed,
            "inventory_low": self.handle_inventory_low,
        }
        
        handler = handlers.get(event.event_type)
        if handler:
            await handler(event)
    
    async def handle_temperature_excursion(self, event: TemperatureEvent):
        # Alert operations team
        await self.notifier.send_alert(
            severity="high",
            message=f"Temperature excursion on shipment {event.shipment_id}",
            details=event.details,
        )
        
        # Update shelf life
        await self.update_shelf_life(event.shipment_id, event)
        
        # Log for compliance
        await self.log_compliance_event(event)
```

### Dynamic Shelf-Life Prediction

```python
class ShelfLifePredictor:
    def __init__(self, temperature_history, product_data):
        self.temp_history = temperature_history
        self.product_data = product_data
    
    async def predict_remaining_shelf_life(self, shipment_id: str) -> ShelfLifePrediction:
        # Get temperature history
        temps = await self.temp_history.get(shipment_id)
        
        # Calculate time-temperature integral
        tti = self.calculate_tti(temps)
        
        # Get base shelf life
        base_shelf_life = self.product_data.get_base_shelf_life(shipment_id)
        
        # Apply TTI model
        remaining = base_shelf_life * self.tti_model(tti)
        
        # Calculate confidence
        confidence = self.calculate_confidence(temps, base_shelf_life)
        
        return ShelfLifePrediction(
            shipment_id=shipment_id,
            remaining_hours=remaining,
            base_shelf_life_hours=base_shelf_life,
            tti_value=tti,
            confidence=confidence,
            factors=self.identify_factors(temps),
        )
```

### Demand Forecasting Engine

```python
class DemandForecastingEngine:
    def __init__(self, model_registry, feature_store):
        self.models = model_registry
        self.features = feature_store
    
    async def forecast(self, product_id: str, location_id: str, horizon_days: int) -> Forecast:
        # Get features
        features = await self.features.get_features(product_id, location_id)
        
        # Get appropriate model
        model = await self.models.get_model(product_id, location_id)
        
        # Generate forecast
        predictions = await model.predict(features, horizon_days)
        
        # Calculate confidence intervals
        ci = self.calculate_confidence_intervals(predictions, model.uncertainty)
        
        # Adjust for special events
        adjusted = await self.adjust_for_events(predictions, location_id)
        
        return Forecast(
            product_id=product_id,
            location_id=location_id,
            predictions=adjusted,
            confidence_intervals=ci,
            accuracy_metrics=model.last_accuracy,
        )
```

### Inventory Optimization

```python
class InventoryOptimizer:
    def __init__(self, demand_forecast, lead_time_data):
        self.demand = demand_forecast
        self.lead_times = lead_time_data
    
    async def optimize_levels(self, product_id: str, location_id: str) -> InventoryRecommendation:
        # Get demand forecast
        forecast = await self.demand.forecast(product_id, location_id, horizon_days=30)
        
        # Get lead time statistics
        lead_time = await self.lead_times.get_statistics(product_id, location_id)
        
        # Calculate safety stock
        safety_stock = self.calculate_safety_stock(
            demand_std=forecast.std_deviation,
            lead_time_mean=lead_time.mean_days,
            lead_time_std=lead_time.std_days,
            service_level=0.95,
        )
        
        # Calculate reorder point
        reorder_point = (
            forecast.average_daily_demand * lead_time.mean_days
            + safety_stock
        )
        
        # Calculate economic order quantity
        eoq = self.calculate_eoq(
            annual_demand=forecast.average_daily_demand * 365,
            ordering_cost=lead_time.ordering_cost,
            holding_cost_pct=0.25,
            unit_cost=lead_time.unit_cost,
        )
        
        return InventoryRecommendation(
            product_id=product_id,
            location_id=location_id,
            safety_stock=safety_stock,
            reorder_point=reorder_point,
            economic_order_quantity=eoq,
            max_level=reorder_point + eoq,
        )
```

## Integration Guide

### IoT Sensor Integration

```python
import asyncio
import json
from datetime import datetime

class IoTSensorIntegration:
    def __init__(self, mqtt_broker: str, topic_prefix: str):
        self.broker = mqtt_broker
        self.topic_prefix = topic_prefix
    
    async def connect(self):
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        await self.client.connect(self.broker)
    
    async def on_message(self, client, userdata, message):
        payload = json.loads(message.payload.decode())
        
        reading = SensorReading(
            sensor_id=payload['sensor_id'],
            temperature=payload['temperature'],
            humidity=payload.get('humidity'),
            location=payload.get('location'),
            timestamp=datetime.fromisoformat(payload['timestamp']),
        )
        
        await self.process_reading(reading)
```

### ERP Integration

```python
class ERPIntegration:
    def __init__(self, erp_url: str, credentials: dict):
        self.erp_url = erp_url
        self.credentials = credentials
    
    async def sync_inventory(self, location_id: str) -> SyncResult:
        # Get inventory from ERP
        erp_inventory = await self.get_erp_inventory(location_id)
        
        # Sync to supply chain system
        synced = 0
        errors = []
        
        for item in erp_inventory:
            try:
                await self.sync_inventory_item(item)
                synced += 1
            except Exception as e:
                errors.append({"item_id": item.id, "error": str(e)})
        
        return SyncResult(synced=synced, errors=errors)
    
    async def create_purchase_order(self, po: PurchaseOrder) -> POResult:
        # Transform to ERP format
        erp_po = self.transform_po(po)
        
        # Submit to ERP
        result = await self.submit_to_erp(erp_po)
        
        return POResult(
            po_id=result.po_id,
            status=result.status,
            estimated_delivery=result.estimated_delivery,
        )
```

### Transportation Management Integration

```python
class TMSIntegration:
    def __init__(self, tms_url: str, api_key: str):
        self.tms_url = tms_url
        self.api_key = api_key
    
    async def optimize_route(self, shipments: List[Shipment]) -> RouteOptimization:
        # Send to TMS for optimization
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "shipments": [s.to_dict() for s in shipments],
            "constraints": {
                "temperature_controlled": True,
                "time_windows": True,
                "max_drive_time_hours": 10,
            },
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.tms_url}/route/optimize",
                headers=headers,
                json=payload,
            )
        
        return self.parse_optimization(response.json())
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_shipments_status_date ON shipments (status, created_at DESC);
CREATE INDEX idx_temperature_readings_shipment ON temperature_readings (shipment_id, recorded_at);
CREATE INDEX idx_inventory_product_location ON inventory (product_id, location_id);
CREATE INDEX idx_orders_status_date ON orders (status, created_at DESC);

-- Partition tables by date
CREATE TABLE temperature_readings (
    id UUID PRIMARY KEY,
    shipment_id VARCHAR(100),
    temperature DECIMAL(5,2),
    recorded_at TIMESTAMP
) PARTITION BY RANGE (recorded_at);

-- Create monthly partitions
CREATE TABLE temperature_readings_2026_07 PARTITION OF temperature_readings
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
```

### Caching Strategy

```python
class SupplyChainCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes
    
    async def get_inventory_levels(self, location_id: str) -> Optional[Dict]:
        cache_key = f"inventory:{location_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        return None
    
    async def cache_inventory_levels(self, location_id: str, levels: Dict):
        cache_key = f"inventory:{location_id}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            json.dumps(levels)
        )
```

### Batch Processing

```python
class SupplyChainBatchProcessor:
    def __init__(self, batch_size: int = 1000):
        self.batch_size = batch_size
    
    async def process_batch(self, items: List, processor: Callable):
        batches = [
            items[i:i+self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*[
                processor(item) for item in batch
            ])
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Data Encryption

```python
from cryptography.fernet import Fernet

class SupplyChainEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive supply chain data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive supply chain data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class SupplyChainAccessControl:
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

### Audit Logging

```python
class SupplyChainAuditLogger:
    def __init__(self, db):
        self.db = db
    
    async def log_event(self, event: AuditEvent):
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'actor_id': event.actor_id,
            'action': event.action,
            'resource_id': event.resource_id,
            'details': event.details,
            'ip_address': event.ip_address,
            'user_agent': event.user_agent,
        }
        
        await self.db.audit_logs.insert(audit_entry)
```

## Troubleshooting Guide

### Common Issues

**Issue: Temperature excursions**
```python
async def diagnose_temperature_excursions(shipment_id: str):
    readings = await get_temperature_readings(shipment_id)
    
    excursions = [r for r in readings if not r.within_range]
    
    print(f"Shipment {shipment_id}:")
    print(f"  Total readings: {len(readings)}")
    print(f"  Excursions: {len(excursions)}")
    print(f"  Excursion rate: {len(excursions)/len(readings):.1%}")
    
    for excursion in excursions:
        print(f"    {excursion.timestamp}: {excursion.temperature}°C")
        print(f"    Duration: {excursion.duration_minutes} minutes")
        print(f"    Max deviation: {excursion.max_deviation}°C")
```

**Issue: High waste rates**
```python
async def analyze_waste_rates(location_id: str, date_range: Tuple[date, date]):
    inventory = await get_inventory_transactions(location_id, date_range)
    
    waste = [t for t in inventory if t.type == "waste"]
    
    print(f"Waste analysis for {location_id}:")
    print(f"  Total transactions: {len(inventory)}")
    print(f"  Waste transactions: {len(waste)}")
    print(f"  Waste rate: {len(waste)/len(inventory):.1%}")
    
    # Analyze by reason
    by_reason = defaultdict(int)
    for w in waste:
        by_reason[w.waste_reason] += 1
    
    for reason, count in by_reason.items():
        print(f"  {reason}: {count}")
```

**Issue: Forecast accuracy issues**
```python
async def diagnose_forecast_accuracy(product_id: str, location_id: str):
    forecast = await get_forecast(product_id, location_id)
    actuals = await get_actual_sales(product_id, location_id, days=30)
    
    # Calculate metrics
    mape = calculate_mape(forecast.predictions, actuals)
    bias = calculate_bias(forecast.predictions, actuals)
    
    print(f"Forecast accuracy for {product_id}:")
    print(f"  MAPE: {mape:.1f}%")
    print(f"  Bias: {bias:.1f}%")
    
    if mape > 20:
        print(f"  WARNING: High forecast error")
        print(f"  Recommendation: Review model parameters")
```

## API Reference

### Shipment API

```python
# Create shipment
POST /api/v1/shipments
Request:
{
    "product_id": "SALMON-ATLANTIC-FRESH",
    "origin": "Seattle, WA",
    "destination": "Chicago, IL",
    "temperature_zone": "fresh",
    "quantity": 500,
    "unit": "lbs"
}

Response:
{
    "shipment_id": "SHP-2026-07-001",
    "status": "created",
    "estimated_arrival": "2026-07-03T12:00:00Z",
    "tracking_url": "https://track.company.com/SHP-2026-07-001"
}

# Get shipment status
GET /api/v1/shipments/{shipment_id}
Response:
{
    "shipment_id": "SHP-2026-07-001",
    "status": "in_transit",
    "current_temperature": 1.5,
    "average_temperature": 1.2,
    "excursion_count": 0,
    "remaining_shelf_life_hours": 72
}
```

### Inventory API

```python
# Get inventory levels
GET /api/v1/inventory/{location_id}
Response:
{
    "location_id": "CHICAGO-DC",
    "items": [
        {
            "product_id": "SALMON-ATLANTIC-FRESH",
            "quantity": 2500,
            "unit": "lbs",
            "expiry_date": "2026-07-05",
            "status": "available"
        }
    ]
}

# Update inventory
POST /api/v1/inventory
Request:
{
    "location_id": "CHICAGO-DC",
    "product_id": "SALMON-ATLANTIC-FRESH",
    "quantity": 500,
    "unit": "lbs",
    "type": "receipt",
    "reference": "SHP-2026-07-001"
}
```

### Forecasting API

```python
# Generate forecast
POST /api/v1/forecasts
Request:
{
    "product_id": "SALMON-ATLANTIC-FRESH",
    "location_id": "CHICAGO-DC",
    "horizon_days": 14,
    "include_weather": true
}

Response:
{
    "forecast_id": "FC-001",
    "predictions": [
        {"date": "2026-07-01", "predicted_units": 250, "ci_lower": 200, "ci_upper": 300},
        {"date": "2026-07-02", "predicted_units": 275, "ci_lower": 220, "ci_upper": 330}
    ],
    "accuracy_metrics": {"mape": 12.5, "bias": 2.3}
}
```

## Data Models

### Shipment Model

```python
class Shipment:
    shipment_id: str
    product_id: str
    origin: str
    destination: str
    temperature_zone: str
    target_range_celsius: Tuple[float, float]
    quantity: Decimal
    unit: str
    status: ShipmentStatus
    estimated_arrival: datetime
    actual_arrival: Optional[datetime]
    carrier: Optional[str]
    trailer_id: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### Temperature Reading Model

```python
class TemperatureReading:
    reading_id: str
    shipment_id: str
    sensor_id: str
    temperature: Decimal
    humidity: Optional[Decimal]
    location: Optional[str]
    recorded_at: datetime
    within_range: bool
    alert_triggered: bool
```

### Inventory Model

```python
class InventoryItem:
    item_id: str
    location_id: str
    product_id: str
    quantity: Decimal
    unit: str
    expiry_date: Optional[date]
    lot_number: Optional[str]
    status: InventoryStatus
    created_at: datetime
    updated_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supply-chain-service
  namespace: supply-chain-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: supply-chain-service
  template:
    metadata:
      labels:
        app: supply-chain-service
    spec:
      containers:
      - name: supply-chain
        image: your-registry/supply-chain-service:2.0.0
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

# Shipment metrics
shipments_counter = Counter(
    'supply_chain_shipments_total',
    'Total shipments',
    ['status', 'temperature_zone']
)

shipment_duration = Histogram(
    'supply_chain_shipment_duration_hours',
    'Shipment duration',
    ['origin', 'destination'],
    buckets=[24, 48, 72, 96, 120]
)

# Temperature metrics
temperature_excursions_counter = Counter(
    'supply_chain_temperature_excursions_total',
    'Total temperature excursions',
    ['shipment_id', 'severity']
)

# Inventory metrics
inventory_levels = Gauge(
    'supply_chain_inventory_levels',
    'Current inventory levels',
    ['location_id', 'product_id']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Supply Chain Operations",
    "panels": [
      {
        "title": "Shipment Status",
        "type": "pie",
        "targets": [
          {
            "expr": "supply_chain_shipments_total",
            "legendFormat": "{{status}}"
          }
        ]
      },
      {
        "title": "Temperature Excursions",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(supply_chain_temperature_excursions_total[5m])",
            "legendFormat": "{{severity}}"
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
- name: supply_chain_alerts
  rules:
  - alert: HighTemperatureExcursionRate
    expr: rate(supply_chain_temperature_excursions_total{severity="high"}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High temperature excursion rate"
      
  - alert: LowInventoryLevels
    expr: supply_chain_inventory_levels < 100
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "Inventory levels below threshold"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from decimal import Decimal

class TestColdChainMonitoring:
    def test_within_range(self, cold_chain_manager):
        reading = TemperatureReading(
            shipment_id="SHP-001",
            sensor_id="SENSOR-01",
            temperature=1.5,
            recorded_at=datetime.utcnow(),
        )
        
        result = cold_chain_manager.check_temperature(reading)
        assert result.within_range == True
        assert result.alert_triggered == False
    
    def test_out_of_range(self, cold_chain_manager):
        reading = TemperatureReading(
            shipment_id="SHP-001",
            sensor_id="SENSOR-01",
            temperature=6.0,
            recorded_at=datetime.utcnow(),
        )
        
        result = cold_chain_manager.check_temperature(reading)
        assert result.within_range == False
        assert result.alert_triggered == True
```

### Integration Tests

```python
class TestEndToEndSupplyChain:
    async def test_shipment_flow(self, supply_chain_system):
        # Create shipment
        shipment = await supply_chain_system.create_shipment(
            product_id="SALMON-ATLANTIC-FRESH",
            origin="Seattle, WA",
            destination="Chicago, IL",
            temperature_zone="fresh",
            quantity=500,
            unit="lbs",
        )
        
        assert shipment.status == "created"
        
        # Update status
        await supply_chain_system.update_shipment_status(
            shipment.shipment_id, "in_transit"
        )
        
        # Verify status changed
        updated = await supply_chain_system.get_shipment(shipment.shipment_id)
        assert updated.status == "in_transit"
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class SupplyChainUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def get_shipment_status(self):
        self.client.get(f"/api/v1/shipments/shipment-{self.shipment_counter}")
        self.shipment_counter += 1
    
    @task(5)
    def create_shipment(self):
        self.client.post("/api/v1/shipments", json={
            "product_id": "SALMON-ATLANTIC-FRESH",
            "origin": "Seattle, WA",
            "destination": "Chicago, IL",
            "quantity": 500,
        })
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/shipments", methods=["POST"])
@app.route("/api/v2/shipments", methods=["POST"])
async def create_shipment():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await create_shipment_v2()
    return await create_shipment_v1()
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

- **FEFO**: First Expired First Out - inventory management method for perishables
- **FIFO**: First In First Out - inventory management method
- **GFSI**: Global Food Safety Initiative - food safety certification benchmark
- **HACCP**: Hazard Analysis Critical Control Points - food safety system
- **MAPE**: Mean Absolute Percentage Error - forecast accuracy metric
- **TTI**: Time-Temperature Indicator - device showing cumulative temperature exposure
- **VMI**: Vendor Managed Inventory - supplier manages inventory levels
- **WMS**: Warehouse Management System - software for warehouse operations

## Changelog

### Version 2.0.0 (2026-07-01)
- Added dynamic shelf-life prediction
- Implemented demand forecasting with external factors
- Enhanced supplier quality management
- Added sustainability metrics tracking

### Version 1.5.0 (2026-01-15)
- Added IoT sensor integration
- Implemented route optimization
- Enhanced inventory management with FEFO

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic cold chain monitoring
- Inventory management

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def create_shipment(
    product_id: str,
    origin: str,
    destination: str,
    temperature_zone: str,
) -> Shipment:
    """Create a new shipment.
    
    Args:
        product_id: Product identifier.
        origin: Origin location.
        destination: Destination location.
        temperature_zone: Temperature zone.
    
    Returns:
        Created shipment.
    
    Raises:
        ShipmentError: If shipment creation fails.
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

Copyright (c) 2026 Food Supply Chain Platform

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
