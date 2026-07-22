---
name: "quantum-cryptography"
category: "quantum"
version: "1.0.0"
tags: ["quantum", "cryptography", "QKD", "BB84", "post-quantum"]
---

# Quantum Cryptography Module

## Overview

The Quantum Cryptography module implements quantum key distribution (QKD) protocols, post-quantum cryptographic primitives, and quantum-secure communication channels. It covers the full lifecycle of quantum-secured key exchange â€” from qubit preparation and measurement through basis reconciliation, error estimation, privacy amplification, and authenticated classical post-processing. The module also includes post-quantum lattice-based encryption for hybrid classical-quantum workflows, providing defense-in-depth against both classical and quantum adversaries.

The module implements multiple QKD protocol families, including prepare-and-measure protocols (BB84, B92), entanglement-based protocols (E91, BBM92), and continuous-variable QKD for practical implementations using standard telecom components. Each protocol includes comprehensive security analysis tools, channel simulation capabilities, and parameter optimization for real-world deployment scenarios. The post-quantum cryptography component provides NIST-standardized algorithms (Kyber, Dilithium) alongside traditional QKD for hybrid security architectures.

All implementations follow the ETSI QKD interface standards and include comprehensive logging for security auditing. The module supports both simulated environments for research and development, and integration with actual quantum hardware through standardized APIs. Security proofs and finite-key analysis are built into every protocol, ensuring that key generation rates and security guarantees are mathematically rigorous even for finite block sizes encountered in practical implementations.

## Core Capabilities

- **BB84 Protocol**: Full implementation of the Bennett-Brassard 1984 QKD protocol with decoy states, including single-photon sources, weak coherent pulse sources, and measurement-device-independent (MDI) variants for enhanced security.
- **E91 Protocol**: Ekert 1991 entanglement-based QKD using Bell inequality verification, with CHSH parameter estimation and device-independent security proofs for hardware-agnostic security guarantees.
- **B92 Protocol**: Simplified two-state QKD using non-orthogonal states, optimized for low-cost implementations with minimal hardware requirements while maintaining provable security.
- **Decoy State QKD**: Decoy-state method to detect photon-number-splitting attacks, with optimized decoy intensity selection and statistical analysis for maximum secure key rate.
- **Sifting**: Classical basis reconciliation over authenticated channel, with bandwidth-efficient protocols for high-speed QKD systems and support for multiple sifting algorithms.
- **Error Estimation**: Quantum bit error rate (QBER) computation with statistical bounds, including finite-key analysis, confidence interval estimation, and adaptive error estimation for real-time parameter adjustment.
- **Privacy Amplification**: Universal hash-based key distillation from partially secure bits, with optimized implementations using Toeplitz matrices and polynomial hashing for high-throughput key generation.
- **Information Reconciliation**: Cascade protocol for error correction with adaptive parameter selection, LDPC code-based reconciliation for high efficiency, and verification procedures for error-free key extraction.
- **Post-Quantum Encryption**: Lattice-based (Kyber-style) key encapsulation, including key generation, encapsulation, and decapsulation with side-channel resistant implementations.
- **Channel Simulation**: Lossy and noisy quantum channel models with Eve intercept, supporting various eavesdropping strategies (intercept-resend, collective, coherent attacks) for security analysis and protocol optimization.

## Usage Examples

### Running BB84 Key Distribution

```python
from quantum_crypto import BB84Protocol, QuantumChannel, ClassicalChannel

# Create channels with realistic parameters
q_channel = QuantumChannel(
    loss=0.1,              # 10% channel loss
    noise=0.02,            # 2% depolarizing noise
    detector_efficiency=0.7,  # 70% detector efficiency
    dark_count_rate=1e-6   # Dark count probability
)
c_channel = ClassicalChannel(authenticated=True, latency_ms=10)

# Initialize protocol with security parameters
bb84 = BB84Protocol(
    key_length=256,
    security_parameter=128,  # 128-bit security
    max_block_size=1e6       # Block size for finite-key analysis
)

# Execute full protocol
session = bb84.run(
    quantum_channel=q_channel,
    classical_channel=c_channel,
    seed=42,
    num_pulses=100000,
    decoy_intensities=[0.1, 0.5, 1.0]  # Decoy state intensities
)

print(f"Secure key: {session.shared_key.hex()}")
print(f"QBER: {session.qber:.4f}")
print(f"Key rate: {session.key_rate:.4f} bits/pulse")
print(f"Privacy amplification factor: {session.amplification_factor:.4f}")
```

