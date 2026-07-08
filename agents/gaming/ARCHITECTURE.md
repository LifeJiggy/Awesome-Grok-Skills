# Gaming Agent — System Architecture

## 1. Executive Summary

The Gaming Agent is a comprehensive game development toolkit providing combat simulation, economy management, progression systems, loot/gacha mechanics, player engagement analytics, QA testing, and difficulty scaling. It is designed as a modular, pluggable system suitable for game designers, developers, and live-ops teams.

---

## 2. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           GAMING AGENT                                    │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │   Combat     │  │   Economy    │  │  Progression │  │    Loot    │  │
│  │   Engine     │  │   Manager    │  │   System     │  │   System   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  Engagement  │  │     QA       │  │  Difficulty  │  │   Event    │  │
│  │  Analyzer    │  │   Manager    │  │   Scaler     │  │  Config    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │         Data Models (Player, Item, Quest, Bug, Level, Event)     │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Deep Dives

### 3.1 Combat Engine

Turn-based combat simulation with formula-driven damage calculation.

**Damage Formula:**
```
raw_damage = attack × skill_multiplier × element_modifier
crit_damage = raw_damage × crit_damage_multiplier (if crit)
defense_reduction = defense / (defense + 100)
after_defense = damage × (1 - defense_reduction)
block_modifier = 0.5 (if blocked)
final_damage = max(1, after_defense × block_modifier)
```

**Battle Flow:**
```
  ┌─────────┐     ┌─────────┐
  │ Attacker│     │Defender │
  └────┬────┘     └────┬────┘
       │                │
       ├── Dodge Check ─┤
       ├── Crit Check ──┤
       ├── Defense Calc ┤
       ├── Block Check ─┤
       │                │
       ▼                ▼
  ┌─────────────────────────┐
  │   Apply Damage / Heal   │
  └────────────┬────────────┘
               │
       ┌───────┴───────┐
       │ HP > 0?       │
       │ Yes → Next Turn│
       │ No  → Winner  │
       └───────────────┘
```

### 3.2 Economy Manager

In-game currency and pricing system with inflation tracking.

**Key Metrics:**
- Circulating supply: Total currency in player hands
- Faucet rate: Currency earned per hour
- Sink rate: Currency spent per hour
- Inflation rate: (earned - spent) / earned

**Health Thresholds:**
| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Inflation | < 5% | 5-15% | > 15% |
| Supply ratio | < 2x | 2-3x | > 3x |
| Sink/Faucet | 0.8-1.2 | 0.5-1.5 | < 0.5 or > 1.5 |

### 3.3 Progression System

Level curves, experience tables, and feature unlock gates.

**Experience Curve:**
```
exp_for_level(N) = base_exp × growth_rate^(N-1)
```

**Default Parameters:**
- base_exp = 100
- growth_rate = 1.15
- max_level = 100

**Unlock Gates:**
```
Level 10:  PvP Arena
Level 15:  Guild System
Level 20:  Crafting
Level 30:  Raids
Level 40:  Legendary Quests
Level 50:  Endgame Dungeons
```

### 3.4 Loot System

Gacha/loot box mechanics with pity timers and probability management.

**Pity System:**
- Counter increments each roll
- At threshold (default 50), guarantees legendary drop
- Counter resets after pity trigger

**Drop Rate Formula:**
```
roll = random() × luck_modifier
cumulative = 0
for entry in sorted_by_rarity:
    cumulative += entry.rate
    if roll <= cumulative:
        return entry
```

### 3.5 Engagement Analyzer

Player segmentation and churn prediction.

**Segmentation Rules:**
| Segment | Criteria |
|---------|----------|
| NEW | playtime < 5h |
| CASUAL | 5h ≤ playtime < 20h |
| REGULAR | 20h ≤ playtime < 100h |
| DEDICATED | playtime ≥ 100h |
| WHALE | total_spent > $100 |
| CHURNED | inactive > 30 days |

**Churn Risk Factors:**
- Inactive > 7 days (+0.3)
- Inactive > 14 days (+0.2)
- Low session count (+0.15)
- Non-paying engaged (+0.1)
- Stalled progression (+0.1)

### 3.6 QA Manager

Bug tracking with severity classification and release readiness.

