---
name: "path-planning"
category: "autonomous-transport"
version: "2.0.0"
tags: ["autonomous-transport", "path-planning", "motion-planning", "trajectory-optimization", "A*", "RRT", "MPC", "lattice-planner"]
---

# Path Planning for Autonomous Vehicles

## Overview

This module provides a comprehensive path-planning framework for autonomous vehicles, covering graph-based search (A*, Dijkstra), sampling-based methods (RRT, RRT*), optimization-based planners (MPC, sequential quadratic programming), lattice-based state-space discretization, and trajectory optimization. It integrates with HD-map providers, localization stacks, and vehicle dynamics models to produce dynamically feasible, collision-free trajectories at planning frequencies up to 100 Hz.

The planner operates across three hierarchical layers â€” route planning (global), behavior planning (tactical), and motion planning (local) â€” each producing outputs consumed by downstream layers. It supports both on-road structured environments and unstructured off-road scenarios, with real-time replanning capabilities for dynamic obstacle avoidance.

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
| Kinematic Bicycle | 4 (x, y, Ïˆ, v) | Low-speed maneuvering | Low |
| Dynamic Bicycle | 6 (+ Î², Î´) | Highway and general driving | Medium |
| Single Track + Roll | 7 (+ Ï†) | High-speed curves | Medium-High |
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
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    ROUTE PLANNER                         â”‚
â”‚  (HD Map + A*)                                          â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚ Map Tiles â”‚â”€â”€â”€â–¶â”‚ Lane Graphâ”‚â”€â”€â”€â–¶â”‚ Route Candidatesâ”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚                                           â”‚             â”‚
â”‚                                    Best Route (JSON)    â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                BEHAVIOR PLANNER           â”‚             â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚  Finite State Machine / Decision Tree            â”‚  â”‚
â”‚  â”‚                                                   â”‚  â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚  â”‚
â”‚  â”‚  â”‚ Lane    â”‚  â”‚ Lane     â”‚  â”‚ Intersection   â”‚  â”‚  â”‚
â”‚  â”‚  â”‚ Follow  â”‚  â”‚ Change   â”‚  â”‚ Navigation     â”‚  â”‚  â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚  â”‚
â”‚  â”‚       â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜           â”‚  â”‚
â”‚  â”‚              Behavior Command (JSON)              â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚            MOTION PLANNER     â”‚                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚  Lattice / Hybrid A* / MPC                        â”‚ â”‚
â”‚  â”‚                                                    â”‚ â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚ â”‚
â”‚  â”‚  â”‚ State      â”‚  â”‚ Obstacle â”‚  â”‚ Cost Function â”‚  â”‚ â”‚
â”‚  â”‚  â”‚ Sampler    â”‚â”€â”€â”‚ Checker  â”‚â”€â”€â”‚ Evaluator     â”‚  â”‚ â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚ â”‚
â”‚  â”‚                                        â”‚          â”‚ â”‚
â”‚  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”          â”‚          â”‚ â”‚
â”‚  â”‚  â”‚ Trajectory â”‚â—€â”€â”‚ Optimal  â”‚â—€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜          â”‚ â”‚
â”‚  â”‚  â”‚ Publisher  â”‚  â”‚ Selector â”‚                     â”‚ â”‚
â”‚  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                     â”‚ â”‚
â”‚  â”‚          Trajectory (30 Hz waypoints)             â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚              CONTROLLER (Downstream)                     â”‚
â”‚  Longitudinal PID + Lateral Stanley / Pure Pursuit      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Lattice Planner State-Space Expansion

```
          Frenet Frame (s, d)
     s (along reference path)
     â–²
     â”‚    â”Œâ”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”
     â”‚    â”‚ State â”‚ â”‚ State â”‚ â”‚ State â”‚  Terminal States
     â”‚    â”‚ (s,d, â”‚ â”‚ (s,d, â”‚ â”‚ (s,d, â”‚
     â”‚    â”‚  v,a) â”‚ â”‚  v,a) â”‚ â”‚  v,a) â”‚
     â”‚    â””â”€â”€â”€â”¬â”€â”€â”€â”˜ â””â”€â”€â”€â”¬â”€â”€â”€â”˜ â””â”€â”€â”€â”¬â”€â”€â”€â”˜
     â”‚        â”‚         â”‚         â”‚
     â”‚    â”Œâ”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”
     â”‚    â”‚     Polynomial Generator  â”‚  Quintic/Quartic
     â”‚    â”‚     (lateral: 5th order)  â”‚  polynomials
     â”‚    â”‚     (longitudinal: 4th)   â”‚
     â”‚    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â”‚                â”‚
     â”‚    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
     â”‚    â”‚    Collision Checker      â”‚  Swept-volume test
     â”‚    â”‚    (OBB / circle approx)  â”‚  against obstacles
     â”‚    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â”‚                â”‚
     â”‚    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
     â”‚    â”‚    Cost Function          â”‚  J = w_jÂ·jerk + w_lÂ·lat
     â”‚    â”‚                           â”‚     + w_sÂ·speed + w_tÂ·time
     â”‚    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â”‚                â–¼
     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¶ d (lateral offset)
```

