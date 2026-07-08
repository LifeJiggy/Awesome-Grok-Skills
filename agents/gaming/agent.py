"""
Gaming Agent — Game development, game mechanics design, player engagement,
monetization strategies, analytics, and QA testing.

This module provides comprehensive game development tools including:
- Game design document (GDD) structure and management
- Game mechanics simulation and balancing
- Player progression and economy systems
- Monetization model analysis (IAP, ads, subscriptions)
- Player engagement analytics and retention modeling
- Loot box and gacha probability systems
- Game balancing (damage, stats, difficulty curves)
- QA test case generation and bug tracking
- Level design and procedural generation helpers
- Performance profiling and optimization metrics
"""

from __future__ import annotations

import logging
import math
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    NamedTuple,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class GameGenre(Enum):
    RPG = "rpg"
    FPS = "fps"
    STRATEGY = "strategy"
    PUZZLE = "puzzle"
    PLATFORMER = "platformer"
    SIMULATION = "simulation"
    MOBA = "moba"
    BATTLE_ROYALE = "battle_royale"
    CARD_GAME = "card_game"
    IDLE = "idle"
    SOCIAL = "social"
    SANDBOX = "sandbox"
    ROGUELIKE = "roguelike"


class PlayerStatus(Enum):
    NEW = "new"
    CASUAL = "casual"
    REGULAR = "regular"
    DEDICATED = "dedicated"
    WHALE = "whale"
    CHURNED = "churned"
    RETURNED = "returned"


class MonetizationModel(Enum):
    FREE_TO_PLAY = "free_to_play"
    PREMIUM = "premium"
    SUBSCRIPTION = "subscription"
    AD_SUPPORTED = "ad_supported"
    HYBRID = "hybrid"
    BATTLE_PASS = "battle_pass"


class CurrencyType(Enum):
    PREMIUM = "premium"        # Real money currency
    SOFT = "soft"              # Earned in-game
    EVENT = "event"            # Limited-time
    SOCIAL = "social"          # From social features
    SEASONAL = "seasonal"      # Season-specific


class LootRarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MYTHIC = "mythic"


class QuestType(Enum):
    MAIN = "main"
    SIDE = "side"
    DAILY = "daily"
    WEEKLY = "weekly"
    EVENT = "event"
    ACHIEVEMENT = "achievement"
    TUTORIAL = "tutorial"
    BOUNTY = "bounty"


