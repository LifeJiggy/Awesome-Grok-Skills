"""
Fan Engagement — Fantasy Analytics, Sentiment Tracking & Interactive Experiences

Provides fantasy projection engines, sentiment analysis, dynamic ticket
pricing, live second-screen experiences, and gamification frameworks.
"""

from __future__ import annotations

import math
import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Platform(str, Enum):
    ESPN = "espn"
    YAHOO = "yahoo"
    FANDUEL = "fanduel"
    DRAFTKINGS = "draftkings"


class Position(str, Enum):
    QUARTERBACK = "QB"
    RUNNING_BACK = "RB"
    WIDE_RECEIVER = "WR"
    TIGHT_END = "TE"
    FLEX = "FLEX"
    DEFENSE = "DEF"
    KICKER = "K"


class SentimentLabel(str, Enum):
    VERY_NEGATIVE = "very_negative"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    VERY_POSITIVE = "very_positive"


class ReadinessStatus(str, Enum):
    READY = "READY"
    CAUTION = "CAUTION"
    NOT_READY = "NOT_READY"


class InteractiveType(str, Enum):
    POLL = "poll"
    PREDICTION = "prediction"
    TRIVIA = "trivia"
    HEATMAP = "heatmap"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class PlayerProjection:
    player_id: str
    name: str
    position: Position
    team: str
    opponent: str
    projected_points: float
    salary: int
    floor: float
    ceiling: float
    injury_status: str = "healthy"
    projected_ownership: float = 0.0

    @property
    def points_per_dollar(self) -> float:
        return self.projected_points / max(self.salary, 1) * 1000

    @property
    def value_tier(self) -> str:
        ppd = self.points_per_dollar
        if ppd > 3.0:
            return "elite"
        elif ppd > 2.5:
            return "strong"
        elif ppd > 2.0:
            return "fair"
        return "overpriced"


@dataclass
class LineupSlot:
    position: Position
    player: PlayerProjection


@dataclass
class OptimizedLineup:
    slots: List[LineupSlot]
    total_salary: int
    expected_points: float
    optimal: bool = True

    @property
    def remaining_salary(self) -> int:
        return 50000 - self.total_salary

    def roster_display(self) -> str:
        lines = []
        for slot in self.slots:
            lines.append(f"  {slot.position.value:4s} | {slot.player.name:25s} "
                        f"| ${slot.player.salary:,} | {slot.player.projected_points:.1f} pts")
        return "\n".join(lines)


@dataclass
class SentimentEvent:
    timestamp: str
    trigger: str
    sentiment_score: float
    positive_pct: float
    negative_pct: float
    mention_count: int
    top_phrase: str
    viral_score: float


@dataclass
class SentimentSummary:
    avg_sentiment: float
    peak_positive_moment: str
    peak_negative_moment: str
    brand_impact_score: float
    total_mentions: int
    sentiment_trend: str


@dataclass
class TicketZone:
    name: str
    base_price: float
    optimal_price: float
    multiplier: float
    projected_sell_through: float
    inventory: int


@dataclass
class PriceElasticity:
    zone: str
    coefficient: float
    optimal_price: float
    revenue_at_optimal: float


@dataclass
class TradeValue:
    player_id: str
    name: str
    rest_of_season_value: float
    age_adjustment: float
    injury_risk_factor: float
    schedule_strength: float
    total_value: float
    trend: str  # "rising", "stable", "declining"


@dataclass
class InteractiveElement:
    element_id: str
    interactive_type: InteractiveType
    question: str
    options: List[str]
    duration_seconds: int
    point_value: int = 0
    min_votes: int = 0

    @classmethod
    def poll(cls, question: str, options: List[str], duration_seconds: int = 60,
             min_votes: int = 100) -> InteractiveElement:
        return cls(
            element_id=str(uuid.uuid4())[:8],
            interactive_type=InteractiveType.POLL,
            question=question,
            options=options,
            duration_seconds=duration_seconds,
            min_votes=min_votes,
        )

    @classmethod
    def prediction(cls, question: str, options: List[str], point_value: int = 50,
                   duration_seconds: int = 120) -> InteractiveElement:
        return cls(
            element_id=str(uuid.uuid4())[:8],
            interactive_type=InteractiveType.PREDICTION,
            question=question,
            options=options,
            duration_seconds=duration_seconds,
            point_value=point_value,
        )


