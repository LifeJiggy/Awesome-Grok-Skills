# Simulation Templates

## 🌌 Orbital Mechanics

### Two-Body Problem
```python
class OrbitalSimulation:
    def __init__(self):
        self.G = 6.67430e-11  # Gravitational constant
        self.bodies = []
        
    def add_body(self, mass, position, velocity, name="Body"):
        """Add a celestial body to the simulation"""
        body = {
            'mass': mass,
            'position': np.array(position, dtype=float),
            'velocity': np.array(velocity, dtype=float),
            'name': name,
            'trajectory': []
        }
        self.bodies.append(body)
        
    def calculate_force(self, body1, body2):
        """Calculate gravitational force between two bodies"""
        r_vec = body2['position'] - body1['position']
        r = np.linalg.norm(r_vec)
        
        if r == 0:
            return np.array([0.0, 0.0, 0.0])
            
        force_magnitude = self.G * body1['mass'] * body2['mass'] / (r**2)
        force_direction = r_vec / r
        
        return force_magnitude * force_direction
        
    def update(self, dt):
        """Update positions using Verlet integration"""
        # Calculate forces
        forces = [np.array([0.0, 0.0, 0.0]) for _ in self.bodies]
        
        for i, body1 in enumerate(self.bodies):
            for j, body2 in enumerate(self.bodies):
                if i != j:
                    forces[i] += self.calculate_force(body1, body2)
        
        # Update velocities and positions
        for i, body in enumerate(self.bodies):
            acceleration = forces[i] / body['mass']
            body['velocity'] += acceleration * dt
            body['position'] += body['velocity'] * dt
            body['trajectory'].append(body['position'].copy())
```

### Earth-Satellite System
```python
def create_satellite_scenario():
    """Create Earth-satellite orbital simulation"""
    sim = OrbitalSimulation()
    
    # Earth (simplified as point mass)
    earth_mass = 5.972e24  # kg
    sim.add_body(earth_mass, [0, 0, 0], [0, 0, 0], "Earth")
    
    # Satellite at 400km altitude (ISS altitude)
    satellite_mass = 420000  # kg
    earth_radius = 6.371e6  # meters
    altitude = 400e3  # 400 km
    
    # Circular orbital velocity
    orbital_radius = earth_radius + altitude
    orbital_speed = np.sqrt(sim.G * earth_mass / orbital_radius)
    
    sim.add_body(
        satellite_mass,
        [orbital_radius, 0, 0],
        [0, orbital_speed, 0],
        "Satellite"
    )
    
    return sim
```

## ⚛️ Particle Physics

### Charged Particle in Magnetic Field
```python
class ChargedParticle:
    def __init__(self, mass, charge, position, velocity):
        self.mass = mass
        self.charge = charge
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.trajectory = []
        
    def lorentz_force(self, E_field, B_field):
        """Calculate Lorentz force: F = q(E + v × B)"""
        electric = self.charge * E_field
        magnetic = self.charge * np.cross(self.velocity, B_field)
        return electric + magnetic
        
    def update(self, E_field, B_field, dt):
        """Update particle state using Runge-Kutta 4th order"""
        def acceleration(pos, vel):
            E = E_field(pos) if callable(E_field) else E_field
            B = B_field(pos) if callable(B_field) else B_field
            force = self.lorentz_force(E, B)
            return force / self.mass
            
        # RK4 integration
        k1_v = acceleration(self.position, self.velocity) * dt
        k1_x = self.velocity * dt
        
        k2_v = acceleration(self.position + k1_x/2, self.velocity + k1_v/2) * dt
        k2_x = (self.velocity + k1_v/2) * dt
        
        k3_v = acceleration(self.position + k2_x/2, self.velocity + k2_v/2) * dt
        k3_x = (self.velocity + k2_v/2) * dt
        
        k4_v = acceleration(self.position + k3_x, self.velocity + k3_v) * dt
        k4_x = (self.velocity + k3_v) * dt
        
        self.velocity += (k1_v + 2*k2_v + 2*k3_v + k4_v) / 6
        self.position += (k1_x + 2*k2_x + 2*k3_x + k4_x) / 6
        self.trajectory.append(self.position.copy())

def uniform_magnetic_field(B_strength):
    """Create uniform magnetic field in z-direction"""
    return lambda pos: np.array([0, 0, B_strength])
```

