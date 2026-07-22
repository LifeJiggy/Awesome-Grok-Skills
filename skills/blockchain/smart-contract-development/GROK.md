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

## Advanced Configuration

### Compiler Settings

```toml
# foundry.toml
[profile.default]
solc_version = "0.8.20"
optimizer = true
optimizer_runs = 200
via_ir = false
evm_version = "shanghai"
ffi = false
fs_permissions = [{ access = "read", path = "./out" }]

[profile.default.rpc_endpoints]
mainnet = "${ETH_RPC_URL}"
sepolia = "${SEPOLIA_RPC_URL}"
arbitrum = "${ARB_RPC_URL}"

[profile.default.etherscan]
mainnet = { key = "${ETHERSCAN_API_KEY}" }
sepolia = { key = "${ETHERSCAN_API_KEY}" }
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ETH_RPC_URL` | Ethereum mainnet RPC endpoint | Required |
| `SEPOLIA_RPC_URL` | Sepolia testnet RPC endpoint | Required for testing |
| `ETHERSCAN_API_KEY` | Etherscan API key for verification | Required for verification |
| `PRIVATE_KEY` | Deployer wallet private key | Required for deployment |
| `FOUNDRY_PROFILE` | Active Foundry profile | `default` |
| `CI` | Set in CI environments | `false` |

### Custom Remappings

```
# remappings.txt
@openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/
@openzeppelin/contracts-upgradeable/=lib/openzeppelin-upgradeable/contracts/
forge-std/=lib/forge-std/src/
solmate/=lib/solmate/src/
```

### Multi-Network Configuration

```toml
# Network-specific profiles
[profile.production]
optimizer = true
optimizer_runs = 100000
via_ir = true
gas_reports = ["MyContract"]

[profile.testing]
fuzz = { runs = 10000, max_test_rejects = 65536 }
invariant = { runs = 256, depth = 32 }
```

## Architecture Patterns

### Diamond Pattern (EIP-2535)

The Diamond pattern allows splitting a contract across multiple implementation contracts while presenting a single external interface.

```
Diamond Proxy
├── DiamondCutFacet (add/replace/remove facets)
├── DiamondLoupeFacet (introspection)
├── OwnershipFacet (access control)
├── FacetA (business logic)
├── FacetB (business logic)
└── FacetC (business logic)
```

Key storage slots:
- `DIAMOND_STORAGE_POSITION`: Diamond storage struct
- `FACET_ADDRESS_POSITION`: Mapping of function selectors to facets
- `FACET_FUNCTION_SELECTORS`: Mapping of facets to their selectors

### Proxy Patterns Comparison

| Pattern | Proxy | Admin | Upgradeability | Gas Overhead |
|---------|-------|-------|----------------|--------------|
| Transparent | TransparentUpgradeableProxy | ProxyAdmin contract | Admin-only upgrade | ~5000 gas |
| UUPS | ERC1967Proxy | Implementation contract | Any holder with role | ~2000 gas |
| Beacon | UpgradeableBeacon | Beacon owner | Single upgrade for all | ~3000 gas |
| Diamond | Diamond | DiamondCut facet | Via facet functions | ~8000 gas |

### Checks-Effects-Interactions Pattern

```solidity
// CORRECT pattern
function withdraw(uint256 amount) external nonReentrant {
    // CHECKS
    require(balanceOf[msg.sender] >= amount, "Insufficient balance");
    
    // EFFECTS
    balanceOf[msg.sender] -= amount;
    totalSupply -= amount;
    
    // INTERACTIONS
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

### Pull-Over-Push Pattern

Instead of pushing funds to multiple recipients (risky with reentrancy), allow each recipient to pull:

```solidity
mapping(address => uint256) public balances;

function withdraw() external nonReentrant {
    uint256 amount = balances[msg.sender];
    require(amount > 0, "No funds");
    balances[msg.sender] = 0;
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
}
```

### Storage Layout Strategy

```
Contract Storage Layout:
├── Gap variables (uint256[N] __gap)
├── Implementation-specific storage
├── Inherited storage (from base contracts)
└── Upgrade-safe storage (ERC-7201 namespaced)
```

## Integration Guide

### Foundry + Hardhat Integration

```bash
# Install both frameworks
forge init my-project
cd my-project
npm init -y
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox

# Use Foundry for testing, Hardhat for deployment
forge test                    # Fast unit tests
npx hardhat deploy --network mainnet  # Hardhat deployment scripts
```

### OpenZeppelin Defender Integration

```python
from smart_contract_development import DefenderIntegration

