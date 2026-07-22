---
name: "quantum-simulation"
category: "quantum"
version: "1.0.0"
tags: ["quantum", "simulation", "hamiltonian", "trotter", "open-system"]
---

# Quantum Simulation Module

## Overview

The Quantum Simulation module provides tools for simulating quantum many-body systems, open quantum systems, and dynamical processes. It implements Hamiltonian simulation via Trotterization, matrix product state (MPS) methods, Lindblad master equation solvers, and quantum process tomography. The module supports both closed-system unitary evolution and open-system dynamics with environmental coupling, making it suitable for studying decoherence, thermalization, and quantum error processes in realistic physical systems.

The module bridges theoretical quantum physics and practical quantum computing by providing efficient simulation tools for systems ranging from small quantum circuits to large many-body spin systems. It includes state-of-the-art numerical methods for time evolution, including adaptive time-stepping, tensor network compression, and quantum Monte Carlo techniques. The open-system capabilities enable accurate modeling of realistic quantum devices, including noise characterization, error channel analysis, and decoherence modeling essential for quantum algorithm development and hardware benchmarking.

All simulation methods include convergence analysis, error estimation, and resource scaling characterization. The module provides both exact methods for small systems and approximate methods for larger systems with controlled accuracy. Whether you are studying quantum phase transitions, analyzing quantum error correction codes, or characterizing quantum hardware noise, this module provides the numerical tools needed for rigorous quantum simulation research.

## Core Capabilities

- **Hamiltonian Simulation**: First- and second-order Trotter-Suzuki decomposition for time evolution with automatic error control, commutator analysis, and adaptive time-step selection for optimal accuracy-efficiency tradeoffs.
- **Open-System Dynamics**: Lindblad master equation solver with arbitrary jump operators, including Monte Carlo wavefunction methods for large systems and deterministic master equation solvers for small systems.
- **Density Matrix Evolution**: Full density matrix propagation for small systems with support for non-Markovian dynamics, time-dependent Hamiltonians, and environmental correlation functions.
- **MPS Methods**: Matrix product state approximation for large 1D systems with automatic bond dimension truncation, time-dependent DMRG, and entanglement entropy monitoring.
- **Correlation Functions**: Compute auto-correlation and cross-correlation functions with spectral analysis, including dynamical structure factors and response functions for linear response theory.
- **Spectral Analysis**: Eigenvalue decomposition and spectral gap estimation with support for partial spectra, Lanczos algorithms, and Arnoldi methods for large sparse Hamiltonians.
- **Thermal States**: Gibbs state preparation at finite temperature using imaginary time evolution, quantum imaginary time evolution (QITE), and minimum entropy principles.
- **Noise Channels**: Apply depolarizing, amplitude damping, phase damping, and amplitude-phase damping channels with configurable parameters for realistic noise modeling.
- **Tomography**: Quantum process and state tomography from measurement data with maximum likelihood estimation, Bayesian inference, and compressed sensing techniques for efficient reconstruction.
- **Entanglement Measures**: Von Neumann entropy, concurrence, entanglement of formation, and logarithmic negativity with support for multipartite entanglement measures and entanglement spectrum analysis.

## Usage Examples

### Time Evolution with Trotterization

```python
from quantum_simulation import HamiltonianSimulator, PauliTerm, SpinChain

# Build Heisenberg chain Hamiltonian
chain = SpinChain(
    num_sites=4,
    coupling_j=1.0,
    field_h=0.5,
    boundary="open"  # or "periodic"
)
hamiltonian = chain.heisenberg_hamiltonian()

# Simulate time evolution with error control
simulator = HamiltonianSimulator(
    hamiltonian,
    num_qubits=4,
    method="trotter",
    order=2,
    error_tolerance=1e-6
)

initial_state = simulator.zero_state()
evolved = simulator.trotter_evolve(
    initial_state,
    time=1.0,
    steps=100,
    order=2,
    adaptive_time_step=True
)

print(f"Fidelity to initial: {simulator.fidelity(initial_state, evolved):.4f}")
print(f"Entanglement entropy: {simulator.entanglement_entropy(evolved):.4f}")
```

### Lindblad Open-System Simulation

