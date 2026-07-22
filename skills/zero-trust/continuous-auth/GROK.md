---
name: "continuous-auth"
category: "zero-trust"
version: "1.0.0"
tags: ["zero-trust", "continuous-auth", "behavioral-biometrics", "session-security"]
---

# Continuous Authentication & Session Monitoring

## Overview

The Continuous Authentication module implements real-time session monitoring,
behavioral biometrics, and anomaly-based access revocation for zero trust
environments. Unlike traditional authentication that verifies identity at login
and trusts the session thereafter, continuous authentication treats every
interaction as an implicit re-verification opportunity. The module monitors user
behavior, device signals, location patterns, and session risk throughout the
access lifetime, enabling dynamic access adjustments including step-up
authentication, session restriction, or immediate revocation.

Behavioral biometrics form the core of continuous verification. Keystroke
dynamics, mouse movement patterns, touchscreen gestures, and navigation behavior
create a unique behavioral fingerprint that is compared against the user's
established baseline. Deviations from this baseline increase the session risk
score, which triggers graduated responses: additional verification prompts,
reduced session privileges, or session termination. The system adapts its
sensitivity based on resource classification — accessing a confidential database
triggers stricter behavioral monitoring than browsing internal documentation.

Device fingerprinting provides a parallel trust signal. The module continuously
validates device health, checks for jailbreak or root indicators, monitors for
unauthorized software installation, and verifies that security controls (disk
encryption, screen lock, antivirus) remain active. Location-based risk signals
detect impossible travel (login from geographically distant locations within
impossible timeframes), unusual access patterns, and connections from known
risky networks. Time-based access patterns identify after-hours access, weekend
anomalies, and deviations from established work schedules.

## Core Capabilities

- Real-time behavioral biometrics with keystroke dynamics, mouse movement, and
  gesture analysis
- Session risk scoring with graduated response thresholds (step-up, restrict,
  revoke)
- Device fingerprinting with continuous health and posture validation
- Impossible travel detection and location-based risk signal analysis
- Time-based access pattern analysis and anomaly detection
- Step-up authentication triggers based on risk score escalation
- Session lifetime management with dynamic timeout adjustment
- Anomaly-based access revocation with configurable response playbooks

## Risk Signal Categories

**Behavioral Signals** — Derived from user interaction patterns:

- Keystroke dynamics: typing speed, dwell time, flight time between keys
- Mouse movement: velocity, trajectory, click patterns
- Touch gestures: swipe speed, pressure, contact area
- Navigation: page access patterns, scroll behavior, tab switching

**Device Signals** — Derived from the endpoint:

- Device identity and registration status
- OS version and patch level
- Security control status (encryption, antivirus, firewall)
- Jailbreak/root detection
- Browser fingerprint stability

**Network Signals** — Derived from the connection:

- IP geolocation and reputation
- VPN/Tor/proxy detection
- Network type (corporate, public Wi-Fi, cellular)
- DNS configuration anomalies

**Temporal Signals** — Derived from access patterns:

- Time of day vs. user's normal schedule
- Day of week vs. user's work pattern
- Session duration anomalies
- Access frequency deviations

## Session Risk Scoring

The session risk score is a composite value between 0.0 and 1.0 that represents
the overall risk of the current session:

```
risk_score = w_b * behavioral_deviation
           + w_d * device_risk
           + w_l * location_risk
           + w_t * time_risk
```

Where w_b, w_d, w_l, w_t are configurable weights that sum to 1.0.

Risk thresholds and responses:

| Score Range | Level | Response |
|------------|-------|----------|
| 0.0 - 0.3 | Low | Normal access, increased logging |
| 0.3 - 0.6 | Medium | Enhanced monitoring, optional step-up |
| 0.6 - 0.85 | High | Step-up authentication required |
| 0.85 - 1.0 | Critical | Session revocation |

## Usage Examples

