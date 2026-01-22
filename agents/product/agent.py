"""
Product Management Agent
Product strategy and roadmap planning
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class Priority(Enum):
    P0 = "critical"
    P1 = "high"
    P2 = "medium"
    P3 = "low"


class FeatureStatus(Enum):
    IDEA = "idea"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    LAUNCHED = "launched"


@dataclass
class Feature:
    feature_id: str
    name: str
    priority: Priority
    status: FeatureStatus
    effort: int


class ProductStrategyManager:
    """Product strategy management"""
    
    def __init__(self):
        self.strategies = {}
    
    def define_product_strategy(self, 
                               vision: str,
                               goals: List[str],
                               target_market: Dict) -> Dict:
        """Define product strategy"""
        return {
            'vision': vision,
            'mission': 'Deliver exceptional value to customers through innovative solutions',
            'strategic_goals': goals,
            'target_market': target_market,
            'competitive_position': {
                'strengths': ['User experience', 'Integration', 'Price'],
                'weaknesses': ['Enterprise features', 'Localization'],
                'opportunities': ['Emerging markets', 'New verticals'],
                'threats': ['Competitor X', 'Market consolidation']
            },
            'success_metrics': [
                'Revenue growth > 20%',
                'Customer satisfaction > 90%',
                'Market share > 15%'
            ],
            'timeline': {
                'short_term': '6 months',
                'medium_term': '18 months',
                'long_term': '3-5 years'
            }
        }
    
    def analyze_market(self, market: str) -> Dict:
        """Analyze market opportunity"""
        return {
            'market': market,
            'market_size': {
                'tam': '$10B',
                'sam': '$2B',
                'som': '$500M'
            },
            'growth_rate': 15,
            'market_trends': [
                'Shift to cloud-native',
                'AI/ML integration',
                'Mobile-first experiences'
            ],
            'customer_segments': [
                {'segment': 'Enterprise', 'needs': ['Security', 'Scale', 'Support'], 'willingness': 'high'},
                {'segment': 'SMB', 'needs': ['Ease of use', 'Price', 'Speed'], 'willingness': 'medium'},
                {'segment': 'Consumer', 'needs': ['Simplicity', 'Mobile', 'Free tier'}, 'willingness': 'low'}
            ],
            'competitive_landscape': {
                'leader': 'Competitor A (30%)',
                'challengers': ['Competitor B (20%)', 'Competitor C (15%)'],
                'niche_players': ['Various small players (35%)']
            }
        }


class RoadmapPlanner:
    """Roadmap planning"""
    
    def __init__(self):
        self.roadmaps = {}
    
    def create_roadmap(self, 
                      product_name: str,
                      timeframe: str,
                      initiatives: List[Dict]) -> Dict:
        """Create product roadmap"""
        roadmap_id = f"road_{len(self.roadmaps)}"
        
        self.roadmaps[roadmap_id] = {
            'roadmap_id': roadmap_id,
            'product': product_name,
            'timeframe': timeframe,
            'initiatives': initiatives
        }
        
        return self.roadmaps[roadmap_id]
    
    def prioritize_features(self, 
                           features: List[Feature],
                           constraints: Dict) -> List[Dict]:
        """Prioritize features"""
        prioritized = []
        
        for feature in features:
            score = self._calculate_priority_score(feature, constraints)
            prioritized.append({
                'feature': feature.name,
                'priority': feature.priority.value,
                'score': score,
                'effort': feature.effort,
                'impact': score / feature.effort if feature.effort > 0 else 0,
                'recommended_quarter': self._determine_quarter(feature.priority, constraints)
            })
        
        return sorted(prioritized, key=lambda x: x['impact'], reverse=True)
    
    def _calculate_priority_score(self, feature: Feature, constraints: Dict) -> int:
        """Calculate priority score"""
        base_score = 100
        priority_weights = {
            Priority.P0: 50,
            Priority.P1: 30,
            Priority.P2: 15,
            Priority.P3: 5
        }
        return base_score + priority_weights.get(feature.priority, 0)
    
    def _determine_quarter(self, priority: Priority, constraints: Dict) -> str:
        """Determine delivery quarter"""
        quarter_mapping = {
            Priority.P0: 'Q1',
            Priority.P1: 'Q1-Q2',
            Priority.P2: 'Q2-Q3',
            Priority.P3: 'Q3-Q4'
        }
        return quarter_mapping.get(priority, 'TBD')
    
    def generate_roadmap_view(self, initiatives: List[Dict]) -> Dict:
        """Generate roadmap visualization"""
        return {
            'timeline': [
                {
                    'quarter': 'Q1 2024',
                    'themes': ['Foundation', 'Core Features'],
                    'initiatives': [
                        {'name': 'API v2', 'status': 'in_progress', 'progress': 60},
                        {'name': 'User Dashboard', 'status': 'planned', 'progress': 0}
                    ]
                },
                {
                    'quarter': 'Q2 2024',
                    'themes': ['Scale', 'Integration'],
                    'initiatives': [
                        {'name': 'Mobile App', 'status': 'planned', 'progress': 0},
                        {'name': 'Third-party Integrations', 'status': 'idea', 'progress': 0}
                    ]
                }
            ],
            'resource_allocation': {
                'engineering': 60,
                'design': 20,
                'qa': 15,
                'product': 5
            },
            'key_milestones': [
                {'date': '2024-03-31', 'milestone': 'API v2 Launch'},
                {'date': '2024-06-30', 'milestone': 'Mobile App Beta'},
                {'date': '2024-09-30', 'milestone': 'Enterprise Features'}
            ]
        }


class FeatureManager:
    """Feature management"""
    
    def __init__(self):
        self.features = {}
    
    def define_feature(self, 
                      name: str,
                      description: str,
                      user_stories: List[str],
                      acceptance_criteria: List[str]) -> Dict:
        """Define feature"""
        feature_id = f"feat_{len(self.features)}"
        
        self.features[feature_id] = {
            'feature_id': feature_id,
            'name': name,
            'description': description,
            'user_stories': user_stories,
            'acceptance_criteria': acceptance_criteria,
            'status': FeatureStatus.IDEA
        }
        
        return self.features[feature_id]
    
    def create_feature_spec(self, feature_id: str) -> Dict:
        """Create feature specification"""
        feature = self.features.get(feature_id)
        if not feature:
            return {'error': 'Feature not found'}
        
        return {
            'spec_id': f"spec_{feature_id}",
            'overview': {
                'title': feature['name'],
                'description': feature['description'],
                'status': feature['status']
            },
            'user_stories': feature['user_stories'],
            'acceptance_criteria': feature['acceptance_criteria'],
            'technical_considerations': [
                'Backend API changes required',
                'Database migration needed',
                'Frontend component updates'
            ],
            'dependencies': ['Related Feature A', 'Infrastructure Update B'],
            'design_assets': ['Mockups', 'Wireframes', 'Prototypes'],
            'metrics': ['Adoption rate', 'User engagement', 'Error rate']
        }
    
    def track_feature_progress(self, feature_id: str) -> Dict:
        """Track feature progress"""
        return {
            'feature_id': feature_id,
            'status': 'in_progress',
            'progress': 65,
            'completion_criteria': [
                {'criterion': 'Development complete', 'status': 'done'},
                {'criterion': 'Code review passed', 'status': 'done'},
                {'criterion': 'QA testing', 'status': 'in_progress'},
                {'criterion': 'Documentation', 'status': 'pending'}
            ],
            'metrics': {
                'story_points_completed': 21,
                'story_points_total': 34,
                'bugs_found': 5,
                'bugs_resolved': 3
            },
            'timeline': {
                'started': '2024-01-01',
                'estimated_completion': '2024-02-15',
                'velocity': 8
            },
            'risks': [
                {'risk': 'Resource constraints', 'mitigation': 'Cross-train team'}
            ]
        }


class ProductAnalytics:
    """Product analytics"""
    
    def __init__(self):
        self.metrics = {}
    
    def analyze_product_metrics(self) -> Dict:
        """Analyze product metrics"""
        return {
            'acquisition': {
                'monthly_visitors': 100000,
                'conversion_rate': 3.5,
                'cac': 50,
                'channels': {
                    'organic': 40,
                    'paid': 35,
                    'referral': 15,
                    'direct': 10
                }
            },
            'activation': {
                'signup_rate': 25,
                'activation_rate': 60,
                'time_to_activate': '2 days'
            },
            'retention': {
                'd1_retention': 40,
                'd7_retention': 25,
                'd30_retention': 15,
                'churn_rate': 5
            },
            'revenue': {
                'mrr': 150000,
                'arr': 1800000,
                'arpu': 50,
                'ltv': 600,
                'ltv_cac_ratio': 12
            },
            'engagement': {
                'dau': 25000,
                'mau': 75000,
                'dau_mau_ratio': 33,
                'session_duration': '8 minutes',
                'features_used': {
                    'core_feature': 70,
                    'advanced_feature': 30,
                    'experimental_feature': 10
                }
            }
        }
    
    def generate_product_health_score(self) -> Dict:
        """Generate product health score"""
        return {
            'overall_score': 78,
            'dimensions': {
                'acquisition': 75,
                'activation': 80,
                'retention': 70,
                'revenue': 85,
                'engagement': 80
            },
            'trends': {
                'improving': ['revenue', 'engagement'],
                'stable': ['acquisition'],
                'declining': ['retention']
            },
            'recommendations': [
                'Focus on retention improvements',
                'Optimize onboarding flow',
                'Expand successful channels'
            ],
            'health_status': 'healthy with room for improvement'
        }


class CustomerFeedbackManager:
    """Customer feedback management"""
    
    def __init__(self):
        self.feedback = {}
    
    def collect_feedback(self, 
                        source: str,
                        feedback_type: str,
                        content: str) -> Dict:
        """Collect customer feedback"""
        feedback_id = f"fb_{len(self.feedback)}"
        
        self.feedback[feedback_id] = {
            'feedback_id': feedback_id,
            'source': source,
            'type': feedback_type,
            'content': content,
            'sentiment': self._analyze_sentiment(content),
            'created_at': datetime.now(),
            'status': 'new'
        }
        
        return self.feedback[feedback_id]
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze feedback sentiment"""
        positive_words = ['love', 'great', 'excellent', 'helpful']
        negative_words = ['bug', 'broken', 'frustrated', 'hate']
        
        text_lower = text.lower()
        if any(word in text_lower for word in positive_words):
            return 'positive'
        elif any(word in text_lower for word in negative_words):
            return 'negative'
        return 'neutral'
    
    def aggregate_feedback(self) -> Dict:
        """Aggregate feedback insights"""
        return {
            'total_feedback': 1000,
            'by_sentiment': {
                'positive': 450,
                'neutral': 350,
                'negative': 200
            },
            'by_category': {
                'feature_requests': 35,
                'bug_reports': 25,
                'general_feedback': 20,
                'praise': 15,
                'complaints': 5
            },
            'top_requests': [
                {'request': 'Dark mode', 'votes': 150, 'status': 'planned'},
                {'request': 'Mobile app', 'votes': 120, 'status': 'in_progress'},
                {'request': 'API access', 'votes': 80, 'status': 'under_review'}
            ],
            'nps_score': 42,
            'customer_satisfaction': 4.2,
            'action_items': [
                {'item': 'Prioritize dark mode', 'impact': 'high'},
                {'item': 'Fix top reported bugs', 'impact': 'medium'},
                {'item': 'Improve onboarding', 'impact': 'medium'}
            ]
        }


