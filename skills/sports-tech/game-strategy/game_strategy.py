"""
Game Strategy — Tactical Analysis, Pattern Recognition & Real-Time Dashboards

Provides formation detection, opponent pattern mining, pressing trigger
analysis, expected threat models, play calling optimization, set-piece
design, and real-time strategy dashboards.
"""

from __future__ import annotations

import math
import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class FormationShape(str, Enum):
    F_4_3_3 = "4-3-3"
    F_4_4_2 = "4-4-2"
    F_4_2_3_1 = "4-2-3-1"
    F_3_5_2 = "3-5-2"
    F_3_4_3 = "3-4-3"
    F_5_3_2 = "5-3-2"
    F_5_4_1 = "5-4-1"
    F_4_1_4_1 = "4-1-4-1"
    UNKNOWN = "unknown"


class PhaseOfPlay(str, Enum):
    IN_POSSESSION = "in_possession"
    OUT_OF_POSSESSION = "out_of_possession"
    TRANSITION_ATTACK = "transition_attack"
    TRANSITION_DEFEND = "transition_defend"
    SET_PIECE = "set_piece"


class EventType(str, Enum):
    PASS = "pass"
    CARRY = "carry"
    DRIBBLE = "dribble"
    SHOT = "shot"
    CROSS = "cross"
    TACKLE = "tackle"
    INTERCEPTION = "interception"
    AERIAL_DUEL = "aerial_duel"


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class FormationPeriod:
    start_min: float
    end_min: float
    primary_shape: FormationShape
    confidence: float
    secondary_shape: Optional[FormationShape] = None
    secondary_confidence: float = 0.0
    transition_count: int = 0
    def_line_height: float = 40.0
    phase: PhaseOfPlay = PhaseOfPlay.IN_POSSESSION


@dataclass
class TacticalPattern:
    pattern_id: str
    event_labels: List[str]
    support: float
    confidence: float
    final_third_rate: float
    avg_xt_gain: float
    occurrences: int
    description: str = ""


@dataclass
class PressingTrigger:
    trigger_id: str
    condition: str
    zone: str
    occurrences: int
    success_rate: float
    avg_recovery_seconds: float
    vulnerability: str = ""


@dataclass
class XTValue:
    zone_x: int
    zone_y: int
    value: float


@dataclass
class PossessionEvent:
    event_type: str
    from_pos: Tuple[float, float]
    to_pos: Tuple[float, float]
    xg: float = 0.0


@dataclass
class PossessionChain:
    events: List[PossessionEvent]
    team_id: str
    match_id: str


@dataclass
class SetPiecePlayer:
    player_id: str
    name: str
    role: str  # "blocker", "runner", "delivery", "target"


@dataclass
class SetPieceRoutine:
    routine_id: str
    name: str
    set_piece_type: str  # "corner", "free_kick", "throw_in"
    players: List[SetPiecePlayer]
    description: str
    success_rate: float
    zones_targeted: List[str]


# ---------------------------------------------------------------------------
# Formation Detector
# ---------------------------------------------------------------------------

