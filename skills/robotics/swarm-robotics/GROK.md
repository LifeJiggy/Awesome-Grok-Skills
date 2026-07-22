---
name: "swarm-robotics"
category: "robotics"
version: "2.0.0"
tags: ["robotics", "swarm", "multi-agent", "emergent-behavior", "distributed-systems", "consensus", "flocking"]
---

# Swarm Robotics

## Overview

The Swarm Robotics module provides the algorithms and infrastructure for coordinating large numbers of simple robotic agents to achieve complex collective behaviors. Inspired by biological swarms — ant colonies, bee hives, bird flocks — swarm robotics replaces centralized control with local interaction rules that produce emergent global behavior. This module covers flocking algorithms, consensus protocols, stigmergic coordination, task allocation, and communication networking for robot swarms.

Swarm systems are defined by decentralization, scalability, robustness to individual failures, and self-organization. Each robot operates with local sensing and local communication, yet the collective achieves goals that no individual could accomplish alone. The module provides the building blocks for deploying swarms in search-and-rescue, environmental monitoring, precision agriculture, warehouse logistics, and entertainment applications. The algorithms are designed to scale from 5 agents to 10,000+ agents without architectural changes.

A key design principle is that no single agent has a complete picture of the swarm state. Coordination emerges from local interactions: agents share information with neighbors within communication range, and global patterns arise from the aggregation of local decisions. This makes the swarm inherently resilient — the loss of any individual agent (or even a large fraction) does not prevent the swarm from achieving its goals. The module provides tools for measuring and monitoring emergent behavior, tuning interaction parameters, and debugging collective phenomena.

## Core Capabilities

- **Flocking Algorithms** — Reynolds-style boids with separation, alignment, and cohesion rules. Supports custom weighting, perception radius limits, and boundary conditions.
- **Consensus Protocols** — Average consensus, leader election, and distributed agreement. Handles asynchronous communication, packet loss, and network partitions.
- **Stigmergic Coordination** — Pheromone-based trail following and digital stigmergy. Agents deposit and sense digital traces on a shared grid to coordinate without direct communication.
- **Task Allocation** — Market-based auction, response threshold, and token-based allocation. Agents bid on tasks based on capability, proximity, and current load.
- **Collision Avoidance** — Velocity obstacle and reciprocal velocity obstacle (RVO) methods. Ensures collision-free motion even in dense swarms.
- **Communication Networking** — Ad-hoc mesh networking, gossip protocols, and range-limited broadcast. Designed for unreliable, bandwidth-constrained channels.
- **Formation Control** — Virtual structure, leader-follower, and behavior-based formation. Supports dynamic reconfiguration and fault-tolerant formations.
- **Swarm Intelligence Optimization** — Particle swarm optimization (PSO), ant colony optimization (ACO) for distributed search and optimization problems.
- **Scalability Testing** — Performance metrics for swarm size, communication load, and task throughput. Includes benchmarking tools for measuring emergent behavior quality.
- **Emergence Monitoring** — Real-time metrics for cohesion, entropy, alignment, and task completion rate. Visualize swarm behavior as it evolves.

## Usage Examples

### Flocking Simulation

```python
from swarm_robotics import SwarmSimulator, Agent, FlockingConfig

config = FlockingConfig(
    separation_weight=1.5,
    alignment_weight=1.0,
    cohesion_weight=1.0,
    perception_radius=5.0,
    max_speed=2.0,
)

sim = SwarmSimulator(config=config)
for i in range(50):
    sim.add_agent(Agent(agent_id=i, position=(random.uniform(-10, 10), random.uniform(-10, 10))))

for step in range(1000):
    sim.step(dt=0.1)
    if step % 100 == 0:
        print(f"Step {step}: center={sim.get_swarm_center()}, cohesion={sim.get_cohesion_metric():.3f}")
```

### Consensus-Based Leader Election

```python
from swarm_robotics import ConsensusProtocol, AgentState

protocol = ConsensusProtocol(protocol_type="leader_election")
agents = [AgentState(agent_id=i, value=float(i)) for i in range(20)]

for round in range(100):
    agents = protocol.step(agents, neighbors_fn=protocol.random_neighbors)
    if protocol.has_converged(agents):
        leader = max(agents, key=lambda a: a.value)
        print(f"Leader elected: agent {leader.agent_id} (value={leader.value:.4f})")
        break
```

### Task Allocation via Auction

```python
from swarm_robotics import TaskAllocator, Task, RobotCapability

allocator = TaskAllocator(allocation_type="auction")
tasks = [
    Task(task_id="t1", required_capability=RobotCapability.SENSOR, priority=1.0),
    Task(task_id="t2", required_capability=RobotCapability.TRANSPORT, priority=0.8),
    Task(task_id="t3", required_capability=RobotCapability.SENSOR, priority=0.5),
]

assignments = allocator.allocate(tasks, robot_positions={0: (0, 0), 1: (5, 3), 2: (10, 1)})
for robot_id, task_list in assignments.items():
    print(f"Robot {robot_id}: {[t.task_id for t in task_list]}")
```

