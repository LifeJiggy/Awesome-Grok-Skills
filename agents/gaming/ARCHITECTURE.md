# Gaming Agent — System Architecture

## 1. Executive Summary

The Gaming Agent is a comprehensive game development toolkit providing combat simulation, economy management, progression systems, loot/gacha mechanics, player engagement analytics, QA testing, and difficulty scaling. It is designed as a modular, pluggable system suitable for game designers, developers, and live-ops teams.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            GAMING AGENT                                      │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐      │
│  │   Combat     │  │   Economy    │  │  Progression │  │    Loot    │      │
│  │   Engine     │  │   Manager    │  │   System     │  │   System   │      │
│  │              │  │              │  │              │  │            │      │
│  │ • Damage calc│  │ • Currency   │  │ • Exp curves │  │ • Drop rate│      │
│  │ • Turn-based │  │ • Faucets    │  │ • Leveling   │  │ • Pity     │      │
│  │ • Balance    │  │ • Sinks      │  │ • Unlocks    │  │ • Rarity   │      │
│  │ • Simulate   │  │ • Inflation  │  │ • Rewards    │  │ • Expected │      │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘      │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐      │
│  │  Engagement  │  │     QA       │  │  Difficulty  │  │   Event    │      │
│  │  Analyzer    │  │   Manager    │  │   Scaler     │  │  Config    │      │
│  │              │  │              │  │              │  │            │      │
│  │ • Segment    │  │ • Bugs       │  │ • Adaptive   │  │ • Seasonal │      │
│  │ • Churn      │  │ • Severity   │  │ • Scaling    │  │ • Limited  │      │
│  │ • Score      │  │ • Release    │  │ • Balance    │  │ • Rewards  │      │
│  │ • Retention  │  │ • Test cases │  │ • Recommend  │  │ • Schedule │      │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │         Data Models (Player, Item, Quest, Bug, Level, Event)        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Deep Dives

### 2.1 Combat Engine

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

**Balance Simulation:**
- Runs N battles between two character builds (default: 1000)
- Measures win rates, average turns, damage distribution
- Balance score: 1.0 = perfectly balanced, 0.0 = one-sided
- Statistical significance check with configurable confidence

### 2.2 Economy Manager

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

**Currency Types:**
- SOFT: Earned through gameplay (gold, coins)
- PREMIUM: Purchased with real money (gems, crystals)
- EVENT: Time-limited seasonal currencies

### 2.3 Progression System

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

**Time-to-Max Estimation:**
- Calculates total experience from level 1 to max
- Estimates based on average earn rate per hour
- Accounts for diminishing returns at higher levels

### 2.4 Loot System

Gacha/loot box mechanics with pity timers and probability management.

**Pity System:**
- Counter increments each roll
- At threshold (default 50), guarantees legendary drop
- Counter resets after pity trigger
- Separate pity counters per rarity tier

**Drop Rate Formula:**
```
roll = random() × luck_modifier
cumulative = 0
for entry in sorted_by_rarity:
    cumulative += entry.rate
    if roll <= cumulative:
        return entry
```

**Rarity Tiers:**
| Rarity | Base Rate | Color |
|--------|-----------|-------|
| Common | 50% | Gray |
| Uncommon | 30% | Green |
| Rare | 15% | Blue |
| Epic | 4% | Purple |
| Legendary | 1% | Gold |

### 2.5 Engagement Analyzer

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

**Engagement Score Formula:**
```
score = (playtime_factor × 0.3) + (session_factor × 0.2) +
        (spending_factor × 0.2) + (social_factor × 0.15) +
        (progression_factor × 0.15)
```

### 2.6 QA Manager

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
- Performance benchmarks met
- Security audit passed

### 2.7 Difficulty Scaler

Adaptive difficulty based on player performance.

**Scaling Formula:**
```
level_diff = enemy_level - player_level
hp_mult = 1 + hp_scale × level_diff (capped at max_multiplier)
dmg_mult = 1 + damage_scale × level_diff (capped at max_multiplier)
```

