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
