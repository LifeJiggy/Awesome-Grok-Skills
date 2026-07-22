---
name: "audience-engagement"
category: "theater-tech"
version: "1.0.0"
tags: ["theater-tech", "audience-engagement", "interactive", "polling", "real-time"]
---

# Audience Engagement System

## Overview

The audience engagement module provides a comprehensive Python API for building interactive audience participation systems in theatrical and live entertainment environments. It encompasses real-time polling and voting, second-screen experiences, social media integration, audience heatmap analytics, wearable device interaction, and pre-show/intermission engagement tools. The system is designed to bridge the gap between performers on stage and the audience in the house, transforming passive spectators into active participants while maintaining the production's artistic integrity and technical reliability.

At its core, the module implements a bidirectional communication layer between the audience's personal devices (smartphones, tablets, wearable tokens) and the show control system. The communication uses WebSocket connections for low-latency bidirectional messaging, with a REST API fallback for devices that can't maintain persistent connections. The architecture supports thousands of simultaneous audience connections through a connection pool manager that handles load balancing, heartbeat monitoring, and graceful degradation when network capacity is exceeded.

The polling engine supports multiple question types: multiple choice, ranked preference, free-text response, spatial input (tap/drag on a canvas), and sentiment rating. Results are aggregated in real-time and can be displayed on stage through integration with the lighting and projection mapping modules, or rendered on the audience's own devices as a synchronized visual experience. The social media integration layer monitors hashtags, mentions, and approved content streams from platforms like Twitter/X, Instagram, and TikTok, filtering and curating audience posts for display while maintaining content moderation.

Audience analytics uses anonymous WiFi probe request sniffing and Bluetooth Low Energy (BLE) beacon triangulation to build heatmaps of audience density, dwell time, and movement patterns. This data is invaluable for optimizing seating layouts, identifying underutilized spaces, and understanding how audiences flow through lobby and intermission spaces. All analytics are collected anonymously in compliance with GDPR and CCPA. Wearable interaction devices (LED wristbands, haptic feedback bands, NFC tokens) enable synchronized audience-wide visual effects that don't require audience members to look at their phone screens.

## Core Capabilities

- Real-time audience polling with multiple choice, ranked, spatial, and sentiment input types
- Bidirectional WebSocket communication with connection pooling for 10,000+ simultaneous devices
- Second-screen synchronized experiences with frame-accurate content delivery
- Social media integration with hashtag monitoring, content curation, and moderation queues
- Audience heatmap analytics via WiFi probe analysis and BLE beacon triangulation
- Wearable device (LED wristband, haptic band) control with synchronized effects
- Pre-show and intermission engagement tools (trivia, countdowns, lobby installations)
- Audience sentiment tracking with real-time trend analysis and alerting

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Show Integration Layer                      │
│   (Lighting Cues, Projection, Sound, Automation)        │
├─────────────────────────────────────────────────────────┤
│              Engagement Analytics Engine                 │
│    (Sentiment, Heatmaps, Device Tracking, Reporting)    │
├─────────────────────────────────────────────────────────┤
│              Content Curation & Moderation               │
│    (Social Media, Polls, Trivia, Queue Management)      │
├─────────────────────────────────────────────────────────┤
│              Communication Layer                        │
│    (WebSocket, REST API, BLE, NFC, WiFi Probes)         │
├─────────────────────────────────────────────────────────┤
│              Device & Wearable Management               │
│   (Smartphones, LED Wristbands, Haptic Bands, Tokens)  │
└─────────────────────────────────────────────────────────┘
```

## Usage Examples

### Interactive Polling

```python
from audience_engagement import EngagementServer, Poll, QuestionType, AudienceSession

# Start the engagement server
server = EngagementServer(
    host="0.0.0.0",
    port=8080,
    max_connections=10000,
    heartbeat_interval_s=30,
)
server.start()

