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

## Path Planning Algorithms Deep Dive

### A* Algorithm — Implementation Details

A* combines the advantages of Dijkstra's algorithm (guaranteed optimality) and greedy best-first search (heuristic guidance). The evaluation function is f(n) = g(n) + h(n).

```python
import heapq
from navigation import Costmap, GridCell

def a_star_search(costmap, start, goal, heuristic="euclidean"):
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic_fn(start, goal, heuristic)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            return reconstruct_path(came_from, current)
        
        for neighbor, cost in costmap.get_neighbors(current):
            tentative_g = g_score[current] + cost
            
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic_fn(neighbor, goal, heuristic)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None  # no path found

def heuristic_fn(a, b, method="euclidean"):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    if method == "euclidean":
        return (dx**2 + dy**2) ** 0.5
    elif method == "manhattan":
        return dx + dy
    elif method == "octile":
        return max(dx, dy) + (2**0.5 - 1) * min(dx, dy)
    elif method == "chebyshev":
        return max(dx, dy)
```

### RRT and RRT* — Rapidly-exploring Random Trees

RRT grows a tree by randomly sampling the configuration space and extending toward random samples. RRT* adds rewiring for asymptotic optimality.

```python
import numpy as np
from navigation import OccupancyGrid, RRTConfig

class RRTPlanner:
    def __init__(self, config):
        self.config = config
        self.tree = None
        self.max_iterations = config.max_iterations
        self.step_size = config.step_size
        self.goal_threshold = config.goal_threshold
        self.goal_bias = config.goal_bias
    
    def plan(self, start, goal, obstacle_map):
        tree = [start]
        parent = {start: None}
        
        for i in range(self.max_iterations):
            # Sample with goal bias
            if np.random.random() < self.goal_bias:
                sample = goal
            else:
                sample = self.random_sample(obstacle_map)
            
            nearest = self.find_nearest(tree, sample)
            new_node = self.steer(nearest, sample, self.step_size)
            
            if new_node and not self.collision(nearest, new_node, obstacle_map):
                tree.append(new_node)
                parent[new_node] = nearest
                
                if self.distance(new_node, goal) < self.goal_threshold:
                    return self.extract_path(parent, new_node)
        
        return None  # no path found
    
    def steer(self, from_node, to_node, step_size):
        direction = np.array(to_node) - np.array(from_node)
        dist = np.linalg.norm(direction)
        if dist < 1e-6:
            return None
        direction = direction / dist
        new_pos = np.array(from_node) + direction * min(step_size, dist)
        return tuple(new_pos)

class RRTStarPlanner(RRTPlanner):
    def __init__(self, config):
        super().__init__(config)
        self.rewire_radius = config.rewire_radius
    
    def rewire(self, tree, new_node, parent):
        neighbors = self.find_neighbors(tree, new_node, self.rewire_radius)
        
        # Find best parent
        best_parent = parent[new_node]
        best_cost = self.cost(parent[new_node]) + self.distance(parent[new_node], new_node)
        
        for neighbor in neighbors:
            candidate_cost = self.cost(neighbor) + self.distance(neighbor, new_node)
            if candidate_cost < best_cost and not self.collision(neighbor, new_node):
                best_parent = neighbor
                best_cost = candidate_cost
        
        parent[new_node] = best_parent
        
        # Rewire neighbors through new_node
        for neighbor in neighbors:
            new_cost = self.cost(new_node) + self.distance(new_node, neighbor)
            if new_cost < self.cost(neighbor):
                if not self.collision(new_node, neighbor):
                    parent[neighbor] = new_node
```

### PRM — Probabilistic Roadmap

PRM builds a roadmap of collision-free configurations by random sampling and local connection. It is multi-query: the roadmap is built once and reused for many queries.

