---
name: "fan-engagement"
category: "sports-tech"
version: "1.0.0"
tags: ["sports-tech", "fan-engagement", "fantasy-sports", "sentiment-analysis"]
---

# Fan Engagement — Fantasy Analytics, Sentiment Tracking & Interactive Experiences

## Overview

Fan engagement in sports technology represents the intersection of data science, behavioral psychology, and digital platform engineering designed to deepen the connection between fans and their favorite teams, players, and leagues. This module provides a comprehensive toolkit for building and optimizing fan-facing products — from fantasy sports analytics engines to real-time second-screen experiences, sentiment analysis pipelines, and gamification frameworks. The global sports fan engagement market is projected to reach $18.5 billion by 2027, driven by the shift from passive viewership to interactive participation.

The fantasy sports analytics subsystem provides projection models, trade value calculators, and lineup optimization engines across major fantasy platforms (ESPN, Yahoo, FanDuel, DraftKings). These models consume performance analytics outputs and apply platform-specific scoring rules, salary constraints, and roster requirements to produce actionable fantasy advice. The trade value calculator uses a combination of rest-of-season projections, age curves, injury risk adjustments, and schedule strength to produce dynamic trade values that update weekly.

The sentiment analysis pipeline processes social media streams (Twitter/X, Reddit, Instagram, TikTok) using fine-tuned transformer models to track real-time fan sentiment during matches, identify viral moments, detect emerging controversies, and measure brand perception shifts. The system supports multi-lingual sentiment detection with sport-specific lexicons that understand domain terms like "red card," "hat trick," or "choke" in their sporting context rather than literal interpretations.

The live match second-screen experience layer provides real-time stats, interactive polls, prediction markets, and AR overlays synchronized with the broadcast timeline. This module handles the complex event-driven architecture required to deliver sub-second updates to millions of concurrent users while maintaining data consistency across distributed caching layers.

## Core Capabilities

- **Fantasy Projection Models**: Platform-specific (ESPN, Yahoo, FanDuel, DraftKings) player projection engines with position-specific scoring, matchup adjustments, and rest-of-season valuations
- **Lineup Optimization**: Mixed-integer programming optimizer for daily fantasy lineups maximizing expected points under salary cap and roster constraints with ownership correlation adjustments
- **Trade Value Calculator**: Dynamic player trade valuations incorporating age curves, injury risk, schedule strength, and league context with visual trade fairness analysis
- **Fan Sentiment Analysis**: Fine-tuned transformer models for real-time sentiment tracking across social platforms with sport-specific lexicon support and multi-lingual capabilities
- **Live Second-Screen Platform**: Event-driven real-time stats dashboard synchronized with broadcast timeline, supporting interactive elements (polls, predictions, trivia) with sub-second delivery
- **Gamification Engine**: Configurable achievement, streak, and reward system for driving recurring fan engagement across digital properties
- **Dynamic Ticket Pricing**: Demand-responsive pricing model incorporating opponent draw, team performance, weather, day-of-week, and historical demand curves
- **AR/VR Experience Framework**: Template-based augmented reality overlay system for live match visualization including player stats, tactical heatmaps, and trajectory projections

## Usage Examples

### Fantasy Player Projection

```python
from fan_engagement import FantasyEngine, Platform, Position

engine = FantasyEngine(platform=Platform.DRAFTKINGS)

# Generate weekly projections for NFL
projections = engine.project_players(
    sport="nfl",
    week=14,
    include_injury_status=True,
    include_weather_adjustments=True,
)

for player in projections.top_players(position=Position.QUARTERBACK, n=5):
    print(f"{player.name:25s} | "
          f"Proj Pts: {player.projected_points:.1f} | "
          f"Salary: ${player.salary:,} | "
          f"Value: {player.points_per_dollar:.4f} | "
          f"Ownership: {player.projected_ownership:.1%}")

# Optimize a lineup
lineup = engine.optimize_lineup(
    budget=50000,
    roster_slots=[
        (Position.QUARTERBACK, 1),
        (Position.RUNNING_BACK, 2),
        (Position.WIDE_RECEIVER, 3),
        (Position.TIGHT_END, 1),
        (Position.FLEX, 1),
        (Position.DEFENSE, 1),
    ],
    optimization_metric="expected_points",
    correlation_pairs=[("QB", "WR1")],  # stack correlated players
)
print(f"Optimized lineup expected points: {lineup.expected_points:.1f}")
print(f"Total salary: ${lineup.total_salary:,}")
```