### Pheromone-Based Trail Following

```python
from swarm_robotics import PheromoneGrid, PheromoneType

grid = PheromoneGrid(width=100, height=100, resolution=0.1)
grid.deposit(x=50, y=50, pheromone_type=PheromoneType.TRAIL, strength=1.0)
grid.diffuse(dt=0.1)
grid.evaporate(dt=0.1)

gradient = grid.sense_gradient(x=50, y=50, sensor_radius=2.0)
print(f"Gradient direction: {gradient}")
```

### Formation Control

```python
from swarm_robotics import FormationController, FormationPattern

controller = FormationController(pattern=FormationPattern.V_SHAPE, spacing=2.0)
leader_pos = (0.0, 0.0)
leader_heading = 0.0
desired = controller.compute_desired_positions(leader_pos, leader_heading, num_agents=8)
for agent_id, pos in desired.items():
    print(f"Agent {agent_id}: desired position {pos}")
```

### Search and Rescue Sweep

```python
from swarm_robotics import SweepPlanner, Agent, SweepConfig

sweep = SweepPlanner(config=SweepConfig(
    area_bounds=(-50, -50, 50, 50),
    sweep_width=3.0,
    overlap_ratio=0.2,
    search_probability_threshold=0.9,
))

agents = [Agent(agent_id=i, position=(0, 0)) for i in range(12)]
coverage = sweep.execute(agents, target_density=0.8)
print(f"Coverage achieved: {coverage.percent:.1f}% in {coverage.time_s:.1f}s")
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Swarm Manager (optional)                 │
│  (mission assignment, global monitoring, parameter tuning)│
└──────────────────────┬──────────────────────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
┌───▼──────────┐ ┌────▼───────────┐ ┌────▼───────────┐
│  Agent 0     │ │  Agent 1       │ │  Agent N       │
│  ┌─────────┐ │ │  ┌─────────┐  │ │  ┌─────────┐   │
│  │ Local   │ │ │  │ Local   │  │ │  │ Local   │   │
│  │ Sensors │ │ │  │ Sensors │  │ │  │ Sensors │   │
│  └────┬────┘ │ │  └────┬────┘  │ │  └────┬────┘   │
│       │      │ │       │       │ │       │        │
│  ┌────▼────┐ │ │  ┌────▼────┐  │ │  ┌────▼────┐   │
│  │Behavior │ │ │  │Behavior │  │ │  │Behavior │   │
│  │ Engine  │ │ │  │ Engine  │  │ │  │ Engine  │   │
│  └────┬────┘ │ │  └────┬────┘  │ │  └────┬────┘   │
│       │      │ │       │       │ │       │        │
│  ┌────▼────┐ │ │  ┌────▼────┐  │ │  ┌────▼────┐   │
│  │Actuator │ │ │  │Actuator │  │ │  │Actuator │   │
│  │ Output  │ │ │  │ Output  │  │ │  │ Output  │   │
│  └─────────┘ │ │  └─────────┘  │ │  └─────────┘   │
└──────────────┘ └────────────────┘ └────────────────┘
         ▲                ▲                ▲
         └────────────────┼────────────────┘
                     Local Comms
                  (range-limited)
```

Each agent runs the same behavior engine independently. Coordination happens through local communication and stigmergic traces. The swarm manager is optional — it provides global monitoring and parameter tuning but is not required for the swarm to function. Removing it causes graceful degradation, not failure.

## Best Practices

1. **Design for scalability first.** Swarm algorithms must work with 10 agents and 10,000 agents. Test with increasing swarm sizes and verify that communication load scales sub-linearly. Use O(1) or O(log N) per-agent algorithms.
2. **Minimize communication.** Every message is a resource cost and a potential failure point. Use local sensing over communication whenever possible, and broadcast only when necessary. Design for 90%+ packet loss.
3. **Embrace randomness.** Stochastic behaviors improve swarm robustness. Deterministic swarms are fragile — they converge to the same failure mode. Add noise to movement, sensing, and decision-making.
4. **Use stigmergy for indirect coordination.** Pheromone-like digital traces allow agents to coordinate without direct communication. This is especially powerful in large swarms where pairwise communication is impractical.
5. **Test against agent failures.** The defining advantage of swarms is graceful degradation. Simulate random agent failures at rates up to 50% and verify the swarm still achieves its goal. Measure the degradation curve.
6. **Set communication range carefully.** Too short and the swarm fragments; too long and communication overhead dominates. Tune range to produce a connected graph with average degree 5-10. Use percolation theory to find the critical range.
7. **Monitor emergence, not individuals.** Swarm metrics (cohesion, entropy, task completion rate) matter more than individual agent states. Instrument the swarm as a whole and alert on emergent behavior anomalies.
8. **Use hierarchical control sparingly.** Hierarchical leaders simplify coordination but create single points of failure. Use flat consensus unless hierarchy is necessary for the task. If hierarchy is needed, implement leader re-election.
9. **Benchmark against centralized solutions.** Swarm approaches should be compared against centralized baselines for correctness and efficiency. A swarm that is robust but never completes its task is not useful.
10. **Simulate before deploying.** Use the swarm simulator extensively. Real robots are expensive and failures cascade in dense swarms. Simulate communication loss, sensor noise, and actuator failures before hardware testing.

