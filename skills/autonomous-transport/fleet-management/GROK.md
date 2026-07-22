---
name: "fleet-management"
category: "autonomous-transport"
version: "2.0.0"
tags: ["autonomous-transport", "fleet-management", "dispatch", "routing", "scheduling", "telematics", "fleet-ops"]
---

# Autonomous Fleet Management

## Overview

This module provides a comprehensive fleet management platform for autonomous vehicle fleets, covering dispatch and assignment, dynamic routing and re-routing, schedule optimization, telematics data collection and analysis, remote monitoring, charging/refueling management, and depot operations. It supports mixed fleets (autonomous + human-driven) with heterogeneous vehicle types (passenger, cargo, delivery) and integrates with ride-hailing platforms, logistics management systems, and city traffic management centers.

The platform operates in three modes: fully autonomous dispatch (no human dispatcher), semi-autonomous (human-in-the-loop for exception handling), and manual dispatch with automated recommendations. It includes a digital twin simulation environment for fleet-wide scenario testing and what-if analysis.

## Core Capabilities

- Real-time vehicle dispatch with multi-objective optimization (wait time, fuel, distance)
- Dynamic routing with live traffic, road closures, and demand forecasting
- Schedule optimization using constraint satisfaction and metaheuristic solvers
- Telematics data ingestion at 10+ Hz (GPS, CAN bus, accelerometer, LiDAR stats)
- Remote vehicle monitoring with real-time dashboard and alert system
- Autonomous vehicle health monitoring and predictive maintenance scheduling
- Charging/refueling scheduling for electric and hybrid fleet vehicles
- Depot management for parking, cleaning, and charging operations
- Fleet-wide digital twin for simulation and what-if analysis
- Integration with ride-hailing APIs (Uber, Lyft, DiDi) and logistics TMS
- Mixed fleet coordination (autonomous + human-driven vehicles)
- Demand forecasting using historical trip data and external signals
- Driver/vehicle assignment optimization for mixed fleets
- Multi-depot, multi-hub vehicle redistribution
- Regulatory compliance reporting (MOT, FMCSA, EU regulations)

## Advanced Configuration

### Platform Configuration

```yaml
fleet_management:
  fleet:
    fleet_id: "fleet_sf_001"
    region: "san_francisco"
    max_vehicles: 500
    vehicle_types:
      - type: "autonomous_passenger"
        count: 200
        capacity_pax: 4
        battery_capacity_kwh: 75
        range_km: 350
        charging_power_kw: 150
      - type: "autonomous_delivery"
        count: 100
        cargo_capacity_m3: 6.0
        cargo_weight_kg: 800
        range_km: 200
      - type: "human_driven"
        count: 100
        driver_shift_hours: 10
  dispatch:
    algorithm: "multi_objective"    # nearest | shortest_queue | multi_objective
    optimization_interval_s: 5
    rebalancing_enabled: true
    rebalancing_lookahead_min: 15
    pickup_tolerance_m: 50
    max_detour_ratio: 1.3           # max 30% detour for pooling
    pool_match_window_s: 30
    surge_threshold_ratio: 1.5      # demand/available vehicles
    idle_vehicle_timeout_s: 300
  routing:
    engine: "osrm"                  # osrm | valhalla | graphhopper
    traffic_provider: "tomtom"      # tomtom | google | HERE
    update_interval_s: 30
    route_freshness_s: 120
    avoid_tolls: false
    avoid_ferries: true
    max_route_alternatives: 3
  scheduling:
    solver: "or_tools"              # or_tools | optaPlanner | custom
    time_window_tolerance_s: 300
    max_vehicles_per_depot: 50
    shift_start_buffer_min: 15
    charging_buffer_percent: 20     # charge when below 20%
    maintenance_window_hours: 2
  telematics:
    ingestion_rate_hz: 10
    batch_size: 100
    retention_days: 90
    compression: "zstd"
    anomaly_detection: true
    anomaly_sensitivity: 0.95
  monitoring:
    heartbeat_interval_s: 5
    heartbeat_timeout_s: 15
    alert_channels: ["slack", "pagerduty", "email"]
    dashboard_refresh_s: 1
  digital_twin:
    enabled: true
    simulation_speed: 10            # 10x real-time
    scenario_library: "/scenarios/"
    max_concurrent_simulations: 5
```

### Dispatch Objective Weights

```yaml
dispatch:
  objectives:
    - name: "wait_time"
      weight: 0.4
      formula: "exp(-pickup_eta_s / 60)"
    - name: "ride_time"
      weight: 0.3
      formula: "1.0 / (1.0 + trip_duration_s / 1800)"
    - name: "fuel_cost"
      weight: 0.2
      formula: "1.0 - (fuel_consumed_kwh / battery_capacity_kwh)"
    - name: "pooling_efficiency"
      weight: 0.1
      formula: "shared_distance / total_distance"
```

## Architecture Patterns

