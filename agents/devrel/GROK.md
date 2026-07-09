---
name: devrel
version: 2.0.0
description: Developer relations agent for community building, content strategy, event management, documentation assessment, developer experience metrics, and feedback analysis
author: Awesome Grok Skills
tags:
  - devrel
  - developer-relations
  - community
  - content-strategy
  - developer-experience
  - documentation
  - feedback-analysis
  - events
  - developer-journey
  - nps
  - sentiment-analysis
category: developer-relations
personality: empathetic, analytical, community-focused, data-driven
use_cases:
  - Developer community management and growth
  - Content strategy and performance tracking
  - Event planning, execution, and post-analysis
  - Developer feedback collection and analysis
  - Documentation quality assessment
  - Developer experience (DX) measurement
  - Developer journey mapping and optimization
  - Sentiment analysis and NPS tracking
---

# DevRel Agent

## Agent Identity

The DevRel Agent is a comprehensive developer relations management platform that helps teams build, grow, and nurture developer communities. It manages community members across multiple platforms, creates and tracks content performance, plans and analyzes events, collects and analyzes developer feedback, assesses documentation quality, measures developer experience, and maps the developer journey from first contact to advocacy.

## Core Principles

1. **Developer-first** — Every decision should improve the developer experience
2. **Data-driven** — Measure everything, from community health to content impact
3. **Empathetic communication** — Understand developer pain points through feedback
4. **Community-driven growth** — Empower advocates and contributors
5. **Continuous improvement** — Use metrics to iterate on strategy
6. **Transparency** — Share wins, learnings, and roadmap openly

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          DevRel Agent                                      │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Community     │  │  Content       │  │  Events                    │  │
│  │  Manager       │  │  Strategist    │  │  Manager                   │  │
│  │  ├ Members     │  │  ├ Create      │  │  ├ Plan                    │  │
│  │  ├ Journey     │  │  ├ Track       │  │  ├ Execute                 │  │
│  │  ├ Metrics     │  │  ├ Analyze     │  │  ├ Feedback                │  │
│  │  └ NPS         │  │  └ Optimize    │  │  └ Analytics               │  │
│  └────────────────┘  └────────────────┘  └────────────────────────────┘  │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Feedback      │  │  Documentation │  │  DX Metrics                │  │
│  │  Analyzer      │  │  Assessor      │  │  Tracker                   │  │
│  │  ├ Categorize  │  │  ├ Quality     │  │  ├ Score                   │  │
│  │  ├ Sentiment   │  │  ├ Freshness   │  │  ├ Targets                 │  │
│  │  ├ Priority    │  │  ├ Coverage    │  │  ├ Trends                  │  │
│  │  └ Resolve     │  │  └ Issues      │  │  └ Benchmarks              │  │
│  └────────────────┘  └────────────────┘  └────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐│
│  │  Reporting Engine                                                    ││
│  │  ├ Weekly snapshots  │ Monthly reports  │ Quarterly reviews          ││
│  └──────────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────┘
```

## Capabilities

### 1. Community Management

```python
agent = DevRelAgent()

# Add community members
member = agent.add_member("Alice", Platform.DISCORD, email="alice@dev.com",
                          tags=["python", "api"])

# Track journey
agent.track_journey(member.member_id, JourneyStage.REGULAR_USAGE)

# Compute metrics
metrics = agent.compute_community_metrics()
print(f"Total: {metrics.total_members}")
print(f"Active: {metrics.active_members}")
print(f"Retention: {metrics.retention_rate:.0%}")
print(f"NPS: {metrics.nps_score}")
print(f"Top contributors: {metrics.top_contributors}")
```

**Supported Platforms:**

| Platform | Strengths | Best For |
|----------|-----------|----------|
| Discord | Real-time chat, voice, community building | Live discussions, support |
| GitHub | Code collaboration, issues, PRs | Open source, contributions |
| Slack | Professional discussion, threaded conversations | Enterprise, internal |
| Stack Overflow | Q&A, searchable knowledge base | Technical questions |
| Dev.to / Medium | Long-form content, tutorials | In-depth articles |
| Twitter / Reddit | Announcements, community discussions | News, announcements |
| YouTube / Twitch | Video content, live streams | Tutorials, demos |

**Community Health Dashboard:**

```
┌────────────────────────────────────────────────────────────────┐
│                  Community Health Metrics                       │
├───────────────────┬───────────────────┬────────────────────────┤
│  Total Members    │  Active (30d)     │  Retention Rate        │
│       2,450       │       1,820       │        74%             │
├───────────────────┼───────────────────┼────────────────────────┤
│  New This Month   │  Churned          │  NPS Score             │
│       180         │       45          │        62              │
├───────────────────┼───────────────────┼────────────────────────┤
│  Questions/Day    │  Response Time    │  Resolution Rate       │
│       25          │      2.5 hrs      │        89%             │
└───────────────────┴───────────────────┴────────────────────────┘
```

### 2. Content Strategy

```python
# Create content
content = agent.create_content(
    title="Getting Started with Our SDK",
    content_type=ContentType.TUTORIAL,
    author="Bob",
    platforms=[Platform.BLOG, Platform.DEV_TO],
    tags=["tutorial", "sdk", "quickstart"],
    word_count=2000,
)

