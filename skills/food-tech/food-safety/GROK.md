---
name: "food-safety"
category: "food-tech"
version: "2.0.0"
tags: ["food-tech", "food-safety", "haccp", "compliance", "quality-control", "traceability"]
difficulty: "intermediate"
estimated_time: "40-55 minutes"
prerequisites: ["python", "food-industry-basics"]
---

# Food Safety Technology

## Overview

Food safety technology provides digital tools for ensuring food products are safe for consumption throughout the supply chain—from farm to fork. This module covers HACCP (Hazard Analysis Critical Control Points) plan management, temperature monitoring, contamination detection, recall management, regulatory compliance (FDA, FSMA, EU regulations), and end-to-end traceability. It addresses the critical need for real-time food safety monitoring in an industry where foodborne illness affects 48 million Americans annually.

## Core Capabilities

- **HACCP Plan Management**: Digital HACCP plan creation, CCP (Critical Control Point) monitoring, corrective action tracking, and verification procedures
- **Temperature Monitoring**: IoT-based continuous temperature monitoring for cold chain integrity with automated alerts and compliance logging
- **Contamination Detection**: Integration with rapid testing systems for pathogen detection (Salmonella, E. coli, Listeria), chemical residues, and allergen screening
- **Traceability Systems**: Farm-to-fork product tracing with lot-level tracking, enabling <4-hour recall response times
- **Recall Management**: Automated recall initiation, affected lot identification, distribution tracing, and regulatory notification
- **Allergen Management**: Allergen tracking, cross-contamination prevention, and label verification systems
- **Sanitation Monitoring**: cleaning and sanitization schedule management, ATP verification, and environmental monitoring programs
- **Supplier Verification**: Supplier food safety assessment, audit management, and certificate tracking
- **Regulatory Compliance**: Automated compliance documentation for FDA FSMA, EU Regulation 178/2002, and Codex Alimentarius
- **Incident Management**: Food safety incident tracking, root cause analysis, and corrective action workflow management

## Usage Examples

### HACCP Plan Management

```python
from food_tech.food_safety import HACCPPlan, CCP, HazardType

plan = HACCPPlan(
    facility_id="PLANT-001",
    product="Fresh Orange Juice",
    flow_description="Receiving → Washing → Extraction → Pasteurization → Filling → Storage",
)

# Define Critical Control Points
plan.add_ccp(
    CCP(
        name="Pasteurization",
        step="Pasteurization",
        hazard=HazardType.BIOLOGICAL,
        critical_limit={"temperature_celsius": 90, "time_seconds": 30},
        monitoring_procedure="Continuous temperature recording",
        corrective_action="Divert product to re-pasteurization",
        verification="Daily calibration check",
    )
)

plan.add_ccp(
    CCP(
        name="Metal Detection",
        step="Post-Filling",
        hazard=HazardType.PHYSICAL,
        critical_limit={"ferrous_mm": 1.5, "non_ferrous_mm": 2.0, "stainless_steel_mm": 2.5},
        monitoring_procedure="Test pieces every 30 minutes",
        corrective_action="Reject and re-inspect affected product",
        verification="Daily sensitivity verification",
    )
)

# Validate the plan
validation = plan.validate()
print(f"CCPs defined: {validation.ccp_count}")
print(f"Hazards covered: {validation.hazard_coverage:.1%}")
print(f"Compliance score: {validation.compliance_score:.1%}")
```

### Temperature Monitoring

```python
from food_tech.food_safety import TemperatureMonitor, AlertSeverity

monitor = TemperatureMonitor(
    facility_id="PLANT-001",
    monitoring_interval_seconds=60,
    alert_channels=["email", "sms", "dashboard"],
)

# Register monitoring points
monitor.register_sensor(
    sensor_id="COLD-STORAGE-01",
    location="Cold Storage Room A",
    target_range_celsius=(-2, 4),
    alert_threshold_celsius=6,
)

monitor.register_sensor(
    sensor_id="TRANSPORT-TRUCK-12",
    location="Refrigerated Truck #12",
    target_range_celsius=(0, 4),
    alert_threshold_celsius=5,
)

# Check current readings
readings = monitor.get_current_readings()
for sensor_id, reading in readings.items():
    status = "OK" if reading.within_range else "ALERT"
    print(f"  {sensor_id}: {reading.temperature_celsius:.1f}C [{status}]")
    if not reading.within_range:
        print(f"    ALERT: {reading.alert_message}")
```

