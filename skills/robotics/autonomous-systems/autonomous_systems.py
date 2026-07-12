"""
autonomous_systems.py — Core framework for self-governing robotic agents.

Provides deliberative and reactive planning, mission management, world modeling,
fault detection/recovery (FDIR), and multi-vehicle coordination for autonomous robots.
"""

from __future__ import annotations

import enum
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SystemState(enum.Enum):
    """High-level state of the autonomous system."""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    RECOVERY = "recovery"
    EMERGENCY_STOP = "emergency_stop"
    MISSION_COMPLETE = "mission_complete"
    MISSION_ABORTED = "mission_aborted"
    FAULT = "fault"


class SensorHealthStatus(enum.Enum):
    """Health status of a monitored sensor."""
    NOMINAL = "nominal"
    DEGRADED = "degraded"
    STALE = "stale"
    TIMEOUT = "timeout"
    FAILED = "failed"


class RecoveryAction(enum.Enum):
    """Actions the FDIR manager can take upon detecting a fault."""
    IGNORE = "ignore"
    RESTART_SENSOR = "restart_sensor"
    SWITCH_TO_ODOMETRY = "switch_to_odometry"
    REDUCE_CAPABILITY = "reduce_capability"
    ABORT_MISSION = "abort_mission"


class BehaviorPriority(enum.IntEnum):
    """Priority levels for the subsumption behavior stack."""
    EMERGENCY = 0
    SAFETY = 10
    REGULATORY = 20
    REACTIVE = 30
    DELIBERATIVE = 40


class WaypointType(enum.Enum):
    """Types of waypoints in a mission."""
    STANDARD = "standard"
    HOVER = "hover"
    SCAN = "scan"
    LOITER = "loiter"
    RETURN_HOME = "return_home"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Vector3:
    """3D vector for positions, velocities, and orientations."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def magnitude(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def distance_to(self, other: Vector3) -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2) ** 0.5


@dataclass
class Waypoint:
    """A single waypoint in a mission plan."""
    position: Vector3
    label: str = ""
    waypoint_type: WaypointType = WaypointType.STANDARD
    speed_ms: float = 1.0
    hover_time_s: float = 0.0
    arrival_tolerance_m: float = 0.5
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AbortCondition:
    """Condition that triggers mission abort."""
    condition_type: str
    threshold: float
    sensor_id: str = ""
    enabled: bool = True

    def check(self, telemetry: dict[str, float]) -> bool:
        value = telemetry.get(self.sensor_id, self.threshold + 1)
        if self.condition_type == "battery_below":
            return value < self.threshold
        if self.condition_type == "obstacle_proximity":
            return value < self.threshold
        return False


@dataclass
class Mission:
    """A complete mission with waypoints and abort conditions."""
    mission_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    waypoints: list[Waypoint] = field(default_factory=list)
    abort_conditions: list[AbortCondition] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MissionResult:
    """Result of executing a mission."""
    mission_id: str
    status: SystemState
    waypoints_completed: int = 0
    total_waypoints: int = 0
    duration_s: float = 0.0
    abort_reason: str = ""
    log: list[str] = field(default_factory=list)


@dataclass
class SensorInput:
    """Aggregated sensor data for one control cycle."""
    timestamp_s: float = 0.0
    position: Vector3 = field(default_factory=Vector3)
    velocity: Vector3 = field(default_factory=Vector3)
    orientation: Vector3 = field(default_factory=Vector3)
    lidar_distances: list[float] = field(default_factory=list)
    lidar_min_distance_m: float = float("inf")
    battery_percent: float = 100.0
    gps_fix: bool = True
    imu_data: dict[str, float] = field(default_factory=dict)


@dataclass
class ActuatorCommand:
    """Command sent to actuators in one control cycle."""
    linear_velocity: float = 0.0
    angular_velocity: float = 0.0
    arm_command: dict[str, float] = field(default_factory=dict)
    emergency_stop: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SensorHealth:
    """Health status of a single sensor."""
    sensor_id: str
    status: SensorHealthStatus = SensorHealthStatus.NOMINAL
    last_update_s: float = 0.0
    timeout_ms: int = 500
    error_count: int = 0


@dataclass
class TelemetryRecord:
    """One entry in the flight log."""
    timestamp_s: float
    state: SystemState
    position: Vector3
    command: ActuatorCommand
    sensors: dict[str, float] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Behavior Layer (Subsumption Architecture)
# ---------------------------------------------------------------------------

class BehaviorLayer:
    """Base class for subsumption behavior layers."""

    def __init__(self, name: str, priority: int = BehaviorPriority.DELIBERATIVE):
        self.name = name
        self.priority = priority
        self.enabled = True

    def evaluate(self, sensor: SensorInput) -> ActuatorCommand | None:
        """Return an ActuatorCommand if this layer wants to act, else None."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"BehaviorLayer(name={self.name!r}, priority={self.priority})"


