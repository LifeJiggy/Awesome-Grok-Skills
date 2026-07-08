---
name: "Social Media Agent"
version: "2.0.0"
description: "Social media management - content scheduling, engagement analytics, audience insights, influencer marketing, reputation monitoring"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["social-media", "content", "engagement", "analytics", "influencer", "reputation"]
category: "social"
personality: "social-strategist"
use_cases:
  - "content-scheduling"
  - "engagement-tracking"
  - "audience-analytics"
  - "influencer-marketing"
  - "reputation-monitoring"
  - "campaign-management"
  - "social-analytics"
  - "brand-monitoring"
---

# Social Media Agent

> Comprehensive social media management with content scheduling, engagement analytics, audience insights, influencer marketing, and reputation monitoring.

## Identity

The Social Agent is a full-lifecycle social media management platform. It handles content creation and scheduling across multiple platforms, tracks engagement with sentiment analysis, analyzes audience demographics and growth, manages influencer collaborations, and monitors brand reputation with crisis detection.

**Core principle:** Every post should reach the right audience at the right time. Every engagement should be understood. Every reputation signal should be tracked.

**Personality:** The agent is a data-driven social strategist who balances creative content with analytical rigor. It prioritizes authentic engagement over vanity metrics, proactive reputation management over reactive crisis response, and consistent presence over sporadic posting.

## Principles

1. **Platform-Native Content** - Respect each platform's rules and norms
2. **Data-Driven Decisions** - Let metrics guide content strategy
3. **Authentic Engagement** - Build genuine relationships, not vanity metrics
4. **Proactive Reputation** - Monitor before crises escalate
5. **Consistent Presence** - Regular, scheduled content builds trust
6. **Measure Everything** - If it can't be measured, it can't be improved
7. **Audience-First** - Content serves the audience, not the brand ego
8. **Cross-Platform Synergy** - Leverage strengths of each platform

## Capabilities

### 1. Content Management

```python
from agents.social.agent import SocialAgent, Platform, ContentType

agent = SocialAgent()

# Create a post
post = agent.content.create_post(
    platform=Platform.TWITTER,
    content="Excited to share our latest feature update!",
    content_type=ContentType.POST,
    hashtags=["#product", "#update"],
    mentions=["@partner"],
    media_urls=["https://example.com/image.jpg"]
)
# post.id = "post_a1b2c3d4"
# post.status = ContentStatus.DRAFT

# Create a thread (Twitter)
posts = agent.content.create_thread(
    platform=Platform.TWITTER,
    messages=[
        "Thread: 5 ways to improve your security posture (1/5)",
        "1. Enable MFA everywhere - it's the single most effective control (2/5)",
        "2. Use a password manager - never reuse passwords (3/5)",
        "3. Keep software updated - patches fix known vulnerabilities (4/5)",
        "4. Be skeptical of links - verify before clicking (5/5)",
    ],
    hashtags=["#security", "#cybersecurity"],
)
# Returns list of 5 connected posts

# Use templates
agent.content.add_template(
    "announcement",
    "Breaking: {{headline}}\n\n{{details}}\n\nLearn more: {{link}}"
)
rendered = agent.content.render_template("announcement", {
    "headline": "New Feature Launch",
    "details": "AI-powered threat detection now available for all plans",
    "link": "https://example.com/launch"
})

# Get content calendar
from datetime import datetime, timedelta
calendar = agent.content.get_calendar(
    start=datetime.now(),
    end=datetime.now() + timedelta(days=7),
    platform=Platform.TWITTER
)
# {
#   "2025-01-15": [
#     {"post_id": "post_abc", "time": "09:00", "content": "..."},
#     {"post_id": "post_def", "time": "14:00", "content": "..."}
#   ]
# }

# Publish post
result = agent.content.publish_post(post.id)
# {"status": "published", "platform_post_id": "tw_1234567890"}
```

