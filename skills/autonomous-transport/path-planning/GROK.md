---
name: "path-planning"
category: "autonomous-transport"
version: "2.0.0"
tags: ["autonomous-transport", "path-planning", "motion-planning", "trajectory-optimization", "A*", "RRT", "MPC", "lattice-planner"]
---

# Path Planning for Autonomous Vehicles

## Overview

This module provides a comprehensive path-planning framework for autonomous vehicles, covering graph-based search (A*, Dijkstra), sampling-based methods (RRT, RRT*), optimization-based planners (MPC, sequential quadratic programming), lattice-based state-space discretization, and trajectory optimization. It integrates with HD-map providers, localization stacks, and vehicle dynamics models to produce dynamically feasible, collision-free trajectories at planning frequencies up to 100 Hz.

The planner operates across three hierarchical layers — route planning (global), behavior planning (tactical), and motion planning (local) — each producing outputs consumed by downstream layers. It supports both on-road structured environments and unstructured off-road scenarios, with real-time replanning capabilities for dynamic obstacle avoidance.

## Core Capabilities

- Global route planning using OpenStreetMap / HERE HD maps with A* and Dijkstra
- Local trajectory generation via Hybrid A*, lattice planner, and RRT*
- Model Predictive Control (MPC) with 6-DOF vehicle dynamics constraints
- Quintic polynomial trajectory smoothing for jerk-minimal paths
- Dynamic obstacle avoidance with velocity obstacle (VO) and reciprocal VO (RVO)
- Traffic rule compliance layer enforcing lane markings, speed limits, and right-of-way
- Controllability analysis verifying dynamic feasibility before trajectory execution
- Multi-goal planning with cost-function-based goal ranking
- Parallel lane-graph construction from HD-map tile data
- Slot-based trajectory deconfliction for multi-vehicle coordination
- Configurable cost weights for comfort, safety, speed, and lane-keeping objectives
- Real-time replanning triggered by perception updates (min 50 ms latency budget)

## Advanced Configuration

### Planner Profile Configuration

```yaml
planner:
  profile: "urban_highway"          # urban | highway | parking | offroad
  global:
    algorithm: "astar"              # astar | dijkstra | rrt_star
    heuristics: "euclidean"         # euclidean | manhattan | octile
    grid_resolution: 0.1            # meters per cell
    map_tile_cache_size_mb: 512
    max_route_length_km: 500
  local:
    algorithm: "lattice"            # lattice | hybrid_astar | mpc
    planning_horizon_s: 5.0
    time_step_s: 0.1
    target_speed_mps: 16.7          # ~60 km/h
    obstacle_inflation_radius_m: 0.5
    kinematic_bounds:
      max_curvature: 0.2            # 1/m (min turning radius 5m)
      max_lateral_accel: 3.0        # m/s^2
      max_longitudinal_accel: 4.0   # m/s^2
      max_longitudinal_decel: 6.0   # m/s^2
  mpc:
    prediction_horizon: 30
    control_horizon: 10
    dt: 0.1
    weight_terminal_state: 5.0
    weight_state_cost: [1.0, 1.0, 0.5, 0.3]  # x, y, yaw, v
    weight_control_effort: [0.1, 0.05]        # steering, throttle
    solver: "ipopt"                 # ipopt | sqp_method | casadi
    max_iterations: 100
    convergence_tolerance: 1e-4
  behavior:
    lane_change_debounce_s: 3.0
    min_gap_m: 2.0
    following_time_gap_s: 1.5
    yield_decel_limit_mps2: 3.5
    intersection_horizon_m: 50.0
```

### Vehicle Dynamics Model Selection

| Model | State Dimension | Use Case | Fidelity |
|-------|----------------|----------|----------|
| Kinematic Bicycle | 4 (x, y, ψ, v) | Low-speed maneuvering | Low |
| Dynamic Bicycle | 6 (+ β, δ) | Highway and general driving | Medium |
| Single Track + Roll | 7 (+ φ) | High-speed curves | Medium-High |
| Multi-body (IPG CarMaker) | 14+ | Validation and simulation | High |

