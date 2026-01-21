# ERC721 Standards

## 🎨 NFT Standards Overview

### ERC721 Basic Implementation
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GrokNFT is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public mintPrice = 0.01 ether;
    bool public mintingActive = false;
    
    constructor() ERC721("Grok NFT", "GROKNFT") {}
    
    function mintNFT(address recipient, string memory tokenURI) 
        public 
        payable 
        returns (uint256) 
    {
        require(mintingActive, "Minting is not active");
        require(_tokenIds.current() < MAX_SUPPLY, "Max supply reached");
        require(msg.value >= mintPrice, "Insufficient payment");
        
        _tokenIds.increment();
        uint256 newItemId = _tokenIds.current();
        
        _mint(recipient, newItemId);
        _setTokenURI(newItemId, tokenURI);
        
        return newItemId;
    }
    
    function toggleMinting() external onlyOwner {
        mintingActive = !mintingActive;
    }
    
    function setMintPrice(uint256 newPrice) external onlyOwner {
        mintPrice = newPrice;
    }
    
    function withdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        payable(owner()).transfer(balance);
    }
}
```

### ERC721 Enumerable
```solidity
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

contract EnumerableNFT is ERC721, ERC721Enumerable, Ownable {
    constructor() ERC721("Enumerable NFT", "ENFT") {}
    
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal override(ERC721, ERC721Enumerable) {
        super._beforeTokenTransfer(from, to, tokenId);
    }
    
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
    
    function tokensOfOwner(address owner) external view returns (uint256[] memory) {
        uint256 balance = balanceOf(owner);
        uint256[] memory tokens = new uint256[](balance);
        
        for (uint256 i = 0; i < balance; i++) {
            tokens[i] = tokenOfOwnerByIndex(owner, i);
        }
        
        return tokens;
    }
}
```

### ERC721A (Gas Optimized)
```solidity
// ERC721A is optimized for batch minting
contract ERC721A is ERC721 {
    uint256 private _currentIndex;
    uint256 private _burnCounter;
    
    mapping(address => uint256) private _ownershipData;
    mapping(uint256 => address) private _tokenApprovals;
    
    constructor(string memory name, string memory symbol) ERC721(name, symbol) {
        _currentIndex = _startTokenId();
    }
    
    function _startTokenId() internal view virtual returns (uint256) {
        return 1;
    }
    
    function nextTokenId() external view returns (uint256) {
        return _currentIndex;
    }
    
    function _mint(address to, uint256 quantity) internal {
        uint256 startTokenId = _currentIndex;
        require(to != address(0), "ERC721A: mint to the zero address");
        
        _beforeTokenTransfers(address(0), to, startTokenId, quantity);
        
        for (uint256 i = 0; i < quantity; i++) {
            _packedOwnerships[startTokenId + i] = _packOwnershipData(to, _BITMASK_NEXT_INITIALIZED);
        }
        
        _currentIndex = startTokenId + quantity;
        
        _afterTokenTransfers(address(0), to, startTokenId, quantity);
    }
}
```

## 🎪 Marketplace Features

### Fixed Price Sale
```solidity
contract NFTMarketplace {
    struct Listing {
        uint256 tokenId;
        address seller;
        uint256 price;
        bool active;
    }
    
    IERC721 public nftContract;
    mapping(uint256 => Listing) public listings;
    
    event Listed(uint256 indexed tokenId, address indexed seller, uint256 price);
    event Sold(uint256 indexed tokenId, address indexed seller, address indexed buyer, uint256 price);
    event ListingCanceled(uint256 indexed tokenId, address indexed seller);
    
    function listToken(uint256 tokenId, uint256 price) external {
        require(nftContract.ownerOf(tokenId) == msg.sender, "Not token owner");
        require(nftContract.getApproved(tokenId) == address(this) || 
                nftContract.isApprovedForAll(msg.sender, address(this)), 
                "Marketplace not approved");
        
        listings[tokenId] = Listing({
            tokenId: tokenId,
            seller: msg.sender,
            price: price,
            active: true
        });
        
        emit Listed(tokenId, msg.sender, price);
    }
    
    function buyToken(uint256 tokenId) external payable {
        Listing storage listing = listings[tokenId];
        require(listing.active, "Token not listed");
        require(msg.value >= listing.price, "Insufficient payment");
        
        listing.active = false;
        
        nftContract.safeTransferFrom(listing.seller, msg.sender, tokenId);
        
        payable(listing.seller).transfer(listing.price);
        
        if (msg.value > listing.price) {
            payable(msg.sender).transfer(msg.value - listing.price);
        }
        
        emit Sold(tokenId, listing.seller, msg.sender, listing.price);
    }
    
    function cancelListing(uint256 tokenId) external {
        Listing storage listing = listings[tokenId];
        require(listing.seller == msg.sender, "Not the seller");
        require(listing.active, "Already inactive");
        
        listing.active = false;
        emit ListingCanceled(tokenId, msg.sender);
    }
}
```

### Auction System
```solidity
contract NFTAuction {
    struct Auction {
        uint256 tokenId;
        address seller;
        uint256 startPrice;
        uint256 endTime;
        address highestBidder;
        uint256 highestBid;
        bool ended;
    }
    
    mapping(uint256 => Auction) public auctions;
    mapping(uint256 => mapping(address => uint256)) public pendingReturns;
    
    event AuctionCreated(uint256 indexed tokenId, address indexed seller, uint256 startPrice, uint256 endTime);
    event BidPlaced(uint256 indexed tokenId, address indexed bidder, uint256 amount);
    event AuctionEnded(uint256 indexed tokenId, address indexed winner, uint256 amount);
    
    function createAuction(
        uint256 tokenId,
        uint256 startPrice,
        uint256 duration
    ) external {
        require(duration > 0, "Duration must be positive");
        
        auctions[tokenId] = Auction({
            tokenId: tokenId,
            seller: msg.sender,
            startPrice: startPrice,
            endTime: block.timestamp + duration,
            highestBidder: address(0),
            highestBid: 0,
            ended: false
        });
        
        emit AuctionCreated(tokenId, msg.sender, startPrice, block.timestamp + duration);
    }
    
    function bid(uint256 tokenId) external payable {
        Auction storage auction = auctions[tokenId];
        require(block.timestamp <= auction.endTime, "Auction ended");
        require(!auction.ended, "Auction already ended");
        require(msg.value >= auction.startPrice, "Bid below start price");
        require(msg.value > auction.highestBid, "Bid not high enough");
        
        if (auction.highestBidder != address(0)) {
            pendingReturns[tokenId][auction.highestBidder] += auction.highestBid;
        }
        
        auction.highestBidder = msg.sender;
        auction.highestBid = msg.value;
        
        emit BidPlaced(tokenId, msg.sender, msg.value);
    }
    
    function endAuction(uint256 tokenId) external {
        Auction storage auction = auctions[tokenId];
        require(block.timestamp >= auction.endTime, "Auction not ended");
        require(!auction.ended, "Auction already ended");
        
        auction.ended = true;
        
        if (auction.highestBidder != address(0)) {
            // Transfer NFT to winner
            IERC721(tokenId).safeTransferFrom(auction.seller, auction.highestBidder, tokenId);
            // Transfer funds to seller
            payable(auction.seller).transfer(auction.highestBid);
        } else {
            // No bids, return to seller
            emit AuctionEnded(tokenId, address(0), 0);
            return;
        }
        
        emit AuctionEnded(tokenId, auction.highestBidder, auction.highestBid);
    }
    
    function withdrawRefund(uint256 tokenId) external {
        uint256 amount = pendingReturns[tokenId][msg.sender];
        require(amount > 0, "No refund available");
        
        pendingReturns[tokenId][msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
```

## 🎯 Dynamic NFTs

### Upgradeable NFTs
```solidity
import "@openzeppelin/contracts-upgradeable/token/ERC721/ERC721Upgradeable.sol";

contract UpgradeableNFT is ERC721Upgradeable, OwnableUpgradeable {
    mapping(uint256 => uint256) public levels;
    mapping(uint256 => uint256) public experience;
    mapping(uint256 => uint256) public lastClaimTime;
    
    function initialize() public initializer {
        __ERC721_init("Upgradeable NFT", "UNFT");
        __Ownable_init();
    }
    
    function gainExperience(uint256 tokenId, uint256 exp) external onlyOwner {
        require(_exists(tokenId), "Token does not exist");
        
        experience[tokenId] += exp;
        checkLevelUp(tokenId);
    }
    
    function checkLevelUp(uint256 tokenId) internal {
        uint256 currentLevel = levels[tokenId];
        uint256 expNeeded = currentLevel * 100;
        
        if (experience[tokenId] >= expNeeded) {
            levels[tokenId] = currentLevel + 1;
            experience[tokenId] -= expNeeded;
            
            // Update tokenURI based on new level
            string memory newURI = string(abi.encodePacked(
                "https://api.mynft.com/metadata/",
                Strings.toString(tokenId),
                "?level=",
                Strings.toString(levels[tokenId])
            ));
            
            _setTokenURI(tokenId, newURI);
        }
    }
}
```

### Generative Art NFT
```solidity
contract GenerativeArtNFT is ERC721, Ownable {
    uint256 public maxSupply;
    uint256 public currentSupply;
    string public baseURI;
    
    struct Artwork {
        uint256 tokenId;
        uint256 seed;
        address creator;
        uint256 timestamp;
    }
    
    mapping(uint256 => Artwork) public artworks;
    
    constructor(string memory _name, string memory _symbol, uint256 _maxSupply) 
        ERC721(_name, _symbol) {
        maxSupply = _maxSupply;
    }
    
    function generateSeed(uint256 tokenId) internal view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.difficulty,
            tokenId,
            msg.sender
        )));
    }
    
    function mintArtwork() external returns (uint256) {
        require(currentSupply < maxSupply, "Max supply reached");
        
        currentSupply++;
        uint256 tokenId = currentSupply;
        uint256 seed = generateSeed(tokenId);
        
        _mint(msg.sender, tokenId);
        
        artworks[tokenId] = Artwork({
            tokenId: tokenId,
            seed: seed,
            creator: msg.sender,
            timestamp: block.timestamp
        });
        
        return tokenId;
    }
    
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "Token does not exist");
        
        Artwork memory artwork = artworks[tokenId];
        
        return string(abi.encodePacked(
            baseURI,
            Strings.toString(tokenId),
            "?seed=",
            Strings.toString(artwork.seed)
        ));
    }
    
    function setBaseURI(string memory _baseURI) external onlyOwner {
        baseURI = _baseURI;
    }
}
```

## 🛡️ Security Considerations

### Anti-Rug Pull Mechanisms
```solidity
contract RugPullProtected {
    uint256 public liquidityLockDuration;
    uint256 public liquidityUnlockTime;
    mapping(address => uint256) public lockedLiquidity;
    
    modifier liquidityLocked() {
        require(block.timestamp < liquidityUnlockTime, "Liquidity unlocked");
        _;
    }
    
    function lockLiquidity(uint256 amount, uint256 duration) external {
        require(lockedLiquidity[msg.sender] == 0, "Already locked");
        
        lockedLiquidity[msg.sender] = amount;
        liquidityUnlockTime = block.timestamp + duration;
        liquidityLockDuration = duration;
    }
    
    function emergencyWithdraw() external {
        require(block.timestamp > liquidityUnlockTime, "Liquidity still locked");
        require(lockedLiquidity[msg.sender] > 0, "No locked liquidity");
        
        uint256 amount = lockedLiquidity[msg.sender];
        lockedLiquidity[msg.sender] = 0;
        
        payable(msg.sender).transfer(amount);
    }
}
```

### Royalty Enforcement
```solidity
import "@openzeppelin/contracts/token/common/ERC2981.sol";

