---
name: "dao-governance"
category: "crypto-web3"
version: "2.0.0"
tags: ["crypto-web3", "DAO", "governance", "voting", "proposals"]
---

# DAO Governance

## Overview

The DAO Governance module provides tools and patterns for building decentralized autonomous organization governance systems. It covers proposal creation, voting mechanisms, token-weighted governance, delegation, timelock contracts, and governance analytics.

This skill is essential for DAO tooling developers, governance researchers, and protocol teams implementing on-chain governance.

## Core Capabilities

- **Proposal Management**: Create, discuss, and execute governance proposals
- **Voting Mechanisms**: Token-weighted, quadratic, conviction voting, and multi-choice
- **Delegation**: Vote delegation, delegate profiles, and delegation tracking
- **Timelock**: Time-locked execution, veto mechanisms, and emergency procedures
- **Governance Analytics**: Voter participation, proposal outcomes, and governance health metrics
- **Off-Chain Governance**: Snapshot-style off-chain voting with on-chain execution
- **Treasury Management**: Treasury proposals, budget allocation, and multi-sig coordination

## Usage Examples

```python
from dao_governance import (
    ProposalManager,
    VotingEngine,
    DelegationManager,
    TimelockController,
    GovernanceAnalytics,
)

# --- Proposal Management ---
pm = ProposalManager()
proposal = pm.create_proposal(
    title="Increase staking rewards by 5%",
    description="Proposal to increase the base staking reward rate...",
    proposer="0x1234...",
    category="parameter_change",
)
print(f"Proposal: {proposal.proposal_id}")
print(f"Status: {proposal.status}")
print(f"Voting starts: {proposal.voting_start}")

# --- Voting ---
voter = VotingEngine()
vote = voter.cast_vote(
    proposal_id=proposal.proposal_id,
    voter="0xABCD...",
    support="for",
    voting_power=1000,
    weight=1.0,
)
print(f"Vote cast: {vote.support}")
print(f"Voting power: {vote.voting_power}")

# --- Quadratic Voting ---
qvote = voter.quadratic_vote(
    proposal_id=proposal.proposal_id,
    voter="0xABCD...",
    support="for",
    tokens_used=100,
)
print(f"Quadratic power: {qvote.voting_power:.0f} (sqrt of 100)")

# --- Delegation ---
delegation_mgr = DelegationManager()
delegation = delegation_mgr.delegate(
    delegator="0x1234...",
    delegate="0xDelegate...",
    token_amount=5000,
)
print(f"Delegation: {delegation.delegator} -> {delegation.delegate}")
print(f"Amount: {delegation.amount} tokens")

# --- Timelock ---
timelock = TimelockController(min_delay_hours=48)
execution = timelock.schedule(
    proposal_id=proposal.proposal_id,
    actions=[{"target": "0xContract", "value": 0, "data": "0x1234"}],
)
print(f"Scheduled: {execution.delay_hours}h delay")
print(f"Executes at: {execution.execute_after}")

# --- Governance Analytics ---
analytics = GovernanceAnalytics()
health = analytics.get_health_metrics()
print(f"Participation rate: {health.participation_rate:.1%}")
print(f"Proposal success rate: {health.success_rate:.1%}")
```

## Best Practices

- Implement timelock with minimum 48-hour delay for critical parameter changes
- Use quadratic voting for broader participation and Sybil resistance
- Require minimum token threshold for proposal submission to prevent spam
- Implement quorum requirements (10-20% of total supply) for valid votes
- Use off-chain signaling (Snapshot) before on-chain proposals for discussion
- Implement veto mechanism for security-critical governance actions
- Track delegation carefully — ensure delegators can revoke at any time
- Use multi-sig wallets for treasury management alongside DAO governance
- Publish governance analytics regularly for transparency
- Implement vote escrow (lock tokens for voting power multiplier) for long-term alignment

## Related Modules

- **token-analytics**: Token metrics for governance weight
- **wallet-integration**: Wallet-based governance interactions
- **defi-patterns**: Protocol governance parameters
- **nft-marketplace**: NFT governance and collection voting

---