## Performance Considerations

- **Per-agent computation**: Each agent should complete its behavior cycle in under 10 ms for 100 Hz control. Avoid O(N) neighbor searches — use spatial hashing or KD-trees for neighbor lookup.
- **Communication bandwidth**: In a 100-agent swarm with 50-byte messages at 10 Hz, total bandwidth is 50 KB/s. Design message formats to be compact. Use delta updates instead of full state broadcasts.
- **Simulation speed**: Simulate 1000 agents at 100 Hz in real-time on a modern workstation. Use vectorized operations (NumPy) for position and velocity updates. Avoid per-agent Python loops in the hot path.
- **Pheromone grid resolution**: A 100x100 grid at 10 cm resolution covers 10m x 10m. Larger areas require coarser resolution or hierarchical grids. Diffusion and evaporation computation is O(grid_size).
- **Consensus convergence time**: Average consensus converges in O(N^2 / lambda_2) steps, where lambda_2 is the algebraic connectivity of the communication graph. Dense graphs converge faster but require more communication.
- **Formation reconfiguration**: Dynamic formation changes cause transient instability. Smooth transitions over 5-10 seconds to prevent oscillation and collision.

## Security Considerations

- **Sybil attacks**: A malicious agent can impersonate multiple identities to disrupt consensus or task allocation. Use cryptographic identity and rate-limit agent registration.
- **Message injection**: Adversarial messages can corrupt pheromone maps or mislead task allocation. Authenticate all inter-agent messages and validate state updates against physical plausibility.
- **Jamming resistance**: Swarm communication can be jammed. Design algorithms to function with intermittent connectivity. Use frequency-hopping or spread-spectrum for critical channels.
- **Agent capture**: A captured agent can leak the swarm's mission parameters and communication keys. Use forward secrecy and limit the information any single agent holds.
- **Fork attacks**: An adversary can split the swarm by injecting false proximity information. Cross-validate ranging measurements with multiple modalities (RF, acoustic, visual).
- **Resource exhaustion**: Malicious agents can drain the swarm's energy or bandwidth by demanding excessive communication. Implement per-agent resource quotas and rate limiting.

## Related Modules

- **autonomous-systems** — Individual agent autonomy within the swarm
- **navigation** — Local path planning and obstacle avoidance for each agent
- **robotics-vision** — Cooperative perception and shared visual maps
- **manipulation** — Cooperative manipulation and object transport by multiple agents

## References

- Brambilla, M., Ferrante, E., Birattari, M., & Dorigo, M. (2013). Swarm robotics: a review from the swarm engineering perspective. *Swarm Intelligence*, 7(1), 1-41.
- Reynolds, C. W. (1987). Flocks, herds and schools: A distributed behavioral model. *ACM SIGGRAPH Computer Graphics*, 21(4), 25-34.
- Olfati-Saber, R. (2006). Flocking for multi-agent dynamic systems: Algorithms and theory. *IEEE Transactions on Automatic Control*, 51(3), 401-420.
- Parker, L. E. (2008). Multiple mobile robot systems. In *Springer Handbook of Robotics* (pp. 921-941).
- Werger, B. B. & Matarić, M. J. (1996). Robotic "food" chains: Externalization of state and program for minimal-agent foraging. *International Conference on Simulation of Adaptive Behavior*.
- Dorigo, M. & Stützle, T. (2004). *Ant Colony Optimization*. MIT Press.
- Swarm Robotics Laboratory, Harvard University: https://seas.harvard.edu/swarm-intelligence
- OpenSwarm Framework Documentation: https://github.com/openswarm-robotics

## Flocking Algorithms — Mathematical Foundations

### Reynolds Boids Model

The classic Reynolds model defines three steering behaviors that each agent computes independently based on local neighbors.