### Particle Collision Simulation
```python
class ParticleCollision:
    def __init__(self):
        self.particles = []
        self.time = 0
        
    def add_particle(self, particle):
        """Add particle to simulation"""
        self.particles.append(particle)
        
    def check_collision(self, p1, p2, collision_radius=1e-10):
        """Check if two particles collide"""
        distance = np.linalg.norm(p1.position - p2.position)
        return distance < collision_radius
        
    def elastic_collision(self, p1, p2):
        """Handle elastic collision between two particles"""
        # Conservation of momentum and energy
        m1, m2 = p1.mass, p2.mass
        v1, v2 = p1.velocity, p2.velocity
        x1, x2 = p1.position, p2.position
        
        # Collision normal
        n = (x2 - x1) / np.linalg.norm(x2 - x1)
        
        # Relative velocity along collision normal
        v_rel = np.dot(v1 - v2, n)
        
        # Don't process if particles are separating
        if v_rel < 0:
            return
            
        # Impulse
        impulse = 2 * m1 * m2 / (m1 + m2) * v_rel * n
        
        # Update velocities
        p1.velocity -= impulse / m1
        p2.velocity += impulse / m2
        
    def step(self, dt):
        """Advance simulation by one time step"""
        # Update particle positions
        for particle in self.particles:
            particle.position += particle.velocity * dt
            
        # Check and handle collisions
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                if self.check_collision(self.particles[i], self.particles[j]):
                    self.elastic_collision(self.particles[i], self.particles[j])
                    
        self.time += dt
```

## 🌊 Fluid Dynamics

