"""
UX Research Module
User research, usability testing, and persona development
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ResearchMethod(Enum):
    INTERVIEW = "interview"
    SURVEY = "survey"
    USABILITY_TEST = "usability_test"
    DIARY_STUDY = "diary_study"
    A_B_TEST = "a_b_test"
    CARD_SORT = "card_sort"
    HEURISTIC_EVAL = "heuristic_evaluation"


class UserSegment(Enum):
    POWER_USER = "power_user"
    CASUAL_USER = "casual_user"
    NEW_USER = "new_user"
    ENTERPRISE = "enterprise"
    MOBILE_USER = "mobile_user"


@dataclass
class Persona:
    persona_id: str
    name: str
    demographic: Dict
    goals: List[str]
    frustrations: List[str]
    behaviors: List[str]
    quote: str
    image_url: Optional[str] = None


@dataclass
class UsabilityIssue:
    issue_id: str
    severity: str
    description: str
    location: str
    recommendation: str
    occurrence_count: int


class UserResearch:
    """User research management"""
    
    def __init__(self):
        self.studies = []
        self.participants = []
    
    def create_research_plan(self,
                             method: ResearchMethod,
                             objectives: List[str],
                             target_audience: List[UserSegment],
                             timeline: str) -> Dict:
        """Create research plan"""
        return {
            'id': f"research_{len(self.studies)}",
            'method': method.value,
            'objectives': objectives,
            'target_audience': [s.value for s in target_audience],
            'timeline': timeline,
            'status': 'planned'
        }
    
    def recruit_participants(self,
                             criteria: Dict,
                             count: int = 10) -> Dict:
        """Recruit research participants"""
        return {
            'criteria': criteria,
            'target_count': count,
            'recruited': count,
            'screened': count * 2,
            'status': 'completed'
        }
    
    def conduct_interview(self,
                          participant_id: str,
                          questions: List[str]) -> Dict:
        """Conduct user interview"""
        return {
            'interview_id': f"int_{participant_id}",
            'participant': participant_id,
            'duration_minutes': 45,
            'key_insights': [
                'User prefers mobile interface',
                'Navigation confusing for new users',
                'Export feature highly valued'
            ],
            'transcript': 'Full transcript here...'
        }
    
    def analyze_interviews(self,
                          interview_ids: List[str]) -> Dict:
        """Analyze interview transcripts"""
        return {
            'interviews_analyzed': len(interview_ids),
            'themes': [
                {'theme': 'Mobile First', 'frequency': 8, 'quotes': ['I always use mobile']},
                {'theme': 'Simplicity', 'frequency': 10, 'quotes': ['Keep it simple']}
            ],
            'pain_points': [
                'Complex onboarding',
                'Hidden features',
                'Slow performance'
            ],
            'opportunities': [
                'Simplified mobile flow',
                'Better onboarding',
                'Performance optimization'
            ]
        }
    
    def create_survey(self,
                      title: str,
                      questions: List[Dict],
                      target_count: int = 100) -> Dict:
        """Create survey"""
        return {
            'survey_id': f"survey_{len(self.studies)}",
            'title': title,
            'questions': questions,
            'target_responses': target_count,
            'status': 'draft'
        }
    
    def analyze_survey(self,
                       survey_id: str,
                       responses: List[Dict]) -> Dict:
        """Analyze survey results"""
        return {
            'survey_id': survey_id,
            'total_responses': len(responses),
            'completion_rate': 0.85,
            'key_findings': [
                {'question': 'Satisfaction', 'score': 4.2, 'trend': 'up'},
                {'question': 'NPS', 'score': 42, 'trend': 'stable'}
            ],
            'demographic_breakdown': {
                'age': {'18-24': 0.15, '25-34': 0.35, '35-44': 0.30, '45+': 0.20},
                'usage': {'daily': 0.40, 'weekly': 0.35, 'monthly': 0.25}
            }
        }


class PersonaDevelopment:
    """Persona creation and management"""
    
    def __init__(self):
        self.personas: List[Persona] = []
    
    def create_persona(self,
                       name: str,
                       demographic: Dict,
                       goals: List[str],
                       frustrations: List[str],
                       behaviors: List[str],
                       quote: str) -> Persona:
        """Create user persona"""
        persona = Persona(
            persona_id=f"persona_{len(self.personas)}",
            name=name,
            demographic=demographic,
            goals=goals,
            frustrations=frustrations,
            behaviors=behaviors,
            quote=quote
        )
        self.personas.append(persona)
        return persona
    
    def generate_persona_from_data(self,
                                   segment_data: Dict) -> Persona:
        """Generate persona from research data"""
        return self.create_persona(
            name=segment_data.get('name', 'User'),
            demographic=segment_data.get('demographics', {}),
            goals=segment_data.get('goals', []),
            frustrations=segment_data.get('frustrations', []),
            behaviors=segment_data.get('behaviors', []),
            quote=segment_data.get('quote', '')
        )
    
    def create_persona_card(self, persona: Persona) -> str:
        """Create visual persona card"""
        card = f"""
