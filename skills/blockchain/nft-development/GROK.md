---
name: "nft-development"
category: "blockchain"
version: "2.0.0"
tags: ["blockchain", "NFT", "ERC-721", "ERC-1155", "digital-assets"]
---

# NFT Development

## Overview

The NFT Development module provides comprehensive tools for creating, deploying, and managing Non-Fungible Tokens (NFTs) on Ethereum and EVM-compatible chains. It covers ERC-721 and ERC-1155 standards, metadata generation, IPFS pinning, royalty management, lazy minting, auction mechanics, and marketplace integration. The module includes smart contract templates, metadata schema validation, collection management, and on-chain provenance tracking.

This skill is essential for NFT artists and creators building collections, game developers implementing in-game assets, platform engineers building marketplaces, and smart contract developers implementing NFT standards.

## Core Capabilities

- **ERC-721 Implementation**: Full NFT standard with metadata, approvals, and transfer mechanisms
- **ERC-1155 Multi-token**: Semi-fungible tokens for game items, editions, and mixed collections
- **Metadata Management**: JSON metadata generation, IPFS/Arweave storage, on-chain metadata (SVG, base64)
- **Lazy Minting**: Gas-free minting where the buyer pays gas, deferred metadata reveal
- **Auction Mechanics**: English auction, Dutch auction, sealed-bid (Vickrey), reserve price management
- **Royalty Standards**: EIP-2981 royalty information, perpetual royalties, split payments
- **Collection Management**: Merkle tree allowlists, phased launches, whitelist verification, supply tracking
- **Marketplace Integration**: Order book, direct listing, offers, bulk operations, cross-chain bridges
- **Provenance Tracking**: On-chain ownership history, transfer events, burn tracking, attribute statistics

## Usage Examples

```python
from nft_development import (
    NFTCollection,
    MetadataGenerator,
    AuctionHouse,
    RoyaltyManager,
    LazyMinter,
)

# --- Create NFT Collection ---
collection = NFTCollection(
    name="Pixel Punks",
    symbol="PUNK",
    base_uri="ipfs://QmYourCID/",
    max_supply=10000,
    royalty_bps=500,  # 5%
)
print(f"Collection: {collection.name}")
print(f"Max supply: {collection.max_supply}")
print(f"Royalty: {collection.royalty_pct}%")

# --- Generate Metadata ---
gen = MetadataGenerator(collection)
metadata = gen.create_metadata(
    name="Pixel Punk #42",
    description="A unique pixel punk from the collection",
    attributes=[
        {"trait_type": "Background", "value": "Blue"},
        {"trait_type": "Eyes", "value": "Laser"},
        {"trait_type": "Mouth", "value": "Grin"},
        {"trait_type": "Rarity", "value": "Legendary"},
    ],
    image="ipfs://QmImageCID/42.png",
)
valid = gen.validate_metadata(metadata)
print(f"Metadata valid: {valid}")
print(f"Token URI: {gen.generate_token_uri(metadata)}")

# --- Lazy Minting (Gas-Free) ---
lazy = LazyMinter(collection)
voucher = lazy.create_voucher(
    token_id=42,
    metadata_uri="ipfs://QmMetadataCID/42.json",
    min_price=0.01,
    signer="0x1234...abcd",
)
print(f"Voucher created for token #{voucher.token_id}")
print(f"Signature: {voucher.signature[:20]}...")

# --- Auction ---
auction_house = AuctionHouse()
auction = auction_house.create_auction(
    token_id=42,
    collection=collection.address,
    start_price=0.1,
    reserve_price=1.0,
    duration_hours=24,
    seller="0x1234...abcd",
)
print(f"Auction #{auction.auction_id}")
print(f"Start: {auction.start_price} ETH")
print(f"Reserve: {auction.reserve_price} ETH")
print(f"Duration: {auction.duration_hours}h")

# --- Bid Management ---
bid = auction_house.place_bid(
    auction_id=auction.auction_id,
    bidder="0x5678...efgh",
    amount=0.5,
)
print(f"Bid placed: {bid.amount} ETH by {bid.bidder[:10]}...")

# --- Royalty Splits ---
royalty_mgr = RoyaltyManager()
splits = royalty_mgr.create_splits(
    total_royalty_bps=500,
    recipients=[
        {"address": "0xArtist...", "bps": 700},
        {"address": "0xPlatform...", "bps": 200},
        {"address": "0xTreasury...", "bps": 100},
    ],
)
print(f"Royalty splits: {splits}")

# --- Allowlist (Merkle Tree) ---
merkle = collection.create_merkle_allowlist(
    addresses=["0xAddr1...", "0xAddr2...", "0xAddr3..."],
    max_per_wallet=2,
)
print(f"Root: {merkle.root}")
print(f"Proof for addr1: {merkle.get_proof('0xAddr1...')}")
```

