---
name: "quantum-simulation"
category: "quantum-computing"
version: "2.0.0"
tags: ["quantum-computing", "quantum-simulation", "hamiltonian", "molecular", "condensed-matter", "trotter", "vqe"]
---

# Quantum Simulation

## Overview

The quantum-simulation module provides tools for simulating quantum systems on both classical and quantum hardware. It implements Hamiltonian simulation methods (Trotter-Suzuki decomposition, linear combination of unitaries, quantum signal processing), molecular electronic structure simulation, condensed matter physics models (Ising, Hubbard, Heisenberg, Fermi-Hubbard), quantum dynamics, open quantum systems with Lindblad master equations, and variational quantum simulation.

This module is designed for computational physicists, quantum chemists, and materials scientists who need to simulate quantum systems from first principles. It supports both digital quantum simulation (circuit-based) and analog quantum simulation (Hamiltonian encoding), with configurable noise models and error mitigation strategies. The module includes classical pre-processing for Hamiltonian construction, symmetry reduction, and embedding methods for large systems.

The simulation engine provides a unified interface for time evolution, ground state search, spectral analysis, and dynamics simulation. It integrates with quantum chemistry packages (PySCF, OpenFermion) for molecular Hamiltonian construction and with condensed matter libraries for lattice model definition. All simulations include resource estimation, error bound computation, and validation against classical exact solutions where feasible.

## Core Capabilities

- **Trotter-Suzuki Decomposition**: First-order and second-order Trotter-Suzuki product formulas for time-evolution simulation with controllable Trotter error bounds. Higher-order formulas available for improved accuracy.
- **Linear Combination of Unitaries (LCU)**: Hamiltonian simulation via oracle-based LCU with quantum signal processing for optimal query complexity. Achieves optimal scaling in Hamiltonian norm.
- **Molecular Electronic Structure**: Hartree-Fock, full configuration interaction (FCI), and coupled cluster (CCSD) calculations for molecular systems with up to 50+ qubits. Includes active space selection and frozen core approximation.
- **Ising Model Simulation**: Transverse-field Ising model, XXZ model, and classical Ising model dynamics with configurable coupling constants and boundary conditions. Supports 1D chains, 2D lattices, and custom geometries.
- **Hubbard Model**: Fermi-Hubbard model simulation for strongly correlated electron systems — critical for understanding high-temperature superconductivity, Mott transitions, and magnetic ordering.
- **Heisenberg Model**: XXX, XXZ, and XYZ Heisenberg spin chain dynamics with arbitrary coupling constants and external magnetic fields. Includes entanglement entropy and correlation function computation.
- **Open Quantum Systems**: Lindblad master equation solver for dissipative quantum dynamics with configurable collapse operators and bath coupling. Supports both Markovian and non-Markovian dynamics.
- **Variational Quantum Simulation**: Hardware-efficient ansatz for real-time dynamics simulation on NISQ devices. Includes variational quantum imaginary time evolution (VarQITE) and variational quantum simulation (VQS).
- **Quantum Phase Estimation**: Extract eigenvalues of quantum operators for spectroscopy and energy measurement. Supports both canonical and iterative QPE.
- **Noise-Aware Simulation**: Configurable noise models (depolarizing, dephasing, amplitude damping, readout error) for realistic quantum device simulation. Includes circuit-level noise modeling.
- **Observable Measurement**: Expectation value computation for Pauli strings, molecular orbital operators, and custom observables. Supports shadow tomography for efficient multi-observable estimation.
- **Energy Landscape Mapping**: Scan potential energy surfaces for molecular dissociation, reaction pathways, and conical intersections. Includes geometry optimization and transition state search.

## Usage Examples

### Transverse-Field Ising Model

