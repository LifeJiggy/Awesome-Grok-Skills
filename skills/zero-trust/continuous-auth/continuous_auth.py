"""
Continuous Authentication & Session Monitoring Module

Real-time session monitoring, behavioral biometrics, anomaly-based access
revocation, step-up authentication triggers, device fingerprinting, and
location-based risk signal analysis for zero trust environments.
"""

from __future__ import annotations

import hashlib
import math
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SessionStatus(Enum):
    ACTIVE = "active"
    STEP_UP_REQUIRED = "step_up_required"
    RESTRICTED = "restricted"
    REVOKED = "revoked"
    EXPIRED = "expired"


class ResponseAction(Enum):
    NONE = "none"
    INCREASE_MONITORING = "increase_monitoring"
    STEP_UP_AUTH = "step_up_auth"
    RESTRICT_ACCESS = "restrict_access"
    REVOKE_SESSION = "revoke_session"


@dataclass
class BehavioralSample:
    sample_type: str
    timestamp: float
    data: dict[str, Any]
    session_id: str = ""


@dataclass
class KeystrokeDynamics:
    timing_data: list[float]
    dwell_times: list[float]
    flight_times: list[float] = field(default_factory=list)
    error_rate: float = 0.0

    @property
    def mean_timing(self) -> float:
        return sum(self.timing_data) / len(self.timing_data) if self.timing_data else 0.0

    @property
    def std_timing(self) -> float:
        if len(self.timing_data) < 2:
            return 0.0
        mean = self.mean_timing
        variance = sum((t - mean) ** 2 for t in self.timing_data) / (
            len(self.timing_data) - 1
        )
        return math.sqrt(variance)

    @property
    def mean_dwell(self) -> float:
        return sum(self.dwell_times) / len(self.dwell_times) if self.dwell_times else 0.0


@dataclass
class MouseMovement:
    trajectory_points: list[tuple[float, float]]
    velocities: list[float]
    acceleration: list[float] = field(default_factory=list)
    click_positions: list[tuple[float, float]] = field(default_factory=list)

    @property
    def mean_velocity(self) -> float:
        return sum(self.velocities) / len(self.velocities) if self.velocities else 0.0

    @property
    def max_velocity(self) -> float:
        return max(self.velocities) if self.velocities else 0.0

    @property
    def trajectory_length(self) -> float:
        if len(self.trajectory_points) < 2:
            return 0.0
        total = 0.0
        for i in range(1, len(self.trajectory_points)):
            dx = self.trajectory_points[i][0] - self.trajectory_points[i - 1][0]
            dy = self.trajectory_points[i][1] - self.trajectory_points[i - 1][1]
            total += math.sqrt(dx * dx + dy * dy)
        return total


@dataclass
class DeviceFingerprint:
    device_id: str
    user_agent: str
    screen_resolution: tuple[int, int]
    timezone: str
    language: str
    platform: str
    plugins: list[str] = field(default_factory=list)
    hardware_concurrency: int = 0
    device_memory: int = 0
    is_jailbroken: bool = False
    security_controls: dict[str, bool] = field(default_factory=dict)
    fingerprint_hash: str = ""

    def __post_init__(self) -> None:
        if not self.fingerprint_hash:
            raw = f"{self.user_agent}:{self.screen_resolution}:{self.timezone}:{self.platform}"
            self.fingerprint_hash = hashlib.sha256(raw.encode()).hexdigest()[:32]


@dataclass
class LocationSignal:
    ip_address: str
    latitude: float
    longitude: float
    country: str
    city: str
    is_vpn: bool = False
    is_tor: bool = False
    is_proxy: bool = False
    timestamp: float = field(default_factory=time.time)
    accuracy_meters: float = 100.0

    @property
    def is_risky_network(self) -> bool:
        return self.is_vpn or self.is_tor or self.is_proxy


@dataclass
class TimeSignal:
    hour_of_day: int
    day_of_week: int
    is_business_hours: bool
    timezone_offset: int = 0
    timestamp: float = field(default_factory=time.time)


@dataclass
class RiskAssessment:
    score: float
    level: RiskLevel
    recommended_action: ResponseAction
    behavioral_deviation: float
    device_risk: float
    location_risk: float
    time_risk: float
    contributing_factors: list[str]
    assessed_at: float = field(default_factory=time.time)


@dataclass
class SessionRiskScore:
    overall: float
    behavioral: float
    device: float
    location: float
    time: float
    factors: list[str] = field(default_factory=list)


