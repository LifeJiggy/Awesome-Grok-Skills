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
