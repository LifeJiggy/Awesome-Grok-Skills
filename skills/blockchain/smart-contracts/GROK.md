---
name: "smart-contracts"
category: "blockchain"
version: "2.0.0"
tags: ["blockchain", "smart-contracts", "security-audit", "formal-verification", "Solidity"]
---

# Smart Contracts (Security & Auditing)

## Overview

The Smart Contracts module focuses on security auditing, formal verification, and vulnerability analysis of Solidity smart contracts. It provides automated detection of common vulnerability classes, manual audit checklist workflows, formal specification generation, and economic attack vector analysis. This module complements the development-focused smart-contract-development module by emphasizing post-development security review.

This skill is essential for smart contract auditors, security researchers, DeFi protocol teams, and anyone deploying contracts that handle significant value. It covers reentrancy, access control, arithmetic, oracle manipulation, flash loan attacks, and economic exploits.

## Core Capabilities

- **Automated Vulnerability Detection**: Slither/Mythril-style static analysis for reentrancy, unchecked calls, integer overflow, and access control issues
- **Manual Audit Checklist**: Structured audit workflow with sections for architecture, access control, business logic, arithmetic, and external interactions
- **Formal Verification**: Specification generation for invariant checking, state machine verification, and correctness proofs
- **Economic Attack Analysis**: Flash loan exploit detection, oracle manipulation, sandwich attack vectors, and governance attacks
- **Upgrade Security**: Storage layout verification, proxy pattern analysis, and initialization vulnerability checks
- **Dependency Analysis**: Known vulnerability database lookup for imported contracts (OpenZeppelin version checking)
- **Gas Griefing Detection**: DoS vectors, unbounded loops, and gas limit exploitation
- **Incident Response**: Post-exploit analysis templates, fund recovery patterns, and pause/upgrade emergency procedures

## Usage Examples

```python
from smart_contracts import (
    AuditEngine,
    FormalVerifier,
    EconomicAnalyzer,
    VulnerabilityDB,
    AuditReport,
)

# --- Run Automated Audit ---
audit = AuditEngine()
results = audit.run_full_audit(
    source_code=contract_source,
    contract_name="MyProtocol",
    compiler_version="0.8.20",
)
print(f"Critical: {results.critical_count}")
print(f"High: {results.high_count}")
print(f"Medium: {results.medium_count}")
print(f"Low: {results.low_count}")
print(f"Informational: {results.info_count}")

for finding in results.findings:
    print(f"\n[{finding.severity.value}] {finding.title}")
    print(f"  Location: {finding.file}:{finding.line}")
    print(f"  Description: {finding.description}")
    print(f"  Recommendation: {finding.recommendation}")
    print(f"  CWE: {finding.cwe_id}")

# --- Formal Verification ---
verifier = FormalVerifier()
spec = verifier.generate_spec(
    contract_source,
    invariants=[
        "totalSupply == sum(balanceOf[account] for all accounts)",
        "balanceOf[account] >= 0 for all accounts",
        "allowance[owner][spender] <= balanceOf[owner]",
    ],
)
print(f"Generated {len(spec.properties)} properties")
verification = verifier.verify(spec)
print(f"Properties verified: {verification.passed}/{verification.total}")
for counterexample in verification.counterexamples:
    print(f"  Counterexample: {counterexample}")

# --- Economic Attack Analysis ---
econ_analyzer = EconomicAnalyzer()
attacks = econ_analyzer.analyze_vectors(
    contract_source,
    protocol_type="lending",
)
for attack in attacks:
    print(f"\nAttack vector: {attack.vector}")
    print(f"  Severity: {attack.severity.value}")
    print(f"  Prerequisites: {', '.join(attack.prerequisites)}")
    print(f"  Impact: {attack.impact}")
    print(f"  Mitigation: {attack.mitigation}")

# --- Vulnerability Database ---
vulndb = VulnerabilityDB()
known = vulndb.check_dependencies(
    dependencies={
        "@openzeppelin/contracts": "4.8.0",
        "@uniswap/v2-periphery": "1.1.0-beta.0",
    }
)
for vuln in known:
    print(f"Known vulnerability: {vuln.id} - {vuln.title}")
    print(f"  Affected: {vuln.affected_versions}")
    print(f"  Patched: {vuln.patched_version}")

# --- Generate Audit Report ---
report = AuditReport(results=results, verifier=verification, economic=attacks)
markdown = report.to_markdown()
report.save("audit_report.md")
```