# Create a session and launch a poll
session = server.create_session(show_id="hamilton_2026_03_15")
poll = Poll(
    question="Which ending should the characters choose?",
    question_type=QuestionType.MULTIPLE_CHOICE,
    options=["Reconciliation", "Separation", "Ambiguity"],
    duration_s=30,
    display_mode=DisplayMode.REAL_TIME_BAR,
)
session.launch_poll(poll)

# Register devices and collect responses
session.register_device(device_id="phone_001", zone="orchestra_center")
session.heartbeat("phone_001")
session.submit_response("phone_001", poll.poll_id, option_index=0)

# Get results
results = session.get_poll_results(poll.poll_id)
print(f"Winner: {results.winning_option} ({results.winning_percentage:.1f}%)")
```

### Audience Heatmap Analytics

```python
from audience_engagement import HeatmapAnalytics, BLEBeacon

analytics = HeatmapAnalytics(
    venue_width_m=30, venue_depth_m=25,
    grid_resolution_m=2.0, anonymize=True, gdpr_compliant=True,
)

# Configure beacons for triangulation
beacons = [
    BLEBeacon(beacon_id="L1", x=0, y=0, z=3, tx_power_dbm=-59),
    BLEBeacon(beacon_id="L2", x=30, y=0, z=3, tx_power_dbm=-59),
    BLEBeacon(beacon_id="L3", x=0, y=25, z=3, tx_power_dbm=-59),
    BLEBeacon(beacon_id="L4", x=30, y=25, z=3, tx_power_dbm=-59),
]
analytics.configure_beacons(beacons)

# Process probe data
for _ in range(100):
    rssi = {"L1": -60, "L2": -75, "L3": -70, "L4": -80}
    analytics.process_probe(rssi)

heatmap = analytics.get_heatmap()
analytics.export_heatmap_image(heatmap, "audience_heatmap.json")
```

### Social Media Curation

```python
from audience_engagement import SocialMediaCurator

curator = SocialMediaCurator(
    platforms=["twitter", "instagram"],
    hashtags=["#LiveTheater", "#ShowNight"],
    moderation_enabled=True,
    auto_approve_keywords=["amazing", "bravo", "love"],
    blocked_keywords=["spam", "offensive"],
)
curator.start_monitoring()

# Ingest and moderate posts
curator.ingest_post("twitter", "@fan1", "What an amazing show! #LiveTheater")
curator.ingest_post("twitter", "@spammer", "Buy cheap tickets now!")

approved = curator.get_approved_posts()
queue = curator.get_queue()
print(f"Approved: {len(approved)}, In queue: {len(queue)}")

# Manual moderation
if queue:
    curator.approve_post(queue[0].post_id)
```

### LED Wristband Control

```python
from audience_engagement import WearableController, WearableProtocol

wearable = WearableController(
    protocol=WearableProtocol.BLE,
    num_wristbands=500,
    battery_monitoring=True,
)

# Synchronized color wash
wearable.set_all(color_hex="#FF4444", fade_ms=500)

# Zone-specific effects
wearable.set_zone("orchestra_center", color_hex="#00FF00")

# Ripple and wave effects
wearable.ripple_effect(
    center_zone="orchestra_center",
    color_hex="#0044FF",
    speed_mps=5.0, duration_s=3.0,
)
wearable.wave_effect(color_hex="#FFFF00", direction="left_to_right", speed_s=2.0)

# Haptic feedback for key moments
wearable.send_haptic(zone="orchestra_left", intensity=0.8, pattern="double")
```

### Sentiment Tracking

```python
from audience_engagement import SentimentTracker, SentimentValue

sentiment = SentimentTracker(window_size=50)

# Record audience reactions throughout the show
sentiment.record(SentimentValue.VERY_POSITIVE)
sentiment.record(SentimentValue.POSITIVE)
sentiment.record(SentimentValue.NEUTRAL)

