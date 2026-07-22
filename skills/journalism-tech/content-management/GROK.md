---
name: "content-management"
category: "journalism-tech"
version: "2.0.0"
tags: ["journalism", "content", "cms", "publishing", "workflow"]
description: "Journalism content management and publishing workflow systems"
---

# Content Management

## Overview

The Content Management module provides editorial workflow tools for newsrooms, including article management, editorial review workflows, version control, scheduling, and multi-platform publishing. It supports collaborative editing, fact-check integration, media management, and analytics for content performance tracking.

## Core Capabilities

- **Article Management**: Create, edit, and manage news articles
- **Editorial Workflow**: Configure editorial review and approval processes
- **Version Control**: Track article changes and revisions
- **Media Library**: Manage images, videos, and documents
- **Scheduling**: Schedule content publication across time zones
- **Multi-Platform Publishing**: Publish to web, mobile, social, and print
- **Content Analytics**: Track content performance and engagement
- **SEO Optimization**: Optimize content for search engines

## Usage Examples

### Article Management

```python
from content_management import CMSManager, Article

cms = CMSManager()

# Create article
article = Article(
    title="City Budget Analysis Reveals Key Findings",
    author="Jane Smith",
    content="An in-depth analysis of the city's budget...",
    category="investigative",
    tags=["budget", "finance", "local-government"],
    featured_image="budget-chart.png",
)

# Save draft
draft = cms.save_draft(article)
print(f"Draft Saved: {draft.id}")
print(f"Version: {draft.version}")

# Submit for review
cms.submit_for_review(draft.id)
```

### Editorial Workflow

```python
from content_management import EditorialWorkflow, ReviewStage

workflow = EditorialWorkflow(
    stages=[
        ReviewStage(name="copy_edit", reviewer_pool="copy-editors"),
        ReviewStage(name="fact_check", reviewer_pool="fact-checkers"),
        ReviewStage(name="editorial_approval", reviewer_pool="editors-in-chief"),
    ],
)

# Process article through workflow
status = workflow.process(article_id="art-001")
print(f"Workflow Status:")
print(f"  Current Stage: {status.current_stage}")
print(f"  Status: {status.status}")
print(f"  Reviewers: {status.assigned_reviewers}")
```

### Content Scheduling

```python
from content_management import ContentScheduler

scheduler = ContentScheduler()

# Schedule publication
schedule = scheduler.schedule(
    article_id="art-001",
    publish_time="2024-01-16T08:00:00Z",
    platforms=["website", "mobile_app", "twitter"],
    timezone="America/New_York",
)

print(f"Publication Scheduled:")
print(f"  Article: {schedule.article_id}")
print(f"  Publish Time: {schedule.publish_time}")
print(f"  Platforms: {schedule.platforms}")
```

### Content Analytics

```python
from content_management import ContentAnalytics

analytics = ContentAnalytics()

# Get article performance
performance = analytics.get_performance(
    article_id="art-001",
    time_range="7d",
)

print(f"Article Performance:")
print(f"  Views: {performance.views}")
print(f"  Unique Readers: {performance.unique_readers}")
print(f"  Average Time: {performance.avg_time_on_page:.1f}s")
print(f"  Social Shares: {performance.social_shares}")
print(f"  Engagement Score: {performance.engagement_score:.1%}")
```

## Best Practices

- **Clear Workflows**: Define clear editorial workflows for each content type
- **Version Control**: Always maintain version history
- **Fact-Check Integration**: Integrate fact-checking into editorial workflow
- **SEO Best Practices**: Optimize headlines, meta descriptions, and structure
- **Multi-Platform Strategy**: Plan content for multiple platforms
- **Analytics Review**: Regularly review content performance
- **Collaborative Editing**: Enable real-time collaboration
- **Archival**: Maintain searchable content archives

## Related Modules

- **data-journalism**: Data analysis for content
- **fact-checking**: Fact-check integration
- **audience-analytics**: Audience engagement tracking

---

## Advanced Configuration

### Editorial Workflow Configuration