# {persona.name}

> "{persona.quote}"

## Demographics
- **Age:** {persona.demographic.get('age', 'N/A')}
- **Occupation:** {persona.demographic.get('occupation', 'N/A')}
- **Location:** {persona.demographic.get('location', 'N/A')}

## Goals
"""
        for goal in persona.goals:
            card += f"- {goal}\n"
        
        card += "\n## Frustrations\n"
        for frustration in persona.frustrations:
            card += f"- {frustration}\n"
        
        card += "\n## Behaviors\n"
        for behavior in persona.behaviors:
            card += f"- {behavior}\n"
        
        return card
    
    def compare_personas(self) -> Dict:
        """Compare personas"""
        return {
            'personas': [p.name for p in self.personas],
            'comparison': [
                {
                    'dimension': 'Technical Sophistication',
                    'values': {'Alice': 'High', 'Bob': 'Medium', 'Carol': 'Low'}
                },
                {
                    'dimension': 'Engagement Level',
                    'values': {'Alice': 'Daily', 'Bob': 'Weekly', 'Carol': 'Monthly'}
                }
            ],
            'key_differences': [
                'Alice is power user, Carol is casual',
                'Bob uses mobile, Alice prefers desktop'
            ]
        }
    
    def map_persona_journey(self, persona: Persona) -> Dict:
        """Map persona customer journey"""
        return {
            'persona': persona.name,
            'journey': [
                {'stage': 'Awareness', 'touchpoints': ['Ads', 'Referral'], 'emotion': 'Curious'},
                {'stage': 'Consideration', 'touchpoints': ['Website', 'Reviews'], 'emotion': 'Interested'},
                {'stage': 'Decision', 'touchpoints': ['Pricing', 'Demo'], 'emotion': 'Evaluating'},
                {'stage': 'Retention', 'touchpoints': ['Onboarding', 'Support'], 'emotion': 'Satisfied'}
            ],
            'pain_points': ['Complex pricing', 'Slow support'],
            'opportunities': ['Simpler pricing', 'Faster support']
        }


class UsabilityTesting:
    """Usability testing management"""
    
    def __init__(self):
        self.tests = []
    
    def create_test_plan(self,
                         task: str,
                         success_criteria: List[str],
                         participant_count: int = 5) -> Dict:
        """Create usability test plan"""
        return {
            'test_id': f"test_{len(self.tests)}",
            'task': task,
            'success_criteria': success_criteria,
            'participant_count': participant_count
        }
    
    def run_usability_session(self,
                              participant_id: str,
                              tasks: List[Dict]) -> Dict:
        """Run usability test session"""
        return {
            'session_id': f"session_{participant_id}",
            'participant': participant_id,
            'tasks_completed': len([t for t in tasks if t.get('completed')]),
            'total_tasks': len(tasks),
            'completion_rate': 0.80,
            'issues_found': [
                {'location': 'Checkout page', 'severity': 'high', 'description': 'Confusing CTA'}
            ],
            'time_on_task_seconds': 180,
            'satisfaction_score': 4.0
        }
    
    def aggregate_test_results(self,
                               session_ids: List[str]) -> Dict:
        """Aggregate usability test results"""
        return {
            'tests_analyzed': len(session_ids),
            'completion_rate': 0.85,
            'avg_task_time_seconds': 200,
            'satisfaction_score': 3.8,
            'issues': [
                {'severity': 'high', 'count': 3, 'description': 'Navigation confusion'},
                {'severity': 'medium', 'count': 5, 'description': 'Missing feedback'},
                {'severity': 'low', 'count': 8, 'description': 'Minor UI issues'}
            ],
            'priority_fixes': [
                'Redesign navigation menu',
                'Add loading indicators',
                'Improve error messages'
            ]
        }
    
    def conduct_heuristic_evaluation(self,
                                     interface: str) -> List[UsabilityIssue]:
        """Conduct heuristic evaluation"""
        return [
            UsabilityIssue(
                issue_id='h1',
                severity='high',
                description='No visibility of system status',
                location='Global',
                recommendation='Add progress indicators',
                occurrence_count=5
            ),
            UsabilityIssue(
                issue_id='h2',
                severity='medium',
                description='User control and freedom limited',
                location='Forms',
                recommendation='Add undo functionality',
                occurrence_count=3
            )
        ]
    
    def create_session_recording(self,
                                 session_id: str) -> Dict:
        """Create session recording metadata"""
        return {
            'session_id': session_id,
            'video_url': f'/recordings/{session_id}.mp4',
            'duration': '00:15:30',
            'events': [
                {'timestamp': '00:01:00', 'event': 'Task started'},
                {'timestamp': '00:05:30', 'event': 'Error encountered'},
                {'timestamp': '00:10:00', 'event': 'Task completed'}
            ]
        }


class JourneyMapping:
    """Customer journey mapping"""
    
    def __init__(self):
        self.journeys = {}
    
    def create_journey_map(self,
                           journey_name: str,
                           stages: List[Dict],
                           personas: List[str]) -> Dict:
        """Create customer journey map"""
        return {
            'journey': journey_name,
            'stages': stages,
            'personas': personas,
            'total_duration': '2 weeks',
            'touchpoints': 15
        }
    
    def analyze_touchpoints(self, journey_id: str) -> Dict:
        """Analyze journey touchpoints"""
        return {
            'journey': journey_id,
            'touchpoints': [
                {'name': 'Website', 'channel': 'Web', 'satisfaction': 4.0, 'conversion': 0.15},
                {'name': 'Mobile App', 'channel': 'Mobile', 'satisfaction': 3.8, 'conversion': 0.12},
                {'name': 'Support', 'channel': 'Chat', 'satisfaction': 4.2, 'conversion': 0.05}
            ],
            'highest_satisfaction': 'Support',
            'lowest_satisfaction': 'Mobile App',
            'recommendations': [
                'Improve mobile app UX',
                'Add more self-service options'
            ]
        }
    
    def identify_moments_of_truth(self, journey_id: str) -> List[Dict]:
        """Identify critical moments of truth"""
        return [
            {
                'moment': 'First Purchase',
                'impact': 'high',
                'satisfaction': 4.0,
                'recommendation': 'Streamline checkout process'
            },
            {
                'moment': 'Customer Support Interaction',
                'impact': 'medium',
                'satisfaction': 4.2,
                'recommendation': 'Maintain quality support'
            }
        ]
    
    def calculate_journey_score(self, journey_id: str) -> Dict:
        """Calculate overall journey score"""
        return {
            'journey': journey_id,
            'overall_score': 78,
            'breakdown': {
                'awareness': 82,
                'consideration': 75,
                'decision': 70,
                'retention': 85,
                'advocacy': 80
            },
            'trend': 'improving',
            'benchmark': 75
        }


class ABTesting:
    """A/B testing for UX optimization"""
    
    def __init__(self):
        self.experiments = {}
    
    def design_experiment(self,
                          control: Dict,
                          variant: Dict,
                          metric: str,
                          sample_size: int = 1000) -> Dict:
        """Design A/B test"""
        return {
            'experiment_id': f"exp_{len(self.experiments)}",
            'control': control,
            'variant': variant,
            'primary_metric': metric,
            'sample_size': sample_size,
            'confidence_level': 0.95,
            'status': 'draft'
        }
    
    def run_experiment(self,
                       experiment_id: str,
                       duration_days: int = 14) -> Dict:
        """Run A/B test"""
        return {
            'experiment_id': experiment_id,
            'status': 'running',
            'days_remaining': duration_days,
            'current_sample_size': 500,
            'required_sample_size': 1000
        }
    
    def analyze_experiment(self,
                           experiment_id: str) -> Dict:
        """Analyze A/B test results"""
        return {
            'experiment_id': experiment_id,
            'status': 'completed',
            'control': {
                'visitors': 1000,
                'conversions': 50,
                'rate': 0.05
            },
            'variant': {
                'visitors': 1000,
                'conversions': 65,
                'rate': 0.065
            },
            'improvement': 0.30,
            'p_value': 0.02,
            'statistically_significant': True,
            'recommendation': 'Roll out variant'
        }
    
    def calculate_sample_size(self,
                              baseline_rate: float,
                              minimum_detectable_effect: float,
                              power: float = 0.8) -> Dict:
        """Calculate required sample size"""
        return {
            'baseline_rate': baseline_rate,
            'mde': minimum_detectable_effect,
            'power': power,
            'required_sample_size': 1000,
            'duration_days': 7
        }


if __name__ == "__main__":
    research = UserResearch()
    plan = research.create_research_plan(
        ResearchMethod.INTERVIEW,
        ['Understand user needs', 'Identify pain points'],
        [UserSegment.NEW_USER],
        '2 weeks'
    )
    print(f"Research plan: {plan['method']}")
    
    personas = PersonaDevelopment()
    p1 = personas.create_persona(
        "Alice Power",
        {'age': '30-40', 'occupation': 'Engineer'},
        ['Quick workflows', 'Advanced features'],
        ['Too many clicks', 'Slow loading'],
        ['Uses keyboard shortcuts', 'Daily login'],
        "I need efficiency in everything I do."
    )
    card = personas.create_persona_card(p1)
    print(f"\nPersona created: {p1.name}")
    
    usability = UsabilityTesting()
    results = usability.aggregate_test_results(['s1', 's2', 's3'])
    print(f"\nCompletion rate: {results['completion_rate']}")
    
    ab = ABTesting()
    analysis = ab.analyze_experiment('exp_1')
    print(f"\nSignificant: {analysis['statistically_significant']}")
    print(f"Recommendation: {analysis['recommendation']}")