**Adaptive Logic:**
- If win_rate > 80%: increase difficulty
- If win_rate < 40%: decrease difficulty
- Adjustments are gradual (±10% per session)
- Minimum difficulty floor to prevent trivial content

---

## 3. Data Flow

```
  ┌──────────────────────────────────────────────────────────────┐
  │                GAME CONFIGURATION                             │
  │  Genre │ Platform │ Monetization │ Target Audience            │
  └────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                CORE SYSTEMS                                   │
  │  Combat ←→ Economy ←→ Progression ←→ Loot                    │
  └────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                PLAYER EXPERIENCE                              │
  │  Battles │ Rewards │ Leveling │ Items │ Quests                │
  └────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                ANALYTICS & QA                                 │
  │  Engagement │ Retention │ Bugs │ Balance │ Economy            │
  └──────────────────────────────────────────────────────────────┘
```

---

## 4. Design Patterns

### Strategy Pattern
Different combat formulas, difficulty algorithms, and loot mechanics are swappable via configuration. Each system implements a common interface, allowing runtime method selection.

### Pity Timer Pattern
Guaranteed outcomes after N attempts — prevents extreme bad luck. Separate counters per rarity tier ensure fair distribution across all drop categories.

### Observer Pattern (Economy)
Economy state changes trigger health checks and alerts. When inflation crosses thresholds, recommendations are generated automatically.

### State Machine (Player)
Player status transitions: NEW → CASUAL → REGULAR → DEDICATED / CHURNED. Each transition triggers appropriate engagement strategies.

### Template Method (Quests)
Quest generation follows a common template with type-specific variations. The base flow (objective → requirements → rewards) is fixed; quest types override specific steps.

---

## 5. Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Type System | Type hints + dataclasses |
| Random | random (seeded for reproducibility) |
| Collections | defaultdict, list |
| Logging | Python logging |
| Dependencies | Zero (stdlib only) |
| Serialization | JSON-compatible dicts |
| Testing | pytest (optional) |

---

## 6. Balance Tuning Framework

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

### Balance Score Interpretation
| Score | Interpretation | Action |
|-------|---------------|--------|
| 0.9-1.0 | Excellent | Ship as-is |
| 0.7-0.9 | Good | Minor tuning |
| 0.5-0.7 | Needs work | Significant adjustments |
| 0.0-0.5 | Broken | Major rebalance needed |

---

## 7. Monetization Models

| Model | Description | Key Metrics |
|-------|-------------|-------------|
| Free-to-Play | Free download, IAP | ARPDAU, conversion rate, LTV |
| Premium | One-time purchase | Sales volume, review score |
| Subscription | Recurring payment | MRR, churn rate |
| Ad-Supported | Ad revenue | eCPM, ad views/session |
| Battle Pass | Seasonal content pass | Pass purchase rate, completion |
| Hybrid | Multiple models | Blended revenue |

### Monetization Ethics
- No pay-to-win mechanics
- Clear odds for loot boxes
- Spending caps or pity systems
- Free players can access all content
- No dark patterns or manipulation

---

## 8. Extension Points

### Custom Combat Formula
Override damage calculation by subclassing or providing a custom function. Implement the CombatFormula interface for full control.

### Custom Loot Table
Define new rarity tiers, drop rates, and pity mechanics. Loot tables are JSON-configurable for easy iteration.

### Custom Difficulty Curve
Provide scaling functions for HP, damage, and enemy behavior. Support adaptive and static difficulty modes.

### Analytics Hooks
Subscribe to events: battle_complete, item_acquired, level_up, purchase, session_start/end. Events are emitted for real-time pipeline integration.

### Custom Player Segments
Define new segmentation rules beyond the built-in set. Custom segments can trigger personalized engagement strategies.

---

## 9. Testing Strategy

### Balance Testing
- Simulate 10K+ battles per matchup
- Verify win rates within 45-55% for balanced characters
- Check TTK (time-to-kill) within acceptable range (3-8 turns)
- Verify no dominant strategy exists