class DifficultyLevel(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    NIGHTMARE = "nightmare"
    CUSTOM = "custom"


class BugSeverity(IntEnum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    COSMETIC = 4


class BugStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    FIX_PENDING = "fix_pending"
    VERIFIED = "verified"
    CLOSED = "closed"
    WONT_FIX = "wont_fix"
    DUPLICATE = "duplicate"


class MetricType(Enum):
    DAU = "dau"
    MAU = "mau"
    RETENTION = "retention"
    SESSION_LENGTH = "session_length"
    ARPDAU = "arpdau"
    LTV = "ltv"
    CONVERSION = "conversion"
    CHURN = "churn"
    ENGAGEMENT_SCORE = "engagement_score"


class StatType(Enum):
    DAMAGE = "damage"
    HEALTH = "health"
    SPEED = "speed"
    DEFENSE = "defense"
    CRIT_CHANCE = "crit_chance"
    CRIT_DAMAGE = "crit_damage"
    DODGE = "dodge"
    BLOCK = "block"
    HEAL = "heal"
    MANA = "mana"
    STAMINA = "stamina"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class GameConfig:
    """Top-level game configuration."""
    title: str
    genre: GameGenre
    platform: List[str] = field(default_factory=lambda: ["PC"])
    monetization: MonetizationModel = MonetizationModel.FREE_TO_PLAY
    target_audience: str = "13+"
    engine: str = "custom"
    max_players: int = 1
    version: str = "1.0.0"
    release_date: Optional[datetime] = None

    @property
    def is_multiplayer(self) -> bool:
        return self.max_players > 1


@dataclass
class CharacterStats:
    """Base character statistics."""
    level: int = 1
    health: float = 100.0
    max_health: float = 100.0
    mana: float = 50.0
    max_mana: float = 50.0
    attack: float = 10.0
    defense: float = 5.0
    speed: float = 1.0
    crit_chance: float = 0.05
    crit_damage: float = 1.5
    dodge: float = 0.03
    block: float = 0.0

    @property
    def effective_hp(self) -> float:
        return self.max_health * (1 + self.defense / 100)

    def scale_with_level(self, growth_rates: Dict[str, float]) -> None:
        for stat, rate in growth_rates.items():
            current = getattr(self, stat, 0)
            setattr(self, stat, current * (1 + rate) ** (self.level - 1))
        self.max_health = self.health
        self.max_mana = self.mana


@dataclass
class Item:
    """In-game item representation."""
    item_id: str
    name: str
    rarity: LootRarity
    item_type: str
    stats: Dict[str, float] = field(default_factory=dict)
    price_soft: int = 0
    price_premium: int = 0
    level_required: int = 1
    stackable: bool = False
    max_stack: int = 1
    description: str = ""
    drop_rate: float = 0.0

    @property
    def power_score(self) -> float:
        return sum(self.stats.values())

    @property
    def is_purchasable(self) -> bool:
        return self.price_soft > 0 or self.price_premium > 0


@dataclass
class Quest:
    """Quest or mission definition."""
    quest_id: str
    name: str
    quest_type: QuestType
    description: str
    objectives: List[Dict[str, Any]] = field(default_factory=list)
    rewards: Dict[str, Any] = field(default_factory=dict)
    level_required: int = 1
    time_limit_hours: Optional[int] = None
    repeatable: bool = False
    prerequisites: List[str] = field(default_factory=list)
    difficulty: DifficultyLevel = DifficultyLevel.NORMAL
    exp_reward: int = 0
    gold_reward: int = 0
    item_rewards: List[str] = field(default_factory=list)

    @property
    def total_objectives(self) -> int:
        return len(self.objectives)

    def is_available(self, player_level: int, completed_quests: Set[str]) -> bool:
        if player_level < self.level_required:
            return False
        return all(p in completed_quests for p in self.prerequisites)


@dataclass
class PlayerProfile:
    """Player account and progression data."""
    player_id: str
    name: str
    level: int = 1
    exp: int = 0
    status: PlayerStatus = PlayerStatus.NEW
    join_date: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)
    currencies: Dict[str, int] = field(default_factory=dict)
    inventory: List[str] = field(default_factory=list)
    completed_quests: Set[str] = field(default_factory=set)
    playtime_hours: float = 0.0
    total_spent: float = 0.0
    session_count: int = 0
    friends: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    chapter_progress: int = 0

    @property
    def days_since_join(self) -> int:
        return (datetime.utcnow() - self.join_date).days

    @property
    def days_since_active(self) -> int:
        return (datetime.utcnow() - self.last_active).days

    @property
    def is_active(self) -> bool:
        return self.days_since_active <= 7

    @property
    def avg_session_length_hours(self) -> float:
        if self.session_count == 0:
            return 0.0
        return self.playtime_hours / self.session_count

    @property
    def lifetime_value(self) -> float:
        return self.total_spent

    @property
    def daily_value(self) -> float:
        days = max(self.days_since_join, 1)
        return self.total_spent / days

    def add_currency(self, currency_type: str, amount: int) -> None:
        self.currencies[currency_type] = self.currencies.get(currency_type, 0) + amount

    def spend_currency(self, currency_type: str, amount: int) -> bool:
        current = self.currencies.get(currency_type, 0)
        if current < amount:
            return False
        self.currencies[currency_type] = current - amount
        return True

    def add_exp(self, amount: int, exp_per_level: Callable[[int], int]) -> int:
        levels_gained = 0
        self.exp += amount
        while self.exp >= exp_per_level(self.level):
            self.exp -= exp_per_level(self.level)
            self.level += 1
            levels_gained += 1
        return levels_gained


@dataclass
class LootTable:
    """Defines drop rates for a loot source."""
    source_id: str
    source_name: str
    entries: List[Dict[str, Any]] = field(default_factory=list)
    pity_counter: int = 0
    pity_threshold: int = 50

    @property
    def total_rate(self) -> float:
        return sum(e.get("rate", 0) for e in self.entries)

    def roll(self, luck_modifier: float = 1.0) -> Optional[Dict[str, Any]]:
        self.pity_counter += 1
        if self.pity_counter >= self.pity_threshold:
            self.pity_counter = 0
            legendaries = [e for e in self.entries if e.get("rarity") == LootRarity.LEGENDARY.value]
            if legendaries:
                return random.choice(legendaries)

        roll = random.random() * luck_modifier
        cumulative = 0.0
        for entry in self.entries:
            cumulative += entry.get("rate", 0)
            if roll <= cumulative:
                return entry
        return self.entries[-1] if self.entries else None


@dataclass
class DamageResult:
    """Result of a damage calculation."""
    raw_damage: float
    is_crit: bool
    is_dodged: bool
    is_blocked: bool
    final_damage: float
    overkill: float = 0.0

    @property
    def effective(self) -> bool:
        return not self.is_dodged and self.final_damage > 0


@dataclass
class BalanceReport:
    """Output of a balance simulation."""
    matchup: str
    iterations: int
    avg_turns: float
    winner_distribution: Dict[str, float] = field(default_factory=dict)
    avg_damage_per_turn: Dict[str, float] = field(default_factory=dict)
    ttk_avg: Dict[str, float] = field(default_factory=dict)
    balance_score: float = 0.0


@dataclass
class RetentionCohort:
    """Player retention by day."""
    cohort_date: datetime
    total_players: int
    retention_by_day: Dict[int, float] = field(default_factory=dict)

    @property
    def d1_retention(self) -> float:
        return self.retention_by_day.get(1, 0.0)

    @property
    def d7_retention(self) -> float:
        return self.retention_by_day.get(7, 0.0)

    @property
    def d30_retention(self) -> float:
        return self.retention_by_day.get(30, 0.0)


@dataclass
class QAbug:
    """QA bug report."""
    bug_id: str
    title: str
    description: str
    severity: BugSeverity
    status: BugStatus = BugStatus.OPEN
    steps_to_reproduce: List[str] = field(default_factory=list)
    expected: str = ""
    actual: str = ""
    environment: str = ""
    reporter: str = ""
    assignee: str = ""
    reported_date: datetime = field(default_factory=datetime.utcnow)
    resolved_date: Optional[datetime] = None
    regression: bool = False
    tags: List[str] = field(default_factory=list)

    @property
    def is_open(self) -> bool:
        return self.status in (BugStatus.OPEN, BugStatus.IN_PROGRESS, BugStatus.FIX_PENDING)

    @property
    def resolution_time_hours(self) -> Optional[float]:
        if self.resolved_date:
            return (self.resolved_date - self.reported_date).total_seconds() / 3600
        return None


@dataclass
class EconomyState:
    """Snapshot of the game economy."""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    total_soft_currency_circulating: float = 0.0
    total_premium_currency_circulating: float = 0.0
    avg_soft_per_player: float = 0.0
    avg_premium_per_player: float = 0.0
    soft_earn_rate_per_hour: float = 0.0
    soft_spend_rate_per_hour: float = 0.0
    premium_earn_rate_per_hour: float = 0.0
    premium_spend_rate_per_hour: float = 0.0
    inflation_rate: float = 0.0

    @property
    def is_healthy(self) -> bool:
        return abs(self.inflation_rate) < 0.05

    @property
    def sink_to_faucet_ratio(self) -> float:
        if self.soft_earn_rate_per_hour == 0:
            return float('inf')
        return self.soft_spend_rate_per_hour / self.soft_earn_rate_per_hour


@dataclass
class LevelConfig:
    """Level/map configuration."""
    level_id: str
    name: str
    difficulty: DifficultyLevel
    recommended_level: int = 1
    enemies: List[Dict[str, Any]] = field(default_factory=list)
    rewards: Dict[str, Any] = field(default_factory=dict)
    time_limit_seconds: Optional[int] = None
    par_score: int = 0
    theme: str = ""
    music_track: str = ""

    @property
    def enemy_count(self) -> int:
        return len(self.enemies)


@dataclass
class EventConfig:
    """Limited-time event configuration."""
    event_id: str
    name: str
    start_date: datetime = field(default_factory=datetime.utcnow)
    end_date: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=7))
    event_type: str = "seasonal"
    currency_earned: str = "event"
    exclusive_rewards: List[str] = field(default_factory=list)
    multiplier: float = 1.0
    description: str = ""

    @property
    def is_active(self) -> bool:
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date

    @property
    def days_remaining(self) -> int:
        remaining = (self.end_date - datetime.utcnow()).days
        return max(remaining, 0)