**Supported Platforms:**
| Platform | Max Length | Max Hashtags | Special Features |
|----------|-----------|--------------|------------------|
| Twitter | 280 | 5 | Threads, Polls |
| LinkedIn | 3,000 | 5 | Articles, Newsletters |
| Instagram | 2,200 | 30 | Reels, Carousels, Stories |
| YouTube | 5,000 | 15 | Shorts, Premieres |
| TikTok | 2,200 | 10 | Duet, Stitch |

### 2. Engagement Tracking

```python
from agents.social.agent import EngagementType

# Track engagement
eng = agent.engagement.track_engagement(
    post_id=post.id,
    user_id="user_123",
    username="techfan",
    engagement_type=EngagementType.COMMENT,
    content="This is exactly what we needed! Great update.",
    platform=Platform.TWITTER
)
# eng.sentiment = SentimentType.POSITIVE
# eng.id = "eng_x1y2z3"

# Track multiple engagements
agent.engagement.track_engagement(post.id, "user_456", "developer1", EngagementType.LIKE)
agent.engagement.track_engagement(post.id, "user_789", "securitypro", EngagementType.SHARE)

# Get engagement metrics
metrics = agent.engagement.get_engagement_metrics(post.id)
# {
#   "total_engagements": 42,
#   "by_type": {"like": 30, "comment": 8, "share": 4},
#   "sentiment_breakdown": {"positive": 35, "neutral": 5, "negative": 2},
#   "engagement_rate": 0.045
# }

# Find top engagers
top = agent.engagement.get_top_engagers(limit=5)
# [
#   {"username": "poweruser", "engagements": 15, "sentiment": "positive"},
#   {"username": "techfan", "engagements": 12, "sentiment": "positive"},
#   ...
# ]

# Sentiment trend
trend = agent.engagement.get_sentiment_trend(days=7)
# [
#   {"date": "2025-01-15", "positive": 45, "neutral": 10, "negative": 3},
#   {"date": "2025-01-14", "positive": 42, "neutral": 8, "negative": 5},
#   ...
# ]

# Create automation
automation = agent.engagement.create_automation(
    trigger="comment_contains_question",
    action="auto_reply_thanks",
    conditions={"sentiment": "positive", "min_engagements": 1},
    name="Thank positive commenters"
)
```

**Engagement Types:**
| Type | Value | Response Priority |
|------|-------|-------------------|
| LIKE | 1 | None |
| COMMENT | 5 | High (if question/complaint) |
| SHARE | 3 | Medium (acknowledge advocacy) |
| MENTION | 2 | Medium (if positive) |
| SAVE | 2 | None |
| CLICK | 1 | Track for analytics |

### 3. Audience Analytics

```python
# Add audience data
agent.audience.add_audience_data(Platform.TWITTER, {
    "followers": 25000,
    "growth_rate": 0.03,
    "engagement_rate": 0.045,
    "active_hours": [9, 12, 14, 18, 20],
    "demographics": {
        "18-24": 0.15,
        "25-34": 0.40,
        "35-44": 0.30,
        "45+": 0.15
    },
    "locations": {"US": 0.45, "UK": 0.20, "Canada": 0.15, "Other": 0.20}
})

# Get optimal posting times
times = agent.audience.get_optimal_posting_times(Platform.TWITTER)
# [
#   {"hour": 18, "score": 5, "engagement_rate": 0.067},
#   {"hour": 12, "score": 4, "engagement_rate": 0.052},
#   {"hour": 9, "score": 3, "engagement_rate": 0.048}
# ]

# Cross-platform overlap
overlap = agent.audience.analyze_cross_platform_overlap()
# {
#   "twitter_linkedin": 0.25,
#   "twitter_instagram": 0.15,
#   "linkedin_instagram": 0.10,
#   "unique_per_platform": {
#     "twitter": 0.40,
#     "linkedin": 0.35,
#     "instagram": 0.50
#   }
# }

# Growth recommendations
recs = agent.audience.get_growth_recommendations()
# [
#   {
#     "platform": "twitter",
#     "recommendation": "Post more video content",
#     "reason": "Video posts have 2x engagement",
#     "priority": "high"
#   },
#   ...
# ]

# Get total reach
total = agent.audience.get_total_reach()
# {"followers": 75000, "unique_reach": 45000, "overlap_rate": 0.40}
```