```python
from continuous_auth import ContinuousAuthEngine, BehavioralBaseline, RiskSignal

# Initialize the continuous authentication engine
engine = ContinuousAuthEngine(
    risk_threshold_low=0.3,
    risk_threshold_medium=0.6,
    risk_threshold_high=0.85,
    session_timeout_base=3600,
    behavioral_analysis_enabled=True,
)

# Create a monitored session
session = engine.create_session(
    user_id="user:alice@corp.com",
    device_id="dev-laptop-042",
    ip_address="192.168.1.100",
    resource="api-payments-001",
    trust_level=0.90,
)

print(f"Session: {session.session_id}")
print(f"  Initial risk score: {session.risk_score:.2f}")
print(f"  Timeout: {session.effective_timeout}s")
```

```python
# Feed behavioral signals
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

# Check session risk
risk = engine.evaluate_session_risk(session.session_id)
print(f"\nRisk evaluation:")
print(f"  Risk score: {risk.score:.2f}")
print(f"  Risk level: {risk.level}")
print(f"  Recommended action: {risk.recommended_action}")
print(f"  Behavioral deviation: {risk.behavioral_deviation:.3f}")

# Handle step-up trigger
if risk.level == "high":
    engine.trigger_step_up_auth(
        session_id=session.session_id,
        required_method="fido2",
        reason="behavioral_anomaly_detected",
    )
```

```python
# Update device fingerprint for continuous validation
from continuous_auth import DeviceFingerprint

fingerprint = DeviceFingerprint(
    device_id="dev-laptop-042",
    user_agent="Mozilla/5.0 Chrome/120.0",
    screen_resolution=(1920, 1080),
    timezone="America/New_York",
    language="en-US",
    platform="Windows",
    security_controls={
        "disk_encryption": True,
        "screen_lock": True,
        "antivirus": True,
    },
)
engine.update_device_fingerprint(session.session_id, fingerprint)

# Update location for impossible travel detection
from continuous_auth import LocationSignal

location = LocationSignal(
    ip_address="192.168.1.100",
    latitude=40.7128,
    longitude=-74.0060,
    country="US",
    city="New York",
)
engine.update_location(session.session_id, location)

# Get session status
status = engine.get_session_status(session.session_id)
for key, value in status.items():
    print(f"  {key}: {value}")
```

## Step-Up Authentication Triggers

When the risk score crosses a threshold, the engine triggers step-up
authentication. The trigger configuration determines which method is required:

```python
# Configure step-up triggers
engine.trigger_step_up_auth(
    session_id=session.session_id,
    required_method="fido2",
    reason="behavioral_anomaly_detected",
)
```

Step-up methods ranked by assurance:
1. FIDO2/WebAuthn — Highest assurance, phishing-resistant
2. Biometric (face/fingerprint) — Strong with liveness detection
3. Push notification — Medium assurance with user confirmation
4. TOTP — Standard MFA, time-based
5. Backup code — Emergency recovery method

## Best Practices

- **Baseline before monitoring**: Establish a behavioral baseline during the
  first 5-10 interactions before enabling anomaly detection. Insufficient
  baseline data causes false positives that degrade user experience.

- **Calibrate sensitivity per resource**: Apply stricter monitoring thresholds
  for high-value resources (financial data, PII) and looser thresholds for
  low-risk resources (internal wiki, documentation). One-size-fits-all
  sensitivity creates either too many false positives or missed threats.

- **Use graduated responses**: Avoid binary allow/deny decisions from continuous
  auth. Implement a gradient: increase monitoring at low risk, prompt for
  step-up at medium risk, restrict access at high risk, and revoke only at
  critical risk.

- **Combine behavioral + device signals**: Behavioral biometrics alone can be
  fooled by sophisticated attackers. Always combine with device fingerprinting,
  location signals, and network context for a composite risk assessment.

- **Minimize user friction**: Step-up authentication should be triggered only
  when the risk score crosses meaningful thresholds. Over-triggering causes auth
  fatigue where users approve prompts without scrutiny.

- **Handle edge cases gracefully**: Account for legitimate behavioral changes —
  new keyboard, injured hand, shared workstation. Provide self-service baseline
  reset and allow users to explain anomalies before revoking access.

- **Log all risk transitions**: Every change in session risk level should be
  logged with the signals that caused the transition. This creates an audit
  trail for incident response and supports tuning of detection thresholds.