### Fan Sentiment Tracking

```python
from fan_engagement import SentimentAnalyzer, Platform, TimeWindow

analyzer = SentimentAnalyzer(
    platforms=[Platform.TWITTER, Platform.REDDIT],
    languages=["en", "es", "pt"],
    sport_lexicon="football_v3",
)

# Track sentiment during a live match
stream = analyzer.track_live(
    match_id="match_2024_final",
    keywords=["#ChampionsLeague", "team_a", "team_b"],
    time_window=TimeWindow(start_minutes=-30, end_minutes=30),
)

for event in stream.sentiment_events:
    print(f"[{event.timestamp}] {event.trigger}")
    print(f"  Sentiment: {event.sentiment_score:+.2f} "
          f"({event.positive_pct:.0%} pos, {event.negative_pct:.0%} neg)")
    print(f"  Volume: {event.mention_count:,} mentions")
    print(f"  Top phrase: '{event.top_phrase}'")
    print(f"  Viral potential: {event.viral_score:.0f}/100")
    print()

# Get post-match summary
summary = analyzer.match_summary("match_2024_final")
print(f"Overall sentiment: {summary.avg_sentiment:+.2f}")
print(f"Peak positive moment: {summary.peak_positive_moment}")
print(f"Peak negative moment: {summary.peak_negative_moment}")
print(f"Brand impact: {summary.brand_impact_score:+.1f}")
```

### Dynamic Ticket Pricing

```python
from fan_engagement import TicketPricingEngine, Venue

engine = TicketPricingEngine(
    venue=Venue(name="Stadium_A", capacity=60000),
    pricing_model="demand_response_v3",
    min_margin=0.15,
    max_price_multiplier=5.0,
)

# Calculate optimal prices for an upcoming match
pricing = engine.calculate_prices(
    match_id="match_2024_final",
    opponent="rival_team",
    days_until_match=14,
    current_inventory=45000,  # tickets remaining
    historical_demand_curve=engine.load_demand_curve("league_finals"),
)

for zone in pricing.zones:
    print(f"{zone.name:20s} | "
          f"Base: ${zone.base_price:.0f} | "
          f"Optimal: ${zone.optimal_price:.0f} | "
          f"Multiplier: {zone.multiplier:.1f}x | "
          f"Projected sell-through: {zone.projected_sell_through:.0%}")

# Check price elasticity
elasticity = engine.price_elasticity_analysis(
    match_id="match_2024_final",
    zone="premium_lower",
    price_range=(80, 200),
)
print(f"Price elasticity: {elasticity.coefficient:.2f}")
print(f"Revenue-maximizing price: ${elasticity.optimal_price:.0f}")
```

### Live Second-Screen Experience

```python
from fan_engagement import SecondScreen, InteractiveElement

app = SecondScreen(
    match_id="match_2024_final",
    broadcast_sync=True,
    latency_target_ms=500,
)

# Register interactive elements
app.register_element(InteractiveElement.poll(
    question="Who will score the next goal?",
    options=["Player A", "Player B", "Player C", "No goal next 10 min"],
    duration_seconds=60,
    min_votes=100,
))

app.register_element(InteractiveElement.prediction(
    question="Final score prediction?",
    options=["2-1", "1-1", "3-0", "0-1"],
    point_value=50,
))

# Stream real-time updates
for update in app.updates():
    if update.type == "goal":
        print(f"GOAL! {update.data['scorer']} scores!")
        print(f"Updated xG: {update.data['xg_after']:.2f}")
    elif update.type == "poll_result":
        print(f"Poll '{update.data['question']}' winner: {update.data['winner']}")
        print(f"  Total votes: {update.data['total_votes']:,}")
```

## Best Practices