```python
from quantum_simulation import LindbladSolver, AmplitudeDampingChannel

# T1 relaxation channel
damping = AmplitudeDampingChannel(
    rate=0.1,
    qubit=0,
    bath_temperature=0.0  # Zero temperature bath
)

# Construct Lindblad solver
solver = LindbladSolver(
    num_qubits=2,
    hamiltonian=heisenberg_hamiltonian,
    jump_operators=[damping.jump_operator()],
    dt=0.01,
    total_time=10.0,
    method="adaptive_rk4"  # or "monte_carlo", "chebyshev"
)

rho0 = solver.zero_density_matrix()
trajectories = solver.solve(
    rho0,
    num_trajectories=1000,  # For Monte Carlo method
    store_states=True
)

print(f"Final purity: {trajectories.purity}")
print(f"Coherence retained: {trajectories.coherence}")
print(f"Decoherence time: {trajectories.decoherence_time:.4f}")
```

### Gibbs State Preparation

```python
from quantum_simulation import GibbsState, Hamiltonian

ham = Hamiltonian.from_pauli_terms([
    PauliTerm("ZZ", [0, 1], coefficient=1.0),
    PauliTerm("X", [0], coefficient=0.5),
    PauliTerm("Z", [1], coefficient=0.3),
])

gibbs = GibbsState(
    hamiltonian=ham,
    temperature=0.5,
    method="imaginary_time_evolution",  # or "qite", "direct_diagonalization"
    convergence_threshold=1e-8
)

rho_gibbs = gibbs.state()
print(f"Energy expectation: {gibbs.energy():.4f}")
print(f"Entropy: {gibbs.entropy():.4f}")
print(f"Purity: {gibbs.purity():.4f}")
print(f"Free energy: {gibbs.free_energy():.4f}")
```

### Correlation Function Computation

```python
from quantum_simulation import CorrelationFunction, TimeEvolution

evolution = TimeEvolution(
    hamiltonian,
    num_qubits=4,
    method="chebyshev",
    max_bond_dimension=64
)

evolution.evolve(
    initial_state,
    timespan=5.0,
    steps=200,
    store_intermediate_states=True
)

corr = CorrelationFunction(evolution)
auto_corr_z = corr.auto_correlation(
    operator="Z",
    site=0,
    times=evolution.time_points(),
    method="linear_response"
)

# Dynamical structure factor
structure_factor = corr.dynamical_structure_factor(
    operator="Z",
    momentum_range=[0, 3.14159],
    frequency_range=[-5.0, 5.0]
)

print(f"Correlation decay time: {corr.decay_time(auto_corr_z):.4f}")
print(f"Spectral peak frequency: {corr.spectral_peak(auto_corr_z):.4f}")
```

### Entanglement Entropy Analysis

```python
from quantum_simulation import Entanglement, ReducedDensityMatrix

ent = Entanglement(num_qubits=4)
rdm = ReducedDensityMatrix.full_to_reduced(
    evolved_state,
    subsystem=[0, 1],
    method="partial_trace"
)

von_neumann = ent.von_neumann_entropy(rdm)
concurrence = ent.concurrence(rdm)
negativity = ent.logarithmic_negativity(evolved_state, bipartition=[0, 1])

print(f"Von Neumann entropy: {von_neumann:.4f}")
print(f"Concurrence: {concurrence:.4f}")
print(f"Logarithmic negativity: {negativity:.4f}")

# Entanglement spectrum
spectrum = ent.entanglement_spectrum(rdm)
print(f"Entanglement spectrum: {spectrum}")
```

### Quantum Process Tomography

```python
from quantum_simulation import ProcessTomography, QuantumChannel

# Define a quantum channel to characterize
channel = QuantumChannel(
    type="depolarizing",
    error_rate=0.05,
    num_qubits=1
)

# Perform process tomography
tomography = ProcessTomography(
    num_qubits=1,
    measurement_basis="pauli",
    state_preparation="single_qubit_tomography"
)

# Generate training data
input_states = tomography.generate_input_states()
output_states = channel.apply(input_states)
measurement_data = tomography.measure(output_states)

# Reconstruct process matrix
process_matrix = tomography.reconstruct(
    measurement_data,
    method="maximum_likelihood",
    regularize=True
)

# Analyze process
fidelity = tomography.fidelity(process_matrix, channel.theoretical_process_matrix())
print(f"Process fidelity: {fidelity:.4f}")
print(f"Process tomography diamond norm: {tomography.diamond_norm(process_matrix):.4f}")
```

## Best Practices