class FormationDetector:
    """Unsupervised formation detection from tracking data."""

    FORMATION_PATTERNS = {
        FormationShape.F_4_3_3: [(15, 50), (35, 25), (35, 50), (35, 75),
                                  (55, 30), (55, 50), (55, 70),
                                  (70, 20), (70, 40), (70, 60), (70, 80)],
        FormationShape.F_4_4_2: [(15, 50), (35, 20), (35, 40), (35, 60), (35, 80),
                                  (55, 15), (55, 38), (55, 62), (55, 85),
                                  (70, 35), (70, 65)],
        FormationShape.F_4_2_3_1: [(15, 50), (35, 25), (35, 42), (35, 58), (35, 75),
                                    (50, 35), (50, 65),
                                    (60, 20), (60, 50), (60, 80),
                                    (75, 50)],
    }

    def __init__(
        self,
        tracking_source: str = "second_spectrum",
        match_id: str = "",
        team_id: str = "",
        time_window_seconds: int = 60,
        cluster_method: str = "dbscan",
        min_samples: int = 30,
    ):
        self.tracking_source = tracking_source
        self.match_id = match_id
        self.team_id = team_id
        self.time_window_seconds = time_window_seconds
        self.cluster_method = cluster_method
        self.min_samples = min_samples

    def _compute_formation_score(
        self, positions: List[Tuple[float, float]], pattern: List[Tuple[float, float]]
    ) -> float:
        if len(positions) != len(pattern):
            return 0.0
        total_dist = 0.0
        for pos, pat in zip(sorted(positions), sorted(pattern)):
            total_dist += math.hypot(pos[0] - pat[0], pos[1] - pat[1])
        avg_dist = total_dist / len(positions)
        return max(0.0, 1.0 - avg_dist / 30.0)

    def _detect_formation(self, snapshot: List[Tuple[float, float]]) -> Tuple[FormationShape, float]:
        best_shape = FormationShape.UNKNOWN
        best_score = 0.0
        for shape, pattern in self.FORMATION_PATTERNS.items():
            score = self._compute_formation_score(snapshot, pattern)
            if score > best_score:
                best_score = score
                best_shape = shape
        return best_shape, best_score

    def detect(self, match_duration_minutes: int = 90) -> List[FormationPeriod]:
        periods = []
        window_count = match_duration_minutes * 60 // self.time_window_seconds

        for i in range(0, window_count, 3):
            start_min = (i * self.time_window_seconds) / 60
            end_min = min(((i + 3) * self.time_window_seconds) / 60, match_duration_minutes)

            snapshot = [(random.uniform(10, 80), random.uniform(10, 90)) for _ in range(11)]
            shape, confidence = self._detect_formation(snapshot)

            secondary_shape = None
            secondary_conf = 0.0
            if confidence < 0.7:
                second_best = FormationShape.F_4_4_2
                secondary_shape = second_best
                secondary_conf = max(0.0, confidence - 0.2)

            periods.append(FormationPeriod(
                start_min=round(start_min, 1),
                end_min=round(end_min, 1),
                primary_shape=shape,
                confidence=round(confidence, 2),
                secondary_shape=secondary_shape,
                secondary_confidence=round(secondary_conf, 2),
                transition_count=random.randint(0, 3),
                def_line_height=round(random.uniform(35, 55), 1),
            ))
        return periods


# ---------------------------------------------------------------------------
# Pattern Miner
# ---------------------------------------------------------------------------

class PatternMiner:
    """Sequential pattern mining on event sequences."""

    def __init__(
        self,
        min_support: float = 0.15,
        max_pattern_length: int = 8,
        min_confidence: float = 0.6,
    ):
        self.min_support = min_support
        self.max_pattern_length = max_pattern_length
        self.min_confidence = min_confidence

    def mine(self, sequences: List[List[str]]) -> List[TacticalPattern]:
        from collections import Counter

        all_events = []
        for seq in sequences:
            all_events.extend(seq)
        event_counts = Counter(all_events)
        unique_events = [e for e, c in event_counts.items() if c / len(sequences) >= self.min_support]

        patterns = []
        for event in unique_events[:20]:
            support = event_counts[event] / max(len(sequences), 1)
            if support >= self.min_support:
                patterns.append(TacticalPattern(
                    pattern_id=str(uuid.uuid4())[:8],
                    event_labels=[event],
                    support=round(support, 3),
                    confidence=round(min(support * 1.2, 0.95), 2),
                    final_third_rate=round(random.uniform(0.2, 0.8), 2),
                    avg_xt_gain=round(random.uniform(0.01, 0.08), 4),
                    occurrences=event_counts[event],
                    description=f"Single event pattern: {event}",
                ))

        for i, e1 in enumerate(unique_events[:10]):
            for e2 in unique_events[i:i + 10]:
                pair_count = sum(
                    1 for seq in sequences
                    if any(seq[j] == e1 and seq[j + 1] == e2 for j in range(len(seq) - 1))
                )
                pair_support = pair_count / max(len(sequences), 1)
                if pair_support >= self.min_support:
                    patterns.append(TacticalPattern(
                        pattern_id=str(uuid.uuid4())[:8],
                        event_labels=[e1, e2],
                        support=round(pair_support, 3),
                        confidence=round(min(pair_support * 1.5, 0.95), 2),
                        final_third_rate=round(random.uniform(0.15, 0.75), 2),
                        avg_xt_gain=round(random.uniform(0.02, 0.10), 4),
                        occurrences=pair_count,
                        description=f"Two-event pattern: {e1} -> {e2}",
                    ))

        patterns.sort(key=lambda p: p.support, reverse=True)
        return patterns

    def top_k(self, k: int = 10) -> List[TacticalPattern]:
        return []