```python
workflow_config = {
    "default_workflow": {
        "stages": [
            {"name": "draft", "type": "author", "auto_assign": True},
            {"name": "copy_edit", "type": "reviewer", "pool": "copy-editors"},
            {"name": "fact_check", "type": "reviewer", "pool": "fact-checkers"},
            {"name": "editorial_approval", "type": "approver", "pool": "editors-in-chief"},
            {"name": "publish", "type": "auto", "trigger": "approval"},
        ],
        "parallel_stages": False,
        "auto_approve_threshold": 0.9,
    },
    "breaking_news_workflow": {
        "stages": [
            {"name": "draft", "type": "author", "auto_assign": True},
            {"name": "quick_review", "type": "reviewer", "pool": "editors-on-duty"},
            {"name": "publish", "type": "auto", "trigger": "approval"},
        ],
    },
}
```

### Media Library Configuration

```python
media_config = {
    "supported_formats": ["jpg", "png", "gif", "mp4", "pdf"],
    "max_file_size_mb": 100,
    "image_processing": {
        "auto_optimize": True,
        "responsive_sizes": [320, 640, 960, 1280],
        "webp_conversion": True,
    },
    "video_processing": {
        "transcode": True,
        "formats": ["mp4", "webm"],
        "quality": ["720p", "1080p"],
    },
}
```

### Scheduling Configuration

```python
scheduling_config = {
    "timezone": "America/New_York",
    "publish_windows": {
        "peak_hours": {"start": 6, "end": 21},
        "breaking_news": {"immediate": True},
    },
    "social_media_sync": True,
    "email_newsletter_sync": True,
}
```

### SEO Configuration

```python
seo_config = {
    "auto_generate_meta": True,
    "keyword_suggestions": True,
    "readability_check": True,
    "internal_linking": True,
    "schema_markup": True,
    "sitemap_generation": True,
}
```

### Multi-Platform Publishing

```python
publishing_config = {
    "platforms": {
        "website": {"enabled": True, "format": "html"},
        "mobile_app": {"enabled": True, "format": "native"},
        "email_newsletter": {"enabled": True, "format": "html"},
        "social_media": {"enabled": True, "platforms": ["twitter", "facebook", "linkedin"]},
        "print": {"enabled": True, "format": "pdf"},
    },
    "cross_posting": True,
    "utm_tracking": True,
}
```

## Architecture Patterns

### Editorial Workflow Architecture

```
┌─────────────────────────────────────────────────┐
│              Content Creation Layer              │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │Author   │  │Editor   │  │ Fact-Checker    ││
│  │Draft    │  │Review   │  │ Verify          ││
│  └────┬────┘  └────┬────┘  └───────┬─────────┘│
│       │            │               │           │
├───────┴────────────┴───────────────┴───────────┤
│              Workflow Engine Layer               │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │ Stage   │  │ Task    │  │ Notification    ││
│  │ Manager │  │ Queue   │  │ Engine          ││
│  └────┬────┘  └────┬────┘  └───────┬─────────┘│
│       │            │               │           │
├───────┴────────────┴───────────────┴───────────┤
│              Publishing Layer                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │ Web     │  │ Mobile  │  │ Social          ││
│  │ CMS     │  │ App     │  │ Media           ││
│  └─────────┘  └─────────┘  └─────────────────┘│
└─────────────────────────────────────────────────┘
```

### Version Control Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  New        │────▶│  Version     │────▶│  Review     │
│  Version    │     │  Created     │     │  Queue      │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Approve│           │  Revise   │         │  Reject   │
                    └─────────┘           └───────────┘         └───────────┘
```

### Multi-Platform Publishing Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Approved   │────▶│  Platform    │────▶│  Content    │
│  Article    │     │  Router      │     │  Adapters   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
         ┌───────────────────────────────────────┼───────────────────────────────────────┐
         │                    │                    │                    │                 │
    ┌────┴────┐          ┌────┴────┐          ┌────┴────┐          ┌────┴────┐     ┌────┴────┐
    │ Website │          │ Mobile  │          │ Email   │          │ Social  │     │ Print   │
    │ CMS     │          │ App     │          │ Newsletter│        │ Media   │     │ PDF     │
    └─────────┘          └─────────┘          └─────────┘          └─────────┘     └─────────┘
```

## Integration Guide

### CMS Integration

```python
def integrate_with_cms(article, cms_config):
    # Prepare article for CMS
    prepared = prepare_for_cms(article, cms_config.format)

    # Publish to CMS
    result = cms_api.publish(
        title=prepared.title,
        content=prepared.content,
        author=prepared.author,
        category=prepared.category,
        tags=prepared.tags,
    )
    return {"article_id": result.id, "url": result.url}
```

