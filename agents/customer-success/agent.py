"""
Customer Success Agent
Customer lifecycle and retention management
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class HealthStatus(Enum):
    HEALTHY = "healthy"
    AT_RISK = "at_risk"
    CRITICAL = "critical"
    CHURNED = "churned"


class EngagementLevel(Enum):
    POWER_USER = "power_user"
    ACTIVE = "active"
    MODERATE = "moderate"
    LOW = "low"
    DORMANT = "dormant"


@dataclass
class Customer:
    customer_id: str
    company: str
    arr: float
    health: HealthStatus
    engagement: EngagementLevel


class CustomerHealthManager:
    """Customer health management"""
    
    def __init__(self):
        self.customers = {}
    
    def assess_health(self, customer_id: str) -> Dict:
        """Assess customer health"""
        return {
            'customer_id': customer_id,
            'overall_health': HealthStatus.AT_RISK,
            'health_score': 62,
            'dimensions': {
                'product_usage': {'score': 70, 'trend': 'stable'},
                'support_tickets': {'score': 55, 'trend': 'declining'},
                'engagement': {'score': 65, 'trend': 'declining'},
                'payment_history': {'score': 90, 'trend': 'stable'},
                'relationship': {'score': 50, 'trend': 'stable'}
            },
            'risk_indicators': [
                {'indicator': 'Decreased login frequency', 'impact': 'medium'},
                {'indicator': 'Support ticket increase', 'impact': 'high'},
                {'indicator': 'Champion leaving', 'impact': 'high'}
            ],
            'recommendations': [
                'Schedule executive check-in',
                'Address support concerns',
                'Identify new champion'
            ]
        }
    
    def monitor_health_scores(self) -> Dict:
        """Monitor all customer health scores"""
        return {
            'total_customers': 100,
            'health_distribution': {
                'healthy': 60,
                'at_risk': 30,
                'critical': 8,
                'churned': 2
            },
            'avg_health_score': 72,
            'trending_down': [
                {'customer_id': 'cust_001', 'reason': 'Support spike'},
                {'customer_id': 'cust_002', 'reason': 'Usage decline'}
            ],
            'churn_risk': {
                'high_risk': 8,
                'medium_risk': 15,
                'low_risk': 77
            },
            'alerts': [
                {'customer': 'Acme Corp', 'alert': 'Health dropped below 60'}
            ]
        }


class OnboardingManager:
    """Customer onboarding"""
    
    def __init__(self):
        self.onboarding_progress = {}
    
    def create_onboarding_plan(self, 
                               customer_id: str,
                               product: str,
                               goals: List[str]) -> Dict:
        """Create onboarding plan"""
        return {
            'customer_id': customer_id,
            'product': product,
            'plan': {
                'week_1': {
                    'focus': 'Foundation',
                    'tasks': [
                        {'task': 'Account setup', 'status': 'pending'},
                        {'task': 'Core features training', 'status': 'pending'},
                        {'task': 'First value demonstration', 'status': 'pending'}
                    ],
                    'success_criteria': ['Account configured', 'Training completed']
                },
                'week_2': {
                    'focus': 'Adoption',
                    'tasks': [
                        {'task': 'Advanced features', 'status': 'pending'},
                        {'task': 'Integration setup', 'status': 'pending'},
                        {'task': 'Team training', 'status': 'pending'}
                    ],
                    'success_criteria': ['Core workflows established']
                },
                'week_3_4': {
                    'focus': 'Optimization',
                    'tasks': [
                        {'task': 'Best practices review', 'status': 'pending'},
                        {'task': 'Advanced use cases', 'status': 'pending'},
                        {'task': 'ROI review', 'status': 'pending'}
                    ],
                    'success_criteria': ['ROI documented', 'Long-term success plan']
                }
            },
            'timeline': '4 weeks',
            'csr_assigned': 'John Smith'
        }
    
    def track_onboarding_progress(self, customer_id: str) -> Dict:
        """Track onboarding progress"""
        return {
            'customer_id': customer_id,
            'start_date': '2024-01-01',
            'current_week': 2,
            'progress': 50,
            'completed_tasks': [
                'Account setup',
                'Core features training',
                'First value demonstration'
            ],
            'upcoming_tasks': [
                'Advanced features',
                'Integration setup'
            ],
            'health_indicators': {
                'engagement': 'on_track',
                'training_completion': 80,
                'adoption_metrics': 60
            },
            'blockers': [],
            'next_milestone': 'Week 2 review'
        }


class RetentionManager:
    """Customer retention management"""
    
    def __init__(self):
        self.retention_campaigns = {}
    
    def identify_churn_risk(self) -> Dict:
        """Identify customers at risk of churning"""
        return {
            'high_risk_customers': [
                {
                    'customer_id': 'cust_001',
                    'company': 'Acme Corp',
                    'arr': 50000,
                    'risk_score': 85,
                    'churn_indicators': [
                        'Usage declined 40%',
                        'Support tickets increased',
                        'Champion departed'
                    ],
                    'retention_priority': 'immediate'
                },
                {
                    'customer_id': 'cust_002',
                    'company': 'TechStart',
                    'arr': 15000,
                    'risk_score': 72,
                    'churn_indicators': [
                        'Payment delays',
                        'Low engagement'
                    ],
                    'retention_priority': 'high'
                }
            ],
            'total_arr_at_risk': 65000,
            'churn_prediction_model': {
                'accuracy': 85,
                'key_factors': ['Usage decline', 'Support sentiment', 'Payment history']
            }
        }
    
    def create_retention_campaign(self, 
                                  customer_id: str,
                                  strategy: str) -> Dict:
        """Create retention campaign"""
        return {
            'campaign_id': f"ret_{datetime.now().strftime('%Y%m%d')}",
            'customer_id': customer_id,
            'strategy': strategy,
            'tactics': [
                {'tactic': 'Executive outreach', 'owner': 'CS Director', 'timing': 'immediate'},
                {'tactic': 'Special pricing offer', 'owner': 'Account Executive', 'timing': 'within week'},
                {'tactic': 'Enhanced support', 'owner': 'Support Lead', 'timing': 'immediate'},
                {'tactic': 'Feature deep-dive', 'owner': 'CSM', 'timing': 'within 2 weeks'}
            ],
            'success_metrics': [
                'Health score improvement > 20%',
                'Contract renewal',
                'Engagement increase'
            ]
        }
    
    def calculate_retention_metrics(self) -> Dict:
        """Calculate retention metrics"""
        return {
            'gross_revenue_retention': 92,
            'net_revenue_retention': 108,
            'logo_retention': 88,
            'avg_lifetime_value': 50000,
            'avg_customer_lifetime': '3.5 years',
            'churn_rate': 8,
            'expansion_revenue': 150000,
            'downgrade_revenue': 30000,
            'factors_affecting_retention': [
                {'factor': 'Product value', 'impact': 'positive'},
                {'factor': 'Customer support', 'impact': 'positive'},
                {'factor': 'Pricing', 'impact': 'neutral'},
                {'factor': 'Competition', 'impact': 'negative'}
            ]
        }


class AccountManager:
    """Account management"""
    
    def __init__(self):
        self.accounts = {}
    
    def manage_account(self, account_id: str) -> Dict:
        """Manage customer account"""
        return {
            'account_id': account_id,
            'company': 'Enterprise Corp',
            'industry': 'Technology',
            'arr': 100000,
            'tier': 'Enterprise',
            'health': HealthStatus.HEALTHY,
            'contacts': [
                {'name': 'Jane Doe', 'role': 'Champion', 'engagement': 'high'},
                {'name': 'John Smith', 'role': 'Technical', 'engagement': 'medium'}
            ],
            'usage_summary': {
                'seats_used': 50,
                'features_adopted': 8,
                'integrations': 3
            },
            'success_plan': [
                {'goal': 'Expand to new department', 'timeline': 'Q2', 'owner': 'CSM'},
                {'goal': 'Renew with 20% growth', 'timeline': 'Q3', 'owner': 'AE'}
            ],
            'opportunities': [
                {'type': 'upsell', 'value': 50000, 'product': 'Enterprise+'},
                {'type': 'cross_sell', 'value': 15000, 'product': 'Analytics add-on'}
            ],
            'engagement_activities': [
                {'type': 'QBR', 'date': '2024-03-15'},
                {'type': 'Training session', 'date': '2024-02-01'}
            ]
        }
    
    def plan_qbr(self, account_id: str) -> Dict:
        """Plan Quarterly Business Review"""
        return {
            'account_id': account_id,
            'qbr_date': '2024-03-15',
            'agenda': [
                {'topic': 'Executive summary', 'duration': '10 min'},
                {'topic': 'Usage highlights', 'duration': '15 min'},
                {'topic': 'Value delivered', 'duration': '15 min'},
                {'topic': 'Future roadmap', 'duration': '15 min'},
                {'topic': 'Expansion opportunities', 'duration': '10 min'},
                {'topic': 'Q&A', 'duration': '5 min'}
            ],
            'materials': [
                'Executive summary deck',
                'ROI analysis',
                'Usage report',
                'Competitive comparison'
            ],
            'attendees': [
                {'name': 'Customer Champion', 'role': 'VP Engineering'},
                {'name': 'Customer Executive', 'role': 'CTO'},
                {'name': 'CSM', 'role': 'Internal'},
                {'name': 'AE', 'role': 'Internal'}
            ],
            'success_metrics': [
                'Renewal commitment',
                'Expansion interest',
                'NPS improvement'
            ]
        }


class CSAnalytics:
    """Customer Success analytics"""
    
    def __init__(self):
        self.reports = {}
    
    def generate_cs_report(self) -> Dict:
        """Generate Customer Success report"""
        return {
            'period': 'Q1 2024',
            'portfolio_summary': {
                'total_customers': 100,
                'total_arr': 5000000,
                'avg_arr': 50000
            },
            'health_metrics': {
                'healthy': 60,
                'at_risk': 30,
                'critical': 8,
                'churned': 2
            },
            'engagement_metrics': {
                'avg_engagement_score': 72,
                'power_users': 20,
                'active_users': 50,
                'dormant_users': 10
            },
            'retention_metrics': {
                'gross_retention': 92,
                'net_retention': 108,
                'churn_rate': 8
            },
            'expansion_metrics': {
                'expansion_revenue': 500000,
                'upsell_rate': 25,
                'cross_sell_rate': 15
            },
            'nps_metrics': {
                'current_nps': 42,
                'promoters': 50,
                'passives': 35,
                'detractors': 15,
                'trending': 'up'
            },
            'cs_team_performance': {
                'accounts_per_csm': 15,
                'avg_response_time': '2 hours',
                'qbr_completion_rate': 95,
                'customer_satisfaction': 4.3
            },
            'recommendations': [
                'Increase QBR frequency for at-risk accounts',
                'Implement automated health alerts',
                'Develop customer education program'
            ]
        }


if __name__ == "__main__":
    health_mgr = CustomerHealthManager()
    
    health = health_mgr.assess_health('cust_001')
    print(f"Health status: {health['overall_health'].value}")
    print(f"Health score: {health['health_score']}")
    print(f"Risk indicators: {len(health['risk_indicators'])}")
    
    monitoring = health_mgr.monitor_health_scores()
    print(f"\nTotal customers: {monitoring['total_customers']}")
    print(f"Healthy: {monitoring['health_distribution']['healthy']}")
    print(f"At risk: {monitoring['health_distribution']['at_risk']}")
    
    onboarding = OnboardingManager()
    plan = onboarding.create_onboarding_plan(
        'cust_new',
        'Analytics Platform',
        ['Adoption', 'Integration', 'ROI']
    )
    print(f"\nOnboarding plan: {plan['timeline']}")
    print(f"CSM assigned: {plan['csr_assigned']}")
    
    retention = RetentionManager()
    at_risk = retention.identify_churn_risk()
    print(f"\nHigh risk customers: {len(at_risk['high_risk_customers'])}")
    print(f"ARR at risk: ${at_risk['total_arr_at_risk']:,}")
    
    retention_metrics = retention.calculate_retention_metrics()
    print(f"GRR: {retention_metrics['gross_revenue_retention']}%")
    print(f"NRR: {retention_metrics['net_revenue_retention']}%")
    print(f"Churn rate: {retention_metrics['churn_rate']}%")
    
    cs_report = CSAnalytics()
    report = cs_report.generate_cs_report()
    print(f"\nPortfolio ARR: ${report['portfolio_summary']['total_arr']:,}")
    print(f"NPS: {report['nps_metrics']['current_nps']}")
    print(f"Net Retention: {report['retention_metrics']['net_retention']}%")