### Runtime Parameter Tuning

Parameters can be overridden at runtime via the parameter server without restarting the planner node:

```
/planner/local/target_speed_mps    12.0
/planner/mpc/weight_state_cost     [2.0, 2.0, 1.0, 0.5]
/planner/local/obstacle_inflation  0.8
```

## Architecture Patterns

### Three-Tier Planning Stack

```
┌─────────────────────────────────────────────────────────┐
│                    ROUTE PLANNER                         │
│  (HD Map + A*)                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐   │
│  │ Map Tiles │───▶│ Lane Graph│───▶│ Route Candidates│   │
│  └──────────┘    └──────────┘    └────────┬─────────┘   │
│                                           │             │
│                                    Best Route (JSON)    │
├───────────────────────────────────────────┼─────────────┤
│                BEHAVIOR PLANNER           │             │
│  ┌────────────────────────────────────────▼──────────┐  │
│  │  Finite State Machine / Decision Tree            │  │
│  │                                                   │  │
│  │  ┌─────────┐  ┌──────────┐  ┌────────────────┐  │  │
│  │  │ Lane    │  │ Lane     │  │ Intersection   │  │  │
│  │  │ Follow  │  │ Change   │  │ Navigation     │  │  │
│  │  └────┬────┘  └────┬─────┘  └───────┬────────┘  │  │
│  │       └─────────────┴────────────────┘           │  │
│  │              Behavior Command (JSON)              │  │
│  └───────────────────────────┬───────────────────────┘  │
├──────────────────────────────┼──────────────────────────┤
│            MOTION PLANNER     │                         │
│  ┌────────────────────────────▼───────────────────────┐ │
│  │  Lattice / Hybrid A* / MPC                        │ │
│  │                                                    │ │
│  │  ┌────────────┐  ┌──────────┐  ┌───────────────┐  │ │
│  │  │ State      │  │ Obstacle │  │ Cost Function │  │ │
│  │  │ Sampler    │──│ Checker  │──│ Evaluator     │  │ │
│  │  └────────────┘  └──────────┘  └───────┬───────┘  │ │
│  │                                        │          │ │
│  │  ┌────────────┐  ┌──────────┐          │          │ │
│  │  │ Trajectory │◀─│ Optimal  │◀─────────┘          │ │
│  │  │ Publisher  │  │ Selector │                     │ │
│  │  └────────────┘  └──────────┘                     │ │
│  │          Trajectory (30 Hz waypoints)             │ │
│  └────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│              CONTROLLER (Downstream)                     │
│  Longitudinal PID + Lateral Stanley / Pure Pursuit      │
└─────────────────────────────────────────────────────────┘
```

### Lattice Planner State-Space Expansion

```
          Frenet Frame (s, d)
     s (along reference path)
     ▲
     │    ┌───────┐ ┌───────┐ ┌───────┐
     │    │ State │ │ State │ │ State │  Terminal States
     │    │ (s,d, │ │ (s,d, │ │ (s,d, │
     │    │  v,a) │ │  v,a) │ │  v,a) │
     │    └───┬───┘ └───┬───┘ └───┬───┘
     │        │         │         │
     │    ┌───┴─────────┴─────────┴───┐
     │    │     Polynomial Generator  │  Quintic/Quartic
     │    │     (lateral: 5th order)  │  polynomials
     │    │     (longitudinal: 4th)   │
     │    └───────────┬───────────────┘
     │                │
     │    ┌───────────▼───────────────┐
     │    │    Collision Checker      │  Swept-volume test
     │    │    (OBB / circle approx)  │  against obstacles
     │    └───────────┬───────────────┘
     │                │
     │    ┌───────────▼───────────────┐
     │    │    Cost Function          │  J = w_j·jerk + w_l·lat
     │    │                           │     + w_s·speed + w_t·time
     │    └───────────┬───────────────┘
     │                ▼
     └──────────────────────▶ d (lateral offset)
```

### MPC Prediction Horizon Visualization