### Economy Testing
- Simulate 30 days of earn/spend
- Verify inflation stays within ±5%
- Check sink/faucet ratio near 1.0
- Test for currency exploits

### Loot Testing
- Simulate 100K drops
- Verify rates match configured probabilities (within 2% tolerance)
- Confirm pity timer triggers correctly
- Test edge cases (first roll, after pity trigger)

### Progression Testing
- Verify exp curves produce reasonable time-to-max
- Check unlock gates are reachable
- Validate level-up rewards scale appropriately
- Test catch-up mechanics

### QA Testing
- Verify bug severity classification accuracy
- Test release readiness criteria enforcement
- Validate test case generation coverage
- Check audit trail completeness

---

## 10. Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Combat simulation (1 battle) | < 5ms | Single battle |
| Balance simulation (1000 battles) | < 500ms | Statistical significance |
| Economy health check | < 10ms | All currencies |
| Loot roll | < 1ms | Single roll |
| Player segmentation | < 50ms | 10K players |
| Engagement score | < 5ms | Single player |
| Difficulty scaling | < 2ms | Single encounter |
| QA release check | < 20ms | All criteria |

---

## 11. Detailed Component Internals

### 11.1 Combat Engine Internals

**Damage Calculation Pipeline:**
```
  1. Base Damage = attack × skill_multiplier
  2. Element Modifier = base_damage × element_modifier
  3. Crit Check = random() < crit_chance
  4. If Crit: damage = element_modifier × crit_damage_multiplier
  5. Defense Reduction = defense / (defense + 100)
  6. After Defense = damage × (1 - defense_reduction)
  7. Block Check = random() < block_chance
  8. If Block: damage = after_defense × 0.5
  9. Final Damage = max(1, damage)
```

**Speed and Turn Order:**
```
  turn_order = sorted(characters, key=lambda c: c.speed, reverse=True)
  for character in turn_order:
      if character.hp > 0:
          execute_turn(character)
```

**Balance Score Calculation:**
```
  balance_score = 1.0 - abs(win_rate_a - 0.5) × 2
  # 1.0 = perfectly balanced (50/50)
  # 0.0 = completely one-sided (100/0)
```

### 11.2 Economy Manager Internals

**Inflation Calculation:**
```
  inflation_rate = (total_earned - total_spent) / total_earned
```

**Health Check Logic:**
```
  health_check():
      issues = []
      for currency in currencies:
          if currency.inflation > 0.15:
              issues.append(f"{currency.name}: High inflation")
          if currency.sink_faucet_ratio < 0.5:
              issues.append(f"{currency.name}: Low sink ratio")
          if currency.sink_faucet_ratio > 1.5:
              issues.append(f"{currency.name}: High sink ratio")
      return {"healthy": len(issues) == 0, "issues": issues}
```

**Currency Flow Tracking:**
```
  earn(currency, amount, source):
      currency.supply += amount
      currency.total_earned += amount
      log_transaction("earn", currency, amount, source)
  
  spend(currency, amount, sink):
      if currency.supply >= amount:
          currency.supply -= amount
          currency.total_spent += amount
          log_transaction("spend", currency, amount, sink)
          return True
      return False
```

### 11.3 Progression System Internals

**Experience Curve Formula:**
```
  exp_for_level(N) = base_exp × growth_rate^(N-1)
  total_exp_to_level(from, to) = Σ exp_for_level(i) for i in range(from, to)
```

**Time-to-Max Calculation:**
```
  total_exp = total_exp_to_level(1, max_level)
  hours_to_max = total_exp / exp_per_hour
```

**Unlock Gate Logic:**
```
  get_unlock_gates(player_level):
      gates = []
      for gate in defined_gates:
          gates.append({
              "feature": gate.feature,
              "level": gate.required_level,
              "unlocked": player_level >= gate.required_level
          })
      return gates
```

### 11.4 Loot System Internals

**Drop Rate Calculation:**
```
  roll = random() × luck_modifier
  cumulative = 0
  for entry in sorted_by_rarity_descending:
      cumulative += entry.rate
      if roll <= cumulative:
          return entry
  return last_entry  # Fallback
```

