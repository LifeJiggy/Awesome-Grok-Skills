"""
Content Agent
Content creation and management automation
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import re
import hashlib


class ContentType(Enum):
    BLOG_POST = "blog"
    SOCIAL_MEDIA = "social"
    EMAIL = "email"
    DOCUMENTATION = "docs"
    VIDEO = "video"
    PODCAST = "podcast"
    LANDING_PAGE = "landing_page"
    NEWSLETTER = "newsletter"
    CASE_STUDY = "case_study"
    WHITEPAPER = "whitepaper"


class ContentStatus(Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Platform(Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    WEBSITE = "website"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    MEDIUM = "medium"
    SUBSTACK = "substack"


class ContentGenerator:
    """AI-powered content generation with brand voice support"""

    def __init__(self):
        self.templates = {}
        self.brand_voice = {}
        self.content_history = []

    def set_brand_voice(self, tone: str, personality: List[str],
                        keywords: List[str] = None):
        """Set brand voice parameters

        Args:
            tone: Primary tone (professional, casual, playful, etc.)
            personality: List of personality traits
            keywords: Optional brand keywords to include
        """
        self.brand_voice = {
            "tone": tone,
            "personality": personality,
            "keywords": keywords or []
        }

    def generate_content(self, content_type: ContentType, topic: str,
                         length: str = "medium",
                         style: str = "professional",
                         target_audience: str = "general",
                         keywords: List[str] = None) -> Dict:
        """Generate content based on parameters

        Args:
            content_type: Type of content to generate
            topic: Main topic or subject
            length: short, medium, or long
            style: Writing style
            target_audience: Target audience description
            keywords: SEO keywords to include

        Returns:
            Dict with generated content and metadata
        """
        word_counts = {"short": 300, "medium": 800, "long": 1500}
        target_words = word_counts.get(length, 800)

        content = self._generate_text(topic, target_words, style)

        result = {
            "type": content_type.value,
            "topic": topic,
            "title": self._generate_title(topic),
            "content": content,
            "word_count": len(content.split()),
            "reading_time_minutes": max(1, len(content.split()) // 200),
            "style": style,
            "target_audience": target_audience,
            "keywords": keywords or [],
            "meta_description": self._generate_meta(topic),
            "cta": self._generate_cta(topic),
            "created_at": datetime.now(),
            "content_id": self._generate_id(topic),
        }

        self.content_history.append(result)
        return result

    def _generate_title(self, topic: str) -> str:
        """Generate optimized title for topic"""
        templates = [
            f"The Ultimate Guide to {topic}",
            f"Why {topic} Matters in 2024",
            f"10 Things You Need to Know About {topic}",
            f"Mastering {topic}: A Complete Guide",
            f"How {topic} is Transforming the Industry",
            f"{topic}: A Comprehensive Overview",
        ]
        return templates[0]

    def _generate_text(self, topic: str, target_words: int,
                       style: str) -> str:
        """Generate body text (placeholder for AI integration)"""
        base = f"This is a comprehensive article about {topic}. "
        paragraphs_needed = max(3, target_words // 100)
        return (base + " ") * paragraphs_needed

    def _generate_meta(self, topic: str) -> str:
        """Generate meta description"""
        return f"Learn about {topic} with our comprehensive guide. Key insights, best practices, and actionable strategies."

    def _generate_cta(self, topic: str) -> str:
        """Generate call to action"""
        return f"Ready to learn more about {topic}? Contact us today."

    def _generate_id(self, topic: str) -> str:
        """Generate unique content ID"""
        raw = f"{topic}_{datetime.now().isoformat()}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    def generate_social_posts(self, content: str,
                              platforms: List[str]) -> Dict:
        """Generate platform-specific social posts

        Args:
            content: Source content to adapt
            platforms: List of platform names

        Returns:
            Dict mapping platform to post data
        """
        posts = {}

        max_lengths = {
            "twitter": 280,
            "linkedin": 3000,
            "instagram": 2200,
            "facebook": 63206,
            "tiktok": 2200,
            "medium": 100000,
        }

        for platform in platforms:
            limit = max_lengths.get(platform, 280)

            if len(content) > limit:
                truncated = content[:limit - 3] + "..."
            else:
                truncated = content

            posts[platform] = {
                "content": truncated,
                "hashtags": self._extract_hashtags(content),
                "length": len(truncated),
                "within_limit": len(content) <= limit,
            }

        return posts

    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from content"""
        return re.findall(r"#(\w+)", content)


