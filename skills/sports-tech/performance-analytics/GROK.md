---
name: "performance-analytics"
category: "sports-tech"
version: "1.0.0"
tags: ["sports-tech", "performance-analytics", "xg-models", "match-statistics"]
---

# Performance Analytics — Advanced Sports Metrics & Match Analysis

## Overview

Performance analytics in sports technology represents the quantitative backbone of modern athletic decision-making. This module provides a comprehensive toolkit for ingesting, processing, and analyzing player and team performance data across multiple sports — with primary emphasis on football (soccer), basketball, and American football. The analytics pipeline covers everything from raw event-level match data (passes, shots, tackles, dribbles) to derived expected models (xG, xA, xT) that quantify the probabilistic value of on-field actions.

At its core, the module implements a multi-layered analytics architecture. The foundational layer handles data normalization across disparate data providers (Opta, StatsBomb, Second Spectrum, Hudl) into a unified schema. The statistical layer applies Bayesian estimation, hierarchical modeling, and Monte Carlo simulation to produce robust player ratings that account for sample size, opposition strength, and match context. The visualization layer generates pitch-level heatmaps, pass networks, and shot maps suitable for coaching staff presentations and broadcast graphics.

The module also includes a full expected goals (xG) model trained on historical shot data, featuring features such as distance to goal, angle to goal, body part used, assist type, defensive pressure index, and goalkeeper positioning score. Beyond xG, the module computes expected assists (xA) from pass sequences, expected threat (xT) for progressive ball progression, and possession value chains that attribute credit across multi-pass attacking sequences.

## Core Capabilities

- **xG Model Engine**: Logistic regression and gradient-boosted expected goals models with 40+ shot features, per-shot probability output, and post-shot xG (PSxG) for goalkeeper evaluation
- **Match Event Normalization**: Unified schema converter for Opta F24, StatsBomb JSON, Wyscout CSV, and Second Spectrum tracking data with automatic provider detection
- **Player Rating System**: Bayesian-adjusted player ratings with positional weighting, minutes-adjusted per-90 statistics, and rolling form indices over configurable windows
- **Pass Network & Heatmap Generation**: Graph-based pass network construction with clustering, plus kernel density estimation heatmaps for spatial activity distributions
- **Possession Value Chains (xT)**: Markov chain-based expected threat model that values each on-ball action by the probability of a goal resulting from the possession state
- **Fatigue & Workload Indicators**: Cumulative load tracking with acute:chronic workload ratio computation, high-intensity running distance, and sprint count thresholds
- **Opponent Scouting Reports**: Automated tactical dossier generation including formation identification, pressing triggers, set-piece tendencies, and key player profiles
- **Historical Trend Analysis**: Longitudinal performance tracking with rolling averages, era-adjusted comparisons, and cross-league benchmarking with normalization factors

## Usage Examples

### Basic xG Calculation

```python
from performance_analytics import ExpectedGoalsModel, ShotEvent

# Initialize the xG model with pre-trained weights
xg_model = ExpectedGoalsModel(model_type="gradient_boosting")

# Create a shot event
shot = ShotEvent(
    event_id="shot_001",
    player_id="p_messi_10",
    team_id="barcelona",
    match_id="match_2024_01",
    x=88.5, y=42.3,  # pitch coordinates (0-100)
    period=2,
    timestamp=4523.7,
    body_part="right_foot",
    assist_type="through_ball",
    first_time=True,
    under_pressure=True,
    distance_to_goal=14.2,
    angle_to_goal=23.5,
    defenders_in_cone=2,
    goalkeeper_distance=4.8,
)

# Compute xG
result = xg_model.predict(shot)
print(f"Shot xG: {result.xg:.4f}")
print(f"Shot xG breakdown: {result.feature_contributions}")
```

### Match Performance Summary

```python
from performance_analytics import MatchAnalyzer, DataProvider

# Initialize with data from a specific match
analyzer = MatchAnalyzer(
    match_id="match_2024_01",
    home_team="barcelona",
    away_team="real_madrid",
    data_provider=DataProvider.STATSBOMB,
)

# Generate comprehensive match report
report = analyzer.generate_report()

# Access individual metrics
print(f"Barcelona xG: {report.home_xg:.2f}")
print(f"Real Madrid xG: {report.away_xg:.2f}")
print(f"Barcelona possession value: {report.home_possession_value:.2f}")

# Get player-level breakdown
for player in report.top_performers(n=5):
    print(f"{player.name}: {player.rating:.1f} | xG+xA: {player.xg_plus_xa:.2f}")
```

