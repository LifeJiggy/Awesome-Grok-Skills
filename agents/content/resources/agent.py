"""
Content Agent
Content creation and management automation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class ContentType(Enum):
    BLOG_POST = "blog"
    SOCIAL_MEDIA = "social"
    EMAIL = "email"
    DOCUMENTATION = "docs"
    VIDEO = "video"
    PODCAST = "podcast"


class ContentGenerator:
    """AI-powered content generation"""
    
    def __init__(self):
        self.templates = {}
        self.brand_voice = {}
    
    def set_brand_voice(self, tone: str, personality: List[str], keywords: List[str] = None):
        """Set brand voice parameters"""
        self.brand_voice = {
            "tone": tone,
            "personality": personality,
            "keywords": keywords or []
        }
    
    def generate_content(self,
                        content_type: ContentType,
                        topic: str,
                        length: str = "medium",
                        style: str = "professional") -> Dict:
        """Generate content"""
        word_counts = {"short": 300, "medium": 800, "long": 1500}
        target_words = word_counts.get(length, 800)
        
        content = self._generate_text(topic, target_words, style)
        
        return {
            "type": content_type.value,
            "topic": topic,
            "title": self._generate_title(topic),
            "content": content,
            "word_count": len(content.split()),
            "style": style,
            "created_at": datetime.now()
        }
    
    def _generate_title(self, topic: str) -> str:
        """Generate title"""
        templates = [
            f"The Ultimate Guide to {topic}",
            f"Why {topic} Matters in 2024",
            f"10 Things You Need to Know About {topic}",
            f"Mastering {topic}: A Complete Guide"
        ]
        return templates[0]
    
    def _generate_text(self, topic: str, target_words: int, style: str) -> str:
        """Generate body text (placeholder)"""
        return f"This is a comprehensive article about {topic}. " * (target_words // 20)
    
    def generate_social_posts(self, content: str, platforms: List[str]) -> Dict:
        """Generate platform-specific social posts"""
        posts = {}
        
        for platform in platforms:
            max_length = {"twitter": 280, "linkedin": 3000, "instagram": 2200, "facebook": 63206}
            limit = max_length.get(platform, 280)
            
            if len(content) > limit:
                truncated = content[:limit - 3] + "..."
            else:
                truncated = content
            
            posts[platform] = {
                "content": truncated,
                "hashtags": self._extract_hashtags(content),
                "length": len(truncated)
            }
        
        return posts
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from content"""
        import re
        return re.findall(r"#(\w+)", content)


class CMSManager:
    """Content management system operations"""
    
    def __init__(self):
        self.content = {}
        self.taxonomy = {}
        self.media_library = []
    
    def create_content(self,
                      content_type: ContentType,
                      title: str,
                      body: str,
                      metadata: Dict = None) -> str:
        """Create new content item"""
        content_id = f"content_{len(self.content) + 1}"
        
        self.content[content_id] = {
            "id": content_id,
            "type": content_type.value,
            "title": title,
            "body": body,
            "status": "draft",
            "metadata": metadata or {},
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "version": 1
        }
        
        return content_id
    
    def update_content(self, content_id: str, updates: Dict) -> bool:
        """Update content"""
        if content_id not in self.content:
            return False
        
        self.content[content_id].update(updates)
        self.content[content_id]["updated_at"] = datetime.now()
        self.content[content_id]["version"] += 1
        return True
    
    def publish_content(self, content_id: str) -> bool:
        """Publish content"""
        if content_id not in self.content:
            return False
        
        self.content[content_id]["status"] = "published"
        self.content[content_id]["published_at"] = datetime.now()
        return True
    
    def add_taxonomy_term(self, taxonomy: str, term: str, parent: str = None):
        """Add taxonomy term"""
        if taxonomy not in self.taxonomy:
            self.taxonomy[taxonomy] = {}
        
        self.taxonomy[taxonomy][term] = {
            "parent": parent,
            "children": []
        }
    
    def get_content_by_taxonomy(self, taxonomy: str, term: str) -> List[Dict]:
        """Get content by taxonomy"""
        return [c for c in self.content.values() 
               if c.get("metadata", {}).get(taxonomy) == term]


