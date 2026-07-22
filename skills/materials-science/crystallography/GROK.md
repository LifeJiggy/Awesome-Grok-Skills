---
name: "crystallography"
category: "materials-science"
version: "2.0.0"
tags: ["materials", "crystallography", "xrd", "diffraction", "structure"]
description: "Crystallography tools for structure analysis and diffraction simulation"
---

# Crystallography

## Overview

The Crystallography module provides tools for crystal structure analysis, X-ray diffraction simulation, symmetry operations, and structure visualization. It supports crystal structure manipulation, diffraction pattern generation, and structure refinement.

## Core Capabilities

- **Crystal Structure**: Define and manipulate crystal structures
- **Symmetry Operations**: Apply space group symmetry operations
- **XRD Simulation**: Simulate X-ray diffraction patterns
- **Structure Refinement**: Rietveld refinement tools
- **Unit Cell Analysis**: Lattice parameters and unit cell calculations
- **Miller Indices**: Generate Miller index planes
- **Band Structure**: Electronic band structure calculation setup
- **Structure Visualization**: Generate structure visualizations

## Usage Examples

### Crystal Structure Definition

```python
from crystallography import CrystalStructure, Lattice

# Define crystal structure
structure = CrystalStructure(
    name="Silicon",
    lattice=Lattice(
        a=5.431, b=5.431, c=5.431,
        alpha=90, beta=90, gamma=90,
    ),
    basis=[
        {"element": "Si", "position": [0.0, 0.0, 0.0]},
        {"element": "Si", "position": [0.25, 0.25, 0.25]},
    ],
    space_group="Fd-3m",
)

print(f"Crystal Structure:")
print(f"  Name: {structure.name}")
print(f"  Space Group: {structure.space_group}")
print(f"  Atoms: {structure.atom_count}")
print(f"  Volume: {structure.volume:.2f} Å³")
```

### XRD Simulation

```python
from crystallography import XRDSimulator, XRDPattern

simulator = XRDSimulator(
    radiation="Cu-Kα",
    wavelength=1.5406,
    two_theta_range=(10, 90),
)

# Simulate pattern
pattern = simulator.simulate(structure)
print(f"XRD Pattern:")
print(f"  Peaks: {pattern.peak_count}")
print(f"  Strongest Peak: {pattern.strongest_peak:.2f}°")
print(f"  d-spacing: {pattern.d_spacings[:3]}")
```

### Symmetry Operations

```python
from crystallography import SymmetryAnalyzer

analyzer = SymmetryAnalyzer()

# Analyze symmetry
symmetry = analyzer.analyze(structure)
print(f"Symmetry Analysis:")
print(f"  Point Group: {symmetry.point_group}")
print(f"  Space Group: {symmetry.space_group}")
print(f"  Wyckoff Positions: {symmetry.wyckoff_count}")
```

### Structure Refinement

```python
from crystallography import RietveldRefinement, RefinementParams

refinement = RietveldRefinement()

# Refine structure
result = refinement.refine(
    structure=structure,
    experimental_data=experimental_xrd,
    params=RefinementParams(
        scale_factor=True,
        background=True,
        peak_shape=True,
    ),
)

print(f"Refinement Results:")
print(f"  R-factor: {result.r_factor:.3f}")
print(f"  Rw: {result.rw:.3f}")
print(f"  Goodness of Fit: {result.gof:.3f}")
```

## Best Practices

- **Data Quality**: Use high-quality diffraction data
- **Model Selection**: Choose appropriate structural model
- **Constraints**: Apply appropriate restraints and constraints
- **Validation**: Validate refined structures
- **Documentation**: Document refinement procedures
- **Reproducibility**: Ensure reproducible results
- **Software Comparison**: Compare results from different software
- **Literature**: Compare with published structures

## Related Modules

- **computational-materials**: DFT calculations for structures
- **materials-database**: Crystal structure storage
- **molecular-simulation**: MD with crystal structures

## Advanced Configuration

### Crystal Structure Configuration