@dataclass
class DifficultyScaling:
    """Scaling parameters for adaptive difficulty."""
    base_enemy_hp: float = 100.0
    base_enemy_damage: float = 10.0
    hp_scale_per_level: float = 0.15
    damage_scale_per_level: float = 0.10
    player_advantage_bonus: float = 0.05
    catch_up_mechanic: bool = True
    max_difficulty_multiplier: float = 2.0

    def scale_enemy(self, base_hp: float, base_dmg: float, player_level: int, enemy_level: int) -> Tuple[float, float]:
        level_diff = enemy_level - player_level
        hp_mult = 1 + self.hp_scale_per_level * level_diff
        dmg_mult = 1 + self.damage_scale_per_level * level_diff
        hp_mult = min(hp_mult, self.max_difficulty_multiplier)
        dmg_mult = min(dmg_mult, self.max_difficulty_multiplier)
        return base_hp * hp_mult, base_dmg * dmg_mult


# ---------------------------------------------------------------------------
# Combat System
# ---------------------------------------------------------------------------

class CombatEngine:
    """
    Turn-based combat simulation with damage formulas,
    critical hits, dodges, and status effects.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        self.rng = random.Random(seed)

    def calculate_damage(
        self,
        attacker: CharacterStats,
        defender: CharacterStats,
        skill_multiplier: float = 1.0,
        element_modifier: float = 1.0,
    ) -> DamageResult:
        raw_damage = attacker.attack * skill_multiplier * element_modifier

        is_dodged = self.rng.random() < defender.dodge
        if is_dodged:
            return DamageResult(raw_damage, False, True, False, 0)

        is_crit = self.rng.random() < attacker.crit_chance
        if is_crit:
            raw_damage *= attacker.crit_damage

        defense_reduction = defender.defense / (defender.defense + 100)
        after_defense = raw_damage * (1 - defense_reduction)

        is_blocked = self.rng.random() < defender.block
        if is_blocked:
            after_defense *= 0.5

        final_damage = max(1, after_defense)
        return DamageResult(raw_damage, is_crit, False, is_blocked, final_damage)

    def simulate_battle(
        self,
        char_a: CharacterStats,
        char_b: CharacterStats,
        max_turns: int = 100,
        name_a: str = "A",
        name_b: str = "B",
    ) -> Dict[str, Any]:
        a_hp = char_a.health
        b_hp = char_b.health
        turns = 0
        a_damage_total = 0
        b_damage_total = 0

        while a_hp > 0 and b_hp > 0 and turns < max_turns:
            turns += 1

            if char_a.speed >= char_b.speed:
                first, second = (char_a, char_b)
                first_hp, second_hp = [a_hp], [b_hp]
            else:
                first, second = (char_b, char_a)
                first_hp, second_hp = [b_hp], [a_hp]

            result = self.calculate_damage(first, second)
            second_hp[0] -= result.final_damage
            if first == char_a:
                a_damage_total += result.final_damage
            else:
                b_damage_total += result.final_damage

            if second_hp[0] <= 0:
                break

            result2 = self.calculate_damage(second, first)
            first_hp[0] -= result2.final_damage
            if second == char_a:
                a_damage_total += result2.final_damage
            else:
                b_damage_total += result2.final_damage

            a_hp, b_hp = first_hp[0], second_hp[0]

        winner = name_a if a_hp > 0 else name_b if b_hp > 0 else "draw"
        return {
            "winner": winner,
            "turns": turns,
            "a_hp_remaining": max(a_hp, 0),
            "b_hp_remaining": max(b_hp, 0),
            "a_total_damage": a_damage_total,
            "b_total_damage": b_damage_total,
        }

    def run_balance_simulation(
        self,
        stats_a: CharacterStats,
        stats_b: CharacterStats,
        name_a: str = "A",
        name_b: str = "B",
        iterations: int = 1000,
    ) -> BalanceReport:
        wins = defaultdict(int)
        total_turns = 0
        damage_a = []
        damage_b = []
        ttk_a = []
        ttk_b = []

        for _ in range(iterations):
            result = self.simulate_battle(stats_a, stats_b, name_a=name_a, name_b=name_b)
            wins[result["winner"]] += 1
            total_turns += result["turns"]
            damage_a.append(result["a_total_damage"])
            damage_b.append(result["b_total_damage"])
            if result["winner"] == name_a:
                ttk_a.append(result["turns"])
            elif result["winner"] == name_b:
                ttk_b.append(result["turns"])

        win_dist = {k: v / iterations for k, v in wins.items()}
        avg_dmg_a = statistics.mean(damage_a) if damage_a else 0
        avg_dmg_b = statistics.mean(damage_b) if damage_b else 0
        balance = 1 - abs(win_dist.get(name_a, 0) - 0.5) * 2

        return BalanceReport(
            matchup=f"{name_a} vs {name_b}",
            iterations=iterations,
            avg_turns=total_turns / iterations,
            winner_distribution=win_dist,
            avg_damage_per_turn={name_a: avg_dmg_a, name_b: avg_dmg_b},
            ttk_avg={name_a: statistics.mean(ttk_a) if ttk_a else 0, name_b: statistics.mean(ttk_b) if ttk_b else 0},
            balance_score=balance,
        )


# ---------------------------------------------------------------------------
# Economy System
# ---------------------------------------------------------------------------

class EconomyManager:
    """
    Manages in-game economy: currencies, pricing, inflation tracking,
    and sink/faucet analysis.
    """

    def __init__(self) -> None:
        self.currencies: Dict[str, Dict[str, Any]] = {}
        self.price_lists: Dict[str, List[Dict[str, Any]]] = {}
        self.history: List[EconomyState] = []
        logger.info("EconomyManager initialized")

    def register_currency(
        self, name: str, currency_type: CurrencyType, initial_supply: float = 0
    ) -> None:
        self.currencies[name] = {
            "type": currency_type.value,
            "supply": initial_supply,
            "circulating": initial_supply,
            "earned_total": 0.0,
            "spent_total": 0.0,
        }

    def earn(self, currency: str, amount: float, source: str = "unknown") -> None:
        if currency not in self.currencies:
            return
        self.currencies[currency]["circulating"] += amount
        self.currencies[currency]["earned_total"] += amount

    def spend(self, currency: str, amount: float, sink: str = "unknown") -> bool:
        if currency not in self.currencies:
            return False
        if self.currencies[currency]["circulating"] < amount:
            return False
        self.currencies[currency]["circulating"] -= amount
        self.currencies[currency]["spent_total"] += amount
        return True

    def get_inflation_rate(self, currency: str) -> float:
        if currency not in self.currencies:
            return 0.0
        c = self.currencies[currency]
        if c["earned_total"] == 0:
            return 0.0
        return (c["earned_total"] - c["spent_total"]) / c["earned_total"]

    def snapshot(self, num_players: int = 1) -> EconomyState:
        state = EconomyState()
        for name, c in self.currencies.items():
            if c["type"] == CurrencyType.SOFT.value:
                state.total_soft_currency_circulating = c["circulating"]
                state.avg_soft_per_player = c["circulating"] / max(num_players, 1)
            elif c["type"] == CurrencyType.PREMIUM.value:
                state.total_premium_currency_circulating = c["circulating"]
                state.avg_premium_per_player = c["circulating"] / max(num_players, 1)
        state.inflation_rate = self.get_inflation_rate("gold")
        self.history.append(state)
        return state

    def health_check(self) -> Dict[str, Any]:
        issues = []
        for name, c in self.currencies.items():
            inf = self.get_inflation_rate(name)
            if inf > 0.1:
                issues.append(f"{name}: high inflation ({inf:.1%})")
            elif inf < -0.1:
                issues.append(f"{name}: deflation ({inf:.1%})")
            if c["circulating"] > c["supply"] * 2:
                issues.append(f"{name}: excessive supply ({c['circulating']:.0f})")
        return {
            "healthy": len(issues) == 0,
            "issues": issues,
            "currencies": {
                name: {
                    "circulating": c["circulating"],
                    "inflation": self.get_inflation_rate(name),
                }
                for name, c in self.currencies.items()
            },
        }

    def set_price(self, item_id: str, currency: str, price: int) -> None:
        if item_id not in self.price_lists:
            self.price_lists[item_id] = []
        self.price_lists[item_id].append({"currency": currency, "price": price})

    def can_afford(self, player: PlayerProfile, item_id: str) -> bool:
        if item_id not in self.price_lists:
            return False
        for pricing in self.price_lists[item_id]:
            cur = player.currencies.get(pricing["currency"], 0)
            if cur >= pricing["price"]:
                return True
        return False


# ---------------------------------------------------------------------------
# Progression System
# ---------------------------------------------------------------------------

class ProgressionSystem:
    """
    Manages player progression: leveling curves, experience tables,
    unlock gates, and difficulty scaling.
    """

    def __init__(
        self,
        max_level: int = 100,
        base_exp: int = 100,
        exp_growth: float = 1.15,
    ) -> None:
        self.max_level = max_level
        self.base_exp = base_exp
        self.exp_growth = exp_growth
        self._exp_table: Dict[int, int] = {}
        self._build_exp_table()

    def _build_exp_table(self) -> None:
        for level in range(1, self.max_level + 1):
            self._exp_table[level] = int(self.base_exp * (self.exp_growth ** (level - 1)))

    def exp_for_level(self, level: int) -> int:
        return self._exp_table.get(level, self._exp_table.get(self.max_level, 999999))

    def total_exp_to_level(self, from_level: int, to_level: int) -> int:
        return sum(self.exp_for_level(l) for l in range(from_level, to_level))

    def level_from_total_exp(self, total_exp: int) -> Tuple[int, int]:
        level = 1
        remaining = total_exp
        while level < self.max_level:
            needed = self.exp_for_level(level)
            if remaining < needed:
                break
            remaining -= needed
            level += 1
        return level, remaining

    def get_unlock_gates(self, current_level: int) -> List[Dict[str, Any]]:
        gates = [
            {"feature": "PvP Arena", "level": 10},
            {"feature": "Guild System", "level": 15},
            {"feature": "Crafting", "level": 20},
            {"feature": "Raids", "level": 30},
            {"feature": "Legendary Quests", "level": 40},
            {"feature": "Endgame Dungeons", "level": 50},
        ]
        return [
            {**g, "unlocked": current_level >= g["level"]}
            for g in gates
        ]

    def generate_curve_data(self, max_level: Optional[int] = None) -> List[Dict[str, Any]]:
        ml = max_level or self.max_level
        return [
            {"level": l, "exp_required": self.exp_for_level(l), "cumulative": self.total_exp_to_level(1, l + 1)}
            for l in range(1, ml + 1)
        ]


# ---------------------------------------------------------------------------
# Loot System
# ---------------------------------------------------------------------------

class LootSystem:
    """
    Loot drop, gacha, and reward distribution system with
    pity timers, luck modifiers, and probability transparency.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        self.rng = random.Random(seed)
        self.tables: Dict[str, LootTable] = {}
        self.drop_history: List[Dict[str, Any]] = []

    def register_table(self, table: LootTable) -> None:
        self.tables[table.source_id] = table

    def open_loot(
        self, source_id: str, count: int = 1, luck: float = 1.0
    ) -> List[Dict[str, Any]]:
        if source_id not in self.tables:
            return []
        table = self.tables[source_id]
        results = []
        for _ in range(count):
            entry = table.roll(luck)
            if entry:
                result = {
                    "item_id": entry.get("item_id", "unknown"),
                    "name": entry.get("name", "Unknown"),
                    "rarity": entry.get("rarity", LootRarity.COMMON.value),
                    "quantity": entry.get("quantity", 1),
                }
                results.append(result)
                self.drop_history.append(result)
        return results

    def get_drop_rates(self, source_id: str) -> Dict[str, float]:
        if source_id not in self.tables:
            return {}
        table = self.tables[source_id]
        return {
            entry.get("name", "unknown"): entry.get("rate", 0)
            for entry in table.entries
        }

    def calculate_expected_value(
        self, source_id: str, rolls: int = 1000, luck: float = 1.0
    ) -> Dict[str, Any]:
        rarity_counts: Dict[str, int] = defaultdict(int)
        for _ in range(rolls):
            results = self.open_loot(source_id, 1, luck)
            for r in results:
                rarity_counts[r["rarity"]] += 1
        return {
            "rolls": rolls,
            "distribution": {k: v / rolls for k, v in rarity_counts.items()},
            "absolute": dict(rarity_counts),
        }

    def pity_status(self, source_id: str) -> Dict[str, Any]:
        if source_id not in self.tables:
            return {}
        table = self.tables[source_id]
        return {
            "source": source_id,
            "pity_counter": table.pity_counter,
            "pity_threshold": table.pity_threshold,
            "rolls_until_pity": table.pity_threshold - table.pity_counter,
        }


