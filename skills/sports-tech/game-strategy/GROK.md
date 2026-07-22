---
name: "game-strategy"
category: "sports-tech"
version: "1.0.0"
tags: ["sports-tech", "game-strategy", "tactical-analysis", "play-calling"]
---

# Game Strategy — Tactical Analysis, Pattern Recognition & Real-Time Dashboards

## Overview

Game strategy in sports technology encompasses the computational tools that enable coaching staff to design, communicate, and adapt tactical plans before and during competition. This module provides a full-stack tactical analysis framework spanning formation analysis, opponent pattern recognition, set-piece design, pressing system optimization, and real-time strategy dashboards. It bridges the gap between qualitative coaching intuition and quantitative evidence, enabling data-informed tactical decisions without replacing the coach's judgment.

The tactical analysis engine models formations as dynamic graphs where nodes represent player positions (with continuous spatial coordinates, not just discrete role labels) and edges represent passing lanes, defensive coverage zones, and pressing connections. Formation detection uses unsupervised clustering on historical tracking data to identify a team's primary and secondary shapes, including hybrid formations that shift between phases of play (e.g., 4-3-3 in possession transitioning to 4-4-2 out of possession). The engine identifies pressing triggers — specific events or spatial conditions that activate a team's press — by correlating defensive intensity spikes with contextual features like ball location, pass direction, and player receiving posture.

The expected threat (xT) model extends the xG framework from shots to all on-ball actions, quantifying how much each action increases the probability of scoring. By chaining xT values across possession sequences, the module produces possession value maps that reveal which build-up patterns are most efficient at progressing toward goal-scoring opportunities. This feeds directly into play calling optimization, where the system suggests tactical adjustments based on the opponent's defensive vulnerabilities identified through pattern mining.

The real-time dashboard subsystem consumes live tracking data and match events to produce an at-a-glance tactical overview during matches. It supports configurable alert thresholds for pressing triggers, possession chain breakdowns, and formation shifts, enabling analysts to relay tactical intelligence to the coaching bench within seconds of a pattern emerging.

## Core Capabilities

- **Dynamic Formation Detection**: Unsupervised clustering on tracking data that identifies primary/secondary formations, phase-of-play transitions, and hybrid shapes with spatial granularity beyond discrete role labels
- **Opponent Pattern Recognition**: Sequential pattern mining (PrefixSpan, SPADE) on event data to identify recurring build-up patterns, pressing triggers, set-piece routines, and transition behaviors
- **Pressing Trigger Analysis**: Correlation engine identifying which spatial, temporal, or event-based conditions activate high-intensity pressing, with heatmaps of press initiation zones and success rates
- **Expected Threat (xT) Model**: Markov-chain based model assigning probability-of-scoring value to every on-ball action, enabling possession value chain analysis across multi-pass sequences
- **Play Calling Optimization**: Recommendation engine suggesting tactical adjustments based on opponent vulnerability analysis, current match state, and historical success rates of specific patterns
- **Set-Piece Design System**: Template-based set-piece design tool with zonal/man-marking assignments, blocking schemes, and delivery targets, scored against opponent defensive structure weaknesses
- **Real-Time Strategy Dashboard**: Live tactical overview consuming tracking data and events, with configurable alerts for formation shifts, pressing triggers, and possession breakdowns
- **Counter-Pressing Metrics**: Quantitative measurement of ball-winning speed after turnover, defensive transition compactness, and re-engagement distance, with benchmarking against league standards

## Usage Examples

### Formation Detection

```python
from game_strategy import FormationDetector, TrackingDataSource

detector = FormationDetector(
    tracking_source=TrackingDataSource.SECOND_SPECTRUM,
    match_id="match_2024_barca_vs_rm",
    team_id="barcelona",
    time_window_seconds=60,  # sliding window for formation estimation
    cluster_method="dbscan",
    min_samples=30,
)

# Detect formations across the match
formations = detector.detect(match_duration_minutes=90)

for period, formation in formations:
    print(f"[{period.start_min:.0f}'-{period.end_min:.0f}'] "
          f"Primary: {formation.primary_shape} "
          f"({formation.confidence:.0%})")
    if formation.secondary_shape:
        print(f"  Secondary: {formation.secondary_shape} "
              f"({formation.secondary_confidence:.0%})")
    print(f"  Transition events: {formation.transition_count}")
    print(f"  Defensive line height: {formation.def_line_height:.1f} m")
```

### Opponent Pattern Mining