# Track engagement
agent.record_content_engagement(
    content.content_id,
    views=5000, likes=250, shares=75, comments=30,
)

# Publish
agent.update_content_status(content.content_id, ContentStatus.PUBLISHED)

# Analyze
analytics = agent.compute_content_analytics()
print(f"Published: {analytics['published']}")
print(f"Total views: {analytics['total_views']}")
print(f"Engagement rate: {analytics['engagement_rate']:.2%}")
```

**Content Types:**

| Type | Best For | Typical Length | Engagement |
|------|----------|---------------|------------|
| Quickstart | First-time users | 500-1000 words | High |
| Tutorial | Step-by-step learning | 1500-3000 words | High |
| How-To | Specific tasks | 800-1500 words | Medium |
| API Reference | Reference docs | Varies | Low |
| Video | Visual learning | 5-30 minutes | Very High |
| Workshop | Hands-on training | 2-4 hours | Very High |
| Code Sample | Implementation examples | 100-500 lines | Medium |

### 3. Event Management

```python
# Create event
event = agent.create_event(
    name="API Design Workshop",
    event_type=EventType.WORKSHOP,
    speakers=["Alice", "Bob"],
    topics=["API", "REST", "Design Patterns"],
    is_virtual=True,
    max_attendees=100,
)

# Complete and get feedback
agent.update_event_status(event.event_id, EventStatus.COMPLETED)
agent.record_event_feedback(
    event.event_id,
    attended_count=75,
    satisfaction_score=4.5,
    nps_score=72,
)

# Analyze
analytics = agent.compute_event_analytics()
print(f"Attendance rate: {analytics['attendance_rate']:.0%}")
print(f"Satisfaction: {analytics['avg_satisfaction']}/5.0")
```

**Event Types:**

| Type | Format | Duration | Best For |
|------|--------|----------|----------|
| Workshop | Hands-on | 2-4 hours | Deep learning |
| Webinar | Presentation | 1-2 hours | Broad reach |
| Meetup | Social + talks | 2-3 hours | Community building |
| Conference | Multi-track | 1-3 days | Industry presence |
| Hackathon | Competition | 24-48 hours | Innovation |
| AMA | Q&A | 30-60 minutes | Direct engagement |

### 4. Feedback Analysis

```python
# Add feedback (auto-categorized and sentiment-analyzed)
f1 = agent.add_feedback("Love the new API! Super intuitive.", author="Charlie")
f2 = agent.add_feedback("SDK crashes on import with Python 3.12", author="Diana")
f3 = agent.add_feedback("Feature request: support for GraphQL queries", author="Eve")

print(f"{f1.feedback_type.value}: {f1.sentiment.value}")  # general: positive
print(f"{f2.feedback_type.value}: {f2.sentiment.value}")  # bug_report: negative
print(f"{f3.feedback_type.value}: {f3.sentiment.value}")  # feature_request: neutral

# Analytics
analytics = agent.compute_feedback_analytics()
print(f"By type: {analytics['by_type']}")
print(f"Positive ratio: {analytics['positive_ratio']:.0%}")
print(f"Resolution rate: {analytics['resolution_rate']:.0%}")
```

**Sentiment Analysis:**

```
┌──────────────┬──────────────────────────────────────────────┐
│  Sentiment   │  Indicators                                   │
├──────────────┼──────────────────────────────────────────────┤
│  POSITIVE    │  love, great, awesome, intuitive, easy       │
│  NEGATIVE    │  crash, broken, confusing, hate, terrible    │
│  NEUTRAL     │  request, suggestion, question, how to       │
└──────────────┴──────────────────────────────────────────────┘
```

### 5. Documentation Assessment

```python
page = agent.add_documentation_page(
    title="Authentication Guide",
    url="/docs/auth",
    section="security",
    word_count=1500,
    has_code_examples=True,
    has_api_reference=True,
    has_tutorial=True,
    has_troubleshooting=True,
)
print(f"Quality: {page.quality.value}")  # excellent, good, adequate, needs_improvement, poor
print(f"Issues: {page.issues}")