class CMSManager:
    """Content management system operations"""

    def __init__(self):
        self.content = {}
        self.taxonomy = {}
        self.media_library = []

    def create_content(self, content_type: ContentType, title: str,
                       body: str, metadata: Dict = None) -> str:
        """Create new content item

        Args:
            content_type: Type of content
            title: Content title
            body: Content body text
            metadata: Optional metadata dict

        Returns:
            Content ID
        """
        content_id = f"content_{len(self.content) + 1}"

        self.content[content_id] = {
            "id": content_id,
            "type": content_type.value,
            "title": title,
            "body": body,
            "status": ContentStatus.DRAFT.value,
            "metadata": metadata or {},
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "version": 1,
        }

        return content_id

    def update_content(self, content_id: str, updates: Dict) -> bool:
        """Update content

        Args:
            content_id: Content to update
            updates: Fields to update

        Returns:
            True if updated successfully
        """
        if content_id not in self.content:
            return False

        self.content[content_id].update(updates)
        self.content[content_id]["updated_at"] = datetime.now()
        self.content[content_id]["version"] += 1
        return True

    def publish_content(self, content_id: str) -> bool:
        """Publish content

        Args:
            content_id: Content to publish

        Returns:
            True if published successfully
        """
        if content_id not in self.content:
            return False

        self.content[content_id]["status"] = ContentStatus.PUBLISHED.value
        self.content[content_id]["published_at"] = datetime.now()
        return True

    def archive_content(self, content_id: str) -> bool:
        """Archive content"""
        if content_id not in self.content:
            return False

        self.content[content_id]["status"] = ContentStatus.ARCHIVED.value
        return True

    def add_taxonomy_term(self, taxonomy: str, term: str,
                          parent: str = None):
        """Add taxonomy term"""
        if taxonomy not in self.taxonomy:
            self.taxonomy[taxonomy] = {}

        self.taxonomy[taxonomy][term] = {
            "parent": parent,
            "children": []
        }

    def get_content_by_taxonomy(self, taxonomy: str,
                                term: str) -> List[Dict]:
        """Get content by taxonomy"""
        return [c for c in self.content.values()
                if c.get("metadata", {}).get(taxonomy) == term]

    def get_content_stats(self) -> Dict:
        """Get content statistics"""
        by_status = {}
        by_type = {}
        total_words = 0

        for c in self.content.values():
            status = c["status"]
            by_status[status] = by_status.get(status, 0) + 1

            ctype = c["type"]
            by_type[ctype] = by_type.get(ctype, 0) + 1

            total_words += len(c.get("body", "").split())

        return {
            "total_content": len(self.content),
            "by_status": by_status,
            "by_type": by_type,
            "total_words": total_words,
            "avg_words_per_piece": total_words // max(1, len(self.content)),
        }


class MediaManager:
    """Media assets management"""

    def __init__(self):
        self.media = {}

    def upload_media(self, filename: str, mime_type: str, size: int,
                     url: str = None) -> str:
        """Upload media asset

        Args:
            filename: Original filename
            mime_type: MIME type
            size: File size in bytes
            url: Optional URL if hosted

        Returns:
            Media ID
        """
        media_id = f"media_{len(self.media) + 1}"

        self.media[media_id] = {
            "id": media_id,
            "filename": filename,
            "mime_type": mime_type,
            "size": size,
            "size_mb": round(size / (1024 * 1024), 2),
            "url": url or f"/media/{media_id}",
            "uploaded_at": datetime.now(),
        }

        return media_id

    def optimize_image(self, media_id: str, width: int = None,
                       height: int = None) -> Dict:
        """Generate optimized image variants

        Args:
            media_id: Media to optimize
            width: Custom width
            height: Custom height

        Returns:
            Dict with variant URLs and specs
        """
        if media_id not in self.media:
            return {"error": "Media not found"}

        original = self.media[media_id]
        variants = {}

        sizes = {
            "thumbnail": (150, 150),
            "medium": (800, 600),
            "large": (1920, 1080),
            "web": (1200, 630),
            "social": (1080, 1080),
        }

        for size_name, dims in sizes.items():
            w, h = dims
            variants[size_name] = {
                "width": width or w,
                "height": height or h,
                "url": f"{original['url']}/{size_name}",
                "format": self._get_optimal_format(original["mime_type"]),
            }

        return variants

    def _get_optimal_format(self, mime_type: str) -> str:
        """Determine optimal format based on MIME type"""
        format_map = {
            "image/jpeg": "webp",
            "image/png": "webp",
            "image/gif": "webp",
            "image/svg+xml": "svg",
        }
        return format_map.get(mime_type, "webp")

    def get_media_stats(self) -> Dict:
        """Get media library statistics"""
        by_type = {}
        total_size = 0

        for m in self.media.values():
            mtype = m["mime_type"].split("/")[0]
            by_type[mtype] = by_type.get(mtype, 0) + 1
            total_size += m["size"]

        return {
            "total_items": len(self.media),
            "by_type": by_type,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "avg_size_mb": round(total_size / max(1, len(self.media)) / (1024 * 1024), 2),
        }


