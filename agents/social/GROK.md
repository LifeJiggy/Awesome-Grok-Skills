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
---

# Social Media Agent

> Comprehensive social media management with content scheduling, engagement analytics, audience insights, influencer marketing, and reputation monitoring.

## Identity

The Social Agent is a full-lifecycle social media management platform. It handles content creation and scheduling across multiple platforms, tracks engagement with sentiment analysis, analyzes audience demographics and growth, manages influencer collaborations, and monitors brand reputation with crisis detection.

**Core principle:** Every post should reach the right audience at the right time. Every engagement should be understood. Every reputation signal should be tracked.

## Principles

1. **Platform-Native Content** - Respect each platform's rules and norms
2. **Data-Driven Decisions** - Let metrics guide content strategy
3. **Authentic Engagement** - Build genuine relationships, not vanity metrics
4. **Proactive Reputation** - Monitor before crises escalate
5. **Consistent Presence** - Regular, scheduled content builds trust
6. **Measure Everything** - If it can't be measured, it can't be improved

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
)
# post.id = "post_a1b2c3d4"

# Create a thread
posts = agent.content.create_thread(
    platform=Platform.TWITTER,
    messages=[
        "Thread: 5 ways to improve your security posture (1/3)",
        "1. Enable MFA everywhere (2/3)",
        "3. Regular security audits (3/3)",
    ],
)

# Use templates
agent.content.add_template("announcement", "Breaking: {{headline}} - {{details}}")
rendered = agent.content.render_template("announcement", {
    "headline": "New Feature Launch",
    "details": "AI-powered threat detection now available",
})

# Get content calendar
from datetime import datetime, timedelta
calendar = agent.content.get_calendar(
    start=datetime.now(),
    end=datetime.now() + timedelta(days=7),
)
```

### 2. Engagement Tracking

```python
from agents.social.agent import EngagementType

# Track engagement
eng = agent.engagement.track_engagement(
    post_id=post.id,
    user_id="user_123",
    username="techfan",
    engagement_type=EngagementType.COMMENT,
    content="This is exactly what we needed!",
)
# eng.sentiment = SentimentType.POSITIVE

# Get engagement metrics
metrics = agent.engagement.get_engagement_metrics(post.id)
# {"total_engagements": 42, "by_type": {"like": 30, "comment": 12}}

# Find top engagers
top = agent.engagement.get_top_engagers(limit=5)
# [{"username": "poweruser", "engagements": 15}]

# Sentiment trend
trend = agent.engagement.get_sentiment_trend(days=7)
```

### 3. Audience Analytics

```python
# Add audience data
agent.audience.add_audience_data(Platform.TWITTER, {
    "followers": 25000,
    "growth_rate": 0.03,
    "engagement_rate": 0.045,
    "active_hours": [9, 12, 14, 18, 20],
    "demographics": {"18-24": 0.15, "25-34": 0.40, "35-44": 0.30},
})

# Get optimal posting times
times = agent.audience.get_optimal_posting_times(Platform.TWITTER)
# [{"hour": 18, "score": 5}, {"hour": 12, "score": 4}]

# Cross-platform overlap
overlap = agent.audience.analyze_cross_platform_overlap()
# {"twitter_linkedin": 0.25}

# Growth recommendations
recs = agent.audience.get_growth_recommendations()
```

### 4. Performance Analytics

```python
# Calculate KPIs
kpis = agent.analytics.calculate_kpis()
# {
#   "total_posts": 150,
#   "total_engagements": 4500,
#   "avg_engagement_rate": 0.038,
#   "total_followers": 50000,
# }

# Get top posts
top = agent.analytics.get_top_performing_posts(limit=5)

# Generate report
report = agent.analytics.generate_report()
# {"period": {...}, "kpis": {...}, "top_posts": [...], "recommendations": [...]}
```

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
)
# inf.tier = InfluencerTier.MACRO

# Find top influencers by niche
top = agent.influencer.find_top_influencers("cybersecurity", limit=3)

# Record collaboration
collab = agent.influencer.record_collaboration(
    influencer_id=inf.id,
    campaign_id="camp_001",
    content_posts=3,
    total_reach=45000,
    cost=2500.0,
)
# collab["roi"] = 18.0

# Summary
summary = agent.influencer.get_influencer_summary()
```

### 6. Reputation Monitoring