**Pity Timer Logic:**
```
  open_loot(table_id):
      table = get_table(table_id)
      pity_counter[table_id] += 1
      
      if pity_counter[table_id] >= table.pity_threshold:
          # Guarantee highest rarity
          result = guaranteed_legendary_drop(table)
          pity_counter[table_id] = 0
          result.pity_triggered = True
          return result
      
      # Normal roll
      return normal_roll(table)
```

**Expected Value Calculation:**
```
  calculate_expected_value(table_id, rolls):
      distribution = {rarity: 0 for rarity in rarities}
      for _ in range(rolls):
          drop = normal_roll(table)
          distribution[drop.rarity] += 1
      return {r: count/rolls for r, count in distribution.items()}
```

### 11.5 Engagement Analyzer Internals

**Player Segmentation Logic:**
```
  segment_players(players):
      segments = defaultdict(list)
      for player in players:
          if player.total_spent > 100:
              segments[WHALE].append(player)
          elif player.playtime_hours < 5:
              segments[NEW].append(player)
          elif player.playtime_hours < 20:
              segments[CASUAL].append(player)
          elif player.playtime_hours < 100:
              segments[REGULAR].append(player)
          else:
              segments[DEDICATED].append(player)
      return segments
```

**Churn Risk Calculation:**
```
  predict_churn_risk(player):
      risk_score = 0.0
      factors = []
      
      if player.days_inactive > 7:
          risk_score += 0.3
          factors.append("inactive_7plus_days")
      if player.days_inactive > 14:
          risk_score += 0.2
          factors.append("inactive_14plus_days")
      if player.session_count < 10:
          risk_score += 0.15
          factors.append("low_session_count")
      if player.total_spent == 0 and player.playtime_hours > 10:
          risk_score += 0.1
          factors.append("non_paying_engaged")
      
      risk_level = "low" if risk_score < 0.3 else "medium" if risk_score < 0.6 else "high"
      return {"risk_score": risk_score, "risk_level": risk_level, "factors": factors}
```

**Engagement Score Formula:**
```
  score = (playtime_factor × 0.3) + (session_factor × 0.2) +
          (spending_factor × 0.2) + (social_factor × 0.15) +
          (progression_factor × 0.15)
  
  # Each factor normalized to 0-100
  playtime_factor = min(100, playtime_hours)
  session_factor = min(100, session_count × 2)
  spending_factor = min(100, total_spent / 5)
  social_factor = min(100, friend_count × 10)
  progression_factor = min(100, level × 2)
```

### 11.6 QA Manager Internals

**Release Readiness Logic:**
```
  release_readiness():
      critical_bugs = count_bugs(severity=CRITICAL, status=OPEN)
      high_bugs = count_bugs(severity=HIGH, status=OPEN)
      test_cases_passed = all_tests_passed()
      
      ready = critical_bugs == 0 and high_bugs == 0 and test_cases_passed
      
      return {
          "ready": ready,
          "critical_bugs": critical_bugs,
          "high_bugs": high_bugs,
          "test_cases_passed": test_cases_passed,
          "recommendation": "Ready to ship" if ready else "Fix blocking issues"
      }
```

### 11.7 Difficulty Scaler Internals

**Scaling Formula:**
```
  level_diff = enemy_level - player_level
  hp_mult = 1 + hp_scale × level_diff
  dmg_mult = 1 + damage_scale × level_diff
  
  # Cap at max_multiplier
  hp_mult = min(hp_mult, max_multiplier)
  dmg_mult = min(dmg_mult, max_multiplier)
  
  scaled_hp = base_hp × hp_mult
  scaled_dmg = base_dmg × dmg_mult
```

**Adaptive Difficulty Logic:**
```
  calculate_recommended_level(player_stats):
      win_rate = player_stats["win_rate"]
      avg_turns = player_stats["avg_turns"]
      current_level = player_stats["current_level"]
      
      if win_rate > 0.8:
          return current_level + 2  # Increase difficulty
      elif win_rate < 0.4:
          return max(1, current_level - 2)  # Decrease difficulty
      else:
          return current_level  # Maintain
```

