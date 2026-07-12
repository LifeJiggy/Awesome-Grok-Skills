"""
swarm_robotics.py — Algorithms and infrastructure for multi-robot swarm coordination.

Provides flocking, consensus, stigmergic coordination, task allocation, collision
avoidance, formation control, and swarm intelligence optimization.
"""

from __future__ import annotations

import enum
import logging
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SwarmState(enum.Enum):
    """State of a swarm agent."""
    IDLE = "idle"
    MOVING = "moving"
    TASK_EXECUTING = "task_executing"
    COMMUNICATING = "communicating"
    FAILED = "failed"
    RECOVERING = "recovering"


class FormationPattern(enum.Enum):
    """Geometric formation patterns."""
    LINE = "line"
    CIRCLE = "circle"
    V_SHAPE = "v_shape"
    GRID = "grid"
    DIAMOND = "diamond"


class PheromoneType(enum.Enum):
    """Types of digital pheromones."""
    TRAIL = "trail"
    FOOD = "food"
    NEST = "nest"
    DANGER = "danger"
    CUSTOM = "custom"


class RobotCapability(enum.Enum):
    """Capabilities a robot can possess."""
    SENSOR = "sensor"
    TRANSPORT = "transport"
    MANIPULATION = "manipulation"
    COMMS_RELAY = "comms_relay"
    GENERIC = "generic"


class ConsensusType(enum.Enum):
    """Types of consensus protocols."""
    AVERAGE = "average"
    LEADER_ELECTION = "leader_election"
    AGREEMENT = "agreement"
    RENDEZVOUS = "rendezvous"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Vector2:
    """2D vector for positions and velocities."""
    x: float = 0.0
    y: float = 0.0

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self) -> Vector2:
        m = self.magnitude()
        if m < 1e-10:
            return Vector2(0, 0)
        return Vector2(self.x / m, self.y / m)

    def distance_to(self, other: Vector2) -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector2:
        return Vector2(self.x * scalar, self.y * scalar)


@dataclass
class Agent:
    """A single swarm agent."""
    agent_id: int = 0
    position: tuple[float, float] = (0.0, 0.0)
    velocity: tuple[float, float] = (0.0, 0.0)
    heading: float = 0.0
    state: SwarmState = SwarmState.IDLE
    capabilities: list[RobotCapability] = field(default_factory=list)
    battery_percent: float = 100.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def pos(self) -> Vector2:
        return Vector2(self.position[0], self.position[1])

    @property
    def vel(self) -> Vector2:
        return Vector2(self.velocity[0], self.velocity[1])


@dataclass
class AgentState:
    """State of an agent in a consensus protocol."""
    agent_id: int = 0
    value: float = 0.0
    converged: bool = False


@dataclass
class FlockingConfig:
    """Configuration for flocking simulation."""
    separation_weight: float = 1.5
    alignment_weight: float = 1.0
    cohesion_weight: float = 1.0
    perception_radius: float = 5.0
    max_speed: float = 2.0
    separation_distance: float = 1.0
    bounds: tuple[float, float, float, float] = (-20.0, -20.0, 20.0, 20.0)


@dataclass
class Task:
    """A task to be allocated to swarm agents."""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    required_capability: RobotCapability = RobotCapability.GENERIC
    priority: float = 1.0
    position: tuple[float, float] = (0.0, 0.0)
    status: str = "pending"
    assigned_to: int = -1


@dataclass
class SwarmMetrics:
    """Aggregate metrics for a swarm."""
    num_agents: int = 0
    center: tuple[float, float] = (0.0, 0.0)
    cohesion: float = 0.0
    average_speed: float = 0.0
    spread: float = 0.0
    task_completion_rate: float = 0.0
    communication_load: int = 0


# ---------------------------------------------------------------------------
# Flocking (Boids)
# ---------------------------------------------------------------------------