1. **Trotter error control**: Use higher-order Trotter formulas and smaller time steps for better accuracy — error scales as O(dt^{p+1}) for order-p. Monitor error bounds and adjust parameters accordingly.
2. **Lindblad validation**: Verify that jump operators satisfy trace-preservation (sum L†L = I for probability conservation). Use the provided validation tools to check physical consistency.
3. **Thermal state convergence**: For large systems, use imaginary-time evolution instead of exact diagonalization for Gibbs states. Monitor convergence through energy variance.
4. **Entanglement monitoring**: Track entanglement entropy during evolution to detect thermalization or many-body localization. Use entanglement as a diagnostic for simulation quality.
5. **Consistency checks**: Always verify that density matrix remains physical (positive semi-definite, unit trace) during simulation. Use the physicality checker to catch numerical errors.
6. **MPS bond dimension**: Monitor and cap bond dimension to control memory — truncation error should be below your accuracy target. Use adaptive bond dimension for time-dependent simulations.
7. **Time step selection**: Use adaptive time stepping for stiff Hamiltonians or rapid decay dynamics. The adaptive algorithms automatically adjust time steps based on local error estimates.
8. **Parallelize trajectories**: Run multiple Monte Carlo trajectories in parallel for open-system simulations with stochastic methods. This provides both speedup and error estimation.
9. **Resource estimation**: Before large simulations, estimate memory and compute requirements using the scaling analysis tools. Plan simulations to fit within available resources.
10. **Benchmarking**: Compare different simulation methods on small instances before applying to large systems. Use the provided benchmarking suite to select optimal methods.

## Performance Considerations

- **Memory scaling**: Exact diagonalization requires O(4^n) memory for n qubits. For systems beyond 12 qubits, use tensor network methods or quantum Monte Carlo.
- **Trotter overhead**: Higher-order Trotter formulas improve accuracy but increase circuit depth. Balance accuracy requirements against computational cost.
- **MPS compression**: Matrix product state methods provide exponential compression for weakly entangled states. Monitor entanglement growth to ensure MPS remains efficient.
- **Adaptive time stepping**: Adaptive algorithms may require more function evaluations but provide better accuracy per computational effort. Use for stiff or multi-scale dynamics.
- **Parallelization**: Monte Carlo trajectory simulations are embarrassingly parallel. Use multiprocessing or GPU acceleration for large numbers of trajectories.
- **Sparse matrix methods**: For large sparse Hamiltonians, use Krylov subspace methods instead of full diagonalization. This provides exponential speedup for localized states.
- **Cache optimization**: Reuse intermediate results in multi-step simulations. The caching system automatically stores frequently accessed data.
- **Numerical precision**: Use double precision for most simulations, but consider extended precision for ill-conditioned problems or long-time evolution.

## Security Considerations

- **Random number generation**: Use reproducible random seeds for Monte Carlo simulations to ensure result reproducibility and enable debugging.
- **Input validation**: Validate Hamiltonian parameters and initial states to prevent numerical instabilities or unphysical results.
- **Resource monitoring**: Monitor memory and compute usage to prevent resource exhaustion attacks on shared simulation resources.
- **Result verification**: Verify simulation results using multiple methods or analytical benchmarks when available. Cross-validation helps catch implementation errors.
- **Side-channel analysis**: Be aware that simulation timing and resource usage may leak information about the problem structure in sensitive applications.
- **Data integrity**: Use checksums or digital signatures for simulation results to ensure data integrity in collaborative research.
- **Access control**: Implement access controls for simulation resources and results in multi-user environments.
- **Audit logging**: Log simulation parameters, methods, and results for reproducibility and security auditing.

## Related Modules

- `quantum-computing` — Gate-level circuit simulation underpinning Hamiltonian simulation, including noise model integration and circuit compilation for simulation algorithms.
- `quantum-cryptography` — Security analysis requires accurate channel noise models from this module for QKD protocol simulation and security proof validation.
- `quantum-optimization` — VQE/QAOA cost function evaluation uses Hamiltonian expectation values computed by this module's simulation engines.
- `quantum-networking` — Entanglement distribution fidelity depends on open-system dynamics for realistic modeling of quantum memory and channel decoherence.

## References