defender = DefenderIntegration(
    api_key="your-defender-api-key",
    api_secret="your-defender-api-secret",
)

# Propose upgrade through Defender
proposal = defender.propose_upgrade(
    proxy_address="0xProxy...",
    new_implementation="0xNewImpl...",
    title="V2 Upgrade",
    description="Adds new fee mechanism",
)
print(f"Proposal URL: {proposal.url}")
```

### The Graph Integration

```solidity
// Event definitions for subgraph indexing
event Transfer(address indexed from, address indexed to, uint256 value);
event Approval(address indexed owner, address indexed spender, uint256 value);
event RoleGranted(bytes32 indexed role, address indexed account, address indexed sender);
```

```yaml
# subgraph.yaml
dataSources:
  - kind: ethereum/contract
    name: MyToken
    network: mainnet
    source:
      address: "0x..."
      abi: MyToken
      startBlock: 18000000
    mapping:
      kind: ethereum/events
      apiVersion: 0.0.7
      language: wasm/assemblyscript
      entities:
        - Token
        - TransferEvent
      abis:
        - name: MyToken
          file: ./abis/MyToken.json
```

### Ethers.js v6 Deployment Script

```javascript
const { ethers } = require("hardhat");

async function deploy() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const Token = await ethers.getContractFactory("GovernanceToken");
  const token = await Token.deploy("Governance Token", "GOV", 1000000n * 10n ** 18n);
  await token.waitForDeployment();

  const address = await token.getAddress();
  console.log("Deployed at:", address);

  // Verify on Etherscan
  await run("verify:verify", {
    address,
    constructorArguments: ["Governance Token", "GOV", 1000000n * 10n ** 18n],
  });
}
```

## Performance Optimization

### Gas Optimization Techniques

| Technique | Savings | Example |
|-----------|---------|---------|
| `calldata` vs `memory` | ~60 gas per call | `function f(uint[] calldata data)` |
| `unchecked` math | ~100 gas/op | `unchecked { ++i; }` |
| Storage packing | ~2000 gas/slot | Pack `uint128 + uint128` in one slot |
| `bytes32` vs `string` | ~200 gas | `bytes32 name` for fixed strings |
| Immutable variables | ~2000 gas/read | `uint256 public immutable MAX_SUPPLY` |
| Short-circuit `require` | Variable | `require(a && b, "Failed")` — check cheap first |
| `uint256` for small values | ~100 gas | Avoids sign extension overhead |

### Assembly Optimizations

```solidity
// Custom error (saves gas vs require with string)
error InsufficientBalance(uint256 available, uint256 required);

// Assembly for low-level operations
function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
    assembly {
        if lt(add(a, b), a) { revert(0, 0) }
    }
    return add(a, b);
}
```

### Storage Optimization

```solidity
// BAD: wastes storage slots
uint8 status;        // slot 0 (1 byte, 31 wasted)
address owner;       // slot 1 (20 bytes, 12 wasted)
uint256 supply;      // slot 2 (32 bytes)

// GOOD: packed into single slot
struct PackedState {
    uint128 supply;     // slot 0 (16 bytes)
    address owner;      // slot 0 (20 bytes) -- fits in same slot
    uint8 status;       // slot 0 (1 byte)
}
```

### Benchmark Analysis

```python
from smart_contract_development import GasBenchmark

benchmark = GasBenchmark()
results = benchmark.run(
    contract="GovernanceToken",
    functions=["transfer", "approve", "mint", "burn"],
    scenarios=[
        {"name": "first_call", "cold_slots": True},
        {"name": "subsequent", "cold_slots": False},
    ],
)
for r in results:
    print(f"{r.function}: {r.avg_gas:,} gas ({r.scenario})")
