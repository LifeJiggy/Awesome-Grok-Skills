from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class QAProcess(Enum):
    REQUIREMENTS_REVIEW = "requirements_review"
    TEST_PLANNING = "test_planning"
    TEST_DESIGN = "test_design"
    TEST_EXECUTION = "test_execution"
    DEFECT_TRACKING = "defect_tracking"
    RELEASE_DECISION = "release_decision"


class DefectPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DefectStatus(Enum):
    NEW = "new"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REOPENED = "reopened"


@dataclass
class TestPlan:
    test_plan_id: str
    name: str
    version: str
    objectives: List[str]
    scope: Dict
    test_strategy: str
    schedule: Dict
    resources: Dict
    risks: List[Dict]
    entry_criteria: List[str]
    exit_criteria: List[str]


@dataclass
class Defect:
    defect_id: str
    title: str
    description: str
    priority: DefectPriority
    status: DefectStatus
    severity: str
    module: str
    test_case_id: str
    steps_to_reproduce: List[str]
    expected_result: str
    actual_result: str
    assigned_to: str
    created_by: str
    created_date: datetime


class QualityAssuranceManager:
    """Manage quality assurance processes"""
    
    def __init__(self):
        self.test_plans = []
        self.defects = []
    
    def create_test_plan(self,
                         name: str,
                         version: str = "1.0") -> TestPlan:
        """Create test plan"""
        return TestPlan(
            test_plan_id=f"TP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=name,
            version=version,
            objectives=["Verify functionality", "Validate performance", "Ensure security"],
            scope={"included": ["User Module", "Payment Module"], "excluded": ["Legacy System"]},
            test_strategy="Hybrid (Manual + Automated)",
            schedule={"start": "2024-02-01", "end": "2024-03-15"},
            resources={"testers": 3, "environments": ["QA", "Staging"]},
            risks=[{"risk": "Resource availability", "mitigation": "Cross-training"}],
            entry_criteria=["Test environment ready", "Test data prepared", "Build available"],
            exit_criteria=["95% test cases executed", "0 critical defects open", "Sign-off obtained"]
        )
    
    def review_requirements(self,
                            requirements: List[Dict]) -> Dict:
        """Review requirements for testability"""
        findings = []
        for req in requirements:
            issues = []
            if not req.get('testable', True):
                issues.append('Non-testable requirement')
            if not req.get('measurable', True):
                issues.append('Non-measurable success criteria')
            if not req.get('complete', True):
                issues.append('Incomplete requirement')
            if issues:
                findings.append({'requirement_id': req.get('id'), 'issues': issues})
        
        return {
            'requirements_reviewed': len(requirements),
            'findings': findings,
            'testability_score': 85 if len(findings) < len(requirements) / 2 else 60,
            'recommendations': ['Add measurable acceptance criteria', 'Break down complex requirements']
        }
    
    def create_test_case(self,
                         test_plan_id: str,
                         test_name: str,
                         module: str,
                         preconditions: List[str],
                         test_steps: List[str],
                         expected_result: str,
                         priority: str = "High") -> Dict:
        """Create test case"""
        return {
            'test_case_id': f"TC-{len(self.test_plans) + 1:04d}",
            'test_plan_id': test_plan_id,
            'title': test_name,
            'module': module,
            'preconditions': preconditions,
            'test_steps': test_steps,
            'expected_result': expected_result,
            'priority': priority,
            'created_date': datetime.now().isoformat(),
            'status': 'Ready',
            'automated': False
        }
    
    def execute_test_cycle(self,
                           test_cases: List[Dict],
                           environment: str = "QA") -> Dict:
        """Execute test cycle"""
        results = {'passed': 0, 'failed': 0, 'blocked': 0, 'skipped': 0, 'not_run': 0}
        defects = []
        
        for tc in test_cases:
            status = tc.get('status', 'Not Run')
            results[status.lower().replace(' ', '_') if status.lower().replace(' ', '_') in results else 'not_run'] += 1
            
            if status == 'Failed':
                defects.append({
                    'test_case': tc['test_case_id'],
                    'failure_reason': 'Assertion failed'
                })
        
        return {
            'cycle_id': f"CYCLE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'environment': environment,
            'total_tests': len(test_cases),
            'results': results,
            'defects_found': len(defects),
            'execution_time_hours': 40,
            'pass_rate': f"{(results['passed']/len(test_cases)*100):.1f}%",
            'defects': defects
        }
    
    def log_defect(self,
                   title: str,
                   description: str,
                   priority: DefectPriority,
                   module: str,
                   test_case_id: str,
                   steps: List[str],
                   expected: str,
                   actual: str) -> Defect:
        """Log defect"""
        defect = Defect(
            defect_id=f"DEF-{len(self.defects) + 1:04d}",
            title=title,
            description=description,
            priority=priority,
            status=DefectStatus.NEW,
            severity='High' if priority == DefectPriority.CRITICAL else 'Medium',
            module=module,
            test_case_id=test_case_id,
            steps_to_reproduce=steps,
            expected_result=expected,
            actual_result=actual,
            assigned_to='',
            created_by='QA Team',
            created_date=datetime.now()
        )
        self.defects.append(defect)
        return defect
    
    def analyze_defect_trends(self) -> Dict:
        """Analyze defect trends"""
        return {
            'total_defects': len(self.defects),
            'by_status': {
                'new': 5,
                'open': 12,
                'in_progress': 8,
                'resolved': 45,
                'closed': 30
            },
            'by_priority': {
                'critical': 3,
                'high': 15,
                'medium': 35,
                'low': 47
            },
            'by_module': {
                'User Module': 25,
                'Payment Module': 30,
                'Reporting': 20,
                'Admin': 25
            },
            'trend': 'decreasing',
            'closure_rate': 85.0,
            'avg_resolution_time_days': 4.5
        }
    
    def calculate_quality_metrics(self,
                                  test_results: Dict,
                                  defect_data: Dict) -> Dict:
        """Calculate quality metrics"""
        total_tests = test_results.get('total_tests', 100)
        passed = test_results.get('results', {}).get('passed', 85)
        
        return {
            'test_effectiveness': (passed / total_tests * 100) if total_tests > 0 else 0,
            'defect_density': len(defect_data.get('by_priority', {}).get('high', 0)) / total_tests * 1000,
            'test_coverage': 85.0,
            'requirements_coverage': 92.0,
            'escape_ratio': 0.15,
            'defect_leakage': 0.05,
            'rework_effort_hours': 25,
            'quality_score': 85 + (passed/total_tests*10) if total_tests > 0 else 85
        }
    
    def perform_release_readiness_review(self,
                                          test_results: Dict,
                                          defect_data: Dict,
                                          exit_criteria: List[str]) -> Dict:
        """Perform release readiness review"""
        status = {'met': [], 'not_met': [], 'pending': []}
        
        for criteria in exit_criteria:
            if '95%' in criteria and test_results.get('pass_rate', '0%') >= '95%':
                status['met'].append(criteria)
            elif 'critical' in criteria.lower() and defect_data.get('by_priority', {}).get('critical', 0) == 0:
                status['met'].append(criteria)
            else:
                status['pending'].append(criteria)
        
        return {
            'release_ready': len(status['not_met']) == 0 and len(status['pending']) == 0,
            'criteria_status': status,
            'risk_level': 'Low' if len(status['not_met']) == 0 else 'Medium' if len(status['pending']) <= 2 else 'High',
            'recommendations': ['Complete pending test cases', 'Verify critical defect fixes'],
            'sign_off_required': ['QA Lead', 'Product Owner', 'Tech Lead']
        }