- Orús, R. (2019). A practical introduction to tensor networks: Tensor network methods for strongly correlated systems. Annals of Physics, 399, 237-314.
- Lindblad, G. (1976). On the generators of quantum dynamical semigroups. Communications in Mathematical Physics, 48(2), 119-130.
- Gorini, V., Kossakowski, A., & Sudarshan, E. C. G. (1976). Completely positive dynamical semigroups of N-level systems. Journal of Mathematical Physics, 17(5), 821-825.
- Trotter, H. F. (1959). On the product of semi-groups of operators. Proceedings of the American Mathematical Society, 10(4), 545-551.
- Suzuki, M. (1990). Fractal decomposition of exponential operators with applications to many-body theories and Monte Carlo simulations. Physics Letters A, 146(6), 319-323.
- arXiv:1907.11231 - Simulating quantum dynamics with tensor networks.
- arXiv:2012.09126 - Quantum simulation of open quantum systems.
- arXiv:2104.02487 - Matrix product state methods for quantum dynamics.

---

## Advanced Hamiltonian Simulation

### Time-Dependent Hamiltonian Evolution

```python
from quantum_simulation import TimeDependentSimulator, Hamiltonian

# Simulate time-dependent Hamiltonian H(t)
def hamiltonian_t(t, params):
    return params['J'] * sum(
        PauliTerm("XX", [i, i+1], coefficient=1.0)
        for i in range(params['num_qubits'] - 1)
    ) + params['h'] * sum(
        PauliTerm("Z", [i], coefficient=params['h_t'](t))
        for i in range(params['num_qubits'])
    )

simulator = TimeDependentSimulator(
    num_qubits=6,
    hamiltonian_fn=hamiltonian_t,
    time_dep_params={'J': 1.0, 'h': 0.5,
                     'h_t': lambda t: 0.5 * (1 + 0.1 * t)},
    method="trotter",
    order=2,
    adaptive_time_step=True,
    error_tolerance=1e-8
)

initial_state = simulator.computational_basis_state([1,0,1,0,1,0])
evolved = simulator.evolve(
    initial_state,
    t_start=0.0,
    t_end=5.0,
    num_steps=500
)

print(f"Fidelity to initial: {simulator.fidelity(initial_state, evolved):.6f}")
print(f"Energy at t=0: {simulator.expectation(evolved, 'H', t=0):.4f}")
print(f"Energy at t=5: {simulator.expectation(evolved, 'H', t=5):.4f}")
```

### Higher-Order Trotter-Suzuki Formulas

```python
from quantum_simulation import TrotterSuzuki, PauliDecomposition

# Compare different Trotter orders
hamiltonian = PauliDecomposition([
    (1.0, "XX", [0, 1]),
    (0.5, "YY", [0, 1]),
    (0.3, "ZZ", [0, 1]),
    (0.7, "X", [0]),
    (0.4, "Z", [1])
])

for order in [1, 2, 4]:
    trotter = TrotterSuzuki(hamiltonian, order=order)
    evolved = trotter.evolve(
        initial_state,
        time=1.0,
        steps=100
    )
    exact = trotter.exact_evolve(initial_state, time=1.0)
    error = trotter.fidelity(evolved, exact)
    print(f"Order {order}: fidelity = {error:.8f}, "
          f"error = {1-error:.2e}")

# Commutator error bounds
bounds = trotter.error_bound(
    initial_state,
    time=1.0,
    steps=100
)
print(f"Comm 1 bound: {bounds.commutator_1:.2e}")
print(f"Comm 2 bound: {bounds.commutator_2:.2e}")
print(f"Total error bound: {bounds.total_error:.2e}")
```

### Chebyshev Expansion Method

```python
from quantum_simulation import ChebyshevSimulator

# Chebyshev expansion for efficient time evolution
cheby = ChebyshevSimulator(
    num_qubits=8,
    hamiltonian=hamiltonian,
    bandwidth=10.0,
    polynomial_order=50,
    error_tolerance=1e-10
)

# Evolve initial state
evolved = cheby.evolve(
    initial_state,
    time=2.0,
    num_coefficients=100
)

print(f"Evolved state fidelity: {cheby.fidelity(evolved, exact):.8f}")
print(f"Coefficients computed: {cheby.num_coefficients}")
print(f"Computational cost: {cheby.cost:.2f} seconds")
```

## Open Quantum Systems Advanced

### Non-Markovian Dynamics

```python
from quantum_simulation import NonMarkovianSolver, SpectralDensity

# Simulate non-Markovian dynamics with structured bath
spectral = SpectralDensity(
    type="ohmic",
    cutoff_frequency=5.0,
    coupling_strength=0.1,
    temperature=0.5
)

solver = NonMarkovianSolver(
    num_qubits=2,
    hamiltonian=hamiltonian,
    bath_spectral_density=spectral,
    method="hierarchical_equations_of_motion",
    max_hierarchy_depth=4,
    dt=0.01,
    total_time=10.0
)

rho0 = solver.zero_density_matrix()
result = solver.solve(rho0, store_dynamics=True)

print(f"Final purity: {result.purity:.4f}")
print(f"Memory effects detected: {result.memory_detected}")
print(f"Brevity time: {result.brevity_time:.4f}")
print(f"Information backflow: {result.information_backflow:.4f}")
```

### Quantum Master Equation Solvers

```python
from quantum_simulation import MasterEquationSolver, Lindbladian

# Compare different master equation solvers
lindblad = Lindbladian(
    hamiltonian=hamiltonian,
    jump_operators=[
        0.1 * PauliTerm("X", [0]),
        0.05 * PauliTerm("X", [1])
    ]
)

solvers = {
    "runge_kutta": MasterEquationSolver(method="rk4", dt=0.01),
    "chebyshev": MasterEquationSolver(method="chebyshev", order=30),
    "trotter": MasterEquationSolver(method="trotter", order=2),
    "adaptive": MasterEquationSolver(method="adaptive", rtol=1e-8)
}

for name, solver in solvers.items():
    result = solver.solve(lindblad, rho0, t_span=(0, 5.0))
    print(f"{name}: purity = {result.purity[-1]:.6f}, "
          f"time = {result.computation_time:.4f}s")
```

### Quantum Process Tomography Advanced

```python
from quantum_simulation import ProcessTomography, ChiMatrix

# Advanced process tomography with compressed sensing
tomography = ProcessTomography(
    num_qubits=2,
    method="compressed_sensing",
    measurement_basis=" pauli ",
    rank_constraint=4,
    sparsity_level=10
)

# Generate training data
input_states = tomography.generate_input_states(num_states=100)
output_states = channel.apply(input_states)
measurements = tomography.measure(output_states, shots=1024)

# Reconstruct process matrix
chi_matrix = tomography.reconstruct(
    measurements,
    method="compressed_sensing",
    regularize=True,
    lambda_reg=0.01
)

# Analyze process
print(f"Process fidelity: {tomography.fidelity(chi_matrix, exact_chi):.6f}")
print(f"Diamond norm distance: {tomography.diamond_norm(chi_matrix, exact_chi):.6f}")
print(f"Choi rank: {tomography.choi_rank(chi_matrix)}")
print(f"Process purity: {tomography.purity(chi_matrix):.4f}")
```

## Tensor Network Methods

### Matrix Product State Evolution

```python
from quantum_simulation import MPSSimulator, TensorNetwork

# MPS simulation for large 1D systems
mps = MPSSimulator(
    num_sites=20,
    max_bond_dimension=64,
    truncation_threshold=1e-8,
    canonical_form="left"
)

# Initialize in product state
state = mps.product_state([0] * 20)

# Time evolution with TEBD
evolved = mps.tebd_evolve(
    initial_state=state,
    hamiltonian=heisenberg_chain,
    time=5.0,
    dt=0.01,
    max_bond_dimension=128,
    truncation_error=1e-6
)

# Compute observables
for site in range(20):
    sz = mps.local_expectation(evolved, "Z", site)
    print(f"Site {site}: <Sz> = {sz:.4f}")

print(f"Entanglement entropy at bond 10: "
      f"{mps.entanglement_entropy(evolved, bond=10):.4f}")
print(f"Max bond dimension reached: {mps.max_bond(evolved)}")
```

### Time-Dependent DMRG

```python
from quantum_simulation import TimeDependentDMRG, MPS

# Time-dependent DMRG for quantum quenches
tdmrg = TimeDependentDMRG(
    num_sites=16,
    max_bond_dimension=100,
    truncation_threshold=1e-8,
    time_step_method="local_ode"
)

# Initial ground state
initial = tdmrg.find_ground_state(
    hamiltonian=initial_hamiltonian,
    dmrg_sweeps=20,
    convergence_threshold=1e-10
)

# Quench Hamiltonian
quench_result = tdmrg.quench(
    initial_state=initial,
    final_hamiltonian=quenched_hamiltonian,
    time=10.0,
    dt=0.1,
    measure_at=[0.5, 1.0, 2.0, 5.0, 10.0]
)

for t, obs in quench_result.observations.items():
    print(f"t={t}: energy={obs.energy:.4f}, "
          f"entanglement={obs.entanglement:.4f}")
```

