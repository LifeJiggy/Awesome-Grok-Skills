---
name: "nft-marketplace"
category: "crypto-web3"
version: "2.0.0"
tags: ["crypto-web3", "NFT", "marketplace", "ERC-721", "trading"]
---

# NFT Marketplace

## Overview

The NFT Marketplace module provides tools and patterns for building NFT trading platforms, including listing management, auction mechanics, royalty enforcement, collection analytics, and marketplace protocol design. It covers both on-chain and off-chain marketplace architecture.

This skill is essential for Web3 developers building NFT marketplaces, marketplace protocol architects, and NFT platform product teams.

## Core Capabilities

- **Listing Management**: Fixed-price listings, auction listings, and listing validation
- **Auction Mechanics**: English auctions, Dutch auctions, sealed-bid, and reserve price management
- **Order Matching**: Order book management, trade settlement, and slippage protection
- **Royalty Enforcement**: EIP-2981 royalty calculation, royalty splitting, and compliance checking
- **Collection Analytics**: Floor price, volume, unique holders, and rarity ranking
- **Marketplace Protocol**: Order types, fee structures, and protocol governance
- **Price Discovery**: Pricing algorithms, rarity-based valuation, and market dynamics

## Usage Examples

```python
from nft_marketplace import (
    ListingManager,
    AuctionEngine,
    OrderMatcher,
    RoyaltyCalculator,
    CollectionAnalytics,
)

# --- Listing Management ---
listing_mgr = ListingManager()
listing = listing_mgr.create_fixed_price(
    collection="0x1234...",
    token_id=42,
    price_eth=1.5,
    seller="0xABCD...",
    duration_hours=72,
)
print(f"Listing: {listing.listing_id}")
print(f"Price: {listing.price_eth} ETH")
print(f"Expires: {listing.expires_at}")

# --- Auction ---
auction_engine = AuctionEngine()
auction = auction_engine.create_english_auction(
    collection="0x1234...",
    token_id=42,
    starting_price=0.1,
    reserve_price=2.0,
    duration_hours=24,
)
bid = auction_engine.place_bid(auction.auction_id, "0xBidder", 1.0)
print(f"Bid: {bid.amount} ETH")
print(f"Reserve met: {auction_engine.check_reserve(auction.auction_id)}")

# --- Order Matching ---
matcher = OrderMatcher()
trade = matcher.execute_trade(
    listing_id=listing.listing_id,
    buyer="0xBuyer",
    price_eth=1.5,
    max_slippage=0.01,
)
print(f"Trade executed: {trade.trade_id}")

# --- Royalty Calculation ---
royalty_calc = RoyaltyCalculator()
royalty = royalty_calc.calculate(
    sale_price_eth=10.0,
    royalty_bps=500,
    seller_share_bps=9500,
)
print(f"Creator royalty: {royalty.creator_share} ETH")
print(f"Seller receives: {royalty.seller_share} ETH")

# --- Collection Analytics ---
analytics = CollectionAnalytics("0x1234...")
stats = analytics.get_stats()
print(f"Floor: {stats.floor_price:.2f} ETH")
print(f"Volume (24h): {stats.volume_24h:.1f} ETH")
print(f"Holders: {stats.unique_holders}")
```

## Best Practices

- Use EIP-2981 for on-chain royalty declarations — honor across all listings
- Implement escrow for fixed-price listings to prevent front-running
- Set minimum bid increments for auctions to prevent bid sniping
- Use commit-reveal for sealed-bid auctions to prevent bid manipulation
- Enforce collection-level royalty standards across marketplace protocol
- Implement anti-snip mechanisms (extend auction on last-minute bids)
- Track floor price in real-time for collection analytics dashboards
- Use Merkle trees for allowlist verification in drop mechanics
- Implement cancel listing with proper on-chain state cleanup
- Use off-chain order signing with on-chain settlement for gas efficiency

## Related Modules

- **defi-patterns**: DeFi composability with NFT collateral
- **token-analytics**: Token analysis for NFT-related tokens
- **wallet-integration**: Wallet connection for marketplace users
- **dao-governance**: Marketplace governance mechanisms

---

## Advanced Configuration

### Marketplace Fee Configuration

Configure marketplace fee structures.

