---
name: "manipulation"
category: "robotics"
version: "2.0.0"
tags: ["robotics", "manipulation", "grasping", "arm-control", "kinematics", "force-control", "pick-and-place"]
---

# Manipulation

## Overview

The Manipulation module provides the algorithms and infrastructure for robotic arm control, grasp planning, kinematics, dynamics, and task-space motion. It covers forward and inverse kinematics, trajectory generation, grasp analysis, force-controlled manipulation, visual servoing, and task sequencing for pick-and-place, assembly, and tool-use applications.

Robotic manipulation is the bridge between perception and the physical world. A manipulation system must convert high-level task goals into joint-space commands, plan collision-free paths through cluttered environments, execute grasps with appropriate force, and verify success through sensing. This module provides production-grade components for each stage of the manipulation pipeline, from raw joint commands to high-level task state machines.

The module is designed for both fixed-base industrial arms (6-DOF and 7-DOF) and mobile manipulators (arm mounted on a mobile base). It supports serial manipulators, parallel mechanisms, and redundant arms. The kinematics engine uses standard DH parameters and supports custom robot definitions via URDF or YAML configuration. Force control is integrated throughout, enabling compliant interaction with uncertain environments — essential for assembly, polishing, and human-robot collaboration.

## Core Capabilities

- **Forward Kinematics** — Compute end-effector pose from joint angles using DH parameters. Supports arbitrary kinematic chains with tool frame transformations.
- **Inverse Kinematics** — Analytical and numerical IK solvers for 6-DOF and 7-DOF arms. Includes null-space optimization for redundant manipulators.
- **Trajectory Generation** — cubic and quintic polynomial trajectories, trapezoidal velocity profiles, and via-point trajectories. Ensures continuity of position, velocity, and acceleration.
- **Grasp Planning** — antipodal grasp synthesis, grasp quality metrics (wrench space, epsilon quality), and approach vector selection. Generates ranked grasp candidates with fallback.
- **Force Control** — impedance control, admittance control, force-torque sensing, and contact detection. Essential for tasks with uncertain contact geometry.
- **Collision Detection** — self-collision checking and environment collision avoidance using signed distance fields and convex hull decomposition.
- **Visual Servoing** — eye-in-hand and eye-to-hand visual servo control. Combines pose estimation with Jacobian-based control for precise alignment.
- **Task Sequencing** — state-machine-based task decomposition for pick-and-place, assembly, and tool-use. Supports conditional transitions, retry logic, and error recovery.
- **Gripper Control** — parallel-jaw and multi-finger gripper abstraction with force and position control modes. Supports adaptive and underactuated grippers.
- **Dynamics** — inverse dynamics for torque control, gravity compensation, and friction modeling. Enables compliant and compliant-feel interactions.

## Usage Examples

### Forward and Inverse Kinematics

```python
from manipulation import RobotArm, DHParameters, JointAngles

dh = DHParameters(
    d=[0.333, 0, 0.316, 0, 0.384, 0, 0.107],
    a=[0, 0, 0, 0.0825, -0.0825, 0, 0],
    alpha=[0, -90, 90, 90, -90, 90, 0],
)

arm = RobotArm(name="panda", dh_params=dh, num_joints=7)
joint_angles = JointAngles(values=[0.0, -0.5, 0.0, -2.0, 0.0, 1.5, 0.785])

# Forward kinematics
ee_pose = arm.forward_kinematics(joint_angles)
print(f"End-effector position: {ee_pose.position}")
print(f"End-effector orientation: {ee_pose.orientation}")

# Inverse kinematics
target = ee_pose
solution = arm.inverse_kinematics(target)
print(f"IK solution: {solution.values}")
```

### Trajectory Generation

```python
from manipulation import TrajectoryGenerator, TrajectoryConfig

traj_gen = TrajectoryGenerator(config=TrajectoryConfig(
    max_velocity=1.0,
    max_acceleration=2.0,
    time_step=0.001,
))

waypoints = [
    JointAngles(values=[0.0, -0.5, 0.0, -2.0, 0.0, 1.5, 0.785]),
    JointAngles(values=[0.5, -0.3, 0.2, -1.5, 0.1, 1.2, 0.5]),
    JointAngles(values=[0.3, 0.0, -0.1, -1.8, -0.2, 1.0, 0.3]),
]

trajectory = traj_gen.generate(waypoints)
print(f"Trajectory: {trajectory.num_points} points, {trajectory.duration_s:.2f} s")
```

### Grasp Planning

