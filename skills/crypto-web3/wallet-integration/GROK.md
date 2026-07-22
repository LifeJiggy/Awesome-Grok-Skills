---
name: "wallet-integration"
category: "crypto-web3"
version: "2.0.0"
tags: ["crypto-web3", "wallet", "web3", "connection", "signing"]
---

# Wallet Integration

## Overview

The Wallet Integration module provides tools and patterns for connecting, authenticating, and interacting with cryptocurrency wallets in Web3 applications. It covers wallet connection protocols, message signing, transaction construction, multi-chain support, and wallet abstraction patterns.

This skill is essential for Web3 frontend developers, dApp engineers, and wallet SDK builders.

## Core Capabilities

- **Wallet Connection**: MetaMask, WalletConnect, Coinbase Wallet, and mobile wallet deep linking
- **Authentication**: SIWE (Sign-In with Ethereum) and message-based authentication
- **Transaction Construction**: Building, signing, and sending transactions with proper gas estimation
- **Multi-Chain**: Chain switching, multi-chain state management, and cross-chain bridging
- **Account Management**: Address derivation, ENS resolution, and account switching
- **Security**: Transaction simulation, risk scoring, and phishing protection
- **Wallet Abstraction**: Smart accounts, social login, and gasless transactions

## Usage Examples

```python
from wallet_integration import (
    WalletConnector,
    TransactionBuilder,
    SIWEAuth,
    ChainManager,
    SecurityChecker,
)

# --- Wallet Connection ---
connector = WalletConnector()
wallet = connector.connect(wallet_type="metamask")
print(f"Connected: {wallet.address}")
print(f"Chain: {wallet.chain_id}")
print(f"Balance: {wallet.balance_eth} ETH")

# --- Transaction Building ---
builder = TransactionBuilder(chain_id=1)
tx = builder.build_transfer(
    from_address="0x1234...",
    to_address="0xABCD...",
    value_eth=0.1,
    gas_price_gwei=20,
    nonce=42,
)
print(f"Transaction: {tx.tx_hash}")
print(f"Gas estimate: {tx.gas_estimate}")
print(f"Max fee: {tx.max_fee_eth} ETH")

# --- SIWE Authentication ---
siwe = SIWEAuth()
message = siwe.create_message(
    address="0x1234...",
    domain="app.example.com",
    uri="https://app.example.com",
    chain_id=1,
    statement="Sign in to access your account",
)
print(f"SIWE message:\n{message}")

# --- Chain Management ---
chains = ChainManager()
supported = chains.get_supported_chains()
print(f"Supported chains: {[c['name'] for c in supported]}")
chain = chains.switch_chain(chain_id=137)
print(f"Switched to: {chain['name']}")

# --- Security ---
security = SecurityChecker()
risk = security.check_address("0x1234...")
print(f"Address risk: {risk.risk_level}")
print(f"Is contract: {risk.is_contract}")
```

## Best Practices

- Always verify the connected address matches what the user expects
- Use SIWE for authentication — never use raw message signing for auth
- Simulate transactions before sending to detect potential reverts
- Show clear transaction details (recipient, value, gas) before signing
- Handle chain switching gracefully — prompt user when wrong chain
- Use WalletConnect v2 for mobile wallet support
- Implement account switching support — users may have multiple accounts
- Store minimal wallet state locally — derive from connected address
- Use ENS for human-readable addresses in UI
- Never request unlimited token approvals — request exact amounts

## Related Modules

- **defi-patterns**: DeFi transaction patterns
- **nft-marketplace**: NFT marketplace wallet interactions
- **token-analytics**: Wallet-based token analysis
- **dao-governance**: Wallet-based governance voting

---

## Advanced Configuration

### Multi-Chain Configuration

Configure multiple blockchain networks.

```python
chain_config = ChainConfig(
    chains={
        1: {"name": "Ethereum", "rpc": "https://eth-mainnet.alchemyapi.io/v2/...", "explorer": "etherscan.io"},
        137: {"name": "Polygon", "rpc": "https://polygon-rpc.com", "explorer": "polygonscan.com"},
        42161: {"name": "Arbitrum", "rpc": "https://arb1.arbitrum.io/rpc", "explorer": "arbiscan.io"},
    },
    default_chain=1,
    fallback_chain=1,
)
```

