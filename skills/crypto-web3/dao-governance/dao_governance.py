"""
DAO Governance Module
Proposals, voting, delegation, timelock, and analytics.
"""

from __future__ import annotations

import logging
import math
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ProposalStatus(Enum):
    DRAFT = "draft"
    PENDING = "pending"
    ACTIVE = "active"
    SUCCEEDED = "succeeded"
    DEFEATED = "defeated"
    QUEUED = "queued"
    EXECUTED = "executed"
    CANCELLED = "cancelled"


class VoteChoice(Enum):
    FOR = "for"
    AGAINST = "against"
    ABSTAIN = "abstain"


class ProposalCategory(Enum):
    PARAMETER_CHANGE = "parameter_change"
    TREASURY_SPEND = "treasury_spend"
    PROTOCOL_UPGRADE = "protocol_upgrade"
    METAGOVERNANCE = "metagovernance"
    EMERGENCY = "emergency"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Proposal:
    """Governance proposal."""
    proposal_id: str
    title: str
    description: str
    proposer: str
    category: ProposalCategory
    status: ProposalStatus = ProposalStatus.DRAFT
    for_votes: float = 0.0
    against_votes: float = 0.0
    abstain_votes: float = 0.0
    quorum: float = 100000
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    voting_start: Optional[datetime] = None
    voting_end: Optional[datetime] = None
    execution_delay_hours: int = 48

    @property
    def total_votes(self) -> float:
        return self.for_votes + self.against_votes + self.abstain_votes

    @property
    def quorum_reached(self) -> bool:
        return self.total_votes >= self.quorum

    @property
    def for_percentage(self) -> float:
        total = self.for_votes + self.against_votes
        return self.for_votes / max(total, 1)

    @property
    def passed(self) -> bool:
        return self.quorum_reached and self.for_percentage > 0.5


@dataclass
class Vote:
    """Governance vote."""
    vote_id: str
    proposal_id: str
    voter: str
    support: VoteChoice
    voting_power: float
    weight: float = 1.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_delegated: bool = False
    delegate: str = ""


@dataclass
class Delegation:
    """Vote delegation."""
    delegator: str
    delegate: str
    amount: float
    token: str = "GOV"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = True


@dataclass
class TimelockAction:
    """Timelock scheduled action."""
    proposal_id: str
    target: str
    value: float
    data: str
    delay_hours: int = 48
    execute_after: str = ""
    executed: bool = False


@dataclass
class GovernanceHealth:
    """Governance health metrics."""
    total_proposals: int = 0
    active_proposals: int = 0
    participation_rate: float = 0.0
    success_rate: float = 0.0
    avg_voting_power: float = 0.0
    unique_voters: int = 0
    delegation_ratio: float = 0.0


# ---------------------------------------------------------------------------
# Proposal Manager
# ---------------------------------------------------------------------------

class ProposalManager:
    """Manage governance proposals."""

    def __init__(self, min_tokens_to_propose: float = 1000):
        self._proposals: Dict[str, Proposal] = {}
        self.min_tokens = min_tokens_to_propose

    def create_proposal(
        self,
        title: str,
        description: str,
        proposer: str,
        category: str = "parameter_change",
        quorum: float = 100000,
    ) -> Proposal:
        proposal_id = f"PROP-{secrets.token_hex(4).upper()}"
        proposal = Proposal(
            proposal_id=proposal_id,
            title=title,
            description=description,
            proposer=proposer,
            category=ProposalCategory(category),
            quorum=quorum,
            voting_start=datetime.now(timezone.utc) + timedelta(days=1),
            voting_end=datetime.now(timezone.utc) + timedelta(days=8),
        )
        self._proposals[proposal_id] = proposal
        return proposal

    def activate(self, proposal_id: str) -> Optional[Proposal]:
        proposal = self._proposals.get(proposal_id)
        if proposal:
            proposal.status = ProposalStatus.ACTIVE
        return proposal

    def get_proposal(self, proposal_id: str) -> Optional[Proposal]:
        return self._proposals.get(proposal_id)

    def list_proposals(
        self, status: Optional[ProposalStatus] = None
    ) -> List[Proposal]:
        proposals = list(self._proposals.values())
        if status:
            proposals = [p for p in proposals if p.status == status]
        return proposals


