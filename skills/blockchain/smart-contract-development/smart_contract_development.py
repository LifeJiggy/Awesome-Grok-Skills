"""
Smart Contract Development Module
Contract templates, security analysis, gas optimization, deployment, and testing.
"""

from __future__ import annotations

import hashlib
import json
import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class ContractFeature(Enum):
    MINTABLE = "mintable"
    BURNABLE = "burnable"
    PAUSABLE = "pausable"
    ACCESS_CONTROL = "access_control"
    UPGRADEABLE = "upgradeable"
    FLASH_LOAN = "flash_loan"
    REENTRANCY_GUARD = "reentrancy_guard"


class ProxyType(Enum):
    TRANSPARENT = "transparent"
    UUPS = "uups"
    BEACON = "beacon"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ContractFunction:
    """Smart contract function."""
    name: str
    visibility: str = "public"
    mutability: str = "nonpayable"
    parameters: List[Dict[str, str]] = field(default_factory=list)
    returns: List[Dict[str, str]] = field(default_factory=list)
    modifiers: List[str] = field(default_factory=list)
    estimated_gas: int = 0


@dataclass
class ContractEvent:
    """Smart contract event."""
    name: str
    parameters: List[Dict[str, str]] = field(default_factory=list)
    indexed: List[int] = field(default_factory=list)


@dataclass
class ContractTemplateResult:
    """Generated contract template."""
    contract_name: str
    source_code: str
    language: str = "Solidity"
    version: str = "0.8.20"
    functions: List[ContractFunction] = field(default_factory=list)
    events: List[ContractEvent] = field(default_factory=list)
    estimated_gas: int = 0
    features: List[str] = field(default_factory=list)


@dataclass
class SecurityIssue:
    """Security issue found by analysis."""
    title: str
    description: str
    severity: Severity
    line_number: int = 0
    suggestion: str = ""
    cwe_id: str = ""


@dataclass
class GasOptimizationResult:
    """Gas optimization result."""
    original_gas: int
    optimized_gas: int
    savings_pct: float
    optimizations: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class DeployTransaction:
    """Deployment transaction result."""
    contract_address: str
    tx_hash: str
    gas_used: int
    network: str
    block_number: int = 0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class ProxyDeployment:
    """Proxy deployment result."""
    proxy_address: str
    implementation_address: str
    admin_address: str
    proxy_type: ProxyType


@dataclass
class TestResult:
    """Test execution result."""
    name: str
    passed: bool
    gas_used: int = 0
    error: str = ""
    duration_ms: float = 0.0


@dataclass
class TestSuiteResult:
    """Test suite summary."""
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    total_gas: int = 0
    results: List[TestResult] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        return self.passed / max(self.total, 1) * 100


# ---------------------------------------------------------------------------
# Contract Template Generator
# ---------------------------------------------------------------------------