### Social Media Integration

```python
def publish_to_social_media(article, social_config):
    # Create social posts
    posts = create_social_posts(article, social_config.platforms)

    # Schedule posts
    for post in posts:
        social_api.schedule_post(
            platform=post.platform,
            content=post.content,
            media=post.media,
            schedule_time=post.schedule_time,
        )
```

### Email Newsletter Integration

```python
def send_newsletter(article, newsletter_config):
    # Prepare newsletter
    newsletter = prepare_newsletter(article, newsletter_config.template)

    # Send to subscribers
    result = newsletter_api.send(
        subject=newsletter.subject,
        content=newsletter.content,
        recipients=newsletter.recipients,
        schedule_time=newsletter.send_time,
    )
    return {"campaign_id": result.id}
```

### Analytics Integration

```python
def track_content_performance(article, analytics_config):
    # Track article metrics
    analytics_api.track(
        article_id=article.id,
        metrics=["views", "reads", "shares", "comments"],
        time_range="30d",
    )
```

## Performance Optimization

### Content Delivery Optimization

```python
delivery_optimization = {
    "cdn_enabled": True,
    "edge_locations": ["us-east-1", "eu-west-1", "ap-southeast-1"],
    "image_optimization": True,
    "lazy_loading": True,
    "compression": True,
}
```

### Database Optimization

```python
db_optimization = {
    "indexing": ["article_id", "author", "publish_date", "category"],
    "connection_pool_size": 20,
    "read_replicas": 2,
    "query_timeout": 10,
}
```

### Caching Strategy

```python
cache_config = {
    "article_cache_ttl": 300,
    "media_cache_ttl": 86400,
    "search_cache_ttl": 60,
    "cache_backend": "redis",
}
```

## Security Considerations

### Content Security

```python
content_security = {
    "xss_protection": True,
    "content_security_policy": True,
    "sanitization": True,
    "malware_scanning": True,
    "access_control": True,
}
```

### User Security

```python
user_security = {
    "role_based_access": True,
    "multi_factor_auth": True,
    "session_management": True,
    "audit_logging": True,
    "password_policy": True,
}
```

### Data Security

```python
data_security = {
    "encryption_at_rest": True,
    "encryption_in_transit": True,
    "backup_enabled": True,
    "disaster_recovery": True,
    "data_retention_policy": True,
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Workflow stuck | Missing approval | Check reviewer assignments |
| Media upload failed | File size exceeded | Compress files |
| Scheduling error | Timezone mismatch | Verify timezone settings |
| SEO issues | Missing metadata | Run SEO audit |
| Publishing delay | Platform API issues | Check platform status |

### Debug Commands

```bash
# Check article status
cms-cli status --article-id art-001

# View workflow
cms-cli workflow --article-id art-001

# Test publishing
cms-cli test-publish --article-id art-001 --platform website
```

## API Reference

### CMSManager

```python
class CMSManager:
    def __init__(self):
        """Initialize CMS manager."""

    def save_draft(self, article: Article) -> Draft:
        """Save article draft."""

    def submit_for_review(self, article_id: str) -> None:
        """Submit article for review."""

    def publish(self, article_id: str) -> PublishedArticle:
        """Publish article."""
```

### Article

```python
@dataclass
class Article:
    title: str
    author: str
    content: str
    category: str
    tags: List[str]
    featured_image: str = None
```

### EditorialWorkflow

```python
class EditorialWorkflow:
    def __init__(self, stages: List[ReviewStage]):
        """Initialize editorial workflow."""

    def process(self, article_id: str) -> WorkflowStatus:
        """Process article through workflow."""
```

### ContentScheduler

```python
class ContentScheduler:
    def __init__(self):
        """Initialize content scheduler."""

    def schedule(self, article_id: str, publish_time: str, platforms: List[str]) -> Schedule:
        """Schedule article publication."""
```

### ContentAnalytics

```python
class ContentAnalytics:
    def __init__(self):
        """Initialize content analytics."""

    def get_performance(self, article_id: str, time_range: str) -> ArticlePerformance:
        """Get article performance metrics."""