```python
marketplace_config = MarketplaceConfig(
    fees={
        "listing_fee": 0,
        "sale_fee": 0.025,  # 2.5%
        "royalty_fee": 0.05,  # 5% to creator
        "protocol_fee": 0.005,  # 0.5% to protocol
    },
    fee_recipients={
        "marketplace": "0xMarketplaceTreasury",
        "creator": "dynamic",  # From EIP-2981
    },
)
```

### Auction Configuration

Configure auction parameters.

```python
auction_config = AuctionConfig(
    english={
        "min_bid_increment_pct": 0.05,  # 5% minimum increase
        "anti_snip_duration_hours": 1,
        "extension_minutes": 10,
    },
    dutch={
        "price_decay_rate": 0.01,  # 1% per minute
        "min_price_pct": 0.1,  # 10% of starting price
    },
    sealed_bid={
        "commit_period_hours": 24,
        "reveal_period_hours": 24,
    },
)
```

### Collection Management

Configure collection-level settings.

```python
collection_config = CollectionConfig(
    max_supply=10000,
    royalty_standard="EIP-2981",
    metadata_standard="IPFS",
    verification_required=True,
)
```

---

## Architecture Patterns

### Order Book Pattern

```python
class OrderBook:
    def __init__(self):
        self.bids = SortedDict()  # price -> orders
        self.asks = SortedDict()

    def add_bid(self, price, amount, buyer):
        self.bids[price].append(Order(price, amount, buyer))

    def match_orders(self):
        while self.bids and self.asks:
            best_bid = self.bids.peekitem(-1)
            best_ask = self.asks.peekitem(0)
            if best_bid[0] >= best_ask[0]:
                self.execute_trade(best_bid, best_ask)
            else:
                break
```

### Escrow Pattern

```python
class NFTEscrow:
    def deposit(self, nft_address, token_id, seller):
        # Transfer NFT to escrow
        nft.transferFrom(seller, self.address, token_id)
        self.listings[token_id] = Listing(nft_address, token_id, seller)

    def release(self, token_id, buyer, price):
        listing = self.listings.pop(token_id)
        # Transfer NFT to buyer
        nft.transferFrom(self.address, buyer, token_id)
        # Transfer payment to seller
        payment.transfer(listing.seller, price)
```

### Allowlist Pattern

```python
class MerkleAllowlist:
    def __init__(self, addresses, amounts):
        self.tree = self.build_merkle_tree(addresses, amounts)

    def verify(self, address, amount, proof):
        leaf = keccak256(encode(address, amount))
        return self.verify_proof(proof, leaf, self.tree.root)
```

---

## Integration Guide

### IPFS Integration

```python
from ipfshttpclient import connect

client = connect()
metadata = {
    "name": "My NFT",
    "description": "A unique digital collectible",
    "image": "ipfs://QmHash/image.png",
    "attributes": [
        {"trait_type": "Background", "value": "Blue"},
        {"trait_type": "Rarity", "value": "Rare"},
    ],
}
result = client.add_json(metadata)
```

### OpenSea Integration

```python
# List on OpenSea
opensea = OpenSeaAPI(api_key="...")
opensea.create_listing(
    asset_contract_address=nft_address,
    token_id=token_id,
    start_price=1.0,
    end_price=0.1,
    duration_hours=24,
)
```

---

## Performance Optimization

### Metadata Caching

```python
metadata_cache = MetadataCache(
    backend="redis",
    ttl_seconds=3600,
    max_entries=10000,
)
```

### Batch Operations

```python
# Batch mint multiple NFTs
def batch_mint(contract, recipients, token_ids):
    tx = contract.functions.batchMint(
        recipients, token_ids
    ).build_transaction({...})
```

---

## Security Considerations

### Signature Verification

```python
# Verify off-chain signatures
def verify_listing_signature(message, signature, expected_signer):
    recovered = recover_signer(message, signature)
    return recovered.lower() == expected_signer.lower()
```

### Front-Running Protection