# ---------------------------------------------------------------------------
# Analytics & Engagement
# ---------------------------------------------------------------------------

class EngagementAnalyzer:
    """
    Player engagement analytics: retention, session analysis,
    churn prediction, and segmentation.
    """

    def __init__(self) -> None:
        self.sessions: List[Dict[str, Any]] = []
        self.cohorts: List[RetentionCohort] = []

    def record_session(
        self, player_id: str, start: datetime, duration_minutes: float,
        activities: List[str] = None
    ) -> None:
        self.sessions.append({
            "player_id": player_id,
            "start": start,
            "duration": duration_minutes,
            "activities": activities or [],
        })

    def calculate_retention(
        self, players: List[PlayerProfile], cohort_date: datetime, days: int = 30
    ) -> RetentionCohort:
        total = len(players)
        retention: Dict[int, float] = {}
        for day in range(1, days + 1):
            target_date = cohort_date + timedelta(days=day)
            active = sum(
                1 for p in players
                if p.last_active.date() >= target_date.date()
            )
            retention[day] = active / total if total > 0 else 0
        return RetentionCohort(
            cohort_date=cohort_date,
            total_players=total,
            retention_by_day=retention,
        )

    def segment_players(self, players: List[PlayerProfile]) -> Dict[PlayerStatus, List[PlayerProfile]]:
        segments: Dict[PlayerStatus, List[PlayerProfile]] = defaultdict(list)
        for p in players:
            if p.days_since_active > 30:
                segments[PlayerStatus.CHURNED].append(p)
            elif p.total_spent > 100:
                segments[PlayerStatus.WHALE].append(p)
            elif p.playtime_hours > 100:
                segments[PlayerStatus.DEDICATED].append(p)
            elif p.playtime_hours > 20:
                segments[PlayerStatus.REGULAR].append(p)
            elif p.playtime_hours > 5:
                segments[PlayerStatus.CASUAL].append(p)
            else:
                segments[PlayerStatus.NEW].append(p)
        return dict(segments)

    def predict_churn_risk(self, player: PlayerProfile) -> Dict[str, Any]:
        risk_score = 0.0
        factors = []
        if player.days_since_active > 7:
            risk_score += 0.3
            factors.append("inactive_7_days")
        if player.days_since_active > 14:
            risk_score += 0.2
            factors.append("inactive_14_days")
        if player.session_count < 5:
            risk_score += 0.15
            factors.append("low_session_count")
        if player.total_spent == 0 and player.playtime_hours > 20:
            risk_score += 0.1
            factors.append("non_paying_engaged")
        if player.level < 10 and player.days_since_join > 7:
            risk_score += 0.1
            factors.append("stalled_progression")
        risk_score = min(risk_score, 1.0)
        level = "low"
        if risk_score > 0.7:
            level = "high"
        elif risk_score > 0.4:
            level = "medium"
        return {"risk_score": risk_score, "risk_level": level, "factors": factors}

    def calculate_engagement_score(self, player: PlayerProfile) -> float:
        score = 0.0
        score += min(player.session_count / 50, 1.0) * 25
        score += min(player.playtime_hours / 100, 1.0) * 25
        score += min(player.level / 50, 1.0) * 25
        activity_recency = max(0, 1 - player.days_since_active / 30)
        score += activity_recency * 25
        return round(score, 1)

    def get_analytics_summary(self, players: List[PlayerProfile]) -> Dict[str, Any]:
        if not players:
            return {}
        segments = self.segment_players(players)
        avg_playtime = statistics.mean(p.playtime_hours for p in players)
        avg_level = statistics.mean(p.level for p in players)
        avg_spend = statistics.mean(p.total_spent for p in players)
        paying = [p for p in players if p.total_spent > 0]
        return {
            "total_players": len(players),
            "avg_playtime_hours": round(avg_playtime, 1),
            "avg_level": round(avg_level, 1),
            "avg_spend": round(avg_spend, 2),
            "conversion_rate": len(paying) / len(players) if players else 0,
            "segments": {k.value: len(v) for k, v in segments.items()},
        }