# ---------------------------------------------------------------------------
# Voting Engine
# ---------------------------------------------------------------------------

class VotingEngine:
    """Cast and manage votes."""

    def __init__(self):
        self._votes: Dict[str, List[Vote]] = {}

    def cast_vote(
        self,
        proposal_id: str,
        voter: str,
        support: str,
        voting_power: float,
        weight: float = 1.0,
    ) -> Vote:
        vote = Vote(
            vote_id=f"VOTE-{secrets.token_hex(4).upper()}",
            proposal_id=proposal_id,
            voter=voter,
            support=VoteChoice(support),
            voting_power=voting_power,
            weight=weight,
        )
        if proposal_id not in self._votes:
            self._votes[proposal_id] = []
        self._votes[proposal_id].append(vote)
        return vote

    def quadratic_vote(
        self,
        proposal_id: str,
        voter: str,
        support: str,
        tokens_used: float,
    ) -> Vote:
        power = math.sqrt(tokens_used)
        return self.cast_vote(proposal_id, voter, support, power)

    def get_votes(self, proposal_id: str) -> List[Vote]:
        return self._votes.get(proposal_id, [])

    def tally(self, proposal_id: str) -> Dict[str, float]:
        votes = self.get_votes(proposal_id)
        return {
            "for": sum(v.voting_power for v in votes if v.support == VoteChoice.FOR),
            "against": sum(v.voting_power for v in votes if v.support == VoteChoice.AGAINST),
            "abstain": sum(v.voting_power for v in votes if v.support == VoteChoice.ABSTAIN),
            "total": len(votes),
        }


# ---------------------------------------------------------------------------
# Delegation Manager
# ---------------------------------------------------------------------------

class DelegationManager:
    """Manage vote delegations."""

    def __init__(self):
        self._delegations: Dict[str, Delegation] = {}

    def delegate(
        self,
        delegator: str,
        delegate: str,
        token_amount: float,
        token: str = "GOV",
    ) -> Delegation:
        delegation = Delegation(
            delegator=delegator,
            delegate=delegate,
            amount=token_amount,
            token=token,
        )
        self._delegations[f"{delegator}:{delegate}"] = delegation
        return delegation

    def revoke(self, delegator: str, delegate: str) -> bool:
        key = f"{delegator}:{delegate}"
        if key in self._delegations:
            self._delegations[key].active = False
            return True
        return False

    def get_delegations_to(self, delegate: str) -> List[Delegation]:
        return [
            d for d in self._delegations.values()
            if d.delegate == delegate and d.active
        ]

    def get_delegated_by(self, delegator: str) -> List[Delegation]:
        return [
            d for d in self._delegations.values()
            if d.delegator == delegator and d.active
        ]

    def total_delegated_to(self, delegate: str) -> float:
        return sum(d.amount for d in self.get_delegations_to(delegate))


# ---------------------------------------------------------------------------
# Timelock Controller
# ---------------------------------------------------------------------------

class TimelockController:
    """Time-locked governance execution."""

    def __init__(self, min_delay_hours: int = 48):
        self.min_delay = min_delay_hours
        self._scheduled: Dict[str, TimelockAction] = {}

    def schedule(
        self,
        proposal_id: str,
        actions: List[Dict[str, Any]],
        delay_hours: Optional[int] = None,
    ) -> TimelockAction:
        delay = max(delay_hours or self.min_delay, self.min_delay)
        execute_after = (datetime.now(timezone.utc) + timedelta(hours=delay)).isoformat()
        action = TimelockAction(
            proposal_id=proposal_id,
            target=actions[0].get("target", "") if actions else "",
            value=actions[0].get("value", 0) if actions else 0,
            data=actions[0].get("data", "0x") if actions else "0x",
            delay_hours=delay,
            execute_after=execute_after,
        )
        self._scheduled[proposal_id] = action
        return action

    def can_execute(self, proposal_id: str) -> bool:
        action = self._scheduled.get(proposal_id)
        if not action or action.executed:
            return False
        return datetime.now(timezone.utc).isoformat() >= action.execute_after

    def execute(self, proposal_id: str) -> bool:
        if self.can_execute(proposal_id):
            self._scheduled[proposal_id].executed = True
            return True
        return False

    def cancel(self, proposal_id: str) -> bool:
        if proposal_id in self._scheduled:
            del self._scheduled[proposal_id]
            return True
        return False


