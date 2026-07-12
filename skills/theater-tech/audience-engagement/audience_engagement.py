"""
Audience Engagement System
Interactive polling, second-screen experiences, social media integration,
wearable control, heatmap analytics, and sentiment tracking.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class QuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    RANKED_PREFERENCE = "ranked_preference"
    FREE_TEXT = "free_text"
    SPATIAL_INPUT = "spatial_input"
    SENTIMENT_RATING = "sentiment_rating"
    YES_NO = "yes_no"


class DisplayMode(Enum):
    REAL_TIME_BAR = "real_time_bar"
    PIE_CHART = "pie_chart"
    WORD_CLOUD = "word_cloud"
    HEATMAP = "heatmap"
    SCROLLING_FEED = "scrolling_feed"


class WearableProtocol(Enum):
    BLE = "ble"
    RF_433MHZ = "rf_433mhz"
    WIFI = "wifi"
    IR = "ir"


class SocialPlatform(Enum):
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    FACEBOOK = "facebook"


class SentimentValue(Enum):
    VERY_NEGATIVE = -2
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1
    VERY_POSITIVE = 2


class EngagementEventType(Enum):
    POLL_LAUNCHED = "poll_launched"
    POLL_RESPONSE = "poll_response"
    POLL_CLOSED = "poll_closed"
    SOCIAL_POST_QUEUED = "social_post_queued"
    SOCIAL_POST_APPROVED = "social_post_approved"
    WEARABLE_EFFECT = "wearable_effect"
    HEATMAP_SNAPSHOT = "heatmap_snapshot"
    SENTIMENT_UPDATE = "sentiment_update"
    DEVICE_CONNECTED = "device_connected"
    DEVICE_DISCONNECTED = "device_disconnected"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class AudienceDevice:
    device_id: str
    session_id: str
    connected_at: float = 0.0
    last_heartbeat: float = 0.0
    zone: str = "general"
    wristband_id: Optional[str] = None

    @property
    def is_active(self) -> bool:
        return (time.time() - self.last_heartbeat) < 60


@dataclass
class PollOption:
    option_id: int
    text: str
    vote_count: int = 0
    color_hex: str = "#4488FF"


@dataclass
class Poll:
    question: str
    question_type: QuestionType = QuestionType.MULTIPLE_CHOICE
    options: Optional[list[str]] = None
    duration_s: float = 30.0
    display_mode: DisplayMode = DisplayMode.REAL_TIME_BAR
    poll_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    launched_at: Optional[float] = None
    closed_at: Optional[float] = None

    def __post_init__(self) -> None:
        if self.options is None:
            self.options = []


@dataclass
class PollResults:
    poll_id: str
    total_responses: int
    winning_option: str
    winning_percentage: float
    option_counts: dict[str, int] = field(default_factory=dict)
    response_timeline: list[tuple[float, int]] = field(default_factory=list)


@dataclass
class PollResponse:
    device_id: str
    poll_id: str
    option_index: int
    option_text: str
    timestamp: float
    free_text: Optional[str] = None
    spatial_x: Optional[float] = None
    spatial_y: Optional[float] = None
    sentiment: Optional[SentimentValue] = None


@dataclass
class SocialPost:
    post_id: str
    platform: SocialPlatform
    author_handle: str
    content: str
    timestamp: float
    approved: bool = False
    display_priority: int = 0
    hashtags: list[str] = field(default_factory=list)


@dataclass
class BLEBeacon:
    beacon_id: str
    x: float
    y: float
    z: float = 0.0
    tx_power_dbm: float = -59.0


@dataclass
class HeatmapCell:
    x: float
    y: float
    density: float = 0.0
    dwell_time_s: float = 0.0
    sample_count: int = 0


@dataclass
class LEDWristband:
    wristband_id: str
    zone: str = "general"
    current_color: str = "#000000"
    brightness: float = 1.0
    battery_pct: float = 100.0
    haptic_enabled: bool = True


@dataclass
class EngagementEvent:
    event_type: EngagementEventType
    timestamp: float
    data: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])


# ---------------------------------------------------------------------------
# Audience Session
# ---------------------------------------------------------------------------

class AudienceSession:
    """Manages a single show's audience interaction session."""

    def __init__(self, show_id: str):
        self.show_id = show_id
        self._devices: dict[str, AudienceDevice] = {}
        self._polls: dict[str, Poll] = {}
        self._responses: dict[str, list[PollResponse]] = {}
        self._events: list[EngagementEvent] = []
        self._sentiment_history: list[tuple[float, float]] = []

    def register_device(self, device_id: str, zone: str = "general") -> AudienceDevice:
        device = AudienceDevice(
            device_id=device_id,
            session_id=self.show_id,
            connected_at=time.time(),
            last_heartbeat=time.time(),
            zone=zone,
        )
        self._devices[device_id] = device
        self._events.append(EngagementEvent(
            event_type=EngagementEventType.DEVICE_CONNECTED,
            timestamp=time.time(),
            data={"device_id": device_id, "zone": zone},
        ))
        logger.info("Device connected: %s (zone: %s)", device_id, zone)
        return device

    def heartbeat(self, device_id: str) -> None:
        if device_id in self._devices:
            self._devices[device_id].last_heartbeat = time.time()

    def launch_poll(self, poll: Poll) -> str:
        poll.launched_at = time.time()
        self._polls[poll.poll_id] = poll
        self._responses[poll.poll_id] = []
        self._events.append(EngagementEvent(
            event_type=EngagementEventType.POLL_LAUNCHED,
            timestamp=time.time(),
            data={"poll_id": poll.poll_id, "question": poll.question},
        ))
        logger.info("Poll launched: '%s' (id: %s)", poll.question, poll.poll_id)
        return poll.poll_id

    def submit_response(
        self,
        device_id: str,
        poll_id: str,
        option_index: int = 0,
        free_text: Optional[str] = None,
        spatial_x: Optional[float] = None,
        spatial_y: Optional[float] = None,
        sentiment: Optional[SentimentValue] = None,
    ) -> bool:
        poll = self._polls.get(poll_id)
        if poll is None:
            return False
        if poll.launched_at and (time.time() - poll.launched_at) > poll.duration_s:
            return False

        option_text = poll.options[option_index] if poll.options and option_index < len(poll.options) else ""
        response = PollResponse(
            device_id=device_id,
            poll_id=poll_id,
            option_index=option_index,
            option_text=option_text,
            timestamp=time.time(),
            free_text=free_text,
            spatial_x=spatial_x,
            spatial_y=spatial_y,
            sentiment=sentiment,
        )
        self._responses.setdefault(poll_id, []).append(response)
        self._events.append(EngagementEvent(
            event_type=EngagementEventType.POLL_RESPONSE,
            timestamp=time.time(),
            data={"device_id": device_id, "poll_id": poll_id, "option": option_text},
        ))
        return True

    def close_poll(self, poll_id: str) -> PollResults:
        poll = self._polls.get(poll_id)
        if poll is None:
            raise ValueError(f"Poll {poll_id} not found")
        poll.closed_at = time.time()

        responses = self._responses.get(poll_id, [])
        counts: dict[str, int] = {}
        for r in responses:
            counts[r.option_text] = counts.get(r.option_text, 0) + 1

        total = len(responses)
        winning = max(counts, key=counts.get) if counts else "No votes"
        winning_pct = (counts[winning] / total * 100) if total > 0 and winning in counts else 0.0

        timeline = []
        for r in sorted(responses, key=lambda x: x.timestamp):
            timeline.append((r.timestamp, r.option_index))

        results = PollResults(
            poll_id=poll_id,
            total_responses=total,
            winning_option=winning,
            winning_percentage=winning_pct,
            option_counts=counts,
            response_timeline=timeline,
        )
        self._events.append(EngagementEvent(
            event_type=EngagementEventType.POLL_CLOSED,
            timestamp=time.time(),
            data={"poll_id": poll_id, "total": total, "winner": winning},
        ))
        return results

    def get_poll_results(self, poll_id: str) -> PollResults:
        return self.close_poll(poll_id)

    def get_active_device_count(self) -> int:
        return sum(1 for d in self._devices.values() if d.is_active)

    def get_events(self, event_type: Optional[EngagementEventType] = None) -> list[EngagementEvent]:
        if event_type:
            return [e for e in self._events if e.event_type == event_type]
        return list(self._events)


