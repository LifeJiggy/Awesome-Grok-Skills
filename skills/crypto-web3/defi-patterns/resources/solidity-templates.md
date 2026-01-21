# Solidity Templates

## 🏗️ Smart Contract Templates

### ERC20 Token
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GrokToken is ERC20, Ownable {
    constructor(
        string memory name,
        string memory symbol,
        uint256 initialSupply
    ) ERC20(name, symbol) {
        _mint(msg.sender, initialSupply * (10 ** decimals()));
    }
    
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
    
    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }
}
```

### DeFi Yield Farming
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract YieldFarm is ReentrancyGuard {
    struct Pool {
        IERC20 stakingToken;
        IERC20 rewardToken;
        uint256 rewardRate;
        uint256 lockPeriod;
        uint256 totalStaked;
        mapping(address => uint256) userStaked;
        mapping(address => uint256) userStakeTime;
    }
    
    mapping(uint256 => Pool) public pools;
    uint256 public poolCount;
    
    function createPool(
        address _stakingToken,
        address _rewardToken,
        uint256 _rewardRate,
        uint256 _lockPeriod
    ) external {
        pools[poolCount] = Pool({
            stakingToken: IERC20(_stakingToken),
            rewardToken: IERC20(_rewardToken),
            rewardRate: _rewardRate,
            lockPeriod: _lockPeriod,
            totalStaked: 0
        });
        poolCount++;
    }
    
    function stake(uint256 poolId, uint256 amount) external nonReentrant {
        Pool storage pool = pools[poolId];
        pool.stakingToken.transferFrom(msg.sender, address(this), amount);
        pool.userStaked[msg.sender] += amount;
        pool.userStakeTime[msg.sender] = block.timestamp;
        pool.totalStaked += amount;
    }
    
    function unstake(uint256 poolId) external nonReentrant {
        Pool storage pool = pools[poolId];
        require(
            block.timestamp >= pool.userStakeTime[msg.sender] + pool.lockPeriod,
            "Tokens are still locked"
        );
        
        uint256 amount = pool.userStaked[msg.sender];
        pool.userStaked[msg.sender] = 0;
        pool.totalStaked -= amount;
        pool.stakingToken.transfer(msg.sender, amount);
    }
}
```

## 🔒 Security Best Practices

### Access Control
```solidity
import "@openzeppelin/contracts/access/AccessControl.sol";

contract SecureContract is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
    
    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
    }
    
    modifier onlyAdmin() {
        require(hasRole(ADMIN_ROLE, msg.sender), "Admin role required");
        _;
    }
    
    modifier onlyOperator() {
        require(hasRole(OPERATOR_ROLE, msg.sender), "Operator role required");
        _;
    }
}
```

### Reentrancy Protection
```solidity
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract ProtectedContract is ReentrancyGuard {
    mapping(address => uint256) public balances;
    
    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        balances[msg.sender] -= amount;
        
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

## 📊 Gas Optimization Patterns

### Batch Operations
```solidity
contract BatchOperations {
    function batchTransfer(address[] calldata recipients, uint256[] calldata amounts) external {
        require(recipients.length == amounts.length, "Array length mismatch");
        
        for (uint256 i = 0; i < recipients.length; i++) {
            // Batch processing logic
        }
    }
    
    function multicall(bytes[] calldata data) external returns (bytes[] memory results) {
        results = new bytes[](data.length);
        for (uint256 i = 0; i < data.length; i++) {
            (bool success, bytes memory result) = address(this).delegatecall(data[i]);
            require(success, "Call failed");
            results[i] = result;
        }
    }
}
```

### Storage Optimization
```solidity
contract StorageOptimized {
    // Use structs to pack multiple values
    struct User {
        uint128 balance;  // Saves gas compared to uint256
        uint64 timestamp;
        uint32 level;
        bool active;
    }
    
    mapping(address => User) public users;
    
    // Use events instead of storage for historical data
    event TransferHistory(
        address indexed from,
        address indexed to,
        uint256 amount,
        uint256 timestamp
    );
}
```

## 🎯 DeFi Patterns

### Liquidity Pool
```solidity
interface IUniswapV2Pair {
    function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external;
}