### Entanglement-Based E91 Protocol

```python
from quantum_crypto import E91Protocol, EntangledSource

source = EntangledSource(
    fidelity=0.95,
    generation_rate=1000,  # Pairs per second
    wavelength=810e-9      # Entangled photon wavelength
)

e91 = E91Protocol(
    key_length=256,
    bell_test=True,
    chsh_bound=2.828,  # Tsirelson bound
    security_parameter=128
)

session = e91.run(
    entangled_source=source,
    measurement_bases="random",  # Random basis selection
    num_rounds=10000,
    verification_rounds=100
)

print(f"Bell parameter S: {session.bell_s:.4f}")
print(f"Violation: {'Yes' if session.bell_s > 2.0 else 'No'}")
print(f"Secure key: {session.shared_key.hex()}")
print(f"Device-independent security: {session.di_security}")
```

### Privacy Amplification

```python
from quantum_crypto import PrivacyAmplifier, UniversalHash

amplifier = PrivacyAmplifier(
    security_parameter=128,
    hash_function=UniversalHash.POLYNOMIAL,
    seed_generation="cryptographic"
)

raw_key = bytes.fromhex("a1b2c3d4e5f6...")
extracted_key = amplifier.amplify(
    raw_key=raw_key,
    leaked_info_bits=20,
    input_length=len(raw_key) * 8,
    hash_seed=amplifier.generate_seed()
)

print(f"Raw key length: {len(raw_key) * 8} bits")
print(f"Amplified key: {extracted_key.hex()}")
print(f"Key reduction: {1 - len(extracted_key)/len(raw_key):.2%}")
```

### Post-Quantum Key Encapsulation

```python
from quantum_crypto import KyberKEM, SecurityLevel

kem = KyberKEM(
    security_level=SecurityLevel.LEVEL3,
    parameter_set="Kyber768",
    side_channel_resistant=True
)

# Key generation
keypair = kem.generate_keypair()
print(f"Public key size: {len(keypair.public_key)} bytes")

# Key encapsulation
encapsulation = kem.encapsulate(keypair.public_key)
print(f"Ciphertext size: {len(encapsulation.ciphertext)} bytes")
print(f"Shared secret: {encapsulation.shared_secret.hex()}")

# Key decapsulation
decapsulated = kem.decapsulate(
    keypair.private_key,
    encapsulation.ciphertext
)
assert decapsulated == encapsulation.shared_secret

# Hybrid QKD + Post-Quantum
from quantum_crypto import HybridKeyExchange
hybrid = HybridKeyExchange(qkd_key=session.shared_key, pqc_key=encapsulation.shared_secret)
final_key = hybrid.derive_key(length=256)
print(f"Hybrid key: {final_key.hex()}")
```

### Intercept-Resend Attack Simulation

```python
from quantum_crypto import BB84Protocol, EveIntercept

eve = EveIntercept(
    intercept_fraction=0.3,      # Eve intercepts 30% of qubits
    strategy="intercept_resend", # Attack strategy
    detection_probability=0.0    # Probability Eve is detected per intercept
)

bb84 = BB84Protocol(key_length=128)

# Run with eavesdropper
session = bb84.run_with_eve(eve=eve, seed=42, num_pulses=50000)

print(f"QBER with Eve: {session.qber:.4f}")
print(f"Detection threshold: 0.11")
print(f"Eve detected: {session.qber > 0.11}")
print(f"Information leaked to Eve: {session.leaked_information:.4f} bits")
print(f"Secure key after privacy amplification: {session.secure_key_length} bits")
```