avg = sentiment.get_current_average()
trend = sentiment.get_trend()
label = sentiment.get_sentiment_label()
print(f"Sentiment: avg={avg:.2f}, trend={trend}, label={label}")
```

### Pre-Show Engagement

```python
from audience_engagement import PreShowEngagement

preshow = PreShowEngagement(session)

# Add trivia questions
preshow.add_trivia(
    "Who wrote Hamilton?",
    ["Lin-Manuel Miranda", "Stephen Sondheim", "Andrew Lloyd Webber"],
    correct_index=0,
)

# Set countdown to show time
preshow.set_countdown(target_timestamp=show_start_time)
remaining = preshow.get_countdown_remaining()
print(f"Countdown: {remaining:.0f}s until showtime")

# Launch trivia round
trivia = preshow.launch_trivia_round()
```

## Best Practices

1. **Always have a fallback plan for network outages.** Audience engagement systems depend on WiFi; design the show to work without audience input if the network fails. Pre-program default cue paths that don't require polling results.

2. **Cap poll duration at 30 seconds for in-show voting.** Longer polls lose audience attention and disrupt pacing. Pre-show and intermission polls can be longer since there's no time pressure.

3. **Moderate all social media content before display.** Even with keyword filtering, use a human-in-the-loop approval queue for content shown on stage-facing screens. One offensive post can derail a production.

4. **Anonymize all audience tracking data by default.** WiFi probe data and BLE signals can theoretically identify individuals — aggregate to 2m grid resolution and discard MAC addresses immediately.

5. **Test wearable wristband battery life under show conditions.** Battery drain varies with LED brightness and BLE advertising frequency. A wristband that dies mid-show is worse than no wristband at all.

6. **Load-test the WebSocket server at 2x expected audience size.** A 500-seat venue should be tested for 1,000 simultaneous connections. Network congestion during a show creates unpredictable latency spikes.

7. **Synchronize audience interaction moments with the lighting and sound cues.** Audience voting should trigger specific pre-programmed looks, not improvised responses. Plan the integration at cue level.

8. **Collect post-show analytics to improve future engagement.** Heatmaps, poll response rates, and device connection patterns reveal what worked and what didn't. Use this data to refine the next production's engagement strategy.

9. **Provide a non-digital participation path.** Not all audience members have smartphones or want to use them during a show. Handheld colored cards, glow sticks, or simple voice participation ensures inclusivity.

10. **Set up a dedicated WiFi network for audience devices.** Sharing bandwidth with production systems (lighting, sound, automation) creates risk. A separate VLAN for audience traffic isolates failure domains.

## Configuration

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Max Connections | 10000 | 100–50000 | Maximum simultaneous device connections |
| Heartbeat Interval | 30s | 10–120s | Device heartbeat frequency |
| Poll Duration | 30s | 5–300s | Default poll voting window |
| Heatmap Resolution | 2.0m | 0.5–5.0m | Grid cell size for density tracking |
| Social Queue Limit | 50 | 10–200 | Maximum posts in moderation queue |

## Related Modules

- [lighting-control](../lighting-control/GROK.md) — Audience-triggered lighting effects and color washes from poll results
- [projection-mapping](../projection-mapping/GROK.md) — Audience-generated content displayed on projection surfaces
- [sound-engineering](../sound-engineering/GROK.md) — Audience audio response capture and interactive soundscapes
- [stage-automation](../stage-automation/GROK.md) — Automation cues triggered by audience voting outcomes

---

## Advanced Configuration

### WebSocket Server Tuning

```python
from audience_engagement import WebSocketConfig

config = WebSocketConfig(
    max_connections=10000,
    heartbeat_interval_s=30,
    max_message_size_bytes=4096,
    ping_timeout_s=10,
    per_message_compression=True,
    connection_timeout_s=30,
    max_frame_size_bytes=16384,
)
```

### BLE Beacon Mesh Configuration

```python
from audience_engagement import BLEMeshConfig

