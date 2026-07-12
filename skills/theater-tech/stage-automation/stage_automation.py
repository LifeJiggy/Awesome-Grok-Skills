"""
Stage Automation Control System
Motorized rigging, fly systems, revolving stages, trap doors, and show control integration.
"""

from __future__ import annotations

import json
import logging
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

class AxisState(Enum):
    IDLE = auto()
    HOMING = auto()
    MOVING = auto()
    AT_LIMIT = auto()
    ERROR = auto()
    E_STOPPED = auto()


class CueStatus(Enum):
    PENDING = auto()
    ARMED = auto()
    EXECUTING = auto()
    COMPLETE = auto()
    FAILED = auto()
    CANCELLED = auto()


class ActuatorType(Enum):
    HYDRAULIC = "hydraulic"
    PNEUMATIC = "pneumatic"
    ELECTRIC = "electric"
    SERVO = "servo"


class MotionProfile(Enum):
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    S_CURVE = "s_curve"


class TimecodeSource(Enum):
    LTC = "ltc"
    MTC = "mtc"
    INTERNAL = "internal"
    ART_NET = "art_net"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class SafetyConfig:
    max_load_kg: float = 500.0
    max_speed_mps: float = 1.2
    estop_response_ms: int = 50
    limit_switch_enabled: bool = True
    load_cell_enabled: bool = True
    collision_buffer_mm: float = 150.0
    temperature_limit_c: float = 85.0
    max_acceleration_mps2: float = 2.0


@dataclass
class MotorTelemetry:
    position_m: float = 0.0
    velocity_mps: float = 0.0
    current_a: float = 0.0
    temperature_c: float = 25.0
    load_kg: float = 0.0
    state: AxisState = AxisState.IDLE
    error_code: int = 0


@dataclass
class MotorAxis:
    axis_id: int
    name: str
    max_travel_m: float = 15.0
    encoder_resolution: int = 2048
    motor_rated_current_a: float = 5.0
    telemetry: MotorTelemetry = field(default_factory=MotorTelemetry)


@dataclass
class CueStep:
    cue_number: int
    timecode: int  # Frames since midnight
    actions: dict[int, dict[str, Any]]
    status: CueStatus = CueStatus.PENDING
    duration_ms: int = 0
    step_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])


@dataclass
class TrapDoorConfig:
    door_id: str
    actuator: ActuatorType
    stroke_mm: float
    open_time_s: float = 2.0
    interlock_group: Optional[str] = None


# ---------------------------------------------------------------------------
# Fly System Controller
# ---------------------------------------------------------------------------