- **Consider network-aware timeouts**: Sessions on untrusted networks (public
  Wi-Fi, hotel networks) should have shorter timeouts than sessions on corporate
  networks. Adjust session lifetime based on network trust level.

## Session Lifecycle

1. **Created** — Session established after initial authentication
2. **Active** — Normal operation, behavioral signals collected
3. **Monitoring** — Risk score elevated, enhanced signal collection
4. **Step-Up Required** — Risk threshold crossed, re-verification needed
5. **Restricted** — Access limited to read-only or specific resources
6. **Revoked** — Session terminated due to critical risk
7. **Expired** — Session timed out due to inactivity

## Related Modules

- [identity-verification](../identity-verification/GROK.md) — Initial identity
  verification and MFA
- [security-framework](../security-framework/GROK.md) — Trust engine and policy
  decisions
- [policy-engine](../policy-engine/GROK.md) — Access control policy enforcement
- [micro-segmentation](../micro-segmentation/GROK.md) — Network-level access
  controls

---

## Advanced Configuration

### Behavioral Baseline Tuning

```python
from continuous_auth import BaselineConfig

baseline_config = BaselineConfig(
    keystroke_model="rnn",
    mouse_model="cnn",
    min_samples=50,
    calibration_window_hours=24,
    drift_threshold=0.15,
    adaptive_sensitivity=True,
)
```

### Risk Score Weights

```python
from continuous_auth import RiskWeights

weights = RiskWeights(
    behavioral=0.35,
    device=0.25,
    location=0.20,
    temporal=0.10,
    network=0.10,
)
```

## Architecture Patterns

### Continuous Auth Pipeline

```
Session Active → Signal Collection → Risk Evaluation → Response → Session Update
```

### Graduated Response Model

```
Low Risk (0.0-0.3) → Normal access, enhanced logging
Medium Risk (0.3-0.6) → Enhanced monitoring
High Risk (0.6-0.85) → Step-up authentication
Critical Risk (0.85-1.0) → Session revocation
```

## Integration Guide

### IdP Integration

```python
from continuous_auth import IdPIntegration

idp = IdPIntegration(provider="okta")
engine.register_idp(idp)
engine.on_step_up_trigger(idp.trigger_mfa)
```

### SIEM Integration

```python
from continuous_auth import SIEMExporter

siem = SIEMExporter(provider="splunk")
engine.export_risk_events(siem)
engine.export_session_transitions(siem)
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Local behavioral analysis | <10ms per signal evaluation |
| Batched signal processing | 100x throughput |
| Risk score caching | Skip recomputation |
| Async device validation | Non-blocking checks |

## Security Considerations

- **Baseline before monitoring**: Collect 50+ samples
- **Combine signals**: Behavioral alone is insufficient
- **Minimize friction**: Only step-up on meaningful risk
- **Handle edge cases**: New keyboard, injury, shared workstation
- **Log all transitions**: Full audit trail

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Too many false positives | Sensitivity too high | Increase min_samples |
| Step-up auth fatigue | Threshold too low | Raise risk_threshold_medium |
| Impossible travel false positive | VPN usage | Whitelist corporate VPN IPs |
| Session timeout too short | Aggressive timeout | Increase session_timeout_base |

## API Reference

### ContinuousAuthEngine

```python
class ContinuousAuthEngine:
    def __init__(self, risk_threshold_low: float, risk_threshold_medium: float, risk_threshold_high: float, session_timeout_base: int)
    def create_session(self, user_id: str, device_id: str, ip_address: str, resource: str, trust_level: float) -> Session
    def record_keystroke_dynamics(self, session_id: str, timing_data: list, dwell_times: list) -> None
    def evaluate_session_risk(self, session_id: str) -> RiskAssessment
    def trigger_step_up_auth(self, session_id: str, required_method: str, reason: str) -> None
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class RiskAssessment:
    score: float
    level: str
    recommended_action: str
    behavioral_deviation: float
    device_risk: float

@dataclass
class Session:
    session_id: str
    user_id: str
    risk_score: float
    effective_timeout: int
    created_at: float
```

## Deployment Guide

### Installation

```bash
pip install continuous-auth
```

### Rollout Strategy

1. Deploy in monitoring-only mode (2 weeks)
2. Tune sensitivity based on false positive rate
3. Enable step-up triggers for high-risk resources
4. Enable revocation for critical-risk
5. Monitor user friction metrics

## Monitoring & Observability

```python
from continuous_auth import MetricsCollector

collector = MetricsCollector()
collector.gauge("session.risk.score", score, tags={"user": user_id})
collector.counter("session.step_up.triggered", count, tags={"reason": reason})
collector.counter("session.revoked", count, tags={"reason": reason})
collector.histogram("session.duration_minutes", duration)
```

## Testing Strategy

```python
import pytest
from continuous_auth import ContinuousAuthEngine

def test_session_creation():
    engine = ContinuousAuthEngine(risk_threshold_low=0.3, risk_threshold_medium=0.6, risk_threshold_high=0.85, session_timeout_base=3600)
    session = engine.create_session("user:alice", "dev-001", "192.168.1.1", "api-test", 0.90)
    assert session.risk_score < 0.3
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added device fingerprinting | Enable device validation |
| 2.0.0 | New risk model | Recalibrate thresholds |

## Glossary

| Term | Definition |
|------|-----------|
| **Behavioral Biometrics** | Authentication from interaction patterns |
| **Impossible Travel** | Login from distant locations in short time |
| **Step-Up Auth** | Additional verification triggered by risk |
| **Risk Score** | Composite value 0.0-1.0 representing session risk |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with behavioral biometrics
- Session risk scoring
- Step-up authentication triggers
- Device fingerprinting

## Contributing Guidelines

```bash
git clone https://github.com/example/continuous-auth.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Behavioral Signal Reference

| Signal | Measurement | Baseline Period | Anomaly Threshold |
|--------|------------|-----------------|-------------------|
| Keystroke dynamics | Timing, dwell, flight | 50+ samples | > 2σ deviation |
| Mouse movement | Velocity, trajectory | 100+ movements | > 2.5σ deviation |
| Touch gestures | Pressure, speed, area | 30+ gestures | > 2σ deviation |
| Navigation | Page flow, scroll | 20+ pages | Deviation from common paths |
| Session duration | Time per session | 10+ sessions | > 3σ deviation |

### Risk Score Components

| Component | Weight | Calculation | Range |
|-----------|--------|-------------|-------|
| Behavioral deviation | 0.35 | Distance from baseline | 0.0-1.0 |
| Device risk | 0.25 | Health + compliance | 0.0-1.0 |
| Location risk | 0.20 | Geo-anomaly score | 0.0-1.0 |
| Temporal risk | 0.10 | Time-of-day deviation | 0.0-1.0 |
| Network risk | 0.10 | Network trust level | 0.0-1.0 |

### Step-Up Authentication Methods

| Method | Assurance | User Friction | Use Case |
|--------|-----------|---------------|----------|
| Push notification | Medium | Low | General step-up |
| TOTP code | Medium | Medium | Standard MFA |
| Biometric | High | Low | High-security |
| FIDO2 | Very High | Low | Critical operations |
| Backup code | High | Medium | Recovery |

### Device Fingerprint Components

| Component | Stability | Uniqueness | Collection |
|-----------|----------|------------|------------|
| User-Agent | High | Low | HTTP header |
| Screen resolution | High | Medium | JavaScript |
| Timezone | High | Low | JavaScript |
| Language | High | Low | HTTP header |
| Platform | High | Low | JavaScript |
| Plugins | Medium | High | JavaScript |
| Canvas fingerprint | High | Very High | Canvas API |
| WebGL fingerprint | High | Very High | WebGL API |

### Impossible Travel Detection

| Speed Threshold | Distance | Time | Action |
|----------------|----------|------|--------|
| > 900 km/h | > 1000 km | < 1 hour | Alert + step-up |
| > 500 km/h | > 500 km | < 1 hour | Alert |
| > 200 km/h | > 200 km | < 1 hour | Monitor |

### Session Lifecycle States

| State | Description | Duration | Transition |
|-------|-------------|----------|------------|
| Created | Initial authentication | — | → Active |
| Active | Normal operation | Until risk | → Monitoring, → Step-Up |
| Monitoring | Enhanced observation | Until resolution | → Active, → Step-Up |
| Step-Up Required | Re-verification needed | Until verify | → Active, → Restricted |
| Restricted | Limited access | Until verify | → Active, → Revoked |
| Revoked | Session terminated | Permanent | — |
| Expired | Inactivity timeout | — | — |

## Real-World Scenarios

### Scenario 1: Banking Application Session Monitoring

A user logs into their banking application from a corporate laptop. The
continuous authentication engine monitors behavioral signals throughout the
session:

```python
# Create monitored banking session
session = engine.create_session(
    user_id="user:bob@bank.com",
    device_id="dev-laptop-bob-001",
    ip_address="10.0.1.50",
    resource="banking-portal",
    trust_level=0.92,
)

# Baseline established after 50 keystroke samples
# Normal typing speed: 65 WPM, normal mouse velocity: 12 px/ms

# After 30 minutes, behavioral signals show deviation
engine.record_keystroke_dynamics(
    session_id=session.session_id,
    timing_data=[0.15, 0.18, 0.12, 0.14, 0.16, 0.13, 0.17, 0.11],
    dwell_times=[0.08, 0.10, 0.07, 0.09, 0.11, 0.08, 0.10, 0.06],
)

risk = engine.evaluate_session_risk(session.session_id)
print(f"Risk evaluation:")
print(f"  Score: {risk.score:.2f}")
print(f"  Level: {risk.level}")
print(f"  Behavioral deviation: {risk.behavioral_deviation:.3f}")
# Behavioral deviation is high — possible session hijacking

# Step-up triggered for high-risk banking session
if risk.level == "high":
    engine.trigger_step_up_auth(
        session_id=session.session_id,
        required_method="fido2",
        reason="behavioral_anomaly",
    )
```

### Scenario 2: Impossible Travel Detection

A user authenticates from New York at 2:00 PM, then a session appears from
London at 2:30 PM — physically impossible:

```python
from continuous_auth import LocationSignal

# First session from New York
location_ny = LocationSignal(
    ip_address="192.168.1.100",
    latitude=40.7128,
    longitude=-74.0060,
    country="US",
    city="New York",
)
engine.update_location(session.session_id, location_ny)

# 30 minutes later, session shows London IP
location_london = LocationSignal(
    ip_address="203.0.113.50",
    latitude=51.5074,
    longitude=-0.1278,
    country="GB",
    city="London",
)
engine.update_location(session.session_id, location_london)

risk = engine.evaluate_session_risk(session.session_id)
# Impossible travel detected — distance: 5570km, speed: ~11000 km/h
print(f"Impossible travel detected! Score: {risk.score:.2f}")
# Decision: Session revoked
```

### Scenario 3: Device Health Degradation

A session starts on a compliant managed device, but the device health
deteriorates during the session:

```python
from continuous_auth import DeviceFingerprint

# Initial device state — fully compliant
initial_fingerprint = DeviceFingerprint(
    device_id="dev-laptop-042",
    user_agent="Mozilla/5.0 Chrome/120.0",
    screen_resolution=(1920, 1080),
    timezone="America/New_York",
    language="en-US",
    platform="Windows",
    security_controls={
        "disk_encryption": True,
        "screen_lock": True,
        "antivirus": True,
        "firewall": True,
    },
)
engine.update_device_fingerprint(session.session_id, initial_fingerprint)

# 20 minutes later — antivirus disabled, firewall off
degraded_fingerprint = DeviceFingerprint(
    device_id="dev-laptop-042",
    user_agent="Mozilla/5.0 Chrome/120.0",
    screen_resolution=(1920, 1080),
    timezone="America/New_York",
    language="en-US",
    platform="Windows",
    security_controls={
        "disk_encryption": True,
        "screen_lock": True,
        "antivirus": False,  # Disabled
        "firewall": False,   # Disabled
    },
)
engine.update_device_fingerprint(session.session_id, degraded_fingerprint)

