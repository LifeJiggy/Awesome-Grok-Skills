---
name: "Content Delivery"
version: "2.0.0"
description: "Comprehensive content delivery toolkit with multi-format support, adaptive streaming, CDN integration, offline access, and accessibility compliance for educational content"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["ed-tech", "content-delivery", "streaming", "CDN", "accessibility", "multi-format"]
category: "ed-tech"
personality: "content-engineer"
use_cases: ["multi-format content", "adaptive streaming", "CDN integration", "offline access", "accessibility"]
---

# Content Delivery

> Production-grade content delivery framework providing multi-format support, adaptive streaming, CDN integration, offline access, and WCAG 2.1 accessibility compliance for educational content delivery.

## Overview

The Content Delivery module provides tools for delivering educational content across devices and networks. It implements multi-format content packaging, adaptive bitrate streaming, CDN integration with edge caching, offline content synchronization, and comprehensive accessibility compliance. Every delivery pipeline includes analytics, monitoring, and rollback capability.

## Core Capabilities

### 1. Multi-Format Support
- Video (MP4, WebM, HLS, DASH)
- Audio (MP3, AAC, OGG)
- Documents (PDF, EPUB, SCORM)
- Interactive content (HTML5, H5P)
- SCORM/xAPI packages

### 2. Adaptive Streaming
- Adaptive bitrate streaming (ABR)
- Quality selection based on bandwidth
- Multi-resolution encoding
- Segment-based delivery
- Buffer management

### 3. CDN Integration
- Multi-CDN support
- Edge caching policies
- Cache invalidation
- Origin shield configuration
- Geographic routing

### 4. Offline Access
- Service worker integration
- IndexedDB storage
- Background synchronization
- Conflict resolution
- Progressive loading

### 5. Accessibility
- WCAG 2.1 AA compliance
- Screen reader optimization
- Keyboard navigation
- Caption and transcript support
- Color contrast compliance

### 6. Content Analytics
- View tracking and engagement
- Completion rate monitoring
- Bandwidth usage analytics
- Device and browser statistics
- Content performance metrics

## Usage Examples

### Multi-Format Content

```python
from content_delivery import ContentManager, ContentFormat

manager = ContentManager()

# Package content in multiple formats
package = manager.package(
    source="lecture_recording.mp4",
    formats=[ContentFormat.MP4, ContentFormat.WEBM, ContentFormat.HLS],
    quality=["1080p", "720p", "480p"],
)

print(f"Formats: {len(package.formats)}")
for fmt in package.formats:
    print(f"  {fmt.format}: {fmt.size_mb:.1f} MB ({fmt.quality})")
```

### Adaptive Streaming

```python
from content_delivery import StreamingEngine

engine = StreamingEngine()

# Configure adaptive streaming
stream = engine.create_stream(
    content_id="lecture-101",
    source="lecture.mp4",
    abr_profiles=[
        {"quality": "1080p", "bitrate": 5000},
        {"quality": "720p", "bitrate": 2500},
        {"quality": "480p", "bitrate": 1000},
    ],
)

print(f"Stream: {stream.stream_id}")
print(f"Manifest: {stream.manifest_url}")
print(f"Segments: {stream.segment_count}")
```

### CDN Integration

```python
from content_delivery import CDNManager

cdn = CDNManager()

# Configure CDN
distribution = cdn.create_distribution(
    origin="s3://content-bucket",
    domains=["content.example.com"],
    cache_policy={"default_ttl": 86400, "max_ttl": 604800},
    ssl_certificate="arn:aws:acm:us-east-1:123456:certificate/abc",
)

print(f"Distribution: {distribution.id}")
print(f"Domain: {distribution.domain}")
print(f"Status: {distribution.status}")
```

### Offline Access

```python
from content_delivery import OfflineManager

offline = OfflineManager()

# Configure offline access
sync = offline.configure_sync(
    course_id="python-101",
    sync_strategy="progressive",
    storage_limit_mb=500,
    priority_content=["core-lessons", "quizzes"],
)

print(f"Sync: {sync.sync_id}")
print(f"Storage: {sync.storage_limit_mb} MB")
print(f"Priority: {sync.priority_content}")
```

## Best Practices

### Content Packaging
- Provide multiple formats for device compatibility
- Use adaptive streaming for video content
- Optimize file sizes without sacrificing quality
- Include fallback formats for legacy devices