contract RoyaltyNFT is ERC721, ERC2981 {
    address payable public royaltyRecipient;
    uint256 public royaltyPercentage; // in basis points (100 = 1%)
    
    constructor(address _royaltyRecipient, uint256 _royaltyPercentage) 
        ERC721("Royalty NFT", "RNFT") {
        royaltyRecipient = _royaltyRecipient;
        royaltyPercentage = _royaltyPercentage;
    }
    
    function royaltyInfo(uint256, uint256 salePrice) 
        external 
        view 
        override 
        returns (address receiver, uint256 royaltyAmount) 
    {
        return (royaltyRecipient, (salePrice * royaltyPercentage) / 10000);
    }
    
    function supportsInterface(bytes4 interfaceId) 
        public 
        view 
        override(ERC721, ERC2981) 
        returns (bool) 
    {
        return super.supportsInterface(interfaceId);
    }
    
    function setRoyaltyInfo(address _recipient, uint256 _percentage) external onlyOwner {
        royaltyRecipient = payable(_recipient);
        royaltyPercentage = _percentage;
    }
}
```

## 🧪 Testing Strategies

### NFT Testing
```javascript
describe("GrokNFT", function () {
    let grokNFT;
    let owner;
    let addr1;
    let addr2;
    
    beforeEach(async function () {
        [owner, addr1, addr2] = await ethers.getSigners();
        
        const GrokNFT = await ethers.getContractFactory("GrokNFT");
        grokNFT = await GrokNFT.deploy();
    });
    
    describe("Minting", function () {
        it("Should mint NFT to recipient", async function () {
            await grokNFT.toggleMinting();
            const tokenId = await grokNFT.mintNFT(
                addr1.address,
                "https://api.mynft.com/metadata/1"
            );
            
            expect(await grokNFT.ownerOf(1)).to.equal(addr1.address);
            expect(await grokNFT.tokenURI(1)).to.equal(
                "https://api.mynft.com/metadata/1"
            );
        });
        
        it("Should enforce mint price", async function () {
            await grokNFT.toggleMinting();
            
            await expect(
                grokNFT.mintNFT(addr1.address, "https://api.mynft.com/metadata/1", {
                    value: ethers.utils.parseEther("0.005") // Less than required
                })
            ).to.be.revertedWith("Insufficient payment");
        });
    });
    
    describe("Marketplace", function () {
        it("Should list and buy NFT", async function () {
            // Mint NFT first
            await grokNFT.toggleMinting();
            await grokNFT.mintNFT(owner.address, "https://api.mynft.com/metadata/1");
            
            // Approve marketplace
            await grokNFT.approve(marketplace.address, 1);
            
            // List NFT
            await marketplace.listToken(1, ethers.utils.parseEther("1"));
            
            // Buy NFT
            await marketplace.connect(addr1).buyToken(1, {
                value: ethers.utils.parseEther("1")
            });
            
            expect(await grokNFT.ownerOf(1)).to.equal(addr1.address);
        });
    });
});
```

## 📊 Analytics

### NFT Analytics
```javascript
// Track NFT sales and trends
class NFTAnalytics {
    constructor(contractAddress) {
        this.contract = new ethers.Contract(contractAddress, nftABI, provider);
    }
    
