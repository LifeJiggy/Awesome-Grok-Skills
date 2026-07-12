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