### MPC Prediction Horizon Visualization

```
 Current      Planning Horizon (5.0 s)
 State t=0  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¶
   â”‚
   â”‚  â—â”â”â”â”â”â”â”â”â—â”â”â”â”â”â”â”â”â—â”â”â”â”â”â”â”â”â—â”â”â”â”â”â”â”â”â—  Planned trajectory
   â”‚  â”‚        â”‚        â”‚        â”‚        â”‚
   â”‚  0.0s    1.0s    2.0s    3.0s    4.0s    5.0s
   â”‚
   â”‚  â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“  Obstacle predictions
   â”‚  â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’â–’  (position uncertainty
   â”‚  â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘â–‘   grows over time)
   â”‚
   â”‚  â—€â”€ Control Horizon (1.0 s) â”€â–¶
   â”‚  u0  u1  u2  u3  u4  u5  u6  u7  u8  u9
   â”‚
   â”‚  Controls applied: u0 only; re-solve at next tick
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
// PathPlan â€” route-level output
message PathPlan {
  Header header
  repeated LaneSegment route_segments = 1;
  geometry_msgs/PoseStamped goal_pose = 2;
  float64 estimated_duration_s = 3;
  float64 estimated_distance_m = 4;
}

// Trajectory â€” motion-level output
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
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚              Shared Memory Region                â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚ Map Cache â”‚  â”‚ Obstacle  â”‚  â”‚ Trajectory  â”‚ â”‚
â”‚  â”‚ (256 MB)  â”‚  â”‚ Ring Buf  â”‚  â”‚ Ring Buffer â”‚ â”‚
â”‚  â”‚           â”‚  â”‚ (16 MB)   â”‚  â”‚ (4 MB)      â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚  Parameter Server (lock-free read)        â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
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

- All incoming obstacle messages are validated for finite values, reasonable bounding-box dimensions (0.1â€“10 m), and monotonic timestamps.
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
- Emergency braking (deceleration up to 8 m/sÂ²) is always possible regardless of planner state.
- A watchdog timer monitors planner output frequency; if no trajectory is published within 200 ms, the controller triggers autonomous emergency braking (AEB).

## Troubleshooting Guide

| Symptom | Probable Cause | Diagnostic Steps | Resolution |
|---------|---------------|------------------|------------|
| Planner outputs empty trajectory | No lane-graph data received | Check `/map/get_lane_graph` service availability; verify map tile cache hit rate in logs | Ensure map server is running; increase `map_tile_cache_size_mb` |
| Trajectory has high jerk (> 2 m/sÂ³) | Insufficient smoothing iterations | Check `planner.local.smoothing_iterations` parameter; inspect cost weights | Increase smoothing iterations to 5; raise `weight_jerk` cost |
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
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚            PlannerState                      â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚ vehicle_state â”‚  â”‚ environment_state  â”‚  â”‚
â”‚  â”‚  x, y, yaw, vâ”‚  â”‚  obstacles: []     â”‚  â”‚
â”‚  â”‚  steer, accel â”‚  â”‚  lane_graph: Graph â”‚  â”‚
â”‚  â”‚  slip_angle   â”‚  â”‚  traffic_lights:[] â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚ route_state   â”‚  â”‚ behavior_state     â”‚  â”‚
â”‚  â”‚  current_lane â”‚  â”‚  fsm_state: Enum   â”‚  â”‚
â”‚  â”‚  goal_pose    â”‚  â”‚  lane_change_dir:  â”‚  â”‚
â”‚  â”‚  distance_to_ â”‚  â”‚    0 (none), Â±1    â”‚  â”‚
â”‚  â”‚    goal       â”‚  â”‚  yield_active: boolâ”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Frenet Frame Coordinate System

The planner operates in Frenet coordinates (s, d) relative to the reference lane centerline:
- **s**: Arc-length along the reference path (longitudinal)
- **d**: Signed lateral offset from the reference path center
- **á¹¡ (s_dot)**: Longitudinal speed along the reference path
- **á¸‹ (d_dot)**: Lateral speed relative to the reference path

Frenet-to-Cartesian conversion uses the reference path's curvature Îº(s):

```
x = X(s) - d Â· sin(Î¸(s))
y = Y(s) + d Â· cos(Î¸(s))
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
  confidence: float  # 0.0â€“1.0
  age_s: float       # time since first detection
  tracker_id: uint32 # consistent across frames