### Wallet Provider Configuration

Configure wallet connection providers.

```python
wallet_providers = WalletProviderConfig(
    providers={
        "metamask": {"injected": True, "qr_code": False},
        "walletconnect": {"project_id": "...", "chains": [1, 137, 42161]},
        "coinbase": {"app_name": "MyApp", "app_logo_url": "https://..."},
        "phantom": {"solana": True, "ethereum": False},
    },
    auto_connect=True,
    remember_last=True,
)
```

### Transaction Configuration

Configure transaction parameters.

```python
tx_config = TransactionConfig(
    gas_settings={
        "speeds": {
            "slow": {"multiplier": 1.0, "max_fee": 50},
            "normal": {"multiplier": 1.2, "max_fee": 100},
            "fast": {"multiplier": 1.5, "max_fee": 200},
        },
        "default_speed": "normal",
    },
    slippage_settings={
        "default": 0.005,  # 0.5%
        "volatile_pairs": 0.03,  # 3%
    },
    confirmation_blocks=1,
)
```

---

## Architecture Patterns

### Wallet State Management

```python
class WalletStateManager:
    def __init__(self):
        self.state = {
            "connected": False,
            "address": None,
            "chain_id": None,
            "balance": None,
        }

    def connect(self, provider):
        address = provider.request("eth_requestAccounts")
        chain_id = provider.request("eth_chainId")
        self.state.update({
            "connected": True,
            "address": address,
            "chain_id": chain_id,
        })
```

### Transaction Queue Pattern

```python
class TransactionQueue:
    def __init__(self):
        self.queue = []
        self.pending = {}

    def add(self, tx):
        self.queue.append(tx)

    def process_next(self):
        if self.queue:
            tx = self.queue.pop(0)
            self.execute(tx)
```

### Wallet Abstraction Pattern

```python
class WalletAbstraction:
    def __init__(self):
        self.adapters = {
            "eoa": EOAAdapter(),
            "smart": SmartAccountAdapter(),
            "multisig": MultisigAdapter(),
        }

    def get_adapter(self, wallet_type):
        return self.adapters[wallet_type]
```

---

## Integration Guide

### wagmi Integration

```javascript
import { useConnect, useAccount, useBalance } from 'wagmi';

function WalletButton() {
  const { connect, connectors } = useConnect();
  const { address, isConnected } = useAccount();
  const { data: balance } = useBalance({ address });

  return isConnected ? (
    <div>{address} - {balance?.formatted} ETH</div>
  ) : (
    <button onClick={() => connect(connectors[0])}>Connect</button>
  );
}
```

### ethers.js Integration

```javascript
import { ethers } from 'ethers';

async function connectWallet() {
  if (window.ethereum) {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner();
    const address = await signer.getAddress();
    return { provider, signer, address };
  }
}
```

---

## Performance Optimization

### Connection Caching

```python
# Cache wallet connections
connection_cache = ConnectionCache(
    ttl_seconds=3600,
    max_entries=100,
)
```

### Batch Balance Queries

```python
# Query multiple token balances at once
async def batch_balances(address, tokens):
    provider = get_provider()
    multicall = MulticallContract(provider)
    return await multicall.get_balances(address, tokens)
```

---

## Security Considerations

### Transaction Simulation

```python
# Simulate transactions before sending
async def safe_send_transaction(tx):
    simulation = await simulate_transaction(tx)
    if simulation.success:
        return await send_transaction(tx)
    else:
        raise TransactionReverted(simulation.error)
```

### Phishing Protection

```python
# Check addresses against known phishing lists
class PhishingChecker:
    def __init__(self):
        self.blocked_addresses = load_blocked_list()

    def check(self, address):
        return address.lower() not in self.blocked_addresses
```

### Approval Limits

```python
# Request specific approval amounts, not unlimited
def approve_token(token, spender, amount):
    return token.approve(spender, amount)  # Not MAX_UINT256
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Wallet not connecting | Wrong chain | Prompt chain switch |
| Transaction stuck | Low gas | Speed up with higher gas |
| Wrong network | User on wrong chain | Auto-switch or prompt |
| Signature rejected | User denied | Explain what's needed |

---

## API Reference

### WalletConnector

```python
class WalletConnector:
    def connect(wallet_type: str) -> Wallet
    def disconnect() -> None
    def get_connected() -> Optional[Wallet]
    def list_available() -> List[WalletProvider]
```

### TransactionBuilder

```python
class TransactionBuilder:
    def build_transfer(from, to, value, chain_id) -> Transaction
    def build_contract_call(contract, method, args, chain_id) -> Transaction
    def estimate_gas(tx) -> int
    def simulate(tx) -> SimulationResult
```

### SIWEAuth

```python
class SIWEAuth:
    def create_message(address, domain, uri, chain_id, statement) -> str
    def verify_message(message, signature) -> bool
    def create_session(address, chain_id) -> Session
```

---

## Data Models

### Wallet

```python
@dataclass
class Wallet:
    address: str
    chain_id: int
    balance_eth: float
    provider: str
    connected_at: datetime
```

### Transaction

```python
@dataclass
class Transaction:
    from_address: str
    to_address: str
    value: int
    chain_id: int
    gas_estimate: int
    max_fee: int
    nonce: int
    data: bytes
```

---

## Deployment Guide

### Frontend Deployment

```yaml
# Vercel deployment
env:
  NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID: ${{ secrets.WALLETCONNECT_PROJECT_ID }}
  NEXT_PUBLIC_ALCHEMY_ID: ${{ secrets.ALCHEMY_ID }}
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `wallet.connect.success` | Successful connections | < 0.9 |
| `wallet.tx.success` | Transaction success rate | < 0.95 |
| `wallet.tx.gas_used` | Gas used per tx | Anomaly |

---

## Testing Strategy

### Wallet Tests

```python
def test_wallet_connection():
    connector = WalletConnector()
    wallet = connector.connect("metamask")
    assert wallet.address.startswith("0x")
    assert wallet.chain_id == 1
```

---

## Versioning & Migration

### SDK Versioning

Follow semantic versioning for wallet SDKs.

---

## Glossary

| Term | Definition |
|------|-----------|
| **SIWE** | Sign-In with Ethereum |
| **EOA** | Externally Owned Account |
| **Smart Account** | Contract-based account with advanced features |
| **Multisig** | Multi-signature wallet |
| **Gas** | Transaction execution fee |

---

## Changelog

### v2.0.0
- Added SIWE authentication
- Multi-chain support
- Wallet abstraction

### v1.0.0
- Initial release with MetaMask support

---

## Contributing Guidelines

- Test on multiple chains
- Handle edge cases (wrong network, low balance)
- Document wallet-specific behaviors

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

## Advanced Configuration

### Wallet Configuration

```yaml
wallets:
  metamask:
    chain_ids: [1, 137, 42161, 10, 8453]
    rpc_urls:
      1: "https://mainnet.infura.io/v3/${INFURA_KEY}"
      137: "https://polygon-rpc.com"
      42161: "https://arb1.arbitrum.io/rpc"
    fallback_rpc: "https://cloudflare-eth.com"
  walletconnect:
    project_id: "${WALLETCONNECT_PROJECT_ID}"
    relay_url: "wss://relay.walletconnect.com"
    metadata:
      name: "My dApp"
      description: "Description"
      url: "https://mydapp.com"
      icons: ["https://mydapp.com/icon.png"]
  coinbase:
    app_id: "${COINBASE_APP_ID}"
    dark_mode: true
  safe:
    tx_service_url: "https://safe-transaction.safe.global"
```

### Authentication Configuration

```yaml
siwe:
  domain: "mydapp.com"
  uri: "https://mydapp.com"
  statement: "Sign in to My dApp"
  chain_id: 1
  expiration_hours: 24
  nonce_length: 16
  resources:
    - "https://api.mydapp.com/v1/"
```

## Architecture Patterns

### Wallet Connection Architecture

```
Connection Stack:
├── Frontend SDK
│   ├── Wallet modal
│   ├── Chain selector
│   ├── Account display
│   └── Connection state
├── Provider Layer
│   ├── EIP-1193 provider
│   ├── Multi-chain provider
│   ├── Fallback providers
│   └── Provider events
├── Wallet Adapters
│   ├── MetaMask (injected)
│   ├── WalletConnect (remote)
│   ├── Coinbase (SDK)
│   ├── Safe (multisig)
│   └── Custom wallets
├── State Management
│   ├── Connection state
│   ├── Chain state
│   ├── Account state
│   └── Balance state
└── Event System
    ├── accountsChanged
    ├── chainChanged
    ├── connect
    ├── disconnect
    └── message
```

### SIWE Authentication Architecture

```
SIWE Flow:
├── Client Side
│   ├── Generate nonce
│   ├── Create SIWE message
│   ├── Request signature
│   └── Send to server
├── Server Side
│   ├── Verify signature
│   ├── Validate nonce
│   ├── Check expiration
│   └── Issue session
├── Session Management
│   ├── JWT token
│   ├── Session store
│   ├── Token refresh
│   └── Logout handling
└── Security
    ├── CSRF protection
    ├── Replay protection
    ├── Origin validation
    └── Rate limiting
```

### Transaction Building Architecture

```
Transaction Flow:
├── Build
│   ├── Construct calldata
│   ├── Estimate gas
│   ├── Set gas price
│   └── Add nonce
├── Sign
│   ├── EIP-1559 support
│   ├── EIP-2930 support
│   ├── Legacy transactions
│   └── Hardware wallet
├── Send
│   ├── Broadcast to network
│   ├── Handle replacement
│   ├── Track confirmation
│   └── Handle reorg
└── Monitor
    ├── Transaction status
    ├── Event logs
    ├── Receipt handling
    └── Error recovery
```

### Multi-Chain Architecture

```
Multi-Chain Management:
├── Chain Registry
│   ├── Chain metadata
│   ├── RPC endpoints
│   ├── Block explorers
│   └── Token lists
├── Chain Switching
│   ├── Request switch
│   ├── Auto-add chain
│   ├── Handle errors
│   └── Fallback chains
├── Cross-Chain
│   ├── Bridge detection
│   ├── Bridge quotes
│   ├── Bridge execution
│   └── Status tracking
└── State Sync
    ├── Balance aggregation
    ├── Position tracking
    ├── History merging
    └── Unified display
```

## Integration Guide

### wagmi/ethers.js Integration

```typescript
import { createConfig, http, useConnect, useAccount, useBalance, useSendTransaction } from 'wagmi'
import { mainnet, polygon, arbitrum, optimism, base } from 'wagmi/chains'
import { metaMask, walletConnect, coinbaseWallet } from 'wagmi/connectors'

const config = createConfig({
  chains: [mainnet, polygon, arbitrum, optimism, base],
  connectors: [
    metaMask(),
    walletConnect({ projectId: process.env.WALLETCONNECT_PROJECT_ID }),
    coinbaseWallet({ appName: 'My dApp' })
  ],
  transports: {
    [mainnet.id]: http(`https://mainnet.infura.io/v3/${process.env.INFURA_KEY}`),
    [polygon.id]: http('https://polygon-rpc.com'),
    [arbitrum.id]: http('https://arb1.arbitrum.io/rpc'),
  }
})

function ConnectButton() {
  const { connect, connectors } = useConnect()
  const { address, isConnected } = useAccount()
  const { data: balance } = useBalance({ address })

  if (isConnected) {
    return (
      <div>
        <p>Connected: {address}</p>
        <p>Balance: {balance?.formatted} {balance?.symbol}</p>
      </div>
    )
  }

  return (
    <div>
      {connectors.map((connector) => (
        <button key={connector.id} onClick={() => connect({ connector })}>
          {connector.name}
        </button>
      ))}
    </div>
  )
}
```

### SIWE Integration

```python
from siwe import SiweMessage
import time
import secrets

class SIWEAuth:
    def __init__(self, domain, origin):
        self.domain = domain
        self.origin = origin
        self.nonces = {}  # In production, use Redis

    def generate_nonce(self, address):
        """Generate and store nonce for address."""
        nonce = secrets.token_hex(16)
        self.nonces[address.lower()] = {
            "nonce": nonce,
            "created_at": time.time(),
            "expires_at": time.time() + 300  # 5 minutes
        }
        return nonce

    def create_message(self, address, chain_id, nonce):
        """Create SIWE message."""
        message = SiweMessage(
            domain=self.domain,
            address=address,
            statement="Sign in to My dApp",
            uri=self.origin,
            version="1",
            chain_id=chain_id,
            nonce=nonce,
            issued_at=datetime.utcnow().isoformat(),
            expiration_time=(datetime.utcnow() + timedelta(hours=24)).isoformat(),
            resources=[f"https://api.{self.domain}/v1/"]
        )
        return message.prepare_message()

    def verify_signature(self, message, signature, address):
        """Verify SIWE signature."""
        siwe_message = SiweMessage(message)

        # Validate
        assert siwe_message.verify({"signature": signature}) == True
        assert siwe_message.domain == self.domain
        assert siwe_message.address.lower() == address.lower()
        assert siwe_message.nonce in self.nonces.get(address.lower(), {})
        assert siwe_message.expiration_time > datetime.utcnow()

        # Invalidate nonce
        del self.nonces[address.lower()]

        return True
```

### Transaction Builder

```python
from web3 import Web3
from eth_account import Account

class TransactionBuilder:
    def __init__(self, w3, chain_id):
        self.w3 = w3
        self.chain_id = chain_id

    def build_transfer(self, from_addr, to_addr, value_eth, token_address=None):
        """Build transfer transaction."""
        if token_address:
            # ERC-20 transfer
            return self.build_erc20_transfer(token_address, to_addr, value_eth)
        else:
            # Native ETH transfer
            return {
                "from": from_addr,
                "to": to_addr,
                "value": self.w3.to_wei(value_eth, "ether"),
                "gas": 21000,
                "nonce": self.w3.eth.get_transaction_count(from_addr),
                "chainId": self.chain_id,
                "type": 2,  # EIP-1559
                "maxFeePerGas": self.w3.eth.gas_price * 2,
                "maxPriorityFeePerGas": self.w3.to_wei(1, "gwei")
            }

    def build_erc20_transfer(self, token_address, to_addr, amount):
        """Build ERC-20 transfer transaction."""
        token = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=self.get_erc20_abi()
        )
        decimals = token.functions.decimals().call()
        amount_wei = int(amount * (10 ** decimals))

        return token.functions.transfer(
            Web3.to_checksum_address(to_addr),
            amount_wei
        ).build_transaction({
            "from": Web3.to_checksum_address(from_addr),
            "gas": 100000,
            "nonce": self.w3.eth.get_transaction_count(from_addr),
            "chainId": self.chain_id,
            "type": 2
        })

    def estimate_gas(self, tx):
        """Estimate gas for transaction."""
        try:
            gas_estimate = self.w3.eth.estimate_gas(tx)
            return int(gas_estimate * 1.2)  # 20% buffer
        except Exception as e:
            raise ValueError(f"Gas estimation failed: {e}")
```

### WalletConnect Integration

```typescript
import SignClient from '@walletconnect/sign-client'
import { Web3Wallet } from '@walletconnect/web3wallet'

class WalletConnectManager {
  private signClient: SignClient
  private web3Wallet: Web3Wallet

  async init() {
    this.signClient = await SignClient.init({
      projectId: process.env.WALLETCONNECT_PROJECT_ID,
      metadata: {
        name: 'My dApp',
        description: 'Description',
        url: 'https://mydapp.com',
        icons: ['https://mydapp.com/icon.png']
      }
    })

    this.web3Wallet = await Web3Wallet.init({
      core: this.signClient.core,
      metadata: {
        name: 'My dApp',
        description: 'Description',
        url: 'https://mydapp.com',
        icons: ['https://mydapp.com/icon.png']
      }
    })
  }

  async connect() {
    const { uri, approval } = await this.signClient.connect({
      requiredNamespaces: {
        eip155: {
          methods: ['eth_sendTransaction', 'personal_sign'],
          chains: ['eip155:1', 'eip155:137'],
          events: ['chainChanged', 'accountsChanged']
        }
      }
    })

    // Display QR code with uri
    return { uri, approval }
  }

  async sendTransaction(topic, transaction) {
    return await this.web3Wallet.request({
      topic,
      chainId: 'eip155:1',
      request: {
        method: 'eth_sendTransaction',
        params: [transaction]
      }
    })
  }
}
```

## Performance Optimization

### Connection Optimization

| Technique | Description | Impact |
|-----------|-------------|--------|
| Lazy loading | Load wallet SDK on demand | Faster initial load |
| Caching | Cache connection state | Faster reconnect |
| Preloading | Pre-connect on hover | Instant connection |
| Fallback | Multiple RPC providers | Better reliability |

### State Management

```
State Optimization:
├── Connection State
│   ├── Debounce events
│   ├── Batch updates
│   └── Optimistic updates
├── Balance State
│   ├── Polling interval
│   ├── Event-driven updates
│   └── Cache invalidation
├── Chain State
│   ├── Lazy chain loading
│   ├── Chain metadata cache
│   └── RPC response cache
└── Transaction State
    ├── Pending queue
    ├── Confirmation tracking
    └── History cache
```

## Security Considerations

### Wallet Security

| Threat | Description | Mitigation |
|--------|-------------|------------|
| Phishing | Fake wallet sites | Domain verification |
| Malicious transactions | Draining approvals | Transaction simulation |
| Key theft | Private key exposure | Hardware wallet support |
| Replay attacks | Reuse signatures | Nonce, chain ID, expiration |
| Front-running | MEV attacks | Private mempool, Flashbots |

### Transaction Simulation

```python
class TransactionSimulator:
    def __init__(self, w3):
        self.w3 = w3

    def simulate_transaction(self, tx):
        """Simulate transaction before signing."""
        try:
            # Estimate gas
            gas_estimate = self.w3.eth.estimate_gas(tx)

            # Simulate state change
            result = self.w3.eth.call(tx)

            # Check for reverts
            if result.hex() == '0x':
                return {"success": True, "gas_estimate": gas_estimate}
            else:
                return {"success": False, "error": "Revert data: " + result.hex()}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_token_approval(self, owner, spender, token_address):
        """Check current token approval."""
        token = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=self.get_erc20_abi()
        )
        allowance = token.functions.allowance(
            Web3.to_checksum_address(owner),
            Web3.to_checksum_address(spender)
        ).call()
        return allowance
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Wrong network | Transaction fails | Prompt chain switch |
| Insufficient balance | Cannot send transaction | Show balance, suggest bridge |
| Nonce too low | Transaction dropped | Get current nonce, resubmit |
| Gas too low | Transaction stuck | Replace with higher gas |
| User rejected | Signature rejected | Handle gracefully, show error |

### Debugging Commands

```bash
# Check account balance
cast balance $ADDRESS --rpc-url $RPC

# Check nonce
cast nonce $ADDRESS --rpc-url $RPC

# Check gas price
cast gas-price --rpc-url $RPC

# Simulate transaction
cast call --from $FROM $CONTRACT $FUNC_SIG $ARGS --rpc-url $RPC

# Check token balance
cast call $TOKEN "balanceOf(address)" $ADDRESS --rpc-url $RPC
```

## Testing Strategy

### Wallet Integration Testing

```
1. Unit Tests
   ├── Connection logic
   ├── SIWE message creation
   ├── Transaction building
   └── State management

2. Integration Tests
   ├── Wallet connection flow
   ├── Transaction signing
   ├── Chain switching
   └── Error handling

3. E2E Tests
   ├── Full connection flow
   ├── Transaction submission
   ├── Multi-wallet support
   └── Mobile wallet testing

4. Security Tests
   ├── Phishing protection
   ├── Transaction simulation
   ├── Nonce validation
   └── Replay protection
```

## Versioning & Migration

### Versioning

```
Major: Provider changes
├── Example: wagmi v1 → v2
├── Requires: Migration guide
└── Risk: High

Minor: New wallet support
├── Example: Add Safe wallet
├── Requires: Testing
└── Risk: Low

Patch: Bug fixes
├── Example: Fix connection state
├── Requires: Basic testing
└── Risk: Very low
```

## Glossary

| Term | Definition |
|------|-----------|
| EIP-1193 | Ethereum Provider JavaScript API |
| EIP-1559 | Fee market transaction |
| EIP-2930 | Access list transaction |
| SIWE | Sign-In with Ethereum |
| WalletConnect | Remote wallet connection protocol |
| dApp Browser | Wallet with built-in browser |
| Hardware Wallet | Physical device for key storage |
| Hot Wallet | Software wallet connected to internet |
| Cold Wallet | Offline wallet for storage |
| MPC | Multi-Party Computation wallet |

## Changelog

### v2.0.0
- Added SIWE authentication
- Multi-chain support
- Wallet abstraction

### v1.0.0
- Initial release with MetaMask support