```python
from manipulation import GraspPlanner, GraspConfig, ObjectGeometry

planner = GraspPlanner(config=GraspConfig(
    approach_distance=0.1,
    pre_grasp_distance=0.05,
    force_threshold_n=20.0,
))

box = ObjectGeometry(
    shape="box",
    dimensions=(0.1, 0.15, 0.08),
    center=(0.5, 0.3, 0.04),
)

grasps = planner.plan_grasps(box)
for i, grasp in enumerate(grasps):
    print(f"Grasp {i}: approach={grasp.approach_vector}, quality={grasp.quality_score:.3f}")
```

### Force-Controlled Manipulation

```python
from manipulation import ForceController, ForceTarget

controller = ForceController(
    kp=50.0,
    kd=5.0,
    ki=0.1,
    force_limit_n=30.0,
)

target = ForceTarget(
    desired_force=(0.0, 0.0, -10.0),
    desired_torque=(0.0, 0.0, 0.0),
)

# In a control loop:
# cmd = controller.compute(current_force_torque, target, dt=0.001)
```

### Pick-and-Place Task

```python
from manipulation import PickPlaceTask, TaskState

task = PickPlaceTask(
    pick_location=(0.4, 0.2, 0.05),
    place_location=(0.4, -0.2, 0.05),
    object_width=0.08,
    approach_height=0.15,
)

task.start()
while task.state != TaskState.COMPLETED:
    cmd = task.step()
    print(f"Task state: {task.state.value}, command: {cmd}")
```

### Assembly Task with Force Feedback

```python
from manipulation import AssemblyTask, InsertionConfig, ForceMonitor

insertion = InsertionConfig(
    peg_diameter_mm=10.0,
    hole_diameter_mm=10.2,
    insertion_depth_mm=15.0,
    search_force_n=5.0,
    insertion_force_n=20.0,
    spiral_search_radius_mm=2.0,
)

assembly = AssemblyTask(config=insertion, force_monitor=ForceMonitor())

# Spiral search for hole alignment
assembly.search_phase()
# Force-controlled insertion
assembly.insert_phase()
print(f"Assembly complete: {assembly.result}")
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Task Sequencer (FSM)                     │
│  (pick, place, assemble, tool-use, error recovery)       │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Motion Planner                           │
│  (trajectory generation, via-points, collision-free)     │
└──────────┬───────────────────────┬──────────────────────┘
           │                       │
┌──────────▼──────────┐  ┌────────▼──────────────────────┐
│  Kinematics Engine  │  │     Grasp Planner              │
│  (FK, IK, Jacobian) │  │  (synthesis, quality, approach)│
└──────────┬──────────┘  └────────┬──────────────────────┘
           │                       │
┌──────────▼───────────────────────▼──────────────────────┐
│                  Force / Impedance Controller             │
│  (torque commands, contact detection, compliance)        │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Robot Driver Interface                       │
│  (joint commands, gripper commands, F/T sensor read)     │
└─────────────────────────────────────────────────────────┘
```

The manipulation pipeline processes high-level task commands through the task sequencer, which decomposes them into motion primitives. Each motion primitive generates a trajectory, which the kinematics engine converts to joint commands. Force control operates at the lowest level, modulating joint torques based on contact feedback. This layered architecture allows each component to be tested and tuned independently.

## Best Practices

1. **Always check joint limits before commanding motion.** Exceeding joint limits can damage the robot. Validate every trajectory point against the URDF-specified limits. Include margin for encoder noise and calibration error.
2. **Use smooth trajectories.** Abrupt motion causes vibrations, tracking errors, and wear. Quintic polynomial trajectories ensure continuity of position, velocity, and acceleration. Limit jerk to prevent mechanical stress.
3. **Implement force control for contact tasks.** Position control alone cannot handle uncertain contact geometry. Impedance control provides compliant interaction with the environment. Tune stiffness and damping for the task.
4. **Plan grasps with multiple candidates.** The best grasp may be unreachable or colliding. Generate a ranked set of grasp candidates and fall back through the list. Replan if all grasps fail.
5. **Verify grasp success.** Never assume a grasp succeeded. Use gripper encoder feedback, force-torque sensing, or vision to confirm the object is held before moving. Implement retry logic for failed grasps.
6. **Use approach vectors aligned with the surface normal.** Grasping perpendicular to a surface is more stable than approaching at an angle. Compute approach vectors from the object's surface geometry or depth map.
7. **Implement collision avoidance at the trajectory level.** Don't rely on reactive collision avoidance alone. Pre-plan collision-free paths using RRT or PRM planners. Check self-collision at every trajectory point.
8. **Calibrate the tool center point (TCP).** The TCP definition directly affects positioning accuracy. Calibrate it with a known reference point before operation. Recalibrate after changing end-effectors.
9. **Handle singularities gracefully.** Near kinematic singularities, small Cartesian motions require large joint velocities. Detect singularity conditions and switch to damped least-squares IK or restrict motion to well-conditioned directions.
10. **Use simulation for development.** Manipulation tasks involve contact, friction, and collision — all hard to debug on real hardware. Develop and test in a physics simulator (PyBullet, MuJoCo, Isaac) before deploying.