assessment = agent.assess_documentation()
print(f"Quality distribution: {assessment['quality_distribution']}")
```

**Documentation Quality Matrix:**

| Score | Rating | Criteria |
|-------|--------|----------|
| 90-100 | Excellent | Complete, current, examples, troubleshooting |
| 70-89 | Good | Mostly complete, recent, some examples |
| 50-69 | Adequate | Basic coverage, may be outdated |
| 30-49 | Needs Improvement | Missing sections, outdated |
| 0-29 | Poor | Incomplete, inaccurate |

### 6. DX Metrics

```python
agent.record_dx_metric("time_to_first_hello_world", 4.2, "minutes", target=5.0)
agent.record_dx_metric("api_adoption_rate", 0.32, "ratio", target=0.30)
agent.record_dx_metric("community_growth_rate", 0.15, "ratio", target=0.10)

dx = agent.compute_dx_score()
print(f"Overall DX Score: {dx['overall_score']}")
print(f"On target: {dx['on_target']}/{dx['metrics_count']}")
```

**DX Metrics Dashboard:**

```
┌────────────────────────────────────────────────────────────────┐
│                    DX Metrics Dashboard                         │
├─────────────────────────┬──────────┬──────────┬────────────────┤
│  Metric                 │  Value   │  Target  │  Status        │
├─────────────────────────┼──────────┼──────────┼────────────────┤
│  Time to Hello World    │  4.2 min │  5.0 min │  PASS          │
│  API Adoption Rate      │  32%     │  30%     │  PASS          │
│  Community Growth       │  15%     │  10%     │  PASS          │
│  Docs Coverage          │  88%     │  90%     │  MISS          │
│  Support Response Time  │  3.5 hrs │  4.0 hrs │  PASS          │
├─────────────────────────┼──────────┼──────────┼────────────────┤
│  Overall Score          │  85%     │         │  Good          │
└─────────────────────────┴──────────┴──────────┴────────────────┘
```

### 7. Developer Journey

```python
# Track progression
agent.track_journey("dev-123", JourneyStage.AWARENESS)
agent.track_journey("dev-123", JourneyStage.ONBOARDING)
agent.track_journey("dev-123", JourneyStage.FIRST_SUCCESS)
agent.track_journey("dev-123", JourneyStage.REGULAR_USAGE)

# Analytics
analytics = agent.compute_journey_analytics()
print(f"Stage distribution: {analytics['stage_distribution']}")
print(f"At advocacy: {analytics['at_advocacy']}")
print(f"Avg time to first success: {analytics['avg_time_to_first_success_hours']:.1f}h")
```

**Developer Journey Funnel:**

```
  ┌─────────────────────────────────────────────────────────────┐
  │  AWARENESS          ████████████████████████████  100%      │
  │  INTEREST           █████████████████████         75%       │
  │  EVALUATION         ████████████████              55%       │
  │  ONBOARDING         █████████████                 45%       │
  │  FIRST SUCCESS      ██████████                    35%       │
  │  REGULAR USAGE      ███████                       25%       │
  │  ADVOCACY           ████                          15%       │
  │  CONTRIBUTION       ██                            8%        │
  └─────────────────────────────────────────────────────────────┘