risk = engine.evaluate_session_risk(session.session_id)
# Device health degraded — risk score increased
print(f"Device risk: {risk.device_risk:.2f}")
print(f"Overall risk: {risk.score:.2f}")
# Step-up triggered due to degraded device posture
```

## Behavioral Biometrics Deep Dive

### Keystroke Dynamics Model

Keystroke dynamics analyze the timing patterns of key presses:

| Feature | Description | Measurement |
|---------|-------------|-------------|
| Dwell time | Duration key is held down | Milliseconds |
| Flight time | Time between consecutive key releases | Milliseconds |
| Latency | Time between key press and release | Milliseconds |
| N-graph timing | Timing of key sequences (di-graphs, tri-graphs) | Milliseconds |
| Typing speed | Words per minute | WPM |
| Error rate | Frequency of backspace/corrections | Percentage |

### Mouse Movement Analysis

Mouse dynamics capture interaction patterns:

| Feature | Description | Detection |
|---------|-------------|-----------|
| Velocity | Speed of cursor movement | Pixels/ms |
| Acceleration | Rate of velocity change | Pixels/ms² |
| Click interval | Time between clicks | Milliseconds |
| Trajectory smoothness | Curvature of movement path | Jerk metric |
| Scroll behavior | Scroll speed and direction | Events/second |

### Touch Gesture Analysis

Mobile device gesture patterns:

| Feature | Description | Measurement |
|---------|-------------|-----------|
| Swipe velocity | Speed of swipe gesture | Pixels/ms |
| Swipe angle | Direction of swipe | Degrees |
| Touch pressure | Force applied to screen | PSI |
| Contact area | Size of finger contact | Square pixels |
| Gesture duration | Total gesture time | Milliseconds |

## Risk-Based Authentication Decision Matrix

| Risk Level | Trust Score | Device State | Location | Action |
|-----------|-------------|-------------|----------|--------|
| Low | > 0.7 | Managed, compliant | Corporate | Allow |
| Low | > 0.7 | Managed, compliant | VPN | Allow |
| Medium | 0.4-0.7 | Managed, some issues | Corporate | Enhanced logging |
| Medium | 0.4-0.7 | Unmanaged | VPN | Step-up MFA |
| High | < 0.4 | Unmanaged | Unknown | Step-up + restrict |
| Critical | Any | Jailbroken/rooted | Any | Revoke session |

## Adaptive Access Configuration

### Dynamic Timeout Adjustment

```python
from continuous_auth import AdaptiveTimeout

timeout_config = AdaptiveTimeout(
    base_timeout_seconds=3600,
    min_timeout_seconds=300,
    max_timeout_seconds=14400,
    risk_factor_multiplier=0.5,  # Timeout = base * (1 - risk * multiplier)
    network_adjustments={
        "corporate": 1.0,      # No adjustment
        "vpn": 0.8,            # 80% of base
        "public_wifi": 0.5,    # 50% of base
        "unknown": 0.3,        # 30% of base
    },
)

# Calculate effective timeout based on current risk and network
effective_timeout = timeout_config.calculate(
    current_risk=0.45,
    network_zone="vpn",
)
# effective_timeout = 3600 * 0.8 * (1 - 0.45 * 0.5) = 2160 seconds
```

### Step-Up Trigger Configuration

```python
from continuous_auth import StepUpConfig

step_up_config = StepUpConfig(
    triggers=[
        {
            "condition": "risk_score >= 0.6",
            "method": "fido2",
            "reason": "high_risk_score",
            "timeout_seconds": 300,
        },
        {
            "condition": "behavioral_deviation >= 0.4",
            "method": "biometric",
            "reason": "behavioral_anomaly",
            "timeout_seconds": 300,
        },
        {
            "condition": "device_risk >= 0.5",
            "method": "fido2",
            "reason": "device_compromise_suspected",
            "timeout_seconds": 180,
        },
        {
            "condition": "impossible_travel == true",
            "method": "fido2+biometric",
            "reason": "impossible_travel",
            "timeout_seconds": 120,
        },
    ],
    max_step_ups_per_session=3,
    cooldown_seconds=600,
)

engine.configure_step_up(step_up_config)
```

## Session Revocation Playbooks

### Automated Response Playbooks

```python
from continuous_auth import RevocationPlaybook