```

## Security Considerations

### Threat Model

| Threat | Impact | Mitigation |
|--------|--------|------------|
| Reentrancy | Critical | ReentrancyGuard, CEI pattern |
| Integer Overflow | High | Solidity 0.8+ checked math |
| Access Control | Critical | OpenZeppelin AccessControl |
| Front-Running | Medium | Commit-reveal, slippage limits |
| Oracle Manipulation | Critical | TWAP, multi-oracle aggregation |
| Flash Loan Attacks | High | Time-weighted operations |
| Storage Collision | Critical | Gap variables, ERC-7201 |

### Security Audit Checklist

- [ ] No reentrancy vulnerabilities (CEI pattern followed)
- [ ] Access control on all state-changing functions
- [ ] Integer overflow/underflow checked (Solidity 0.8+)
- [ ] External calls at end of functions
- [ ] No arbitrary `delegatecall` targets
- [ ] Pause mechanism for emergency response
- [ ] Multi-sig for admin operations
- [ ] Slither static analysis clean
- [ ] Mythril analysis clean
- [ ] Fuzz testing covers edge cases
- [ ] Invariant tests verify core assumptions
- [ ] All contracts verified on Etherscan

### Emergency Response Procedures

```
1. DETECT: Alert triggers on anomalous activity
2. ASSESS: Determine severity and affected contracts
3. PAUSE: Activate emergency pause if available
4. INVESTIGATE: Analyze transaction traces and state
5. REMEDIATE: Deploy fix via upgrade or new deployment
6. RECOVER: Resume operations after validation
7. POST-MORTEM: Document root cause and preventive measures
```

## Troubleshooting Guide

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| `EvmError: Revert` | Contract reverted | Check require/revert conditions |
| `Nonce too low` | Stale nonce | Fetch fresh nonce from RPC |
| `Replacement transaction underpriced` | Gas too low | Increase gas price for replacement |
| `Internal error: too much recursion` | Stack overflow | Refactor to reduce stack depth |
| `Compiler run successful` but no output | Missing ABI | Check compiler output settings |

### Debugging Workflow

```bash
# Trace failed transaction
cast tx 0x... --rpc-url $ETH_RPC_URL -vvvv

# Debug with Foundry
forge test --match-test testFailing -vvvv

# Estimate gas before sending
cast estimate 0xContract "transfer(address,uint256)" 0xRecipient 1000 --rpc-url $ETH_RPC_URL

# Check contract storage
cast storage 0xContract 0 --rpc-url $ETH_RPC_URL
```

###常见 Deployment Failures

```
1. Insufficient gas: Increase gas limit by 20-30%
2. Nonce conflict: Use explicit nonce management
3. Chain ID mismatch: Verify hardhat.config network settings
4. Constructor args mismatch: Verify ABI encoding
5. Insufficient funds: Check deployer ETH balance
```

## API Reference

### ContractTemplate

```python
class ContractTemplate:
    """Generate smart contract source code from templates."""
    
    def generate_erc20(
        name: str,
        symbol: str,
        decimals: int,
        initial_supply: int,
        features: list[str] = None,
    ) -> ContractArtifact:
        """Generate ERC-20 contract with specified features."""
    
    def generate_erc721(
        name: str,
        symbol: str,
        base_uri: str,
        features: list[str] = None,
    ) -> ContractArtifact:
        """Generate ERC-721 contract."""
    
    def generate_erc1155(
        name: str,
        base_uri: str,
        token_uris: list[str] = None,
    ) -> ContractArtifact:
        """Generate ERC-1155 contract."""
```

### SecurityAnalyzer

```python
class SecurityAnalyzer:
    """Static analysis for smart contract vulnerabilities."""
    
    def analyze(source_code: str) -> list[SecurityIssue]:
        """Run full security analysis on source code."""
    
    def check_reentrancy(source_code: str) -> list[SecurityIssue]:
        """Check for reentrancy vulnerabilities."""
    
    def check_access_control(source_code: str) -> list[SecurityIssue]:
        """Check for access control issues."""

class SecurityIssue:
    severity: SeverityLevel  # critical, high, medium, low, info
    title: str
    description: str
    line_number: int
    suggestion: str
    cwe_id: str
```

### GasOptimizer

```python
class GasOptimizer:
    """Analyze and optimize gas usage in smart contracts."""
    
    def optimize(source_code: str) -> OptimizationResult:
        """Apply gas optimizations to source code."""
    
    def estimate_gas(contract_address: str, calls: list[CallSpec]) -> GasEstimate:
        """Estimate gas for contract interactions."""

class OptimizationResult:
    original_gas: int
    optimized_gas: int
    savings_pct: float
    optimizations_applied: list[str]
```

### DeploymentManager

```python
class DeploymentManager:
    """Manage contract deployments across networks."""
    
    def __init__(self, network: str, private_key: str = None): ...
    
    def deploy(
        contract: ContractArtifact,
        constructor_args: list = None,
        confirmations: int = 1,
    ) -> DeploymentResult:
        """Deploy contract to network."""
    
    def deploy_proxy(
        contract: ContractArtifact,
        proxy_type: str = "transparent",
        admin: str = None,
    ) -> ProxyDeploymentResult:
        """Deploy upgradeable proxy."""
    
    def verify(
        contract_address: str,
        contract_name: str,
        compiler_version: str,
        optimizations: bool = True,
    ) -> VerificationResult:
        """Verify contract on block explorer."""