### Platform Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │ Rider    │  │ Driver   │  │ Dispatcher│  │ Fleet Ops  │ │
│  │ App      │  │ App      │  │ Console  │  │ Dashboard  │ │
│  │ (iOS/    │  │ (iOS/    │  │ (Web)    │  │ (Web)      │ │
│  │ Android/ │  │ Android) │  │          │  │            │ │
│  │ Web)     │  │          │  │          │  │            │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────┬──────┘ │
├───────┴──────────────┴──────────────┴──────────────┴────────┤
│                    API GATEWAY                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  REST / gRPC / WebSocket                             │   │
│  │  Authentication: OAuth 2.0 + JWT                     │   │
│  │  Rate Limiting: Per-client token bucket              │   │
│  │  Load Balancer: Round-robin with health checks       │   │
│  └──────────────────────┬───────────────────────────────┘   │
├─────────────────────────┼───────────────────────────────────┤
│                    SERVICE LAYER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │ Dispatch │  │ Routing  │  │ Schedule │  │ Telematics │ │
│  │ Service  │  │ Service  │  │ Service  │  │ Ingestion  │ │
│  │          │  │          │  │          │  │            │ │
│  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────┐ │  │ ┌────────┐ │ │
│  │ │Matching   │ │ │OSRM/ │ │  │ │OR-   │ │  │ │Kafka   │ │ │
│  │ │Engine │ │  │ │Valhalla│ │  │ │Tools │ │  │ │Stream  │ │ │
│  │ └──────┘ │  │ └──────┘ │  │ └──────┘ │  │ └────────┘ │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │ Vehicle  │  │ Demand   │  │ Charging │  │ Digital    │ │
│  │ Health   │  │ Forecast │  │ Manager  │  │ Twin       │ │
│  │ Monitor  │  │ Service  │  │          │  │ Sim Engine │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    DATA LAYER                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │ PostGIS  │  │ Redis    │  │ TimescaleDB│ │ S3 / GCS  │ │
│  │ (trip    │  │ (real-   │  │ (telemetry│  │ (logs,    │ │
│  │  data,   │  │  time    │  │  time     │  │  backups) │ │
│  │  vehicle │  │  state)  │  │  series)  │  │           │ │
│  │  registry│  │          │  │          │  │           │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    INFRASTRUCTURE                            │
│  Kubernetes | Kafka | Envoy | Vault | Prometheus | Grafana │
└─────────────────────────────────────────────────────────────┘
```

### Dispatch Algorithm Flow

```
┌──────────────┐
│ Ride Request │
│ (pickup,     │
│  dropoff,    │
│  pax_count)  │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────┐
│ 1. FILTER: Remove unavailable vehicles   │
│    - Out of service area                 │
│    - Battery < charging_threshold        │
│    - Already on trip (unless pooling)    │
│    - Maintenance mode                    │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│ 2. CANDIDATE GENERATION                  │
│    - K-nearest idle vehicles (K=20)      │
│    - Current trip vehicles (pool match)  │
│    - ETA to pickup via routing engine    │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│ 3. SCORING: Multi-objective evaluation   │
│    Score = Σ(w_i × objective_i)          │
│    Objectives: wait, ride, fuel, pool    │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│ 4. CONSTRAINT CHECK                      │
│    - Vehicle capacity >= pax_count       │
│    - Detour ratio <= max_detour_ratio    │
│    - No time-window violations           │
│    - Regulatory zone compliance          │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│ 5. ASSIGNMENT: Best vehicle selected     │
│    - Reserve vehicle (Redis lock)        │
│    - Generate trip plan                  │
│    - Notify vehicle via V2X/comms        │
│    - Notify rider with ETA              │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│ 6. REBALANCING CHECK (async)             │
│    - Predict demand 15 min ahead         │
│    - Identify supply-demand gaps         │
│    - Send idle vehicles to high-demand   │
└──────────────────────────────────────────┘
```

### Vehicle State Machine

```
                        ┌────────────┐
              ┌────────▶│   IDLE     │◀────────┐
              │         └─────┬──────┘         │
              │               │                │
         (rebalance)    (ride assigned)   (trip complete)
              │               │                │
              │               ▼                │
              │         ┌────────────┐         │
              │         │ EN_ROUTE_  │         │
              │         │ TO_PICKUP  │         │
              │         └─────┬──────┘         │
              │               │                │
              │         (pickup arrived)        │
              │               │                │
              │               ▼                │
              │         ┌────────────┐         │
              │         │ ON_TRIP    │─────────┘
              │         └─────┬──────┘
              │               │
              │         (low battery /
              │          maintenance /
              │          shift end)
              │               │
              │               ▼
              │         ┌────────────┐
              └─────────│ RETURNING  │
                        │ TO_DEPOT   │
                        └─────┬──────┘
                              │
                        (depot arrived)
                              │
                              ▼
                        ┌────────────┐
                        │ CHARGING / │
                        │ MAINTENANCE│
                        └─────┬──────┘
                              │
                        (charge complete)
                              │
                              └──────▶ IDLE
```

## Integration Guide

### Dependencies

| Component | Version | Purpose |
|-----------|---------|---------|
| `fleet-core` | >= 4.0.0 | Vehicle registry, trip management |
| `routing-engine` | >= 3.0.0 | OSRM / Valhalla route computation |
| `telemetry-store` | >= 2.5.0 | TimescaleDB for time-series telematics |
| `realtime-state` | >= 2.0.0 | Redis-backed real-time vehicle state |
| `demand-forecast` | >= 1.5.0 | ML-based demand prediction |
| `charging-manager` | >= 1.0.0 | EV charging scheduling and station management |
| `common-msgs` | >= 2.0.0 | Shared protobuf definitions |
| `auth-service` | >= 2.0.0 | OAuth 2.0 / JWT authentication |

### REST API Integration

```python
import httpx
from fleet_core.models import Vehicle, Trip, DispatchRequest

class FleetAPIClient:
    def __init__(self, base_url: str, api_key: str):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10.0
        )

    async def dispatch(self, request: DispatchRequest) -> Trip:
        """Submit a dispatch request and receive an assigned trip."""
        resp = await self.client.post("/api/v2/dispatch", json=request.to_dict())
        resp.raise_for_status()
        return Trip.from_dict(resp.json())

    async def get_vehicle_status(self, vehicle_id: str) -> Vehicle:
        """Get real-time vehicle status."""
        resp = await self.client.get(f"/api/v2/vehicles/{vehicle_id}")
        resp.raise_for_status()
        return Vehicle.from_dict(resp.json())

    async def rebalance(self, zone: str) -> list[dict]:
        """Trigger demand-based rebalancing for a zone."""
        resp = await self.client.post(f"/api/v2/fleet/rebalance", json={"zone": zone})
        resp.raise_for_status()
        return resp.json()["assignments"]

    async def get_trip_updates(self, trip_id: str) -> dict:
        """Get real-time trip progress updates."""
        resp = await self.client.get(f"/api/v2/trips/{trip_id}/updates")
        resp.raise_for_status()
        return resp.json()