```
 Current      Planning Horizon (5.0 s)
 State t=0  ─────────────────────────────────▶
   │
   │  ●━━━━━━━━●━━━━━━━━●━━━━━━━━●━━━━━━━━●  Planned trajectory
   │  │        │        │        │        │
   │  0.0s    1.0s    2.0s    3.0s    4.0s    5.0s
   │
   │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  Obstacle predictions
   │  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  (position uncertainty
   │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   grows over time)
   │
   │  ◀─ Control Horizon (1.0 s) ─▶
   │  u0  u1  u2  u3  u4  u5  u6  u7  u8  u9
   │
   │  Controls applied: u0 only; re-solve at next tick
```

## Integration Guide

### Dependencies

| Component | Version | Purpose |
|-----------|---------|---------|
| `map-core` | >= 3.2.0 | HD map tile loading, lane-graph queries |
| `localization-fusion` | >= 2.1.0 | EKF-based pose estimation, odometry |
| `perception-stack` | >= 4.0.0 | 3D bounding-box obstacle list, tracked objects |
| `vehicle-dynamics` | >= 1.5.0 | Bicycle model, tire forces, steering actuator model |
| `common-msgs` | >= 2.0.0 | `PathPlan`, `Trajectory`, `ObstacleArray` protobuf definitions |
| `parameter-server` | >= 1.0.0 | Runtime parameter overrides without restart |

### ROS 2 Integration

```python
import rclpy
from rclpy.node import Node
from common_msgs.msg import PathPlan, Trajectory, ObstacleArray
from map_core.srv import GetLaneGraph
from path_planning.planners import LatticePlanner, MPCPlanner

class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner')
        self.declare_parameter('planner_type', 'lattice')
        self.declare_parameter('target_speed', 16.7)

        planner_type = self.get_parameter('planner_type').value
        if planner_type == 'lattice':
            self.planner = LatticePlanner(self.get_parameter('target_speed').value)
        elif planner_type == 'mpc':
            self.planner = MPCPlanner(self.get_parameter('target_speed').value)

        self.map_client = self.create_client(GetLaneGraph, '/map/get_lane_graph')
        self.sub_obstacles = self.create_subscription(
            ObstacleArray, '/perception/obstacles', self._on_obstacles, 10)
        self.sub_localization = self.create_subscription(
            Odometry, '/localization/odometry', self._on_odom, 10)
        self.pub_trajectory = self.create_publisher(Trajectory, '/planner/trajectory', 10)

    def _on_obstacles(self, msg: ObstacleArray):
        self.latest_obstacles = msg

    def _on_odom(self, msg: Odometry):
        if self.latest_obstacles is None:
            return
        request = GetLaneGraph.Request()
        request.origin = msg.pose.pose.position
        request.radius_m = 200.0
        future = self.map_client.call_async(request)
        future.add_done_callback(lambda f: self._plan(msg, f.result()))

    def _plan(self, odom_msg, lane_graph_response):
        trajectory = self.planner.plan(
            current_state=odom_msg,
            lane_graph=lane_graph_response.lane_graph,
            obstacles=self.latest_obstacles)
        self.pub_trajectory.publish(trajectory)
```

### Message Interface

```protobuf
// PathPlan — route-level output
message PathPlan {
  Header header
  repeated LaneSegment route_segments = 1;
  geometry_msgs/PoseStamped goal_pose = 2;
  float64 estimated_duration_s = 3;
  float64 estimated_distance_m = 4;
}

// Trajectory — motion-level output
message Trajectory {
  Header header
  repeated TrajectoryPoint points = 1;    // 30 Hz at 5 s horizon = 150 points
  float64 planning_horizon_s = 2;
  PlannerDebugInfo debug_info = 3;
}

message TrajectoryPoint {
  float64 time_from_start_s = 1;
  geometry_msgs/PoseStamped pose = 2;
  float64 velocity_mps = 3;
  float64 acceleration_mps2 = 4;
  float64 curvature = 5;
}
```

## Performance Optimization

### Latency Budget