```

## Data Models

### ContractArtifact

```
ContractArtifact:
  contract_name: str          # Name of the contract
  source_code: str            # Full Solidity source
  abi: list[dict]             # ABI JSON
  bytecode: str               # Hex-encoded bytecode
  functions: list[Function]   # Extracted function signatures
  events: list[Event]         # Extracted event definitions
  estimated_gas: int          # Estimated deployment gas
  compiler_version: str       # Solidity compiler version
  metadata_hash: str          # IPFS metadata hash
```

### DeploymentResult

```
DeploymentResult:
  contract_address: str       # Deployed contract address
  tx_hash: str                # Transaction hash
  gas_used: int               # Gas consumed
  block_number: int           # Block of deployment
  network: str                # Network name
  deployer: str               # Deployer address
  timestamp: int              # Unix timestamp
  verification_status: str    # pending, verified, failed
```

### SecurityReport

```
SecurityReport:
  total_findings: int
  critical: list[SecurityIssue]
  high: list[SecurityIssue]
  medium: list[SecurityIssue]
  low: list[SecurityIssue]
  informational: list[SecurityIssue]
  overall_risk: str           # critical, high, medium, low
  scan_duration_ms: int
  tool_versions: dict[str, str]
```

## Deployment Guide

### Prerequisites

```bash
# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Install dependencies
forge install OpenZeppelin/openzeppelin-contracts
forge install OpenZeppelin/openzeppelin-contracts-upgradeable

# Set environment variables
export ETH_RPC_URL="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"
export SEPOLIA_RPC_URL="https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY"
export PRIVATE_KEY="your-deployer-private-key"
export ETHERSCAN_API_KEY="your-etherscan-key"
```

### Deployment Workflow

```
1. Write contract code
2. Write unit tests (forge test)
3. Write fuzz tests (foundry fuzz)
4. Run static analysis (slither)
5. Deploy to testnet (sepolia)
6. Verify on testnet explorer
7. Integration testing on testnet
8. Security audit
9. Deploy to mainnet
10. Verify on Etherscan
11. Transfer ownership to multisig
12. Update documentation
```

### Post-Deployment Verification

```bash
# Verify contract source code
forge verify-contract 0xAddress MyContract \
  --chain-id 1 \
  --constructor-args $(cast abi-encode "constructor(string,string,uint256)" "Token" "TKN" 1000000000000000000000000)

# Check deployment
cast call 0xAddress "name()" --rpc-url $ETH_RPC_URL
cast call 0xAddress "symbol()" --rpc-url $ETH_RPC_URL
cast call 0xAddress "totalSupply()" --rpc-url $ETH_RPC_URL
```

## Monitoring & Observability

### Key Metrics to Monitor

| Metric | Alert Threshold | Description |
|--------|----------------|-------------|
| Transaction volume | >2x baseline | Unusual activity spike |
| Failed transactions | >5% rate | Potential contract issue |
| Gas usage anomaly | >3x average | Possible attack vector |
| Large transfers | >1% supply | Whale movement alert |
| Admin function calls | Any call | Privileged action monitoring |
| Pause events | Any event | Emergency response trigger |

### Event Monitoring Setup

```python
from smart_contract_development import EventMonitor

monitor = EventMonitor(
    contract_address="0x...",
    rpc_url="https://eth-mainnet.g.alchemy.com/v2/...",
)

monitor.watch_events(
    events=["Transfer", "Approval", "Paused"],
    callback=lambda event: print(f"Event: {event.name} - {event.args}"),
    from_block="latest",
)
```

### Logging Best Practices

```
Structured logging format:
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info",
  "contract": "0x...",
  "function": "transfer",
  "caller": "0x...",
  "args": {"to": "0x...", "amount": "1000000"},
  "tx_hash": "0x...",
  "gas_used": 52000,
  "block": 18000000
}
```

## Testing Strategy

### Test Pyramid

```
         /\
        /  \        E2E Tests (few)
       /    \       - Fork tests
      /------\      
     /        \     Integration Tests (some)
    /          \    - Multi-contract interaction
   /------------\   
  /              \  Unit Tests (many)
 /                \ - Individual function tests