```

### WebSocket Real-Time Updates

```python
import websockets
import json

async def subscribe_vehicle_updates(vehicle_ids: list[str]):
    async with websockets.connect("wss://api.fleet.example.com/ws/vehicles") as ws:
        await ws.send(json.dumps({
            "action": "subscribe",
            "vehicle_ids": vehicle_ids,
            "fields": ["position", "speed", "battery", "status"]
        }))
        async for message in ws:
            update = json.loads(message)
            process_vehicle_update(update)
```

### Message Interface

```protobuf
// DispatchRequest
message DispatchRequest {
  string request_id = 1;
  string rider_id = 2;
  Position pickup = 3;
  Position dropoff = 4;
  int32 passenger_count = 5;
  string vehicle_type = 6;          // "passenger", "delivery"
  bool pooling_allowed = 7;
  int64 requested_time_s = 8;       // 0 = now
  map<string, string> metadata = 9;
}

// Trip (assigned)
message Trip {
  string trip_id = 1;
  string vehicle_id = 2;
  string rider_id = 3;
  Position pickup = 4;
  Position dropoff = 5;
  Route route = 6;
  float estimated_duration_s = 7;
  float estimated_distance_m = 8;
  float estimated_fare = 9;
  TripStatus status = 10;
  repeated TripUpdate updates = 11;
}

// Vehicle Telematics
message TelematicsData {
  string vehicle_id = 1;
  int64 timestamp_ms = 2;
  Position position = 3;
  float heading_deg = 4;
  float speed_mps = 5;
  float battery_percent = 6;
  float battery_voltage = 7;
  float motor_temperature_c = 8;
  float tire_pressure_psi = 9;
  repeated float accelerometer = 10; // [x, y, z]
  repeated float gyroscope = 11;     // [x, y, z]
  VehicleHealthStatus health = 12;
  map<string, float> can_signals = 13;
}
```

## Performance Optimization

### Dispatch Latency Budget

| Stage | Budget (ms) | Technique |
|-------|-------------|-----------|
| Request validation | 2 | Schema validation + auth check |
| Vehicle filtering | 5 | Redis spatial index (GeoHash) |
| Candidate generation | 10 | K-NN on pre-computed distances |
| Routing (pickup ETA) | 30 | Cached routing with live traffic delta |
| Multi-objective scoring | 3 | Vectorized NumPy scoring |
| Constraint checking | 2 | Pre-filtered constraint sets |
| Assignment commit | 5 | Redis atomic transaction |
| Notification dispatch | 3 | Async pub/sub to vehicle |
| **Total** | **60** | **Target: < 100 ms p99** |

### Telematics Ingestion Pipeline

```
Vehicle (10 Hz)
    │
    │  ┌──────────────────────────────────────────────────┐
    │  │  Kafka Ingestion Layer                           │
    │  │  Topic: telematics.{fleet_id}.{vehicle_type}     │
    │  │  Partitions: 32 (by vehicle_id hash)             │
    │  │  Replication factor: 3                           │
    │  └──────────────────────┬───────────────────────────┘
    │                         │
    │  ┌──────────────────────▼───────────────────────────┐
    │  │  Stream Processing (Flink / Kafka Streams)        │
    │  │  1. Deserialize protobuf                          │
    │  │  2. Validate schema                               │
    │  │  3. Anomaly detection (z-score on speed/accel)    │
    │  │  4. Aggregate 1-second windows (avg, min, max)    │
    │  │  5. Write to TimescaleDB (hypertable)             │
    │  │  6. Update Redis (real-time state)                │
    │  └──────────────────────┬───────────────────────────┘
    │                         │
    │  ┌──────────────────────▼───────────────────────────┐
    │  │  Storage Layer                                    │
    │  │  TimescaleDB: 90-day retention, compression       │
    │  │  S3: Long-term archive (Parquet, 1-year retention)│
    │  │  Redis: Current state (TTL 30s)                   │
    │  └──────────────────────────────────────────────────┘