```python
# Use commit-reveal for sensitive operations
class CommitReveal:
    def commit(self, hash):
        # Store hash on-chain
        pass

    def reveal(self, value, salt):
        # Verify matches commit
        assert keccak256(encode(value, salt)) == stored_hash
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Listing failed | Insufficient approval | Approve marketplace |
| Auction not ending | Anti-snip extension | Wait for final extension |
| Royalty not paid | Non-compliant marketplace | Use EIP-2981 |
| Metadata broken | IPFS unavailable | Check IPFS gateway |

---

## API Reference

### ListingManager

```python
class ListingManager:
    def create_fixed_price(collection, token_id, price, seller, duration) -> Listing
    def cancel_listing(listing_id) -> None
    def update_price(listing_id, new_price) -> Listing
    def get_active_listings(collection) -> List[Listing]
```

### AuctionEngine

```python
class AuctionEngine:
    def create_english_auction(collection, token_id, start_price, reserve, duration) -> Auction
    def place_bid(auction_id, bidder, amount) -> Bid
    def end_auction(auction_id) -> AuctionResult
    def check_reserve(auction_id) -> bool
```

---

## Data Models

### Listing

```python
@dataclass
class Listing:
    listing_id: str
    collection: str
    token_id: int
    price: float
    seller: str
    status: str  # active, sold, cancelled
    created_at: datetime
    expires_at: datetime
```

### Auction

```python
@dataclass
class Auction:
    auction_id: str
    collection: str
    token_id: int
    start_price: float
    reserve_price: float
    current_bid: Optional[Bid]
    status: str  # active, ended, cancelled
    ends_at: datetime
```

---

## Deployment Guide

### Marketplace Deployment

```bash
# Deploy marketplace contract
forge create --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  src/NFTMarketplace.sol:NFTMarketplace \
  --constructor-args $FEE_RECIPIENT $FEE_BPS
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `nft.listing.count` | Active listings | Anomaly |
| `nft.sale.volume` | Daily volume | Anomaly |
| `nft.auction.active` | Active auctions | Spike |

---

## Testing Strategy

### Marketplace Tests

```python
def test_listing():
    marketplace = NFTMarketplace()
    listing = marketplace.create_fixed_price(nft, token_id, 1.0, seller, 72)
    assert listing.status == "active"

def test_purchase():
    marketplace.purchase(listing_id, buyer, price)
    assert nft.ownerOf(token_id) == buyer
```

---

## Versioning & Migration

### Contract Versioning

Follow semantic versioning for marketplace contracts.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Floor Price** | Lowest price in a collection |
| **Reserve Price** | Minimum acceptable auction price |
| **Anti-Snip** | Mechanism to prevent last-second bids |
| **Allowlist** | Pre-approved list for NFT drops |
| **Reveal** | Unveiling of NFT metadata after mint |

---

## Changelog

### v2.0.0
- Added sealed-bid auctions
- Merkle allowlist support
- Multi-collection analytics

### v1.0.0
- Initial release with fixed-price listings

---

## Contributing Guidelines

- Test all marketplace interactions
- Verify signature security
- Document fee structures

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

## Advanced Configuration

### Marketplace Configuration

```yaml
marketplace:
  protocol_fee: 2.5  # percentage
  creator_royalty: 10  # percentage (EIP-2981)
  min_bid_increment: 0.01  # ETH
  auction_duration_hours: 24
  listing_expiry_days: 30
  supported_chains: [1, 137, 42161, 10, 8453]
  payment_tokens:
    - symbol: "ETH"
      address: "0x0000000000000000000000000000000000000000"
    - symbol: "WETH"
      address: "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    - symbol: "USDC"
      address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
```

### Collection Configuration

```yaml
collections:
  default:
    max_supply: 10000
    royalty_bps: 1000  # 10%
    require_creator_verification: true
    allow_lazy_mint: true
    metadata_standard: "IPFS"
  premium:
    max_supply: 1000
    royalty_bps: 750  # 7.5%
    require_creator_verification: true
    allow_lazy_mint: false
    metadata_standard: "Arweave"
```

## Architecture Patterns

### Marketplace Architecture