1. **Respect rate limits on social media APIs** — Twitter/X, Reddit, and Instagram all enforce strict rate limits. Implement exponential backoff, request queuing, and respect `Retry-After` headers to maintain API access.

2. **Handle timezone and locale correctly in live experiences** — fans worldwide watch the same match but at different local times. Always display times in the user's configured timezone and format numbers according to their locale.

3. **Implement content moderation on user-generated content** — real-time fan interactions (chat, polls, predictions) can be exploited for spam or abuse. Deploy automated moderation with human fallback for flagged content.

4. **Optimize for mobile-first delivery** — over 80% of second-screen usage occurs on mobile devices. Design data payloads for low-bandwidth conditions and prioritize visual clarity over information density.

5. **Calibrate fantasy projections against platform-specific scoring** — a projection model tuned for ESPN scoring will produce incorrect advice on FanDuel. Always validate projection accuracy against the target platform's rules.

6. **Use A/B testing for gamification mechanics** — engagement features like streaks, achievements, and rewards have complex behavioral effects. Test variations with controlled user cohorts before broad deployment.

7. **Implement data freshness guarantees** — stale statistics in a live experience destroy credibility. Define maximum acceptable staleness per data type and fail gracefully when freshness SLAs are breached.

8. **Balance monetization with user experience** — dynamic pricing and premium content should enhance, not degrade, the fan experience. Monitor churn metrics alongside revenue metrics to detect exploitation thresholds.

## Related Modules

- [performance-analytics](../performance-analytics/GROK.md) — Provides player and team statistics that feed fantasy projections and fan-facing analytics
- [game-strategy](../game-strategy/GROK.md) — Supplies tactical insights for interactive match commentary and fan education content
- [wearable-tech](../wearable-tech/GROK.md) — Streams live player tracking data for real-time second-screen visualizations
- [injury-prevention](../injury-prevention/GROK.md) — Provides player availability data that affects fantasy projections and fan expectations

## Advanced Configuration

The fan engagement module provides extensive configuration for fantasy engines, sentiment analysis, dynamic pricing, and second-screen experiences.

### Fantasy Engine Configuration

```yaml
# config/fan_engagement.yaml
fantasy_engine:
  platforms:
    draftkings:
      salary_cap: 50000
      roster_slots:
        quarterback: 1
        running_back: 2
        wide_receiver: 3
        tight_end: 1
        flex: 1
        defense: 1
      scoring:
        passing_yards: 0.04
        passing_td: 4
        rushing_yards: 0.1
        rushing_td: 6
        receiving_yards: 0.1
        receiving_td: 6
        reception: 1
        fumble_lost: -2
        interception_thrown: -1

    fanduel:
      salary_cap: 60000
      roster_slots:
        quarterback: 1
        running_back: 2
        wide_receiver: 3
        tight_end: 1
        flex: 1
        defense: 1

  projection_models:
    rest_of_season:
      min_games_played: 3
      injury_adjustment: true
      schedule_adjustment: true
      recency_weight_decay: 0.95

    weekly:
      matchup_adjustment: true
      weather_adjustment: true
      home_away_split: true
      recency_window_games: 4

  lineup_optimizer:
    algorithm: "mixed_integer_programming"
    solver: "glpk"
    max_computation_seconds: 30
    correlation_stacking: true
    ownership_contrarian: false
    min_salary_usage: 0.95
```

### Sentiment Analysis Configuration

```yaml
sentiment_analysis:
  models:
    primary:
      type: "transformer"
      name: "sports-sentiment-v3"
      max_sequence_length: 512
      device: "cuda"
    fallback:
      type: "lexicon"
      lexicon_path: "lexicons/sports_v2.csv"

  platforms:
    twitter:
      api_key: "${TWITTER_API_KEY}"
      api_secret: "${TWITTER_API_SECRET}"
      rate_limit_per_15min: 900
      stream_reconnect_delay: 5
      languages: ["en", "es", "pt", "fr", "de"]

    reddit:
      client_id: "${REDDIT_CLIENT_ID}"
      client_secret: "${REDDIT_CLIENT_SECRET}"
      subreddits:
        - "soccer"
        - "football"
        - "nba"
        - "nfl"
        - "fantasyfootball"
      rate_limit_per_minute: 60

  sport_lexicons:
    - name: "football_v3"
      terms:
        positive: ["hat trick", "screamer", "world class", "clinical finish"]
        negative: ["choke", "bottle", "red card", "penalty miss", "own goal"]
        neutral: ["substitution", "corner kick", "free kick", "halftime"]

  output:
    sentiment_granularity: "sentence"
    entity_level_sentiment: true
    aspect_sentiment: true
```