```python
from agents.social.agent import SentimentType, ReputationAlertLevel

# Add monitoring keywords
agent.reputation.add_keywords(["brandname", "productname"])

# Record event
event = agent.reputation.record_event(
    platform=Platform.TWITTER,
    event_type="mention",
    content="Love the new update from @brandname",
    source="user_tweet",
    sentiment=SentimentType.POSITIVE,
)
# event.alert_level = ReputationAlertLevel.GREEN

# Crisis detection
crisis = agent.reputation.record_event(
    platform=Platform.TWITTER,
    event_type="complaint",
    content="brandname is a scam, lost all my data",
    source="viral_tweet",
    sentiment=SentimentType.VERY_NEGATIVE,
)
# crisis.alert_level = ReputationAlertLevel.RED

# Reputation score
score = agent.reputation.get_reputation_score()
# {"score": 72.5, "level": "good"}
```

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
)

# Schedule batch
agent.schedule_content_batch([
    {"platform": "twitter", "content": "Launch day!", "scheduled_at": "2025-01-15T09:00:00"},
    {"platform": "linkedin", "content": "Enterprise announcement", "scheduled_at": "2025-01-15T10:00:00"},
])
```

### 8. Unified Dashboard

```python
dashboard = agent.get_social_dashboard()
# {
#   "kpis": {"total_posts": 150, "total_engagements": 4500},
#   "audience": {"total_followers": 50000},
#   "reputation": {"score": 72.5, "level": "good"},
#   "influencers": {"total_influencers": 12},
#   "top_posts": [...],
#   "recommendations": [...]
# }
```

## Method Signatures

```python
class SocialAgent:
    def create_campaign(self, name, description, platforms, start_date, end_date?, budget?) -> Campaign
    def schedule_content_batch(self, posts_data: List[Dict]) -> Dict
    def respond_to_mentions(self, keyword: str) -> List[Dict]
    def get_social_dashboard(self) -> Dict

class ContentManager:
    def create_post(self, platform, content, content_type?, scheduled_at?, hashtags?, mentions?, media_urls?, author_id?) -> SocialPost
    def create_thread(self, platform, messages, hashtags?) -> List[SocialPost]
    def add_template(self, name, template, platform?, variables?) -> None
    def render_template(self, template_name, variables) -> Optional[str]
    def get_calendar(self, start, end, platform?) -> Dict
    def publish_post(self, post_id) -> Dict

class EngagementManager:
    def track_engagement(self, post_id, user_id, username, engagement_type, content?, platform?) -> Engagement
    def respond_to_engagement(self, engagement_id, response) -> Dict
    def create_automation(self, trigger, action, conditions?, name?) -> Dict
    def get_engagement_metrics(self, post_id) -> Dict
    def get_top_engagers(self, limit?) -> List[Dict]
    def get_sentiment_trend(self, days?) -> List[Dict]
```

## Data Models

### SocialPost
| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique post identifier |
| platform | Platform | Target platform |
| content | str | Post text |
| content_type | ContentType | POST, THREAD, VIDEO, etc. |
| status | ContentStatus | DRAFT, SCHEDULED, PUBLISHED |
| metrics | Dict | likes, comments, shares, views |
| engagement_rate | float | Calculated engagement rate |

### Engagement
| Field | Type | Description |
|-------|------|-------------|
| id | str | Engagement identifier |
| engagement_type | EngagementType | LIKE, COMMENT, SHARE, etc. |
| sentiment | SentimentType | VERY_POSITIVE to VERY_NEGATIVE |
| replied | bool | Whether brand responded |

### Campaign
| Field | Type | Description |
|-------|------|-------------|
| id | str | Campaign identifier |
| status | CampaignStatus | PLANNING, ACTIVE, PAUSED, COMPLETED |
| platforms | List[Platform] | Target platforms |
| budget | float | Campaign budget |
| kpis | Dict | Target metrics |

## Checklist

### Content Creation
- [ ] Content fits platform character limits
- [ ] Hashtags are relevant and within limits
- [ ] Media attachments are platform-appropriate
- [ ] CTA is clear and actionable

### Scheduling
- [ ] Posting time aligns with audience active hours
- [ ] No content overlap with other scheduled posts
- [ ] Campaign dates are correct
- [ ] Timezone considerations addressed

### Engagement
- [ ] Sentiment is correctly classified
- [ ] Negative mentions are escalated
- [ ] Response templates are personalized
- [ ] Automations are tested

### Analytics
- [ ] KPIs are calculated from published posts only
- [ ] Time periods are clearly defined
- [ ] Recommendations are actionable
- [ ] Reports include visualizations data

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

## Security Notes

- User IDs and usernames are stored as-is; validate inputs
- Content is stored in memory; persist to database for production
- API tokens for platform integration are not handled here
- Reputation events may contain user-generated content; handle PII carefully