### Continuous-Variable QKD Simulation

```python
from quantum_crypto import CVQKDProtocol, GaussianChannel

# Continuous-variable QKD using coherent states
channel = GaussianChannel(
    transmittance=0.5,      # 50% channel transmittance
    excess_noise=0.01,      # Excess noise in shot noise units
    electronic_noise=0.01   # Detector electronic noise
)

cvqkd = CVQKDProtocol(
    modulation_variance=4.0,  # Signal modulation variance
    reconciliation_method="multilevel",
    security_proof="composite"
)

session = cvqkd.run(
    channel=channel,
    num_symbols=1000000,
    symbol_rate=100e6  # 100 MHz symbol rate
)

print(f"Secret key rate: {session.key_rate:.2f} bits/symbol")
print(f"Channel transmittance: {session.transmittance:.4f}")
print(f"Excess noise: {session.excess_noise:.4f}")
```

## Best Practices

1. **Always authenticate the classical channel**: QKD without authentication is vulnerable to man-in-the-middle attacks. Use message authentication codes (MAC) with pre-shared keys or quantum-resistant signatures.
2. **Set QBER thresholds**: Abort key exchange if QBER exceeds ~11% (BB84) â€” this indicates an eavesdropper or excessive channel noise. Implement adaptive thresholds based on finite-key analysis.
3. **Use decoy states**: Always employ decoy-state method to defeat photon-number-splitting attacks on weak coherent pulse sources. Optimize decoy intensities for your channel loss and noise characteristics.
4. **Apply privacy amplification**: Never use raw sifted key directly â€” always amplify to remove partial information leakage. Use universal hash functions with cryptographically secure seeds.
5. **Validate Bell inequalities**: For E91, verify CHSH inequality violation before trusting entanglement-based security. Implement continuous monitoring of Bell parameters during key exchange.
6. **Hybrid approach**: Combine QKD with post-quantum KEM for defense-in-depth. Use key combination functions that are secure even if one component is compromised.
7. **Key rate optimization**: Tune pulse rate and loss budget to maximize secure key rate per second. Use finite-key analysis for realistic performance estimation in practical deployments.
8. **Regular key refresh**: Rotate QKD-derived keys frequently to bound the impact of any single compromise. Implement key lifecycle management with automatic expiration.
9. **Hardware calibration**: Regularly calibrate quantum detectors and sources to maintain specified performance. Include calibration verification in your key exchange protocol.
10. **Security auditing**: Log all key exchange events with timestamps, error rates, and security parameters. Implement intrusion detection based on statistical anomalies in QBER and key rates.

## Security Considerations

- **Finite-key effects**: Real implementations use finite block sizes, which reduce secure key rates compared to asymptotic analyses. Use the provided finite-key analysis tools for realistic security guarantees.
- **Detector vulnerabilities**: Implement measurement-device-independent (MDI) QKD to protect against detector side-channel attacks. Monitor detector performance for anomalies that may indicate tampering.
- **Side-channel resistance**: Consider timing side-channels in classical post-processing. Use constant-time implementations for all cryptographic operations.
- **Random number generation**: Use quantum random number generators for basis selection and key generation. Classical PRNGs may introduce vulnerabilities if not properly seeded.
- **Parameter estimation**: Use statistical tests to verify that measured QBER is consistent with expected channel parameters. Implement hypothesis testing for eavesdropper detection.
- **Key management**: Store quantum-generated keys securely with hardware security modules (HSMs). Implement key hierarchy with regular master key refresh.
- **Protocol security proofs**: All protocols include formal security proofs based on composable security frameworks. Verify that your implementation matches the assumptions in the security proof.
- **Post-quantum migration**: Plan for hybrid classical-quantum cryptography during the transition period. Use the provided migration assessment tools to evaluate your security posture.

## Related Modules

- `quantum-computing` â€” Low-level qubit and gate operations used by QKD protocol implementations, including circuit-based Bell state generation and measurement.
- `quantum-networking` â€” Entanglement distribution and quantum repeater infrastructure for long-distance QKD networks, including trusted node architectures.
- `quantum-simulation` â€” Channel noise simulation and security proof modeling for protocol analysis and optimization, including realistic hardware noise models.