### Pass Network Analysis

```python
from performance_analytics import PassNetworkBuilder

builder = PassNetworkBuilder(
    match_id="match_2024_01",
    team_id="barcelona",
    min_passes=3,  # minimum passes between pair to include
    normalize_by_possession=True,
)

network = builder.build()

# Identify key passing triangles
triangles = network.find_clustering(method="louvain", resolution=0.8)
for cluster in triangles:
    print(f"Cluster: {[p.name for p in cluster.players]}")
    print(f"  Intra-cluster pass rate: {cluster.internal_pass_rate:.1%}")
    print(f"  Key connector: {cluster.connector_player.name}")

# Generate visualization data
viz = network.to_plotly_data()
```

### Player Benchmarking Across Leagues

```python
from performance_analytics import LeagueBenchmark, Position

benchmark = LeagueBenchmark(
    leagues=["premier_league", "la_liga", "bundesliga", "serie_a", "ligue_1"],
    season=2024,
    position=Position.MIDFIELDER,
    minutes_threshold=900,
)

# Compare a player against league medians
comparison = benchmark.compare_player(
    player_id="p_bellingham_5",
    metrics=["progressive_passes", "tackles_won", "xg_plus_xa", "aerial_duels_won"],
)

for metric, stats in comparison.items():
    print(f"{metric}: {stats.player_value:.2f} "
          f"(league median: {stats.league_median:.2f}, "
          f"percentile: {stats.percentile:.0f})")
```

## Best Practices

1. **Always normalize by minutes played** — raw totals mislead when comparing players with different playing time. Use per-90 or per-100-touch metrics as the default comparison unit.

2. **Apply Bayesian shrinkage for small samples** — players with fewer than ~500 minutes of data should have their statistics regressed toward positional means to avoid overfitting to noise.

3. **Use pitch coordinates consistently** — adopt a single coordinate system (typically 0-100 for both axes) and convert provider-specific formats during ingestion, never downstream.

4. **Account for match state** — a goal scored at 3-0 in the 85th minute carries different tactical weight than one at 0-0 in the 30th. Filter or weight events by match state when doing tactical analysis.

5. **Validate xG models against calibration curves** — plot predicted vs. observed goal rates in bins. A well-calibrated model should fall along the diagonal. Retrain when calibration drifts beyond acceptable thresholds.

6. **Distinguish correlation from causation in player ratings** — high ratings may reflect team quality rather than individual contribution. Use possession-adjusted metrics and opponent strength weighting.

7. **Version your model weights and training data** — reproducibility requires locking the exact dataset, feature set, and hyperparameters used for each model version. Store as artifacts alongside the code.

8. **Report confidence intervals, not point estimates** — every metric should carry an uncertainty band. A player with 0.35 xG from 10 shots is very different from 0.35 xG from 80 shots.

## Data Schema

The module operates on a normalized event-level schema that abstracts away provider-specific formats:

```json
{
  "event_id": "uuid",
  "match_id": "string",
  "team_id": "string",
  "player_id": "string",
  "timestamp": "float (seconds from kickoff)",
  "period": "int (1, 2, or extra time)",
  "event_type": "pass | shot | carry | tackle | ...",
  "x": "float (0-100 pitch coordinate)",
  "y": "float (0-100 pitch coordinate)",
  "end_x": "float (optional)",
  "end_y": "float (optional)",
  "outcome": "successful | unsuccessful | ...",
  "meta": "dict (provider-specific extensions)"
}
```

All downstream analytics — xG, xA, xT, pass networks, player ratings — consume this unified schema. Provider-specific converters (Opta F24, StatsBomb JSON, Wyscout CSV) handle the mapping at ingestion time, so analytical code never references provider-specific field names.

## Integration Architecture

The module is designed as a composable analytics layer that sits between raw data storage and consumption layers:

- **Ingestion Layer**: Provider adapters normalize raw match data into the unified schema and persist to a time-series database (InfluxDB or TimescaleDB recommended).
- **Computation Layer**: Stateless analytics functions (xG prediction, rating computation, network construction) operate on query snapshots. All models are versioned and stored as serialized artifacts.
- **Caching Layer**: Precomputed per-match reports and player season aggregates are materialized to reduce query latency for dashboard consumers.
- **API Layer**: RESTful endpoints expose analytics results with pagination, filtering by date range/team/player, and configurable metric selection.
- **Export Layer**: CSV, JSON, and PDF export for coaching staff reports. Broadcast graphics integration via SVG template rendering.