# ---------------------------------------------------------------------------
# Engagement Server
# ---------------------------------------------------------------------------

class EngagementServer:
    """WebSocket/HTTP server for audience interaction."""

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        max_connections: int = 10000,
        heartbeat_interval_s: float = 30.0,
    ):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.heartbeat_interval_s = heartbeat_interval_s
        self._running = False
        self._sessions: dict[str, AudienceSession] = {}
        self._connection_count = 0

    def start(self) -> bool:
        self._running = True
        logger.info("Engagement server started on %s:%d (max %d connections)", self.host, self.port, self.max_connections)
        return True

    def stop(self) -> None:
        self._running = False
        logger.info("Engagement server stopped")

    def create_session(self, show_id: str) -> AudienceSession:
        session = AudienceSession(show_id=show_id)
        self._sessions[show_id] = session
        return session

    def get_session(self, show_id: str) -> Optional[AudienceSession]:
        return self._sessions.get(show_id)

    @property
    def total_connections(self) -> int:
        return sum(s.get_active_device_count() for s in self._sessions.values())


# ---------------------------------------------------------------------------
# Heatmap Analytics
# ---------------------------------------------------------------------------

class HeatmapAnalytics:
    """Audience density heatmap via WiFi/BLE tracking."""

    def __init__(
        self,
        venue_width_m: float = 30.0,
        venue_depth_m: float = 25.0,
        grid_resolution_m: float = 2.0,
        anonymize: bool = True,
        gdpr_compliant: bool = True,
    ):
        self.venue_width_m = venue_width_m
        self.venue_depth_m = venue_depth_m
        self.grid_resolution_m = grid_resolution_m
        self.anonymize = anonymize
        self.gdpr_compliant = gdpr_compliant
        self._beacons: list[BLEBeacon] = []
        self._grid_cols = int(math.ceil(venue_width_m / grid_resolution_m))
        self._grid_rows = int(math.ceil(venue_depth_m / grid_resolution_m))
        self._grid: list[list[HeatmapCell]] = []

        for row in range(self._grid_rows):
            grid_row = []
            for col in range(self._grid_cols):
                x = col * grid_resolution_m + grid_resolution_m / 2
                y = row * grid_resolution_m + grid_resolution_m / 2
                grid_row.append(HeatmapCell(x=x, y=y))
            self._grid.append(grid_row)

    def configure_beacons(self, beacons: list[BLEBeacon]) -> None:
        self._beacons = beacons
        logger.info("Configured %d BLE beacons", len(beacons))

    def _triangulate_position(
        self, rssi_values: dict[str, float],
    ) -> Optional[tuple[float, float]]:
        if len(rssi_values) < 3:
            return None
        estimated_positions = []
        for bid, rssi in rssi_values.items():
            beacon = next((b for b in self._beacons if b.beacon_id == bid), None)
            if beacon:
                distance = 10 ** ((beacon.tx_power_dbm - rssi) / (10 * 2.5))
                estimated_positions.append((beacon.x, beacon.y, distance))

        if len(estimated_positions) < 3:
            return None
        xs = [p[0] for p in estimated_positions]
        ys = [p[1] for p in estimated_positions]
        x_est = sum(xs) / len(xs)
        y_est = sum(ys) / len(ys)
        return (x_est, y_est)

    def process_probe(self, rssi_values: dict[str, float]) -> Optional[tuple[float, float]]:
        pos = self._triangulate_position(rssi_values)
        if pos is None:
            return None
        col = int(pos[0] / self.grid_resolution_m)
        row = int(pos[1] / self.grid_resolution_m)
        col = max(0, min(col, self._grid_cols - 1))
        row = max(0, min(row, self._grid_rows - 1))
        self._grid[row][col].density += 1.0
        self._grid[row][col].sample_count += 1
        if self.anonymize:
            return (round(pos[0], 1), round(pos[1], 1))
        return pos

    def get_heatmap(self) -> list[list[dict[str, Any]]]:
        max_density = max(
            (cell.density for row in self._grid for cell in row), default=1.0
        )
        result = []
        for row in self._grid:
            row_data = []
            for cell in row:
                normalized = cell.density / max_density if max_density > 0 else 0
                row_data.append({
                    "x": cell.x, "y": cell.y,
                    "density": normalized,
                    "raw_count": cell.sample_count,
                })
            result.append(row_data)
        return result

    def start_collection(self, probe_collector: Any) -> None:
        logger.info("Started heatmap collection from probe collector")

    def export_heatmap_image(self, heatmap: list[list[dict[str, Any]]], filepath: str) -> None:
        width = len(heatmap[0]) if heatmap else 0
        height = len(heatmap)
        data = {"width": width, "height": height, "cells": heatmap}
        Path(filepath).write_text(json.dumps(data, indent=2))
        logger.info("Heatmap exported to %s (%dx%d)", filepath, width, height)