@dataclass
class AuthSession:
    session_id: str
    user_id: str
    device_id: str
    ip_address: str
    resource: str
    trust_level: float
    risk_score: float = 0.0
    status: SessionStatus = SessionStatus.ACTIVE
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    base_timeout: int = 3600
    step_up_count: int = 0
    behavioral_samples: list[BehavioralSample] = field(default_factory=list)
    location_history: list[LocationSignal] = field(default_factory=list)

    @property
    def effective_timeout(self) -> int:
        risk_multiplier = max(0.2, 1.0 - self.risk_score)
        return int(self.base_timeout * risk_multiplier)

    @property
    def is_expired(self) -> bool:
        return (time.time() - self.last_activity) > self.effective_timeout

    @property
    def session_duration(self) -> float:
        return time.time() - self.created_at


class BehavioralAnalyzer:
    def __init__(self) -> None:
        self._baselines: dict[str, dict[str, Any]] = {}
        self._samples: dict[str, deque] = {}

    def establish_baseline(
        self,
        user_id: str,
        keystroke_dynamics: KeystrokeDynamics | None = None,
        mouse_movement: MouseMovement | None = None,
    ) -> None:
        baseline: dict[str, Any] = {}
        if keystroke_dynamics:
            baseline["keystroke_mean_timing"] = keystroke_dynamics.mean_timing
            baseline["keystroke_std_timing"] = keystroke_dynamics.std_timing
            baseline["keystroke_mean_dwell"] = keystroke_dynamics.mean_dwell
        if mouse_movement:
            baseline["mouse_mean_velocity"] = mouse_movement.mean_velocity
            baseline["mouse_trajectory_length"] = mouse_movement.trajectory_length
        baseline["established_at"] = time.time()
        self._baselines[user_id] = baseline

    def add_sample(self, session_id: str, sample: BehavioralSample) -> None:
        if session_id not in self._samples:
            self._samples[session_id] = deque(maxlen=100)
        self._samples[session_id].append(sample)

    def compute_deviation(
        self, user_id: str, current: KeystrokeDynamics | None = None
    ) -> float:
        baseline = self._baselines.get(user_id)
        if not baseline or not current:
            return 0.0

        deviation = 0.0
        count = 0

        if "keystroke_mean_timing" in baseline and current.mean_timing > 0:
            bl_mean = baseline["keystroke_mean_timing"]
            if bl_mean > 0:
                deviation += abs(current.mean_timing - bl_mean) / bl_mean
                count += 1

        if "keystroke_std_timing" in baseline and current.std_timing > 0:
            bl_std = baseline["keystroke_std_timing"]
            if bl_std > 0:
                deviation += abs(current.std_timing - bl_std) / bl_std
                count += 1

        return min(deviation / max(count, 1), 1.0)

    def has_baseline(self, user_id: str) -> bool:
        return user_id in self._baselines


class DeviceAnalyzer:
    def __init__(self) -> None:
        self._known_devices: dict[str, dict[str, Any]] = {}

    def register_device(
        self, user_id: str, fingerprint: DeviceFingerprint
    ) -> None:
        if user_id not in self._known_devices:
            self._known_devices[user_id] = {}
        self._known_devices[user_id][fingerprint.fingerprint_hash] = {
            "first_seen": time.time(),
            "last_seen": time.time(),
        }

    def compute_risk(
        self, user_id: str, fingerprint: DeviceFingerprint
    ) -> tuple[float, list[str]]:
        risk = 0.0
        factors: list[str] = []

        if fingerprint.is_jailbroken:
            risk += 0.4
            factors.append("device_jailbroken")

        security_checks = fingerprint.security_controls
        if not security_checks.get("disk_encryption", True):
            risk += 0.15
            factors.append("disk_encryption_disabled")
        if not security_checks.get("screen_lock", True):
            risk += 0.1
            factors.append("screen_lock_disabled")
        if not security_checks.get("antivirus", False):
            risk += 0.05
            factors.append("antivirus_not_detected")

        user_devices = self._known_devices.get(user_id, {})
        if fingerprint.fingerprint_hash not in user_devices:
            risk += 0.2
            factors.append("unknown_device")

        return min(risk, 1.0), factors

    def update_last_seen(self, user_id: str, fingerprint_hash: str) -> None:
        devices = self._known_devices.get(user_id, {})
        if fingerprint_hash in devices:
            devices[fingerprint_hash]["last_seen"] = time.time()


