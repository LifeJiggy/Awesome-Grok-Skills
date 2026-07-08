# Gaming Agent

> Game development toolkit for combat simulation, economy management, player engagement analytics, loot systems, progression design, QA testing, and difficulty scaling.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Usage](#usage)
  - [Combat System](#combat-system)
  - [Economy Management](#economy-management)
  - [Progression System](#progression-system)
  - [Loot System](#loot-system)
  - [Engagement Analytics](#engagement-analytics)
  - [QA Management](#qa-management)
  - [Difficulty Scaling](#difficulty-scaling)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Gaming Agent provides a complete toolkit for game design and development:

- **Combat Engine**: Turn-based battle simulation with damage formulas, critical hits, dodges, and balance testing
- **Economy Manager**: In-game currency tracking, pricing, inflation monitoring, and sink/faucet analysis
- **Progression System**: Level curves, experience tables, and feature unlock gates
- **Loot System**: Gacha/loot box mechanics with pity timers, probability management, and drop rate verification
- **Engagement Analytics**: Player segmentation, churn prediction, and retention modeling
- **QA Manager**: Bug tracking with severity classification and release readiness assessment
- **Difficulty Scaler**: Adaptive difficulty based on player performance

Built with zero external dependencies — pure Python standard library.

---

## Features

| Category | Capabilities |
|----------|-------------|
| Combat | Turn-based simulation, damage formula, crit/dodge/block, balance testing |
| Economy | Currency tracking, inflation monitoring, sink/faucet analysis, health checks |
| Progression | Exp curves, level-up system, feature unlocks, curve visualization |
| Loot | Gacha mechanics, pity timers, drop rate verification, probability simulation |
| Engagement | Player segmentation, churn prediction, retention analysis, engagement scoring |
| QA | Bug tracking, severity classification, test case generation, release readiness |
| Difficulty | Adaptive scaling, encounter balancing, difficulty curves |
| Events | Limited-time events, seasonal content, multipliers |

---

## Quick Start

```python
from agents.gaming.agent import CombatEngine, CharacterStats, EconomyManager, CurrencyType

# Combat simulation
combat = CombatEngine(seed=42)
warrior = CharacterStats(level=10, health=500, attack=50, defense=20, speed=1.0)
mage = CharacterStats(level=10, health=300, attack=80, defense=10, speed=1.2)
result = combat.simulate_battle(warrior, mage, name_a="Warrior", name_b="Mage")
print(f"Winner: {result['winner']} in {result['turns']} turns")

# Economy tracking
economy = EconomyManager()
economy.register_currency("gold", CurrencyType.SOFT, 1_000_000)
economy.earn("gold", 500, "quest_reward")
economy.spend("gold", 200, "shop")
print(f"Health: {economy.health_check()['healthy']}")
```

### Run the Agent

```bash
python agents/gaming/agent.py
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Gaming Agent                            │
├─────────────────────────────────────────────────────────────┤
│  Combat Engine │ Economy Manager │ Progression System        │
│  Loot System   │ Engagement      │ QA Manager │ Difficulty   │
├─────────────────────────────────────────────────────────────┤
│     Data Models (Player, Item, Quest, Bug, Level, Event)    │
└─────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

---

## Usage

### Combat System

```python
from agents.gaming.agent import CombatEngine, CharacterStats

combat = CombatEngine(seed=42)

# Define characters
warrior = CharacterStats(level=10, health=500, attack=50, defense=20, speed=1.0, crit_chance=0.1)
mage = CharacterStats(level=10, health=300, attack=80, defense=10, speed=1.2, crit_chance=0.15)

# Single battle
result = combat.simulate_battle(warrior, mage, name_a="Warrior", name_b="Mage")
print(f"Winner: {result['winner']}, Turns: {result['turns']}")

# Balance simulation (1000 iterations)
balance = combat.run_balance_simulation(warrior, mage, "Warrior", "Mage", iterations=1000)
print(f"Balance score: {balance.balance_score:.3f}")
print(f"Win rates: {balance.winner_distribution}")
```

### Economy Management

```python
from agents.gaming.agent import EconomyManager, CurrencyType

economy = EconomyManager()

# Register currencies
economy.register_currency("gold", CurrencyType.SOFT, initial_supply=1_000_000)
economy.register_currency("gems", CurrencyType.PREMIUM, initial_supply=50_000)
economy.register_currency("tokens", CurrencyType.EVENT, initial_supply=0)

# Faucets (earning)
economy.earn("gold", 500, source="quest_reward")
economy.earn("gold", 200, source="monster_drop")
economy.earn("gems", 10, source="daily_login")

# Sinks (spending)
economy.spend("gold", 200, sink="shop_purchase")
economy.spend("gems", 50, sink="gacha_pull")

# Health check
health = economy.health_check()
print(f"Economy healthy: {health['healthy']}")
print(f"Issues: {health['issues']}")
```

### Progression System

```python
from agents.gaming.agent import ProgressionSystem

prog = ProgressionSystem(max_level=100, base_exp=100, exp_growth=1.15)

# Exp requirements
print(f"Exp for level 5: {prog.exp_for_level(5)}")   # 174
print(f"Exp for level 10: {prog.exp_for_level(10)}")  # 351
print(f"Exp for level 50: {prog.exp_for_level(50)}")  # 10,836

# Total exp to reach a level
total = prog.total_exp_to_level(1, 50)
print(f"Total exp to level 50: {total}")

# Feature unlocks
gates = prog.get_unlock_gates(player_level=25)
for gate in gates:
    status = "UNLOCKED" if gate["unlocked"] else "LOCKED"
    print(f"  Level {gate['level']}: {gate['feature']} - {status}")

# Generate curve data for visualization
curve = prog.generate_curve_data(max_level=30)
```

### Loot System

```python
from agents.gaming.agent import LootSystem, LootTable

loot = LootSystem(seed=42)

# Define a loot table
chest = LootTable(
    source_id="chest_1",
    source_name="Wooden Chest",
    pity_threshold=50,
    entries=[
        {"item_id": "sword_1", "name": "Iron Sword", "rarity": "common", "rate": 0.50},
        {"item_id": "shield_1", "name": "Wooden Shield", "rarity": "uncommon", "rate": 0.30},
        {"item_id": "ring_1", "name": "Magic Ring", "rarity": "rare", "rate": 0.15},
        {"item_id": "dragon_sword", "name": "Dragon Blade", "rarity": "legendary", "rate": 0.05},
    ]
)
loot.register_table(chest)

# Roll 10 drops
drops = loot.open_loot("chest_1", count=10, luck=1.0)
for drop in drops:
    print(f"  {drop['name']} ({drop['rarity']})")

# Verify drop rates with simulation
ev = loot.calculate_expected_value("chest_1", rolls=10000)
print(f"Observed rates: {ev['distribution']}")

# Pity status
pity = loot.pity_status("chest_1")
print(f"Rolls until pity: {pity['rolls_until_pity']}")
```

### Engagement Analytics

```python
from agents.gaming.agent import EngagementAnalyzer, PlayerProfile, PlayerStatus

analytics = EngagementAnalyzer()

# Create sample players
players = [
    PlayerProfile("P1", "Hero", level=25, playtime_hours=80, total_spent=50, session_count=40),
    PlayerProfile("P2", "Noob", level=3, playtime_hours=2, total_spent=0, session_count=3),
    PlayerProfile("P3", "Whale", level=40, playtime_hours=200, total_spent=500, session_count=100),
    PlayerProfile("P4", "Lurker", level=15, playtime_hours=30, total_spent=0, session_count=15),
]

# Segment players
segments = analytics.segment_players(players)
for status, group in segments.items():
    print(f"  {status.value}: {len(group)} players")

# Churn prediction
for p in players:
    risk = analytics.predict_churn_risk(p)
    print(f"  {p.name}: risk={risk['risk_score']:.2f} ({risk['risk_level']})")

# Engagement scores
for p in players:
    score = analytics.calculate_engagement_score(p)
    print(f"  {p.name}: engagement={score}")

# Full summary
summary = analytics.get_analytics_summary(players)
```

### QA Management

```python
from agents.gaming.agent import QAManager, BugSeverity, BugStatus

qa = QAManager()

# Report bugs
bug1 = qa.report_bug("Crash on level 5", "Game crashes entering level 5", BugSeverity.CRITICAL)
bug2 = qa.report_bug("UI overlap", "Inventory overlaps shop UI", BugSeverity.MEDIUM)
bug3 = qa.report_bug("Sound glitch", "Music loops incorrectly", BugSeverity.LOW)

# Update status
qa.update_bug_status(bug1.bug_id, BugStatus.VERIFIED)

# Get summary
summary = qa.bug_summary()
print(f"Open: {summary['open']}, Critical: {summary['critical_open']}")

# Release readiness
ready = qa.release_readiness()
print(f"Ready: {ready['ready']}, Recommendation: {ready['recommendation']}")
```

### Difficulty Scaling

```python
from agents.gaming.agent import DifficultyScaler, DifficultyScaling

scaler = DifficultyScaler(DifficultyScaling(
    base_enemy_hp=100,
    base_enemy_damage=10,
    hp_scale_per_level=0.15,
    damage_scale_per_level=0.10,
))

# Scale an encounter
scaled = scaler.scale_encounter(base_hp=100, base_dmg=10, player_level=10, enemy_level=15)
print(f"Scaled: HP={scaled['hp']:.1f}, Damage={scaled['damage']:.1f}")

# Generate difficulty curve
curve = scaler.generate_difficulty_curve(max_level=20)
for point in curve[:5]:
    print(f"  Level {point['level']}: HP={point['hp']:.0f}, DMG={point['damage']:.1f}")

# Recommend difficulty
rec = scaler.calculate_recommended_level({"win_rate": 0.85, "avg_turns": 2, "current_level": 10})
print(f"Recommended level: {rec}")
```

---

## API Reference

### Core Classes

| Class | Description |
|-------|-------------|
| `CombatEngine` | Turn-based combat simulation and balance testing |
| `EconomyManager` | Currency tracking and inflation monitoring |
| `ProgressionSystem` | Level curves and feature unlocks |
| `LootSystem` | Gacha/loot mechanics with pity timers |
| `EngagementAnalyzer` | Player segmentation and churn prediction |
| `QAManager` | Bug tracking and release readiness |
| `DifficultyScaler` | Adaptive difficulty scaling |

### Data Classes

| Class | Description |
|-------|-------------|
| `GameConfig` | Top-level game configuration |
| `CharacterStats` | Character combat statistics |
| `PlayerProfile` | Player account and progression |
| `Item` | In-game item definition |
| `Quest` | Quest/mission definition |
| `LootTable` | Loot drop configuration |
| `BalanceReport` | Balance simulation results |
| `RetentionCohort` | Player retention data |
| `QAbug` | Bug report |
| `LevelConfig` | Level/map configuration |
| `EventConfig` | Limited-time event |

### Enums

| Enum | Values |
|------|--------|
| `GameGenre` | RPG, FPS, STRATEGY, PUZZLE, PLATFORMER, MOBA, BATTLE_ROYALE, CARD_GAME, IDLE, ROGUELIKE |
| `PlayerStatus` | NEW, CASUAL, REGULAR, DEDICATED, WHALE, CHURNED, RETURNED |
| `MonetizationModel` | FREE_TO_PLAY, PREMIUM, SUBSCRIPTION, AD_SUPPORTED, BATTLE_PASS, HYBRID |
| `CurrencyType` | PREMIUM, SOFT, EVENT, SOCIAL, SEASONAL |
| `LootRarity` | COMMON, UNCOMMON, RARE, EPIC, LEGENDARY, MYTHIC |
| `BugSeverity` | CRITICAL(0), HIGH(1), MEDIUM(2), LOW(3), COSMETIC(4) |

---

## Examples

### Complete Game Design Session

```python
from agents.gaming.agent import *

# 1. Configure game
config = GameConfig(title="Dragon Quest Legends", genre=GameGenre.RPG)

# 2. Set up economy
economy = EconomyManager()
economy.register_currency("gold", CurrencyType.SOFT, 1_000_000)
economy.register_currency("gems", CurrencyType.PREMIUM, 50_000)

# 3. Define progression
prog = ProgressionSystem(max_level=100, base_exp=100, exp_growth=1.15)

# 4. Create loot tables
loot = LootSystem(seed=42)
chest = LootTable("chest_1", "Wooden Chest", pity_threshold=50, entries=[...])
loot.register_table(chest)

# 5. Balance combat
combat = CombatEngine(seed=42)
balance = combat.run_balance_simulation(warrior, mage, iterations=1000)
assert balance.balance_score > 0.6, "Combat is unbalanced"

# 6. Analyze players
analytics = EngagementAnalyzer()
summary = analytics.get_analytics_summary(players)

# 7. QA testing
qa = QAManager()
assert qa.release_readiness()["ready"], "Cannot ship with open critical bugs"
```

---

## Configuration

### Combat Engine
```python
combat = CombatEngine(seed=42)  # Reproducible results
```

### Progression System
```python
prog = ProgressionSystem(
    max_level=100,        # Maximum player level
    base_exp=100,         # Exp required for level 2
    exp_growth=1.15,      # Multiplier per level
)
```

### Loot System
```python
loot = LootSystem(seed=42)
# Configure pity threshold per table
table = LootTable("id", "name", pity_threshold=50, entries=[...])
```

---

## Best Practices

1. **Always seed random generators** for reproducible testing
2. **Run 1000+ simulations** for balance testing
3. **Monitor economy inflation** weekly during live ops
4. **Implement pity timers** for loot boxes
5. **Track player segments** to understand your audience
6. **Test difficulty curves** with real player data
7. **Maintain zero critical bugs** before release
8. **Balance for fun**, not for realism
9. **Provide transparent drop rates** to players
10. **Design ethical monetization** that adds value

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Balance always favors one side | Check base stats, review crit/dodge rates, run more simulations |
| Inflation too high | Add more sinks, reduce earn rates, add decay mechanics |
| Loot feels unfair | Implement pity timer, show rates, guarantee minimum rarity |
| Players churn early | Review onboarding, add tutorials, implement daily quests |
| QA has too many bugs | Prioritize by severity, automate testing, add CI/CD checks |
| Difficulty spikes | Smooth the curve, add catch-up mechanics, provide difficulty options |

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

---

## License

MIT License. See [LICENSE](../../LICENSE) for details.

---

## Files

- `agent.py` — Full implementation
- `ARCHITECTURE.md` — System architecture
- `GROK.md` — Agent identity and patterns
- `README.md` — This file
- `resources/` — Additional resources

---

*Design fun, balance with data, ship with confidence.*