| Stage | Budget (ms) | Technique |
|-------|-------------|-----------|
| Map query | 5 | Tile cache hit; async pre-fetch 500 m ahead |
| Obstacle preprocessing | 3 | Vectorized bounding-box conversion in NumPy |
| Lattice expansion | 25 | Parallel expansion of 7 terminal states per layer |
| Collision checking | 10 | Spatial hashing (cell size 2 m) + early-exit |
| Cost evaluation | 5 | SIMD-optimized cost kernel |
| Trajectory smoothing | 2 | Cubic spline interpolation (pre-computed basis) |
| Total | 50 | **Target: 20 Hz minimum, 50 Hz preferred** |

### Memory Layout

```
┌─────────────────────────────────────────────────┐
│              Shared Memory Region                │
│  ┌───────────┐  ┌───────────┐  ┌─────────────┐ │
│  │ Map Cache │  │ Obstacle  │  │ Trajectory  │ │
│  │ (256 MB)  │  │ Ring Buf  │  │ Ring Buffer │ │
│  │           │  │ (16 MB)   │  │ (4 MB)      │ │
│  └───────────┘  └───────────┘  └─────────────┘ │
│  ┌───────────────────────────────────────────┐  │
│  │  Parameter Server (lock-free read)        │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Optimization Techniques

- **Precomputed cost maps**: Static map elements (lane boundaries, speed zones) are rasterized into a cost grid at initialization, eliminating per-frame polygon intersection queries.
- **Spatial hashing for obstacles**: Obstacles are inserted into a uniform grid (cell size = 2 m). Collision checks only test obstacles in the same or adjacent cells, reducing average collision-check count from O(N) to O(1-5).
- **SIMD cost evaluation**: The lattice cost function uses SSE/AVX intrinsics for parallel evaluation of 4 candidate trajectories per instruction cycle.
- **Warm-starting MPC**: Previous optimal control sequence is shifted forward and used as the initial guess for the next solve, reducing IPOPT iteration count from ~40 to ~12.
- **Asynchronous map pre-fetching**: A background thread loads map tiles 500 m along the current route direction, keeping the tile cache hot.
- **Trajectory interpolation for output**: Only 10 control points are optimized; the output trajectory is expanded to 150 points via cubic spline interpolation in the output stage.

## Security Considerations

### Input Validation

- All incoming obstacle messages are validated for finite values, reasonable bounding-box dimensions (0.1–10 m), and monotonic timestamps.
- Map tile integrity is verified via SHA-256 checksums against a signed manifest before lane-graph construction.
- Localization covariance is clamped; if the EKF reports a covariance exceeding a configurable threshold (e.g., position std > 2 m), the planner enters a safe-state (decelerate and stop).

### Cyber-Physical Security

- Trajectory commands are signed with HMAC-SHA256 using a per-vehicle key to prevent injection attacks on the CAN bus.
- OTA parameter updates require two-factor authorization (operator approval + cryptographic signature).
- Planner debug logs are sanitized to remove raw GPS coordinates before transmission to cloud logging services.
- Map tiles received over the air are authenticated; unsigned or corrupted tiles trigger a fallback to the last known-good cache.

### Safety Envelope

- The planner enforces a hard speed limit (configurable per zone) that cannot be overridden by the behavior layer.
- Minimum following distance is a hard constraint in the cost function with infinite weight, not a soft penalty.
- Emergency braking (deceleration up to 8 m/s²) is always possible regardless of planner state.
- A watchdog timer monitors planner output frequency; if no trajectory is published within 200 ms, the controller triggers autonomous emergency braking (AEB).

## Troubleshooting Guide

| Symptom | Probable Cause | Diagnostic Steps | Resolution |
|---------|---------------|------------------|------------|
| Planner outputs empty trajectory | No lane-graph data received | Check `/map/get_lane_graph` service availability; verify map tile cache hit rate in logs | Ensure map server is running; increase `map_tile_cache_size_mb` |
| Trajectory has high jerk (> 2 m/s³) | Insufficient smoothing iterations | Check `planner.local.smoothing_iterations` parameter; inspect cost weights | Increase smoothing iterations to 5; raise `weight_jerk` cost |
| MPC solver fails to converge | Initial guess too far from feasible solution | Check warm-start state; inspect IPOPT iteration count in debug output | Ensure previous trajectory is used as warm-start; reduce `prediction_horizon` |
| Lattice planner is slow (> 80 ms) | Too many terminal states or dense obstacle grid | Profile `collision_check_count` in debug output; check spatial hash cell size | Reduce lattice layers from 5 to 3; increase spatial hash cell size to 3 m |
| Vehicle leaves lane during curve | Curvature limit too aggressive | Compare vehicle max curvature vs planned curvature in trajectory output | Reduce `target_speed_mps` or increase `max_curvature` bound |
| Planner replans erratically | Obstacle tracking jitter causing rapid cost changes | Check obstacle age distribution; verify tracker ID consistency | Increase `obstacle_inflation_radius_m`; add obstacle age filter (min 0.3 s) |
| Route planner picks suboptimal route | Heuristic mismatch or grid resolution too coarse | Compare A* open-set expansion count; check heuristic function selection | Use `octile` heuristic; reduce `grid_resolution` to 0.05 m |
| Trajectory collides with static object | Inflation radius too small for vehicle footprint | Replay trajectory with vehicle swept volume overlaid on occupancy grid | Increase `obstacle_inflation_radius_m` to vehicle half-width + 0.5 m |

## API Reference

### `LatticePlanner`

```python
class LatticePlanner:
    def __init__(self, target_speed_mps: float = 16.7):
        """Initialize lattice planner with target cruising speed."""

    def plan(self, current_state: Odometry, lane_graph: LaneGraph,
             obstacles: ObstacleArray) -> Trajectory:
        """Generate a dynamically feasible trajectory.

        Args:
            current_state: Current vehicle odometry (pose + twist).
            lane_graph: Lane graph from map_core service.
            obstacles: Tracked obstacles from perception stack.

        Returns:
            Trajectory with 150 waypoints at 30 Hz.

        Raises:
            PlanningTimeoutError: If planning exceeds 100 ms.
            NoFeasibleTrajectoryError: If all candidate trajectories fail.
        """

    def reconfigure(self, params: dict) -> None:
        """Update planner parameters at runtime via parameter server."""

    def get_debug_info(self) -> PlannerDebugInfo:
        """Return planning statistics (expand count, cost breakdown, timing)."""