## Performance Considerations

- **IK solve time**: Numerical IK solvers converge in 5-50 iterations (1-10 ms). Analytical solvers are sub-millisecond but only work for specific kinematic chains. Use analytical solvers for 6-DOF industrial arms.
- **Trajectory computation**: Quintic polynomial trajectories for 100 waypoints compute in <1 ms. Collision checking is the bottleneck — use bounding volume hierarchies (BVH) for fast rejection.
- **Grasp planning**: Antipodal grasp synthesis on a mesh with 10K faces takes 10-100 ms. Pre-compute grasp libraries for known objects and use lookup for real-time performance.
- **Force control loop rate**: Impedance control requires 500-1000 Hz for stable contact interaction. Use real-time operating systems or dedicated force control hardware for this loop rate.
- **Collision checking**: Environment collision with signed distance fields queries in O(1) per point. Self-collision with convex decomposition requires O(N^2) pair checks — precompute the collision matrix.
- **Visual servoing**: Feature-based visual servoing runs at camera frame rate (30-60 Hz). The Jacobian computation and control update take 1-5 ms. Use GPU-accelerated feature detection for the full pipeline.

## Security Considerations

- **Workspace limits**: Enforce Cartesian workspace boundaries in hardware. A compromised motion planner should not be able to command the arm outside the safe workspace. Use hard limits, not just software checks.
- **Speed and force limits**: Set maximum joint velocities, accelerations, and force limits appropriate for human-robot collaboration. These limits must be enforced at the controller level, not just in the planner.
- **Emergency stop**: The E-stop must be hardware-wired and independent of software. It should cut power to the joints and engage brakes. Test E-stop regularly.
- **Payload verification**: Verify the payload matches expectations before manipulation. Unexpected weight can cause loss of control. Use force-torque sensing to detect payload anomalies.
- **Access control**: Manipulation commands should be authenticated. Unauthorized arm commands in a shared workspace pose physical safety risks. Implement command signing for networked robots.
- **Secure calibration data**: Robot calibration parameters (DH, TCP, joint offsets) directly affect positioning accuracy. Tampering with calibration can cause collisions. Store calibration data with integrity checks.

## Related Modules

- **robotics-vision** — Visual servoing and object pose estimation for grasp targeting
- **autonomous-systems** — Mission planning that sequences manipulation tasks
- **navigation** — Base positioning and mobile manipulation
- **swarm-robotics** — Cooperative manipulation by multiple arms

## References

- Siciliano, B., Sciavicco, L., Villani, L., & Oriolo, G. (2009). *Robotics: Modelling, Planning and Control*. Springer.
- Murray, R. M., Li, Z., & Sastry, S. S. (1994). *A Mathematical Introduction to Robotic Manipulation*. CRC Press.
- Mahler, J. et al. (2017). Dex-Net 2.0: Deep learning to plan robust grasps with synthetic point clouds and analytic grasp metrics. *RSS*.
- Hogan, N. (1985). Impedance control: An approach to manipulation. *ASME Journal of Dynamic Systems*, 107(1), 1-24.
- Kavraki, L. E., Svestka, P., Latombe, J.-C., & Overmars, M. H. (1996). Probabilistic roadmaps for path planning in high-dimensional configuration spaces. *IEEE Trans. RA*, 12(4), 566-580.
- MoveIt! Motion Planning Framework: https://moveit.ros.org/
- PyBullet Physics Simulation: https://pybullet.org/
- Franka Emika Robot Interface: https://frankaemika.github.io/docs/

## Advanced Grasp Planning Algorithms

### Antipodal Grasp Synthesis

Antipodal grasps are the foundation of parallel-jaw grasping. Given an object mesh with surface normals, the algorithm searches for pairs of points where the surface normals at both contact points are approximately antiparallel and aligned with the gripper closing axis.

```python
from manipulation import AntipodalGraspSynthesizer, MeshObject

synthesizer = AntipodalGraspSynthesizer(
    angle_threshold_deg=15.0,
    friction_coefficient=0.6,
    max_grasp_candidates=100,
)

obj = MeshObject.from_file("object.stl")
candidates = synthesizer.synthesize(obj)

for grasp in candidates[:5]:
    print(f"Contact 1: {grasp.contact_points[0]}")
    print(f"Contact 2: {grasp.contact_points[1]}")
    print(f"Approach: {grasp.approach_vector}")
    print(f"Epsilon quality: {grasp.epsilon_quality:.4f}")
```

### Grasp Quality Metrics

The wrench space quality metric measures the smallest wrench the grasp can resist. A higher epsilon quality indicates a more robust grasp.

```
Grasp Wrench Space (GWS):
  Given contact points {c_1, ..., c_k} and contact normals {n_1, ...n_k}:
  
  For each contact i with friction cone half-angle phi:
    Generate m friction cone approximations:
      f_ij = mu * cos(phi) * n_i + sin(phi) * t_ij  (j = 1..m)
      w_ij = [f_ij; c_i × f_ij]  (6D wrench)
    
  GWS = convex hull of all w_ij
  
  Epsilon quality = max r such that B(0, r) ⊂ GWS
  where B(0, r) is the ball of radius r centered at origin
```

```python
from manipulation import WrenchSpaceAnalyzer

analyzer = WrenchSpaceAnalyzer(friction_coefficient=0.6, num_friction_cones=8)

for grasp in candidates:
    wrench_space = analyzer.compute_gws(grasp.contact_points, grasp.contact_normals)
    epsilon = analyzer.epsilon_quality(wrench_space)
    volume = analyzer.volume(wrench_space)
    grasp.quality_score = epsilon
```

### Grasp Planning with Object Uncertainty

When object pose is uncertain, robust grasp planning considers the distribution of possible object poses and maximizes expected quality.

```python
from manipulation import RobustGraspPlanner, PoseDistribution

robust_planner = RobustGraspPlanner(
    base_planner=synthesizer,
    num_pose_samples=100,
    quality_threshold=0.01,
)

# Object pose distribution from perception
pose_dist = PoseDistribution(
    mean_pose=estimated_pose,
    covariance=pose_uncertainty,
)

robust_grasps = robust_planner.plan(obj, pose_dist)
for grasp in robust_grasps:
    print(f"Expected quality: {grasp.expected_quality:.4f}, "
          f"Worst-case: {grasp.worst_case_quality:.4f}")
```

### Grasp Selection Pipeline

The full grasp selection pipeline combines synthesis, scoring, reachability checking, and collision detection to produce executable grasp candidates.

```python
from manipulation import GraspSelectionPipeline, ReachabilityChecker

pipeline = GraspSelectionPipeline(
    synthesizer=synthesizer,
    quality_scorer=WrenchSpaceAnalyzer(friction_coefficient=0.6),
    reachability_checker=ReachabilityChecker(arm, joint_limits=True),
    collision_checker=collision_env,
    max_candidates=50,
    top_k=5,
)

selected = pipeline.select(obj, camera_pose)
for i, grasp in enumerate(selected):
    print(f"Rank {i}: quality={grasp.quality_score:.4f}, "
          f"reachable={grasp.reachable}, collision_free={grasp.collision_free}")
```

## Force Control Deep Dive

### Impedance Control Theory

Impedance control regulates the relationship between end-effector position and contact force. The desired behavior is modeled as a mass-spring-damper system:

```
M_d * (ẍ - ẍ_d) + B_d * (ẋ - ẋ_d) + K_d * (x - x_d) = F_ext

Where:
  M_d = desired inertia matrix (6x6)
  B_d = desired damping matrix (6x6)
  K_d = desired stiffness matrix (6x6)
  x_d = desired trajectory
  F_ext = measured external force/torque
  
Joint-space impedance:
  τ = M(q) * J⁻¹ * (ẍ_d - J̇ * q̇) + C(q, q̇) * q̇ + g(q) 
      + J^T * (M_d * ë + B_d * ė + K_d * e)
  
  where e = x_d - x is the pose error
```

### Admittance Control

Admittance control is the dual of impedance control — it takes force input and produces motion output. Useful when the robot has good position control but needs compliant behavior.

```python
from manipulation import AdmittanceController, AdmittanceParams

controller = AdmittanceController(params=AdmittanceParams(
    mass_d=5.0,
    damping_d=50.0,
    stiffness_d=200.0,
    force_filter_cutoff_hz=10.0,
    position_gain=100.0,
))

# Control loop at 1 kHz
for step in range(num_steps):
    measured_force = ft_sensor.read()
    desired_force = force_target.get()
    
    accel = controller.compute_acceleration(measured_force, desired_force)
    velocity = controller.integrate_velocity(accel, dt=0.001)
    position_cmd = controller.integrate_position(velocity, dt=0.001)
    
    robot.set_joint_positions(position_cmd)
```