## References

- Bennett, C. H., & Brassard, G. (1984). Quantum cryptography: Public key distribution and coin tossing. Proceedings of IEEE International Conference on Computers, Systems and Signal Processing, 175-179.
- Ekert, A. K. (1991). Quantum cryptography based on Bell's theorem. Physical Review Letters, 67(6), 661.
- Lo, H. K., Curty, M., & Qi, B. (2014). Measurement-device-independent quantum key distribution. Physical Review Letters, 112(13), 130503.
- Winick, A., et al. (2016). Secure key distribution for continuous-variable quantum key distribution. Physical Review X, 6(2), 021040.
- NIST Post-Quantum Cryptography Standardization. (2024). FIPS 203, 204, 205 Standards.
- ETSI QKD Standards. (2023). ETSI GS QKD 004, 008, 014.
- arXiv:2003.06557 - Advances in quantum key distribution.
- arXiv:2109.07425 - Practical challenges in quantum cryptography.
- arXiv:2201.10763 - Device-independent quantum key distribution.

---

## Advanced QKD Protocols

### Measurement-Device-Independent QKD

MDI-QKD eliminates all detector side-channel attacks by having both Alice and Bob send quantum states to an untrusted Charlie for Bell state measurement.

```python
from quantum_crypto import MDIQKDProtocol, QuantumChannel

# Configure MDI-QKD with two quantum channels
alice_channel = QuantumChannel(
    loss=0.1,
    noise=0.02,
    detector_efficiency=0.7,
    dark_count_rate=1e-6
)

bob_channel = QuantumChannel(
    loss=0.12,
    noise=0.025,
    detector_efficiency=0.65,
    dark_count_rate=1e-6
)

mdiqkd = MDIQKDProtocol(
    key_length=256,
    security_parameter=100,
    decoy_intensities=[0.1, 0.5, 1.0],
    basis_choices=["rectilinear", "diagonal"]
)

session = mdiqkd.run(
    alice_channel=alice_channel,
    bob_channel=bob_channel,
    charlie_efficiency=0.85,
    charlie_dark_count=1e-7,
    num_pulses=200000,
    coincidence_window_ns=1.0
)

print(f"Secure key length: {session.secure_key_length} bits")
print(f"QBER: {session.qber:.4f}")
print(f"Key rate: {session.key_rate:.4f} bits/pulse")
print(f"Finite-key security parameter: {session.security_parameter}")
```

### Twin-Field QKD

Twin-field QKD overcomes the rate-distance limit of conventional QKD by using single-photon interference at a central node.

```python
from quantum_crypto import TwinFieldQKD, PhaseLocking

# Configure twin-field QKD
tf_qkd = TwinFieldQKD(
    key_length=256,
    security_parameter=128,
    phase_tracking=True,
    phase_noise_rate=0.01,
    dead_time_ns=50
)

phase_lock = PhaseLocking(
    method="active_feedback",
    bandwidth_mhz=100,
    lock_precision_rad=0.01
)

session = tf_qkd.run(
    distance_km=500,
    fiber_loss_db_per_km=0.2,
    detector_efficiency=0.9,
    dark_count_rate=100,  # Hz
    pulse_rate_ghz=1.0,
    num_pulses=1e9,
    phase_lock=phase_lock
)

print(f"Secret key rate: {session.key_rate:.2f} bits/s")
print(f"Maximum distance: {session.max_distance_km} km")
print(f"Channel transmittance: {session.transmittance:.6f}")
print(f"Phase drift compensated: {session.phase_compensated}")
```

### Continuous-Variable MDI-QKD