class TestEnvironmentManager:
    """Manage test environments"""
    
    def __init__(self):
        self.environments = []
    
    def create_environment(self,
                           name: str,
                           env_type: str,
                           config: Dict) -> Dict:
        """Create test environment"""
        return {
            'env_id': f"ENV-{len(self.environments) + 1:03d}",
            'name': name,
            'type': env_type,
            'configuration': config,
            'status': 'Available',
            'services': ['Web Server', 'Database', 'API Gateway'],
            'test_data': 'Refreshed 2024-01-15'
        }
    
    def compare_environments(self,
                             env1: Dict,
                             env2: Dict) -> Dict:
        """Compare two environments"""
        return {
            'environment_1': env1['name'],
            'environment_2': env2['name'],
            'differences': [
                {'component': 'Database', 'env1_version': 'PostgreSQL 14', 'env2_version': 'PostgreSQL 15'},
                {'component': 'API', 'env1_version': 'v2.1', 'env2_version': 'v2.2'}
            ],
            'compatibility_score': 85.0,
            'recommendations': ['Update env1 to match env2']
        }


class QAReportGenerator:
    """Generate QA reports"""
    
    def generate_test_summary_report(self,
                                     project: str,
                                     test_cycle: Dict,
                                     defect_analysis: Dict) -> Dict:
        """Generate test summary report"""
        return {
            'report_id': f"QA-RPT-{datetime.now().strftime('%Y%m%d')}",
            'project': project,
            'period': '2024-01-01 to 2024-01-31',
            'executive_summary': {
                'total_tests_executed': test_cycle.get('total_tests', 150),
                'pass_rate': test_cycle.get('pass_rate', '95%'),
                'defects_found': test_cycle.get('defects_found', 12),
                'critical_defects': defect_analysis.get('by_priority', {}).get('critical', 0),
                'release_recommendation': 'GO' if test_cycle.get('pass_rate', '0%') >= '95%' else 'CONDITIONAL GO'
            },
            'test_execution': {
                'by_module': {
                    'User Module': {'executed': 45, 'passed': 43, 'failed': 2},
                    'Payment Module': {'executed': 30, 'passed': 28, 'failed': 2},
                    'Reporting': {'executed': 25, 'passed': 25, 'failed': 0}
                },
                'by_type': {
                    'Functional': 70,
                    'Integration': 20,
                    'Regression': 10
                }
            },
            'defect_summary': {
                'total': defect_analysis.get('total_defects', 100),
                'open': defect_analysis.get('by_status', {}).get('open', 10),
                'resolved': defect_analysis.get('by_status', {}).get('resolved', 80),
                'by_severity': defect_analysis.get('by_priority', {})
            },
            'quality_metrics': {
                'test_coverage': 85.0,
                'requirements_coverage': 92.0,
                'defect_density': 0.5,
                'test_effectiveness': 95.0
            },
            'recommendations': ['Continue regression testing', 'Improve test data management']
        }


