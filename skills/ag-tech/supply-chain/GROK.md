---
name: "supply-chain"
category: "ag-tech"
version: "2.0.0"
tags: ["agriculture", "supply-chain", "traceability", "logistics", "cold-chain", "farm-to-fork", "blockchain"]
---

# Agricultural Supply Chain

## Overview

End-to-end agricultural supply chain management platform covering farm-to-fork traceability, cold chain monitoring, logistics optimization, inventory management, and regulatory compliance. This module tracks produce from field harvest through packing, processing, storage, transportation, and retail delivery using IoT sensors, GPS tracking, blockchain-based provenance records, and automated documentation. Supports FSMA 204 traceability requirements, USDA organic certification tracking, and GAP (Good Agricultural Practices) audit documentation.

## Core Capabilities

- **Farm-to-Fork Traceability**: Track every produce lot from field harvest to consumer with full chain of custody documentation
- **Cold Chain Monitoring**: Real-time temperature, humidity, and ethylene monitoring throughout transportation and storage
- **Logistics Optimization**: Route planning, load optimization, and delivery scheduling with fuel cost minimization
- **Inventory Management**: Lot-based inventory tracking with FIFO/FEFO rotation, shelf-life prediction, and waste reduction
- **Blockchain Provenance**: Immutable distributed ledger records for organic, fair-trade, and geographic indication certifications
- **Regulatory Compliance**: Automated FSMA 204 traceability documentation, USDA inspection records, and organic certification logs
- **Quality Grading**: Automated quality assessment at packing and receiving based on visual, weight, and temperature criteria
- **Demand Forecasting**: Predict retail demand using historical sales data, seasonal patterns, and market signals

## Usage

```python
from supply_chain import (
    Traceability, Lot, ColdChain, LogisticsOptimizer, InventoryManager
)

# Create a traceable lot from harvest
lot = Lot.create(
    crop="tomatoes",
    variety="Roma",
    field_id="FIELD-001",
    harvest_date="2024-07-15",
    quantity_lbs=5000,
    grade="USDA #1",
    organic_certified=True,
    harvest_crew="Team-A",
)
print(f"Lot {lot.lot_id} created: {lot.quantity_lbs} lbs of {lot.variety} {lot.crop}")
print(f"  QR Code: {lot.qr_code_url}")

# Track through supply chain
trace = Traceability()
trace.record_event(lot.lot_id, "harvest", "Field-001", "Farm-001")
trace.record_event(lot.lot_id, "wash_pack", "Pack-001", "Cooler-01")
trace.record_event(lot.lot_id, "storage", "Cooler-01", "Temp: 38°F")
trace.record_event(lot.lot_id, "transport", "Truck-4521", "Route: Farm→Distribution")
trace.record_event(lot.lot_id, "receive", "DC-Chicago", "Inspection: Passed")

history = trace.get_full_history(lot.lot_id)
print(f"\nTraceability chain ({len(history)} events):")
for event in history:
    print(f"  {event.timestamp}: {event.event_type} — {event.description}")

# Cold chain monitoring
cold = ColdChain()
cold.start_monitoring(lot.lot_id, sensor_id="TEMP-001", max_temp_f=41.0)
status = cold.check_status(lot.lot_id)
print(f"\nCold chain: {status.status} (current: {status.current_temp_f}°F, max: {status.max_temp_f}°F)")
```

```python
# Inventory management
inventory = InventoryManager()
inventory.receive(lot)
print(f"\nInventory: {inventory.total_lbs:.0f} lbs in stock")
print(f"  Lots: {inventory.lot_count}")
print(f"  Expiring soon: {inventory.expiring_lots_count}")

# Logistics optimization
optimizer = LogisticsOptimizer()
route = optimizer.optimize_route(
    origin="Farm-001",
    destinations=["DC-Chicago", "Retail-Store-101", "Retail-Store-205"],
    vehicle_capacity_lbs=40000,
)
print(f"\nOptimized route: {route.total_miles:.0f} miles, {route.estimated_hours:.1f} hours")
print(f"  Fuel cost: ${route.fuel_cost:.2f}")
for stop in route.stops:
    print(f"  Stop {stop.order}: {stop.location} ({stop.estimated_arrival})")
```