### Streaming
- Configure appropriate ABR profiles
- Set segment duration to 2-6 seconds
- Use CMAF for low-latency delivery
- Monitor buffer health continuously

### CDN
- Set appropriate cache TTLs by content type
- Use cache invalidation for content updates
- Configure origin shield to reduce load
- Monitor CDN performance and costs

### Offline
- Sync content during off-peak hours
- Implement conflict resolution for progress
- Set storage limits per device
- Provide clear offline indicators

### Accessibility
- Include captions for all video content
- Provide transcripts for audio content
- Ensure keyboard navigation works
- Test with screen readers regularly

## Related Modules

- **learning-platforms**: Platform integration for content delivery
- **adaptive-learning**: Adaptive content selection
- **student-analytics**: Content engagement analytics
- **assessment-systems**: Assessment content delivery

---

## Advanced Configuration

### CDN Configuration

```python
from content_delivery import CDNConfig

cdn_config = CDNConfig(
    provider="cloudfront",
    origins=[
        {"domain": "primary.example.com", "weight": 80},
        {"domain": "secondary.example.com", "weight": 20},
    ],
    cache_policies={
        "static_assets": {"ttl": 86400, "compress": True},
        "video_segments": {"ttl": 3600, "compress": False},
        "api_responses": {"ttl": 300, "compress": True},
    },
    ssl_certificate="arn:aws:acm:us-east-1:123456:certificate/abc",
    waf_enabled=True,
    geo_restrictions={"blocked_countries": ["CN", "RU"]},
)
```

### Video Encoding Profiles

```python
from content_delivery import EncodingProfiles

profiles = EncodingProfiles()

# Define encoding ladder
profiles.add_ladder(
    name="educational_standard",
    profiles=[
        {"resolution": "1920x1080", "bitrate": 5000, "codec": "h264"},
        {"resolution": "1280x720", "bitrate": 2500, "codec": "h264"},
        {"resolution": "854x480", "bitrate": 1000, "codec": "h264"},
        {"resolution": "640x360", "bitrate": 500, "codec": "h264"},
    ],
    audio_profiles=[
        {"codec": "aac", "bitrate": 128, "channels": 2},
        {"codec": "aac", "bitrate": 64, "channels": 1},
    ],
)

# Generate manifests
manifests = profiles.generate_manifests(
    source="lecture.mp4",
    formats=["hls", "dash"],
    output_dir="/output/manifests",
)
```

## Architecture Patterns

### Content Delivery Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Upload    │────▶│  Processing  │────▶│  Storage    │
│   Portal    │     │  Queue       │     │  (S3)       │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                                                ▼
┌─────────────────┐     ┌─────────────────────────┐
│  CDN Edge       │◀────│  Manifest Generation     │
│  Servers        │     └─────────────────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────┐
│  Player Client  │────▶│  Analytics  │
│                 │     │  Collection │
└─────────────────┘     └─────────────┘
```

### Multi-Region Architecture

```python
from content_delivery import MultiRegionConfig

region_config = MultiRegionConfig(
    regions={
        "us-east-1": {"priority": 1, "origin": "s3://us-east-content"},
        "eu-west-1": {"priority": 2, "origin": "s3://eu-west-content"},
        "ap-southeast-1": {"priority": 3, "origin": "s3://ap-se-content"},
    },
    routing="latency_based",
    failover=True,
    health_check_interval=60,
)
```

## Integration Guide

### Video Platform Integration

```python
from content_delivery import VideoIntegration

video = VideoIntegration(provider="vimeo")

# Upload and process video
video_upload = video.upload(
    source="lecture.mp4",
    metadata={
        "title": "Introduction to Python",
        "course_id": "python-101",
        "chapter": 1,
    },
    encoding_profile="educational_standard",
)

print(f"Video ID: {video_upload.video_id}")
print(f"HLS URL: {video_upload.hls_url}")
print(f"DASH URL: {video_upload.dash_url}")

# Set up webhooks
video.configure_webhooks(
    events=["encoding.complete", "analytics.update"],
    endpoint="https://platform.example.com/webhooks/video",
)
```

### Storage Integration

```python
from content_delivery import StorageManager

storage = StorageManager()

# Configure multi-tier storage
storage.configure_tiers(
    hot={
        "provider": "s3",
        "bucket": "content-hot",
        "ttl_days": 30,
    },
    warm={
        "provider": "s3-ia",
        "bucket": "content-warm",
        "ttl_days": 90,
    },
    cold={
        "provider": "glacier",
        "bucket": "content-cold",
        "ttl_days": 365,
    },
)