mesh = BLEMeshConfig(
    beacon_count=16,
    advertising_interval_ms=100,
    tx_power_dbm=-59,
    scan_window_ms=100,
    scan_interval_ms=200,
    rssi_filter_threshold=-90,
    triangulation_algorithm="weighted_centroid",
)
```

## Architecture Patterns

### Bidirectional Communication Flow

```
Audience Device (Phone/Wearable)
        │
        │ WebSocket / BLE / WiFi Probe
        ▼
┌──────────────┐
│ Connection   │── Load balancing, heartbeat, pool management
│ Manager      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Engagement   │── Polls, trivia, social media
│ Engine       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Show         │── Lighting, sound, automation, projection
│ Integration  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Analytics    │── Heatmaps, sentiment, engagement metrics
│ Engine       │
└──────────────┘
```

### Content Moderation Pipeline

```
User Post
    │
    ▼
┌──────────────┐
│ Auto-Filter  │── Keyword blocklist, spam detection
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ ML Classifier│── Toxicity, sentiment, relevance scoring
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Human Queue  │── Moderator approval for stage display
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Display      │── Rendered on stage-facing screens
└──────────────┘
```

## Integration Guide

### Lighting Integration

```python
from audience_engagement import ShowIntegrationBridge

bridge = ShowIntegrationBridge()
bridge.on_poll_complete("lighting_wash", callback=lambda result: set_lighting_color(result.winning_option))
bridge.on_sentiment_threshold(0.8, callback=lambda: trigger_applause_lighting())
bridge.on_wearable_sync("color_wash", callback=lambda zone, color: set_wristband_zone(zone, color))
```

### Automation Trigger Integration

```python
bridge.on_poll_complete("reveal_choice", callback=lambda r: trigger_automation_cue(r.cue_number))
bridge.on_trivia_correct("prize_effect", callback=lambda device: trigger_pyro_cue())
```

## Performance Optimization

| Optimization | Impact |
|-------------|--------|
| WebSocket connection pooling | 50% more concurrent connections |
| Heartbeat batching | Reduced network overhead |
| Analytics aggregation windows | 90% less database writes |
| Wearable command batching | 10x more wristband throughput |
| CDN-cached polling UI | Instant poll display |

## Security Considerations

- **Network isolation**: Audience WiFi on dedicated VLAN, separate from production
- **Rate limiting**: Per-device rate limits on all API endpoints
- **Content moderation**: All social media content queued before display
- **Data anonymization**: WiFi probe data aggregated to 2m grid, MAC discarded
- **GDPR compliance**: Opt-in consent for all tracking, data retention limits
- **Device authentication**: HMAC tokens for wearable device registration
- **DDoS protection**: Connection rate limiting per IP range

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Devices disconnecting | Heartbeat timeout | Increase timeout, check WiFi AP capacity |
| Poll results delayed | Network congestion | Reduce WebSocket message frequency |
| Social posts not displaying | Moderation queue full | Increase queue limit, add moderators |
| Wristband color lag | BLE congestion | Reduce advertising frequency, batch commands |
| Heatmap accuracy poor | Insufficient beacons | Add more beacons, recalibrate positions |
| Memory usage growing | Connection pool leak | Check heartbeat cleanup, restart server |

## API Reference

### EngagementServer

```python
class EngagementServer:
    def __init__(self, host: str, port: int, max_connections: int, heartbeat_interval_s: int)
    def start(self) -> None
    def stop(self) -> None
    def create_session(self, show_id: str) -> AudienceSession
    def get_stats(self) -> ServerStats
```

### AudienceSession

```python
class AudienceSession:
    def launch_poll(self, poll: Poll) -> PollResult
    def get_poll_results(self, poll_id: str) -> PollResult
    def register_device(self, device_id: str, zone: str) -> None
    def submit_response(self, device_id: str, poll_id: str, **kwargs) -> None
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    RANKED = "ranked"
    FREE_TEXT = "free_text"
    SPATIAL = "spatial"
    SENTIMENT = "sentiment"