## Best Practices

- Assign a unique lot number at the moment of harvest — never after the fact
- Record temperature data at minimum every 5 minutes during cold chain transport
- Maintain 24-month records for FSMA 204 traceability compliance
- Use blockchain for high-value certifications (organic, geographic indication) where fraud risk is high
- Implement FIFO (First In, First Out) or FEFO (First Expired, First Out) for perishable inventory
- Document every transfer of custody with timestamp, responsible party, and condition at handoff
- Integrate IoT temperature loggers with cloud dashboards for real-time cold chain visibility
- Validate vehicle pre-cooling records before loading perishable produce
- Maintain contingency plans for cold chain failures (backup refrigeration, expedited delivery)
- Conduct mock recall exercises quarterly to verify traceability system effectiveness

## Related Modules

- **precision-farming** — Field-level production data feeds supply chain traceability
- **crop-monitoring** — Harvest timing optimization based on crop maturity
- **agricultural-iot** — IoT sensors for cold chain and field monitoring
- **soil-analysis** — Soil conditions affect produce quality and shelf life
- **blockchain** → **smart-contracts** — Smart contract templates for supply chain automation

## Advanced Configuration

### YAML Configuration
```yaml
version: "2.0.0"
settings:
  mode: "production"
  concurrency: 4
  timeout_ms: 30000
  retry:
    max_attempts: 3
    backoff_ms: 1000
  logging:
    level: "info"
    format: "json"
  data_sources:
    primary: "database"
    cache: "redis"
    storage: "s3"
```

### JSON Configuration
```json
{"version":"2.0.0","settings":{"mode":"production","concurrency":4,"timeout_ms":30000}}
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SKILL_MODE` | Runtime mode | `production` |
| `SKILL_CONCURRENCY` | Max concurrent ops | `4` |
| `SKILL_TIMEOUT` | Timeout (ms) | `30000` |
| `SKILL_LOG_LEVEL` | Log verbosity | `info` |
| `SKILL_DB_URL` | Database URL | -- |

## Architecture Patterns

### System Architecture
```
+---------------------------------------------------+
|                   Client Layer                     |
|  +----------+  +----------+  +------------------+  |
|  |  Web UI  |  | CLI Tool |  |  API Consumer    |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|              Processing Layer                      |
|  +----------+  +----------+  +------------------+  |
|  | Collector|  | Analyzer |  |  Generator       |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|                 Data Layer                          |
|  +----------+  +----------+  +------------------+  |
|  |  Cache   |  | TimeSrs  |  |  File Storage    |  |
|  |  (Redis) |  | (InfluxDB|  |  (S3/GCS)       |  |
|  +----------+  +----------+  +------------------+  |
+---------------------------------------------------+
```

### Data Flow
```
Input -> Validate -> Transform -> Process -> Enrich -> Store -> Response
  |         |           |          |         |        |
  |    [Schema]    [Mapping]   [Core]    [Merge]  [Persist]
  +---------+-----------+----------+---------+--------+
                    Error Handling Pipeline
```

## Integration Guide

### REST API
```python
import requests
response = requests.post("https://api.example.com/v1/integration", json={"source": "field-sensor"})
```

### Webhook
```python
webhook = {"url": "https://your-system.com/webhooks/data", "events": ["data.received"]}
```

## Performance Optimization

### Benchmarks
| Operation | Throughput | Latency (p50) | Latency (p99) |
|-----------|-----------|---------------|---------------|
| Data Ingest | 50,000 pts/s | 2ms | 15ms |
| Query | 5,000 ops/s | 20ms | 100ms |
| Analysis | 1,000 ops/s | 100ms | 500ms |

### Optimization Tips
1. **Batch Ingestion**: Group readings into batches
2. **Downsampling**: Reduce resolution for historical data
3. **Edge Computing**: Process locally to reduce bandwidth
4. **Connection Pooling**: Reuse connections
5. **Compression**: Use gzip for transfers

## Security Considerations

### Threat Model
| Threat | Risk | Mitigation |
|--------|------|------------|
| Data tampering | High | HMAC signing, audit logging |
| Unauthorized access | High | OAuth 2.0, mTLS |
| Data exfiltration | High | Encryption at rest |
| Man-in-the-middle | Medium | TLS 1.3 |