```python
from quantum_crypto import CVMDIQKD, GaussianModulation

cv_mdi = CVMDIQKD(
    reconciliation_method="multilevel",
    security_proof="composite",
    excess_noise_threshold=0.05
)

modulation = GaussianModulation(
    variance=4.0,
    modulation_bandwidth_mhz=100,
    clipping_level=10.0
)

session = cv_mdi.run(
    channel_transmittance=0.1,
    excess_noise=0.01,
    electronic_noise=0.01,
    symbol_rate_mhz=100,
    num_symbols=1e8,
    modulation=modulation
)

print(f"Key rate: {session.key_rate:.2f} bits/symbol")
print(f"Reconciliation efficiency: {session.reconciliation_efficiency:.4f}")
print(f"Secret fraction: {session.secret_fraction:.4f}")
```

## Advanced Attack Analysis

### Coherent Attack Simulation

```python
from quantum_crypto import CoherentAttack, BB84Protocol

# Simulate the most general (coherent) quantum attack
attack = CoherentAttack(
    type="collective",
    eavesdropper_memory_size=1000,
    optimization_rounds=100
)

bb84 = BB84Protocol(key_length=256)

# Run protocol under coherent attack
session = bb84.run_with_attack(
    attack=attack,
    num_pulses=100000,
    channel_loss=0.1,
    detector_efficiency=0.7
)

print(f"QBER under attack: {session.qber:.4f}")
print(f"Key rate under attack: {session.key_rate:.4f}")
print(f"Security parameter achieved: {session.security_parameter}")
print(f"Eve's information bound: {session.eve_information:.4f} bits")
```

### Photon-Number-Splitting Attack

```python
from quantum_crypto import PNSAttack, WCPSource

# Simulate photon-number-splitting attack on weak coherent pulses
source = WCPSource(
    mean_photon_number=0.5,
    multiphoton_probability=0.22,
    dark_count_rate=1e-6
)

pns_attack = PNSAttack(
    splitting_strategy="optimal",
    photon_number_limit=5,
    eavesdropper_efficiency=0.95
)

# Analyze vulnerability
vulnerability = pns_attack.analyze(
    source=source,
    channel_loss=0.1,
    detection_efficiency=0.7
)

print(f"PNS vulnerability: {vulnerability.is_vulnerable}")
print(f"Optimal mean photon number: {vulnerability.optimal_mu:.4f}")
print(f"Secure key rate with decoy: {vulnerability.decoy_key_rate:.4f}")
print(f"Secure key rate without decoy: {vulnerability.no_decoy_key_rate:.4f}")
```

### Side-Channel Attack Detection

```python
from quantum_crypto import SideChannelDetector, AnomalyAnalyzer

detector = SideChannelDetector(
    timing_tolerance_ns=0.1,
    intensity_tolerance=0.01,
    wavelength_tolerance_nm=0.1
)

# Monitor for detector blinding attacks
blinding_test = detector.test_blinding(
    detector_response_func=lambda x: x,
    control_light_intensity=0.5,
    bright_light_intensity=1000.0,
    num_samples=10000
)

print(f"Detector blinding possible: {blinding_test.is_vulnerable}")
print(f"Bright light threshold: {blinding_test.threshold:.4f}")
print(f"Countermeasure recommended: {blinding_test.countermeasure}")

# Analyze timing side channels
timing_analysis = detector.analyze_timing(
    gate_width_ns=1.0,
    jitter_ns=0.3,
    afterpulse_probability=0.01
)

print(f"Timing vulnerability: {timing_analysis.is_vulnerable}")
print(f"Information leakage rate: {timing_analysis.leakage_rate:.6f} bits/ns")
```

## Finite-Key Security Analysis

### Finite-Key Effects on Key Rate

```python
from quantum_crypto import FiniteKeyAnalysis, SecurityParameter

# Analyze finite-key effects for different block sizes
analyzer = FiniteKeyAnalysis(
    security_parameter=128,
    qber=0.03,
    channel_loss=0.1,
    detector_efficiency=0.7
)

block_sizes = [1000, 10000, 100000, 1000000]
for n in block_sizes:
    result = analyzer.compute_key_rate(block_size=n)
    print(f"Block size {n:>10}: key rate = {result.key_rate:.4f} bits/pulse")
    print(f"  Statistical fluctuation: {result.statistical_fluctuation:.6f}")
    print(f"  Privacy amplification cost: {result.privacy_cost:.4f}")
    print(f"  Composable security: {result.security_parameter}")
```