### Traceability System

```python
from food_tech.food_safety import TraceabilitySystem

trace = TraceabilitySystem(
    lot_level_tracking=True,
    qr_code_generation=True,
    blockchain_anchored=False,
)

# Record product journey
trace.record_event(
    lot_number="OJ-2026-07-001",
    event_type="harvest",
    location="Sunny Grove Farm, FL",
    timestamp="2026-07-01T06:00:00",
    details={"variety": "Navel", "quantity_kg": 5000},
)

trace.record_event(
    lot_number="OJ-2026-07-001",
    event_type="processing",
    location="JuiceCo Plant, Orlando",
    timestamp="2026-07-01T14:00:00",
    details={"process": "cold_press", "batch_size_liters": 4800},
)

# Full trace
history = trace.trace_lot("OJ-2026-07-001")
print(f"Events recorded: {len(history.events)}")
print(f"Farm to shelf: {history.total_duration_hours:.1f} hours")
for event in history.events:
    print(f"  {event.event_type}: {event.location} @ {event.timestamp[:16]}")
```

### Recall Management

```python
from food_tech.food_safety import RecallManager, RecallSeverity

recall_mgr = RecallManager()

# Initiate a recall
recall = recall_mgr.initiate(
    product="Fresh Orange Juice",
    lot_numbers=["OJ-2026-07-001", "OJ-2026-07-002"],
    reason="Potential Salmonella contamination",
    severity=RecallSeverity.CLASS_1,
    initiating_agency="FDA",
)

print(f"Recall ID: {recall.recall_id}")
print(f"Severity: {recall.severity.value}")

# Trace affected distribution
distribution = recall_mgr.trace_distribution(recall.recall_id)
print(f"Units affected: {distribution.total_units}")
print(f"Retailers notified: {distribution.retailer_count}")
print(f"States affected: {distribution.states_affected}")
```

## Best Practices

- Maintain digital HACCP records with tamper-evident timestamps for FDA inspection readiness
- Monitor cold chain temperatures continuously; manual logging misses excursions between checks
- Implement <4 hour traceability capability as required by FSMA Rule 204
- Test recall procedures quarterly with mock recalls to verify traceability system effectiveness
- Keep allergen management data current with recipe/formulation changes
- Calibrate all monitoring instruments on documented schedules with NIST-traceable standards
- Document all corrective actions with root cause analysis, not just the corrective action itself
- Train all food handlers on GMPs and retrain annually; maintain signed training records
- Conduct environmental monitoring programs for Listeria in ready-to-eat food facilities
- Integrate supplier certificates of analysis with incoming inspection procedures

## Related Modules

- `food-tech/supply-chain` - Supply chain traceability and logistics
- `food-tech/agriculture-data` - Farm-level data for traceability
- `food-tech/nutrition-analysis` - Product composition data
- `food-tech/restaurant-tech` - Food safety in restaurant operations

## Advanced Configuration

### HACCP Plan Configuration

```yaml
haccp:
  facility:
    id: "PLANT-001"
    name: "JuiceCo Processing Facility"
    address: "123 Food Safety Lane, Orlando, FL"
    regulatory_agency: "FDA"
    fsma_registered: true
    
  products:
    - name: "Fresh Orange Juice"
      category: "beverage"
      shelf_life_days: 14
      storage_temp_celsius: [0, 4]
      hazards:
        - type: "biological"
          agent: "Salmonella"
          severity: "high"
          probability: "medium"
        - type: "physical"
          agent: "metal"
          severity: "high"
          probability: "low"
          
  critical_control_points:
    - name: "Pasteurization"
      step: "Pasteurization"
      hazard: "biological"
      critical_limit:
        temperature_celsius: 90
        time_seconds: 30
      monitoring:
        method: "continuous_recording"
        frequency: "continuous"
        responsible: "Production Supervisor"
      corrective_action:
        immediate: "Divert product to re-pasteurization"
        long_term: "Investigate pasteurizer maintenance"
      verification:
        frequency: "daily"
        method: "calibration_check"
        records: "verification_log"
        
    - name: "Metal Detection"
      step: "Post-Filling"
      hazard: "physical"
      critical_limit:
        ferrous_mm: 1.5
        non_ferrous_mm: 2.0
        stainless_steel_mm: 2.5
      monitoring:
        method: "test_pieces"
        frequency: "every_30_minutes"
        responsible: "Quality Technician"
      corrective_action:
        immediate: "Reject and re-inspect affected product"
        long_term: "Investigate metal detector sensitivity"
      verification:
        frequency: "daily"
        method: "sensitivity_verification"
        records: "verification_log"
```