```

### Caching Strategy

| Data | Cache Layer | TTL | Invalidation |
|------|------------|-----|-------------|
| Vehicle position | Redis | 5 s | Telematics update |
| Route segments | In-memory LRU | 120 s | Traffic update event |
| Demand forecast | Redis | 300 s | New forecast computation |
| Station availability | Redis | 10 s | Charging event |
| Trip fare estimate | Redis | 60 s | Route update |

### Database Optimization

- **TimescaleDB hypertable partitioning**: Auto-partition by time (1-day chunks) with compression after 7 days.
- **PostGIS spatial indexing**: GiST index on vehicle positions for fast spatial queries.
- **Connection pooling**: PgBouncer with 50 connections for the dispatch service.
- **Read replicas**: Route and schedule queries against read replicas to reduce primary load.
- **Bulk inserts**: Telematics ingestion uses COPY protocol for 100k+ inserts/second.

## Security Considerations

### Data Protection

- All PII (rider ID, trip history, payment) encrypted at rest (AES-256) and in transit (TLS 1.3).
- Trip data anonymized after 30 days; rider IDs replaced with pseudonymous tokens.
- Telematics data does not contain rider PII; vehicle positions are aggregated for analytics.
- GDPR/CCPA compliance: right-to-erasure API endpoint for rider trip data deletion.

### Access Control

```
┌──────────────────────────────────────────────────┐
│              Role-Based Access Control             │
│                                                    │
│  Role              Permissions                     │
│  ─────────────────────────────────────────────     │
│  fleet_admin       All operations                 │
│  dispatcher        Dispatch, rebalance, assign     │
│  vehicle_ops       Vehicle status, telematics      │
│  maintenance       Health data, maintenance schedule│
│  analyst           Read-only analytics, reports     │
│  rider             Own trip data only              │
│  api_external      Dispatch requests only (scoped) │
└──────────────────────────────────────────────────┘
```

### API Security

- OAuth 2.0 with PKCE for mobile app authentication.
- API key + HMAC-SHA256 signature for server-to-server calls.
- Rate limiting: 100 req/s per API key, 1000 req/s per fleet account.
- Request payload size limit: 1 MB (dispatch), 100 KB (telematics batch).
- IP allowlisting for administrative endpoints.

### Vehicle Communication Security

- End-to-end encryption (TLS 1.3) for all vehicle-to-cloud communication.
- Mutual TLS (mTLS) with per-vehicle client certificates.
- OTA update signing with RSA-4096; rollback protection via anti-replay nonces.
- Command authentication: all remote vehicle commands require fleet_admin or dispatcher role + HMAC.

## Troubleshooting Guide

| Symptom | Probable Cause | Diagnostic Steps | Resolution |
|---------|---------------|------------------|------------|
| Dispatch latency > 200 ms | Routing engine overload | Check OSRM CPU usage; review route cache hit rate | Scale routing engine horizontally; increase route cache TTL |
| Vehicle not receiving assignments | Redis lock stuck | Check vehicle state in Redis; look for orphaned locks | Clear stale locks; restart dispatch service |
| Telematics gaps in data | Vehicle network disconnectivity | Check vehicle heartbeat timestamps; inspect Kafka consumer lag | Investigate vehicle cellular connection; add retry buffering |
| Demand forecast inaccurate | Insufficient training data or stale model | Compare predicted vs actual demand; check model age | Retrain model with recent data; add external signals (events, weather) |
| Charging schedule conflicts | Multiple vehicles assigned same charger | Check charging_manager allocation table | Implement charger reservation locking; add 10-min buffer between sessions |
| Trip ETA consistently wrong | Traffic data stale or route engine bug | Compare predicted vs actual trip durations; check traffic data freshness | Reduce route update interval; validate traffic API subscription |
| Fleet-wide vehicle dropout | Network infrastructure issue | Check cellular gateway status; review fleet heartbeat aggregate | Investigate regional network outage; switch to backup communication channel |
| Rebalancing creates deadlocks | Circular vehicle movements | Review rebalancing assignments; check zone graph connectivity | Add randomness to rebalancing; cap moves per zone per cycle |
| Memory leak in telematics service | Unbounded Kafka consumer buffers | Monitor heap usage; check for growing channel buffer sizes | Set consumer max.poll.records; implement backpressure |

## API Reference

### Dispatch Service

```python
class DispatchService:
    def __init__(self, fleet_id: str, routing_engine: RoutingEngine):
        """Initialize dispatch service with fleet context."""

    async def request_dispatch(self, request: DispatchRequest) -> DispatchResult:
        """Process a dispatch request and return vehicle assignment.

        Returns:
            DispatchResult with assigned vehicle, ETA, trip plan,
            or rejection with reason.
        """

    async def cancel_dispatch(self, trip_id: str, reason: str) -> bool:
        """Cancel an active dispatch and release the vehicle."""

    async def pool_match(self, trip_a: Trip, trip_b: Trip) -> PoolMatchResult:
        """Evaluate if two trips can be pooled with acceptable detour."""

    async def rebalance_zone(self, zone_id: str) -> list[VehicleAssignment]:
        """Rebalance vehicle supply in a zone based on demand forecast."""