```python
from quantum_simulation import (
    SimulationEngine, HamiltonianType, SimulationMethod,
    NoiseConfig, BackendConfig
)

# 1D transverse-field Ising model
engine = SimulationEngine(
    hamiltonian_type=HamiltonianType.TRANSVERSE_ISING,
    num_qubits=8,
    backend=BackendConfig(num_qubits=8, shots=4096),
    noise=NoiseConfig(depolarizing_rate=0.005)
)

result = engine.run(
    method=SimulationMethod.TROTTER_SECOND_ORDER,
    time_steps=50,
    final_time=2.0,
    coupling_constants={"J": 1.0, "h": 0.5},
    boundary="periodic"
)

print(f"Ground state energy: {result.ground_state_energy:.6f}")
print(f"Magnetization: {result.magnetization:.4f}")
print(f"Circuit depth: {result.circuit_depth}")
print(f"Trotter error: {result.trotter_error:.2e}")
```

### Molecular Electronic Structure

```python
from quantum_simulation import SimulationEngine, MoleculeConfig, SimulationMethod

molecule = MoleculeConfig(
    atoms=["H", "H"],
    bond_distance=0.735,
    basis="sto-3g",
    charge=0,
    multiplicity=1
)

engine = SimulationEngine(
    hamiltonian_type=HamiltonianType.MOLECULAR,
    molecule=molecule
)

# VQE for ground state energy
result = engine.run(
    method=SimulationMethod.VQE,
    ansatz="UCCSD",
    optimizer="COBYLA",
    max_iterations=200,
    convergence_threshold=1e-8
)

print(f"VQE energy: {result.ground_state_energy:.8f} Ha")
print(f"Exact energy: {result.exact_energy:.8f} Ha")
print(f"Coefficients: {result.ansatz_parameters}")
```

### Fermi-Hubbard Model

```python
from quantum_simulation import SimulationEngine, HamiltonianType, SimulationMethod

engine = SimulationEngine(
    hamiltonian_type=HamiltonianType.FERMI_HUBBARD,
    num_qubits=8
)

result = engine.run(
    method=SimulationMethod.VQE,
    hopping_amplitude=1.0,
    on_site_repulsion=4.0,
    filling=0.5,
    lattice_geometry="chain",
    num_layers=4
)

print(f"Ground state energy: {result.ground_state_energy:.6f}")
print(f"Double occupancy: {result.metadata.get('double_occupancy', 0):.4f}")
print(f"Momentum distribution: {result.metadata.get('momentum_distribution', [])}")
```

### Heisenberg Spin Chain

```python
from quantum_simulation import SimulationEngine, HamiltonianType, SimulationMethod

engine = SimulationEngine(
    hamiltonian_type=HamiltonianType.HEISENBERG_XXX,
    num_qubits=6
)

result = engine.run(
    method=SimulationMethod.TROTTER_SECOND_ORDER,
    time_steps=30,
    final_time=3.0,
    coupling={"Jx": 1.0, "Jy": 1.0, "Jz": 1.0},
    magnetic_field=0.5
)

print(f"Entanglement entropy: {result.metadata.get('entanglement_entropy', []):.4f}")
print(f"Spin correlations: {result.metadata.get('spin_correlations', [])}")
```

### Open Quantum System (Lindblad Dynamics)

```python
from quantum_simulation import SimulationEngine, LindbladConfig

lindblad = LindbladConfig(
    collapse_operators=["sigma_minus", "sigma_z"],
    bath_temperature=0.1,
    coupling_strength=0.01
)

engine = SimulationEngine(
    hamiltonian_type=HamiltonianType.TWO_LEVEL,
    num_qubits=2,
    lindblad_config=lindblad
)

result = engine.run(
    method=SimulationMethod.LINDBLAD,
    time_steps=100,
    final_time=5.0
)

print(f"Purity: {result.metadata.get('purity', []):.4f}")
print(f"Coherence: {result.metadata.get('coherence', []):.4f}")
```

### Energy Surface Scan