### 2D Incompressible Flow (Simplified Navier-Stokes)
```python
class FluidSimulation2D:
    def __init__(self, width, height, viscosity=0.01, density=1.0):
        self.width = width
        self.height = height
        self.viscosity = viscosity
        self.density = density
        
        # Velocity field (u, v components)
        self.u = np.zeros((height, width))
        self.v = np.zeros((height, width))
        
        # Pressure field
        self.p = np.zeros((height, width))
        
        # Divergence field for pressure correction
        self.div = np.zeros((height, width))
        
    def apply_force(self, x, y, fx, fy, radius=5):
        """Apply external force at specific location"""
        y_indices, x_indices = np.ogrid[:self.height, :self.width]
        mask = (x_indices - x)**2 + (y_indices - y)**2 <= radius**2
        
        self.u[mask] += fx
        self.v[mask] += fy
        
    def advect(self, dt):
        """Advection step using semi-Lagrangian method"""
        new_u = np.zeros_like(self.u)
        new_v = np.zeros_like(self.v)
        
        for j in range(1, self.height - 1):
            for i in range(1, self.width - 1):
                # Trace particle back in time
                x = i - dt * self.u[j, i]
                y = j - dt * self.v[j, i]
                
                # Clamp to boundaries
                x = np.clip(x, 0, self.width - 1)
                y = np.clip(y, 0, self.height - 1)
                
                # Bilinear interpolation
                i0, j0 = int(x), int(y)
                i1, j1 = min(i0 + 1, self.width - 1), min(j0 + 1, self.height - 1)
                
                sx, sy = x - i0, y - j0
                
                new_u[j, i] = (1-sx)*(1-sy)*self.u[j0,i0] + sx*(1-sy)*self.u[j0,i1] + \
                             (1-sx)*sy*self.u[j1,i0] + sx*sy*self.u[j1,i1]
                new_v[j, i] = (1-sx)*(1-sy)*self.v[j0,i0] + sx*(1-sy)*self.v[j0,i1] + \
                             (1-sx)*sy*self.v[j1,i0] + sx*sy*self.v[j1,i1]
        
        self.u = new_u
        self.v = new_v
        
    def diffuse(self, dt):
        """Diffusion step (viscosity)"""
        alpha = self.viscosity * dt
        
        # Gauss-Seidel relaxation
        for _ in range(10):  # iterations
            u_old = self.u.copy()
            v_old = self.v.copy()
            
            for j in range(1, self.height - 1):
                for i in range(1, self.width - 1):
                    self.u[j, i] = (u_old[j, i] + alpha * (
                        self.u[j-1, i] + self.u[j+1, i] + 
                        self.u[j, i-1] + self.u[j, i+1]
                    )) / (1 + 4*alpha)
                    
                    self.v[j, i] = (v_old[j, i] + alpha * (
                        self.v[j-1, i] + self.v[j+1, i] + 
                        self.v[j, i-1] + self.v[j, i+1]
                    )) / (1 + 4*alpha)
        
    def pressure_correction(self):
        """Pressure correction to maintain incompressibility"""
        # Calculate divergence
        for j in range(1, self.height - 1):
            for i in range(1, self.width - 1):
                self.div[j, i] = (self.u[j, i+1] - self.u[j, i-1] + 
                                  self.v[j+1, i] - self.v[j-1, i]) * 0.5
        
        # Solve pressure Poisson equation
        self.p.fill(0)
        for _ in range(50):  # iterations
            p_old = self.p.copy()
            for j in range(1, self.height - 1):
                for i in range(1, self.width - 1):
                    self.p[j, i] = (p_old[j, i] - self.div[j, i] + 
                                   p_old[j-1, i] + p_old[j+1, i] + 
                                   p_old[j, i-1] + p_old[j, i+1]) * 0.25
        
        # Apply pressure correction
        for j in range(1, self.height - 1):
            for i in range(1, self.width - 1):
                self.u[j, i] -= 0.5 * (self.p[j, i+1] - self.p[j, i-1])
                self.v[j, i] -= 0.5 * (self.p[j+1, i] - self.p[j-1, i])
        
    def step(self, dt):
        """Complete simulation step"""
        self.advect(dt)
        self.diffuse(dt)
        self.pressure_correction()
```

## 🔥 Thermodynamics

### Heat Transfer Simulation
```python
class HeatTransferSimulation:
    def __init__(self, width, height, thermal_diffusivity=1.0):
        self.width = width
        self.height = height
        self.alpha = thermal_diffusivity  # thermal diffusivity
        self.temperature = np.zeros((height, width))
        self.heat_sources = []
        
    def add_heat_source(self, x, y, power, radius=3):
        """Add a constant heat source"""
        self.heat_sources.append({'x': x, 'y': y, 'power': power, 'radius': radius})
        
    def apply_heat_sources(self):
        """Apply all heat sources to temperature field"""
        for source in self.heat_sources:
            y_indices, x_indices = np.ogrid[:self.height, :self.width]
            mask = (x_indices - source['x'])**2 + (y_indices - source['y'])**2 <= source['radius']**2
            self.temperature[mask] += source['power']
            
    def diffuse_heat(self, dt):
        """Heat diffusion using finite difference method"""
        # 2D heat equation: ∂T/∂t = α(∂²T/∂x² + ∂²T/∂y²)
        
        # Stability condition: dt <= (dx² * dy²) / (2α(dx² + dy²))
        dx = dy = 1.0
        max_dt = (dx**2 * dy**2) / (2 * self.alpha * (dx**2 + dy**2))
        dt = min(dt, max_dt)
        
        new_temp = self.temperature.copy()
        
        for j in range(1, self.height - 1):
            for i in range(1, self.width - 1):
                laplacian = (self.temperature[j, i+1] + self.temperature[j, i-1] + 
                           self.temperature[j+1, i] + self.temperature[j-1, i] - 
                           4 * self.temperature[j, i])
                
                new_temp[j, i] = self.temperature[j, i] + self.alpha * dt * laplacian
        
        self.temperature = new_temp
        
    def set_boundary_conditions(self, boundary_type='dirichlet', value=0):
        """Set boundary conditions"""
        if boundary_type == 'dirichlet':
            # Fixed temperature at boundaries
            self.temperature[0, :] = value    # top
            self.temperature[-1, :] = value   # bottom
            self.temperature[:, 0] = value    # left
            self.temperature[:, -1] = value   # right
            
        elif boundary_type == 'neumann':
            # Zero gradient at boundaries (insulated)
            self.temperature[0, :] = self.temperature[1, :]    # top
            self.temperature[-1, :] = self.temperature[-2, :]   # bottom
            self.temperature[:, 0] = self.temperature[:, 1]    # left
            self.temperature[:, -1] = self.temperature[:, -2]   # right
            
    def step(self, dt):
        """Advance simulation by one time step"""
        self.apply_heat_sources()
        self.diffuse_heat(dt)
```