```

### Telematics Service

```python
class TelematicsService:
    def __init__(self, kafka_config: dict, db_pool: asyncpg.Pool):
        """Initialize telematics ingestion pipeline."""

    async def ingest_batch(self, data: list[TelematicsData]) -> IngestResult:
        """Ingest a batch of telematics records.

        Validates, detects anomalies, and writes to storage.
        """

    async def get_vehicle_history(self, vehicle_id: str,
                                   start: datetime, end: datetime) -> list[TelematicsData]:
        """Query historical telematics data for a vehicle."""

    async def get_fleet_snapshot(self) -> FleetSnapshot:
        """Return current state of all vehicles in the fleet."""

    async def detect_anomalies(self, vehicle_id: str,
                                window_s: int = 300) -> list[Anomaly]:
        """Run anomaly detection on recent telematics data."""
```

### Routing Service

```python
class RoutingService:
    def __init__(self, engine: str = "osrm"):
        """Initialize routing engine adapter."""

    async def compute_route(self, origin: Position, destination: Position,
                            alternatives: int = 3) -> list[Route]:
        """Compute route alternatives with current traffic conditions."""

    async def compute_eta(self, origin: Position, destination: Position) -> float:
        """Quick ETA computation without full route details."""

    async def update_traffic(self, traffic_update: TrafficUpdate) -> None:
        """Apply real-time traffic data to routing graph."""

    async def get_road_segments(self, bbox: BoundingBox) -> list[RoadSegment]:
        """Return road segment details within a bounding box."""
```

### Charging Manager

```python
class ChargingManager:
    def __init__(self, stations: list[ChargingStation]):
        """Initialize with available charging stations."""

    async def schedule_charging(self, vehicle_id: str,
                                 battery_percent: float,
                                 next_trip_eta: float) -> ChargingSchedule:
        """Schedule optimal charging session.

        Considers: charger availability, electricity cost (time-of-use),
        vehicle battery degradation, and upcoming trip requirements.
        """

    async def reserve_charger(self, charger_id: str,
                               vehicle_id: str,
                               time_window: TimeWindow) -> Reservation:
        """Reserve a charger for a specific time window."""

    async def get_station_status(self, station_id: str) -> StationStatus:
        """Return real-time charger availability and queue length."""
```

## Data Models

### Vehicle State

```
Vehicle:
├── vehicle_id: UUID
├── type: enum (AUTONOMOUS_PASSENGER, AUTONOMOUS_DELIVERY, HUMAN_DRIVEN)
├── status: VehicleStatus
│   ├── operational: enum (ACTIVE, INACTIVE, MAINTENANCE, CHARGING)
│   ├── trip_state: enum (IDLE, EN_ROUTE_TO_PICKUP, ON_TRIP, RETURNING_TO_DEPOT)
│   └── health: enum (HEALTHY, WARNING, CRITICAL, OFFLINE)
├── position:
│   ├── lat: float64
│   ├── lon: float64
│   ├── heading_deg: float32
│   └── accuracy_m: float32
├── capabilities:
│   ├── passenger_capacity: int32
│   ├── cargo_capacity_m3: float32
│   ├── cargo_weight_kg: float32
│   ├── wheelchair_accessible: bool
│   ├── child_seat: bool
│   └── autonomic_level: enum (L2, L3, L4, L5)
├── energy:
│   ├── battery_percent: float32
│   ├── battery_kwh: float32
│   ├── range_km: float32
│   ├── charging_power_kw: float32
│   └── charging_status: enum (NOT_CHARGING, CHARGING, FULL)
├── health:
│   ├── odometer_km: float64
│   ├── tire_pressure: map<string, float32>
│   ├── brake_pad_mm: float32
│   ├── motor_temperature_c: float32
│   ├── last_maintenance_date: date
│   └── next_maintenance_km: float64
└── telemetry:
    ├── last_heartbeat_s: int64
    ├── speed_mps: float32
    ├── accel_mps2: list<float32>  # [x, y, z]
    └── can_signals: map<string, float32>
