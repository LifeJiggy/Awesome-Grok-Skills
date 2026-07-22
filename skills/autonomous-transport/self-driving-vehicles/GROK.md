---
name: "self-driving-vehicles"
category: "autonomous-transport"
version: "2.0.0"
tags: ["autonomous-transport", "self-driving-vehicles", "perception", "planning", "control"]
---

# Self Driving Vehicles

## Overview

Comprehensive self-driving-vehicles capabilities within the autonomous-transport domain. This module provides tools, frameworks, and best practices for autonomous vehicle operations including sensor fusion, perception, path planning, vehicle control, and safety systems.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from self_driving_vehicles import Engine

engine = Engine()
engine.configure()
results = engine.run()
print(results)
```

## Best Practices

- Follow safety-first design principles (ASIL-D compliance)
- Implement redundant sensor systems for fault tolerance
- Use simulation-based testing before real-world deployment
- Validate perception models with diverse driving scenarios
- Monitor system health continuously during operation
- Document all API interfaces for safety audits

## Related Modules

- **lidar-processing** — LiDAR point cloud processing
- **path-planning** — Route and trajectory planning
- **vehicle-to-everything** — V2X communication
- **fleet-management** — Multi-vehicle coordination

## Advanced Configuration

### Sensor Fusion Configuration

```python
from self_driving_vehicles import SensorFusion, SensorConfig, FusionMethod

sensor_config = SensorConfig(
    cameras=[
        {"id": "front_center", "resolution": (1920, 1080), "fov": 120, "fps": 30},
        {"id": "front_left", "resolution": (1920, 1080), "fov": 60, "fps": 30},
        {"id": "front_right", "resolution": (1920, 1080), "fov": 60, "fps": 30},
        {"id": "rear", "resolution": (1920, 1080), "fov": 120, "fps": 30},
    ],
    lidar=[
        {"id": "main_lidar", "type": "velodyne_vls128", "channels": 128, "range_m": 200, "fps": 10},
    ],
    radar=[
        {"id": "front_radar", "type": "continental_ars540", "range_m": 300, "fov": 60},
        {"id": "corner_radars", "type": "conti_ars408", "range_m": 150, "fov": 140, "count": 4},
    ],
    imu={"id": "main_imu", "type": "vectornav_vn100", "update_rate_hz": 200},
    gps={"id": "main_gps", "type": "trimble_ag372", "update_rate_hz": 10, "rtk_enabled": True},
)

fusion = SensorFusion(method=FusionMethod.EXTENDED_KALMAN_FILTER)
```

### Perception Pipeline

```python
from self_driving_vehicles import PerceptionPipeline, PerceptionConfig

perception_config = PerceptionConfig(
    object_detection={"model": "yolov8x", "confidence_threshold": 0.5},
    lane_detection={"model": "lanenet", "max_lanes": 4},
    tracking={"method": "deep_sort", "max_age": 30},
)
perception = PerceptionPipeline(config=perception_config)
```

### Planning Configuration

```python
from self_driving_vehicles import Planner, PlanningConfig

planning_config = PlanningConfig(
    global_planner={"algorithm": "hybrid_astar", "grid_resolution_m": 0.5},
    local_planner={"algorithm": "mpc", "horizon_s": 3.0, "dt_s": 0.1},
    behavior_planner={"max_speed_kmh": 130, "min_following_distance_m": 2.0},
)
```

## Architecture Patterns

### Self-Driving Vehicle Architecture

```
+------------------------------------------------------------------+
|              Self-Driving Vehicle Architecture                    |
+------------------------------------------------------------------+
|  +----------------+    +----------------+    +----------------+  |
|  |  Perception    |    |  Planning      |    |  Control       |  |
|  |  Layer         |    |  Layer         |    |  Layer         |  |
|  |  Camera        |    |  Global Plan   |    |  Steering      |  |
|  |  LiDAR         |<-->|  Local Plan    |<-->|  Throttle      |  |
|  |  Radar         |    |  Behavior      |    |  Braking       |  |
|  +----------------+    +----------------+    +----------------+  |
|          |                    |                     |            |
|          v                    v                     v            |
|  +----------------------------------------------------------------+
|  |  Sensor Fusion  |  HD Map Service  |  Localization Service   |
|  +----------------------------------------------------------------+
|                              |                                    |
|                              v                                    |
|  +----------------------------------------------------------------+
|  |  Redundancy Manager  |  Failover System  |  Emergency Stop   |
|  +----------------------------------------------------------------+
+------------------------------------------------------------------+
```

### Perception Pipeline Flow

```
Sensor Data -> Preprocessing -> Feature Extraction -> Sensor Fusion
    -> Object Tracking -> Prediction -> World Model Update