contract LiquidityPool {
    IUniswapV2Pair public pair;
    
    function getAmountOut(uint amountIn, uint reserveIn, uint reserveOut) public pure returns (uint amountOut) {
        uint amountInWithFee = amountIn * 997;
        uint numerator = amountInWithFee * reserveOut;
        uint denominator = reserveIn * 1000 + amountInWithFee;
        return numerator / denominator;
    }
    
    function swapTokens(address tokenIn, uint amountIn) external {
        // Liquidity pool swap logic
    }
}
```

### Governance
```solidity
contract DAO {
    struct Proposal {
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 deadline;
        bool executed;
        mapping(address => bool) hasVoted;
    }
    
    mapping(uint256 => Proposal) public proposals;
    mapping(address => uint256) public votingPower;
    
    function createProposal(string memory description) external returns (uint256) {
        // Proposal creation logic
    }
    
    function vote(uint256 proposalId, bool support) external {
        // Voting logic
    }
}
```

## 🧪 Testing Templates

### Hardhat Testing
```javascript
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GrokToken", function () {
    let grokToken;
    let owner;
    let addr1;
    
    beforeEach(async function () {
        [owner, addr1] = await ethers.getSigners();
        
        const GrokToken = await ethers.getContractFactory("GrokToken");
        grokToken = await GrokToken.deploy("Grok Token", "GROK", 1000000);
    });
    
    describe("Deployment", function () {
        it("Should set the right owner", async function () {
            expect(await grokToken.owner()).to.equal(owner.address);
        });
        
        it("Should assign total supply to owner", async function () {
            const ownerBalance = await grokToken.balanceOf(owner.address);
            expect(await grokToken.totalSupply()).to.equal(ownerBalance);
        });
    });
    
    describe("Transactions", function () {
        it("Should transfer tokens between accounts", async function () {
            await grokToken.transfer(addr1.address, 50);
            const addr1Balance = await grokToken.balanceOf(addr1.address);
            expect(addr1Balance).to.equal(50);
        });
    });
});
```

### Foundry Testing
```solidity
import "forge-std/Test.sol";
import "../src/GrokToken.sol";

contract GrokTokenTest is Test {
    GrokToken public grokToken;
    
    function setUp() public {
        grokToken = new GrokToken("Grok Token", "GROK", 1000000);
    }
    
    function testDeployment() public {
        assertEq(grokToken.name(), "Grok Token");
        assertEq(grokToken.symbol(), "GROK");
        assertEq(grokToken.totalSupply(), 1000000 * 10 ** 18);
    }
    
    function testTransfer() public {
        address recipient = address(0x1);
        uint256 amount = 100 * 10 ** 18;
        
        grokToken.transfer(recipient, amount);
        assertEq(grokToken.balanceOf(recipient), amount);
    }
}
```

## 🚀 Deployment Scripts

### Hardhat Deployment
```javascript
async function main() {
    const [deployer] = await ethers.getSigners();
    
    console.log("Deploying contracts with account:", deployer.address);
    console.log("Account balance:", (await deployer.getBalance()).toString());
    
    const GrokToken = await ethers.getContractFactory("GrokToken");
    const grokToken = await GrokToken.deploy("Grok Token", "GROK", 1000000);
    
    console.log("GrokToken deployed to:", grokToken.address);
    
    // Verify on Etherscan
    if (network.name !== "hardhat") {
        await grokToken.deployTransaction.wait(5);
        await hre.run("verify:verify", {
            address: grokToken.address,
            constructorArguments: ["Grok Token", "GROK", 1000000]
        });
    }
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
```

### Foundry Deployment
```solidity
// script/Deploy.s.sol
import "forge-std/Script.sol";
import "../src/GrokToken.sol";

contract DeployScript is Script {
    function run() external {
        vm.startBroadcast();
        
        GrokToken grokToken = new GrokToken("Grok Token", "GROK", 1000000);
        
        console.log("GrokToken deployed at:", address(grokToken));
        
        vm.stopBroadcast();
    }
}
```

## 📈 Monitoring

### Event Watching
```javascript
const grokToken = await ethers.getContractAt("GrokToken", contractAddress);

grokToken.on("Transfer", (from, to, amount) => {
    console.log(`Transfer: ${from} -> ${to}, Amount: ${ethers.utils.formatEther(amount)}`);
});

// Filter for specific events
const filter = grokToken.filters.Transfer(null, "0xTargetAddress");
grokToken.on(filter, (from, to, amount) => {
    console.log(`Transfer to target: ${ethers.utils.formatEther(amount)}`);
});
```

---

*Remember: Always audit your smart contracts before deploying to mainnet. Use established libraries like OpenZeppelin for battle-tested implementations.* 🔒