## Best Practices

- Use ERC-721A for gas-efficient batch minting (saves ~70% gas vs standard ERC-721)
- Store metadata on IPFS or Arweave — never rely on centralized servers for permanent metadata
- Use EIP-2981 for on-chain royalty declarations; markets that support it will honor your royalties
- Implement Merkle tree allowlists for fair launches — cheaper than on-chain storage of addresses
- Use lazy minting for collections where the creator wants zero upfront gas cost
- Set appropriate royalty percentages — 5-10% is standard; >10% discourages secondary trading
- Use a revealing mechanism (delayed metadata) to prevent sniping during mint
- Test all NFT contracts on testnets before mainnet; use OpenZeppelin's audited implementations
- Include `supportsInterface` for ERC-165 compliance — marketplaces check this
- For ERC-1155, batch mint and batch transfer to save gas on large collections

## Related Modules

- **smart-contract-development**: Solidity contract development for NFT logic
- **smart-contracts**: Security auditing of NFT smart contracts
- **defi**: DeFi compositability with NFT collateral and fractionalization
- **consensus-mechanisms**: Transaction finality for NFT transfers

## Advanced Configuration

### Metadata Storage Configuration

```python
from nft_development import StorageConfig

storage = StorageConfig(
    primary="ipfs",
    fallback="arweave",
    ipfs_gateway="https://ipfs.io/ipfs/",
    arweave_wallet="arweave-wallet.json",
    pin_service="pinata",
    pinata_api_key="YOUR_KEY",
    pinata_secret="YOUR_SECRET",
    encryption_enabled=False,
)
```

### Reveal Configuration

```python
from nft_development import RevealConfig

reveal = RevealConfig(
    reveal_type="delayed",          # delayed, manual, random
    reveal_delay_blocks=7200,       # ~24 hours on Ethereum
    placeholder_uri="ipfs://placeholder/",
    random_seed_block=18000000,
    batch_size=100,                 # tokens per reveal batch
)
```

### Collection Deployment Config

```python
from nft_development import CollectionConfig

config = CollectionConfig(
    name="Pixel Punks",
    symbol="PUNK",
    max_supply=10000,
    royalty_bps=500,
    chain_id=1,
    gas_limit=5000000,
    auto_verify=True,
    contract_uri="ipfs://contract-metadata/",
    consecutive_token_ids=True,
    start_token_id=1,
)
```

## Architecture Patterns

### NFT Collection Architecture

```
NFT Collection System:
├── Smart Contract Layer
│   ├── ERC-721A (gas-efficient minting)
│   ├── AccessControl (roles)
│   ├── Ownable (admin)
│   ├── Pausable (emergency)
│   └── ERC-2981 (royalties)
├── Metadata Layer
│   ├── On-chain metadata (SVG/base64)
│   ├── IPFS/Arweave (off-chain)
│   └── Delayed reveal mechanism
├── Minting Layer
│   ├── Public mint (Dutch/English auction)
│   ├── Allowlist (Merkle proof)
│   ├── Lazy minting (gas-free)
│   └── Presale stages
├── Marketplace Layer
│   ├── Direct listings
│   ├── Auctions (English/Dutch)
│   ├── Offers/bids
│   └── Cross-chain bridges
└── Analytics Layer
    ├── Ownership tracking
    ├── Transfer history
    ├── Floor price monitoring
    └── Rarity ranking
```

### Lazy Minting Architecture

```
Creator Side:
├── Create voucher (off-chain)
│   ├── Token ID
│   ├── Metadata URI
│   ├── Price
│   └── Signature
└── Share voucher with buyer

Buyer Side:
├── Submit voucher to contract
├── Pay mint price
├── Gas for minting paid by buyer
└── Token minted with creator's signature
```