### Security Checklist
- [ ] All data encrypted in transit
- [ ] API keys in secure vault
- [ ] Firmware signed and verified
- [ ] Network segmentation for IoT
- [ ] Audit logging enabled

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| Sensor offline | Battery/signal | Check battery, verify range |
| Data gaps | Network outage | Enable edge buffering |
| Incorrect readings | Sensor drift | Recalibrate |
| High latency | Bottleneck | Scale workers |
| Storage full | Retention | Adjust retention policy |

## API Reference

### `init(config: Config) -> Instance`
Initialize the skill.

### `process(input: Input) -> Result`
Process input data.

### `validate(input: Input) -> ValidationResult`
Validate input schema.

## Data Models

### Sensor Reading Schema
```json
{"type":"object","required":["sensor_id","timestamp","value"],"properties":{"sensor_id":{"type":"string"},"timestamp":{"type":"string","format":"date-time"},"value":{"type":"number"}}}
```

## Deployment Guide

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "-m", "uvicorn", "main:app"]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skill-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: skill
  template:
    spec:
      containers:
      - name: skill
        image: skill:2.0.0
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

## Monitoring & Observability

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `ingest_total` | Counter | Data ingested | -- |
| `ingest_latency_ms` | Histogram | Ingest latency | p99 > 100ms |
| `error_rate` | Gauge | Error rate | > 5% |
| `sensor_offline` | Gauge | Offline sensors | > 0 |

## Testing Strategy

### Unit Tests
```python
def test_process():
    result = skill.process(test_input)
    assert result.status == "success"
```

### Integration Tests
```python
@pytest.mark.integration
def test_pipeline():
    result = skill.process(sensor_data)
    assert result.status == "success"
```

## Versioning & Migration

- Major version for breaking changes
- 6-month deprecation notice
- Migration guide provided

### Changelog
- **[2.0.0]** -- New architecture
- **[1.5.0]** -- Performance improvements
- **[1.0.0]** -- Initial release

## Glossary

| Term | Definition |
|------|------------|
| **Pipeline** | Ordered processing steps |
| **Schema** | Data structure definition |
| **Ingestion** | Collecting and storing data |
| **Downsampling** | Reducing data resolution |
| **Time-Series** | Time-indexed data |
| **Edge Computing** | Processing near source |
| **TTL** | Time-to-live |

## Changelog

### [2.0.0] -- 2024-12-01
- Major release with new architecture

### [1.5.0] -- 2024-06-15
- Performance improvements

### [1.0.0] -- 2024-01-01
- Initial stable release

## Contributing Guidelines

### Development Setup
```bash
git clone https://github.com/example/skill.git
cd skill
pip install -e ".[dev]"
pytest
```

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

## License

MIT License -- Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Advanced Concepts

### Cold Chain Temperature Thresholds
| Product | Optimal Temp (F) | Min Temp (F) | Max Temp (F) | Max RH% | Ethylene Sensitivity |
|---------|------------------|---------------|---------------|---------|---------------------|
| Tomatoes | 55-70 | 50 | 75 | 90 | High |
| Lettuce | 32-34 | 30 | 36 | 98 | Low |
| Berries | 32-34 | 30 | 36 | 90 | Moderate |
| Apples | 30-32 | 28 | 36 | 90 | High |
| Bananas | 56-58 | 54 | 60 | 85-90 | High |
| Melons | 45-50 | 40 | 55 | 85-90 | Moderate |
| Carrots | 32-34 | 30 | 36 | 98 | Low |
| Citrus | 45-50 | 40 | 55 | 85-90 | Low |