```python
from game_strategy import PatternMiner, EventSequence

miner = PatternMiner(
    min_support=0.15,       # pattern must occur in 15%+ of possessions
    max_pattern_length=8,   # max events in a sequence
    min_confidence=0.6,
)

# Mine build-up patterns from opponent match data
sequences = EventSequence.from_matches(
    match_ids=["match_opponent_1", "match_opponent_2", "match_opponent_3"],
    team_id="opponent_team",
    event_types=["pass", "carry", "dribble"],
)

patterns = miner.mine(sequences)

# Identify the opponent's most frequent build-up routes
for pattern in patterns.top_k(10):
    print(f"Pattern: {' -> '.join(pattern.event_labels)}")
    print(f"  Frequency: {pattern.support:.1%}")
    print(f"  Leads to final third: {pattern.final_third_rate:.1%}")
    print(f"  Avg xT gain: {pattern.avg_xt_gain:.3f}")
    print()
```

### Pressing Trigger Identification

```python
from game_strategy import PressingAnalyzer

analyzer = PressingAnalyzer(
    tracking_data="match_2024_tracking.parquet",
    event_data="match_2024_events.json",
    high_press_threshold=9.0,  # m/s^2 acceleration threshold
    pressing_window_seconds=5,
)

triggers = analyzer.identify_triggers(team_id="liverpool")

for trigger in triggers:
    print(f"Trigger: {trigger.condition}")
    print(f"  Zone: {trigger.zone.description}")
    print(f"  Frequency: {trigger.occurrences} times per match (avg)")
    print(f"  Success rate: {trigger.success_rate:.1%}")
    print(f"  Avg recovery time: {trigger.avg_recovery_seconds:.1f}s")
    print(f"  Vulnerability: {trigger.opponent_exploits.description}")
    print()
```

### Expected Threat (xT) Possession Analysis

```python
from game_strategy import XTModel, PossessionChain

xt_model = XTModel(
    grid_cols=16,    # pitch divided into 16x12 zones
    grid_rows=12,
    model_path="models/xt_v2_markov.pkl",
)

# Analyze a possession chain
chain = PossessionChain(
    events=[
        {"type": "pass", "from": (20, 50), "to": (35, 45)},
        {"type": "carry", "from": (35, 45), "to": (50, 40)},
        {"type": "pass", "from": (50, 40), "to": (70, 35)},
        {"type": "shot", "from": (85, 30), "xg": 0.35},
    ],
    team_id="man_city",
    match_id="match_2024_01",
)

# Compute xT for each action
xt_values = xt_model.evaluate_chain(chain)
for event, xt in zip(chain.events, xt_values):
    print(f"{event['type']:8s} | xT: {xt:+.4f} | "
          f"cumulative: {sum(xt_values[:xt_values.index(xt)+1]):.4f}")

# Season-level possession value analysis
season_xt = xt_model.season_summary(
    team_id="man_city",
    season=2024,
    min_possessions=50,
)
print(f"Avg possession xT: {season_xt.avg_xt_per_possession:.4f}")
print(f"Most efficient build-up zone: {season_xt.most_efficient_zone}")
```

## Best Practices

1. **Always contextualize formation data with match state** — a team's formation at 2-0 up in the 85th minute differs fundamentally from their shape at 0-0 in the 20th. Segment analysis by match state to avoid misleading tactical conclusions.

2. **Use sufficient sample sizes for pattern mining** — single-match patterns are noise. Require at least 5-10 matches of data before drawing tactical conclusions from sequential pattern mining. Adjust min_support thresholds for smaller samples.

3. **Validate pressing triggers against defensive transition metrics** — a pressing trigger with high activation frequency but low ball-recovery success is a liability, not a weapon. Always pair trigger identification with outcome analysis.

4. **Implement spatial awareness in xT models** — a pass from zone A to zone B has different value depending on the defensive structure present. Augment position-only xT with defensive pressure features for more accurate action valuation.

5. **Distinguish between tactical intent and execution** — a team may intend to press high but fail due to fitness or coordination. Separate intention (design) from execution (metrics) when reporting tactical analysis to avoid conflating planning with performance.

6. **Use real-time dashboards for pattern confirmation, not discovery** — live dashboards confirm pre-match hypotheses quickly. True pattern discovery requires post-match deep analysis with full tracking data and multiple angle review.

7. **Design set-pieces against specific opponent weaknesses** — generic set-piece routines are less effective than routines tailored to exploit identified weaknesses in the opponent's zonal or man-marking system.

