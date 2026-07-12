"""
navigation.py — Robot localization, mapping, path planning, and trajectory tracking.

Provides SLAM, particle filter localization, A* and RRT planning, pure pursuit and
Stanley controllers, EKF odometry fusion, costmap management, and DWA local planning.
"""

from __future__ import annotations

import enum
import logging
import math
import random
import time
from dataclasses import dataclass, field
from typing import Any, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PlannerType(enum.Enum):
    """Path planning algorithms."""
    ASTAR = "astar"
    DIJKSTRA = "dijkstra"
    RRT = "rrt"
    RRT_STAR = "rrt_star"


class ControllerType(enum.Enum):
    """Trajectory tracking controllers."""
    PURE_PURSUIT = "pure_pursuit"
    STANLEY = "stanley"
    PID = "pid"


class MapCellState(enum.Enum):
    """Occupancy grid cell states."""
    FREE = 0
    OCCUPIED = 1
    UNKNOWN = 2
    INFLATED = 3


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Vector2:
    """2D vector for navigation."""
    x: float = 0.0
    y: float = 0.0

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def distance_to(self, other: Vector2) -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def normalize(self) -> Vector2:
        m = self.magnitude()
        return Vector2(self.x / m, self.y / m) if m > 1e-10 else Vector2(0, 0)


@dataclass
class Pose2D:
    """2D pose with position and heading."""
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0  # radians

    def distance_to(self, other: Pose2D) -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


@dataclass
class Velocity:
    """Linear and angular velocity command."""
    linear: float = 0.0
    angular: float = 0.0


@dataclass
class LidarScan:
    """LiDAR scan data."""
    ranges: list[float] = field(default_factory=list)
    angle_min: float = -math.pi
    angle_max: float = math.pi
    angle_increment: float = math.pi / 180.0
    timestamp_s: float = 0.0
    step_count: int = 0
    loop_closure_detected: bool = False


@dataclass
class IMUData:
    """IMU sensor data."""
    linear_acceleration: tuple[float, float, float] = (0.0, 0.0, 0.0)
    angular_velocity: tuple[float, float, float] = (0.0, 0.0, 0.0)
    orientation: tuple[float, float, float] = (0.0, 0.0, 0.0)
    timestamp_s: float = 0.0


@dataclass
class WheelOdometry:
    """Wheel encoder odometry."""
    linear_velocity: float = 0.0
    angular_velocity: float = 0.0
    timestamp_s: float = 0.0


@dataclass
class DynamicObstacle:
    """A dynamic obstacle in the environment."""
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    radius: float = 0.3


@dataclass
class SLAMConfig:
    """Configuration for SLAM."""
    map_resolution: float = 0.05
    map_size_cells: tuple[int, int] = (400, 400)
    loop_closure_enabled: bool = True
    max_particles: int = 50
    scan_buffer_size: int = 20