@dataclass
class Poll:
    question: str
    question_type: QuestionType
    options: list
    duration_s: int
    display_mode: str

@dataclass
class PollResult:
    poll_id: str
    winning_option: str
    winning_percentage: float
    total_responses: int
    response_distribution: dict
```

## Deployment Guide

### Installation

```bash
pip install audience-engagement
```

### Pre-Show Checklist

1. Start engagement server and verify WebSocket connectivity
2. Configure BLE beacon positions and verify triangulation
3. Load and test all polls and trivia questions
4. Test social media moderation pipeline
5. Verify wearable wristband connectivity and battery
6. Load-test at 2x expected audience size
7. Test fallback path (non-digital participation)
8. Set up dedicated audience WiFi network

## Monitoring & Observability

```python
from audience_engagement import MetricsCollector

collector = MetricsCollector()
collector.gauge("engagement.connected_devices", count)
collector.counter("engagement.poll.responses", count, tags={"poll_id": pid})
collector.histogram("engagement.websocket.latency_ms", latency)
collector.gauge("engagement.heatmap.density", density, tags={"zone": zone})
collector.counter("engagement.social.posts_approved", count)
collector.gauge("engagement.wearable.battery_avg", pct)
```

## Testing Strategy

```python
import pytest
from audience_engagement import EngagementServer, Poll, QuestionType

@pytest.fixture
async def server():
    s = EngagementServer(host="localhost", port=8081, max_connections=100, heartbeat_interval_s=5)
    await s.start()
    yield s
    await s.stop()

async def test_poll_launch(server):
    session = server.create_session(show_id="test_show")
    poll = Poll(question="Test?", question_type=QuestionType.MULTIPLE_CHOICE, options=["A", "B"], duration_s=10)
    result = session.launch_poll(poll)
    assert result.poll_id is not None
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added BLE wristband support | Pair wristbands via BLE scan |
| 2.0.0 | New WebSocket protocol | Update client SDK to v2 |

## Glossary

| Term | Definition |
|------|-----------|
| **BLE** | Bluetooth Low Energy |
| **WebSocket** | Persistent bidirectional TCP connection |
| **Heatmap** | Spatial density visualization of audience positions |
| **Sentiment** | Emotional valence measurement from audience input |
| **VWAP** | Volume-Weighted Audience Participation |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with WebSocket communication
- Real-time polling and voting
- Social media integration with moderation
- Audience heatmap analytics

## Contributing Guidelines

```bash
git clone https://github.com/example/audience-engagement.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### WebSocket Protocol Reference

| Message Type | Direction | Payload | Frequency |
|-------------|-----------|---------|-----------|
| `heartbeat` | Client → Server | `{device_id}` | Every 30s |
| `poll_start` | Server → Client | `{poll_id, question, options}` | On poll launch |
| `poll_response` | Client → Server | `{device_id, poll_id, option}` | Once per poll |
| `poll_result` | Server → Client | `{poll_id, results}` | On poll close |
| `social_post` | Server → Client | `{post_id, author, content, platform}` | Real-time |
| `wearable_command` | Server → Device | `{color, zone, effect, duration}` | Real-time |
| `trivia_question` | Server → Client | `{question, options, time_limit}` | On trivia |
| `trivia_answer` | Client → Server | `{device_id, question_id, answer}` | On answer |

### BLE Wristband Protocol

| Command | Opcode | Parameters | Description |
|---------|--------|------------|-------------|
| `set_color` | 0x01 | RGB (3 bytes) | Set solid color |
| `fade_to` | 0x02 | RGB, duration_ms | Fade to color |
| `pulse` | 0x03 | RGB, frequency | Pulsing effect |
| `wave` | 0x04 | RGB, direction, speed | Wave effect |
| `ripple` | 0x05 | RGB, center_x, center_y | Ripple from point |
| `off` | 0x06 | — | Turn off LEDs |
| `battery_level` | 0x10 | — | Query battery |
| `haptic` | 0x20 | intensity, pattern | Haptic feedback |

### Engagement Metrics Reference

| Metric | Target | Description |
|--------|--------|-------------|
| Device connection rate | > 70% | % of audience connected |
| Poll participation rate | > 50% | % of connected devices responding |
| Social post approval rate | > 80% | % of posts passing moderation |
| Wristband activation rate | > 90% | % of wristbands responding |
| Heatmap coverage | > 80% | % of venue covered by beacons |
| Average session duration | > 60 min | How long audience stays engaged |
| Sentiment score | > 0.7 | Average positive sentiment |

### Content Moderation Rules

| Rule | Action | Priority |
|------|--------|----------|
| Profanity detected | Block | High |
| Personal information (PII) | Block | High |
| Competitor mention | Flag for review | Medium |
| Hashtag match | Auto-approve | Low |
| Sentiment negative | Flag for review | Medium |
| Link detected | Block | High |
| Image content | Flag for review | High |
| Spam pattern detected | Block | High |

### Pre-Show Engagement Timeline

```
-60 min: Doors open, lobby WiFi available
    │
    ├── Trivia round 1 (5 questions)
    ├── Countdown timer visible
    └── Lobby installation active