## 🎯 Usage Examples

### Multi-Physics Coupling
```python
def coupled_simulation():
    """Example of coupled physics simulation"""
    
    # Create orbital simulation
    orbit_sim = OrbitalSimulation()
    orbit_sim.add_body(5.972e24, [0, 0, 0], [0, 0, 0], "Earth")
    orbit_sim.add_body(1000, [6.771e6, 0, 0], [0, 7800, 0], "Satellite")
    
    # Create thermal simulation (satellite heating)
    thermal_sim = HeatTransferSimulation(100, 100)
    thermal_sim.add_heat_source(50, 50, 100)  # Solar heating
    
    # Run coupled simulation
    dt = 1.0
    for step in range(1000):
        # Update orbital mechanics
        orbit_sim.update(dt)
        
        # Update thermal dynamics
        thermal_sim.step(dt)
        
        # Check for temperature effects on orbit (simplified)
        avg_temp = np.mean(thermal_sim.temperature)
        if avg_temp > 50:  # High temperature affects satellite
            # Simulate orbital decay due to thermal expansion
            for body in orbit_sim.bodies:
                if body['name'] == 'Satellite':
                    body['velocity'] *= 0.9999  # Slight velocity reduction
                    
    return orbit_sim, thermal_sim
```

### Real-time Visualization
```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_simulation(sim, steps=1000, dt=0.1):
    """Create real-time animation of simulation"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Setup plots
    line1, = ax1.plot([], [], 'b-')
    scatter1 = ax1.scatter([], [], c='red', s=50)
    
    im = ax2.imshow(np.zeros((100, 100)), cmap='hot', vmin=0, vmax=100)
    
    def init():
        ax1.set_xlim(-1e7, 1e7)
        ax1.set_ylim(-1e7, 1e7)
        ax1.set_aspect('equal')
        ax2.set_xlim(0, 100)
        ax2.set_ylim(0, 100)
        return line1, scatter1, im
    
    def update(frame):
        # Update simulation
        sim.step(dt)
        
        # Update orbital plot
        if hasattr(sim, 'bodies'):
            for body in sim.bodies:
                if body['name'] == 'Satellite' and len(body['trajectory']) > 1:
                    trajectory = np.array(body['trajectory'])
                    line1.set_data(trajectory[:, 0], trajectory[:, 1])
                    scatter1.set_offsets([[body['position'][0], body['position'][1]]])
        
        # Update thermal plot
        if hasattr(sim, 'temperature'):
            im.set_array(sim.temperature)
            
        return line1, scatter1, im
    
    anim = animation.FuncAnimation(fig, update, init_func=init, frames=steps, 
                                  interval=50, blit=False)
    
    plt.show()
    return anim
```

---

*Remember: The accuracy of physics simulations depends on numerical stability, appropriate time steps, and validation against real-world data. Always verify your models!* ⚛️