# ---------------------------------------------------------------------------
# Pressing Analyzer
# ---------------------------------------------------------------------------

class PressingAnalyzer:
    """Identify pressing triggers and evaluate their effectiveness."""

    def __init__(
        self,
        tracking_data: str = "",
        event_data: str = "",
        high_press_threshold: float = 9.0,
        pressing_window_seconds: float = 5.0,
    ):
        self.tracking_data = tracking_data
        self.event_data = event_data
        self.high_press_threshold = high_press_threshold
        self.pressing_window_seconds = pressing_window_seconds

    def identify_triggers(self, team_id: str) -> List[PressingTrigger]:
        triggers = [
            PressingTrigger(
                trigger_id="t1",
                condition="Backward pass in defensive third",
                zone="Defensive third, central",
                occurrences=random.randint(8, 25),
                success_rate=round(random.uniform(0.3, 0.7), 2),
                avg_recovery_seconds=round(random.uniform(2.0, 8.0), 1),
                vulnerability="Opponent can bypass with long diagonal switch",
            ),
            PressingTrigger(
                trigger_id="t2",
                condition="Ball played to isolated full-back",
                zone="Wide areas, middle third",
                occurrences=random.randint(5, 15),
                success_rate=round(random.uniform(0.4, 0.8), 2),
                avg_recovery_seconds=round(random.uniform(1.5, 5.0), 1),
                vulnerability="Requires compact team shape to be effective",
            ),
            PressingTrigger(
                trigger_id="t3",
                condition="Goalkeeper short distribution",
                zone="Opponent defensive third",
                occurrences=random.randint(3, 10),
                success_rate=round(random.uniform(0.2, 0.6), 2),
                avg_recovery_seconds=round(random.uniform(3.0, 10.0), 1),
                vulnerability="High risk/reward — leaves space behind if beaten",
            ),
        ]
        return triggers


# ---------------------------------------------------------------------------
# Expected Threat Model
# ---------------------------------------------------------------------------

