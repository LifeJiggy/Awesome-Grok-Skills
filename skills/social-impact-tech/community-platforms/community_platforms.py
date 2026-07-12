"""
community_platforms.py — Community Engagement, Moderation & Mutual Aid Toolkit

Provides discussion forums, content moderation pipelines, gamification engines,
mutual aid resource matching, event management, and community analytics.
"""

from __future__ import annotations

import math
import re
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable
from datetime import datetime, timedelta
from collections import defaultdict
import random


class ModerationAction(Enum):
    APPROVE = "approve"
    FLAG_FOR_REVIEW = "flag_for_review"
    REJECT = "reject"
    QUARANTINE = "quarantine"


class TrustLevel(Enum):
    NEWCOMER = 0
    BASIC = 1
    MEMBER = 2
    REGULAR = 3
    TRUSTED = 4
    LEADER = 5


class ContentType(Enum):
    POST = "post"
    COMMENT = "comment"
    MESSAGE = "message"
    EVENT = "event"
    RESOURCE = "resource"


class EventStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class UrgencyLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Member:
    member_id: str
    display_name: str
    email: str
    trust_level: TrustLevel = TrustLevel.NEWCOMER
    reputation: float = 0.0
    joined_at: datetime = field(default_factory=datetime.now)
    posts_count: int = 0
    helpful_count: int = 0
    moderation_flags: int = 0
    badges: list[str] = field(default_factory=list)

    @property
    def account_age_days(self) -> int:
        return (datetime.now() - self.joined_at).days


@dataclass
class Category:
    name: str
    description: str
    required_trust_level: TrustLevel = TrustLevel.NEWCOMER
    post_count: int = 0


@dataclass
class Topic:
    topic_id: str
    category: str
    author: Member
    title: str
    body: str
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    reply_count: int = 0
    views: int = 0
    pinned: bool = False
    closed: bool = False


@dataclass
class ModerationDecision:
    action: ModerationAction
    confidence: float
    reasons: list[str]
    flagged_patterns: list[str]


@dataclass
class ResourceOffer:
    provider_id: str
    skill: str
    availability: list[str]
    location: tuple[float, float]
    capacity: int = 1
    current_bookings: int = 0
    description: str = ""
    rating: float = 5.0

    @property
    def available_spots(self) -> int:
        return max(0, self.capacity - self.current_bookings)


@dataclass
class ResourceRequest:
    requester_id: str
    need: str
    urgency: UrgencyLevel
    location: tuple[float, float]
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class MatchResult:
    offer: ResourceOffer
    request: ResourceRequest
    score: float
    distance_km: float
    reason: str


@dataclass
class CommunityEvent:
    event_id: str
    title: str
    date: str
    time: str
    location: str
    max_attendees: int
    volunteer_roles: list[str]
    status: EventStatus = EventStatus.DRAFT
    rsvps: dict[str, str] = field(default_factory=dict)
    feedback: list[dict] = field(default_factory=list)

    @property
    def attendee_count(self) -> int:
        return len(self.rsvps)

    @property
    def spots_remaining(self) -> int:
        return max(0, self.max_attendees - self.attendee_count)


@dataclass
class TopicSummary:
    topic_id: str
    title: str
    author: str
    replies: int
    views: int
    activity_score: float


class SpamPatterns:
    PATTERNS = [
        (r"(buy|sell|discount|free money|click here|act now)", 0.4),
        (r"(viagra|cialis|bitcoin investment|wire transfer)", 0.8),
        (r"(http[s]?://[^\s]+){3,}", 0.5),
        (r"(!{3,}|I LOVE THIS|AMAZING DEAL)", 0.3),
        (r"(follow me|check my|visit my)", 0.3),
    ]
    HATE_SPEECH_PATTERNS = [
        (r"\b(slur_pattern_placeholder)\b", 0.9),
        (r"\b(kill all|exterminate)\b", 0.95),
    ]


class CommunityForum:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.categories: dict[str, Category] = {}
        self.members: dict[str, Member] = {}
        self.topics: dict[str, Topic] = {}
        self._topic_counter = 0

    def add_category(self, category: Category) -> None:
        self.categories[category.name] = category

    def register_member(self, member_id: str, display_name: str, email: str) -> Member:
        if member_id in self.members:
            raise ValueError(f"Member '{member_id}' already exists")
        member = Member(member_id=member_id, display_name=display_name, email=email)
        self.members[member_id] = member
        return member

    def post_topic(
        self,
        category: str,
        author: Member,
        title: str,
        body: str,
        tags: list[str] | None = None,
    ) -> Topic:
        if category not in self.categories:
            raise ValueError(f"Category '{category}' not found")

        cat = self.categories[category]
        if author.trust_level.value < cat.required_trust_level.value:
            raise PermissionError(
                f"Trust level {author.trust_level.value} insufficient for category '{category}' "
                f"(requires {cat.required_trust_level.value})"
            )

        self._topic_counter += 1
        topic_id = f"topic_{self._topic_counter}"
        topic = Topic(
            topic_id=topic_id,
            category=category,
            author=author,
            title=title,
            body=body,
            tags=tags or [],
        )
        self.topics[topic_id] = topic
        author.posts_count += 1
        author.reputation += 2.0
        cat.post_count += 1
        return topic

    def get_trending_topics(self, limit: int = 10) -> list[TopicSummary]:
        summaries = []
        for topic in self.topics.values():
            hours_since = max(1, (datetime.now() - topic.created_at).total_seconds() / 3600)
            activity_score = (topic.reply_count * 2 + topic.views * 0.1) / math.log(hours_since + 1)
            summaries.append(TopicSummary(
                topic_id=topic.topic_id,
                title=topic.title,
                author=topic.author.display_name,
                replies=topic.reply_count,
                views=topic.views,
                activity_score=round(activity_score, 2),
            ))
        summaries.sort(key=lambda s: s.activity_score, reverse=True)
        return summaries[:limit]


class ModerationPipeline:
    def __init__(self, auto_filter: bool = True, human_review_threshold: float = 0.7):
        self.auto_filter = auto_filter
        self.human_review_threshold = human_review_threshold
        self.flagged_content: list[dict] = []

    def evaluate(
        self,
        content: str,
        author_reputation: float = 50.0,
        author_age_days: int = 30,
    ) -> ModerationDecision:
        spam_score = self._check_spam_patterns(content)
        new_account_modifier = max(0, (30 - author_age_days) / 30) * 0.2
        spam_score = min(1.0, spam_score + new_account_modifier)

        if spam_score >= 0.8:
            action = ModerationAction.REJECT
        elif spam_score >= self.human_review_threshold:
            action = ModerationAction.FLAG_FOR_REVIEW
        elif spam_score >= 0.4:
            action = ModerationAction.QUARANTINE
        else:
            action = ModerationAction.APPROVE

        reasons = []
        flagged = []

        if spam_score > 0.3:
            reasons.append(f"Spam score: {spam_score:.2f}")
        if author_age_days < 7:
            reasons.append(f"New account ({author_age_days} days old)")
        if author_reputation < 10:
            reasons.append(f"Low reputation ({author_reputation})")

        patterns = SpamPatterns.PATTERNS + SpamPatterns.HATE_SPEECH_PATTERNS
        for pattern, _ in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                flagged.append(pattern)

        if action != ModerationAction.APPROVE:
            self.flagged_content.append({
                "content": content[:200],
                "action": action.value,
                "spam_score": spam_score,
                "reasons": reasons,
                "timestamp": datetime.now().isoformat(),
            })

        return ModerationDecision(
            action=action,
            confidence=1.0 - spam_score if action == ModerationAction.APPROVE else spam_score,
            reasons=reasons,
            flagged_patterns=flagged,
        )

    def _check_spam_patterns(self, content: str) -> float:
        scores = []
        for pattern, weight in SpamPatterns.PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                scores.append(weight)
        return max(scores) if scores else 0.0

    def get_moderation_stats(self) -> dict:
        if not self.flagged_content:
            return {"total_flagged": 0, "actions": {}}
        actions = defaultdict(int)
        for item in self.flagged_content:
            actions[item["action"]] += 1
        return {"total_flagged": len(self.flagged_content), "actions": dict(actions)}


class GamificationEngine:
    BADGE_RULES = {
        "first_post": lambda m: m.posts_count >= 1,
        "prolific_helper": lambda m: m.helpful_count >= 10,
        "trusted_member": lambda m: m.reputation >= 100,
        "community_veteran": lambda m: m.account_age_days >= 365,
        "moderator": lambda m: m.trust_level.value >= TrustLevel.TRUSTED.value,
    }
    REPONSE_POINTS = {"post": 2, "helpful": 5, "moderation": 3, "event_organize": 10}

    def __init__(self):
        self.leaderboard: list[dict] = []

    def award_points(self, member: Member, action: str, multiplier: float = 1.0) -> float:
        points = self.REPONSE_POINTS.get(action, 0) * multiplier
        member.reputation += points
        return points

    def check_and_award_badges(self, member: Member) -> list[str]:
        new_badges = []
        for badge_name, rule_func in self.BADGE_RULES.items():
            if badge_name not in member.badges and rule_func(member):
                member.badges.append(badge_name)
                new_badges.append(badge_name)
        return new_badges

    def update_trust_level(self, member: Member) -> TrustLevel:
        rep = member.reputation
        age = member.account_age_days

        if rep >= 500 and age >= 180 and member.moderation_flags == 0:
            new_level = TrustLevel.LEADER
        elif rep >= 200 and age >= 90:
            new_level = TrustLevel.TRUSTED
        elif rep >= 50 and age >= 30:
            new_level = TrustLevel.REGULAR
        elif rep >= 10 and age >= 7:
            new_level = TrustLevel.MEMBER
        elif rep >= 2:
            new_level = TrustLevel.BASIC
        else:
            new_level = TrustLevel.NEWCOMER

        member.trust_level = new_level
        return new_level

    def generate_leaderboard(self, members: list[Member], limit: int = 10) -> list[dict]:
        sorted_members = sorted(members, key=lambda m: m.reputation, reverse=True)
        leaderboard = []
        for i, member in enumerate(sorted_members[:limit]):
            leaderboard.append({
                "rank": i + 1,
                "member_id": member.member_id,
                "display_name": member.display_name,
                "reputation": member.reputation,
                "trust_level": member.trust_level.value,
                "badges": len(member.badges),
            })
        return leaderboard