```python
from crystallography import StructureConfig, LatticeType

structure_config = StructureConfig(
    # Lattice types
    lattice_types={
        LatticeType.CUBIC: {
            "description": "Cubic (a=b=c, α=β=γ=90°)",
            "parameters": ["a"],
            "volume_formula": "a³",
        },
        LatticeType.HEXAGONAL: {
            "description": "Hexagonal (a=b≠c, α=β=90°, γ=120°)",
            "parameters": ["a", "c"],
            "volume_formula": "√3/2 × a² × c",
        },
        LatticeType.TETRAGONAL: {
            "description": "Tetragonal (a=b≠c, α=β=γ=90°)",
            "parameters": ["a", "c"],
            "volume_formula": "a² × c",
        },
        LatticeType.ORTHORHOMBIC: {
            "description": "Orthorhombic (a≠b≠c, α=β=γ=90°)",
            "parameters": ["a", "b", "c"],
            "volume_formula": "a × b × c",
        },
        LatticeType.MONOCLINIC: {
            "description": "Monoclinic (a≠b≠c, α=γ=90°, β≠90°)",
            "parameters": ["a", "b", "c", "β"],
            "volume_formula": "a × b × c × sin(β)",
        },
        LatticeType.TRICLINIC: {
            "description": "Triclinic (a≠b≠c, α≠β≠γ)",
            "parameters": ["a", "b", "c", "α", "β", "γ"],
            "volume_formula": "complex",
        },
    },
    # Space group settings
    space_group_settings={
        "full_symbol": True,
        "hall_symbol": True,
        "international_number": True,
        "setting": "standard",
    },
    # Basis representations
    basis_representations={
        "fractional": "Fractional coordinates",
        "cartesian": "Cartesian coordinates",
        "direct": "Direct lattice vectors",
        "reciprocal": "Reciprocal lattice vectors",
    },
)

config = StructureConfig(structure_config)
```

### XRD Simulation Configuration

```python
from crystallography import XRDConfig, RadiationType

xrd_config = XRDConfig(
    # Radiation sources
    radiation_sources={
        RadiationType.CU_KA: {
            "description": "Cu Kα radiation",
            "wavelength": 1.5406,
            "energy": 8.04,
            "common": True,
        },
        RadiationType.MO_KA: {
            "description": "Mo Kα radiation",
            "wavelength": 0.7107,
            "energy": 17.44,
            "common": True,
        },
        RadiationType.CO_KA: {
            "description": "Co Kα radiation",
            "wavelength": 1.7890,
            "energy": 6.93,
            "common": False,
        },
    },
    # Simulation parameters
    simulation_params={
        "two_theta_range": (5, 120),
        "step_size": 0.02,
        "peak_shape": "pseudo_voigt",
        "u_parameter": 0.5,
        "v_parameter": -0.3,
        "w_parameter": 0.1,
        "preferred_orientation": None,
    },
    # Peak detection
    peak_detection={
        "algorithm": "derivative",
        "threshold": 0.01,
        "min_intensity": 0.001,
        "max_peaks": 100,
    },
    # Background
    background={
        "method": "polynomial",
        "order": 6,
        "points": 20,
    },
)

simulator = XRDSimulator(xrd_config)
```

### Refinement Configuration

```python
from crystallography import RefinementConfig, RefinementStrategy

refinement_config = RefinementConfig(
    # Refinement strategies
    strategies={
        RefinementStrategy.LEAST_SQUARES: {
            "description": "Least squares refinement",
            "algorithm": "levenberg_marquardt",
            "convergence": 1e-6,
            "max_iterations": 100,
        },
        RefinementStrategy.RIETVELD: {
            "description": "Rietveld refinement",
            "algorithm": "rietveld",
            "convergence": 1e-6,
            "max_iterations": 50,
        },
        RefinementStrategy.PAWLEY: {
            "description": "Pawley refinement",
            "algorithm": "pawley",
            "convergence": 1e-6,
            "max_iterations": 30,
        },
    },
    # Refinable parameters
    refinable_parameters={
        "scale_factor": {"initial": 1.0, "bounds": [0, 10]},
        "background": {"initial": 0.0, "bounds": [0, 1000]},
        "zero_shift": {"initial": 0.0, "bounds": [-0.5, 0.5]},
        "lattice_parameters": {"initial": None, "bounds": [0.9, 1.1]},
        "atomic_positions": {"initial": None, "bounds": [-0.1, 0.1]},
        "thermal_parameters": {"initial": 0.5, "bounds": [0.1, 5.0]},
    },
    # Convergence criteria
    convergence_criteria={
        "r_factor": 0.05,
        "rw": 0.10,
        "gof": 1.5,
        "delta_r": 0.001,
    },
    # Restraints
    restraints={
        "bond_lengths": {"sigma": 0.01},
        "bond_angles": {"sigma": 1.0},
        "thermal_ellipsoids": {"sigma": 0.01},
    },
)

refinement = RietveldRefinement(refinement_config)
```