class FlockingEngine:
    """Reynolds-style flocking with separation, alignment, and cohesion."""

    def __init__(self, config: FlockingConfig):
        self.config = config

    def compute_forces(self, agent: Agent, neighbors: list[Agent]) -> tuple[float, float]:
        """Compute the flocking force vector for an agent given its neighbors."""
        sep = self._separation(agent, neighbors)
        ali = self._alignment(agent, neighbors)
        coh = self._cohesion(agent, neighbors)

        fx = (sep.x * self.config.separation_weight +
              ali.x * self.config.alignment_weight +
              coh.x * self.config.cohesion_weight)
        fy = (sep.y * self.config.separation_weight +
              ali.y * self.config.alignment_weight +
              coh.y * self.config.cohesion_weight)
        return (fx, fy)

    def _separation(self, agent: Agent, neighbors: list[Agent]) -> Vector2:
        steer = Vector2(0, 0)
        count = 0
        for n in neighbors:
            d = agent.pos.distance_to(n.pos)
            if 0 < d < self.config.separation_distance:
                diff = agent.pos - n.pos
                steer = steer + diff.normalize().multiply(1.0 / max(d, 0.01))
                count += 1
        if count > 0:
            steer = steer * (1.0 / count)
        return steer

    def _alignment(self, agent: Agent, neighbors: list[Agent]) -> Vector2:
        avg = Vector2(0, 0)
        count = 0
        for n in neighbors:
            d = agent.pos.distance_to(n.pos)
            if 0 < d < self.config.perception_radius:
                avg = avg + n.vel
                count += 1
        if count > 0:
            avg = avg * (1.0 / count)
            return avg.normalize()
        return Vector2(0, 0)

    def _cohesion(self, agent: Agent, neighbors: list[Agent]) -> Vector2:
        center = Vector2(0, 0)
        count = 0
        for n in neighbors:
            d = agent.pos.distance_to(n.pos)
            if 0 < d < self.config.perception_radius:
                center = center + n.pos
                count += 1
        if count > 0:
            center = center * (1.0 / count)
            desired = center - agent.pos
            return desired.normalize()
        return Vector2(0, 0)


# ---------------------------------------------------------------------------
# Consensus Protocol
# ---------------------------------------------------------------------------

class ConsensusProtocol:
    """Distributed consensus for leader election and average consensus."""

    def __init__(self, protocol_type: str = "average"):
        self.protocol_type = ConsensusType(protocol_type)
        self._convergence_threshold = 1e-4

    def step(self, agents: list[AgentState], neighbors_fn: Any = None) -> list[AgentState]:
        """Execute one round of the consensus protocol."""
        if self.protocol_type == ConsensusType.AVERAGE:
            return self._average_step(agents, neighbors_fn)
        elif self.protocol_type == ConsensusType.LEADER_ELECTION:
            return self._leader_election_step(agents, neighbors_fn)
        return agents

    def _average_step(self, agents: list[AgentState], neighbors_fn: Any) -> list[AgentState]:
        new_agents = []
        for agent in agents:
            neighbors = neighbors_fn(agent.agent_id) if neighbors_fn else []
            values = [a.value for a in agents if a.agent_id in neighbors or a.agent_id == agent.agent_id]
            avg = sum(values) / len(values) if values else agent.value
            new_agents.append(AgentState(agent_id=agent.agent_id, value=avg))
        return new_agents

    def _leader_election_step(self, agents: list[AgentState], neighbors_fn: Any) -> list[AgentState]:
        new_agents = []
        for agent in agents:
            neighbors = neighbors_fn(agent.agent_id) if neighbors_fn else []
            neighbor_values = {a.agent_id: a.value for a in agents if a.agent_id in neighbors}
            max_val = max(neighbor_values.values()) if neighbor_values else agent.value
            new_val = max(agent.value, max_val * 0.99)
            new_agents.append(AgentState(agent_id=agent.agent_id, value=new_val))
        return new_agents

    def has_converged(self, agents: list[AgentState]) -> bool:
        if len(agents) < 2:
            return True
        values = [a.value for a in agents]
        return max(values) - min(values) < self._convergence_threshold

    def random_neighbors(self, agent_id: int) -> list[int]:
        """Default neighbor function: random subset."""
        all_ids = list(range(50))
        return random.sample(all_ids, min(5, len(all_ids)))


# ---------------------------------------------------------------------------
# Task Allocation
# ---------------------------------------------------------------------------