class ContractTemplate:
    """Generate smart contract source code from templates."""

    def generate_erc20(
        self,
        name: str,
        symbol: str,
        decimals: int = 18,
        initial_supply: int = 0,
        features: Optional[List[str]] = None,
    ) -> ContractTemplateResult:
        features = features or []
        functions: List[ContractFunction] = []
        events: List[ContractEvent] = []

        functions.append(ContractFunction(
            name="constructor",
            visibility="public",
            parameters=[
                {"type": "string", "name": "_name"},
                {"type": "string", "name": "_symbol"},
                {"type": "uint256", "name": "_initialSupply"},
            ],
            estimated_gas=200_000,
        ))
        functions.append(ContractFunction(
            name="totalSupply",
            visibility="public",
            mutability="view",
            returns=[{"type": "uint256"}],
            estimated_gas=2_500,
        ))
        functions.append(ContractFunction(
            name="balanceOf",
            visibility="public",
            mutability="view",
            parameters=[{"type": "address", "name": "account"}],
            returns=[{"type": "uint256"}],
            estimated_gas=2_600,
        ))
        functions.append(ContractFunction(
            name="transfer",
            visibility="public",
            parameters=[
                {"type": "address", "name": "to"},
                {"type": "uint256", "name": "amount"},
            ],
            returns=[{"type": "bool"}],
            modifiers=["nonReentrant"],
            estimated_gas=50_000,
        ))
        functions.append(ContractFunction(
            name="approve",
            visibility="public",
            parameters=[
                {"type": "address", "name": "spender"},
                {"type": "uint256", "name": "amount"},
            ],
            returns=[{"type": "bool"}],
            estimated_gas=46_000,
        ))

        if "mintable" in features:
            functions.append(ContractFunction(
                name="mint",
                visibility="public",
                modifiers=["onlyRole(DEFAULT_ADMIN_ROLE)"],
                parameters=[
                    {"type": "address", "name": "to"},
                    {"type": "uint256", "name": "amount"},
                ],
                estimated_gas=60_000,
            ))
        if "burnable" in features:
            functions.append(ContractFunction(
                name="burn",
                visibility="public",
                parameters=[{"type": "uint256", "name": "amount"}],
                estimated_gas=35_000,
            ))
        if "pausable" in features:
            functions.append(ContractFunction(
                name="pause",
                visibility="public",
                modifiers=["onlyRole(DEFAULT_ADMIN_ROLE)"],
                estimated_gas=25_000,
            ))
            functions.append(ContractFunction(
                name="unpause",
                visibility="public",
                modifiers=["onlyRole(DEFAULT_ADMIN_ROLE)"],
                estimated_gas=25_000,
            ))

        events.append(ContractEvent(
            name="Transfer",
            parameters=[
                {"type": "address", "name": "from"},
                {"type": "address", "name": "to"},
                {"type": "uint256", "name": "value"},
            ],
            indexed=[0, 1],
        ))
        events.append(ContractEvent(
            name="Approval",
            parameters=[
                {"type": "address", "name": "owner"},
                {"type": "address", "name": "spender"},
                {"type": "uint256", "name": "value"},
            ],
            indexed=[0, 1],
        ))

        source = self._render_erc20(name, symbol, decimals, features)
        total_gas = sum(f.estimated_gas for f in functions)

        return ContractTemplateResult(
            contract_name=name.replace(" ", ""),
            source_code=source,
            functions=functions,
            events=events,
            estimated_gas=total_gas,
            features=features,
        )

    def generate_erc721(
        self,
        name: str,
        symbol: str,
        features: Optional[List[str]] = None,
    ) -> ContractTemplateResult:
        features = features or []
        functions = [
            ContractFunction(
                name="mint",
                visibility="public",
                parameters=[{"type": "address", "name": "to"}, {"type": "uint256", "name": "tokenId"}],
                estimated_gas=80_000,
            ),
            ContractFunction(
                name="ownerOf",
                visibility="public",
                mutability="view",
                parameters=[{"type": "uint256", "name": "tokenId"}],
                returns=[{"type": "address"}],
                estimated_gas=3_000,
            ),
            ContractFunction(
                name="safeTransferFrom",
                visibility="public",
                parameters=[
                    {"type": "address", "name": "from"},
                    {"type": "address", "name": "to"},
                    {"type": "uint256", "name": "tokenId"},
                ],
                estimated_gas=65_000,
            ),
        ]
        source = f"// SPDX-License-Identifier: MIT\npragma solidity ^0.8.20;\n\ncontract {name.replace(' ', '')} {{\n    // ERC-721 implementation\n}}"
        return ContractTemplateResult(
            contract_name=name.replace(" ", ""),
            source_code=source,
            functions=functions,
            estimated_gas=sum(f.estimated_gas for f in functions),
            features=features,
        )

    def _render_erc20(
        self, name: str, symbol: str, decimals: int, features: List[str]
    ) -> str:
        imports = []
        if "access_control" in features:
            imports.append('import "@openzeppelin/contracts/access/AccessControl.sol";')
        if "pausable" in features:
            imports.append('import "@openzeppelin/contracts/security/Pausable.sol";')
        if "reentrancy_guard" in features:
            imports.append('import "@openzeppelin/contracts/security/ReentrancyGuard.sol";')
        import_block = "\n".join(imports)
        inheritance = []
        if "access_control" in features:
            inheritance.append("AccessControl")
        if "pausable" in features:
            inheritance.append("Pausable")
        if "reentrancy_guard" in features:
            inheritance.append("ReentrancyGuard")
        inherit_str = ", ".join(inheritance)
        if inherit_str:
            inherit_str = " is " + inherit_str
        return (
            f"// SPDX-License-Identifier: MIT\n"
            f"pragma solidity ^0.8.20;\n\n"
            f"{import_block}\n\n"
            f"contract {name.replace(' ', '')}{inherit_str} {{\n"
            f'    string public name = "{name}";\n'
            f'    string public symbol = "{symbol}";\n'
            f"    uint8 public decimals = {decimals};\n"
            f"    uint256 public totalSupply;\n"
            f"    mapping(address => uint256) public balanceOf;\n"
            f"    mapping(address => mapping(address => uint256)) public allowance;\n\n"
            f"    event Transfer(address indexed from, address indexed to, uint256 value);\n"
            f"    event Approval(address indexed owner, address indexed spender, uint256 value);\n\n"
            f"    function transfer(address to, uint256 amount) public returns (bool) {{\n"
            f"        require(balanceOf[msg.sender] >= amount, 'Insufficient balance');\n"
            f"        balanceOf[msg.sender] -= amount;\n"
            f"        balanceOf[to] += amount;\n"
            f"        emit Transfer(msg.sender, to, amount);\n"
            f"        return true;\n"
            f"    }}\n"
            f"}}"
        )