---

## 12. Error Handling Strategy

### 12.1 Input Validation

| Component | Validation | Error Type |
|-----------|------------|------------|
| CombatEngine | Positive stats, valid levels | ValueError |
| EconomyManager | Positive amounts, valid currency | ValueError |
| ProgressionSystem | Positive level, valid exp | ValueError |
| LootSystem | Valid table_id, positive count | ValueError |
| EngagementAnalyzer | Valid player data | ValueError |
| QAManager | Non-empty title, valid severity | ValueError |
| DifficultyScaler | Positive base values | ValueError |

### 12.2 Graceful Degradation

- **Invalid stats**: Use defaults with warning
- **Missing currency**: Create with zero balance
- **Invalid loot table**: Return empty drops
- **Insufficient data**: Return partial analytics

---

## 13. Testing Architecture

### 13.1 Test Categories

| Category | Coverage | Tools |
|----------|----------|-------|
| Unit Tests | Individual methods | pytest |
| Integration Tests | System interaction | pytest |
| Simulation Tests | Balance verification | pytest |
| Statistical Tests | Drop rate validation | scipy |

### 13.2 Test Data Strategy

- **Synthetic characters**: Known stat distributions
- **Simulated players**: Varied engagement patterns
- **Edge cases**: Level 1 vs max, zero stats, empty inventories

---

## 14. Configuration Management

### 14.1 Default Configuration

```python
DEFAULT_CONFIG = {
    "combat": {
        "seed": None,
        "crit_damage_multiplier": 1.5,
        "block_damage_reduction": 0.5,
        "defense_factor": 100,
    },
    "economy": {
        "inflation_warning": 0.05,
        "inflation_critical": 0.15,
        "sink_faucet_healthy_range": (0.8, 1.2),
    },
    "progression": {
        "max_level": 100,
        "base_exp": 100,
        "exp_growth": 1.15,
    },
    "loot": {
        "default_pity_threshold": 50,
        "luck_modifier_max": 2.0,
    },
    "difficulty": {
        "hp_scale": 0.15,
        "damage_scale": 0.10,
        "max_multiplier": 3.0,
        "adaptive_threshold_high": 0.8,
        "adaptive_threshold_low": 0.4,
    },
}
```

---

## 15. Logging and Monitoring

### 15.1 Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Damage calculations, loot rolls |
| INFO | Battle completion, level ups, purchases |
| WARNING | Balance issues, inflation alerts |
| ERROR | Invalid inputs, calculation failures |

### 15.2 Metrics to Monitor

- Battle simulation performance
- Economy health metrics
- Player engagement trends
- Loot drop distributions
- QA bug resolution rates

---

## 16. Future Roadmap

### 16.1 Short-term Enhancements

- Additional combat formulas (cooldowns, mana)
- More loot mechanics (crafting, trading)
- Enhanced analytics (cohort analysis)
- Export capabilities (CSV, JSON)

### 16.2 Medium-term Enhancements

- Real-time multiplayer simulation
- AI-controlled opponents
- Procedural content generation
- Machine learning for balance

### 16.3 Long-term Vision

- Unity/Unreal integration
- Live operations dashboard
- Cross-platform player data
- Predictive analytics

---

## 17. Comparison with Industry Tools

| Feature | Gaming Agent | Unity | Unreal | Custom |
|---------|--------------|-------|--------|--------|
| Dependencies | Zero | Engine | Engine | Varies |
| Combat Sim | Built-in | Via scripts | Via blueprints | Custom |
| Economy | Built-in | Via plugins | Via plugins | Custom |
| Loot | Built-in | Via plugins | Via plugins | Custom |
| Analytics | Built-in | Via services | Via services | Custom |
| Cost | Free | Runtime fee | Runtime fee | Dev time |
| Learning Curve | Low | Medium | High | Varies |

---

**See Also**: [GROK.md](./GROK.md) for agent identity and capabilities,
[README.md](./README.md) for quick start and API reference.