### Temperature Monitoring Configuration

```yaml
temperature_monitoring:
  sensors:
    - id: "COLD-STORAGE-01"
      location: "Cold Storage Room A"
      type: "digital_probe"
      target_range_celsius: [-2, 4]
      alert_threshold_celsius: 6
      recording_interval_seconds: 60
      calibration_frequency_days: 30
      
    - id: "TRANSPORT-TRUCK-12"
      location: "Refrigerated Truck #12"
      type: "wireless_logger"
      target_range_celsius: [0, 4]
      alert_threshold_celsius: 5
      recording_interval_seconds: 300
      calibration_frequency_days: 90
      
  alerts:
    channels:
      - type: "email"
        recipients: ["safety@juiceco.com", "ops@juiceco.com"]
      - type: "sms"
        recipients: ["+1-555-0101", "+1-555-0102"]
      - type: "dashboard"
        enabled: true
    escalation:
      enabled: true
      escalation_time_minutes: 15
      escalation_contacts: ["+1-555-0103"]
      
  compliance:
    retention_days: 730  # 2 years
    report_generation: "daily"
    regulatory_format: "FDA_FSMA"
```

### Traceability Configuration

```yaml
traceability:
  lot_tracking:
    enabled: true
    lot_number_format: "{product_code}-{date}-{sequence}"
    auto_generate: true
    
  events:
    tracked:
      - "harvest"
      - "receiving"
      - "processing"
      - "packaging"
      - "storage"
      - "shipping"
      - "retail"
    required_fields:
      - "lot_number"
      - "event_type"
      - "location"
      - "timestamp"
      - "quantity"
      - "responsible_party"
      
  blockchain:
    enabled: false
    network: "hyperledger"
    anchor_frequency: "daily"
    
  recall_capability:
    target_hours: 4
    mock_recall_frequency_days: 90
    success_threshold_pct: 95
```

## Architecture Patterns

### Event-Driven Food Safety Monitoring

```python
class FoodSafetyEventProcessor:
    def __init__(self, event_store, compliance_engine):
        self.event_store = event_store
        self.compliance_engine = compliance_engine
    
    async def process_event(self, event: FoodSafetyEvent):
        # Store event
        await self.event_store.store(event)
        
        # Run compliance checks
        checks = await self.compliance_engine.run_checks(event)
        
        # Generate alerts if needed
        alerts = await self.generate_alerts(checks)
        
        # Update audit trail
        await self.update_audit_trail(event, checks, alerts)
        
        return FoodSafetyResult(
            event=event,
            checks=checks,
            alerts=alerts,
        )
```

### Real-Time Temperature Monitoring

```python
class RealTimeTemperatureMonitor:
    def __init__(self, sensor_registry, alert_service):
        self.sensors = sensor_registry
        self.alerts = alert_service
        self.readings = {}
    
    async def process_reading(self, sensor_id: str, reading: TemperatureReading):
        # Store reading
        self.readings[sensor_id] = reading
        
        # Check against limits
        sensor = self.sensors.get(sensor_id)
        if not sensor:
            return
        
        if reading.temperature < sensor.target_range[0]:
            await self.alerts.send_alert(
                sensor_id=sensor_id,
                alert_type="low_temperature",
                temperature=reading.temperature,
                threshold=sensor.target_range[0],
            )
        elif reading.temperature > sensor.target_range[1]:
            await self.alerts.send_alert(
                sensor_id=sensor_id,
                alert_type="high_temperature",
                temperature=reading.temperature,
                threshold=sensor.target_range[1],
            )
    
    async def get_current_status(self) -> Dict[str, SensorStatus]:
        status = {}
        for sensor_id, reading in self.readings.items():
            sensor = self.sensors.get(sensor_id)
            if sensor:
                status[sensor_id] = SensorStatus(
                    sensor_id=sensor_id,
                    temperature=reading.temperature,
                    within_range=sensor.target_range[0] <= reading.temperature <= sensor.target_range[1],
                    last_updated=reading.timestamp,
                )
        return status
```