8. **Quantify counter-pressing speed** — the time between losing possession and re-engaging the ball is the single most predictive defensive transition metric. Benchmark it against league standards and track it over time.

## Data Requirements

Each analytical component has specific data dependencies:

- **Formation Detection**: Requires tracking data at ≥2 Hz with all 22 player positions plus ball position. StatsBomb, Second Spectrum, and Hawk-Eye provide compatible feeds. Formation detection degrades below 1 Hz due to position uncertainty during rapid transitions.
- **Pattern Mining**: Requires event-level data with at minimum pass, carry, and shot events including start/end coordinates. A minimum of 5 matches is recommended for statistically meaningful patterns; 10+ matches for high-confidence patterns.
- **Pressing Analysis**: Requires tracking data at ≥5 Hz to capture pressing intensity (player acceleration). Event data for context (pass direction, receiving posture). Ideal: 25 Hz tracking with event overlay.
- **xT Model**: Requires event data with accurate pitch coordinates and a historical training corpus of 500+ matches for the Markov transition matrix estimation.
- **Set-Piece Design**: Requires opponent defensive structure data (tracking or event-based) from at least 3-5 set-piece situations of the same type.

## Algorithm Details

### Formation Detection Algorithm

The formation detector uses a two-stage approach:

1. **Spatial Clustering**: At each time window, player positions are clustered using DBSCAN to identify the defensive line, midfield line, and attacking line. The number of players in each line constrains the possible formations.
2. **Template Matching**: The clustered positions are matched against a library of canonical formation templates using a distance metric that accounts for horizontal spread, vertical compactness, and line heights. The best-matching template with highest confidence score is selected.

The system supports hybrid formation detection by tracking formation transitions over time. When a team shifts between shapes (e.g., 4-3-3 in possession to 4-4-2 out of possession), the detector identifies the primary and secondary formations along with the transition trigger conditions.

### Expected Threat Markov Model

The xT model divides the pitch into a grid (default 16x12 zones) and estimates:

- **Zone Values**: The probability of scoring from each zone, estimated from historical shot data
- **Transition Matrix**: The probability of moving the ball from any zone to any other zone via a single action
- **Action Values**: The xT gain of any action = zone_value(destination) - zone_value(origin) + transition_adjustment

This formulation values not just the endpoint of an action but the probability of reaching that endpoint, producing more accurate valuations than naive distance-to-goal models.

## Integration Points

The module exposes tactical analysis results through several integration channels:

- **Pre-Match Dossiers**: Automated PDF reports generated 24-48 hours before kickoff, containing opponent formation analysis, pressing trigger profiles, and set-piece vulnerabilities
- **Live Dashboard API**: WebSocket endpoint streaming real-time formation detection, pressing intensity, and xT accumulation during matches
- **Post-Match Reports**: Comprehensive tactical analysis with event-level breakdowns, possession value chains, and comparison against pre-match hypotheses
- **Coaching Integration**: Structured data feeds compatible with tactical board software (TacticalPad, Coach Paint) for interactive coaching sessions

## Related Modules

- [performance-analytics](../performance-analytics/GROK.md) — Provides player and match statistics that feed tactical analysis models
- [wearable-tech](../wearable-tech/GROK.md) — Supplies real-time positioning data for live tactical dashboards and pressing intensity metrics
- [injury-prevention](../injury-prevention/GROK.md) — Uses tactical workload data (pressing intensity, sprint count) for load management
- [fan-engagement](../fan-engagement/GROK.md) — Consumes tactical insights for real-time match commentary and fan-facing analytics

## Advanced Configuration

The game strategy module provides extensive configuration for tactical analysis engines, pattern mining algorithms, and real-time dashboard parameters.

### Formation Detection Configuration

```yaml
# config/game_strategy.yaml
formation_detection:
  algorithm: "dbscan"
  time_window_seconds: 60
  min_samples: 30
  eps_meters: 2.5

  templates:
    - name: "4-3-3"
      lines:
        defense: [4]
        midfield: [3]
        attack: [3]
      positions:
        goalkeeper: {x: 5, y: 50}
        left_back: {x: 25, y: 15}
        center_back_left: {x: 25, y: 40}
        center_back_right: {x: 25, y: 60}
        right_back: {x: 25, y: 85}
        left_midfield: {x: 50, y: 25}
        central_midfield: {x: 50, y: 50}
        right_midfield: {x: 50, y: 75}
        left_wing: {x: 75, y: 20}
        striker: {x: 80, y: 50}
        right_wing: {x: 75, y: 80}

    - name: "4-4-2"
      lines:
        defense: [4]
        midfield: [4]
        attack: [2]

    - name: "3-5-2"
      lines:
        defense: [3]
        midfield: [5]
        attack: [2]

    - name: "4-2-3-1"
      lines:
        defense: [4]
        midfield: [2, 3]
        attack: [1]

  transition_detection:
    enabled: true
    min_possession_seconds: 5
    formation_change_threshold: 0.3
```