class EmergencyStopLayer(BehaviorLayer):
    """Highest-priority layer: halts the robot on imminent collision."""

    def __init__(self, min_distance_m: float = 0.2):
        super().__init__("emergency_stop", BehaviorPriority.EMERGENCY)
        self.min_distance_m = min_distance_m

    def evaluate(self, sensor: SensorInput) -> ActuatorCommand | None:
        if sensor.lidar_min_distance_m < self.min_distance_m:
            logger.warning("Emergency stop triggered: obstacle at %.2f m", sensor.lidar_min_distance_m)
            return ActuatorCommand(linear_velocity=0.0, angular_velocity=0.0, emergency_stop=True)
        return None


class ObstacleAvoidanceLayer(BehaviorLayer):
    """Reactive layer that steers away from nearby obstacles."""

    def __init__(self, safety_distance_m: float = 1.0, turn_gain: float = 1.5):
        super().__init__("obstacle_avoidance", BehaviorPriority.REACTIVE)
        self.safety_distance_m = safety_distance_m
        self.turn_gain = turn_gain

    def evaluate(self, sensor: SensorInput) -> ActuatorCommand | None:
        if not sensor.lidar_distances:
            return None
        min_idx = min(range(len(sensor.lidar_distances)), key=lambda i: sensor.lidar_distances[i])
        min_dist = sensor.lidar_distances[min_idx]
        if min_dist < self.safety_distance_m:
            # Steer away from the closest obstacle
            angle = (min_idx / max(len(sensor.lidar_distances) - 1, 1)) * 3.14159 - 1.5708
            angular = -angle * self.turn_gain
            return ActuatorCommand(linear_velocity=0.3, angular_velocity=angular)
        return None


# ---------------------------------------------------------------------------
# Fault Detection, Isolation, and Recovery (FDIR)
# ---------------------------------------------------------------------------

class FDIRManager:
    """Monitors sensor health and triggers recovery actions on faults."""

    def __init__(self):
        self._watchdogs: dict[str, int] = {}  # sensor_id -> timeout_ms
        self._health: dict[str, SensorHealth] = {}
        self._fault_handlers: list[Callable[[str, SensorHealth], RecoveryAction]] = []

    def register_watchdog(self, sensor_id: str, timeout_ms: int = 500) -> None:
        self._watchdogs[sensor_id] = timeout_ms
        self._health[sensor_id] = SensorHealth(
            sensor_id=sensor_id,
            status=SensorHealthStatus.NOMINAL,
            last_update_s=time.time(),
            timeout_ms=timeout_ms,
        )
        logger.info("Registered watchdog for sensor '%s' (timeout=%d ms)", sensor_id, timeout_ms)

    def on_fault(self, func: Callable[[str, SensorHealth], RecoveryAction]) -> Callable:
        self._fault_handlers.append(func)
        return func

    def update_sensor(self, sensor_id: str) -> None:
        if sensor_id in self._health:
            self._health[sensor_id].last_update_s = time.time()
            self._health[sensor_id].status = SensorHealthStatus.NOMINAL

    def check_all(self) -> dict[str, RecoveryAction]:
        """Check all sensors and return actions for any that are unhealthy."""
        now = time.time()
        actions: dict[str, RecoveryAction] = {}
        for sid, health in self._health.items():
            elapsed_ms = (now - health.last_update_s) * 1000
            timeout = self._watchdogs.get(sid, 500)
            if elapsed_ms > timeout * 3:
                health.status = SensorHealthStatus.FAILED
            elif elapsed_ms > timeout * 1.5:
                health.status = SensorHealthStatus.TIMEOUT
            elif elapsed_ms > timeout:
                health.status = SensorHealthStatus.STALE
            else:
                health.status = SensorHealthStatus.NOMINAL
                continue

            health.error_count += 1
            logger.warning("Sensor '%s' unhealthy: %s (errors=%d)", sid, health.status.value, health.error_count)
            for handler in self._fault_handlers:
                action = handler(sid, health)
                if action != RecoveryAction.IGNORE:
                    actions[sid] = action
                    break
        return actions

    def get_health(self, sensor_id: str) -> SensorHealth | None:
        return self._health.get(sensor_id)

    def get_all_health(self) -> dict[str, SensorHealth]:
        return dict(self._health)