# ---------------------------------------------------------------------------
# WiFi Probe Collector
# ---------------------------------------------------------------------------

class WiFiProbeCollector:
    """Collects WiFi probe requests for anonymous presence detection."""

    def __init__(self, interface: str = "wlan0", channel_hop: bool = True):
        self.interface = interface
        self.channel_hop = channel_hop
        self._probes: list[dict[str, Any]] = []

    def capture_probe(self, mac_hash: str, rssi: float, channel: int) -> dict[str, Any]:
        probe = {
            "mac_hash": mac_hash,
            "rssi": rssi,
            "channel": channel,
            "timestamp": time.time(),
        }
        self._probes.append(probe)
        return probe

    def get_recent_probes(self, window_s: float = 60) -> list[dict[str, Any]]:
        cutoff = time.time() - window_s
        return [p for p in self._probes if p["timestamp"] > cutoff]


# ---------------------------------------------------------------------------
# Social Media Curator
# ---------------------------------------------------------------------------

class SocialMediaCurator:
    """Curates and moderates social media content for display."""

    def __init__(
        self,
        platforms: Optional[list[str]] = None,
        hashtags: Optional[list[str]] = None,
        moderation_enabled: bool = True,
        auto_approve_keywords: Optional[list[str]] = None,
        blocked_keywords: Optional[list[str]] = None,
    ):
        self.platforms = [SocialPlatform(p) for p in (platforms or ["twitter"])]
        self.hashtags = hashtags or []
        self.moderation_enabled = moderation_enabled
        self.auto_approve_keywords = [kw.lower() for kw in (auto_approve_keywords or [])]
        self.blocked_keywords = [kw.lower() for kw in (blocked_keywords or [])]
        self._queue: list[SocialPost] = []
        self._approved: list[SocialPost] = []
        self._running = False

    def start_monitoring(self) -> None:
        self._running = True
        logger.info("Social media monitoring started for %s", [p.value for p in self.platforms])

    def stop_monitoring(self) -> None:
        self._running = False

    def ingest_post(self, platform: str, author: str, content: str, hashtags: Optional[list[str]] = None) -> SocialPost:
        post = SocialPost(
            post_id=uuid.uuid4().hex[:8],
            platform=SocialPlatform(platform),
            author_handle=author,
            content=content,
            timestamp=time.time(),
            hashtags=hashtags or [],
        )
        if self._check_blocked(content):
            logger.info("Blocked post from @%s: %s", author, content[:50])
            return post
        if self._check_auto_approve(content):
            post.approved = True
            self._approved.append(post)
        elif self.moderation_enabled:
            self._queue.append(post)
        else:
            post.approved = True
            self._approved.append(post)
        return post

    def approve_post(self, post_id: str) -> bool:
        post = next((p for p in self._queue if p.post_id == post_id), None)
        if post:
            post.approved = True
            self._approved.append(post)
            self._queue.remove(post)
            self._log_event(EngagementEventType.SOCIAL_POST_APPROVED, {"post_id": post_id})
            return True
        return False

    def reject_post(self, post_id: str) -> bool:
        post = next((p for p in self._queue if p.post_id == post_id), None)
        if post:
            self._queue.remove(post)
            return True
        return False

    def get_approved_posts(self, limit: int = 20) -> list[SocialPost]:
        return self._approved[:limit]

    def get_queue(self) -> list[SocialPost]:
        return list(self._queue)

    def _check_blocked(self, content: str) -> bool:
        content_lower = content.lower()
        return any(kw in content_lower for kw in self.blocked_keywords)

    def _check_auto_approve(self, content: str) -> bool:
        content_lower = content.lower()
        return any(kw in content_lower for kw in self.auto_approve_keywords)

    def _log_event(self, event_type: EngagementEventType, data: dict[str, Any]) -> None:
        logger.info("Social event: %s — %s", event_type.value, data)


