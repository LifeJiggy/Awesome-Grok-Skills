---
name: Physics Simulation
category: core
difficulty: advanced
time_estimate: "4-8 hours"
dependencies: ["three.js", "cannon.js", "matter-js"]
tags: ["physics", "simulation", "3d", "mathematics", "computational"]
grok_personality: "physics-enthusiast"
description: "Create accurate physics simulations with Grok's deep understanding of physical laws and mathematical precision"
---

# Physics Simulation Skill

## Overview
Grok, you'll implement physics simulations that leverage your deep understanding of physical laws. This skill focuses on creating accurate, efficient simulations for everything from particle systems to orbital mechanics.

## Core Physics Domains

### 1. Classical Mechanics
- Newton's laws of motion
- Conservation of energy and momentum
- Rigid body dynamics
- Collision detection and response

### 2. Electromagnetism
- Coulomb's law and electric fields
- Magnetic field interactions
- Electromagnetic wave propagation

### 3. Quantum Mechanics (Simplified)
- Wave function evolution
- Quantum tunneling effects
- Particle probability distributions

### 4. Thermodynamics
- Heat transfer simulations
- Gas dynamics
- Phase transitions

## Implementation Patterns

### Basic Physics Engine
```javascript
class PhysicsEngine {
  constructor(dt = 0.016) { // 60 FPS
    this.dt = dt;
    this.bodies = [];
    this.forces = [];
    this.constraints = [];
    this.gravity = { x: 0, y: -9.81, z: 0 };
  }
  
  addBody(body) {
    this.bodies.push(body);
    return body;
  }
  
  addForce(force) {
    this.forces.push(force);
    return force;
  }
  
  step() {
    // Apply forces
    for (const body of this.bodies) {
      body.force = { x: 0, y: 0, z: 0 };
      
      // Gravity
      body.force.y += body.mass * this.gravity.y;
      
      // Additional forces
      for (const force of this.forces) {
        const f = force.apply(body);
        body.force.x += f.x;
        body.force.y += f.y;
        body.force.z += f.z;
      }
    }
    
    // Integrate motion (Verlet integration)
    for (const body of this.bodies) {
      if (!body.isStatic) {
        const acceleration = {
          x: body.force.x / body.mass,
          y: body.force.y / body.mass,
          z: body.force.z / body.mass
        };
        
        // Verlet integration for better stability
        const newPosition = {
          x: 2 * body.position.x - body.oldPosition.x + acceleration.x * this.dt * this.dt,
          y: 2 * body.position.y - body.oldPosition.y + acceleration.y * this.dt * this.dt,
          z: 2 * body.position.z - body.oldPosition.z + acceleration.z * this.dt * this.dt
        };
        
        body.oldPosition = { ...body.position };
        body.position = newPosition;
      }
    }
    
    // Handle collisions
    this.handleCollisions();
    
    // Apply constraints
    for (const constraint of this.constraints) {
      constraint.apply();
    }
  }
  
  handleCollisions() {
    for (let i = 0; i < this.bodies.length; i++) {
      for (let j = i + 1; j < this.bodies.length; j++) {
        const bodyA = this.bodies[i];
        const bodyB = this.bodies[j];
        
        if (this.checkCollision(bodyA, bodyB)) {
          this.resolveCollision(bodyA, bodyB);
        }
      }
    }
  }
  
  checkCollision(bodyA, bodyB) {
    const dx = bodyB.position.x - bodyA.position.x;
    const dy = bodyB.position.y - bodyA.position.y;
    const dz = bodyB.position.z - bodyA.position.z;
    const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
    
    return distance < (bodyA.radius + bodyB.radius);
  }
  
  resolveCollision(bodyA, bodyB) {
    // Calculate collision normal
    const dx = bodyB.position.x - bodyA.position.x;
    const dy = bodyB.position.y - bodyA.position.y;
    const dz = bodyB.position.z - bodyA.position.z;
    const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
    
    const nx = dx / distance;
    const ny = dy / distance;
    const nz = dz / distance;
    
    // Separate bodies
    const overlap = (bodyA.radius + bodyB.radius) - distance;
    const separationX = nx * overlap * 0.5;
    const separationY = ny * overlap * 0.5;
    const separationZ = nz * overlap * 0.5;
    
    if (!bodyA.isStatic) {
      bodyA.position.x -= separationX;
      bodyA.position.y -= separationY;
      bodyA.position.z -= separationZ;
    }
    
    if (!bodyB.isStatic) {
      bodyB.position.x += separationX;
      bodyB.position.y += separationY;
      bodyB.position.z += separationZ;
    }
    
    // Calculate relative velocity
    const vxA = bodyA.position.x - bodyA.oldPosition.x;
    const vyA = bodyA.position.y - bodyA.oldPosition.y;
    const vzA = bodyA.position.z - bodyA.oldPosition.z;
    
    const vxB = bodyB.position.x - bodyB.oldPosition.x;
    const vyB = bodyB.position.y - bodyB.oldPosition.y;
    const vzB = bodyB.position.z - bodyB.oldPosition.z;
    
    const relativeVelocityX = vxB - vxA;
    const relativeVelocityY = vyB - vyA;
    const relativeVelocityZ = vzB - vzA;
    
    // Calculate impulse
    const velocityAlongNormal = relativeVelocityX * nx + relativeVelocityY * ny + relativeVelocityZ * nz;
    
    if (velocityAlongNormal > 0) return;
    
    const restitution = 0.8; // Coefficient of restitution
    const impulse = 2 * velocityAlongNormal / (1/bodyA.mass + 1/bodyB.mass);
    const impulseX = impulse * nx * restitution;
    const impulseY = impulse * ny * restitution;
    const impulseZ = impulse * nz * restitution;
    
    // Apply impulse
    if (!bodyA.isStatic) {
      bodyA.oldPosition.x -= impulseX / bodyA.mass;
      bodyA.oldPosition.y -= impulseY / bodyA.mass;
      bodyA.oldPosition.z -= impulseZ / bodyA.mass;
    }
    
    if (!bodyB.isStatic) {
      bodyB.oldPosition.x += impulseX / bodyB.mass;
      bodyB.oldPosition.y += impulseY / bodyB.mass;
      bodyB.oldPosition.z += impulseZ / bodyB.mass;
    }
  }
}
```