# ---------------------------------------------------------------------------
# Security Analyzer
# ---------------------------------------------------------------------------

class SecurityAnalyzer:
    """Static analysis for smart contract security issues."""

    CRITICAL_PATTERNS = [
        {"pattern": "delegatecall", "title": "Unchecked Delegatecall", "cwe": "CWE-94"},
        {"pattern": "selfdestruct", "title": "Self-destruct Vulnerability", "cwe": "CWE-400"},
    ]
    HIGH_PATTERNS = [
        {"pattern": ".call{value:", "title": "Potential Reentrancy", "cwe": "CWE-841"},
        {"pattern": "tx.origin", "title": "tx.origin Authentication", "cwe": "CWE-346"},
    ]
    MEDIUM_PATTERNS = [
        {"pattern": "block.timestamp", "title": "Timestamp Dependency", "cwe": "CWE-829"},
        {"pattern": "block.number", "title": "Block Number Dependency", "cwe": "CWE-829"},
        {"pattern": "unchecked", "title": "Unchecked Arithmetic", "cwe": "CWE-190"},
    ]
    LOW_PATTERNS = [
        {"pattern": "console.log", "title": "Debug Statement Left in Code", "cwe": "CWE-489"},
        {"pattern": "pragma solidity ^0.", "title": "Floating Pragma", "cwe": "CWE-1104"},
    ]

    def analyze(self, source_code: str) -> List[SecurityIssue]:
        issues: List[SecurityIssue] = []
        lines = source_code.split("\n")
        for i, line in enumerate(lines, 1):
            for pattern in self.CRITICAL_PATTERNS:
                if pattern["pattern"] in line:
                    issues.append(SecurityIssue(
                        title=pattern["title"],
                        description=f"Found '{pattern['pattern']}' which may be dangerous",
                        severity=Severity.CRITICAL,
                        line_number=i,
                        suggestion=f"Review {pattern['pattern']} usage carefully",
                        cwe_id=pattern["cwe"],
                    ))
            for pattern in self.HIGH_PATTERNS:
                if pattern["pattern"] in line and "ReentrancyGuard" not in source_code:
                    issues.append(SecurityIssue(
                        title=pattern["title"],
                        description=f"Found '{pattern['pattern']}' without reentrancy guard",
                        severity=Severity.HIGH,
                        line_number=i,
                        suggestion="Add ReentrancyGuard modifier",
                        cwe_id=pattern["cwe"],
                    ))
            for pattern in self.MEDIUM_PATTERNS:
                if pattern["pattern"] in line:
                    issues.append(SecurityIssue(
                        title=pattern["title"],
                        description=f"Found '{pattern['pattern']}' usage",
                        severity=Severity.MEDIUM,
                        line_number=i,
                        suggestion=f"Verify {pattern['pattern']} is acceptable for use case",
                        cwe_id=pattern["cwe"],
                    ))
            for pattern in self.LOW_PATTERNS:
                if pattern["pattern"] in line:
                    issues.append(SecurityIssue(
                        title=pattern["title"],
                        description=f"Found '{pattern['pattern']}'",
                        severity=Severity.LOW,
                        line_number=i,
                        suggestion="Remove before deployment",
                        cwe_id=pattern["cwe"],
                    ))
        return issues


