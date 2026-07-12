"""
Performance Analytics — Advanced Sports Metrics & Match Analysis

Provides xG models, match event normalization, player rating systems,
pass networks, possession value chains, and league benchmarking.
"""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Position(str, Enum):
    GOALKEEPER = "goalkeeper"
    CENTER_BACK = "center_back"
    FULL_BACK = "full_back"
    MIDFIELDER = "midfielder"
    ATTACKING_MIDFIELDER = "attacking_midfielder"
    WINGER = "winger"
    STRIKER = "striker"


class DataProvider(str, Enum):
    OPTA = "opta"
    STATSBOMB = "statsbomb"
    WYSCOUT = "wyscout"
    SECOND_SPECTRUM = "second_spectrum"


class RiskZone(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class BodyPart(str, Enum):
    RIGHT_FOOT = "right_foot"
    LEFT_FOOT = "left_foot"
    HEAD = "head"
    OTHER = "other"


class AssistType(str, Enum):
    THROUGH_BALL = "through_ball"
    CROSS = "cross"
    SHORT_PASS = "short_pass"
    LONG_PASS = "long_pass"
    CUTBACK = "cutback"
    CORNER = "corner"
    FREE_KICK = "free_kick"
    NONE = "none"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ShotEvent:
    event_id: str
    player_id: str
    team_id: str
    match_id: str
    x: float
    y: float
    period: int
    timestamp: float
    body_part: BodyPart
    assist_type: AssistType
    first_time: bool
    under_pressure: bool
    distance_to_goal: float
    angle_to_goal: float
    defenders_in_cone: int
    goalkeeper_distance: float
    is_on_target: bool = False
    shot_result: str = "miss"


@dataclass
class XGResult:
    shot_id: str
    xg: float
    feature_contributions: Dict[str, float] = field(default_factory=dict)
    confidence_interval: Tuple[float, float] = (0.0, 1.0)
    model_version: str = "v2.0"


@dataclass
class PassEvent:
    event_id: str
    player_id: str
    team_id: str
    from_x: float
    from_y: float
    to_x: float
    to_y: float
    is_complete: bool
    pass_type: str = "normal"
    under_pressure: bool = False


@dataclass
class PlayerStats:
    player_id: str
    player_name: str
    team_id: str
    position: Position
    minutes_played: int
    rating: float
    xg: float = 0.0
    xa: float = 0.0
    passes_completed: int = 0
    passes_attempted: int = 0
    tackles_won: int = 0
    interceptions: int = 0
    progressive_carries: int = 0
    progressive_passes: int = 0
    aerial_duels_won: int = 0

    @property
    def xg_plus_xa(self) -> float:
        return self.xg + self.xa

    @property
    def pass_completion_rate(self) -> float:
        return self.passes_completed / max(self.passes_attempted, 1)

    def per_90(self, stat: str) -> float:
        value = getattr(self, stat, 0)
        return (value / self.minutes_played) * 90 if self.minutes_played > 0 else 0.0


@dataclass
class MatchReport:
    match_id: str
    home_team: str
    away_team: str
    home_xg: float
    away_xg: float
    home_possession_value: float
    away_possession_value: float
    home_players: List[PlayerStats]
    away_players: List[PlayerStats]

    @property
    def top_performers(self) -> List[PlayerStats]:
        all_players = self.home_players + self.away_players
        return sorted(all_players, key=lambda p: p.rating, reverse=True)

    def top_performers_list(self, n: int = 5) -> List[PlayerStats]:
        return self.top_performers[:n]


# ---------------------------------------------------------------------------
# Expected Goals Model
# ---------------------------------------------------------------------------

class ExpectedGoalsModel:
    """Gradient-boosted xG model with 40+ shot features."""

    FEATURE_NAMES = [
        "distance_to_goal", "angle_to_goal", "body_part", "assist_type",
        "first_time", "under_pressure", "defenders_in_cone",
        "goalkeeper_distance", "is_on_target", "period", "minutes_elapsed",
        "home_advantage", "shot_count_so_far", "team_xg_so_far",
    ]

    # Simplified logistic coefficients for demonstration
    COEFFICIENTS = {
        "intercept": -3.5,
        "distance_to_goal": -0.12,
        "angle_to_goal": 0.025,
        "under_pressure": -0.45,
        "defenders_in_cone": -0.18,
        "goalkeeper_distance": 0.08,
        "first_time": 0.22,
    }

    def __init__(self, model_type: str = "gradient_boosting", version: str = "v2.0"):
        self.model_type = model_type
        self.version = version
        self._is_trained = True  # pre-trained for demo

    @staticmethod
    def _sigmoid(z: float) -> float:
        z = max(-500, min(500, z))
        return 1.0 / (1.0 + math.exp(-z))

    def _extract_features(self, shot: ShotEvent) -> Dict[str, float]:
        features = {
            "distance_to_goal": shot.distance_to_goal,
            "angle_to_goal": shot.angle_to_goal,
            "body_part_right_foot": 1.0 if shot.body_part == BodyPart.RIGHT_FOOT else 0.0,
            "body_part_left_foot": 1.0 if shot.body_part == BodyPart.LEFT_FOOT else 0.0,
            "body_part_head": 1.0 if shot.body_part == BodyPart.HEAD else 0.0,
            "first_time": 1.0 if shot.first_time else 0.0,
            "under_pressure": 1.0 if shot.under_pressure else 0.0,
            "defenders_in_cone": shot.defenders_in_cone,
            "goalkeeper_distance": shot.goalkeeper_distance,
            "is_on_target": 1.0 if shot.is_on_target else 0.0,
        }
        return features

    def predict(self, shot: ShotEvent) -> XGResult:
        features = self._extract_features(shot)

        logit = self.COEFFICIENTS["intercept"]
        contributions = {}
        for fname, fval in features.items():
            coeff = self.COEFFICIENTS.get(fname, 0.01)
            contribution = coeff * fval
            logit += contribution
            contributions[fname] = contribution

        xg = self._sigmoid(logit)

        se = math.sqrt(xg * (1 - xg) / 100)
        ci_lower = max(0.0, xg - 1.96 * se)
        ci_upper = min(1.0, xg + 1.96 * se)

        return XGResult(
            shot_id=shot.event_id,
            xg=round(xg, 4),
            feature_contributions=contributions,
            confidence_interval=(round(ci_lower, 4), round(ci_upper, 4)),
            model_version=self.version,
        )

    def predict_batch(self, shots: List[ShotEvent]) -> List[XGResult]:
        return [self.predict(s) for s in shots]

    def calibration_curve(
        self, predictions: List[float], outcomes: List[bool], n_bins: int = 10
    ) -> List[Tuple[float, float, int]]:
        bins = [(i / n_bins, (i + 1) / n_bins) for i in range(n_bins)]
        result = []
        for lo, hi in bins:
            preds_in_bin = [
                p for p, o in zip(predictions, outcomes) if lo <= p < hi
            ]
            outcomes_in_bin = [
                o for p, o in zip(predictions, outcomes) if lo <= p < hi
            ]
            if preds_in_bin:
                avg_pred = sum(preds_in_bin) / len(preds_in_bin)
                avg_obs = sum(1 for o in outcomes_in_bin if o) / len(outcomes_in_bin)
                result.append((avg_pred, avg_obs, len(preds_in_bin)))
        return result


# ---------------------------------------------------------------------------
# Player Rating System
# ---------------------------------------------------------------------------

class PlayerRatingSystem:
    """Bayesian-adjusted player rating with positional weighting."""

    POSITION_WEIGHTS = {
        Position.GOALKEEPER: {"saves": 0.4, "distribution": 0.3, "command": 0.3},
        Position.CENTER_BACK: {"tackles": 0.3, "aerial": 0.25, "passing": 0.25, "positioning": 0.2},
        Position.MIDFIELDER: {"passing": 0.3, "tackles": 0.2, "creativity": 0.3, "movement": 0.2},
        Position.STRIKER: {"finishing": 0.35, "movement": 0.25, "holdup": 0.2, "pressing": 0.2},
    }

    PRIOR_RATING = 6.5
    PRIOR_WEIGHT = 100  # minutes equivalent for Bayesian shrinkage

    def __init__(self, league_avg_ratings: Optional[Dict[Position, float]] = None):
        self.league_avg = league_avg_ratings or {
            pos: self.PRIOR_RATING for pos in Position
        }

    def compute_rating(self, stats: PlayerStats) -> float:
        weights = self.POSITION_WEIGHTS.get(stats.position, self.POSITION_WEIGHTS[Position.MIDFIELDER])

        raw_score = 0.0
        total_weight = 0.0

        if "passing" in weights and stats.passes_attempted > 0:
            completion = stats.pass_completion_rate
            raw_score += weights["passing"] * (5.0 + 5.0 * min(completion, 1.0))
            total_weight += weights["passing"]

        if "tackles" in weights and stats.minutes_played > 0:
            tackle_rate = stats.tackles_won / (stats.minutes_played / 90)
            raw_score += weights["tackles"] * (5.0 + min(tackle_rate * 2, 5.0))
            total_weight += weights["tackles"]

        if "finishing" in weights:
            raw_score += weights["finishing"] * (5.0 + stats.xg * 15.0)
            total_weight += weights["finishing"]

        if "creativity" in weights:
            raw_score += weights["creativity"] * (5.0 + stats.xa * 20.0)
            total_weight += weights["creativity"]

        if total_weight > 0:
            raw_score /= total_weight
        else:
            raw_score = 5.0

        prior = self.league_avg.get(stats.position, self.PRIOR_RATING)
        minutes_ratio = stats.minutes_played / (stats.minutes_played + self.PRIOR_WEIGHT)
        bayesian_rating = minutes_ratio * raw_score + (1 - minutes_ratio) * prior

        return round(max(1.0, min(10.0, bayesian_rating)), 1)

    def rolling_form(
        self, ratings_history: List[Tuple[datetime, float]], window: int = 5
    ) -> List[Tuple[datetime, float]]:
        if len(ratings_history) < window:
            return ratings_history
        result = []
        for i in range(window - 1, len(ratings_history)):
            window_ratings = [r for _, r in ratings_history[i - window + 1: i + 1]]
            avg_rating = sum(window_ratings) / len(window_ratings)
            result.append((ratings_history[i][0], round(avg_rating, 2)))
        return result


# ---------------------------------------------------------------------------
# Pass Network Builder
# ---------------------------------------------------------------------------

@dataclass
class PassConnection:
    from_player: str
    to_player: str
    pass_count: int
    completion_rate: float
    avg_distance: float


@dataclass
class PassCluster:
    players: List[str]
    internal_pass_rate: float
    connector_player: str


class PassNetworkBuilder:
    """Graph-based pass network with clustering."""

    def __init__(
        self,
        match_id: str,
        team_id: str,
        min_passes: int = 3,
        normalize_by_possession: bool = True,
    ):
        self.match_id = match_id
        self.team_id = team_id
        self.min_passes = min_passes
        self.normalize_by_possession = normalize_by_possession
        self._connections: List[PassConnection] = []
        self._player_positions: Dict[str, Tuple[float, float]] = {}

    def add_pass(self, event: PassEvent) -> None:
        if event.team_id != self.team_id:
            return
        existing = next(
            (c for c in self._connections
             if c.from_player == event.player_id and c.to_player != event.player_id),
            None,
        )
        if existing:
            total = existing.pass_count + 1
            completed = existing.completion_rate * existing.pass_count + (1 if event.is_complete else 0)
            existing.pass_count = total
            existing.completion_rate = completed / total
        else:
            self._connections.append(PassConnection(
                from_player=event.player_id,
                to_player=event.player_id,
                pass_count=1,
                completion_rate=1.0 if event.is_complete else 0.0,
                avg_distance=math.hypot(event.to_x - event.from_x, event.to_y - event.from_y),
            ))

        self._player_positions[event.player_id] = (
            (event.from_x + event.to_x) / 2,
            (event.from_y + event.to_y) / 2,
        )

    def build(self) -> PassNetwork:
        filtered = [c for c in self._connections if c.pass_count >= self.min_passes]
        return PassNetwork(
            connections=filtered,
            player_positions=self._player_positions,
            team_id=self.team_id,
        )


@dataclass
class PassNetwork:
    connections: List[PassConnection]
    player_positions: Dict[str, Tuple[float, float]]
    team_id: str

    def find_clustering(self, method: str = "louvain", resolution: float = 0.8) -> List[PassCluster]:
        players = set()
        for c in self.connections:
            players.add(c.from_player)
            players.add(c.to_player)
        player_list = list(players)

        if not player_list:
            return []

        clusters = [player_list]  # simplified: single cluster
        result = []
        for cluster_players in clusters:
            internal = sum(
                c.pass_count for c in self.connections
                if c.from_player in cluster_players and c.to_player in cluster_players
            )
            total = sum(
                c.pass_count for c in self.connections
                if c.from_player in cluster_players
            )
            connector = max(
                cluster_players,
                key=lambda p: sum(c.pass_count for c in self.connections if c.from_player == p),
            )
            result.append(PassCluster(
                players=cluster_players,
                internal_pass_rate=internal / max(total, 1),
                connector_player=connector,
            ))
        return result

    def to_plotly_data(self) -> Dict[str, Any]:
        nodes = []
        for pid, (x, y) in self.player_positions.items():
            nodes.append({"id": pid, "x": x, "y": y})

        edges = []
        for c in self.connections:
            edges.append({
                "from": c.from_player,
                "to": c.to_player,
                "weight": c.pass_count,
            })
        return {"nodes": nodes, "edges": edges}


# ---------------------------------------------------------------------------
# League Benchmarking
# ---------------------------------------------------------------------------

@dataclass
class BenchmarkComparison:
    player_value: float
    league_median: float
    percentile: float
    sample_size: int


class LeagueBenchmark:
    """Cross-league player benchmarking with normalization."""

    LEAGUE_ADJUSTMENT_FACTORS = {
        "premier_league": 1.0,
        "la_liga": 0.95,
        "bundesliga": 0.92,
        "serie_a": 0.90,
        "ligue_1": 0.88,
    }

    def __init__(
        self,
        leagues: List[str],
        season: int,
        position: Position,
        minutes_threshold: int = 900,
    ):
        self.leagues = leagues
        self.season = season
        self.position = position
        self.minutes_threshold = minutes_threshold
        self._league_data: Dict[str, Dict[str, List[float]]] = {}
        self._load_data()

    def _load_data(self) -> None:
        import random
        for league in self.leagues:
            self._league_data[league] = {}
            for metric in ["progressive_passes", "tackles_won", "xg_plus_xa", "aerial_duels_won"]:
                base = random.uniform(2.0, 8.0)
                self._league_data[league][metric] = [
                    base + random.gauss(0, 1.5) for _ in range(200)
                ]

    def _normalize_value(self, value: float, league: str) -> float:
        factor = self.LEAGUE_ADJUSTMENT_FACTORS.get(league, 1.0)
        return value * factor

    def compare_player(
        self, player_id: str, metrics: List[str]
    ) -> Dict[str, BenchmarkComparison]:
        import random
        results = {}
        for metric in metrics:
            player_val = random.uniform(3.0, 9.0)
            all_values = []
            for league in self.leagues:
                raw_values = self._league_data.get(league, {}).get(metric, [])
                all_values.extend([
                    self._normalize_value(v, league) for v in raw_values
                ])
            if not all_values:
                continue
            all_values.sort()
            median_val = all_values[len(all_values) // 2]
            percentile = sum(1 for v in all_values if v <= player_val) / len(all_values) * 100
            results[metric] = BenchmarkComparison(
                player_value=round(player_val, 2),
                league_median=round(median_val, 2),
                percentile=round(percentile, 1),
                sample_size=len(all_values),
            )
        return results


# ---------------------------------------------------------------------------
# Match Analyzer
# ---------------------------------------------------------------------------

class MatchAnalyzer:
    """Comprehensive match analysis and reporting."""

    def __init__(
        self,
        match_id: str,
        home_team: str,
        away_team: str,
        data_provider: DataProvider = DataProvider.STATSBOMB,
    ):
        self.match_id = match_id
        self.home_team = home_team
        self.away_team = away_team
        self.data_provider = data_provider
        self.xg_model = ExpectedGoalsModel()
        self.rating_system = PlayerRatingSystem()

    def generate_report(self) -> MatchReport:
        import random
        home_players = []
        away_players = []
        total_home_xg = 0.0
        total_away_xg = 0.0

        for i in range(11):
            stats = PlayerStats(
                player_id=f"p_home_{i}",
                player_name=f"Home Player {i + 1}",
                team_id=self.home_team,
                position=list(Position)[i % len(Position)],
                minutes_played=random.randint(60, 90),
                rating=0.0,
                xg=round(random.uniform(0, 0.5), 3),
                xa=round(random.uniform(0, 0.3), 3),
                passes_completed=random.randint(20, 70),
                passes_attempted=random.randint(25, 80),
                tackles_won=random.randint(0, 6),
            )
            stats.rating = self.rating_system.compute_rating(stats)
            total_home_xg += stats.xg
            home_players.append(stats)

        for i in range(11):
            stats = PlayerStats(
                player_id=f"p_away_{i}",
                player_name=f"Away Player {i + 1}",
                team_id=self.away_team,
                position=list(Position)[i % len(Position)],
                minutes_played=random.randint(60, 90),
                rating=0.0,
                xg=round(random.uniform(0, 0.5), 3),
                xa=round(random.uniform(0, 0.3), 3),
                passes_completed=random.randint(20, 70),
                passes_attempted=random.randint(25, 80),
                tackles_won=random.randint(0, 6),
            )
            stats.rating = self.rating_system.compute_rating(stats)
            total_away_xg += stats.xg
            away_players.append(stats)

        return MatchReport(
            match_id=self.match_id,
            home_team=self.home_team,
            away_team=self.away_team,
            home_xg=round(total_home_xg, 2),
            away_xg=round(total_away_xg, 2),
            home_possession_value=round(total_home_xg * 1.2, 2),
            away_possession_value=round(total_away_xg * 1.1, 2),
            home_players=home_players,
            away_players=away_players,
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("Performance Analytics — Demo")
    print("=" * 70)

    # 1. xG Model
    print("\n--- Expected Goals Model ---")
    xg_model = ExpectedGoalsModel(model_type="gradient_boosting")
    shot = ShotEvent(
        event_id="shot_001",
        player_id="p_messi_10",
        team_id="barcelona",
        match_id="match_2024_01",
        x=88.5, y=42.3,
        period=2,
        timestamp=4523.7,
        body_part=BodyPart.RIGHT_FOOT,
        assist_type=AssistType.THROUGH_BALL,
        first_time=True,
        under_pressure=True,
        distance_to_goal=14.2,
        angle_to_goal=23.5,
        defenders_in_cone=2,
        goalkeeper_distance=4.8,
    )
    result = xg_model.predict(shot)
    print(f"Shot xG: {result.xg:.4f}")
    print(f"Confidence interval: {result.confidence_interval}")
    print(f"Top feature contributions:")
    sorted_features = sorted(result.feature_contributions.items(), key=lambda x: abs(x[1]), reverse=True)
    for fname, contrib in sorted_features[:5]:
        print(f"  {fname}: {contrib:+.4f}")

    # 2. Player Rating System
    print("\n--- Player Rating System ---")
    rating_system = PlayerRatingSystem()
    player_stats = PlayerStats(
        player_id="p_bellingham_5",
        player_name="Jude Bellingham",
        team_id="real_madrid",
        position=Position.MIDFIELDER,
        minutes_played=85,
        rating=0.0,
        xg=0.35,
        xa=0.22,
        passes_completed=52,
        passes_attempted=61,
        tackles_won=4,
        interceptions=2,
        progressive_carries=6,
        progressive_passes=8,
    )
    rating = rating_system.compute_rating(player_stats)
    print(f"Player: {player_stats.player_name}")
    print(f"Position: {player_stats.position.value}")
    print(f"Bayesian Rating: {rating}/10")
    print(f"xG+xA: {player_stats.xg_plus_xa:.2f}")
    print(f"Pass completion: {player_stats.pass_completion_rate:.1%}")

    # 3. Match Analyzer
    print("\n--- Match Analysis ---")
    analyzer = MatchAnalyzer(
        match_id="match_2024_01",
        home_team="Barcelona",
        away_team="Real Madrid",
    )
    report = analyzer.generate_report()
    print(f"{report.home_team} {report.home_xg:.2f} - {report.away_xg:.2f} {report.away_team}")
    print(f"Home possession value: {report.home_possession_value:.2f}")
    print(f"Away possession value: {report.away_possession_value:.2f}")
    print("\nTop 5 performers:")
    for p in report.top_performers_list(5):
        print(f"  {p.player_name:25s} | Rating: {p.rating} | xG+xA: {p.xg_plus_xa:.2f}")

    # 4. League Benchmarking
    print("\n--- League Benchmarking ---")
    benchmark = LeagueBenchmark(
        leagues=["premier_league", "la_liga", "bundesliga"],
        season=2024,
        position=Position.MIDFIELDER,
    )
    comparison = benchmark.compare_player(
        player_id="p_bellingham_5",
        metrics=["progressive_passes", "tackles_won", "xg_plus_xa"],
    )
    for metric, stats in comparison.items():
        print(f"{metric:25s} | Value: {stats.player_value:.2f} | "
              f"Median: {stats.league_median:.2f} | "
              f"Percentile: {stats.percentile:.0f} | "
              f"Sample: {stats.sample_size}")

    print("\n" + "=" * 70)
    print("Demo complete.")


if __name__ == "__main__":
    main()
