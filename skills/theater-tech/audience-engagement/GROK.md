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