# ---------------------------------------------------------------------------
# Governance Analytics
# ---------------------------------------------------------------------------

class GovernanceAnalytics:
    """Analyze governance metrics."""

    def __init__(self):
        self._proposals: List[Proposal] = []
        self._votes: List[Vote] = []

    def get_health_metrics(self) -> GovernanceHealth:
        total = max(len(self._proposals), 1)
        active = sum(1 for p in self._proposals if p.status == ProposalStatus.ACTIVE)
        succeeded = sum(1 for p in self._proposals if p.status == ProposalStatus.SUCCEEDED)
        total_votes = sum(p.total_votes for p in self._proposals)
        unique_voters = len(set(v.voter for v in self._votes))
        return GovernanceHealth(
            total_proposals=len(self._proposals),
            active_proposals=active,
            participation_rate=min(1.0, total_votes / max(total * 100000, 1)),
            success_rate=succeeded / total,
            avg_voting_power=total_votes / max(len(self._votes), 1),
            unique_voters=unique_voters,
            delegation_ratio=0.3,
        )

    def voter_retention(self) -> float:
        if len(self._votes) < 2:
            return 0.0
        voters_per_proposal: Dict[str, set] = {}
        for vote in self._votes:
            if vote.proposal_id not in voters_per_proposal:
                voters_per_proposal[vote.proposal_id] = set()
            voters_per_proposal[vote.proposal_id].add(vote.voter)
        if len(voters_per_proposal) < 2:
            return 0.0
        prop_ids = list(voters_per_proposals.keys())
        first_voters = voters_per_proposals[prop_ids[0]]
        last_voters = voters_per_proposals[prop_ids[-1]]
        return len(first_voters & last_voters) / max(len(first_voters), 1)


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  DAO Governance Demo")
    print("=" * 60)

    print("\n[1] Create Proposal")
    pm = ProposalManager()
    proposal = pm.create_proposal(
        "Increase staking rewards by 5%",
        "Proposal to increase the base staking reward rate from 4% to 9% APY.",
        "0x1234",
        "parameter_change",
    )
    print(f"  ID: {proposal.proposal_id}")
    print(f"  Status: {proposal.status.value}")

    print("\n[2] Cast Votes")
    engine = VotingEngine()
    engine.cast_vote(proposal.proposal_id, "0xAlice", "for", 5000)
    engine.cast_vote(proposal.proposal_id, "0xBob", "for", 3000)
    engine.cast_vote(proposal.proposal_id, "0xCarol", "against", 2000)
    tally = engine.tally(proposal.proposal_id)
    print(f"  For: {tally['for']}, Against: {tally['against']}")
    print(f"  Total votes: {tally['total']}")

    print("\n[3] Quadratic Voting")
    qvote = engine.quadratic_vote(proposal.proposal_id, "0xDave", "for", 100)
    print(f"  Tokens: 100 -> Power: {qvote.voting_power:.0f}")

    print("\n[4] Delegation")
    del_mgr = DelegationManager()
    delegation = del_mgr.delegate("0xEve", "0xDelegate", 5000)
    print(f"  Delegated: {delegation.amount} GOV")
    print(f"  Total to delegate: {del_mgr.total_delegated_to('0xDelegate')}")

    print("\n[5] Timelock")
    timelock = TimelockController(min_delay_hours=48)
    execution = timelock.schedule(proposal.proposal_id, [{"target": "0xContract", "value": 0, "data": "0x1234"}])
    print(f"  Delay: {execution.delay_hours}h")
    print(f"  Execute after: {execution.execute_after}")
    print(f"  Can execute now: {timelock.can_execute(proposal.proposal_id)}")

    print("\n[6] Governance Analytics")
    analytics = GovernanceAnalytics()
    health = analytics.get_health_metrics()
    print(f"  Proposals: {health.total_proposals}")
    print(f"  Participation: {health.participation_rate:.1%}")

    print("\n" + "=" * 60)
    print("  DAO governance demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
