# Smart Contracts

## Overview

Smart contracts are self-executing programs stored on blockchain networks that automatically enforce and execute the terms of an agreement between parties. Originally pioneered by Ethereum, smart contracts enable decentralized applications (DApps) by providing trustless execution of code without intermediaries. This skill encompasses smart contract development, testing, deployment, and security auditing across multiple blockchain platforms. Smart contracts form the foundation of decentralized finance, NFTs, DAOs, and countless other Web3 applications that are transforming industries.

## Core Capabilities

Solidity development provides the primary language for Ethereum-compatible smart contracts, supporting object-oriented programming concepts with contract classes, inheritance, and libraries. Vyper offers an alternative Python-like syntax focused on security and gas optimization. Rust-based development for Solana and other high-performance chains enables concurrent execution and lower transaction costs. Contract testing frameworks like Foundry and Hardhat provide comprehensive unit, integration, and fuzz testing capabilities.

Smart contract security auditing identifies vulnerabilities including reentrancy, integer overflow/underflow, access control flaws, and front-running attacks. Upgradeable contract patterns using proxy delegates enable iterative development while preserving state and addresses. Gas optimization techniques minimize transaction costs through assembly-level optimization and efficient storage patterns. Multi-signature wallet implementations provide secure asset management requiring multiple approvals.

## Usage Examples

```python
from smart_contract_skill import SmartContract, SolidityCompiler, DeploymentManager, SecurityAuditor

# Create ERC-20 token contract
token_contract = SmartContract(
    name="MyToken",
    language="solidity",
    version="0.8.21",
    framework="foundry"
)

# Define token parameters
token_code = token_contract.generate_erc20(
    name="MyToken",
    symbol="MTK",
    decimals=18,
    initial_supply=1000000,
    mintable=True,
    burnable=True,
    pausable=True
)

# Create NFT contract with royalties
nft_contract = SmartContract(
    name="MyNFT",
    language="solidity",
    version="0.8.21"
)

nft_code = nft_contract.generate_erc721(
    name="MyNFT",
    symbol="MNFT",
    base_uri="ipfs://QmYourCID/",
    mintable=True,
    burnable=False,
    enumerable=True,
    supports_erc2981=True,
    royalty_percentage=250  # 2.5%
)

# Compile contracts
compiler = SolidityCompiler(
    solc_version="0.8.21",
    optimizer_enabled=True,
    optimizer_runs=200
)

compile_result = compiler.compile({
    "MyToken.sol": token_code,
    "MyNFT.sol": nft_code
})

print(f"Compilation Status: {compile_result.success}")
print(f"Bytecode Hash: {compile_result.bytecode_hash}")
print(f"ABI: {compile_result.abi}")

# Deploy to testnet
deployment_manager = DeploymentManager(
    network="sepolia",
    rpc_url="https://sepolia.infura.io/v3/YOUR_INFURA_KEY",
    private_key="YOUR_PRIVATE_KEY"
)

# Deploy ERC-20
token_deployment = deployment_manager.deploy(
    contract_name="MyToken",
    bytecode=compile_result.bytecode["MyToken"],
    abi=compile_result.abi["MyToken"],
    constructor_args=[]
)
print(f"Token Address: {token_deployment.contract_address}")
print(f"Transaction Hash: {token_deployment.transaction_hash}")

# Deploy ERC-721
nft_deployment = deployment_manager.deploy(
    contract_name="MyNFT",
    bytecode=compile_result.bytecode["MyNFT"],
    abi=compile_result.abi["MyNFT"],
    constructor_args=[]
)
print(f"NFT Address: {nft_deployment.contract_address}")

# Security audit
auditor = SecurityAuditor(
    framework="slither",
    mythril_enabled=True,
    manual_review=True
)

audit_result = auditor.audit(
    contracts=[token_code, nft_code],
    severity_threshold="medium"
)

print(f"Issues Found: {audit_result.total_issues}")
print(f"Critical: {audit_result.critical_count}")
print(f"High: {audit_result.high_count}")
print(f"Medium: {audit_result.medium_count}")
print(f"Low: {audit_result.low_count}")

# Generate upgradeable proxy contract
proxy_contract = SmartContract(
    name="TransparentProxy",
    language="solidity",
    version="0.8.21"
)

proxy_code = proxy_contract.generate_proxy(
    implementation_address=nft_deployment.contract_address,
    admin_address="0xAdminAddress",
    upgradeable=True,
    transparent_pattern=True
)
```

## Best Practices

Follow the principle of least privilege in access control, using modifiers and role-based permission systems to limit contract functionality. Implement reentrancy guards on all external calls using checks-effects-interactions pattern or ReentrancyGuard. Use safe math libraries or built-in overflow checking with Solidity 0.8+. Emit events for all state changes to enable off-chain indexing and monitoring.

Write comprehensive tests covering happy paths, edge cases, and failure scenarios using property-based testing where possible. Use formal verification for critical contracts handling significant value. Plan for upgrades from the start using proxy patterns, understanding the trade-offs between transparency and UUPS approaches. Document contract functionality clearly for users, auditors, and future developers.

## Related Skills

- DeFi (decentralized finance protocols)
- Blockchain Architecture (distributed ledger fundamentals)
- Security Auditing (smart contract vulnerability assessment)
- Web3 Development (blockchain application integration)

## Use Cases

Smart contracts power decentralized finance protocols enabling lending, borrowing, and trading without centralized intermediaries. NFT contracts establish digital ownership and provenance for art, gaming items, and collectibles. DAO governance contracts enable decentralized decision-making and treasury management. Supply chain applications use smart contracts to track provenance and automate payments based on delivery verification.
