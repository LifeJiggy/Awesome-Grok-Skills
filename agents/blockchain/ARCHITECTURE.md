# Blockchain Agent Architecture

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Deep Dives](#component-deep-dives)
- [Data Flow](#data-flow)
- [Design Patterns](#design-patterns)
- [Technology Stack](#technology-stack)
- [Security Architecture](#security-architecture)
- [Scalability](#scalability)
- [Deployment](#deployment)
- [Monitoring](#monitoring)

---

## Overview

The Blockchain Agent is a comprehensive Web3 platform that provides smart contract management, tokenization, DeFi protocol interaction, NFT operations, DAO governance, and on-chain analytics. It abstracts blockchain complexity while providing enterprise-grade security and reliability.

### Core Capabilities

```
┌─────────────────────────────────────────────────────────────────┐
│                     Blockchain Agent                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │  Contract  │  │  Token    │  │   DeFi    │  │    NFT    │  │
│  │  Manager   │  │  Manager  │  │  Manager  │  │  Manager  │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │  Wallet   │  │   DAO     │  │  Web3     │  │  Security │  │
│  │  Manager  │  │  Manager  │  │ Analytics │  │  Auditor  │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Security First**: Every transaction is validated and audited
2. **Multi-Chain Support**: Abstract chain-specific complexity
3. **Gas Optimization**: Minimize transaction costs
4. **Compliance Ready**: Support for KYC/AML requirements
5. **Decentralization**: Minimize trusted intermediaries

---

## System Architecture

### High-Level Architecture

```
                           ┌──────────────────────┐
                           │     API Gateway       │
                           │    (Rate Limiting)    │
                           └──────────┬───────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
   ┌─────▼─────┐              ┌───────▼───────┐            ┌──────▼──────┐
   │  Contract  │              │   Token       │            │    DeFi     │
   │  Service   │              │   Service     │            │   Service   │
   └─────┬─────┘              └───────┬───────┘            └──────┬──────┘
         │                            │                            │
         └────────────────────────────┼────────────────────────────┘
                                      │
                           ┌──────────▼───────────┐
                           │   Blockchain Layer    │
                           │  (Multi-Chain Router) │
                           └──────────┬───────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
   ┌─────▼─────┐              ┌───────▼───────┐            ┌──────▼──────┐
   │  Ethereum  │              │    Polygon    │            │   Solana    │
   │  Mainnet   │              │    Mainnet    │            │   Mainnet   │
   └───────────┘              └───────────────┘            └─────────────┘
```

### Component Interaction Matrix

```
                    Contract  Token   DeFi    NFT    Wallet   DAO   Analytics
                    ────────  ─────   ────    ───    ──────   ───   ─────────
Contract Manager      ●         ●       ○      ○       ●      ○       ○
Token Manager         ●         ●       ●      ●       ●      ●       ●
DeFi Manager          ○         ●       ●      ○       ●      ○       ●
NFT Manager           ●         ●       ○      ●       ●      ○       ●
Wallet Manager        ●         ●       ●      ●       ●      ●       ●
DAO Manager           ○         ●       ○      ○       ●      ●       ○
Web3 Analytics        ○         ●       ●      ●       ○      ●       ●

● = Direct dependency    ○ = No dependency
```

---

## Component Deep Dives

### 1. Smart Contract Manager

Manages the lifecycle of smart contracts from deployment to deprecation.

```
┌─────────────────────────────────────────────────────────────────┐
│                   Smart Contract Manager                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Contract Lifecycle                       │   │
│  │                                                          │   │
│  │  Draft ──▶ Test ──▶ Audit ──▶ Deploy ──▶ Monitor       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Components                              │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │ Compiler │  │ Deployer │  │ Verifier │  │Auditor │ │   │
│  │  │  (Solc)  │  │ (Web3)   │  │ (Ethers) │  │(Slither)│ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Security Checks                         │   │
│  │                                                          │   │
│  │  • Static Analysis (Slither, Mythril)                    │   │
│  │  • Formal Verification (Certora)                         │   │
│  │  • Gas Optimization                                      │   │
│  │  • Access Control Validation                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Contract Security Checklist:**

| Check | Description | Severity |
|-------|-------------|----------|
| Reentrancy | No external calls before state updates | Critical |
| Integer Overflow | Use SafeMath or Solidity 0.8+ | High |
| Access Control | Proper modifiers on sensitive functions | High |
| Front-Running | Commit-reveal or slippage protection | Medium |
| Timestamp Dependence | Avoid block.timestamp for critical logic | Low |
| Denial of Service | Pull payment pattern for withdrawals | High |

### 2. Token Manager

Handles token creation, management, and tokenomics calculation.

```
┌─────────────────────────────────────────────────────────────────┐
│                       Token Manager                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Token Standards                         │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │  ERC20   │  │  ERC721  │  │ ERC1155  │  │ SPL    │ │   │
│  │  │  Fungible│  │ Non-Fung │  │ Multi    │  │ Solana  │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Token Features                          │   │
│  │                                                          │   │
│  │  • Mintable (controlled supply)                          │   │
│  │  • Burnable (deflationary)                               │   │
│  │  • Pausable (emergency stop)                             │   │
│  │  • Snapshot (balance history)                            │   │
│  │  • Vote (governance)                                     │   │
│  │  • Permit (gasless approvals)                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Tokenomics Engine                        │   │
│  │                                                          │   │
│  │  Distribution ──▶ Vesting ──▶ Emission ──▶ Utility      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Token Distribution Templates:**

| Template | Team | Investors | Public | Ecosystem | Treasury |
|----------|------|-----------|--------|-----------|----------|
| Startup | 20% | 25% | 15% | 25% | 15% |
| DAO | 10% | 10% | 20% | 40% | 20% |
| DeFi | 15% | 15% | 10% | 40% | 20% |
| NFT | 5% | 10% | 30% | 35% | 20% |

### 3. DeFi Protocol Manager

Manages interactions with decentralized finance protocols.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DeFi Protocol Manager                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Protocol Types                          │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │   DEX    │  │ Lending  │  │  Yield   │  │Bridge  │ │   │
│  │  │ (Uniswap)│  │ (Aave)   │  │ (Yearn)  │  │(Wormhole)│ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Position Management                     │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │  Create  │  │  Update  │  │  Close   │  │Harvest │ │   │
│  │  │ Position │  │ Position │  │ Position │  │Rewards │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Risk Assessment                         │   │
│  │                                                          │   │
│  │  • Smart Contract Risk                                   │   │
│  │  • Impermanent Loss Calculation                          │   │
│  │  • Oracle Risk                                           │   │
│  │  • Liquidity Risk                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4. NFT Manager

Manages NFT collections, minting, and marketplace operations.

```
┌─────────────────────────────────────────────────────────────────┐
│                       NFT Manager                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Collection Lifecycle                    │   │
│  │                                                          │   │
│  │  Create ──▶ Configure ──▶ Deploy ──▶ Mint ──▶ Trade    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Components                              │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │ Metadata │  │  Mint    │  │ Royalty  │  │Market  │ │   │
│  │  │  (IPFS)  │  │  Engine  │  │ Manager  │  │place   │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Features                                │   │
│  │                                                          │   │
│  │  • Batch Minting                                         │   │
│  │  • Metadata Updates                                      │   │
│  │  • Royalty Enforcement                                   │   │
│  │  • Reveal Mechanisms                                     │   │
│  │  • Allowlists                                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5. Wallet Manager

Manages wallets, signing, and transaction execution.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Wallet Manager                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Wallet Types                            │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │   Hot    │  │   Cold   │  │ Multi-Sig│  │  MPC   │ │   │
│  │  │ (MetaMask│  │ (Ledger) │  │(Gnosis)  │  │(Fireblocks)│ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Operations                              │   │
│  │                                                          │   │
│  │  • Balance Query                                         │   │
│  │  • Transaction Building                                  │   │
│  │  • Signature Management                                  │   │
│  │  • Nonce Management                                      │   │
│  │  • Gas Estimation                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6. DAO Manager

Manages decentralized autonomous organization governance.

```
┌─────────────────────────────────────────────────────────────────┐
│                       DAO Manager                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Governance Models                        │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │  Token   │  │Quadratic │  │Conviction│  │  Time  │ │   │
│  │  │ Weighted │  │ Voting   │  │ Voting   │  │Weighted│ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Proposal Lifecycle                      │   │
│  │                                                          │   │
│  │  Submit ──▶ Discussion ──▶ Voting ──▶ Execution ──▶Timelock│   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Treasury Management                     │   │
│  │                                                          │   │
│  │  • Multi-signature required                              │   │
│  │  • Spending limits                                       │   │
│  │  • Vesting schedules                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Transaction Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Transaction Flow                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Request                                                   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Step 1: Validation                                     │   │
│  │  • Check parameters                                     │   │
│  │  • Verify permissions                                   │   │
│  │  • Estimate gas                                         │   │
│  └───────────────────────────┬─────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Step 2: Preparation                                    │   │
│  │  • Build transaction                                    │   │
│  │  • Sign with wallet                                     │   │
│  │  • Add to pending pool                                  │   │
│  └───────────────────────────┬─────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Step 3: Submission                                     │   │
│  │  • Broadcast to network                                 │   │
│  │  • Monitor confirmation                                 │   │
│  │  • Handle replacements (speedup/cancel)                 │   │
│  └───────────────────────────┬─────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Step 4: Confirmation                                   │   │
│  │  • Update internal state                                │   │
│  │  • Emit events                                          │   │
│  │  • Notify user                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Contract Interaction Flow

```
                    ┌─────────────────┐
                    │  User Request   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Method Lookup  │
                    │  (ABI Decode)   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Parameter      │
                    │  Validation     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
       ┌───────────┐  ┌───────────┐  ┌───────────┐
       │   View    │  │   State   │  │  Events   │
       │  (Read)   │  │  (Write)  │  │  (Filter) │
       └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │   Response  │
                     │   Builder   │
                     └─────────────┘
```

---

## Design Patterns

### 1. Proxy Pattern (Upgradeable Contracts)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Proxy Pattern                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User ──▶ ┌─────────────┐                                      │
│           │   Proxy     │                                      │
│           │   Contract  │                                      │
│           └──────┬──────┘                                      │
│                  │                                              │
│                  ▼                                              │
│           ┌─────────────┐                                      │
│           │  Delegate   │                                      │
│           │  Call       │                                      │
│           └──────┬──────┘                                      │
│                  │                                              │
│                  ▼                                              │
│           ┌─────────────┐                                      │
│           │  Logic      │                                      │
│           │  Contract   │◀── Upgradeable                       │
│           └─────────────┘                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Factory Pattern (Token Creation)

```python
class TokenFactory:
    @staticmethod
    def create_erc20(params: TokenParams) -> Contract:
        # Deploy ERC20 implementation
        pass
    
    @staticmethod
    def create_erc721(params: NFTParams) -> Contract:
        # Deploy ERC721 implementation
        pass
    
    @staticmethod
    def create_erc1155(params: MultiTokenParams) -> Contract:
        # Deploy ERC1155 implementation
        pass
```

### 3. Observer Pattern (Event Monitoring)

```python
class EventMonitor:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event: str, callback: Callable):
        self.listeners[event].append(callback)
    
    def emit(self, event: str, data: Any):
        for callback in self.listeners[event]:
            callback(data)
```

### 4. Strategy Pattern (Multi-Chain)

```python
class ChainStrategy:
    def get_balance(self, address: str) -> float: ...
    def send_transaction(self, tx: Transaction) -> str: ...
    def estimate_gas(self, tx: Transaction) -> int: ...

class EthereumStrategy(ChainStrategy): ...
class PolygonStrategy(ChainStrategy): ...
class SolanaStrategy(ChainStrategy): ...
```

---

## Technology Stack

### Core Components

| Layer | Technology | Purpose |
|-------|-----------|---------|
| RPC | Web3.py / Ethers.js | Blockchain interaction |
| Contracts | Solidity / Rust | Smart contract development |
| Storage | IPFS / Arweave | Decentralized storage |
| Indexing | The Graph | On-chain data indexing |
| Signing | EIP-712 | Typed structured signing |

### Supported Chains

| Chain | Native Token | Block Time | Gas Model |
|-------|-------------|------------|-----------|
| Ethereum | ETH | 12s | EIP-1559 |
| Polygon | MATIC | 2s | Low gas |
| Arbitrum | ETH | 0.25s | L2 gas |
| Optimism | ETH | 2s | L2 gas |
| Solana | SOL | 0.4s | Compute units |
| Avalanche | AVAX | 2s | Gas |
| Base | ETH | 2s | L2 gas |

---

## Security Architecture

### Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Layer 1: Input Validation                               │   │
│  │  • Parameter type checking                               │   │
│  │  • Range validation                                      │   │
│  │  • Address checksum verification                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Layer 2: Access Control                                 │   │
│  │  • Role-based permissions                                │   │
│  │  • Multi-signature requirements                          │   │
│  │  • Time-locked operations                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Layer 3: Transaction Security                           │   │
│  │  • Gas estimation and limits                             │   │
│  │  • Nonce management                                      │   │
│  │  • Replay protection                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Layer 4: Monitoring                                     │   │
│  │  • Transaction monitoring                                │   │
│  │  • Anomaly detection                                     │   │
│  │  • Alert system                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Private Key Management

| Method | Security | Use Case |
|--------|----------|----------|
| Environment Variable | Basic | Development |
| AWS KMS | High | Production |
| HashiCorp Vault | High | Enterprise |
| MPC | Very High | Institutional |
| Hardware Wallet | Very High | Cold storage |

---

## Scalability

### Multi-Chain Architecture

```
                    ┌─────────────────┐
                    │   API Gateway   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Chain Router   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
  ┌─────▼─────┐       ┌─────▼─────┐       ┌─────▼─────┐
  │  Ethereum  │       │  Polygon  │       │  Solana   │
  │  Adapter   │       │  Adapter  │       │  Adapter  │
  └─────┬─────┘       └─────┬─────┘       └─────┬─────┘
        │                    │                    │
        ▼                    ▼                    ▼
  ┌───────────┐       ┌───────────┐       ┌───────────┐
  │  Ethereum │       │  Polygon  │       │  Solana   │
  │  Network  │       │  Network  │       │  Network  │
  └───────────┘       └───────────┘       └───────────┘
```

### Performance Targets

| Metric | Target | Strategy |
|--------|--------|----------|
| Transaction Latency | < 5s | Multi-chain routing |
| Gas Optimization | 30% savings | Batch operations |
| Uptime | 99.9% | Redundant RPCs |
| Throughput | 1000 TPS | L2 + batching |

---

## Deployment

### Docker Deployment

```yaml
version: '3.8'
services:
  blockchain-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ETHEREUM_RPC_URL=${ETHEREUM_RPC_URL}
      - PRIVATE_KEY=${PRIVATE_KEY}
      - IPFS_API=${IPFS_API}
    volumes:
      - ./abis:/app/abis
      - ./contracts:/app/contracts
```

### Environment Variables

```bash
# Blockchain RPCs
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/xxx
POLYGON_RPC_URL=https://polygon-rpc.com
ARBITRUM_RPC_URL=https://arb1.arbitrum.io/rpc

# Private Keys (use KMS in production)
PRIVATE_KEY=0x...

# IPFS
IPFS_API=/ip4/127.0.0.1/tcp/5001

# The Graph
GRAPH_API_KEY=xxx
```

---

## Monitoring

### Key Metrics

```yaml
Transaction Metrics:
  - transactions_submitted
  - transactions_confirmed
  - transactions_failed
  - average_gas_used
  - gas_cost_usd

Contract Metrics:
  - contracts_deployed
  - contract_interactions
  - contract_errors

Network Metrics:
  - block_number
  - gas_price
  - network_congestion
```

### Alert Rules

| Alert | Condition | Severity |
|-------|-----------|----------|
| High Gas | gas_price > 100 gwei | Warning |
| Tx Failed | failure_rate > 5% | Critical |
| Contract Pause | pause_event detected | Critical |
| Balance Low | balance < threshold | Warning |