### Blockchain Provenance Integration
```python
from supply_chain import BlockchainProvenance

bc = BlockchainProvenance(network="ethereum", contract="0x1234...abcd")

# Record harvest event on blockchain
tx = bc.record_event(
    event_type="harvest",
    lot_id="LOT-2024-0715-001",
    data={
        "field_id": "FIELD-001",
        "crop": "tomatoes",
        "variety": "Roma",
        "quantity_lbs": 5000,
        "harvest_date": "2024-07-15",
        "organic_certified": True,
        "gps_coordinates": {"lat": 38.01, "lon": -98.01},
    },
    actor="Farm-001",
)
print(f"Transaction hash: {tx.hash}")
print(f"Block number: {tx.block_number}")
print(f"Gas used: {tx.gas_used}")

# Verify chain of custody
chain = bc.get_provenance_chain("LOT-2024-0715-001")
for event in chain:
    print(f"  {event.timestamp}: {event.event_type} by {event.actor} (verified: {event.verified})")
```

### Route Optimization Engine
```python
from supply_chain import RouteOptimizer

optimizer = RouteOptimizer()

# Optimize multi-stop delivery route
route = optimizer.optimize(
    origin={"lat": 38.01, "lon": -98.01, "name": "Farm-001"},
    destinations=[
        {"lat": 41.88, "lon": -87.63, "name": "Chicago DC", "delivery_window": "06:00-10:00"},
        {"lat": 42.33, "lon": -83.05, "name": "Detroit Store", "delivery_window": "14:00-18:00"},
        {"lat": 39.76, "lon": -86.16, "name": "Indianapolis Store", "delivery_window": "08:00-12:00"},
    ],
    vehicle_capacity_lbs=40000,
    vehicle_fuel_efficiency_mpg=6.5,
    fuel_cost_per_gallon=3.85,
    driver_hourly_rate=25.00,
)
print(f"Optimized distance: {route.total_miles:.0f} miles")
print(f"Estimated time: {route.estimated_hours:.1f} hours")
print(f"Fuel cost: ${route.fuel_cost:.2f}")
print(f"Driver cost: ${route.driver_cost:.2f}")
print(f"Total cost: ${route.total_cost:.2f}")
for stop in route.stops:
    print(f"  Stop {stop.order}: {stop.name} ({stop.estimated_arrival})")
```

### Shelf Life Prediction
```python
from supply_chain import ShelfLifePredictor

predictor = ShelfLifePredictor()

# Predict remaining shelf life
prediction = predictor.predict(
    product="tomatoes",
    variety="Roma",
    harvest_date="2024-07-15",
    current_temp_f=38,
    current_humidity_pct=90,
    days_since_harvest=3,
    quality_grade="USDA #1",
)
print(f"Remaining shelf life: {prediction.remaining_days} days")
print(f"Quality score: {prediction.quality_score}/100")
print(f"Sell-by date: {prediction.sell_by_date}")
print(f"Use-by date: {prediction.use_by_date}")
print(f"Waste risk: {prediction.waste_risk}")  # 'low', 'medium', 'high'
```

### Demand Forecasting Model
```python
from supply_chain import DemandForecaster

forecaster = DemandForecaster()

# Forecast demand for next 4 weeks
forecast = forecaster.forecast(
    product="tomatoes",
    store_id="STORE-101",
    historical_weeks=52,
    forecast_weeks=4,
    include_seasonality=True,
    include_trend=True,
    include_promotions=True,
)
for week in forecast.weeks:
    print(f"  Week {week.number}: {week.predicted_cases} cases (CI: {week.ci_low}-{week.ci_high})")

print(f"\nSeasonality index:")
for month, idx in forecast.seasonality.items():
    print(f"  {month}: {idx:.2f}")
```

### Lot Traceability Query
```python
from supply_chain import TraceabilityQuery

query = TraceabilityQuery()

# Trace forward (where did this lot go?)
forward = query.trace_forward(lot_id="LOT-2024-0715-001")
print(f"Forward trace ({len(forward.events)} events):")
for event in forward.events:
    print(f"  {event.timestamp}: {event.event_type} -> {event.destination}")

# Trace backward (where did this lot come from?)
backward = query.trace_backward(lot_id="LOT-2024-0715-001")
print(f"\nBackward trace ({len(backward.events)} events):")
for event in backward.events:
    print(f"  {event.timestamp}: {event.event_type} <- {event.source}")

# Recall simulation
recall = query.simulate_recall(
    affected_lots=["LOT-2024-0715-001", "LOT-2024-0715-002"],
    contamination_type="Listeria",
)
print(f"\nRecall scope:")
print(f"  Affected lots: {recall.affected_lots}")
print(f"  Downstream recipients: {recall.recipients}")
print(f"  Estimated volume: {recall.total_lbs:.0f} lbs")
print(f"  Trace completion time: {recall.trace_time_seconds:.0f} seconds")
```