@dataclass
class UpdateEvent:
    type: str
    data: Dict[str, Any]


# ---------------------------------------------------------------------------
# Fantasy Engine
# ---------------------------------------------------------------------------

class FantasyEngine:
    """Platform-specific fantasy projection and lineup optimization."""

    SCORING_RULES = {
        Platform.DRAFTKINGS: {
            Position.QUARTERBACK: {"pass_yard": 0.04, "pass_td": 4, "rush_yard": 0.1, "interception": -1},
            Position.RUNNING_BACK: {"rush_yard": 0.1, "rush_td": 6, "reception": 1, "rec_yard": 0.1},
            Position.WIDE_RECEIVER: {"reception": 1, "rec_yard": 0.1, "rec_td": 6, "rush_yard": 0.1},
            Position.TIGHT_END: {"reception": 1, "rec_yard": 0.1, "rec_td": 6},
        },
        Platform.FANDUEL: {
            Position.QUARTERBACK: {"pass_yard": 0.04, "pass_td": 4, "rush_yard": 0.1, "interception": -1},
            Position.RUNNING_BACK: {"rush_yard": 0.1, "rush_td": 6, "reception": 0.5, "rec_yard": 0.1},
            Position.WIDE_RECEIVER: {"reception": 0.5, "rec_yard": 0.1, "rec_td": 6},
            Position.TIGHT_END: {"reception": 0.5, "rec_yard": 0.1, "rec_td": 6},
        },
    }

    def __init__(self, platform: Platform = Platform.DRAFTKINGS):
        self.platform = platform
        self.scoring_rules = self.SCORING_RULES.get(platform, self.SCORING_RULES[Platform.DRAFTKINGS])

    def project_players(
        self,
        sport: str = "nfl",
        week: int = 14,
        include_injury_status: bool = True,
        include_weather_adjustments: bool = True,
    ) -> List[PlayerProjection]:
        players = []
        positions = [Position.QUARTERBACK, Position.RUNNING_BACK, Position.WIDE_RECEIVER, Position.TIGHT_END]
        names = [
            "Patrick Mahomes", "Josh Allen", "Lamar Jackson", "Jalen Hurts",
            "Derrick Henry", "Christian McCaffrey", "Saquon Barkley", "Breece Hall",
            "Tyreek Hill", "CeeDee Lamb", "Amon-Ra St. Brown", "Davante Adams",
            "Travis Kelce", "Mark Andrews", "T.J. Hockenson", "Sam LaPorta",
        ]
        teams = ["KC", "BUF", "BAL", "PHI", "TEN", "SF", "NYG", "NYJ",
                 "MIA", "DAL", "DET", "GB", "KC", "BAL", "MIN", "DET"]

        for i, name in enumerate(names):
            pos = positions[i % len(positions)]
            pts = round(random.uniform(8, 35), 1)
            salary = random.choice([4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500])
            players.append(PlayerProjection(
                player_id=f"p_{i:03d}",
                name=name,
                position=pos,
                team=teams[i],
                opponent=teams[(i + 5) % len(teams)],
                projected_points=pts,
                salary=salary,
                floor=round(pts * 0.5, 1),
                ceiling=round(pts * 1.8, 1),
                injury_status="healthy" if random.random() > 0.2 else "questionable",
                projected_ownership=round(random.uniform(0.05, 0.35), 2),
            ))
        return players

    def optimize_lineup(
        self,
        budget: int = 50000,
        roster_slots: Optional[List[Tuple[Position, int]]] = None,
        optimization_metric: str = "expected_points",
        correlation_pairs: Optional[List[Tuple[str, str]]] = None,
    ) -> OptimizedLineup:
        roster_slots = roster_slots or [
            (Position.QUARTERBACK, 1),
            (Position.RUNNING_BACK, 2),
            (Position.WIDE_RECEIVER, 3),
            (Position.TIGHT_END, 1),
            (Position.FLEX, 1),
            (Position.DEFENSE, 1),
        ]

        players = self.project_players()
        slots = []
        used_players = set()
        remaining_budget = budget

        for pos, count in roster_slots:
            candidates = [
                p for p in players
                if p.position == pos and p.player_id not in used_players
            ]
            candidates.sort(key=lambda p: p.points_per_dollar, reverse=True)

            for _ in range(count):
                for candidate in candidates:
                    if candidate.salary <= remaining_budget and candidate.player_id not in used_players:
                        slots.append(LineupSlot(position=pos, player=candidate))
                        used_players.add(candidate.player_id)
                        remaining_budget -= candidate.salary
                        break

        total_salary = sum(s.player.salary for s in slots)
        expected_points = sum(s.player.projected_points for s in slots)

        return OptimizedLineup(
            slots=slots,
            total_salary=total_salary,
            expected_points=round(expected_points, 1),
        )


