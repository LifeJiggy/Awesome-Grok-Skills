"""Audience Development Agent - Audience Growth and Engagement."""

import os
import json
import hashlib
import datetime
import random
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum


class Channel(Enum):
    SOCIAL = "social"
    EMAIL = "email"
    CONTENT = "content"
    COMMUNITY = "community"
    SEO = "seo"
    PAID = "paid"
    INFLUENCER = "influencer"
    AFFILIATE = "affiliate"
    REFERRAL = "referral"
    PR = "pr"


class GrowthTactic(Enum):
    CONTENT_MARKETING = "content_marketing"
    SOCIAL_CAMPAIGN = "social_campaign"
    EMAIL_SEQUENCE = "email_sequence"
    PARTNERSHIP = "partnership"
    VIRAL_LOOP = "viral_loop"
    REFERRAL_PROGRAM = "referral_program"
    INFLUENCER_COLLAB = "influencer_collab"
    WEBINAR = "webinar"
    FREE_TRIAL = "free_trial"
    FREEMIUM = "freemium"


class AudienceSegment(Enum):
    NEW_VISITORS = "new_visitors"
    RETURNING = "returning"
    ENGAGED = "engaged"
    POWER_USERS = "power_users"
    CHURNED = "churned"
    PROSPECTS = "prospects"
    CUSTOMERS = "customers"
    ADVOCATES = "advocates"