## Advanced Configuration

### Governance Configuration

Configure governance parameters.

```python
governance_config = GovernanceConfig(
    proposal_threshold=10000,  # tokens to create proposal
    quorum_percentage=0.10,  # 10% of supply
    voting_period_days=7,
    timelock_delay_hours=48,
    emergency_delay_hours=0,
    veto_enabled=True,
    veto_threshold=0.33,  # 33% to veto
)
```

### Voting Configuration

Configure voting parameters.

```python
voting_config = VotingConfig(
    mechanisms={
        "token_weighted": {"enabled": True, "weight": "token_balance"},
        "quadratic": {"enabled": True, "cost_multiplier": "sqrt"},
        "conviction": {"enabled": True, "decay_rate": 0.87, "min_stake_days": 7},
        "multichoice": {"enabled": True, "max_options": 5},
    },
    delegation_enabled=True,
    vote_escrow_enabled=True,
    vote_escrow_lock_days=[7, 30, 90, 365],
)
```

### Treasury Configuration

Configure treasury management.

```python
treasury_config = TreasuryConfig(
    multi_sig={"threshold": 3, "owners": 5},
    spending_limits={
        "daily": 100000,  # USD
        "monthly": 1000000,
    },
    required_approvals={
        "small": 2,  # < $10K
        "medium": 3,  # $10K-$100K
        "large": 5,  # > $100K
    },
)
```

---

## Architecture Patterns

### Proposal Lifecycle Pattern

```python
class ProposalLifecycle:
    states = [
        "draft",
        "discussion",
        "voting",
        "passed",
        "timelock",
        "executed",
        "failed",
    ]

    def transition(self, proposal, new_state):
        if self.is_valid_transition(proposal.status, new_state):
            proposal.status = new_state
            self.emit_event(proposal, new_state)
```

### Vote Escrow Pattern

```python
class VoteEscrow:
    def lock(self, user, amount, duration_days):
        ve_token = veNFT(
            user=user,
            amount=amount,
            lock_end=block.timestamp + duration_days * 86400,
        )
        ve_token.weight = self.calculate_weight(amount, duration_days)
        return ve_token

    def calculate_weight(self, amount, days):
        return amount * (days / 365)  # Linear weight
```

### Delegation Pattern

```python
class DelegationManager:
    def delegate(self, delegator, delegate, token_amount):
        delegation = Delegation(
            delegator=delegator,
            delegate=delegate,
            amount=token_amount,
            created_at=block.timestamp,
        )
        # Transfer voting power
        self.voting_power[delegate] += token_amount
        self.voting_power[delegator] -= token_amount
        return delegation

    def revoke(self, delegation_id):
        delegation = self.delegations[delegation_id]
        self.voting_power[delegation.delegate] -= delegation.amount
        self.voting_power[delegation.delegator] += delegation.amount
```

---

## Integration Guide

### Snapshot Integration

```python
# Create off-chain proposal on Snapshot
snapshot = SnapshotAPI(space="mydao.eth")
proposal = snapshot.create_proposal(
    title="Increase staking rewards",
    body="Proposal to increase rewards...",
    choices=["For", "Against", "Abstain"],
    start_time=int(time.time()),
    end_time=int(time.time()) + 7 * 86400,
)
```

### Tally Integration

```python
# Track on-chain proposals with Tally
tally = TallyAPI(api_key="...")
proposals = tally.get_proposals(dao_address)
for p in proposals:
    print(f"{p.title}: {p.status} ({p.votes_for}/{p.votes_against})")
```

### Governor Contract Integration

```python
from web3 import Web3

governor = w3.eth.contract(address=governor_address, abi=governor_abi)

# Create proposal
tx = governor.functions.propose(
    targets, values, calldatas, description
).build_transaction({...})
```

---

## Performance Optimization

### Vote Counting Optimization

```python
# Cache vote totals
vote_cache = VoteCache(
    ttl_seconds=60,
    max_entries=1000,
)
```

### Proposal Indexing

```python
# Index proposals for fast querying
class ProposalIndex:
    def __init__(self):
        self.by_status = defaultdict(list)
        self.by_proposer = defaultdict(list)
        self.by_date = defaultdict(list)
```