```

### `MPCPlanner`

```python
class MPCPlanner:
    def __init__(self, prediction_horizon: int = 30, dt: float = 0.1):
        """Initialize MPC planner with CasADi/IPOPT backend."""

    def plan(self, current_state: Odometry, reference_path: Trajectory,
             obstacles: ObstacleArray) -> Trajectory:
        """Solve MPC optimization problem and return control trajectory.

        Uses previous solution as warm-start. Applies QP-based
        obstacle linearization at each iteration.
        """

    def set_reference_path(self, path: Trajectory) -> None:
        """Update the reference path for path-tracking MPC mode."""

    def get_solver_stats(self) -> SolverStats:
        """Return IPOPT solver statistics (iterations, objective, wall time)."""
```

### `RoutePlanner`

```python
class RoutePlanner:
    def __init__(self, map_provider: str = "hd_map"):
        """Initialize global route planner with map tile provider."""

    def find_route(self, origin: Pose, destination: Pose,
                   constraints: RouteConstraints = None) -> PathPlan:
        """Find optimal route between origin and destination.

        Supports waypoint-based routes with intermediate goals,
        highway preference, and toll avoidance constraints.
        """

    def reroute(self, current_pose: Pose, reason: str) -> PathPlan:
        """Recompute route from current position due to detour or blockage."""
```

## Data Models

### Internal State Representation

```
┌─────────────────────────────────────────────┐
│            PlannerState                      │
│  ┌───────────────┐  ┌────────────────────┐  │
│  │ vehicle_state │  │ environment_state  │  │
│  │  x, y, yaw, v│  │  obstacles: []     │  │
│  │  steer, accel │  │  lane_graph: Graph │  │
│  │  slip_angle   │  │  traffic_lights:[] │  │
│  └───────────────┘  └────────────────────┘  │
│  ┌───────────────┐  ┌────────────────────┐  │
│  │ route_state   │  │ behavior_state     │  │
│  │  current_lane │  │  fsm_state: Enum   │  │
│  │  goal_pose    │  │  lane_change_dir:  │  │
│  │  distance_to_ │  │    0 (none), ±1    │  │
│  │    goal       │  │  yield_active: bool│  │
│  └───────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────┘
```

### Frenet Frame Coordinate System

The planner operates in Frenet coordinates (s, d) relative to the reference lane centerline:
- **s**: Arc-length along the reference path (longitudinal)
- **d**: Signed lateral offset from the reference path center
- **ṡ (s_dot)**: Longitudinal speed along the reference path
- **ḋ (d_dot)**: Lateral speed relative to the reference path

Frenet-to-Cartesian conversion uses the reference path's curvature κ(s):

```
x = X(s) - d · sin(θ(s))
y = Y(s) + d · cos(θ(s))
```

### Obstacle Representation

```
Obstacle:
  id: uint64
  type: enum (VEHICLE, PEDESTRIAN, CYCLIST, STATIC)
  pose: geometry_msgs/Pose
  dimensions: {length, width, height}  # meters
  velocity: geometry_msgs/Twist
  predicted_trajectory: list[TrajectoryPoint]  # from prediction module
  confidence: float  # 0.0–1.0
  age_s: float       # time since first detection
  tracker_id: uint32 # consistent across frames
```

### Cost Function Structure

```
J_total = w_jerk  · J_jerk
        + w_lat   · J_lateral_offset
        + w_speed · J_speed_deviation
        + w_time  · J_time_to_goal
        + w_comfort · J_lateral_acceleration
        + w_safety · J_proximity_to_obstacles
        + w_rule  · J_traffic_rule_violation

Where:
  J_jerk           = ∫ (d³d/dt³)² dt       (minimize jerk)
  J_lateral_offset = ∫ d² dt               (stay centered in lane)
  J_speed_dev      = ∫ (v - v_target)² dt  (maintain target speed)
  J_time_to_goal   = T_total               (minimize travel time)
  J_lateral_accel  = ∫ (v² · κ)² dt        (comfort constraint)
  J_proximity      = Σ (1 / distance_to_obs)²  (safety penalty)
  J_traffic_rule   = Σ indicator(rule_violated)  (hard penalty)
```

## Deployment Guide

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4-core x86-64 @ 2.5 GHz | 8-core @ 3.5 GHz |
| GPU | Not required | NVIDIA Orin (for perception integration) |
| RAM | 8 GB | 16 GB (256 MB for map cache) |
| Storage | 20 GB SSD | 100 GB NVMe (map tile storage) |
| CAN Interface | 1x CAN 2.0B | 2x CAN FD |
| GNSS | Single-frequency RTK | Dual-frequency RTK + IMU |

### Docker Deployment

```dockerfile
FROM ros:humble-ros-base
RUN apt-get update && apt-get install -y \
    libeigen3-dev libcoinor-dev libipopt-dev
COPY package.xml /ros/path_planning/
COPY src/ /ros/path_planning/src/
RUN colcon build --packages-select path_planning
ENTRYPOINT ["ros2", "launch", "path_planning", "planner.launch.py"]
```

### Launch Configuration

```python
# planner.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='path_planning', executable='route_planner',
             parameters=['config/route.yaml']),
        Node(package='path_planning', executable='behavior_planner',
             parameters=['config/behavior.yaml']),
        Node(package='path_planning', executable='motion_planner',
             parameters=['config/motion.yaml']),
        Node(package='path_planning', executable='planner_node',
             parameters=[{'planner_type': 'lattice'}]),
    ])
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: path-planner
spec:
  replicas: 1
  selector:
    matchLabels:
      app: path-planner
  template:
    metadata:
      labels:
        app: path-planner
    spec:
      containers:
      - name: planner
        image: registry.example.com/path-planner:v2.0.0
        resources:
          limits:
            cpu: "4"
            memory: "8Gi"
          requests:
            cpu: "2"
            memory: "4Gi"
        env:
        - name: PLANNER_TYPE
          value: "lattice"
        - name: MAP_CACHE_SIZE_MB
          value: "256"
        volumeMounts:
        - name: map-cache
          mountPath: /var/cache/map-tiles
      volumes:
      - name: map-cache
        hostPath:
          path: /data/map-tiles
          type: Directory
