"""
Marketing Agent
Marketing automation and campaign management
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class CampaignStatus(Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class AudienceSegment:
    """Customer audience segmentation"""
    
    def __init__(self):
        self.segments = {}
        self.criteria = {}
    
    def create_segment(self, 
                      name: str,
                      criteria: Dict) -> str:
        """Create audience segment"""
        segment_id = f"seg_{len(self.segments)}"
        self.segments[segment_id] = {
            "name": name,
            "criteria": criteria,
            "size": 0
        }
        return segment_id
    
    def estimate_size(self, segment_id: str, total_customers: int) -> int:
        """Estimate segment size"""
        criteria = self.segments.get(segment_id, {}).get("criteria", {})
        
        if not criteria:
            return total_customers
        
        multiplier = 1.0
        for field, value in criteria.items():
            if "age" in field:
                multiplier *= 0.3
            elif "location" in field:
                multiplier *= 0.5
            elif "behavior" in field:
                multiplier *= 0.2
        
        size = int(total_customers * min(multiplier, 1.0))
        self.segments[segment_id]["size"] = size
        return size
    
    def get_segments(self) -> List[Dict]:
        """Get all segments"""
        return [
            {"id": k, "name": v["name"], "size": v["size"]}
            for k, v in self.segments.items()
        ]


class CampaignManager:
    """Marketing campaign management"""
    
    def __init__(self):
        self.campaigns = {}
        self.templates = {}
    
    def create_campaign(self,
                       name: str,
                       channel: str,
                       audience: List[str],
                       content: Dict,
                       schedule: Dict = None) -> str:
        """Create marketing campaign"""
        campaign_id = f"camp_{int(datetime.now().timestamp())}"
        
        self.campaigns[campaign_id] = {
            "name": name,
            "channel": channel,
            "audience": audience,
            "content": content,
            "schedule": schedule or {"start": datetime.now()},
            "status": CampaignStatus.DRAFT,
            "metrics": {
                "sent": 0,
                "opened": 0,
                "clicked": 0,
                "converted": 0
            }
        }
        
        return campaign_id
    
    def launch_campaign(self, campaign_id: str) -> bool:
        """Launch campaign"""
        if campaign_id not in self.campaigns:
            return False
        
        self.campaigns[campaign_id]["status"] = CampaignStatus.ACTIVE
        self.campaigns[campaign_id]["launched_at"] = datetime.now()
        return True
    
    def update_metrics(self, 
                      campaign_id: str,
                      metrics: Dict) -> bool:
        """Update campaign metrics"""
        if campaign_id not in self.campaigns:
            return False
        
        for key, value in metrics.items():
            if key in self.campaigns[campaign_id]["metrics"]:
                self.campaigns[campaign_id]["metrics"][key] += value
        
        return True
    
    def get_campaign_analytics(self, campaign_id: str) -> Dict:
        """Get campaign analytics"""
        if campaign_id not in self.campaigns:
            return {}
        
        metrics = self.campaigns[campaign_id]["metrics"]
        sent = metrics.get("sent", 1)
        
        return {
            "sent": sent,
            "opened": metrics.get("opened", 0),
            "clicked": metrics.get("clicked", 0),
            "converted": metrics.get("converted", 0),
            "open_rate": (metrics.get("opened", 0) / sent * 100) if sent > 0 else 0,
            "click_rate": (metrics.get("clicked", 0) / sent * 100) if sent > 0 else 0,
            "conversion_rate": (metrics.get("converted", 0) / sent * 100) if sent > 0 else 0
        }
    
    def get_all_campaigns(self) -> List[Dict]:
        """Get all campaigns"""
        return [
            {
                "id": k,
                "name": v["name"],
                "status": v["status"].value,
                "channel": v["channel"]
            }
            for k, v in self.campaigns.items()
        ]


class ContentGenerator:
    """Marketing content generation"""
    
    def __init__(self):
        self.templates = {}
        self.brand_voice = {}
    
    def add_template(self,
                    template_id: str,
                    template_type: str,
                    template: str):
        """Add content template"""
        self.templates[template_id] = {
            "type": template_type,
            "template": template
        }
    
    def generate_content(self,
                        template_id: str,
                        variables: Dict) -> str:
        """Generate content from template"""
        if template_id not in self.templates:
            raise ValueError(f"Template {template_id} not found")
        
        template = self.templates[template_id]["template"]
        content = template
        
        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
            content = content.replace(f"{{{{{key.upper()}}}}}", str(value))
        
        return content
    
    def set_brand_voice(self, 
                       tone: str,
                       keywords: List[str] = None,
                       cta_style: str = "direct"):
        """Set brand voice parameters"""
        self.brand_voice = {
            "tone": tone,
            "keywords": keywords or [],
            "cta_style": cta_style
        }
    
    def generate_social_post(self,
                            platform: str,
                            message: str,
                            include_cta: bool = True) -> str:
        """Generate social media post"""
        post = message
        
        if include_cta:
            if self.brand_voice.get("cta_style") == "direct":
                cta = "Shop now!"
            else:
                cta = "Learn more →"
            post += f"\n\n{cta}"
        
        if self.brand_voice.get("keywords"):
            tags = " ".join([f"#{k}" for k in self.brand_voice["keywords"][:5]])
            post += f"\n\n{tags}"
        
        max_length = {"twitter": 280, "linkedin": 3000, "instagram": 2200}
        if len(post) > max_length.get(platform, 280):
            post = post[:max_length[platform] - 3] + "..."
        
        return post
    
    def generate_email(self,
                      subject_template: str,
                      body_template: str,
                      variables: Dict) -> Dict:
        """Generate email content"""
        subject = self.generate_content(subject_template, variables)
        body = self.generate_content(body_template, variables)
        
        return {
            "subject": subject,
            "body": body,
            "preview_text": variables.get("preview", subject[:50])
        }


class AnalyticsDashboard:
    """Marketing analytics dashboard"""
    
    def __init__(self):
        self.metrics = {}
        self.goals = {}
    
    def track_event(self, 
                   event_type: str,
                   properties: Dict):
        """Track marketing event"""
        if event_type not in self.metrics:
            self.metrics[event_type] = []
        
        self.metrics[event_type].append({
            "properties": properties,
            "timestamp": datetime.now()
        })
    
    def set_goal(self, 
                goal_id: str,
                metric: str,
                target: float,
                period: str = "monthly"):
        """Set marketing goal"""
        self.goals[goal_id] = {
            "metric": metric,
            "target": target,
            "current": 0,
            "period": period
        }
    
    def update_goal_progress(self, goal_id: str, value: float):
        """Update goal progress"""
        if goal_id in self.goals:
            self.goals[goal_id]["current"] = value
    
    def get_goal_status(self) -> List[Dict]:
        """Get goal status"""
        return [
            {
                "goal_id": k,
                "metric": v["metric"],
                "target": v["target"],
                "current": v["current"],
                "progress": (v["current"] / v["target"] * 100) if v["target"] > 0 else 0
            }
            for k, v in self.goals.items()
        ]
    
    def generate_report(self) -> Dict:
        """Generate marketing report"""
        total_impressions = len(self.metrics.get("impression", []))
        total_clicks = len(self.metrics.get("click", []))
        total_conversions = len(self.metrics.get("conversion", []))
        
        return {
            "period": {"start": datetime.now() - timedelta(days=30), "end": datetime.now()},
            "impressions": total_impressions,
            "clicks": total_clicks,
            "conversions": total_conversions,
            "ctr": (total_clicks / total_impressions * 100) if total_impressions > 0 else 0,
            "conversion_rate": (total_conversions / total_clicks * 100) if total_clicks > 0 else 0,
            "goal_progress": self.get_goal_status()
        }


class SEOAnalyzer:
    """SEO analysis utilities"""
    
    def __init__(self):
        self.keywords = {}
        self.competitors = {}
    
    def analyze_keyword(self, 
                       keyword: str,
                       content: str) -> Dict:
        """Analyze keyword in content"""
        import re
        content_lower = content.lower()
        keyword_lower = keyword.lower()
        
        occurrences = content_lower.count(keyword_lower)
        density = (occurrences * len(keyword_lower) / len(content_lower) * 100) if len(content_lower) > 0 else 0
        
        return {
            "keyword": keyword,
            "occurrences": occurrences,
            "density": round(density, 2),
            "suggestions": self._get_suggestions(occurrences, density)
        }
    
    def _get_suggestions(self, occurrences: int, density: float) -> List[str]:
        """Get optimization suggestions"""
        suggestions = []
        
        if occurrences == 0:
            suggestions.append("Add keyword to content")
        if density < 0.5:
            suggestions.append("Increase keyword density")
        elif density > 3.0:
            suggestions.append("Reduce keyword usage to avoid over-optimization")
        
        return suggestions
    
    def get_serp_preview(self, 
                        title: str,
                        meta_description: str,
                        url: str,
                        keyword: str) -> Dict:
        """Generate SERP preview"""
        return {
            "title": title[:60] + "..." if len(title) > 60 else title,
            "url": url,
            "description": meta_description[:160] + "..." if len(meta_description) > 160 else meta_description,
            "keyword": keyword,
            "keyword_in_title": keyword.lower() in title.lower(),
            "keyword_in_description": keyword.lower() in meta_description.lower()
        }


if __name__ == "__main__":
    audience = AudienceSegment()
    campaigns = CampaignManager()
    content = ContentGenerator()
    analytics = AnalyticsDashboard()
    seo = SEOAnalyzer()
    
    seg_id = audience.create_segment("Young Professionals", {
        "age_range": "25-35",
        "location": "urban",
        "interests": "technology"
    })
    seg_size = audience.estimate_size(seg_id, 10000)
    
    campaign_id = campaigns.create_campaign(
        "Summer Sale",
        "email",
        [seg_id],
        {"subject": "Summer Sale - 50% Off!", "body": "Shop now"}
    )
    campaigns.launch_campaign(campaign_id)
    
    content.set_brand_voice("friendly", ["summer", "sale", "fashion"], "direct")
    email = content.generate_email(
        "Special Offer for {{NAME}}",
        "Hi {{NAME}},\n\nCheck out our {{PRODUCT}}!",
        {"NAME": "John", "PRODUCT": "Summer Collection"}
    )
    
    analytics.track_event("impression", {"campaign": campaign_id})
    analytics.set_goal("conversions", "sales", 1000)
    
    seo_analysis = seo.analyze_keyword("marketing", "Marketing is essential for business growth. Effective marketing strategies...")
    serp = seo.get_serp_preview(
        "Best Marketing Services",
        "Professional marketing services for your business",
        "https://example.com/marketing",
        "marketing services"
    )
    
    print(f"Segment: {seg_id}, Size: {seg_size}")
    print(f"Campaign: {campaign_id}")
    print(f"Email subject: {email['subject']}")
    print(f"SEO keyword density: {seo_analysis['density']}%")
    print(f"SERP keyword in title: {serp['keyword_in_title']}")
