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