# Move content between tiers
storage.lifecycle_rule(
    prefix="videos/",
    transitions=[
        {"days": 30, "target": "warm"},
        {"days": 90, "target": "cold"},
    ],
)
```

## Performance Optimization

### Bandwidth Optimization

```python
from content_delivery import BandwidthOptimizer

optimizer = BandwidthOptimizer()

# Analyze and optimize
analysis = optimizer.analyze_usage(
    time_range_days=30,
    content_type="video",
)

print(f"Total bandwidth: {analysis.total_gb:.1f} GB")
print(f"Cost: ${analysis.cost_usd:.2f}")
print(f"Optimization opportunities:")
for opp in optimization.opportunities:
    print(f"  {opp.description}: ${opp.savings_usd:.2f}/month")
```

### Cache Optimization

```python
from content_delivery import CacheOptimizer

cache_opt = CacheOptimizer()

# Optimize cache policies
optimized = cache_opt.optimize(
    distribution_id="dist-123",
    metrics={
        "hit_rate_target": 0.95,
        "latency_target_ms": 50,
    },
)

print(f"Current hit rate: {optimized.current_hit_rate:.1%}")
print(f"Projected hit rate: {optimized.projected_hit_rate:.1%}")
print(f"Recommended changes: {optimized.recommendations}")
```

## Security Considerations

### Content Protection

```python
from content_delivery import DRMManager

drm = DRMManager()

# Configure DRM
drm_config = drm.configure(
    provider="widevine",
    license_server="https://license.example.com",
    encryption_key="your-encryption-key",
    output_protected=True,
)

# Generate DRM-protected content
protected = drm.protect_content(
    content_id="video-123",
    encryption=drm_config,
    output_formats=["hls", "dash"],
)
```

### Signed URLs

```python
from content_delivery import SignedURLGenerator

url_gen = SignedURLGenerator()

# Generate signed URL
signed_url = url_gen.generate(
    resource="https://content.example.com/videos/lecture-101.mp4",
    expiry_minutes=60,
    ip_restrictions=["192.168.1.0/24"],
    download_count_limit=5,
)