## Architecture Patterns

### Crystallography Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                Crystallography Pipeline                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │ Structure│──▶│ Symmetry │──▶│   XRD    │──▶│Refinement│ │
│  │  Input   │   │ Analysis │   │Simulation│   │  Engine  │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       │              │              │              │        │
│       ▼              ▼              ▼              ▼        │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Lattice │   │  Space   │   │  Peak    │   │ Parameter│ │
│  │  Builder │   │  Group   │   │Analysis  │   │ Optimizer│ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Event-Driven Crystallography

```yaml
events:
  structure.created:
    description: "New crystal structure created"
    payload:
      structure_id: "string"
      space_group: "string"
      atom_count: "integer"
    handlers:
      - validate_structure
      - analyze_symmetry
      - index_structure

  xrd.simulated:
    description: "XRD pattern simulated"
    payload:
      pattern_id: "string"
      structure_id: "string"
      peak_count: "integer"
    handlers:
      - analyze_peaks
      - compare_experimental
      - store_results

  refinement.completed:
    description: "Structure refinement completed"
    payload:
      refinement_id: "string"
      r_factor: "float"
      convergence: "boolean"
    handlers:
      - validate_refinement
      - update_structure
      - notify_users

  structure.refined:
    description: "Structure refined"
    payload:
      structure_id: "string"
      refinement_id: "string"
      improvement: "float"
    handlers:
      - update_database
      - generate_report
      - notify_users
```

### Data Flow Architecture

```python
from crystallography import CrystallographyPipeline

class CrystallographyPipeline:
    def __init__(self):
        self.structure_builder = StructureBuilder()
        self.symmetry_analyzer = SymmetryAnalyzer()
        self.xrd_simulator = XRDSimulator()
        self.refinement_engine = RietveldRefinement()

    async def analyze_structure(self, structure_data: StructureData):
        # Stage 1: Structure building
        structure = await self.structure_builder.build(structure_data)

        # Stage 2: Symmetry analysis
        symmetry = await self.symmetry_analyzer.analyze(structure)

        # Stage 3: XRD simulation
        xrd_pattern = await self.xrd_simulator.simulate(structure)

        # Stage 4: Peak analysis
        peaks = await self.analyze_peaks(xrd_pattern)

        return {
            "structure": structure,
            "symmetry": symmetry,
            "xrd_pattern": xrd_pattern,
            "peaks": peaks,
        }

    async def refine_structure(self, structure, experimental_data):
        # Stage 1: Initial refinement
        initial_result = await self.refinement_engine.refine(
            structure=structure,
            experimental_data=experimental_data,
        )

        # Stage 2: Parameter optimization
        optimized_result = await self.refinement_engine.optimize(
            initial_result,
        )

        # Stage 3: Validation
        validation = await self.validate_refinement(optimized_result)

        return {
            "refined_structure": optimized_result.structure,
            "refinement_metrics": optimized_result.metrics,
            "validation": validation,
        }
```

## Integration Guide

### Materials Database Integration

```python
from crystallography import MaterialsDBIntegration

db = MaterialsDBIntegration(
    database="materials_project",
    api_key="your_api_key",
)

# Fetch crystal structure
async def fetch_structure(material_id: str):
    return await db.get_structure(material_id)

# Store refined structure
async def store_refined_structure(structure: CrystalStructure):
    return await db.store_structure(structure)
```

### Visualization Integration

```python
from crystallography import VisualizationIntegration

viz = VisualizationIntegration(
    tools=["vesta", "pymatgen", "ase"],
)

# Visualize crystal structure
async def visualize_structure(structure: CrystalStructure):
    return await viz.create_visualizations(
        structure=structure,
        views=["unit_cell", "polyhedra", "ball_and_stick"],
        formats=["png", "pdf"],
    )

# Plot XRD pattern
async def plot_xrd_pattern(pattern: XRDPattern):
    return await viz.create_xrd_plot(
        pattern=pattern,
        format="png",
    )
```

### Diffraction Data Integration

```python
from crystallography import DiffractionDataIntegration

diffraction = DiffractionDataIntegration(
    formats=["cif", "xy", "gsas"],
)

# Import experimental data
async def import_experimental_data(file_path: str):
    return await diffraction.import_data(file_path)

# Export refined data
async def export_refined_data(structure: CrystalStructure, format: str):
    return await diffraction.export_data(structure, format)
```