### Tensor Network Contraction Optimization

```python
from quantum_simulation import TensorContraction, TensorNetwork

# Optimize tensor network contraction order
network = TensorNetwork()
# Build a complex tensor network
for i in range(10):
    network.add_tensor(
        name=f"T{i}",
        indices=[f"i{i}", f"i{(i+1)%10}"],
        shape=(2, 2)
    )

# Find optimal contraction order
optimizer = TensorContraction(network)
optimal_order = optimizer.optimize(
    method="greedy",
    cost_model="flops"
)

print(f"Contraction cost: {optimal_order.cost:.2e} FLOPs")
print(f"Memory requirement: {optimal_order.memory:.2e} bytes")
print(f"Contraction tree: {optimal_order.tree}")
```

## Quantum Chemistry Simulation

### Molecular Hamiltonian Construction

```python
from quantum_simulation import MolecularHamiltonian, BasisSet

# Construct molecular Hamiltonian from electronic structure
basis = BasisSet(
    name="sto-3g",
    atoms=[("H", [0, 0, 0]), ("H", [0, 0, 0.74])],
    charge=0,
    spin=0
)

hamiltonian = MolecularHamiltonian(
    basis=basis,
    method="hartree_fock",
    active_space=None,
    frozen_orbitals=0
)

print(f"Number of qubits: {hamiltonian.num_qubits}")
print(f"One-electron integrals: {hamiltonian.one_electron_integral.shape}")
print(f"Two-electron integrals: {hamiltonian.two_electron_integral.shape}")
print(f"Nuclear repulsion: {hamiltonian.nuclear_repulsion:.6f}")
print(f"HF energy: {hamiltonian.hf_energy:.6f}")
```

### Full Configuration Interaction

```python
from quantum_simulation import FCI, MolecularHamiltonian

# Full configuration interaction for small molecules
fci = FCI(
    num_qubits=4,
    num_electrons=2,
    point_group="d2h",
    symmetry_adapted=True
)

# Solve FCI problem
result = fci.solve(hamiltonian)
print(f"FCI ground state energy: {result.energy:.8f}")
print(f"FCI excited states: {result.excited_energies[:3]}")
print(f"Dipole moment: {result.dipole_moment:.4f}")
print(f"FCI computation time: {result.computation_time:.2f} seconds")
```

### Quantum Chemistry Post-Processing

```python
from quantum_simulation import ChemistryPostProcessor

# Post-process quantum chemistry results
post_processor = ChemistryPostProcessor(
    method="mp2",
    basis="cc-pvdz",
    frozen_core=True
)

# Compute correlation energy
correlation = post_processor.compute_correlation(
    hf_energy=-1.1373,
    mo_integrals=mo_integrals
)

print(f"MP2 correlation energy: {correlation.energy:.8f}")
print(f"MP2 total energy: {correlation.total_energy:.8f}")
print(f"Dipole moment: {correlation.dipole_moment:.4f}")
print(f"Orbital energies: {correlation.orbital_energies}")
```

## Many-Body Physics Simulation

### Transverse-Field Ising Model

```python
from quantum_simulation import TransverseIsingModel, ExactDiagonalization

# Study quantum phase transition in transverse-field Ising model
tfim = TransverseIsingModel(
    num_sites=12,
    coupling_j=1.0,
    transverse_field=1.0,
    boundary="periodic"
)

# Exact diagonalization for small systems
ed = ExactDiagonalization(num_qubits=12)
ground_state = ed.find_ground_state(tfim.hamiltonian())

# Scan transverse field
for h in [0.1, 0.5, 1.0, 1.5, 2.0]:
    tfim.transverse_field = h
    gs = ed.find_ground_state(tfim.hamiltonian())
    magnetization = ed.expectation(gs, tfim.magnetization_operator())
    print(f"h={h:.1f}: <Mx> = {magnetization:.4f}")

print(f"Critical point expected at h=1.0")
```

### Bose-Hubbard Model