class MediaManager:
    """Media assets management"""
    
    def __init__(self):
        self.media = {}
    
    def upload_media(self, filename: str, mime_type: str, size: int, url: str = None) -> str:
        """Upload media asset"""
        media_id = f"media_{len(self.media) + 1}"
        
        self.media[media_id] = {
            "id": media_id,
            "filename": filename,
            "mime_type": mime_type,
            "size": size,
            "url": url or f"/media/{media_id}",
            "uploaded_at": datetime.now()
        }
        
        return media_id
    
    def optimize_image(self, media_id: str, width: int = None, height: int = None) -> Dict:
        """Generate optimized image variants"""
        if media_id not in self.media:
            return {"error": "Media not found"}
        
        original = self.media[media_id]
        variants = {}
        
        for size_name, dims in [("thumbnail", (150, 150)), ("medium", (800, 600)), ("large", (1920, 1080))]:
            w, h = dims
            variants[size_name] = {
                "width": width or w,
                "height": height or h,
                "url": f"{original['url']}/{size_name}"
            }
        
        return variants
    
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
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }


class SEOAnalyzer:
    """SEO content analysis"""
    
    def __init__(self):
        self.keywords = {}
    
    def analyze_content(self, title: str, content: str, target_keyword: str) -> Dict:
        """Analyze content for SEO"""
        content_lower = content.lower()
        keyword_lower = target_keyword.lower()
        
        keyword_count = content_lower.count(keyword_lower)
        keyword_density = (keyword_count * len(target_keyword) / len(content)) * 100 if content else 0
        
        readability_score = self._calculate_readability(content)
        
        suggestions = []
        if keyword_density < 0.5:
            suggestions.append("Increase keyword density")
        if readability_score < 60:
            suggestions.append("Improve readability with shorter sentences")
        if len(title) > 60:
            suggestions.append("Shorten title for better SERP display")
        
        return {
            "keyword": target_keyword,
            "count": keyword_count,
            "density": round(keyword_density, 2),
            "readability": readability_score,
            "suggestions": suggestions,
            "title_optimization": self._optimize_title(title, target_keyword)
        }
    
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
        return {
            "current": title,
            "keyword_included": keyword.lower() in title.lower(),
            "length": len(title),
            "recommendation": "Include keyword at the beginning" if keyword.lower() not in title.lower() else "Good title"
        }


class ContentScheduler:
    """Content publishing scheduler"""
    
    def __init__(self):
        self.schedule = []
    
    def schedule_content(self,
                        content_id: str,
                        publish_date: datetime,
                        channels: List[str]) -> str:
        """Schedule content for publishing"""
        schedule_id = f"schedule_{len(self.schedule) + 1}"
        
        self.schedule.append({
            "id": schedule_id,
            "content_id": content_id,
            "scheduled_at": publish_date,
            "channels": channels,
            "status": "scheduled"
        })
        
        return schedule_id
    
    def get_upcoming_content(self, days: int = 7) -> List[Dict]:
        """Get scheduled content"""
        from datetime import timedelta
        end_date = datetime.now() + timedelta(days=days)
        
        return [s for s in self.schedule 
               if s["scheduled_at"] <= end_date and s["status"] == "scheduled"]
    
    def cancel_schedule(self, schedule_id: str) -> bool:
        """Cancel scheduled content"""
        for s in self.schedule:
            if s["id"] == schedule_id:
                s["status"] = "cancelled"
                return True
        return False


if __name__ == "__main__":
    generator = ContentGenerator()
    generator.set_brand_voice("friendly", ["helpful", "expert"], ["tech", "innovation"])
    
    blog = generator.generate_content(ContentType.BLOG_POST, "Machine Learning", "long")
    social_posts = generator.generate_social_posts(blog["content"], ["twitter", "linkedin"])
    
    cms = CMSManager()
    content_id = cms.create_content(ContentType.BLOG_POST, "My Blog Post", "Blog content here...")
    cms.publish_content(content_id)
    
    media = MediaManager()
    media_id = media.upload_media("image.jpg", "image/jpeg", 1024000)
    variants = media.optimize_image(media_id)
    
    seo = SEOAnalyzer()
    analysis = seo.analyze_content("Introduction to AI", "Artificial Intelligence is...", "artificial intelligence")
    
    scheduler = ContentScheduler()
    scheduler.schedule_content(content_id, datetime.now() + timedelta(days=1), ["twitter", "blog"])
    
    print(f"Blog generated: {blog['word_count']} words")
    print(f"Social posts: {list(social_posts.keys())}")
    print(f"Content published: {cms.content[content_id]['status']}")
    print(f"Media variants: {list(variants.keys())}")
    print(f"SEO density: {analysis['density']}%")
    print(f"Scheduled items: {len(scheduler.get_upcoming_content())}")