```python
import numpy as np
from swarm_robotics import AgentState

class BoidFlocking:
    def __init__(self, config):
        self.separation_weight = config.separation_weight
        self.alignment_weight = config.alignment_weight
        self.cohesion_weight = config.cohesion_weight
        self.perception_radius = config.perception_radius
        self.max_force = config.max_force
        self.max_speed = config.max_speed
    
    def compute_steering(self, agent, neighbors):
        if not neighbors:
            return np.zeros(2)
        
        separation = self.separation(agent, neighbors)
        alignment = self.alignment(agent, neighbors)
        cohesion = self.cohesion(agent, neighbors)
        
        force = (self.separation_weight * separation +
                 self.alignment_weight * alignment +
                 self.cohesion_weight * cohesion)
        
        # Clamp force
        force_magnitude = np.linalg.norm(force)
        if force_magnitude > self.max_force:
            force = force / force_magnitude * self.max_force
        
        return force
    
    def separation(self, agent, neighbors):
        steer = np.zeros(2)
        count = 0
        for nb in neighbors:
            dist = np.linalg.norm(agent.position - nb.position)
            if 0 < dist < self.perception_radius * 0.5:
                diff = agent.position - nb.position
                diff = diff / (dist + 1e-6)
                steer += diff
                count += 1
        if count > 0:
            steer /= count
        return steer
    
    def alignment(self, agent, neighbors):
        avg_velocity = np.zeros(2)
        count = 0
        for nb in neighbors:
            dist = np.linalg.norm(agent.position - nb.position)
            if dist < self.perception_radius:
                avg_velocity += nb.velocity
                count += 1
        if count > 0:
            avg_velocity /= count
            return avg_velocity - agent.velocity
        return np.zeros(2)
    
    def cohesion(self, agent, neighbors):
        center_of_mass = np.zeros(2)
        count = 0
        for nb in neighbors:
            dist = np.linalg.norm(agent.position - nb.position)
            if dist < self.perception_radius:
                center_of_mass += nb.position
                count += 1
        if count > 0:
            center_of_mass /= count
            desired = center_of_mass - agent.position
            return desired
        return np.zeros(2)
```

### Olfati-Saber Flocking with Virtual Leader

Olfati-Saber's model adds gradient-based inter-agent forces and a navigational feedback term toward a virtual leader.

```python
class OlfatiSaberFlocking:
    def __init__(self, config):
        self.sigma_norm = config.sigma_norm
        self.epsilon = config.epsilon
        self.sigma1 = config.sigma1
        self.sigma2 = config.sigma2
        self.a = config.a
        self.b = config.b
        self.h = config.h
        self.c1 = config.c1
        self.c2 = config.c2
        self.d = config.desired_distance
        self.r = config.communication_range
    
    def compute_acceleration(self, agent, neighbors, virtual_leader):
        # Gradient-based potential (attractive/repulsive)
        gradient_force = np.zeros(2)
        for nb in neighbors:
            dist = np.linalg.norm(agent.position - nb.position)
            gradient_force += self.gradient(self.sigma_norm(dist - self.d)) * (agent.position - nb.position) / (dist + 1e-6)
        
        # Velocity consensus
        consensus_force = np.zeros(2)
        for nb in neighbors:
            consensus_force += (nb.velocity - agent.velocity)
        
        # Navigational feedback toward virtual leader
        nav_force = self.c1 * (virtual_leader.position - agent.position) + \
                    self.c2 * (virtual_leader.velocity - agent.velocity)
        
        acceleration = gradient_force + consensus_force + nav_force
        return acceleration
    
    def gradient(self, z):
        if 0 <= z < self.h:
            return 2 * self.a * (z - self.h)
        elif z >= self.h:
            return self.a * np.exp(-z + self.h)
        else:
            return 0
    
    def sigma_norm(self, z):
        return (1 / self.epsilon) * (np.sqrt(1 + self.epsilon * z**2) - 1)
```

## Consensus Protocols — Deep Dive

### Average Consensus

Average consensus converges all agents to the average of their initial values. It is provably convergent on connected graphs.

```python
import numpy as np
from swarm_robotics import CommunicationGraph

class AverageConsensus:
    def __init__(self, graph, step_size=0.1):
        self.graph = graph
        self.step_size = step_size
    
    def step(self, values):
        new_values = {}
        for agent_id, neighbors in self.graph.get_neighbors().items():
            neighbors = list(neighbors)
            n = len(neighbors)
            if n == 0:
                new_values[agent_id] = values[agent_id]
                continue
            
            neighbor_sum = sum(values[nb] for nb in neighbors)
            new_values[agent_id] = values[agent_id] + self.step_size * (
                neighbor_sum / n - values[agent_id]
            )
        
        return new_values
    
    def has_converged(self, values, threshold=1e-4):
        vals = list(values.values())
        return max(vals) - min(vals) < threshold

class WeightedConsensus:
    def __init__(self, graph, weights=None):
        self.graph = graph
        self.weights = weights or {}
    
    def step(self, values):
        new_values = {}
        for agent_id, neighbors in self.graph.get_neighbors().items():
            neighbors = list(neighbors)
            weight_sum = 0
            weighted_sum = 0
            
            for nb in neighbors:
                w = self.weights.get((agent_id, nb), 1.0)
                weighted_sum += w * values[nb]
                weight_sum += w
            
            if weight_sum > 0:
                new_values[agent_id] = weighted_sum / weight_sum
            else:
                new_values[agent_id] = values[agent_id]
        
        return new_values
```

### Leader Election via Max-Value Consensus

```python
class LeaderElection:
    def __init__(self, graph):
        self.graph = graph
    
    def elect(self, agent_values, max_rounds=100):
        values = dict(agent_values)
        
        for round_num in range(max_rounds):
            new_values = {}
            for agent_id, neighbors in self.graph.get_neighbors().items():
                neighbors = list(neighbors)
                max_val = values[agent_id]
                max_id = agent_id
                
                for nb in neighbors:
                    if values[nb] > max_val:
                        max_val = values[nb]
                        max_id = nb
                    elif values[nb] == max_val and nb < max_id:
                        max_id = nb  # tie-break by ID
                
                new_values[agent_id] = values[max_id]
            
            values = new_values
            
            # Check if all agents agree
            if len(set(values.values())) == 1:
                leader_value = list(values.values())[0]
                leader_id = [aid for aid, v in agent_values.items() if v == leader_value][0]
                return leader_id, round_num + 1
        
        return None, max_rounds
```