class LocationAnalyzer:
    EARTH_RADIUS_KM = 6371.0
    MAX_SPEED_KMH = 1000.0

    def __init__(self) -> None:
        self._location_history: dict[str, list[LocationSignal]] = {}

    def add_location(self, user_id: str, location: LocationSignal) -> None:
        if user_id not in self._location_history:
            self._location_history[user_id] = []
        self._location_history[user_id].append(location)

    def compute_risk(
        self, user_id: str, current: LocationSignal
    ) -> tuple[float, list[str]]:
        risk = 0.0
        factors: list[str] = []

        if current.is_risky_network:
            risk += 0.2
            factors.append("risky_network")

        history = self._location_history.get(user_id, [])
        if history:
            last = history[-1]
            distance = self._haversine(
                last.latitude, last.longitude,
                current.latitude, current.longitude,
            )
            time_diff_hours = (current.timestamp - last.timestamp) / 3600

            if time_diff_hours > 0:
                speed = distance / time_diff_hours
                if speed > self.MAX_SPEED_KMH and distance > 100:
                    risk += 0.5
                    factors.append("impossible_travel")

            if current.country != last.country:
                risk += 0.1
                factors.append("country_change")

        return min(risk, 1.0), factors

    def _haversine(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        return self.EARTH_RADIUS_KM * c


class TimeAnalyzer:
    BUSINESS_HOURS_START = 8
    BUSINESS_HOURS_END = 18

    def compute_risk(self, signal: TimeSignal) -> tuple[float, list[str]]:
        risk = 0.0
        factors: list[str] = []

        if not signal.is_business_hours:
            risk += 0.15
            factors.append("outside_business_hours")

        if signal.hour_of_day < 6 or signal.hour_of_day > 22:
            risk += 0.1
            factors.append("unusual_hour")

        if signal.day_of_week >= 5:
            risk += 0.05
            factors.append("weekend_access")

        return min(risk, 1.0), factors


class ContinuousAuthEngine:
    def __init__(
        self,
        risk_threshold_low: float = 0.3,
        risk_threshold_medium: float = 0.6,
        risk_threshold_high: float = 0.85,
        session_timeout_base: int = 3600,
        behavioral_analysis_enabled: bool = True,
    ):
        self.risk_threshold_low = risk_threshold_low
        self.risk_threshold_medium = risk_threshold_medium
        self.risk_threshold_high = risk_threshold_high
        self.session_timeout_base = session_timeout_base
        self.behavioral_enabled = behavioral_analysis_enabled

        self._sessions: dict[str, AuthSession] = {}
        self._behavioral = BehavioralAnalyzer()
        self._device = DeviceAnalyzer()
        self._location = LocationAnalyzer()
        self._time = TimeAnalyzer()
        self._events: list[dict[str, Any]] = []

    def create_session(
        self,
        user_id: str,
        device_id: str,
        ip_address: str,
        resource: str,
        trust_level: float = 0.7,
    ) -> AuthSession:
        session = AuthSession(
            session_id=uuid.uuid4().hex[:16],
            user_id=user_id,
            device_id=device_id,
            ip_address=ip_address,
            resource=resource,
            trust_level=trust_level,
            base_timeout=self.session_timeout_base,
        )
        self._sessions[session.session_id] = session
        self._log_event("session_created", session.session_id, {"user_id": user_id})
        return session

    def record_keystroke_dynamics(
        self,
        session_id: str,
        timing_data: list[float],
        dwell_times: list[float],
    ) -> None:
        session = self._get_session(session_id)
        dynamics = KeystrokeDynamics(timing_data=timing_data, dwell_times=dwell_times)

        sample = BehavioralSample(
            sample_type="keystroke",
            timestamp=time.time(),
            data={
                "mean_timing": dynamics.mean_timing,
                "std_timing": dynamics.std_timing,
                "mean_dwell": dynamics.mean_dwell,
            },
            session_id=session_id,
        )
        self._behavioral.add_sample(session_id, sample)
        self._update_risk_from_behavioral(session, dynamics)

    def record_mouse_movement(
        self,
        session_id: str,
        trajectory_points: list[tuple[float, float]],
        velocities: list[float],
    ) -> None:
        session = self._get_session(session_id)
        movement = MouseMovement(
            trajectory_points=trajectory_points, velocities=velocities
        )

        sample = BehavioralSample(
            sample_type="mouse",
            timestamp=time.time(),
            data={
                "mean_velocity": movement.mean_velocity,
                "trajectory_length": movement.trajectory_length,
                "point_count": len(trajectory_points),
            },
            session_id=session_id,
        )
        self._behavioral.add_sample(session_id, sample)
        session.last_activity = time.time()

    def update_device_fingerprint(
        self, session_id: str, fingerprint: DeviceFingerprint
    ) -> None:
        session = self._get_session(session_id)
        risk, factors = self._device.compute_risk(session.user_id, fingerprint)
        session.risk_score = min(session.risk_score + risk * 0.3, 1.0)
        self._device.register_device(session.user_id, fingerprint)

        if risk > 0.3:
            self._log_event(
                "device_risk_detected",
                session_id,
                {"risk": risk, "factors": factors},
            )

    def update_location(self, session_id: str, location: LocationSignal) -> None:
        session = self._get_session(session_id)
        risk, factors = self._location.compute_risk(session.user_id, location)
        self._location.add_location(session.user_id, location)
        session.location_history.append(location)
        session.risk_score = min(session.risk_score + risk * 0.3, 1.0)

        if risk > 0.3:
            self._log_event(
                "location_risk_detected",
                session_id,
                {"risk": risk, "factors": factors},
            )

    def evaluate_session_risk(self, session_id: str) -> RiskAssessment:
        session = self._get_session(session_id)

        time_signal = TimeSignal(
            hour_of_day=int(time.strftime("%H")),
            day_of_week=int(time.strftime("%w")),
            is_business_hours=self.BUSINESS_HOURS_START
            <= int(time.strftime("%H"))
            <= self.BUSINESS_HOURS_END,
        )
        time_risk, time_factors = self._time.compute_risk(time_signal)

        overall_score = session.risk_score
        level = self._score_to_level(overall_score)
        action = self._level_to_action(level)

        behavioral_deviation = 0.0
        if session.behavioral_samples:
            last_keystroke = None
            for s in reversed(session.behavioral_samples):
                if s.sample_type == "keystroke":
                    last_keystroke = KeystrokeDynamics(
                        timing_data=[s.data.get("mean_timing", 0)],
                        dwell_times=[s.data.get("mean_dwell", 0)],
                    )
                    break
            if last_keystroke:
                behavioral_deviation = self._behavioral.compute_deviation(
                    session.user_id, last_keystroke
                )

        all_factors = time_factors
        if overall_score > 0.5:
            all_factors.append("elevated_overall_risk")

        assessment = RiskAssessment(
            score=overall_score,
            level=level,
            recommended_action=action,
            behavioral_deviation=behavioral_deviation,
            device_risk=min(overall_score * 0.8, 1.0),
            location_risk=min(overall_score * 0.6, 1.0),
            time_risk=time_risk,
            contributing_factors=all_factors,
        )

        self._apply_response(session, action)
        return assessment

    def trigger_step_up_auth(
        self,
        session_id: str,
        required_method: str = "fido2",
        reason: str = "risk_threshold_exceeded",
    ) -> dict[str, Any]:
        session = self._get_session(session_id)
        session.status = SessionStatus.STEP_UP_REQUIRED
        session.step_up_count += 1

        self._log_event(
            "step_up_triggered",
            session_id,
            {"method": required_method, "reason": reason},
        )

        return {
            "session_id": session_id,
            "required_method": required_method,
            "reason": reason,
            "step_up_count": session.step_up_count,
        }

    def get_session_status(self, session_id: str) -> dict[str, Any]:
        session = self._sessions.get(session_id)
        if not session:
            return {"error": "session_not_found"}
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "status": session.status.value,
            "risk_score": round(session.risk_score, 3),
            "session_duration": round(session.session_duration, 1),
            "effective_timeout": session.effective_timeout,
            "is_expired": session.is_expired,
            "step_up_count": session.step_up_count,
        }

    def revoke_session(self, session_id: str, reason: str) -> dict[str, Any]:
        session = self._get_session(session_id)
        session.status = SessionStatus.REVOKED
        self._log_event("session_revoked", session_id, {"reason": reason})
        return {"session_id": session_id, "status": "revoked", "reason": reason}

    def get_events(
        self, session_id: str | None = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        events = self._events
        if session_id:
            events = [e for e in events if e.get("session_id") == session_id]
        return events[-limit:]

    def _get_session(self, session_id: str) -> AuthSession:
        session = self._sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        if session.status == SessionStatus.REVOKED:
            raise ValueError(f"Session {session_id} has been revoked")
        return session

    def _update_risk_from_behavioral(
        self, session: AuthSession, dynamics: KeystrokeDynamics
    ) -> None:
        deviation = self._behavioral.compute_deviation(session.user_id, dynamics)
        session.risk_score = min(session.risk_score + deviation * 0.2, 1.0)
        session.last_activity = time.time()

    def _score_to_level(self, score: float) -> RiskLevel:
        if score >= self.risk_threshold_high:
            return RiskLevel.CRITICAL
        elif score >= self.risk_threshold_medium:
            return RiskLevel.HIGH
        elif score >= self.risk_threshold_low:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _level_to_action(self, level: RiskLevel) -> ResponseAction:
        mapping = {
            RiskLevel.LOW: ResponseAction.NONE,
            RiskLevel.MEDIUM: ResponseAction.INCREASE_MONITORING,
            RiskLevel.HIGH: ResponseAction.STEP_UP_AUTH,
            RiskLevel.CRITICAL: ResponseAction.REVOKE_SESSION,
        }
        return mapping.get(level, ResponseAction.NONE)

    def _apply_response(
        self, session: AuthSession, action: ResponseAction
    ) -> None:
        if action == ResponseAction.STEP_UP_AUTH:
            session.status = SessionStatus.STEP_UP_REQUIRED
        elif action == ResponseAction.REVOKE_SESSION:
            session.status = SessionStatus.REVOKED
        elif action == ResponseAction.RESTRICT_ACCESS:
            session.status = SessionStatus.RESTRICTED

    def _log_event(
        self, event_type: str, session_id: str, data: dict[str, Any]
    ) -> None:
        self._events.append({
            "event_type": event_type,
            "session_id": session_id,
            "timestamp": time.time(),
            "data": data,
        })


def main() -> None:
    print("=" * 60)
    print("Continuous Authentication Module — Demo")
    print("=" * 60)

    engine = ContinuousAuthEngine(
        risk_threshold_low=0.3,
        risk_threshold_medium=0.6,
        risk_threshold_high=0.85,
        session_timeout_base=3600,
    )

    session = engine.create_session(
        user_id="user:alice@corp.com",
        device_id="dev-laptop-042",
        ip_address="192.168.1.100",
        resource="api-payments-001",
        trust_level=0.90,
    )
    print(f"\nSession created: {session.session_id}")
    print(f"  Base timeout: {session.base_timeout}s")

    engine.record_keystroke_dynamics(
        session_id=session.session_id,
        timing_data=[0.08, 0.12, 0.05, 0.09, 0.11, 0.07, 0.06, 0.10],
        dwell_times=[0.04, 0.06, 0.03, 0.05, 0.06, 0.04, 0.03, 0.05],
    )

    engine.record_mouse_movement(
        session_id=session.session_id,
        trajectory_points=[(100, 200), (150, 220), (200, 210), (250, 250)],
        velocities=[12.5, 8.3, 10.1, 15.2],
    )
    print(f"\nBehavioral signals recorded.")

    fingerprint = DeviceFingerprint(
        device_id="dev-laptop-042",
        user_agent="Mozilla/5.0 Chrome/120.0",
        screen_resolution=(1920, 1080),
        timezone="America/New_York",
        language="en-US",
        platform="Windows",
        security_controls={"disk_encryption": True, "screen_lock": True, "antivirus": True},
    )
    engine.update_device_fingerprint(session.session_id, fingerprint)

    location = LocationSignal(
        ip_address="192.168.1.100",
        latitude=40.7128,
        longitude=-74.0060,
        country="US",
        city="New York",
    )
    engine.update_location(session.session_id, location)

    risk = engine.evaluate_session_risk(session.session_id)
    print(f"\nRisk Assessment:")
    print(f"  Score: {risk.score:.3f}")
    print(f"  Level: {risk.level.value}")
    print(f"  Action: {risk.recommended_action.value}")
    print(f"  Behavioral deviation: {risk.behavioral_deviation:.3f}")
    print(f"  Factors: {risk.contributing_factors}")

    distant_location = LocationSignal(
        ip_address="203.0.113.50",
        latitude=51.5074,
        longitude=-0.1278,
        country="GB",
        city="London",
        timestamp=time.time() + 3600,
    )
    engine.update_location(session.session_id, distant_location)

    risk2 = engine.evaluate_session_risk(session.session_id)
    print(f"\nPost-location-change Risk:")
    print(f"  Score: {risk2.score:.3f}")
    print(f"  Level: {risk2.level.value}")
    print(f"  Action: {risk2.recommended_action.value}")
    print(f"  Factors: {risk2.contributing_factors}")

    status = engine.get_session_status(session.session_id)
    print(f"\nSession Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")

    events = engine.get_events(session.session_id)
    print(f"\nSession Events ({len(events)} total):")
    for evt in events:
        print(f"  [{evt['event_type']}] {evt['data']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