# ---------------------------------------------------------------------------
# Trade Value Calculator
# ---------------------------------------------------------------------------

class TradeValueCalculator:
    """Dynamic player trade valuations with age curves and injury risk."""

    AGE_CURVE_PEAK = 26
    AGE_CURVE_DECLINE_RATE = 0.05

    def __init__(self, season: int = 2024):
        self.season = season

    def _age_adjustment(self, age: int) -> float:
        if age <= self.AGE_CURVE_PEAK:
            return 1.0 + (self.AGE_CURVE_PEAK - age) * 0.02
        decline_years = age - self.AGE_CURVE_PEAK
        return max(0.3, 1.0 - decline_years * self.AGE_CURVE_DECLINE_RATE)

    def compute_values(self, players: List[Dict[str, Any]]) -> List[TradeValue]:
        values = []
        for p in players:
            age_adj = self._age_adjustment(p.get("age", 25))
            injury_risk = 1.0 - p.get("injury_history_count", 0) * 0.08
            schedule_str = 1.0 + p.get("remaining_schedule_difficulty", 0) * 0.1
            ros_value = p.get("rest_of_season_projection", 100)

            total = ros_value * age_adj * injury_risk * schedule_str
            trend = "rising" if total > ros_value * 1.1 else "declining" if total < ros_value * 0.9 else "stable"

            values.append(TradeValue(
                player_id=p.get("id", ""),
                name=p.get("name", "Unknown"),
                rest_of_season_value=round(ros_value, 1),
                age_adjustment=round(age_adj, 3),
                injury_risk_factor=round(injury_risk, 3),
                schedule_strength=round(schedule_str, 3),
                total_value=round(total, 1),
                trend=trend,
            ))
        return sorted(values, key=lambda v: v.total_value, reverse=True)


# ---------------------------------------------------------------------------
# Sentiment Analyzer
# ---------------------------------------------------------------------------