```python
class PRMPlanner:
    def __init__(self, config):
        self.num_samples = config.num_samples
        self.k_neighbors = config.k_neighbors
        self.connection_distance = config.connection_distance
    
    def build_roadmap(self, obstacle_map, bounds):
        samples = []
        for _ in range(self.num_samples):
            sample = self.sample_free_space(obstacle_map, bounds)
            if sample:
                samples.append(sample)
        
        # Build graph with k-nearest neighbor connections
        graph = {s: [] for s in samples}
        for s in samples:
            neighbors = self.k_nearest(samples, s, self.k_neighbors)
            for neighbor in neighbors:
                if (self.distance(s, neighbor) < self.connection_distance and
                    not self.collision(s, neighbor, obstacle_map)):
                    cost = self.distance(s, neighbor)
                    graph[s].append((neighbor, cost))
                    graph[neighbor].append((s, cost))
        
        return graph
    
    def query(self, roadmap, start, goal, obstacle_map):
        # Connect start and goal to roadmap
        roadmap[start] = []
        roadmap[goal] = []
        
        for node in list(roadmap.keys()):
            if node in (start, goal):
                continue
            if (self.distance(start, node) < self.connection_distance and
                not self.collision(start, node, obstacle_map)):
                roadmap[start].append((node, self.distance(start, node)))
                roadmap[node].append((start, self.distance(start, node)))
            if (self.distance(goal, node) < self.connection_distance and
                not self.collision(goal, node, obstacle_map)):
                roadmap[goal].append((node, self.distance(goal, node)))
                roadmap[node].append((goal, self.distance(goal, node)))
        
        # A* on roadmap
        return a_star_on_graph(roadmap, start, goal)
```

### Kinodynamic Planning with RRT

For nonholonomic vehicles (car-like robots), kinodynamic RRT considers differential constraints during tree extension.

```python
class KinodynamicRRT:
    def __init__(self, config):
        self.step_size = config.step_size
        self.num_controls = config.num_control_samples
        self.dt = config.integration_timestep
    
    def extend(self, state, target, obstacle_map):
        best_state = state
        best_dist = float('inf')
        
        for _ in range(self.num_controls):
            # Sample control (linear velocity, steering angle)
            v = np.random.uniform(0, self.max_speed)
            phi = np.random.uniform(-self.max_steer, self.max_steer)
            
            # Forward simulate
            new_state = self.integrate(state, v, phi, self.step_size)
            
            if not self.collision(state, new_state, obstacle_map):
                dist = self.distance(new_state, target)
                if dist < best_dist:
                    best_dist = dist
                    best_state = new_state
        
        return best_state
    
    def integrate(self, state, v, phi, dt):
        x, y, theta = state
        L = self.wheelbase
        
        # Bicycle model integration
        dx = v * np.cos(theta) * dt
        dy = v * np.sin(theta) * dt
        dtheta = (v / L) * np.tan(phi) * dt
        
        return (x + dx, y + dy, theta + dtheta)
```

## SLAM Algorithms in Detail

### Scan Matching — Iterative Closest Point (ICP)

ICP aligns two point clouds by iteratively finding correspondences and computing the optimal rigid transformation.

```python
import numpy as np
from navigation import PointCloud

def icp(source, target, max_iterations=50, tolerance=1e-6):
    # Initialize transformation
    R = np.eye(3)
    t = np.zeros(3)
    
    for iteration in range(max_iterations):
        # Transform source
        source_transformed = (R @ source.T).T + t
        
        # Find closest points in target
        distances, indices = nearest_neighbors(source_transformed, target)
        
        # Filter outliers
        inlier_mask = distances < np.percentile(distances, 90)
        source_inliers = source_transformed[inlier_mask]
        target_inliers = target[indices[inlier_mask]]
        
        # Compute optimal transformation
        R_new, t_new = rigid_transform_svd(source_inliers, target_inliers)
        
        # Update transformation
        R = R_new @ R
        t = R_new @ t + t_new
        
        # Check convergence
        if np.linalg.norm(t_new) < tolerance and np.linalg.norm(R_new - np.eye(3)) < tolerance:
            break
    
    return R, t

def rigid_transform_svd(A, B):
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    
    H = (A - centroid_A).T @ (B - centroid_B)
    U, S, Vt = np.linalg.svd(H)
    
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T
    
    t = centroid_B - R @ centroid_A
    return R, t
```

### Normal Distributions Transform (NDT)

NDT represents the target scan as a set of normal distributions in a voxel grid, then optimizes the pose to maximize the likelihood of the source scan under these distributions.

```python
from navigation import NDTScanMatcher, VoxelGrid

class NDTMatcher:
    def __init__(self, voxel_size=0.5):
        self.voxel_size = voxel_size
    
    def build_ndt(self, target_cloud):
        voxel_grid = VoxelGrid(self.voxel_size)
        voxel_grid.insert(target_cloud)
        
        ndt = {}
        for voxel_idx, points in voxel_grid.get_voxels():
            mean = np.mean(points, axis=0)
            cov = np.cov(points.T) + np.eye(3) * 1e-6  # regularization
            ndt[voxel_idx] = (mean, np.linalg.inv(cov))
        
        return ndt
    
    def match(self, source_cloud, ndt, initial_pose):
        pose = initial_pose.copy()
        
        for iteration in range(50):
            score = 0
            gradient = np.zeros(6)
            hessian = np.zeros((6, 6))
            
            for point in source_cloud:
                transformed = self.transform_point(point, pose)
                voxel_idx = self.get_voxel_idx(transformed)
                
                if voxel_idx in ndt:
                    mean, cov_inv = ndt[voxel_idx]
                    diff = transformed - mean
                    score += -0.5 * diff.T @ cov_inv @ diff
                    
                    # Compute Jacobian and accumulate
                    J = self.point_jacobian(point, pose)
                    gradient += -J.T @ cov_inv @ diff
                    hessian += -J.T @ cov_inv @ J
            
            # Update pose
            delta = np.linalg.solve(hessian, -gradient)
            pose = self.update_pose(pose, delta)
            
            if np.linalg.norm(delta) < 1e-6:
                break
        
        return pose
```

### Loop Closure Detection

Loop closure recognition uses visual or geometric features to detect when the robot revisits a location.

```python
from navigation import LoopClosureDetector, BagOfWords

class LoopClosureDetector:
    def __init__(self, vocab_size=1000, min_score=0.7):
        self.bow = BagOfWords(vocab_size)
        self.database = {}
        self.min_score = min_score
        self.current_query_id = 0
    
    def add_keyframe(self, features, descriptors):
        bow_vector = self.bow.quantize(descriptors)
        self.database[self.current_query_id] = {
            'bow': bow_vector,
            'features': features,
            'descriptors': descriptors,
        }
        self.current_query_id += 1
    
    def detect(self, query_descriptors, current_pose, max_distance=10.0):
        query_bow = self.bow.quantize(query_descriptors)
        
        candidates = []
        for kid, kf in self.database.items():
            score = self.bow.compare(query_bow, kf['bow'])
            if score > self.min_score:
                # Verify geometric consistency
                if self几何验证(query_descriptors, kf['descriptors']):
                    distance = np.linalg.norm(
                        np.array(current_pose[:2]) - np.array(self.get_keyframe_pose(kid)[:2])
                    )
                    if distance > max_distance:  # not too close
                        candidates.append((kid, score, distance))
        
        if candidates:
            best = max(candidates, key=lambda x: x[1])
            return best[0]
        return None
```

## Sensor Fusion Algorithms

### Extended Kalman Filter — Full Implementation

```python
import numpy as np
from navigation import SensorModel

class ExtendedKalmanFilter:
    def __init__(self, state_dim, process_noise):
        self.state_dim = state_dim
        self.x = np.zeros(state_dim)
        self.P = np.eye(state_dim) * 1.0
        self.Q = process_noise
    
    def predict(self, u, dt):
        # State transition (bicycle model or differential drive)
        x, y, theta, v = self.x
        self.x[0] = x + v * np.cos(theta) * dt
        self.x[1] = y + v * np.sin(theta) * dt
        self.x[2] = theta + u[1] * dt  # u = [v, omega]
        self.x[3] = u[0]
        
        # Jacobian of state transition
        F = np.eye(self.state_dim)
        F[0, 2] = -v * np.sin(theta) * dt
        F[0, 3] = np.cos(theta) * dt
        F[1, 2] = v * np.cos(theta) * dt
        F[1, 3] = np.sin(theta) * dt
        F[2, 2] = 1.0
        
        self.P = F @ self.P @ F.T + self.Q
    
    def update(self, z, H, R):
        # Innovation
        y = z - H @ self.x
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        
        self.x = self.x + K @ y
        self.P = (np.eye(self.state_dim) - K @ H) @ self.P
    
    def get_pose(self):
        return (self.x[0], self.x[1], self.x[2])

# Usage
ekf = ExtendedKalmanFilter(
    state_dim=4,
    process_noise=np.diag([0.1, 0.1, 0.01, 0.1])
)

for odom, lidar in sensor_stream:
    # Predict with odometry
    ekf.predict([odom.linear_velocity, odom.angular_velocity], dt=0.05)
    
    # Update with LiDAR scan matching
    if lidar.matched:
        H = np.zeros((3, 4))
        H[:3, :3] = np.eye(3)
        R = np.diag([0.05, 0.05, 0.01])
        ekf.update(np.array(lidar.pose), H, R)
```

### Particle Filter Localization — Implementation

```python
import numpy as np
from navigation import OccupancyGrid

class ParticleFilter:
    def __init__(self, num_particles, map_grid, motion_noise, sensor_noise):
        self.num_particles = num_particles
        self.map = map_grid
        self.motion_noise = motion_noise
        self.sensor_noise = sensor_noise
        
        # Initialize particles uniformly
        free_cells = map_grid.get_free_cells()
        indices = np.random.choice(len(free_cells), num_particles)
        self.particles = np.array([free_cells[i] for i in indices])
        self.weights = np.ones(num_particles) / num_particles
    
    def predict(self, odom_delta):
        # Motion model with noise
        noise = np.random.normal(0, self.motion_noise, self.particles.shape)
        self.particles[:, 0] += odom_delta[0] * np.cos(self.particles[:, 2]) + noise[:, 0]
        self.particles[:, 1] += odom_delta[0] * np.sin(self.particles[:, 2]) + noise[:, 1]
        self.particles[:, 2] += odom_delta[1] + noise[:, 2]
        
        # Map matching
        for i, p in enumerate(self.particles):
            if not self.map.is_free(p[0], p[1]):
                self.particles[i] = self.map.random_free_cell()
    
    def update_weights(self, lidar_scan):
        for i, p in enumerate(self.particles):
            self.weights[i] = self.sensor_model(p, lidar_scan)
        
        self.weights /= np.sum(self.weights)
    
    def resample(self):
        indices = np.random.choice(
            self.num_particles,
            size=self.num_particles,
            p=self.weights
        )
        self.particles = self.particles[indices].copy()
        self.weights = np.ones(self.num_particles) / self.num_particles
    
    def get_estimate(self):
        # Weighted average
        x = np.average(self.particles[:, 0], weights=self.weights)
        y = np.average(self.particles[:, 1], weights=self.weights)
        theta = np.average(self.particles[:, 2], weights=self.weights)
        return (x, y, theta)
    
    def get_covariance(self):
        return np.cov(self.particles.T, aweights=self.weights)
```

## Local Planning Algorithms

### Timed Elastic Band (TEB)

TEB optimizes a trajectory with respect to time, obstacle avoidance, velocity limits, and acceleration limits.

```python
from navigation import TEBPlanner, TEBConfig

class TEBPlannerImpl:
    def __init__(self, config):
        self.config = config
        self.teb = None
    
    def plan(self, global_path, start_vel, goal_vel, obstacles):
        # Initialize TEB from global path
        teb = self.initialize_teb(global_path, start_vel, goal_vel)
        
        # Optimize
        for iteration in range(self.config.max_iterations):
            # Obstacle cost
            obstacle_cost = self.compute_obstacle_cost(teb, obstacles)
            
            # Velocity/acceleration cost
            kinematic_cost = self.compute_kinematic_cost(teb)
            
            # Time cost
            time_cost = self.compute_time_cost(teb)
            
            # Update via Levenberg-Marquardt
            delta = self.levenberg_marquardt_step(teb, obstacle_cost + kinematic_cost + time_cost)
            teb = self.apply_update(teb, delta)
            
            if np.linalg.norm(delta) < self.config.convergence_threshold:
                break
        
        return teb

    def compute_obstacle_cost(self, teb, obstacles):
        cost = 0
        for i, pose in enumerate(teb.poses):
            for obs in obstacles:
                dist = self.distance_to_obstacle(pose, obs)
                if dist < self.config.obstacle_gain_threshold:
                    cost += 0.5 * self.config.obstacle_gain / (dist**2)
        return cost
```

### Model Predictive Control (MPC) for Navigation

```python
import numpy as np
from navigation import MPCConfig, VehicleModel

class MPCController:
    def __init__(self, config, vehicle_model):
        self.config = config
        self.model = vehicle_model
        self.horizon = config.horizon
        self.dt = config.dt
    
    def solve(self, current_state, reference_trajectory):
        # Initialize control sequence
        u_seq = np.zeros((self.horizon, 2))  # [v, omega]
        
        for iteration in range(self.config.max_iterations):
            # Forward simulate with current controls
            predicted_states = self.model.simulate(current_state, u_seq, self.dt)
            
            # Compute cost
            cost = self.compute_cost(predicted_states, u_seq, reference_trajectory)
            
            # Compute gradient via finite differences
            gradient = self.compute_gradient(current_state, u_seq, reference_trajectory)
            
            # Update controls
            u_seq = u_seq - self.config.step_size * gradient
            
            # Apply constraints
            u_seq = self.clip_controls(u_seq)
        
        return u_seq[0]  # return first control
    
    def compute_cost(self, states, controls, reference):
        tracking_cost = 0
        control_cost = 0
        
        for i in range(self.horizon):
            # Tracking error
            error = states[i] - reference[i]
            tracking_cost += error.T @ self.config.Q @ error
            
            # Control effort
            control_cost += controls[i].T @ self.config.R @ controls[i]
            
            # Terminal cost
            if i == self.horizon - 1:
                terminal_error = states[i] - reference[i]
                tracking_cost += terminal_error.T @ self.config.Q_terminal @ terminal_error
        
        return tracking_cost + control_cost
```

## Trajectory Tracking Controllers

### Stanley Controller

Stanley controller uses both heading error and cross-track error for path following, providing smooth convergence to the path.

```python
import numpy as np

class StanleyController:
    def __init__(self, k_heading, k_cross_track, wheelbase):
        self.k_heading = k_heading
        self.k_cross_track = k_cross_track
        self.wheelbase = wheelbase
    
    def compute(self, current_pose, path, current_velocity):
        x, y, theta = current_pose
        
        # Find closest point on path
        closest_idx = self.find_closest_point(path, (x, y))
        closest_point = path[closest_idx]
        
        # Heading of path at closest point
        if closest_idx < len(path) - 1:
            path_heading = np.arctan2(
                path[closest_idx + 1][1] - closest_point[1],
                path[closest_idx + 1][0] - closest_point[0]
            )
        else:
            path_heading = theta
        
        # Cross-track error
        cross_track_error = self.compute_cross_track_error((x, y), path)
        
        # Heading error
        heading_error = path_heading - theta
        heading_error = np.arctan2(np.sin(heading_error), np.cos(heading_error))
        
        # Steering command
        steering = heading_error + np.arctan2(
            self.k_cross_track * cross_track_error,
            max(current_velocity, 0.1)
        )
        
        # Clamp steering
        steering = np.clip(steering, -self.max_steer, self.max_steer)
        
        return steering
    
    def compute_cross_track_error(self, point, path):
        # Find perpendicular distance to nearest segment
        min_dist = float('inf')
        for i in range(len(path) - 1):
            p1, p2 = path[i], path[i + 1]
            dist = self.point_to_segment_distance(point, p1, p2)
            min_dist = min(min_dist, dist)
        
        # Sign based on left/right of path
        closest_idx = self.find_closest_point(path, point)
        path_dir = np.array(path[min(closest_idx + 1, len(path) - 1)]) - np.array(path[closest_idx])
        to_point = np.array(point) - np.array(path[closest_idx])
        sign = np.sign(np.cross(path_dir, to_point))
        
        return sign * min_dist
```

### Pure Pursuit with Curvature Constraint

```python
class PurePursuitEnhanced:
    def __init__(self, lookahead_min, lookahead_max, max_curvature):
        self.lookahead_min = lookahead_min
        self.lookahead_max = lookahead_max
        self.max_curvature = max_curvature
    
    def compute(self, robot_pose, path, velocity):
        # Adaptive lookahead based on curvature
        lookahead = self.compute_lookahead(path, velocity)
        
        # Find lookahead point
        target = self.find_lookahead_point(robot_pose, path, lookahead)
        
        # Compute curvature
        dx = target[0] - robot_pose[0]
        dy = target[1] - robot_pose[1]
        L = np.sqrt(dx**2 + dy**2)
        
        # Angle to target
        alpha = np.arctan2(dy, dx) - robot_pose[2]
        alpha = np.arctan2(np.sin(alpha), np.cos(alpha))
        
        # Curvature
        curvature = 2 * np.sin(alpha) / L
        
        # Clamp curvature
        curvature = np.clip(curvature, -self.max_curvature, self.max_curvature)
        
        # Angular velocity
        angular_velocity = curvature * velocity
        
        return angular_velocity
    
    def compute_lookahead(self, path, velocity):
        # Scale lookahead with velocity
        lookahead = self.lookahead_min + (self.lookahead_max - self.lookahead_min) * (velocity / 2.0)
        return np.clip(lookahead, self.lookahead_min, self.lookahead_max)
```

## Occupancy Grid Mapping

### Bayesian Occupancy Grid Update

```python
import numpy as np

class OccupancyGridMapper:
    def __init__(self, width, height, resolution, prior=0.5):
        self.resolution = resolution
        self.grid = np.full((height, width), prior)
        self.log_odds_grid = np.zeros((height, width))
        
        # Log-odds parameters
        self.l_occ = 0.85   # log-odds of occupied
        self.l_free = -0.4   # log-odds of free
        self.l_min = -5.0    # lower bound
        self.l_max = 5.0     # upper bound
    
    def update(self, robot_pose, scan):
        for angle, range_val in scan.ranges:
            if range_val >= scan.range_max:
                continue
            
            # Ray endpoints
            end_x = robot_pose[0] + range_val * np.cos(robot_pose[2] + angle)
            end_y = robot_pose[1] + range_val * np.sin(robot_pose[2] + angle)
            
            # Mark cells along ray as free
            free_cells = self.raycast(robot_pose[:2], (end_x, end_y))
            for cell in free_cells:
                self.update_cell(cell, self.l_free)
            
            # Mark endpoint as occupied
            occ_cell = self.world_to_grid(end_x, end_y)
            self.update_cell(occ_cell, self.l_occ)
    
    def update_cell(self, cell, log_odds_update):
        x, y = cell
        if 0 <= x < self.grid.shape[1] and 0 <= y < self.grid.shape[0]:
            self.log_odds_grid[y, x] = np.clip(
                self.log_odds_grid[y, x] + log_odds_update,
                self.l_min, self.l_max
            )
            self.grid[y, x] = 1.0 / (1.0 + np.exp(-self.log_odds_grid[y, x]))
```

## Configuration Reference

### Navigation Stack Configuration

```yaml
navigation:
  global_planner:
    algorithm: "astar"
    heuristic: "octile"
    allow_unknown: false
    default_tolerance: 0.2
    
  local_planner:
    algorithm: "dwa"
    max_speed: 1.5
    max_accel: 2.0
    max_yaw_rate: 3.0
    heading_weight: 0.15
    clearance_weight: 0.1
    velocity_weight: 0.1
    
  costmap:
    global_frame: "map"
    robot_base_frame: "base_link"
    update_frequency: 5.0
    publish_frequency: 2.0
    resolution: 0.05
    
    static_layer:
      enabled: true
      map_topic: "/map"
      
    obstacle_layer:
      enabled: true
      observation_sources: ["lidar", "sonar"]
      lidar:
        topic: "/scan"
        sensor_frame: "laser_link"
        max_obstacle_height: 2.0
        
    inflation_layer:
      enabled: true
      inflation_radius: 0.55
      cost_scaling_factor: 10.0
      
  recovery_behaviors:
    - name: "conservative_reset"
      behavior: "clear_costmap"
      area: 2.0
    - name: "rotate_recovery"
      behavior: "rotate_in_place"
      max_angular_vel: 0.5
    - name: "aggressive_reset"
      behavior: "clear_costmap"
      area: 5.0
```

### SLAM Configuration

```yaml
slam:
  algorithm: "cartographer"
  
  scan_matching:
    type: "ceres"
    max_iterations: 10
    convergence_threshold: 1e-6
    
  loop_closure:
    enabled: true
    strategy: "visual_bow"
    min_interval_frames: 50
    min_score: 0.7
    max_distance_m: 10.0
    
  submap:
    num_range_data: 90
    resolution: 0.05
    
  pose_graph:
    optimization_interval: 90
    max_num_iterations: 10
    homogeneous_cost_threshold: 1.0e-6
    
  motion_filter:
    max_time_seconds: 0.5
    max_distance_meters: 0.1
    max_angle_radians: 0.1
```