## Performance Optimization

### Parallel Structure Analysis

```python
import asyncio
from crystallography import ParallelAnalyzer

analyzer = ParallelAnalyzer(max_concurrent=4)

async def parallel_analysis(structures: list):
    """Analyze multiple structures in parallel."""
    semaphore = asyncio.Semaphore(4)

    async def analyze_with_semaphore(structure):
        async with semaphore:
            return await analyzer.analyze(structure)

    tasks = [analyze_with_semaphore(s) for s in structures]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return {
        "completed": len([r for r in results if not isinstance(r, Exception)]),
        "failed": len([r for r in results if isinstance(r, Exception)]),
        "results": [r for r in results if not isinstance(r, Exception)],
    }
```

### XRD Simulation Optimization

```python
from crystallography import XRDoptimizer

xrd_optimizer = XRDoptimizer()

# Optimize simulation parameters
async def optimize_xrd_simulation(structure: CrystalStructure):
    # Determine optimal parameters
    optimal_params = await xrd_optimizer.optimize_parameters(
        structure=structure,
        criteria=["accuracy", "speed"],
    )

    # Run optimized simulation
    pattern = await xrd_optimizer.simulate(
        structure=structure,
        parameters=optimal_params,
    )

    return pattern

# Batch simulation
async def batch_xrd_simulation(structures: list):
    """Simulate XRD for multiple structures."""
    tasks = [xrd_optimizer.simulate(s) for s in structures]
    results = await asyncio.gather(*tasks)

    return results
```

### Refinement Optimization

```python
from crystallography import RefinementOptimizer

refinement_optimizer = RefinementOptimizer()

# Optimize refinement strategy
async def optimize_refinement(structure, experimental_data):
    # Determine optimal strategy
    optimal_strategy = await refinement_optimizer.optimize_strategy(
        structure=structure,
        experimental_data=experimental_data,
    )

    # Run optimized refinement
    result = await refinement_optimizer.refine(
        structure=structure,
        experimental_data=experimental_data,
        strategy=optimal_strategy,
    )

    return result
```

## Security Considerations

### Data Protection

```python
from crystallography import CrystalSecurity

security = CrystalSecurity(
    encryption_algorithm="AES-256-GCM",
    access_logging=True,
)

# Encrypt sensitive structures
@security.encrypt_sensitive
async def store_sensitive_structure(structure: CrystalStructure):
    """Store structure with encryption."""
    return await db.store(structure)

# Access control
@security.require_permission("structure.read")
async def access_structure(structure_id: str):
    """Access structure with security controls."""
    return await db.get(structure_id)
```

### Intellectual Property Protection

```python
from crystallography import IPProtection

ip_protection = IPProtection(
    watermark_enabled=True,
    access_logging=True,
)

# Protect proprietary structures
@ip_protection.protect
async def store_proprietary_structure(structure: CrystalStructure):
    """Store structure with IP protection."""
    return await db.store(structure)

# Track access
@ip_protection.track_access
async def access_proprietary_structure(structure_id: str):
    """Access structure with tracking."""
    return await db.get(structure_id)
```

### Audit Trail

```python
from crystallography import CrystalAuditTrail
from datetime import datetime

audit_trail = CrystalAuditTrail(
    storage="database",
    retention_days=2555,
)

def log_crystal_action(
    action: str,
    user_id: str,
    structure_id: str,
    details: dict = None,
):
    """Log crystallography-related action."""
    audit_trail.log(
        timestamp=datetime.utcnow(),
        action=action,
        user_id=user_id,
        resource_type="structure",
        resource_id=structure_id,
        ip_address=get_client_ip(),
        details=details or {},
    )

# Example usage
log_crystal_action(
    action="structure.created",
    user_id="user-001",
    structure_id="struct-001",
    details={"space_group": "Fd-3m", "atom_count": 8},
)
```

## Troubleshooting Guide

### Common Issues

#### Issue: Symmetry Detection Failures

```python
# Symptom: Incorrect space group assignment
# Diagnosis:
from crystallography import SymmetryDiagnostics

diagnostics = SymmetryDiagnostics()

analysis = diagnostics.analyze_symmetry("struct-001")
print(f"Detected space group: {analysis.detected_space_group}")
print(f"Expected space group: {analysis.expected_space_group}")
print(f"Symmetry operations: {analysis.symmetry_operations}")
print(f"Recommendations: {analysis.recommendations}")

# Resolution:
# 1. Check atomic positions
# 2. Verify lattice parameters
# 3. Use different tolerance
```