**Audience Metrics:**
| Metric | Formula | Description |
|--------|---------|-------------|
| Growth Rate | (current - previous) / previous × 100 | Follower growth |
| Engagement Rate | (likes + comments + shares) / followers × 100 | Activity level |
| Active Hours | Hour with highest engagement | Best posting times |
| Demographics | Age/gender/location breakdown | Audience composition |
| Overlap Rate | Shared followers / total followers | Cross-platform uniqueness |

### 4. Performance Analytics

```python
# Calculate KPIs
kpis = agent.analytics.calculate_kpis()
# {
#   "total_posts": 150,
#   "total_engagements": 4500,
#   "avg_engagement_rate": 0.038,
#   "total_followers": 50000,
#   "follower_growth": 0.05,
#   "total_reach": 125000,
#   "total_impressions": 450000,
#   "click_through_rate": 0.025,
#   "share_of_voice": 0.22,
#   "sentiment_score": 0.78
# }

# Get top posts
top = agent.analytics.get_top_performing_posts(limit=5)
# [
#   {
#     "post_id": "post_abc",
#     "platform": "twitter",
#     "content": "Excited to announce...",
#     "engagements": 245,
#     "engagement_rate": 0.089,
#     "sentiment": "very_positive"
#   },
#   ...
# ]

# Platform breakdown
breakdown = agent.analytics.get_platform_breakdown()
# {
#   "twitter": {"posts": 80, "engagements": 2500, "engagement_rate": 0.042},
#   "linkedin": {"posts": 40, "engagements": 1200, "engagement_rate": 0.035},
#   "instagram": {"posts": 30, "engagements": 800, "engagement_rate": 0.032}
# }

# Generate report
report = agent.analytics.generate_report(period_days=30)
# {
#   "period": {"start": "2025-01-01", "end": "2025-01-31"},
#   "kpis": {...},
#   "top_posts": [...],
#   "platform_breakdown": {...},
#   "recommendations": [
#     "Increase video content on Instagram",
#     "Post more during evening hours",
#     ...
#   ]
# }
```

**KPI Definitions:**
| KPI | Target | Formula |
|-----|--------|---------|
| Engagement Rate | > 3% | engagements / impressions × 100 |
| Click-Through Rate | > 2% | clicks / impressions × 100 |
| Share of Voice | > 20% | brand_mentions / total_mentions × 100 |
| Sentiment Score | > 70% | positive / (positive + negative) × 100 |
| Follower Growth | > 2% monthly | new_followers / total_followers × 100 |

### 5. Influencer Marketing

```python
from agents.social.agent import InfluencerTier

# Add influencer
inf = agent.influencer.add_influencer(
    username="securityexpert",
    platform=Platform.TWITTER,
    followers=150000,
    engagement_rate=0.05,
    niche="cybersecurity",
    cost=2500.0,
    bio="Cybersecurity researcher and educator"
)
# inf.tier = InfluencerTier.MACRO
# inf.id = "inf_xyz789"

# Find top influencers by niche
top = agent.influencer.find_top_influencers("cybersecurity", limit=3)
# [
#   {"username": "securityexpert", "followers": 150000, "engagement_rate": 0.05},
#   {"username": "cyberguru", "followers": 85000, "engagement_rate": 0.07},
#   {"username": "infosecpro", "followers": 62000, "engagement_rate": 0.06}
# ]

# Find by tier
micro = agent.influencer.find_by_tier(InfluencerTier.MICRO)

# Record collaboration
collab = agent.influencer.record_collaboration(
    influencer_id=inf.id,
    campaign_id="camp_001",
    content_posts=3,
    total_reach=45000,
    total_engagements=2250,
    cost=2500.0,
    conversions=25,
    revenue=12500.0
)
# collab["roi"] = 400.0  # (12500 - 2500) / 2500 × 100

# Summary
summary = agent.influencer.get_influencer_summary()
# {
#   "total_influencers": 12,
#   "by_tier": {"nano": 5, "micro": 4, "macro": 2, "mega": 1},
#   "total_collaborations": 28,
#   "total_reach": 450000,
#   "avg_roi": 285.5,
#   "top_performer": "securityexpert"
# }
```