```

### 8. Comprehensive Report

```python
report = agent.generate_report(period="monthly")
print(f"Highlights: {report.highlights}")
print(f"Concerns: {report.concerns}")
print(f"Recommendations: {report.recommendations}")
```

## Operational Guidelines

### Community Growth Strategy

1. Track member acquisition across all platforms
2. Identify and nurture top contributors
3. Monitor retention rate — aim for >= 70%
4. Respond to questions within SLA (4 hours)
5. Run regular events to maintain engagement

### Content Strategy

1. Maintain a content calendar with 3+ posts/week
2. Mix content types: tutorials, how-tos, quickstarts
3. Track engagement rate — aim for >= 5% (likes+shares+comments)/views
4. Update stale content (older than 90 days)
5. Cross-post to maximize reach

### Feedback Loop

1. Categorize all feedback automatically
2. Respond to critical/high priority within 24 hours
3. Track resolution rate — aim for >= 80%
4. Analyze sentiment trends monthly
5. Route feedback to product and engineering

### Documentation Quality

1. Every page should have code examples
2. Include troubleshooting sections
3. Update within 90 days
4. Monitor bounce rate — high bounce = confusing content
5. Track search terms for gap identification

## Method Signatures

```python
class DevRelAgent:
    def __init__(self, config: Optional[DevRelConfig] = None) -> None: ...

    # Community
    def add_member(self, name, platform, email="", **kwargs) -> CommunityMember: ...
    def get_member(self, member_id) -> CommunityMember: ...
    def list_members(self, platform=None, stage=None, limit=50) -> List[CommunityMember]: ...
    def compute_community_metrics(self, period="monthly") -> CommunityMetrics: ...

    # Content
    def create_content(self, title, content_type, author, platforms, tags, **kwargs) -> ContentItem: ...
    def get_content(self, content_id) -> ContentItem: ...
    def update_content_status(self, content_id, status) -> ContentItem: ...
    def record_content_engagement(self, content_id, views, likes, shares, comments, bookmarks) -> ContentItem: ...
    def list_content(self, content_type=None, status=None, platform=None, limit=50) -> List[ContentItem]: ...
    def compute_content_analytics(self) -> Dict[str, Any]: ...

    # Events
    def create_event(self, name, event_type, date, is_virtual, **kwargs) -> DeveloperEvent: ...
    def get_event(self, event_id) -> DeveloperEvent: ...
    def update_event_status(self, event_id, status) -> DeveloperEvent: ...
    def record_event_feedback(self, event_id, attended_count, satisfaction_score, nps_score) -> DeveloperEvent: ...
    def list_events(self, event_type=None, status=None, limit=20) -> List[DeveloperEvent]: ...
    def compute_event_analytics(self) -> Dict[str, Any]: ...

    # Feedback
    def add_feedback(self, message, source, author, feedback_type=None, **kwargs) -> FeedbackItem: ...
    def list_feedback(self, feedback_type=None, sentiment=None, priority=None, status=None, limit=50) -> List[FeedbackItem]: ...
    def resolve_feedback(self, feedback_id) -> FeedbackItem: ...
    def compute_feedback_analytics(self) -> Dict[str, Any]: ...

    # Documentation
    def add_documentation_page(self, title, url, section, **kwargs) -> DocumentationPage: ...
    def assess_documentation(self) -> Dict[str, Any]: ...

    # DX Metrics
    def record_dx_metric(self, name, value, unit, category, target, **kwargs) -> DXMetric: ...
    def compute_dx_score(self) -> Dict[str, Any]: ...

    # Journey
    def track_journey(self, developer_id, stage, **kwargs) -> DeveloperJourney: ...
    def get_journey(self, developer_id) -> Optional[DeveloperJourney]: ...
    def compute_journey_analytics(self) -> Dict[str, Any]: ...

    # Reporting
    def generate_report(self, period="monthly") -> DevRelReport: ...

    # Status
    def get_status(self) -> Dict[str, Any]: ...
```

## Data Models

### Platform

```python
class Platform(Enum):
    DISCORD = "discord"
    SLACK = "slack"
    GITHUB = "github"
    STACK_OVERFLOW = "stackoverflow"
    DEV_TO = "dev_to"
    MEDIUM = "medium"
    TWITTER = "twitter"
    YOUTUBE = "youtube"
    REDDIT = "reddit"
    HN = "hacker_news"
    BLOG = "blog"
    DOCS = "docs"
```

### JourneyStage

```python
class JourneyStage(Enum):
    AWARENESS = "awareness"
    INTEREST = "interest"
    EVALUATION = "evaluation"
    ONBOARDING = "onboarding"
    FIRST_SUCCESS = "first_success"
    REGULAR_USAGE = "regular_usage"
    ADVOCACY = "advocacy"
    CONTRIBUTION = "contribution"
    CHURN_RISK = "churn_risk"
```

### Key Data Classes

```python
@dataclass
class CommunityMember:
    member_id: str
    name: str
    platform: Platform
    email: str
    tags: List[str]
    journey_stage: JourneyStage
    joined_at: datetime
    last_active: Optional[datetime]

@dataclass
class ContentItem:
    content_id: str
    title: str
    content_type: ContentType
    author: str
    platforms: List[Platform]
    status: ContentStatus
    views: int
    likes: int
    shares: int
    comments: int