## Best Practices

- Run automated analysis BEFORE manual review to catch low-hanging fruit
- Always verify that math operations cannot overflow/underflow even with Solidity 0.8+
- Check that all external calls use the checks-effects-interactions pattern
- Verify that access control is implemented at every state-changing function
- Test with extreme values (MAX_UINT256, 0, address(0)) that attackers would try
- Check for front-running vulnerability on any function with economic incentives
- Verify oracle update mechanisms cannot be manipulated by flash loans
- Audit proxy upgrade storage layouts for collision with implementation slots
- Use invariant testing (foundry fuzz) to verify core protocol invariants hold
- Document all trust assumptions and external dependencies in the audit report

## Related Modules

- **smart-contract-development**: Contract development and architecture patterns
- **defi**: DeFi-specific vulnerability patterns and attack vectors
- **nft-development**: NFT contract security considerations
- **security-audit**: General security audit methodology

## Advanced Configuration

### Audit Tool Configuration

```yaml
# slither.config.json
{
  "detectors_to_run": "reentrancy-eth,arbitrary-send,controlled-delegatecall",
  "exclude_informational": true,
  "exclude_low": false,
  "filter_paths": "lib/,test/",
  "solc_remaps": [
    "@openzeppelin/=lib/openzeppelin-contracts/"
  ]
}
```

### Mythril Configuration

```json
{
  "execution_timeout": 30,
  "max_depth": 22,
  "loop_bound": 32,
  "create_timeout": 10,
  "transaction_count": 2,
  "strategy": "bfs",
  "smt_timeout": 300
}
```

### Echidna Property Testing Config

```yaml
# echidna.yaml
testMode: "property"
testLimit: 50000
shrinkLimit: 5000
seqLen: 100
deployer: "0x10000"
sender: ["0x10001", "0x10002", "0x10003"]
```

### Formal Verification with Certora

```json
{
  "files": ["contracts/MyProtocol.sol"],
  "spec": "specs/MyProtocol.spec",
  "verify": "MyProtocol:contracts/MyProtocol.sol",
  "prover_args": ["-depth 22", "-smt_nonLinearArithmetic true"],
  "loop_iter": 10,
  "solc_optimize": true,
  "solc_optimize_runs": 200
}
```

## Architecture Patterns

### Audit Workflow Architecture

```
Source Code Input
├── Static Analysis (Slither, Mythril)
│   ├── Vulnerability Detection
│   ├── Code Quality Issues
│   └── Gas Optimization Suggestions
├── Formal Verification (Certora, Halmos)
│   ├── Invariant Specification
│   ├── Property Proving
│   └── Counterexample Generation
├── Manual Review
│   ├── Architecture Assessment
│   ├── Access Control Review
│   ├── Business Logic Analysis
│   └── External Integration Review
└── Economic Analysis
    ├── Flash Loan Vectors
    ├── Oracle Manipulation
    └── Governance Attacks
```

### Vulnerability Classification Matrix

| Severity | Description | Response Time |
|----------|-------------|---------------|
| Critical | Direct fund loss, protocol insolvency | Immediate pause |
| High | Significant fund loss possible | Fix within 24 hours |
| Medium | Limited impact, requires specific conditions | Fix within 1 week |
| Low | Minor issues, gas waste, best practice violations | Fix before next release |
| Informational | Style issues, optimization suggestions | Track for future |

### Trust Boundary Model

```
External Calls (UNTRUSTED)
    ↓
Entry Points (VALIDATE)
    ↓
Access Control (AUTHORIZE)
    ↓
Business Logic (PROCESS)
    ↓
State Changes (COMMIT)
    ↓
Effects (EMIT)
    ↓
External Calls (INTERACT)
```