### Byzantine-Resilient Consensus

When some agents may be malicious, Byzantine-resilient protocols ensure convergence despite faulty agents.

```python
class ByzantineResilientConsensus:
    def __init__(self, graph, max_byzantine):
        self.graph = graph
        self.f = max_byzantine
    
    def trimmed_mean_step(self, values):
        new_values = {}
        for agent_id, neighbors in self.graph.get_neighbors().items():
            all_values = [values[agent_id]] + [values[nb] for nb in neighbors]
            sorted_vals = sorted(all_values)
            
            # Trim the f largest and f smallest
            trimmed = sorted_vals[self.f:-self.f] if len(sorted_vals) > 2 * self.f else sorted_vals
            
            new_values[agent_id] = np.mean(trimmed)
        
        return new_values
    
    def has_converged(self, values, threshold=1e-4):
        vals = list(values.values())
        return max(vals) - min(vals) < threshold
```

## Task Allocation Algorithms

### Market-Based Auction Allocation

Each task is auctioned, and robots bid based on cost (distance, time, capability). The lowest bidder wins.

```python
from swarm_robotics import Task, Robot

class AuctionAllocator:
    def __init__(self, cost_fn):
        self.cost_fn = cost_fn
    
    def allocate(self, tasks, robots):
        assignments = {r.id: [] for r in robots}
        unassigned_tasks = list(tasks)
        
        for task in tasks:
            bids = {}
            for robot in robots:
                cost = self.cost_fn(robot, task, assignments[robot.id])
                bids[robot.id] = cost
            
            # Winner is lowest bidder
            winner_id = min(bids, key=bids.get)
            assignments[winner_id].append(task)
        
        return assignments
    
    def reallocate(self, assignments, robots, new_task):
        # Find best robot considering current load
        costs = {}
        for robot in robots:
            current_load = len(assignments[robot.id])
            base_cost = self.cost_fn(robot, new_task, assignments[robot.id])
            # Penalize loaded robots
            costs[robot.id] = base_cost * (1 + 0.1 * current_load)
        
        winner_id = min(costs, key=costs.get)
        assignments[winner_id].append(new_task)
        return assignments, winner_id
```

### Response Threshold Allocation

Agents have internal thresholds for each task type. When the task stimulus exceeds the threshold, the agent responds.

```python
import numpy as np

class ResponseThresholdAllocator:
    def __init__(self, task_types, threshold_params):
        self.task_types = task_types
        self.theta = threshold_params  # {task_type: (theta_min, theta_max)}
    
    def response_probability(self, stimulus, agent_threshold):
        theta_min, theta_max = self.theta[agent_threshold]
        if stimulus <= theta_min:
            return 0.0
        elif stimulus >= theta_max:
            return 1.0
        else:
            return (stimulus - theta_min) / (theta_max - theta_min)
    
    def step(self, agents, task_stimuli):
        assignments = {}
        for task_type, stimulus in task_stimuli.items():
            for agent in agents:
                if task_type in agent.capabilities:
                    prob = self.response_probability(stimulus, agent.thresholds[task_type])
                    if np.random.random() < prob:
                        assignments.setdefault(task_type, []).append(agent.id)
        
        # Resolve conflicts (assign to first responder per task)
        final = {}
        for task_type, candidates in assignments.items():
            final[task_type] = candidates[0] if candidates else None
        
        return final
```

## Emergent Behavior Patterns

### Stigmergic Trail Formation

Agents deposit and follow digital pheromone trails to form emergent transportation networks.

```python
import numpy as np

class StigmergicTrailFormation:
    def __init__(self, grid_size, deposit_rate, evaporation_rate, diffusion_rate):
        self.grid = np.zeros(grid_size)
        self.deposit_rate = deposit_rate
        self.evaporation_rate = evaporation_rate
        self.diffusion_rate = diffusion_rate
    
    def deposit(self, position, strength=1.0):
        x, y = int(position[0]), int(position[1])
        if 0 <= x < self.grid.shape[1] and 0 <= y < self.grid.shape[0]:
            self.grid[y, x] += self.deposit_rate * strength
    
    def diffuse(self, dt):
        kernel = np.array([[0.05, 0.1, 0.05],
                           [0.1,  0.4, 0.1 ],
                           [0.05, 0.1, 0.05]])
        
        from scipy.ndimage import convolve
        self.grid = convolve(self.grid, kernel) * self.diffusion_rate + \
                    self.grid * (1 - self.diffusion_rate)
    
    def evaporate(self, dt):
        self.grid *= (1 - self.evaporation_rate * dt)
    
    def sense_gradient(self, position, radius=2.0):
        x, y = position
        region = self.grid[
            max(0, int(y - radius)):int(y + radius) + 1,
            max(0, int(x - radius)):int(x + radius) + 1
        ]
        
        if region.size == 0:
            return np.zeros(2)
        
        # Compute gradient
        gy, gx = np.gradient(region)
        center_y = min(int(y), gy.shape[0] - 1)
        center_x = min(int(x), gx.shape[1] - 1)
        
        return np.array([gx[center_y, center_x], gy[center_y, center_x]])
```