class SentimentAnalyzer:
    """Real-time fan sentiment tracking across social platforms."""

    SPORT_LEXICON = {
        "hat trick": 0.9, "goal": 0.7, "assist": 0.6, "save": 0.5,
        "red card": -0.6, "penalty": 0.3, "foul": -0.3, "offside": -0.2,
        "champion": 0.9, "choke": -0.7, "clutch": 0.8, "bottle": -0.5,
        "mvp": 0.8, "trash": -0.6, "fire": 0.5, "clown": -0.7,
    }

    def __init__(
        self,
        platforms: Optional[List[str]] = None,
        languages: Optional[List[str]] = None,
        sport_lexicon: str = "football_v3",
    ):
        self.platforms = platforms or ["twitter"]
        self.languages = languages or ["en"]
        self.sport_lexicon = sport_lexicon

    def _simple_sentiment(self, text: str) -> float:
        score = 0.0
        words = text.lower().split()
        matched = 0
        for word in words:
            if word in self.SPORT_LEXICON:
                score += self.SPORT_LEXICON[word]
                matched += 1
        if matched == 0:
            return 0.0
        return max(-1.0, min(1.0, score / matched))

    def track_live(
        self,
        match_id: str,
        keywords: Optional[List[str]] = None,
        time_window: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        events = []
        for i in range(10):
            score = random.uniform(-0.8, 0.8)
            events.append(SentimentEvent(
                timestamp=f"2024-01-01T{14 + i // 2}:{(i % 2) * 30:02d}:00Z",
                trigger=random.choice(["goal", "foul", "substitution", "var_review", "chance"]),
                sentiment_score=round(score, 2),
                positive_pct=round(max(0, (1 + score) / 2 * 100), 1),
                negative_pct=round(max(0, (1 - score) / 2 * 100), 1),
                mention_count=random.randint(500, 50000),
                top_phrase=random.choice(["great goal", "terrible ref", "what a save", " VAR out"]),
                viral_score=round(random.uniform(0, 100), 0),
            ))
        return {"events": events, "match_id": match_id}

    def match_summary(self, match_id: str) -> SentimentSummary:
        return SentimentSummary(
            avg_sentiment=round(random.uniform(-0.3, 0.5), 2),
            peak_positive_moment="Goal at 67'",
            peak_negative_moment="Red card at 42'",
            brand_impact_score=round(random.uniform(-2, 5), 1),
            total_mentions=random.randint(50000, 500000),
            sentiment_trend=random.choice(["improving", "stable", "declining"]),
        )


# ---------------------------------------------------------------------------
# Ticket Pricing Engine
# ---------------------------------------------------------------------------

class TicketPricingEngine:
    """Demand-responsive dynamic ticket pricing."""

    def __init__(
        self,
        venue_name: str = "Stadium",
        capacity: int = 60000,
        pricing_model: str = "demand_response_v3",
        min_margin: float = 0.15,
        max_price_multiplier: float = 5.0,
    ):
        self.venue_name = venue_name
        self.capacity = capacity
        self.pricing_model = pricing_model
        self.min_margin = min_margin
        self.max_price_multiplier = max_price_multiplier

    def calculate_prices(
        self,
        match_id: str,
        opponent: str,
        days_until_match: int,
        current_inventory: int,
        historical_demand_curve: Optional[Dict[str, float]] = None,
    ) -> List[TicketZone]:
        zones = [
            ("Premium Lower", 150.0, 0.20),
            ("Premium Upper", 120.0, 0.25),
            ("Standard Lower", 80.0, 0.30),
            ("Standard Upper", 55.0, 0.25),
            ("General Admission", 35.0, 0.35),
        ]

        urgency_factor = max(1.0, (30 - days_until_match) / 15)
        opponent_factor = 1.3 if opponent in ["rival_team", "top_6"] else 1.0
        inventory_factor = max(1.0, (self.capacity - current_inventory) / self.capacity * 2)

        result = []
        for name, base_price, inventory_share in zones:
            zone_capacity = int(self.capacity * inventory_share)
            multiplier = min(
                self.max_price_multiplier,
                urgency_factor * opponent_factor * inventory_factor
            )
            optimal = round(base_price * multiplier, 2)
            sell_through = min(1.0, inventory_factor * 0.8)

            result.append(TicketZone(
                name=name,
                base_price=base_price,
                optimal_price=optimal,
                multiplier=round(multiplier, 2),
                projected_sell_through=round(sell_through, 2),
                inventory=zone_capacity,
            ))
        return result

    def price_elasticity_analysis(
        self, match_id: str, zone: str, price_range: Tuple[float, float]
    ) -> PriceElasticity:
        low, high = price_range
        mid = (low + high) / 2
        elasticity = round(random.uniform(-1.5, -0.5), 2)
        optimal = round(mid * (1 + elasticity * 0.1), 2)
        return PriceElasticity(
            zone=zone,
            coefficient=elasticity,
            optimal_price=optimal,
            revenue_at_optimal=round(optimal * random.randint(500, 2000), 2),
        )


# ---------------------------------------------------------------------------
# Second Screen Experience
# ---------------------------------------------------------------------------

class SecondScreen:
    """Live second-screen experience with interactive elements."""

    def __init__(
        self,
        match_id: str,
        broadcast_sync: bool = True,
        latency_target_ms: int = 500,
    ):
        self.match_id = match_id
        self.broadcast_sync = broadcast_sync
        self.latency_target_ms = latency_target_ms
        self._elements: List[InteractiveElement] = []
        self._update_queue: List[UpdateEvent] = []

    def register_element(self, element: InteractiveElement) -> None:
        self._elements.append(element)

    def updates(self) -> List[UpdateEvent]:
        events = [
            UpdateEvent(type="goal", data={
                "scorer": "Player A",
                "minute": 67,
                "xg_after": 0.82,
            }),
            UpdateEvent(type="poll_result", data={
                "question": "Man of the Match so far?",
                "winner": "Player B",
                "total_votes": 15420,
            }),
            UpdateEvent(type="stat_update", data={
                "possession": {"home": 58, "away": 42},
                "shots": {"home": 12, "away": 7},
            }),
        ]
        self._update_queue.extend(events)
        return events


# ---------------------------------------------------------------------------
# Gamification Engine
# ---------------------------------------------------------------------------

class GamificationEngine:
    """Achievement, streak, and reward system for fan engagement."""

    ACHIEVEMENT_DEFINITIONS = {
        "first_prediction": {"name": "First Guess", "description": "Make your first prediction", "points": 10},
        "prediction_streak_5": {"name": "Hot Streak", "description": "5 correct predictions in a row", "points": 100},
        "prediction_streak_10": {"name": "On Fire", "description": "10 correct predictions in a row", "points": 500},
        "match_watcher_10": {"name": "Dedicated Fan", "description": "Watch 10 matches live", "points": 200},
        "social_share_5": {"name": "Amplifier", "description": "Share 5 match moments", "points": 50},
    }

    def __init__(self, user_id: str):
        self.user_id = user_id
        self._achievements: List[str] = []
        self._streak: int = 0
        self._total_points: int = 0
        self._predictions_correct: int = 0
        self._predictions_total: int = 0

    def record_prediction(self, correct: bool) -> Dict[str, Any]:
        self._predictions_total += 1
        result = {"correct": correct, "new_achievements": []}

        if correct:
            self._predictions_correct += 1
            self._streak += 1
            self._total_points += 10
            result["points_earned"] = 10

            if self._streak == 5 and "prediction_streak_5" not in self._achievements:
                self._achievements.append("prediction_streak_5")
                self._total_points += 100
                result["new_achievements"].append("prediction_streak_5")
            elif self._streak == 10 and "prediction_streak_10" not in self._achievements:
                self._achievements.append("prediction_streak_10")
                self._total_points += 500
                result["new_achievements"].append("prediction_streak_10")
        else:
            self._streak = 0
            result["points_earned"] = 0

        result["streak"] = self._streak
        result["total_points"] = self._total_points
        result["accuracy"] = round(
            self._predictions_correct / max(self._predictions_total, 1) * 100, 1
        )
        return result

    def get_leaderboard_position(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "total_points": self._total_points,
            "achievements_count": len(self._achievements),
            "accuracy": round(self._predictions_correct / max(self._predictions_total, 1) * 100, 1),
            "current_streak": self._streak,
        }


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("Fan Engagement — Demo")
    print("=" * 70)

    # 1. Fantasy Engine
    print("\n--- Fantasy Projection & Lineup Optimization ---")
    engine = FantasyEngine(platform=Platform.DRAFTKINGS)
    projections = engine.project_players(sport="nfl", week=14)
    print("Top 5 projected players:")
    projections.sort(key=lambda p: p.projected_points, reverse=True)
    for p in projections[:5]:
        print(f"  {p.name:25s} | {p.position.value:3s} | "
              f"Proj: {p.projected_points:5.1f} | Salary: ${p.salary:,} | "
              f"Value: {p.points_per_dollar:.3f} | Ownership: {p.projected_ownership:.0%}")

    lineup = engine.optimize_lineup(budget=50000)
    print(f"\nOptimized Lineup (Expected: {lineup.expected_points:.1f} pts):")
    print(lineup.roster_display())

    # 2. Trade Values
    print("\n--- Trade Value Calculator ---")
    tvc = TradeValueCalculator(season=2024)
    trade_data = [
        {"id": "p1", "name": "Player A", "age": 24, "rest_of_season_projection": 150,
         "injury_history_count": 0, "remaining_schedule_difficulty": 0.2},
        {"id": "p2", "name": "Player B", "age": 30, "rest_of_season_projection": 120,
         "injury_history_count": 2, "remaining_schedule_difficulty": -0.1},
    ]
    values = tvc.compute_values(trade_data)
    for v in values:
        print(f"  {v.name:15s} | Value: {v.total_value:6.1f} | "
              f"Age adj: {v.age_adjustment:.3f} | Injury risk: {v.injury_risk_factor:.3f} | "
              f"Trend: {v.trend}")

    # 3. Sentiment Analysis
    print("\n--- Fan Sentiment Analysis ---")
    sa = SentimentAnalyzer(platforms=["twitter", "reddit"])
    result = sa.track_live(match_id="match_final", keywords=["#Final"])
    for evt in result["events"][:3]:
        print(f"  [{evt.timestamp}] {evt.trigger:15s} | Sentiment: {evt.sentiment_score:+.2f} | "
              f"Volume: {evt.mention_count:,} | Viral: {evt.viral_score:.0f}")

    summary = sa.match_summary("match_final")
    print(f"\n  Avg sentiment: {summary.avg_sentiment:+.2f}")
    print(f"  Trend: {summary.sentiment_trend}")
    print(f"  Total mentions: {summary.total_mentions:,}")

    # 4. Dynamic Ticket Pricing
    print("\n--- Dynamic Ticket Pricing ---")
    tpe = TicketPricingEngine(venue_name="Stadium A", capacity=60000)
    pricing = tpe.calculate_prices(
        match_id="match_final",
        opponent="rival_team",
        days_until_match=7,
        current_inventory=45000,
    )
    for zone in pricing:
        print(f"  {zone.name:20s} | Base: ${zone.base_price:6.0f} | "
              f"Optimal: ${zone.optimal_price:6.0f} | {zone.multiplier:.1f}x | "
              f"Sell-through: {zone.projected_sell_through:.0%}")

    elasticity = tpe.price_elasticity_analysis("match_final", "Premium Lower", (80, 200))
    print(f"\n  Price elasticity: {elasticity.coefficient:.2f}")
    print(f"  Revenue-maximizing price: ${elasticity.optimal_price:.0f}")

    # 5. Gamification
    print("\n--- Gamification Engine ---")
    gamification = GamificationEngine(user_id="fan_001")
    for correct in [True, True, True, True, True, True, False, True, True, True, True]:
        result = gamification.record_prediction(correct)
        if result.get("new_achievements"):
            print(f"  NEW ACHIEVEMENT: {result['new_achievements']}")
    print(f"  Final stats: {gamification.get_leaderboard_position()}")

    print("\n" + "=" * 70)
    print("Demo complete.")


if __name__ == "__main__":
    main()