```

## Monitoring and Observability

### Key Metrics

| Metric | Type | Unit | Alert Threshold |
|--------|------|------|-----------------|
| `planner_planning_time_ms` | Histogram | ms | p99 > 80 |
| `planner_trajectory_jerk_max` | Gauge | m/s³ | > 2.0 |
| `planner_collision_check_count` | Counter | count | — |
| `planner_mpc_iterations` | Histogram | count | p95 > 60 |
| `planner_map_tile_cache_hit_rate` | Gauge | ratio | < 0.9 |
| `planner_obstacle_age_p99` | Gauge | ms | > 500 |
| `planner_replan_frequency_hz` | Gauge | Hz | < 15 |
| `planner_feasibility_violation_count` | Counter | count | > 0 |

### Prometheus Scrape Config

```yaml
scrape_configs:
  - job_name: 'path_planner'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: /metrics
    scrape_interval: 1s  # High-frequency for real-time monitoring
```

### Grafana Dashboard Panels

- **Planning Latency**: Time-series of p50/p95/p99 planning time
- **Trajectory Quality**: Overlay of jerk, lateral acceleration, curvature profiles
- **Obstacle Map**: 2D scatter plot of detected obstacles with predicted trajectories
- **Cost Breakdown**: Stacked bar chart of individual cost components per planning cycle
- **Map Cache Performance**: Hit rate and miss rate over time

### Distributed Tracing

```
TRACE_ID: 7f3a2b1c-...
├── route_planner.find_route          [12 ms]
│   ├── map_tile_fetch                [5 ms]
│   ├── lane_graph_construction       [4 ms]
│   └── a_star_search                 [3 ms]
├── behavior_planner.decide           [2 ms]
│   ├── traffic_light_query           [0.5 ms]
│   └── state_machine_transition      [1.5 ms]
└── motion_planner.plan               [35 ms]
    ├── lattice_expand                [15 ms]
    ├── collision_check               [10 ms]
    ├── cost_evaluate                 [5 ms]
    └── trajectory_smooth             [2 ms] (parallel)