## Performance Considerations

- xG prediction on a single shot takes <1ms; batch prediction on a full match (~250 shots) completes in <100ms
- Pass network construction scales linearly with event count; a 90-minute match (~2000 events) processes in <500ms
- Player rating computation for a full squad (22 players) completes in <200ms with precomputed per-90 statistics
- League benchmarking across 5 leagues with 500+ players per league completes in <2s with indexed data

## Related Modules

- [game-strategy](../game-strategy/GROK.md) — Tactical formation analysis and play calling optimization that consumes performance analytics outputs
- [wearable-tech](../wearable-tech/GROK.md) — IMU and GPS data streams that feed sprint velocity and workload indicators
- [injury-prevention](../injury-prevention/GROK.md) — Load management models that use performance workload data for injury risk scoring
- [fan-engagement](../fan-engagement/GROK.md) — Fantasy sports analytics that consume player performance metrics for scoring

## Advanced Configuration

The performance analytics module exposes extensive configuration options through a YAML-based configuration system. The primary configuration file should be placed at the project root or specified via the `PERF_ANALYTICS_CONFIG` environment variable.

### Model Configuration

```yaml
# config/performance_analytics.yaml
xg_model:
  type: "gradient_boosting"
  model_path: "models/xg_v3_gradient_boosting.pkl"
  feature_set: "full_v3"
  n_estimators: 500
  max_depth: 6
  learning_rate: 0.05
  min_samples_leaf: 20
  calibration_method: "isotonic_regression"

player_rating:
  method: "bayesian_adjusted"
  min_minutes: 450
  shrinkage_prior: "position_mean"
  positional_weights:
    goalkeeper:
      shot_stopping: 0.35
      distribution: 0.25
      aerial_duels: 0.15
      claiming: 0.15
      sweeper: 0.10
    defender:
      tackles_won: 0.20
      interceptions: 0.15
      aerial_duels: 0.15
      progressive_passes: 0.15
      pressure_regains: 0.10
      xg_prevented: 0.10
      dribbles_completed: 0.05
      fouls_committed: -0.05
    midfielder:
      progressive_passes: 0.15
      progressive_carries: 0.10
      tackles_won: 0.10
      interceptions: 0.10
      xg_plus_xa: 0.15
      pressure_regains: 0.10
      successful_dribbles: 0.05
      key_passes: 0.10
      aerial_duels_won: 0.05
    forward:
      xg: 0.25
      xa: 0.15
      successful_dribbles: 0.10
      progressive_carries: 0.10
      shot_creating_actions: 0.15
      aerial_duels_won: 0.10
      non_penalty_goals: 0.15

pass_network:
  min_passes: 3
  normalize_by_possession: true
  clustering_method: "louvain"
  clustering_resolution: 0.8
  node_size_metric: "pass_volume"
  edge_width_metric: "completion_rate"
```

### Data Ingestion Settings

```yaml
data_providers:
  statsbomb:
    api_key: "${STATSBOMB_API_KEY}"
    rate_limit_per_minute: 30
    retry_attempts: 3
    retry_backoff: 2.0
    timeout_seconds: 30
  opta:
    feed_url: "${OPTA_FEED_URL}"
    authentication:
      type: "basic"
      username: "${OPTA_USER}"
      password: "${OPTA_PASS}"
  wyscout:
    api_token: "${WYSCOUT_TOKEN}"
    export_format: "csv"
    compression: "gzip"

normalization:
  pitch_coordinates: "0_100"
  coordinate_system:
    x_range: [0, 100]
    y_range: [0, 100]
    origin: "bottom_left"
  timestamp_format: "seconds_from_kickoff"
  outcome_mapping:
    successful: ["complete", "won", "on_target"]
    unsuccessful: ["incomplete", "lost", "off_target", "blocked"]
```

### Caching Configuration

```yaml
caching:
  enabled: true
  backend: "redis"
  redis_url: "${REDIS_URL:redis://localhost:6379}"
  default_ttl_seconds: 3600
  per_match_report_ttl: 86400
  player_season_agg_ttl: 43200
  max_memory_mb: 512
  eviction_policy: "lru"
```

## Architecture Patterns

The performance analytics module follows several established architectural patterns to ensure maintainability, testability, and scalability.

