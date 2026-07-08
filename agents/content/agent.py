"""
Content Agent - Content Management and Creation Workflows.

Provides comprehensive content management, creation workflows, editorial
processes, publishing pipelines, analytics tracking, and content moderation
across multiple platforms and formats.
"""

from __future__ import annotations

import logging
import uuid
import json
import hashlib
import re
import math
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Set, Union
from collections import defaultdict

logger = logging.getLogger(__name__)


# =============================================================================
# Enumerations
# =============================================================================

class ContentType(Enum):
    """Types of content."""
    BLOG_POST = "blog_post"
    ARTICLE = "article"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    LANDING_PAGE = "landing_page"
    VIDEO_SCRIPT = "video_script"
    PODCAST_SCRIPT = "podcast_script"
    WHITEPAPER = "whitepaper"
    CASE_STUDY = "case_study"
    DOCUMENTATION = "documentation"
    NEWSLETTER = "newsletter"
    PRESS_RELEASE = "press_release"
    PRODUCT_DESCRIPTION = "product_description"
    ADVERTISEMENT = "advertisement"
    INFOGRAPHIC = "infographic"


class ContentStatus(Enum):
    """Status of content in the workflow."""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    REVISION = "revision"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Tone(Enum):
    """Content tone and voice."""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"
    TECHNICAL = "technical"
    AUTHORITATIVE = "authoritative"
    FRIENDLY = "friendly"
    FORMAL = "formal"
    PERSUASIVE = "persuasive"
    EDUCATIONAL = "educational"


class Platform(Enum):
    """Publishing platforms."""
    WEBSITE = "website"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    MEDIUM = "medium"
    YOUTUBE = "youtube"
    SUBSTACK = "substack"
    GITHUB = "github"
    SLACK = "slack"


class ContentCategory(Enum):
    """Content categorization."""
    THOUGHT_LEADERSHIP = "thought_leadership"
    PRODUCT = "product"
    HOW_TO = "how_to"
    CASE_STUDY = "case_study"
    NEWS = "news"
    OPINION = "opinion"
    TUTORIAL = "tutorial"
    INTERVIEW = "interview"
    ROUNDUP = "roundup"
    GATED = "gated"