### Pattern Mining Configuration

```yaml
pattern_mining:
  algorithm: "prefixspan"
  min_support: 0.15
  max_pattern_length: 8
  min_confidence: 0.6

  event_types:
    - "pass"
    - "carry"
    - "dribble"
    - "shot"
    - "cross"
    - "through_ball"
    - "long_ball"
    - "set_piece"

  spatial_zones:
    columns: 16
    rows: 12
    zone_labels: true

  filters:
    min_x_gain: 5.0
    exclude_own_half_only: true
    include_counter_attacks: true
```

### xT Model Configuration

```yaml
xt_model:
  grid_cols: 16
  grid_rows: 12
  transition_matrix_path: "models/xt_markov_v2.pkl"
  training_matches: 500
  discount_factor: 0.95

  value_computation:
    method: "iterative"
    max_iterations: 100
    convergence_threshold: 1e-6

  action_types:
    pass:
      weight: 1.0
    carry:
      weight: 0.8
    cross:
      weight: 1.2
    shot:
      weight: 1.5
```

## Architecture Patterns

### Event-Driven Architecture for Real-Time Analysis

The game strategy module uses an event-driven architecture to process live match data with minimal latency:

```
Live Tracking Feed
      │
      ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Event     │───▶│   Stream    │───▶│  Dashboard  │
│   Router    │    │  Processor  │    │   Emitter   │
└──────┬──────┘    └──────┬──────┘    └─────────────┘
       │                  │
       ▼                  ▼
┌─────────────┐    ┌─────────────┐
│   Pattern   │    │  Formation  │
│   Detector  │    │  Detector   │
└─────────────┘    └─────────────┘
```

### CQRS for Tactical Data

```python
from dataclasses import dataclass
from typing import List, Optional

# Command side - writes tactical data
@dataclass
class TacticalCommand:
    command_id: str
    match_id: str
    command_type: str  # "update_formation", "log_pattern", "record_xT"
    payload: dict
    timestamp: datetime

# Query side - reads tactical data
@dataclass
class FormationQuery:
    match_id: str
    time_range: Optional[tuple] = None
    team_id: Optional[str] = None

class TacticalCommandHandler:
    def __init__(self, event_store, projection_builder):
        self.event_store = event_store
        self.projections = projection_builder

    def handle_update_formation(self, command: TacticalCommand):
        event = FormationUpdatedEvent(
            match_id=command.match_id,
            formation=command.payload["formation"],
            confidence=command.payload["confidence"],
            timestamp=command.timestamp,
        )
        self.event_store.append(event)
        self.projections.update(event)

class TacticalQueryHandler:
    def __init__(self, projection_store):
        self.projections = projection_store

    def handle_formation_query(self, query: FormationQuery) -> List[FormationSnapshot]:
        return self.projections.get_formations(
            match_id=query.match_id,
            time_range=query.time_range,
            team_id=query.team_id,
        )
```

### Strategy Pattern for Play Calling

```python
from abc import ABC, abstractmethod

class PlayCallingStrategy(ABC):
    @abstractmethod
    def recommend(self, match_state: MatchState) -> List[TacticalRecommendation]:
        pass

class CounterAttackStrategy(PlayCallingStrategy):
    def __init__(self, opponent_vulnerabilities):
        self.vulnerabilities = opponent_vulnerabilities

    def recommend(self, match_state: MatchState) -> List[TacticalRecommendation]:
        if match_state.transition_phase == "defensive_to_attack":
            return self._generate_counter_recommendations(match_state)
        return []

class PossessionStrategy(PlayCallingStrategy):
    def __init__(self, team_style: str):
        self.style = team_style

    def recommend(self, match_state: MatchState) -> List[TacticalRecommendation]:
        if match_state.possession_percentage > 55:
            return self._generate_possession_recommendations(match_state)
        return []

class PlayCallingOrchestrator:
    def __init__(self, strategies: List[PlayCallingStrategy]):
        self.strategies = strategies

    def get_recommendations(self, match_state: MatchState) -> List[TacticalRecommendation]:
        all_recommendations = []
        for strategy in self.strategies:
            recommendations = strategy.recommend(match_state)
            all_recommendations.extend(recommendations)
        return sorted(all_recommendations, key=lambda r: r.confidence, reverse=True)
```

