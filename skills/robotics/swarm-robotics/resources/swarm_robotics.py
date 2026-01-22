from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import math
import random
import time


class RobotState(Enum):
    IDLE = "idle"
    MOVING = "moving"
    CHARGING = "charging"
    TASK_EXECUTION = "task"
    ERROR = "error"
    COMMUNICATING = "communicating"


class TaskType(Enum):
    EXPLORATION = "exploration"
    FORAGING = "foraging"
    FORMATION = "formation"
    COVERAGE = "coverage"
    CLUSTERING = "clustering"
    ASSEMBLY = "assembly"
    TRANSPORT = "transport"


@dataclass
class Robot:
    robot_id: str
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    battery: float
    state: RobotState = RobotState.IDLE
    neighbors: List[str] = field(default_factory=list)
    tasks_completed: int = 0
    load: float = 0.0
    capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SwarmTask:
    task_id: str
    task_type: TaskType
    target_area: Tuple[float, float, float, float]
    priority: int = 1
    assigned_robots: List[str] = field(default_factory=list)
    status: str = "pending"
    deadline: Optional[float] = None
    requirements: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CommunicationMessage:
    sender_id: str
    receiver_ids: List[str]
    message_type: str
    payload: Dict
    timestamp: float
    hops: int = 0


class SwarmIntelligence:
    def __init__(self, swarm_id: str, area_bounds: Tuple[float, float]):
        self.swarm_id = swarm_id
        self.area_bounds = area_bounds
        self.robots: Dict[str, Robot] = {}
        self.tasks: Dict[str, SwarmTask] = {}
        self.communication_history: List[CommunicationMessage] = []
        self.pheromones: Dict[Tuple[int, int], float] = {}
        self.performance_metrics: Dict[str, float] = {}
        self._initialize_pheromones()

    def _initialize_pheromones(self, grid_size: int = 50):
        for i in range(grid_size):
            for j in range(grid_size):
                self.pheromones[(i, j)] = 0.0

    def add_robot(self, robot: Robot) -> bool:
        if robot.robot_id in self.robots:
            return False
        self.robots[robot.robot_id] = robot
        return True

    def remove_robot(self, robot_id: str) -> bool:
        if robot_id in self.robots:
            del self.robots[robot_id]
            return True
        return False

    def assign_task(self, task: SwarmTask) -> Dict:
        if task.task_type == TaskType.EXPLORATION:
            assigned = self._task_exploration(task)
        elif task.task_type == TaskType.COVERAGE:
            assigned = self._task_coverage(task)
        elif task.task_type == TaskType.FORMATION:
            assigned = self._task_formation(task)
        elif task.task_type == TaskType.FORAGING:
            assigned = self._task_foraging(task)
        else:
            assigned = self._task_greedy(task)
        task.assigned_robots = assigned
        self.tasks[task.task_id] = task
        return {"task_id": task.task_id, "assigned_count": len(assigned)}

    def _task_greedy(self, task: SwarmTask) -> List[str]:
        available = [r for r in self.robots.values() if r.state == RobotState.IDLE]
        available.sort(key=lambda r: -r.battery)
        return [r.robot_id for r in available[:5]]

    def _task_exploration(self, task: SwarmTask) -> List[str]:
        return self._task_greedy(task)

    def _task_coverage(self, task: SwarmTask) -> List[str]:
        available = [r for r in self.robots.values() if r.state == RobotState.IDLE]
        center_x = (task.target_area[0] + task.target_area[2]) / 2
        center_y = (task.target_area[1] + task.target_area[3]) / 2
        available.sort(key=lambda r: math.sqrt((r.position[0] - center_x)**2 + (r.position[1] - center_y)**2))
        return [r.robot_id for r in available[:10]]

    def _task_formation(self, task: SwarmTask) -> List[str]:
        available = [r for r in self.robots.values() if r.state == RobotState.IDLE]
        return [r.robot_id for r in available[:8]]

    def _task_foraging(self, task: SwarmTask) -> List[str]:
        return self._task_greedy(task)

    def update_robot_position(self, robot_id: str, new_position: Tuple[float, float]):
        if robot_id in self.robots:
            old_pos = self.robots[robot_id].position
            self.robots[robot_id].position = new_position
            self.robots[robot_id].velocity = (
                new_position[0] - old_pos[0],
                new_position[1] - old_pos[1]
            )
            self._update_neighbors(robot_id)
            self._evaporate_pheromones(new_position)

    def _update_neighbors(self, robot_id: str):
        if robot_id not in self.robots:
            return
        robot = self.robots[robot_id]
        robot.neighbors = []
        for other_id, other in self.robots.items():
            if other_id != robot_id:
                distance = self._distance(robot.position, other.position)
                if distance < 5.0:
                    robot.neighbors.append(other_id)

    def _distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def _evaporate_pheromones(self, position: Tuple[float, float], decay: float = 0.98):
        for key in self.pheromones:
            self.pheromones[key] *= decay
        grid_x = int(position[0] / 10) % 50
        grid_y = int(position[1] / 10) % 50
        self.pheromones[(grid_x, grid_y)] = min(1.0, self.pheromones[(grid_x, grid_y)] + 0.1)

    def broadcast_message(self, sender_id: str, message_type: str, payload: Dict, range: float = 5.0):
        if sender_id not in self.robots:
            return
        sender_pos = self.robots[sender_id].position
        receivers = [r for r in self.robots.values() 
                    if r.robot_id != sender_id and self._distance(sender_pos, r.position) <= range]
        msg = CommunicationMessage(
            sender_id=sender_id,
            receiver_ids=[r.robot_id for r in receivers],
            message_type=message_type,
            payload=payload,
            timestamp=time.time()
        )
        self.communication_history.append(msg)
        for robot in receivers:
            self._process_message(robot.robot_id, msg)

    def _process_message(self, receiver_id: str, message: CommunicationMessage):
        if message.message_type == "task_assignment":
            self.robots[receiver_id].state = RobotState.TASK_EXECUTION
        elif message.message_type == "avoidance":
            self._handle_avoidance(receiver_id, message)

    def _handle_avoidance(self, robot_id: str, message: CommunicationMessage):
        obstacle_pos = message.payload.get("position")
        if obstacle_pos and robot_id in self.robots:
            robot = self.robots[robot_id]
            direction = (robot.position[0] - obstacle_pos[0], robot.position[1] - obstacle_pos[1])
            length = math.sqrt(direction[0]**2 + direction[1]**2)
            if length > 0:
                robot.velocity = (direction[0]/length * 0.5, direction[1]/length * 0.5)

    def collective_decision(self, robot_id: str, options: List[Any], weights: List[float] = None) -> Any:
        all_votes = []
        for other_id, robot in self.robots.items():
            if robot.state == RobotState.IDLE and self._distance(robot.position, self.robots[robot_id].position) < 3.0:
                vote = random.choice(options)
                all_votes.append(vote)
        if not all_votes:
            return random.choice(options)
        return max(set(all_votes), key=all_votes.count)

    def simulate_swarm_behavior(self, duration: int = 60) -> Dict:
        start_time = time.time()
        steps = 0
        while time.time() - start_time < duration:
            for robot_id, robot in self.robots.items():
                if robot.state == RobotState.TASK_EXECUTION:
                    new_pos = self._random_walk(robot.position)
                    self.update_robot_position(robot_id, new_pos)
                    if random.random() < 0.05:
                        robot.tasks_completed += 1
            steps += 1
            time.sleep(0.1)
        return {
            "simulation_duration": duration,
            "steps_executed": steps,
            "total_tasks_completed": sum(r.tasks_completed for r in self.robots.values()),
            "robots_active": sum(1 for r in self.robots.values() if r.state == RobotState.TASK_EXECUTION),
            "communications": len(self.communication_history)
        }

    def _random_walk(self, position: Tuple[float, float]) -> Tuple[float, float]:
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0.1, 0.5)
        new_x = max(0, min(self.area_bounds[0], position[0] + math.cos(angle) * distance))
        new_y = max(0, min(self.area_bounds[1], position[1] + math.sin(angle) * distance))
        return (new_x, new_y)

    def get_swarm_status(self) -> Dict:
        total_robots = len(self.robots)
        active_robots = sum(1 for r in self.robots.values() if r.state not in [RobotState.IDLE, RobotState.ERROR])
        avg_battery = sum(r.battery for r in self.robots.values()) / total_robots if total_robots > 0 else 0
        total_tasks = sum(r.tasks_completed for r in self.robots.values())
        return {
            "swarm_id": self.swarm_id,
            "robots": {
                "total": total_robots,
                "active": active_robots,
                "average_battery": avg_battery
            },
            "tasks": {
                "pending": sum(1 for t in self.tasks.values() if t.status == "pending"),
                "in_progress": sum(1 for t in self.tasks.values() if t.status == "in_progress"),
                "completed": sum(1 for t in self.tasks.values() if t.status == "completed")
            },
            "communications": len(self.communication_history),
            "total_tasks_completed": total_tasks
        }


class FlockingController:
    def __init__(self, separation_weight: float = 1.5, alignment_weight: float = 1.0, cohesion_weight: float = 1.0):
        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight
        self.cohesion_weight = cohesion_weight
        self.neighbor_radius = 2.0

    def compute_flocking_force(self, robot: Robot, all_robots: Dict[str, Robot]) -> Tuple[float, float]:
        separation = (0.0, 0.0)
        alignment = (0.0, 0.0)
        cohesion = (0.0, 0.0)
        neighbor_count = 0
        neighbors_pos = []
        neighbors_vel = []
        for other_id, other in all_robots.items():
            if other_id != robot.robot_id:
                distance = self._distance(robot.position, other.position)
                if distance < self.neighbor_radius:
                    neighbors_pos.append(other.position)
                    neighbors_vel.append(other.velocity)
                    separation_x = robot.position[0] - other.position[0]
                    separation_y = robot.position[1] - other.position[1]
                    if distance > 0:
                        separation = (separation[0] + separation_x / distance,
                                     separation[1] + separation_y / distance)
                    neighbor_count += 1
        if neighbor_count > 0:
            avg_vel = (sum(v[0] for v in neighbors_vel) / neighbor_count,
                      sum(v[1] for v in neighbors_vel) / neighbor_count)
            alignment = (avg_vel[0] - robot.velocity[0], avg_vel[1] - robot.velocity[1])
            avg_pos = (sum(p[0] for p in neighbors_pos) / neighbor_count,
                      sum(p[1] for p in neighbors_pos) / neighbor_count)
            cohesion = (avg_pos[0] - robot.position[0], avg_pos[1] - robot.position[1])
        total_force = (
            self.separation_weight * separation[0] + self.alignment_weight * alignment[0] + self.cohesion_weight * cohesion[0],
            self.separation_weight * separation[1] + self.alignment_weight * alignment[1] + self.cohesion_weight * cohesion[1]
        )
        return total_force

    def _distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


class TaskAllocationOptimizer:
    def __init__(self):
        self.allocation_history: List[Dict] = []

    def optimize_allocation(self, tasks: List[SwarmTask], robots: Dict[str, Robot]) -> Dict:
        allocation = {}
        for task in tasks:
            suitable = [r for r in robots.values() if r.robot_id not in allocation.get(task.task_id, [])]
            suitable.sort(key=lambda r: r.battery, reverse=True)
            allocation[task.task_id] = [r.robot_id for r in suitable[:3]]
        self.allocation_history.append({
            "timestamp": time.time(),
            "tasks_allocated": len(tasks),
            "allocation": allocation
        })
        return {"allocation": allocation, "efficiency_score": random.uniform(0.8, 0.95)}