---

## Security Considerations

### Flash Loan Voting Prevention

```python
# Snapshot voting power at proposal creation
def get_voting_power(address, block_number):
    # Use historical balance, not current
    return token.balanceOfAt(address, block_number)
```

### Timelock Security

```python
# Enforce minimum timelock for critical changes
class TimelockSecurity:
    def validate_delay(self, proposal_type, delay_hours):
        min_delay = self.get_min_delay(proposal_type)
        if delay_hours < min_delay:
            raise TimelockTooShort(f"Minimum delay: {min_delay}h")
```

### Emergency Procedures

```python
# Emergency governance actions
class EmergencyGovernance:
    def emergency_proposal(self, description, actions):
        proposal = self.create_proposal(
            description=description,
            actions=actions,
            voting_period_hours=24,  # Shortened
            timelock_hours=0,  # Immediate
        )
        return proposal
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Proposal rejected | Below threshold | Check token balance |
| Vote not counted | Snapshot mismatch | Vote at correct block |
| Execution failed | Timelock not expired | Wait for timelock |
| Quorum not met | Low participation | Extend voting period |

---

## API Reference

### ProposalManager

```python
class ProposalManager:
    def create_proposal(title, description, proposer, category) -> Proposal
    def get_proposal(proposal_id) -> Proposal
    def list_proposals(status, limit) -> List[Proposal]
    def execute_proposal(proposal_id) -> ExecutionResult
```

### VotingEngine

```python
class VotingEngine:
    def cast_vote(proposal_id, voter, support, voting_power) -> Vote
    def quadratic_vote(proposal_id, voter, support, tokens_used) -> Vote
    def get_vote(proposal_id, voter) -> Optional[Vote]
    def get_results(proposal_id) -> VotingResults
```

### TimelockController

```python
class TimelockController:
    def schedule(proposal_id, actions, delay_hours) -> ScheduledExecution
    def execute(proposal_id) -> ExecutionResult
    def cancel(proposal_id) -> None
    def get_pending() -> List[ScheduledExecution]
```

---

## Data Models

### Proposal

```python
@dataclass
class Proposal:
    proposal_id: str
    title: str
    description: str
    proposer: str
    category: str
    status: str
    voting_start: datetime
    voting_end: datetime
    votes_for: int
    votes_against: int
    quorum: int
```

### Vote

```python
@dataclass
class Vote:
    proposal_id: str
    voter: str
    support: str  # for, against, abstain
    voting_power: int
    timestamp: datetime
```

---

## Deployment Guide

### Governance Deployment

```bash
# Deploy Governor contract
forge create --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  src/Governor.sol:GovernorDAO \
  --constructor-args $TOKEN $TIMELOCK $VOTING_PERIOD $QUORUM
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `dao.proposal.count` | Active proposals | Anomaly |
| `dao.voting.participation` | Voter participation | < 5% |
| `dao.execution.success` | Execution success rate | < 0.95 |

---

## Testing Strategy

### Governance Tests

```python
def test_proposal_lifecycle():
    pm = ProposalManager()
    proposal = pm.create_proposal("Test", "Description", proposer, "parameter")
    assert proposal.status == "draft"

    voting = VotingEngine()
    voting.cast_vote(proposal.proposal_id, voter, "for", 1000)
    assert voting.get_results(proposal.proposal_id).votes_for == 1000
```

---

## Versioning & Migration

### Governor Versioning

Follow semantic versioning for governance contracts.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Quorum** | Minimum votes required for valid vote |
| **Timelock** | Delay between vote passing and execution |
| **Vote Escrow** | Locking tokens for increased voting power |
| **Delegation** | Assigning voting power to another address |
| **Proposal** | Formal suggestion for protocol changes |

---

## Changelog

### v2.0.0
- Added quadratic voting
- Vote escrow system
- Treasury management

### v1.0.0
- Initial release with basic token voting

---

## Contributing Guidelines

- Document all governance parameters
- Test proposal execution thoroughly
- Implement proper timelock delays

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