class SEOAnalyzer:
    """SEO content analysis"""

    def __init__(self):
        self.keywords = {}
        self.analysis_history = []

    def analyze_content(self, title: str, content: str,
                        target_keyword: str) -> Dict:
        """Analyze content for SEO

        Args:
            title: Content title
            content: Content body
            target_keyword: Primary keyword to optimize for

        Returns:
            SEO analysis with score and recommendations
        """
        content_lower = content.lower()
        keyword_lower = target_keyword.lower()

        keyword_count = content_lower.count(keyword_lower)
        keyword_density = (
            (keyword_count * len(target_keyword) / len(content)) * 100
            if content else 0
        )

        readability_score = self._calculate_readability(content)

        suggestions = []
        if keyword_density < 0.5:
            suggestions.append("Increase keyword density (target 1-2%)")
        if keyword_density > 3.0:
            suggestions.append("Reduce keyword density (target 1-2%)")
        if readability_score < 60:
            suggestions.append("Improve readability with shorter sentences")
        if len(title) > 60:
            suggestions.append("Shorten title for better SERP display (< 60 chars)")
        if keyword_lower not in title.lower():
            suggestions.append("Include primary keyword in title")
        if keyword_lower not in content[:200].lower():
            suggestions.append("Include keyword in first 200 characters")
        if not re.search(r'<h[1-3]>', content):
            suggestions.append("Add headings (H1, H2, H3) for structure")

        result = {
            "keyword": target_keyword,
            "count": keyword_count,
            "density": round(keyword_density, 2),
            "readability": readability_score,
            "title_length": len(title),
            "word_count": len(content.split()),
            "suggestions": suggestions,
            "title_optimization": self._optimize_title(title, target_keyword),
            "score": self._calculate_seo_score(
                keyword_density, readability_score, title, content
            ),
        }

        self.analysis_history.append(result)
        return result

    def _calculate_readability(self, text: str) -> int:
        """Calculate Flesch reading ease (simplified)"""
        sentences = text.count(".") + text.count("!") + text.count("?")
        words = len(text.split())
        if sentences == 0 or words == 0:
            return 50
        avg_sentence_length = words / sentences
        return max(0, min(100, 206.835 - 1.015 * avg_sentence_length))

    def _optimize_title(self, title: str, keyword: str) -> Dict:
        """Analyze title optimization"""
        keyword_in_title = keyword.lower() in title.lower()
        return {
            "current": title,
            "keyword_included": keyword_in_title,
            "length": len(title),
            "recommendation": (
                "Good title" if keyword_in_title
                else "Include keyword at the beginning"
            ),
        }

    def _calculate_seo_score(self, density: float, readability: float,
                             title: str, content: str) -> int:
        """Calculate overall SEO score (0-100)"""
        score = 0

        # Keyword density score (0-30)
        if 1.0 <= density <= 2.0:
            score += 30
        elif 0.5 <= density < 1.0 or 2.0 < density <= 3.0:
            score += 20
        else:
            score += 10

        # Readability score (0-30)
        score += int(readability * 0.3)

        # Title score (0-20)
        if len(title) <= 60:
            score += 10
        if len(title) >= 30:
            score += 10

        # Content length score (0-20)
        word_count = len(content.split())
        if word_count >= 800:
            score += 20
        elif word_count >= 300:
            score += 10

        return min(100, score)