# ---------------------------------------------------------------------------
# Wearable Controller
# ---------------------------------------------------------------------------

class WearableController:
    """Controls LED wristbands and haptic wearable devices."""

    def __init__(
        self,
        protocol: WearableProtocol = WearableProtocol.BLE,
        num_wristbands: int = 500,
        battery_monitoring: bool = True,
    ):
        self.protocol = protocol
        self.num_wristbands = num_wristbands
        self.battery_monitoring = battery_monitoring
        self._wristbands: dict[str, LEDWristband] = {}
        self._zones: dict[str, list[str]] = {}

        for i in range(num_wristbands):
            wb_id = f"WB{i:04d}"
            zone = self._assign_zone(i)
            wb = LEDWristband(wristband_id=wb_id, zone=zone)
            self._wristbands[wb_id] = wb
            self._zones.setdefault(zone, []).append(wb_id)

    def _assign_zone(self, index: int) -> str:
        zones = ["orchestra_left", "orchestra_center", "orchestra_right", "balcony"]
        return zones[index % len(zones)]

    def set_all(self, color_hex: str = "#FFFFFF", fade_ms: int = 0, brightness: float = 1.0) -> int:
        count = 0
        for wb in self._wristbands.values():
            wb.current_color = color_hex
            wb.brightness = brightness
            count += 1
        logger.info("Set all %d wristbands to %s (fade %dms)", count, color_hex, fade_ms)
        return count

    def set_zone(self, zone: str, color_hex: str, fade_ms: int = 0) -> int:
        wbs = self._zones.get(zone, [])
        for wb_id in wbs:
            self._wristbands[wb_id].current_color = color_hex
        logger.info("Set %d wristbands in zone '%s' to %s", len(wbs), zone, color_hex)
        return len(wbs)

    def ripple_effect(
        self,
        center_zone: str,
        color_hex: str,
        speed_mps: float = 5.0,
        duration_s: float = 3.0,
    ) -> None:
        logger.info(
            "Ripple effect from '%s': color=%s, speed=%.1f m/s, duration=%.1fs",
            center_zone, color_hex, speed_mps, duration_s,
        )

    def wave_effect(
        self,
        color_hex: str,
        direction: str = "left_to_right",
        speed_s: float = 2.0,
    ) -> None:
        logger.info("Wave effect: color=%s, direction=%s, speed=%.1fs", color_hex, direction, speed_s)

    def pulse_effect(
        self,
        color_hex: str,
        pulse_rate_hz: float = 1.0,
        duration_s: float = 5.0,
    ) -> None:
        logger.info("Pulse effect: color=%s, rate=%.1f Hz, duration=%.1fs", color_hex, pulse_rate_hz, duration_s)

    def send_haptic(self, zone: str, intensity: float, pattern: str = "single") -> int:
        count = 0
        for wb_id in self._zones.get(zone, []):
            wb = self._wristbands[wb_id]
            if wb.haptic_enabled:
                count += 1
        logger.info("Haptic to %d devices in '%s': intensity=%.2f, pattern=%s", count, zone, intensity, pattern)
        return count

    def get_battery_levels(self) -> dict[str, float]:
        return {wb_id: wb.battery_pct for wb_id, wb in self._wristbands.items()}

    def get_zone_counts(self) -> dict[str, int]:
        return {zone: len(wbs) for zone, wbs in self._zones.items()}