## Integration Guide

### Slither CI Integration

```yaml
# .github/workflows/security.yml
name: Security Analysis
on: [push, pull_request]
jobs:
  slither:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: crytic/slither-action@v0.3.0
        with:
          fail-on: medium
          slither-config: slither.config.json
```

### Mythril CI Integration

```yaml
  mythril:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Mythril
        run: |
          pip install mythril
          myth analyze contracts/ --execution-timeout 30 --json-output mythril-report.json
```

### Foundry Integration

```bash
# Run all security checks
forge test --match-path test/security -vvvv
forge coverage --report lcov
slither . --checklist security-audit-checklist.md
```

### Audit Report Generation

```python
from smart_contracts import AuditReport

report = AuditReport(
    results=slither_results + mythril_results,
    verifier=formal_verification,
    economic=economic_analysis,
    metadata={
        "auditor": "Security Team",
        "date": "2024-01-15",
        "scope": "MyProtocol v1.0",
        "commit": "abc1234",
    },
)
report.to_markdown("audit_report.md")
report.to_pdf("audit_report.pdf")
```

## Performance Optimization

### Analysis Speed Optimization

| Tool | Parallelization | Cache | Speedup |
|------|----------------|-------|---------|
| Slither | Multi-file analysis | Compiled output | 3-5x |
| Mythril | Function-level parallelism | State pruning | 2-4x |
| Echidna | Campaign parallelism | Coverage cache | 5-10x |
| Certora | Server-side parallelism | Proof cache | 10-50x |

### Coverage Optimization

```bash
# Fast coverage on large codebases
forge coverage --report summary
forge coverage --ir-minimum  # Faster but less precise

# Selective deep coverage
forge coverage --match-contract CriticalContract
```

### Test Execution Optimization

```solidity
// Use forge snapshots for regression testing
forge snapshot --match-contract TestSuite
forge snapshot --check   // Compare against baseline

// Use fork testing sparingly — cache RPC results
forge test --fork-url $ETH_RPC_URL --fork-block-number 18000000
```

## Security Considerations

### Audit Scope Definition

```
In-Scope:
├── All production Solidity contracts
├── Configuration parameters and initialization
├── Proxy upgrade mechanisms
├── External contract integrations (oracles, DEXes)
├── Access control and privilege escalation paths
├── Economic incentive mechanisms
└── Event emissions and off-chain implications

Out-of-Scope:
├── Test contracts and test helpers
├── Third-party library internals (unless forked)
├── Frontend and client-side code
├── Infrastructure and deployment scripts
└── Centralized server components
```

### Privilege Escalation Vectors

| Vector | Description | Check |
|--------|-------------|-------|
| Delegatecall to untrusted | Arbitrary code execution | Verify all delegatecall targets |
| Owner key compromise | Full admin access | Multi-sig + timelock |
| Oracle manipulation | Price feed corruption | TWAP + multi-oracle |
| Flash loan governance | One-shot voting power | Time-weighted voting |
| Storage collision | State corruption | Gap variables + layout verification |
| Initialize re-entry | Re-initialization attack | Initialized modifier |

## Troubleshooting Guide

### Common Audit Findings

| Finding | Description | Fix |
|---------|-------------|-----|
| Reentrancy | External call before state update | CEI pattern |
| Unchecked return | Low-level call result ignored | Require success |
| Centralization | Single EOA admin | Multi-sig + timelock |
| Integer overflow | Pre-0.8 arithmetic | Upgrade Solidity |
| Front-running | Predictable transactions | Commit-reveal |
| Flash loan vector | Single-block manipulation | Time-weighted ops |

### Slither False Positive Management

```python
# Add inline suppression
# slither-disable-next-line reentrancy-eth
function withdraw() external nonReentrant {
    // This is safe because of reentrancy guard
}
```

### Formal Verification Troubleshooting

```
Issue: Timeout on complex invariant
Solution: Decompose into simpler invariants

Issue: Counterexample too large
Solution: Add constraints to limit search space

Issue: Under-approximation warning
Solution: Increase loop iterations and timeout
```