```python
from quantum_simulation import BoseHubbard, DMRGSolver

# Simulate Bose-Hubbard model with DMRG
bose_hubbard = BoseHubbard(
    num_sites=10,
    tunneling=1.0,
    interaction=4.0,
    filling=1.0,
    boundary="open"
)

dmrg = DMRGSolver(
    num_sites=10,
    max_bond_dimension=200,
    sweeps=30,
    convergence_threshold=1e-10
)

ground_state = dmrg.find_ground_state(bose_hubbard.hamiltonian())

# Compute observables
for site in range(10):
    density = dmrg.expectation(ground_state, "number", site)
    print(f"Site {site}: <n> = {density:.4f}")

print(f"Compressibility: {dmrg.compressibility(ground_state):.4f}")
print(f"Entanglement entropy: {dmrg.entanglement_entropy(ground_state, bond=5):.4f}")
```

### Heisenberg Spin Chain

```python
from quantum_simulation import HeisenbergChain, SpinCorrelator

# Study spin correlations in Heisenberg chain
chain = HeisenbergChain(
    num_sites=8,
    coupling_x=1.0,
    coupling_y=1.0,
    coupling_z=1.0,
    boundary="open"
)

# Compute spin-spin correlators
correlator = SpinCorrelator(chain)

for r in range(1, 8):
    corr_xx = correlator.correlation("XX", site1=0, site2=r)
    corr_zz = correlator.correlation("ZZ", site1=0, site2=r)
    print(f"r={r}: <S0xSr> = {corr_xx:.4f}, <S0zSr> = {corr_zz:.4f}")

# Compute dynamic structure factor
structure_factor = correlator.dynamical_structure_factor(
    operator="Z",
    momentum_points=100,
    frequency_points=200
)
print(f"Spectral gap: {structure_factor.gap:.4f}")
print(f"Magnon dispersion: {structure_factor.dispersion[:5]}")
```

## Entanglement and Correlation Analysis

### Entanglement Entropy Scaling

```python
from quantum_simulation import EntanglementScaling, MPS

# Study entanglement entropy scaling
scaling = EntanglementScaling(mps_simulator)

system_sizes = [4, 8, 12, 16, 20, 24]
for n in system_sizes:
    chain = HeisenbergChain(num_sites=n)
    gs = scaling.find_ground_state(chain.hamiltonian())
    entropy = scaling.entanglement_entropy(gs, bond=n//2)
    print(f"N={n}: S(L/2) = {entropy:.4f}")

# Fit to area law or volume law
fit = scaling.fit_entropy_scaling(system_sizes, method="log")
print(f"Scaling coefficient: {fit.coefficient:.4f}")
print(f"Scaling type: {fit.scaling_type}")
```

### Mutual Information and Negativity

```python
from quantum_simulation import MutualInformation, Negativity

# Compute quantum mutual information
mi = MutualInformation(num_qubits=6)

# For a 6-qubit state
mi_matrix = mi.compute_matrix(evolved_state)
for i in range(6):
    for j in range(i+1, 6):
        print(f"I({i}:{j}) = {mi_matrix[i,j]:.4f}")

# Compute negativity for bipartite entanglement
neg = Negativity()
bipartite_neg = neg.logarithmic_negativity(
    evolved_state,
    subsystem_a=[0, 1, 2],
    subsystem_b=[3, 4, 5]
)
print(f"Log negativity: {bipartite_neg:.4f}")
```

## Numerical Methods and Benchmarks

### Comparison of Simulation Methods

```python
from quantum_simulation import MethodBenchmark, BenchmarkSuite

# Benchmark different simulation methods
suite = BenchmarkSuite(
    methods=["exact_diagonalization", "trotter_2", "trotter_4",
             "chebyshev", "mps", "qmc"],
    system_sizes=[4, 6, 8, 10, 12],
    time_spans=[1.0, 5.0, 10.0]
)

results = suite.run(
    hamiltonian=heisenberg_chain,
    error_metric="fidelity",
    reference_method="exact_diagonalization"
)

for method, method_results in results.items():
    print(f"\n{method}:")
    for size, size_result in method_results.items():
        print(f"  N={size}: fidelity={size_result.fidelity:.6f}, "
              f"time={size_result.computation_time:.4f}s, "
              f"memory={size_result.memory_mb:.1f}MB")
```

### Convergence Analysis