```

## Testing Strategy

### Unit Tests

- **Cost function correctness**: Verify each cost term evaluates correctly for known states (e.g., centered vehicle → zero lateral cost).
- **Frenet-Cartesian conversion**: Round-trip conversion accuracy < 1 mm error.
- **Collision checker**: Known geometric configurations (touching, overlapping, separated) with expected boolean results.
- **Polynomial generator**: Verify quintic polynomial boundary conditions (position, velocity, acceleration at start/end).

### Integration Tests

- **End-to-end planning**: Feed recorded perception + localization data into planner; verify output trajectory is collision-free and within kinematic limits.
- **Map service failure**: Simulate map service timeout; verify planner falls back to last-known lane graph.
- **High obstacle density**: 200+ obstacles; verify planning latency stays under 100 ms.

### Simulation Tests

- **CARLA / LGSVL scenarios**: 50+ traffic scenarios (lane change, cut-in, pedestrian crossing, emergency vehicle) with automated pass/fail criteria.
- **Adversarial scenarios**: Malformed obstacle messages, GPS spoofing, map tile corruption.
- **Stress test**: 1000 consecutive planning cycles with varying obstacle counts (10–500) to detect memory leaks and latency drift.

### Continuous Integration

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Lint &  │───▶│  Unit    │───▶│ Integr.  │───▶│  Sim     │
│  Type    │    │  Tests   │    │  Tests   │    │  Tests   │
│  Check   │    │  (< 5m)  │    │  (< 15m) │    │  (< 30m) │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

## Versioning and Migration

### Semantic Versioning

- **MAJOR**: Breaking changes to API, message formats, or behavior semantics.
- **MINOR**: New planner algorithms, new cost functions, backward-compatible.
- **PATCH**: Bug fixes, parameter tuning, performance improvements.

### Migration Guide (v1.x → v2.0)

1. Update `PathPlan` protobuf to v2 schema (add `estimated_distance_m` field).
2. Replace deprecated `ReactivePlanner` class with `LatticePlanner`.
3. Update launch files to include `planner.launch.py` instead of single-node `planner_node`.
4. Migrate parameter keys from `planner/max_speed` to `planner/local/target_speed_mps`.
5. Re-run integration test suite to verify behavioral equivalence.

### Deprecation Policy

Deprecated features emit a warning for two minor versions before removal. Warnings include the version where deprecation started and the version where removal will occur.

## Glossary

| Term | Definition |
|------|-----------|
| **A*** | Optimal graph-search algorithm using heuristic cost estimation |
| **Frenet Frame** | Coordinate system aligned with the reference path (s = longitudinal, d = lateral) |
| **Hybrid A*** | A* variant operating in continuous state space with kinematic constraints |
| **Lattice Planner** | State-space discretization planner using precomputed motion primitives |
| **MPC** | Model Predictive Control — optimization-based controller using a vehicle dynamics model |
| **RRT*** | Rapidly-exploring Random Tree with asymptotic optimality guarantee |
| **Quintic Polynomial** | 5th-order polynomial used for smooth trajectory generation with boundary constraints |
| **Kinematic Bicycle Model** | Two-wheel vehicle model relating steering angle to path curvature |
| **Slip Angle (β)** | Angle between vehicle heading and velocity vector |
| **Warm Start** | Initializing an optimization solver with a previous solution to reduce iterations |
| **Spatial Hashing** | Grid-based spatial index for fast proximity queries |
| **Obstacle Inflation** | Expanding obstacle boundaries by vehicle radius for circle-approximation collision checking |
| **Cost Map** | Rasterized grid where each cell encodes traversal cost |
| **Lane Graph** | Graph representation of drivable lanes with connectivity and metadata |
| **BEV** | Bird's-Eye View — top-down perspective used for planning and perception fusion |
| **OTA** | Over-The-Air — remote software and map update delivery |

## Changelog

### v2.0.0 (2025-06-15)

- Added lattice planner with multi-layer state-space expansion
- Added MPC planner with IPOPT/CasADi backend
- Introduced Frenet frame coordinate system for local planning
- Added distributed tracing support
- Added Kubernetes deployment manifests
- New cost function framework with configurable weights

### v1.2.0 (2025-01-20)

- Added RRT* planner for unstructured environments
- Improved A* performance with octile heuristic
- Added map tile pre-fetching for long routes
- Fixed memory leak in obstacle ring buffer

### v1.1.0 (2024-09-10)

- Added behavior planner integration (FSM-based)
- Added traffic light compliance layer
- Added following-distance constraint

### v1.0.0 (2024-05-01)

- Initial release with A* route planner and basic motion planner
- Support for HD map tile loading from local cache

## Contributing Guidelines

### Development Workflow

1. Fork the repository and create a feature branch from `main`.
2. Implement changes with corresponding unit tests (minimum 80% coverage for new code).
3. Run the full CI pipeline locally: `make test-ci`.
4. Submit a pull request with a description of changes and any migration notes.
5. Request review from at least two maintainers.

### Code Standards

- Python: Follow PEP 8; use `ruff` for linting, `mypy` for type checking.
- C++: Follow Google C++ Style Guide; use `clang-tidy` and `clang-format`.
- All planner algorithms must have a companion paper citation in docstrings.
- Performance-critical paths must include benchmark results in PR description.

### Commit Convention

Use Conventional Commits: `feat(planner): add RRT* for unstructured environments`

### Review Checklist

- [ ] Planner output is collision-free (verified by integration test).
- [ ] Planning latency meets budget (< 100 ms).
- [ ] All cost function weights are configurable via parameter server.
- [ ] Debug output includes sufficient information for post-hoc analysis.
- [ ] No hardcoded constants — all magic numbers extracted to configuration.

## License

Apache License, Version 2.0. See the repository root `LICENSE` file for full text.

Copyright 2024-2025 Awesome Grok Skills Contributors.
