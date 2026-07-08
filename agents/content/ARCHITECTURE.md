# Content Agent — Architecture

## 1. Overview

The Content Agent is a content management and creation system designed to streamline content workflows from ideation through publishing and performance tracking. It combines content generation, SEO optimization, calendar management, social media publishing, moderation, and analytics into a unified content operations platform.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          CONTENT AGENT v2.0                                  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                         CONTENT LAYER                                  │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────────┐   │  │
│  │  │   Content    │  │     SEO      │  │        Calendar            │   │  │
│  │  │  Generator   │  │  Optimizer   │  │        Manager             │   │  │
│  │  │              │  │              │  │                            │   │  │
│  │  │ • Titles     │  │ • Keywords   │  │ • Topic suggestions        │   │  │
│  │  │ • Bodies     │  │ • Readabil.  │  │ • Date range queries       │   │  │
│  │  │ • Meta desc  │  │ • Structure  │  │ • Platform scheduling      │   │  │
│  │  │ • CTAs       │  │ • Links      │  │ • Status tracking          │   │  │
│  │  └──────┬───────┘  └──────┬───────┘  └────────────┬───────────────┘   │  │
│  │         │                 │                       │                    │  │
│  │  ┌──────┴───────┐  ┌──────┴───────┐  ┌───────────┴──────────────┐    │  │
│  │  │    Social    │  │   Content    │  │      Performance         │    │  │
│  │  │   Manager    │  │  Moderator   │  │      Tracker             │    │  │
│  │  │              │  │              │  │                          │    │  │
│  │  │ • Platform   │  │ • Quality    │  │ • Views, clicks          │    │  │
│  │  │ • Hashtags   │  │ • Flags      │  │ • Engagement rate        │    │  │
│  │  │ • Threads    │  │ • Brand      │  │ • CTR, conversions       │    │  │
│  │  │ • Timing     │  │ • Compliance │  │ • Trend analysis         │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘    │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│  ┌─────────────────────────────────┴──────────────────────────────────────┐  │
│  │                           DATA LAYER                                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │  │
│  │  │ Content  │  │ Calendar │  │  Social  │  │Perform-  │              │  │
│  │  │ Pieces   │  │ Entries  │  │  Posts   │  │ance Data │              │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘              │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 2. System Components

### 2.1 Content Generator
- Creates titles, bodies, meta descriptions, CTAs
- Supports multiple content types (blog, article, social, email, etc.)
- Tone-aware content creation
- Keyword extraction and integration
- Word count and reading time calculation
- Audience-targeted messaging
- Multi-paragraph structured output
- Inline keyword placement at optimal positions

### 2.2 SEO Optimizer
- Keyword density analysis with per-keyword breakdowns
- Readability scoring (Flesch-Kincaid Reading Ease and Grade Level)
- Heading and structure analysis (H1, H2, H3 hierarchy)
- Internal/external link counting and recommendations
- Meta description quality scoring
- URL slug generation and validation
- Content length optimization guidance
- Actionable, prioritized optimization recommendations

### 2.3 Content Calendar Manager
- Calendar entry creation and management with status tracking
- Topic suggestion engine based on niche and keywords
- Date range filtering and platform-based queries
- Publishing schedule visualization
- Status lifecycle (draft → scheduled → published → archived)
- Author assignment and tracking
- Overlap and conflict detection

### 2.4 Social Media Manager
- Platform-specific content optimization (Twitter, LinkedIn, Instagram, Facebook, Medium, Substack)
- Character limit enforcement per platform
- Hashtag generation based on content analysis
- Thread creation for Twitter with logical flow
- Optimal posting time suggestions based on platform data
- Tone adaptation per platform
- Engagement prediction heuristics

### 2.5 Content Moderator
- Quality scoring with configurable thresholds
- Flagged term detection and categorization
- Brand compliance checking against style guidelines
- Improvement suggestions with priority ranking
- Configurable moderation rules
- Batch moderation support
- Audit trail for moderation decisions