### Hybrid Force/Position Control

For tasks requiring simultaneous position and force control along different directions (e.g., polishing, wiping), hybrid control decomposes the task space into force-controlled and position-controlled directions.

```
Task Space Decomposition:
  S = selection matrix (6x6, diagonal)
  S_ij = 1 if axis j is force-controlled
  S_ij = 0 if axis j is position-controlled
  
Control Law:
  τ = J^T * (S * F_desired + (I - S) * (K_p * e_p + K_d * ė_p))
      + gravity_compensation + coriolis_compensation
```

```python
from manipulation import HybridForcePositionController

hfp = HybridForcePositionController(
    arm=robot,
    selection_matrix=[0, 0, 1, 0, 0, 0],  # force control only in Z
    force_gain=0.5,
    position_gain=[100, 100, 0, 200, 200, 200],  # position in XY and orientation
)

target_force_z = -15.0  # 15N downward
for step in range(num_steps):
    cmd = hfp.step(
        measured_force_torque=ft_sensor.read(),
        desired_force_z=target_force_z,
        desired_position=polishing_trajectory[step],
    )
    robot.set_joint_torques(cmd)
```

## Assembly Task Algorithms

### Peg-in-Hole Insertion

The classic peg-in-hole assembly problem requires searching for the hole, aligning the peg, and inserting with force control.

```python
from manipulation import PegInHoleTask, InsertionPhase

task = PegInHoleTask(
    peg_diameter_mm=8.0,
    hole_diameter_mm=8.1,
    insertion_depth_mm=20.0,
    compliance_radius_mm=0.5,
)

# Phase 1: Search — spiral pattern to find the hole
task.set_phase(InsertionPhase.SEARCH)
task.configure_spiral(
    max_radius_mm=3.0,
    step_size_mm=0.2,
    search_force_n=2.0,
)

# Phase 2: Align — use force feedback to center the peg
task.set_phase(InsertionPhase.ALIGN)
task.configure_alignment(
    force_threshold_n=5.0,
    position_correction_gain=0.1,
)

# Phase 3: Insert — force-controlled insertion
task.set_phase(InsertionPhase.INSERT)
task.configure_insertion(
    max_insertion_force_n=25.0,
    target_depth_mm=15.0,
    depth_tolerance_mm=0.5,
)

result = task.execute()
print(f"Assembly: {result.success}, depth={result.inserted_depth_mm:.2f}mm, "
      f"force={result.peak_force_n:.1f}N")
```

### Dual-Arm Coordination

Dual-arm manipulation requires synchronized trajectory execution, relative pose maintenance, and coordinated force control.

```python
from manipulation import DualArmCoordinator, ArmPair, CoordinationMode

coordinator = DualArmCoordinator(
    arms=ArmPair(left=left_arm, right=right_arm),
    coordination_mode=CoordinationMode.SYNCHRONIZED,
    max_relative_position_error_mm=2.0,
    max_relative_orientation_error_deg=5.0,
)

# Define cooperative task
task = coordinator.create_cooperative_task(
    object_pose=box_pose,
    grasp_config_left=left_grasp,
    grasp_config_right=right_grasp,
    transport_velocity=0.2,
)

# Execute coordinated transport
for step in task.trajectory():
    left_cmd, right_cmd = coordinator.compute_commands(step)
    left_arm.set_joint_positions(left_cmd)
    right_arm.set_joint_positions(right_cmd)
```

### Dual-Arm Force Coordination

When two arms share a load, force distribution must be managed to prevent one arm from bearing excessive load.

```python
from manipulation import DualArmForceController

force_ctrl = DualArmForceController(
    left_arm=left_arm,
    right_arm=right_arm,
    force_distribution_method="proportional",
    max_force_per_arm_n=30.0,
    force_balance_tolerance_n=5.0,
)

load_mass_kg = 2.0
gravity_force = load_mass_kg * 9.81
desired_total_force = -gravity_force  # upward

for step in range(num_steps):
    left_force, right_force = force_ctrl.distribute(
        total_force_z=desired_total_force,
        left_position=left_arm.get_end_effector_pose(),
        right_position=right_arm.get_end_effector_pose(),
    )
    
    left_cmd = force_ctrl.compute(left_force, left_arm.read_force_torque())
    right_cmd = force_ctrl.compute(right_force, right_arm.read_force_torque())
    
    left_arm.set_joint_torques(left_cmd)
    right_arm.set_joint_torques(right_cmd)
```

## Tool Use and End-Effector Control

### Tool Center Point Management

The TCP defines the point that the robot positions in Cartesian space. Different tools require different TCP definitions.