```

### Control Loop (100Hz)

```
Read Sensors -> Update State -> Get Trajectory -> Compute Control
    -> Send Commands -> Monitor Safety -> Loop
```

## Integration Guide

### ROS2 Integration

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class AutonomousDrivingNode(Node):
    def __init__(self):
        super().__init__('autonomous_driving')
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.01, self.control_loop)

    def control_loop(self):
        state = self.get_vehicle_state()
        trajectory = self.planner.plan(state, self.goal)
        control = self.controller.compute(state, trajectory)
        cmd_vel = Twist()
        cmd_vel.linear.x = control.speed
        cmd_vel.angular.z = control.steering
        self.cmd_vel_pub.publish(cmd_vel)
```

### CAN Bus Integration

```python
import can
import struct

class CANInterface:
    def __init__(self, interface='socketcan', channel='can0'):
        self.bus = can.interface.Bus(interface=interface, channel=channel)

    def send_steering(self, angle_deg):
        data = struct.pack('>h', int(angle_deg * 100))
        msg = can.Message(arbitration_id=0x100, data=data)
        self.bus.send(msg)

    def send_throttle(self, position_pct):
        data = struct.pack('>H', int(position_pct * 100))
        msg = can.Message(arbitration_id=0x101, data=data)
        self.bus.send(msg)
```

## Performance Optimization

### Perception Optimization

```python
perception_opt = PerceptionOptimizer(
    config={"target_latency_ms": 100, "max_gpu_usage": 0.8},
    optimizations={"model_quantization": True, "tensorrt": True},
)
stats = perception_opt.get_stats()
print(f"Perception latency: {stats.latency_ms:.1f}ms")
```

### Planning Optimization

```python
planning_opt = PlanningOptimizer(
    optimizations={"parallel_planning": True, "cached_lane_graph": True},
)
```

## Safety Considerations

### Functional Safety (ASIL-D)

```python
from self_driving_vehicles import SafetyManager

safety = SafetyManager(config={
    "asil_level": "D",
    "redundancy": {"sensors": True, "compute": True, "actuators": True},
    "failover": {"strategy": "minimum_risk_condition"},
})

@safety.on_safety_event
def on_safety_event(event):
    print(f"Safety event: {event.type} - {event.severity}")
```

### Cybersecurity

```python
cybersecurity = CybersecurityManager(config={
    "intrusion_detection": True,
    "encrypted_communication": True,
    "secure_boot": True,
})
```

## Troubleshooting Guide

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Sensor failure** | Missing data | Check connections, recalibrate |
| **Perception errors** | Incorrect detections | Retrain models, check calibration |
| **Planning failures** | No trajectory | Check map data, verify constraints |
| **Control instability** | Jerky motion | Tune PID gains, check latency |
| **Localization drift** | Position error | Use RTK GPS, add visual odometry |

## API Reference

```python
class SensorFusion:
    def __init__(self, method: str, config: dict): ...
    def fuse(self, sensor_data: dict) -> FusedState: ...

class Planner:
    def __init__(self, config: dict): ...
    def plan(self, current_state, goal, obstacles, lane_graph) -> Trajectory: ...

class Controller:
    def __init__(self, config: dict): ...
    def compute(self, state, trajectory) -> ControlCommand: ...
```

## Data Models

```python
@dataclass
class VehicleState:
    position: Vector3
    orientation: Quaternion
    velocity: Vector3
    steering_angle: float
    speed_kmh: float
    timestamp: float

@dataclass
class Detection:
    class_name: str
    confidence: float
    bbox: BoundingBox
    position: Vector3
    velocity: Vector3

@dataclass
class Trajectory:
    points: List[TrajectoryPoint]
    duration_s: float
    max_speed_mps: float

@dataclass
class ControlCommand:
    steering_angle: float
    throttle_position: float
    brake_pressure: float
    gear: str
```

