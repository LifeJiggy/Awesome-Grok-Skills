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