### FSMA 204 Documentation
```python
from supply_chain import FSMA204Doc

fsma = FSMA204Doc()

# Generate required Key Data Elements (KDEs)
doc = fsma.generate_kdes(
    lot_id="LOT-2024-0715-001",
    product="tomatoes",
    critical_tracking_events=[
        {"event": "harvest", "location": "Field-001", "date": "2024-07-15"},
        {"event": "first_receiver", "location": "Pack-001", "date": "2024-07-15"},
        {"event": "transformer", "location": "Processor-001", "date": "2024-07-16"},
        {"event": "shipping", "location": "DC-Chicago", "date": "2024-07-17"},
    ],
)
print(f"FSMA 204 compliant: {doc.is_compliant}")
print(f"KDEs captured: {doc.kde_count}")
print(f"Missing elements: {doc.missing_elements}")
doc.export_pdf("fsma_204_record.pdf")
```

### Quality Grading Automation
```python
from supply_chain import QualityGrader

grader = QualityGrader()

# Automated quality assessment
result = grader.assess(
    product="tomatoes",
    images=["tomato_batch_1.jpg", "tomato_batch_2.jpg"],
    weight_data={"avg_weight_g": 180, "std_dev_g": 15},
    temperature_f=38,
)
print(f"Grade: {result.grade}")  # 'USDA #1', 'USDA #2', 'U.S. Commercial'
print(f"Color score: {result.color_score}/100")
print(f"Size uniformity: {result.size_uniformity:.1f}%")
print(f"Defect rate: {result.defect_pct:.1f}%")
print(f"Rejection rate: {result.rejection_pct:.1f}%")
```

### Inventory Management
```python
from supply_chain import InventoryManager

inv = InventoryManager(warehouse_id="WH-001")

# Receive lot
inv.receive(lot)

# Check inventory levels
levels = inv.get_levels(product="tomatoes")
print(f"Total in stock: {levels.total_lbs:.0f} lbs")
print(f"Lots in stock: {levels.lot_count}")
print(f"Oldest lot: {levels.oldest_lot_age_days} days")
print(f"Expiring within 3 days: {levels.expiring_3d_lbs:.0f} lbs")

# FIFO allocation
allocation = inv.allocate(
    product="tomatoes",
    requested_lbs=2000,
    method="FEFO",  # First Expired, First Out
)
print(f"Allocated from {len(allocation.lots)} lots:")
for lot_alloc in allocation.lots:
    print(f"  {lot_alloc.lot_id}: {lot_alloc.lbs:.0f} lbs (expires {lot_alloc.expiry_date})")
```

### Food Safety Compliance
```python
from supply_chain import FoodSafety

safety = FoodSafety()

# HACCP plan check
haccp = safety.check_haccp(
    facility_id="PACK-001",
    product="fresh-cut vegetables",
)
print(f"HACCP plan: {'Current' if haccp.is_current else 'EXPIRED'}")
print(f"CCPs monitored: {haccp.ccp_count}")
print(f"Deviations this month: {haccp.deviations}")
print(f"Corrective actions open: {haccp.open_actions}")

# GAP audit readiness
gap = safety.gap_readiness(
    facility_id="FARM-001",
    scope="harvest",  # 'pre-harvest', 'harvest', 'post-harvest'
)
print(f"GAP readiness score: {gap.score}/100")
print(f"Critical items: {gap.critical_items}")
print(f"Major items: {gap.major_items}")
print(f"Minor items: {gap.minor_items}")
```

### Lot Tracking Codes
```python
from supply_chain import LotCodeGenerator

generator = LotCodeGenerator()

# Generate lot codes
code = generator.generate(
    farm_id="FARM-001",
    field_id="FIELD-001",
    crop="tomatoes",
    harvest_date="2024-07-15",
    sequence=1,
)
print(f"Lot code: {code.lot_code}")  # 'F001-001-TOM-240715-001'
print(f"QR code: {code.qr_url}")
print(f"Barcode: {code.barcode_128}")

# Parse lot code
parsed = generator.parse("F001-001-TOM-240715-001")
print(f"Farm: {parsed.farm_id}")
print(f"Field: {parsed.field_id}")
print(f"Crop: {parsed.crop}")
print(f"Date: {parsed.harvest_date}")
print(f"Sequence: {parsed.sequence}")
```