**Influencer Tiers:**
| Tier | Followers | Engagement | Typical Cost | Use Case |
|------|-----------|------------|--------------|----------|
| Nano | 1K-10K | 5-10% | $50-500 | Niche communities |
| Micro | 10K-100K | 3-5% | $500-5,000 | Targeted reach |
| Macro | 100K-1M | 1-3% | $5,000-50,000 | Brand campaigns |
| Mega | 1M+ | 0.5-2% | $50,000+ | Mass reach |

### 6. Reputation Monitoring

```python
from agents.social.agent import SentimentType, ReputationAlertLevel

# Add monitoring keywords
agent.reputation.add_keywords(["brandname", "productname", "@brandhandle"])

# Record event
event = agent.reputation.record_event(
    platform=Platform.TWITTER,
    event_type="mention",
    content="Love the new update from @brandname! Great work!",
    source="user_tweet",
    sentiment=SentimentType.POSITIVE,
    url="https://twitter.com/user/status/123"
)
# event.alert_level = ReputationAlertLevel.GREEN

# Crisis detection
crisis = agent.reputation.record_event(
    platform=Platform.TWITTER,
    event_type="complaint",
    content="@brandname is a scam, lost all my data, worst experience ever!",
    source="viral_tweet",
    sentiment=SentimentType.VERY_NEGATIVE,
    url="https://twitter.com/user/status/456"
)
# crisis.alert_level = ReputationAlertLevel.RED

# Reputation score
score = agent.reputation.get_reputation_score()
# {
#   "score": 72.5,
#   "level": "good",
#   "total_events": 1250,
#   "by_sentiment": {
#     "very_positive": 150,
#     "positive": 800,
#     "neutral": 200,
#     "negative": 80,
#     "very_negative": 20
#   },
#   "alert_level": "GREEN"
# }

# Recent events
recent = agent.reputation.get_recent_events(limit=10)
# [
#   {
#     "platform": "twitter",
#     "event_type": "mention",
#     "sentiment": "positive",
#     "alert_level": "green",
#     "content": "Love the new feature..."
#   },
#   ...
# ]

# Crisis detection
crisis_check = agent.reputation.detect_crisis()
# {
#   "crisis_detected": False,
#   "negative_trend": False,
#   "recent_negative_count": 5,
#   "threshold": 10,
#   "recommendation": "Continue monitoring"
# }
```

**Alert Levels:**
| Level | Condition | Response Time |
|-------|-----------|---------------|
| GREEN | Positive/neutral sentiment | Monitor |
| YELLOW | Negative sentiment trend | 24 hours |
| ORANGE | Very negative sentiment | 4 hours |
| RED | Crisis keywords detected | 15 minutes |

### 7. Campaign Management

```python
# Create campaign
campaign = agent.create_campaign(
    name="Q1 Product Launch",
    description="Multi-platform launch campaign",
    platforms=[Platform.TWITTER, Platform.LINKEDIN, Platform.INSTAGRAM],
    start_date=datetime(2025, 1, 15),
    end_date=datetime(2025, 2, 15),
    budget=10000.0,
    goals={"reach": 100000, "engagement_rate": 0.05, "conversions": 500}
)
# campaign.id = "camp_launch_q1"

# Schedule batch
agent.schedule_content_batch([
    {
        "platform": "twitter",
        "content": "Launch day! Excited to announce...",
        "scheduled_at": "2025-01-15T09:00:00"
    },
    {
        "platform": "linkedin",
        "content": "We're thrilled to announce our enterprise solution...",
        "scheduled_at": "2025-01-15T10:00:00"
    },
    {
        "platform": "instagram",
        "content": "New beginnings! Check out our latest...",
        "scheduled_at": "2025-01-15T12:00:00"
    }
])

# Get campaign summary
summary = agent.get_campaign_summary(campaign.id)
# {
#   "campaign_id": "camp_launch_q1",
#   "status": "active",
#   "days_remaining": 25,
#   "posts_scheduled": 12,
#   "posts_published": 8,
#   "total_engagements": 1250,
#   "budget_spent": 3500.0,
#   "budget_remaining": 6500.0
# }
```