### Collective Foraging

Agents search for food sources and recruit others through stigmergic signals, forming emergent foraging trails.

```python
class CollectiveForaging:
    def __init__(self, num_agents, environment, stigmergy):
        self.agents = [ForagingAgent(i) for i in range(num_agents)]
        self.env = environment
        self.stigmergy = stigmergy
    
    def step(self, dt):
        for agent in self.agents:
            if agent.state == "searching":
                gradient = self.stigmergy.sense_gradient(agent.position)
                agent.move_toward(gradient, noise=0.3)
                
                if self.env.has_food(agent.position):
                    agent.carry_food = True
                    agent.state = "returning"
                    agent.deposit_pheromone(self.stigmergy)
            
            elif agent.state == "returning":
                gradient = self.stigmergy.sense_gradient(agent.position)
                agent.move_toward(-gradient, noise=0.1)  # away from pheromone
                
                if self.env.is_nest(agent.position):
                    agent.carry_food = False
                    agent.state = "searching"
```

## Communication Networking

### Gossip Protocol for State Dissemination

```python
import random

class GossipProtocol:
    def __init__(self, agents, fanout=3):
        self.agents = agents
        self.fanout = fanout
    
    def disseminate(self, agent_states):
        new_states = dict(agent_states)
        
        for agent_id, state in agent_states.items():
            neighbors = self.get_neighbors(agent_id)
            if len(neighbors) == 0:
                continue
            
            targets = random.sample(neighbors, min(self.fanout, len(neighbors)))
            for target_id in targets:
                # Push gossip: send own state to random neighbors
                new_states[target_id] = self.merge(new_states[target_id], state)
        
        return new_states
    
    def merge(self, local, remote):
        # CRDT-style merge (last-writer-wins)
        if remote['timestamp'] > local['timestamp']:
            return remote
        return local

class PushPullGossip:
    def __init__(self, agents):
        self.agents = agents
    
    def step(self, agent_states):
        new_states = dict(agent_states)
        
        for agent_id, neighbors in self.adjacency.items():
            partner_id = random.choice(neighbors)
            
            # Pull partner's state
            partner_state = agent_states[partner_id]
            local_state = agent_states[agent_id]
            
            # Merge (average for numeric, latest for categorical)
            if isinstance(local_state['value'], (int, float)):
                merged = (local_state['value'] + partner_state['value']) / 2
            else:
                merged = partner_state['value'] if partner_state['timestamp'] > local_state['timestamp'] else local_state['value']
            
            new_states[agent_id] = {'value': merged, 'timestamp': max(local_state['timestamp'], partner_state['timestamp'])}
        
        return new_states
```

## Formation Control Algorithms

### Virtual Structure Method

The entire formation is treated as a rigid body. Each agent tracks its assigned position in the virtual structure.

```python
class VirtualStructureFormation:
    def __init__(self, pattern, leader_id):
        self.pattern = pattern  # dict: agent_id -> relative_offset
        self.leader_id = leader_id
    
    def compute_desired_positions(self, leader_pose, leader_heading):
        positions = {}
        cos_h = np.cos(leader_heading)
        sin_h = np.sin(leader_heading)
        
        for agent_id, offset in self.pattern.items():
            # Rotate offset by leader heading
            rotated_offset = np.array([
                cos_h * offset[0] - sin_h * offset[1],
                sin_h * offset[0] + cos_h * offset[1]
            ])
            positions[agent_id] = np.array(leader_pose[:2]) + rotated_offset
        
        return positions

class FormationController:
    def __init__(self, structure, position_gain, heading_gain):
        self.structure = structure
        self.kp = position_gain
        self.kh = heading_gain
    
    def compute_velocity(self, agent_id, current_pose, leader_pose, leader_heading):
        desired = self.structure.compute_desired_positions(leader_pose, leader_heading)
        
        if agent_id not in desired:
            return np.zeros(2)
        
        error = desired[agent_id] - np.array(current_pose[:2])
        
        # PD control
        velocity = self.kp * error
        
        return velocity
```

### Consensus-Based Formation Control

Each agent converges to its desired offset relative to its neighbors without a global leader.