```python
from quantum_simulation import SimulationEngine, MoleculeConfig, BondDistanceScan

molecule = MoleculeConfig(atoms=["H", "H"], basis="sto-3g")
scan = BondDistanceScan(molecule=molecule, min_distance=0.3, max_distance=3.0, steps=20)

engine = SimulationEngine(hamiltonian_type=HamiltonianType.MOLECULAR, molecule=molecule)
result = engine.scan_energy_surface(scan=scan, method=SimulationMethod.VQE)

for point in result.energy_points:
    print(f"R={point.bond_distance:.2f} A: E={point.energy:.6f} Ha")
```

## Architecture

```
quantum_simulation/
  __init__.py
  hamiltonians/
    ising.py                # Transverse-field Ising model
    heisenberg.py           # XXX/XXZ/XYZ Heisenberg models
    hubbard.py              # Fermi-Hubbard model
    molecular.py            # Molecular electronic structure Hamiltonians
    custom.py               # Custom Hamiltonian construction
  methods/
    trotter.py              # Trotter-Suzuki product formulas
    lcu.py                  # Linear Combination of Unitaries
    qsp.py                  # Quantum Signal Processing
    vqe.py                  # Variational Quantum Eigensolver
    qpe.py                  # Quantum Phase Estimation
    lindblad.py             # Lindblad master equation solver
    varqite.py              # Variational Quantum Imaginary Time Evolution
  encoding/
    jordan_wigner.py        # Jordan-Wigner transformation
    bravyi_kitaev.py        # Bravyi-Kitaev transformation
    parity.py               # Parity transformation
    fermionic.py            # Fermionic encoding utilities
  noise/
    depolarizing.py         # Depolarizing noise channel
    dephasing.py            # Dephasing noise channel
    amplitude_damping.py    # Amplitude damping channel
    circuit_level.py        # Circuit-level noise model
  observables/
    pauli_strings.py        # Pauli string expectation values
    molecular_orbitals.py   # Molecular orbital operators
    correlation.py          # Correlation functions
    entanglement.py         # Entanglement entropy computation
  analysis/
    energy_landscape.py     # Potential energy surface scanning
    spectral.py             # Spectral analysis
    dynamics.py             # Time dynamics analysis
    resource_estimator.py   # Qubit and gate count estimation
```

## Best Practices

1. **Trotter step size**: Use step size dt <= 0.01 for second-order Trotter to keep error below 10^-4. For first-order, use dt <= 0.005. Scale inversely with Hamiltonian norm ||H||.

2. **Molecular basis selection**: Use STO-3G for prototyping, 6-31G* for medium accuracy, and cc-pVTZ for production-quality results. Larger bases require more qubits via Jordan-Wigner or Bravyi-Kitaev mapping.

3. **VQE convergence**: Use COBYLA for noisy backends (gradient-free), L-BFGS-B for noiseless (gradient-based). Start from Hartree-Fock initial point. Monitor cost function variance across shots and use parameter initialization strategies.

4. **Noise mitigation**: Apply zero-noise extrapolation with at least 3 noise levels. Use readout error mitigation for all shot-based measurements. Consider probabilistic error cancellation for small circuits and clifford data regression for larger ones.

5. **Qubit encoding**: Jordan-Wigner preserves fermion symmetry but uses O(N) qubit overhead. Bravyi-Kitaev reduces to O(log N) but requires careful operator transformation. Choose based on system size and operator locality requirements.

6. **Symmetry exploitation**: Use particle number conservation, spin symmetry, and point group symmetry to reduce circuit depth. Block-diagonalize Hamiltonian before simulation. Implement symmetry verification as a post-selection step.

7. **Error bounds**: Always compute and report Trotter error bounds. Use commutator-based bounds for first-order and nested commutator bounds for second-order formulas. Include both upper and lower bounds when possible.

8. **Classical pre-processing**: Diagonalize small subsystems classically. Use embedding methods (DMET, dynamical mean-field theory) for large systems where full quantum simulation is infeasible. Active space selection reduces qubit count dramatically.

9. **Resource estimation**: Before running on real hardware, estimate T-gate count, circuit depth, and number of logical qubits. Surface code overhead is ~1000x for fault-tolerant execution. Plan accordingly for algorithm runtime.