-30 min: Seat finding period
    │
    ├── Seat finder tool
    ├── WiFi connection prompt
    └── Pre-show video

-15 min: Final countdown
    │
    ├── Last trivia round
    ├── Phone silence reminder
    └── Show preview content

-5 min: Show about to begin
    │
    ├── Final countdown
    ├── Wristband color wash
    └── Phones to silent mode

-0 min: Show starts
    │
    ├── In-show engagement begins
    └── Wristband effects sync with show
```

### Heatmap Configuration

```python
from audience_engagement import HeatmapConfig

config = HeatmapConfig(
    venue_width_m=30,
    venue_depth_m=25,
    grid_resolution_m=2.0,
    beacon_positions=[
        {"id": "L1", "x": 0, "y": 0, "z": 3},
        {"id": "L2", "x": 30, "y": 0, "z": 3},
        {"id": "L3", "x": 0, "y": 25, "z": 3},
        {"id": "L4", "x": 30, "y": 25, "z": 3},
        {"id": "C1", "x": 15, "y": 12, "z": 6},
    ],
    rssi_filter_threshold=-90,
    triangulation_algorithm="weighted_centroid",
    anonymize=True,
    gdpr_compliant=True,
    data_retention_days=7,
)
```

### Troubleshooting Decision Tree

```
Devices can't connect
    │
    ├── Check WiFi AP capacity → Increase if > 80% utilized
    ├── Check SSID broadcast → Ensure visible
    ├── Check DHCP pool → Ensure enough IPs
    ├── Check firewall rules → Allow WebSocket ports
    └── Check server load → Scale horizontally

Poll results not updating
    │
    ├── Check WebSocket connection → Verify ping/pong
    ├── Check server processing → Monitor CPU/memory
    ├── Check database writes → Verify connection pool
    └── Check client rendering → Inspect browser console

Wristband not responding
    │
    ├── Check battery level → Replace if low
    ├── Check BLE signal → Move closer to transmitter
    ├── Check wristband registration → Re-register device
    ├── Check firmware version → Update if needed
    └── Check for interference → Change BLE channel