### Event Sourcing for Match Data

All match events are stored as an immutable append-only log. Derived analytics (xG, ratings, pass networks) are computed as projections from this event log, enabling:

- **Retroactive recomputation**: When the xG model is updated, all historical xG values can be regenerated from the stored events
- **Auditability**: Every derived metric can be traced back to the exact event(s) that contributed to it
- **Multiple projections**: The same event data can produce different analytical views without modification

### Repository Pattern

Data access is abstracted behind repository interfaces:

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from performance_analytics.models import MatchEvent, Player

class MatchEventRepository(ABC):
    @abstractmethod
    def get_events_by_match(self, match_id: str) -> List[MatchEvent]:
        pass

    @abstractmethod
    def get_events_by_player(self, player_id: str,
                             start_date: str, end_date: str) -> List[MatchEvent]:
        pass

    @abstractmethod
    def store_events(self, events: List[MatchEvent]) -> None:
        pass

class PostgresMatchEventRepository(MatchEventRepository):
    def __init__(self, connection_pool):
        self.pool = connection_pool

    def get_events_by_match(self, match_id: str) -> List[MatchEvent]:
        with self.pool.cursor() as cur:
            cur.execute(
                "SELECT * FROM match_events WHERE match_id = %s "
                "ORDER BY timestamp",
                (match_id,)
            )
            return [MatchEvent.from_row(row) for row in cur.fetchall()]
```

### Strategy Pattern for Data Providers

Each data provider (StatsBomb, Opta, Wyscout) implements a common provider interface:

```python
class DataProviderStrategy(ABC):
    @abstractmethod
    def fetch_match_events(self, match_id: str) -> List[RawEvent]:
        pass

    @abstractmethod
    def normalize_to_schema(self, raw_events: List[RawEvent]) -> List[MatchEvent]:
        pass

    @abstractmethod
    def validate_data_quality(self, events: List[MatchEvent]) -> DataQualityReport:
        pass

class StatsBombProvider(DataProviderStrategy):
    def __init__(self, api_key: str):
        self.client = StatsBombClient(api_key)

    def fetch_match_events(self, match_id: str) -> List[RawEvent]:
        return self.client.get_events(match_id)

    def normalize_to_schema(self, raw_events: List[RawEvent]) -> List[MatchEvent]:
        return [self._convert_event(e) for e in raw_events]

    def validate_data_quality(self, events: List[MatchEvent]) -> DataQualityReport:
        return DataQualityReport(
            total_events=len(events),
            missing_coordinates=events.count(lambda e: e.x is None),
            duplicate_events=self._find_duplicates(events),
            timestamp_gaps=self._find_gaps(events),
        )
```

### Command Pattern for Analytics Operations

Analytics computations are encapsulated as command objects that can be queued, retried, and logged:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class AnalyticsCommand:
    command_id: str
    match_id: str
    analytics_type: str  # "xg", "rating", "pass_network"
    parameters: dict
    created_at: datetime
    status: str = "pending"
    result: Optional[dict] = None
    error: Optional[str] = None

class AnalyticsCommandHandler:
    def __init__(self, repository, model_registry):
        self.repository = repository
        self.models = model_registry

    def execute(self, command: AnalyticsCommand):
        command.status = "running"
        try:
            model = self.models.get_model(command.analytics_type)
            result = model.compute(
                match_id=command.match_id,
                **command.parameters
            )
            command.status = "completed"
            command.result = result
        except Exception as e:
            command.status = "failed"
            command.error = str(e)
        finally:
            self.repository.save_command(command)
```

## Integration Guide

### REST API Integration

The module exposes a RESTful API for consuming analytics results. All endpoints follow standard conventions:

```python
from fastapi import FastAPI, Query
from performance_analytics.api import router

app = FastAPI(
    title="Performance Analytics API",
    version="1.0.0",
    description="Sports performance analytics service",
)

app.include_router(router, prefix="/api/v1")

# Example endpoint definitions
@app.get("/api/v1/matches/{match_id}/xg")
async def get_match_xg(match_id: str):
    """Retrieve xG data for a specific match."""
    xg_service = XGService()
    return xg_service.get_match_xg(match_id)

@app.get("/api/v1/players/{player_id}/rating")
async def get_player_rating(
    player_id: str,
    match_id: str = Query(None),
    window: int = Query(10, ge=1, le=50),
):
    """Retrieve player rating with optional match and window filters."""
    rating_service = RatingService()
    return rating_service.get_rating(player_id, match_id, window)
```