### Orbital Mechanics
```javascript
class OrbitalSimulation {
  constructor() {
    this.G = 6.67430e-11; // Gravitational constant
    this.bodies = [];
    this.time = 0;
    this.dt = 3600; // 1 hour time step
  }
  
  addCelestialBody(name, mass, position, velocity) {
    const body = {
      name,
      mass,
      position: { ...position },
      velocity: { ...velocity },
      trail: []
    };
    
    this.bodies.push(body);
    return body;
  }
  
  calculateGravitationalForce(body1, body2) {
    const dx = body2.position.x - body1.position.x;
    const dy = body2.position.y - body1.position.y;
    const dz = body2.position.z - body1.position.z;
    
    const distanceSquared = dx * dx + dy * dy + dz * dz;
    const distance = Math.sqrt(distanceSquared);
    
    const forceMagnitude = this.G * body1.mass * body2.mass / distanceSquared;
    
    return {
      x: forceMagnitude * dx / distance,
      y: forceMagnitude * dy / distance,
      z: forceMagnitude * dz / distance
    };
  }
  
  update() {
    // Calculate forces
    const forces = this.bodies.map(() => ({ x: 0, y: 0, z: 0 }));
    
    for (let i = 0; i < this.bodies.length; i++) {
      for (let j = i + 1; j < this.bodies.length; j++) {
        const force = this.calculateGravitationalForce(this.bodies[i], this.bodies[j]);
        
        forces[i].x += force.x;
        forces[i].y += force.y;
        forces[i].z += force.z;
        
        forces[j].x -= force.x;
        forces[j].y -= force.y;
        forces[j].z -= force.z;
      }
    }
    
    // Update velocities and positions (Euler integration)
    for (let i = 0; i < this.bodies.length; i++) {
      const body = this.bodies[i];
      const force = forces[i];
      
      // Update velocity
      const acceleration = {
        x: force.x / body.mass,
        y: force.y / body.mass,
        z: force.z / body.mass
      };
      
      body.velocity.x += acceleration.x * this.dt;
      body.velocity.y += acceleration.y * this.dt;
      body.velocity.z += acceleration.z * this.dt;
      
      // Update position
      body.position.x += body.velocity.x * this.dt;
      body.position.y += body.velocity.y * this.dt;
      body.position.z += body.velocity.z * this.dt;
      
      // Store trail (limit trail length)
      body.trail.push({ ...body.position });
      if (body.trail.length > 500) {
        body.trail.shift();
      }
    }
    
    this.time += this.dt;
  }
  
  calculateOrbitalElements(body, centralBody) {
    // Calculate orbital elements relative to central body
    const r = {
      x: body.position.x - centralBody.position.x,
      y: body.position.y - centralBody.position.y,
      z: body.position.z - centralBody.position.z
    };
    
    const v = {
      x: body.velocity.x - centralBody.velocity.x,
      y: body.velocity.y - centralBody.velocity.y,
      z: body.velocity.z - centralBody.velocity.z
    };
    
    const rMagnitude = Math.sqrt(r.x * r.x + r.y * r.y + r.z * r.z);
    const vMagnitude = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
    
    // Specific orbital energy
    const mu = this.G * centralBody.mass;
    const energy = (vMagnitude * vMagnitude) / 2 - mu / rMagnitude;
    
    // Semi-major axis
    const a = -mu / (2 * energy);
    
    // Eccentricity vector
    const h = this.crossProduct(r, v); // Specific angular momentum
    const eVector = {
      x: ((vMagnitude * vMagnitude - mu / rMagnitude) * r.x - this.dotProduct(r, v) * v.x) / mu,
      y: ((vMagnitude * vMagnitude - mu / rMagnitude) * r.y - this.dotProduct(r, v) * v.y) / mu,
      z: ((vMagnitude * vMagnitude - mu / rMagnitude) * r.z - this.dotProduct(r, v) * v.z) / mu
    };
    
    const eccentricity = Math.sqrt(this.dotProduct(eVector, eVector));
    
    return {
      semiMajorAxis: a,
      eccentricity,
      period: 2 * Math.PI * Math.sqrt(Math.pow(a, 3) / mu),
      specificEnergy: energy
    };
  }
  
  crossProduct(a, b) {
    return {
      x: a.y * b.z - a.z * b.y,
      y: a.z * b.x - a.x * b.z,
      z: a.x * b.y - a.y * b.x
    };
  }
  
  dotProduct(a, b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
  }
}
```