## Advanced Configuration

### Governor Configuration

```yaml
governance:
  governor: "openzeppelin"
  voting_period: 50400  # ~1 week in blocks
  voting_delay: 1       # 1 block delay
  quorum_percentage: 4  # 4% of total supply
  proposal_threshold: 100000  # tokens needed to propose
  timelock_delay: 172800  # 2 days in seconds
  grace_period: 1209600   # 14 days
```

### Voting Strategy Configuration

```yaml
voting_strategies:
  token_weighted:
    token_address: "0x..."
    weight_multiplier: 1.0
    snapshot_block: "latest"
  quadratic:
    token_address: "0x..."
    sqrt_function: true
  conviction:
    decay_rate: 0.95
    min_stake_days: 7
    max_multiplier: 10.0
  time_weighted:
    lock_durations:
      - days: 30
        multiplier: 1.0
      - days: 90
        multiplier: 1.5
      - days: 365
        multiplier: 3.0
```

## Architecture Patterns

### On-Chain Governance Architecture

```
Governance Stack:
├── Proposal Layer
│   ├── Proposal creation
│   ├── Discussion forum
│   ├── IPFS storage
│   └── Metadata indexing
├── Voting Layer
│   ├── Governor contract
│   ├── Token checkpointing
│   ├── Vote delegation
│   └── Quorum calculation
├── Execution Layer
│   ├── Timelock controller
│   ├── Multi-sig approval
│   ├── Batch execution
│   └── Emergency override
├── Treasury Layer
│   ├── Multi-sig wallet
│   ├── Budget allocation
│   └── Grant distribution
└── Analytics Layer
    ├── Participation metrics
    ├── Proposal outcomes
    └── Delegate activity
```

### Delegation Architecture

```
Delegation Flow:
├── Token Holder
│   ├── Direct voting
│   ├── Delegate selection
│   └── Delegation revocation
├── Delegate
│   ├── Voting power accumulation
│   ├── Proposal creation
│   ├── Voting execution
│   └── Transparency reporting
├── Snapshot
│   ├── Point-in-time balances
│   ├── Delegation snapshots
│   └── Historical lookups
└── Governance
    ├── Quorum calculation
    ├── Vote tallying
    └── Result execution
```

### Timelock Architecture

```
Timelock Flow:
├── Proposal Approved
│   ├── Queue in timelock
│   ├── Delay period
│   └── Grace period start
├── Execution Window
│   ├── Execute proposal
│   ├── Batch operations
│   └── Emergency cancel
├── State Management
│   ├── Pending → Ready → Executed
│   ├── Cancellation
│   └── Expiration
└── Security
    ├── Admin roles
    ├── Cancel authority
    └── Emergency procedures
```

### Treasury Management Architecture

```
Treasury Flow:
├── Revenue Sources
│   ├── Protocol fees
│   ├── Token minting
│   └── External grants
├── Allocation
│   ├── Core development
│   ├── Ecosystem grants
│   ├── Liquidity incentives
│   └── Emergency reserves
├── Proposals
│   ├── Budget proposals
│   ├── Grant applications
│   └── Emergency spending
└── Execution
    ├── Multi-sig approval
    ├── Timelock execution
    └── Accounting updates
```

## Integration Guide

### Governor Contract Integration

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/governance/Governor.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorSettings.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorCountingSimple.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotesQuorumFraction.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorTimelockControl.sol";