if __name__ == "__main__":
    strategy = ProductStrategyManager()
    
    product_strategy = strategy.define_product_strategy(
        "Revolutionary analytics platform",
        ["Increase market share", "Improve customer satisfaction"],
        {'segment': 'Enterprise', 'size': '500-5000 employees'}
    )
    print(f"Vision: {product_strategy['vision']}")
    print(f"Market position: {product_strategy['competitive_position']['strengths']}")
    
    roadmap = RoadmapPlanner()
    features = [
        Feature('feat_1', 'API v2', Priority.P0, FeatureStatus.PLANNED, 21),
        Feature('feat_2', 'Mobile App', Priority.P1, FeatureStatus.IDEA, 34),
        Feature('feat_3', 'Dark Mode', Priority.P2, FeatureStatus.IDEA, 13)
    ]
    prioritized = roadmap.prioritize_features(features, {'budget': 100})
    print(f"\nPrioritized features: {len(prioritized)}")
    for f in prioritized[:2]:
        print(f"  {f['feature']}: Score={f['score']}, Impact/Effort={f['impact']:.2f}")
    
    roadmap_view = roadmap.generate_roadmap_view([])
    print(f"\nTimeline: {len(roadmap_view['timeline'])} quarters")
    print(f"Key milestones: {len(roadmap_view['key_milestones'])}")
    
    analytics = ProductAnalytics()
    metrics = analytics.analyze_product_metrics()
    print(f"\nMRR: ${metrics['revenue']['mrr']:,}")
    print(f"ARR: ${metrics['revenue']['arr']:,}")
    print(f"Customer satisfaction: {metrics['retention']['churn_rate']}% churn")
    print(f"D30 retention: {metrics['retention']['d30_retention']}%")
    
    health = analytics.generate_product_health_score()
    print(f"\nOverall health score: {health['overall_score']}/100")
    print(f"Status: {health['health_status']}")