### Particle System
```javascript
class ParticleSystem {
  constructor(maxParticles = 1000) {
    this.particles = [];
    this.maxParticles = maxParticles;
    this.emitters = [];
    this.forces = [];
  }
  
  addEmitter(emitter) {
    this.emitters.push(emitter);
    return emitter;
  }
  
  addForce(force) {
    this.forces.push(force);
    return force;
  }
  
  emit(dt) {
    for (const emitter of this.emitters) {
      const newParticles = emitter.emit(dt);
      
      for (const particle of newParticles) {
        if (this.particles.length < this.maxParticles) {
          this.particles.push(particle);
        }
      }
    }
  }
  
  update(dt) {
    // Emit new particles
    this.emit(dt);
    
    // Update existing particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const particle = this.particles[i];
      
      // Apply forces
      for (const force of this.forces) {
        force.apply(particle, dt);
      }
      
      // Update particle
      particle.update(dt);
      
      // Remove dead particles
      if (particle.isDead()) {
        this.particles.splice(i, 1);
      }
    }
  }
  
  getParticleData() {
    return this.particles.map(p => ({
      position: p.position,
      velocity: p.velocity,
      color: p.color,
      size: p.size,
      life: p.life
    }));
  }
}

class Particle {
  constructor(position, velocity, life = 1.0) {
    this.position = { ...position };
    this.velocity = { ...velocity };
    this.life = life;
    this.maxLife = life;
    this.color = { r: 255, g: 255, b: 255, a: 255 };
    this.size = 1.0;
  }
  
  update(dt) {
    // Update position
    this.position.x += this.velocity.x * dt;
    this.position.y += this.velocity.y * dt;
    this.position.z += this.velocity.z * dt;
    
    // Update life
    this.life -= dt;
    
    // Update alpha based on life
    this.color.a = Math.floor(255 * (this.life / this.maxLife));
  }
  
  isDead() {
    return this.life <= 0;
  }
}

class ParticleEmitter {
  constructor(position, rate = 10) {
    this.position = position;
    this.rate = rate; // particles per second
    this.accumulator = 0;
  }
  
  emit(dt) {
    this.accumulator += this.rate * dt;
    const particles = [];
    
    while (this.accumulator >= 1) {
      const particle = this.createParticle();
      particles.push(particle);
      this.accumulator -= 1;
    }
    
    return particles;
  }
  
  createParticle() {
    // Random velocity within a cone
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.random() * Math.PI / 4;
    const speed = 5 + Math.random() * 10;
    
    const velocity = {
      x: speed * Math.sin(phi) * Math.cos(theta),
      y: speed * Math.cos(phi),
      z: speed * Math.sin(phi) * Math.sin(theta)
    };
    
    return new Particle(
      { ...this.position },
      velocity,
      1.0 + Math.random() * 2.0
    );
  }
}
```