```
Marketplace Stack:
├── Frontend
│   ├── Collection browser
│   ├── NFT detail pages
│   ├── Listing creation
│   ├── Auction bidding
│   └── Portfolio management
├── Backend
│   ├── Indexer (Subgraph/Covalent)
│   ├── Order book API
│   ├── Price oracle
│   ├── Notification service
│   └── Analytics engine
├── Smart Contracts
│   ├── Exchange (core trading)
│   ├── Collection (ERC-721/1155)
│   ├── Auction (English/Dutch)
│   ├── Royalty (EIP-2981)
│   └── Governance (protocol fees)
├── Storage
│   ├── IPFS/Arweave (metadata)
│   ├── On-chain (orders)
│   └── Off-chain (user data)
└── Infrastructure
    ├── RPC nodes
    ├── Indexer nodes
    └── CDN (images/media)
```

### Order Book Architecture

```
Order Flow:
├── Listing Creation
│   ├── Seller signs order
│   ├── Order validation
│   ├── Fee calculation
│   └── Order storage
├── Order Matching
│   ├── Buyer bid/offers
│   ├── Price matching
│   ├── Order priority
│   └── Settlement
├── Settlement
│   ├── Token transfer
│   ├── NFT transfer
│   ├── Royalty payment
│   ├── Fee collection
│   └── Event emission
└── Analytics
    ├── Price history
    ├── Volume tracking
    └── Floor price
```

### Auction Architecture

```
Auction Types:
├── English Auction
│   ├── Minimum bid
│   ├── Bid increment
│   ├── Reserve price
│   └── Anti-sniping
├── Dutch Auction
│   ├── Starting price
│   ├── Price decay
│   ├── Buy now
│   └── Time-based
├── Sealed Bid
│   ├── Commit phase
│   ├── Reveal phase
│   ├── Highest bid wins
│   └── Privacy protection
└── Timed Auction
    ├── Fixed duration
    ├── Auto-extension
    ├── Winner selection
    └── Payment processing
```

### Royalty Architecture

```
Royalty Flow:
├── EIP-2981 Standard
│   ├── Royalty info query
│   ├── Receiver address
│   └── Royalty amount
├── Royalty Enforcement
│   ├── Operator filter
│   ├── On-chain checks
│   └── Compliance tracking
├── Royalty Splitting
│   ├── Creator share
│   ├── Platform share
│   └── Multi-recipient
└── Payment Processing
    ├── ETH/WETH transfer
    ├── ERC-20 transfer
    └── Batch payments
```

## Integration Guide