### Graph-Based Formation Modeling

```python
import networkx as nx
from typing import Dict, List

class FormationGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_player(self, player_id: str, position: tuple, role: str):
        self.graph.add_node(
            player_id,
            position=position,
            role=role,
        )

    def add_passing_lane(self, from_player: str, to_player: str,
                         frequency: float, success_rate: float):
        self.graph.add_edge(
            from_player, to_player,
            frequency=frequency,
            success_rate=success_rate,
            weight=frequency * success_rate,
        )

    def find_key_connectors(self) -> List[str]:
        betweenness = nx.betweenness_centrality(self.graph, weight="weight")
        return sorted(betweenness.keys(), key=lambda x: betweenness[x], reverse=True)[:3]

    def identify_pressing_network(self, pressing_threshold: float) -> List[List[str]]:
        pressing_edges = [
            (u, v) for u, v, d in self.graph.edges(data=True)
            if d.get("pressing_intensity", 0) > pressing_threshold
        ]
        pressing_subgraph = self.graph.edge_subgraph(pressing_edges)
        return list(nx.connected_components(pressing_subgraph))
```

## Integration Guide

### Coaching Staff Integration

```python
class CoachingDashboardIntegration:
    def __init__(self, tactical_api_url: str):
        self.api_url = tactical_api_url

    def push_pre_match_dossier(self, match_id: str, dossier: PreMatchDossier):
        payload = {
            "match_id": match_id,
            "opponent_formation": dossier.opponent_formation,
            "pressing_triggers": dossier.pressing_triggers,
            "set_piece_vulnerabilities": dossier.set_piece_vulnerabilities,
            "key_players": dossier.key_player_profiles,
            "recommended_tactics": dossier.tactical_recommendations,
        }
        response = requests.post(
            f"{self.api_url}/dossiers",
            json=payload,
            headers={"Authorization": f"Bearer {self.coach_token}"},
        )
        return response.json()

    def stream_live_tactics(self, match_id: str):
        ws = websocket.create_connection(
            f"{self.api_url}/live/{match_id}",
            header={"Authorization": f"Bearer {self.coach_token}"}
        )
        for message in ws:
            tactical_update = json.loads(message)
            yield tactical_update
```

### Broadcast Graphics Integration

```python
class BroadcastGraphicsBridge:
    def __init__(self, graphics_api: str):
        self.graphics_api = graphics_api

    def update_formation_overlay(self, match_id: str, formation: Formation):
        overlay_data = {
            "type": "formation_overlay",
            "match_id": match_id,
            "team": formation.team_id,
            "shape": formation.primary_shape,
            "players": [
                {
                    "id": p.player_id,
                    "name": p.display_name,
                    "x": p.position_x,
                    "y": p.position_y,
                    "role": p.role,
                }
                for p in formation.players
            ],
            "confidence": formation.confidence,
        }
        requests.post(
            f"{self.graphics_api}/overlays",
            json=overlay_data,
        )

    def render_pass_network(self, network: PassNetwork, output_format: str = "svg"):
        svg_data = network.to_svg(
            width=1920,
            height=1080,
            pitch_color="green",
            node_color="white",
            edge_color="yellow",
        )
        return svg_data
```

## Performance Optimization

### Spatial Indexing for Zone Queries

```python
from shapely.geometry import Point
from shapely.strtree import STRtree

class SpatialZoneIndex:
    def __init__(self, pitch_zones: List[PitchZone]):
        self.zones = pitch_zones
        self.geometries = [zone.geometry for zone in pitch_zones]
        self.tree = STRtree(self.geometries)

    def get_zone(self, x: float, y: float) -> PitchZone:
        point = Point(x, y)
        idx = self.tree.query(point)
        return self.zones[idx]

    def get_zones_in_region(self, min_x: float, max_x: float,
                            min_y: float, max_y: float) -> List[PitchZone]:
        from shapely.geometry import box
        region = box(min_x, min_y, max_x, max_y)
        indices = self.tree.query(region)
        return [self.zones[i] for i in indices]
```