### Electromagnetic Simulation
```javascript
class ElectromagneticSimulation {
  constructor() {
    this.k = 8.99e9; // Coulomb's constant
    this.charges = [];
    this.electricField = [];
    this.magneticField = [];
  }
  
  addCharge(charge) {
    this.charges.push(charge);
    return charge;
  }
  
  calculateElectricField(point) {
    let field = { x: 0, y: 0, z: 0 };
    
    for (const charge of this.charges) {
      const dx = point.x - charge.position.x;
      const dy = point.y - charge.position.y;
      const dz = point.z - charge.position.z;
      
      const distanceSquared = dx * dx + dy * dy + dz * dz;
      const distance = Math.sqrt(distanceSquared);
      
      if (distance > 0.001) { // Avoid division by zero
        const fieldMagnitude = this.k * charge.charge / distanceSquared;
        
        field.x += fieldMagnitude * dx / distance;
        field.y += fieldMagnitude * dy / distance;
        field.z += fieldMagnitude * dz / distance;
      }
    }
    
    return field;
  }
  
  calculateMagneticField(point) {
    let field = { x: 0, y: 0, z: 0 };
    
    for (const charge of this.charges) {
      if (charge.velocity) {
        // Biot-Savart law (simplified)
        const dx = point.x - charge.position.x;
        const dy = point.y - charge.position.y;
        const dz = point.z - charge.position.z;
        
        const distanceSquared = dx * dx + dy * dy + dz * dz;
        const distance = Math.sqrt(distanceSquared);
        
        if (distance > 0.001) {
          const crossProduct = this.crossProduct(charge.velocity, { x: dx, y: dy, z: dz });
          const fieldMagnitude = (this.k * 1e-7 * charge.charge) / distanceSquared;
          
          field.x += fieldMagnitude * crossProduct.x / distance;
          field.y += fieldMagnitude * crossProduct.y / distance;
          field.z += fieldMagnitude * crossProduct.z / distance;
        }
      }
    }
    
    return field;
  }
  
  crossProduct(a, b) {
    return {
      x: a.y * b.z - a.z * b.y,
      y: a.z * b.x - a.x * b.z,
      z: a.x * b.y - a.y * b.x
    };
  }
}
```

## Visualization Integration

### Three.js Renderer
```javascript
class PhysicsRenderer {
  constructor(canvas, physicsEngine) {
    this.canvas = canvas;
    this.physicsEngine = physicsEngine;
    
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, canvas.width / canvas.height, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer({ canvas });
    
    this.meshes = new Map();
    this.initializeScene();
  }
  
  initializeScene() {
    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040);
    this.scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5);
    this.scene.add(directionalLight);
    
    // Camera position
    this.camera.position.set(0, 5, 10);
    this.camera.lookAt(0, 0, 0);
  }
  
  update() {
    // Update mesh positions based on physics bodies
    for (const body of this.physicsEngine.bodies) {
      let mesh = this.meshes.get(body);
      
      if (!mesh) {
        const geometry = new THREE.SphereGeometry(body.radius, 32, 32);
        const material = new THREE.MeshPhongMaterial({ color: body.color || 0x00ff00 });
        mesh = new THREE.Mesh(geometry, material);
        this.scene.add(mesh);
        this.meshes.set(body, mesh);
      }
      
      mesh.position.set(body.position.x, body.position.y, body.position.z);
    }
    
    this.renderer.render(this.scene, this.camera);
  }
  
  animate() {
    requestAnimationFrame(() => this.animate());
    this.physicsEngine.step();
    this.update();
  }
}
```