```

### Trip Model

```
Trip:
├── trip_id: UUID
├── request_id: UUID
├── rider_id: UUID (nullable for delivery)
├── vehicle_id: UUID
├── status: TripStatus
│   ├── requested → assigned → vehicle_en_route →
│   │   arrived_at_pickup → boarding → en_route →
│   │   arrived_at_dropoff → completed | cancelled
│   └── cancellation_reason: string (nullable)
├── pickup:
│   ├── position: {lat, lon}
│   ├── address: string
│   └── time_window: {earliest, latest}
├── dropoff:
│   ├── position: {lat, lon}
│   ├── address: string
│   └── time_window: {earliest, latest}
├── route:
│   ├── segments: list<RouteSegment>
│   ├── total_distance_m: float64
│   ├── total_duration_s: float64
│   └── traffic_conditions: enum (FREE_FLOW, MODERATE, CONGESTED, GRIDLOCK)
├── pooling:
│   ├── is_pooled: bool
│   ├── pool_id: UUID (nullable)
│   ├── co_riders: list<UUID>
│   └── detour_ratio: float32
├── fare:
│   ├── base_fare: float32
│   ├── distance_fare: float32
│   ├── time_fare: float32
│   ├── surge_multiplier: float32
│   ├── discount: float32
│   └── total_fare: float32
└── timestamps:
    ├── requested_at: datetime
    ├── assigned_at: datetime
    ├── pickup_arrived_at: datetime
    ├── trip_started_at: datetime
    ├── trip_completed_at: datetime
    └── total_wait_s: float64
```

### Telematics Schema (TimescaleDB)

```sql
CREATE TABLE telematics (
    time         TIMESTAMPTZ NOT NULL,
    vehicle_id   UUID NOT NULL,
    lat          DOUBLE PRECISION,
    lon          DOUBLE PRECISION,
    heading      REAL,
    speed        REAL,
    battery_pct  REAL,
    battery_v    REAL,
    motor_temp   REAL,
    tire_pressure JSONB,
    accel_x      REAL,
    accel_y      REAL,
    accel_z      REAL,
    gyro_x       REAL,
    gyro_y       REAL,
    gyro_z       REAL,
    can_signals  JSONB
);

SELECT create_hypertable('telematics', 'time',
    chunk_time_interval => INTERVAL '1 day');

-- Compression policy: compress chunks older than 7 days
ALTER TABLE telematics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'vehicle_id',
    timescaledb.compress_orderby = 'time DESC'
);

SELECT add_compression_policy('telematics', INTERVAL '7 days');

-- Retention policy: drop chunks older than 90 days
SELECT add_retention_policy('telematics', INTERVAL '90 days');
```

### Demand Forecast Model

```
DemandForecast:
├── zone_id: string
├── timestamp: datetime
├── predicted_demand: int32
├── confidence_interval: {lower: int32, upper: int32}
├── features_used:
│   ├── historical_demand_1h: float32
│   ├── historical_demand_24h: float32
│   ├── day_of_week: int8
│   ├── hour_of_day: int8
│   ├── is_holiday: bool
│   ├── weather_condition: enum
│   ├── temperature_c: float32
│   ├── nearby_events: list<Event>
│   └── public_transit_disruption: bool
└── model_version: string
```

## Deployment Guide

### Hardware Requirements (Cloud)

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Dispatch Service | 2 vCPU, 4 GB RAM | 4 vCPU, 8 GB RAM (x3 replicas) |
| Routing Engine | 4 vCPU, 8 GB RAM | 8 vCPU, 16 GB RAM (x2 replicas) |
| Telematics Ingestion | 4 vCPU, 8 GB RAM | 8 vCPU, 16 GB RAM (x3 replicas) |
| TimescaleDB | 8 vCPU, 32 GB RAM, 500 GB SSD | 16 vCPU, 64 GB RAM, 2 TB NVMe |
| Redis Cluster | 3 nodes, 4 GB each | 6 nodes, 16 GB each (cluster mode) |
| Kafka Cluster | 3 brokers, 8 vCPU, 16 GB | 6 brokers, 16 vCPU, 32 GB |

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dispatch-service
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: dispatch-service
  template:
    metadata:
      labels:
        app: dispatch-service
    spec:
      containers:
      - name: dispatch
        image: registry.example.com/dispatch-service:v2.0.0
        ports:
        - containerPort: 8080
        - containerPort: 9090  # metrics
        env:
        - name: FLEET_ID
          value: "fleet_sf_001"
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: fleet-secrets
              key: redis-url
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: fleet-secrets
              key: database-url
        resources:
          limits:
            cpu: "4"
            memory: "8Gi"
          requests:
            cpu: "2"
            memory: "4Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          periodSeconds: 5
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]  # drain connections
```

### Database Migration

```bash
# Run pending migrations
fleetctl db migrate --target latest

# Backup before migration
fleetctl db backup --name pre-v2.0-migration

# Verify migration
fleetctl db verify --version 2.0.0
```