```python
from quantum_simulation import ConvergenceAnalyzer

# Analyze convergence of different methods
analyzer = ConvergenceAnalyzer()

trotter_convergence = analyzer.analyze_trotter_convergence(
    hamiltonian=hamiltonian,
    time=1.0,
    steps_range=[10, 20, 50, 100, 200, 500],
    order=2
)

print("Trotter convergence:")
for steps, error in trotter_convergence.items():
    print(f"  steps={steps}: error={error:.2e}")

cheby_convergence = analyzer.analyze_chebyshev_convergence(
    hamiltonian=hamiltonian,
    time=1.0,
    orders=[10, 20, 30, 50, 100]
)

print("\nChebyshev convergence:")
for order, error in cheby_convergence.items():
    print(f"  order={order}: error={error:.2e}")
```

## Quantum Error Simulation

### Depolarizing Channel Simulation

```python
from quantum_simulation import DepolarizingChannel, ChannelSimulation

# Simulate depolarizing noise channel
channel = DepolarizingChannel(
    num_qubits=2,
    error_rate=0.05,
    error_type="full"
)

simulator = ChannelSimulation(channel)
result = simulator.simulate(
    initial_state=bell_state,
    num_shots=10000,
    process_tomography=True
)

print(f"Process fidelity: {result.process_fidelity:.4f}")
print(f"Average gate fidelity: {result.average_gate_fidelity:.4f}")
print(f"Entanglement fidelity: {result.entanglement_fidelity:.4f}")
print(f"Noise strength: {result.noise_strength:.4f}")
```

### Amplitude Damping Channel

```python
from quantum_simulation import AmplitudeDampingChannel

# Simulate T1 relaxation
amp_damp = AmplitudeDampingChannel(
    num_qubits=1,
    t1_time=50.0,
    t2_time=70.0,
    gate_time=0.1
)

# Simulate decay from |1> state
initial = amp_damp.excited_state()
evolved = amp_damp.evolve(initial, time=10.0)

print(f"Population in |0>: {amp_damp.population(evolved, 0):.4f}")
print(f"Population in |1>: {amp_damp.population(evolved, 1):.4f}")
print(f"Coherence: {amp_damp.coherence(evolved):.4f}")
print(f"Purity: {amp_damp.purity(evolved):.4f}")
```

## Advanced Topics

### Krylov Subspace Methods

```python
from quantum_simulation import KrylovSubspace, ArnoldiIteration

# Krylov subspace method for time evolution
krylov = KrylovSubspace(
    num_qubits=10,
    subspace_dimension=20,
    method="arnoldi",
    reorthogonalization=True
)

# Build Krylov subspace
subspace = krylov.build(
    initial_state,
    hamiltonian,
    time_step=0.1
)

print(f"Subspace dimension: {subspace.dimension}")
print(f"Hessenberg matrix:\n{subspace.hessenberg_matrix[:5,:5]}")
print(f"Ritz values: {subspace.ritz_values[:5]}")

# Evolve using Krylov
evolved = krylov.evolve(initial_state, hamiltonian, time=1.0)
print(f"Krylov fidelity: {krylov.fidelity(evolved, exact):.6f}")
```

### Variational Quantum Simulation

```python
from quantum_simulation import VariationalSimulator, Ansatz

# Variational quantum simulation for time evolution
ansatz = Ansatz(
    num_qubits=4,
    depth=3,
    entanglement="full",
    parameterization="angle"
)

var_sim = VariationalSimulator(
    ansatz=ansatz,
    cost_function="fidelity",
    optimizer="adam",
    max_iterations=200
)

# Variational time evolution
var_result = var_sim.time_evolve(
    initial_state,
    hamiltonian,
    time=1.0,
    dt=0.1,
    overlap_target=None
)

print(f"Final fidelity: {var_result.fidelity:.6f}")
print(f"Parameters optimized: {var_result.num_parameters}")
print(f"Convergence iterations: {var_result.iterations}")
```

### Quantum walks

```python
from quantum_simulation import QuantumWalk, Graph

# Quantum walk on a graph
graph = Graph(
    vertices=10,
    edges=[(i, (i+1) % 10) for i in range(10)]
)

walk = QuantumWalk(
    graph=graph,
    coin_operator="hadamard",
    num_steps=100,
    initial_position=0
)

result = walk.simulate()
print(f"Position distribution after 100 steps:")
for pos, prob in result.distribution.items():
    if prob > 0.01:
        print(f"  Position {pos}: {prob:.4f}")

print(f"Spread: {result.spread:.4f}")
print(f"Mixedness: {result.mixedness:.4f}")
```