# ---------------------------------------------------------------------------
# Occupancy Grid and Path Planning
# ---------------------------------------------------------------------------

class OccupancyGrid:
    """Simple 2D occupancy grid for world modeling."""

    def __init__(self, width_cells: int = 200, height_cells: int = 200, resolution: float = 0.1):
        self.width = width_cells
        self.height = height_cells
        self.resolution = resolution
        self.grid: list[list[float]] = [[0.0] * width_cells for _ in range(height_cells)]
        self.origin_x = 0.0
        self.origin_y = 0.0

    def world_to_grid(self, x: float, y: float) -> tuple[int, int]:
        gx = int((x - self.origin_x) / self.resolution)
        gy = int((y - self.origin_y) / self.resolution)
        gx = max(0, min(gx, self.width - 1))
        gy = max(0, min(gy, self.height - 1))
        return gx, gy

    def set_occupied(self, x: float, y: float, confidence: float = 1.0) -> None:
        gx, gy = self.world_to_grid(x, y)
        self.grid[gy][gx] = min(1.0, max(0.0, confidence))

    def is_occupied(self, x: float, y: float) -> bool:
        gx, gy = self.world_to_grid(x, y)
        return self.grid[gy][gx] > 0.5

    def inflate(self, radius_m: float) -> OccupancyGrid:
        inflated = OccupancyGrid(self.width, self.height, self.resolution)
        radius_cells = int(radius_m / self.resolution)
        for gy in range(self.height):
            for gx in range(self.width):
                if self.grid[gy][gx] > 0.5:
                    for dy in range(-radius_cells, radius_cells + 1):
                        for dx in range(-radius_cells, radius_cells + 1):
                            ny, nx = gy + dy, gx + dx
                            if 0 <= ny < self.height and 0 <= nx < self.width:
                                if (dx**2 + dy**2) ** 0.5 <= radius_cells:
                                    inflated.grid[ny][nx] = 1.0
        return inflated


class AStarPlanner:
    """A* path planner on an occupancy grid."""

    def __init__(self, grid: OccupancyGrid, inflation_radius: float = 0.3):
        self.grid = grid
        self.inflated = grid.inflate(inflation_radius)

    def _heuristic(self, a: tuple[int, int], b: tuple[int, int]) -> float:
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5

    def _neighbors(self, node: tuple[int, int]) -> list[tuple[int, int]]:
        gx, gy = node
        result = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nx, ny = gx + dx, gy + dy
            if 0 <= nx < self.inflated.width and 0 <= ny < self.inflated.height:
                if self.inflated.grid[ny][nx] < 0.5:
                    result.append((nx, ny))
        return result

    def plan(self, start: tuple[float, float], goal: tuple[float, float]) -> list[tuple[float, float]]:
        sx, sy = self.grid.world_to_grid(*start)
        gx, gy = self.grid.world_to_grid(*goal)
        open_set: list[tuple[float, tuple[int, int]]] = [(0.0, (sx, sy))]
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], float] = {(sx, sy): 0.0}

        while open_set:
            open_set.sort(key=lambda x: x[0])
            _, current = open_set.pop(0)
            if current == (gx, gy):
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return [
                    (p[0] * self.grid.resolution + self.grid.origin_x,
                     p[1] * self.grid.resolution + self.grid.origin_y)
                    for p in path
                ]

            for neighbor in self._neighbors(current):
                tentative_g = g_score[current] + self._heuristic(current, neighbor)
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self._heuristic(neighbor, (gx, gy))
                    open_set.append((f, neighbor))

        logger.warning("A* planner: no path found from %s to %s", start, goal)
        return []


# ---------------------------------------------------------------------------
# Autonomous Engine
# ---------------------------------------------------------------------------