class ContentScheduler:
    """Content publishing scheduler"""

    def __init__(self):
        self.schedule = []

    def schedule_content(self, content_id: str, publish_date: datetime,
                         channels: List[str]) -> str:
        """Schedule content for publishing

        Args:
            content_id: Content to schedule
            publish_date: When to publish
            channels: Channels to publish to

        Returns:
            Schedule ID
        """
        schedule_id = f"schedule_{len(self.schedule) + 1}"

        self.schedule.append({
            "id": schedule_id,
            "content_id": content_id,
            "scheduled_at": publish_date,
            "channels": channels,
            "status": "scheduled",
        })

        return schedule_id

    def get_upcoming_content(self, days: int = 7) -> List[Dict]:
        """Get scheduled content for next N days"""
        end_date = datetime.now() + timedelta(days=days)

        return [s for s in self.schedule
                if s["scheduled_at"] <= end_date
                and s["status"] == "scheduled"]

    def cancel_schedule(self, schedule_id: str) -> bool:
        """Cancel scheduled content"""
        for s in self.schedule:
            if s["id"] == schedule_id:
                s["status"] = "cancelled"
                return True
        return False

    def get_schedule_stats(self) -> Dict:
        """Get scheduling statistics"""
        by_status = {}
        by_channel = {}

        for s in self.schedule:
            status = s["status"]
            by_status[status] = by_status.get(status, 0) + 1

            for channel in s["channels"]:
                by_channel[channel] = by_channel.get(channel, 0) + 1

        return {
            "total_scheduled": len(self.schedule),
            "by_status": by_status,
            "by_channel": by_channel,
            "upcoming_7_days": len(self.get_upcoming_content(7)),
        }


class ContentModerator:
    """Content quality and brand compliance moderation"""

    def __init__(self):
        self.flagged_terms = [
            "guarantee", "free money", "no risk", "100% guaranteed",
            "act now", "limited time", "once in a lifetime",
        ]
        self.brand_terms = {}
        self.moderation_history = []

    def moderate_content(self, content: Dict) -> Dict:
        """Moderate content for quality and compliance

        Args:
            content: Content to moderate

        Returns:
            Moderation result with score, flags, and suggestions
        """
        text = f"{content.get('title', '')} {content.get('content', '')}".lower()

        flags = []
        suggestions = []
        score = 100

        # Check for flagged terms
        for term in self.flagged_terms:
            if term in text:
                flags.append(f"Contains flagged term: '{term}'")
                score -= 10

        # Check content length
        word_count = len(text.split())
        if word_count < 300:
            suggestions.append("Content is too short for SEO (< 300 words)")
            score -= 10

        if word_count > 3000:
            suggestions.append("Consider breaking into multiple pieces")

        # Check for CTA
        cta_indicators = ["click", "sign up", "learn more", "get started", "contact"]
        has_cta = any(indicator in text for indicator in cta_indicators)
        if not has_cta:
            suggestions.append("Add a clear call to action")
            score -= 5

        # Brand compliance
        if self.brand_terms:
            for term, required in self.brand_terms.items():
                if required and term not in text:
                    suggestions.append(f"Missing required brand term: '{term}'")
                    score -= 5

        result = {
            "approved": score >= 70,
            "score": max(0, score),
            "flags": flags,
            "suggestions": suggestions,
            "word_count": word_count,
            "has_cta": has_cta,
        }

        self.moderation_history.append(result)
        return result

    def set_brand_terms(self, terms: Dict[str, bool]):
        """Set brand compliance terms

        Args:
            terms: Dict mapping term to required (True) or optional (False)
        """
        self.brand_terms = terms


if __name__ == "__main__":
    # Demo
    generator = ContentGenerator()
    generator.set_brand_voice("friendly", ["helpful", "expert"], ["tech", "innovation"])

    blog = generator.generate_content(
        ContentType.BLOG_POST, "Machine Learning", "long",
        target_audience="developers", keywords=["ML", "AI"]
    )
    social_posts = generator.generate_social_posts(
        blog["content"], ["twitter", "linkedin"]
    )

    cms = CMSManager()
    content_id = cms.create_content(
        ContentType.BLOG_POST, "My Blog Post", "Blog content here..."
    )
    cms.publish_content(content_id)

    media = MediaManager()
    media_id = media.upload_media("image.jpg", "image/jpeg", 1024000)
    variants = media.optimize_image(media_id)

    seo = SEOAnalyzer()
    analysis = seo.analyze_content(
        "Introduction to AI",
        "Artificial Intelligence is transforming industries...",
        "artificial intelligence"
    )

    scheduler = ContentScheduler()
    scheduler.schedule_content(
        content_id,
        datetime.now() + timedelta(days=1),
        ["twitter", "blog"]
    )

    moderator = ContentModerator()
    mod_result = moderator.moderate_content({
        "title": blog["title"],
        "content": blog["content"],
    })

    print(f"Blog generated: {blog['word_count']} words")
    print(f"Social posts: {list(social_posts.keys())}")
    print(f"Content published: {cms.content[content_id]['status']}")
    print(f"Media variants: {list(variants.keys())}")
    print(f"SEO score: {analysis['score']}")
    print(f"SEO density: {analysis['density']}%")
    print(f"Scheduled items: {len(scheduler.get_upcoming_content())}")
    print(f"Moderation approved: {mod_result['approved']}")
    print(f"Moderation score: {mod_result['score']}")