# ---------------------------------------------------------------------------
# Sentiment Tracker
# ---------------------------------------------------------------------------

class SentimentTracker:
    """Tracks audience sentiment over time via polls and reactions."""

    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self._readings: list[tuple[float, float]] = []

    def record(self, value: SentimentValue, weight: float = 1.0) -> None:
        self._readings.append((time.time(), value.value * weight))
        if len(self._readings) > self.window_size * 10:
            self._readings = self._readings[-self.window_size * 10:]

    def get_current_average(self) -> float:
        if not self._readings:
            return 0.0
        recent = self._readings[-self.window_size:]
        return sum(v for _, v in recent) / len(recent)

    def get_trend(self) -> str:
        if len(self._readings) < 10:
            return "insufficient_data"
        half = len(self._readings) // 2
        first_half = sum(v for _, v in self._readings[:half]) / half
        second_half = sum(v for _, v in self._readings[half:]) / (len(self._readings) - half)
        diff = second_half - first_half
        if diff > 0.3:
            return "improving"
        elif diff < -0.3:
            return "declining"
        return "stable"

    def get_sentiment_label(self) -> str:
        avg = self.get_current_average()
        if avg > 1.0:
            return "very_positive"
        elif avg > 0.3:
            return "positive"
        elif avg > -0.3:
            return "neutral"
        elif avg > -1.0:
            return "negative"
        return "very_negative"

    def export_data(self, filepath: str) -> None:
        data = {
            "readings": [{"timestamp": t, "value": v} for t, v in self._readings],
            "current_average": self.get_current_average(),
            "trend": self.get_trend(),
            "label": self.get_sentiment_label(),
        }
        Path(filepath).write_text(json.dumps(data, indent=2))
        logger.info("Sentiment data exported to %s", filepath)


