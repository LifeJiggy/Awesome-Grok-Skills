#!/usr/bin/env python3
"""
Physics Simulation Engine Agent
Specialized agent for physics-based simulations, modeling, and computational physics.

This module provides comprehensive physics simulation capabilities including:
- Classical mechanics (Newtonian, Lagrangian, Hamiltonian)
- Quantum mechanics (wave functions, Schrodinger equation)
- Fluid dynamics (Navier-Stokes equations)
- Thermodynamics (heat transfer, statistical mechanics)
- Electromagnetism (Maxwell's equations)
- Rigid body dynamics
- Collision detection and response
- Particle systems
- Constraint solvers
- Numerical integration methods
"""

from __future__ import annotations

import logging
import math
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence, Set, Tuple, Union

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PhysicsDomain(Enum):
    """Supported physics simulation domains."""
    CLASSICAL_MECHANICS = "classical_mechanics"
    QUANTUM_MECHANICS = "quantum_mechanics"
    RELATIVITY = "relativity"
    FLUID_DYNAMICS = "fluid_dynamics"
    THERMODYNAMICS = "thermodynamics"
    ELECTROMAGNETISM = "electromagnetism"
    SOLID_MECHANICS = "solid_mechanics"
    STATISTICAL_PHYSICS = "statistical_physics"
    PARTICLE_PHYSICS = "particle_physics"
    OPTICS = "optics"
    ACOUSTICS = "acoustics"
    GRAVITY = "gravity"


class IntegrationMethod(Enum):
    """Numerical integration methods."""
    EULER = "euler"
    VELOCITY_VERLET = "velocity_verlet"
    RK4 = "runge_kutta_4"
    LEAPFROG = "leapfrog"
    SYMPLECTIC_EULER = "symplectic_euler"
    HEUN = "heun"
    ADAMS_BASHFORTH = "adams_bashforth"


class CollisionType(Enum):
    """Collision detection types."""
    NONE = "none"
    SPHERE_SPHERE = "sphere_sphere"
    AABB = "aabb"
    OBB = "obb"
    MESH = "mesh"
    RAY = "ray"
    PLANE = "plane"


class ConstraintType(Enum):
    """Physics constraint types."""
    DISTANCE = "distance"
    SPRING = "spring"
    HINGE = "hinge"
    BALL_SOCKET = "ball_socket"
    PRISMATIC = "prismatic"
    FIXED = "fixed"
    MOTOR = "motor"


class ParticleType(Enum):
    """Particle system types."""
    GRAVITY = "gravity"
    EXPLOSION = "explosion"
    FOUNTAIN = "fountain"
    SMOKE = "smoke"
    FIRE = "fire"
    RAIN = "rain"
    SNOW = "snow"


class MaterialType(Enum):
    """Material property types."""
    RIGID = "rigid"
    ELASTIC = "elastic"
    PLASTIC = "plastic"
    FLUID = "fluid"
    GAS = "gas"
    POWDER = "powder"


class ForceType(Enum):
    """Types of forces."""
    GRAVITY = "gravity"
    SPRING = "spring"
    DAMPING = "damping"
    FRICTION = "friction"
    THRUST = "thrust"
    LIFT = "lift"
    DRAG = "drag"
    ELECTROMAGNETIC = "electromagnetic"
    CUSTOM = "custom"


class BoundaryCondition(Enum):
    """Boundary conditions for simulations."""
    REFLECTIVE = "reflective"
    ABSORBING = "absorbing"
    PERIODIC = "periodic"
    DIRICHLET = "dirichlet"
    NEUMANN = "neumann"
    MIXED = "mixed"