### Dynamic Ticket Pricing Configuration

```yaml
ticket_pricing:
  model: "demand_response_v3"
  optimization_target: "revenue_maximization"

  constraints:
    min_margin: 0.15
    max_price_multiplier: 5.0
    min_price_floor: 10.0
    price_change_cooldown_hours: 24

  demand_factors:
    opponent_draw_weight: 0.30
    team_performance_weight: 0.25
    day_of_week_weight: 0.15
    weather_weight: 0.10
    historical_demand_weight: 0.20

  zones:
    - name: "premium_lower"
      base_price: 120
      capacity: 5000
    - name: "premium_upper"
      base_price: 95
      capacity: 8000
    - name: "standard_lower"
      base_price: 65
      capacity: 15000
    - name: "standard_upper"
      base_price: 45
      capacity: 20000
    - name: "nosebleed"
      base_price: 25
      capacity: 12000
```

## Architecture Patterns

### Event-Driven Fan Interaction

The fan engagement platform uses an event-driven architecture to handle millions of concurrent fan interactions:

```
Fan Mobile App
      │
      ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   API        │───▶│   Event     │───▶│   Stream    │
│   Gateway    │    │   Router    │    │   Processor │
└─────────────┘    └──────┬──────┘    └──────┬──────┘
                          │                   │
          ┌───────────────┼───────────────┐   │
          ▼               ▼               ▼   │
   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
   │  Fantasy    │ │  Sentiment  │ │  Gamification│
   │  Engine     │ │  Analyzer   │ │  Engine      │
   └─────────────┘ └─────────────┘ └─────────────┘
```

### CQRS for Fan Data

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FanCommand:
    command_id: str
    user_id: str
    command_type: str  # "join_contest", "submit_lineup", "vote_poll"
    payload: dict
    timestamp: datetime

@dataclass
class FanQuery:
    user_id: str
    query_type: str  # "lineup_status", "contest_rank", "sentiment_trend"
    filters: dict

class FanCommandHandler:
    def __init__(self, event_store, projection_builder):
        self.event_store = event_store
        self.projections = projection_builder

    def handle_join_contest(self, command: FanCommand):
        event = ContestJoinedEvent(
            user_id=command.user_id,
            contest_id=command.payload["contest_id"],
            entry_fee=command.payload["entry_fee"],
            timestamp=command.timestamp,
        )
        self.event_store.append(event)
        self.projections.update(event)

class FanQueryHandler:
    def __init__(self, projection_store):
        self.projections = projection_store

    def handle_lineup_status(self, query: FanQuery) -> dict:
        return self.projections.get_user_lineup(
            user_id=query.user_id,
            contest_id=query.filters.get("contest_id"),
        )
```

### Real-Time Fan Notification System

```python
import asyncio
from typing import Dict, Set

class FanNotificationHub:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.subscriptions: Dict[str, Set[str]] = {}

    async def subscribe(self, user_id: str, event_types: list):
        for event_type in event_types:
            key = f"fan_notifications:{event_type}"
            await self.redis.sadd(key, user_id)

    async def publish(self, event_type: str, notification: dict):
        key = f"fan_notifications:{event_type}"
        subscribers = await self.redis.smembers(key)
        for user_id in subscribers:
            await self._send_to_user(user_id, notification)

    async def _send_to_user(self, user_id: str, notification: dict):
        channel = f"user:{user_id}:notifications"
        await self.redis.publish(channel, json.dumps(notification))
```

### Gamification State Machine

```python
from enum import Enum
from dataclasses import dataclass

class AchievementState(Enum):
    LOCKED = "locked"
    IN_PROGRESS = "in_progress"
    UNLOCKED = "unlocked"
    EXPIRED = "expired"