### Cached Pattern Database

```python
from functools import lru_cache
import hashlib

class PatternCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    def _make_key(self, match_ids: tuple, team_id: str) -> str:
        content = f"{match_ids}:{team_id}"
        return f"patterns:{hashlib.md5(content.encode()).hexdigest()}"

    def get_patterns(self, match_ids: tuple, team_id: str) -> Optional[List]:
        key = self._make_key(match_ids, team_id)
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None

    def set_patterns(self, match_ids: tuple, team_id: str, patterns: List, ttl: int = 3600):
        key = self._make_key(match_ids, team_id)
        self.redis.setex(key, ttl, json.dumps(patterns))
```

### Parallel Pattern Mining

```python
from concurrent.futures import ProcessPoolExecutor
from typing import List

class ParallelPatternMiner:
    def __init__(self, num_workers: int = 8):
        self.executor = ProcessPoolExecutor(max_workers=num_workers)

    def mine_patterns_parallel(
        self,
        match_data_chunks: List[List[EventSequence]],
        config: PatternMiningConfig,
    ) -> List[Pattern]:
        futures = []
        for chunk in match_data_chunks:
            future = self.executor.submit(
                self._mine_chunk, chunk, config
            )
            futures.append(future)

        all_patterns = []
        for future in futures:
            patterns = future.result(timeout=60)
            all_patterns.extend(patterns)

        return self._deduplicate_patterns(all_patterns)
```

## Security Considerations

### API Authentication

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TacticalAPIAuth:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    async def verify_token(self, token: str = Depends(oauth2_scheme)) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            if "tactical:read" not in payload.get("scopes", []):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
```

### Data Sanitization

```python
import re

class TacticalDataSanitizer:
    SENSITIVE_PATTERNS = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b\d{16}\b',              # Credit card
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
    ]

    def sanitize_match_data(self, data: dict) -> dict:
        sanitized = json.dumps(data)
        for pattern in self.SENSITIVE_PATTERNS:
            sanitized = re.sub(pattern, "[REDACTED]", sanitized)
        return json.loads(sanitized)

    def sanitize_coaching_notes(self, notes: str) -> str:
        return re.sub(r'\b\d{3}-\d{2}-\d{4}\b', "[REDACTED]", notes)
```

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Formation detection shows wrong shape | Insufficient tracking data points | Increase time window; check tracking data quality |
| Pattern mining returns no results | min_support threshold too high | Lower min_support; ensure sufficient match data |
| xT values seem unrealistic | Markov model not converged | Increase max_iterations; verify training data quality |
| Live dashboard has high latency | WebSocket connection pooling issue | Increase connection pool; check network bandwidth |
| Pressing triggers not identified | Accelerometer threshold misconfigured | Adjust high_press_threshold; validate sensor calibration |
| Pass network shows isolated nodes | min_passes threshold too high | Lower threshold; check event data completeness |

### Debugging Formation Detection

```python
from game_strategy.diagnostics import FormationDebugger

debugger = FormationDebugger(match_id="match_2024_01")

# Inspect clustering quality
cluster_report = debugger.analyze_clusters(time_window="45-60")
print(f"Clusters found: {cluster_report.num_clusters}")
print(f"Silhouette score: {cluster_report.silhouette_score:.3f}")
print(f"Davies-Bouldin index: {cluster_report.davies_bouldin:.3f}")

# Check position data quality
quality = debugger.check_tracking_quality()
print(f"Missing positions: {quality.missing_count}")
print(f"Outlier positions: {quality.outlier_count}")
print(f"Average position uncertainty: {quality.avg_uncertainty_m:.2f}m")
```

### xT Model Validation

```python
from game_strategy.validation import XTValidator

validator = XTValidator(model_path="models/xt_v2_markov.pkl")

# Validate against historical data
validation = validator.validate(
    test_matches=["match_2024_01", "match_2024_02", "match_2024_03"],
    metric="calibration_error",
)