### Message Queue Integration

For asynchronous analytics processing, the module integrates with message queues (RabbitMQ, Kafka):

```python
import pika
import json

class AnalyticsMessagePublisher:
    def __init__(self, amqp_url: str):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(amqp_url)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='analytics',
            exchange_type='topic'
        )

    def publish_match_analytics(self, match_id: str, analytics_type: str):
        message = {
            "match_id": match_id,
            "analytics_type": analytics_type,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.channel.basic_publish(
            exchange='analytics',
            routing_key=f'compute.{analytics_type}',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent
                content_type='application/json',
            )
        )
```

### WebSocket Real-Time Updates

For live analytics streaming during matches:

```python
import asyncio
import websockets
import json

class LiveAnalyticsStream:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.subscribers = set()

    async def subscribe(self, websocket, match_id: str):
        self.subscribers.add(websocket)
        pubsub = self.redis.pubsub()
        pubsub.subscribe(f"analytics:{match_id}")
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    await websocket.send(message["data"].decode())
        finally:
            self.subscribers.remove(websocket)

    async def broadcast_analytics(self, match_id: str, data: dict):
        self.redis.publish(
            f"analytics:{match_id}",
            json.dumps(data)
        )
```

## Performance Optimization

### Database Query Optimization

```sql
-- Composite index for common query patterns
CREATE INDEX idx_match_events_composite
ON match_events (match_id, event_type, timestamp)
INCLUDE (player_id, team_id, x, y, outcome);

-- Partial index for shot events (frequent xG queries)
CREATE INDEX idx_shots_partial
ON match_events (match_id, timestamp)
WHERE event_type = 'shot';

-- Materialized view for precomputed per-match aggregates
CREATE MATERIALIZED VIEW match_xg_summary AS
SELECT
    match_id,
    team_id,
    COUNT(*) FILTER (WHERE event_type = 'shot') AS shot_count,
    SUM(xg_value) AS total_xg,
    AVG(xg_value) AS avg_xg_per_shot,
    COUNT(*) FILTER (WHERE outcome = 'goal') AS actual_goals
FROM match_events
WHERE event_type = 'shot'
GROUP BY match_id, team_id;
```

### Batch Processing Pipeline

```python
from concurrent.futures import ProcessPoolExecutor
from typing import List

class BatchAnalyticsProcessor:
    def __init__(self, max_workers: int = 8):
        self.executor = ProcessPoolExecutor(max_workers=max_workers)

    def process_matches_batch(
        self,
        match_ids: List[str],
        analytics_types: List[str],
    ) -> dict:
        futures = {}
        for match_id in match_ids:
            for analytics_type in analytics_types:
                key = f"{match_id}:{analytics_type}"
                futures[key] = self.executor.submit(
                    self._compute_analytics,
                    match_id, analytics_type
                )

        results = {}
        for key, future in futures.items():
            results[key] = future.result(timeout=30)
        return results
```

### In-Memory Caching Strategy

```python
from functools import lru_cache
from typing import Optional

class CachedAnalyticsEngine:
    def __init__(self, cache_backend):
        self.cache = cache_backend

    def get_xg(self, shot_id: str) -> Optional[float]:
        cache_key = f"xg:{shot_id}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return float(cached)
        result = self.xg_model.predict(shot_id)
        self.cache.set(cache_key, result.xg, ttl=3600)
        return result.xg

    def invalidate_match_cache(self, match_id: str):
        pattern = f"*:{match_id}:*"
        keys = self.cache.keys(pattern)
        if keys:
            self.cache.delete(*keys)
```

## Security Considerations

### Authentication and Authorization

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

class AnalyticsAuthMiddleware:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    async def verify_token(
        self,
        credentials: HTTPAuthorizationCredentials = Security(security),
    ) -> dict:
        token = credentials.credentials
        payload = self.auth_service.verify_jwt(token)
        if payload is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )
        if "analytics:read" not in payload.get("scopes", []):
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )
        return payload
```

### Data Encryption

```python
from cryptography.fernet import Fernet