**Severity Levels:**
- CRITICAL: Game-breaking, crashes, data loss
- HIGH: Major feature broken, significant impact
- MEDIUM: Noticeable issue, workaround exists
- LOW: Minor inconvenience
- COSMETIC: Visual-only, no gameplay impact

**Release Readiness Criteria:**
- Zero CRITICAL open bugs
- Zero HIGH open bugs
- All test cases passed

### 3.7 Difficulty Scaler

Adaptive difficulty based on player performance.

**Scaling Formula:**
```
level_diff = enemy_level - player_level
hp_mult = 1 + hp_scale × level_diff (capped at max_multiplier)
dmg_mult = 1 + damage_scale × level_diff (capped at max_multiplier)
```

---

## 4. Data Flow

```
  ┌──────────────────────────────────────────────────────┐
  │                GAME CONFIGURATION                     │
  │  Genre │ Platform │ Monetization │ Target Audience    │
  └────────────────────────┬─────────────────────────────┘
                           │
                           ▼
  ┌──────────────────────────────────────────────────────┐
  │                CORE SYSTEMS                           │
  │  Combat ←→ Economy ←→ Progression ←→ Loot            │
  └────────────────────────┬─────────────────────────────┘
                           │
                           ▼
  ┌──────────────────────────────────────────────────────┐
  │                PLAYER EXPERIENCE                      │
  │  Battles │ Rewards │ Leveling │ Items │ Quests        │
  └────────────────────────┬─────────────────────────────┘
                           │
                           ▼
  ┌──────────────────────────────────────────────────────┐
  │                ANALYTICS & QA                         │
  │  Engagement │ Retention │ Bugs │ Balance │ Economy    │
  └──────────────────────────────────────────────────────┘
```

---

## 5. Design Patterns

### Strategy Pattern
Different combat formulas, difficulty algorithms, and loot mechanics are swappable via configuration.

### Pity Timer Pattern
Guaranteed outcomes after N attempts — prevents extreme bad luck.

### Observer Pattern (Economy)
Economy state changes trigger health checks and alerts.

### State Machine (Player)
Player status transitions: NEW → CASUAL → REGULAR → DEDICATED / CHURNED.

---

## 6. Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Type System | Type hints + dataclasses |
| Random | random (seeded for reproducibility) |
| Collections | defaultdict, list |
| Logging | Python logging |
| Dependencies | Zero (stdlib only) |

---

## 7. Balance Tuning Framework

### Simulation Approach
1. Define two character builds with stats
2. Run N simulated battles (default 1000)
3. Measure win rates, average turns, damage distribution
4. Score balance: 1.0 = perfectly balanced, 0.0 = one-sided

### Tuning Levers
- Base stats (HP, ATK, DEF, SPD)
- Crit chance and damage multiplier
- Dodge and block rates
- Skill multipliers
- Element modifiers

---

## 8. Monetization Models

| Model | Description | Key Metrics |
|-------|-------------|-------------|
| Free-to-Play | Free download, IAP | ARPDAU, conversion rate, LTV |
| Premium | One-time purchase | Sales volume, review score |
| Subscription | Recurring payment | MRR, churn rate |
| Ad-Supported | Ad revenue | eCPM, ad views/session |
| Battle Pass | Seasonal content pass | Pass purchase rate, completion |
| Hybrid | Multiple models | Blended revenue |

---

## 9. Extension Points

### Custom Combat Formula
Override damage calculation by subclassing or providing a custom function.

### Custom Loot Table
Define new rarity tiers, drop rates, and pity mechanics.

### Custom Difficulty Curve
Provide scaling functions for HP, damage, and enemy behavior.

### Analytics Hooks
Subscribe to events: battle_complete, item_acquired, level_up, purchase, session_start/end.

---

## 10. Testing Strategy

### Balance Testing
- Simulate 10K+ battles per matchup
- Verify win rates within 45-55% for balanced characters
- Check TTK (time-to-kill) within acceptable range

### Economy Testing
- Simulate 30 days of earn/spend
- Verify inflation stays within ±5%
- Check sink/faucet ratio near 1.0

### Loot Testing
- Simulate 100K drops
- Verify rates match configured probabilities
- Confirm pity timer triggers correctly

### Progression Testing
- Verify exp curves produce reasonable time-to-max
- Check unlock gates are reachable
- Validate level-up rewards scale appropriately