### Dutch Auction Pattern

```
Price Curve:
├── Start Price: 2.0 ETH
├── Duration: 1000 blocks
├── Price Decrease: linear or step function
├── Reserve Price: 0.1 ETH
└── Mechanism:
    ├── Each bid must meet current price
    ├── Price decreases over time
    ├── First bid above current price wins
    └── No front-running protection
```

## Integration Guide

### IPFS/Pinata Integration

```python
from nft_development import IPFSPublisher

publisher = IPFSPublisher(
    pinata_api_key="YOUR_KEY",
    pinata_secret="YOUR_SECRET",
)

# Pin metadata JSON
metadata_hash = publisher.pin_json({
    "name": "Pixel Punk #42",
    "description": "Unique pixel punk",
    "image": "ipfs://QmImageHash/",
    "attributes": [
        {"trait_type": "Background", "value": "Blue"},
        {"trait_type": "Rarity", "value": "Legendary"},
    ],
})
print(f"Metadata CID: {metadata_hash}")

# Pin image file
image_hash = publisher.pin_file("path/to/image.png")
print(f"Image CID: {image_hash}")
```

### Marketplace Integration (OpenSea)

```solidity
// OpenSea Seaport compatible listing
interface ISeaport {
    function fulfillBasicOrder(
        BasicOrderParameters calldata params
    ) external payable returns (bool fulfilled);
}

// List NFT for sale
function listForSale(
    address token,
    uint256 tokenId,
    uint256 price,
    uint256 duration
) external;
```

### The Graph Subgraph

```yaml
# subgraph.yaml
dataSources:
  - kind: ethereum/contract
    name: PixelPunks
    network: mainnet
    source:
      address: "0x..."
      abi: PixelPunks
      startBlock: 18000000
    mapping:
      entities:
        - Token
        - TransferEvent
        - MintEvent
        - SaleEvent
```

### Cross-Chain Bridge Integration

```python
from nft_development import BridgeManager

bridge = BridgeManager(
    source_chain="ethereum",
    destination_chain="polygon",
    bridge_protocol="layerzero",
)

# Lock NFT on source chain
lock_tx = bridge.lock(
    contract="0x...",
    token_id=42,
    destination_address="0x...",
)
print(f"Lock tx: {lock_tx.tx_hash}")

# Mint wrapped NFT on destination
wrapped = bridge.get_wrapped_info(
    source_contract="0x...",
    source_token_id=42,
)
print(f"Wrapped contract: {wrapped.contract_address}")
```

## Performance Optimization

### Gas-Efficient Minting

| Technique | Gas per Mint | Description |
|-----------|-------------|-------------|
| ERC-721A | ~50,000 | Batch mint for identical NFTs |
| Merkle Allowlist | ~80,000 | Gas-efficient allowlist verification |
| Lazy Minting | ~0 (creator) | Buyer pays gas |
| Dutch Auction | ~60,000 | Variable pricing |
| Storage Optimization | ~30,000 | Packed metadata storage |

### Batch Operations

```solidity
// Batch mint (ERC-721A style)
function mintBatch(uint256 quantity) external payable {
    require(quantity <= maxPerWallet);
    require(totalMinted + quantity <= maxSupply);
    _safeMint(msg.sender, quantity);
}

// Batch transfer
function safeBatchTransferFrom(
    address from,
    address to,
    uint256[] calldata ids,
    uint256[] calldata amounts
) external;
```

### Metadata Caching

```python
from nft_development import MetadataCache

cache = MetadataCache(
    ttl_seconds=3600,
    max_size=10000,
    storage="redis",
)

# Cache metadata lookups
metadata = cache.get_or_fetch(
    token_id=42,
    fetch_fn=lambda: ipfs_client.get(f"ipfs://QmMetadata/42.json"),
)
```

## Security Considerations

### NFT Security Checklist

- [ ] ERC-165 `supportsInterface` implemented correctly
- [ ] Owner-only functions protected by AccessControl
- [ ] Pausable for emergency response
- [ ] Merkle proof verification is sound (no hash collision risk)
- [ ] Lazy minting signatures cannot be replayed
- [ ] Royalty amounts capped (max 10%)
- [ ] Token URI cannot be changed after reveal
- [ ] No reentrancy in mint or transfer functions
- [ ] Integer overflow protection (Solidity 0.8+)
- [ ] Metadata stored on decentralized storage (IPFS/Arweave)