```

### Cost Function Structure

```
J_total = w_jerk  Â· J_jerk
        + w_lat   Â· J_lateral_offset
        + w_speed Â· J_speed_deviation
        + w_time  Â· J_time_to_goal
        + w_comfort Â· J_lateral_acceleration
        + w_safety Â· J_proximity_to_obstacles
        + w_rule  Â· J_traffic_rule_violation

Where:
  J_jerk           = âˆ« (dÂ³d/dtÂ³)Â² dt       (minimize jerk)
  J_lateral_offset = âˆ« dÂ² dt               (stay centered in lane)
  J_speed_dev      = âˆ« (v - v_target)Â² dt  (maintain target speed)
  J_time_to_goal   = T_total               (minimize travel time)
  J_lateral_accel  = âˆ« (vÂ² Â· Îº)Â² dt        (comfort constraint)
  J_proximity      = Î£ (1 / distance_to_obs)Â²  (safety penalty)
  J_traffic_rule   = Î£ indicator(rule_violated)  (hard penalty)
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
| `planner_trajectory_jerk_max` | Gauge | m/sÂ³ | > 2.0 |
| `planner_collision_check_count` | Counter | count | â€” |
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
â”œâ”€â”€ route_planner.find_route          [12 ms]
â”‚   â”œâ”€â”€ map_tile_fetch                [5 ms]
â”‚   â”œâ”€â”€ lane_graph_construction       [4 ms]
â”‚   â””â”€â”€ a_star_search                 [3 ms]
â”œâ”€â”€ behavior_planner.decide           [2 ms]
â”‚   â”œâ”€â”€ traffic_light_query           [0.5 ms]
â”‚   â””â”€â”€ state_machine_transition      [1.5 ms]
â””â”€â”€ motion_planner.plan               [35 ms]
    â”œâ”€â”€ lattice_expand                [15 ms]
    â”œâ”€â”€ collision_check               [10 ms]
    â”œâ”€â”€ cost_evaluate                 [5 ms]
    â””â”€â”€ trajectory_smooth             [2 ms] (parallel)
```

## Testing Strategy

### Unit Tests

- **Cost function correctness**: Verify each cost term evaluates correctly for known states (e.g., centered vehicle â†’ zero lateral cost).
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
- **Stress test**: 1000 consecutive planning cycles with varying obstacle counts (10â€“500) to detect memory leaks and latency drift.

### Continuous Integration

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Lint &  â”‚â”€â”€â”€â–¶â”‚  Unit    â”‚â”€â”€â”€â–¶â”‚ Integr.  â”‚â”€â”€â”€â–¶â”‚  Sim     â”‚
â”‚  Type    â”‚    â”‚  Tests   â”‚    â”‚  Tests   â”‚    â”‚  Tests   â”‚
â”‚  Check   â”‚    â”‚  (< 5m)  â”‚    â”‚  (< 15m) â”‚    â”‚  (< 30m) â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Versioning and Migration

### Semantic Versioning

- **MAJOR**: Breaking changes to API, message formats, or behavior semantics.
- **MINOR**: New planner algorithms, new cost functions, backward-compatible.
- **PATCH**: Bug fixes, parameter tuning, performance improvements.

### Migration Guide (v1.x â†’ v2.0)

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
| **MPC** | Model Predictive Control â€” optimization-based controller using a vehicle dynamics model |
| **RRT*** | Rapidly-exploring Random Tree with asymptotic optimality guarantee |
| **Quintic Polynomial** | 5th-order polynomial used for smooth trajectory generation with boundary constraints |
| **Kinematic Bicycle Model** | Two-wheel vehicle model relating steering angle to path curvature |
| **Slip Angle (Î²)** | Angle between vehicle heading and velocity vector |
| **Warm Start** | Initializing an optimization solver with a previous solution to reduce iterations |
| **Spatial Hashing** | Grid-based spatial index for fast proximity queries |
| **Obstacle Inflation** | Expanding obstacle boundaries by vehicle radius for circle-approximation collision checking |
| **Cost Map** | Rasterized grid where each cell encodes traversal cost |
| **Lane Graph** | Graph representation of drivable lanes with connectivity and metadata |
| **BEV** | Bird's-Eye View â€” top-down perspective used for planning and perception fusion |
| **OTA** | Over-The-Air â€” remote software and map update delivery |

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
- [ ] No hardcoded constants â€” all magic numbers extracted to configuration.

## License

Apache License, Version 2.0. See the repository root `LICENSE` file for full text.

Copyright 2024-2025 Awesome Grok Skills Contributors.


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