10. **Validation**: Always compare quantum simulation results with classical exact diagonalization for small instances (<= 12 qubits). Use fidelity metrics, energy errors, and correlation function comparison to quantify agreement.

## Performance Considerations

- **Trotter error scaling**: Second-order Trotter error scales as O(dt^3), making it 5-10x more accurate than first-order O(dt^2) for the same step size. Use higher-order formulas for high-precision simulations.
- **Circuit depth vs accuracy**: More Trotter steps improve accuracy but increase circuit depth. For NISQ devices, balance Trotter error against noise accumulation. Typically, dt=0.01 with 100 steps is a good starting point.
- **VQE iteration count**: VQE typically converges in 20-200 iterations depending on ansatz, optimizer, and noise level. Each iteration requires 2^n_evaluation circuits for gradient estimation (or 2 for SPSA).
- **Memory scaling**: Classical statevector simulation requires 2^n complex amplitudes. For n=25 qubits, this is ~1 GB. Quantum hardware avoids this but introduces noise. Use matrix product state (MPS) methods for weakly entangled systems.
- **Hamiltonian construction**: Molecular Hamiltonian construction scales as O(N^4) classically for N basis functions. Use integral pre-screening and symmetry to reduce this. Pre-compute and cache Hamiltonian coefficients.
- **Noise threshold**: For variational algorithms, noise above ~10^-3 per gate causes convergence failure. Use error mitigation to effectively reduce noise below this threshold. Zero-noise extrapolation can improve results by 2-5x.

## Security Considerations

- **Simulation data confidentiality**: Molecular and materials simulation results may have commercial value (drug design, catalyst optimization). Protect simulation data with appropriate access controls and encryption.
- **Code integrity**: Verify that simulation codes produce correct results by comparing against known analytical solutions and classical benchmarks. Tampered simulation code could produce incorrect scientific results.
- **Reproducibility**: Ensure all simulations are reproducible by recording random seeds, hardware configurations, and software versions. Use containerized environments for long-term reproducibility.
- **Resource estimation sensitivity**: Quantum resource estimates for specific problems may reveal strategic capabilities (e.g., drug discovery timelines, materials design advantages). Treat resource estimates as sensitive in competitive contexts.
- **Cloud quantum computing**: When using cloud quantum backends, be aware that circuit descriptions and measurement results may be logged by the provider. Use local simulators for sensitive simulations.

## Related Modules

- **quantum-algorithms** — Algorithmic primitives (VQE, QPE, Grover) used within simulation methods; the algorithm framework that drives simulation execution and provides optimization subroutines.
- **quantum-optimization** — Variational optimization methods (QAOA) applied to simulation parameter tuning and Hamiltonian ground state search. Includes QUBO formulation for combinatorial simulation problems.
- **quantum-error-correction** — Error correction codes that protect simulation circuits; essential for scaling to large molecular and condensed matter systems beyond NISQ limitations.
- **quantum-cryptography** — Quantum-secure protocols for transmitting simulation results and Hamiltonian data across quantum networks. Includes secure multi-party computation for collaborative simulations.

## References

- Aspuru-Guzik, A. et al. (2005). Simulated quantum computation of molecular energies. *Science*, 309(5741), 1704-1707.
- Bauer, B. et al. (2020). Quantum algorithms for quantum chemistry and quantum materials science. *Chemical Reviews*, 120(22), 12685-12717.
- Childs, A. M. et al. (2018). THEORY OF TROTTER ERROR WITH AND WITHOUT SYMMETRIES. *PRX Quantum*, 2(3), 030305.
- McArdle, S. et al. (2020). Quantum computational chemistry. *Reviews of Modern Physics*, 92(1), 015003.
- Kandala, A. et al. (2017). Hardware-efficient variational quantum eigensolver for small molecules and quantum magnets. *Nature*, 549(7671), 242-246.
- Preskill, J. (2018). Quantum computing in the NISQ era and beyond. *Quantum*, 2, 79.

