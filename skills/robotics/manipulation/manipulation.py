"""
manipulation.py — Robotic arm control, kinematics, grasp planning, and force control.

Provides forward/inverse kinematics, trajectory generation, grasp synthesis,
force control, visual servoing, and task sequencing for manipulation applications.
"""

from __future__ import annotations

import enum
import logging
import math
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class JointType(enum.Enum):
    """Types of robotic joints."""
    REVOLUTE = "revolute"
    PRISMATIC = "prismatic"
    FIXED = "fixed"


class TaskState(enum.Enum):
    """States of a manipulation task."""
    IDLE = "idle"
    APPROACHING = "approaching"
    DESCENDING = "descending"
    GRASPING = "grasping"
    LIFTING = "lifting"
    TRANSPORTING = "transporting"
    PLACING = "placing"
    RELEASING = "releasing"
    RETREATING = "retreating"
    COMPLETED = "completed"
    FAILED = "failed"


class GraspType(enum.Enum):
    """Types of grasps."""
    ANTIPODAL = "antipodal"
    POWER = "power"
    PINCH = "pinch"
    ENVELOPING = "enveloping"
    SUCTIOn = "suction"


class ForceMode(enum.Enum):
    """Force control modes."""
    POSITION = "position"
    FORCE = "force"
    IMPEDANCE = "impedance"
    HYBRID = "hybrid"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class DHParameters:
    """Denavit-Hartenberg parameters for a robot arm."""
    d: list[float] = field(default_factory=list)       # link offset
    a: list[float] = field(default_factory=list)       # link length
    alpha: list[float] = field(default_factory=list)   # link twist
    theta_offset: list[float] = field(default_factory=list)  # joint angle offset

    @property
    def num_joints(self) -> int:
        return len(self.d)


@dataclass
class JointAngles:
    """Joint angles for a robot arm."""
    values: list[float] = field(default_factory=list)
    timestamp_s: float = 0.0

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, idx: int) -> float:
        return self.values[idx]


@dataclass
class JointLimits:
    """Joint angle and velocity limits."""
    lower: list[float] = field(default_factory=list)
    upper: list[float] = field(default_factory=list)
    velocity_limit: list[float] = field(default_factory=list)
    effort_limit: list[float] = field(default_factory=list)