### 8. Unified Dashboard

```python
dashboard = agent.get_social_dashboard()
# {
#   "kpis": {
#     "total_posts": 150,
#     "total_engagements": 4500,
#     "avg_engagement_rate": 0.038,
#     "follower_growth": 0.05
#   },
#   "audience": {
#     "total_followers": 50000,
#     "growth_rate": 0.05,
#     "top_platform": "twitter"
#   },
#   "reputation": {
#     "score": 72.5,
#     "level": "good",
#     "alert_level": "GREEN"
#   },
#   "influencers": {
#     "total_influencers": 12,
#     "avg_roi": 285.5
#   },
#   "top_posts": [...],
#   "recommendations": [
#     "Increase video content on Instagram",
#     "Post more during evening hours",
#     "Engage with top commenters"
#   ]
# }
```

## Method Signatures

```python
class SocialAgent:
    def create_campaign(self, name: str, description: str, platforms: List[Platform], start_date: datetime, end_date: Optional[datetime] = None, budget: Optional[float] = None) -> Campaign
    def schedule_content_batch(self, posts_data: List[Dict]) -> Dict
    def respond_to_mentions(self, keyword: str) -> List[Dict]
    def get_social_dashboard(self) -> Dict
    def get_campaign_summary(self, campaign_id: str) -> Dict

class ContentManager:
    def create_post(self, platform: Platform, content: str, content_type: ContentType = ContentType.POST, scheduled_at: Optional[datetime] = None, hashtags: Optional[List[str]] = None, mentions: Optional[List[str]] = None, media_urls: Optional[List[str]] = None, author_id: Optional[str] = None) -> SocialPost
    def create_thread(self, platform: Platform, messages: List[str], hashtags: Optional[List[str]] = None) -> List[SocialPost]
    def add_template(self, name: str, template: str, platform: Optional[Platform] = None, variables: Optional[List[str]] = None) -> None
    def render_template(self, template_name: str, variables: Dict[str, str]) -> Optional[str]
    def get_calendar(self, start: datetime, end: datetime, platform: Optional[Platform] = None) -> Dict
    def publish_post(self, post_id: str) -> Dict
    def update_post(self, post_id: str, content: Optional[str] = None, hashtags: Optional[List[str]] = None) -> SocialPost
    def delete_post(self, post_id: str) -> bool
    def validate_content(self, platform: Platform, content: str) -> Dict

class EngagementManager:
    def track_engagement(self, post_id: str, user_id: str, username: str, engagement_type: EngagementType, content: Optional[str] = None, platform: Optional[Platform] = None) -> Engagement
    def respond_to_engagement(self, engagement_id: str, response: str) -> Dict
    def create_automation(self, trigger: str, action: str, conditions: Optional[Dict] = None, name: Optional[str] = None) -> Dict
    def get_engagement_metrics(self, post_id: str) -> Dict
    def get_top_engagers(self, limit: int = 10) -> List[Dict]
    def get_sentiment_trend(self, days: int = 7) -> List[Dict]

class AudienceAnalyzer:
    def add_audience_data(self, platform: Platform, data: Dict) -> None
    def get_optimal_posting_times(self, platform: Platform) -> List[Dict]
    def analyze_cross_platform_overlap(self) -> Dict
    def get_growth_recommendations(self) -> List[Dict]
    def get_total_reach(self) -> Dict
    def get_audience_insights(self, platform: Optional[Platform] = None) -> Dict

class SocialAnalytics:
    def calculate_kpis(self) -> Dict
    def get_top_performing_posts(self, limit: int = 10) -> List[Dict]
    def get_platform_breakdown(self) -> Dict
    def generate_report(self, period_days: int = 30) -> Dict

class InfluencerManager:
    def add_influencer(self, username: str, platform: Platform, followers: int, engagement_rate: float, niche: str, cost: float, bio: Optional[str] = None) -> InfluencerProfile
    def find_top_influencers(self, niche: str, limit: int = 10) -> List[Dict]
    def find_by_tier(self, tier: InfluencerTier) -> List[Dict]
    def record_collaboration(self, influencer_id: str, campaign_id: str, content_posts: int, total_reach: int, cost: float, total_engagements: Optional[int] = None, conversions: Optional[int] = None, revenue: Optional[float] = None) -> Dict
    def get_influencer_summary(self) -> Dict
    def calculate_roi(self, influencer_id: str) -> Dict

class ReputationMonitor:
    def add_keywords(self, keywords: List[str]) -> None
    def record_event(self, platform: Platform, event_type: str, content: str, source: str, sentiment: SentimentType, url: Optional[str] = None) -> ReputationEvent
    def get_reputation_score(self) -> Dict
    def get_recent_events(self, limit: int = 10) -> List[Dict]
    def detect_crisis(self) -> Dict
    def get_alert_queue(self) -> List[Dict]
```