@dataclass
class Achievement:
    achievement_id: str
    name: str
    description: str
    requirement: dict
    reward_points: int
    state: AchievementState = AchievementState.LOCKED
    progress: float = 0.0

class GamificationEngine:
    def __init__(self, achievement_definitions: list):
        self.achievements = {a.achievement_id: a for a in achievement_definitions}

    def update_progress(self, user_id: str, event_type: str, event_data: dict):
        for achievement in self.achievements.values():
            if achievement.state == AchievementState.LOCKED:
                if self._check_trigger(achievement, event_type, event_data):
                    achievement.state = AchievementState.IN_PROGRESS

            if achievement.state == AchievementState.IN_PROGRESS:
                progress = self._calculate_progress(achievement, user_id, event_data)
                achievement.progress = min(1.0, achievement.progress + progress)
                if achievement.progress >= 1.0:
                    achievement.state = AchievementState.UNLOCKED
                    self._award_points(user_id, achievement.reward_points)
```

## Integration Guide

### Fantasy Platform API Integration

```python
class DraftKingsAPI:
    BASE_URL = "https://api.draftkings.com"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def get_contests(self, sport: str) -> List[dict]:
        response = self.session.get(
            f"{self.BASE_URL}/contests",
            params={"sport": sport, "status": "upcoming"}
        )
        return response.json()["contests"]

    def get_player_pool(self, contest_id: str) -> List[dict]:
        response = self.session.get(
            f"{self.BASE_URL}/contests/{contest_id}/players"
        )
        return response.json()["players"]

    def submit_lineup(self, contest_id: str, lineup: dict) -> dict:
        response = self.session.post(
            f"{self.BASE_URL}/contests/{contest_id}/lineups",
            json=lineup
        )
        return response.json()
```

### Social Media Integration

```python
import tweepy

class TwitterFanSentiment:
    def __init__(self, api_credentials: dict):
        auth = tweepy.OAuthHandler(
            api_credentials["consumer_key"],
            api_credentials["consumer_secret"]
        )
        auth.set_access_token(
            api_credentials["access_token"],
            api_credentials["access_token_secret"]
        )
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def stream_sentiment(self, keywords: list, callback):
        class SentimentStreamListener(tweepy.StreamingClient):
            def __init__(self, analyzer, callback):
                super().__init__(bearer_token=analyzer.bearer_token)
                self.analyzer = analyzer
                self.callback = callback

            def on_tweet(self, tweet):
                sentiment = self.analyzer.analyze(tweet.text)
                self.callback({
                    "text": tweet.text,
                    "sentiment": sentiment,
                    "user": tweet.author.screen_name,
                    "created_at": tweet.created_at,
                })

        stream = SentimentStreamListener(self, callback)
        for keyword in keywords:
            stream.add_rules(tweepy.StreamRule(keyword))
        stream.filter()
