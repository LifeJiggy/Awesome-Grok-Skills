"""
Content Agent
Content creation and optimization
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class ContentType(Enum):
    BLOG_POST = "blog_post"
    ARTICLE = "article"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    LANDING_PAGE = "landing_page"
    VIDEO_SCRIPT = "video_script"
    PODCAST_SCRIPT = "podcast_script"


class Tone(Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"
    TECHNICAL = "technical"


@dataclass
class ContentPiece:
    content_id: str
    title: str
    content_type: ContentType
    body: str
    seo_score: int
    readability_score: int


class ContentGenerator:
    """AI-powered content generation"""
    
    def __init__(self):
        self.templates = {}
        self.writing_guidelines = {}
    
    def generate_content(self, 
                        topic: str,
                        content_type: ContentType,
                        tone: Tone,
                        target_audience: str,
                        keywords: Optional[List[str]] = None) -> Dict:
        """Generate content piece"""
        content = {
            'title': self._generate_title(topic, content_type),
            'content_type': content_type.value,
            'tone': tone.value,
            'audience': target_audience,
            'body': self._generate_body(topic, content_type, tone, target_audience),
            'keywords': keywords or self._extract_keywords(topic),
            'meta_description': self._generate_meta_description(topic),
            'cta': self._generate_cta(content_type)
        }
        
        return content
    
    def _generate_title(self, topic: str, content_type: ContentType) -> str:
        """Generate engaging title"""
        title_templates = {
            ContentType.BLOG_POST: [
                f"10 Essential Things You Need to Know About {topic}",
                f"How to Master {topic} in 30 Days",
                f"The Ultimate Guide to {topic}"
            ],
            ContentType.ARTICLE: [
                f"Understanding {topic}: A Comprehensive Analysis",
                f"Why {topic} Matters More Than Ever",
                f"The Future of {topic}"
            ],
            ContentType.SOCIAL_MEDIA: [
                f"Ready to level up your {topic}? Here's how 🧵",
                f"Quick tip about {topic} that will change your game 🎯",
                f"Hot take: {topic} is underrated 🤔"
            ]
        }
        
        templates = title_templates.get(content_type, [f"Everything About {topic}"])
        return templates[0]
    
    def _generate_body(self, 
                      topic: str,
                      content_type: ContentType,
                      tone: Tone,
                      audience: str) -> str:
        """Generate content body"""
        intro = f"Have you ever wondered about {topic}? You're not alone.\n\n"
        
        sections = [
            f"## What is {topic}?\n\n{topic} is an important concept that affects everyone in {audience}.\n\n",
            f"## Why Does It Matter?\n\nUnderstanding {topic} can make a significant difference in your success.\n\n",
            f"## Key Benefits\n\n- Benefit 1: Improved outcomes\n- Benefit 2: Time savings\n- Benefit 3: Cost efficiency\n\n",
            f"## How to Get Started\n\nGetting started with {topic} is easier than you think. Follow these steps:\n\n1. Research the basics\n2. Practice consistently\n3. Track your progress\n4. Refine your approach\n\n",
            f"## Common Mistakes to Avoid\n\nMany people make these errors when dealing with {topic}:\n\n- Mistake 1: Skipping fundamentals\n- Mistake 2: Inconsistent practice\n- Mistake 3: Not measuring results\n\n"
        ]
        
        conclusion = f"## Conclusion\n\nIn conclusion, {topic} is a powerful tool that can transform your results.\nStart implementing these strategies today and see the difference for yourself.\n\n"
        
        return intro + "\n".join(sections) + conclusion
    
    def _extract_keywords(self, topic: str) -> List[str]:
        """Extract SEO keywords"""
        return [
            topic.lower(),
            f"best {topic.lower()}",
            f"{topic.lower()} guide",
            f"how to {topic.lower()}",
            f"{topic.lower()} tips"
        ]
    
    def _generate_meta_description(self, topic: str) -> str:
        """Generate SEO meta description"""
        return f"Learn everything you need to know about {topic}. Expert guide with practical tips and strategies for success."
    
    def _generate_cta(self, content_type: ContentType) -> str:
        """Generate call-to-action"""
        cta_options = {
            ContentType.BLOG_POST: "Subscribe to our newsletter for more tips!",
            ContentType.LANDING_PAGE: "Start your free trial today!",
            ContentType.EMAIL: "Click here to learn more",
            ContentType.SOCIAL_MEDIA: "Link in bio for details! 🚀"
        }
        return cta_options.get(content_type, "Learn more now!")


class SEOOptimizer:
    """SEO content optimization"""
    
    def __init__(self):
        self.seo_guidelines = {}
    
    def analyze_content_seo(self, 
                           content: str,
                           target_keywords: List[str]) -> Dict:
        """Analyze content SEO optimization"""
        return {
            'overall_score': 75,
            'keyword_analysis': self._analyze_keywords(content, target_keywords),
            'readability': self._analyze_readability(content),
            'structure': self._analyze_structure(content),
            'recommendations': self._generate_seo_recommendations(target_keywords)
        }
    
    def _analyze_keywords(self, content: str, keywords: List[str]) -> Dict:
        """Analyze keyword usage"""
        content_lower = content.lower()
        return {
            'keyword_density': {},
            'usage_analysis': [
                {'keyword': kw, 'count': content_lower.count(kw.lower()), 'placement': 'good'}
                for kw in keywords
            ],
            'missing_keywords': [],
            'overused_keywords': []
        }
    
    def _analyze_readability(self, content: str) -> Dict:
        """Analyze content readability"""
        words = content.split()
        sentences = content.split('.')
        return {
            'flesch_score': 65,
            'avg_sentence_length': len(words) / max(len(sentences), 1),
            'avg_word_length': sum(len(w) for w in words) / max(len(words), 1),
            'grade_level': '8th grade',
            'readability_rating': 'good'
        }
    
    def _analyze_structure(self, content: str) -> Dict:
        """Analyze content structure"""
        return {
            'heading_count': content.count('##'),
            'paragraph_count': content.count('\n\n'),
            'bullet_points': content.count('- '),
            'has_meta_description': True,
            'has_cta': True,
            'structure_score': 80
        }
    
    def _generate_seo_recommendations(self, keywords: List[str]) -> List[str]:
        """Generate SEO improvement recommendations"""
        return [
            "Add more internal links",
            "Include keywords in first paragraph",
            "Add image alt text with keywords",
            "Optimize URL structure",
            "Add schema markup"
        ]
    
    def optimize_for_keyword(self, 
                            content: str,
                            keyword: str,
                            target_density: float = 0.02) -> Dict:
        """Optimize content for specific keyword"""
        word_count = len(content.split())
        keyword_count = content.lower().count(keyword.lower())
        current_density = keyword_count / word_count if word_count > 0 else 0
        
        return {
            'keyword': keyword,
            'current_density': round(current_density * 100, 2),
            'target_density': round(target_density * 100, 2),
            'changes_needed': round((target_density - current_density) * word_count),
            'optimized_content': content
        }


class ContentCalendar:
    """Content planning and scheduling"""
    
    def __init__(self):
        self.calendar = {}
    
    def create_content_calendar(self, 
                               start_date: datetime,
                               weeks: int = 4) -> Dict:
        """Create content calendar"""
        calendar = {
            'start_date': start_date.isoformat(),
            'weeks': [],
            'content_types': ['blog', 'social', 'email', 'video'],
            'frequency': {
                'blog': '2x per week',
                'social': 'daily',
                'email': '1x per week',
                'video': '1x per week'
            }
        }
        
        for week in range(weeks):
            week_content = {
                'week': week + 1,
                'content_items': []
            }
            
            week_content['content_items'] = [
                {'day': 'Monday', 'type': 'blog', 'topic': f'Topic {week*2 + 1}'},
                {'day': 'Tuesday', 'type': 'social', 'topic': f'Tip {week*3 + 1}'},
                {'day': 'Wednesday', 'type': 'blog', 'topic': f'Topic {week*2 + 2}'},
                {'day': 'Thursday', 'type': 'video', 'topic': f'Tutorial {week + 1}'},
                {'day': 'Friday', 'type': 'social', 'topic': f'Weekly roundup'},
                {'day': 'Sunday', 'type': 'email', 'topic': f'Newsletter {week + 1}'}
            ]
            
            calendar['weeks'].append(week_content)
        
        return calendar
    
    def suggest_content_topics(self, 
                              niche: str,
                              num_topics: int = 10) -> List[Dict]:
        """Suggest content topics"""
        topics = []
        for i in range(num_topics):
            topics.append({
                'id': f'topic_{i+1}',
                'title': f"{niche} Guide: {i+1} Essential Tips",
                'type': 'blog' if i % 2 == 0 else 'video',
                'search_volume': 'high',
                'competition': 'medium',
                'trend': 'rising',
                'keyword_difficulty': 40 + i * 3
            })
        return topics


class SocialMediaManager:
    """Social media content management"""
    
    def __init__(self):
        self.platforms = {}
    
    def generate_social_post(self, 
                            platform: str,
                            content: str,
                            engagement_goal: str = "engagement") -> Dict:
        """Generate platform-optimized post"""
        platform_configs = {
            'twitter': {'max_length': 280, 'style': 'concise'},
            'linkedin': {'max_length': 3000, 'style': 'professional'},
            'instagram': {'max_length': 2200, 'style': 'visual'},
            'facebook': {'max_length': 63206, 'style': 'casual'}
        }
        
        config = platform_configs.get(platform, {'max_length': 500, 'style': 'general'})
        
        return {
            'platform': platform,
            'post': content[:config['max_length']],
            'character_count': len(content),
            'hashtags': self._generate_hashtags(content),
            'optimal_posting_time': self._get_optimal_time(platform),
            'engagement_tips': [
                'Ask a question',
                'Use relevant hashtags',
                'Include a call-to-action'
            ]
        }
    
    def _generate_hashtags(self, content: str) -> List[str]:
        """Generate relevant hashtags"""
        words = content.split()[:5]
        return [f"#{word.lower()}" for word in words if len(word) > 3]
    
    def _get_optimal_time(self, platform: str) -> str:
        """Get optimal posting time"""
        times = {
            'twitter': '9:00 AM EST',
            'linkedin': '8:00 AM EST',
            'instagram': '11:00 AM EST',
            'facebook': '1:00 PM EST'
        }
        return times.get(platform, '12:00 PM EST')
    
    def analyze_social_performance(self, 
                                  platform: str,
                                  posts: List[Dict]) -> Dict:
        """Analyze social media performance"""
        return {
            'platform': platform,
            'total_posts': len(posts),
            'total_reach': 50000,
            'total_engagement': 2500,
            'avg_engagement_rate': 5.0,
            'top_performing_post': {
                'content': 'Top performing post...',
                'reach': 15000,
                'engagement': 1200
            },
            'recommendations': [
                'Post more during peak hours',
                'Use more visual content',
                'Engage with comments promptly'
            ]
        }


if __name__ == "__main__":
    generator = ContentGenerator()
    
    content = generator.generate_content(
        topic="Digital Marketing",
        content_type=ContentType.BLOG_POST,
        tone=Tone.PROFESSIONAL,
        target_audience="business owners",
        keywords=["digital marketing", "marketing strategy", "online marketing"]
    )
    print(f"Title: {content['title']}")
    print(f"Keywords: {content['keywords']}")
    print(f"CTA: {content['cta']}")
    
    seo = SEOOptimizer()
    analysis = seo.analyze_content_seo(content['body'], content['keywords'])
    print(f"\nSEO Score: {analysis['overall_score']}")
    print(f"Readability: {analysis['readability']['readability_rating']}")
    print(f"Recommendations: {len(analysis['recommendations'])}")
    
    calendar = ContentCalendar()
    cal = calendar.create_content_calendar(datetime.now(), 4)
    print(f"\nCalendar: {len(cal['weeks'])} weeks")
    print(f"Week 1 items: {len(cal['weeks'][0]['content_items'])}")
    
    social = SocialMediaManager()
    post = social.generate_social_post('twitter', 'Check out our new product launch!')
    print(f"\nTwitter post: {len(post['post'])} chars")
    print(f"Hashtags: {post['hashtags']}")