### Parameter Estimation Under Finite Keys

```python
from quantum_crypto import ParameterEstimator, ConfidenceInterval

# Estimate QBER with confidence intervals
estimator = ParameterEstimator(
    confidence_level=0.99,
    method="chernoff_bound"
)

# Simulate measurement outcomes
outcomes = estimator.simulate_measurements(
    true_qber=0.03,
    num_samples=10000,
    seed=42
)

estimate = estimator.estimate_qber(outcomes)
ci = estimator.confidence_interval(outcomes)

print(f"Estimated QBER: {estimate:.6f}")
print(f"True QBER: 0.030000")
print(f"99% CI: [{ci.lower:.6f}, {ci.upper:.6f}]")
print(f"CI width: {ci.width:.6f}")
print(f"Estimation overhead: {estimator.overhead_factor:.4f}")
```

## Information Reconciliation

### Cascade Protocol Implementation

```python
from quantum_crypto import CascadeReconciliation, ErrorCorrection

# Configure Cascade protocol for efficient error correction
cascade = CascadeReconciliation(
    initial_block_size=128,
    max_rounds=20,
    target_error_rate=0.01,
    verification_method="polynomial_hash"
)

# Reconcile a raw key
raw_key = bytes(256)  # 2048-bit raw key
reconciliation = cascade.reconcile(
    raw_key=raw_key,
    estimated_qber=0.03,
    privacy_amplification_seed=None
)

print(f"Raw key length: {len(raw_key) * 8} bits")
print(f"Reconciled key length: {len(reconciliation.reconciled_key) * 8} bits")
print(f"Error rate after reconciliation: {reconciliation.residual_error_rate:.10f}")
print(f"Information leaked: {reconciliation.leaked_bits} bits")
print(f"Number of passes: {reconciliation.num_passes}")
print(f"Efficiency: {reconciliation.efficiency:.4f}")
```

### LDPC-Based Reconciliation

```python
from quantum_crypto import LDPCReconciliation, LDPCCode

# Use LDPC codes for high-efficiency reconciliation
ldpc_code = LDPCCode(
    block_length=65536,
    rate=0.8,
    design_snr_db=0.5,
    max_iterations=50
)

reconciliation = LDPCReconciliation(
    code=ldpc_code,
    syndrome_bits=13107,
    verification_bits=256
)

result = reconciliation.reconcile(
    raw_key=raw_key,
    qber=0.03
)

print(f"Code rate: {ldpc_code.rate:.2f}")
print(f"Reconciliation efficiency: {result.efficiency:.4f}")
print(f"Syndrome communication: {result.syndrome_bits} bits")
print(f"Verification passed: {result.verified}")
```

## Privacy Amplification Details

### Universal Hash Function Families

```python
from quantum_crypto import UniversalHashFamily, ToeplitzHash, PolynomialHash

# Compare different universal hash families
toeplitz = ToeplitzHash(seed_length=1024)
polynomial = PolynomialHash(field_size=2**64, degree=10)

key = bytes.fromhex("a1b2c3d4e5f67890" * 16)

# Measure compression and randomness
toeplitz_result = toeplitz.compress(key, output_length=256)
polynomial_result = polynomial.compress(key, output_length=256)

print(f"Input length: {len(key) * 8} bits")
print(f"Toeplitz output: {toeplitz_result.hex()}")
print(f"Polynomial output: {polynomial_result.hex()}")
print(f"Toeplitz seed overhead: {toeplitz.seed_length} bits")
print(f"Polynomial seed overhead: {polynomial.seed_length} bits")

# Verify universality
toeplitz_universal = toeplitz.verify_universality(num_tests=10000)
polynomial_universal = polynomial.verify_universality(num_tests=10000)
print(f"Toeplitz universality: {toeplitz_universal:.4f}")
print(f"Polynomial universality: {polynomial_universal:.4f}")
```