```python
from manipulation import TCPManager, ToolDefinition

tcp_manager = TCPManager(arm=robot)

# Define a screwdriver tool
screwdriver = ToolDefinition(
    name="screwdriver",
    tcp_offset=(0.0, 0.0, 0.15),  # 150mm from flange
    tcp_orientation=(0, 0, 0),
    mass_kg=0.3,
    inertia_tensor=(0.001, 0.001, 0.0005),
    grip_force_n=10.0,
)

tcp_manager.register_tool(screwdriver)
tcp_manager.select_tool("screwdriver")

# Now all Cartesian commands are relative to the tool tip
robot.move_to_cartesian(target_pose)  # positions the screwdriver tip
```

### Tool Change Sequence

```python
from manipulation import ToolChanger, ToolStation

changer = ToolChanger(
    stations=[
        ToolStation(id="s1", position=(0.4, 0.3, 0.1), tool="gripper"),
        ToolStation(id="s2", position=(0.4, -0.3, 0.1), tool="screwdriver"),
        ToolStation(id="s3", position=(0.4, 0.0, 0.1), tool="wrench"),
    ],
)

# Execute tool change
result = changer.change_tool(from_tool="gripper", to_tool="screwdriver")
print(f"Tool change: {result.success}, time={result.duration_s:.1f}s")
print(f"Current tool: {changer.active_tool}")
```

### Gripper Force Optimization

Optimal grip force balances secure holding against object damage.

```
Minimum grip force for secure hold:
  F_min = m * (a_max + g) / (2 * mu * cos(theta))
  
  where:
    m = object mass (kg)
    a_max = maximum acceleration (m/s²)
    g = gravitational acceleration (9.81 m/s²)
    mu = friction coefficient
    theta = angle between gripper normal and gravity
  
Maximum safe grip force:
  F_max = object_yield_force / safety_factor
  
  safety_factor typically 2-5 depending on object fragility
```

```python
from manipulation import GripForceOptimizer

optimizer = GripForceOptimizer(
    friction_coefficient=0.5,
    safety_factor=3.0,
    acceleration_budget=5.0,
)

force = optimizer.compute(
    object_mass_kg=0.5,
    object_yield_force_n=50.0,
    grip_angle_deg=0.0,
    lifting_acceleration=2.0,
)

print(f"Optimal grip force: {force.optimal_n:.1f}N "
      f"(min={force.minimum_n:.1f}N, max={force.maximum_n:.1f}N)")
```

## Kinematics Deep Dive

### Jacobian Computation

The geometric Jacobian relates joint velocities to end-effector velocities. It is essential for force control, singularity analysis, and manipulability computation.

```python
from manipulation import JacobianComputer

jac_comp = JacobianComputer(arm=robot)

# Compute full 6xN Jacobian
J = jac_comp.compute_geometric(joint_angles)
print(f"Jacobian shape: {J.shape}")

# Singularity analysis via manipulability index
w = jac_comp.manipulability_index(J)
print(f"Manipulability: {w:.4f}")

# Compute condition number for isotropy analysis
cond = jac_comp.condition_number(J)
print(f"Condition number: {cond:.2f}")

# Null-space projection for redundancy resolution
null_space = jac_comp.null_space(J)
print(f"Null-space dimension: {null_space.shape[1]}")
```

### Redundancy Resolution

For 7-DOF arms, the null space of the Jacobian provides extra degrees of freedom that can be used for secondary objectives (singularity avoidance, joint limit avoidance, obstacle avoidance).

```python
from manipulation import NullSpaceOptimizer

ns_optimizer = NullSpaceOptimizer(
    arm=robot,
    primary_task="cartesian_tracking",
    secondary_tasks=[
        "joint_limit_avoidance",
        "singularity_avoidance",
        "elbow_manipulability",
    ],
    task_weights=[1.0, 0.5, 0.3, 0.2],
)

for step in range(num_steps):
    cmd = ns_optimizer.solve(
        desired_cartesian_velocity=cart_vel[step],
        current_joint_angles=joint_angles,
    )
    robot.set_joint_velocities(cmd)
```

## Trajectory Optimization

### Time-Optimal Path Following

Given a geometric path, time-optimal trajectory generation finds the fastest execution that respects velocity, acceleration, and torque limits.

```python
from manipulation import TOPPRAPlanner, PathConstraints

path = robot.compute_cartesian_path(waypoints, resolution=0.01)
constraints = PathConstraints(
    max_joint_velocities=robot.get_velocity_limits(),
    max_joint_accelerations=robot.get_acceleration_limits(),
    max_joint_torques=robot.get_torque_limits(),
)

toppra = TOPPRAPlanner()
trajectory = toppra.plan(path, constraints)

print(f"Optimal duration: {trajectory.duration_s:.3f}s")
print(f"Velocity profile: {trajectory.velocity_profile.shape}")
```