/------------------\
```

### Foundry Test Structure

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/GovernanceToken.sol";

contract GovernanceTokenTest is Test {
    GovernanceToken token;
    address owner = address(1);
    address alice = address(2);
    address bob = address(3);

    function setUp() public {
        vm.prank(owner);
        token = new GovernanceToken("GovToken", "GOV", 1000 ether);
    }

    function test_initial_supply() public view {
        assertEq(token.totalSupply(), 1000 ether);
        assertEq(token.balanceOf(owner), 1000 ether);
    }

    function test_transfer() public {
        vm.prank(owner);
        token.transfer(alice, 100 ether);
        assertEq(token.balanceOf(alice), 100 ether);
    }

    function testFuzz_transfer(uint256 amount) public {
        vm.assume(amount <= 1000 ether);
        vm.prank(owner);
        token.transfer(alice, amount);
        assertEq(token.balanceOf(alice), amount);
    }

    function test_invariant_supply() public view {
        assertEq(token.totalSupply(), 1000 ether);
    }
}
```

### CI/CD Pipeline

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: foundry-rs/foundry-toolchain@v1
      - run: forge test -vvv
      - run: forge coverage
      - run: slither .
```

## Versioning & Migration

### Semantic Versioning for Contracts

```
Major (X.0.0): Breaking storage layout changes, new proxy deployment
Minor (0.X.0): New functions, new features, storage-compatible
Patch (0.0.X): Bug fixes, gas optimizations (no storage changes)
```

### Upgrade Migration Checklist

- [ ] Storage layout compatibility verified
- [ ] No storage slot collisions with new variables
- [ ] New functions do not shadow inherited functions
- [ ] Initialize new state variables in upgrade initializer
- [ ] Test upgrade on fork of mainnet
- [ ] Multisig approval for upgrade transaction
- [ ] Rollback plan documented
- [ ] Post-upgrade verification script ready

## Glossary

| Term | Definition |
|------|-----------|
| ABI | Application Binary Interface — encoding for calling contract functions |
| CEI | Checks-Effects-Interactions pattern for reentrancy prevention |
| CREATE2 | Opcode for deterministic contract deployment addresses |
| Delegatecall | Executes code of another contract in caller's context |
| EIP | Ethereum Improvement Proposal — standard for Ethereum features |
| ERC | Ethereum Request for Comments — application-level standard |
| EVM | Ethereum Virtual Machine — runtime for smart contracts |
| Gas | Unit of computational cost on Ethereum |
| Immutable | Variable set once at deployment, stored in bytecode |
| Reentrancy | Attack where external call re-enters the calling function |
| Selector | First 4 bytes of keccak256 of function signature |
| Slippage | Difference between expected and actual swap output |
| Storage Slot | 32-byte unit of contract storage |
| Timelock | Delay mechanism for governance actions |
| UUPS | Universal Upgradeable Proxy Standard |

## Changelog

### 2.0.0 (2024-12-01)
- Added Diamond pattern (EIP-2535) support
- Added ERC-7201 namespaced storage patterns
- Updated Foundry integration to latest version
- Added Forge invariant testing templates

### 1.2.0 (2024-08-15)
- Added gas optimization benchmarking
- Added Slither and Mythril integration
- Improved deployment scripts for multi-network

### 1.1.0 (2024-05-20)
- Added UUPS proxy pattern support
- Added OpenZeppelin Defender integration
- Added The Graph subgraph templates

### 1.0.0 (2024-02-01)
- Initial release with ERC-20, ERC-721, ERC-1155 templates
- Basic security analysis
- Foundry and Hardhat test frameworks
- Etherscan verification support

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/your-org/smart-contract-development
cd smart-contract-development
pip install -e ".[dev]"
pre-commit install
```

### Code Style

- Follow Solidity style guide (https://docs.soliditylang.org/en/latest/style-guide.html)
- Use 4-space indentation in Python code
- All functions must have NatSpec documentation
- Run `forge fmt` before committing Solidity code
- Run `ruff check` before committing Python code

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all existing tests pass
4. Update documentation for new features
5. Request review from maintainers
6. Squash merge after approval

### Commit Messages

```
feat: add diamond proxy support
fix: resolve storage collision in upgradeable contract
docs: update gas optimization guide
test: add fuzz tests for ERC-20 transfer
```

## License

MIT License

Copyright (c) 2024 Smart Contract Development Contributors

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