class SensitiveDataEncryption:
    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)

    def encrypt_player_data(self, data: dict) -> bytes:
        serialized = json.dumps(data).encode()
        return self.cipher.encrypt(serialized)

    def decrypt_player_data(self, encrypted: bytes) -> dict:
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted.decode())
```

### API Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/matches/{match_id}/xg")
@limiter.limit("100/minute")
async def get_match_xg_rate_limited(match_id: str):
    return xg_service.get_match_xg(match_id)
```

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| xG predictions cluster near 0.5 | Model calibration drift | Retrain model on recent data; check feature distribution shift |
| Pass network shows disconnected nodes | Min-passes threshold too high | Lower `min_passes` parameter; verify event data quality |
| Player ratings show NaN for some players | Insufficient minutes played | Increase `min_minutes` threshold or use Bayesian shrinkage |
| Match report generation is slow | Large event dataset without indexing | Add composite database index; enable result caching |
| Coordinate conversion produces negative values | Origin mismatch between providers | Verify provider-specific coordinate systems; use explicit conversion |

### Debugging Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("performance_analytics")

# Enable model-level debugging
xg_model = ExpectedGoalsModel(
    model_type="gradient_boosting",
    debug=True,  # enables detailed prediction logging
)

# Inspect feature contributions
result = xg_model.predict(shot)
print(f"Feature contributions: {result.feature_contributions}")
print(f"Model version: {result.model_version}")
print(f"Inference time: {result.inference_time_ms:.1f}ms")
```

### Data Quality Validation

```python
from performance_analytics.validation import DataQualityValidator

validator = DataQualityValidator()

report = validator.validate_match_events(events)
print(f"Validation report:")
print(f"  Total events: {report.total_events}")
print(f"  Valid events: {report.valid_events}")
print(f"  Warnings: {len(report.warnings)}")
for warning in report.warnings:
    print(f"    - {warning.field}: {warning.message}")
print(f"  Errors: {len(report.errors)}")
for error in report.errors:
    print(f"    - {error.field}: {error.message}")
```

## API Reference

### Core Classes

| Class | Description | Key Methods |
|-------|-------------|-------------|
| `ExpectedGoalsModel` | xG prediction engine | `predict(shot)`, `batch_predict(shots)`, `calibrate(data)` |
| `MatchAnalyzer` | Match-level analysis | `generate_report()`, `get_possession_chains()`, `get_shots()` |
| `PlayerRatingSystem` | Bayesian player ratings | `compute_rating(player_id)`, `rank_squad()`, `compare_to_league()` |
| `PassNetworkBuilder` | Pass network construction | `build()`, `find_clustering()`, `to_plotly_data()` |
| `XTModel` | Expected threat model | `evaluate_action()`, `evaluate_chain()`, `season_summary()` |
| `LeagueBenchmark` | Cross-league comparison | `compare_player()`, `percentile_rank()`, `get_distribution()` |

### Data Classes

| Class | Description | Fields |
|-------|-------------|--------|
| `ShotEvent` | Individual shot event | `event_id, player_id, team_id, match_id, x, y, body_part, assist_type, distance_to_goal, angle_to_goal, ...` |
| `MatchReport` | Comprehensive match analysis | `match_id, home_xg, away_xg, possession, pass_networks, top_performers, ...` |
| `PlayerRating` | Player performance rating | `player_id, rating, minutes, per_90_stats, confidence_interval, ...` |
| `XGResult` | xG prediction result | `xg, post_shot_xg, feature_contributions, model_version, calibration_score` |
| `PossessionChain` | xT possession sequence | `events, team_id, match_id, total_xt, ...` |

## Data Models

### Entity Relationship Diagram

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│     Matches      │     │   Match Events    │     │    Players      │
├─────────────────┤     ├──────────────────┤     ├─────────────────┤
│ match_id (PK)   │────<│ event_id (PK)    │>────│ player_id (PK)  │
│ competition_id   │     │ match_id (FK)    │     │ name            │
│ season           │     │ player_id (FK)   │     │ position        │
│ date             │     │ team_id (FK)     │     │ team_id (FK)    │
│ home_team        │     │ event_type       │     │ nationality     │
│ away_team        │     │ timestamp        │     │ date_of_birth   │
│ venue            │     │ period           │     │ height_cm       │
│ score_home       │     │ x, y             │     │ weight_kg       │
│ score_away       │     │ end_x, end_y     │     └─────────────────┘
│ attendance      │     │ outcome          │
│ referee          │     │ xg_value         │     ┌─────────────────┐
└─────────────────┘     │ meta             │     │  Player Ratings  │
                        └──────────────────┘     ├─────────────────┤
                                                 │ rating_id (PK)  │
┌─────────────────┐     ┌──────────────────┐     │ player_id (FK)  │
│     Teams        │     │  Pass Networks   │     │ match_id (FK)   │
├─────────────────┤     ├──────────────────┤     │ rating          │
│ team_id (PK)    │────<│ network_id (PK)  │     │ minutes_played  │
│ name            │     │ match_id (FK)    │     │ per_90_xg       │
│ league          │     │ team_id (FK)     │     │ per_90_xa       │
│ country         │     │ nodes (JSON)     │     │ confidence_low  │
│ founded_year    │     │ edges (JSON)     │     │ confidence_high │
│ stadium         │     │ clusters (JSON)  │     │ computed_at     │
│ capacity        │     │ created_at       │     └─────────────────┘
└─────────────────┘     └──────────────────┘
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "performance_analytics.api:app", \
     "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "4"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: performance-analytics
  labels:
    app: performance-analytics
spec:
  replicas: 3
  selector:
    matchLabels:
      app: performance-analytics
  template:
    metadata:
      labels:
        app: performance-analytics
    spec:
      containers:
      - name: analytics-api
        image: performance-analytics:1.0.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: analytics-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: analytics-config
              key: redis-url
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## Monitoring & Observability

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    'analytics_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'analytics_api_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

XG_PREDICTIONS = Counter(
    'xg_predictions_total',
    'Total xG predictions made',
    ['model_version']
)

ACTIVE_MATCHES = Gauge(
    'active_matches_tracked',
    'Number of matches being tracked in real-time'
)
```

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "model_loaded": check_model_availability(),
    }
    healthy = all(checks.values())
    return {
        "status": "healthy" if healthy else "degraded",
        "checks": checks,
        "version": "1.0.0",
    }