### HACCP Plan Validation

```python
class HACCPPlanValidator:
    def __init__(self):
        self.validation_rules = self.load_validation_rules()
    
    async def validate_plan(self, plan: HACCPPlan) -> ValidationResult:
        errors = []
        warnings = []
        
        # Check CCP coverage
        if len(plan.ccps) < 2:
            errors.append("Plan must have at least 2 CCPs")
        
        # Check hazard coverage
        covered_hazards = set(ccp.hazard for ccp in plan.ccps)
        all_hazards = set(hazard.type for hazard in plan.hazards)
        uncovered = all_hazards - covered_hazards
        
        if uncovered:
            warnings.append(f"Uncovered hazards: {uncovered}")
        
        # Check critical limits
        for ccp in plan.ccps:
            if not ccp.critical_limit:
                errors.append(f"CCP {ccp.name} missing critical limit")
            if not ccp.corrective_action:
                errors.append(f"CCP {ccp.name} missing corrective action")
        
        # Calculate compliance score
        compliance_score = self.calculate_compliance_score(errors, warnings)
        
        return ValidationResult(
            errors=errors,
            warnings=warnings,
            compliance_score=compliance_score,
            is_valid=len(errors) == 0,
        )
```

### Recall Management Pattern

```python
class RecallManager:
    def __init__(self, traceability_system, notification_service):
        self.traceability = traceability_system
        self.notifier = notification_service
    
    async def initiate_recall(self, recall_data: RecallData) -> Recall:
        # Create recall record
        recall = Recall(
            id=str(uuid.uuid4()),
            product=recall_data.product,
            lot_numbers=recall_data.lot_numbers,
            reason=recall_data.reason,
            severity=recall_data.severity,
            status="initiated",
            created_at=datetime.utcnow(),
        )
        
        # Trace affected distribution
        distribution = await self.traceability.trace_lots(recall_data.lot_numbers)
        
        # Notify affected parties
        await self.notifier.notify_distribution(distribution, recall)
        
        # Update status
        recall.status = "in_progress"
        recall.distribution = distribution
        
        return recall
```

## Integration Guide

### IoT Temperature Sensor Integration

```python
import asyncio
import json
from datetime import datetime

class IoTTemperatureIntegration:
    def __init__(self, mqtt_broker: str, topic_prefix: str):
        self.broker = mqtt_broker
        self.topic_prefix = topic_prefix
    
    async def connect(self):
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        await self.client.connect(self.broker)
    
    async def on_message(self, client, userdata, message):
        payload = json.loads(message.payload.decode())
        
        reading = TemperatureReading(
            sensor_id=payload['sensor_id'],
            temperature=payload['temperature'],
            timestamp=datetime.fromisoformat(payload['timestamp']),
            battery_level=payload.get('battery_level'),
        )
        
        await self.process_reading(reading)
```

### LIMS Integration

```python
class LIMSIntegration:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
    
    async def submit_sample(self, sample: Sample) -> TestResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "sample_id": sample.id,
            "lot_number": sample.lot_number,
            "test_type": sample.test_type,
            "collection_date": sample.collection_date.isoformat(),
            "collector": sample.collector,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/samples",
                headers=headers,
                json=payload,
            )
        
        return self.parse_response(response.json())
    
    async def get_test_results(self, sample_id: str) -> List[TestResult]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/samples/{sample_id}/results",
                headers=headers,
            )
        
        return self.parse_results(response.json())
```

### ERP Integration