```python
class ConsensusFormation:
    def __init__(self, offsets, communication_graph):
        self.offsets = offsets  # agent_id -> desired_offset from neighbors
        self.graph = communication_graph
    
    def step(self, agent_positions, dt):
        new_positions = {}
        
        for agent_id, neighbors in self.graph.get_neighbors().items():
            neighbor_positions = list(neighbors)
            
            if not neighbor_positions:
                new_positions[agent_id] = agent_positions[agent_id]
                continue
            
            # Compute desired position based on offsets
            desired = np.zeros(2)
            count = 0
            for nb_id in neighbor_positions:
                if nb_id in self.offsets.get(agent_id, {}):
                    offset = self.offsets[agent_id][nb_id]
                    desired += agent_positions[nb_id] + np.array(offset)
                    count += 1
            
            if count > 0:
                desired /= count
                velocity = 0.5 * (desired - np.array(agent_positions[agent_id]))
                new_positions[agent_id] = tuple(np.array(agent_positions[agent_id]) + velocity * dt)
            else:
                new_positions[agent_id] = agent_positions[agent_id]
        
        return new_positions
```

## Swarm Intelligence Optimization

### Particle Swarm Optimization (PSO)

```python
import numpy as np

class ParticleSwarmOptimization:
    def __init__(self, num_particles, dimensions, objective_fn,
                 w=0.7, c1=1.5, c2=1.5, bounds=None):
        self.num_particles = num_particles
        self.dimensions = dimensions
        self.objective = objective_fn
        self.w = w  # inertia weight
        self.c1 = c1  # cognitive coefficient
        self.c2 = c2  # social coefficient
        self.bounds = bounds
        
        self.positions = np.random.uniform(bounds[0], bounds[1], (num_particles, dimensions))
        self.velocities = np.random.uniform(-1, 1, (num_particles, dimensions))
        self.personal_best = self.positions.copy()
        self.personal_best_values = np.full(num_particles, np.inf)
        self.global_best = None
        self.global_best_value = np.inf
    
    def step(self):
        for i in range(self.num_particles):
            value = self.objective(self.positions[i])
            
            if value < self.personal_best_values[i]:
                self.personal_best_values[i] = value
                self.personal_best[i] = self.positions[i].copy()
            
            if value < self.global_best_value:
                self.global_best_value = value
                self.global_best = self.positions[i].copy()
        
        r1 = np.random.random((self.num_particles, self.dimensions))
        r2 = np.random.random((self.num_particles, self.dimensions))
        
        self.velocities = (self.w * self.velocities +
                          self.c1 * r1 * (self.personal_best - self.positions) +
                          self.c2 * r2 * (self.global_best - self.positions))
        
        self.positions += self.velocities
        self.positions = np.clip(self.positions, self.bounds[0], self.bounds[1])
        
        return self.global_best, self.global_best_value
```

### Ant Colony Optimization (ACO) for Path Planning

```python
import numpy as np

class AntColonyOptimization:
    def __init__(self, num_ants, num_nodes, distance_matrix, 
                 alpha=1.0, beta=2.0, rho=0.5, q=1.0):
        self.num_ants = num_ants
        self.num_nodes = num_nodes
        self.distances = distance_matrix
        self.alpha = alpha  # pheromone importance
        self.beta = beta    # heuristic importance
        self.rho = rho      # evaporation rate
        self.q = q          # pheromone deposit factor
        
        self.pheromone = np.ones((num_nodes, num_nodes)) * 0.1
        self.heuristic = 1.0 / (self.distances + 1e-6)
    
    def construct_solutions(self):
        solutions = []
        
        for ant in range(self.num_ants):
            start = np.random.randint(self.num_nodes)
            path = [start]
            visited = {start}
            
            while len(path) < self.num_nodes:
                current = path[-1]
                probs = self.compute_probs(current, visited)
                next_node = np.random.choice(self.num_nodes, p=probs)
                path.append(next_node)
                visited.add(next_node)
            
            path.append(path[0])  # return to start
            solutions.append(path)
        
        return solutions
    
    def compute_probs(self, current, visited):
        tau = self.pheromone[current] ** self.alpha
        eta = self.heuristic[current] ** self.beta
        
        for node in visited:
            tau[node] = 0
            eta[node] = 0
        
        total = np.sum(tau * eta)
        if total == 0:
            return np.ones(self.num_nodes) / self.num_nodes
        
        return (tau * eta) / total
    
    def update_pheromone(self, solutions):
        self.pheromone *= (1 - self.rho)
        
        for path in solutions:
            path_length = sum(self.distances[path[i], path[i+1]] for i in range(len(path) - 1))
            deposit = self.q / path_length
            
            for i in range(len(path) - 1):
                self.pheromone[path[i], path[i+1]] += deposit
                self.pheromone[path[i+1], path[i]] += deposit
```

## Scalability Analysis

### Communication Complexity