### 2.6 Performance Tracker
- Views, clicks, shares, comments, likes tracking
- Engagement rate calculation with weighted scoring
- CTR and conversion rate monitoring
- Trend analysis over time windows
- Top performer identification with ranking
- Content ROI estimation
- Comparative performance analysis across content types

## 3. Data Flow

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│   Topic     │───>│  Content     │───>│    SEO       │
│   Input     │    │  Generator   │    │  Optimizer   │
└─────────────┘    └──────┬───────┘    └──────┬───────┘
                          │                   │
                          v                   v
                   ┌──────────────┐    ┌──────────────┐
                   │  Content     │───>│  Calendar    │
                   │  Moderator   │    │  Manager     │
                   └──────┬───────┘    └──────┬───────┘
                          │                   │
                          v                   v
                   ┌──────────────┐    ┌──────────────┐
                   │  Social      │───>│ Performance  │
                   │  Manager     │    │  Tracker     │
                   └──────────────┘    └──────────────┘
```

### 3.1 Content Lifecycle

1. **Ideation**: Topic suggestion engine generates ideas based on niche, trending keywords, and content gaps
2. **Creation**: Content generation with tone, audience, and keyword targeting
3. **Optimization**: SEO analysis and readability improvement recommendations
4. **Review**: Moderation and quality assurance with scoring
5. **Scheduling**: Calendar management and platform assignment
6. **Publishing**: Social media and website deployment
7. **Measurement**: Performance tracking, analysis, and iterative improvement

### 3.2 State Transitions

```
┌────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│  Draft │───>│ In Review │───>│ Approved │───>│ Published│
└────────┘    └─────┬─────┘    └──────────┘    └──────────┘
                    │
                    v
              ┌──────────┐
              │ Flagged  │──> Remove/Edit ──> In Review
              └──────────┘
```

## 4. Design Patterns

### 4.1 Strategy Pattern
Content generation uses different strategies based on content type (blog vs. social vs. email). Each strategy defines its own template structure, tone rules, and length constraints.

### 4.2 Template Method Pattern
Content generation follows a common template with type-specific variations. The base flow (topic → title → body → meta → CTA) is fixed; content-type classes override specific steps.

### 4.3 Observer Pattern
Performance tracker observes content publish events and records metrics. When a new performance record arrives, it notifies the trend analyzer and top-performer calculator.

### 4.4 Repository Pattern
Content store acts as a repository for content pieces and metadata. All storage operations go through this abstraction, enabling future database migration without changing business logic.

### 4.5 Facade Pattern
ContentAgent provides a simplified interface over the complex content subsystem. External callers interact with one class that delegates to generators, optimizers, moderators, and trackers.

### 4.6 Chain of Responsibility
Content moderation applies a chain of checks: flagged terms → brand compliance → quality scoring → approval. Each handler passes or stops the chain.

## 5. Component Deep Dive

### 5.1 Content Generation Pipeline

```
┌─────────────────────────────────────────────────────────┐
│              Content Generation Pipeline                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Topic + Audience + Tone                                │
│       │                                                 │
│       v                                                 │
│  ┌─────────────┐                                        │
│  │ Title Gen   │──> Multiple title options              │
│  └──────┬──────┘    (SEO-optimized, engaging)           │
│         v                                               │
│  ┌─────────────┐                                        │
│  │ Body Gen    │──> Structured sections                 │
│  └──────┬──────┘    (intro, body, conclusion)           │
│         v                                               │
│  ┌─────────────┐                                        │
│  │ Meta Gen    │──> SEO-optimized descriptions          │
│  └──────┬──────┘    (150-160 chars, keyword-rich)       │
│         v                                               │
│  ┌─────────────┐                                        │
│  │ CTA Gen     │──> Conversion-optimized calls          │
│  └──────┬──────┘    (action-specific, compelling)       │
│         v                                               │
│  ┌─────────────┐                                        │
│  │ Keyword     │──> Extracted and ranked keywords       │
│  └─────────────┘    (primary, secondary, long-tail)     │
└─────────────────────────────────────────────────────────┘
```

### 5.2 SEO Scoring Model

```
┌─────────────────────────────────────────────────────────┐
│                  SEO Score Calculation                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Keyword Score (40% weight)                             │
│  ├── Keyword density within target range (1-2%)         │
│  ├── Primary keyword in title                           │
│  ├── Primary keyword in first paragraph                 │
│  ├── Keywords in meta description                       │
│  └── Keyword distribution across content                │
│                                                         │
│  Readability Score (30% weight)                         │
│  ├── Flesch-Kincaid reading ease (target: >60)          │
│  ├── Average sentence length (target: <20 words)        │
│  ├── Average word length                                │
│  └── Grade level appropriateness (target: 8th-10th)     │
│                                                         │
│  Structure Score (30% weight)                           │
│  ├── Heading hierarchy (H1, H2, H3)                    │
│  ├── Paragraph organization                             │
│  ├── Bullet/numbered lists                              │
│  ├── Internal/external links (target: 3-5 each)        │
│  └── Image usage (alt text present)                     │
│                                                         │
│  Overall = Keyword * 0.4 + Readability * 0.3           │
│          + Structure * 0.3                              │
│                                                         │
│  Grade Scale:                                           │
│  ├── 90-100: Excellent                                 │
│  ├── 70-89: Good                                       │
│  ├── 50-69: Needs Improvement                          │
│  └── 0-49: Poor                                        │
└─────────────────────────────────────────────────────────┘
```

### 5.3 Platform Optimization Matrix

```
┌──────────────────────────────────────────────────────────────────────┐
│                   Platform Optimization Matrix                       │
├──────────────┬──────────┬───────────┬──────────────┬────────────────┤
│ Platform     │ Max Len  │ Style     │ Optimal Time │ Hashtag Limit  │
├──────────────┼──────────┼───────────┼──────────────┼────────────────┤
│ Twitter      │ 280      │ Concise   │ 9:00 AM EST  │ 2-3            │
│ LinkedIn     │ 3000     │ Profess.  │ 8:00 AM EST  │ 3-5            │
│ Instagram    │ 2200     │ Visual    │ 11:00 AM EST │ 10-15          │
│ Facebook     │ 63206    │ Casual    │ 1:00 PM EST  │ 1-2            │
│ Medium       │ Unlimited│ Long-form │ 10:00 AM EST │ 0-3            │
│ Substack     │ Unlimited│ Newsletter│ 7:00 AM EST  │ 0              │
│ Threads      │ 500      │ Casual    │ 12:00 PM EST │ 3-5            │
│ TikTok       │ 2200     │ Trendy    │ 7:00 PM EST  │ 3-5            │
└──────────────┴──────────┴───────────┴──────────────┴────────────────┘
```

### 5.4 Content Type Specifications

```
┌──────────────────────────────────────────────────────────────────┐
│                   Content Type Specifications                     │
├──────────────┬───────────────┬──────────────┬───────────────────┤
│ Type         │ Word Count    │ Tone Default │ Primary Goal      │
├──────────────┼───────────────┼──────────────┼───────────────────┤
│ blog_post    │ 800-2000      │ professional │ SEO, education    │
│ article      │ 600-1500      │ professional │ News, analysis    │
│ social_media │ 50-280        │ casual       │ Engagement        │
│ email        │ 200-500       │ persuasive   │ Conversion        │
│ landing_page │ 300-800       │ persuasive   │ Lead generation   │
│ video_script │ 500-2000      │ educational  │ Instruction       │
│ whitepaper   │ 2000-5000     │ technical    │ Authority         │
│ case_study   │ 800-1500      │ professional │ Social proof      │
│ documentation│ 500-5000      │ technical    │ Product support   │
│ newsletter   │ 400-1200      │ friendly     │ Subscriber retain │
└──────────────┴───────────────┴──────────────┴───────────────────┘
```

## 6. Tech Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.10+ | Type hints, dataclasses, modern syntax |
| Data Models | dataclasses | Typed, serializable, lightweight |
| Storage | In-memory | Fast, no external deps, demo-friendly |
| Text Analysis | Regex-based | Keyword and structure analysis |
| Serialization | dict/to_dict | JSON-compatible output |
| Readability | Flesch-Kincaid | Industry-standard scoring |
| ID Generation | hashlib.md5 | Deterministic unique IDs |
| Date Handling | datetime | Calendar operations |
| Random | random | Topic suggestion variety |
| Collections | defaultdict | Efficient aggregation |

## 7. Security Considerations

### 7.1 Content Safety
- Moderation checks for inappropriate content before publishing
- Brand compliance verification against configurable rulesets
- Flagged term detection with categorized severity levels
- Quality assurance scoring with minimum thresholds

### 7.2 Data Privacy
- No PII stored in content by default
- Author attribution tracked but anonymizable
- Performance data aggregated and anonymized
- Content export supports redaction mode

### 7.3 API Security
- Rate limiting on content generation endpoints
- Input sanitization for topic and keyword parameters
- Content length validation to prevent abuse
- Audit logging for all moderation decisions

## 8. Scalability

### 8.1 Current Architecture
- In-memory content store: ~10,000 pieces
- Calendar entries: ~5,000
- Social posts: ~50,000
- Performance records: ~100,000
- Moderation log: ~10,000 entries

### 8.2 Scaling Strategies
- **Database backend**: PostgreSQL for persistent storage with full-text search
- **CDN integration**: Content delivery optimization for published assets
- **Analytics pipeline**: Real-time performance dashboards with streaming updates
- **API layer**: REST API for external integrations and webhooks
- **Message queue**: Async processing for social media publishing
- **Caching layer**: Redis for frequently accessed content and analytics

### 8.3 Performance Targets

| Metric | Current | Scaled Target |
|--------|---------|---------------|
| Content generation | < 500ms | < 200ms |
| SEO analysis | < 100ms | < 50ms |
| Moderation | < 50ms | < 20ms |
| Calendar query | < 30ms | < 10ms |
| Performance lookup | < 20ms | < 5ms |
| Social post creation | < 100ms | < 50ms |

## 9. Integration Points

```
┌─────────────────┐     ┌──────────────────┐
│ Content Agent   │────>│ CMS Platforms    │
│                 │     │ (WordPress, etc) │
└────────┬────────┘     └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ Social APIs      │
         │             │ (Twitter, etc)   │
         │             └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ Analytics        │
         │             │ (GA, Mixpanel)   │
         │             └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ SEO Tools        │
         │             │ (Ahrefs, SEMrush)│
         │             └──────────────────┘
         │
         └────────────>┌──────────────────┐
                       │ Email Platforms  │
                       │ (SendGrid, etc)  │
                       └──────────────────┘