class CampaignStatus(Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class Config:
    primary_channel: str = "social"
    secondary_channel: str = "email"
    target_growth: str = "2x"
    engagement_threshold: float = 0.05
    conversion_target: float = 0.03
    churn_threshold: float = 0.10
    beta_threshold: float = 0.95
    notification_threshold: float = 0.05
    experiment_duration_days: int = 14
    min_sample_size: int = 1000
    confidence_level: float = 0.95
    auto_optimize: bool = True
    ab_testing_enabled: bool = True
    personalization: bool = True
    retry_max: int = 3
    retry_delay_seconds: int = 5
    output_format: str = "json"
    tags: List[str] = field(default_factory=list)
    excluded_segments: List[str] = field(default_factory=list)
    budget_monthly: float = 5000.0
    team_size: int = 3


@dataclass
class Audience:
    id: str
    segment: str
    channel: str
    size: int
    engagement_rate: float
    growth_rate: float
    demographics: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Campaign:
    id: str
    name: str
    channel: str
    tactic: str
    status: str
    target_segment: str
    budget: float
    spent: float = 0.0
    reach: int = 0
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    engagement_rate: float = 0.0
    conversion_rate: float = 0.0
    roi: float = 0.0
    created_at: str = ""
    updated_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Experiment:
    id: str
    name: str
    hypothesis: str
    variant_a: str
    variant_b: str
    status: str
    campaign_id: str
    sample_size: int = 0
    confidence: float = 0.0
    winner: str = ""
    lift_percent: float = 0.0
    created_at: str = ""


@dataclass
class Insight:
    id: str
    category: str
    title: str
    description: str
    data: Dict[str, Any] = field(default_factory=dict)
    actionable: bool = True
    priority: str = "medium"
    created_at: str = ""


class AudienceStorage:
    """Persists audience data, campaigns, and experiments."""

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or "/tmp/audience_development.json"
        self.audiences: Dict[str, Audience] = {}
        self.campaigns: Dict[str, Campaign] = {}
        self.experiments: Dict[str, Experiment] = {}
        self.insights: Dict[str, Insight] = {}
        self._load()

    def save_audience(self, audience: Audience) -> Audience:
        self.audiences[audience.id] = audience
        self._persist()
        return audience

    def get_audience(self, audience_id: str) -> Optional[Audience]:
        return self.audiences.get(audience_id)

    def list_audiences(self, segment: Optional[str] = None) -> List[Audience]:
        audiences = list(self.audiences.values())
        if segment:
            audiences = [a for a in audiences if a.segment == segment]
        return audiences

    def save_campaign(self, campaign: Campaign) -> Campaign:
        self.campaigns[campaign.id] = campaign
        self._persist()
        return campaign

    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        return self.campaigns.get(campaign_id)

    def list_campaigns(self, channel: Optional[str] = None, status: Optional[str] = None) -> List[Campaign]:
        campaigns = list(self.campaigns.values())
        if channel:
            campaigns = [c for c in campaigns if c.channel == channel]
        if status:
            campaigns = [c for c in campaigns if c.status == status]
        return campaigns

    def save_experiment(self, experiment: Experiment) -> Experiment:
        self.experiments[experiment.id] = experiment
        self._persist()
        return experiment

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        return self.experiments.get(experiment_id)

    def list_experiments(self, campaign_id: Optional[str] = None) -> List[Experiment]:
        experiments = list(self.experiments.values())
        if campaign_id:
            experiments = [e for e in experiments if e.campaign_id == campaign_id]
        return experiments

    def save_insight(self, insight: Insight) -> Insight:
        self.insights[insight.id] = insight
        self._persist()
        return insight

    def list_insights(self, category: Optional[str] = None) -> List[Insight]:
        insights = list(self.insights.values())
        if category:
            insights = [i for i in insights if i.category == category]
        return insights

    def delete_audience(self, audience_id: str) -> bool:
        if audience_id in self.audiences:
            del self.audiences[audience_id]
            self._persist()
            return True
        return False

    def delete_campaign(self, campaign_id: str) -> bool:
        if campaign_id in self.campaigns:
            del self.campaigns[campaign_id]
            self._persist()
            return True
        return False

    def _persist(self) -> None:
        try:
            data = {
                "audiences": {k: self._serialize_audience(v) for k, v in self.audiences.items()},
                "campaigns": {k: self._serialize_campaign(v) for k, v in self.campaigns.items()},
                "experiments": {k: self._serialize_experiment(v) for k, v in self.experiments.items()},
                "insights": {k: self._serialize_insight(v) for k, v in self.insights.items()},
            }
            with open(self.storage_path, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception:
            pass

    def _load(self) -> None:
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                for k, v in data.get("audiences", {}).items():
                    self.audiences[k] = Audience(**v)
                for k, v in data.get("campaigns", {}).items():
                    self.campaigns[k] = Campaign(**v)
                for k, v in data.get("experiments", {}).items():
                    self.experiments[k] = Experiment(**v)
                for k, v in data.get("insights", {}).items():
                    self.insights[k] = Insight(**v)
        except Exception:
            pass

    def _serialize_audience(self, a: Audience) -> Dict[str, Any]:
        return a.__dict__

    def _serialize_campaign(self, c: Campaign) -> Dict[str, Any]:
        return c.__dict__

    def _serialize_experiment(self, e: Experiment) -> Dict[str, Any]:
        return e.__dict__

    def _serialize_insight(self, i: Insight) -> Dict[str, Any]:
        return i.__dict__


class AudienceAnalyzer:
    """Analyzes audience data and generates insights."""

    def __init__(self, storage: AudienceStorage):
        self._storage = storage

    def analyze_audience(self, channel: str, segment: Optional[str] = None) -> Dict[str, Any]:
        audiences = self._storage.list_audiences(segment)
        if not audiences:
            audiences = self._generate_sample_audiences(channel, segment)

        total_size = sum(a.size for a in audiences)
        avg_engagement = sum(a.engagement_rate for a in audiences) / max(1, len(audiences))
        avg_growth = sum(a.growth_rate for a in audiences) / max(1, len(audiences))
        demographics = self._aggregate_demographics(audiences)
        channel_health = self._calculate_channel_health(audiences)

        return {
            "channel": channel,
            "segment": segment or "all",
            "total_size": total_size,
            "audience_count": len(audiences),
            "average_engagement_rate": round(avg_engagement, 4),
            "average_growth_rate": round(avg_growth, 4),
            "demographics": demographics,
            "channel_health": channel_health,
            "top_segments": [
                {"segment": a.segment, "size": a.size, "engagement_rate": a.engagement_rate}
                for a in sorted(audiences, key=lambda x: x.engagement_rate, reverse=True)[:5]
            ],
            "at_risk_segments": [
                {"segment": a.segment, "engagement_rate": a.engagement_rate, "reason": "Low engagement"}
                for a in audiences if a.engagement_rate < 0.02
            ],
        }

    def _generate_sample_audiences(self, channel: str, segment: Optional[str]) -> List[Audience]:
        segments = [s.value for s in AudienceSegment]
        if segment:
            segments = [segment]
        audiences = []
        timestamp = datetime.datetime.now().isoformat()
        for seg in segments:
            for i in range(3):
                aud = Audience(
                    id=f"aud-{hashlib.md5((channel + seg + str(i)).encode()).hexdigest()[:8]}",
                    segment=seg,
                    channel=channel,
                    size=random.randint(500, 50000),
                    engagement_rate=round(random.uniform(0.01, 0.15), 4),
                    growth_rate=round(random.uniform(-0.05, 0.25), 4),
                    demographics=self._generate_demographics(),
                    created_at=timestamp,
                    updated_at=timestamp,
                )
                audiences.append(aud)
        return audiences

    def _generate_demographics(self) -> Dict[str, Any]:
        return {
            "age": {"18-24": random.randint(10, 30), "25-34": random.randint(20, 40), "35-44": random.randint(15, 30), "45+": random.randint(5, 20)},
            "gender": {"male": random.randint(20, 50), "female": random.randint(20, 50), "other": random.randint(1, 10)},
            "location": {"US": random.randint(30, 60), "EU": random.randint(10, 30), "APAC": random.randint(5, 20), "other": random.randint(1, 10)},
            "device": {"mobile": random.randint(40, 70), "desktop": random.randint(20, 50), "tablet": random.randint(5, 15)},
        }

    def _aggregate_demographics(self, audiences: List[Audience]) -> Dict[str, Any]:
        aggregated = {"age": {}, "gender": {}, "location": {}, "device": {}}
        for aud in audiences:
            demos = aud.demographics
            for key in aggregated:
                for sub_key, value in demos.get(key, {}).items():
                    aggregated[key][sub_key] = aggregated[key].get(sub_key, 0) + value
        return aggregated

    def _calculate_channel_health(self, audiences: List[Audience]) -> Dict[str, Any]:
        if not audiences:
            return {"status": "unknown", "score": 0.0}
        avg_engagement = sum(a.engagement_rate for a in audiences) / len(audiences)
        avg_growth = sum(a.growth_rate for a in audiences) / len(audiences)
        score = min(100.0, avg_engagement * 200 + avg_growth * 100 + 50)
        status = "healthy" if score >= 70 else ("at_risk" if score >= 40 else "critical")
        return {"status": status, "score": round(score, 2), "avg_engagement": round(avg_engagement, 4), "avg_growth": round(avg_growth, 4)}

    def generate_insights(self, channel: str) -> List[Insight]:
        analysis = self.analyze_audience(channel)
        insights = []
        timestamp = datetime.datetime.now().isoformat()

        if analysis["average_engagement_rate"] < 0.03:
            insights.append(Insight(
                id=f"ins-{hashlib.md5((channel + 'engagement').encode()).hexdigest()[:8]}",
                category="engagement",
                title="Low engagement detected",
                description=f"Average engagement rate is {analysis['average_engagement_rate']:.2%}, below the 5% threshold.",
                data={"avg_engagement_rate": analysis["average_engagement_rate"]},
                actionable=True,
                priority="high",
                created_at=timestamp,
            ))

        if analysis["average_growth_rate"] < 0.0:
            insights.append(Insight(
                id=f"ins-{hashlib.md5((channel + 'growth').encode()).hexdigest()[:8]}",
                category="growth",
                title="Negative growth trend",
                description=f"Average growth rate is {analysis['average_growth_rate']:.2%}. Audience is shrinking.",
                data={"avg_growth_rate": analysis["average_growth_rate"]},
                actionable=True,
                priority="critical",
                created_at=timestamp,
            ))

        insights.append(Insight(
            id=f"ins-{hashlib.md5((channel + 'opportunity').encode()).hexdigest()[:8]}",
            category="opportunity",
            title="Optimize top segment",
            description=f"Top segment: {analysis['top_segments'][0]['segment']} with engagement rate {analysis['top_segments'][0]['engagement_rate']:.2%}.",
            data={"top_segment": analysis["top_segments"][0]},
            actionable=True,
            priority="medium",
            created_at=timestamp,
        ))

        for insight in insights:
            self._storage.save_insight(insight)
        return insights


class ContentOptimizer:
    """Optimizes content for audience engagement."""

    def __init__(self):
        self._templates: Dict[str, str] = {
            "social_post": "🚀 {hook}\n\n{body}\n\n{cta}\n\n{hashtags}",
            "email_subject": "Exciting news about {topic}!",
            "email_body": "Hi {name},\n\n{body}\n\nBest regards,\n{from_name}",
            "headline": "{benefit} for {audience}: {proof}",
            "cta_button": "{action} Now",
        }

    def optimize_for_engagement(self, content: str, channel: str, audience: Optional[Audience] = None) -> Dict[str, Any]:
        optimized_content = content
        score = self._score_content(content, channel)
        suggestions = self._generate_optimization_suggestions(content, channel, score)
        if channel == Channel.SOCIAL.value:
            optimized_content = self._optimize_social(content)
        elif channel == Channel.EMAIL.value:
            optimized_content = self._optimize_email(content)
        elif channel == Channel.CONTENT.value:
            optimized_content = self._optimize_content(content)

        return {
            "original": content,
            "optimized": optimized_content,
            "predicted_engagement": round(min(0.30, score / 100 * 0.25), 4),
            "original_score": score,
            "optimized_score": min(100.0, score * 1.2),
            "suggestions": suggestions,
            "tone": self._detect_tone(content),
            "readability_score": self._score_readability(content),
            "channel": channel,
        }

    def optimize_for_conversion(self, content: str, goal: str = "signup") -> Dict[str, Any]:
        conversion_elements = {"signup": ["Form", "CTA", "Benefit", "Social Proof"], "purchase": ["Product", "Price", "CTA", "Guarantee"], "demo": ["Demo Form", "Calendar", "CTA", "Value Prop"]}
        elements = conversion_elements.get(goal, ["CTA", "Value Prop"])
        optimized = content
        for element in elements:
            if element.lower() not in content.lower():
                optimized += f"\n\n[Add {element}]"
        return {
            "original": content,
            "optimized": optimized,
            "conversion_elements_added": elements,
            "predicted_conversion": round(random.uniform(0.02, 0.08), 4),
        }

    def _optimize_social(self, content: str) -> str:
        optimized = content
        if not any(optimized.startswith(prefix) for prefix in ["🚀", "💡", "🔥", "✨", "📱", "✅"]):
            optimized = "🚀 " + optimized
        if "?" not in optimized and len(optimized) > 50:
            optimized += "\n\nWhat do you think? 👇"
        if not any(optimized.count(hashtag) >= 1 for hashtag in ["#", "#"]):
            hashtags = ["#Growth", "#Marketing", "#Audience"]
            optimized += "\n\n" + " ".join(hashtags[:3])
        return optimized

    def _optimize_email(self, content: str) -> str:
        optimized = content
        if "{{name}}" not in optimized:
            optimized = "Hi {{name}},\n\n" + optimized
        if "{" not in optimized:
            optimized += "\n\n[Add personalized CTA]"
        if "unsubscribe" not in optimized.lower():
            optimized += "\n\n---\nUnsubscribe | Preferences"
        return optimized

    def _optimize_content(self, content: str) -> str:
        optimized = content
        word_count = len(optimized.split())
        if word_count < 300:
            optimized += "\n\n" + " ".join(["Additional context and details would go here." for _ in range(5)])
        if not optimized.strip().endswith((".", "!", "?")):
            optimized += "."
        return optimized

    def _score_content(self, content: str, channel: str) -> float:
        base_score = 70.0
        if 50 <= len(content) <= 300:
            base_score += 10.0
        if "?" in content:
            base_score += 5.0
        if "!" in content:
            base_score += 3.0
        if any(ord(c) == 0x1F600 for c in content):
            base_score += 5.0
        if "#" in content and channel == Channel.SOCIAL.value:
            base_score += 5.0
        if channel == Channel.EMAIL.value:
            if "unsubscribe" in content.lower():
                base_score += 5.0
            if "{{" in content or "{%" in content:
                base_score += 10.0
        return min(100.0, base_score)

    def _generate_optimization_suggestions(self, content: str, channel: str, score: float) -> List[str]:
        suggestions = []
        if score < 50:
            suggestions.append("Add a compelling hook in the first 100 characters.")
        if len(content) > 500 and channel == Channel.SOCIAL.value:
            suggestions.append("Shorten content for better social engagement.")
        if len(content) < 100:
            suggestions.append("Expand content with more detail and value.")
        if "CTA" not in content.upper() and "http" not in content:
            suggestions.append("Add a clear call-to-action.")
        if not suggestions:
            suggestions.append("Content is well-formed. Consider A/B testing with minor variants.")
        return suggestions

    def _detect_tone(self, content: str) -> str:
        text = content.lower()
        if any(word in text for word in ["urgent", "limited", "hurry", "now", "fast"]):
            return "urgent"
        if any(word in text for word in ["exclusive", "secret", "insider", "private"]):
            return "exclusive"
        if any(word in text for word in ["friendly", "hello", "hi", "thanks", "cheers"]):
            return "friendly"
        if any(word in text for word in ["proven", "guaranteed", "results", "studies"]):
            return "authoritative"
        return "neutral"

    def _score_readability(self, content: str) -> float:
        words = content.split()
        if not words:
            return 0.0
        sentences = content.split(".")
        avg_words_per_sentence = len(words) / max(1, len(sentences))
        score = 100.0
        if avg_words_per_sentence > 20:
            score -= (avg_words_per_sentence - 20) * 2
        if avg_words_per_sentence < 5:
            score -= 5.0
        return max(0.0, min(100.0, round(score, 2)))


class CampaignManager:
    """Manages audience development campaigns."""

    def __init__(self, storage: AudienceStorage):
        self._storage = storage

    def create_campaign(self, name: str, channel: str, tactic: str, target_segment: str, budget: float,
                        description: str = "", start_date: Optional[str] = None,
                        end_date: Optional[str] = None) -> Campaign:
        campaign_id = f"camp-{hashlib.md5((name + channel + datetime.datetime.now().isoformat()).encode()).hexdigest()[:8]}"
        timestamp = datetime.datetime.now().isoformat()
        campaign = Campaign(
            id=campaign_id,
            name=name,
            channel=channel,
            tactic=tactic,
            status=CampaignStatus.DRAFT.value,
            target_segment=target_segment,
            budget=budget,
            created_at=timestamp,
            updated_at=timestamp,
            metadata={"description": description, "start_date": start_date, "end_date": end_date},
        )
        self._storage.save_campaign(campaign)
        return campaign

    def launch_campaign(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self._storage.get_campaign(campaign_id)
        if not campaign:
            return {"status": "error", "message": "Campaign not found"}
        campaign.status = CampaignStatus.RUNNING.value
        campaign.updated_at = datetime.datetime.now().isoformat()
        self._storage.save_campaign(campaign)
        return {"status": "launched", "campaign_id": campaign_id, "name": campaign.name}

    def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self._storage.get_campaign(campaign_id)
        if not campaign:
            return {"status": "error", "message": "Campaign not found"}
        campaign.status = CampaignStatus.PAUSED.value
        campaign.updated_at = datetime.datetime.now().isoformat()
        self._storage.save_campaign(campaign)
        return {"status": "paused", "campaign_id": campaign_id}

    def update_campaign_metrics(self, campaign_id: str, reach: int = 0, impressions: int = 0,
                                 clicks: int = 0, conversions: int = 0, spent: float = 0.0) -> Dict[str, Any]:
        campaign = self._storage.get_campaign(campaign_id)
        if not campaign:
            return {"status": "error", "message": "Campaign not found"}
        campaign.reach += reach
        campaign.impressions += impressions
        campaign.clicks += clicks
        campaign.conversions += conversions
        campaign.spent += spent
        campaign.engagement_rate = round((campaign.clicks / max(1, campaign.impressions)), 4)
        campaign.conversion_rate = round((campaign.conversions / max(1, campaign.clicks)), 4)
        campaign.roi = round((campaign.conversions * 50 - campaign.spent) / max(1, campaign.spent), 4)
        campaign.updated_at = datetime.datetime.now().isoformat()
        self._storage.save_campaign(campaign)
        return self._summarize_campaign(campaign)

    def _summarize_campaign(self, campaign: Campaign) -> Dict[str, Any]:
        return {
            "campaign_id": campaign.id,
            "name": campaign.name,
            "channel": campaign.channel,
            "status": campaign.status,
            "budget": campaign.budget,
            "spent": campaign.spent,
            "reach": campaign.reach,
            "impressions": campaign.impressions,
            "clicks": campaign.clicks,
            "conversions": campaign.conversions,
            "engagement_rate": campaign.engagement_rate,
            "conversion_rate": campaign.conversion_rate,
            "roi": campaign.roi,
            "cpc": round(campaign.spent / max(1, campaign.clicks), 2),
        }

    def get_campaign_summary(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self._storage.get_campaign(campaign_id)
        if not campaign:
            return {"status": "error", "message": "Campaign not found"}
        return self._summarize_campaign(campaign)

    def calculate_roi(self, campaign_id: str) -> float:
        campaign = self._storage.get_campaign(campaign_id)
        if not campaign:
            return 0.0
        return campaign.roi


class ExperimentManager:
    """Manages growth experiments and A/B tests."""

    def __init__(self, storage: AudienceStorage):
        self._storage = storage
        self._running_experiments: Dict[str, Dict[str, Any]] = {}

    def create_experiment(self, name: str, hypothesis: str, variant_a: str, variant_b: str,
                          campaign_id: str, sample_size: int = 1000,
                          confidence_level: float = 0.95) -> Experiment:
        experiment_id = f"exp-{hashlib.md5((name + datetime.datetime.now().isoformat()).encode()).hexdigest()[:8]}"
        timestamp = datetime.datetime.now().isoformat()
        experiment = Experiment(
            id=experiment_id,
            name=name,
            hypothesis=hypothesis,
            variant_a=variant_a,
            variant_b=variant_b,
            status=CampaignStatus.RUNNING.value,
            campaign_id=campaign_id,
            sample_size=sample_size,
            confidence=confidence_level,
            created_at=timestamp,
        )
        self._storage.save_experiment(experiment)
        self._running_experiments[experiment_id] = {
            "variant_a_responses": 0,
            "variant_b_responses": 0,
            "variant_a_successes": 0,
            "variant_b_successes": 0,
        }
        return experiment

    def record_response(self, experiment_id: str, variant: str, success: bool) -> Dict[str, Any]:
        if experiment_id not in self._running_experiments:
            return {"status": "error", "message": "Experiment not found"}
        exp_state = self._running_experiments[experiment_id]
        key = f"variant_{variant.lower().replace('variant ', '')}_responses"
        success_key = f"variant_{variant.lower().replace('variant ', '')}_successes"
        exp_state[key] = exp_state.get(key, 0) + 1
        if success:
            exp_state[success_key] = exp_state.get(success_key, 0) + 1
        total_samples = exp_state["variant_a_responses"] + exp_state["variant_b_responses"]
        if total_samples >= self._storage.experiments[experiment_id].sample_size:
            return self._analyze_experiment(experiment_id)
        return {"status": "collecting", "samples_collected": total_samples, "required": self._storage.experiments[experiment_id].sample_size}

    def _analyze_experiment(self, experiment_id: str) -> Dict[str, Any]:
        if experiment_id not in self._running_experiments:
            return {"status": "error", "message": "Experiment not found"}
        experiment = self._storage.get_experiment(experiment_id)
        if not experiment:
            return {"status": "error", "message": "Experiment not found"}
        exp_state = self._running_experiments[experiment_id]
        a_total = exp_state.get("variant_a_responses", 0)
        b_total = exp_state.get("variant_b_responses", 0)
        a_success = exp_state.get("variant_a_successes", 0)
        b_success = exp_state.get("variant_b_successes", 0)
        a_rate = a_success / max(1, a_total)
        b_rate = b_success / max(1, b_total)
        lift = ((b_rate - a_rate) / max(0.001, a_rate)) * 100
        winner = "variant B" if b_rate > a_rate else "variant A"
        is_significant = abs(lift) > 5.0
        experiment.status = CampaignStatus.COMPLETED.value
        experiment.sample_size = a_total + b_total
        experiment.confidence = 0.95 if is_significant else 0.80
        experiment.winner = winner
        experiment.lift_percent = round(lift, 2)
        self._storage.save_experiment(experiment)
        return {
            "status": "completed",
            "experiment_id": experiment_id,
            "winner": winner,
            "lift_percent": round(lift, 2),
            "variant_a_rate": round(a_rate, 4),
            "variant_b_rate": round(b_rate, 4),
            "sample_size": experiment.sample_size,
            "confidence": experiment.confidence,
            "is_significant": is_significant,
        }

    def get_experiment_results(self, experiment_id: str) -> Dict[str, Any]:
        experiment = self._storage.get_experiment(experiment_id)
        if not experiment:
            return {"status": "error", "message": "Experiment not found"}
        return {
            "experiment_id": experiment_id,
            "name": experiment.name,
            "status": experiment.status,
            "winner": experiment.winner,
            "lift_percent": experiment.lift_percent,
            "sample_size": experiment.sample_size,
            "confidence": experiment.confidence,
        }


class ContentPlanner:
    """Plans content calendars and distribution."""

    def __init__(self):
        self._content_types = ["blog", "video", "podcast", "infographic", "social_post", "email", "whitepaper"]
        self._content_calendar: Dict[str, List[Dict]] = {}

    def plan_content_calendar(self, brand: str, weeks: int = 4,
                              channels: Optional[List[str]] = None) -> Dict[str, Any]:
        channels = channels or [c.value for c in Channel]
        calendar = []
        timestamp = datetime.datetime.now()
        content_id_counter = 1
        content_templates = {
            Channel.SOCIAL.value: [
                {"title": f"{brand} Tip #{i}", "type": "social_post", "engagement_hook": True}
                for i in range(1, 8)
            ],
            Channel.EMAIL.value: [
                {"title": f"Newsletter: {brand} Update", "type": "email_newsletter", "length": "medium"},
                {"title": f"Promo: Exclusive {brand} Offer", "type": "email_promo", "length": "short"},
            ],
            Channel.CONTENT.value: [
                {"title": f"How {brand} Solves X", "type": "blog", "word_count": 1500},
                {"title": f"{brand} Case Study: Y", "type": "blog", "word_count": 2000},
                {"title": f"The Future of {brand}", "type": "blog", "word_count": 1200},
            ],
            Channel.COMMUNITY.value: [
                {"title": f"{brand} Community Spotlight", "type": "social_post", "engagement_hook": True},
                {"title": f"{brand} AMA Session", "type": "social_post", "engagement_hook": True},
            ],
        }
        for week in range(weeks):
            week_start = timestamp + datetime.timedelta(weeks=week)
            for day in range(7):
                date = week_start + datetime.timedelta(days=day)
                for channel in channels:
                    if channel not in content_templates:
                        continue
                    template_idx = (week * 7 + day) % len(content_templates[channel])
                    template = content_templates[channel][template_idx]
                    item = {
                        "content_id": f"cnt-{content_id_counter:04d}",
                        "date": date.strftime("%Y-%m-%d"),
                        "channel": channel,
                        "title": template.get("title", f"{brand} Content"),
                        "type": template.get("type", "social_post"),
                        "status": "planned",
                        "word_count": template.get("word_count", 200),
                        "engagement_hook": template.get("engagement_hook", False),
                        "cta_required": template.get("type") in ["email_promo", "social_post"],
                        "metadata": {},
                    }
                    calendar.append(item)
                    content_id_counter += 1
        self._content_calendar[brand] = calendar
        self._save_calendar()
        return {
            "brand": brand,
            "weeks_planned": weeks,
            "total_pieces": len(calendar),
            "channels": channels,
            "calendar_preview": calendar[:10],
        }

    def get_calendar(self, brand: str) -> List[Dict]:
        return self._content_calendar.get(brand, [])

    def _save_calendar(self) -> None:
        try:
            with open("/tmp/content_calendar.json", "w") as f:
                json.dump(self._content_calendar, f, indent=2)
        except Exception:
            pass


class MetricsCalculator:
    """Calculates core audience development metrics."""

    def calculate_growth_rate(self, current: int, previous: int) -> float:
        if previous == 0:
            return 0.0
        return round((current - previous) / previous, 4)

    def calculate_churn_rate(self, lost: int, total: int) -> float:
        if total == 0:
            return 0.0
        return round(lost / total, 4)

    def calculate_ltv(self, avg_revenue_per_user: float, avg_lifespan_months: float) -> float:
        return round(avg_revenue_per_user * avg_lifespan_months, 2)

    def calculate_cac(self, total_spend: float, new_customers: int) -> float:
        if new_customers == 0:
            return 0.0
        return round(total_spend / new_customers, 2)

    def calculate_engagement_rate(self, engagements: int, impressions: int) -> float:
        if impressions == 0:
            return 0.0
        return round(engagements / impressions, 4)

    def calculate_virality_coefficient(self, inviter_count: int, invited_count: int) -> float:
        if invited_count == 0:
            return 0.0
        return round(inviter_count / invited_count, 4)

    def calculate_roi(self, revenue: float, spend: float) -> float:
        if spend == 0:
            return 0.0
        return round((revenue - spend) / spend, 4)

    def calculate_nrr(self, starting_revenue: float, expansion_revenue: float, churned_revenue: float) -> float:
        if starting_revenue == 0:
            return 0.0
        return round((starting_revenue - churned_revenue + expansion_revenue) / starting_revenue, 4)

    def aggregate_campaign_metrics(self, campaigns: List[Campaign]) -> Dict[str, Any]:
        if not campaigns:
            return {"total_campaigns": 0}
        total_budget = sum(c.budget for c in campaigns)
        total_spent = sum(c.spent for c in campaigns)
        total_reach = sum(c.reach for c in campaigns)
        total_impressions = sum(c.impressions for c in campaigns)
        total_conversions = sum(c.conversions for c in campaigns)
        total_roi = sum(c.roi for c in campaigns)
        return {
            "total_campaigns": len(campaigns),
            "total_budget": total_budget,
            "total_spent": total_spent,
            "total_reach": total_reach,
            "total_impressions": total_impressions,
            "total_conversions": total_conversions,
            "average_roi": round(total_roi / max(1, len(campaigns)), 4),
            "overall_conversion_rate": round(total_conversions / max(1, total_reach), 4),
            "cpm": round((total_spent / max(1, total_impressions)) * 1000, 2),
            "cpc": round(total_spent / max(1, total_conversions), 2),
        }


class AudienceDevelopmentAgent:
    """Agent for audience development and growth."""

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._audiences: List[Audience] = []
        self._campaigns: List[Campaign] = []
        self._experiments: List[Experiment] = []
        self._insights: List[Insight] = []
        self._storage = AudienceStorage()
        self._analyzer = AudienceAnalyzer(self._storage)
        self._content_optimizer = ContentOptimizer()
        self._campaign_manager = CampaignManager(self._storage)
        self._experiment_manager = ExperimentManager(self._storage)
        self._content_planner = ContentPlanner()
        self._metrics = MetricsCalculator()

    def create_strategy(self, brand_id: str, target_growth: str,
                        channels: Optional[List[str]] = None) -> Dict[str, Any]:
        channels = channels or [Channel.SOCIAL.value, Channel.EMAIL.value, Channel.CONTENT.value]
        strategy_id = f"strat-{hashlib.md5((brand_id + target_growth).encode()).hexdigest()[:8]}"
        timestamp = datetime.datetime.now().isoformat()
        tactics = self._generate_tactics(channels, target_growth)
        strategy = {
            "strategy_id": strategy_id,
            "brand_id": brand_id,
            "target_growth": target_growth,
            "channels": channels,
            "tactics": tactics,
            "timeline_weeks": self._config.experiment_duration_days // 7,
            "budget_monthly": self._config.budget_monthly,
            "target_audience": self._define_target_audience(),
            "kpis": self._define_strategy_kpis(),
            "created_at": timestamp,
            "status": "draft",
        }
        return strategy

    def _generate_tactics(self, channels: List[str], target_growth: str) -> List[Dict[str, Any]]:
        all_tactics = []
        for channel in channels:
            channel_tactics = {
                Channel.SOCIAL.value: [
                    {"tactic": "content_calendar", "description": "Weekly social content calendar", "priority": "high"},
                    {"tactic": "influencer_collab", "description": "Partner with 5 micro-influencers", "priority": "medium"},
                    {"tactic": "community_building", "description": "Launch brand community group", "priority": "medium"},
                ],
                Channel.EMAIL.value: [
                    {"tactic": "welcome_sequence", "description": "5-email welcome sequence", "priority": "high"},
                    {"tactic": "newsletter", "description": "Weekly newsletter", "priority": "medium"},
                    {"tactic": "re_engagement", "description": "Win-back campaign", "priority": "low"},
                ],
                Channel.CONTENT.value: [
                    {"tactic": "seo_optimization", "description": "Optimize 20 top pages", "priority": "high"},
                    {"tactic": "blog_schedule", "description": "2 blog posts per week", "priority": "high"},
                    {"tactic": "video_content", "description": "Weekly video shorts", "priority": "medium"},
                ],
                Channel.COMMUNITY.value: [
                    {"tactic": "forum_moderation", "description": "Daily community moderation", "priority": "medium"},
                    {"tactic": "ama_sessions", "description": "Bi-weekly AMA", "priority": "low"},
                ],
            }
            all_tactics.extend(channel_tactics.get(channel, []))
        return all_tactics

    def _define_target_audience(self) -> Dict[str, Any]:
        return {
            "segments": [s.value for s in AudienceSegment],
            "primary_segment": AudienceSegment.PROSPECTS.value,
            "demographics": {"age_range": "25-45", "interests": ["technology", "business", "learning"]},
            "pain_points": ["time constraints", "skill gaps", "information overload"],
            "motivations": ["career growth", "efficiency", "community"],
        }

    def _define_strategy_kpis(self) -> List[Dict[str, Any]]:
        return [
            {"name": "Audience Growth", "target": self._config.target_growth, "metrics": ["growth_rate", "size"]},
            {"name": "Engagement Rate", "target": f"{int(self._config.engagement_threshold * 100)}%", "metrics": ["engagement_rate", "interaction_rate"]},
            {"name": "Conversion Rate", "target": f"{int(self._config.conversion_target * 100)}%", "metrics": ["conversion_rate", "cac"]},
            {"name": "Retention", "target": f"< {int(self._config.churn_threshold * 100)}%", "metrics": ["churn_rate", "nrr"]},
        ]

    def analyze_audience(self, channel: str, segment: Optional[str] = None) -> Dict[str, Any]:
        return self._analyzer.analyze_audience(channel, segment)

    def optimize_engagement(self, channel: str, content: str,
                            audience_id: Optional[str] = None) -> Dict[str, Any]:
        audience = None
        if audience_id:
            audience = self._storage.get_audience(audience_id)
        return self._content_optimizer.optimize_for_engagement(content, channel, audience)

    def optimize_for_conversion(self, content: str, goal: str = "signup") -> Dict[str, Any]:
        return self._content_optimizer.optimize_for_conversion(content, goal)

    def run_growth_experiment(self, experiment: Dict, campaign_id: Optional[str] = None) -> Dict[str, Any]:
        campaign_id = campaign_id or "default"
        exp_obj = self._experiment_manager.create_experiment(
            name=experiment.get("name", "Exp-1"),
            hypothesis=experiment.get("hypothesis", "Variant B performs better"),
            variant_a=experiment.get("variant_a", "Control"),
            variant_b=experiment.get("variant_b", "Treatment"),
            campaign_id=campaign_id,
            sample_size=experiment.get("sample_size", self._config.min_sample_size),
            confidence_level=self._config.confidence_level,
        )
        self._experiments.append(exp_obj)
        return {"experiment_id": exp_obj.id, "status": "running", "sample_size": exp_obj.sample_size, "campaign_id": campaign_id}

    def create_campaign(self, name: str, channel: str, tactic: str, budget: float,
                        description: str = "", start_date: Optional[str] = None,
                        end_date: Optional[str] = None) -> Campaign:
        return self._campaign_manager.create_campaign(name, channel, tactic, "all", budget,
                                                      description, start_date, end_date)

    def launch_campaign(self, campaign_id: str) -> Dict[str, Any]:
        return self._campaign_manager.launch_campaign(campaign_id)

    def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        return self._campaign_manager.pause_campaign(campaign_id)

    def update_campaign_metrics(self, campaign_id: str, **metrics) -> Dict[str, Any]:
        return self._campaign_manager.update_campaign_metrics(campaign_id, **metrics)

    def plan_content_calendar(self, brand: str, weeks: int = 4, channels: Optional[List[str]] = None) -> Dict[str, Any]:
        return self._content_planner.plan_content_calendar(brand, weeks, channels)

    def generate_growth_report(self, channel: str) -> Dict[str, Any]:
        analysis = self._analyzer.analyze_audience(channel)
        campaigns = self._storage.list_campaigns(channel=channel)
        campaign_metrics = self._metrics.aggregate_campaign_metrics(campaigns)
        insights = self._analyzer.generate_insights(channel)
        experiments = self._storage.list_experiments()
        completed_experiments = [e for e in experiments if e.status == CampaignStatus.COMPLETED.value]
        return {
            "report_title": f"Growth Report - {channel}",
            "generated_at": datetime.datetime.now().isoformat(),
            "channel_analysis": analysis,
            "campaign_metrics": campaign_metrics,
            "total_campaigns": len(campaigns),
            "active_campaigns": len([c for c in campaigns if c.status == CampaignStatus.RUNNING.value]),
            "insights": [{"id": i.id, "title": i.title, "priority": i.priority} for i in insights],
            "insights_count": len(insights),
            "experiments": {
                "total": len(experiments),
                "completed": len(completed_experiments),
                "results": [{"id": e.id, "winner": e.winner, "lift": e.lift_percent} for e in completed_experiments],
            },
            "recommendations": [i.description for i in insights if i.actionable and i.priority == "high"],
        }

    def get_recommendations(self, channel: str) -> List[Dict[str, Any]]:
        insights = self._analyzer.generate_insights(channel)
        return [{"id": i.id, "title": i.title, "priority": i.priority, "actionable": i.actionable} for i in insights]

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "AudienceDevelopmentAgent",
            "audiences": len(self._audiences),
            "campaigns": len(self._campaigns),
            "experiments": len(self._experiments),
            "insights": len(self._insights),
            "config": {
                "primary_channel": self._config.primary_channel,
                "target_growth": self._config.target_growth,
                "budget_monthly": self._config.budget_monthly,
            },
            "storage": {
                "total_audiences": len(self._storage.audiences),
                "total_campaigns": len(self._storage.campaigns),
                "total_experiments": len(self._storage.experiments),
                "total_insights": len(self._storage.insights),
            },
        }

    def export_data(self, format: str = "json") -> Dict[str, Any]:
        campaigns = self._storage.list_campaigns()
        experiments = self._storage.list_experiments()
        insights = self._storage.list_insights()
        data = {
            "campaigns": [self._campaign_manager._summarize_campaign(c) for c in campaigns],
            "experiments": [{"id": e.id, "name": e.name, "status": e.status, "winner": e.winner} for e in experiments],
            "insights": [{"id": i.id, "title": i.title, "priority": i.priority} for i in insights],
        }
        if format == "json":
            return {"format": "json", "data": data}
        elif format == "csv":
            return {"format": "csv", "data": data}
        return {"format": format, "data": data}


def main():
    print("Audience Development Agent Demo")
    agent = AudienceDevelopmentAgent()
    strategy = agent.create_strategy(brand_id="brand-1", target_growth="2x")
    analysis = agent.analyze_audience(channel="social")
    content = agent.optimize_engagement(channel="social", content="Check out our new product!")
    campaign = agent.create_campaign(name="Spring Campaign", channel="social", tactic="social_campaign", budget=2000.0)
    status = agent.get_status()
    print(status)


if __name__ == "__main__":
    main()