## Advanced Configuration

### Hamiltonian Construction Configuration

```python
from quantum_simulation import HamiltonianBuilder, HamiltonianType, EncodingType

# Advanced Hamiltonian construction
builder = HamiltonianBuilder(
    hamiltonian_type=HamiltonianType.MOLECULAR,
    encoding=EncodingType.BRAVYI_KITAEV,
    active_space_selection=True,
    active_orbitals=6,
    frozen_core=True,
    symmetry_reduction=True,
    point_group="d2h",
)

hamiltonian = builder.build(
    molecule="LiH",
    basis="cc-pvdz",
    charge=0,
    multiplicity=1,
)

print(f"Hilbert space dimension: {hamiltonian.hilbert_dimension}")
print(f"Number of qubits: {hamiltonian.n_qubits}")
print(f"Number of Pauli terms: {hamiltonian.n_terms}")
print(f"Sparsity: {hamiltonian.sparsity:.4f}")
```

### Trotter Error Control Configuration

```python
from quantum_simulation import TrotterConfig, ErrorBound

trotter_config = TrotterConfig(
    order=2,
    num_steps=100,
    final_time=2.0,
    error_bound=ErrorBound(
        method="commutator",
        max_error=1e-4,
        adaptive_step_size=True,
        min_step_size=0.001,
        max_step_size=0.1,
    ),
    symmetry_verification=True,
    post_selection=True,
)

engine = SimulationEngine(
    hamiltonian_type=HamiltonianType.TRANSVERSE_ISING,
    trotter_config=trotter_config,
)

result = engine.run_trotter()
print(f"Trotter error: {result.trotter_error:.2e}")
print(f"Actual step sizes: {result.step_sizes[:5]}")
```

### Noise-Aware Simulation Configuration

```python
from quantum_simulation import NoiseConfig, CircuitNoiseModel

noise_config = NoiseConfig(
    circuit_noise=CircuitNoiseModel(
        single_qubit_error_rate=1e-4,
        two_qubit_error_rate=1e-3,
        measurement_error_rate=0.02,
        idle_error_rate=1e-5,
        t1=50e3,
        t2=70e3,
        gate_time_1q=35,
        gate_time_2q=300,
    ),
    error_mitigation={
        "method": "zne",
        "extrapolation": "linear",
        "noise_factors": [1.0, 1.5, 2.0],
        "readout_mitigation": True,
        "readout_shots": 8192,
    },
)

engine = SimulationEngine(
    hamiltonian_type=HamiltonianType.MOLECULAR,
    noise_config=noise_config,
)
```

## Architecture Patterns

### Simulation Pipeline Pattern

```python
from quantum_simulation import SimulationPipeline, PipelineStage

pipeline = SimulationPipeline(stages=[
    PipelineStage(
        name="hamiltonian_construction",
        type="classical",
        processor=lambda x: build_hamiltonian(x),
    ),
    PipelineStage(
        name="encoding",
        type="quantum",
        processor=lambda x: encode_hamiltonian(x),
    ),
    PipelineStage(
        name="time_evolution",
        type="quantum",
        processor=lambda x: evolve_state(x),
    ),
    PipelineStage(
        name="measurement",
        type="quantum",
        processor=lambda x: measure_observables(x),
    ),
    PipelineStage(
        name="analysis",
        type="classical",
        processor=lambda x: analyze_results(x),
    ),
])

result = pipeline.execute(molecule="H2", time=2.0)
```

### Variational Simulation Pattern

```python
from quantum_simulation import VariationalSimulator, VariationalConfig

var_config = VariationalConfig(
    ansatz="uccsd",
    optimizer="cobyla",
    max_iterations=200,
    convergence_threshold=1e-6,
    error_mitigation=True,
    symmetry_verification=True,
)

simulator = VariationalSimulator(
    hamiltonian_type=HamiltonianType.MOLECULAR,
    variational_config=var_config,
)

result = simulator.find_ground_state(molecule="H2", basis="sto-3g")
print(f"Ground state energy: {result.energy:.8f} Ha")
print(f"Chemical accuracy: {result.chemical_accuracy_mHartree:.3f} mHa")
```

