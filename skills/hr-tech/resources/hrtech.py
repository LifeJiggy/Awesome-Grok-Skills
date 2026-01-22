#!/usr/bin/env python3
"""
HRTech - Human Resources Technology Implementation
Talent management, workforce analytics, and employee experience.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
import random

class JobType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    REMOTE = "remote"

class CandidateStatus(Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    HIRED = "hired"
    REJECTED = "rejected"

class EmployeeStatus(Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    PROBATION = "probation"

@dataclass
class JobPosting:
    id: str
    title: str
    department: str
    location: str
    job_type: JobType
    requirements: List[str]
    salary_range: Dict[str, float]
    status: str

@dataclass
class Candidate:
    id: str
    name: str
    email: str
    skills: List[str]
    experience_years: int
    status: CandidateStatus
    match_score: float

@dataclass
class Employee:
    id: str
    name: str
    department: str
    position: str
    hire_date: datetime
    manager: str
    status: EmployeeStatus
    performance_score: float

class TalentAcquisitionEngine:
    """AI-powered recruitment."""
    
    def __init__(self):
        self.candidates: Dict[str, Candidate] = {}
        self.job_postings: Dict[str, JobPosting] = {}
    
    def post_job(self, title: str, department: str,
                location: str, job_type: JobType) -> JobPosting:
        """Create job posting."""
        posting = JobPosting(
            id=f"JOB_{len(self.job_postings) + 1}",
            title=title,
            department=department,
            location=location,
            job_type=job_type,
            requirements=self._get_default_requirements(title),
            salary_range={'min': 50000, 'max': 100000},
            status='active'
        )
        self.job_postings[posting.id] = posting
        return posting
    
    def _get_default_requirements(self, title: str) -> List[str]:
        """Get default job requirements."""
        return [
            'Bachelor degree or equivalent',
            '3+ years experience',
            'Strong communication skills',
            'Team collaboration ability'
        ]
    
    def screen_candidates(self, job_id: str,
                         candidate_data: List[Dict]) -> List[Candidate]:
        """AI screen and match candidates."""
        job = self.job_postings.get(job_id)
        if not job:
            return []
        
        screened = []
        for data in candidate_data:
            candidate = Candidate(
                id=f"CAND_{len(self.candidates) + 1}",
                name=data['name'],
                email=data['email'],
                skills=data.get('skills', []),
                experience_years=data.get('experience', 0),
                status=CandidateStatus.APPLIED,
                match_score=random.uniform(60, 98)
            )
            self.candidates[candidate.id] = candidate
            screened.append(candidate)
        
        return sorted(screened, key=lambda c: c.match_score, reverse=True)
    
    def schedule_interview(self, candidate_id: str,
                          interviewers: List[str]) -> Dict[str, Any]:
        """Schedule interview."""
        return {
            'candidate_id': candidate_id,
            'interview_type': 'technical',
            'duration_minutes': 45,
            'scheduled_time': (datetime.now() + timedelta(days=random.randint(1, 7))).isoformat(),
            'interviewers': interviewers,
            'meeting_link': 'https://meet.hrtech.app/interview/123',
            'preparation_materials': ['Job description', 'Resume', 'Technical test']
        }

class EmployeeManagementSystem:
    """Manages employee lifecycle."""
    
    def __init__(self):
        self.employees: Dict[str, Employee] = {}
        self.leave_requests: List[Dict] = []
    
    def onboard_employee(self, name: str, department: str,
                        position: str, manager: str) -> Employee:
        """Onboard new employee."""
        employee = Employee(
            id=f"EMP_{len(self.employees) + 1}",
            name=name,
            department=department,
            position=position,
            hire_date=datetime.now(),
            manager=manager,
            status=EmployeeStatus.PROBATION,
            performance_score=0.0
        )
        self.employees[employee.id] = employee
        return employee
    
    def request_leave(self, employee_id: str,
                     leave_type: str, days: int) -> Dict[str, Any]:
        """Submit leave request."""
        request = {
            'request_id': f"LR_{random.randint(1000, 9999)}",
            'employee_id': employee_id,
            'type': leave_type,
            'duration_days': days,
            'status': 'pending',
            'submission_date': datetime.now().isoformat()
        }
        self.leave_requests.append(request)
        return request
    
    def process_leave(self, request_id: str, approved: bool) -> Dict[str, Any]:
        """Process leave request."""
        for request in self.leave_requests:
            if request['request_id'] == request_id:
                request['status'] = 'approved' if approved else 'denied'
                request['processed_date'] = datetime.now().isoformat()
                return request
        return {'error': 'Request not found'}
    
    def calculate_tenure(self, employee_id: str) -> Dict[str, Any]:
        """Calculate employee tenure."""
        employee = self.employees.get(employee_id)
        if not employee:
            return {'error': 'Employee not found'}
        
        days_employed = (datetime.now() - employee.hire_date).days
        years = days_employed / 365
        
        return {
            'employee_id': employee_id,
            'hire_date': employee.hire_date.isoformat(),
            'years_employed': round(years, 1),
            'tenure_category': 'senior' if years > 5 else 'mid' if years > 2 else 'junior',
            'benefits_eligible': years >= 1
        }

class WorkforceAnalytics:
    """Comprehensive workforce analytics."""
    
    def __init__(self):
        self.reports: List[Dict] = []
    
    def generate_analytics_report(self) -> Dict[str, Any]:
        """Generate workforce analytics report."""
        return {
            'headcount': {
                'total': random.randint(500, 2000),
                'by_department': {
                    'Engineering': random.randint(100, 400),
                    'Sales': random.randint(50, 200),
                    'Marketing': random.randint(30, 100),
                    'Operations': random.randint(80, 300)
                },
                'growth_rate': round(random.uniform(-5, 15), 1)
            },
            'attrition': {
                'rate': round(random.uniform(5, 20), 1),
                'voluntary_vs_involuntary': '80/20',
                'top_reasons': ['Career growth', 'Compensation', 'Work-life balance']
            },
            'engagement': {
                'score': round(random.uniform(60, 85), 1),
                'survey_response_rate': round(random.uniform(70, 90), 1),
                'satisfaction_trend': 'improving'
            },
            'diversity': {
                'gender_ratio': '45/55',
                'ethnicity_diversity': round(random.uniform(30, 50), 1),
                'inclusion_score': round(random.uniform(65, 85), 1)
            },
            'compensation': {
                'avg_salary': round(random.uniform(60000, 120000), 0),
                'budget_utilization': round(random.uniform(85, 105), 1)
            }
        }
    
    def predict_attrition(self) -> Dict[str, Any]:
        """Predict employee attrition risk."""
        at_risk = random.randint(10, 50)
        
        return {
            'prediction_model': 'Random Forest',
            'at_risk_employees': at_risk,
            'risk_factors': [
                'No promotion in 3+ years',
                'Manager change',
                'Compensation below market',
                'Low engagement scores'
            ],
            'retention_recommendations': [
                'Proactive career discussion',
                'Market-based salary adjustment',
                'Mentorship program',
                'Flexible work options'
            ],
            'estimated_cost_of_turnover': round(random.uniform(50000, 200000), 0)
        }
    
    def analyze_skills_gaps(self) -> Dict[str, Any]:
        """Analyze organizational skills gaps."""
        return {
            'critical_skills': [
                {'skill': 'Cloud Architecture', 'demand': 85, 'supply': 60},
                {'skill': 'Data Science', 'demand': 90, 'supply': 55},
                {'skill': 'AI/ML', 'demand': 80, 'supply': 45}
            ],
            'gap_severity': {
                'critical': 3,
                'high': 5,
                'medium': 8
            },
            'training_recommendations': [
                'Cloud certification program',
                'Data literacy training',
                'Leadership development'
            ],
            'hiring_priorities': [
                'Senior Engineers',
                'Product Managers',
                'UX Designers'
            ]
        }

class PerformanceManagementSystem:
    """Manages performance reviews."""
    
    def __init__(self):
        self.reviews: List[Dict] = []
    
    def create_review_cycle(self, name: str,
                           duration_weeks: int) -> Dict[str, Any]:
        """Create performance review cycle."""
        return {
            'cycle_id': f"REV_{random.randint(1000, 9999)}",
            'name': name,
            'start_date': datetime.now().isoformat(),
            'duration_weeks': duration_weeks,
            'phases': [
                {'phase': 'Self-assessment', 'week': 1},
                {'phase': 'Manager review', 'week': 2},
                {'phase': 'Calibration', 'week': 3},
                {'phase': 'Finalization', 'week': 4}
            ],
            'participants': random.randint(100, 1000),
            'completion_rate': 0
        }
    
    def conduct_review(self, employee_id: str,
                      reviewer: str) -> Dict[str, Any]:
        """Conduct performance review."""
        scores = {
            'performance': round(random.uniform(3, 5), 1),
            'goals': round(random.uniform(2.5, 5), 1),
            'skills': round(random.uniform(3, 5), 1),
            'potential': round(random.uniform(3, 5), 1)
        }
        
        avg_score = sum(scores.values()) / len(scores)
        
        review = {
            'review_id': f"REV_{random.randint(1000, 9999)}",
            'employee_id': employee_id,
            'reviewer': reviewer,
            'period': 'Q4 2024',
            'scores': scores,
            'overall_rating': round(avg_score, 1),
            'rating_label': 'Exceeds' if avg_score >= 4.5 else 'Meets' if avg_score >= 3.5 else 'Developing',
            'strengths': ['Technical skills', 'Team collaboration'],
            'improvement_areas': ['Communication', 'Strategic thinking'],
            'recommendations': [
                'Consider for promotion',
                'Assign mentor',
                'Leadership training'
            ]
        }
        self.reviews.append(review)
        return review
    
    def calibrate_reviews(self, department: str) -> Dict[str, Any]:
        """Calibrate review scores."""
        return {
            'department': department,
            'reviews_calibrated': random.randint(20, 100),
            'adjustments': {
                'upward': random.randint(5, 20),
                'downward': random.randint(3, 15),
                'no_change': random.randint(50, 150)
            },
            'calibration_score': round(random.uniform(3.5, 4.2), 2),
            'distribution': {
                'exceeds_expectations': round(random.uniform(10, 25), 1),
                'meets_expectations': round(random.uniform(55, 70), 1),
                'needs_improvement': round(random.uniform(5, 15), 1)
            }
        }

class HRTechAgent:
    """Main HRTech agent."""
    
    def __init__(self):
        self.talent = TalentAcquisitionEngine()
        self.employees = EmployeeManagementSystem()
        self.analytics = WorkforceAnalytics()
        self.performance = PerformanceManagementSystem()
    
    def create_hire_package(self, job_title: str,
                           department: str,
                           location: str) -> Dict[str, Any]:
        """Create complete hiring package."""
        job = self.talent.post_job(job_title, department, location, JobType.FULL_TIME)
        
        candidates = self.talent.screen_candidates(job.id, [
            {'name': 'Candidate A', 'email': 'a@example.com', 'skills': ['Python', 'SQL'], 'experience': 5},
            {'name': 'Candidate B', 'email': 'b@example.com', 'skills': ['Java', 'Cloud'], 'experience': 7}
        ])
        
        return {
            'job_posting': {
                'id': job.id,
                'title': job.title,
                'department': job.department
            },
            'top_candidates': [
                {'name': c.name, 'match_score': c.match_score}
                for c in candidates[:3]
            ],
            'salary_benchmark': {
                'min': job.salary_range['min'],
                'max': job.salary_range['max'],
                'market_percentile': random.randint(50, 90)
            },
            'time_to_hire_estimate': f"{random.randint(3, 8)} weeks"
        }
    
    def get_hr_dashboard(self) -> Dict[str, Any]:
        """Get HR technology dashboard."""
        return {
            'talent': {
                'open_positions': len(self.talent.job_postings),
                'active_candidates': len(self.talent.candidates)
            },
            'employees': {
                'total': len(self.employees.employees),
                'on_leave': len(self.employees.leave_requests)
            },
            'analytics': {
                'reports_generated': len(self.analytics.reports)
            },
            'performance': {
                'reviews_completed': len(self.performance.reviews)
            }
        }

def main():
    """Main entry point."""
    agent = HRTechAgent()
    
    package = agent.create_hire_package(
        'Senior Engineer',
        'Engineering',
        'Remote'
    )
    print(f"Hire package: {package}")

if __name__ == "__main__":
    main()