### Privacy Amplification Pipeline

```python
from quantum_crypto import PrivacyAmplificationPipeline

pipeline = PrivacyAmplificationPipeline(
    security_parameter=128,
    hash_function="toeplitz",
    batch_size=1000,
    parallel_workers=4
)

# Process multiple key blocks
key_blocks = [bytes(256) for _ in range(100)]
amplified_keys = pipeline.process_batch(
    key_blocks=key_blocks,
    leaked_info_per_block=20,
    seed_rotation=True
)

print(f"Processed {len(key_blocks)} blocks")
print(f"Output key length: {len(amplified_keys[0]) * 8} bits")
print(f"Total throughput: {pipeline.throughput:.2f} bits/s")
print(f"Security parameter per block: {pipeline.security_parameter}")
```

## Quantum Random Number Generation

### Quantum RNG for Key Generation

```python
from quantum_crypto import QuantumRNG, QRNGSource

# Configure quantum random number generator
qrng = QuantumRNG(
    source_type="vacuum_fluctuation",
    min_entropy_threshold=0.99,
    whitening_method="von_neumann"
)

# Generate random bits
random_bits = qrng.generate(
    num_bits=10000,
    post_processing="extractor",
    extractor_seed=bytes(64)
)

# Analyze randomness quality
analysis = qrng.analyze(random_bits)
print(f"Min-entropy: {analysis.min_entropy:.4f}")
print(f"Collision entropy: {analysis.collision_entropy:.4f}")
print(f"Guessing entropy: {analysis.guessing_entropy:.4f}")
print(f"NIST SP 800-90B compliant: {analysis.compliant}")

# Use for QKD basis selection
basis_choices = qrng.generate_basis_choices(
    num_pulses=100000,
    bases=["rectilinear", "diagonal"],
    bias=0.5
)
print(f"Basis bias: {analysis.bias:.4f}")
```

## Quantum Error Correction for QKD

### Error Correction for Quantum Channels

```python
from quantum_crypto import QuantumErrorCorrection, SteaneCode

# Apply error correction to protect quantum states in QKD
steane = SteaneCode()

# Encode qubits for transmission
encoded_qubits = steane.encode(
    qubit_state=[0.7071, 0.7071],  # |+> state
    num_redundant=7
)

# Simulate channel noise
noisy_qubits = steane.apply_noise(
    encoded_qubits,
    error_rate=0.05,
    error_type="depolarizing"
)

# Decode and correct
decoded, correction_info = steane.decode(
    noisy_qubits,
    syndrome_measurement=True
)

print(f"Encoded qubits: {encoded_qubits.shape}")
print(f"Syndrome: {correction_info.syndrome}")
print(f"Errors corrected: {correction_info.num_errors}")
print(f"Output fidelity: {correction_info.fidelity:.4f}")
```

## Post-Quantum Cryptography Integration

### Hybrid QKD + PQC Key Exchange

```python
from quantum_crypto import HybridKeyExchange, KyberKEM, DilithiumSignature

# Combine QKD with post-quantum cryptography
qkd_key = bytes(32)  # From QKD session
pqc_keypair = KyberKEM(security_level=3).generate_keypair()
encapsulation = KyberKEM(security_level=3).encapsulate(pqc_keypair.public_key)

hybrid = HybridKeyExchange(
    qkd_key=qkd_key,
    pqc_shared_secret=encapsulation.shared_secret,
    kdf="hkdf_sha256",
    combination_method="concatenation_then_kdf"
)

final_key = hybrid.derive_key(
    length=256,
    context=b"quantum-secure-session",
    info=b"hybrid-key-exchange"
)

print(f"Final key: {final_key.hex()}")
print(f"Key length: {len(final_key) * 8} bits")
print(f"Security level: {hybrid.security_level}")

# Sign with dilithium for authentication
signer = DilithiumSignature(security_level=3)
signature = signer.sign(final_key)
print(f"Signature size: {len(signature)} bytes")
verified = signer.verify(final_key, signature, pqc_keypair.public_key)
print(f"Signature verified: {verified}")
```