## Deployment Guide

```python
from self_driving_vehicles import VehicleDeployment

deployment = VehicleDeployment(config={
    "vehicle_id": "AV-001",
    "compute": "nvidia_orin",
    "testing": {"simulation": True, "closed_course": True, "public_road": True},
})
deployment.deploy()
```

## Monitoring & Observability

```python
from self_driving_vehicles import VehicleMonitor

monitor = VehicleMonitor(
    vehicle_id="AV-001",
    metrics=["perception_latency", "planning_latency", "vehicle_speed"],
    alerts={
        "sensor_failure": {"severity": "critical", "action": "safe_stop"},
        "high_latency": {"threshold": 200, "action": "reduce_speed"},
    },
)
monitor.start()
```

## Testing Strategy

```python
import pytest
from self_driving_vehicles import PerceptionPipeline, Planner

class TestPerception:
    def test_object_detection(self):
        perception = PerceptionPipeline(config=perception_config)
        detections = perception.process(sensor_data)
        assert len(detections) > 0

class TestPlanning:
    def test_trajectory_generation(self):
        planner = Planner(config=planning_config)
        trajectory = planner.plan(state, goal, obstacles, lane_graph)
        assert len(trajectory.points) > 0
```

## Versioning & Migration

| Version | Changes | Breaking |
|---------|---------|----------|
| 2.0.0 | Added V2X support, improved perception | Yes |
| 1.5.0 | Added HD map integration | No |
| 1.0.0 | Initial release | N/A |

## Glossary

| Term | Definition |
|------|------------|
| **ASIL** | Automotive Safety Integrity Level |
| **EKF** | Extended Kalman Filter |
| **HD Map** | High-Definition Map |
| **LiDAR** | Light Detection and Ranging |
| **MPC** | Model Predictive Control |
| **RTK** | Real-Time Kinematic |
| **V2X** | Vehicle-to-Everything |

## Changelog

### 2.0.0 (2024-01-15)
- Added V2X support, improved perception accuracy

### 1.5.0 (2023-10-01)
- Added HD map integration

### 1.0.0 (2023-06-01)
- Initial release

## Contributing Guidelines

```bash
git clone https://github.com/company/self-driving-vehicles.git
cd self-driving-vehicles
pip install -e ".[dev]"
pytest tests/
```

## Detailed Architecture

### Sensor Stack Architecture

```
+------------------------------------------------------------------+
|                    Sensor Stack Architecture                      |
+------------------------------------------------------------------+
|                                                                  |
|  +------------------+    +------------------+                     |
|  |  Camera Module   |    |  LiDAR Module    |                     |
|  |                  |    |                  |                     |
|  |  6x RGB Cameras  |    |  Velodyne VLS-128|                     |
|  |  30fps, 1080p    |    |  128 channels    |                     |
|  |  120deg FOV      |    |  200m range      |                     |
|  +--------+---------+    +--------+---------+                     |
|           |                       |                               |
|           v                       v                               |
|  +------------------------------------------------------------+  |
|  |               Sensor Fusion Engine (EKF)                    |  |
|  |  - Timestamp synchronization (PTP IEEE 1588)                |  |
|  |  - Spatial calibration (extrinsic matrices)                 |  |
|  |  - Temporal alignment (interpolation)                       |  |
|  |  - State estimation (position, velocity, orientation)       |  |
|  +----------------------------+-------------------------------+  |
|                               |                                   |
|  +------------------+    +---v-----------+                       |
|  |  Radar Module    |    |  IMU Module   |                       |
|  |  5x Continental  |    |  VectorNav    |                       |
|  |  ARS540/408      |    |  VN-100       |                       |
|  +------------------+    +---------------+                       |
+------------------------------------------------------------------+
```

### Planning Stack Architecture

