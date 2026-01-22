"""
Robotics Pipeline
Autonomous systems and robotics
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from collections import deque


class RobotState(Enum):
    IDLE = "idle"
    MOVING = "moving"
    CHARGING = "charging"
    ERROR = "error"
    CALIBRATING = "calibrating"


@dataclass
class JointState:
    position: float
    velocity: float
    effort: float
    acceleration: float = 0.0


@dataclass
class Task:
    task_id: str
    task_type: str
    priority: int
    parameters: Dict = field(default_factory=dict)
    deadline: Optional[float] = None


class Kinematics:
    """Robot kinematics calculations"""
    
    def __init__(self, 
                 dh_params: List[Dict] = None,
                 num_joints: int = 6):
        self.num_joints = num_joints
        self.dh_params = dh_params or [
            {"a": 0, "d": 0.089, "alpha": -np.pi/2},
            {"a": 0.425, "d": 0, "alpha": 0},
            {"a": 0.392, "d": 0, "alpha": 0},
            {"a": 0, "d": 0.109, "alpha": np.pi/2},
            {"a": 0, "d": 0.095, "alpha": -np.pi/2},
            {"a": 0, "d": 0.082, "alpha": 0}
        ]
    
    def forward_kinematics(self, 
                          joint_positions: List[float]) -> np.ndarray:
        """Calculate end-effector position from joint angles"""
        T = np.eye(4)
        
        for i, (theta, dh) in enumerate(zip(joint_positions, self.dh_params)):
            a, d, alpha = dh["a"], dh["d"], dh["alpha"]
            
            c_theta = np.cos(theta)
            s_theta = np.sin(theta)
            c_alpha = np.cos(alpha)
            s_alpha = np.sin(alpha)
            
            T_i = np.array([
                [c_theta, -s_theta*c_alpha, s_theta*s_alpha, a*c_theta],
                [s_theta, c_theta*c_alpha, -c_theta*s_alpha, a*s_theta],
                [0, s_alpha, c_alpha, d],
                [0, 0, 0, 1]
            ])
            
            T = T @ T_i
        
        return T
    
    def inverse_kinematics(self, 
                          target_pose: np.ndarray,
                          initial_guess: List[float] = None) -> List[float]:
        """Calculate joint angles for target position"""
        guess = initial_guess or [0] * self.num_joints
        
        for _ in range(100):
            current_T = self.forward_kinematics(guess)
            error = self._pose_error(target_pose, current_T)
            
            if np.linalg.norm(error) < 1e-4:
                break
            
            jacobian = self._calculate_jacobian(guess)
            try:
                delta_theta = np.linalg.lstsq(jacobian, error, rcond=None)[0]
                guess = [t + 0.1 * d for t, d in zip(guess, delta_theta)]
            except:
                break
        
        return guess
    
    def _pose_error(self, target: np.ndarray, current: np.ndarray) -> np.ndarray:
        """Calculate pose error"""
        pos_error = target[:3, 3] - current[:3, 3]
        
        rotation_error = current[:3, :3].T @ target[:3, :3]
        rot_vec = self._rotation_to_vector(rotation_error)
        
        return np.concatenate([pos_error, rot_vec])
    
    def _rotation_to_vector(self, R: np.ndarray) -> np.ndarray:
        """Convert rotation matrix to rotation vector"""
        return np.array([R[2,1] - R[1,2], R[0,2] - R[2,0], R[1,0] - R[0,1]]) / 2
    
    def _calculate_jacobian(self, joint_positions: List[float]) -> np.ndarray:
        """Calculate Jacobian matrix"""
        J = np.zeros((6, self.num_joints))
        T = np.eye(4)
        
        for i in range(self.num_joints):
            if i > 0:
                T = T @ self._get_transform(joint_positions[i-1], i-1)
            
            o_n = T[:3, 3]
            z_axis = T[:3, 2]
            
            if i < self.num_joints - 1:
                T_next = self._get_transform(joint_positions[i], i)
                o_next = T_next[:3, 3]
            else:
                o_next = self.forward_kinematics(joint_positions)[:3, 3]
            
            J[:3, i] = np.cross(z_axis, o_next - o_n)
            J[3:, i] = z_axis
        
        return J
    
    def _get_transform(self, theta: float, i: int) -> np.ndarray:
        """Get DH transform"""
        dh = self.dh_params[i]
        a, d, alpha = dh["a"], dh["d"], dh["alpha"]
        
        c_theta = np.cos(theta)
        s_theta = np.sin(theta)
        c_alpha = np.cos(alpha)
        s_alpha = np.sin(alpha)
        
        return np.array([
            [c_theta, -s_theta*c_alpha, s_theta*s_alpha, a*c_theta],
            [s_theta, c_theta*c_alpha, -c_theta*s_alpha, a*s_theta],
            [0, s_alpha, c_alpha, d],
            [0, 0, 0, 1]
        ])


class PathPlanner:
    """Robot path planning"""
    
    def __init__(self, 
                 workspace_bounds: Dict = None,
                 obstacle_radius: float = 0.1):
        self.workspace_bounds = workspace_bounds or {
            "x": (-1, 1),
            "y": (-1, 1),
            "z": (0, 1)
        }
        self.obstacle_radius = obstacle_radius
        self.obstacles = []
    
    def plan_path(self, 
                 start: np.ndarray,
                 goal: np.ndarray,
                 obstacles: List[np.ndarray] = None) -> List[np.ndarray]:
        """Plan collision-free path using RRT"""
        obstacles = obstacles or []
        self.obstacles = obstacles
        
        tree = {tuple(start): None}
        path = [start]
        
        for _ in range(1000):
            random_point = self._sample_point()
            nearest = self._find_nearest(tree, random_point)
            new_point = self._steer(nearest, random_point)
            
            if not self._collision_check(nearest, new_point):
                tree[tuple(new_point)] = nearest
                
                if np.linalg.norm(new_point - goal) < 0.05:
                    path = self._reconstruct_path(tree, new_point)
                    path.append(goal)
                    return path
        
        return [start, goal]
    
    def _sample_point(self) -> np.ndarray:
        """Sample random point in workspace"""
        return np.array([
            np.random.uniform(*self.workspace_bounds["x"]),
            np.random.uniform(*self.workspace_bounds["y"]),
            np.random.uniform(*self.workspace_bounds["z"])
        ])
    
    def _find_nearest(self, tree: Dict, point: np.ndarray) -> np.ndarray:
        """Find nearest node in tree"""
        return np.array(list(tree.keys())[
            np.argmin([np.linalg.norm(np.array(k) - point) for k in tree.keys()])
        ])
    
    def _steer(self, from_point: np.ndarray, to_point: np.ndarray) -> np.ndarray:
        """Steer towards target"""
        direction = to_point - from_point
        distance = np.linalg.norm(direction)
        
        if distance > 0.1:
            direction = direction / distance * 0.1
        
        return from_point + direction
    
    def _collision_check(self, point1: np.ndarray, point2: np.ndarray) -> bool:
        """Check collision along line segment"""
        for obstacle in self.obstacles:
            for t in np.linspace(0, 1, 10):
                point = point1 + t * (point2 - point1)
                if np.linalg.norm(point - obstacle) < self.obstacle_radius:
                    return True
        return False
    
    def _reconstruct_path(self, tree: Dict, end: np.ndarray) -> List[np.ndarray]:
        """Reconstruct path from tree"""
        path = [end]
        current = tuple(end)
        
        while tree[current] is not None:
            path.append(np.array(current))
            current = tree[current]
        
        return list(reversed(path))


class TrajectoryGenerator:
    """Smooth trajectory generation"""
    
    def __init__(self):
        self.max_velocity = 0.5
        self.max_acceleration = 1.0
    
    def generate_trapezoidal(self,
                            start: float,
                            goal: float,
                            max_vel: float = None,
                            max_acc: float = None) -> Tuple[List[float], List[float], List[float]]:
        """Generate trapezoidal velocity profile"""
        max_vel = max_vel or self.max_velocity
        max_acc = max_acc or self.max_acceleration
        
        distance = abs(goal - start)
        t_acc = max_vel / max_acc
        d_acc = 0.5 * max_acc * t_acc**2
        
        if distance < 2 * d_acc:
            t_acc = np.sqrt(distance / max_acc)
            d_acc = 0.5 * max_acc * t_acc**2
        
        t_total = 2 * t_acc + (distance - 2 * d_acc) / max_vel
        
        times = [0]
        positions = [start]
        velocities = [0]
        
        for t in np.arange(0, t_total, 0.01):
            if t < t_acc:
                pos = start + 0.5 * max_acc * t**2
                vel = max_acc * t
            elif t < t_total - t_acc:
                pos = start + d_acc + max_vel * (t - t_acc)
                vel = max_vel
            else:
                t_dec = t - (t_total - t_acc)
                pos = goal - 0.5 * max_acc * (t_total - t)**2
                vel = max_acc * (t_total - t)
            
            times.append(t)
            positions.append(pos)
            velocities.append(vel)
        
        return times, positions, velocities


class RobotController:
    """Robot state machine and controller"""
    
    def __init__(self):
        self.state = RobotState.IDLE
        self.joint_states = []
        self.task_queue = deque()
        self.current_task = None
        self.emergency_stop = False
    
    def add_task(self, task: Task):
        """Add task to queue"""
        self.task_queue.append(task)
        self.task_queue = deque(sorted(self.task_queue, key=lambda t: t.priority))
    
    def execute_task(self, task: Task) -> bool:
        """Execute single task"""
        self.current_task = task
        self.state = RobotState.MOVING
        
        success = self._run_task_steps(task)
        
        if success:
            self.state = RobotState.IDLE
            self.current_task = None
        
        return success
    
    def _run_task_steps(self, task: Task) -> bool:
        """Run task execution steps"""
        return True
    
    def emergency_stop_active(self):
        """Activate emergency stop"""
        self.emergency_stop = True
        self.state = RobotState.ERROR
    
    def reset_emergency_stop(self):
        """Reset emergency stop"""
        self.emergency_stop = False
        self.state = RobotState.IDLE
    
    def get_status(self) -> Dict:
        """Get robot status"""
        return {
            "state": self.state.value,
            "emergency_stop": self.emergency_stop,
            "current_task": self.current_task.task_id if self.current_task else None,
            "queue_length": len(self.task_queue)
        }


if __name__ == "__main__":
    kinematics = Kinematics()
    planner = PathPlanner()
    trajectory = TrajectoryGenerator()
    controller = RobotController()
    
    joint_positions = [0.1, 0.2, 0.3, 0.1, 0.1, 0.1]
    pose = kinematics.forward_kinematics(joint_positions)
    
    start = np.array([0, 0, 0])
    goal = np.array([0.5, 0.5, 0.5])
    obstacles = [np.array([0.25, 0.25, 0.25])]
    path = planner.plan_path(start, goal, obstacles)
    
    times, positions, velocities = trajectory.generate_trapezoidal(0, 1.0)
    
    controller.add_task(Task("task1", "move", 1))
    status = controller.get_status()
    
    print(f"End-effector position: {pose[:3, 3]}")
    print(f"Path points: {len(path)}")
    print(f"Trajectory points: {len(times)}")
    print(f"Robot state: {status['state']}")