### Energy Surface Mapping Pattern

```python
from quantum_simulation import EnergySurfaceMapper, ScanConfig

scan_config = ScanConfig(
    min_distance=0.3,
    max_distance=3.0,
    steps=20,
    method="vqe",
    interpolation="spline",
)

mapper = EnergySurfaceMapper(
    hamiltonian_type=HamiltonianType.MOLECULAR,
    scan_config=scan_config,
)

surface = mapper.scan(molecule="H2", basis="sto-3g")
print(f"Equilibrium distance: {surface.equilibrium_distance:.3f} A")
print(f"Dissociation energy: {surface.dissociation_energy:.6f} Ha")
print(f"Dissociation curve saved: {surface.plot_path}")
```

## Integration Guide

### PySCF Integration

```python
from quantum_simulation import PySCFAdapter, MoleculeConfig

adapter = PySCFAdapter()

# Convert PySCF molecule to quantum simulation format
pyscf_mol = adapter.create_pyscf_molecule(
    atoms=["H", "H"],
    basis="sto-3g",
    charge=0,
    multiplicity=1,
)

# Get Hamiltonian
hamiltonian = adapter.get_hamiltonian(pyscf_mol, encoding="jordan_wigner")
print(f"Qubits needed: {hamiltonian.n_qubits}")
print(f"Pauli terms: {hamiltonian.n_terms}")

# Get exact energy
exact_energy = adapter.get_exact_energy(pyscf_mol)
print(f"Exact energy: {exact_energy:.8f} Ha")
```

### OpenFermion Integration

```python
from quantum_simulation import OpenFermionAdapter

adapter = OpenFermionAdapter()

# Convert OpenFermion operator to quantum simulation format
from openfermion import FermionOperator
openfermion_op = FermionOperator('0^ 1', 1.0)

quantum_op = adapter.convert_operator(openfermion_op)
print(f"Converted operator: {quantum_op}")
print(f"Number of terms: {quantum_op.n_terms}")
```

## Performance Optimization

### Circuit Optimization

```python
from quantum_simulation import CircuitOptimizer

optimizer = CircuitOptimizer(
    optimization_level=3,
    target_gates=["cx", "u3"],
    coupling_map="ibmq_mumbai",
)

optimized = optimizer.optimize(circuit)
print(f"Original depth: {circuit.depth()}")
print(f"Optimized depth: {optimized.depth()}")
print(f"Gate reduction: {(1 - optimized.depth()/circuit.depth())*100:.1f}%")
```

### Parallel Execution

```python
from quantum_simulation import ParallelExecutor

executor = ParallelExecutor(
    max_workers=8,
    batch_size=100,
    backend="aer_simulator",
)

circuits = [create_circuit(params) for params in parameter_list]
results = executor.execute_batch(circuits)
print(f"Total time: {results.total_time_ms:.1f} ms")
print(f"Throughput: {results.circuits_per_second:.1f} circuits/s")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Trotter Error Too Large

**Symptom**: Error > 1e-3, results inaccurate

**Solution**:
```python
# Increase number of steps
trotter_config.num_steps = 200

# Use higher-order Trotter
trotter_config.order = 4

# Use adaptive step size
trotter_config.error_bound.adaptive_step_size = True
```

#### 2. VQE Not Converging

**Symptom**: Energy oscillates or plateaus

**Solution**:
```python
# Use better optimizer
var_config.optimizer = "l-bfgs-b"

# Start from Hartree-Fock
var_config.initial_point = "hf"

# Increase max iterations
var_config.max_iterations = 500
```

#### 3. Circuit Depth Too Large

**Symptom**: Exceeds hardware limits

**Solution**:
```python
# Use active space selection
builder.active_space_selection = True
builder.active_orbitals = 4

# Use simpler encoding
builder.encoding = EncodingType.JORDAN_WIGENER