## Monitoring and Observability

### Key Metrics

| Metric | Type | Unit | Alert Threshold |
|--------|------|------|-----------------|
| `dispatch_latency_p99_ms` | Histogram | ms | > 150 |
| `dispatch_success_rate` | Gauge | ratio | < 0.95 |
| `dispatch_rejection_rate` | Gauge | ratio | > 0.1 |
| `fleet_utilization` | Gauge | ratio | < 0.5 (low demand) |
| `fleet_active_vehicles` | Gauge | count | — |
| `fleet_idle_vehicles` | Gauge | count | — |
| `telematics_ingestion_rate` | Gauge | records/s | < 1000 (per fleet) |
| `telematics_kafka_lag` | Gauge | records | > 10000 |
| `vehicle_health_warning` | Gauge | count | > 5 |
| `vehicle_health_critical` | Gauge | count | > 0 |
| `charging_station_utilization` | Gauge | ratio | > 0.95 (queuing) |
| `demand_forecast_mape` | Gauge | percent | > 25 |
| `trip_eta_accuracy_mae` | Gauge | seconds | > 120 |
| `pooling_rate` | Gauge | ratio | — |

### Grafana Dashboard

- **Fleet Overview Map**: Real-time vehicle positions on a map with status color coding
- **Dispatch Pipeline**: Request → filter → score → assign pipeline latency breakdown
- **Demand Heatmap**: Zone-level demand vs supply over time
- **Vehicle Health Grid**: All vehicles with health indicators (green/yellow/red)
- **Charging Status**: Station utilization, queue lengths, energy consumed
- **Telematics Pipeline**: Kafka consumer lag, ingestion rate, anomaly count
- **Business Metrics**: Trip count, revenue, utilization rate, rider satisfaction

### Alerting Rules

```yaml
alerts:
  - name: "dispatch_latency_high"
    condition: "dispatch_latency_p99_ms > 150"
    for: "5m"
    severity: "warning"
    channels: ["slack"]

  - name: "vehicle_critical_health"
    condition: "vehicle_health_critical > 0"
    for: "0m"
    severity: "critical"
    channels: ["pagerduty", "slack"]

  - name: "fleet_idle_too_many"
    condition: "fleet_idle_vehicles / fleet_active_vehicles > 0.7"
    for: "15m"
    severity: "info"
    channels: ["slack"]
    action: "Trigger rebalancing in high-demand zones"

  - name: "charging_station_full"
    condition: "charging_station_utilization > 0.95"
    for: "10m"
    severity: "warning"
    channels: ["slack", "email"]
```

### Distributed Tracing

```
TRACE_ID: 8a2f1b3e-...
├── api_gateway.validate_request              [2 ms]
├── dispatch_service.request_dispatch        [58 ms]
│   ├── vehicle_filter.spatial_query          [5 ms]
│   ├── routing_service.compute_eta          [32 ms]
│   │   ├── osrm.route_query                 [28 ms]
│   │   └── traffic_enrichment               [4 ms]
│   ├── scoring.multi_objective_evaluate     [3 ms]
│   ├── constraint_check.validate            [2 ms]
│   ├── assignment.commit                    [5 ms]
│   │   └── redis.setnx_lock                 [1 ms]
│   └── notification.dispatch_async          [3 ms]
│       └── kafka.produce                    [1 ms]
└── response_serialization                   [1 ms]
```

## Testing Strategy

### Unit Tests

- **Dispatch scoring**: Verify each objective weight produces expected ranking for known vehicle configurations.
- **Route computation**: Mock routing engine; verify ETA and distance calculations.
- **Demand forecast**: Validate model predictions against held-out test data (MAPE < 20%).
- **Charging schedule**: Verify optimal charger assignment with known constraints.
- **Constraint validation**: Edge cases (zero capacity, out-of-range battery, expired maintenance).

### Integration Tests

- **End-to-end dispatch**: Submit ride request → receive assignment → verify vehicle position moves to pickup.
- **Multi-vehicle coordination**: 10 concurrent dispatch requests → verify no double-assignments.
- **Telematics pipeline**: Insert batch → verify TimescaleDB writes and Redis state updates.
- **Rebalancing**: Simulate demand spike → verify idle vehicles move to high-demand zone.

### Load Tests

- **Dispatch throughput**: 1000 requests/second sustained for 10 minutes.
- **Telematics ingestion**: 10,000 vehicles × 10 Hz = 100,000 records/second.
- **Route computation**: 500 concurrent route requests with < 50 ms p99.
- **Database**: 1 million trip records queryable in < 500 ms.

### Digital Twin Simulation