print(f"Calibration error: {validation.calibration_error:.4f}")
print(f"Kendall tau correlation: {validation.kendall_tau:.3f}")
print(f"Zone value range: [{validation.min_zone_value:.4f}, {validation.max_zone_value:.4f}]")
```

## API Reference

### Core Classes

| Class | Description | Key Methods |
|-------|-------------|-------------|
| `FormationDetector` | Unsupervised formation detection | `detect()`, `get_transitions()`, `confidence_score()` |
| `PatternMiner` | Sequential pattern mining | `mine()`, `top_k()`, `filter_by_type()` |
| `PressingAnalyzer` | Pressing trigger identification | `identify_triggers()`, `analyze_success_rate()` |
| `XTModel` | Expected threat computation | `evaluate_action()`, `evaluate_chain()`, `season_summary()` |
| `PlayCallingEngine` | Tactical recommendation engine | `get_recommendations()`, `rank_strategies()` |
| `SetPieceDesigner` | Set-piece design tool | `design_routine()`, `evaluate_vs_opponent()` |

### Data Classes

| Class | Description | Key Fields |
|-------|-------------|------------|
| `Formation` | Detected formation snapshot | `team_id, primary_shape, confidence, players, time_range` |
| `Pattern` | Discovered tactical pattern | `event_sequence, support, confidence, avg_xt_gain` |
| `PressingTrigger` | Identified pressing condition | `condition, zone, frequency, success_rate` |
| `XTValue` | Action value | `action_type, origin_zone, dest_zone, xt_gain` |
| `TacticalRecommendation` | Play calling suggestion | `strategy, confidence, expected_impact, rationale` |

## Data Models

### Tactical Data Schema

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│     Matches      │     │   Formations      │     │    Patterns     │
├─────────────────┤     ├──────────────────┤     ├─────────────────┤
│ match_id (PK)   │────<│ formation_id (PK)│────<│ pattern_id (PK) │
│ home_team        │     │ match_id (FK)    │     │ match_ids       │
│ away_team        │     │ team_id (FK)     │     │ team_id         │
│ date             │     │ shape            │     │ event_sequence  │
│ competition      │     │ confidence       │     │ support         │
└─────────────────┘     │ time_start       │     │ confidence      │
                        │ time_end         │     │ avg_xt_gain     │
┌─────────────────┐     │ transition_from  │     │ created_at      │
│   xT Grid       │     └──────────────────┘     └─────────────────┘
├─────────────────┤
│ zone_id (PK)    │     ┌──────────────────┐
│ row             │     │  Pressing Triggers│
│ col             │     ├──────────────────┤
│ zone_value      │     │ trigger_id (PK)  │
│ transition_probs│     │ team_id          │
│ shot_probability│     │ condition        │
│ goal_probability│     │ zone_id          │
└─────────────────┘     │ frequency        │
                        │ success_rate     │
                        │ avg_recovery_sec │
                        └──────────────────┘
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: game-strategy-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: game-strategy
  template:
    metadata:
      labels:
        app: game-strategy
    spec:
      containers:
      - name: api
        image: game-strategy:1.0.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: strategy-secrets
              key: redis-url
        - name: MODEL_PATH
          value: "/models"
        volumeMounts:
        - name: model-volume
          mountPath: /models
      volumes:
      - name: model-volume
        persistentVolumeClaim:
          claimName: strategy-models-pvc
```

## Monitoring & Observability

### Tactical Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

FORMATION_DETECTIONS = Counter(
    'formation_detections_total',
    'Total formation detections',
    ['team_id', 'formation_shape']
)

PATTERN_MINING_DURATION = Histogram(
    'pattern_mining_duration_seconds',
    'Time to mine patterns',
    ['algorithm'],
    buckets=[1, 5, 10, 30, 60, 120]
)

XT_COMPUTATIONS = Counter(
    'xt_computations_total',
    'Total xT computations',
    ['action_type']
)

LIVE_DASHBOARD_LATENCY = Histogram(
    'live_dashboard_latency_seconds',
    'End-to-end dashboard update latency',
    buckets=[0.1, 0.25, 0.5, 1.0, 2.0]
)

ACTIVE_MATCHES = Gauge(
    'active_matches_analyzed',
    'Number of matches with active tactical analysis'
)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from game_strategy import FormationDetector, XTModel

class TestFormationDetector:
    def setup_method(self):
        self.detector = FormationDetector(
            time_window_seconds=60,
            cluster_method="dbscan",
        )

    def test_433_detection(self, sample_433_tracking):
        formation = self.detector.detect_single_window(sample_433_tracking)
        assert formation.shape == "4-3-3"
        assert formation.confidence > 0.8

    def test_transition_detection(self, sample_transition_data):
        transitions = self.detector.detect_transitions(sample_transition_data)
        assert len(transitions) > 0
        assert all(t.confidence > 0.5 for t in transitions)