# Compress circuit
from quantum_simulation import compress_circuit
compressed = compress_circuit(circuit)
```

## API Reference

### Core Classes

#### `SimulationEngine`
```python
class SimulationEngine:
    def __init__(self, hamiltonian_type: HamiltonianType, **kwargs) -> None: ...
    def run(self, method: SimulationMethod, **kwargs) -> SimulationResult: ...
    def run_trotter(self, **kwargs) -> TrotterResult: ...
    def run_vqe(self, **kwargs) -> VQEResult: ...
    def run_qpe(self, **kwargs) -> QPEResult: ...
```

## Data Models

### Simulation Result Schema

```json
{
  "method": "vqe",
  "status": "success",
  "ground_state_energy": -1.8572750302,
  "exact_energy": -1.8572750302,
  "chemical_accuracy_mHartree": 0.001,
  "circuit_depth": 45,
  "gate_count": {"cx": 12, "u3": 8},
  "execution_time_ms": 125.3,
  "convergence_iterations": 50
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quantum_simulation/ /app/quantum_simulation/
WORKDIR /app

ENV QS_BACKEND=default.qubit
ENV QS_OPTIMIZATION_LEVEL=2

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from quantum_simulation import health_check; health_check()"

CMD ["python", "-m", "quantum_simulation.server"]
```

## Monitoring & Observability

### Metrics Collection

```python
from quantum_simulation import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("qs_energy", type="gauge")
collector.register_metric("qs_trotter_error", type="gauge")
collector.register_metric("qs_circuit_depth", type="gauge")
collector.register_metric("qs_execution_time", type="histogram")

collector.set("qs_energy", result.energy)
collector.set("qs_trotter_error", result.trotter_error)
collector.set("qs_circuit_depth", result.circuit_depth)
collector.observe("qs_execution_time", exec_time_ms)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from quantum_simulation import SimulationEngine, HamiltonianType

class TestSimulation:
    def setup_method(self):
        self.engine = SimulationEngine(
            hamiltonian_type=HamiltonianType.TRANSVERSE_ISING,
            num_qubits=4,
        )
    
    def test_trotter_convergence(self):
        result = self.engine.run_trotter(num_steps=100, final_time=1.0)
        assert result.trotter_error < 1e-3
    
    def test_vqe_ground_state(self):
        result = self.engine.run_vqe(molecule="H2")
        assert abs(result.energy - (-1.857)) < 0.01
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: Adaptive Trotter step sizes
- **Added**: Noise-aware simulation
- **Improved**: 2x faster VQE convergence
- **Fixed**: Memory leak in long simulations

## Glossary

| Term | Definition |
|------|------------|
| **Trotter-Suzuki** | Product formula for time evolution |
| **VQE** | Variational Quantum Eigensolver |
| **QPE** | Quantum Phase Estimation |
| **Hamiltonian** | Quantum observable representing energy |
| **Jordan-Wigner** | Fermion-to-qubit mapping |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/quantum-simulation.git
cd quantum-simulation
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Quantum Simulation Contributors

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

---

*Last updated: 2024-01-15*
*Version: 2.0.0*

## Data Validation

### Input Validation

```python
from quantum_simulation import InputValidator

validator = InputValidator()

# Validate Hamiltonian
validator.validate_hamiltonian(hamiltonian)

# Validate circuit parameters
validator.validate_parameters(parameters, bounds=(-3.14, 3.14))

# Validate simulation config
validator.validate_config(simulation_config)
```

### Output Validation

```python
from quantum_simulation import OutputValidator

validator = OutputValidator()

# Validate simulation results
validator.validate_result(result)

# Validate energy bounds
validator.validate_energy_bounds(result.energy, expected_bounds=(-10.0, 0.0))

# Validate physical constraints
validator.validate_physical_constraints(result)
```

## Advanced Patterns

### Hamiltonian Simulation Patterns

```python
from quantum_simulation import HamiltonianSimulator, SimulationPattern

simulator = HamiltonianSimulator(
    pattern=SimulationPattern.TROTTER_SUZUKI,
    order=2,
    num_steps=100,
    error_bound=1e-4,
)

# Simulate time evolution
result = simulator.simulate(
    hamiltonian=ising_hamiltonian,
    initial_state=initial_state,
    time=2.0,
    observables=["energy", "magnetization"],
)

print(f"Final energy: {result.energy:.6f}")
print(f"Final magnetization: {result.magnetization:.4f}")
```

### Variational Simulation Patterns

```python
from quantum_simulation import VariationalSimulator, VariationalPattern

var_simulator = VariationalSimulator(
    pattern=VariationalPattern.VQE,
    ansatz="uccsd",
    optimizer="cobyla",
    max_iterations=200,
    convergence_threshold=1e-6,
)

# Find ground state
result = var_simulator.find_ground_state(
    hamiltonian=molecular_hamiltonian,
    initial_point="hartree-fock",
)

print(f"Ground state energy: {result.energy:.8f} Ha")
print(f"Chemical accuracy: {result.chemical_accuracy:.3f} mHa")
```

### Noise Simulation Patterns

```python
from quantum_simulation import NoiseSimulator, NoisePattern

noise_simulator = NoiseSimulator(
    pattern=NoisePattern.CIRCUIT_LEVEL,
    noise_model={
        "single_qubit_error": 1e-4,
        "two_qubit_error": 1e-3,
        "measurement_error": 0.02,
        "t1": 50e3,
        "t2": 70e3,
    },
)

# Simulate with noise
noisy_result = noise_simulator.simulate(circuit)
clean_result = noise_simulator.simulate(circuit, noise=False)

print(f"Noisy energy: {noisy_result.energy:.6f}")
print(f"Clean energy: {clean_result.energy:.6f}")
print(f"Noise impact: {abs(noisy_result.energy - clean_result.energy):.6f}")
```

### Error Mitigation Patterns

```python
from quantum_simulation import ErrorMitigator, MitigationPattern

mitigator = ErrorMitigator(
    pattern=MitigationPattern.ZERO_NOISE_EXTRAPOLATION,
    noise_factors=[1.0, 1.5, 2.0],
    extrapolation="linear",
)

# Apply error mitigation
mitigated_result = mitigator.mitigate(
    circuit=circuit,
    backend=backend,
    shots=8192,
)

print(f"Raw energy: {raw_result.energy:.6f}")
print(f"Mitigated energy: {mitigated_result.energy:.6f}")
print(f"Improvement: {abs(raw_result.energy - exact_energy) - abs(mitigated_result.energy - exact_energy):.6f}")
```

### Resource Estimation Patterns

```python
from quantum_simulation import ResourceEstimator, EstimationPattern

estimator = ResourceEstimator(
    pattern=EstimationPattern.SURFACE_CODE,
    physical_error_rate=0.001,
    logical_error_rate=1e-10,
)

# Estimate resources
resources = estimator.estimate(
    algorithm="vqe",
    molecule="LiH",
    basis="sto-3g",
    method="uccsd",
)

print(f"Logical qubits: {resources.logical_qubits}")
print(f"Physical qubits: {resources.physical_qubits}")
print(f"T-gates: {resources.t_gate_count}")
print(f"Circuit depth: {resources.circuit_depth}")
```

### Benchmarking Patterns

```python
from quantum_simulation import BenchmarkSuite, BenchmarkPattern

benchmark = BenchmarkSuite(
    pattern=BenchmarkPattern.RANDOM_CIRCUIT,
    num_qubits_range=[4, 6, 8, 10],
    depth_range=[10, 20, 30, 40],
    num_circuits=100,
)

# Run benchmark
results = benchmark.run(backend=backend)
print(f"Average fidelity: {results.avg_fidelity:.4f}")
print(f"Fidelity decay: {results.fidelity_decay_rate:.4f}")
print(f"Cross-entropy benchmark: {results.xeb_score:.4f}")
```