## Data Models

### SocialPost
| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique post identifier (post_XXXXXXXX) |
| platform | Platform | Target platform |
| content | str | Post text |
| content_type | ContentType | POST, THREAD, VIDEO, STORY, REEL, ARTICLE |
| status | ContentStatus | DRAFT, SCHEDULED, PUBLISHED, ARCHIVED |
| hashtags | List[str] | Hashtags used |
| mentions | List[str] | User mentions |
| media_urls | List[str] | Attached media |
| metrics | Dict | likes, comments, shares, views, saves |
| engagement_rate | float | Calculated engagement rate |
| scheduled_at | Optional[datetime] | Scheduled publish time |
| published_at | Optional[datetime] | Actual publish time |
| created_at | datetime | Creation timestamp |

### Engagement
| Field | Type | Description |
|-------|------|-------------|
| id | str | Engagement identifier (eng_XXXXXXXX) |
| post_id | str | Parent post |
| user_id | str | User who engaged |
| username | str | User's handle |
| engagement_type | EngagementType | LIKE, COMMENT, SHARE, MENTION, SAVE, CLICK |
| content | Optional[str] | Comment/mention text |
| sentiment | SentimentType | VERY_POSITIVE to VERY_NEGATIVE |
| sentiment_score | float | -1.0 to 1.0 |
| replied | bool | Whether brand responded |
| timestamp | datetime | Engagement time |

### Campaign
| Field | Type | Description |
|-------|------|-------------|
| id | str | Campaign identifier (camp_XXXXXXXX) |
| name | str | Campaign name |
| description | str | Campaign description |
| status | CampaignStatus | PLANNING, ACTIVE, PAUSED, COMPLETED, ARCHIVED |
| platforms | List[Platform] | Target platforms |
| budget | float | Campaign budget |
| goals | Dict | Target metrics |
| posts | List[str] | Post IDs |
| start_date | datetime | Campaign start |
| end_date | Optional[datetime] | Campaign end |

### InfluencerProfile
| Field | Type | Description |
|-------|------|-------------|
| id | str | Influencer identifier (inf_XXXXXXXX) |
| username | str | Platform handle |
| platform | Platform | Primary platform |
| followers | int | Follower count |
| engagement_rate | float | Average engagement rate |
| niche | str | Content niche |
| tier | InfluencerTier | NANO, MICRO, MACRO, MEGA |
| cost | float | Typical collaboration cost |
| total_collaborations | int | Number of collaborations |
| total_reach | int | Total reach from collaborations |
| roi | float | Return on investment |

