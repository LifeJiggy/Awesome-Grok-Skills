---
name: "navigation"
category: "robotics"
version: "2.0.0"
tags: ["robotics", "navigation", "slam", "path-planning", "localization", "trajectory-tracking", "costmap", "odometry"]
---

# Navigation

## Overview

The Navigation module provides the algorithms and infrastructure for robot localization, mapping, path planning, and trajectory tracking. It covers Simultaneous Localization and Mapping (SLAM) with LiDAR and visual sensors, probabilistic localization with particle filters and Kalman filters, global and local path planning, trajectory following with pure pursuit and Stanley controllers, and odometry fusion from multiple sensor sources.

Navigation is the foundation of mobile robotics — the ability to know where you are, build a map of the world, plan a path to a goal, and follow that path accurately. This module provides production-grade algorithms for indoor and outdoor mobile robots, autonomous vehicles, and UAVs. It supports both structured environments (warehouses, factories) and unstructured environments (agricultural fields, disaster zones).

The module is designed as a layered system: localization provides the pose estimate, mapping builds the environment representation, global planning finds a rough path, local planning avoids obstacles in real-time, and trajectory tracking converts the path into motor commands. Each layer can operate independently and has its own update rate, allowing the system to balance accuracy, responsiveness, and computational cost. The layers communicate through shared data structures (costmaps, path lists) that are updated atomically to prevent race conditions.

## Core Capabilities

- **SLAM** — LiDAR-based and visual SLAM with loop closure detection. Supports both scan-matching (ICP, NDT) and feature-based approaches with pose graph optimization.
- **Localization** — Monte Carlo localization (particle filter), Extended Kalman Filter (EKF) localization, and histogram filter localization. Handles global localization and kidnapped robot problems.
- **Occupancy Grid Mapping** — Bayesian occupancy grid updates from LiDAR, sonar, and depth cameras. Supports multi-resolution maps and incremental updates.
- **Global Path Planning** — A*, Dijkstra, and RRT (Rapidly-exploring Random Trees) with kinodynamic extensions. Includes heuristic functions optimized for grid and continuous spaces.
- **Local Path Planning** — Dynamic Window Approach (DWA), Timed Elastic Band (TEB), and Model Predictive Control (MPC). Handles dynamic obstacles and velocity constraints.
- **Trajectory Tracking** — Pure pursuit controller, Stanley controller, and PID tracking. Supports both differential-drive and Ackermann-steered vehicles.
- **Odometry Fusion** — IMU + wheel odometry fusion with EKF. Supports visual odometry, GPS, and LiDAR odometry as additional sources.
- **Costmap Management** — Layered costmaps with static, obstacle, inflation, and custom layers. Configurable resolution, update rate, and propagation.
- **Waypoint Navigation** — Follow waypoint missions with heading and speed constraints. Supports curved paths, spline interpolation, and speed profiling.
- **Recovery Behaviors** — Auto-generated recovery behaviors for localization failure, obstacle recovery, and emergency stops. Configurable behavior trees for complex recovery sequences.

## Usage Examples

### SLAM Map Building

```python
from navigation import SLAMEngine, LidarScan, SLAMConfig

slam = SLAMEngine(config=SLAMConfig(
    map_resolution=0.05,
    map_size_cells=(400, 400),
    loop_closure_enabled=True,
    max_particles=50,
))

for scan in lidar_stream:
    pose = slam.process_scan(scan)
    if scan.loop_closure_detected:
        print(f"Loop closed at pose {pose}")
    if scan.step_count % 100 == 0:
        print(f"Current pose: {pose}")
```

### Particle Filter Localization

```python
from navigation import ParticleFilter, Map, SensorModel

pf = ParticleFilter(
    num_particles=1000,
    map_data=occupancy_map,
    sensor_model=SensorModel(lidar_range=12.0, sigma=0.2),
)

for odom, lidar in sensor_stream:
    estimated_pose = pf.update(odom, lidar)
    print(f"Localized: {estimated_pose}")
```

### A* Path Planning

```python
from navigation import AStarPlanner, Costmap

planner = AStarPlanner(costmap=costmap, inflation_radius=0.3)
path = planner.plan(
    start=(1.0, 2.0),
    goal=(15.0, 18.0),
    heuristic="euclidean",
)
print(f"Path: {len(path)} waypoints")
```

### Pure Pursuit Controller

```python
from navigation import PurePursuitController, Pose2D

controller = PurePursuitController(
    lookahead_distance=0.8,
    max_linear_velocity=1.0,
    max_angular_velocity=2.0,
)

for pose in pose_stream:
    cmd = controller.track(path, pose)
    print(f"Command: linear={cmd.linear:.2f}, angular={cmd.angular:.2f}")
```

### EKF Odometry Fusion

```python
from navigation import EKFFusion, IMUData, WheelOdometry

fusion = EKFFusion()
for imu, odom in sensor_stream:
    fused_pose = fusion.update(imu, odom)
    print(f"Fused pose: {fused_pose}")
```

### Dynamic Window Approach

```python
from navigation import DWAPlanner, Velocity, DynamicObstacle

dwa = DWAPlanner(
    max_speed=1.5,
    max_accel=2.0,
    max_yaw_rate=3.0,
    dt=0.1,
    heading_weight=0.15,
    clearance_weight=0.1,
    velocity_weight=0.1,
)

current = Velocity(linear=0.5, angular=0.0)
obstacles = [DynamicObstacle(x=3.0, y=1.0, vx=0.0, vy=0.0, radius=0.3)]
best_cmd = dwa.plan(current, goal, obstacles, path)
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Waypoint Navigator                      │
│  (mission waypoints, heading constraints, speed profile) │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Global Planner                          │
│  (A*, Dijkstra, RRT on costmap)                         │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Local Planner                           │
│  (DWA, TEB, MPC — avoids dynamic obstacles)             │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Trajectory Tracker                          │
│  (pure pursuit, Stanley, PID → motor commands)          │
└──────────────────────┬──────────────────────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
┌───▼──────────┐ ┌────▼───────────┐ ┌────▼───────────┐
│ Localization │ │   Costmap      │ │  Odometry      │
│ (particle    │ │ (static,       │ │  Fusion        │
│  filter, EKF)│ │  obstacle,     │ │  (IMU + wheel) │
│              │ │  inflation)    │ │                │
└──────────────┘ └────────────────┘ └────────────────┘
    ▲                  ▲                  ▲
    │                  │                  │
 LiDAR/Visual      LiDAR/SONAR       IMU/Wheel/GPS
```

The localization module provides the pose estimate used by all other layers. The costmap integrates sensor data into a unified obstacle representation. The global planner finds a path on the costmap, and the local planner refines it to avoid dynamic obstacles. The trajectory tracker converts the planned path into velocity commands. Each layer runs at its own frequency: localization at 10-50 Hz, costmap at 5-10 Hz, global planner on-demand, local planner at 5-10 Hz, and tracker at 50-100 Hz.

## Best Practices

1. **Tune your costmap inflation radius carefully.** Too small and the robot clips obstacles; too large and it cannot navigate narrow passages. The inflation radius should match the robot's inscribed radius plus a safety margin. Test in your actual environment.
2. **Use multi-resolution maps.** Coarse maps for global planning, fine maps for local planning. This dramatically reduces planning time without sacrificing local accuracy. A 5 cm local map and 20 cm global map is a good starting point.
3. **Enable loop closure in SLAM.** Without loop closure, SLAM maps drift indefinitely. Loop closure corrects accumulated drift by recognizing previously visited locations. Use visual features or scan matching for loop detection.
4. **Fuse multiple odometry sources.** Wheel odometry alone drifts. IMU alone drifts. Fuse them with an EKF for robust pose estimation. Add visual odometry or GPS when available. Weight each source by its reliability.
5. **Set appropriate particle counts for localization.** Too few particles and the filter diverges; too many wastes computation. 500-1000 particles work for most indoor environments. Use KLD-sampling for adaptive particle count in large spaces.
6. **Recovery behaviors are essential.** Plan for localization failure, costmap clear-out, and emergency stops. A robot that gets stuck without a recovery behavior is a failed deployment. Use behavior trees for complex recovery sequences.
7. **Validate paths before execution.** Always check that a planned path does not intersect with dynamic obstacles that appeared after planning. Replan at a rate faster than obstacle dynamics. Use the local planner to handle real-time obstacles.
8. **Use trajectory smoothing.** Raw A* paths are jagged. Apply B-spline or Dubins path smoothing to produce drivable trajectories that respect the robot's kinematic constraints. Smoothed paths reduce wear and improve tracking accuracy.
9. **Profile localization accuracy regularly.** Compare localization estimates against ground truth (AprilTag markers, GPS, motion capture) periodically. Drift rates of 1-2% are typical; anything worse indicates sensor or tuning issues.
10. **Design for outdoor conditions.** Outdoor navigation requires handling rain, snow, glare, and uneven terrain. Use weather-resistant sensors and tune algorithms for high dynamic range. Add GPS and IMU for outdoor robustness.

## Performance Considerations

- **SLAM computation**: ICP scan matching takes 5-20 ms per scan on modern hardware. Loop closure detection with BoW (Bag of Words) takes 10-50 ms. Keep the pose graph small by pruning old nodes.
- **Particle filter scaling**: 1000 particles with 360-ray sensor model takes 5-10 ms per update. Use range-limited rays and adaptive particle count to reduce cost. GPU acceleration can speed this 10x.
- **A* planning time**: A* on a 400x400 grid takes 1-5 ms. On a 1000x1000 grid, it can take 50-200 ms. Use hierarchical planning or jump-point search for large grids.
- **DWA computation**: DWA evaluates ~1000 velocity samples in 1-5 ms. TEB takes 10-50 ms but produces smoother trajectories. Use DWA for fast reaction, TEB for smoother paths.
- **Costmap update rate**: Update the obstacle layer at sensor rate (10-50 Hz). The inflation layer recomputes in 10-100 ms depending on resolution. Cache the inflation layer and only recompute when obstacles change.
- **Memory usage**: A 1000x1000 occupancy grid at 5 cm resolution uses 1 MB. Multiple layers (static, obstacle, inflation) multiply this. Use signed byte arrays and compression for memory-constrained platforms.

## Security Considerations

- **Map integrity**: Occupancy maps used for navigation can be tampered with. Verify map checksums before loading and detect unauthorized modifications. A malicious map can direct the robot into unsafe areas.
- **Sensor spoofing defense**: LiDAR and GPS spoofing can cause navigation failures. Cross-validate sensor inputs and detect anomalies. Use redundant sensors and trust voting for critical measurements.
- **Localization attack detection**: An adversary can manipulate odometry to cause localization drift. Monitor for sudden pose jumps and cross-check with independent sensors. Implement anomaly detection on pose estimates.
- **Path injection prevention**: Ensure planned paths come from the authenticated planner, not external sources. Validate path waypoints against the costmap before execution.
- **Secure waypoint storage**: Waypoint missions may contain sensitive locations. Encrypt stored missions and implement access controls. Verify mission integrity before execution.
- **Communication security**: For multi-robot SLAM, secure the inter-robot communication channel. An adversary could inject false scan data to corrupt the shared map.

## Related Modules

- **autonomous-systems** — Mission planning and fault recovery above the navigation layer
- **robotics-vision** — Visual SLAM and visual odometry for camera-based navigation
- **manipulation** — Mobile manipulation requiring coordinated base and arm motion
- **swarm-robotics** — Multi-robot SLAM and formation navigation

## References

- Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press.
- Siegwart, R., Nourbakhsh, I. R., & Scaramuzza, D. (2011). *Introduction to Autonomous Mobile Robots*. MIT Press.
- LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press.
- Fox, D., Burgard, W., & Thrun, S. (1997). The dynamic window approach to collision avoidance. *IEEE Robotics & Automation Magazine*, 4(1), 23-33.
- Kavraki, L. E. et al. (1996). Probabilistic roadmaps for path planning in high-dimensional configuration spaces. *IEEE Trans. RA*, 12(4), 566-580.
- Montemerlo, M. et al. (2002). FastSLAM: A factored solution to the simultaneous localization and mapping problem. *AAAI*.
- ROS 2 Navigation2 Documentation: https://docs.ros.org/en/humble/Tutorials/Navigation.html
- Navigation2 GitHub Repository: https://github.com/ros-navigation/navigation2
- Autoware Foundation: https://autoware.org/