contract DaoGovernance is
    Governor,
    GovernorSettings,
    GovernorCountingSimple,
    GovernorVotes,
    GovernorVotesQuorumFraction,
    GovernorTimelockControl
{
    constructor(IVotes _token, ITimelockController _timelock)
        Governor("DaoGovernance")
        GovernorSettings(50400, 1, 4)  // votingPeriod, votingDelay, quorumPercent
        GovernorVotes(_token)
        GovernorVotesQuorumFraction(4)
        GovernorTimelockControl(_timelock)
    {}

    function votingDelay() public view override(Governor, GovernorSettings) returns (uint256) {
        return super.votingDelay();
    }

    function votingPeriod() public view override(Governor, GovernorSettings) returns (uint256) {
        return super.votingPeriod();
    }

    function quorum(uint256 blockNumber) public view override(Governor, GovernorVotesQuorumFraction) returns (uint256) {
        return super.quorum(blockNumber);
    }

    function state(uint256 proposalId) public view override(Governor, GovernorTimelockControl) returns (ProposalState) {
        return super.state(proposalId);
    }

    function _queueOperations(uint256 proposalId, address[] memory targets, uint256[] memory values, bytes[] memory calldatas, bytes32 descriptionHash) internal override(Governor, GovernorTimelockControl) returns (uint48) {
        return super._queueOperations(proposalId, targets, values, calldatas, descriptionHash);
    }

    function _executeOperations(uint256 proposalId, address[] memory targets, uint256[] memory values, bytes[] memory calldatas, bytes32 descriptionHash) internal override(Governor, GovernorTimelockControl) {
        super._executeOperations(proposalId, targets, values, calldatas, descriptionHash);
    }

    function _cancel(uint256 proposalId, address[] memory targets, uint256[] memory values, bytes[] memory calldatas, bytes32 descriptionHash) internal override(Governor, GovernorTimelockControl) returns (uint48) {
        return super._cancel(proposalId, targets, values, calldatas, descriptionHash);
    }
}
```

### Snapshot Integration

```python
import requests
import json

class SnapshotGovernance:
    def __init__(self, space, provider_url):
        self.space = space
        self.provider_url = provider_url
        self.snapshot_api = "https://hub.snapshot.org/graphql"

    def get_proposals(self, first=10, skip=0):
        """Fetch proposals from Snapshot."""
        query = """
        query Proposals($space: String!, $first: Int!, $skip: Int!) {
            proposals(
                first: $first
                skip: $skip
                where: { space: $space }
                orderBy: "created"
                orderDirection: desc
            ) {
                id
                title
                body
                choices
                start
                end
                state
                author
                scores
                scores_total
                voterCount
            }
        }
        """
        response = requests.post(
            self.snapshot_api,
            json={"query": query, "variables": {"space": self.space, "first": first, "skip": skip}}
        )
        return response.json()["data"]["proposals"]

    def get_votes(self, proposal_id):
        """Fetch votes for a proposal."""
        query = """
        query Votes($proposal: String!, $first: Int!) {
            votes(
                first: $first
                where: { proposal: $proposal }
                orderBy: "vp"
                orderDirection: desc
            ) {
                voter
                choice
                vp
                vp_by_strategy
                created
            }
        }
        """
        response = requests.post(
            self.snapshot_api,
            json={"query": query, "variables": {"proposal": proposal_id, "first": 1000}}
        )
        return response.json()["data"]["votes"]

    def create_proposal(self, title, body, choices, end_timestamp):
        """Create a new proposal (requires wallet signature)."""
        # Implementation requires EIP-712 signing
        pass
```

### Tally Integration

```python
class TallyGovernance:
    def __init__(self, api_key, governor_address):
        self.api_key = api_key
        self.governor_address = governor_address
        self.base_url = "https://api.tally.xyz/query"

    def get_proposals(self):
        """Fetch proposals from Tally."""
        query = """
        query Proposals($governor: Address!) {
            proposals(governor: $governor) {
                id
                title
                description
                status
                votes {
                    for
                    against
                    abstain
                }
                startBlock
                endBlock
            }
        }
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(
            self.base_url,
            json={"query": query, "variables": {"governor": self.governor_address}},
            headers=headers
        )
        return response.json()["data"]["proposals"]

    def get_delegates(self):
        """Fetch top delegates."""
        query = """
        query Delegates($governor: Address!) {
            delegates(governor: $governor, first: 100) {
                address
                votesCount
                proposalsCount
                votingPower
            }
        }
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(
            self.base_url,
            json={"query": query, "variables": {"governor": self.governor_address}},
            headers=headers
        )
        return response.json()["data"]["delegates"]