### Obstacle-Avoiding Trajectory Optimization

CHOMP (Covariant Hamiltonian Optimization for Motion Planning) and TrajOpt optimize trajectories to minimize a cost function combining smoothness and obstacle distance.

```python
from manipulation import TrajOptPlanner, ObstacleCost, SmoothnessCost

trajopt = TrajOptPlanner(arm=robot, num_waypoints=50)

trajopt.set_costs([
    ObstacleCost(sdf_environment, weight=1.0, safety_margin=0.02),
    SmoothnessCost(weight=0.1),
    JointLimitCost(weight=0.5),
])

trajopt.set_initial_trajectory(linear_interpolation(start, goal, n=50))
optimized = trajopt.optimize(max_iterations=100, convergence_threshold=1e-4)

print(f"Cost: {optimized.total_cost:.4f}")
print(f"Min obstacle distance: {optimized.min_obstacle_distance:.4f}m")
```

## Calibration and Accuracy

### Kinematic Calibration

DH parameters from the manufacturer are approximate. Kinematic calibration uses measured data to identify more accurate parameters.

```python
from manipulation import KinematicCalibrator, CalibrationPose

calibrator = KinematicCalibrator(
    arm=robot,
    measurement_type="laser_tracker",
    dh_nominal=robot.get_dh_parameters(),
)

# Collect calibration data
calibration_poses = [
    CalibrationPose(joint_angles=q, measured_ee_pose=p)
    for q, p in calibration_measurements
]

calibrated_dh = calibrator.calibrate(
    measurements=calibration_poses,
    optimize_for=["d", "a", "alpha", "joint_offset"],
    regularization_weight=0.01,
)

robot.set_dh_parameters(calibrated_dh)

# Evaluate improvement
error_before = calibrator.evaluate_error(robot.get_dh_parameters(), measurements)
error_after = calibrator.evaluate_error(calibrated_dh, measurements)
print(f"RMS error: {error_before:.4f}m -> {error_after:.4f}m")
```

### Online Calibration Refinement

During operation, small drifts can be corrected using vision-based measurements.

```python
from manipulation import OnlineCalibrator

online_cal = OnlineCalibrator(
    arm=robot,
    vision_system=apriltag_detector,
    learning_rate=0.01,
    correction_limit=0.001,
)

for step in range(num_steps):
    robot.move_to_calibration_pose()
    tag_pose = apriltag_detector.detect()
    
    correction = online_cal.update(tag_pose)
    if correction.magnitude > 0.0001:
        print(f"TCP correction: {correction}")
        robot.apply_tcp_correction(correction)
```

## Simulation and Debugging

### Physics Simulation Integration

```python
from manipulation import SimBridge, SimConfig

sim = SimBridge(config=SimConfig(
    physics_engine="mujoco",
    timestep=0.002,
    gravity=(0, 0, -9.81),
    render_enabled=True,
))

# Load robot and environment
sim.load_robot("panda.urdf")
sim.load_object("box.obj", position=(0.5, 0.3, 0.05))

# Simulate grasping
sim.step()
robot_state = sim.get_robot_state()
object_state = sim.get_object_state("box")
contact = sim.get_contacts("gripper", "box")
print(f"Contact force: {contact.force}")
```

### Debugging Visualization

```python
from manipulation import ManipulationDebugger

debugger = ManipulationDebugger(arm=robot)

# Visualize robot state
debugger.plot_robot(joint_angles)
debugger.plot_jacobian(J, singularity_threshold=0.01)

# Visualize grasp candidates
debugger.plot_grasps(candidates, object_mesh=obj)

# Visualize trajectory
debugger.plot_trajectory(trajectory, show_velocities=True, show_accelerations=True)

# Record animation
debugger.record_trajectory(trajectory, filename="grasp_demo.mp4", fps=30)
```

## Error Recovery Strategies

### Grasp Failure Recovery

```python
from manipulation import GraspRecoveryStrategy, RecoveryAction

strategy = GraspRecoveryStrategy(
    max_retries=3,
    actions=[
        RecoveryAction.REGRASP,
        RecoveryAction.REORIENT_OBJECT,
        RecoveryAction.RETREAT_AND_RETRY,
        RecoveryAction.REQUEST_HUMAN_HELP,
    ],
)

for attempt in range(strategy.max_retries):
    result = try_grasp(object_pose)
    if result.success:
        break
    
    recovery = strategy.next_recovery(result.failure_reason)
    print(f"Attempt {attempt}: {recovery.action.value}")
    execute_recovery(recovery)
```