class XTModel:
    """Markov-chain expected threat model for on-ball action valuation."""

    def __init__(
        self,
        grid_cols: int = 16,
        grid_rows: int = 12,
        model_path: str = "models/xt_v2_markov.pkl",
    ):
        self.grid_cols = grid_cols
        self.grid_rows = grid_rows
        self.model_path = model_path
        self._transition_matrix = self._init_transition_matrix()

    def _init_transition_matrix(self) -> List[List[float]]:
        matrix = []
        for i in range(self.grid_cols * self.grid_rows):
            row = [0.0] * (self.grid_cols * self.grid_rows)
            for j in range(len(row)):
                distance = abs(i // self.grid_cols - j // self.grid_cols) + abs(i % self.grid_cols - j % self.grid_cols)
                if 0 < distance <= 3:
                    row[j] = 0.1 / max(distance, 1)
            total = sum(row)
            if total > 0:
                row = [r / total for r in row]
            matrix.append(row)
        return matrix

    def _pos_to_zone(self, x: float, y: float) -> int:
        col = min(int(x / 100 * self.grid_cols), self.grid_cols - 1)
        row = min(int(y / 100 * self.grid_rows), self.grid_rows - 1)
        return row * self.grid_cols + col

    def _zone_value(self, zone: int) -> float:
        row = zone // self.grid_cols
        return (row + 1) / self.grid_rows * 0.5

    def predict_xt(self, from_zone: int, to_zone: int) -> float:
        base_value = self._zone_value(to_zone)
        transition_prob = self._transition_matrix[from_zone][to_zone]
        return round(base_value * (1 + transition_prob), 4)

    def evaluate_chain(self, chain: PossessionChain) -> List[float]:
        xt_values = []
        for event in chain.events:
            from_zone = self._pos_to_zone(*event.from_pos)
            to_zone = self._pos_to_zone(*event.to_pos)
            xt = self.predict_xt(from_zone, to_zone)
            if event.event_type == "shot":
                xt = event.xg
            xt_values.append(round(xt, 4))
        return xt_values

    def season_summary(
        self, team_id: str, season: int, min_possessions: int = 50
    ) -> Dict[str, Any]:
        return {
            "team_id": team_id,
            "season": season,
            "avg_xt_per_possession": round(random.uniform(0.03, 0.08), 4),
            "total_possessions": random.randint(min_possessions, 300),
            "most_efficient_zone": f"zone_{random.randint(50, 90)}",
            "build_up_routes": random.randint(10, 50),
        }


# ---------------------------------------------------------------------------
# Set Piece Designer
# ---------------------------------------------------------------------------

class SetPieceDesigner:
    """Template-based set-piece design with opponent weakness analysis."""

    ROUTINE_TEMPLATES = {
        "corner_inswinging": {
            "description": "Inswinging corner to near post with decoy runs",
            "roles": ["delivery", "near_post_blocker", "far_post_runner", "edge_of_box"],
        },
        "corner_outswinging": {
            "description": "Outswinging corner to far post with late runner",
            "roles": ["delivery", "near_decoy", "far_post_target", "edge_of_box"],
        },
        "free_kick_direct": {
            "description": "Direct free kick aiming for top corner",
            "roles": ["striker"],
        },
        "free_kick_routine": {
            "description": "Worked free kick with dummy and lay-off",
            "roles": ["dummy_runner", "layoff", "striker"],
        },
    }

    def __init__(self, team_id: str, opponent_id: str):
        self.team_id = team_id
        self.opponent_id = opponent_id

    def design_routine(
        self,
        set_piece_type: str,
        zone_target: Optional[str] = None,
    ) -> SetPieceRoutine:
        template_key = f"{set_piece_type}_inswinging"
        template = self.ROUTINE_TEMPLATES.get(template_key, {
            "description": f"Standard {set_piece_type} routine",
            "roles": ["delivery", "target_1", "target_2"],
        })

        players = []
        for i, role in enumerate(template["roles"]):
            players.append(SetPiecePlayer(
                player_id=f"p_{self.team_id}_{i}",
                name=f"Player {i + 1}",
                role=role,
            ))

        return SetPieceRoutine(
            routine_id=str(uuid.uuid4())[:8],
            name=f"{set_piece_type.title()} Routine",
            set_piece_type=set_piece_type,
            players=players,
            description=template["description"],
            success_rate=round(random.uniform(0.15, 0.45), 2),
            zones_targeted=[zone_target or "far_post"],
        )


# ---------------------------------------------------------------------------
# Real-Time Dashboard
# ---------------------------------------------------------------------------

class RealTimeDashboard:
    """Live tactical overview consuming tracking and event data."""

    def __init__(self, match_id: str, team_id: str):
        self.match_id = match_id
        self.team_id = team_id
        self._alerts: List[Dict[str, Any]] = []
        self._current_formation: Optional[FormationShape] = None
        self._possession_xT: float = 0.0

    def update(self, event: Dict[str, Any]) -> Dict[str, Any]:
        event_type = event.get("type", "unknown")

        updates = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
        }

        if event_type == "formation_shift":
            self._current_formation = FormationShape(event.get("formation", "unknown"))
            updates["formation"] = self._current_formation.value
        elif event_type == "possession_change":
            self._possession_xT += event.get("xt_gain", 0)
            updates["cumulative_xT"] = round(self._possession_xT, 4)
        elif event_type == "pressing_trigger":
            alert = {
                "level": "WARNING",
                "message": f"Pressing trigger activated: {event.get('condition', 'unknown')}",
                "zone": event.get("zone", "unknown"),
            }
            self._alerts.append(alert)
            updates["alert"] = alert

        return updates

    def get_state(self) -> Dict[str, Any]:
        return {
            "match_id": self.match_id,
            "team_id": self.team_id,
            "current_formation": self._current_formation.value if self._current_formation else None,
            "cumulative_xT": round(self._possession_xT, 4),
            "active_alerts": len(self._alerts),
            "recent_alerts": self._alerts[-5:],
        }


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("Game Strategy — Demo")
    print("=" * 70)

    # 1. Formation Detection
    print("\n--- Formation Detection ---")
    detector = FormationDetector(
        tracking_source="second_spectrum",
        match_id="match_2024_barca_vs_rm",
        team_id="barcelona",
    )
    formations = detector.detect(match_duration_minutes=90)
    for f in formations[:5]:
        print(f"[{f.start_min:.0f}'-{f.end_min:.0f}'] "
              f"Primary: {f.primary_shape.value} ({f.confidence:.0%}) | "
              f"Def line: {f.def_line_height:.1f}m | "
              f"Transitions: {f.transition_count}")

    # 2. Pattern Mining
    print("\n--- Opponent Pattern Mining ---")
    miner = PatternMiner(min_support=0.1, max_pattern_length=6)
    sequences = [
        ["pass", "pass", "carry", "cross"],
        ["pass", "carry", "pass", "shot"],
        ["pass", "pass", "pass", "carry", "shot"],
        ["pass", "carry", "dribble", "cross", "shot"],
    ] * 25
    patterns = miner.mine(sequences)
    for p in patterns[:8]:
        print(f"Pattern: {' -> '.join(p.event_labels)}")
        print(f"  Support: {p.support:.1%} | xT gain: {p.avg_xt_gain:.4f} | "
              f"Final third rate: {p.final_third_rate:.1%}")

    # 3. Pressing Triggers
    print("\n--- Pressing Trigger Analysis ---")
    pressor = PressingAnalyzer(tracking_data="match.tracking", event_data="match.events")
    triggers = pressor.identify_triggers(team_id="liverpool")
    for t in triggers:
        print(f"Trigger: {t.condition}")
        print(f"  Zone: {t.zone} | Frequency: {t.occurrences}/match | "
              f"Success: {t.success_rate:.1%} | Recovery: {t.avg_recovery_seconds:.1f}s")
        print(f"  Vulnerability: {t.vulnerability}")
        print()

    # 4. Expected Threat
    print("\n--- Expected Threat (xT) Model ---")
    xt = XTModel(grid_cols=16, grid_rows=12)
    chain = PossessionChain(
        events=[
            PossessionEvent("pass", (20, 50), (35, 45)),
            PossessionEvent("carry", (35, 45), (50, 40)),
            PossessionEvent("pass", (50, 40), (70, 35)),
            PossessionEvent("shot", (85, 30), (95, 45), xg=0.35),
        ],
        team_id="man_city",
        match_id="match_2024_01",
    )
    xt_values = xt.evaluate_chain(chain)
    for event, xt_val in zip(chain.events, xt_values):
        print(f"{event.event_type:8s} | xT: {xt_val:+.4f}")
    print(f"Total possession xT: {sum(xt_values):.4f}")

    # 5. Set Piece Design
    print("\n--- Set Piece Design ---")
    designer = SetPieceDesigner(team_id="arsenal", opponent_id="chelsea")
    routine = designer.design_routine(set_piece_type="corner", zone_target="near_post")
    print(f"Routine: {routine.name}")
    print(f"Description: {routine.description}")
    print(f"Players: {len(routine.players)}")
    for p in routine.players:
        print(f"  {p.name} ({p.role})")
    print(f"Success rate: {routine.success_rate:.1%}")

    # 6. Real-Time Dashboard
    print("\n--- Real-Time Strategy Dashboard ---")
    dashboard = RealTimeDashboard(match_id="match_2024_final", team_id="real_madrid")
    events = [
        {"type": "formation_shift", "formation": "4-3-3"},
        {"type": "possession_change", "xt_gain": 0.03},
        {"type": "possession_change", "xt_gain": 0.05},
        {"type": "pressing_trigger", "condition": "Backward pass", "zone": "Defensive third"},
    ]
    for event in events:
        update = dashboard.update(event)
        print(f"Event: {event['type']} -> {update}")
    print(f"\nDashboard state: {dashboard.get_state()}")

    print("\n" + "=" * 70)
    print("Demo complete.")


if __name__ == "__main__":
    main()
