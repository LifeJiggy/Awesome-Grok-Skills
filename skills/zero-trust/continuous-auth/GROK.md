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