class TaskAllocator:
    """Distribute tasks among robots using auction or threshold-based methods."""

    def __init__(self, allocation_type: str = "auction"):
        self.allocation_type = allocation_type

    def allocate(self, tasks: list[Task], robot_positions: dict[int, tuple[float, float]],
                 robot_capabilities: dict[int, RobotCapability] | None = None) -> dict[int, list[Task]]:
        """Allocate tasks to robots."""
        assignments: dict[int, list[Task]] = {rid: [] for rid in robot_positions}
        for task in tasks:
            best_robot = -1
            best_cost = float("inf")
            for rid, pos in robot_positions.items():
                cap = robot_capabilities.get(rid, RobotCapability.GENERIC) if robot_capabilities else RobotCapability.GENERIC
                if cap != task.required_capability and task.required_capability != RobotCapability.GENERIC:
                    continue
                cost = math.sqrt((pos[0] - task.position[0])**2 + (pos[1] - task.position[1])**2)
                cost /= max(task.priority, 0.01)
                if cost < best_cost:
                    best_cost = cost
                    best_robot = rid
            if best_robot >= 0:
                task.assigned_to = best_robot
                task.status = "assigned"
                assignments[best_robot].append(task)
        return assignments


# ---------------------------------------------------------------------------
# Pheromone Grid (Stigmergy)
# ---------------------------------------------------------------------------

class PheromoneGrid:
    """2D grid for digital pheromone simulation."""

    def __init__(self, width: int = 100, height: int = 100, resolution: float = 0.1):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.grid: dict[PheromoneType, list[list[float]]] = {
            pt: [[0.0] * width for _ in range(height)] for pt in PheromoneType
        }
        self.evaporation_rate: dict[PheromoneType, float] = {pt: 0.01 for pt in PheromoneType}
        self.diffusion_rate: dict[PheromoneType, float] = {pt: 0.05 for pt in PheromoneType}

    def _world_to_grid(self, x: float, y: float) -> tuple[int, int]:
        gx = int(x / self.resolution) % self.width
        gy = int(y / self.resolution) % self.height
        return gx, gy

    def deposit(self, x: float, y: float, pheromone_type: PheromoneType, strength: float = 1.0) -> None:
        gx, gy = self._world_to_grid(x, y)
        self.grid[pheromone_type][gy][gx] = min(1.0, self.grid[pheromone_type][gy][gx] + strength)

    def evaporate(self, dt: float = 0.1) -> None:
        for pt in PheromoneType:
            rate = self.evaporation_rate[pt]
            for gy in range(self.height):
                for gx in range(self.width):
                    self.grid[pt][gy][gx] *= max(0.0, 1.0 - rate * dt)

    def diffuse(self, dt: float = 0.1) -> None:
        for pt in PheromoneType:
            rate = self.diffusion_rate[pt]
            new_grid = [row[:] for row in self.grid[pt]]
            for gy in range(1, self.height - 1):
                for gx in range(1, self.width - 1):
                    neighbors_sum = (
                        self.grid[pt][gy-1][gx] + self.grid[pt][gy+1][gx] +
                        self.grid[pt][gy][gx-1] + self.grid[pt][gy][gx+1]
                    )
                    avg = neighbors_sum / 4.0
                    new_grid[gy][gx] = self.grid[pt][gy][gx] * (1 - rate) + avg * rate
            self.grid[pt] = new_grid

    def sense(self, x: float, y: float, pheromone_type: PheromoneType, sensor_radius: float = 1.0) -> float:
        gx, gy = self._world_to_grid(x, y)
        r = int(sensor_radius / self.resolution)
        total = 0.0
        count = 0
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                nx, ny = gx + dx, gy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    total += self.grid[pheromone_type][ny][nx]
                    count += 1
        return total / count if count > 0 else 0.0

    def sense_gradient(self, x: float, y: float, sensor_radius: float = 1.0) -> tuple[float, float]:
        """Compute the pheromone concentration gradient at a position."""
        dx = self.sense(x + 0.1, y, PheromoneType.TRAIL, sensor_radius) - \
             self.sense(x - 0.1, y, PheromoneType.TRAIL, sensor_radius)
        dy = self.sense(x, y + 0.1, PheromoneType.TRAIL, sensor_radius) - \
             self.sense(x, y - 0.1, PheromoneType.TRAIL, sensor_radius)
        return (dx, dy)


# ---------------------------------------------------------------------------
# Formation Control
# ---------------------------------------------------------------------------