    async getTopHolders() {
        const transferEvents = await this.contract.queryFilter(
            this.contract.filters.Transfer()
        );
        
        const balances = {};
        
        transferEvents.forEach(event => {
            const from = event.args.from;
            const to = event.args.to;
            
            if (from !== ethers.constants.AddressZero) {
                balances[from] = (balances[from] || 0) - 1;
            }
            
            if (to !== ethers.constants.AddressZero) {
                balances[to] = (balances[to] || 0) + 1;
            }
        });
        
        return Object.entries(balances)
            .filter(([_, balance]) => balance > 0)
            .sort((a, b) => b[1] - a[1]);
    }
    
    async getSalesData(timeframe = '7d') {
        const now = Date.now();
        const timeframeMs = this.parseTimeframe(timeframe);
        const startTime = new Date(now - timeframeMs);
        
        const sales = [];
        const events = await this.contract.queryFilter(
            this.contract.filters.Sold(),
            startTime.getBlockNumber()
        );
        
        events.forEach(event => {
            sales.push({
                tokenId: event.args.tokenId,
                price: ethers.utils.formatEther(event.args.price),
                timestamp: event.args.timestamp
            });
        });
        
        return sales;
    }
}
```

---

*Remember: Always implement proper security measures including access controls, reentrancy protection, and thorough testing before deploying NFT contracts to mainnet.* 🎨