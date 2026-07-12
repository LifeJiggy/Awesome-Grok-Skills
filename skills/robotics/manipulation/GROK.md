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