class AutonomousEngine:
    """Main engine orchestrating the sense-plan-act loop for an autonomous robot."""

    def __init__(self, name: str = "autonomous-robot"):
        self.name = name
        self.state = SystemState.IDLE
        self._behavior_stack: list[BehaviorLayer] = []
        self._fdir = FDIRManager()
        self._telemetry: list[TelemetryRecord] = []
        self._config: dict[str, Any] = {}
        self._current_mission: Mission | None = None
        self._waypoint_index: int = 0

    def configure(self, **kwargs: Any) -> None:
        """Configure the engine with key-value parameters."""
        self._config.update(kwargs)
        self._fdir.register_watchdog("imu", kwargs.get("imu_timeout_ms", 100))
        self._fdir.register_watchdog("gps", kwargs.get("gps_timeout_ms", 500))
        self._fdir.register_watchdog("lidar", kwargs.get("lidar_timeout_ms", 200))
        logger.info("Engine '%s' configured: %s", self.name, self._config)

    def add_behavior(self, layer: BehaviorLayer) -> None:
        self._behavior_stack.append(layer)
        self._behavior_stack.sort(key=lambda l: l.priority)

    def run(self, mission: Mission) -> MissionResult:
        """Execute a full mission and return the result."""
        self._current_mission = mission
        self._waypoint_index = 0
        self.state = SystemState.PLANNING
        result = MissionResult(
            mission_id=mission.mission_id,
            status=SystemState.EXECUTING,
            total_waypoints=len(mission.waypoints),
        )
        start_time = time.time()
        logger.info("Starting mission '%s' with %d waypoints", mission.name, len(mission.waypoints))

        while self._waypoint_index < len(mission.waypoints):
            # Check abort conditions
            telemetry = self._build_telemetry_snapshot()
            for ac in mission.abort_conditions:
                if ac.check(telemetry):
                    self.state = SystemState.MISSION_ABORTED
                    result.status = SystemState.MISSION_ABORTED
                    result.abort_reason = f"Abort condition met: {ac.condition_type} < {ac.threshold}"
                    result.log.append(result.abort_reason)
                    result.duration_s = time.time() - start_time
                    logger.warning(result.abort_reason)
                    return result

            # FDIR check
            faults = self._fdir.check_all()
            for sensor_id, action in faults.items():
                if action == RecoveryAction.ABORT_MISSION:
                    self.state = SystemState.FAULT
                    result.status = SystemState.MISSION_ABORTED
                    result.abort_reason = f"Sensor fault: {sensor_id} -> {action.value}"
                    result.log.append(result.abort_reason)
                    result.duration_s = time.time() - start_time
                    return result

            # Execute waypoint
            wp = mission.waypoints[self._waypoint_index]
            logger.info("Navigating to waypoint '%s' at (%.1f, %.1f, %.1f)", wp.label, wp.position.x, wp.position.y, wp.position.z)
            result.log.append(f"Waypoint {self._waypoint_index}: {wp.label}")
            self._waypoint_index += 1

        self.state = SystemState.MISSION_COMPLETE
        result.status = SystemState.MISSION_COMPLETE
        result.waypoints_completed = len(mission.waypoints)
        result.duration_s = time.time() - start_time
        logger.info("Mission '%s' completed in %.1f s", mission.name, result.duration_s)
        return result

    def get_status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "state": self.state.value,
            "behaviors": [b.name for b in self._behavior_stack],
            "fdir_health": {k: v.status.value for k, v in self._fdir.get_all_health().items()},
            "telemetry_count": len(self._telemetry),
            "config": self._config,
        }

    def _build_telemetry_snapshot(self) -> dict[str, float]:
        return {
            "battery": self._config.get("battery_percent", 100.0),
            "lidar_min": self._config.get("lidar_min_distance_m", 5.0),
        }

    def process_sensors(self, sensor: SensorInput) -> ActuatorCommand:
        """Run the behavior stack on fresh sensor data and return the winning command."""
        for layer in self._behavior_stack:
            if not layer.enabled:
                continue
            cmd = layer.evaluate(sensor)
            if cmd is not None:
                logger.debug("Behavior '%s' produced command", layer.name)
                return cmd
        return ActuatorCommand(linear_velocity=0.0, angular_velocity=0.0)


# ---------------------------------------------------------------------------
# Multi-Vehicle Coordinator
# ---------------------------------------------------------------------------

class VehicleHandle:
    """Reference to a vehicle in a multi-vehicle formation."""

    def __init__(self, vehicle_id: str, position: Vector3):
        self.vehicle_id = vehicle_id
        self.position = position
        self.role = "follower"