class TestXTModel:
    def setup_method(self):
        self.model = XTModel(grid_cols=16, grid_rows=12)

    def test_shot_xt_positive(self):
        shot_action = {"type": "shot", "from": (85, 50), "xg": 0.3}
        xt = self.model.evaluate_action(shot_action)
        assert xt > 0

    def test_own_half_xt_negative(self):
        back_pass = {"type": "pass", "from": (50, 50), "to": (20, 50)}
        xt = self.model.evaluate_action(back_pass)
        assert xt <= 0
```

### Integration Tests

```python
class TestTacticalPipelineIntegration:
    def test_full_analysis_pipeline(self, sample_match_data):
        detector = FormationDetector()
        miner = PatternMiner()
        xt_model = XTModel()

        formations = detector.detect(sample_match_data)
        patterns = miner.mine_from_match(sample_match_data)
        xt_values = xt_model.evaluate_match(sample_match_data)

        assert len(formations) > 0
        assert len(patterns) >= 0
        assert len(xt_values) > 0
```

## Versioning & Migration

### Model Versioning

```python
class TacticalModelRegistry:
    def __init__(self, registry_path: str):
        self.registry_path = registry_path

    def register_xt_model(self, model, version: str, metadata: dict):
        path = os.path.join(self.registry_path, f"xt_model_{version}.pkl")
        joblib.dump(model, path)
        self._update_manifest(version, metadata)

    def load_xt_model(self, version: str = "latest"):
        if version == "latest":
            version = self._get_latest_version()
        path = os.path.join(self.registry_path, f"xt_model_{version}.pkl")
        return joblib.load(path)
```

### Data Migration

```sql
-- Add confidence columns to formation table
ALTER TABLE formations
ADD COLUMN confidence DECIMAL(5,4) DEFAULT 0.0,
ADD COLUMN secondary_shape VARCHAR(10),
ADD COLUMN secondary_confidence DECIMAL(5,4);

-- Backfill confidence from existing data
UPDATE formations
SET confidence = 0.75
WHERE confidence = 0.0 AND shape IS NOT NULL;
```

## Glossary

| Term | Definition |
|------|------------|
| **xT (Expected Threat)** | Markov-chain model valuing on-ball actions by probability of scoring |
| **Pressing Trigger** | Specific event or condition that activates a team's high-intensity press |
| **Formation Shape** | Spatial arrangement of players in their primary tactical structure |
| **Transition Phase** | Period between possession changes (attack to defense or vice versa) |
| **Counter-Press** | Immediate pressing after losing possession to regain the ball quickly |
| **Build-Up Pattern** | Recurring sequence of passes progressing from defensive to attacking zones |
| **Set Piece** | Restart situations: corners, free kicks, throw-ins, goal kicks |
| **Zonal Marking** | Defensive system where players guard specific pitch zones |
| **Man Marking** | Defensive system where players are assigned to specific opponents |
| **Possession Value Chain** | Sequential xT values across a single possession sequence |
| **Defensive Line Height** | Average vertical position of the defensive line from own goal |
| **Pressing Intensity** | Measure of acceleration/deceleration during pressing actions |
| **Spatial Compactness** | Team's spread across the pitch (lower = more compact) |
| **Progressive Action** | Action that moves the ball significantly toward the opponent's goal |
| **Tactical Transition** | Formation shift between phases of play (e.g., 4-3-3 to 4-4-2) |

## Changelog

### Version 1.0.0 (2024-01-15)

- Initial release with formation detection and pattern mining
- xT Markov chain model for action valuation
- Real-time strategy dashboard with WebSocket streaming
- Pre-match dossier generation

### Version 1.1.0 (2024-04-01)

- Added pressing trigger analysis
- Enhanced pattern mining with PrefixSpan algorithm
- Set-piece design system with zonal/man-marking evaluation
- Counter-pressing metrics implementation

### Version 1.2.0 (2024-07-15)

- Improved formation detection with hybrid shape support
- xT model v2 with defensive pressure features
- Play calling recommendation engine
- Enhanced real-time dashboard with configurable alerts

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/sports-tech/game-strategy.git
cd game-strategy
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=game_strategy

# Run pattern mining benchmarks
python -m game_strategy.benchmarks.pattern_mining
```

### Code Standards

- All tactical algorithms must include unit tests with synthetic data
- xT model changes require validation against 100+ match test set
- Formation detection changes require testing across 4+ formation types
- Real-time components must maintain <500ms latency under load

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