# Playbook for compromised session
compromised_playbook = RevocationPlaybook(
    playbook_id="compromised-session",
    triggers=["critical_risk", "impossible_travel", "malware_detected"],
    actions=[
        {"order": 1, "action": "revoke_session", "delay_seconds": 0},
        {"order": 2, "action": "notify_user", "channels": ["email", "push"]},
        {"order": 3, "action": "lock_account", "duration_seconds": 3600},
        {"order": 4, "action": "create_incident", "severity": "high"},
        {"order": 5, "action": "notify_security_ops", "channel": "slack"},
    ],
)

# Playbook for degraded device
degraded_device_playbook = RevocationPlaybook(
    playbook_id="degraded-device",
    triggers=["device_risk_critical", "jailbreak_detected"],
    actions=[
        {"order": 1, "action": "restrict_to_read_only", "delay_seconds": 0},
        {"order": 2, "action": "trigger_step_up", "method": "fido2"},
        {"order": 3, "action": "notify_user", "channels": ["push"]},
        {"order": 4, "action": "log_for_review", "priority": "medium"},
    ],
)

engine.register_playbook(compromised_playbook)
engine.register_playbook(degraded_device_playbook)
```

## Network-Aware Session Management

### Corporate vs Public Network Policies

| Network Type | Session Timeout | Step-Up Required | Max Sessions |
|-------------|----------------|------------------|--------------|
| Corporate LAN | 8 hours | No | 3 |
| Corporate VPN | 4 hours | No | 2 |
| Home VPN | 2 hours | On risk > 0.5 | 1 |
| Public Wi-Fi | 30 minutes | On risk > 0.3 | 1 |
| Unknown network | 15 minutes | Always | 1 |

```python
from continuous_auth import NetworkPolicy

network_policies = {
    "corporate_lan": NetworkPolicy(
        session_timeout=28800,
        step_up_threshold=0.8,
        max_concurrent_sessions=3,
        behavioral_sensitivity=0.7,
    ),
    "corporate_vpn": NetworkPolicy(
        session_timeout=14400,
        step_up_threshold=0.6,
        max_concurrent_sessions=2,
        behavioral_sensitivity=0.8,
    ),
    "public_wifi": NetworkPolicy(
        session_timeout=1800,
        step_up_threshold=0.3,
        max_concurrent_sessions=1,
        behavioral_sensitivity=0.95,
    ),
}

engine.configure_network_policies(network_policies)
```

## Integration with SIEM and SOAR

### SIEM Event Schema

```json
{
  "event_type": "continuous_auth.risk_transition",
  "timestamp": "2024-01-15T10:30:00Z",
  "session_id": "sess-abc123",
  "user_id": "user:alice@corp.com",
  "previous_risk_level": "low",
  "current_risk_level": "high",
  "risk_score": 0.72,
  "trigger": "behavioral_anomaly",
  "signals": {
    "behavioral_deviation": 0.45,
    "device_risk": 0.10,
    "location_risk": 0.15,
    "temporal_risk": 0.02
  },
  "action_taken": "step_up_required",
  "device_id": "dev-laptop-042",
  "ip_address": "192.168.1.100"
}
```

### SOAR Integration

```python
from continuous_auth import SOARIntegration

soar = SOARIntegration(
    platform="xsoar",
    api_endpoint="https://xsoar:8443/api/v1",
    api_key="your-api-key",
)

# Register SOAR playbooks
soar.register_playbook(
    trigger="session_revoked",
    playbook_id="incident-response-session-compromise",
    auto_execute=True,
)

soar.register_playbook(
    trigger="impossible_travel_detected",
    playbook_id="investigate-impossible-travel",
    auto_execute=False,  # Require analyst approval
)
```

## Performance Benchmarks

| Operation | Target Latency | P99 Latency | Throughput |
|-----------|---------------|-------------|------------|
| Keystroke analysis | < 10ms | 25ms | 1000 eval/s |
| Mouse analysis | < 15ms | 40ms | 500 eval/s |
| Risk score computation | < 5ms | 15ms | 2000 eval/s |
| Device validation | < 50ms | 150ms | 200 eval/s |
| Location check | < 30ms | 80ms | 300 eval/s |
| Full session evaluation | < 100ms | 250ms | 100 eval/s |