```
┌──────────────────────────────────────────┐
│          Digital Twin Simulation          │
│                                           │
│  ┌──────────┐    ┌──────────────────┐    │
│  │ Demand   │───▶│ Fleet Simulator  │    │
│  │ Generator│    │ (SUMO / custom)  │    │
│  └──────────┘    └────────┬─────────┘    │
│                           │               │
│  ┌────────────────────────▼──────────┐   │
│  │  Evaluation Metrics:              │   │
│  │  - Average wait time              │   │
│  │  - Fleet utilization              │   │
│  │  - Revenue per vehicle-hour       │   │
│  │  - Rebalancing distance           │   │
│  │  - Rider satisfaction score       │   │
│  └───────────────────────────────────┘   │
└──────────────────────────────────────────┘
```

## Versioning and Migration

### Semantic Versioning

- **MAJOR**: Breaking API changes, database schema changes, new fleet model.
- **MINOR**: New dispatch algorithms, new telematics fields, backward-compatible.
- **PATCH**: Bug fixes, performance improvements, configuration changes.

### Migration Guide (v1.x → v2.0)

1. Update `fleetctl` CLI: `pip install fleet-management==2.0.0`
2. Run database migration: `fleetctl db migrate --target 2.0.0`
3. Update API client to v2 endpoints (`/api/v2/` prefix).
4. Migrate dispatch configuration to new YAML schema (see Advanced Configuration).
5. Update vehicle firmware to support new telematics message format.
6. Verify all integrations with the v2 API using the integration test suite.

### Deprecation Policy

- Deprecated REST endpoints return `Sunset` header with removal date.
- Deprecated fields in protobuf messages are annotated with `deprecated = true`.
- Two minor-version deprecation window before removal.

## Glossary

| Term | Definition |
|------|-----------|
| **Dispatch** | Process of matching a ride request to an available vehicle |
| **Rebalancing** | Repositioning idle vehicles to areas of anticipated demand |
| **Pooling** | Combining multiple ride requests into a single vehicle trip |
| **Detour Ratio** | Ratio of pooled trip distance to direct trip distance |
| **Telematics** | Vehicle sensor data (GPS, CAN bus, accelerometer) transmitted to cloud |
| **Hyperlocal** | Geographic zone for demand forecasting (typically 200-500 m radius) |
| **Utilization** | Percentage of time a vehicle is carrying passengers vs idle |
| **Deadheading** | Driving without passengers (to pickup or rebalance) |
| **Surge Pricing** | Dynamic fare multiplier when demand exceeds supply |
| **Time-of-Use Charging** | Scheduling EV charging during off-peak electricity rate periods |
| **Digital Twin** | Virtual replica of the fleet for simulation and scenario testing |
| **Geofence** | Virtual boundary defining operational area or restricted zone |
| **Or-Tools** | Google's open-source optimization library for routing and scheduling |
| **TimescaleDB** | PostgreSQL extension optimized for time-series data |
| **Hypertable** | TimescaleDB's partitioned time-series table abstraction |
| **OSRM** | Open Source Routing Machine — high-performance routing engine |

## Changelog

### v2.0.0 (2025-06-15)

- Added digital twin simulation engine
- Added demand forecasting with ML models (historical + external signals)
- Added multi-depot vehicle redistribution
- Added mixed fleet coordination (autonomous + human-driven)
- New multi-objective dispatch algorithm
- New charging manager with time-of-use optimization
- Added Kubernetes deployment manifests
- Migrated telematics pipeline to Kafka Streams

### v1.3.0 (2025-02-01)

- Added pooling / ride-sharing dispatch mode
- Added real-time rebalancing based on demand prediction
- Improved dispatch latency (p99 from 150 ms to 60 ms)

### v1.2.0 (2024-10-15)

- Added vehicle health monitoring and predictive maintenance
- Added charging station management
- Added WebSocket real-time updates

### v1.1.0 (2024-07-01)

- Added telematics ingestion pipeline
- Added TimescaleDB for time-series storage
- Added basic demand heatmaps

### v1.0.0 (2024-04-01)

- Initial release with basic dispatch, routing, and vehicle tracking
- REST API for ride requests and vehicle management

## Contributing Guidelines

### Development Workflow

1. Fork the repository and create a feature branch from `main`.
2. Implement changes with unit and integration tests.
3. Run the full test suite: `make test-ci`
4. Run load tests for any dispatch or telematics changes: `make load-test`
5. Submit a pull request with:
   - Description of changes
   - Performance benchmarks (latency, throughput)
   - Database migration scripts (if applicable)
6. Request review from fleet operations and platform engineering teams.

### Code Standards

- Python: PEP 8 with `ruff` linting, `mypy` strict mode
- TypeScript (dashboard): ESLint with strict rules
- All database changes require migration scripts with rollback
- API changes must be backward-compatible within a minor version
- Performance-critical code must include benchmarks in PR description

### Commit Convention

Use Conventional Commits: `feat(dispatch): add multi-objective scoring with pooling support`

### Testing Requirements

- Unit test coverage: minimum 80% for new code
- Integration tests for all API endpoints
- Load tests for dispatch and telematics ingestion paths
- Digital twin simulation test for new dispatch algorithms

## License

Apache License, Version 2.0. See the repository root `LICENSE` file for full text.

Copyright 2024-2025 Awesome Grok Skills Contributors.
