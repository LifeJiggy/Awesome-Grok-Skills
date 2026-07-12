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