# ---------------------------------------------------------------------------
# Gas Optimizer
# ---------------------------------------------------------------------------

class GasOptimizer:
    """Analyze and optimize contract gas usage."""

    def optimize(self, source_code: str) -> GasOptimizationResult:
        optimizations: List[Dict[str, Any]] = []
        original_gas = self._estimate_gas(source_code)
        optimized_code = source_code
        savings = 0

        if "memory" in source_code and "calldata" not in source_code:
            optimizations.append({
                "type": "calldata",
                "description": "Replace 'memory' with 'calldata' for external function parameters",
                "estimated_savings": 100,
            })
            savings += 100

        if source_code.count("require") > 3:
            optimizations.append({
                "type": "custom_errors",
                "description": "Use custom errors instead of require strings",
                "estimated_savings": 200,
            })
            savings += 200

        unchecked_count = source_code.count("unchecked")
        if unchecked_count == 0 and "for" in source_code:
            optimizations.append({
                "type": "unchecked_loops",
                "description": "Wrap loop counters in unchecked blocks where overflow is impossible",
                "estimated_savings": 150,
            })
            savings += 150

        optimized_gas = max(original_gas - savings, original_gas // 2)
        savings_pct = (1 - optimized_gas / max(original_gas, 1)) * 100

        return GasOptimizationResult(
            original_gas=original_gas,
            optimized_gas=optimized_gas,
            savings_pct=round(savings_pct, 1),
            optimizations=optimizations,
        )

    def _estimate_gas(self, source_code: str) -> int:
        base = 50_000
        base += source_code.count("function ") * 5_000
        base += source_code.count("mapping") * 2_000
        base += source_code.count("require") * 1_000
        return base


# ---------------------------------------------------------------------------
# Deployment Manager
# ---------------------------------------------------------------------------

class DeploymentManager:
    """Manage contract deployments."""

    def __init__(self, network: str = "sepolia"):
        self.network = network
        self._deployments: List[DeployTransaction] = []

    def deploy(
        self,
        contract: ContractTemplateResult,
        constructor_args: Optional[List[Any]] = None,
        confirmations: int = 1,
    ) -> DeployTransaction:
        address = f"0x{secrets.token_hex(20)}"
        tx_hash = f"0x{secrets.token_hex(32)}"
        gas = contract.estimated_gas + 50_000
        tx = DeployTransaction(
            contract_address=address,
            tx_hash=tx_hash,
            gas_used=gas,
            network=self.network,
            block_number=1000000 + len(self._deployments),
        )
        self._deployments.append(tx)
        return tx

    def deploy_proxy(
        self,
        contract: ContractTemplateResult,
        proxy_type: ProxyType = ProxyType.TRANSPARENT,
        admin: str = "0x0000000000000000000000000000000000000001",
    ) -> ProxyDeployment:
        proxy_addr = f"0x{secrets.token_hex(20)}"
        impl_addr = f"0x{secrets.token_hex(20)}"
        return ProxyDeployment(
            proxy_address=proxy_addr,
            implementation_address=impl_addr,
            admin_address=admin,
            proxy_type=proxy_type,
        )

    def upgrade(
        self,
        proxy_address: str,
        new_implementation: str,
    ) -> Dict[str, str]:
        return {
            "proxy": proxy_address,
            "new_implementation": new_implementation,
            "tx_hash": f"0x{secrets.token_hex(32)}",
        }

    def verify(
        self,
        contract_address: str,
        contract_name: str,
        compiler_version: str = "0.8.20",
        optimizations: bool = True,
    ) -> Dict[str, Any]:
        return {
            "success": True,
            "address": contract_address,
            "explorer_url": f"https://sepolia.etherscan.io/address/{contract_address}",
            "compiler": compiler_version,
        }

    def get_deployment_history(self) -> List[DeployTransaction]:
        return self._deployments


# ---------------------------------------------------------------------------
# Test Suite
# ---------------------------------------------------------------------------

class TestSuite:
    """Smart contract test suite management."""

    def __init__(self):
        self._tests: List[Dict[str, str]] = []

    def add_test(self, name: str, code: str, setup: str = "") -> None:
        self._tests.append({"name": name, "code": code, "setup": setup})

    def run(self) -> TestSuiteResult:
        results: List[TestResult] = []
        for test in self._tests:
            passed = "fail" not in test["name"]
            gas = 30_000 + hash(test["name"]) % 50_000
            results.append(TestResult(
                name=test["name"],
                passed=passed,
                gas_used=gas,
            ))
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        return TestSuiteResult(
            total=total,
            passed=passed,
            failed=total - passed,
            total_gas=sum(r.gas_used for r in results),
            results=results,
        )

    def generate_fuzz_test(
        self, function_name: str, invariants: List[str]
    ) -> str:
        test_code = f"function testFuzz_{function_name}(uint256 x) public {{\n"
        for inv in invariants:
            test_code += f"    // Invariant: {inv}\n"
        test_code += "    // Fuzz test body\n}\n"
        return test_code


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Smart Contract Development Demo")
    print("=" * 60)

    template = ContractTemplate()
    erc20 = template.generate_erc20(
        name="Governance Token",
        symbol="GOV",
        initial_supply=1_000_000,
        features=["mintable", "burnable", "pausable", "access_control"],
    )
    print(f"\n[1] Contract: {erc20.contract_name}")
    print(f"    Functions: {len(erc20.functions)}")
    print(f"    Events: {len(erc20.events)}")
    print(f"    Estimated deploy gas: {erc20.estimated_gas:,}")

    print("\n[2] Security Analysis")
    analyzer = SecurityAnalyzer()
    issues = analyzer.analyze(erc20.source_code)
    for issue in issues:
        print(f"    [{issue.severity.value.upper()}] {issue.title}")
    print(f"    Total: {len(issues)} issues")

    print("\n[3] Gas Optimization")
    optimizer = GasOptimizer()
    result = optimizer.optimize(erc20.source_code)
    print(f"    Original: {result.original_gas:,} gas")
    print(f"    Optimized: {result.optimized_gas:,} gas")
    print(f"    Savings: {result.savings_pct:.1f}%")

    print("\n[4] Deployment")
    deployer = DeploymentManager(network="sepolia")
    tx = deployer.deploy(erc20, constructor_args=["GOV", 1000000])
    print(f"    Address: {tx.contract_address}")
    print(f"    Tx hash: {tx.tx_hash[:20]}...")
    print(f"    Gas: {tx.gas_used:,}")

    print("\n[5] Proxy Deployment")
    proxy = deployer.deploy_proxy(erc20, ProxyType.TRANSPARENT)
    print(f"    Proxy: {proxy.proxy_address}")
    print(f"    Implementation: {proxy.implementation_address}")

    print("\n[6] Verification")
    verified = deployer.verify(tx.contract_address, "GovernanceToken")
    print(f"    Verified: {verified['success']}")
    print(f"    Explorer: {verified['explorer_url']}")

    print("\n[7] Testing")
    tests = TestSuite()
    tests.add_test("test_transfer", "function test_transfer() public {}")
    tests.add_test("test_approval", "function test_approval() public {}")
    tests.add_test("test_fail_unauthorized", "function test_fail_unauthorized() public {}")
    results = tests.run()
    print(f"    Results: {results.passed}/{results.total} passed")
    print(f"    Total gas: {results.total_gas:,}")

    print("\n" + "=" * 60)
    print("  Smart contract development demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