### Motion Execution Recovery

```python
from manipulation import MotionRecoveryHandler

handler = MotionRecoveryHandler(arm=robot)

# Monitor execution
try:
    for cmd in trajectory.commands():
        robot.execute(cmd)
except JointLimitException as e:
    handler.handle_joint_limit(e)
except CollisionException as e:
    handler.handle_collision(e)
except SingularPointException as e:
    handler.handle_singularity(e)
except ExecutionTimeoutException as e:
    handler.handle_timeout(e)
```

## Multi-Finger Grasp Planning

### Envelope Grasp Synthesis

For multi-finger hands, envelope grasps wrap all fingers around the object for maximum contact area.

```python
from manipulation import MultiFingerGraspPlanner, HandModel

hand = HandModel(
    num_fingers=3,
    finger_lengths=[0.08, 0.06, 0.04],
    palm_width=0.1,
    max_joint_torques=[1.0, 0.8, 0.6],
)

planner = MultiFingerGraspPlanner(hand=hand)
grasps = planner.plan_envelope(
    object_mesh=obj,
    num_finger_contacts=3,
    contact_force_per_finger=5.0,
)

for grasp in grasps:
    print(f"Grasp type: {grasp.grasp_type}")
    print(f"Contact points: {len(grasp.contacts)}")
    print(f"Quality: {grasp.quality_score:.4f}")
```

### Power Grasp vs Precision Grasp Selection

```python
from manipulation import GraspTypeSelector

selector = GraspTypeSelector(
    object_weight_threshold_n=10.0,
    precision_task_threshold_mm=0.5,
)

for obj in objects_to_grasp:
    grasp_type = selector.select(
        object_mass=obj.mass_kg,
        object_size=obj.dimensions,
        task_requirement=obj.task,
    )
    
    if grasp_type == "power":
        grasps = power_planner.plan(obj)
    else:
        grasps = precision_planner.plan(obj)
    
    execute_best_grasp(grasps)
```

## Configuration Reference

### Robot Arm Configuration (YAML)

```yaml
robot:
  name: "panda"
  type: "serial_manipulator"
  num_joints: 7
  
  dh_parameters:
    d: [0.333, 0, 0.316, 0, 0.384, 0, 0.107]
    a: [0, 0, 0, 0.0825, -0.0825, 0, 0]
    alpha: [0, -90, 90, 90, -90, 90, 0]
  
  joint_limits:
    position_min: [-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973]
    position_max: [2.8973, 1.7628, 2.8973, -0.0698, 2.8973, 3.7525, 2.8973]
    velocity_max: [2.175, 2.175, 2.175, 2.175, 2.61, 2.61, 2.61]
    acceleration_max: [15.0, 7.5, 10.0, 12.5, 15.0, 20.0, 20.0]
    torque_max: [87.0, 87.0, 87.0, 87.0, 12.0, 12.0, 12.0]
  
  tool_center_point:
    offset: [0.0, 0.0, 0.107]
    orientation: [0, 0, 0]
  
  dynamics:
    mass: [4.97, 0.64, 3.22, 3.59, 2.71, 2.15, 0.45]
    center_of_mass: [[0, 0, -0.12], [0, 0, 0.01], [0, 0, -0.12],
                     [0.06, 0, -0.04], [0, 0, 0.06], [0, 0, -0.04], [0, 0, 0.02]]
```

### Force Controller Configuration

```yaml
force_control:
  controller_type: "impedance"
  
  impedance:
    mass: 5.0
    damping: 50.0
    stiffness: 200.0
  
  force_sensor:
    type: "ati_gamma"
    mount: "end_effector"
    noise_filter_cutoff_hz: 10.0
    bias_samples: 100
  
  safety:
    max_force_n: 50.0
    max_torque_nm: 5.0
    force_rate_limit_n_per_s: 100.0
    emergency_stop_force_n: 80.0
```

### Grasp Planner Configuration

```yaml
grasp_planning:
  synthesizer: "antipodal"
  
  antipodal:
    angle_threshold_deg: 15.0
    friction_coefficient: 0.6
    surface_sample_density: 1000
  
  quality_metrics:
    wrench_space:
      enabled: true
      friction_cones: 8
    approach_alignment:
      enabled: true
      weight: 0.3
  
  reachability:
    joint_limit_margin_deg: 5.0
    singularity_threshold: 0.05
    self_collision_margin_m: 0.02
  
  selection:
    top_k: 5
    min_quality: 0.01
    prefer_surface_normal: true
```