class FormationController:
    """Compute desired positions for formation flying/driving."""

    def __init__(self, pattern: FormationPattern = FormationPattern.LINE, spacing: float = 2.0):
        self.pattern = pattern
        self.spacing = spacing

    def compute_desired_positions(self, leader_pos: tuple[float, float], leader_heading: float,
                                   num_agents: int) -> dict[int, tuple[float, float]]:
        if self.pattern == FormationPattern.LINE:
            return self._line(leader_pos, leader_heading, num_agents)
        elif self.pattern == FormationPattern.V_SHAPE:
            return self._v_shape(leader_pos, leader_heading, num_agents)
        elif self.pattern == FormationPattern.CIRCLE:
            return self._circle(leader_pos, num_agents)
        elif self.pattern == FormationPattern.GRID:
            return self._grid(leader_pos, num_agents)
        elif self.pattern == FormationPattern.DIAMOND:
            return self._diamond(leader_pos, num_agents)
        return {}

    def _line(self, leader_pos: tuple[float, float], heading: float,
              num_agents: int) -> dict[int, tuple[float, float]]:
        positions = {0: leader_pos}
        for i in range(1, num_agents):
            offset = i * self.spacing
            positions[i] = (
                leader_pos[0] - offset * math.cos(heading),
                leader_pos[1] - offset * math.sin(heading),
            )
        return positions

    def _v_shape(self, leader_pos: tuple[float, float], heading: float,
                 num_agents: int) -> dict[int, tuple[float, float]]:
        positions = {0: leader_pos}
        half = num_agents // 2
        for i in range(1, num_agents):
            side = 1 if i % 2 == 1 else -1
            row = (i + 1) // 2
            positions[i] = (
                leader_pos[0] - row * self.spacing * math.cos(heading) + side * row * self.spacing * 0.5 * math.sin(heading),
                leader_pos[1] - row * self.spacing * math.sin(heading) - side * row * self.spacing * 0.5 * math.cos(heading),
            )
        return positions

    def _circle(self, center: tuple[float, float], num_agents: int) -> dict[int, tuple[float, float]]:
        radius = self.spacing * num_agents / (2 * math.pi)
        positions = {}
        for i in range(num_agents):
            angle = 2 * math.pi * i / num_agents
            positions[i] = (center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle))
        return positions

    def _grid(self, origin: tuple[float, float], num_agents: int) -> dict[int, tuple[float, float]]:
        cols = int(math.ceil(math.sqrt(num_agents)))
        positions = {}
        for i in range(num_agents):
            row = i // cols
            col = i % cols
            positions[i] = (origin[0] + col * self.spacing, origin[1] + row * self.spacing)
        return positions

    def _diamond(self, center: tuple[float, float], num_agents: int) -> dict[int, tuple[float, float]]:
        positions = {0: center}
        offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for i in range(1, num_agents):
            layer = (i - 1) // 4 + 1
            idx = (i - 1) % 4
            dx, dy = offsets[idx]
            positions[i] = (center[0] + dx * self.spacing * layer, center[1] + dy * self.spacing * layer)
        return positions


# ---------------------------------------------------------------------------
# Swarm Simulator
# ---------------------------------------------------------------------------