## Quantum Key Management

### Key Lifecycle Management

```python
from quantum_crypto import KeyManager, KeyStore, KeyPolicy

# Configure key management system
key_store = KeyStore(
    storage_type="hsm",
    max_keys=10000,
    encryption_algorithm="aes_256_gcm"
)

policy = KeyPolicy(
    max_key_age_seconds=3600,
    max_usage_count=1000000,
    min_security_parameter=128,
    auto_refresh=True
)

manager = KeyManager(store=key_store, policy=policy)

# Generate and store QKD keys
key_id = manager.generate_key(
    source="qkd",
    length=256,
    metadata={"protocol": "BB84", "session_id": "abc123"}
)

# Retrieve and use key
key = manager.get_key(key_id)
print(f"Key ID: {key_id}")
print(f"Key age: {key.age_seconds:.1f} seconds")
print(f"Usage count: {key.usage_count}")
print(f"Remaining budget: {key.remaining_budget}")

# Key refresh
new_key_id = manager.refresh_key(key_id)
print(f"New key ID: {new_key_id}")
```

### Quantum Key Distribution Network Management

```python
from quantum_crypto import QKDNetworkManager, NetworkNode

# Manage a multi-node QKD network
network = QKDNetworkManager()

# Add nodes
alice = network.add_node("Alice", role="sender")
bob = network.add_node("Bob", role="receiver")
charlie = network.add_node("Charlie", role="trusted_relay")

# Configure links
network.add_link(
    alice, charlie,
    protocol="BB84",
    key_rate=10000,
    distance_km=50
)
network.add_link(
    charlie, bob,
    protocol="E91",
    key_rate=5000,
    distance_km=80
)

# Monitor network
status = network.get_status()
print(f"Network nodes: {len(status.nodes)}")
print(f"Active links: {len(status.active_links)}")
print(f"Total key rate: {status.total_key_rate:.1f} bits/s")
print(f"Average QBER: {status.average_qber:.4f}")

# Route key from Alice to Bob
route = network.find_route("Alice", "Bob")
print(f"Route: {' â†’ '.join(route.path)}")
print(f"Hops: {route.hops}")
print(f"End-to-end key rate: {route.key_rate:.1f} bits/s")
```

## Security Proof Framework

### Composable Security Proofs

```python
from quantum_crypto import SecurityProof, ComposableSecurity

# Verify composable security of a QKD protocol
proof = SecurityProof(
    protocol="BB84_decoy",
    attack_model="coherent",
    finite_key=True,
    composable=True
)

security_result = proof.verify(
    qber=0.03,
    block_size=1000000,
    privacy_amplification_factor=0.8,
    error_correction_efficiency=0.95
)

print(f"Security parameter: {security_result.security_parameter}")
print(f"Composable security: {security_result.is_composable}")
print(f"Key rate lower bound: {security_result.key_rate_bound:.4f}")
print(f"Proof assumptions: {security_result.assumptions}")
print(f"Proof method: {proof.proof_method}")
```

## Performance Benchmarking

### QKD Protocol Benchmarking Suite

```python
from quantum_crypto import QKDBenchmark, BenchmarkSuite

# Run comprehensive QKD benchmarking
suite = BenchmarkSuite(
    protocols=["BB84", "E91", "MDI_QKD", "TF_QKD"],
    distances_km=[10, 50, 100, 200, 500],
    channel_models=["ideal", "realistic", "noisy"]
)

results = suite.run(
    num_shots=1000000,
    include_statistical_analysis=True
)

for protocol, protocol_results in results.items():
    print(f"\n{protocol}:")
    for distance, dist_results in protocol_results.items():
        print(f"  {distance} km:")
        print(f"    Key rate: {dist_results.key_rate:.2f} bits/s")
        print(f"    QBER: {dist_results.qber:.4f}")
        print(f"    Secure key fraction: {dist_results.secure_fraction:.4f}")
        print(f"    Execution time: {dist_results.execution_time:.2f} s")
```

## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills
