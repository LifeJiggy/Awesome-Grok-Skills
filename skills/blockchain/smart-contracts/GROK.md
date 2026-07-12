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