### Exchange Contract Integration

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract NFTExchange is ReentrancyGuard {
    struct Listing {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 price;
        address paymentToken;
        uint256 expiry;
        bool active;
    }

    mapping(bytes32 => Listing) public listings;
    uint256 public protocolFeeBps = 250; // 2.5%
    address public feeRecipient;

    event ListingCreated(bytes32 indexed listingId, address seller, address nftContract, uint256 tokenId, uint256 price);
    event ListingFilled(bytes32 indexed listingId, address buyer, uint256 price);
    event ListingCancelled(bytes32 indexed listingId);

    function createListing(
        address nftContract,
        uint256 tokenId,
        uint256 price,
        address paymentToken,
        uint256 duration
    ) external returns (bytes32) {
        require(price > 0, "Price must be > 0");

        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        bytes32 listingId = keccak256(abi.encodePacked(nftContract, tokenId, block.timestamp));
        listings[listingId] = Listing({
            seller: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            price: price,
            paymentToken: paymentToken,
            expiry: block.timestamp + duration,
            active: true
        });

        emit ListingCreated(listingId, msg.sender, nftContract, tokenId, price);
        return listingId;
    }

    function buyListing(bytes32 listingId) external payable nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.active, "Listing not active");
        require(block.timestamp < listing.expiry, "Listing expired");
        require(msg.value >= listing.price, "Insufficient payment");

        // Protocol fee
        uint256 fee = (listing.price * protocolFeeBps) / 10000;
        uint256 sellerProceeds = listing.price - fee;

        // Transfer NFT
        IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);

        // Transfer payment
        payable(listing.seller).transfer(sellerProceeds);
        payable(feeRecipient).transfer(fee);

        listing.active = false;
        emit ListingFilled(listingId, msg.sender, listing.price);
    }

    function cancelListing(bytes32 listingId) external {
        Listing storage listing = listings[listingId];
        require(listing.seller == msg.sender, "Not seller");
        require(listing.active, "Listing not active");

        IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);
        listing.active = false;

        emit ListingCancelled(listingId);
    }
}
```

### Auction Contract Integration

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract NFTAuction is ReentrancyGuard {
    struct Auction {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 startPrice;
        uint256 reservePrice;
        uint256 highestBid;
        address highestBidder;
        uint256 startTime;
        uint256 endTime;
        bool settled;
    }

    mapping(uint256 => Auction) public auctions;
    uint256 public nextAuctionId;

    event AuctionCreated(uint256 indexed auctionId, address seller, address nftContract, uint256 tokenId, uint256 startPrice);
    event BidPlaced(uint256 indexed auctionId, address bidder, uint256 amount);
    event AuctionSettled(uint256 indexed auctionId, address winner, uint256 amount);

    function createAuction(
        address nftContract,
        uint256 tokenId,
        uint256 startPrice,
        uint256 reservePrice,
        uint256 duration
    ) external returns (uint256) {
        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        uint256 auctionId = nextAuctionId++;
        auctions[auctionId] = Auction({
            seller: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            startPrice: startPrice,
            reservePrice: reservePrice,
            highestBid: 0,
            highestBidder: address(0),
            startTime: block.timestamp,
            endTime: block.timestamp + duration,
            settled: false
        });

        emit AuctionCreated(auctionId, msg.sender, nftContract, tokenId, startPrice);
        return auctionId;
    }

    function placeBid(uint256 auctionId) external payable nonReentrant {
        Auction storage auction = auctions[auctionId];
        require(block.timestamp >= auction.startTime, "Auction not started");
        require(block.timestamp < auction.endTime, "Auction ended");
        require(msg.value > auction.highestBid, "Bid too low");

        // Refund previous bidder
        if (auction.highestBidder != address(0)) {
            payable(auction.highestBidder).transfer(auction.highestBid);
        }

        auction.highestBid = msg.value;
        auction.highestBidder = msg.sender;

        emit BidPlaced(auctionId, msg.sender, msg.value);
    }

    function settleAuction(uint256 auctionId) external {
        Auction storage auction = auctions[auctionId];
        require(block.timestamp >= auction.endTime, "Auction not ended");
        require(!auction.settled, "Already settled");

        if (auction.highestBid >= auction.reservePrice && auction.highestBidder != address(0)) {
            // Transfer NFT to winner
            IERC721(auction.nftContract).transferFrom(address(this), auction.highestBidder, auction.tokenId);
            // Transfer payment to seller
            payable(auction.seller).transfer(auction.highestBid);

            emit AuctionSettled(auctionId, auction.highestBidder, auction.highestBid);
        } else {
            // Return NFT to seller (reserve not met)
            IERC721(auction.nftContract).transferFrom(address(this), auction.seller, auction.tokenId);
        }

        auction.settled = true;
    }
}
```

### Indexer Integration (Subgraph)

```graphql
# schema.graphql
type Collection @entity {
  id: Bytes!
  name: String!
  symbol: String!
  totalSupply: BigInt!
  uniqueHolders: BigInt!
  floorPrice: BigDecimal
  volumeTraded: BigDecimal!
  creatorRoyaltyBps: Int!
}

type NFT @entity {
  id: Bytes!
  collection: Collection!
  tokenId: BigInt!
  owner: Bytes!
  lastSalePrice: BigDecimal
  lastSaleTimestamp: BigInt
  tokenURI: String!
  metadata: NFTMetadata
}

type Listing @entity {
  id: Bytes!
  nft: NFT!
  seller: Bytes!
  price: BigDecimal!
  paymentToken: Bytes!
  status: ListingStatus!
  createdAt: BigInt!
  expiresAt: BigInt!
}

type Auction @entity {
  id: Bytes!
  nft: NFT!
  seller: Bytes!
  startPrice: BigDecimal!
  highestBid: BigDecimal
  highestBidder: Bytes
  startTime: BigInt!
  endTime: BigInt!
  settled: Boolean!
}

type Sale @entity {
  id: Bytes!
  nft: NFT!
  seller: Bytes!
  buyer: Bytes!
  price: BigDecimal!
  paymentToken: Bytes!
  timestamp: BigInt!
  txHash: Bytes!
}
```

## Performance Optimization

### Indexing Optimization