```

### Performance Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| WebSocket connections | > 10,000 | 5,000-10,000 | < 5,000 |
| WebSocket latency | < 100ms | 100-500ms | > 500ms |
| Poll response time | < 200ms | 200-500ms | > 500ms |
| BLE command latency | < 50ms | 50-200ms | > 200ms |
| Heatmap update interval | 5s | 5-15s | > 15s |
| Social moderation queue | < 50 | 50-200 | > 200 |
| Device battery (avg) | > 30% | 15-30% | < 15% |

### WiFi Network Design

| Component | Specification |
|-----------|--------------|
| Access Points | Enterprise-grade (Ubiquiti, Aruba) |
| AP Density | 1 per 50-100 devices |
| Channel Planning | Non-overlapping channels (1, 6, 11) |
| VLAN | Dedicated audience VLAN |
| DHCP Pool | /22 or larger (1000+ IPs) |
| Bandwidth per AP | 1 Gbps uplink |
| QoS | WMM enabled, prioritize WebSocket |
| Security | WPA2-Enterprise or open with captive portal |

### Device Compatibility Matrix

| Device Type | WebSocket | BLE | NFC | WiFi Probe | Notes |
|------------|-----------|-----|-----|------------|-------|
| iOS 14+ | Yes | Yes | Yes | Yes | Full support |
| Android 10+ | Yes | Yes | Limited | Yes | Full support |
| iPad | Yes | Yes | Yes | Yes | Recommended for VJ |
| Laptop | Yes | No | No | Yes | Web-based only |
| LED Wristband | No | Yes | No | No | BLE only |
| Haptic Band | No | Yes | No | No | BLE only |
| NFC Token | No | No | Yes | No | Tap to interact |

### Social Media Platform Integration

| Platform | API | Rate Limit | Content Types |
|----------|-----|-----------|---------------|
| Twitter/X | v2 | 300 req/15min | Text, images, video |
| Instagram | Graph API | 200 req/hour | Images, stories |
| TikTok | Marketing API | 100 req/day | Video |
| Facebook | Graph API | 200 req/hour | Text, images |
| Mastodon | v1 | Varies by instance | Text, images |

### Complete Engagement Analytics Schema

```json
{
  "show_id": "hamilton_2026_03_15",
  "venue": "Richard Rodgers Theatre",
  "attendance": 1320,
  "connected_devices": 892,
  "engagement_rate": 0.676,
  "polls": [
    {
      "poll_id": "poll_001",
      "question": "Which ending?",
      "total_responses": 654,
      "response_rate": 0.733,
      "results": {"option_a": 280, "option_b": 210, "option_c": 164}
    }
  ],
  "sentiment": {
    "average": 0.82,
    "trend": "positive",
    "peak_moment": "01:25:00",
    "peak_sentiment": 0.95
  },
  "heatmaps": {
    "peak_density_zone": "orchestra_center",
    "peak_density_time": "01:15:00",
    "density_value": 4.2
  },
  "wearables": {
    "total": 500,
    "active": 478,
    "effects_triggered": 12,
    "average_battery_pct": 67
  }
}
```

### Engagement Event Timeline Template

```
PRE-SHOW (60 min before)
    │
    ├── 00:00 - WiFi network active
    ├── 00:00 - Lobby installation active
    ├── 15:00 - Trivia round 1
    ├── 30:00 - Trivia round 2
    ├── 45:00 - Final trivia, countdown starts
    └── 55:00 - Phone silence reminder

ACT 1
    │
    ├── 01:00:00 - Wristband color wash (opening)
    ├── 01:15:00 - Poll 1 (interactive moment)
    ├── 01:25:00 - Wristband ripple effect
    ├── 01:35:00 - Social media display
    └── 01:45:00 - Act 1 curtain call effect

INTERMISSION
    │
    ├── 00:00 - Intermission trivia
    ├── 05:00 - Social media wall
    ├── 10:00 - Poll 2 (audience choice)
    └── 15:00 - Countdown to Act 2

ACT 2
    │
    ├── 02:00:00 - Wristband color wash
    ├── 02:15:00 - Poll 3
    ├── 02:30:00 - Audience vote → automation cue
    ├── 02:45:00 - Final wristband effect
    └── 03:00:00 - Curtain call celebration effect

POST-SHOW
    │
    ├── 00:00 - Thank you message
    ├── 05:00 - Post-show survey
    └── 10:00 - WiFi network shutdown

### Complete Device Registration Protocol

```python
from audience_engagement import DeviceRegistration

# Device registration flow
registration = DeviceRegistration(
    show_id="hamilton_2026_03_15",
    venue_id="richard_rogers_theatre",
    max_devices_per_ip=5,
    require_agb_acceptance=True,
    collect_demographics=False,  # GDPR: don't collect unless needed
)

# Register device
device = registration.register(
    device_id="phone_abc123",
    device_type="smartphone",
    platform="ios",
    screen_size="6.1_inch",
    connection_type="wifi",
    zone="orchestra_center",
)

# Generate session token
token = registration.create_session(device)
# Token sent to device for WebSocket authentication
```

### Poll Response Analytics

| Metric | Calculation | Target |
|--------|------------|--------|
| Response Rate | Responses / Connected Devices | > 50% |
| Response Time | Avg time from poll launch to response | < 10s |
| Completion Rate | Fully completed polls / Total polls | > 80% |
| Drop-off Rate | Abandoned polls / Started polls | < 10% |
| Peak Concurrent | Max simultaneous responses | > 30% of connected |
| Zone Distribution | Responses per zone / Total | Even distribution |

### Wearable Effect Library

| Effect | Description | Duration | Use Case |
|--------|-------------|----------|----------|
| Color Wash | Solid color across all | Variable | Opening, transitions |
| Ripple | Color spreads from center | 3s | Reveals, climaxes |
| Wave | Color sweeps left to right | 2-5s | Musical moments |
| Pulse | Rhythmic brightness change | Variable | Music sync |
| Sparkle | Random bright flashes | 5s | Magic, celebrations |
| Fade In | Gradual color increase | 2-3s | Gentle transitions |
| Fade Out | Gradual color decrease | 2-3s | Scene endings |
| Rainbow | Continuous color cycle | Variable | Finale, celebration |
| Strobe | Rapid on/off flashing | 1-2s | Rock concert feel |
| Off | All LEDs off | Instant | Blackouts |

### WiFi Network Design Specification

```
NETWORK ARCHITECTURE
    │
    ├── Internet Gateway (1 Gbps)
    │       │
    │   ┌───┴───┐
    │   │ Core  │ (L3 switch)
    │   │ Switch│
    │   └───┬───┘
    │       │
    │   ┌───┴───┬───┬───┐
    │   │       │   │   │
    │   AP1    AP2  AP3  AP4  (Enterprise WiFi 6)
    │   │       │   │   │
    │   └───┬───┘   │   │
    │       │       │   │
    │   Audience VLAN  Production VLAN
    │   (10.10.x.x)    (10.20.x.x)
    │
    ├── Dedicated DNS (Pi-hole or similar)
    ├── DHCP: /22 subnet (1000+ IPs)
    ├── QoS: Prioritize WebSocket traffic
    └── Firewall: Isolate from production
```

### Post-Show Analytics Report Template

```json
{
  "show_id": "hamilton_2026_03_15",
  "report_date": "2026-03-15",
  "summary": {
    "total_attendance": 1320,
    "connected_devices": 892,
    "engagement_rate": 0.676,
    "average_sentiment": 0.82,
    "peak_engagement_time": "01:25:00"
  },
  "polls": {
    "total_polls": 3,
    "total_responses": 1854,
    "average_response_rate": 0.694,
    "most_popular_poll": "poll_001"
  },
  "social_media": {
    "posts_collected": 234,
    "posts_approved": 198,
    "approval_rate": 0.846,
    "top_hashtag": "#LiveTheater"
  },
  "wearables": {
    "total_distributed": 500,
    "active_during_show": 478,
    "effects_triggered": 12,
    "average_battery_remaining": 0.67
  },
  "heatmap": {
    "densest_zone": "orchestra_center",
    "densest_time": "01:15:00",
    "coverage_percentage": 0.85
  },
  "recommendations": [
    "Increase AP density in balcony area",
    "Consider larger trivia prize to boost engagement",
    "Wristband battery adequate for 2-hour shows"
  ]
}
```
```