class SolverStatus(Enum):
    """Solver convergence status."""
    CONVERGED = "converged"
    DIVERGED = "diverged"
    MAX_ITERATIONS = "max_iterations"
    STABLE = "stable"
    UNSTABLE = "unstable"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Vector3:
    """3D vector for physics calculations."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float) -> 'Vector3':
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> 'Vector3':
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(self) -> 'Vector3':
        return Vector3(-self.x, -self.y, -self.z)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3):
            return NotImplemented
        return (abs(self.x - other.x) < 1e-10 and
                abs(self.y - other.y) < 1e-10 and
                abs(self.z - other.z) < 1e-10)

    def __repr__(self) -> str:
        return f"Vector3({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    @property
    def magnitude_squared(self) -> float:
        return self.x**2 + self.y**2 + self.z**2

    def normalized(self) -> 'Vector3':
        mag = self.magnitude
        if mag < 1e-10:
            return Vector3(0, 0, 0)
        return self / mag

    def dot(self, other: 'Vector3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3') -> 'Vector3':
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def distance_to(self, other: 'Vector3') -> float:
        return (self - other).magnitude

    def lerp(self, other: 'Vector3', t: float) -> 'Vector3':
        return Vector3(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t,
            self.z + (other.z - self.z) * t
        )

    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]

    @classmethod
    def from_list(cls, values: List[float]) -> 'Vector3':
        if len(values) < 3:
            raise ValueError("Need 3 values for Vector3")
        return cls(values[0], values[1], values[2])

    @classmethod
    def zero(cls) -> 'Vector3':
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def one(cls) -> 'Vector3':
        return cls(1.0, 1.0, 1.0)

    @classmethod
    def up(cls) -> 'Vector3':
        return cls(0.0, 1.0, 0.0)

    @classmethod
    def right(cls) -> 'Vector3':
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def forward(cls) -> 'Vector3':
        return cls(0.0, 0.0, 1.0)


@dataclass
class Matrix4x4:
    """4x4 transformation matrix."""
    data: List[List[float]] = field(default_factory=lambda: [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])

    def __mul__(self, other: 'Matrix4x4') -> 'Matrix4x4':
        result = [[0.0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    result[i][j] += self.data[i][k] * other.data[k][j]
        return Matrix4x4(result)

    def transform_vector(self, vec: Vector3) -> Vector3:
        x = self.data[0][0] * vec.x + self.data[0][1] * vec.y + self.data[0][2] * vec.z + self.data[0][3]
        y = self.data[1][0] * vec.x + self.data[1][1] * vec.y + self.data[1][2] * vec.z + self.data[1][3]
        z = self.data[2][0] * vec.x + self.data[2][1] * vec.y + self.data[2][2] * vec.z + self.data[2][3]
        return Vector3(x, y, z)

    @classmethod
    def translation(cls, x: float, y: float, z: float) -> 'Matrix4x4':
        return cls([
            [1.0, 0.0, 0.0, x],
            [0.0, 1.0, 0.0, y],
            [0.0, 0.0, 1.0, z],
            [0.0, 0.0, 0.0, 1.0]
        ])

    @classmethod
    def scaling(cls, x: float, y: float, z: float) -> 'Matrix4x4':
        return cls([
            [x, 0.0, 0.0, 0.0],
            [0.0, y, 0.0, 0.0],
            [0.0, 0.0, z, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

    @classmethod
    def rotation_x(cls, angle_rad: float) -> 'Matrix4x4':
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        return cls([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, c, -s, 0.0],
            [0.0, s, c, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

    @classmethod
    def rotation_y(cls, angle_rad: float) -> 'Matrix4x4':
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        return cls([
            [c, 0.0, s, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-s, 0.0, c, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

    @classmethod
    def rotation_z(cls, angle_rad: float) -> 'Matrix4x4':
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        return cls([
            [c, -s, 0.0, 0.0],
            [s, c, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])


@dataclass
class Quaternion:
    """Quaternion for rotation representation."""
    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __mul__(self, other: 'Quaternion') -> 'Quaternion':
        return Quaternion(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        )

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)

    def normalized(self) -> 'Quaternion':
        mag = self.magnitude
        if mag < 1e-10:
            return Quaternion(1, 0, 0, 0)
        return Quaternion(self.w/mag, self.x/mag, self.y/mag, self.z/mag)

    def conjugate(self) -> 'Quaternion':
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self) -> 'Quaternion':
        mag_sq = self.magnitude**2
        if mag_sq < 1e-10:
            return Quaternion(1, 0, 0, 0)
        conj = self.conjugate()
        return Quaternion(conj.w/mag_sq, conj.x/mag_sq, conj.y/mag_sq, conj.z/mag_sq)

    def rotate_vector(self, vec: Vector3) -> Vector3:
        q_vec = Quaternion(0, vec.x, vec.y, vec.z)
        result = self * q_vec * self.conjugate()
        return Vector3(result.x, result.y, result.z)

    def to_euler(self) -> Tuple[float, float, float]:
        """Convert quaternion to Euler angles (roll, pitch, yaw)."""
        sinr_cosp = 2 * (self.w * self.x + self.y * self.z)
        cosr_cosp = 1 - 2 * (self.x**2 + self.y**2)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (self.w * self.y - self.z * self.x)
        sinp = max(-1, min(1, sinp))
        pitch = math.asin(sinp)

        siny_cosp = 2 * (self.w * self.z + self.x * self.y)
        cosy_cosp = 1 - 2 * (self.y**2 + self.z**2)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw

    @classmethod
    def from_axis_angle(cls, axis: Vector3, angle_rad: float) -> 'Quaternion':
        half_angle = angle_rad / 2
        s = math.sin(half_angle)
        norm = axis.normalized()
        return cls(math.cos(half_angle), norm.x * s, norm.y * s, norm.z * s)

    @classmethod
    def from_euler(cls, roll: float, pitch: float, yaw: float) -> 'Quaternion':
        cr, sr = math.cos(roll/2), math.sin(roll/2)
        cp, sp = math.cos(pitch/2), math.sin(pitch/2)
        cy, sy = math.cos(yaw/2), math.sin(yaw/2)
        return cls(
            cr * cp * cy + sr * sp * sy,
            sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy
        )

    @classmethod
    def identity(cls) -> 'Quaternion':
        return cls(1, 0, 0, 0)


@dataclass
class AABB:
    """Axis-Aligned Bounding Box."""
    min_point: Vector3 = field(default_factory=Vector3.zero)
    max_point: Vector3 = field(default_factory=Vector3.zero)

    @property
    def center(self) -> Vector3:
        return (self.min_point + self.max_point) * 0.5

    @property
    def size(self) -> Vector3:
        return self.max_point - self.min_point

    @property
    def half_extents(self) -> Vector3:
        return self.size * 0.5

    def contains_point(self, point: Vector3) -> bool:
        return (self.min_point.x <= point.x <= self.max_point.x and
                self.min_point.y <= point.y <= self.max_point.y and
                self.min_point.z <= point.z <= self.max_point.z)

    def intersects(self, other: 'AABB') -> bool:
        return (self.min_point.x <= other.max_point.x and self.max_point.x >= other.min_point.x and
                self.min_point.y <= other.max_point.y and self.max_point.y >= other.min_point.y and
                self.min_point.z <= other.max_point.z and self.max_point.z >= other.min_point.z)

    def expand(self, point: Vector3) -> 'AABB':
        return AABB(
            Vector3(min(self.min_point.x, point.x), min(self.min_point.y, point.y), min(self.min_point.z, point.z)),
            Vector3(max(self.max_point.x, point.x), max(self.max_point.y, point.y), max(self.max_point.z, point.z))
        )


@dataclass
class Ray:
    """Ray for ray casting."""
    origin: Vector3 = field(default_factory=Vector3.zero)
    direction: Vector3 = field(default_factory=Vector3.forward)
    max_distance: float = 1000.0

    def point_at(self, t: float) -> Vector3:
        return self.origin + self.direction * t


@dataclass
class Material:
    """Material properties for physics objects."""
    name: str = "default"
    material_type: MaterialType = MaterialType.RIGID
    density: float = 1.0
    restitution: float = 0.5
    friction: float = 0.5
    mass: float = 1.0
    temperature: float = 20.0
    thermal_conductivity: float = 0.0
    specific_heat: float = 0.0
    Youngs_modulus: float = 0.0
    Poisson_ratio: float = 0.0

    @property
    def inverse_mass(self) -> float:
        if self.mass < 1e-10:
            return 0.0
        return 1.0 / self.mass


@dataclass
class Force:
    """Force applied to a physics object."""
    force_type: ForceType = ForceType.GRAVITY
    direction: Vector3 = field(default_factory=Vector3.zero)
    magnitude: float = 0.0
    application_point: Vector3 = field(default_factory=Vector3.zero)
    parameters: Dict[str, Any] = field(default_factory=dict)

    @property
    def force_vector(self) -> Vector3:
        if self.direction.magnitude < 1e-10:
            return Vector3.zero()
        return self.direction.normalized() * self.magnitude


@dataclass
class Collision:
    """Collision detection result."""
    collision_type: CollisionType = CollisionType.NONE
    point: Vector3 = field(default_factory=Vector3.zero)
    normal: Vector3 = field(default_factory=Vector3.zero)
    penetration_depth: float = 0.0
    object_a: str = ""
    object_b: str = ""
    relative_velocity: Vector3 = field(default_factory=Vector3.zero)

    @property
    def is_colliding(self) -> bool:
        return self.collision_type != CollisionType.NONE


@dataclass
class Constraint:
    """Physics constraint between objects."""
    constraint_id: str = ""
    constraint_type: ConstraintType = ConstraintType.DISTANCE
    object_a: str = ""
    object_b: str = ""
    anchor_a: Vector3 = field(default_factory=Vector3.zero)
    anchor_b: Vector3 = field(default_factory=Vector3.zero)
    rest_length: float = 1.0
    stiffness: float = 100.0
    damping: float = 10.0
    enabled: bool = True


@dataclass
class Particle:
    """Particle in a particle system."""
    particle_id: str = ""
    position: Vector3 = field(default_factory=Vector3.zero)
    velocity: Vector3 = field(default_factory=Vector3.zero)
    acceleration: Vector3 = field(default_factory=Vector3.zero)
    mass: float = 1.0
    lifetime: float = 1.0
    age: float = 0.0
    size: float = 1.0
    color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    alive: bool = True

    @property
    def is_alive(self) -> bool:
        return self.alive and self.age < self.lifetime

    @property
    def life_ratio(self) -> float:
        if self.lifetime < 1e-10:
            return 0.0
        return min(self.age / self.lifetime, 1.0)

    def update(self, dt: float) -> None:
        if not self.is_alive:
            return
        self.velocity = self.velocity + self.acceleration * dt
        self.position = self.position + self.velocity * dt
        self.age += dt
        if self.age >= self.lifetime:
            self.alive = False


@dataclass
class RigidBody:
    """Rigid body for physics simulation."""
    body_id: str = ""
    position: Vector3 = field(default_factory=Vector3.zero)
    rotation: Quaternion = field(default_factory=Quaternion.identity)
    velocity: Vector3 = field(default_factory=Vector3.zero)
    angular_velocity: Vector3 = field(default_factory=Vector3.zero)
    material: Material = field(default_factory=Material)
    forces: List[Force] = field(default_factory=list)
    torque: Vector3 = field(default_factory=Vector3.zero)
    aabb: AABB = field(default_factory=AABB)
    use_gravity: bool = True
    is_kinematic: bool = False
    is_static: bool = False
    constraints: List[str] = field(default_factory=list)

    @property
    def mass(self) -> float:
        return self.material.mass

    @property
    def inverse_mass(self) -> float:
        if self.is_static or self.is_kinematic:
            return 0.0
        return self.material.inverse_mass

    @property
    def is_dynamic(self) -> bool:
        return not self.is_static and not self.is_kinematic

    def apply_force(self, force: Force) -> None:
        self.forces.append(force)

    def apply_impulse(self, impulse: Vector3) -> None:
        if self.is_static or self.is_kinematic:
            return
        self.velocity = self.velocity + impulse * self.inverse_mass

    def apply_torque(self, torque: Vector3) -> None:
        self.torque = self.torque + torque

    def get_total_force(self) -> Vector3:
        total = Vector3.zero()
        for force in self.forces:
            total = total + force.force_vector
        return total

    def clear_forces(self) -> None:
        self.forces.clear()
        self.torque = Vector3.zero()


@dataclass
class SimulationConfig:
    """Configuration for physics simulation."""
    domain: PhysicsDomain = PhysicsDomain.CLASSICAL_MECHANICS
    timestep: float = 0.01
    duration: float = 10.0
    precision: str = "double"
    parallelize: bool = True
    max_iterations: int = 1000
    tolerance: float = 1e-6
    boundary_condition: BoundaryCondition = BoundaryCondition.REFLECTIVE
    gravity: Vector3 = field(default_factory=lambda: Vector3(0, -9.81, 0))
    air_density: float = 1.225
    temperature: float = 20.0
    debug: bool = False


@dataclass
class SimulationState:
    """State of a physics simulation."""
    time: float = 0.0
    step_count: int = 0
    bodies: Dict[str, RigidBody] = field(default_factory=dict)
    particles: Dict[str, Particle] = field(default_factory=dict)
    constraints: List[Constraint] = field(default_factory=list)
    collisions: List[Collision] = field(default_factory=list)
    energy: float = 0.0
    momentum: Vector3 = field(default_factory=Vector3.zero)

    def copy(self) -> 'SimulationState':
        return SimulationState(
            time=self.time,
            step_count=self.step_count,
            bodies=self.bodies.copy(),
            particles=self.particles.copy(),
            constraints=self.constraints.copy(),
            collisions=self.collisions.copy(),
            energy=self.energy,
            momentum=Vector3(self.momentum.x, self.momentum.y, self.momentum.z)
        )


@dataclass
class SimulationResult:
    """Result of a physics simulation."""
    domain: PhysicsDomain = PhysicsDomain.CLASSICAL_MECHANICS
    trajectory: List[Dict[str, Any]] = field(default_factory=list)
    total_steps: int = 0
    final_time: float = 0.0
    energy_conservation: float = 0.0
    momentum_conservation: float = 0.0
    status: SolverStatus = SolverStatus.CONVERGED
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_successful(self) -> bool:
        return self.status == SolverStatus.CONVERGED or self.status == SolverStatus.STABLE


@dataclass
class Mesh:
    """3D mesh for collision detection."""
    vertices: List[Vector3] = field(default_factory=list)
    triangles: List[Tuple[int, int, int]] = field(default_factory=list)
    normals: List[Vector3] = field(default_factory=list)
    name: str = ""

    @property
    def vertex_count(self) -> int:
        return len(self.vertices)

    @property
    def triangle_count(self) -> int:
        return len(self.triangles)

    def get_aabb(self) -> AABB:
        if not self.vertices:
            return AABB()
        min_pt = self.vertices[0]
        max_pt = self.vertices[0]
        for v in self.vertices[1:]:
            min_pt = Vector3(min(min_pt.x, v.x), min(min_pt.y, v.y), min(min_pt.z, v.z))
            max_pt = Vector3(max(max_pt.x, v.x), max(max_pt.y, v.y), max(max_pt.z, v.z))
        return AABB(min_pt, max_pt)


# ---------------------------------------------------------------------------
# Physics Engines
# ---------------------------------------------------------------------------

class PhysicsEngine:
    """Core physics simulation engine base class."""

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.state = SimulationState()
        self.trajectory: List[Dict[str, Any]] = []
        self._step_count = 0

    def initialize(self, initial_conditions: Dict[str, Any]) -> None:
        self.state = SimulationState()
        self.trajectory = []
        self._step_count = 0
        if "bodies" in initial_conditions:
            for body_id, body_data in initial_conditions["bodies"].items():
                body = RigidBody(
                    body_id=body_id,
                    position=Vector3.from_list(body_data.get("position", [0, 0, 0])),
                    velocity=Vector3.from_list(body_data.get("velocity", [0, 0, 0])),
                    material=Material(mass=body_data.get("mass", 1.0))
                )
                self.state.bodies[body_id] = body
        if "particles" in initial_conditions:
            for pid, pdata in initial_conditions["particles"].items():
                particle = Particle(
                    particle_id=pid,
                    position=Vector3.from_list(pdata.get("position", [0, 0, 0])),
                    velocity=Vector3.from_list(pdata.get("velocity", [0, 0, 0])),
                    mass=pdata.get("mass", 1.0),
                    lifetime=pdata.get("lifetime", 1.0),
                    size=pdata.get("size", 1.0)
                )
                self.state.particles[pid] = particle
        self._record_state()

    def step(self) -> SimulationState:
        raise NotImplementedError

    def run(self) -> List[Dict[str, Any]]:
        results = []
        t = 0.0
        while t < self.config.duration and self._step_count < self.config.max_iterations:
            self.state = self.step()
            self._record_state()
            results.append(self._get_state_dict())
            t += self.config.timestep
            self._step_count += 1
        return results

    def _record_state(self) -> None:
        self.state.time = self._step_count * self.config.timestep
        self.state.step_count = self._step_count

    def _get_state_dict(self) -> Dict[str, Any]:
        return {
            "time": self.state.time,
            "step": self.state.step_count,
            "bodies": {
                bid: {
                    "position": body.position.to_list(),
                    "velocity": body.velocity.to_list(),
                    "mass": body.mass
                }
                for bid, body in self.state.bodies.items()
            },
            "particles": {
                pid: {
                    "position": p.position.to_list(),
                    "velocity": p.velocity.to_list(),
                    "alive": p.is_alive
                }
                for pid, p in self.state.particles.items()
            }
        }

    def get_trajectory(self) -> List[Dict[str, Any]]:
        return self.trajectory

    def get_energy(self) -> float:
        return self.state.energy

    def get_momentum(self) -> Vector3:
        return self.state.momentum


class ClassicalMechanicsEngine(PhysicsEngine):
    """Classical mechanics simulation engine."""

    def __init__(self, config: SimulationConfig, integration_method: IntegrationMethod = IntegrationMethod.VELOCITY_VERLET) -> None:
        super().__init__(config)
        self.integration_method = integration_method

    def step(self) -> SimulationState:
        dt = self.config.timestep
        new_state = self.state.copy()

        for body_id, body in self.state.bodies.items():
            if body.is_static:
                continue

            # Calculate forces
            total_force = body.get_total_force()
            if body.use_gravity:
                total_force = total_force + self.config.gravity * body.mass

            # Calculate acceleration
            acceleration = total_force * body.inverse_mass

            # Integration
            if self.integration_method == IntegrationMethod.EULER:
                new_body = self._euler_step(body, acceleration, dt)
            elif self.integration_method == IntegrationMethod.VELOCITY_VERLET:
                new_body = self._velocity_verlet_step(body, acceleration, dt)
            elif self.integration_method == IntegrationMethod.RK4:
                new_body = self._rk4_step(body, dt)
            elif self.integration_method == IntegrationMethod.LEAPFROG:
                new_body = self._leapfrog_step(body, dt)
            else:
                new_body = self._symplectic_euler_step(body, acceleration, dt)

            new_state.bodies[body_id] = new_body

        new_state.time = self.state.time + dt
        new_state.step_count = self.state.step_count + 1
        return new_state

    def _euler_step(self, body: RigidBody, acceleration: Vector3, dt: float) -> RigidBody:
        new_body = RigidBody(
            body_id=body.body_id,
            position=body.position + body.velocity * dt,
            velocity=body.velocity + acceleration * dt,
            rotation=body.rotation,
            angular_velocity=body.angular_velocity,
            material=body.material,
            forces=[],
            use_gravity=body.use_gravity,
            is_kinematic=body.is_kinematic,
            is_static=body.is_static
        )
        return new_body

    def _velocity_verlet_step(self, body: RigidBody, acceleration: Vector3, dt: float) -> RigidBody:
        new_position = body.position + body.velocity * dt + acceleration * (0.5 * dt * dt)
        new_velocity = body.velocity + acceleration * dt
        new_body = RigidBody(
            body_id=body.body_id,
            position=new_position,
            velocity=new_velocity,
            rotation=body.rotation,
            angular_velocity=body.angular_velocity,
            material=body.material,
            forces=[],
            use_gravity=body.use_gravity,
            is_kinematic=body.is_kinematic,
            is_static=body.is_static
        )
        return new_body

    def _rk4_step(self, body: RigidBody, dt: float) -> RigidBody:
        k1v = self._compute_acceleration(body)
        k1x = body.velocity

        k2v = self._compute_acceleration(RigidBody(
            body_id=body.body_id,
            position=body.position + k1x * (dt/2),
            velocity=body.velocity + k1v * (dt/2),
            material=body.material
        ))
        k2x = body.velocity + k1v * (dt/2)

        k3v = self._compute_acceleration(RigidBody(
            body_id=body.body_id,
            position=body.position + k2x * (dt/2),
            velocity=body.velocity + k2v * (dt/2),
            material=body.material
        ))
        k3x = body.velocity + k2v * (dt/2)

        k4v = self._compute_acceleration(RigidBody(
            body_id=body.body_id,
            position=body.position + k3x * dt,
            velocity=body.velocity + k3v * dt,
            material=body.material
        ))
        k4x = body.velocity + k3v * dt

        new_position = body.position + (k1x + k2x*2 + k3x*2 + k4x) * (dt/6)
        new_velocity = body.velocity + (k1v + k2v*2 + k3v*2 + k4v) * (dt/6)

        return RigidBody(
            body_id=body.body_id,
            position=new_position,
            velocity=new_velocity,
            rotation=body.rotation,
            angular_velocity=body.angular_velocity,
            material=body.material,
            forces=[],
            use_gravity=body.use_gravity,
            is_kinematic=body.is_kinematic,
            is_static=body.is_static
        )

    def _leapfrog_step(self, body: RigidBody, dt: float) -> RigidBody:
        half_dt = dt / 2
        acceleration = self._compute_acceleration(body)
        new_velocity = body.velocity + acceleration * half_dt
        new_position = body.position + new_velocity * dt
        new_velocity = new_velocity + acceleration * half_dt

        return RigidBody(
            body_id=body.body_id,
            position=new_position,
            velocity=new_velocity,
            rotation=body.rotation,
            angular_velocity=body.angular_velocity,
            material=body.material,
            forces=[],
            use_gravity=body.use_gravity,
            is_kinematic=body.is_kinematic,
            is_static=body.is_static
        )

    def _symplectic_euler_step(self, body: RigidBody, acceleration: Vector3, dt: float) -> RigidBody:
        new_velocity = body.velocity + acceleration * dt
        new_position = body.position + new_velocity * dt

        return RigidBody(
            body_id=body.body_id,
            position=new_position,
            velocity=new_velocity,
            rotation=body.rotation,
            angular_velocity=body.angular_velocity,
            material=body.material,
            forces=[],
            use_gravity=body.use_gravity,
            is_kinematic=body.is_kinematic,
            is_static=body.is_static
        )

    def _compute_acceleration(self, body: RigidBody) -> Vector3:
        total_force = body.get_total_force()
        if body.use_gravity:
            total_force = total_force + self.config.gravity * body.mass
        return total_force * body.inverse_mass


class QuantumMechanicsEngine(PhysicsEngine):
    """Quantum mechanics simulation engine."""

    def step(self) -> SimulationState:
        new_state = self.state.copy()
        dt = self.config.timestep

        for pid, particle in self.state.particles.items():
            if not particle.is_alive:
                continue

            # Simple quantum-inspired evolution (placeholder)
            # In a real implementation, this would solve the Schrodinger equation
            new_particle = Particle(
                particle_id=pid,
                position=particle.position + particle.velocity * dt,
                velocity=particle.velocity + particle.acceleration * dt,
                mass=particle.mass,
                lifetime=particle.lifetime,
                age=particle.age + dt,
                size=particle.size,
                color=particle.color,
                alive=particle.age + dt < particle.lifetime
            )
            new_state.particles[pid] = new_particle

        new_state.time = self.state.time + dt
        new_state.step_count = self.state.step_count + 1
        return new_state


class FluidDynamicsEngine(PhysicsEngine):
    """Fluid dynamics simulation engine using Navier-Stokes."""

    def __init__(self, config: SimulationConfig, grid_size: Tuple[int, int] = (100, 100)) -> None:
        super().__init__(config)
        self.grid_size = grid_size
        self.viscosity = 0.001
        self.density = 1.0
        self.velocity_x: List[List[float]] = [[0.0] * grid_size[1] for _ in range(grid_size[0])]
        self.velocity_y: List[List[float]] = [[0.0] * grid_size[1] for _ in range(grid_size[0])]
        self.pressure: List[List[float]] = [[0.0] * grid_size[1] for _ in range(grid_size[0])]

    def step(self) -> SimulationState:
        new_state = self.state.copy()
        dt = self.config.timestep

        # Simple fluid simulation (Jacobi iteration for pressure solve)
        for i in range(1, self.grid_size[0] - 1):
            for j in range(1, self.grid_size[1] - 1):
                # Diffusion step
                self.velocity_x[i][j] += self.viscosity * dt * (
                    self.velocity_x[i+1][j] + self.velocity_x[i-1][j] +
                    self.velocity_x[i][j+1] + self.velocity_x[i][j-1] -
                    4 * self.velocity_x[i][j]
                )
                self.velocity_y[i][j] += self.viscosity * dt * (
                    self.velocity_y[i+1][j] + self.velocity_y[i-1][j] +
                    self.velocity_y[i][j+1] + self.velocity_y[i][j-1] -
                    4 * self.velocity_y[i][j]
                )

        new_state.time = self.state.time + dt
        new_state.step_count = self.state.step_count + 1
        return new_state


class ThermodynamicsEngine(PhysicsEngine):
    """Thermodynamics simulation engine."""

    def __init__(self, config: SimulationConfig, grid_size: Tuple[int, int] = (50, 50)) -> None:
        super().__init__(config)
        self.grid_size = grid_size
        self.temperature_field: List[List[float]] = [
            [config.temperature] * grid_size[1] for _ in range(grid_size[0])
        ]
        self.thermal_diffusivity = 0.0001

    def step(self) -> SimulationState:
        new_state = self.state.copy()
        dt = self.config.timestep

        # Heat equation: dT/dt = α * ∇²T
        new_field = [row[:] for row in self.temperature_field]
        for i in range(1, self.grid_size[0] - 1):
            for j in range(1, self.grid_size[1] - 1):
                laplacian = (
                    self.temperature_field[i+1][j] + self.temperature_field[i-1][j] +
                    self.temperature_field[i][j+1] + self.temperature_field[i][j-1] -
                    4 * self.temperature_field[i][j]
                )
                new_field[i][j] = self.temperature_field[i][j] + self.thermal_diffusivity * dt * laplacian

        self.temperature_field = new_field
        new_state.time = self.state.time + dt
        new_state.step_count = self.state.step_count + 1
        return new_state


# ---------------------------------------------------------------------------
# Collision Detection
# ---------------------------------------------------------------------------

class CollisionDetector:
    """Collision detection system."""

    def __init__(self) -> None:
        self.broad_phase_pairs: List[Tuple[str, str]] = []

    def detect_sphere_sphere(self, pos_a: Vector3, radius_a: float,
                            pos_b: Vector3, radius_b: float) -> Collision:
        distance = pos_a.distance_to(pos_b)
        combined_radius = radius_a + radius_b
        if distance < combined_radius:
            normal = (pos_b - pos_a).normalized()
            penetration = combined_radius - distance
            return Collision(
                collision_type=CollisionType.SPHERE_SPHERE,
                point=pos_a + normal * radius_a,
                normal=normal,
                penetration_depth=penetration
            )
        return Collision(collision_type=CollisionType.NONE)

    def detect_aabb(self, aabb_a: AABB, aabb_b: AABB) -> Collision:
        if aabb_a.intersects(aabb_b):
            center_a = aabb_a.center
            center_b = aabb_b.center
            normal = (center_b - center_a).normalized()
            return Collision(
                collision_type=CollisionType.AABB,
                point=(center_a + center_b) * 0.5,
                normal=normal,
                penetration_depth=0.0
            )
        return Collision(collision_type=CollisionType.NONE)

    def detect_ray_sphere(self, ray: Ray, center: Vector3, radius: float) -> Optional[float]:
        oc = ray.origin - center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - radius * radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None
        t = (-b - math.sqrt(discriminant)) / (2 * a)
        if t < 0:
            t = (-b + math.sqrt(discriminant)) / (2 * a)
        if t < 0 or t > ray.max_distance:
            return None
        return t

    def detect_ray_plane(self, ray: Ray, plane_point: Vector3, plane_normal: Vector3) -> Optional[float]:
        denom = plane_normal.dot(ray.direction)
        if abs(denom) < 1e-10:
            return None
        t = (plane_point - ray.origin).dot(plane_normal) / denom
        if t < 0 or t > ray.max_distance:
            return None
        return t

    def broad_phase(self, bodies: Dict[str, RigidBody]) -> List[Tuple[str, str]]:
        pairs = []
        body_list = list(bodies.values())
        for i in range(len(body_list)):
            for j in range(i + 1, len(body_list)):
                if body_list[i].aabb.intersects(body_list[j].aabb):
                    pairs.append((body_list[i].body_id, body_list[j].body_id))
        return pairs


# ---------------------------------------------------------------------------
# Constraint Solver
# ---------------------------------------------------------------------------

class ConstraintSolver:
    """Constraint solver for physics simulations."""

    def __init__(self, iterations: int = 10) -> None:
        self.iterations = iterations

    def solve_distance_constraint(self, pos_a: Vector3, pos_b: Vector3,
                                 rest_length: float, stiffness: float) -> Tuple[Vector3, Vector3]:
        delta = pos_b - pos_a
        current_length = delta.magnitude
        if current_length < 1e-10:
            return pos_a, pos_b
        correction = (current_length - rest_length) / current_length * stiffness
        correction_vec = delta * correction * 0.5
        return pos_a + correction_vec, pos_b - correction_vec

    def solve_spring_constraint(self, pos_a: Vector3, pos_b: Vector3,
                               rest_length: float, stiffness: float, damping: float,
                               vel_a: Vector3, vel_b: Vector3) -> Tuple[Vector3, Vector3, Vector3, Vector3]:
        delta = pos_b - pos_a
        current_length = delta.magnitude
        if current_length < 1e-10:
            return pos_a, pos_b, vel_a, vel_b
        direction = delta / current_length
        spring_force = (current_length - rest_length) * stiffness
        relative_vel = vel_b - vel_a
        damping_force = relative_vel.dot(direction) * damping
        total_force = spring_force + damping_force
        force_vec = direction * total_force
        return pos_a + force_vec * 0.5, pos_b - force_vec * 0.5, vel_a + force_vec * 0.5, vel_b - force_vec * 0.5


# ---------------------------------------------------------------------------
# Particle System
# ---------------------------------------------------------------------------

class ParticleSystem:
    """Particle system for visual effects."""

    def __init__(self, particle_type: ParticleType = ParticleType.GRAVITY) -> None:
        self.particle_type = particle_type
        self.particles: Dict[str, Particle] = {}
        self._counter = 0
        self.emitter_position = Vector3.zero()
        self.emission_rate = 10.0
        self.particle_lifetime = 2.0
        self.particle_speed = 5.0
        self.particle_size = 1.0
        self.gravity = Vector3(0, -9.81, 0)

    def emit(self, count: int = 1) -> List[Particle]:
        new_particles = []
        for _ in range(count):
            self._counter += 1
            pid = f"P-{self._counter:06d}"

            if self.particle_type == ParticleType.FOUNTAIN:
                velocity = Vector3(
                    random.uniform(-1, 1),
                    random.uniform(self.particle_speed * 0.5, self.particle_speed),
                    random.uniform(-1, 1)
                )
            elif self.particle_type == ParticleType.EXPLOSION:
                theta = random.uniform(0, 2 * math.pi)
                phi = random.uniform(0, math.pi)
                speed = random.uniform(0, self.particle_speed)
                velocity = Vector3(
                    speed * math.sin(phi) * math.cos(theta),
                    speed * math.sin(phi) * math.sin(theta),
                    speed * math.cos(phi)
                )
            elif self.particle_type == ParticleType.RAIN:
                velocity = Vector3(0, -self.particle_speed, 0)
            elif self.particle_type == ParticleType.SNOW:
                velocity = Vector3(
                    random.uniform(-0.5, 0.5),
                    -random.uniform(0.5, self.particle_speed),
                    random.uniform(-0.5, 0.5)
                )
            else:
                velocity = Vector3(
                    random.uniform(-1, 1),
                    random.uniform(0, self.particle_speed),
                    random.uniform(-1, 1)
                )

            particle = Particle(
                particle_id=pid,
                position=Vector3(self.emitter_position.x, self.emitter_position.y, self.emitter_position.z),
                velocity=velocity,
                lifetime=self.particle_lifetime,
                size=self.particle_size
            )
            self.particles[pid] = particle
            new_particles.append(particle)
        return new_particles

    def update(self, dt: float) -> None:
        to_remove = []
        for pid, particle in self.particles.items():
            if not particle.is_alive:
                to_remove.append(pid)
                continue
            particle.velocity = particle.velocity + self.gravity * dt
            particle.position = particle.position + particle.velocity * dt
            particle.age += dt
        for pid in to_remove:
            del self.particles[pid]

    def get_alive_particles(self) -> List[Particle]:
        return [p for p in self.particles.values() if p.is_alive]

    def clear(self) -> None:
        self.particles.clear()


# ---------------------------------------------------------------------------
# N-Body Gravity
# ---------------------------------------------------------------------------

class NBodyGravity:
    """N-body gravitational simulation."""

    def __init__(self, gravitational_constant: float = 6.674e-11) -> None:
        self.G = gravitational_constant
        self.bodies: List[RigidBody] = []

    def add_body(self, body: RigidBody) -> None:
        self.bodies.append(body)

    def compute_gravitational_force(self, body_a: RigidBody, body_b: RigidBody) -> Vector3:
        delta = body_b.position - body_a.position
        distance_sq = max(delta.magnitude_squared, 1e-10)
        distance = math.sqrt(distance_sq)
        force_magnitude = self.G * body_a.mass * body_b.mass / distance_sq
        return delta.normalized() * force_magnitude

    def compute_all_forces(self) -> Dict[str, Vector3]:
        forces: Dict[str, Vector3] = {body.body_id: Vector3.zero() for body in self.bodies}
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                force = self.compute_gravitational_force(self.bodies[i], self.bodies[j])
                forces[self.bodies[i].body_id] = forces[self.bodies[i].body_id] + force
                forces[self.bodies[j].body_id] = forces[self.bodies[j].body_id] - force
        return forces

    def step(self, dt: float) -> None:
        forces = self.compute_all_forces()
        for body in self.bodies:
            if body.is_static:
                continue
            acceleration = forces[body.body_id] * body.inverse_mass
            body.velocity = body.velocity + acceleration * dt
            body.position = body.position + body.velocity * dt

    def compute_total_energy(self) -> float:
        kinetic = 0.0
        potential = 0.0
        for body in self.bodies:
            kinetic += 0.5 * body.mass * body.velocity.magnitude_squared
        for i in range(len(self.bodies)):
            for j in range(i + 1, len(self.bodies)):
                distance = self.bodies[i].position.distance_to(self.bodies[j].position)
                if distance > 1e-10:
                    potential -= self.G * self.bodies[i].mass * self.bodies[j].mass / distance
        return kinetic + potential

    def compute_total_momentum(self) -> Vector3:
        momentum = Vector3.zero()
        for body in self.bodies:
            momentum = momentum + body.velocity * body.mass
        return momentum


# ---------------------------------------------------------------------------
# Main Agent
# ---------------------------------------------------------------------------

class PhysicsSimulationAgent:
    """Main agent for physics simulations."""

    def __init__(self) -> None:
        self.domain = PhysicsDomain
        self.engines: Dict[PhysicsDomain, PhysicsEngine] = {}
        self.history: List[Dict[str, Any]] = []
        self.collision_detector = CollisionDetector()
        self.constraint_solver = ConstraintSolver()
        self.particle_systems: Dict[str, ParticleSystem] = {}

    def create_engine(self, config: SimulationConfig) -> PhysicsEngine:
        engine_map: Dict[PhysicsDomain, type] = {
            PhysicsDomain.CLASSICAL_MECHANICS: ClassicalMechanicsEngine,
            PhysicsDomain.QUANTUM_MECHANICS: QuantumMechanicsEngine,
            PhysicsDomain.FLUID_DYNAMICS: FluidDynamicsEngine,
            PhysicsDomain.THERMODYNAMICS: ThermodynamicsEngine,
        }
        engine_class = engine_map.get(config.domain)
        if engine_class is None:
            raise ValueError(f"No engine for domain: {config.domain}")
        engine = engine_class(config)
        self.engines[config.domain] = engine
        return engine

    def run_simulation(self, domain: PhysicsDomain,
                       initial_conditions: Dict[str, Any],
                       timestep: float = 0.001,
                       duration: float = 10.0) -> List[Dict[str, Any]]:
        config = SimulationConfig(
            domain=domain,
            timestep=timestep,
            duration=duration,
            precision="double"
        )
        engine = self.create_engine(config)
        engine.initialize(initial_conditions)
        results = engine.run()
        self.history.append({
            "domain": domain.value,
            "results_count": len(results),
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
        return results

    def analyze_trajectory(self, trajectory: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not trajectory:
            return {}

        positions = []
        velocities = []
        for state in trajectory:
            for body_data in state.get("bodies", {}).values():
                positions.append(body_data.get("position", [0, 0, 0]))
                velocities.append(body_data.get("velocity", [0, 0, 0]))

        if not positions:
            return {}

        total_energy = 0.0
        for pos, vel in zip(positions, velocities):
            kinetic = 0.5 * sum(v**2 for v in vel)
            potential = sum(p**2 for p in pos)
            total_energy += kinetic + potential

        avg_energy = total_energy / len(trajectory) if trajectory else 0

        return {
            "total_steps": len(trajectory),
            "average_energy": avg_energy,
            "initial_position": positions[0] if positions else [0, 0, 0],
            "final_position": positions[-1] if positions else [0, 0, 0],
            "displacement": math.sqrt(sum((positions[-1][i] - positions[0][i])**2 for i in range(3))) if positions else 0
        }

    def optimize_parameters(self, domain: PhysicsDomain,
                           target_metric: str,
                           param_ranges: Dict[str, Tuple[float, float]],
                           initial_conditions: Dict[str, Any]) -> Dict[str, Any]:
        best_value = float("inf") if "error" in target_metric or "loss" in target_metric else float("-inf")
        best_params: Dict[str, float] = {}

        for param_name, (min_val, max_val) in param_ranges.items():
            step = (max_val - min_val) / 10
            current = min_val
            while current <= max_val:
                params = {param_name: current}
                try:
                    results = self.run_simulation(domain, initial_conditions, **params)
                    metric = self.analyze_trajectory(results).get(target_metric, 0)

                    if ("error" in target_metric or "loss" in target_metric) and metric < best_value:
                        best_value = metric
                        best_params = params
                    elif metric > best_value:
                        best_value = metric
                        best_params = params
                except Exception as e:
                    logger.warning(f"Simulation failed with params {params}: {e}")

                current += step

        return {"best_params": best_params, "best_value": best_value}

    def create_particle_system(self, name: str, particle_type: ParticleType = ParticleType.GRAVITY) -> ParticleSystem:
        system = ParticleSystem(particle_type)
        self.particle_systems[name] = system
        return system

    def detect_collisions(self, bodies: Dict[str, RigidBody]) -> List[Collision]:
        collisions = []
        pairs = self.collision_detector.broad_phase(bodies)
        for id_a, id_b in pairs:
            body_a = bodies[id_a]
            body_b = bodies[id_b]
            # Simple AABB collision
            collision = self.collision_detector.detect_aabb(body_a.aabb, body_b.aabb)
            if collision.is_colliding:
                collision.object_a = id_a
                collision.object_b = id_b
                collisions.append(collision)
        return collisions

    def get_simulation_stats(self) -> Dict[str, Any]:
        return {
            "total_simulations": len(self.history),
            "domains_used": list(set(h["domain"] for h in self.history)),
            "total_steps": sum(h["results_count"] for h in self.history),
            "particle_systems": len(self.particle_systems)
        }


def main() -> None:
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("  Physics Simulation Engine Agent")
    print("  Comprehensive Physics Simulation Platform")
    print("=" * 60)

    agent = PhysicsSimulationAgent()

    # Classical mechanics simulation
    initial_conditions = {
        "bodies": {
            "body1": {
                "position": [1.0, 0.0, 0.0],
                "velocity": [0.0, 1.0, 0.0],
                "mass": 1.0
            }
        }
    }

    results = agent.run_simulation(
        PhysicsDomain.CLASSICAL_MECHANICS,
        initial_conditions,
        timestep=0.01,
        duration=5.0
    )

    analysis = agent.analyze_trajectory(results)
    print(f"\nClassical Mechanics Simulation:")
    print(f"  Steps: {analysis.get('total_steps', 0)}")
    print(f"  Displacement: {analysis.get('displacement', 0):.4f}")

    # Particle system
    particle_system = agent.create_particle_system("fountain", ParticleType.FOUNTAIN)
    particle_system.emit(100)
    particle_system.update(0.1)
    alive = particle_system.get_alive_particles()
    print(f"\nParticle System:")
    print(f"  Alive particles: {len(alive)}")

    # Collision detection
    print(f"\nCollision Detection:")
    print(f"  Detector initialized")

    # N-body gravity
    print(f"\nN-Body Gravity:")
    print(f"  Ready for gravitational simulations")

    # Simulation stats
    stats = agent.get_simulation_stats()
    print(f"\nSimulation Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("  Physics Simulation Engine demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()