### Transportation Monitoring
```python
from supply_chain import TransportMonitor

monitor = TransportMonitor()

# Monitor shipment
monitor.start(
    lot_id="LOT-2024-0715-001",
    truck_id="TRUCK-4521",
    sensor_id="TEMP-001",
    route_id="ROUTE-CHI-DET",
)

# Check status
status = monitor.get_status("LOT-2024-0715-001")
print(f"Current temp: {status.current_temp_f}F")
print(f"Max temp: {status.max_temp_f}F")
print(f"Min temp: {status.min_temp_f}F")
print(f"Door open events: {status.door_events}")
print(f"Location: ({status.lat:.4f}, {status.lon:.4f})")
print(f"ETA: {status.eta}")
print(f"Status: {status.condition_status}")  # 'good', 'warning', 'breach'
```

### Cost Analysis
```python
from supply_chain import CostAnalyzer

analyzer = CostAnalyzer()

# Analyze supply chain costs
costs = analyzer.analyze(
    lot_id="LOT-2024-0715-001",
    include=[
        "harvest_labor",
        "transport",
        "cold_storage",
        "packing",
        "insurance",
        "compliance",
    ],
)
print(f"Total cost: ${costs.total:.2f}")
print(f"Cost per lb: ${costs.per_lb:.4f}")
print(f"Cost breakdown:")
for item in costs.breakdown:
    print(f"  {item.category}: ${item.amount:.2f} ({item.pct:.1f}%)")
```

### Recall Effectiveness
```python
from supply_chain import RecallEffectiveness

re = RecallEffectiveness()

# Evaluate recall performance
result = re.evaluate(
    recall_id="RECALL-2024-001",
    start_date="2024-07-20",
    end_date="2024-07-27",
)
print(f"Recall effectiveness: {result.effectiveness_pct:.1f}%")
print(f"Response time: {result.response_time_hours:.1f} hours")
print(f"Product recovered: {result.recovered_pct:.1f}%")
print(f"Public notifications: {result.notifications_sent}")
print(f"Customer complaints: {result.complaints}")
```

### Sustainability Metrics
```python
from supply_chain import SustainabilityMetrics

metrics = SustainabilityMetrics()

# Calculate carbon footprint
carbon = metrics.calculate_carbon(
    lot_id="LOT-2024-0715-001",
    transport_miles=500,
    cold_storage_hours=72,
    packaging_kg=50,
)
print(f"Carbon footprint: {carbon.total_kg_co2:.1f} kg CO2")
print(f"Transport: {carbon.transport_kg:.1f} kg CO2")
print(f"Storage: {carbon.storage_kg:.1f} kg CO2")
print(f"Packaging: {carbon.packaging_kg:.1f} kg CO2")
print(f"Per lb: {carbon.per_lb_kg:.3f} kg CO2/lb")

# Water usage
water = metrics.calculate_water(
    field_id="FIELD-001",
    crop="tomatoes",
    irrigation_method="drip",
    season_inches=24,
)
print(f"Water footprint: {water.total_gallons:.0f} gallons")
print(f"Per lb: {water.per_lb_gallons:.2f} gal/lb")
```

---

## Return format (required)

Your FINAL assistant message — what the spawning agent will receive — MUST start with this header block:

  **Status**: success | partial | failed | blocked
  **Summary**: <one sentence describing what happened>

After the header, include the actual deliverable (whatever the task asked for in its prompt).

If applicable, also include below the deliverable:

  **Files touched**: <comma-separated paths or "(none)">
  **Findings worth promoting**: <bullet list of cross-task transferable facts; "(none)" if just routine work>

This format lets the spawning agent and the checkpoint writer extract your progress without parsing free-form prose. Do NOT precede the header with an introduction — your final message must start with "**Status**:".