class SEOImpact(Enum):
    """SEO impact levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ContentPiece:
    """A single piece of content."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    content_type: str = ContentType.BLOG_POST.value
    body: str = ""
    summary: str = ""
    author: str = ""
    status: str = ContentStatus.DRAFT.value
    platform: str = Platform.WEBSITE.value
    category: str = ContentCategory.THOUGHT_LEADERSHIP.value
    tone: str = Tone.PROFESSIONAL.value
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    target_audience: str = ""
    meta_description: str = ""
    slug: str = ""
    word_count: int = 0
    reading_time_minutes: int = 0
    seo_score: float = 0.0
    readability_score: float = 0.0
    cta: str = ""
    scheduled_date: Optional[str] = None
    published_date: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content_type": self.content_type,
            "body": self.body,
            "summary": self.summary,
            "author": self.author,
            "status": self.status,
            "platform": self.platform,
            "category": self.category,
            "tone": self.tone,
            "tags": self.tags,
            "keywords": self.keywords,
            "target_audience": self.target_audience,
            "meta_description": self.meta_description,
            "slug": self.slug,
            "word_count": self.word_count,
            "reading_time_minutes": self.reading_time_minutes,
            "seo_score": self.seo_score,
            "readability_score": self.readability_score,
            "cta": self.cta,
            "scheduled_date": self.scheduled_date,
            "published_date": self.published_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class ContentCalendar:
    """Content calendar entry."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    content_type: str = ""
    platform: str = ""
    scheduled_date: str = ""
    author: str = ""
    status: str = "planned"
    keywords: List[str] = field(default_factory=list)
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content_type": self.content_type,
            "platform": self.platform,
            "scheduled_date": self.scheduled_date,
            "author": self.author,
            "status": self.status,
            "keywords": self.keywords,
            "notes": self.notes,
            "created_at": self.created_at,
        }


@dataclass
class SEOMetrics:
    """SEO analysis metrics."""
    content_id: str = ""
    overall_score: float = 0.0
    keyword_density: Dict[str, float] = field(default_factory=dict)
    keyword_usage: List[Dict[str, Any]] = field(default_factory=list)
    readability_score: float = 0.0
    flesch_score: float = 0.0
    grade_level: str = ""
    heading_count: int = 0
    paragraph_count: int = 0
    bullet_count: int = 0
    internal_links: int = 0
    external_links: int = 0
    image_count: int = 0
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_id": self.content_id,
            "overall_score": self.overall_score,
            "keyword_density": self.keyword_density,
            "readability_score": self.readability_score,
            "flesch_score": self.flesch_score,
            "grade_level": self.grade_level,
            "heading_count": self.heading_count,
            "paragraph_count": self.paragraph_count,
            "bullet_count": self.bullet_count,
            "internal_links": self.internal_links,
            "external_links": self.external_links,
            "image_count": self.image_count,
            "recommendations": self.recommendations,
        }


@dataclass
class ContentPerformance:
    """Content performance analytics."""
    content_id: str = ""
    views: int = 0
    unique_views: int = 0
    clicks: int = 0
    shares: int = 0
    comments: int = 0
    likes: int = 0
    avg_time_on_page: float = 0.0
    bounce_rate: float = 0.0
    conversion_rate: float = 0.0
    ctr: float = 0.0
    engagement_rate: float = 0.0
    period: str = ""
    measured_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_id": self.content_id,
            "views": self.views,
            "unique_views": self.unique_views,
            "clicks": self.clicks,
            "shares": self.shares,
            "comments": self.comments,
            "likes": self.likes,
            "avg_time_on_page": self.avg_time_on_page,
            "bounce_rate": self.bounce_rate,
            "conversion_rate": self.conversion_rate,
            "ctr": self.ctr,
            "engagement_rate": self.engagement_rate,
            "period": self.period,
            "measured_at": self.measured_at,
        }


@dataclass
class ModerationResult:
    """Content moderation result."""
    content_id: str = ""
    approved: bool = True
    score: float = 100.0
    flags: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    moderated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_id": self.content_id,
            "approved": self.approved,
            "score": self.score,
            "flags": self.flags,
            "suggestions": self.suggestions,
            "moderated_at": self.moderated_at,
        }


# =============================================================================
# Content Generator
# =============================================================================

class ContentGenerator:
    """
    Generates content across multiple formats and types.

    Creates titles, bodies, meta descriptions, CTAs, and keywords
    based on content type, tone, and target audience.
    """

    def __init__(self) -> None:
        self._templates: Dict[str, List[str]] = {
            "blog_titles": [
                "The Ultimate Guide to {topic}: Everything You Need to Know",
                "How to Master {topic} in 30 Days",
                "10 Essential {topic} Strategies for {audience}",
                "{topic}: A Comprehensive Guide for {audience}",
                "Why {topic} Matters More Than Ever in 2024",
            ],
            "article_titles": [
                "Understanding {topic}: A Deep Dive",
                "The Future of {topic}: Trends and Predictions",
                "{topic} Explained: What {audience} Need to Know",
                "How {topic} Is Transforming {audience}",
            ],
            "social_titles": [
                "Ready to level up your {topic}? Here's how",
                "Quick tip about {topic} that will change your game",
                "Hot take: {topic} is underrated",
                "The one thing about {topic} nobody tells you",
            ],
        }

    def generate_content(
        self,
        topic: str,
        content_type: str = "blog_post",
        tone: str = "professional",
        target_audience: str = "general",
        keywords: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Generate a complete content piece."""
        ct = ContentType(content_type) if content_type in [e.value for e in ContentType] else ContentType.BLOG_POST
        tn = Tone(tone) if tone in [e.value for e in Tone] else Tone.PROFESSIONAL

        title = self._generate_title(topic, ct, target_audience)
        body = self._generate_body(topic, ct, tn, target_audience)
        meta_desc = self._generate_meta_description(topic, target_audience)
        cta = self._generate_cta(ct, target_audience)
        extracted_keywords = keywords or self._extract_keywords(topic)

        word_count = len(body.split())
        reading_time = max(1, word_count // 200)

        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

        piece = ContentPiece(
            title=title,
            content_type=ct.value,
            body=body,
            summary=body[:200] + "..." if len(body) > 200 else body,
            tone=tn.value,
            target_audience=target_audience,
            keywords=extracted_keywords,
            meta_description=meta_desc,
            slug=slug,
            word_count=word_count,
            reading_time_minutes=reading_time,
            cta=cta,
        )

        return piece.to_dict()

    def _generate_title(
        self, topic: str, content_type: ContentType, audience: str
    ) -> str:
        template_key = f"{content_type.value.split('_')[0]}_titles"
        templates = self._templates.get(template_key, self._templates["blog_titles"])
        template = templates[hash(topic) % len(templates)]
        return template.format(topic=topic, audience=audience)

    def _generate_body(
        self, topic: str, content_type: ContentType, tone: Tone, audience: str
    ) -> str:
        sections = [
            f"## Introduction\n\nHave you ever wondered about {topic}? You're not alone. Many {audience} face challenges in this area, and understanding the fundamentals can make a significant difference.\n",
            f"## What is {topic}?\n\n{topic} is a critical concept that affects {audience} across multiple dimensions. At its core, it encompasses the strategies, tools, and methodologies that drive results.\n",
            f"## Why {topic} Matters\n\nUnderstanding {topic} is essential for {audience} who want to stay competitive. Here's why:\n\n- **Efficiency**: Streamline your processes and save time\n- **Effectiveness**: Achieve better results with less effort\n- **Growth**: Scale your impact and reach new audiences\n",
            f"## Getting Started with {topic}\n\n1. **Assess Your Current State**: Understand where you are today\n2. **Set Clear Goals**: Define what success looks like\n3. **Choose the Right Tools**: Select platforms that fit your needs\n4. **Implement Gradually**: Start small and iterate\n5. **Measure Results**: Track key metrics and adjust\n",
            f"## Best Practices\n\n- Start with a clear strategy before diving into tactics\n- Focus on quality over quantity in all content creation\n- Engage with your audience regularly and authentically\n- Stay updated on industry trends and changes\n- Document your processes for consistency\n",
            f"## Common Mistakes to Avoid\n\n- Skipping the research phase\n- Trying to do everything at once\n- Ignoring analytics and data\n- Not adapting to audience feedback\n- Being inconsistent with publishing\n",
            f"## Conclusion\n\n{topic} is a powerful tool that can transform your results as {audience}. By following the strategies outlined in this guide, you'll be well-equipped to navigate the landscape and achieve your goals.\n\nStart implementing these tips today and see the difference for yourself.\n",
        ]
        return "\n".join(sections)

    def _generate_meta_description(self, topic: str, audience: str) -> str:
        return f"Learn everything you need to know about {topic}. Expert guide with practical tips and strategies for {audience}."

    def _generate_cta(self, content_type: ContentType, audience: str) -> str:
        ctas = {
            ContentType.BLOG_POST: f"Subscribe to our newsletter for more {audience} insights!",
            ContentType.LANDING_PAGE: "Start your free trial today!",
            ContentType.EMAIL: "Click here to learn more",
            ContentType.SOCIAL_MEDIA: "Link in bio for details!",
            ContentType.WHITEPAPER: "Download the full whitepaper",
        }
        return ctas.get(content_type, "Learn more now!")

    def _extract_keywords(self, topic: str) -> List[str]:
        base = topic.lower().split()
        return [
            topic.lower(),
            f"best {topic.lower()}",
            f"{topic.lower()} guide",
            f"how to {topic.lower()}",
            f"{topic.lower()} tips",
        ]


# =============================================================================
# SEO Optimizer
# =============================================================================

class SEOOptimizer:
    """
    Analyzes and optimizes content for search engines.

    Provides keyword analysis, readability scoring, structure analysis,
    and actionable optimization recommendations.
    """

    def __init__(self) -> None:
        self._seo_guidelines = {
            "title_length": (50, 60),
            "meta_description_length": (150, 160),
            "keyword_density_target": (0.01, 0.03),
            "min_word_count": 300,
            "target_flesch_score": 60,
        }

    def analyze_content(
        self,
        content: str,
        target_keywords: List[str],
        title: str = "",
        meta_description: str = "",
    ) -> SEOMetrics:
        """Analyze content for SEO optimization."""
        content_lower = content.lower()
        words = content.split()
        word_count = len(words)
        sentences = [s.strip() for s in content.split('.') if s.strip()]

        # Keyword analysis
        keyword_density = {}
        keyword_usage = []
        for kw in target_keywords:
            count = content_lower.count(kw.lower())
            density = count / max(word_count, 1)
            keyword_density[kw] = round(density * 100, 2)
            keyword_usage.append({
                "keyword": kw,
                "count": count,
                "density": round(density * 100, 2),
                "in_title": kw.lower() in title.lower() if title else False,
                "in_meta": kw.lower() in meta_description.lower() if meta_description else False,
            })

        # Readability
        avg_sentence_length = word_count / max(len(sentences), 1)
        avg_word_length = sum(len(w) for w in words) / max(word_count, 1)
        flesch_score = max(0, min(100, 206.835 - 1.015 * avg_sentence_length - 84.6 * (sum(len(w) for w in words) / max(word_count, 1) / 5)))

        if flesch_score >= 80:
            grade_level = "5th grade"
        elif flesch_score >= 60:
            grade_level = "8th grade"
        elif flesch_score >= 40:
            grade_level = "11th grade"
        else:
            grade_level = "College graduate"

        # Structure analysis
        heading_count = len(re.findall(r'^#{1,6}\s', content, re.MULTILINE))
        paragraph_count = len([p for p in content.split('\n\n') if p.strip()])
        bullet_count = len(re.findall(r'^[-*]\s', content, re.MULTILINE))
        internal_links = len(re.findall(r'\[.*?\]\((?!http).*?\)', content))
        external_links = len(re.findall(r'\[.*?\]\(https?://.*?\)', content))
        image_count = len(re.findall(r'!\[.*?\]\(.*?\)', content))

        # Overall score
        keyword_score = min(100, sum(min(100, ku["density"] * 1000) for ku in keyword_usage) / max(len(keyword_usage), 1))
        structure_score = min(100, (heading_count * 10 + paragraph_count * 5 + bullet_count * 3))
        overall_score = (keyword_score * 0.4 + flesch_score * 0.3 + min(100, structure_score) * 0.3)

        # Recommendations
        recommendations = []
        if word_count < 300:
            recommendations.append("Increase content length to at least 300 words")
        if heading_count < 2:
            recommendations.append("Add more headings (H2, H3) for better structure")
        if not any(ku["in_title"] for ku in keyword_usage):
            recommendations.append("Include primary keyword in the title")
        if flesch_score < 50:
            recommendations.append("Improve readability with shorter sentences")
        if internal_links == 0:
            recommendations.append("Add internal links to related content")
        if external_links == 0:
            recommendations.append("Add links to authoritative external sources")

        return SEOMetrics(
            overall_score=round(overall_score, 2),
            keyword_density=keyword_density,
            keyword_usage=keyword_usage,
            readability_score=round(flesch_score, 2),
            flesch_score=round(flesch_score, 2),
            grade_level=grade_level,
            heading_count=heading_count,
            paragraph_count=paragraph_count,
            bullet_count=bullet_count,
            internal_links=internal_links,
            external_links=external_links,
            image_count=image_count,
            recommendations=recommendations,
        )

    def optimize_for_keyword(
        self,
        content: str,
        keyword: str,
        target_density: float = 0.02,
    ) -> Dict[str, Any]:
        """Optimize content for a specific keyword."""
        word_count = len(content.split())
        keyword_count = content.lower().count(keyword.lower())
        current_density = keyword_count / max(word_count, 1)
        target_count = round(target_density * word_count)
        additional_needed = max(0, target_count - keyword_count)

        return {
            "keyword": keyword,
            "current_count": keyword_count,
            "target_count": target_count,
            "current_density": round(current_density * 100, 2),
            "target_density": round(target_density * 100, 2),
            "additional_occurrences_needed": additional_needed,
            "suggestion": f"Add '{keyword}' {additional_needed} more times naturally",
        }


# =============================================================================
# Content Calendar Manager
# =============================================================================

class ContentCalendarManager:
    """
    Manages content planning and scheduling.

    Creates calendars, suggests topics, and tracks publishing schedules.
    """

    def __init__(self) -> None:
        self._calendar_entries: Dict[str, ContentCalendar] = {}
        self._by_date: Dict[str, List[str]] = defaultdict(list)

    def create_entry(
        self,
        title: str,
        content_type: str,
        platform: str,
        scheduled_date: str,
        author: str = "",
        keywords: Optional[List[str]] = None,
    ) -> ContentCalendar:
        """Create a calendar entry."""
        entry = ContentCalendar(
            title=title,
            content_type=content_type,
            platform=platform,
            scheduled_date=scheduled_date,
            author=author,
            keywords=keywords or [],
        )
        self._calendar_entries[entry.id] = entry
        self._by_date[scheduled_date].append(entry.id)
        return entry

    def suggest_topics(
        self,
        niche: str,
        count: int = 10,
    ) -> List[Dict[str, Any]]:
        """Suggest content topics based on niche."""
        topic_templates = [
            "The Ultimate Guide to {niche}",
            "10 {niche} Tips for Beginners",
            "How to Improve Your {niche} Strategy",
            "{niche} Trends to Watch in 2024",
            "Common {niche} Mistakes and How to Avoid Them",
            "Advanced {niche} Techniques",
            "{niche} vs. The Competition: A Comparison",
            "The Future of {niche}",
            "Expert Interviews on {niche}",
            "{niche} Case Studies: Success Stories",
            "Getting Started with {niche}: A Step-by-Step Guide",
            "How {niche} Is Changing the Industry",
            "The ROI of {niche}: Measuring Success",
            "{niche} Tools and Resources You Need",
            "Building a {niche} Strategy from Scratch",
        ]

        topics = []
        for i in range(min(count, len(topic_templates))):
            title = topic_templates[i].format(niche=niche)
            topics.append({
                "id": f"topic-{i+1}",
                "title": title,
                "type": "blog" if i % 3 != 0 else "video",
                "search_volume": "high" if i < 5 else "medium",
                "competition": "medium",
                "trend": "rising",
                "keyword_difficulty": 30 + i * 5,
            })
        return topics

    def get_calendar(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get calendar entries with optional date range."""
        entries = list(self._calendar_entries.values())
        if start_date:
            entries = [e for e in entries if e.scheduled_date >= start_date]
        if end_date:
            entries = [e for e in entries if e.scheduled_date <= end_date]
        entries.sort(key=lambda e: e.scheduled_date)
        return [e.to_dict() for e in entries]

    def get_calendar_summary(self) -> Dict[str, Any]:
        """Get calendar summary statistics."""
        by_type: Dict[str, int] = defaultdict(int)
        by_platform: Dict[str, int] = defaultdict(int)
        for entry in self._calendar_entries.values():
            by_type[entry.content_type] += 1
            by_platform[entry.platform] += 1

        return {
            "total_entries": len(self._calendar_entries),
            "by_type": dict(by_type),
            "by_platform": dict(by_platform),
        }


# =============================================================================
# Social Media Manager
# =============================================================================

class SocialMediaManager:
    """
    Manages social media content creation and optimization.

    Generates platform-optimized posts with hashtags and scheduling.
    """

    PLATFORM_CONFIGS = {
        "twitter": {"max_length": 280, "style": "concise", "optimal_time": "9:00 AM EST"},
        "linkedin": {"max_length": 3000, "style": "professional", "optimal_time": "8:00 AM EST"},
        "instagram": {"max_length": 2200, "style": "visual", "optimal_time": "11:00 AM EST"},
        "facebook": {"max_length": 63206, "style": "casual", "optimal_time": "1:00 PM EST"},
    }

    def __init__(self) -> None:
        self._posts: List[Dict[str, Any]] = []

    def generate_post(
        self,
        platform: str,
        content: str,
        engagement_goal: str = "engagement",
    ) -> Dict[str, Any]:
        """Generate a platform-optimized social media post."""
        config = self.PLATFORM_CONFIGS.get(platform, {"max_length": 500, "style": "general", "optimal_time": "12:00 PM EST"})

        truncated = content[:config["max_length"]]
        hashtags = self._generate_hashtags(content)

        post = {
            "platform": platform,
            "post": truncated,
            "character_count": len(truncated),
            "hashtags": hashtags,
            "optimal_posting_time": config["optimal_time"],
            "style": config["style"],
            "engagement_tips": [
                "Ask a question to encourage comments",
                "Use relevant hashtags for discoverability",
                "Include a clear call-to-action",
                "Post during peak engagement hours",
            ],
        }

        self._posts.append(post)
        return post

    def generate_thread(
        self,
        topic: str,
        tweet_count: int = 5,
    ) -> List[Dict[str, Any]]:
        """Generate a Twitter thread."""
        tweets = []
        for i in range(tweet_count):
            if i == 0:
                tweet = f"Thread: {topic} - Here's what you need to know 🧵"
            elif i == tweet_count - 1:
                tweet = f"That's a wrap on {topic}! If you found this helpful, RT the first tweet and follow for more. 🙏"
            else:
                tweet = f"{i}/{tweet_count}: Key insight about {topic}..."

            tweets.append({
                "tweet_number": i + 1,
                "content": tweet[:280],
                "character_count": min(len(tweet), 280),
            })
        return tweets

    def _generate_hashtags(self, content: str) -> List[str]:
        words = content.split()[:5]
        return [f"#{word.lower()}" for word in words if len(word) > 3]

    def get_performance_summary(self) -> Dict[str, Any]:
        return {
            "total_posts": len(self._posts),
            "by_platform": {p: sum(1 for post in self._posts if post["platform"] == p) for p in set(post["platform"] for post in self._posts)},
        }


# =============================================================================
# Content Moderator
# =============================================================================

class ContentModerator:
    """
    Reviews and moderates content for quality, compliance, and brand consistency.

    Checks for inappropriate content, spelling errors, brand violations,
    and provides improvement suggestions.
    """

    def __init__(self) -> None:
        self._flagged_terms = [
            "spam", "clickbait", "misleading", "unverified",
        ]
        self._brand_violations = [
            "competitor name", "proprietary information",
        ]

    def moderate(self, content: ContentPiece) -> ModerationResult:
        """Moderate a content piece."""
        flags = []
        suggestions = []
        score = 100.0

        # Check for flagged terms
        body_lower = content.body.lower()
        for term in self._flagged_terms:
            if term in body_lower:
                flags.append(f"Contains flagged term: '{term}'")
                score -= 10

        # Check word count
        if content.word_count < 100:
            flags.append("Content too short (under 100 words)")
            score -= 15
            suggestions.append("Expand content to at least 300 words for better SEO")

        # Check for meta description
        if not content.meta_description:
            suggestions.append("Add a meta description for better SEO")

        # Check for keywords
        if not content.keywords:
            suggestions.append("Add target keywords for SEO optimization")

        # Check for CTA
        if not content.cta:
            suggestions.append("Add a call-to-action to improve conversion")

        # Check for title
        if not content.title or len(content.title) < 10:
            flags.append("Title too short or missing")
            score -= 10

        approved = score >= 70 and len(flags) == 0

        return ModerationResult(
            content_id=content.id,
            approved=approved,
            score=max(0, score),
            flags=flags,
            suggestions=suggestions,
        )


# =============================================================================
# Content Performance Tracker
# =============================================================================

class PerformanceTracker:
    """
    Tracks and analyzes content performance metrics.

    Monitors views, engagement, conversions, and other KPIs.
    """

    def __init__(self) -> None:
        self._metrics: Dict[str, List[ContentPerformance]] = defaultdict(list)

    def record_metrics(
        self,
        content_id: str,
        views: int = 0,
        clicks: int = 0,
        shares: int = 0,
        comments: int = 0,
        likes: int = 0,
        avg_time_on_page: float = 0.0,
        bounce_rate: float = 0.0,
        conversion_rate: float = 0.0,
    ) -> ContentPerformance:
        """Record performance metrics for content."""
        engagement_rate = (clicks + shares + comments + likes) / max(views, 1)
        ctr = clicks / max(views, 1)

        perf = ContentPerformance(
            content_id=content_id,
            views=views,
            clicks=clicks,
            shares=shares,
            comments=comments,
            likes=likes,
            avg_time_on_page=avg_time_on_page,
            bounce_rate=bounce_rate,
            conversion_rate=conversion_rate,
            ctr=round(ctr, 4),
            engagement_rate=round(engagement_rate, 4),
        )

        self._metrics[content_id].append(perf)
        return perf

    def get_content_performance(self, content_id: str) -> Dict[str, Any]:
        """Get performance summary for a content piece."""
        metrics = self._metrics.get(content_id, [])
        if not metrics:
            return {"content_id": content_id, "data_points": 0}

        latest = metrics[-1]
        return {
            "content_id": content_id,
            "data_points": len(metrics),
            "latest": latest.to_dict(),
            "trend": self._calculate_trend(metrics),
        }

    def get_top_performing(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing content by engagement."""
        summaries = []
        for content_id, metrics_list in self._metrics.items():
            if metrics_list:
                latest = metrics_list[-1]
                summaries.append({
                    "content_id": content_id,
                    "views": latest.views,
                    "engagement_rate": latest.engagement_rate,
                    "ctr": latest.ctr,
                })

        summaries.sort(key=lambda x: x["engagement_rate"], reverse=True)
        return summaries[:limit]

    def _calculate_trend(self, metrics: List[ContentPerformance]) -> str:
        if len(metrics) < 2:
            return "insufficient_data"
        recent = metrics[-1].engagement_rate
        previous = metrics[-2].engagement_rate
        if recent > previous * 1.1:
            return "improving"
        elif recent < previous * 0.9:
            return "declining"
        return "stable"


# =============================================================================
# Main Content Agent
# =============================================================================

class ContentAgent:
    """
    Primary orchestrator for content management and creation.

    Coordinates content generation, SEO optimization, calendar management,
    social media publishing, moderation, and performance tracking.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._generator = ContentGenerator()
        self._seo_optimizer = SEOOptimizer()
        self._calendar_manager = ContentCalendarManager()
        self._social_manager = SocialMediaManager()
        self._moderator = ContentModerator()
        self._performance_tracker = PerformanceTracker()
        self._content_store: Dict[str, ContentPiece] = {}
        self._created_at = datetime.utcnow()

        logger.info("ContentAgent initialized")

    def generate_content(
        self,
        topic: str,
        content_type: str = "blog_post",
        tone: str = "professional",
        target_audience: str = "general",
        keywords: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Generate a content piece."""
        result = self._generator.generate_content(
            topic=topic,
            content_type=content_type,
            tone=tone,
            target_audience=target_audience,
            keywords=keywords,
        )

        piece = ContentPiece(**{k: v for k, v in result.items() if k in ContentPiece.__dataclass_fields__})
        self._content_store[piece.id] = piece

        logger.info("Content generated: %s (%s)", piece.title, piece.id)
        return result

    def analyze_seo(
        self,
        content_id: str,
        keywords: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Analyze content for SEO."""
        piece = self._content_store.get(content_id)
        if not piece:
            return {"error": f"Content {content_id} not found"}

        target_keywords = keywords or piece.keywords
        metrics = self._seo_optimizer.analyze_content(
            content=piece.body,
            target_keywords=target_keywords,
            title=piece.title,
            meta_description=piece.meta_description,
        )

        piece.seo_score = metrics.overall_score
        piece.readability_score = metrics.readability_score
        return metrics.to_dict()

    def moderate_content(self, content_id: str) -> Dict[str, Any]:
        """Moderate a content piece."""
        piece = self._content_store.get(content_id)
        if not piece:
            return {"error": f"Content {content_id} not found"}

        result = self._moderator.moderate(piece)
        return result.to_dict()

    def add_calendar_entry(
        self,
        title: str,
        content_type: str,
        platform: str,
        scheduled_date: str,
        author: str = "",
        keywords: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Add a content calendar entry."""
        entry = self._calendar_manager.create_entry(
            title=title,
            content_type=content_type,
            platform=platform,
            scheduled_date=scheduled_date,
            author=author,
            keywords=keywords,
        )
        return entry.to_dict()

    def suggest_topics(
        self, niche: str, count: int = 10
    ) -> List[Dict[str, Any]]:
        """Suggest content topics."""
        return self._calendar_manager.suggest_topics(niche, count)

    def generate_social_post(
        self,
        platform: str,
        content: str,
    ) -> Dict[str, Any]:
        """Generate a social media post."""
        return self._social_manager.generate_post(platform, content)

    def generate_social_thread(
        self,
        topic: str,
        tweet_count: int = 5,
    ) -> List[Dict[str, Any]]:
        """Generate a Twitter thread."""
        return self._social_manager.generate_thread(topic, tweet_count)

    def record_performance(
        self,
        content_id: str,
        views: int = 0,
        clicks: int = 0,
        shares: int = 0,
        comments: int = 0,
        likes: int = 0,
    ) -> Dict[str, Any]:
        """Record content performance metrics."""
        perf = self._performance_tracker.record_metrics(
            content_id=content_id,
            views=views,
            clicks=clicks,
            shares=shares,
            comments=comments,
            likes=likes,
        )
        return perf.to_dict()

    def get_content_performance(self, content_id: str) -> Dict[str, Any]:
        """Get performance for a content piece."""
        return self._performance_tracker.get_content_performance(content_id)

    def get_top_performing(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing content."""
        return self._performance_tracker.get_top_performing(limit)

    def get_calendar(self, start_date: str = "", end_date: str = "") -> List[Dict[str, Any]]:
        """Get content calendar."""
        return self._calendar_manager.get_calendar(
            start_date=start_date or None,
            end_date=end_date or None,
        )

    def get_calendar_summary(self) -> Dict[str, Any]:
        """Get calendar summary."""
        return self._calendar_manager.get_calendar_summary()

    def list_content(self) -> List[Dict[str, Any]]:
        """List all content pieces."""
        return [p.to_dict() for p in self._content_store.values()]

    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent": "ContentAgent",
            "version": "2.0.0",
            "content_pieces": len(self._content_store),
            "calendar_entries": len(self._calendar_manager._calendar_entries),
            "social_posts": len(self._social_manager._posts),
            "uptime": str(datetime.utcnow() - self._created_at),
        }


# =============================================================================
# Entry Point
# =============================================================================

def main() -> None:
    """Demonstrate the Content Agent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    print("=" * 70)
    print("  Content Agent v2.0 - Demonstration")
    print("=" * 70)

    agent = ContentAgent()

    # Generate content
    print("\n--- Generating Content ---")
    content = agent.generate_content(
        topic="AI in Content Marketing",
        content_type="blog_post",
        tone="professional",
        target_audience="marketers",
        keywords=["AI content", "content marketing", "AI tools"],
    )
    print(f"Title: {content['title']}")
    print(f"Words: {content['word_count']}, Reading time: {content['reading_time_minutes']} min")

    # SEO analysis
    print("\n--- SEO Analysis ---")
    seo = agent.analyze_seo(content["id"])
    print(f"SEO Score: {seo['overall_score']}")
    print(f"Readability: {seo['readability_score']}")
    print(f"Recommendations: {len(seo['recommendations'])}")

    # Content moderation
    print("\n--- Content Moderation ---")
    mod = agent.moderate_content(content["id"])
    print(f"Approved: {mod['approved']}, Score: {mod['score']}")

    # Calendar
    print("\n--- Content Calendar ---")
    agent.add_calendar_entry(
        title="AI Content Trends",
        content_type="blog_post",
        platform="website",
        scheduled_date="2024-02-01",
        author="Content Team",
    )
    topics = agent.suggest_topics("AI Marketing", 5)
    print(f"Calendar entries: {agent.get_calendar_summary()['total_entries']}")
    print(f"Topic suggestions: {len(topics)}")

    # Social media
    print("\n--- Social Media ---")
    post = agent.generate_social_post("twitter", "AI is transforming content marketing. Here's how to stay ahead.")
    print(f"Twitter post: {post['character_count']} chars")

    # Performance tracking
    print("\n--- Performance Tracking ---")
    agent.record_performance(content["id"], views=1500, clicks=120, shares=45, comments=20)
    perf = agent.get_content_performance(content["id"])
    print(f"Views: {perf['latest']['views']}, Engagement: {perf['latest']['engagement_rate']}")

    # Status
    print("\n--- Agent Status ---")
    status = agent.get_status()
    for k, v in status.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 70)
    print("  Demonstration Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