# ---------------------------------------------------------------------------
# Pre-Show Engagement
# ---------------------------------------------------------------------------

class PreShowEngagement:
    """Manages pre-show and intermission engagement activities."""

    def __init__(self, session: AudienceSession):
        self.session = session
        self._trivia_questions: list[dict[str, Any]] = []
        self._countdown_target: Optional[float] = None

    def add_trivia(self, question: str, options: list[str], correct_index: int) -> str:
        trivia_id = uuid.uuid4().hex[:8]
        self._trivia_questions.append({
            "id": trivia_id,
            "question": question,
            "options": options,
            "correct_index": correct_index,
        })
        return trivia_id

    def set_countdown(self, target_timestamp: float) -> None:
        self._countdown_target = target_timestamp
        logger.info("Countdown set to %.0f", target_timestamp)

    def get_countdown_remaining(self) -> Optional[float]:
        if self._countdown_target is None:
            return None
        remaining = self._countdown_target - time.time()
        return max(0.0, remaining)

    def launch_trivia_round(self) -> Optional[dict[str, Any]]:
        if not self._trivia_questions:
            return None
        q = self._trivia_questions.pop(0)
        poll = Poll(
            question=q["question"],
            question_type=QuestionType.MULTIPLE_CHOICE,
            options=q["options"],
            duration_s=20,
        )
        self.session.launch_poll(poll)
        return {"trivia_id": q["id"], "poll_id": poll.poll_id}

    def get_leaderboard(self) -> list[dict[str, Any]]:
        return []


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("=" * 60)
    print("  Audience Engagement System — Demo")
    print("=" * 60)

    # --- Server & Session ---
    server = EngagementServer(host="0.0.0.0", port=8080, max_connections=10000)
    server.start()
    session = server.create_session(show_id="hamilton_2026_03_15")

    # Register devices
    for i in range(50):
        session.register_device(device_id=f"device_{i:03d}", zone=["orchestra_left", "orchestra_center", "orchestra_right"][i % 3])
    print(f"Active devices: {session.get_active_device_count()}")

    # --- Polling ---
    poll = Poll(
        question="Which ending should the characters choose?",
        question_type=QuestionType.MULTIPLE_CHOICE,
        options=["Reconciliation", "Separation", "Ambiguity"],
        duration_s=30,
        display_mode=DisplayMode.REAL_TIME_BAR,
    )
    session.launch_poll(poll)

    for i in range(35):
        device_id = f"device_{i:03d}"
        session.heartbeat(device_id)
        choice = random.choice([0, 1, 2])
        session.submit_response(device_id, poll.poll_id, option_index=choice)

    results = session.get_poll_results(poll.poll_id)
    print(f"Poll results: {results.total_responses} responses, winner: '{results.winning_option}' ({results.winning_percentage:.1f}%)")
    print(f"Option counts: {results.option_counts}")

    # --- Heatmap Analytics ---
    analytics = HeatmapAnalytics(venue_width_m=30, venue_depth_m=25, grid_resolution_m=2.0)
    beacons = [
        BLEBeacon(beacon_id="L1", x=0, y=0, z=3, tx_power_dbm=-59),
        BLEBeacon(beacon_id="L2", x=30, y=0, z=3, tx_power_dbm=-59),
        BLEBeacon(beacon_id="L3", x=0, y=25, z=3, tx_power_dbm=-59),
    ]
    analytics.configure_beacons(beacons)
    for _ in range(100):
        rssi = {"L1": -60 + random.uniform(-5, 5), "L2": -75 + random.uniform(-5, 5), "L3": -70 + random.uniform(-5, 5)}
        analytics.process_probe(rssi)
    heatmap = analytics.get_heatmap()
    analytics.export_heatmap_image(heatmap, "/tmp/heatmap.json")
    print(f"Heatmap grid: {len(heatmap)}x{len(heatmap[0]) if heatmap else 0}")

    # --- Social Media ---
    curator = SocialMediaCurator(
        platforms=["twitter", "instagram"],
        hashtags=["#LiveTheater"],
        moderation_enabled=True,
        auto_approve_keywords=["bravo", "amazing"],
        blocked_keywords=["spam"],
    )
    curator.start_monitoring()
    curator.ingest_post("twitter", "@fan1", "What an amazing show! #LiveTheater")
    curator.ingest_post("twitter", "@spammer", "Buy cheap tickets now!")
    curator.ingest_post("instagram", "@patron", "Bravo to the entire cast!")
    approved = curator.get_approved_posts()
    queue = curator.get_queue()
    print(f"Social: {len(approved)} approved, {len(queue)} in queue")

    # --- Wearable Controller ---
    wearable = WearableController(protocol=WearableProtocol.BLE, num_wristbands=200)
    wearable.set_all(color_hex="#FF4444", fade_ms=500)
    wearable.set_zone("orchestra_center", color_hex="#00FF00")
    wearable.ripple_effect(center_zone="orchestra_center", color_hex="#0044FF", speed_mps=5.0)
    wearable.wave_effect(color_hex="#FFFF00", direction="left_to_right")
    wearable.send_haptic(zone="orchestra_left", intensity=0.8, pattern="double")
    print(f"Wristband zones: {wearable.get_zone_counts()}")

    # --- Sentiment Tracking ---
    sentiment = SentimentTracker()
    for _ in range(20):
        sentiment.record(random.choice(list(SentimentValue)))
    print(f"Sentiment: avg={sentiment.get_current_average():.2f}, trend={sentiment.get_trend()}, label={sentiment.get_sentiment_label()}")
    sentiment.export_data("/tmp/sentiment.json")

    # --- Pre-Show ---
    preshow = PreShowEngagement(session)
    preshow.add_trivia("Who wrote Hamilton?", ["Lin-Manuel Miranda", "Stephen Sondheim", "Andrew Lloyd Webber"], 0)
    preshow.add_trivia("What year did Hamilton premiere?", ["2013", "2015", "2017"], 1)
    preshow.set_countdown(time.time() + 900)
    trivia = preshow.launch_trivia_round()
    remaining = preshow.get_countdown_remaining()
    print(f"Trivia launched: {trivia['poll_id']}, countdown remaining: {remaining:.0f}s")

    # --- Session Events ---
    events = session.get_events(EngagementEventType.POLL_RESPONSE)
    print(f"Total poll response events: {len(events)}")

    server.stop()
    print("\nDemo complete.")


if __name__ == "__main__":
    main()