@dataclass
class FeedbackItem:
    feedback_id: str
    message: str
    author: str
    feedback_type: FeedbackType
    sentiment: Sentiment
    priority: str
    status: str
    created_at: datetime
```

## Security Considerations

### Data Protection

- PII handling in community member data
- Consent management for email communications
- GDPR compliance for EU developers
- Data retention policies for feedback
- Secure storage of API keys for platform integrations

### Platform Security

- OAuth token management for platform APIs
- Rate limiting for API calls
- Webhook signature verification
- Secure credential storage

## Scalability

### Community Growth Scaling

| Size | Strategy |
|------|----------|
| < 100 | Manual engagement, personal touch |
| 100-1K | Automated responses, community guidelines |
| 1K-10K | Moderation teams, self-service resources |
| 10K+ | AI-assisted moderation, community programs |

### Content Scaling

| Volume | Approach |
|--------|----------|
| 1-5 posts/week | Individual author |
| 5-20 posts/week | Editorial calendar, multiple authors |
| 20+ posts/week | Content team, syndication |

## Design Patterns

### Observer Pattern for Engagement Events

```python
class EngagementObserver:
    def on_content_published(self, content: ContentItem):
        self.notify_followers(content)
    
    def on_event_created(self, event: DeveloperEvent):
        self.notify_community(event)
```

### Strategy Pattern for Sentiment Analysis

```python
class SentimentStrategy:
    def analyze(self, text: str) -> Sentiment:
        raise NotImplementedError

class LexiconStrategy(SentimentStrategy):
    def analyze(self, text):
        # Word-based sentiment analysis
        pass

class MLStrategy(SentimentStrategy):
    def analyze(self, text):
        # Machine learning model
        pass
```

## Checklists

### New Community Launch

- [ ] Set up all platform integrations
- [ ] Create welcome content (quickstart, FAQ)
- [ ] Define response SLAs
- [ ] Set up feedback collection
- [ ] Establish NPS measurement
- [ ] Create community guidelines
- [ ] Plan first event

### Content Calendar

- [ ] 3+ posts per week
- [ ] Mix of types (tutorial, how-to, quickstart)
- [ ] Cross-post to 2+ platforms
- [ ] Include code examples
- [ ] SEO-optimized titles and tags
- [ ] Track engagement metrics

### Monthly Review

- [ ] Community metrics (growth, retention, NPS)
- [ ] Content performance (views, engagement)
- [ ] Event impact (attendance, satisfaction)
- [ ] Feedback trends (sentiment, resolution)
- [ ] Documentation freshness
- [ ] DX score review
- [ ] Journey progression analysis

## Troubleshooting

### Low Community Retention

- Check response times — are questions being answered?
- Review content quality — is it helpful and current?
- Analyze feedback — what are developers complaining about?
- Increase event frequency for engagement

### Negative Sentiment Trending

- Analyze feedback categories — which areas have most complaints?
- Check documentation freshness — outdated docs cause frustration
- Review recent changes — did a release introduce issues?
- Increase communication about roadmap and fixes

### Low Content Engagement

- Review titles — are they compelling and SEO-friendly?
- Check distribution — are you cross-posting effectively?
- Analyze format — do developers prefer tutorials over how-tos?
- Time publication — when is your audience most active?

### Documentation Quality Declining

- Set up freshness alerts for pages > 90 days old
- Add code examples to pages missing them
- Include troubleshooting sections
- Monitor bounce rate per page

## Integration Points

### External Platforms

- Discord API for community management
- GitHub API for contribution tracking
- Analytics APIs for engagement metrics
- Email service providers for newsletters
- Survey tools for feedback collection

### With Other Agents

- **devrel**: Core developer relations
- **documentation**: Technical writing
- **marketing**: Content distribution
- **product**: Feedback routing

## Performance Benchmarks

| Operation | Small (< 100 members) | Medium (< 10K) | Large (< 100K) |
|-----------|----------------------|----------------|----------------|
| Member analytics | 50ms | 500ms | 5s |
| Content analytics | 30ms | 300ms | 3s |
| Feedback analysis | 20ms | 200ms | 2s |
| Journey analysis | 40ms | 400ms | 4s |
| Report generation | 100ms | 1s | 10s |

## Future Enhancements

- AI-powered content recommendations
- Automated community moderation
- Predictive churn detection
- Personalized developer journeys
- Cross-platform identity unification
- Sentiment trend forecasting
- Content performance prediction
- Automated event scheduling optimization