print(f"Signed URL: {signed_url.url}")
print(f"Expires: {signed_url.expires_at}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Video buffering | Low ABR profiles | Add lower bitrate options |
| High CDN costs | Poor cache hit rate | Optimize cache policies |
| Playback errors | DRM issues | Verify license server |
| Slow uploads | Large files | Use multipart upload |
| Offline sync conflicts | Concurrent edits | Implement conflict resolution |

### Debug Mode

```python
from content_delivery import enable_debug

enable_debug(
    components=["cdn", "encoding", "player"],
    log_level="DEBUG",
    trace_requests=True,
)
```

## API Reference

### REST Endpoints

```
POST   /api/v1/content/upload               Upload content
GET    /api/v1/content/{id}                 Get content details
DELETE /api/v1/content/{id}                 Delete content
GET    /api/v1/content/{id}/stream          Get streaming URLs
GET    /api/v1/content/{id}/analytics       Get engagement analytics
POST   /api/v1/content/{id}/transcode      Trigger transcoding
GET    /api/v1/cdn/distributions            List CDN distributions
POST   /api/v1/cdn/invalidate              Invalidate cache
```

### Data Models

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class Content:
    id: UUID
    title: str
    content_type: str
    source_url: str
    formats: List["ContentFormat"]
    duration_seconds: Optional[int]
    created_at: datetime

@dataclass
class ContentFormat:
    format: str
    quality: str
    size_mb: float
    bitrate_kbps: int
    url: str

@dataclass
class StreamingManifest:
    content_id: UUID
    hls_url: str
    dash_url: str
    thumbnail_url: str
    duration_seconds: int

@dataclass
class EngagementMetrics:
    content_id: UUID
    views: int
    unique_viewers: int
    avg_watch_time_seconds: float
    completion_rate: float
    drop_off_points: List[float]
```

## Deployment Guide

### Kubernetes Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: content-delivery
spec:
  replicas: 3
  selector:
    matchLabels:
      app: content-delivery
  template:
    spec:
      containers:
      - name: api
        image: content-delivery:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        env:
        - name: CDN_PROVIDER
          value: "cloudfront"
        - name: STORAGE_BUCKET
          valueFrom:
            secretKeyRef:
              name: content-secrets
              key: storage-bucket
```

## Monitoring & Observability

### Key Metrics

```python
from content_delivery import Metrics

metrics = Metrics()

# Track delivery performance
metrics.histogram("content.delivery_latency_ms", latency, tags={"format": "hls"})
metrics.counter("content.views_total", tags={"content_type": "video"})

# Track CDN performance
metrics.gauge("cdn.hit_rate", hit_rate, tags={"distribution": "dist-123"})
metrics.gauge("cdn.bandwidth_gb", bandwidth, tags={"region": "us-east-1"})
```

## Testing Strategy

### Load Testing

```python
from content_delivery import LoadTest

load_test = LoadTest()

# Simulate concurrent viewers
results = load_test.simulate(
    content_id="video-101",
    concurrent_viewers=1000,
    duration_minutes=30,
    viewer_behavior="mixed",
)

print(f"Buffering events: {results.buffering_events}")
print(f"Avg startup time: {results.avg_startup_ms:.0f}ms")
print(f"Error rate: {results.error_rate:.2%}")
```

## Versioning & Migration

### Version History

- **2.0.0**: Added multi-CDN, DRM, advanced analytics
- **1.5.0**: Added offline sync, adaptive streaming
- **1.0.0**: Initial release with basic delivery

## Glossary

| Term | Definition |
|------|------------|
| **ABR** | Adaptive Bitrate Streaming |
| **HLS** | HTTP Live Streaming |
| **DASH** | Dynamic Adaptive Streaming over HTTP |
| **CDN** | Content Delivery Network |
| **DRM** | Digital Rights Management |
| **CMAF** | Common Media Application Format |
| **Manifest** | Playlist file for streaming |

## Changelog

### Version 2.0.0
- Multi-CDN support
- DRM integration
- Advanced analytics
- Multi-region deployment

### Version 1.5.0
- Adaptive streaming
- Offline content sync
- CDN optimization

### Version 1.0.0
- Initial release
- Basic content delivery
- Simple analytics

## Contributing Guidelines

1. Test with real content
2. Validate across devices
3. Document API changes
4. Monitor performance impact

## Accessibility Deep Dive

### Screen Reader Optimization

```python
from content_delivery import AccessibilityOptimizer

optimizer = AccessibilityOptimizer()

# Optimize content for screen readers
optimized = optimizer.optimize_for_screen_reader(
    content_id="lecture-101",
    settings={
        "alt_text_required": True,
        "aria_labels": True,
        "heading_hierarchy": True,
        "table_captions": True,
        "form_labels": True,
    },
)

print(f"Accessibility Score: {optimized.score:.0%}")
print(f"Issues Fixed: {optimized.issues_fixed}")
print(f"Remaining Issues: {optimized.remaining_issues}")
```

### Caption and Transcript Generation

```python
from content_delivery import CaptionGenerator

caption_gen = CaptionGenerator()

# Generate captions for video
captions = caption_gen.generate(
    video_id="lecture-101",
    languages=["en", "es", "fr"],
    auto_align=True,
    max_chars_per_line=42,
)

print(f"Captions generated for {len(captions.languages)} languages")
print(f"Segments: {captions.segment_count}")
print(f"Accuracy: {captions.accuracy:.1%}")
```

### Color Contrast Compliance

```python
from content_delivery import ContrastChecker

checker = ContrastChecker()

# Check contrast ratios
report = checker.check_content(
    content_id="slide-deck-101",
    standard="WCAG_AA",
)

print(f"Contrast Report:")
print(f"  Pass Rate: {report.pass_rate:.1%}")
print(f"  Failures: {report.failure_count}")
for failure in report.failures[:3]:
    print(f"    {failure.element}: {failure.ratio:.1f}:1 (need {failure.required_ratio}:1)")
```

## Content Protection Strategies

### Digital Watermarking

```python
from content_delivery import WatermarkManager

watermark = WatermarkManager()

# Apply invisible watermark
watermarked = watermark.apply(
    content_id="lecture-101",
    watermark_type="invisible",
    user_id="student@example.com",
    tracking_id="track-abc123",
)

print(f"Watermark applied: {watermarked.id}")
print(f"Detection confidence: {watermarked.detection_confidence:.1%}")
```

### DRM Configuration

```python
from content_delivery import DRMConfig

drm_config = DRMConfig(
    widevine={
        "security_level": "L1",
        "hdcp_required": True,
        "persistent_license": False,
    },
    fairplay={
        "server_url": "https://fps.example.com",
        "certificate": "/certs/fairplay.pem",
    },
    playready={
        "la_url": "https://playready.example.com/license",
        "header_object_id": "urn:uuid:9a04f079-9840-4286-ab92-e65be0885f95",
    },
)
```

## Offline-First Architecture

### Service Worker Configuration

```python
from content_delivery import ServiceWorkerConfig

sw_config = ServiceWorkerConfig(
    cache_strategies={
        "static_assets": "cache_first",
        "api_responses": "network_first",
        "video_segments": "stale_while_revalidate",
    },
    cache_sizes={
        "pages": 50,
        "assets": 200,
        "api_cache": 100,
    },
    sync_strategy="background_sync",
)

# Generate service worker
sw_code = sw_config.generate()
print(f"Service Worker generated: {len(sw_code)} bytes")
```

### IndexedDB Storage Manager

```python
from content_delivery import OfflineStorage

storage = OfflineStorage(
    database="edu_content_db",
    version=1,
    stores=[
        {"name": "courses", "keyPath": "course_id"},
        {"name": "lessons", "keyPath": "lesson_id"},
        {"name": "progress", "keyPath": "user_lesson_id"},
        {"name": "quizzes", "keyPath": "quiz_id"},
    ],
)

# Store content for offline
storage.store(
    store="courses",
    data={
        "course_id": "python-101",
        "title": "Python Fundamentals",
        "lessons": ["intro", "variables", "loops"],
        "cached_at": "2024-01-15T10:00:00Z",
    },
)

# Sync when online
sync_result = storage.sync_pending(
    endpoint="https://api.example.com/sync",
    batch_size=50,
)
print(f"Synced: {sync_result.synced_count} items")
print(f"Pending: {sync_result.pending_count} items")
```

### Content Prioritization for Offline

```python
from content_delivery import ContentPrioritizer

prioritizer = ContentPrioritizer()

# Prioritize content for offline download
priorities = prioritizer.prioritize(
    course_id="python-101",
    user_progress={"completed": ["intro"], "current": "variables"},
    storage_limit_mb=200,
)

print(f"Offline Download Priorities:")
for item in priorities.items:
    print(f"  {item.title}: Priority {item.priority} ({item.size_mb:.1f} MB)")
print(f"Total size: {priorities.total_size_mb:.1f} MB")
print(f"Storage used: {priorities.storage_usage:.1%}")
```

## Content Analytics Deep Dive

### Engagement Heatmaps

```python
from content_delivery import EngagementHeatmap

heatmap = EngagementHeatmap()

# Generate engagement heatmap
data = heatmap.generate(
    video_id="lecture-101",
    resolution_seconds=5,
)

print(f"Engagement Heatmap:")
print(f"  Total data points: {len(data.points)}")
print(f"  Peak engagement: {data.peak_timestamp}s ({data.peak_engagement:.1%})")
print(f"  Lowest engagement: {data.low_timestamp}s ({data.low_engagement:.1%})")
print(f"  Average engagement: {data.avg_engagement:.1%}")
```

### Drop-off Analysis

```python
from content_delivery import DropoffAnalyzer

analyzer = DropoffAnalyzer()

# Analyze where viewers stop watching
dropoffs = analyzer.analyze(
    video_id="lecture-101",
    total_viewers=500,
)

print(f"Drop-off Analysis:")
for point in dropoffs.significant_dropoffs:
    print(f"  {point.timestamp}s: {point.dropoff_rate:.1%} dropped ({point.remaining_viewers} remaining)")
    print(f"    Reason: {point.possible_reason}")
```

### A/B Testing for Content

```python
from content_delivery import ContentABTest

ab_test = ContentABTest()

# Test content variants
test = ab_test.create_test(
    name="Video Intro Test",
    content_id="lecture-101",
    variants=[
        {"name": "control", "intro": "standard"},
        {"name": "short_intro", "intro": "10s_hook"},
    ],
    metric="completion_rate",
    traffic_split=50,
    duration_days=14,
)

results = ab_test.get_results(test.id)
print(f"A/B Test Results:")
print(f"  Winner: {results.winner}")
print(f"  Improvement: {results.improvement:.1%}")
print(f"  Statistical Significance: {results.is_significant}")
```

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills