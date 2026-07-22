---
name: "stage-automation"
category: "theater-tech"
version: "1.0.0"
tags: ["theater-tech", "stage-automation", "rigging", "fly-systems", "show-control"]
---

# Stage Automation Control System

## Overview

The stage automation module provides programmatic control over motorized theatrical stage machinery, including fly systems, revolving platforms, trap doors, and automated scenic elements. It abstracts the complexity of multiple manufacturer protocols (Kinesys, ShowTex, ETC, Computerized theatrical systems) into a unified Python API that allows show control operators to program, test, and execute complex automation cues with deterministic timing and comprehensive safety interlocks. The module is designed for venues ranging from 200-seat black box theaters to 2,000-seat touring houses, with configurable safety parameters that adapt to each venue's rigging plot, load ratings, and operational procedures.

Modern theatrical productions demand seamless integration between automation hardware, lighting rigs, sound systems, and media servers. This module bridges those domains by providing DMX/Art-Net bridge capabilities, SMPTE timecode synchronization, and a declarative cue-list format that can encode entire show sequences. Every movement is subject to safety limit validation, collision detection, and emergency stop propagation — ensuring that no software bug or operator error can cause physical harm to performers or crew. The module supports both single-venue installations and touring configurations where rigging plots change between venues.

The architecture follows a layered approach: a hardware abstraction layer handles vendor-specific communication, a motion planning layer computes trajectories with acceleration/deceleration ramps, a cue management layer orchestrates sequencing and look-ahead, and a safety layer enforces hard limits independent of the control logic. This separation ensures that safety constraints are never bypassed by higher-level code paths, a critical requirement in venues where automation moves tons of scenery above performers' heads. The safety layer operates on a watchdog timer — if the control layer fails to check in within 100ms, all axes automatically decelerate to a stop.

## Core Capabilities

- Motorized fly system control with multi-line synchronization and load-aware speed limiting
- Revolving stage programming with angular velocity profiling and position-dependent interlocks
- Trap door sequencing with hydraulic/pneumatic actuator coordination
- DMX512/Art-Net bridge for cue-synchronized lighting and effects integration
- SMPTE/LTC timecode lock and chase for frame-accurate show control
- Safety interlock management with E-stop propagation, limit switch monitoring, and load cell verification
- Declarative cue-list format supporting parallel, sequential, and conditional cue groups
- Real-time telemetry dashboard with motor current, position, velocity, and temperature monitoring

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Show Controller                       │
│         (Cue List, Timecode, User Interface)            │
├─────────────────────────────────────────────────────────┤
│                  Cue Management Layer                    │
│      (Sequential, Parallel, Conditional, Follow)        │
├─────────────────────────────────────────────────────────┤
│                 Motion Planning Layer                    │
│    (Trapezoidal Profiles, S-Curves, Sync Groups)        │
├─────────────────────────────────────────────────────────┤
│               Hardware Abstraction Layer                 │
│      (Kinesys, ShowTex, ETC, Custom Protocol)           │
├─────────────────────────────────────────────────────────┤
│                    Safety Layer                          │
│  (Limit Switches, Load Cells, E-Stop, Watchdog Timer)   │
└─────────────────────────────────────────────────────────┘
```

## Usage Examples

### Fly System Control

```python
from stage_automation import FlySystem, MotorAxis, SafetyConfig, CueList

# Initialize a 6-line Kinesys fly system
fly = FlySystem(
    controller_ip="192.168.1.100",
    num_lines=6,
    safety=SafetyConfig(
        max_load_kg=500,
        max_speed_mps=1.2,
        estop_response_ms=50,
        limit_switch_enabled=True,
    ),
)

# Connect and home all axes
fly.connect()
fly.home_all()

# Program a synchronized blackout drop
cue_1 = fly.create_cue(
    cue_number=1,
    actions={
        1: {"target_pos": 0.0, "speed": 0.8, "ramp_ms": 500},
        2: {"target_pos": 0.0, "speed": 0.8, "ramp_ms": 500},
        3: {"target_pos": 0.0, "speed": 0.6, "ramp_ms": 750},
    },
    timecode=0x01000000,
)

# Execute with position monitoring
fly.execute_cue(1)
print(f"Line 1 position: {fly.get_position(1):.2f}m")
print(f"Line 1 telemetry: {fly.get_telemetry(1)}")
```

### Revolving Stage and Trap Doors

```python
from stage_automation import RevolvingStage, TrapDoorSequencer

# Configure a 12-meter revolving platform
revolve = RevolvingStage(
    diameter_m=12.0,
    motor_rpm_max=6,
    encoder_resolution=4096,
    controller_port="/dev/ttyUSB0",
)
revolve.connect()
revolve.calibrate_zero(home_position_deg=0)

# Program a 180-degree reveal over 8 seconds
revolve.program_move(
    target_deg=180.0,
    duration_s=8.0,
    profile="ease_in_out",
)

# Sequence two trap doors for a magic reveal
traps = TrapDoorSequencer(
    doors=[
        {"id": "trap_A", "actuator": "hydraulic", "stroke_mm": 800},
        {"id": "trap_B", "actuator": "pneumatic", "stroke_mm": 600},
    ],
)
traps.sequence(
    steps=[
        {"door": "trap_A", "action": "open", "duration_s": 1.5},
        {"door": "trap_B", "action": "open", "duration_s": 2.0, "delay_s": 0.5},
        {"door": "trap_A", "action": "close", "duration_s": 1.0, "delay_s": 3.0},
    ],
    interlock_required=True,
)
```

### Show Control and Timecode

```python
from stage_automation import ShowController, TimecodeSource, DMXBridge

# Master show controller with SMPTE chase
controller = ShowController(
    timecode_source=TimecodeSource.LTC,
    ltc_input_device="snd:hw:1,0",
    bpm_reference=120,
)

# Bridge automation cues to DMX for followspot triggering
bridge = DMXBridge(
    universe=0,
    art_net_ip="2.0.0.1",
    dmx_channel_map={1: "followspot_1_intensity", 2: "followspot_2_intensity"},
)
controller.attach_bridge(bridge)

# Load and run a cue list
controller.load_cue_list("act_2_sc3.json")
controller.go()
```

### Safety System Configuration

```python
from stage_automation import SafetyConfig, FlySystem

# Custom safety configuration for a specific venue
venue_safety = SafetyConfig(
    max_load_kg=350,          # Per-line load limit
    max_speed_mps=0.8,        # Reduced for tight stage
    estop_response_ms=30,     # Fast E-stop
    limit_switch_enabled=True,
    load_cell_enabled=True,
    collision_buffer_mm=200,  # Extra clearance
    temperature_limit_c=75,   # Motor thermal limit
    max_acceleration_mps2=1.5,
)

fly = FlySystem(
    controller_ip="192.168.1.100",
    num_lines=8,
    safety=venue_safety,
)
```

## Best Practices

1. **Always verify safety interlocks before every cue execution.** The `SafetyConfig` limits are hard-coded defaults, but each venue's rigging plot has unique load ratings — override them explicitly per installation. Never assume defaults are correct.

2. **Test every automation cue at reduced speed before full-speed rehearsal.** The `speed` parameter accepts a 0.0–1.0 multiplier; always rehearse at 0.3 first, then 0.5, then full speed. This catches mechanical issues and programming errors without risking scenery or performers.

3. **Use timecode lock for frame-critical cues.** Free-running cue lists accumulate drift; SMPTE LTC chase keeps automation synchronized to lighting and sound to within one frame (33ms at 30fps). For musical productions, drift of even 100ms is perceptible.

4. **Maintain a physical E-stop chain independent of software.** The module's `emergency_stop()` sends a software stop command, but the hardware E-stop circuit must be wired in series and never rely on the network. The hardware E-stop should be tested at the start of every rehearsal.

5. **Log every motor's current draw during rehearsal.** A gradual increase in peak current over weeks indicates mechanical wear that should be serviced before failure. Current spikes above 120% of rated current trigger an automatic warning.

6. **Back up cue lists to version control before every tech rehearsal.** The JSON cue-list format is designed for diffing; use it. A single misplaced decimal point in a cue number can cascade through an entire show.

7. **Separate show-control logic from safety logic in your architecture.** The safety layer must be independently testable and never gated behind a feature flag or configuration toggle. Safety code should have its own test suite that runs in CI.

8. **Run the collision-detection pre-scan before each performance.** Even if scenery positions haven't changed, load shifts or cable snags can alter clearance envelopes. The pre-scan takes 15 seconds and has prevented multiple incidents.

9. **Document every interlock override with operator initials and reason.** If a safety interlock is bypassed for a specific cue (e.g., a performer needs to pass through a moving piece), log who authorized it, when, and why. This is an OSHA documentation requirement in many jurisdictions.

10. **Calibrate load cells at the start of every production.** Load cells drift with temperature and humidity. A 10-minute calibration procedure at the start of tech ensures accurate weight readings throughout the run.

## Configuration

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `max_load_kg` | 500 | 50–2000 | Maximum load per line in kilograms |
| `max_speed_mps` | 1.2 | 0.1–3.0 | Maximum line speed in meters/second |
| `estop_response_ms` | 50 | 10–200 | E-stop response time in milliseconds |
| `collision_buffer_mm` | 150 | 50–500 | Minimum clearance between moving elements |
| `temperature_limit_c` | 85 | 60–120 | Motor thermal shutdown threshold |

## Troubleshooting

- **Axis won't home:** Check limit switch wiring and verify the axis isn't already at the limit. Manual jog to center position before homing.
- **E-stop won't reset:** Verify all hardware E-stop buttons are released. Check the safety relay wiring. Some systems require a manual key switch reset.
- **Cue list drift:** Enable SMPTE LTC chase mode. Free-running mode accumulates drift proportional to system clock accuracy.
- **Motor current spikes:** Check for mechanical obstructions, bearing wear, or cable snags. Compare baseline current from initial installation.

## Related Modules

- [lighting-control](../lighting-control/GROK.md) — DMX/Art-Net partner for followspot and effects synchronization
- [sound-engineering](../sound-engineering/GROK.md) — Audio cue synchronization and spatial reference for automation timing
- [projection-mapping](../projection-mapping/GROK.md) — Projection surface tracking linked to automated scenic movement
- [audience-engagement](../audience-engagement/GROK.md) — Trigger audience interaction cues from automation events

---

## Advanced Configuration

### Network Topology Configuration

```python
from stage_automation import NetworkConfig, ControllerTopology

topology = ControllerTopology(
    primary_controller="192.168.1.100",
    backup_controller="192.168.1.101",
    redundancy_mode="hot_standby",
    heartbeat_interval_ms=100,
    failover_timeout_ms=500,
)

network = NetworkConfig(
    primary_subnet="192.168.1.0/24",
    automation_vlan=10,
    dmx_artnet_subnet="2.0.0.0/8",
    qos_priority=7,
    multicast_group="239.255.0.1",
)
```

### Custom Protocol Registration

```python
from stage_automation import ProtocolRegistry, CustomProtocol

registry = ProtocolRegistry()

class MyCustomProtocol(CustomProtocol):
    def connect(self, ip, port): ...
    def send_command(self, axis_id, command): ...
    def read_position(self, axis_id): ...
    def emergency_stop(self): ...

registry.register("custom_rig", MyCustomProtocol)
```

### Advanced Safety Layer Configuration

```python
from stage_automation import SafetyConfig, WatchdogConfig, CollisionModel

safety = SafetyConfig(
    max_load_kg=500,
    max_speed_mps=1.2,
    estop_response_ms=30,
    watchdog=WatchdogConfig(
        check_interval_ms=50,
        timeout_ms=100,
        action="decelerate_to_stop",
        max_deceleration_mps2=2.0,
    ),
    collision_model=CollisionModel(
        enabled=True,
        scan_resolution_mm=10,
        prediction_horizon_ms=2000,
        buffer_multiplier=1.5,
    ),
    thermal_monitoring=True,
    current_spike_threshold_pct=120,
    vibration_monitoring=True,
)
```

## Architecture Patterns

### Event-Driven Cue Execution

```
User Input / Timecode
        │
        ▼
┌───────────────┐
│  Cue Scheduler │──── Schedules future cues
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Motion Planner │──── Computes trajectories
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Safety Validator│──── Checks limits before dispatch
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ HAL Dispatcher │──── Sends to hardware
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Telemetry Feed │──── Reports back to dashboard
└───────────────┘
```

### Redundant Controller Architecture

For touring and high-reliability installations, deploy controllers in hot-standby pairs with automatic failover. The primary controller drives all axes while the backup continuously mirrors state. If the primary loses heartbeat, the backup assumes control within 500ms and decelerates all axes to safe positions.

### Cue List State Machine

```
IDLE → LOADED → STANDBY → EXECUTING → COMPLETED
  ↑                                      │
  └──────────── RESET ◄─────────────────┘