### Common NFT Vulnerabilities

| Vulnerability | Description | Fix |
|---------------|-------------|-----|
| Signature Replay | Same voucher minted twice | Nonce tracking |
| Signature Front-Running | Miner sees and uses signature | Commit-reveal |
| Metadata Centralization | Server can change metadata | IPFS/Arweave |
| Royalty Bypass | Transfer outside marketplace | On-chain enforcement |
| Allowlist Bypass | Fake Merkle proofs | Cryptographic verification |

## Troubleshooting Guide

### Common Minting Issues

| Error | Cause | Solution |
|-------|-------|----------|
| INSUFFICIENT_ALLOWANCE | Not approved for marketplace | Call setApprovalForAll |
| ALREADY_MINTED | Token ID already exists | Check token ID range |
| MAX_SUPPLY_REACHED | Collection sold out | Wait for secondary market |
| INVALID_PROOF | Merkle proof failed | Verify address is in allowlist |
| PAYMENT_INSUFFICIENT | Wrong price sent | Check current mint price |

### IPFS/Pinata Issues

```
Issue: Metadata not loading
1. Check CID is correct
2. Verify Pinata pin status
3. Try different IPFS gateway
4. Check for pin expiration

Issue: Images not rendering
1. Verify image CID in metadata
2. Check content-type headers
3. Test direct IPFS link
4. Check for gateway rate limiting
```

### Gas Estimation

```bash
# Estimate mint gas
cast estimate 0xContract "mint(uint256)" 1 --rpc-url $ETH_RPC_URL

# Check current gas price
cast gas-price --rpc-url $ETH_RPC_URL

# Optimize gas limit
cast estimate 0xContract "mintBatch(uint256)" 10 --rpc-url $ETH_RPC_URL
```

## API Reference

### NFTCollection

```python
class NFTCollection:
    def __init__(
        name: str,
        symbol: str,
        base_uri: str,
        max_supply: int,
        royalty_bps: int = 500,
    ): ...
    
    def deploy(self, chain_id: int = 1) -> DeploymentResult:
        """Deploy collection contract."""
    
    def create_merkle_allowlist(
        addresses: list[str],
        max_per_wallet: int,
    ) -> MerkleTree:
        """Generate Merkle tree for allowlist."""
    
    def mint(
        to: str,
        quantity: int,
        price: float,
    ) -> MintResult:
        """Mint tokens to address."""
```

### MetadataGenerator

```python
class MetadataGenerator:
    def create_metadata(
        name: str,
        description: str,
        attributes: list[dict],
        image: str,
    ) -> dict:
        """Generate OpenSea-compatible metadata."""
    
    def validate_metadata(metadata: dict) -> bool:
        """Validate metadata against schema."""
    
    def generate_token_uri(metadata: dict) -> str:
        """Generate token URI from metadata."""
    
    def batch_generate(
        collection_config: dict,
        attribute_combinations: list[dict],
    ) -> list[dict]:
        """Batch generate metadata for collection."""
```

### AuctionHouse

```python
class AuctionHouse:
    def create_auction(
        token_id: int,
        collection: str,
        start_price: float,
        reserve_price: float,
        duration_hours: int,
        seller: str,
    ) -> Auction:
        """Create a new auction."""
    
    def place_bid(
        auction_id: str,
        bidder: str,
        amount: float,
    ) -> Bid:
        """Place a bid on an auction."""
    
    def settle_auction(auction_id: str) -> SettlementResult:
        """Settle completed auction."""
```

## Data Models

### NFTMetadata

```
NFTMetadata:
  name: str                    # Token name
  description: str             # Token description
  image: str                   # Image URI (IPFS/Arweave)
  animation_url: str           # Optional animation
  external_url: str            # External link
  attributes: list[Attribute]  # Traits
  background_color: str        # Hex color

Attribute:
  trait_type: str              # Trait category
  value: str | int | float    # Trait value
  display_type: str            # number, boost_number, date, etc.
```

### Auction

```
Auction:
  auction_id: str
  token_id: int
  collection: str
  seller: str
  start_price: float
  current_price: float
  reserve_price: float
  highest_bidder: str
  start_time: int              # Unix timestamp
  end_time: int
  status: str                  # active, ended, settled
  bid_count: int
```