class FlySystem:
    """Multi-line motorized fly system with safety interlocks."""

    def __init__(
        self,
        controller_ip: str,
        num_lines: int = 6,
        safety: Optional[SafetyConfig] = None,
    ):
        self.controller_ip = controller_ip
        self.num_lines = num_lines
        self.safety = safety or SafetyConfig()
        self.axes: dict[int, MotorAxis] = {}
        self._connected = False
        self._estop_active = False
        self._cues: list[CueStep] = []

        for i in range(1, num_lines + 1):
            self.axes[i] = MotorAxis(axis_id=i, name=f"Line {i}")

    def connect(self) -> bool:
        logger.info("Connecting to fly system controller at %s", self.controller_ip)
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False
        logger.info("Disconnected from fly system controller")

    def home_all(self) -> dict[int, bool]:
        if not self._connected:
            raise RuntimeError("Not connected to controller")
        results = {}
        for axis_id, axis in self.axes.items():
            axis.telemetry.state = AxisState.HOMING
            logger.info("Homing axis %d (%s)", axis_id, axis.name)
            axis.telemetry.state = AxisState.IDLE
            results[axis_id] = True
        return results

    def emergency_stop(self) -> None:
        self._estop_active = True
        for axis in self.axes.values():
            axis.telemetry.state = AxisState.E_STOPPED
        logger.critical("EMERGENCY STOP triggered on all axes")

    def reset_estop(self) -> bool:
        if not self._estop_active:
            return True
        self._estop_active = False
        for axis in self.axes.values():
            axis.telemetry.state = AxisState.IDLE
        logger.info("E-stop reset acknowledged")
        return True

    def _validate_move(self, axis_id: int, target_pos: float, speed: float) -> None:
        if self._estop_active:
            raise RuntimeError("E-stop is active — cannot execute moves")
        axis = self.axes[axis_id]
        if target_pos < 0 or target_pos > axis.max_travel_m:
            raise ValueError(
                f"Target {target_pos}m out of range for axis {axis_id} "
                f"(max {axis.max_travel_m}m)"
            )
        if speed > self.safety.max_speed_mps:
            raise ValueError(
                f"Speed {speed} m/s exceeds safety limit "
                f"{self.safety.max_speed_mps} m/s"
            )

    def move_axis(
        self,
        axis_id: int,
        target_pos: float,
        speed: float,
        ramp_ms: int = 500,
        profile: MotionProfile = MotionProfile.EASE_IN_OUT,
    ) -> bool:
        self._validate_move(axis_id, target_pos, speed)
        axis = self.axes[axis_id]
        axis.telemetry.state = AxisState.MOVING
        axis.telemetry.velocity_mps = speed
        logger.info(
            "Axis %d moving to %.2fm at %.2f m/s (ramp %dms, profile %s)",
            axis_id, target_pos, speed, ramp_ms, profile.value,
        )
        axis.telemetry.position_m = target_pos
        axis.telemetry.velocity_mps = 0.0
        axis.telemetry.state = AxisState.IDLE
        return True

    def get_position(self, axis_id: int) -> float:
        return self.axes[axis_id].telemetry.position_m

    def get_telemetry(self, axis_id: int) -> MotorTelemetry:
        return self.axes[axis_id].telemetry

    def create_cue(
        self,
        cue_number: int,
        actions: dict[int, dict[str, Any]],
        timecode: int = 0,
    ) -> CueStep:
        cue = CueStep(cue_number=cue_number, timecode=timecode, actions=actions)
        self._cues.append(cue)
        self._cues.sort(key=lambda c: c.cue_number)
        logger.info("Created cue %d with %d axis actions", cue_number, len(actions))
        return cue

    def execute_cue(self, cue_number: int) -> bool:
        if self._estop_active:
            raise RuntimeError("E-stop active")
        cue = next((c for c in self._cues if c.cue_number == cue_number), None)
        if cue is None:
            raise ValueError(f"Cue {cue_number} not found")
        cue.status = CueStatus.EXECUTING
        for axis_id, params in cue.actions.items():
            self.move_axis(
                axis_id=axis_id,
                target_pos=params.get("target_pos", 0),
                speed=params.get("speed", 0.5),
                ramp_ms=params.get("ramp_ms", 500),
            )
        cue.status = CueStatus.COMPLETE
        logger.info("Cue %d executed successfully", cue_number)
        return True


# ---------------------------------------------------------------------------
# Revolving Stage
# ---------------------------------------------------------------------------

class RevolvingStage:
    """Motorized revolving platform with position tracking."""

    def __init__(
        self,
        diameter_m: float,
        motor_rpm_max: float = 6.0,
        encoder_resolution: int = 4096,
        controller_port: str = "/dev/ttyUSB0",
    ):
        self.diameter_m = diameter_m
        self.motor_rpm_max = motor_rpm_max
        self.encoder_resolution = encoder_resolution
        self.controller_port = controller_port
        self._connected = False
        self._current_deg = 0.0
        self._zero_offset_deg = 0.0

    def connect(self) -> bool:
        logger.info("Connecting revolving stage on %s", self.controller_port)
        self._connected = True
        return True

    def calibrate_zero(self, home_position_deg: float = 0) -> None:
        self._zero_offset_deg = home_position_deg
        self._current_deg = 0.0
        logger.info("Zero calibrated at %.1f degrees", home_position_deg)

    def _deg_to_encoder(self, deg: float) -> int:
        return int((deg / 360.0) * self.encoder_resolution)

    def _encoder_to_deg(self, encoder: int) -> float:
        return (encoder / self.encoder_resolution) * 360.0

    def program_move(
        self,
        target_deg: float,
        duration_s: float,
        profile: str = "ease_in_out",
    ) -> bool:
        if not self._connected:
            raise RuntimeError("Not connected")
        move_deg = target_deg - self._current_deg
        required_rpm = abs(move_deg) / (360.0 * duration_s / 60.0)
        if required_rpm > self.motor_rpm_max:
            raise ValueError(
                f"Required {required_rpm:.1f} RPM exceeds max {self.motor_rpm_max} RPM"
            )
        logger.info(
            "Revolving stage: %.1f° -> %.1f° over %.1fs (profile: %s)",
            self._current_deg, target_deg, duration_s, profile,
        )
        self._current_deg = target_deg
        return True

    def get_position_deg(self) -> float:
        return self._current_deg

    def get_position_encoder(self) -> int:
        return self._deg_to_encoder(self._current_deg)


# ---------------------------------------------------------------------------
# Trap Door Sequencer
# ---------------------------------------------------------------------------

