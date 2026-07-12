---
name: "smart-contract-development"
category: "blockchain"
version: "2.0.0"
tags: ["blockchain", "solidity", "smart-contracts", "ethereum", "development"]
---

# Smart Contract Development

## Overview

The Smart Contract Development module provides a comprehensive toolkit for writing, testing, deploying, and managing Solidity smart contracts on Ethereum and EVM-compatible chains. It covers contract architecture patterns, security best practices, gas optimization, upgradeability proxies, testing frameworks, deployment scripts, and verification workflows.

This skill is essential for blockchain developers building DeFi protocols, NFT platforms, DAOs, and any on-chain application. It emphasizes security-first development with checks-effects-interactions pattern, reentrancy guards, and access control.

## Core Capabilities

- **Contract Architecture**: Modular contract design, diamond pattern (EIP-2535), beacon proxies, and upgradability patterns
- **Security Patterns**: Reentrancy guards, checks-effects-interactions, pull-over-push, rate limiting, and pause mechanisms
- **Gas Optimization**: Storage packing, calldata vs memory, unchecked math, assembly snippets, and benchmark analysis
- **Access Control**: Role-based (OpenZeppelin), ownership, multi-sig, timelock, and permissionless design patterns
- **Testing**: Foundry (forge test), Hardhat, unit tests, fuzz testing, invariant testing, and fork testing
- **Deployment**: Scripted deployments, CREATE2 deterministic addresses, proxy deployment, and mainnet verification
- **Upgradeability**: Transparent proxy, UUPS, beacon proxy, storage layout management, and migration strategies
- **Token Standards**: ERC-20, ERC-721, ERC-1155, ERC-4626 vault, and custom token implementations
- **Event Design**: Structured logging, off-chain indexing, and event-driven architecture

## Usage Examples

```python
from smart_contract_development import (
    ContractTemplate,
    SecurityAnalyzer,
    GasOptimizer,
    DeploymentManager,
    TestSuite,
)

# --- Generate Contract Template ---
template = ContractTemplate()
erc20 = template.generate_erc20(
    name="Governance Token",
    symbol="GOV",
    decimals=18,
    initial_supply=1_000_000,
    features=["mintable", "burnable", "pausable", "access_control"],
)
print(f"Contract: {erc20.contract_name}")
print(f"Functions: {len(erc20.functions)}")
print(f"Events: {len(erc20.events)}")
print(f"Estimated gas (deploy): {erc20.estimated_gas:,}")

# --- Security Analysis ---
analyzer = SecurityAnalyzer()
issues = analyzer.analyze(erc20.source_code)
for issue in issues:
    print(f"  [{issue.severity.value}] {issue.title}")
    print(f"    {issue.description}")
    print(f"    Line {issue.line_number}: {issue.suggestion}")
print(f"Total issues: {len(issues)}")

# --- Gas Optimization ---
optimizer = GasOptimizer()
optimized = optimizer.optimize(erc20.source_code)
print(f"Gas savings: {optimized.savings_pct:.1f}%")
print(f"Original: {optimized.original_gas:,} gas")
print(f"Optimized: {optimized.optimized_gas:,} gas")

# --- Deployment ---
deployer = DeploymentManager(network="sepolia")
deploy_tx = deployer.deploy(
    contract=erc20,
    constructor_args=["Governance Token", "GOV", 1000000 * 10**18],
    confirmations=1,
)
print(f"Deployed at: {deploy_tx.contract_address}")
print(f"Tx hash: {deploy_tx.tx_hash}")
print(f"Gas used: {deploy_tx.gas_used:,}")

# --- Proxy Deployment (Upgradeable) ---
proxy = deployer.deploy_proxy(
    contract=erc20,
    proxy_type="transparent",
    admin="0xAdminAddress...",
)
print(f"Proxy: {proxy.proxy_address}")
print(f"Implementation: {proxy.implementation_address}")

# --- Test Suite ---
tests = TestSuite()
tests.add_test(
    name="test_transfer",
    setup="deploy contract",
    code="""
    function test_transfer() public {
        vm.prune(owner);
        token.transfer(recipient, 100);
        assertEq(token.balanceOf(recipient), 100);
    }
    """,
)
tests.add_test(
    name="test_fail_unauthorized",
    code="""
    function test_fail_unauthorized() public {
        vm.prune(attacker);
        token.mint(attacker, 1000);
    }
    """,
)
results = tests.run()
print(f"Tests: {results.passed}/{results.total} passed")

# --- Contract Verification ---
verified = deployer.verify(
    contract_address=deploy_tx.contract_address,
    contract_name="GovernanceToken",
    compiler_version="0.8.20",
    optimizations=True,
)
print(f"Verified: {verified.success}")
```

## Best Practices

- Always use Checks-Effects-Interactions pattern to prevent reentrancy
- Use OpenZeppelin's battle-tested libraries for ERC-20, access control, and security utilities
- Prefer `calldata` over `memory` for external function arguments (saves gas)
- Use `unchecked` blocks for math operations where overflow is impossible (saves gas)
- Implement pause functionality for emergency response in production contracts
- Use multi-signature wallets for admin operations — never use single EOA for contract ownership
- Run slither, mythril, and echidna static analysis before deployment
- Use foundry fuzz testing with meaningful invariants for complex protocol logic
- Store configuration in separate storage contracts to enable upgradeability
- Verify all contracts on Etherscan immediately after deployment for transparency

## Related Modules

- **smart-contracts**: Security auditing and formal verification of smart contracts
- **defi**: DeFi protocol implementation patterns
- **nft-development**: NFT-specific contract development
- **consensus-mechanisms**: Transaction processing and finality