```python
class ERPIntegration:
    def __init__(self, erp_url: str, credentials: dict):
        self.erp_url = erp_url
        self.credentials = credentials
    
    async def get_product_master(self, product_code: str) -> ProductMaster:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.erp_url}/products/{product_code}",
                auth=(self.credentials['username'], self.credentials['password']),
            )
        
        return self.parse_product(response.json())
    
    async def sync_lot_data(self, lot: Lot) -> SyncResult:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.erp_url}/lots",
                auth=(self.credentials['username'], self.credentials['password']),
                json=lot.to_dict(),
            )
        
        return self.parse_sync_result(response.json())
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_temperature_readings_sensor_date 
ON temperature_readings (sensor_id, recorded_at DESC);

CREATE INDEX idx_haccp_logs_facility_date 
ON haccp_logs (facility_id, recorded_at DESC);

CREATE INDEX idx_traceability_events_lot 
ON traceability_events (lot_number, event_type, recorded_at);

-- Partition tables by date
CREATE TABLE temperature_readings (
    id UUID PRIMARY KEY,
    sensor_id VARCHAR(100),
    temperature DECIMAL(5,2),
    recorded_at TIMESTAMP
) PARTITION BY RANGE (recorded_at);

-- Create monthly partitions
CREATE TABLE temperature_readings_2026_07 PARTITION OF temperature_readings
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
```

### Caching Strategy

```python
class FoodSafetyCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes
    
    async def get_sensor_status(self, sensor_id: str) -> Optional[SensorStatus]:
        cache_key = f"sensor_status:{sensor_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return SensorStatus.from_json(cached)
        return None
    
    async def cache_sensor_status(self, sensor_id: str, status: SensorStatus):
        cache_key = f"sensor_status:{sensor_id}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            status.to_json()
        )
```

### Batch Processing

```python
class BatchProcessor:
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

class FoodSafetyEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive food safety data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive food safety data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class FoodSafetyAccessControl:
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
class FoodSafetyAuditLogger:
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

**Issue: Temperature excursion alerts**
```python
async def diagnose_temperature_excursion(sensor_id: str):
    readings = await get_recent_readings(sensor_id, hours=24)
    
    excursions = [r for r in readings if not r.within_range]
    
    print(f"Sensor {sensor_id}:")
    print(f"  Total readings: {len(readings)}")
    print(f"  Excursions: {len(excursions)}")
    print(f"  Excursion rate: {len(excursions)/len(readings):.1%}")
    
    for excursion in excursions:
        print(f"    {excursion.timestamp}: {excursion.temperature}°C")
        print(f"    Duration: {excursion.duration_minutes} minutes")
        print(f"    Max deviation: {excursion.max_deviation}°C")
```

**Issue: HACCP plan non-compliance**
```python
async def audit_haccp_compliance(facility_id: str):
    plan = await get_haccp_plan(facility_id)
    logs = await get_haccp_logs(facility_id, days=30)
    
    compliance_issues = []
    
    # Check CCP monitoring
    for ccp in plan.ccps:
        monitoring_logs = [l for l in logs if l.ccp_name == ccp.name]
        
        if len(monitoring_logs) == 0:
            compliance_issues.append(f"CCP {ccp.name}: No monitoring logs")
        elif len(monitoring_logs) < 100:  # Expected minimum
            compliance_issues.append(f"CCP {ccp.name}: Insufficient monitoring")
    
    # Check corrective actions
    deviations = [l for l in logs if l.deviation]
    for deviation in deviations:
        if not deviation.corrective_action:
            compliance_issues.append(f"Deviation {deviation.id}: No corrective action")
    
    return compliance_issues
```

**Issue: Traceability gaps**
```python
async def identify_traceability_gaps(lot_number: str):
    events = await get_traceability_events(lot_number)
    
    required_events = ["harvest", "receiving", "processing", "packaging", "shipping"]
    recorded_events = set(e.event_type for e in events)
    
    missing_events = set(required_events) - recorded_events
    
    if missing_events:
        print(f"Lot {lot_number}:")
        print(f"  Missing events: {missing_events}")
        print(f"  Traceability gap detected")
        return False
    
    print(f"Lot {lot_number}: Full traceability confirmed")
    return True
```

## API Reference

### Temperature Monitoring API

```python
# Get current temperature readings
GET /api/v1/temperature/readings
Response:
{
    "readings": [
        {
            "sensor_id": "COLD-STORAGE-01",
            "temperature": 2.5,
            "unit": "celsius",
            "within_range": true,
            "recorded_at": "2026-07-01T12:00:00Z"
        }
    ]
}