class FormationController:
    """Leader-follower formation controller."""

    def __init__(self):
        self.leader: VehicleHandle | None = None
        self.followers: list[VehicleHandle] = []
        self.offsets: dict[str, Vector3] = {}

    def set_leader(self, vehicle: VehicleHandle) -> None:
        vehicle.role = "leader"
        self.leader = vehicle

    def add_follower(self, vehicle: VehicleHandle, offset: Vector3) -> None:
        self.followers.append(vehicle)
        self.offsets[vehicle.vehicle_id] = offset

    def compute_desired_positions(self) -> dict[str, Vector3]:
        if self.leader is None:
            return {}
        desired: dict[str, Vector3] = {}
        for follower in self.followers:
            offset = self.offsets.get(follower.vehicle_id, Vector3())
            desired[follower.vehicle_id] = Vector3(
                x=self.leader.position.x + offset.x,
                y=self.leader.position.y + offset.y,
                z=self.leader.position.z + offset.z,
            )
        return desired

    def get_formation_error(self) -> dict[str, float]:
        desired = self.compute_desired_positions()
        errors: dict[str, float] = {}
        for follower in self.followers:
            if follower.vehicle_id in desired:
                errors[follower.vehicle_id] = follower.position.distance_to(desired[follower.vehicle_id])
        return errors


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the autonomous systems module."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    print("=== Autonomous Systems Demo ===\n")

    # 1. Configure the engine
    engine = AutonomousEngine(name="rover-alpha")
    engine.configure(
        control_frequency_hz=50,
        safety_enabled=True,
        max_velocity_ms=2.0,
        battery_percent=85.0,
        imu_timeout_ms=100,
        gps_timeout_ms=500,
    )

    # 2. Add behavior layers
    engine.add_behavior(EmergencyStopLayer(min_distance_m=0.2))
    engine.add_behavior(ObstacleAvoidanceLayer(safety_distance_m=1.0, turn_gain=1.5))

    # 3. Register fault handlers
    @engine._fdir.on_fault
    def on_sensor_fault(sensor_id: str, health: SensorHealth) -> RecoveryAction:
        if health.status in (SensorHealthStatus.TIMEOUT, SensorHealthStatus.FAILED):
            return RecoveryAction.ABORT_MISSION
        return RecoveryAction.IGNORE

    # 4. Create and run a mission
    mission = Mission(
        name="field-survey",
        waypoints=[
            Waypoint(position=Vector3(0, 0, 0), label="home", waypoint_type=WaypointType.RETURN_HOME),
            Waypoint(position=Vector3(10, 5, 0), label="scan-1", waypoint_type=WaypointType.SCAN),
            Waypoint(position=Vector3(10, 15, 0), label="scan-2", waypoint_type=WaypointType.SCAN),
            Waypoint(position=Vector3(0, 15, 0), label="scan-3", waypoint_type=WaypointType.SCAN),
        ],
        abort_conditions=[
            AbortCondition(condition_type="battery_below", threshold=15.0, sensor_id="battery"),
            AbortCondition(condition_type="obstacle_proximity", threshold=0.3, sensor_id="lidar_min"),
        ],
    )
    result = engine.run(mission)
    print(f"Mission result: {result.status.value}")
    print(f"Waypoints completed: {result.waypoints_completed}/{result.total_waypoints}")
    print(f"Duration: {result.duration_s:.2f} s")

    # 5. Sensor processing demo
    print("\n--- Sensor Processing ---")
    sensor = SensorInput(
        timestamp_s=time.time(),
        lidar_distances=[2.0, 1.5, 0.8, 0.3, 1.2, 2.5],
        lidar_min_distance_m=0.3,
    )
    cmd = engine.process_sensors(sensor)
    print(f"Actuator command: linear={cmd.linear_velocity:.2f}, angular={cmd.angular_velocity:.2f}")

    # 6. World model demo
    print("\n--- Occupancy Grid & Path Planning ---")
    grid = OccupancyGrid(width_cells=100, height_cells=100, resolution=0.1)
    for i in range(20, 40):
        grid.set_occupied(i * 0.1, 1.0, confidence=0.9)
    planner = AStarPlanner(grid, inflation_radius=0.3)
    path = planner.plan((0.0, 0.0), (5.0, 5.0))
    print(f"Planned path with {len(path)} points")

    # 7. Multi-vehicle formation
    print("\n--- Formation Control ---")
    fc = FormationController()
    leader = VehicleHandle("uav-1", Vector3(0, 0, 10))
    fc.set_leader(leader)
    fc.add_follower(VehicleHandle("uav-2", Vector3(-1, -1, 10)), Vector3(-3, 0, 0))
    fc.add_follower(VehicleHandle("uav-3", Vector3(1, -1, 10)), Vector3(3, 0, 0))
    errors = fc.get_formation_error()
    for vid, err in errors.items():
        print(f"  {vid} formation error: {err:.2f} m")

    # 8. Status
    print("\n--- Engine Status ---")
    for key, value in engine.get_status().items():
        print(f"  {key}: {value}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