```

## Data Models

### Draft

```python
@dataclass
class Draft:
    id: str
    article: Article
    version: int
    created_at: datetime
    updated_at: datetime
```

### WorkflowStatus

```python
@dataclass
class WorkflowStatus:
    article_id: str
    current_stage: str
    status: str
    assigned_reviewers: List[str]
    created_at: datetime
    updated_at: datetime
```

### Schedule

```python
@dataclass
class Schedule:
    article_id: str
    publish_time: str
    platforms: List[str]
    timezone: str
    status: str
```

### ArticlePerformance

```python
@dataclass
class ArticlePerformance:
    article_id: str
    views: int
    unique_readers: int
    avg_time_on_page: float
    social_shares: int
    engagement_score: float
```

## Deployment Guide

### Initial Setup

```bash
# Initialize CMS
cms-cli init

# Configure workflows
cms-cli configure --workflows workflows.yaml

# Import content
cms-cli import --source archive/
```

### Production Deployment

```bash
# Deploy to server
cms-cli deploy --config production.yaml

# Verify deployment
cms-cli verify --endpoints all
```

## Monitoring & Observability

### CMS Metrics

```python
metrics_config = {
    "articles_published": "counter",
    "workflow_completion_time": "histogram",
    "media_uploads": "counter",
    "seo_score": "gauge",
    "engagement_rate": "gauge",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Content Management Dashboard",
    "panels": [
        "editorial_pipeline",
        "content_performance",
        "seo_metrics",
        "publication_schedule",
    ],
}
```

## Testing Strategy

### Unit Tests

```python
def test_article_creation():
    cms = CMSManager()
    article = Article(title="Test", author="Test Author", content="Test content")
    draft = cms.save_draft(article)
    assert draft.id is not None
```

### Integration Tests

```python
def test_workflow_processing():
    workflow = EditorialWorkflow(mock_stages)
    status = workflow.process("art-001")
    assert status.status == "in_progress"
```

## Versioning & Migration

### Content Versioning

```python
version_config = {
    "article_versioning": True,
    "media_versioning": True,
    "rollback_enabled": True,
    "version_history_days": 365,
}
```

## Glossary

| Term | Definition |
|------|------------|
| **CMS** | Content Management System |
| **Editorial Workflow** | Process for content review and approval |
| **SEO** | Search Engine Optimization |
| **Multi-Platform Publishing** | Publishing to multiple channels |
| **Content Analytics** | Tracking content performance |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with multi-platform |
| 1.5.0 | 2024-11-01 | Added SEO optimization |
| 1.4.0 | 2024-09-15 | Enhanced workflow engine |
| 1.3.0 | 2024-07-20 | Media library improvements |
| 1.2.0 | 2024-05-10 | Scheduling enhancements |
| 1.1.0 | 2024-03-01 | Analytics integration |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow editorial standards
2. Test workflows thoroughly
3. Document content processes
4. Review for SEO
5. Verify multi-platform rendering

## Editorial Analytics

### Content Pipeline Metrics

```python
from content_management import PipelineMetrics

metrics = PipelineMetrics()

# Analyze editorial pipeline
report = metrics.analyze(
    time_range_days=30,
    stages=["draft", "copy_edit", "fact_check", "approval", "publish"],
)

print(f"Editorial Pipeline Metrics:")
print(f"  Total Articles: {report.total_articles}")
print(f"  Avg Time to Publish: {report.avg_time_to_publish_hours:.1f} hours")
for stage in report.stage_metrics:
    print(f"  {stage.name}: {stage.avg_hours:.1f}h (bottleneck: {stage.is_bottleneck})")
```

### Author Performance

```python
from content_management import AuthorAnalytics

author_analytics = AuthorAnalytics()

# Analyze author performance
performance = author_analytics.analyze(
    time_range_days=30,
    metrics=["output", "engagement", "quality"],
)

for author in performance.authors[:5]:
    print(f"\n{author.name}:")
    print(f"  Articles Published: {author.article_count}")
    print(f"  Avg Engagement Score: {author.avg_engagement:.1%}")
    print(f"  Avg Read Time: {author.avg_read_time_seconds:.0f}s")
    print(f"  SEO Score: {author.avg_seo_score:.0f}/100")
```

## License

MIT License. See LICENSE file for full terms.