# Get temperature history
GET /api/v1/temperature/history/{sensor_id}
Query Parameters:
  - start_date: 2026-07-01
  - end_date: 2026-07-02
  - interval: 1h
Response:
{
    "sensor_id": "COLD-STORAGE-01",
    "readings": [...],
    "statistics": {
        "min": -1.5,
        "max": 3.8,
        "avg": 1.2,
        "excursions": 2
    }
}
```

### HACCP Management API

```python
# Get HACCP plan
GET /api/v1/haccp/plans/{plan_id}
Response:
{
    "plan_id": "HACCP-001",
    "facility_id": "PLANT-001",
    "product": "Fresh Orange Juice",
    "ccps": [...],
    "validation_status": "approved",
    "last_review_date": "2026-06-15"
}

# Submit HACCP log
POST /api/v1/haccp/logs
Request:
{
    "plan_id": "HACCP-001",
    "ccp_name": "Pasteurization",
    "recorded_at": "2026-07-01T12:00:00Z",
    "temperature": 92.5,
    "time_seconds": 35,
    "operator_id": "OP-001"
}
Response:
{
    "log_id": "LOG-001",
    "status": "recorded",
    "within_limits": true
}
```

### Traceability API

```python
# Trace lot
GET /api/v1/traceability/lot/{lot_number}
Response:
{
    "lot_number": "OJ-2026-07-001",
    "events": [
        {
            "event_type": "harvest",
            "location": "Sunny Grove Farm, FL",
            "timestamp": "2026-07-01T06:00:00Z",
            "quantity": 5000,
            "unit": "kg"
        },
        {
            "event_type": "processing",
            "location": "JuiceCo Plant, Orlando",
            "timestamp": "2026-07-01T14:00:00Z",
            "quantity": 4800,
            "unit": "liters"
        }
    ],
    "farm_to_shelf_hours": 36.5
}

# Record traceability event
POST /api/v1/traceability/events
Request:
{
    "lot_number": "OJ-2026-07-001",
    "event_type": "shipping",
    "location": "JuiceCo Warehouse, Orlando",
    "timestamp": "2026-07-02T08:00:00Z",
    "quantity": 4800,
    "unit": "liters",
    "destination": "Retail Distribution Center"
}
```

## Data Models

### Temperature Reading Model

```python
class TemperatureReading:
    reading_id: str
    sensor_id: str
    temperature: Decimal
    unit: str  # celsius, fahrenheit
    recorded_at: datetime
    battery_level: Optional[int]
    within_range: bool
    alert_triggered: bool
```

### HACCP Log Model

```python
class HACCPLog:
    log_id: str
    plan_id: str
    ccp_name: str
    recorded_at: datetime
    operator_id: str
    measurements: Dict[str, Any]
    within_limits: bool
    deviation: Optional[Deviation]
    corrective_action: Optional[CorrectiveAction]
```

### Traceability Event Model

```python
class TraceabilityEvent:
    event_id: str
    lot_number: str
    event_type: str
    location: str
    timestamp: datetime
    quantity: Decimal
    unit: str
    details: Dict[str, Any]
    recorded_by: str
    created_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: food-safety-service
  namespace: food-safety-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: food-safety-service
  template:
    metadata:
      labels:
        app: food-safety-service
    spec:
      containers:
      - name: food-safety
        image: your-registry/food-safety-service:2.0.0
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

# Temperature metrics
temperature_readings_counter = Counter(
    'temperature_readings_total',
    'Total temperature readings',
    ['sensor_id', 'status']
)

temperature_excursion_counter = Counter(
    'temperature_excursions_total',
    'Total temperature excursions',
    ['sensor_id', 'severity']
)

# HACCP metrics
haccp_logs_counter = Counter(
    'haccp_logs_total',
    'Total HACCP logs',
    ['plan_id', 'ccp_name', 'status']
)