Additional states:
PAUSED (during execution)
ABORTED (emergency stop)
ERROR (safety violation)
```

## Integration Guide

### DMX/Art-Net Bridge Setup

```python
from stage_automation import DMXBridge

bridge = DMXBridge(
    universe=0,
    art_net_ip="2.0.0.1",
    multicast=False,
    refresh_rate_hz=44,
)
bridge.start()
bridge.bind_cue(cue_number=1, dmx_snapshot="cue1_dmx.json")
```

### SMPTE Timecode Integration

```python
from stage_automation import TimecodeSource, SMPTEBridge

tc = SMPTEBridge(
    source=TimecodeSource.LTC,
    input_device="snd:hw:1,0",
    frame_rate=30,
    chase_enabled=True,
)
tc.start()
tc.sync_cue_list("full_show.json")
```

### External Show Control Protocols

- **OSC**: Map automation cues to OSC messages for integration with QLab, Isadora, and other show control software
- **MIDI**: Trigger automation from MIDI notes, timecode, or CC messages
- **TCP/UDP**: Custom protocol integration for proprietary equipment
- **GPIO**: Hardware trigger inputs for stage-side buttons and sensors

## Performance Optimization

| Optimization | Impact | Implementation |
|-------------|--------|----------------|
| Trapezoidal velocity profiling | Smooth motion, reduced jerk | Enable in SafetyConfig |
| Precomputed trajectory cache | 30% faster cue start | Cache common movement patterns |
| Telemetry batch transmission | Reduced network load | Aggregate 10 telemetry frames per packet |
| Hardware polling optimization | Lower CPU usage | Increase poll interval for non-critical axes |
| Motion interpolation | Smoother multi-axis sync | Use cubic spline interpolation |

## Security Considerations

- **Network isolation**: Automation networks must be on a dedicated VLAN with no internet access
- **Authentication**: All controller connections require HMAC-signed authentication tokens
- **Encryption**: TLS 1.3 for all network communication between software and controllers
- **Access control**: Role-based access with operator, programmer, and administrator levels
- **Audit logging**: All safety overrides, E-stop events, and configuration changes are logged
- **Physical security**: Controller hardware should be in locked racks with key switches
- **Firmware verification**: Validate controller firmware checksums before each show
- **Backup controllers**: Hot-standby redundancy prevents single points of failure

## Troubleshooting Guide

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| Axis drift during hold | Encoder calibration drift | Recalibrate encoder zero position |
| Intermittent communication | Network congestion or cable fault | Check dedicated VLAN, replace Cat6 cables |
| Cue timing jitter | Insufficient CPU priority | Set process to real-time scheduling class |
| Telemetry gaps | Multicast router misconfiguration | Verify IGMP snooping on switches |
| Safety false positives | Sensor noise from EMI | Shield sensor cables, add ferrite beads |
| Controller failover delay | Heartbeat timeout too long | Reduce watchdog timeout to 50ms |
| Load cell readings unstable | Temperature drift | Recalibrate load cells, check ambient temperature |

## API Reference

### FlySystem

```python
class FlySystem:
    def __init__(self, controller_ip: str, num_lines: int, safety: SafetyConfig)
    def connect(self) -> None
    def disconnect(self) -> None
    def home_all(self) -> None
    def home_axis(self, axis_id: int) -> None
    def create_cue(self, cue_number: int, actions: dict, timecode: int = None) -> Cue
    def execute_cue(self, cue_number: int) -> CueResult
    def emergency_stop(self) -> None
    def get_position(self, axis_id: int) -> float
    def get_telemetry(self, axis_id: int) -> Telemetry
    def jog(self, axis_id: int, speed: float) -> None
```

### RevolvingStage

```python
class RevolvingStage:
    def __init__(self, diameter_m: float, motor_rpm_max: float, encoder_resolution: int, controller_port: str)
    def connect(self) -> None
    def calibrate_zero(self, home_position_deg: float) -> None
    def program_move(self, target_deg: float, duration_s: float, profile: str) -> None
    def get_position(self) -> float
    def stop(self) -> None
```

## Data Models

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List

class AxisState(Enum):
    IDLE = "idle"
    MOVING = "moving"
    HOLDING = "holding"
    HOMING = "homing"
    ERROR = "error"
    E_STOPPED = "e_stopped"

@dataclass
class Telemetry:
    axis_id: int
    position_m: float
    velocity_mps: float
    current_amps: float
    temperature_c: float
    state: AxisState
    load_kg: float
    encoder_count: int
    timestamp_ms: float

@dataclass
class Cue:
    cue_number: int
    actions: dict
    timecode: Optional[int]
    status: str
    created_at: str

@dataclass
class SafetyConfig:
    max_load_kg: float = 500
    max_speed_mps: float = 1.2
    estop_response_ms: int = 50
    collision_buffer_mm: int = 150
    temperature_limit_c: float = 85
    max_acceleration_mps2: float = 2.0
```