### AllowlistEntry

```
AllowlistEntry:
  address: str
  max_quantity: int
  price: float
  merkle_proof: list[str]      # Proof bytes
  claimed: bool
  claim_quantity: int
```

## Deployment Guide

### Collection Deployment Steps

```
1. Generate metadata for all tokens
2. Pin metadata and images to IPFS
3. Deploy contract to testnet
4. Test minting (public + allowlist)
5. Test reveal mechanism
6. Deploy contract to mainnet
7. Verify on Etherscan
8. Set up metadata pinning service
9. Configure marketplace listings
10. Enable monitoring and alerts
```

### IPFS Setup

```bash
# Install IPFS Desktop or run IPFS daemon
ipfs init
ipfs daemon

# Pin files to Pinata
curl -X POST "https://api.pinata.cloud/pinning/pinFileToIPFS" \
  -H "pinata_api_key: YOUR_KEY" \
  -F "file=@metadata.json"
```

## Monitoring & Observability

### Collection Metrics

| Metric | Description | Alert |
|--------|-------------|-------|
| Mint Rate | Tokens minted per hour | >2x baseline |
| Floor Price | Lowest listing price | >20% drop |
| Volume | 24h trading volume | >50% change |
| Unique Holders | Number of unique owners | Concentration >10% |
| Metadata Requests | IPFS gateway hits | >1000/min |
| Gas Price | Current mint gas cost | >100 gwei |

## Testing Strategy

### Test Coverage

```
1. Unit Tests
   ├── Mint function (single, batch)
   ├── Transfer function (all variants)
   ├── Approval mechanics
   ├── Royalty calculation
   └── Allowlist verification

2. Integration Tests
   ├── IPFS metadata loading
   ├── Marketplace listing
   ├── Auction mechanics
   ├── Lazy minting flow
   └── Cross-chain bridge

3. Security Tests
   ├── Signature replay protection
   ├── Allowlist bypass attempts
   ├── Reentrancy in mint
   └── Integer overflow edge cases
```

## Versioning & Migration

### Contract Versioning

```
v1.0: Initial collection (ERC-721)
v1.1: Add ERC-2981 royalties
v2.0: Migration to ERC-721A for batch minting
v2.1: Add lazy minting support
v3.0: Cross-chain bridge integration
```

### Metadata Migration

```
1. Generate new metadata with updated fields
2. Pin new metadata to IPFS
3. Update base URI or token URI on contract
4. Verify all tokens resolve correctly
5. Update marketplace listings
```

## Glossary

| Term | Definition |
|------|-----------|
| ERC-721 | Non-Fungible Token standard |
| ERC-1155 | Multi-Token standard (semi-fungible) |
| ERC-2981 | NFT Royalty standard |
| ERC-721A | Gas-efficient batch minting standard |
| Lazy Minting | Creator-deferred gas cost minting |
| Dutch Auction | Price decreases over time auction |
| Merkle Tree | Cryptographic data structure for allowlists |
| IPFS | InterPlanetary File System — decentralized storage |
| Floor Price | Lowest price for collection on secondary market |
| Metadata | JSON describing NFT attributes and image |

## Changelog

### 2.0.0 (2024-12-01)
- Added ERC-721A batch minting support
- Added cross-chain bridge integration
- Added Dutch auction mechanics
- Improved IPFS pinning reliability

### 1.2.0 (2024-08-15)
- Added lazy minting (gas-free creator minting)
- Added Merkle tree allowlist generation
- Added metadata caching layer

### 1.1.0 (2024-05-20)
- Added ERC-2981 royalty support
- Added marketplace integration
- Added batch metadata generation

### 1.0.0 (2024-02-01)
- Initial release with ERC-721 and ERC-1155
- Basic metadata generation
- IPFS storage support

## Contributing Guidelines

### Adding New Token Standards

1. Implement the standard interface
2. Add test suite for all standard functions
3. Ensure ERC-165 compliance
4. Document gas costs vs alternatives
5. Submit PR with audit report

### Code Quality

- All contracts must pass Slither analysis
- Test coverage >95% line coverage
- Gas benchmarks for all functions
- NatSpec documentation on all public functions

## License

MIT License

Copyright (c) 2024 NFT Development Contributors

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