@dataclass
class Pose:
    """6-DOF pose (position + orientation as Euler angles)."""
    position: tuple[float, float, float] = (0.0, 0.0, 0.0)
    orientation: tuple[float, float, float] = (0.0, 0.0, 0.0)  # roll, pitch, yaw
    rotation_matrix: list[list[float]] = field(
        default_factory=lambda: [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    )


@dataclass
class TrajectoryConfig:
    """Configuration for trajectory generation."""
    max_velocity: float = 1.0
    max_acceleration: float = 2.0
    time_step: float = 0.001
    blend_radius: float = 0.05


@dataclass
class TrajectoryPoint:
    """A single point along a trajectory."""
    joint_angles: JointAngles
    velocity: list[float] = field(default_factory=list)
    acceleration: list[float] = field(default_factory=list)
    time_s: float = 0.0


@dataclass
class Trajectory:
    """A complete trajectory through waypoints."""
    points: list[TrajectoryPoint] = field(default_factory=list)
    duration_s: float = 0.0

    @property
    def num_points(self) -> int:
        return len(self.points)


@dataclass
class GraspConfig:
    """Configuration for grasp planning."""
    approach_distance: float = 0.1
    pre_grasp_distance: float = 0.05
    force_threshold_n: float = 20.0
    max_grasps: int = 10


@dataclass
class ObjectGeometry:
    """Geometry of an object to be grasped."""
    shape: str = "box"
    dimensions: tuple[float, float, float] = (0.1, 0.1, 0.1)
    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    surface_normals: list[tuple[float, float, float]] = field(default_factory=list)


@dataclass
class GraspCandidate:
    """A candidate grasp configuration."""
    grasp_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    grasp_type: GraspType = GraspType.ANTIPODAL
    approach_vector: tuple[float, float, float] = (0.0, 0.0, -1.0)
    grasp_point: tuple[float, float, float] = (0.0, 0.0, 0.0)
    pre_grasp_pose: Pose = field(default_factory=Pose)
    grasp_pose: Pose = field(default_factory=Pose)
    quality_score: float = 0.0
    force_required_n: float = 0.0


@dataclass
class ForceTarget:
    """Target force and torque for force-controlled manipulation."""
    desired_force: tuple[float, float, float] = (0.0, 0.0, 0.0)
    desired_torque: tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class ForceTorqueReading:
    """Force-torque sensor reading."""
    force: tuple[float, float, float] = (0.0, 0.0, 0.0)
    torque: tuple[float, float, float] = (0.0, 0.0, 0.0)
    timestamp_s: float = 0.0


@dataclass
class GripperCommand:
    """Command for a gripper."""
    position: float = 0.0        # 0.0 = open, 1.0 = closed
    force: float = 10.0          # gripping force in Newtons
    speed: float = 0.05          # m/s


# ---------------------------------------------------------------------------
# Forward Kinematics
# ---------------------------------------------------------------------------

class ForwardKinematics:
    """Compute end-effector pose from joint angles using DH parameters."""

    def __init__(self, dh: DHParameters):
        self.dh = dh

    def compute(self, joints: JointAngles) -> Pose:
        """Compute the end-effector pose for given joint angles."""
        T = self._identity_matrix()
        for i in range(min(len(joints), self.dh.num_joints)):
            d = self.dh.d[i]
            a = self.dh.a[i]
            alpha_rad = math.radians(self.dh.alpha[i])
            theta = joints[i]

            # DH transformation matrix
            ct, st = math.cos(theta), math.sin(theta)
            ca, sa = math.cos(alpha_rad), math.sin(alpha_rad)

            T_i = [
                [ct, -st * ca, st * sa, a * ct],
                [st, ct * ca, -ct * sa, a * st],
                [0, sa, ca, d],
                [0, 0, 0, 1],
            ]
            T = self._mat_mul(T, T_i)

        position = (T[0][3], T[1][3], T[2][3])
        # Extract Euler angles from rotation matrix
        roll = math.atan2(T[2][1], T[2][2])
        pitch = math.atan2(-T[2][0], math.sqrt(T[2][1]**2 + T[2][2]**2))
        yaw = math.atan2(T[1][0], T[0][0])

        return Pose(
            position=position,
            orientation=(roll, pitch, yaw),
            rotation_matrix=[row[:3] for row in T[:3]],
        )

    def _identity_matrix(self) -> list[list[float]]:
        return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    def _mat_mul(self, A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
        result = [[0.0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i][j] += A[i][k] * B[k][j]
        return result


# ---------------------------------------------------------------------------
# Inverse Kinematics
# ---------------------------------------------------------------------------

class InverseKinematics:
    """Numerical inverse kinematics using the Jacobian transpose method."""

    def __init__(self, fk: ForwardKinematics, dh: DHParameters, max_iterations: int = 100,
                 tolerance: float = 0.001):
        self.fk = fk
        self.dh = dh
        self.max_iterations = max_iterations
        self.tolerance = tolerance

    def solve(self, target: Pose, initial_guess: JointAngles | None = None) -> JointAngles | None:
        """Solve IK for the target pose."""
        if initial_guess is None:
            initial_guess = JointAngles(values=[0.0] * self.dh.num_joints)

        joints = list(initial_guess.values)
        for iteration in range(self.max_iterations):
            current = self.fk.compute(JointAngles(values=joints))
            error = self._pose_error(current, target)

            if error < self.tolerance:
                logger.info("IK converged at iteration %d (error=%.4f)", iteration, error)
                return JointAngles(values=joints)

            # Compute numerical Jacobian
            jacobian = self._compute_jacobian(JointAngles(values=joints))

            # Jacobian transpose method
            dt = 0.1
            for i in range(len(joints)):
                delta = sum(jacobian[j][i] * (target.position[j] - current.position[j]) for j in range(3))
                joints[i] += dt * delta

        logger.warning("IK did not converge after %d iterations", self.max_iterations)
        return None

    def _pose_error(self, current: Pose, target: Pose) -> float:
        dx = target.position[0] - current.position[0]
        dy = target.position[1] - current.position[1]
        dz = target.position[2] - current.position[2]
        return math.sqrt(dx**2 + dy**2 + dz**2)

    def _compute_jacobian(self, joints: JointAngles) -> list[list[float]]:
        """Compute the 3xN Jacobian numerically."""
        delta = 0.001
        n = len(joints)
        jacobian = [[0.0] * n for _ in range(3)]
        base_pose = self.fk.compute(joints)

        for i in range(n):
            perturbed = list(joints.values)
            perturbed[i] += delta
            perturbed_pose = self.fk.compute(JointAngles(values=perturbed))
            for j in range(3):
                jacobian[j][i] = (perturbed_pose.position[j] - base_pose.position[j]) / delta
        return jacobian


# ---------------------------------------------------------------------------
# Trajectory Generation
# ---------------------------------------------------------------------------

class TrajectoryGenerator:
    """Generate smooth trajectories through waypoints."""

    def __init__(self, config: TrajectoryConfig | None = None):
        self.config = config or TrajectoryConfig()

    def generate(self, waypoints: list[JointAngles]) -> Trajectory:
        """Generate a trajectory through the given waypoints."""
        if len(waypoints) < 2:
            return Trajectory(points=[
                TrajectoryPoint(joint_angles=waypoints[0] if waypoints else JointAngles(), time_s=0.0)
            ])

        all_points: list[TrajectoryPoint] = []
        total_time = 0.0

        for i in range(len(waypoints) - 1):
            start = waypoints[i]
            end = waypoints[i + 1]
            segment = self._generate_segment(start, end, total_time)
            all_points.extend(segment)
            if segment:
                total_time = segment[-1].time_s

        return Trajectory(points=all_points, duration_s=total_time)

    def _generate_segment(self, start: JointAngles, end: JointAngles,
                          time_offset: float) -> list[TrajectoryPoint]:
        """Generate a cubic polynomial trajectory for one segment."""
        n_joints = max(len(start), len(end))
        duration = 0.0

        # Compute duration based on max velocity constraint
        for j in range(n_joints):
            displacement = abs(end[j] - start[j])
            t = 2.0 * displacement / self.config.max_velocity
            duration = max(duration, t)

        if duration < 0.01:
            duration = 0.5

        points: list[TrajectoryPoint] = []
        dt = self.config.time_step
        t = 0.0
        while t <= duration:
            s = self._cubic_profile(t, duration)
            values = []
            for j in range(n_joints):
                val = start[j] + (end[j] - start[j]) * s
                values.append(val)
            points.append(TrajectoryPoint(
                joint_angles=JointAngles(values=values),
                time_s=time_offset + t,
            ))
            t += dt

        return points

    def _cubic_profile(self, t: float, duration: float) -> float:
        """Cubic time profile: smooth acceleration and deceleration."""
        if t <= 0:
            return 0.0
        if t >= duration:
            return 1.0
        s = t / duration
        return 3 * s**2 - 2 * s**3  # smoothstep


# ---------------------------------------------------------------------------
# Grasp Planning
# ---------------------------------------------------------------------------

class GraspPlanner:
    """Plan grasps for objects based on geometry."""

    def __init__(self, config: GraspConfig | None = None):
        self.config = config or GraspConfig()

    def plan_grasps(self, obj: ObjectGeometry) -> list[GraspCandidate]:
        """Generate ranked grasp candidates for an object."""
        grasps: list[GraspCandidate] = []

        if obj.shape == "box":
            grasps.extend(self._box_grasps(obj))
        elif obj.shape == "cylinder":
            grasps.extend(self._cylinder_grasps(obj))
        else:
            grasps.extend(self._generic_grasps(obj))

        grasps.sort(key=lambda g: g.quality_score, reverse=True)
        return grasps[:self.config.max_grasps]

    def _box_grasps(self, obj: ObjectGeometry) -> list[GraspCandidate]:
        grasps = []
        cx, cy, cz = obj.center
        w, h, d = obj.dimensions

        # Top grasp
        grasps.append(GraspCandidate(
            grasp_type=GraspType.ANTIPODAL,
            approach_vector=(0, 0, -1),
            grasp_point=(cx, cy, cz + d / 2),
            quality_score=0.9,
            force_required_n=self.config.force_threshold_n,
        ))
        # Side grasps
        for axis, normal in [("x", (1, 0, 0)), ("x", (-1, 0, 0)), ("y", (0, 1, 0)), ("y", (0, -1, 0))]:
            grasps.append(GraspCandidate(
                grasp_type=GraspType.ANTIPODAL,
                approach_vector=normal,
                grasp_point=(cx, cy, cz),
                quality_score=0.7,
                force_required_n=self.config.force_threshold_n * 1.2,
            ))
        return grasps

    def _cylinder_grasps(self, obj: ObjectGeometry) -> list[GraspCandidate]:
        cx, cy, cz = obj.center
        grasps = [
            GraspCandidate(
                grasp_type=GraspType.POWER,
                approach_vector=(0, 0, -1),
                grasp_point=(cx, cy, cz + obj.dimensions[2] / 2),
                quality_score=0.85,
            ),
            GraspCandidate(
                grasp_type=GraspType.ANTIPODAL,
                approach_vector=(1, 0, 0),
                grasp_point=(cx, cy, cz),
                quality_score=0.75,
            ),
        ]
        return grasps

    def _generic_grasps(self, obj: ObjectGeometry) -> list[GraspCandidate]:
        return [GraspCandidate(
            grasp_type=GraspType.PINCH,
            approach_vector=(0, 0, -1),
            grasp_point=obj.center,
            quality_score=0.5,
        )]


# ---------------------------------------------------------------------------
# Force Controller
# ---------------------------------------------------------------------------

class ForceController:
    """PID-based force/impedance controller for manipulation."""

    def __init__(self, kp: float = 50.0, kd: float = 5.0, ki: float = 0.1,
                 force_limit_n: float = 30.0, mode: ForceMode = ForceMode.IMPEDANCE):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.force_limit_n = force_limit_n
        self.mode = mode
        self._integral_error = [0.0, 0.0, 0.0]
        self._prev_error = [0.0, 0.0, 0.0]

    def compute(self, current: ForceTorqueReading, target: ForceTarget,
                dt: float = 0.001) -> list[float]:
        """Compute the force control command."""
        cmd = [0.0, 0.0, 0.0]
        for i in range(3):
            error = target.desired_force[i] - current.force[i]
            self._integral_error[i] += error * dt
            derivative = (error - self._prev_error[i]) / max(dt, 1e-6)

            output = self.kp * error + self.kd * derivative + self.ki * self._integral_error[i]
            output = max(-self.force_limit_n, min(self.force_limit_n, output))
            cmd[i] = output
            self._prev_error[i] = error

        return cmd

    def reset(self) -> None:
        self._integral_error = [0.0, 0.0, 0.0]
        self._prev_error = [0.0, 0.0, 0.0]


# ---------------------------------------------------------------------------
# Gripper Controller
# ---------------------------------------------------------------------------

class GripperController:
    """Control a parallel-jaw gripper."""

    def __init__(self, max_opening_m: float = 0.08, max_force_n: float = 20.0):
        self.max_opening_m = max_opening_m
        self.max_force_n = max_force_n
        self.current_position = 0.0  # 0=open, 1=closed
        self.is_grasping = False

    def open(self, speed: float = 0.05) -> GripperCommand:
        self.current_position = 0.0
        self.is_grasping = False
        return GripperCommand(position=0.0, force=0.0, speed=speed)

    def close(self, force: float = 10.0, speed: float = 0.05) -> GripperCommand:
        self.current_position = 1.0
        return GripperCommand(position=1.0, force=force, speed=speed)

    def grasp(self, object_width_m: float, force: float = 10.0) -> GripperCommand:
        position = min(1.0, object_width_m / self.max_opening_m)
        self.current_position = position
        self.is_grasping = True
        return GripperCommand(position=position, force=force)

    def get_opening_m(self) -> float:
        return self.current_position * self.max_opening_m


# ---------------------------------------------------------------------------
# Robot Arm
# ---------------------------------------------------------------------------

class RobotArm:
    """Complete robot arm with kinematics and trajectory execution."""

    def __init__(self, name: str, dh_params: DHParameters, num_joints: int = 7,
                 joint_limits: JointLimits | None = None):
        self.name = name
        self.dh_params = dh_params
        self.num_joints = num_joints
        self.joint_limits = joint_limits
        self._fk = ForwardKinematics(dh_params)
        self._ik = InverseKinematics(self._fk, dh_params)
        self._gripper = GripperController()
        self._current_joints = JointAngles(values=[0.0] * num_joints)

    def forward_kinematics(self, joints: JointAngles) -> Pose:
        return self._fk.compute(joints)

    def inverse_kinematics(self, target: Pose, initial_guess: JointAngles | None = None) -> JointAngles | None:
        return self._ik.solve(target, initial_guess)

    def validate_joints(self, joints: JointAngles) -> bool:
        if self.joint_limits is None:
            return True
        for i in range(min(len(joints), len(self.joint_limits.lower))):
            if joints[i] < self.joint_limits.lower[i] or joints[i] > self.joint_limits.upper[i]:
                logger.warning("Joint %d out of limits: %.3f not in [%.3f, %.3f]",
                               i, joints[i], self.joint_limits.lower[i], self.joint_limits.upper[i])
                return False
        return True

    def get_gripper(self) -> GripperController:
        return self._gripper


# ---------------------------------------------------------------------------
# Pick-and-Place Task
# ---------------------------------------------------------------------------

class PickPlaceTask:
    """State-machine-based pick-and-place task."""

    def __init__(self, pick_location: tuple[float, float, float],
                 place_location: tuple[float, float, float],
                 object_width: float = 0.08,
                 approach_height: float = 0.15):
        self.pick_location = pick_location
        self.place_location = place_location
        self.object_width = object_width
        self.approach_height = approach_height
        self.state = TaskState.IDLE
        self._step_count = 0

    def start(self) -> None:
        self.state = TaskState.APPROACHING
        self._step_count = 0
        logger.info("Pick-and-place task started")

    def step(self) -> dict[str, Any]:
        """Advance the task state machine by one step."""
        self._step_count += 1
        command: dict[str, Any] = {"step": self._step_count}

        if self.state == TaskState.APPROACHING:
            command["target"] = (self.pick_location[0], self.pick_location[1], self.approach_height)
            self.state = TaskState.DESCENDING
        elif self.state == TaskState.DESCENDING:
            command["target"] = self.pick_location
            self.state = TaskState.GRASPING
        elif self.state == TaskState.GRASPING:
            command["gripper"] = "close"
            command["force"] = 10.0
            self.state = TaskState.LIFTING
        elif self.state == TaskState.LIFTING:
            command["target"] = (self.pick_location[0], self.pick_location[1], self.approach_height)
            self.state = TaskState.TRANSPORTING
        elif self.state == TaskState.TRANSPORTING:
            command["target"] = (self.place_location[0], self.place_location[1], self.approach_height)
            self.state = TaskState.PLACING
        elif self.state == TaskState.PLACING:
            command["target"] = self.place_location
            self.state = TaskState.RELEASING
        elif self.state == TaskState.RELEASING:
            command["gripper"] = "open"
            self.state = TaskState.RETREATING
        elif self.state == TaskState.RETREATING:
            command["target"] = (self.place_location[0], self.place_location[1], self.approach_height)
            self.state = TaskState.COMPLETED
        elif self.state == TaskState.COMPLETED:
            command["message"] = "Task complete"
        elif self.state == TaskState.FAILED:
            command["message"] = "Task failed"

        return command


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the manipulation module."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    print("=== Manipulation Demo ===\n")

    # 1. Robot Arm with Kinematics
    print("--- Forward & Inverse Kinematics ---")
    dh = DHParameters(
        d=[0.333, 0, 0.316, 0, 0.384, 0, 0.107],
        a=[0, 0, 0, 0.0825, -0.0825, 0, 0],
        alpha=[0, -90, 90, 90, -90, 90, 0],
    )
    arm = RobotArm(name="panda", dh_params=dh, num_joints=7)
    joints = JointAngles(values=[0.0, -0.5, 0.0, -2.0, 0.0, 1.5, 0.785])
    ee_pose = arm.forward_kinematics(joints)
    print(f"FK: position={ee_pose.position}, orientation={ee_pose.orientation}")

    target = Pose(position=(0.4, 0.2, 0.3))
    ik_result = arm.inverse_kinematics(target)
    if ik_result:
        print(f"IK: {ik_result.values[:3]}...")

    # 2. Trajectory Generation
    print("\n--- Trajectory Generation ---")
    traj_gen = TrajectoryGenerator(TrajectoryConfig(max_velocity=1.0, max_acceleration=2.0))
    waypoints = [
        JointAngles(values=[0.0, -0.5, 0.0, -2.0, 0.0, 1.5, 0.785]),
        JointAngles(values=[0.5, -0.3, 0.2, -1.5, 0.1, 1.2, 0.5]),
        JointAngles(values=[0.3, 0.0, -0.1, -1.8, -0.2, 1.0, 0.3]),
    ]
    trajectory = traj_gen.generate(waypoints)
    print(f"Trajectory: {trajectory.num_points} points, {trajectory.duration_s:.2f} s")

    # 3. Grasp Planning
    print("\n--- Grasp Planning ---")
    planner = GraspPlanner(GraspConfig(approach_distance=0.1))
    box = ObjectGeometry(shape="box", dimensions=(0.1, 0.15, 0.08), center=(0.5, 0.3, 0.04))
    grasps = planner.plan_grasps(box)
    for i, g in enumerate(grasps[:3]):
        print(f"  Grasp {i}: type={g.grasp_type.value}, quality={g.quality_score:.3f}, "
              f"approach={g.approach_vector}")

    # 4. Force Control
    print("\n--- Force Control ---")
    force_ctrl = ForceController(kp=50.0, kd=5.0, ki=0.1, force_limit_n=30.0)
    target_force = ForceTarget(desired_force=(0.0, 0.0, -10.0))
    reading = ForceTorqueReading(force=(0.0, 0.0, -2.0))
    cmd = force_ctrl.compute(reading, target_force, dt=0.001)
    print(f"  Force command: [{cmd[0]:.2f}, {cmd[1]:.2f}, {cmd[2]:.2f}]")

    # 5. Gripper Control
    print("\n--- Gripper Control ---")
    gripper = GripperController(max_opening_m=0.08)
    cmd = gripper.grasp(0.05, force=10.0)
    print(f"  Grasp: pos={cmd.position:.2f}, opening={gripper.get_opening_m()*1000:.1f}mm")
    cmd = gripper.open()
    print(f"  Open: pos={cmd.position:.2f}")

    # 6. Pick-and-Place Task
    print("\n--- Pick-and-Place Task ---")
    task = PickPlaceTask(
        pick_location=(0.4, 0.2, 0.05),
        place_location=(0.4, -0.2, 0.05),
        object_width=0.08,
        approach_height=0.15,
    )
    task.start()
    while task.state != TaskState.COMPLETED:
        cmd = task.step()
        print(f"  Step {cmd['step']}: {task.state.value}")
        if cmd.get("gripper"):
            print(f"    Gripper: {cmd['gripper']}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