```python
class SwarmScalabilityAnalyzer:
    def __init__(self, swarm_sizes=[10, 50, 100, 500, 1000]):
        self.swarm_sizes = swarm_sizes
    
    def measure_communication_load(self, algorithm, neighbors_per_agent):
        results = []
        for N in self.swarm_sizes:
            msg_per_step = N * neighbors_per_agent
            bytes_per_msg = 64  # typical state message
            total_bandwidth = msg_per_step * bytes_per_msg
            
            results.append({
                'swarm_size': N,
                'messages_per_step': msg_per_step,
                'bandwidth_bytes': total_bandwidth,
                'per_agent_msgs': neighbors_per_agent,
            })
        
        return results
    
    def measure_convergence_time(self, consensus_protocol, graph_generator):
        results = []
        for N in self.swarm_sizes:
            graph = graph_generator.generate(N, connectivity=0.3)
            algebraic_connectivity = graph.algebraic_connectivity()
            
            # Theoretical convergence bound
            convergence_steps = N**2 / algebraic_connectivity
            
            results.append({
                'swarm_size': N,
                'algebraic_connectivity': algebraic_connectivity,
                'theoretical_convergence_steps': convergence_steps,
            })
        
        return results
```

### Emergence Metrics

```python
class EmergenceMetrics:
    def __init__(self):
        pass
    
    def cohesion(self, positions):
        center = np.mean(positions, axis=0)
        distances = np.linalg.norm(positions - center, axis=1)
        return np.mean(distances)
    
    def alignment(self, velocities):
        if len(velocities) == 0:
            return 0.0
        avg_velocity = np.mean(velocities, axis=0)
        avg_speed = np.linalg.norm(avg_velocity)
        total_speed = np.mean(np.linalg.norm(velocities, axis=1))
        if total_speed < 1e-6:
            return 0.0
        return avg_speed / total_speed
    
    def entropy(self, positions, grid_size=10, bounds=(-50, 50)):
        grid = np.zeros((grid_size, grid_size))
        for pos in positions:
            x = int((pos[0] - bounds[0]) / (bounds[1] - bounds[0]) * (grid_size - 1))
            y = int((pos[1] - bounds[0]) / (bounds[1] - bounds[0]) * (grid_size - 1))
            x = np.clip(x, 0, grid_size - 1)
            y = np.clip(y, 0, grid_size - 1)
            grid[y, x] += 1
        
        grid = grid / np.sum(grid)
        nonzero = grid[grid > 0]
        return -np.sum(nonzero * np.log2(nonzero))
    
    def task_completion_rate(self, tasks_completed, tasks_total, time_elapsed):
        if time_elapsed < 1e-6:
            return 0.0
        return tasks_completed / time_elapsed
```

## Fault Tolerance and Resilience

### Agent Failure Simulation

```python
class FaultInjector:
    def __init__(self, failure_rate, failure_types):
        self.failure_rate = failure_rate
        self.failure_types = failure_types
    
    def inject(self, agents, dt):
        for agent in agents:
            if np.random.random() < self.failure_rate * dt:
                failure_type = np.random.choice(self.failure_types)
                agent.apply_failure(failure_type)
    
    def simulate_graceful_degradation(self, swarm, mission, failure_rates):
        results = []
        for rate in failure_rates:
            self.failure_rate = rate
            success = mission.execute(swarm, self)
            results.append({
                'failure_rate': rate,
                'mission_success': success,
                'completion_pct': mission.completion_percentage(),
            })
        return results

class AgentStateRecovery:
    def __init__(self, health_check_interval=1.0):
        self.health_check_interval = health_check_interval
    
    def monitor(self, agents, dt):
        unhealthy = []
        for agent in agents:
            if not agent.is_alive() or agent.health_score < 0.3:
                unhealthy.append(agent)
        
        return unhealthy
    
    def redistribute_tasks(self, failed_agents, survivors, task_allocator):
        freed_tasks = []
        for agent in failed_agents:
            freed_tasks.extend(agent.assigned_tasks)
        
        # Reallocate freed tasks
        for task in freed_tasks:
            best_survivor = min(survivors, key=lambda s: task_allocator.cost(s, task))
            best_survivor.assign_task(task)
```

## Configuration Reference

### Swarm Agent Configuration

```yaml
swarm:
  agent:
    id_format: "agent_{:04d}"
    max_speed: 2.0
    max_accel: 1.0
    communication_range: 10.0
    sensing_range: 8.0
    battery_capacity_wh: 50.0
    message_buffer_size: 100
  
  flocking:
    separation_weight: 1.5
    alignment_weight: 1.0
    cohesion_weight: 1.0
    perception_radius: 5.0
    boundary_mode: "wrap"
  
  consensus:
    protocol: "average"
    step_size: 0.1
    convergence_threshold: 0.001
    max_rounds: 100
  
  task_allocation:
    algorithm: "auction"
    reallocation_interval: 5.0
    load_balance_weight: 0.2
  
  communication:
    protocol: "gossip"
    fanout: 3
    message_size_bytes: 64
    send_rate_hz: 10
    packet_loss_rate: 0.1
```

### Simulation Configuration

```yaml
simulation:
  engine: "mujoco"
  timestep: 0.01
  realtime_factor: 1.0
  
  rendering:
    enabled: true
    resolution: [1920, 1080]
    fps: 60
  
  metrics:
    cohesion: true
    alignment: true
    entropy: true
    task_completion_rate: true
    communication_load: true
    record_interval: 10
  
  fault_injection:
    enabled: false
    failure_rate: 0.01
    failure_types: ["sensor", "actuator", "communication", "complete"]
```