```

### Broadcast Integration

```python
class BroadcastIntegration:
    def __init__(self, graphics_api_url: str):
        self.graphics_url = graphics_api_url

    def push_live_stats(self, match_id: str, stats: dict):
        payload = {
            "type": "live_stats",
            "match_id": match_id,
            "data": {
                "possession": stats["possession"],
                "xg": {"home": stats["home_xg"], "away": stats["away_xg"]},
                "shots": {"home": stats["home_shots"], "away": stats["away_shots"]},
                "top_performer": stats["mvp"]["name"],
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
        requests.post(f"{self.graphics_url}/overlays", json=payload)

    def push_fantasy_update(self, player_id: str, points: float):
        payload = {
            "type": "fantasy_points",
            "player_id": player_id,
            "points": points,
        }
        requests.post(f"{self.graphics_url}/fantasy", json=payload)
```

## Performance Optimization

### Caching Strategies

```python
from functools import lru_cache
import redis

class FanEngagementCache:
    def __init__(self, redis_client):
        self.redis = redis_client

    def cache_projections(self, sport: str, week: int, projections: dict, ttl: int = 300):
        key = f"projections:{sport}:{week}"
        self.redis.setex(key, ttl, json.dumps(projections))

    def get_cached_projections(self, sport: str, week: int) -> Optional[dict]:
        key = f"projections:{sport}:{week}"
        cached = self.redis.get(key)
        return json.loads(cached) if cached else None

    def cache_sentiment(self, match_id: str, sentiment: dict, ttl: int = 60):
        key = f"sentiment:{match_id}"
        self.redis.setex(key, ttl, json.dumps(sentiment))
```

### Parallel Contest Processing

```python
from concurrent.futures import ProcessPoolExecutor
from typing import List

class ParallelContestProcessor:
    def __init__(self, num_workers: int = 8):
        self.executor = ProcessPoolExecutor(max_workers=num_workers)

    def process_contests_batch(self, contests: List[dict]) -> List[dict]:
        futures = []
        for contest in contests:
            future = self.executor.submit(self._process_contest, contest)
            futures.append(future)

        results = []
        for future in futures:
            results.append(future.result(timeout=60))
        return results
```

### WebSocket Connection Pooling

```python
import asyncio
from typing import Dict, Set

class WebSocketPool:
    def __init__(self, max_connections: int = 10000):
        self.connections: Dict[str, Set] = {}
        self.max_connections = max_connections

    async def add_connection(self, user_id: str, websocket):
        if len(self.connections) >= self.max_connections:
            await self._evict_oldest()
        if user_id not in self.connections:
            self.connections[user_id] = set()
        self.connections[user_id].add(websocket)

    async def broadcast(self, user_id: str, message: dict):
        if user_id in self.connections:
            dead = set()
            for ws in self.connections[user_id]:
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.add(ws)
            self.connections[user_id] -= dead
```

## Security Considerations

### User Authentication

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class FanAuthMiddleware:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    async def verify_token(self, token: str = Depends(oauth2_scheme)) -> dict:
        try:
            payload = self.auth_service.verify_jwt(token)
            if "fan:engage" not in payload.get("scopes", []):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return payload
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
```

### Content Moderation

```python
class ContentModerator:
    def __init__(self, ml_model_path: str):
        self.model = load_moderation_model(ml_model_path)

    def moderate_comment(self, text: str) -> dict:
        prediction = self.model.predict(text)
        return {
            "is_safe": prediction["toxicity_score"] < 0.7,
            "toxicity_score": prediction["toxicity_score"],
            "categories": prediction["categories"],
            "action": "approve" if prediction["toxicity_score"] < 0.5 else "flag",
        }

    def moderate_batch(self, comments: list) -> list:
        return [self.moderate_comment(c) for c in comments]
```

### Payment Security

```python
import stripe

class SecurePaymentProcessor:
    def __init__(self, stripe_secret_key: str):
        stripe.api_key = stripe_secret_key

    def process_ticket_purchase(self, user_id: str, ticket_id: str, amount: float):
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency="usd",
            metadata={"user_id": user_id, "ticket_id": ticket_id},
            automatic_payment_methods={"enabled": True},
        )
        return {
            "payment_id": payment_intent.id,
            "status": payment_intent.status,
            "client_secret": payment_intent.client_secret,
        }
```

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Fantasy projections stale | Cache TTL expired | Refresh projections; check data pipeline health |
| Sentiment analysis delayed | Social API rate limit | Implement backoff; increase rate limit allocation |
| Lineup optimizer timeout | Too many constraints | Simplify roster constraints; increase timeout |
| WebSocket disconnections | Connection pool exhaustion | Increase pool size; implement reconnection logic |
| Payment processing fails | Invalid card data | Validate card before processing; handle errors gracefully |
| Dynamic pricing oscillating | Demand signal noise | Add smoothing filter; increase cooldown period |

### Debugging Sentiment Analysis

```python
from fan_engagement.diagnostics import SentimentDebugger

debugger = SentimentDebugger(model_path="models/sentiment_v3.onnx")

# Analyze a single text
result = debugger.analyze_with_debug("What a terrible performance!")
print(f"Sentiment: {result.sentiment}")
print(f"Confidence: {result.confidence:.3f}")
print(f"Token contributions: {result.token_contributions}")

# Check for misclassifications
errors = debugger.find_errors(test_data, threshold=0.3)
print(f"Misclassification rate: {errors.error_rate:.1%}")
```

## API Reference

### Core Classes

| Class | Description | Key Methods |
|-------|-------------|-------------|
| `FantasyEngine` | Fantasy projection and optimization | `project_players()`, `optimize_lineup()`, `calculate_trade_value()` |
| `SentimentAnalyzer` | Fan sentiment analysis | `analyze_text()`, `track_live()`, `match_summary()` |
| `TicketPricingEngine` | Dynamic ticket pricing | `calculate_prices()`, `price_elasticity_analysis()` |
| `SecondScreen` | Live match second-screen | `register_element()`, `updates()`, `get_live_stats()` |
| `GamificationEngine` | Fan gamification system | `update_progress()`, `get_achievements()`, `award_points()` |
| `ContentModerator` | User content moderation | `moderate_comment()`, `moderate_batch()` |

### Data Classes

| Class | Description | Key Fields |
|-------|-------------|------------|
| `PlayerProjection` | Fantasy player projection | `player_id, projected_points, salary, matchup_score, injury_status` |
| `OptimizedLineup` | DFS optimized lineup | `players, total_salary, expected_points, projected_ownership` |
| `SentimentResult` | Sentiment analysis result | `text, sentiment_score, confidence, entities, aspects` |
| `TicketPrice` | Dynamic ticket price | `zone, base_price, optimal_price, multiplier, sell_through_projection` |
| `Achievement` | Gamification achievement | `achievement_id, name, description, progress, reward_points` |

## Data Models

### Fan Engagement Schema

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│      Users       │     │  Contest Entries  │     │    Contests     │
├─────────────────┤     ├──────────────────┤     ├─────────────────┤
│ user_id (PK)    │────<│ entry_id (PK)    │────<│ contest_id (PK) │
│ username        │     │ user_id (FK)     │     │ name            │
│ email           │     │ contest_id (FK)  │     │ sport           │
│ created_at      │     │ lineup (JSON)    │     │ entry_fee       │
│ preferences     │     │ entry_fee        │     │ prize_pool      │
│ achievement_pts │     │ current_points   │     │ max_entries     │
└─────────────────┘     │ rank             │     │ start_time      │
                        │ winnings         │     │ status          │
┌─────────────────┐     └──────────────────┘     └─────────────────┘
│  Sentiment Logs │
├─────────────────┤     ┌──────────────────┐
│ log_id (PK)     │     │   Achievements   │
│ match_id        │     ├──────────────────┤
│ platform        │     │ achievement_id   │
│ text            │     │ user_id (FK)     │
│ sentiment_score │     │ type             │
│ entities        │     │ progress         │
│ timestamp       │     │ unlocked_at      │
└─────────────────┘     │ points_awarded   │
                        └──────────────────┘
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fan-engagement-api
spec:
  replicas: 5
  selector:
    matchLabels:
      app: fan-engagement
  template:
    spec:
      containers:
      - name: api
        image: fan-engagement:1.0.0
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
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: fan-secrets
              key: redis-url
        - name: STRIPE_KEY
          valueFrom:
            secretKeyRef:
              name: fan-secrets
              key: stripe-key
```

## Monitoring & Observability

### Fan Engagement Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

ACTIVE_USERS = Gauge(
    'fan_active_users',
    'Number of active fan users',
    ['platform']
)

CONTEST_ENTRIES = Counter(
    'fan_contest_entries_total',
    'Total contest entries',
    ['sport']
)

SENTIMENT_ANALYSIS_LATENCY = Histogram(
    'sentiment_analysis_latency_seconds',
    'Sentiment analysis processing time',
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5]
)

TICKET_PURCHASES = Counter(
    'fan_ticket_purchases_total',
    'Total ticket purchases',
    ['zone']
)

LINEUP_OPTIMIZATION_TIME = Histogram(
    'lineup_optimization_seconds',
    'Time to optimize a lineup',
    buckets=[0.1, 0.5, 1, 5, 10, 30]
)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from fan_engagement import FantasyEngine, SentimentAnalyzer

class TestFantasyEngine:
    def setup_method(self):
        self.engine = FantasyEngine(platform="draftkings")

    def test_projection_range(self, sample_player_data):
        projections = self.engine.project_players(sport="nfl", week=14)
        for proj in projections:
            assert 0 <= proj.projected_points <= 50

    def test_lineup_salary_constraint(self, sample_player_pool):
        lineup = self.engine.optimize_lineup(budget=50000)
        assert lineup.total_salary <= 50000
        assert len(lineup.players) == 9

class TestSentimentAnalyzer:
    def setup_method(self):
        self.analyzer = SentimentAnalyzer(model_path="models/sentiment_test.onnx")

    def test_positive_sentiment(self):
        result = self.analyzer.analyze_text("Great goal! What a player!")
        assert result.sentiment_score > 0.5

    def test_negative_sentiment(self):
        result = self.analyzer.analyze_text("Terrible performance, should be substituted")
        assert result.sentiment_score < -0.3
```

## Versioning & Migration

### Data Schema Migration

```sql
-- Add gamification tables
CREATE TABLE user_achievements (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    achievement_type VARCHAR(100),
    progress DECIMAL(5,4) DEFAULT 0.0,
    unlocked_at TIMESTAMP,
    points_awarded INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_achievements_user
ON user_achievements (user_id);
```

### API Versioning

```python
from fastapi import APIRouter

router_v1 = APIRouter(prefix="/api/v1")
router_v2 = APIRouter(prefix="/api/v2")

@router_v1.get("/projections")
async def get_projections_v1(sport: str, week: int):
    """V1: Basic projections endpoint"""
    return engine.project_players(sport, week)

@router_v2.get("/projections")
async def get_projections_v2(sport: str, week: int, include_confidence: bool = True):
    """V2: Enhanced projections with confidence intervals"""
    projections = engine.project_players(sport, week)
    if include_confidence:
        for p in projections:
            p.confidence_interval = engine.compute_confidence(p)
    return projections
```

## Glossary

| Term | Definition |
|------|------------|
| **DFS** | Daily Fantasy Sports — contests with single-day or single-event durations |
| **GPP** | Guaranteed Prize Pool — large-field DFS tournaments with fixed prize pools |
| **Cash Game** | DFS contest (50/50, head-to-head) where roughly half of entries win |
| **Ownership** | Percentage of lineups in a contest that include a specific player |
| **Stacking** | Selecting correlated players (e.g., QB + WR from same team) for upside |
| **Salary Cap** | Maximum total salary for constructing a DFS lineup |
| **Flex Position** | Versatile roster slot accepting multiple positions |
| **Sentiment Score** | Numerical value (-1 to +1) representing text sentiment polarity |
| **Viral Score** | Metric predicting likelihood of content going viral |
| **Demand Elasticity** | Measure of how ticket demand changes with price adjustments |
| **Achievement** | Milestone unlocked by completing specific fan engagement actions |
| **Streak** | Consecutive days/weeks of engagement activity |
| **Second Screen** | Mobile device used alongside TV broadcast for interactive content |
| **AR Overlay** | Augmented reality element overlaid on live match video feed |
| **Content Moderation** | Automated filtering of user-generated content for safety |

## Changelog

### Version 1.0.0 (2024-01-15)

- Initial release with fantasy projection engine
- Sentiment analysis with transformer models
- Dynamic ticket pricing model
- Basic second-screen experience platform

### Version 1.1.0 (2024-04-01)

- Added DraftKings and FanDuel platform support
- Enhanced sentiment analysis with sport-specific lexicons
- Gamification engine with achievements and streaks
- Real-time WebSocket updates for live matches

### Version 1.2.0 (2024-07-15)

- Improved lineup optimizer with MIP solver
- Multi-language sentiment support
- AR/VR experience framework
- Advanced content moderation with ML models

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/sports-tech/fan-engagement.git
cd fan-engagement
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=fan_engagement

# Run linting
ruff check .
ruff format .
```

### Code Standards

- Fantasy projection changes must be validated against historical accuracy
- Sentiment model changes require evaluation on 1000+ labeled examples
- Pricing model changes must be backtested on 6+ months of data
- All user-facing features must include content moderation

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
