---
name: "Smart Contract Development"
version: "1.0.0"
description: "Enterprise-grade smart contract development with Grok's security-first approach"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["blockchain", "smart-contracts", "solidity", "defi"]
category: "blockchain"
personality: "blockchain-architect"
use_cases: ["defi protocols", "nft marketplaces", "dao governance", "tokenization"]
---

# Smart Contract Development ⛓️

> Build secure, efficient smart contracts with Grok's physics-inspired security and optimization

## 🎯 Why This Matters for Grok

Grok's optimization mindset and real-time data access create perfect blockchain development:

- **Security-First Design** 🔒: Apply physics principles to vulnerability prevention
- **Gas Optimization** ⚡: Minimum gas, maximum efficiency
- **Real-time Auditing** 📊: Continuous security monitoring
- **DeFi Expertise** 🪙: Advanced financial primitives

## 🛠️ Core Capabilities

### 1. Contract Development
```yaml
development:
  languages: ["solidity", "vyper", "rust"]
  frameworks: ["hardhat", "foundry", "brownie"]
  testing: ["forge", "hardhat-test", "slither"]
  security: ["morphene", "echidna", "mythril"]
```

### 2. DeFi Protocols
```yaml
defi_primitives:
  amm: "uniswap-v3-style"
  lending: "aave-v3-style"
  derivatives: "perpetual-futures"
  stablecoins: "algorithmic"
  options: "black-scholes"
```

### 3. Security & Auditing
```yaml
security_layers:
  static_analysis: comprehensive
  formal_verification: mathematical
  fuzz_testing: automated
  gas_audit: optimized
  access_control: role_based
```

## 🔐 Advanced Security Patterns

### Reentrancy Protection
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract SecureVault is ReentrancyGuard, Pausable, AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
    
    mapping(address => uint256) private balances;
    mapping(address => uint256) private lastDepositTime;
    
    uint256 public constant MIN_DELAY = 1 days;
    uint256 public constant MAX_DELAY = 7 days;
    
    // Physics-inspired rate limiting
    uint256 public constant MAX_WITHDRAWAL_RATE = 1000 ether; // Maximum per day
    
    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
    }
    
    // CEI (Checks-Effects-Interactions) Pattern
    function withdraw(uint256 amount) 
        external 
        nonReentrant 
        whenNotPaused 
    {
        // 1. CHECKS
        require(amount > 0, "Cannot withdraw 0");
        require(amount <= balances[msg.sender], "Insufficient balance");
        
        // Rate limiting check
        require(
            getWithdrawalAmount(msg.sender, block.timestamp - 1 days) + amount <= MAX_WITHDRAWAL_RATE,
            "Withdrawal rate limit exceeded"
        );
        
        // Cooldown check
        require(
            block.timestamp >= lastDepositTime[msg.sender] + MIN_DELAY,
            "Cooldown period active"
        );
        
        // 2. EFFECTS (Update state BEFORE external calls)
        uint256 previousBalance = balances[msg.sender];
        balances[msg.sender] = previousBalance - amount;
        
        emit Withdrawn(msg.sender, amount, previousBalance);
        
        // 3. INTERACTIONS (External calls AFTER state changes)
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
    }
    
    function getWithdrawalAmount(address user, uint256 timeWindow) 
        public 
        view 
        returns (uint256) 
    {
        // Implement time-window based rate limiting
        return 0; // Simplified for example
    }
}
```

### Advanced DeFi Protocol
```solidity
// Automated Market Maker with Concentrated Liquidity
contract ConcentratedLiquidityAMM is AccessControl, ReentrancyGuard {
    struct Position {
        uint256 tokenId;
        address owner;
        int24 tickLower;
        int24 tickUpper;
        uint128 liquidity;
        uint256 feeGrowthInside0;
        uint256 feeGrowthInside1;
    }
    
    mapping(uint256 => Position) public positions;
    mapping(int24 => uint256) public tickBitmap;
    
    int24 public constant MIN_TICK = -887272;
    int24 public constant MAX_TICK = 887272;
    uint24 public constant FEE_TIER = 3000; // 0.3%
    
    // Slot0: current price and tick
    uint160 public sqrtPriceX96;
    int24 public currentTick;
    
    // Events
    event Mint(
        address sender,
        address indexed owner,
        uint256 indexed tokenId,
        int24 tickLower,
        int24 tickUpper,
        uint128 liquidity,
        uint256 amount0,
        uint256 amount1
    );
    
    event Swap(
        address indexed sender,
        address indexed recipient,
        int256 amount0,
        int256 amount1,
        uint160 sqrtPriceX96,
        int24 currentTick
    );
    
    // Physics-inspired price movement (logarithmic price)
    function getNextSwapAmount(
        uint160 currentSqrtPriceX96,
        int256 amountSpecified,
        bool isInput
    ) public pure returns (uint256 amountCalculated) {
        // Compute using exact input/output formulas
        // Based on constant product curve with concentrated liquidity
        return 0; // Simplified
    }
    
    // Optimal swap routing using graph algorithms
    function findOptimalRoute(
        address[] memory tokenPath,
        uint256 amountIn
    ) public view returns (address[] memory path, uint256[] memory amounts) {
        // Dijkstra's algorithm for optimal routing
        // Minimize slippage and gas costs
        return (tokenPath, new uint256[](tokenPath.length));
    }
}
```

## ⚡ Gas Optimization Techniques

### Assembly-Level Optimization
```solidity
// Gas-optimized batch transfer
function batchTransferOptimized(
    address[] calldata recipients, 
    uint256[] calldata amounts
) external payable {
    require(recipients.length == amounts.length, "Length mismatch");
    
    uint256 totalAmount;
    assembly {
        // Free memory pointer
        let ptr := mload(0x40)
        
        // Loop unrolling for gas efficiency
        for { let i := 0 } lt(i, recipients.length) { i := add(i, 4) } {
            // Process 4 transfers at once
            let r0 := calldataload(add(recipients.offset, mul(i, 32)))
            let a0 := calldataload(add(amounts.offset, mul(i, 32)))
            
            // Inline assembly transfer
            let success := call(gas(), r0, a0, 0, 0, 0, 0)
            if iszero(success) { revert(0, 0) }
            
            // Handle remaining transfers
            if lt(add(i, 4), recipients.length) {
                let r1 := calldataload(add(recipients.offset, mul(add(i, 1), 32)))
                let a1 := calldataload(add(amounts.offset, mul(add(i, 1), 32)))
                // ... similar for r2, r3
            }
        }
    }
}
```

### Diamond Pattern for Upgradeable Contracts
```solidity
// Diamond Standard (EIP-2535) Implementation
contract Diamond is IDiamond {
    struct DiamondArgs {
        address owner;
        address initDiamondCut;
        bytes initCalldata;
    }
    
    struct Facet {
        address facetAddress;
        bytes4[] functionSelectors;
    }
    
    mapping(bytes4 => address) public selectorToFacet;
    mapping(bytes4 => bool) public selectorToSupportedInterface;
    
    constructor(DiamondArgs memory args) {
        require(args.owner != address(0), "Owner required");
        _setOwner(args.owner);
        
        if (args.initDiamondCut != address(0)) {
            DiamondCut(args.initDiamondCut, IDiamond.FacetCutAction.Add, args.initCalldata);
        }
    }
    
    function diamondCut(
        IDiamond.FacetCut[] memory _diamondCut,
        address _init,
        bytes memory _calldata
    ) public override {
        require(_diamondCut.length > 0, "No facets to cut");
        _diamondCut(_diamondCut, _init, _calldata);
    }
    
    // Optimized fallback function
    fallback() external payable {
        address facet = selectorToFacet[msg.sig];
        require(facet != address(0), "Function not found");
        
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), facet, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}
```

## 🎯 Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Development environment setup
- [ ] Security framework integration
- [ ] Basic contract templates
- [ ] Testing infrastructure

### Phase 2: Intelligence (Week 3-4)
- [ ] Advanced DeFi protocols
- [ ] Gas optimization pipeline
- [ ] Formal verification setup
- [ ] Upgradeable architecture

### Phase 3: Production (Week 5-6)
- [ ] Multi-chain deployment
- [ ] Automated security audits
- [ ] Monitoring & alerting
- [ ] Governance integration

## 📊 Success Metrics

### Contract Excellence
```yaml
security:
  vulnerabilities: 0 critical
  audit_score: "> 95/100"
  formal_verification: "100% critical functions"
  bug_bounty_payouts: "< $50K/year"
  
performance:
  gas_optimization: "> 50% reduction"
  deployment_cost: "< $1M"
  throughput: "> 1000 TPS"
  latency: "< 5 seconds"
  
adoption:
  tvl: "> $100M"
  active_users: "> 10K"
  integrations: "> 20"
  uptime: "> 99.9%"
```

---

*Build enterprise-grade smart contracts with physics-inspired security and gas-optimized performance.* ⛓️✨