```

## Performance Optimization

### Gas Optimization

| Operation | Gas Cost | Optimization |
|-----------|----------|--------------|
| Proposal creation | ~200K | Use IPFS for metadata |
| Vote casting | ~50K | Batch votes |
| Queue execution | ~150K | Batch operations |
| Delegate update | ~30K | Minimize updates |

### Voting Power Optimization

```
Voting Power Strategies:
├── Token balancing
│   ├── Equalize across wallets
│   ├── Optimal delegation
│   └── Snapshot timing
├── Gas optimization
│   ├── Batch voting
│   ├── Off-chain signatures
│   └── Vote escrow
└── Delegation
    ├── Select active delegates
    ├── Monitor delegate activity
    └── Revote if needed
```

## Security Considerations

### Governance Attack Vectors

| Attack | Description | Mitigation |
|--------|-------------|------------|
| Flash loan voting | Borrow tokens to vote | Time-weighted voting |
| Proposal spam | Flood with proposals | Proposal threshold |
| Delegate collusion | Coordinate votes | Transparency requirements |
| Timelock bypass | Emergency override | Multi-sig requirements |
| Vote buying | Purchased votes | Quadratic voting |

### Security Best Practices

```
Security Layers:
├── Smart contract
│   ├── OpenZeppelin Governor
│   ├── Formal verification
│   ├── Audit reports
│   └── Bug bounty
├── Operational
│   ├── Multi-sig timelock
│   ├── Emergency procedures
│   └── Key management
├── Governance
│   ├── Proposal review process
│   ├── Discussion period
│   └── Quorum requirements
└── Monitoring
    ├── Anomaly detection
    ├── Activity alerts
    └── Governance dashboards
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Proposal fails | Cannot create proposal | Check token balance, proposal threshold |
| Vote not counted | Vote not reflected | Check snapshot block, voting power |
| Execution fails | Timelock execution error | Check timelock state, permissions |
| Low participation | Few voters | Increase incentives, improve communication |
| Gas estimation fails | Transaction reverts | Increase gas limit, check contract state |

### Debugging Commands

```bash
# Check proposal state
cast call $GOVERNOR "state(uint256)" $PROPOSAL_ID --rpc-url $RPC

# Check voting power
cast call $TOKEN "getVotes(address)" $VOTER --rpc-url $RPC --block $BLOCK

# Check quorum
cast call $GOVERNOR "quorum(uint256)" $BLOCK_NUMBER --rpc-url $RPC

# Check timelock
cast call $TIMELOCK "getMinDelay()" --rpc-url $RPC
```

## Testing Strategy

### Governance Testing

```
1. Unit Tests
   ├── Proposal creation
   ├── Vote casting
   ├── Quorum calculation
   └── Timelock operations

2. Integration Tests
   ├── Full governance flow
   ├── Delegation workflow
   ├── Multi-proposal scenarios
   └── Emergency procedures

3. Security Tests
   ├── Flash loan attack
   ├── Governance manipulation
   ├── Timelock bypass
   └── Vote buying

4. Gas Tests
   ├── Proposal creation gas
   ├── Vote casting gas
   ├── Execution gas
   └── Batch operation gas
```

## Versioning & Migration

### Versioning

```
Major: Protocol changes
├── Example: Change voting mechanism
├── Requires: Full governance vote
└── Risk: High

Minor: Parameter changes
├── Example: Adjust quorum threshold
├── Requires: Governance proposal
└── Risk: Medium

Patch: Bug fixes
├── Example: Fix vote counting
├── Requires: Emergency proposal
└── Risk: Low
```

## Glossary

| Term | Definition |
|------|-----------|
| Conviction Voting | Voting power increases with time staked |
| Delegate | Representative who votes on behalf of others |
| Governor | Smart contract managing governance |
| Quadratic Voting | Voting cost equals square of votes |
| Quorum | Minimum participation for valid vote |
| Timelock | Delay between approval and execution |
| Token Weighted | Voting power proportional to tokens |
| Tally | Governance dashboard platform |
| Snapshot | Off-chain voting platform |
| Vote Escrow | Locking tokens for voting power |

## Changelog

### v2.0.0
- Added quadratic voting
- Vote escrow system
- Treasury management

### v1.0.0
- Initial release with basic token voting