## API Reference

### AuditEngine

```python
class AuditEngine:
    def run_full_audit(
        source_code: str,
        contract_name: str,
        compiler_version: str = "0.8.20",
        optimization_runs: int = 200,
    ) -> AuditResults:
        """Run comprehensive security audit."""
    
    def run_static_analysis(
        source_code: str,
        tools: list[str] = ["slither", "mythril"],
    ) -> AnalysisResults:
        """Run static analysis tools."""

class AuditResults:
    findings: list[Finding]
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    analysis_time_ms: int
    tool_versions: dict[str, str]
```

### FormalVerifier

```python
class FormalVerifier:
    def generate_spec(
        source_code: str,
        invariants: list[str],
    ) -> FormalSpec:
        """Generate formal specification from invariants."""
    
    def verify(spec: FormalSpec) -> VerificationResult:
        """Run formal verification on specification."""
    
    def model_check(
        source_code: str,
        properties: list[str],
        depth: int = 22,
    ) -> ModelCheckResult:
        """Run bounded model checking."""

class VerificationResult:
    passed: int
    total: int
    counterexamples: list[Counterexample]
    proof_timeout: bool
    verification_time_ms: int
```

### EconomicAnalyzer

```python
class EconomicAnalyzer:
    def analyze_vectors(
        source_code: str,
        protocol_type: str,  # lending, amm, governance, vault
    ) -> list[AttackVector]:
        """Analyze economic attack vectors."""
    
    def simulate_flash_loan_attack(
        source_code: str,
        asset: str,
        amount: int,
    ) -> FlashLoanSimulation:
        """Simulate flash loan exploit scenario."""

class AttackVector:
    vector: str
    severity: SeverityLevel
    prerequisites: list[str]
    impact: str
    mitigation: str
    cvss_score: float
```

## Data Models

### Finding

```
Finding:
  id: str                    # Unique finding identifier
  title: str                 # Short description
  severity: SeverityLevel    # critical, high, medium, low, info
  category: str              # reentrancy, access_control, arithmetic, etc.
  file: str                  # Source file path
  line: int                  # Line number
  code_snippet: str          # Relevant code
  description: str           # Detailed description
  recommendation: str        # Fix suggestion
  cwe_id: str                # CWE reference
  references: list[str]      # Related CVEs or articles
  confidence: float          # 0.0-1.0
```

### FormalSpec

```
FormalSpec:
  contract_name: str
  properties: list[Property]
  invariants: list[Invariant]
  preconditions: list[str]
  postconditions: list[str]
  methods: list[MethodSpec]

Property:
  name: str
  description: str
  formula: str               # Temporal logic formula
  expected: str              # satisfied, violated, unknown

Invariant:
  name: str
  expression: str
  scope: str                 # global, per-function, per-transaction
```

### AuditReport

```
AuditReport:
  metadata: AuditMetadata
  executive_summary: str
  scope: str
  findings: list[Finding]
  recommendations: list[str]
  appendix: dict
  generated_at: datetime
  auditor: str
  methodology: str
```

## Deployment Guide

### Audit Prerequisites

```
1. Complete, compilable source code
2. All test suites passing (unit, integration, fuzz)
3. Deployment scripts tested on testnet
4. Documentation of protocol mechanics
5. External dependency versions pinned
6. Known limitations documented
7. Previous audit findings addressed
```

### Audit Execution Steps

```
1. Code freeze and repository snapshot
2. Automated analysis (Slither, Mythril, Echidna)
3. Manual review — Architecture and design
4. Manual review — Access control and auth
5. Manual review — Business logic
6. Manual review — External interactions
7. Economic attack analysis
8. Formal verification (if applicable)
9. Finding classification and severity scoring
10. Report drafting and internal review
11. Report delivery and debrief
12. Remediation support
13. Re-audit of fixes
```

## Monitoring & Observability

### Post-Deployment Monitoring