| Technique | Description | Speedup |
|-----------|-------------|---------|
| Batch indexing | Process multiple blocks | 3-5x |
| Parallel processing | Multiple collections | 2-4x |
| Caching | Cache metadata | 5-10x |
| Lazy loading | Load on demand | 2-3x |

### Query Optimization

```
Query Strategies:
├── Pagination
│   ├── Cursor-based (preferred)
│   ├── Offset-based (legacy)
│   └── Keyset pagination
├── Caching
│   ├── Redis cache
│   ├── CDN cache
│   └── Browser cache
├── Indexing
│   ├── Composite indexes
│   ├── Partial indexes
│   └── Materialized views
└── Optimization
    ├── Select only needed fields
    ├── Avoid N+1 queries
    └── Use DataLoader
```

## Security Considerations

### Marketplace Security

| Threat | Description | Mitigation |
|--------|-------------|------------|
| Front-running | MEV/sandwich attacks | Private mempool, commit-reveal |
| Price manipulation | Wash trading | Volume verification, KYC |
| Signature replay | Reuse old signatures | Nonce, expiration, chain ID |
| Royalty bypass | Skip royalty payment | On-chain enforcement |
| Fake listings | Unauthorized listings | On-chain approval verification |

### Signature Security

```
Signature Best Practices:
├── EIP-712 typed data
│   ├── Domain separator
│   ├── Type hashes
│   └── Chain ID inclusion
├── Nonce management
│   ├── Sequential nonces
│   ├── Random nonces
│   └── Expiration timestamps
├── Verification
│   ├── Recover signer
│   ├── Check authorization
│   └── Validate parameters
└── Storage
    ├── Secure key management
    ├── HSM integration
    └── Multi-sig for high value
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Listing fails | Transaction reverts | Check approval, balance |
| Auction not settling | NFT stuck | Check endTime, settlement |
| Royalty not paid | Creator not receiving | Check EIP-2981 implementation |
| Metadata broken | Image not loading | Check IPFS/Arweave link |
| Price oracle stale | Wrong floor price | Update oracle, check freshness |

### Debugging Commands

```bash
# Check NFT owner
cast call $NFT "ownerOf(uint256)" $TOKEN_ID --rpc-url $RPC

# Check marketplace approval
cast call $NFT "isApprovedForAll(address,address)" $OWNER $MARKETPLACE --rpc-url $RPC

# Check listing state
cast call $MARKETPLACE "listings(bytes32)" $LISTING_ID --rpc-url $RPC

# Check auction state
cast call $AUCTION "auctions(uint256)" $AUCTION_ID --rpc-url $RPC
```

## Testing Strategy

### Marketplace Testing

```
1. Unit Tests
   ├── Listing creation/cancellation
   ├── Buy/sell flows
   ├── Auction bidding/settlement
   └── Royalty calculation

2. Integration Tests
   ├── End-to-end trading
   ├── Multi-collection support
   ├── Cross-chain bridging
   └── Payment token variety

3. Security Tests
   ├── Signature verification
   ├── Reentrancy attacks
   ├── Front-running resistance
   └── Price manipulation

4. Performance Tests
   ├── Transaction throughput
   ├── Gas optimization
   ├── Indexer performance
   └── API response time
```

## Versioning & Migration

### Versioning

```
Major: Protocol changes
├── Example: New order type
├── Requires: Governance vote
└── Risk: High

Minor: Feature additions
├── Example: Add auction type
├── Requires: Testing
└── Risk: Low

Patch: Bug fixes
├── Example: Fix royalty calculation
├── Requires: Basic testing
└── Risk: Very low
```

## Glossary

| Term | Definition |
|------|-----------|
| ERC-721 | Non-fungible token standard |
| ERC-1155 | Multi-token standard |
| EIP-2981 | NFT royalty standard |
| Floor Price | Lowest listed price in collection |
| Lazy Minting | Mint NFT on first purchase |
| Metadata | NFT attributes and media links |
| Order Book | Active listings and bids |
| Royalty | Creator payment on secondary sales |
| Sealed Bid | Auction with hidden bids |
| Wash Trading | Fake trading to inflate volume |

## Changelog

### v2.0.0
- Added Dutch auctions
- Added sealed-bid auctions
- Merkle allowlist support
- Multi-collection analytics

### v1.0.0
- Initial release with fixed-price listings