if __name__ == "__main__":
    qa = QualityAssuranceManager()
    
    plan = qa.create_test_plan("Release 2.0", "1.0")
    print(f"Test Plan: {plan.test_plan_id} - {plan.name}")
    
    review = qa.review_requirements([
        {'id': 'REQ-001', 'testable': True, 'measurable': True, 'complete': True},
        {'id': 'REQ-002', 'testable': False, 'measurable': True, 'complete': True}
    ])
    print(f"Requirements Review: {review['testability_score']}% testability score")
    
    test_case = qa.create_test_case(
        plan.test_plan_id,
        "Verify user login",
        "User Module",
        ["User exists", "Browser is clean"],
        ["Navigate to login", "Enter credentials", "Click login"],
        "User is logged in successfully"
    )
    print(f"Test Case: {test_case['test_case_id']} - {test_case['title']}")
    
    cycle = qa.execute_test_cycle([test_case, test_case, test_case], "QA")
    print(f"Test Cycle: {cycle['pass_rate']} pass rate, {cycle['defects_found']} defects")
    
    defect = qa.log_defect(
        "Login fails with valid credentials",
        "Users cannot login despite valid credentials",
        DefectPriority.HIGH,
        "User Module",
        test_case['test_case_id'],
        ["Navigate to login", "Enter valid credentials", "Click login"],
        "User should be logged in",
        "Error message displayed"
    )
    print(f"Defect: {defect.defect_id} - {defect.priority.value}")
    
    trends = qa.analyze_defect_trends()
    print(f"Defect Trends: {trends['total_defects']} total, {trends['closure_rate']}% closure rate")
    
    metrics = qa.calculate_quality_metrics(cycle, trends)
    print(f"Quality Score: {metrics['quality_score']:.1f}")
    
    release = qa.perform_release_readiness_review(cycle, trends, plan.exit_criteria)
    print(f"Release Ready: {release['release_ready']} (Risk: {release['risk_level']})")
    
    env = TestEnvironmentManager().create_environment("QA Environment", "Testing", {'os': 'Linux', 'db': 'PostgreSQL'})
    print(f"Environment: {env['name']} - {env['status']}")
    
    report = QAReportGenerator().generate_test_summary_report("Project X", cycle, trends)
    print(f"Report: {report['executive_summary']['release_recommendation']} for release")