# Traceability metrics
traceability_events_counter = Counter(
    'traceability_events_total',
    'Total traceability events',
    ['lot_number', 'event_type']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Food Safety Monitoring",
    "panels": [
      {
        "title": "Temperature Readings",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(temperature_readings_total[5m])",
            "legendFormat": "{{sensor_id}} - {{status}}"
          }
        ]
      },
      {
        "title": "Temperature Excursions",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(temperature_excursions_total[5m])",
            "legendFormat": "{{sensor_id}}"
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
- name: food_safety_alerts
  rules:
  - alert: HighTemperatureExcursion
    expr: rate(temperature_excursions_total{severity="high"}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High temperature excursion rate"
      
  - alert: HACCPMonitoringMissed
    expr: haccp_logs_missing > 0
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "HACCP monitoring logs missing"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from decimal import Decimal

class TestTemperatureMonitoring:
    def test_within_range(self, temperature_monitor):
        reading = TemperatureReading(
            sensor_id="COLD-STORAGE-01",
            temperature=2.5,
            recorded_at=datetime.utcnow(),
        )
        
        result = temperature_monitor.check_reading(reading)
        assert result.within_range == True
        assert result.alert_triggered == False
    
    def test_out_of_range(self, temperature_monitor):
        reading = TemperatureReading(
            sensor_id="COLD-STORAGE-01",
            temperature=7.5,
            recorded_at=datetime.utcnow(),
        )
        
        result = temperature_monitor.check_reading(reading)
        assert result.within_range == False
        assert result.alert_triggered == True
```

### Integration Tests

```python
class TestEndToEndFoodSafety:
    async def test_haccp_workflow(self, haccp_manager):
        # Create HACCP plan
        plan = await haccp_manager.create_plan(
            facility_id="PLANT-001",
            product="Fresh Orange Juice",
        )
        
        # Record CCP monitoring
        log = await haccp_manager.record_ccp_log(
            plan_id=plan.plan_id,
            ccp_name="Pasteurization",
            measurements={"temperature": 92.5, "time_seconds": 35},
        )
        
        assert log.within_limits == True
        
        # Verify compliance
        compliance = await haccp_manager.verify_compliance(plan.plan_id)
        assert compliance.is_compliant == True
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class FoodSafetyUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def get_temperature_readings(self):
        self.client.get("/api/v1/temperature/readings")
    
    @task(5)
    def submit_temperature_reading(self):
        self.client.post("/api/v1/temperature/readings", json={
            "sensor_id": f"SENSOR-{self.sensor_counter}",
            "temperature": 2.5,
            "recorded_at": datetime.utcnow().isoformat(),
        })
        self.sensor_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/temperature/readings", methods=["GET"])
@app.route("/api/v2/temperature/readings", methods=["GET"])
async def get_temperature_readings():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await get_temperature_readings_v2()
    return await get_temperature_readings_v1()
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

- **ATP**: Adenosine Triphosphate - bioluminescence test for surface cleanliness
- **CCP**: Critical Control Point - step in food process where control can be applied
- **CIP**: Clean-in-Place - automated cleaning of processing equipment
- **FSMA**: Food Safety Modernization Act - US FDA food safety regulations
- **GMP**: Good Manufacturing Practices - basic conditions for food production
- **HACCP**: Hazard Analysis Critical Control Points - systematic food safety approach
- **LIMS**: Laboratory Information Management System - software for lab data
- **PCQI**: Preventive Controls Qualified Individual - certified food safety person
- **SOP**: Standard Operating Procedure - documented process instructions
- **TTC**: Time-Temperature Control - food safety management for perishables

## Changelog

### Version 2.0.0 (2026-07-01)
- Added IoT temperature monitoring integration
- Implemented blockchain-anchored traceability
- Enhanced recall management with automated notifications
- Added environmental monitoring for Listeria

### Version 1.5.0 (2026-01-15)
- Added HACCP plan validation
- Implemented allergen management
- Enhanced supplier verification

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic HACCP management
- Temperature monitoring

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def check_temperature(
    sensor_id: str,
    temperature: Decimal,
) -> TemperatureResult:
    """Check temperature reading against limits.
    
    Args:
        sensor_id: Sensor identifier.
        temperature: Temperature reading.
    
    Returns:
        Temperature check result.
    
    Raises:
        SensorError: If sensor not found.
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

Copyright (c) 2026 Food Safety Technology Platform

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