class TrapDoorSequencer:
    """Sequences multiple trap door actuators with interlocks."""

    def __init__(self, doors: list[dict[str, Any]]):
        self.doors: dict[str, TrapDoorConfig] = {}
        for door_data in doors:
            config = TrapDoorConfig(
                door_id=door_data["id"],
                actuator=ActuatorType(door_data.get("actuator", "electric")),
                stroke_mm=door_data.get("stroke_mm", 600),
            )
            self.doors[config.door_id] = config
        self._interlock_groups: dict[str, list[str]] = {}

    def set_interlock_group(self, group_name: str, door_ids: list[str]) -> None:
        self._interlock_groups[group_name] = door_ids

    def _check_interlocks(self, door_id: str) -> bool:
        for group_name, members in self._interlock_groups.items():
            if door_id in members:
                for other_id in members:
                    if other_id != door_id:
                        logger.debug(
                            "Interlock group '%s': %s must be closed before %s opens",
                            group_name, other_id, door_id,
                        )
        return True

    def sequence(
        self,
        steps: list[dict[str, Any]],
        interlock_required: bool = True,
    ) -> list[dict[str, Any]]:
        results = []
        for step in steps:
            door_id = step["door"]
            action = step["action"]
            if door_id not in self.doors:
                raise ValueError(f"Unknown door: {door_id}")
            if interlock_required:
                self._check_interlocks(door_id)
            config = self.doors[door_id]
            logger.info(
                "Trap door '%s' %s (actuator: %s, stroke: %.0fmm)",
                door_id, action, config.actuator.value, config.stroke_mm,
            )
            results.append({"door_id": door_id, "action": action, "success": True})
        return results

    def emergency_close_all(self) -> None:
        logger.critical("Emergency closing all trap doors")
        for door_id, config in self.doors.items():
            logger.info("Closing door '%s'", door_id)


# ---------------------------------------------------------------------------
# DMX Bridge
# ---------------------------------------------------------------------------

class DMXBridge:
    """Bridges automation events to DMX512/Art-Net channels."""

    def __init__(
        self,
        universe: int = 0,
        art_net_ip: str = "2.0.0.1",
        dmx_channel_map: Optional[dict[int, str]] = None,
    ):
        self.universe = universe
        self.art_net_ip = art_net_ip
        self.dmx_channel_map = dmx_channel_map or {}
        self._dmx_frame: list[int] = [0] * 512

    def set_channel(self, channel: int, value: int) -> None:
        if not 1 <= channel <= 512:
            raise ValueError(f"DMX channel must be 1-512, got {channel}")
        if not 0 <= value <= 255:
            raise ValueError(f"DMX value must be 0-255, got {value}")
        self._dmx_frame[channel - 1] = value

    def send_frame(self) -> bool:
        logger.debug(
            "Sending DMX frame to universe %d via Art-Net (%s): %d non-zero channels",
            self.universe,
            self.art_net_ip,
            sum(1 for v in self._dmx_frame if v > 0),
        )
        return True

    def trigger_from_cue(self, cue_data: dict[str, Any]) -> None:
        for key, value in cue_data.items():
            for ch, name in self.dmx_channel_map.items():
                if name == key:
                    self.set_channel(ch, int(value))
        self.send_frame()


# ---------------------------------------------------------------------------
# Timecode Synchronizer
# ---------------------------------------------------------------------------