class MutualAidMatcher:
    def __init__(self, radius_km: float = 10.0):
        self.radius_km = radius_km
        self.offers: list[ResourceOffer] = []
        self.requests: list[ResourceRequest] = []

    def add_offer(self, offer: ResourceOffer) -> None:
        self.offers.append(offer)

    def add_request(self, request: ResourceRequest) -> None:
        self.requests.append(request)

    def _haversine_distance(self, loc1: tuple[float, float], loc2: tuple[float, float]) -> float:
        lat1, lon1 = math.radians(loc1[0]), math.radians(loc1[1])
        lat2, lon2 = math.radians(loc2[0]), math.radians(loc2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        return 6371 * c

    def _compute_match_score(
        self,
        offer: ResourceOffer,
        request: ResourceRequest,
    ) -> tuple[float, str]:
        distance = self._haversine_distance(offer.location, request.location)
        if distance > self.radius_km:
            return 0.0, "Outside radius"

        distance_score = max(0, 1.0 - (distance / self.radius_km))
        skill_match = 1.0 if offer.skill.lower() in request.need.lower() or request.need.lower() in offer.skill.lower() else 0.3
        availability_score = 1.0 if offer.available_spots > 0 else 0.0
        urgency_multiplier = {
            UrgencyLevel.CRITICAL: 1.5,
            UrgencyLevel.HIGH: 1.2,
            UrgencyLevel.MEDIUM: 1.0,
            UrgencyLevel.LOW: 0.8,
        }.get(request.urgency, 1.0)

        raw_score = (distance_score * 0.4 + skill_match * 0.4 + availability_score * 0.2) * urgency_multiplier
        reason = f"Distance={distance:.1f}km, Skill match={skill_match}, Spots={offer.available_spots}"

        return min(1.0, raw_score), reason

    def find_matches(self, limit: int = 10) -> list[MatchResult]:
        all_matches: list[MatchResult] = []

        for request in self.requests:
            for offer in self.offers:
                if offer.available_spots <= 0:
                    continue
                score, reason = self._compute_match_score(offer, request)
                if score > 0:
                    distance = self._haversine_distance(offer.location, request.location)
                    all_matches.append(MatchResult(
                        offer=offer,
                        request=request,
                        score=round(score, 3),
                        distance_km=round(distance, 2),
                        reason=reason,
                    ))

        all_matches.sort(key=lambda m: m.score, reverse=True)
        return all_matches[:limit]


class EventManager:
    def __init__(self):
        self.events: dict[str, CommunityEvent] = {}
        self._event_counter = 0

    def create_event(
        self,
        title: str,
        date: str,
        time: str,
        location: str,
        max_attendees: int,
        volunteer_roles: list[str] | None = None,
    ) -> CommunityEvent:
        self._event_counter += 1
        event_id = f"event_{self._event_counter}"
        event = CommunityEvent(
            event_id=event_id,
            title=title,
            date=date,
            time=time,
            location=location,
            max_attendees=max_attendees,
            volunteer_roles=volunteer_roles or [],
            status=EventStatus.PUBLISHED,
        )
        self.events[event_id] = event
        return event

    def rsvp(self, event_id: str, member_id: str, role: str | None = None) -> bool:
        event = self.events.get(event_id)
        if not event:
            raise ValueError(f"Event '{event_id}' not found")
        if event.spots_remaining == 0:
            return False
        event.rsvps[member_id] = role or "attendee"
        return True

    def cancel_rsvp(self, event_id: str, member_id: str) -> bool:
        event = self.events.get(event_id)
        if not event or member_id not in event.rsvps:
            return False
        del event.rsvps[member_id]
        return True

    def get_rsvp_count(self, event_id: str) -> int:
        event = self.events.get(event_id)
        return event.attendee_count if event else 0

    def add_feedback(self, event_id: str, member_id: str, rating: int, comment: str = "") -> None:
        event = self.events.get(event_id)
        if event:
            event.feedback.append({
                "member_id": member_id,
                "rating": max(1, min(5, rating)),
                "comment": comment,
                "timestamp": datetime.now().isoformat(),
            })

    def get_event_analytics(self, event_id: str) -> dict:
        event = self.events.get(event_id)
        if not event:
            return {}
        ratings = [f["rating"] for f in event.feedback] if event.feedback else [0]
        roles = defaultdict(int)
        for role in event.rsvps.values():
            roles[role] += 1
        return {
            "event_id": event_id,
            "title": event.title,
            "status": event.status.value,
            "attendees": event.attendee_count,
            "capacity_utilization": event.attendee_count / event.max_attendees if event.max_attendees else 0,
            "role_distribution": dict(roles),
            "average_rating": round(sum(ratings) / len(ratings), 2),
            "feedback_count": len(event.feedback),
        }


class CommunityAnalytics:
    def __init__(self, forum: CommunityForum):
        self.forum = forum

    def get_health_metrics(self) -> dict:
        members = list(self.forum.members.values())
        if not members:
            return {"member_count": 0}

        total_posts = sum(m.posts_count for m in members)
        total_helpful = sum(m.helpful_count for m in members)
        avg_reputation = sum(m.reputation for m in members) / len(members)
        newcomer_count = sum(1 for m in members if m.account_age_days < 30)
        veteran_count = sum(1 for m in members if m.account_age_days >= 365)

        return {
            "member_count": len(members),
            "total_posts": total_posts,
            "total_helpful_answers": total_helpful,
            "average_reputation": round(avg_reputation, 2),
            "newcomer_count_30d": newcomer_count,
            "veteran_count_1y": veteran_count,
            "newcomer_ratio": round(newcomer_count / len(members), 3) if members else 0,
            "engagement_depth": round(total_helpful / max(total_posts, 1), 2),
            "category_stats": {name: cat.post_count for name, cat in self.forum.categories.items()},
        }

    def detect_power_law(self) -> dict:
        members = sorted(self.forum.members.values(), key=lambda m: m.posts_count, reverse=True)
        if not members:
            return {"gini": 0, "top_10_percent_posts": 0}

        posts = [m.posts_count for m in members]
        total_posts = sum(posts)
        if total_posts == 0:
            return {"gini": 0, "top_10_percent_posts": 0}

        n = len(posts)
        sorted_posts = sorted(posts)
        cumulative = 0
        gini_sum = 0
        for i, val in enumerate(sorted_posts):
            cumulative += val
            gini_sum += (2 * (i + 1) - n - 1) * val
        gini = gini_sum / (n * total_posts) if n > 0 else 0

        top_10_count = max(1, n // 10)
        top_10_posts = sum(posts[:top_10_count])

        return {
            "gini_coefficient": round(gini, 3),
            "top_10_percent_posts": round(top_10_posts / total_posts, 3),
            "most_active_member": members[0].display_name if members else None,
            "least_active_posts": posts[-1] if posts else 0,
        }


def main() -> None:
    print("=== Community Platforms Demo ===\n")

    # 1. Forum Setup
    print("--- Forum Setup ---")
    forum = CommunityForum("Greenway Gardens", "Community garden coordination")
    forum.add_category(Category(name="Offers", description="Available resources"))
    forum.add_category(Category(name="Requests", description="What people need"))
    forum.add_category(Category(name="Discussions", description="General chat", required_trust_level=TrustLevel.MEMBER))

    alice = forum.register_member("alice", "Alice Chen", "alice@example.com")
    bob = forum.register_member("bob", "Bob Johnson", "bob@example.com")
    carol = forum.register_member("carol", "Carol Davis", "carol@example.com")

    engine = GamificationEngine()
    engine.award_points(alice, "post")
    engine.award_points(alice, "helpful", multiplier=2)
    alice.reputation = 155
    engine.update_trust_level(alice)

    topic1 = forum.post_topic("Offers", alice, "Free Seedlings", "I have extra tomato seedlings to share!", tags=["plants", "free"])
    print(f"  Posted: {topic1.title} by {topic1.author.display_name}")

    # 2. Moderation
    print("\n--- Moderation ---")
    pipeline = ModerationPipeline(human_review_threshold=0.7)
    decisions = [
        pipeline.evaluate("Great tips on composting, thanks!", 85, 60),
        pipeline.evaluate("Buy my AMAZING product!!! Click here!!!", 3, 1),
        pipeline.evaluate("I'd like to volunteer at the garden this weekend.", 45, 14),
    ]
    for d in decisions:
        print(f"  {d.action.value}: confidence={d.confidence:.2f}, reasons={d.reasons}")

    # 3. Mutual Aid
    print("\n--- Mutual Aid Matching ---")
    matcher = MutualAidMatcher(radius_km=15)
    matcher.add_offer(ResourceOffer("bob", "woodworking", ["weekday_morning"], (40.7128, -74.006), capacity=2))
    matcher.add_request(ResourceRequest("maria", "furniture repair", UrgencyLevel.MEDIUM, (40.715, -74.008)))
    matches = matcher.find_matches()
    for m in matches:
        print(f"  Score={m.score:.3f}, Distance={m.distance_km}km — {m.reason}")

    # 4. Events
    print("\n--- Event Management ---")
    em = EventManager()
    event = em.create_event("Spring Planting", "2026-04-15", "09:00", "Community Garden", 20, ["Gardener", "Helper"])
    em.rsvp(event.event_id, "alice", "Gardener")
    em.rsvp(event.event_id, "bob", "Helper")
    em.add_feedback(event.event_id, "alice", 5, "Great event!")
    analytics = em.get_event_analytics(event.event_id)
    print(f"  Attendees: {analytics['attendees']}, Avg rating: {analytics['average_rating']}")

    # 5. Community Health
    print("\n--- Community Analytics ---")
    ca = CommunityAnalytics(forum)
    health = ca.get_health_metrics()
    print(f"  Members: {health['member_count']}, Posts: {health['total_posts']}")
    print(f"  Avg reputation: {health['average_reputation']}")
    power_law = ca.detect_power_law()
    print(f"  Gini coefficient: {power_law['gini_coefficient']}")

    # 6. Gamification
    print("\n--- Gamification ---")
    badges = engine.check_and_award_badges(alice)
    print(f"  Alice earned badges: {badges}")
    lb = engine.generate_leaderboard(list(forum.members.values()))
    for entry in lb:
        print(f"  #{entry['rank']} {entry['display_name']} — rep: {entry['reputation']}")


if __name__ == "__main__":
    main()