## Deployment Guide

### Prerequisites

- Python 3.10+
- Dedicated automation network (VLAN)
- Compatible controller hardware (Kinesys, ShowTex, or ETC)
- Network switch with QoS support
- UPS for controller hardware

### Installation

```bash
pip install stage-automation
# Or from source
git clone https://github.com/example/stage-automation.git
cd stage-automation
pip install -e ".[dev]"
```

### Venue Setup Checklist

1. Verify network connectivity to all controllers
2. Run controller self-test diagnostics
3. Calibrate all axes and home positions
4. Load venue-specific SafetyConfig
5. Test E-stop chain end-to-end
6. Run collision detection pre-scan
7. Verify load cell calibration
8. Test telemetry dashboard
9. Load and verify cue lists
10. Conduct full-speed rehearsal test

## Monitoring & Observability

```python
from stage_automation import MetricsCollector

collector = MetricsCollector()

# Track key metrics
collector.gauge("automation.axes.position", position, tags={"axis": axis_id})
collector.counter("automation.cues.executed", count, tags={"status": status})
collector.histogram("automation.cue.duration_ms", duration)
collector.counter("automation.safety.estop_count", count)
collector.gauge("automation.motor.current_amps", current, tags={"axis": axis_id})
collector.histogram("automation.motor.temperature_c", temperature)
collector.counter("automation.network.packets_lost", count)
```

## Testing Strategy

```python
import pytest
from stage_automation import FlySystem, SafetyConfig

@pytest.fixture
def fly_system():
    return FlySystem(
        controller_ip="192.168.1.100",
        num_lines=6,
        safety=SafetyConfig(max_load_kg=500),
    )

def test_emergency_stop(fly_system):
    fly_system.connect()
    fly_system.emergency_stop()
    for i in range(1, 7):
        assert fly_system.get_telemetry(i).state == AxisState.E_STOPPED

def test_safety_limit_enforcement(fly_system):
    fly_system.connect()
    result = fly_system.create_cue(
        cue_number=99,
        actions={1: {"target_pos": 100.0, "speed": 2.0}},
    )
    assert result.warnings  # Speed exceeds max
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added sACN support | Update Art-Net config to include sACN |
| 1.2.0 | New collision detection model | Re-run calibration for existing venues |
| 2.0.0 | Breaking: SafetyConfig schema v2 | Migrate SafetyConfig fields per guide |

## Glossary

| Term | Definition |
|------|-----------|
| **Fly System** | Motorized rigging for raising and lowering scenery |
| **E-Stop** | Emergency stop — immediate hardware-level halt |
| **SMPTE LTC** | Linear Timecode for synchronization |
| **HAL** | Hardware Abstraction Layer |
| **Art-Net** | DMX over Ethernet protocol |
| **Load Cell** | Sensor measuring weight on a rigging line |
| **Watchdog** | Safety timer that triggers stop if control layer fails |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with Kinesys and ShowTex support
- Fly system, revolving stage, and trap door control
- SMPTE LTC timecode synchronization
- Safety interlock system with E-stop propagation

### Version 1.1.0 (2024-06-01)
- Added sACN (E1.31) network output
- Improved collision detection algorithms
- Added telemetry dashboard

## Contributing Guidelines

```bash
git clone https://github.com/example/stage-automation.git
cd stage-automation
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/
```

### Code Standards
- All safety-critical code requires peer review
- Hardware interaction tests must run on simulated controllers
- Documentation required for all public APIs

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Complete Configuration Matrix

| Parameter | Minimum | Default | Maximum | Unit | Description |
|-----------|---------|---------|---------|------|-------------|
| `max_load_kg` | 50 | 500 | 2000 | kg | Maximum load per rigging line |
| `max_speed_mps` | 0.1 | 1.2 | 3.0 | m/s | Maximum line travel speed |
| `estop_response_ms` | 10 | 50 | 200 | ms | Emergency stop response time |
| `collision_buffer_mm` | 50 | 150 | 500 | mm | Minimum clearance between elements |
| `temperature_limit_c` | 60 | 85 | 120 | °C | Motor thermal shutdown threshold |
| `max_acceleration_mps2` | 0.5 | 2.0 | 5.0 | m/s² | Maximum acceleration rate |
| `watchdog_interval_ms` | 10 | 50 | 200 | ms | Safety watchdog check interval |
| `watchdog_timeout_ms` | 50 | 100 | 500 | ms | Watchdog timeout before E-stop |
| `encoder_resolution` | 1024 | 4096 | 16384 | counts/rev | Encoder pulse resolution |
| `load_cell_sample_rate_hz` | 10 | 100 | 1000 | Hz | Load cell sampling frequency |
| `telemetry_interval_ms` | 50 | 100 | 500 | ms | Telemetry reporting interval |
| `dmx_universe_count` | 1 | 4 | 64 | — | Number of DMX universes |
| `artnet_refresh_hz` | 1 | 44 | 44 | Hz | Art-Net frame rate |

### Complete Cue List Format

```json
{
  "cue_list_name": "Full Show - Act 1",
  "version": "1.0.0",
  "created_at": "2024-01-15T10:00:00Z",
  "timecode_start": "01:00:00:00",
  "timecode_format": "30fps",
  "cues": [
    {
      "cue_number": 1,
      "timecode": "01:00:00:00",
      "label": "Blackout drop",
      "actions": {
        "fly_line_1": {"target_pos": 0.0, "speed": 0.8, "ramp_ms": 500, "profile": "trapezoidal"},
        "fly_line_2": {"target_pos": 0.0, "speed": 0.8, "ramp_ms": 500, "profile": "trapezoidal"},
        "fly_line_3": {"target_pos": 0.0, "speed": 0.6, "ramp_ms": 750, "profile": "s_curve"},
        "revolve_1": {"target_deg": 180.0, "duration_s": 8.0, "profile": "ease_in_out"},
        "dmx_snapshot": "cue1_lighting.json"
      },
      "parallel": true,
      "safety_check": true,
      "collision_scan": true
    },
    {
      "cue_number": 2,
      "timecode": "01:00:08:00",
      "label": "Reveal scenic",
      "actions": {
        "fly_line_4": {"target_pos": 6.0, "speed": 0.4, "ramp_ms": 1000, "profile": "s_curve"},
        "fly_line_5": {"target_pos": 6.0, "speed": 0.4, "ramp_ms": 1000, "profile": "s_curve"}
      },
      "parallel": true,
      "follow_time_s": 12.0,
      "safety_check": true
    },
    {
      "cue_number": 3,
      "timecode": "01:00:20:00",
      "label": "Trap door reveal",
      "actions": {
        "trap_A": {"action": "open", "duration_s": 1.5},
        "trap_B": {"action": "open", "duration_s": 2.0, "delay_s": 0.5}
      },
      "parallel": false,
      "safety_check": true,
      "performer_clearance_required": true
    }
  ]
}
```

### Safety System State Diagram

```
NORMAL OPERATION
    │
    ├── Fault Detected
    │       │
    │       ▼
    │   ASSESS SEVERITY
    │       │
    │       ├── Minor (sensor drift)
    │       │       │
    │       │       ▼
    │       │   LOG WARNING
    │       │   Continue with reduced limits
    │       │
    │       ├── Moderate (current spike)
    │       │       │
    │       │       ▼
    │       │   REDUCE SPEED
    │       │   Alert operator
    │       │   Continue monitoring
    │       │
    │       └── Critical (limit exceeded, collision)
    │               │
    │               ▼
    │           EMERGENCY STOP
    │           All axes decelerate
    │           Propagate E-stop to hardware
    │           Log event
    │           Alert all operators
    │
    └── Manual E-Stop Pressed
            │
            ▼
        EMERGENCY STOP
        Same as critical fault path
```

### Motor Control Profiles

| Profile | Description | Use Case |
|---------|-------------|----------|
| **Trapezoidal** | Constant velocity with linear ramps | Standard scenery movement |
| **S-Curve** | Smooth acceleration with jerk limiting | Performer-carrying loads |
| **Ease-In-Out** | Cubic easing for natural motion | Revolving stage, reveals |
| **Constant Velocity** | No ramp, immediate speed change | Not recommended for loads |
| **Custom Bezier** | User-defined control points | Special effects |

### Multi-Venue Configuration

```python
from stage_automation import VenueConfig, VenueProfile

# Configure venues for a touring show
venues = {
    "broadway_house": VenueConfig(
        name="Broadway Theater",
        stage_width_m=16.0,
        stage_depth_m=12.0,
        fly_lines=12,
        max_load_per_line_kg=500,
        trap_doors=4,
        revolve_diameter_m=10.0,
        network_topology="dedicated_vlan",
    ),
    "regional_house": VenueConfig(
        name="Regional Touring House",
        stage_width_m=12.0,
        stage_depth_m=9.0,
        fly_lines=8,
        max_load_per_line_kg=350,
        trap_doors=2,
        revolve_diameter_m=8.0,
        network_topology="shared_vlan",
    ),
    "blackbox": VenueConfig(
        name="Black Box Theater",
        stage_width_m=8.0,
        stage_depth_m=6.0,
        fly_lines=4,
        max_load_per_line_kg=200,
        trap_doors=0,
        revolve_diameter_m=0,
        network_topology="local",
    ),
}

# Select venue profile
profile = VenueProfile(venues["broadway_house"])
safety = profile.generate_safety_config()
automation = profile.generate_automation_config()
```

### Operator Workflow

```
PRE-SHOW (2 hours before)
    │
    ├── Load venue configuration
    ├── Verify network connectivity to all controllers
    ├── Run controller self-test diagnostics
    ├── Calibrate all axes and home positions
    ├── Test E-stop chain end-to-end
    ├── Run collision detection pre-scan
    ├── Verify load cell calibration
    ├── Load and verify cue lists
    └── Test telemetry dashboard

TECH REHEARSAL
    │
    ├── Run cue list at reduced speed (0.3x)
    ├── Verify all cue timings
    ├── Check motor current draws
    ├── Verify telemetry accuracy
    ├── Test E-stop during movement
    ├── Increment speed to 0.5x, then full
    └── Document any mechanical issues

PERFORMANCE
    │
    ├── Pre-show system check (30 min before)
    ├── Load show cue list
    ├── Lock configuration (prevent changes)
    ├── Monitor telemetry during performance
    ├── Respond to any warnings
    └── Post-show system log

POST-SHOW
    │
    ├── Export telemetry logs
    ├── Backup cue lists
    ├── Log any anomalies
    └── Schedule maintenance if needed
```

### Troubleshooting Decision Tree

```
Axis won't move
    │
    ├── Check E-stop status → Release if engaged
    ├── Check limit switches → Verify wiring and alignment
    ├── Check motor current → Compare to baseline
    ├── Check network connection → Verify cable and switch
    ├── Check controller status → Restart if needed
    └── Contact support if unresolved

Cue timing off
    │
    ├── Enable SMPTE chase → Re-sync to timecode
    ├── Check system clock accuracy → Use NTP
    ├── Check cue list format → Verify JSON syntax
    ├── Check follow times → Verify no cascading delays
    └── Profile CPU usage → Ensure real-time scheduling

Telemetry gaps
    │
    ├── Check network congestion → Verify VLAN isolation
    ├── Check multicast routing → Verify IGMP snooping
    ├── Check telemetry interval → Reduce frequency
    ├── Check controller load → Reduce other operations
    └── Check packet loss → Replace cables if needed
```

### Performance Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| E-stop response time | < 50ms | 50-100ms | > 100ms |
| Position accuracy | ± 2mm | ± 5mm | ± 10mm |
| Telemetry latency | < 50ms | 50-100ms | > 100ms |
| Cue execution jitter | < 10ms | 10-30ms | > 30ms |
| Motor current (nominal) | Rated ± 10% | Rated ± 20% | Rated ± 30% |
| Network packet loss | 0% | < 0.1% | > 0.1% |
| Controller uptime | > 99.9% | > 99.5% | < 99.5% |

### Maintenance Schedule

| Task | Frequency | Duration | Responsible |
|------|-----------|----------|-------------|
| Visual inspection | Before every show | 10 min | Operator |
| E-stop chain test | Before every show | 5 min | Operator |
| Load cell calibration | Start of production | 15 min | Technician |
| Encoder calibration | Monthly | 30 min | Technician |
| Motor bearing inspection | Quarterly | 2 hours | Engineer |
| Cable integrity test | Quarterly | 1 hour | Technician |
| Firmware update | As released | 30 min | Engineer |
| Full system overhaul | Annually | 8 hours | Engineering team |