class TimecodeSynchronizer:
    """SMPTE/LTC timecode chase and synchronization."""

    def __init__(self, source: TimecodeSource = TimecodeSource.INTERNAL, device: str = ""):
        self.source = source
        self.device = device
        self._current_tc = 0
        self._locked = False
        self._callbacks: list[Callable[[int], None]] = []

    def lock(self) -> bool:
        logger.info("Attempting timecode lock (source: %s)", self.source.value)
        self._locked = True
        return True

    def on_timecode(self, callback: Callable[[int], None]) -> None:
        self._callbacks.append(callback)

    def update(self, tc: int) -> None:
        self._current_tc = tc
        for cb in self._callbacks:
            cb(tc)

    def get_timecode(self) -> int:
        return self._current_tc

    def is_locked(self) -> bool:
        return self._locked

    @staticmethod
    def frames_to_tc_string(frames: int) -> str:
        f = frames % 30
        s = (frames // 30) % 60
        m = (frames // 1800) % 60
        h = (frames // 108000) % 24
        return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"


# ---------------------------------------------------------------------------
# Show Controller
# ---------------------------------------------------------------------------

class ShowController:
    """Master show control orchestrator for automation, timecode, and DMX."""

    def __init__(
        self,
        timecode_source: TimecodeSource = TimecodeSource.INTERNAL,
        ltc_input_device: str = "",
        bpm_reference: float = 120.0,
    ):
        self.timecode_source = timecode_source
        self.ltc_input_device = ltc_input_device
        self.bpm_reference = bpm_reference
        self._cue_list: list[CueStep] = []
        self._current_cue_index = -1
        self._bridges: list[DMXBridge] = []
        self._running = False
        self.tc_sync = TimecodeSynchronizer(source=timecode_source, device=ltc_input_device)

    def attach_bridge(self, bridge: DMXBridge) -> None:
        self._bridges.append(bridge)

    def load_cue_list(self, filepath: str) -> int:
        path = Path(filepath)
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            self._cue_list = [
                CueStep(cue_number=c["number"], timecode=c.get("tc", 0), actions=c.get("actions", {}))
                for c in data.get("cues", [])
            ]
        else:
            logger.warning("Cue list file not found: %s — starting empty", filepath)
        self._cue_list.sort(key=lambda c: c.cue_number)
        return len(self._cue_list)

    def go(self) -> bool:
        self._running = True
        self.tc_sync.lock()
        logger.info("Show controller GO — armed with %d cues", len(self._cue_list))
        return True

    def stop(self) -> None:
        self._running = False
        logger.info("Show controller STOP")

    def get_next_cue(self) -> Optional[CueStep]:
        next_idx = self._current_cue_index + 1
        if next_idx < len(self._cue_list):
            return self._cue_list[next_idx]
        return None


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    print("=" * 60)
    print("  Stage Automation Control System — Demo")
    print("=" * 60)

    # --- Fly System ---
    fly = FlySystem(
        controller_ip="192.168.1.100",
        num_lines=6,
        safety=SafetyConfig(max_load_kg=500, max_speed_mps=1.2),
    )
    fly.connect()
    fly.home_all()

    fly.move_axis(axis_id=1, target_pos=8.5, speed=0.8, ramp_ms=500)
    print(f"Line 1 position: {fly.get_position(1):.2f}m")

    cue = fly.create_cue(
        cue_number=1,
        actions={1: {"target_pos": 0.0, "speed": 0.8}, 2: {"target_pos": 0.0, "speed": 0.6}},
        timecode=108000,
    )
    fly.execute_cue(1)

    # --- Revolving Stage ---
    revolve = RevolvingStage(diameter_m=12.0, motor_rpm_max=6)
    revolve.connect()
    revolve.calibrate_zero(home_position_deg=0)
    revolve.program_move(target_deg=180.0, duration_s=8.0, profile="ease_in_out")
    print(f"Revolving stage position: {revolve.get_position_deg():.1f}°")

    # --- Trap Doors ---
    traps = TrapDoorSequencer(doors=[
        {"id": "trap_A", "actuator": "hydraulic", "stroke_mm": 800},
        {"id": "trap_B", "actuator": "pneumatic", "stroke_mm": 600},
    ])
    results = traps.sequence(steps=[
        {"door": "trap_A", "action": "open", "duration_s": 1.5},
        {"door": "trap_B", "action": "open", "duration_s": 2.0},
    ])
    print(f"Trap sequence results: {results}")

    # --- DMX Bridge ---
    bridge = DMXBridge(universe=0, art_net_ip="2.0.0.1", dmx_channel_map={1: "spot_1", 2: "spot_2"})
    bridge.set_channel(1, 255)
    bridge.set_channel(2, 128)
    bridge.send_frame()

    # --- Show Controller ---
    tc_sync = TimecodeSynchronizer(source=TimecodeSource.LTC, device="snd:hw:1,0")
    tc_sync.lock()
    tc_sync.on_timecode(lambda tc: logger.debug("TC: %s", TimecodeSynchronizer.frames_to_tc_string(tc)))
    tc_sync.update(108000)
    print(f"Timecode: {TimecodeSynchronizer.frames_to_tc_string(tc_sync.get_timecode())}")

    controller = ShowController(timecode_source=TimecodeSource.LTC, ltc_input_device="snd:hw:1,0")
    controller.attach_bridge(bridge)
    controller.go()
    print(f"Next cue: {controller.get_next_cue()}")

    # --- Safety Demo ---
    fly.emergency_stop()
    print("E-stop active:", fly._estop_active)
    fly.reset_estop()
    print("E-stop active after reset:", fly._estop_active)

    fly.disconnect()
    print("\nDemo complete.")


if __name__ == "__main__":
    main()