```
+------------------------------------------------------------------+
|                    Planning Stack Architecture                    |
+------------------------------------------------------------------+
|                                                                  |
|  +------------------------------------------------------------+  |
|  |                    Route Planning                           |  |
|  |  - HD Map query (OpenDRIVE format)                         |  |
|  |  - GPS to lane matching                                     |  |
|  |  - Route optimization (Dijkstra / A*)                      |  |
|  +----------------------------+-------------------------------+  |
|                               |                                   |
|  +------------------------------------------------------------+  |
|  |                    Behavior Planning                        |  |
|  |  - Lane change decisions                                    |  |
|  |  - Overtaking logic                                         |  |
|  |  - Traffic rule compliance                                  |  |
|  |  - Right-of-way determination                               |  |
|  +----------------------------+-------------------------------+  |
|                               |                                   |
|  +------------------------------------------------------------+  |
|  |                    Motion Planning (MPC)                    |  |
|  |  - Trajectory generation (quintic polynomials)              |  |
|  |  - Obstacle avoidance (ORCA / VO)                           |  |
|  |  - Comfort optimization (jerk minimization)                 |  |
|  |  - Kinodynamic constraints                                  |  |
|  +----------------------------+-------------------------------+  |
|                               |                                   |
|  +------------------------------------------------------------+  |
|  |                    Trajectory Validation                     |  |
|  |  - Collision checking (swept volume)                        |  |
|  |  - Feasibility check (dynamic limits)                       |  |
|  |  - Safety score calculation                                 |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

### Control Stack Architecture

```
+------------------------------------------------------------------+
|                    Control Stack Architecture                     |
+------------------------------------------------------------------+
|                                                                  |
|  +-------------------+    +-------------------+                   |
|  |  Lateral Control  |    |  Longitudinal     |                   |
|  |  (Steering)       |    |  Control          |                   |
|  |                   |    |  (Speed/Brake)    |                   |
|  |  - Stanley        |    |  - PID            |                   |
|  |  - Pure Pursuit   |    |  - MPC            |                   |
|  |  - MPC            |    |  - Adaptive Cruise|                   |
|  +--------+----------+    +--------+----------+                   |
|           |                       |                               |
|           v                       v                               |
|  +------------------------------------------------------------+  |
|  |               Actuator Interface Layer                      |  |
|  |  - CAN bus communication (500 kbps)                         |  |
|  |  - steer-by-wire (EPS)                                      |  |
|  |  - brake-by-wire (EHB)                                      |  |
|  |  - throttle-by-wire (ETC)                                   |  |
|  +----------------------------+-------------------------------+  |
|                               |                                   |
|  +------------------------------------------------------------+  |
|  |               Safety Monitor                                |  |
|  |  - Watchdog timer (10ms timeout)                            |  |
|  |  - Actuator feedback validation                             |  |
|  |  - Emergency fallback (minimum risk condition)              |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

### Data Flow Architecture

```
+------------------------------------------------------------------+
|                    Data Flow Architecture                         |
+------------------------------------------------------------------+
|                                                                  |
|  Sensor Data (10-200 Hz)                                         |
|       |                                                          |
|       v                                                          |
|  +-------------------+                                           |
|  |  Data Ingestion   |  Kafka / DDS / ROS2                      |
|  +-------------------+                                           |
|       |                                                          |
|       +---+---+---+---+                                         |
|       |   |   |   |   |                                         |
|       v   v   v   v   v                                         |
|  +----+ +----+ +----+ +----+ +----+                              |
|  |Per-| |Per-| |Per-| |Fus-| |Log |                              |
|  |cep-| |cep-| |cep-| |ion | |ger |                              |
|  |tion| |tion| |tion| |    | |    |                              |
|  |Cam | |LiD | |Rdr | |    | |    |                              |
|  +--+-+ +--+-+ +--+-+ +--+-+ +----+                              |
|     |     |     |     |                                          |
|     v     v     v     v                                          |
|  +------------------------------------------------------------+  |
|  |              Perception Fusion Layer                         |  |
|  |  Object list, lane list, free space, traffic lights         |  |
|  +----------------------------+-------------------------------+  |
|                               |                                   |
|                               v                                   |
|  +------------------------------------------------------------+  |
|  |              World Model (Shared State)                     |  |
|  |  Ego state, objects, lanes, signals, HD map context         |  |
|  +----------------------------+-------------------------------+  |
|                               |                                   |
|                    +----------+----------+                       |
|                    |                     |                        |
|                    v                     v                        |
|  +-------------------+    +-------------------+                   |
|  |  Planning Module  |    |  Logging Module   |                   |
|  +-------------------+    +-------------------+                   |
+------------------------------------------------------------------+
```