## Quick Start Examples

### Simple Pendulum
```javascript
class PendulumSimulation {
  constructor(length, mass, initialAngle) {
    this.length = length;
    this.mass = mass;
    this.angle = initialAngle;
    this.angularVelocity = 0;
    this.gravity = 9.81;
    this.dt = 0.01;
  }
  
  update() {
    // Calculate angular acceleration (equation of motion)
    const angularAcceleration = -(this.gravity / this.length) * Math.sin(this.angle);
    
    // Update angular velocity and angle (Euler integration)
    this.angularVelocity += angularAcceleration * this.dt;
    this.angle += this.angularVelocity * this.dt;
    
    // Apply damping
    this.angularVelocity *= 0.999;
  }
  
  getPosition() {
    return {
      x: this.length * Math.sin(this.angle),
      y: -this.length * Math.cos(this.angle)
    };
  }
}
```

### Projectile Motion
```javascript
class ProjectileSimulation {
  constructor(initialPosition, initialVelocity, gravity = -9.81) {
    this.position = { ...initialPosition };
    this.velocity = { ...initialVelocity };
    this.gravity = gravity;
    this.dt = 0.01;
    this.trail = [];
  }
  
  update() {
    // Update velocity (gravity only affects y-component)
    this.velocity.y += this.gravity * this.dt;
    
    // Update position
    this.position.x += this.velocity.x * this.dt;
    this.position.y += this.velocity.y * this.dt;
    
    // Store trail
    this.trail.push({ ...this.position });
    if (this.trail.length > 100) {
      this.trail.shift();
    }
  }
  
  getTrajectoryEquation() {
    // Analytical solution for projectile motion
    const v0x = this.velocity.x;
    const v0y = this.velocity.y;
    const g = this.gravity;
    
    return (t) => ({
      x: this.position.x + v0x * t,
      y: this.position.y + v0y * t + 0.5 * g * t * t
    });
  }
}
```

## Performance Optimization

### Spatial Partitioning
```javascript
class SpatialGrid {
  constructor(cellSize, bounds) {
    this.cellSize = cellSize;
    this.bounds = bounds;
    this.cells = new Map();
  }
  
  getCellKey(position) {
    const x = Math.floor(position.x / this.cellSize);
    const y = Math.floor(position.y / this.cellSize);
    const z = Math.floor(position.z / this.cellSize);
    return `${x},${y},${z}`;
  }
  
  addBody(body) {
    const key = this.getCellKey(body.position);
    
    if (!this.cells.has(key)) {
      this.cells.set(key, []);
    }
    
    this.cells.get(key).push(body);
  }
  
  getNearbyBodies(body, radius) {
    const nearby = [];
    const cellRadius = Math.ceil(radius / this.cellSize);
    
    const centerCell = this.getCellKey(body.position);
    const [cx, cy, cz] = centerCell.split(',').map(Number);
    
    for (let x = cx - cellRadius; x <= cx + cellRadius; x++) {
      for (let y = cy - cellRadius; y <= cy + cellRadius; y++) {
        for (let z = cz - cellRadius; z <= cz + cellRadius; z++) {
          const key = `${x},${y},${z}`;
          const cell = this.cells.get(key);
          
          if (cell) {
            nearby.push(...cell);
          }
        }
      }
    }
    
    return nearby;
  }
}
```

## Best Practices

1. **Numerical Stability**: Use appropriate integration methods (Verlet for stability, RK4 for accuracy)
2. **Performance**: Implement spatial partitioning for large numbers of bodies
3. **Precision**: Use double precision for orbital mechanics, single precision for real-time simulations
4. **Time Steps**: Choose appropriate time steps for the simulation scale
5. **Conservation**: Monitor energy and momentum conservation to validate simulations

Remember: Physics simulations are computational approximations of reality. Focus on the level of accuracy required for your specific use case while maintaining computational efficiency.