```

### Alerting Rules

```yaml
groups:
  - name: performance-analytics
    rules:
      - alert: HighErrorRate
        expr: rate(analytics_api_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on analytics API"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(analytics_api_request_latency_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency on analytics API"

      - alert: ModelDriftDetected
        expr: xg_calibration_error > 0.1
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: "xG model calibration drift detected"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from performance_analytics import ExpectedGoalsModel, ShotEvent

class TestExpectedGoalsModel:
    def setup_method(self):
        self.model = ExpectedGoalsModel(model_type="logistic_regression")

    def test_single_shot_prediction_range(self):
        shot = ShotEvent(
            x=88.5, y=42.3,
            distance_to_goal=14.2,
            angle_to_goal=23.5,
            body_part="right_foot",
            under_pressure=True,
        )
        result = self.model.predict(shot)
        assert 0.0 <= result.xg <= 1.0

    def test_close_shot_higher_xg_than_distant(self):
        close_shot = ShotEvent(distance_to_goal=5, angle_to_goal=45, ...)
        far_shot = ShotEvent(distance_to_goal=30, angle_to_goal=15, ...)
        close_xg = self.model.predict(close_shot).xg
        far_xg = self.model.predict(far_shot).xg
        assert close_xg > far_xg

    @pytest.mark.parametrize("body_part", ["right_foot", "left_foot", "head"])
    def test_body_part_prediction(self, body_part):
        shot = ShotEvent(body_part=body_part, distance_to_goal=12, ...)
        result = self.model.predict(shot)
        assert 0.0 <= result.xg <= 1.0
```

### Integration Tests

```python
class TestMatchAnalysisIntegration:
    @pytest.fixture
    def test_database(self):
        # Set up test database with fixture data
        db = create_test_database()
        load_fixture_matches(db, count=10)
        yield db
        db.teardown()

    def test_full_match_analysis_pipeline(self, test_database):
        analyzer = MatchAnalyzer(
            match_id="test_match_001",
            db_connection=test_database,
        )
        report = analyzer.generate_report()
        assert report.home_xg > 0
        assert report.away_xg > 0
        assert len(report.top_performers(n=5)) == 5
        assert report.pass_networks is not None
```

### Performance Tests

```python
import time

class TestPerformanceBenchmarks:
    def test_xg_batch_prediction_throughput(self):
        model = ExpectedGoalsModel()
        shots = [create_random_shot() for _ in range(1000)]

        start = time.perf_counter()
        results = model.batch_predict(shots)
        elapsed = time.perf_counter() - start

        throughput = len(shots) / elapsed
        assert throughput > 10000, f"Throughput {throughput:.0f} < 10000 shots/sec"
        assert len(results) == 1000
```

## Versioning & Migration

### Semantic Versioning

The module follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes to public API or data schema
- **MAJOR**: New features, backward-compatible
- **PATCH**: Bug fixes, performance improvements

### Model Versioning

```python
class ModelVersionManager:
    def __init__(self, model_registry):
        self.registry = model_registry

    def register_model(self, model, metadata):
        version = self._generate_version()
        self.registry.store(
            model=model,
            version=version,
            metadata={
                "trained_at": datetime.utcnow().isoformat(),
                "training_data_hash": metadata.data_hash,
                "features": metadata.feature_list,
                "metrics": metadata.performance_metrics,
            }
        )
        return version

    def load_model(self, model_type: str, version: str = "latest"):
        return self.registry.load(model_type, version)
```

### Database Migration

```python
# migrations/003_add_xg_post_shot.sql
-- Add post-shot xG support

ALTER TABLE match_events
ADD COLUMN post_shot_xg DECIMAL(5,4);

ALTER TABLE match_events
ADD COLUMN psxg_model_version VARCHAR(50);

CREATE INDEX idx_events_psxg
ON match_events (post_shot_xg)
WHERE post_shot_xg IS NOT NULL;

-- Backfill existing shot events
UPDATE match_events
SET post_shot_xg = xg_value * 0.95,
    psxg_model_version = 'psxg_v1.0'
WHERE event_type = 'shot'
  AND post_shot_xg IS NULL;
```

## Glossary

| Term | Definition |
|------|------------|
| **xG (Expected Goals)** | A metric that assigns a probability value to each shot based on historical conversion rates from similar positions and situations |
| **xA (Expected Assists)** | The expected goal value of shots that directly follow a player's pass, measuring creative contribution |
| **xT (Expected Threat)** | A Markov-chain model that values every on-ball action by the probability of a goal resulting from the possession state |
| **PSxG (Post-Shot xG)** | xG calculated after the shot is taken, incorporating goalkeeper position and shot placement |
| **ACWR** | Acute:Chronic Workload Ratio, comparing recent training load to longer-term baseline |
| **Per-90 Stats** | Statistics normalized to 90 minutes of playing time for fair comparison |
| **Bayesian Shrinkage** | Statistical technique that pulls small-sample estimates toward a prior (population mean) |
| **Calibration** | How well predicted probabilities match observed frequencies |
| **Feature Contribution** | The individual impact of each input variable on a model prediction |
| **Possession Value** | The cumulative xT gained during a single possession sequence |
| **Heatmap** | Kernel density estimation visualization of spatial activity distribution |
| **Pass Network** | Graph-based representation of passing relationships between players |
| **Clustering** | Unsupervised grouping of similar pass patterns or formation shapes |
| **Progressive Pass** | A pass that moves the ball significantly closer to the opponent's goal |
| **Shot-Creating Action** | The two offensive actions directly leading to a shot attempt |

## Changelog

### Version 1.0.0 (2024-01-15)

- Initial release with xG model engine, match event normalization, and player rating system
- Support for StatsBomb, Opta, and Wyscout data providers
- Pass network construction with Louvain clustering
- Expected Threat (xT) Markov chain model
- RESTful API with FastAPI framework

### Version 1.1.0 (2024-03-20)

- Added gradient-boosted xG model alongside logistic regression
- Implemented post-shot xG (PSxG) for goalkeeper evaluation
- Enhanced player rating system with positional weighting
- Added cross-league benchmarking with normalization factors

### Version 1.2.0 (2024-06-10)

- WebSocket real-time analytics streaming
- Batch processing pipeline for historical analysis
- Advanced caching with Redis backend
- Comprehensive data quality validation framework

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/sports-tech/performance-analytics.git
cd performance-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=performance_analytics

# Run linting
ruff check .
ruff format .
```

### Code Standards

- All code must pass `ruff check` with zero warnings
- Type hints required for all public functions
- Docstrings required for all public classes and methods
- Test coverage minimum: 80% for new features
- Commit messages follow Conventional Commits format

### Pull Request Process

1. Fork the repository and create a feature branch
2. Write tests for all new functionality
3. Update documentation for API changes
4. Run the full test suite and ensure all tests pass
5. Submit PR with descriptive title and detailed description
6. Address review feedback promptly
7. Merge after approval from at least one maintainer

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Copyright (c) 2024 Sports Tech Analytics

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