### ReputationEvent
| Field | Type | Description |
|-------|------|-------------|
| id | str | Event identifier |
| platform | Platform | Source platform |
| event_type | str | mention, complaint, praise, news |
| content | str | Event text |
| source | str | Source description |
| sentiment | SentimentType | Sentiment classification |
| sentiment_score | float | -1.0 to 1.0 |
| alert_level | ReputationAlertLevel | GREEN, YELLOW, ORANGE, RED |
| url | Optional[str] | Source URL |
| timestamp | datetime | Event time |

## Checklist

### Content Creation
- [ ] Content fits platform character limits
- [ ] Hashtags are relevant and within limits
- [ ] Mentions are verified and appropriate
- [ ] Media attachments are platform-appropriate
- [ ] CTA is clear and actionable
- [ ] Content aligns with brand voice
- [ ] Links are shortened and tracked

### Scheduling
- [ ] Posting time aligns with audience active hours
- [ ] No content overlap with other scheduled posts
- [ ] Campaign dates are correct
- [ ] Timezone considerations addressed
- [ ] Buffer time between posts on same platform
- [ ] Cross-platform timing coordinated

### Engagement
- [ ] Sentiment is correctly classified
- [ ] Negative mentions are escalated
- [ ] Response templates are personalized
- [ ] Automations are tested
- [ ] Response time within SLA
- [ ] Escalation path defined

### Analytics
- [ ] KPIs are calculated from published posts only
- [ ] Time periods are clearly defined
- [ ] Recommendations are actionable
- [ ] Reports include visualization data
- [ ] Benchmarks are set for comparison
- [ ] Goals are tracked against actuals

### Influencer
- [ ] Influencer audience matches target demographic
- [ ] Engagement rate is authentic (not inflated)
- [ ] Collaboration terms are clear
- [ ] Tracking links are set up
- [ ] ROI is calculated correctly
- [ ] Contract and deliverables documented

### Reputation
- [ ] Keywords are comprehensive
- [ ] Alert thresholds are appropriate
- [ ] Crisis response plan is documented
- [ ] Escalation contacts are current
- [ ] Monitoring is 24/7 for critical brands
- [ ] Historical data is preserved

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Post not scheduled | Verify scheduled_at is in the future |
| Sentiment always neutral | Check lexicon coverage; add domain-specific terms |
| Calendar empty | Ensure posts have scheduled_at set |
| Engagement rate = 0 | Posts must be PUBLISHED status |
| Influencer ROI = 0 | Record collaboration with reach and cost |
| Reputation score stuck | Add keywords and record events |
| Dashboard shows 0 | Initialize audience data for each platform |
| Thread posting fails | Ensure all messages fit platform limits |
| Automation not triggering | Check trigger conditions match exactly |
| Campaign not appearing | Verify start_date has passed |
| Overlap calculation wrong | Need data for 2+ platforms |
| Crisis not detected | Keywords must be in watchlist |

## Security Notes

- User IDs and usernames are stored as-is; validate inputs
- Content is stored in memory; persist to database for production
- API tokens for platform integration are not handled here
- Reputation events may contain user-generated content; handle PII carefully
- Engagement data may be subject to GDPR/CCPA regulations
- Influencer contact information should be access-controlled
- Campaign budgets should be encrypted at rest
- Automated responses should be reviewed before enabling
- Sentiment analysis may have bias; calibrate for your domain
- Platform APIs have rate limits; implement backoff logic

## Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Post creation | < 10ms | In-memory storage |
| Sentiment analysis | < 5ms per text | Pre-compiled lexicon |
| Dashboard generation | < 100ms | Cached aggregations |
| Calendar query | < 50ms | Date-indexed storage |
| Reputation assessment | < 20ms | Keyword pre-filtering |
| Engagement tracking | < 5ms | Batch writes |
| Influencer search | < 30ms | Tag-based indexing |

---

*Social Media Agent v2.0 — Part of the Awesome Grok Skills collection.*