# ---------------------------------------------------------------------------
# QA System
# ---------------------------------------------------------------------------

class QAManager:
    """
    QA bug tracking, test case management, and release readiness assessment.
    """

    def __init__(self) -> None:
        self.bugs: Dict[str, QAbug] = {}
        self.test_cases: List[Dict[str, Any]] = []
        self._bug_counter = 0

    def report_bug(self, title: str, description: str, severity: BugSeverity, **kwargs: Any) -> QAbug:
        self._bug_counter += 1
        bug_id = f"BUG-{self._bug_counter:04d}"
        bug = QAbug(
            bug_id=bug_id, title=title, description=description,
            severity=severity, **kwargs,
        )
        self.bugs[bug_id] = bug
        logger.info("Bug reported: %s [%s] %s", bug_id, severity.name, title)
        return bug

    def update_bug_status(self, bug_id: str, status: BugStatus) -> bool:
        if bug_id not in self.bugs:
            return False
        self.bugs[bug_id].status = status
        if status in (BugStatus.VERIFIED, BugStatus.CLOSED):
            self.bugs[bug_id].resolved_date = datetime.utcnow()
        return True

    def get_open_bugs(self) -> List[QAbug]:
        return [b for b in self.bugs.values() if b.is_open]

    def get_critical_bugs(self) -> List[QAbug]:
        return [b for b in self.bugs.values() if b.severity == BugSeverity.CRITICAL and b.is_open]

    def bug_summary(self) -> Dict[str, Any]:
        by_severity = defaultdict(int)
        by_status = defaultdict(int)
        for bug in self.bugs.values():
            by_severity[bug.severity.name] += 1
            by_status[bug.status.value] += 1
        return {
            "total": len(self.bugs),
            "open": len(self.get_open_bugs()),
            "critical_open": len(self.get_critical_bugs()),
            "by_severity": dict(by_severity),
            "by_status": dict(by_status),
        }

    def generate_test_cases(self, feature: str, test_type: str = "functional") -> List[Dict[str, Any]]:
        cases = [
            {
                "id": f"TC-{len(self.test_cases) + i + 1:04d}",
                "feature": feature,
                "type": test_type,
                "title": f"{test_type.title()} test for {feature} - scenario {i + 1}",
                "steps": [f"Step {j + 1}" for j in range(3)],
                "expected": "Feature works as specified",
                "priority": "high",
            }
            for i in range(3)
        ]
        self.test_cases.extend(cases)
        return cases

    def release_readiness(self) -> Dict[str, Any]:
        critical = self.get_critical_bugs()
        high = [b for b in self.bugs.values() if b.severity == BugSeverity.HIGH and b.is_open]
        return {
            "ready": len(critical) == 0 and len(high) == 0,
            "blocking_issues": len(critical) + len(high),
            "critical_bugs": len(critical),
            "high_bugs": len(high),
            "recommendation": "Ready to ship" if len(critical) == 0 else "Must fix critical bugs first",
        }