@dataclass
class Costmap:
    """Layered costmap for navigation."""
    width_cells: int = 200
    height_cells: int = 200
    resolution: float = 0.05
    origin_x: float = 0.0
    origin_y: float = 0.0
    data: list[list[int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.data:
            self.data = [[0] * self.width_cells for _ in range(self.height_cells)]

    def world_to_grid(self, x: float, y: float) -> tuple[int, int]:
        gx = int((x - self.origin_x) / self.resolution)
        gy = int((y - self.origin_y) / self.resolution)
        return max(0, min(gx, self.width_cells - 1)), max(0, min(gy, self.height_cells - 1))

    def grid_to_world(self, gx: int, gy: int) -> tuple[float, float]:
        return (gx * self.resolution + self.origin_x, gy * self.resolution + self.origin_y)

    def set_occupied(self, x: float, y: float) -> None:
        gx, gy = self.world_to_grid(x, y)
        self.data[gy][gx] = 100

    def is_occupied(self, x: float, y: float) -> bool:
        gx, gy = self.world_to_grid(x, y)
        return self.data[gy][gx] >= 50

    def inflate(self, radius_m: float) -> None:
        radius_cells = int(radius_m / self.resolution)
        new_data = [row[:] for row in self.data]
        for gy in range(self.height_cells):
            for gx in range(self.width_cells):
                if self.data[gy][gx] >= 50:
                    for dy in range(-radius_cells, radius_cells + 1):
                        for dx in range(-radius_cells, radius_cells + 1):
                            ny, nx = gy + dy, gx + dx
                            if 0 <= ny < self.height_cells and 0 <= nx < self.width_cells:
                                if (dx**2 + dy**2) ** 0.5 <= radius_cells:
                                    new_data[ny][nx] = max(new_data[ny][nx], 80)
        self.data = new_data


@dataclass
class Particle:
    """A particle in the particle filter."""
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0
    weight: float = 1.0


# ---------------------------------------------------------------------------
# Occupancy Grid Mapping
# ---------------------------------------------------------------------------

class OccupancyGridMapper:
    """Build occupancy grid maps from LiDAR scans."""

    def __init__(self, resolution: float = 0.05, width_cells: int = 400, height_cells: int = 400):
        self.resolution = resolution
        self.grid: list[list[float]] = [[0.5] * width_cells for _ in range(height_cells)]
        self.width = width_cells
        self.height = height_cells
        self.log_odds_occ = 0.85
        self.log_odds_free = -0.4

    def update(self, pose: Pose2D, scan: LidarScan) -> None:
        """Update the grid with a new LiDAR scan."""
        for i, r in enumerate(scan.ranges):
            if r <= 0 or r > 30.0:
                continue
            angle = scan.angle_min + i * scan.angle_increment
            hit_x = pose.x + r * math.cos(pose.theta + angle)
            hit_y = pose.y + r * math.sin(pose.theta + angle)
            gx, gy = self._world_to_grid(hit_x, hit_y)
            if 0 <= gx < self.width and 0 <= gy < self.height:
                self.grid[gy][gx] = min(1.0, self.grid[gy][gx] + self.log_odds_occ)

            # Mark free cells along the ray
            for t in range(0, int(r / self.resolution), 2):
                fx = pose.x + t * self.resolution * math.cos(pose.theta + angle)
                fy = pose.y + t * self.resolution * math.sin(pose.theta + angle)
                fgx, fgy = self._world_to_grid(fx, fy)
                if 0 <= fgx < self.width and 0 <= fgy < self.height:
                    self.grid[fgy][fgx] = max(0.0, self.grid[fgy][fgx] + self.log_odds_free)

    def _world_to_grid(self, x: float, y: float) -> tuple[int, int]:
        return int(x / self.resolution + self.width // 2), int(y / self.resolution + self.height // 2)


# ---------------------------------------------------------------------------
# SLAM Engine
# ---------------------------------------------------------------------------

class SLAMEngine:
    """Simplified SLAM with particle filter and loop closure."""

    def __init__(self, config: SLAMConfig | None = None):
        self.config = config or SLAMConfig()
        self._mapper = OccupancyGridMapper(
            resolution=self.config.map_resolution,
            width_cells=self.config.map_size_cells[0],
            height_cells=self.config.map_size_cells[1],
        )
        self._pose = Pose2D()
        self._step_count = 0
        self._visited_places: list[Pose2D] = []

    def process_scan(self, scan: LidarScan) -> Pose2D:
        """Process a LiDAR scan and update the map."""
        self._mapper.update(self._pose, scan)
        self._visited_places.append(Pose2D(self._pose.x, self._pose.y, self._pose.theta))

        # Loop closure detection (simplified)
        if self.config.loop_closure_enabled and len(self._visited_places) > 50:
            for vp in self._visited_places[:-50]:
                if self._pose.distance_to(vp) < 0.5:
                    scan.loop_closure_detected = True
                    break

        self._step_count += 1
        return Pose2D(self._pose.x, self._pose.y, self._pose.theta)


# ---------------------------------------------------------------------------
# Particle Filter Localization
# ---------------------------------------------------------------------------

class ParticleFilter:
    """Monte Carlo localization using a particle filter."""

    def __init__(self, num_particles: int = 1000, map_data: OccupancyGridMapper | None = None,
                 sigma: float = 0.2):
        self.num_particles = num_particles
        self.map_data = map_data
        self.sigma = sigma
        self._particles = [Particle(
            x=random.uniform(-5, 5),
            y=random.uniform(-5, 5),
            theta=random.uniform(-math.pi, math.pi),
        ) for _ in range(num_particles)]

    def update(self, odom: WheelOdometry, scan: LidarScan) -> Pose2D:
        """Update particles with motion and sensor models."""
        # Motion model: propagate particles
        for p in self._particles:
            p.x += odom.linear_velocity * math.cos(p.theta) * 0.1 + random.gauss(0, self.sigma)
            p.y += odom.linear_velocity * math.sin(p.theta) * 0.1 + random.gauss(0, self.sigma)
            p.theta += odom.angular_velocity * 0.1 + random.gauss(0, self.sigma * 0.5)

        # Sensor model: reweight particles
        total_weight = 0.0
        for p in self._particles:
            match_score = self._sensor_model(p, scan)
            p.weight = match_score
            total_weight += match_score

        # Normalize weights
        if total_weight > 0:
            for p in self._particles:
                p.weight /= total_weight

        # Resample
        self._resample()

        # Estimated pose
        x_est = sum(p.x * p.weight for p in self._particles)
        y_est = sum(p.y * p.weight for p in self._particles)
        theta_est = sum(p.theta * p.weight for p in self._particles)
        return Pose2D(x_est, y_est, theta_est)

    def _sensor_model(self, particle: Particle, scan: LidarScan) -> float:
        score = 1.0
        for i in range(0, len(scan.ranges), 10):
            r = scan.ranges[i]
            if r <= 0 or r > 30.0:
                continue
            angle = scan.angle_min + i * scan.angle_increment
            hx = particle.x + r * math.cos(particle.theta + angle)
            hy = particle.y + r * math.sin(particle.theta + angle)
            if self.map_data and self.map_data.is_occupied(hx, hy):
                score *= 1.5
            else:
                score *= 0.5
        return score

    def _resample(self) -> None:
        new_particles: list[Particle] = []
        cumulative = [0.0]
        for p in self._particles:
            cumulative.append(cumulative[-1] + p.weight)

        for _ in range(self.num_particles):
            r = random.random()
            for i in range(1, len(cumulative)):
                if r <= cumulative[i]:
                    orig = self._particles[i - 1]
                    new_particles.append(Particle(
                        x=orig.x + random.gauss(0, self.sigma * 0.5),
                        y=orig.y + random.gauss(0, self.sigma * 0.5),
                        theta=orig.theta + random.gauss(0, self.sigma * 0.2),
                        weight=1.0 / self.num_particles,
                    ))
                    break
        self._particles = new_particles


# ---------------------------------------------------------------------------
# A* Path Planner
# ---------------------------------------------------------------------------

class AStarPlanner:
    """A* path planner on a costmap."""

    def __init__(self, costmap: Costmap | None = None, inflation_radius: float = 0.3):
        self.costmap = costmap or Costmap()
        self.inflation_radius = inflation_radius

    def plan(self, start: tuple[float, float], goal: tuple[float, float],
             heuristic: str = "euclidean") -> list[tuple[float, float]]:
        """Plan a path from start to goal."""
        sx, sy = self.costmap.world_to_grid(*start)
        gx, gy = self.costmap.world_to_grid(*goal)

        open_set: list[tuple[float, int, int]] = [(0.0, sx, sy)]
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], float] = {(sx, sy): 0.0}

        while open_set:
            open_set.sort(key=lambda x: x[0])
            _, cx, cy = open_set.pop(0)
            if (cx, cy) == (gx, gy):
                path = [(cx, cy)]
                current = (cx, cy)
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return [self.costmap.grid_to_world(px, py) for px, py in path]

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.costmap.width_cells and 0 <= ny < self.costmap.height_cells:
                    if self.costmap.data[ny][nx] >= 50:
                        continue
                    move_cost = math.sqrt(dx**2 + dy**2)
                    tentative_g = g_score[(cx, cy)] + move_cost
                    if tentative_g < g_score.get((nx, ny), float("inf")):
                        came_from[(nx, ny)] = (cx, cy)
                        g_score[(nx, ny)] = tentative_g
                        h = math.sqrt((nx - gx)**2 + (ny - gy)**2)
                        open_set.append((tentative_g + h, nx, ny))

        logger.warning("No path found from %s to %s", start, goal)
        return []


# ---------------------------------------------------------------------------
# RRT Planner
# ---------------------------------------------------------------------------

class RRTPlanner:
    """Rapidly-exploring Random Tree planner."""

    def __init__(self, costmap: Costmap | None = None, max_iterations: int = 5000,
                 step_size: float = 0.5, goal_bias: float = 0.1):
        self.costmap = costmap or Costmap()
        self.max_iterations = max_iterations
        self.step_size = step_size
        self.goal_bias = goal_bias

    def plan(self, start: tuple[float, float], goal: tuple[float, float]) -> list[tuple[float, float]]:
        """Plan a path using RRT."""
        tree: dict[tuple[float, float], tuple[float, float] | None] = {start: None}

        for _ in range(self.max_iterations):
            if random.random() < self.goal_bias:
                sample = goal
            else:
                sample = (random.uniform(0, self.costmap.width_cells * self.costmap.resolution),
                          random.uniform(0, self.costmap.height_cells * self.costmap.resolution))

            nearest = min(tree.keys(), key=lambda n: math.sqrt((n[0]-sample[0])**2 + (n[1]-sample[1])**2))
            direction = (sample[0] - nearest[0], sample[1] - nearest[1])
            dist = math.sqrt(direction[0]**2 + direction[1]**2)
            if dist < 1e-6:
                continue
            new = (nearest[0] + direction[0] / dist * min(self.step_size, dist),
                   nearest[1] + direction[1] / dist * min(self.step_size, dist))

            if not self.costmap.is_occupied(*new):
                tree[new] = nearest
                if math.sqrt((new[0]-goal[0])**2 + (new[1]-goal[1])**2) < self.step_size:
                    path = [goal, new]
                    current = new
                    while tree.get(current) is not None:
                        current = tree[current]
                        path.append(current)
                    path.reverse()
                    return path

        logger.warning("RRT: no path found after %d iterations", self.max_iterations)
        return []


# ---------------------------------------------------------------------------
# Pure Pursuit Controller
# ---------------------------------------------------------------------------

class PurePursuitController:
    """Pure pursuit trajectory tracking controller."""

    def __init__(self, lookahead_distance: float = 0.8, max_linear_velocity: float = 1.0,
                 max_angular_velocity: float = 2.0):
        self.lookahead_distance = lookahead_distance
        self.max_linear_velocity = max_linear_velocity
        self.max_angular_velocity = max_angular_velocity

    def track(self, path: list[tuple[float, float]], pose: Pose2D) -> Velocity:
        """Compute velocity command to follow a path."""
        if not path:
            return Velocity(0, 0)

        # Find the lookahead point
        lookahead_point = self._find_lookahead(path, pose)
        if lookahead_point is None:
            return Velocity(0, 0)

        # Compute curvature
        dx = lookahead_point[0] - pose.x
        dy = lookahead_point[1] - pose.y
        angle_to_target = math.atan2(dy, dx)
        angle_error = self._normalize_angle(angle_to_target - pose.theta)
        distance = math.sqrt(dx**2 + dy**2)

        # Control law
        linear = min(self.max_linear_velocity, distance * 0.5)
        angular = 2.0 * linear * math.sin(angle_error) / max(self.lookahead_distance, 0.01)
        angular = max(-self.max_angular_velocity, min(self.max_angular_velocity, angular))

        return Velocity(linear=linear, angular=angular)

    def _find_lookahead(self, path: list[tuple[float, float]], pose: Pose2D) -> tuple[float, float] | None:
        for point in path:
            dist = math.sqrt((point[0] - pose.x)**2 + (point[1] - pose.y)**2)
            if dist >= self.lookahead_distance:
                return point
        return path[-1] if path else None

    def _normalize_angle(self, angle: float) -> float:
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle


# ---------------------------------------------------------------------------
# Stanley Controller
# ---------------------------------------------------------------------------

class StanleyController:
    """Stanley controller for path tracking."""

    def __init__(self, k_gain: float = 2.0, k_soft: float = 1.0,
                 max_linear_velocity: float = 1.0, max_angular_velocity: float = 2.0):
        self.k_gain = k_gain
        self.k_soft = k_soft
        self.max_linear_velocity = max_linear_velocity
        self.max_angular_velocity = max_angular_velocity

    def track(self, path: list[tuple[float, float]], pose: Pose2D) -> Velocity:
        """Compute velocity command using Stanley method."""
        if not path:
            return Velocity(0, 0)

        # Find the closest point on the path
        min_dist = float("inf")
        closest_idx = 0
        for i, point in enumerate(path):
            dist = math.sqrt((point[0] - pose.x)**2 + (point[1] - pose.y)**2)
            if dist < min_dist:
                min_dist = dist
                closest_idx = i

        closest = path[closest_idx]
        next_idx = min(closest_idx + 1, len(path) - 1)
        path_point = path[next_idx]

        # Heading error
        path_angle = math.atan2(path_point[1] - closest[1], path_point[0] - closest[0])
        heading_error = path_angle - pose.theta

        # Cross-track error
        dx = pose.x - closest[0]
        dy = pose.y - closest[1]
        cross_track = math.sin(path_angle) * dx - math.cos(path_angle) * dy

        # Stanley control law
        linear = min(self.max_linear_velocity, 1.0)
        steering = heading_error + math.atan2(self.k_gain * cross_track, linear + self.k_soft)
        angular = max(-self.max_angular_velocity, min(self.max_angular_velocity, steering * 2.0))

        return Velocity(linear=linear, angular=angular)


# ---------------------------------------------------------------------------
# EKF Odometry Fusion
# ---------------------------------------------------------------------------

class EKFFusion:
    """Extended Kalman Filter for fusing IMU and wheel odometry."""

    def __init__(self):
        # State: [x, y, theta, v, omega]
        self._state = [0.0, 0.0, 0.0, 0.0, 0.0]
        self._P = [[1.0] * 5 for _ in range(5)]  # covariance
        self._Q = [[0.01] * 5 for _ in range(5)]  # process noise
        self._R_imu = [[0.1] * 3 for _ in range(3)]
        self._R_odom = [[0.05] * 2 for _ in range(2)]

    def update(self, imu: IMUData, odom: WheelOdometry) -> Pose2D:
        """Fuse IMU and odometry data."""
        # Prediction step
        dt = 0.01
        v = odom.linear_velocity
        omega = odom.angular_velocity
        self._state[0] += v * math.cos(self._state[2]) * dt
        self._state[1] += v * math.sin(self._state[2]) * dt
        self._state[2] += omega * dt
        self._state[3] = v
        self._state[4] = omega

        # Update with IMU heading
        imu_yaw = imu.orientation[2]
        innovation = imu_yaw - self._state[2]
        self._state[2] += innovation * 0.1  # simple gain

        return Pose2D(self._state[0], self._state[1], self._state[2])


# ---------------------------------------------------------------------------
# DWA Local Planner
# ---------------------------------------------------------------------------

class DWAPlanner:
    """Dynamic Window Approach local planner."""

    def __init__(self, max_speed: float = 1.5, max_accel: float = 2.0,
                 max_yaw_rate: float = 3.0, dt: float = 0.1,
                 heading_weight: float = 0.15, clearance_weight: float = 0.1,
                 velocity_weight: float = 0.1):
        self.max_speed = max_speed
        self.max_accel = max_accel
        self.max_yaw_rate = max_yaw_rate
        self.dt = dt
        self.heading_weight = heading_weight
        self.clearance_weight = clearance_weight
        self.velocity_weight = velocity_weight

    def plan(self, current: Velocity, goal: tuple[float, float],
             obstacles: list[DynamicObstacle], path: list[tuple[float, float]]) -> Velocity:
        """Select the best velocity command using DWA."""
        best_score = -float("inf")
        best_cmd = Velocity(current.linear, current.angular)

        for v in [i * 0.1 for i in range(0, int(self.max_speed * 10) + 1)]:
            for w in [i * 0.1 for i in range(-int(self.max_yaw_rate * 10), int(self.max_yaw_rate * 10) + 1)]:
                # Predict trajectory
                x, y, theta = 0, 0, 0
                for _ in range(10):
                    x += v * math.cos(theta) * self.dt
                    y += v * math.sin(theta) * self.dt
                    theta += w * self.dt

                # Score
                heading_score = self._heading_score(x, y, theta, goal)
                clearance_score = self._clearance_score(x, y, obstacles)
                velocity_score = v / self.max_speed

                total = (heading_score * self.heading_weight +
                         clearance_score * self.clearance_weight +
                         velocity_score * self.velocity_weight)

                if total > best_score:
                    best_score = total
                    best_cmd = Velocity(v, w)

        return best_cmd

    def _heading_score(self, x: float, y: float, theta: float,
                       goal: tuple[float, float]) -> float:
        goal_angle = math.atan2(goal[1] - y, goal[0] - x)
        error = abs(goal_angle - theta)
        return 1.0 - error / math.pi

    def _clearance_score(self, x: float, y: float, obstacles: list[DynamicObstacle]) -> float:
        if not obstacles:
            return 1.0
        min_dist = min(math.sqrt((x - o.x)**2 + (y - o.y)**2) for o in obstacles)
        return min(1.0, min_dist / 2.0)


# ---------------------------------------------------------------------------
# Waypoint Navigator
# ---------------------------------------------------------------------------

class WaypointNavigator:
    """Follow a sequence of waypoints with heading constraints."""

    def __init__(self, arrival_tolerance: float = 0.5, default_speed: float = 1.0):
        self.arrival_tolerance = arrival_tolerance
        self.default_speed = default_speed
        self._current_index = 0
        self._controller = PurePursuitController(lookahead_distance=0.8)

    def set_waypoints(self, waypoints: list[tuple[float, float]]) -> None:
        self._waypoints = waypoints
        self._current_index = 0

    def get_command(self, pose: Pose2D) -> Velocity:
        """Get velocity command toward the current waypoint."""
        if self._current_index >= len(self._waypoints):
            return Velocity(0, 0)

        wp = self._waypoints[self._current_index]
        dist = math.sqrt((wp[0] - pose.x)**2 + (wp[1] - pose.y)**2)

        if dist < self.arrival_tolerance:
            self._current_index += 1
            if self._current_index >= len(self._waypoints):
                return Velocity(0, 0)
            wp = self._waypoints[self._current_index]

        return self._controller.track([wp, wp], pose)


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the navigation module."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    print("=== Navigation Demo ===\n")

    # 1. SLAM
    print("--- SLAM Map Building ---")
    slam = SLAMEngine(SLAMConfig(loop_closure_enabled=True, max_particles=50))
    scan = LidarScan(ranges=[2.0 + random.random() for _ in range(360)])
    for step in range(5):
        scan.step_count = step
        pose = slam.process_scan(scan)
        print(f"  Step {step}: pose=({pose.x:.2f}, {pose.y:.2f}, {pose.theta:.2f})")
        scan.ranges = [r + random.uniform(-0.1, 0.1) for r in scan.ranges]

    # 2. A* Planning
    print("\n--- A* Path Planning ---")
    costmap = Costmap(width_cells=100, height_cells=100, resolution=0.1)
    for i in range(20, 40):
        costmap.set_occupied(i * 0.1, 1.0)
    astar = AStarPlanner(costmap, inflation_radius=0.3)
    path = astar.plan((0.5, 0.5), (9.0, 9.0))
    print(f"  Path: {len(path)} waypoints")

    # 3. RRT Planning
    print("\n--- RRT Path Planning ---")
    rrt = RRTPlanner(costmap, max_iterations=3000, step_size=0.5)
    rrt_path = rrt.plan((0.5, 0.5), (9.0, 9.0))
    print(f"  Path: {len(rrt_path)} waypoints")

    # 4. Pure Pursuit
    print("\n--- Pure Pursuit Controller ---")
    pp = PurePursuitController(lookahead_distance=0.8, max_linear_velocity=1.0)
    test_path = [(i * 0.5, math.sin(i * 0.3)) for i in range(20)]
    pose = Pose2D(0, 0, 0)
    for step in range(5):
        cmd = pp.track(test_path, pose)
        pose.x += cmd.linear * math.cos(pose.theta) * 0.1
        pose.y += cmd.linear * math.sin(pose.theta) * 0.1
        pose.theta += cmd.angular * 0.1
        print(f"  Step {step}: pose=({pose.x:.2f}, {pose.y:.2f}), cmd=({cmd.linear:.2f}, {cmd.angular:.2f})")

    # 5. Stanley Controller
    print("\n--- Stanley Controller ---")
    stanley = StanleyController(k_gain=2.0, k_soft=1.0)
    pose = Pose2D(0, 0, 0)
    for step in range(5):
        cmd = stanley.track(test_path, pose)
        pose.x += cmd.linear * math.cos(pose.theta) * 0.1
        pose.y += cmd.linear * math.sin(pose.theta) * 0.1
        pose.theta += cmd.angular * 0.1
        print(f"  Step {step}: pose=({pose.x:.2f}, {pose.y:.2f}), cmd=({cmd.linear:.2f}, {cmd.angular:.2f})")

    # 6. EKF Fusion
    print("\n--- EKF Odometry Fusion ---")
    ekf = EKFFusion()
    for step in range(5):
        imu = IMUData(
            linear_acceleration=(0.1, 0.0, 9.8),
            angular_velocity=(0.0, 0.0, 0.05),
            orientation=(0.0, 0.0, step * 0.05),
        )
        odom = WheelOdometry(linear_velocity=0.5, angular_velocity=0.05)
        fused = ekf.update(imu, odom)
        print(f"  Step {step}: fused=({fused.x:.3f}, {fused.y:.3f}, {fused.theta:.3f})")

    # 7. DWA Local Planner
    print("\n--- DWA Local Planner ---")
    dwa = DWAPlanner(max_speed=1.5, max_accel=2.0)
    current_vel = Velocity(0.5, 0.0)
    obstacles = [DynamicObstacle(x=3.0, y=1.0, radius=0.3)]
    best = dwa.plan(current_vel, (5.0, 5.0), obstacles, [(5.0, 5.0)])
    print(f"  Best command: linear={best.linear:.2f}, angular={best.angular:.2f}")

    # 8. Waypoint Navigator
    print("\n--- Waypoint Navigator ---")
    nav = WaypointNavigator(arrival_tolerance=0.5)
    nav.set_waypoints([(1.0, 0.0), (2.0, 1.0), (3.0, 0.0)])
    pose = Pose2D(0, 0, 0)
    for step in range(10):
        cmd = nav.get_command(pose)
        pose.x += cmd.linear * math.cos(pose.theta) * 0.2
        pose.y += cmd.linear * math.sin(pose.theta) * 0.2
        pose.theta += cmd.angular * 0.2
        print(f"  Step {step}: pose=({pose.x:.2f}, {pose.y:.2f}), wp_idx={nav._current_index}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