#### Issue: XRD Pattern Mismatch

```python
# Symptom: Simulated XRD doesn't match experimental
# Diagnosis:
from crystallography import XRDDiagnostics

xrd_diag = XRDDiagnostics()

analysis = xrd_diag.analyze_mismatch(
    simulated=simulated_pattern,
    experimental=experimental_pattern,
)
print(f"Peak shifts: {analysis.peak_shifts}")
print(f"Intensity differences: {analysis.intensity_diff}")
print(f"Recommendations: {analysis.recommendations}")

# Resolution:
# 1. Check wavelength
# 2. Verify structure
# 3. Adjust peak shape parameters
```

#### Issue: Refinement Convergence

```python
# Symptom: Refinement not converging
# Diagnosis:
from crystallography import RefinementDiagnostics

refine_diag = RefinementDiagnostics()

analysis = refine_diag.analyze_convergence("refinement-001")
print(f"Iterations: {analysis.iterations}")
print(f"R-factor history: {analysis.r_factor_history}")
print(f"Parameter changes: {analysis.parameter_changes}")
print(f"Recommendations: {analysis.recommendations}")

# Resolution:
# 1. Adjust convergence criteria
# 2. Apply restraints
# 3. Fix problematic parameters
```

## API Reference

### Structure API

```python
# POST /api/v2/structures
# Create structure

@router.post("/structures")
async def create_structure(
    request: CreateStructureRequest,
) -> StructureResponse:
    """
    Create crystal structure.

    Args:
        request: Structure creation data

    Returns:
        StructureResponse with created structure
    """
    pass

# GET /api/v2/structures/{structure_id}
# Get structure

@router.get("/structures/{structure_id}")
async def get_structure(
    structure_id: str,
) -> StructureResponse:
    """
    Get structure details.

    Args:
        structure_id: Structure identifier

    Returns:
        StructureResponse with structure details
    """
    pass
```

### XRD API

```python
# POST /api/v2/structures/{structure_id}/xrd
# Simulate XRD

@router.post("/structures/{structure_id}/xrd")
async def simulate_xrd(
    structure_id: str,
    request: XRDRequest,
) -> XRDResponse:
    """
    Simulate XRD pattern.

    Args:
        structure_id: Structure identifier
        request: XRD simulation parameters

    Returns:
        XRDResponse with simulated pattern
    """
    pass
```

### Refinement API

```python
# POST /api/v2/structures/{structure_id}/refine
# Refine structure

@router.post("/structures/{structure_id}/refine")
async def refine_structure(
    structure_id: str,
    request: RefinementRequest,
) -> RefinementResponse:
    """
    Refine crystal structure.

    Args:
        structure_id: Structure identifier
        request: Refinement parameters

    Returns:
        RefinementResponse with refinement results
    """
    pass
```

## Data Models

### Structure Model

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum

class StructureStatus(Enum):
    DRAFT = "draft"
    VALIDATED = "validated"
    REFINED = "refined"

@dataclass
class CrystalStructure:
    id: str
    name: str
    formula: str
    space_group: str
    lattice: Dict
    basis: List[Dict]
    status: StructureStatus
    atom_count: int
    volume: float
    density: float
    created_at: datetime
    updated_at: datetime
    created_by: str
    metadata: Dict
```

### XRD Model

```python
@dataclass
class XRDPattern:
    id: str
    structure_id: str
    radiation: str
    wavelength: float
    two_theta: List[float]
    intensity: List[float]
    d_spacings: List[float]
    peak_count: int
    strongest_peak: float
    created_at: datetime
```

### Refinement Model

```python
@dataclass
class RefinementResult:
    id: str
    structure_id: str
    strategy: str
    r_factor: float
    rw: float
    gof: float
    iterations: int
    converged: bool
    parameters: Dict
    created_at: datetime
    created_by: str
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crystallography-api
  namespace: materials-science
spec:
  replicas: 3
  selector:
    matchLabels:
      app: crystallography-api
  template:
    metadata:
      labels:
        app: crystallography-api
    spec:
      containers:
      - name: crystallography-api
        image: materials-science/crystallography:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: crystal-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

## Monitoring & Observability

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge

STRUCTURES_CREATED = Counter(
    'crystal_structures_created_total',
    'Total structures created'
)

XRD_SIMULATIONS = Counter(
    'crystal_xrd_simulations_total',
    'Total XRD simulations',
    ['radiation']
)

REFINEMENTS_COMPLETED = Counter(
    'crystal_refinements_completed_total',
    'Total refinements completed',
    ['strategy']
)

REFINEMENT_RFACTOR = Histogram(
    'crystal_refinement_rfactor',
    'Refinement R-factor',
    buckets=[0.01, 0.05, 0.10, 0.15, 0.20]
)
```

### Logging Configuration

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "structure_id": getattr(record, "structure_id", None),
            "user_id": getattr(record, "user_id", None),
        }
        return json.dumps(log_entry)

def setup_logging():
    logger = logging.getLogger("crystallography")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    return logger
```

## Testing Strategy

### Unit Tests

```python
import pytest
from crystallography import CrystalStructure, XRDSimulator

class TestCrystalStructure:
    def setup_method(self):
        self.structure = CrystalStructure(
            name="Test",
            lattice={"a": 5.0, "b": 5.0, "c": 5.0, "alpha": 90, "beta": 90, "gamma": 90},
            basis=[{"element": "Si", "position": [0, 0, 0]}],
            space_group="Fm-3m",
        )

    def test_volume_calculation(self):
        """Test volume calculation."""
        volume = self.structure.volume
        assert volume == 125.0
```

### Integration Tests

```python
import pytest
from httpx import AsyncClient
from crystallography import app

@pytest.mark.asyncio
class TestCrystalAPI:
    async def test_create_structure(self, async_client: AsyncClient):
        """Test structure creation endpoint."""
        response = await async_client.post(
            "/api/v2/structures",
            json={
                "name": "Test Structure",
                "lattice": {"a": 5.0, "b": 5.0, "c": 5.0},
                "basis": [{"element": "Si", "position": [0, 0, 0]}],
                "space_group": "Fm-3m",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Structure"
```

## Versioning & Migration

### API Versioning

```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.post("/structures")
async def create_structure_v1():
    pass

@v2_router.post("/structures")
async def create_structure_v2(request: CreateStructureRequest):
    pass

app.include_router(v1_router)
app.include_router(v2_router)
```

### Database Migrations

```python
# migrations/001_initial_schema.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'structures',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('formula', sa.String(200), nullable=False),
        sa.Column('space_group', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table('structures')
```

## Glossary

### Crystallography Terms

| Term | Definition |
|------|------------|
| **Lattice** | Regular array of points in space |
| **Unit Cell** | Smallest repeating unit of crystal |
| **Space Group** | Symmetry operations of crystal |
| **Miller Indices** | Indices defining crystal planes |
| **d-spacing** | Distance between crystal planes |
| **Bragg's Law** | nλ = 2d sin(θ) |
| **R-factor** | Measure of refinement quality |
| **Wyckoff Position** | Symmetry-equivalent positions |
| **Basis** | Atoms associated with lattice points |
| **Reciprocal Lattice** | Fourier transform of real lattice |

## Changelog

### Version 2.0.0 (2024-01-15)
- Added advanced refinement
- Implemented parallel analysis
- Enhanced XRD simulation
- Added visualization tools

### Version 1.5.0 (2023-10-01)
- Added symmetry analysis
- Implemented Rietveld refinement
- Enhanced structure manipulation
- Added reporting

### Version 1.4.0 (2023-07-15)
- Added XRD simulation
- Implemented peak analysis
- Added structure input
- Enhanced security

### Version 1.3.0 (2023-04-01)
- Added crystal structures
- Implemented lattice calculations
- Added space group support
- Enhanced API

### Version 1.2.0 (2023-01-15)
- Added basic structures
- Implemented lattice builder
- Added unit cell calculations
- Enhanced documentation

### Version 1.1.0 (2022-10-01)
- Added structure input
- Implemented basic analysis
- Added visualization
- Enhanced UI

### Version 1.0.0 (2022-07-15)
- Initial release
- Basic crystallography
- REST API
- PostgreSQL support

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/company/crystallography.git
cd crystallography
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest
uvicorn main:app --reload
```

### Code Standards

- Follow PEP 8
- Use type hints
- Write docstrings
- Maintain 80% test coverage
- Run linting before commit

## License

MIT License

Copyright (c) 2024 Crystallography Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