## Detailed Usage Examples

### Complete Pipeline Example

```python
from self_driving_vehicles import (
    SensorFusion, PerceptionPipeline, Planner, Controller, SafetyManager
)

# Initialize all modules
fusion = SensorFusion(method="ekf")
perception = PerceptionPipeline(config=perception_config)
planner = Planner(config=planning_config)
controller = Controller(config=control_config)
safety = SafetyManager(config=safety_config)

# Main autonomous driving loop
async def autonomous_loop(vehicle):
    while vehicle.is_active():
        # 1. Read sensors
        sensor_data = await vehicle.read_sensors()

        # 2. Fuse sensor data
        fused_state = fusion.fuse(sensor_data)

        # 3. Perception
        detections = perception.process(sensor_data)
        lanes = perception.detect_lanes(sensor_data)
        signals = perception.detect_traffic_signals(sensor_data)

        # 4. Update world model
        world_model.update(
            ego_state=fused_state,
            objects=detections,
            lanes=lanes,
            signals=signals,
        )

        # 5. Plan trajectory
        trajectory = planner.plan(
            current_state=fused_state,
            goal=vehicle.get目的地(),
            world_model=world_model,
        )

        # 6. Safety check
        if not safety.validate_trajectory(trajectory):
            trajectory = safety.minimum_risk_trajectory(fused_state)

        # 7. Control
        command = controller.compute(fused_state, trajectory)

        # 8. Actuate
        await vehicle.send_command(command)

        # 9. Monitor
        safety.monitor_system_health()

        await asyncio.sleep(0.01)  # 100Hz loop
```

### Simulation Example

```python
from self_driving_vehicles import SimulationEnvironment

# Create simulation
sim = SimulationEnvironment(
    map="town01",
    weather="clear",
    traffic_density="medium",
    pedestrians=True,
)

# Run scenario
vehicle = sim.spawn_vehicle(
    position=(100, 200),
    heading=0.0,
    autopilot=True,
)

# Run simulation
for tick in range(1000):
    sim.step()
    state = vehicle.get_state()
    print(f"Tick {tick}: speed={state.speed_kmh:.1f}km/h, "
          f"pos=({state.position.x:.1f}, {state.position.y:.1f})")

# Collect metrics
metrics = sim.get_metrics()
print(f"Distance traveled: {metrics.distance_m:.1f}m")
print(f"Average speed: {metrics.avg_speed_kmh:.1f}km/h")
print(f"Collisions: {metrics.collision_count}")
print(f"Traffic violations: {metrics.violation_count}")
```

### Data Recording Example

```python
from self_driving_vehicles import DataRecorder

recorder = DataRecorder(
    output_dir="/data/drive_logs",
    format="rosbag2",
    compression="lz4",
)

# Start recording
recorder.start(
    topics=[
        "/camera/front/image_raw",
        "/lidar/points",
        "/radar/detections",
        "/vehicle/odom",
        "/vehicle/control",
    ],
)

# Drive and record
vehicle.drive(route, duration_s=300)

# Stop recording
recorder.stop()
print(f"Recorded {recorder.size_mb:.1f}MB in {recorder.duration_s:.0f}s")
```

## Sensor Specifications

| Sensor | Model | Range | FOV | Resolution | Update Rate |
|--------|-------|-------|-----|------------|-------------|
| Front Camera | Sony IMX490 | 200m | 120° | 1920×1080 | 30 Hz |
| Side Camera | Sony IMX462 | 100m | 90° | 1280×720 | 30 Hz |
| Rear Camera | Sony IMX490 | 150m | 120° | 1920×1080 | 30 Hz |
| Main LiDAR | Velodyne VLS-128 | 200m | 360° | 128 channels | 10 Hz |
| Short LiDAR | Velodyne VLP-16 | 100m | 360° | 16 channels | 20 Hz |
| Front Radar | Continental ARS540 | 300m | 60° | N/A | 20 Hz |
| Corner Radar | Continental ARS408 | 150m | 140° | N/A | 20 Hz |
| IMU | VectorNav VN-100 | N/A | N/A | 9-axis | 200 Hz |
| GPS | Trimble AG372 | Global | N/A | RTK | 10 Hz |

## Detailed Control Algorithms

### Pure Pursuit Controller