# ---------------------------------------------------------------------------
# Difficulty Scaler
# ---------------------------------------------------------------------------

class DifficultyScaler:
    """Adaptive difficulty system based on player performance."""

    def __init__(self, config: Optional[DifficultyScaling] = None) -> None:
        self.config = config or DifficultyScaling()

    def scale_encounter(
        self, base_hp: float, base_damage: float, player_level: int, enemy_level: int
    ) -> Dict[str, float]:
        hp, dmg = self.config.scale_enemy(base_hp, base_damage, player_level, enemy_level)
        return {"hp": hp, "damage": dmg}

    def calculate_recommended_level(
        self, player_performance: Dict[str, float]
    ) -> int:
        win_rate = player_performance.get("win_rate", 0.5)
        avg_turns = player_performance.get("avg_turns", 5)
        if win_rate > 0.8 and avg_turns < 3:
            return min(player_performance.get("current_level", 1) + 5, 100)
        elif win_rate < 0.3:
            return max(player_performance.get("current_level", 1) - 3, 1)
        return player_performance.get("current_level", 1)

    def generate_difficulty_curve(
        self, max_level: int = 50, base_hp: float = 100, base_dmg: float = 10
    ) -> List[Dict[str, Any]]:
        curve = []
        for level in range(1, max_level + 1):
            hp, dmg = self.config.scale_enemy(base_hp, base_dmg, 1, level)
            curve.append({"level": level, "hp": round(hp, 1), "damage": round(dmg, 1)})
        return curve


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("Gaming Agent — Comprehensive Demo")
    print("=" * 60)

    # Game Config
    config = GameConfig(title="Dragon Quest Legends", genre=GameGenre.RPG, platform=["PC", "Mobile"], monetization=MonetizationModel.FREE_TO_PLAY)
    print(f"\nGame: {config.title} ({config.genre.value})")
    print(f"Platforms: {', '.join(config.platform)}")

    # Combat System
    combat = CombatEngine(seed=42)
    warrior = CharacterStats(level=10, health=500, attack=50, defense=20, speed=1.0, crit_chance=0.1)
    mage = CharacterStats(level=10, health=300, attack=80, defense=10, speed=1.2, crit_chance=0.15)
    result = combat.simulate_battle(warrior, mage, name_a="Warrior", name_b="Mage")
    print(f"\nBattle: {result['winner']} won in {result['turns']} turns")

    balance = combat.run_balance_simulation(warrior, mage, "Warrior", "Mage", 500)
    print(f"Balance score: {balance.balance_score:.3f} (1.0 = perfect)")
    print(f"Win distribution: {balance.winner_distribution}")

    # Economy
    economy = EconomyManager()
    economy.register_currency("gold", CurrencyType.SOFT, 1000000)
    economy.register_currency("gems", CurrencyType.PREMIUM, 50000)
    economy.earn("gold", 500, "quest_reward")
    economy.spend("gold", 200, "shop_purchase")
    health = economy.health_check()
    print(f"\nEconomy healthy: {health['healthy']}")

    # Progression
    progression = ProgressionSystem(max_level=100, base_exp=100, exp_growth=1.15)
    print(f"\nExp for level 10: {progression.exp_for_level(10)}")
    print(f"Total exp to level 50: {progression.total_exp_to_level(1, 50)}")

    # Loot System
    loot = LootSystem(seed=42)
    table = LootTable("chest_1", "Wooden Chest", entries=[
        {"item_id": "sword_1", "name": "Iron Sword", "rarity": "common", "rate": 0.5},
        {"item_id": "shield_1", "name": "Wooden Shield", "rarity": "uncommon", "rate": 0.3},
        {"item_id": "ring_1", "name": "Magic Ring", "rarity": "rare", "rate": 0.15},
        {"item_id": "sword_legendary", "name": "Dragon Blade", "rarity": "legendary", "rate": 0.05},
    ])
    loot.register_table(table)
    drops = loot.open_loot("chest_1", 10)
    print(f"\nLoot drops: {[d['name'] for d in drops]}")

    # Engagement
    analytics = EngagementAnalyzer()
    players = [
        PlayerProfile("P1", "Hero", level=25, playtime_hours=80, total_spent=50, session_count=40, last_active=datetime.utcnow() - timedelta(days=1)),
        PlayerProfile("P2", "Noob", level=3, playtime_hours=2, total_spent=0, session_count=3),
        PlayerProfile("P3", "Whale", level=40, playtime_hours=200, total_spent=500, session_count=100),
    ]
    summary = analytics.get_analytics_summary(players)
    print(f"\nAnalytics: {summary['total_players']} players, avg level {summary['avg_level']}")
    print(f"Segments: {summary['segments']}")

    # QA
    qa = QAManager()
    qa.report_bug("Crash on level 5", "Game crashes when entering level 5", BugSeverity.CRITICAL)
    qa.report_bug("UI overlap", "Inventory overlaps shop UI", BugSeverity.MEDIUM)
    qa.release_readiness()
    print(f"\nQA: {qa.bug_summary()['open']} open bugs")

    # Difficulty
    scaler = DifficultyScaler()
    curve = scaler.generate_difficulty_curve(max_level=10)
    print(f"\nDifficulty curve (levels 1-10): HP range {curve[0]['hp']:.0f} - {curve[-1]['hp']:.0f}")

    print("\n" + "=" * 60)
    print("Gaming Agent demo complete.")
    print("=" * 60)