```
Monitor for:
├── Unusual transaction volume spikes
├── Admin function calls
├── Large value transfers
├── Failed transactions (reverts)
├── New contract interactions
├── Oracle price feed anomalies
└── Governance proposal activity
```

### Alert Configuration

```yaml
alerts:
  - name: "Large Transfer"
    condition: "transfer_amount > 1% of total_supply"
    severity: medium
    action: notify_security_team
    
  - name: "Admin Function Call"
    condition: "caller != multisig_address AND function.is_admin"
    severity: high
    action: pause_and_investigate
    
  - name: "Flash Loan Volume"
    condition: "flash_loan_amount > $10M"
    severity: medium
    action: monitor_for_exploit
```

## Testing Strategy

### Security Test Categories

```
1. Unit Security Tests
   ├── Access control verification
   ├── Reentrancy guard testing
   └── Integer boundary testing

2. Fuzz Testing
   ├── Property-based testing (Echidna)
   ├── Invariant testing (Foundry)
   └── Differential testing

3. Integration Security Tests
   ├── Multi-contract interaction
   ├── External call behavior
   └── Proxy upgrade security

4. Economic Security Tests
   ├── Flash loan scenarios
   ├── Oracle manipulation
   └── Governance attack simulation
```

### Fuzz Testing Strategy

```solidity
// Foundry invariant test
function invariant_no_negative_balances() public {
    for (uint i = 0; i < tokenSupply; i++) {
        assertGe(token.balanceOf(token.ownerOf(i)), 0);
    }
}

function invariant_total_supply_conservation() public {
    assertEq(token.totalSupply(), initialSupply);
}
```

## Versioning & Migration

### Audit Versioning

```
v1.0.0-audit.0  Initial audit
v1.0.0-audit.1  Remediation of critical findings
v1.0.0-audit.2  Remediation of high findings
v1.0.0-audit.3  Final re-audit — all findings resolved
```

### Finding Lifecycle

```
Submitted → Triaged → Confirmed → Fix Proposed → Fix Implemented → Verified → Closed
                    └→ Disputed → Evidence Provided → Re-triaged
```

## Glossary

| Term | Definition |
|------|-----------|
| Audit | Systematic review of smart contract code for security vulnerabilities |
| CEI | Checks-Effects-Interactions pattern for reentrancy prevention |
| CVSS | Common Vulnerability Scoring System — severity rating |
| CWE | Common Weakness Enumeration — vulnerability taxonomy |
| Fuzz Testing | Randomized testing with unexpected inputs |
| Invariant | Property that must hold true in all states |
| Model Checking | Exhaustive state space exploration for property verification |
| Reentrancy | Attack pattern where external call re-enters calling function |
| Slither | Static analysis framework for Solidity |
| Mythril | Security analysis tool using symbolic execution |
| Echidna | Property-based testing tool for Solidity |
| Certora | Formal verification platform for smart contracts |

## Changelog

### 2.0.0 (2024-12-01)
- Added Certora formal verification integration
- Added economic attack analysis module
- Improved false positive suppression
- Added audit report PDF generation

### 1.2.0 (2024-08-15)
- Added Echidna property testing templates
- Improved Slither configuration presets
- Added multi-contract audit support

### 1.1.0 (2024-05-20)
- Added Mythril integration
- Added severity classification matrix
- Improved audit report templates

### 1.0.0 (2024-02-01)
- Initial release with Slither integration
- Basic audit checklist
- Manual review workflow

## Contributing Guidelines

### Adding New Vulnerability Patterns

1. Create a new detector in `detectors/`
2. Add test cases in `tests/detectors/`
3. Document the pattern in the knowledge base
4. Submit PR with test results showing detection rate

### Audit Report Templates

- Use standard severity levels: Critical, High, Medium, Low, Informational
- Include code snippets with line numbers
- Provide actionable recommendations with code examples
- Reference CWE IDs where applicable

### Testing Requirements

- All new detectors must pass unit tests
- False positive rate must be documented
- Performance benchmarks must be within thresholds

## License

MIT License

Copyright (c) 2024 Smart Contracts Security Contributors

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