```python
class PurePursuitController:
    def __init__(self, wheelbase_m=2.7, lookahead_m=5.0):
        self.wheelbase = wheelbase_m
        self.lookahead = lookahead_m

    def compute_steering(self, ego_state, trajectory):
        # Find lookahead point on trajectory
        lookahead_point = trajectory.find_point_at_distance(
            ego_state.position, self.lookahead
        )

        # Calculate curvature
        dx = lookahead_point.x - ego_state.position.x
        dy = lookahead_point.y - ego_state.position.y
        heading = math.atan2(dy, dx)

        # Calculate steering angle
        alpha = heading - ego_state.heading
        steering_angle = math.atan2(
            2.0 * self.wheelbase * math.sin(alpha),
            self.lookahead
        )

        return steering_angle
```

### PID Speed Controller

```python
class PIDSpeedController:
    def __init__(self, kp=1.0, ki=0.1, kd=0.05):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, target_speed, current_speed, dt):
        error = target_speed - current_speed
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        output = (self.kp * error +
                  self.ki * self.integral +
                  self.kd * derivative)

        # Anti-windup
        self.integral = max(-100, min(100, self.integral))

        return output
```

### MPC Controller

```python
class MPCController:
    def __init__(self, horizon=20, dt=0.1):
        self.horizon = horizon
        self.dt = dt

    def solve(self, state, trajectory, obstacles):
        # Formulate optimization problem
        problem = {
            "objective": self._build_objective(state, trajectory),
            "constraints": [
                self._kinematic_constraints(),
                self._dynamic_constraints(),
                self._obstacle_constraints(obstacles),
                self._input_constraints(),
            ],
            "initial_guess": self._warm_start(state, trajectory),
        }

        # Solve with OSQP / IPOPT
        solution = solve_qp(problem)

        return solution
```

## HD Map Integration

```python
from hd_map import HDMap, LaneGraph, Route

class MapService:
    def __init__(self, map_path):
        self.hd_map = HDMap.load(map_path)
        self.lane_graph = self.hd_map.get_lane_graph()

    def get_route(self, start, end):
        return self.lane_graph.find_route(start, end)

    def get_lane_information(self, position):
        lane = self.lane_graph.find_lane(position)
        if lane:
            return {
                "lane_id": lane.id,
                "lane_type": lane.type,
                "speed_limit": lane.speed_limit,
                "center_line": lane.center_line,
            }
        return None

    def get_nearby_features(self, position, radius_m=50):
        features = []
        features.extend(self.lane_graph.get_lanes_in_radius(position, radius_m))
        features.extend(self.hd_map.get_traffic_signs(position, radius_m))
        features.extend(self.hd_map.get_traffic_lights(position, radius_m))
        return features
```

## Detailed Test Scenarios

```python
from self_driving_vehicles import TestScenario, ScenarioBuilder

# Build test scenario
scenario = ScenarioBuilder("cut_in_avoidance") \
    .set_ego_vehicle(position=(0, 0), speed_kmh=60) \
    .add_lead_vehicle(position=(50, 0), speed_kmh=80) \
    .add_cut_in_vehicle(
        from_lane=1, to_lane=0,
        cut_in_position=30,
        cut_in_speed_kmh=50,
        trigger_time_s=5.0,
    ) \
    .set_weather("rain") \
    .set_duration_s(30) \
    .build()

# Run scenario
result = scenario.run(vehicle_system)

# Evaluate
assert result.no_collision, "Vehicle should avoid collision"
assert result.stay_in_lane, "Vehicle should stay in lane"
assert result.comfort_score > 0.7, "Ride should be comfortable"
assert result.speed_compliance, "Vehicle should obey speed limits"
```

## Contributing Guidelines

```bash
git clone https://github.com/company/self-driving-vehicles.git
cd self-driving-vehicles
pip install -e ".[dev]"
pytest tests/
```

### Code Review Checklist

- [ ] Safety-critical code reviewed by 2 senior engineers
- [ ] Unit test coverage > 80% for new code
- [ ] Integration tests pass in simulation
- [ ] No hardcoded values — all configurable
- [ ] Logging at appropriate levels
- [ ] Error handling for all failure modes
- [ ] Documentation updated

## License

Apache License 2.0

Copyright 2024 Company Name

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