class SwarmSimulator:
    """Simulate a swarm of agents with flocking behavior."""

    def __init__(self, config: FlockingConfig | None = None):
        self.config = config or FlockingConfig()
        self._agents: list[Agent] = []
        self._flocking = FlockingEngine(self.config)
        self._step_count = 0

    def add_agent(self, agent: Agent) -> None:
        self._agents.append(agent)

    def step(self, dt: float = 0.1) -> None:
        """Advance the simulation by one time step."""
        for agent in self._agents:
            neighbors = [a for a in self._agents if a.agent_id != agent.agent_id]
            fx, fy = self._flocking.compute_forces(agent, neighbors)

            vx = agent.velocity[0] + fx * dt
            vy = agent.velocity[1] + fy * dt

            speed = math.sqrt(vx**2 + vy**2)
            if speed > self.config.max_speed:
                vx = vx / speed * self.config.max_speed
                vy = vy / speed * self.config.max_speed

            x = agent.position[0] + vx * dt
            y = agent.position[1] + vy * dt

            # Bounds wrapping
            x_min, y_min, x_max, y_max = self.config.bounds
            x = x_min + (x - x_min) % (x_max - x_min)
            y = y_min + (y - y_min) % (y_max - y_min)

            agent.position = (x, y)
            agent.velocity = (vx, vy)
            agent.heading = math.atan2(vy, vx)

        self._step_count += 1

    def get_swarm_center(self) -> tuple[float, float]:
        if not self._agents:
            return (0.0, 0.0)
        cx = sum(a.position[0] for a in self._agents) / len(self._agents)
        cy = sum(a.position[1] for a in self._agents) / len(self._agents)
        return (cx, cy)

    def get_cohesion_metric(self) -> float:
        center = self.get_swarm_center()
        if not self._agents:
            return 0.0
        total_dist = sum(
            math.sqrt((a.position[0] - center[0])**2 + (a.position[1] - center[1])**2)
            for a in self._agents
        )
        return total_dist / len(self._agents)

    def get_spread(self) -> float:
        center = self.get_swarm_center()
        if not self._agents:
            return 0.0
        return max(
            math.sqrt((a.position[0] - center[0])**2 + (a.position[1] - center[1])**2)
            for a in self._agents
        )

    def get_metrics(self) -> SwarmMetrics:
        center = self.get_swarm_center()
        avg_speed = sum(a.vel.magnitude() for a in self._agents) / max(len(self._agents), 1)
        return SwarmMetrics(
            num_agents=len(self._agents),
            center=center,
            cohesion=self.get_cohesion_metric(),
            average_speed=avg_speed,
            spread=self.get_spread(),
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the swarm robotics module."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    print("=== Swarm Robotics Demo ===\n")

    # 1. Flocking Simulation
    print("--- Flocking Simulation ---")
    config = FlockingConfig(
        separation_weight=1.5,
        alignment_weight=1.0,
        cohesion_weight=1.0,
        perception_radius=5.0,
        max_speed=2.0,
    )
    sim = SwarmSimulator(config)
    for i in range(30):
        sim.add_agent(Agent(
            agent_id=i,
            position=(random.uniform(-10, 10), random.uniform(-10, 10)),
            velocity=(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)),
        ))

    for step in range(100):
        sim.step(dt=0.1)
        if step % 25 == 0:
            metrics = sim.get_metrics()
            print(f"  Step {step}: center=({metrics.center[0]:.1f}, {metrics.center[1]:.1f}), "
                  f"cohesion={metrics.cohesion:.3f}, spread={metrics.spread:.3f}")

    # 2. Consensus Protocol
    print("\n--- Consensus Protocol (Leader Election) ---")
    protocol = ConsensusProtocol(protocol_type="leader_election")
    agents = [AgentState(agent_id=i, value=float(random.uniform(0, 100))) for i in range(20)]
    for round_num in range(100):
        agents = protocol.step(agents, neighbors_fn=protocol.random_neighbors)
        if protocol.has_converged(agents):
            leader = max(agents, key=lambda a: a.value)
            print(f"  Converged at round {round_num}: leader=agent {leader.agent_id} (value={leader.value:.4f})")
            break
    else:
        print("  Did not converge within 100 rounds")

    # 3. Task Allocation
    print("\n--- Task Allocation (Auction) ---")
    allocator = TaskAllocator(allocation_type="auction")
    tasks = [
        Task(task_id="t1", required_capability=RobotCapability.SENSOR, priority=1.0, position=(5, 5)),
        Task(task_id="t2", required_capability=RobotCapability.TRANSPORT, priority=0.8, position=(10, 3)),
        Task(task_id="t3", required_capability=RobotCapability.SENSOR, priority=0.5, position=(2, 8)),
    ]
    robot_positions = {0: (0, 0), 1: (5, 3), 2: (10, 10)}
    robot_caps = {0: RobotCapability.SENSOR, 1: RobotCapability.TRANSPORT, 2: RobotCapability.SENSOR}
    assignments = allocator.allocate(tasks, robot_positions, robot_caps)
    for rid, task_list in assignments.items():
        print(f"  Robot {rid}: {[t.task_id for t in task_list]}")

    # 4. Pheromone Grid
    print("\n--- Pheromone Trail Following ---")
    grid = PheromoneGrid(width=50, height=50, resolution=0.2)
    for i in range(10):
        grid.deposit(x=i * 0.5, y=25 * 0.2, pheromone_type=PheromoneType.TRAIL, strength=0.8)
    grid.diffuse(dt=0.1)
    grid.evaporate(dt=0.1)
    grad = grid.sense_gradient(x=2.5, y=5.0, sensor_radius=1.0)
    print(f"  Gradient at (2.5, 5.0): ({grad[0]:.4f}, {grad[1]:.4f})")

    # 5. Formation Control
    print("\n--- Formation Control ---")
    for pattern in [FormationPattern.LINE, FormationPattern.V_SHAPE, FormationPattern.CIRCLE, FormationPattern.GRID]:
        fc = FormationController(pattern=pattern, spacing=2.0)
        positions = fc.compute_desired_positions((0, 0), 0.0, num_agents=6)
        print(f"  {pattern.value}: {len(positions)} positions")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