```

## 10. Error Handling

| Error Type | Handling Strategy |
|-----------|-------------------|
| Content not found | Return error with available IDs |
| Invalid content type | Fall back to blog_post |
| Invalid platform | Use generic platform settings |
| Empty content | Return validation error |
| SEO analysis failure | Return partial results with warnings |
| Moderation timeout | Flag for manual review |
| Calendar conflict | Suggest alternative slots |
| Platform API error | Queue for retry with backoff |

## 11. Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Content generation | < 500ms | Body + metadata |
| SEO analysis | < 100ms | 1000-word article |
| Moderation | < 50ms | Single content piece |
| Calendar query | < 30ms | 5K entries |
| Performance lookup | < 20ms | Single content ID |
| Social post creation | < 100ms | Platform adaptation |
| Topic suggestion | < 150ms | 10 suggestions |

## 12. Testing Strategy

### Unit Tests
- Content generation accuracy across all content types
- SEO scoring correctness with known inputs
- Platform limit enforcement for each platform
- Moderation rule evaluation with edge cases
- Performance metric calculation accuracy
- Calendar entry CRUD operations
- Social post adaptation correctness

### Integration Tests
- Full content lifecycle (generate → optimize → moderate → publish)
- Multi-platform content adaptation pipeline
- Calendar scheduling with conflict detection
- Performance tracking with trend analysis
- Moderation chain with multiple rule evaluations

### Acceptance Tests
- End-to-end content operations workflow
- SEO improvement validation against benchmarks
- Performance tracking accuracy over time periods
- Content type consistency across all formats
- Brand compliance verification across moderation rules
