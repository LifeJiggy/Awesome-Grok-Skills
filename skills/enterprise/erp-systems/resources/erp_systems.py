from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class ERPModule(Enum):
    FINANCE = "Finance"
    HRM = "Human Resources"
    SCM = "Supply Chain"
    CRM = "Customer Relationship"
    MANUFACTURING = "Manufacturing"
    PROJECT = "Project Management"


@dataclass
class ERPProject:
    project_id: str
    name: str
    modules: List[str]
    timeline_months: int
    budget: float


class ERPImplementationManager:
    """Manage ERP implementation projects"""
    
    def __init__(self):
        self.projects = []
    
    def create_implementation_plan(self,
                                   name: str,
                                   modules: List[ERPModule],
                                   timeline_months: int = 18,
                                   budget: float = 500000) -> ERPProject:
        """Create ERP implementation plan"""
        return ERPProject(
            project_id=f"ERP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=name,
            modules=[m.value for m in modules],
            timeline_months=timeline_months,
            budget=budget
        )
    
    def design_phases(self,
                      project: ERPProject) -> Dict:
        """Design implementation phases"""
        phase_duration = project.timeline_months / 5
        
        return {
            'project': project.name,
            'phases': [
                {
                    'phase': 1,
                    'name': 'Discovery & Design',
                    'duration_months': phase_duration,
                    'activities': [
                        'Requirements gathering',
                        'Current state analysis',
                        'Future state design',
                        'Gap analysis',
                        'Solution design'
                    ],
                    'deliverables': [
                        'Business requirements document',
                        'Current state diagrams',
                        'Future state design',
                        'Gap analysis report',
                        'Solution architecture'
                    ],
                    'resources': {'analysts': 3, 'consultants': 2, 'it': 2}
                },
                {
                    'phase': 2,
                    'name': 'Configuration & Development',
                    'duration_months': phase_duration * 2,
                    'activities': [
                        'System configuration',
                        'Custom development',
                        'Integration setup',
                        'Data migration planning',
                        'Security setup'
                    ],
                    'deliverables': [
                        'Configured system',
                        'Custom reports',
                        'Integration interfaces',
                        'Data migration scripts',
                        'Security roles'
                    ],
                    'resources': {'developers': 4, 'consultants': 3, 'it': 3}
                },
                {
                    'phase': 3,
                    'name': 'Testing',
                    'duration_months': phase_duration,
                    'activities': [
                        'Unit testing',
                        'Integration testing',
                        'User acceptance testing',
                        'Performance testing',
                        'Security testing'
                    ],
                    'deliverables': [
                        'Test plans',
                        'Test scripts',
                        'Defect reports',
                        'UAT sign-off',
                        'Performance report'
                    ],
                    'resources': {'testers': 3, 'business': 5, 'consultants': 2}
                },
                {
                    'phase': 4,
                    'name': 'Deployment',
                    'duration_months': phase_duration,
                    'activities': [
                        'Data migration',
                        'Cutover planning',
                        'Go-live preparation',
                        'Hypercare support',
                        'Training delivery'
                    ],
                    'deliverables': [
                        'Migrated data',
                        'Cutover plan',
                        'Go-live checklist',
                        'Support processes',
                        'Training materials'
                    ],
                    'resources': {'all': 10}
                },
                {
                    'phase': 5,
                    'name': 'Optimization',
                    'duration_months': phase_duration,
                    'activities': [
                        'Post-implementation review',
                        'Performance tuning',
                        'Process optimization',
                        'Advanced training',
                        'Continuous improvement'
                    ],
                    'deliverables': [
                        'Benefits realization report',
                        'Optimization recommendations',
                        'Advanced training',
                        'Continuous improvement plan'
                    ],
                    'resources': {'consultants': 2, 'analysts': 2}
                }
            ],
            'total_resources': '8-12 FTEs',
            'critical_path': 'Testing → Deployment'
        }
    
    def analyze_business_processes(self,
                                   processes: List[Dict]) -> Dict:
        """Analyze and map business processes"""
        return {
            'processes_analyzed': len(processes),
            'current_state_findings': [
                {'process': 'Order to Cash', 'efficiency': 65, 'automation': 40},
                {'process': 'Procure to Pay', 'efficiency': 70, 'automation': 50},
                {'process': 'Hire to Retire', 'efficiency': 60, 'automation': 35},
                {'process': 'Plan to Produce', 'efficiency': 55, 'automation': 45}
            ],
            'pain_points': [
                'Manual data entry between systems',
                'Lack of real-time reporting',
                'Inventory visibility issues',
                'Duplicate data entry'
            ],
            'erp_benefits': [
                {'area': 'Process Efficiency', 'expected_improvement': '25-40%'},
                {'area': 'Data Accuracy', 'expected_improvement': '90-95%'},
                {'area': 'Reporting Speed', 'expected_improvement': '70-80%'},
                {'area': 'Compliance', 'expected_improvement': 'Significant'}
            ]
        }
    
    def configure_finance_module(self) -> Dict:
        """Configure finance module"""
        return {
            'module': 'Finance',
            'sub_modules': [
                'General Ledger',
                'Accounts Payable',
                'Accounts Receivable',
                'Fixed Assets',
                'Cash Management',
                'Financial Reporting'
            ],
            'chart_of_accounts': {
                'structure': 'Segmented (Company > Account > Cost Center)',
                'segments': 4,
                'total_accounts': 500
            },
            'key_processes': [
                'Journal entry approval workflow',
                'Invoice matching and payment',
                'Revenue recognition',
                'Period close automation',
                'Intercompany reconciliation'
            ],
            'integrations': [
                'Banking interfaces',
                'Tax calculation engines',
                'Treasury systems',
                'Audit management'
            ]
        }
    
    def configure_supply_chain_module(self) -> Dict:
        """Configure supply chain module"""
        return {
            'module': 'Supply Chain',
            'sub_modules': [
                'Procurement',
                'Inventory Management',
                'Order Management',
                'Warehouse Management',
                'Transportation'
            ],
            'key_processes': [
                'Supplier qualification',
                'Purchase requisition to order',
                'Inventory valuation',
                'Demand forecasting',
                'Shipment tracking'
            ],
            'optimizations': [
                'Safety stock calculation',
                'Reorder point optimization',
                'Vendor selection scoring',
                'Route optimization'
            ],
            'integrations': [
                'Supplier portals',
                'Logistics providers',
                'Quality management',
                'Demand planning'
            ]
        }
    
    def configure_hr_module(self) -> Dict:
        """Configure HR module"""
        return {
            'module': 'Human Resources',
            'sub_modules': [
                'Core HR',
                'Talent Management',
                'Learning',
                'Compensation',
                'Time & Attendance'
            ],
            'key_processes': [
                'Employee lifecycle management',
                'Performance reviews',
                'Learning delivery',
                'Benefits administration',
                'Payroll integration'
            ],
            'compliance': [
                'GDPR data handling',
                'EEO reporting',
                'OSHA recordkeeping',
                'I-9 verification'
            ],
            'self_service': [
                'Employee self-service',
                'Manager self-service',
                'Time entry',
                'Benefits enrollment'
            ]
        }
    
    def plan_data_migration(self,
                           source_systems: List[str],
                           target_modules: List[str]) -> Dict:
        """Plan data migration strategy"""
        return {
            'sources': source_systems,
            'targets': target_modules,
            'migration_strategy': 'Phased by module',
            'data_volume': {
                'customers': 50000,
                'suppliers': 5000,
                'products': 10000,
                'transactions': 500000
            },
            'phases': [
                {'phase': 'Extract', 'tool': 'Informatica/SSIS', 'schedule': 'Week 1-2'},
                {'phase': 'Transform', 'tool': 'Python/SQL', 'schedule': 'Week 2-4'},
                {'phase': 'Validate', 'tool': 'Custom validation scripts', 'schedule': 'Week 4-5'},
                {'phase': 'Load', 'tool': 'ERP import tools', 'schedule': 'Week 5-6'},
                {'phase': 'Verify', 'tool': 'Reconciliation reports', 'schedule': 'Week 6-7'}
            ],
            'data_quality_checks': [
                'Duplicate detection',
                'Referential integrity',
                'Format standardization',
                'Value validation'
            ],
            'rollback_plan': 'Point-in-time recovery for each phase'
        }
    
    def manage_change_management(self,
                                stakeholders: List[str]) -> Dict:
        """Manage organizational change"""
        return {
            'change_impact': {
                'high_impact': ['Finance team', 'Operations team'],
                'medium_impact': ['Sales team', 'HR team'],
                'low_impact': ['Executive team', 'IT team']
            },
            'communication_plan': {
                'kick_off': 'All stakeholders',
                'weekly_updates': 'Project team',
                'monthly_newsletters': 'All employees',
                'town_halls': 'Department heads'
            },
            'training_program': {
                'role_based_training': True,
                'training_types': [
                    'End-user training',
                    'Administrator training',
                    'Power user training',
                    'Executive briefing'
                ],
                'delivery_methods': [
                    'Classroom sessions',
                    'E-learning modules',
                    'Hands-on workshops',
                    'Just-in-time guides'
                ]
            },
            'resistance_management': [
                'Early engagement',
                'Change champions',
                'Quick wins',
                'Feedback mechanisms'
            ],
            'success_metrics': [
                'User adoption rate > 90%',
                'Training completion > 95%',
                'System usage > 80%',
                'Satisfaction score > 4/5'
            ]
        }
    
    def calculate_roi(self,
                      investment: float,
                      benefits: Dict) -> Dict:
        """Calculate ERP ROI"""
        yearly_savings = (
            benefits.get('labor_savings', 200000) +
            benefits.get('efficiency_gains', 150000) +
            benefits.get('error_reduction', 100000) +
            benefits.get('inventory_optimization', 80000) +
            benefits.get('compliance_savings', 50000)
        )
        
        payback_years = investment / yearly_savings
        
        return {
            'investment_breakdown': {
                'software': investment * 0.35,
                'implementation': investment * 0.40,
                'hardware': investment * 0.15,
                'training': investment * 0.10
            },
            'annual_benefits': {
                'total': yearly_savings,
                'labor_savings': benefits.get('labor_savings', 200000),
                'efficiency_gains': benefits.get('efficiency_gains', 150000),
                'error_reduction': benefits.get('error_reduction', 100000),
                'inventory_optimization': benefits.get('inventory_optimization', 80000),
                'compliance_savings': benefits.get('compliance_savings', 50000)
            },
            'roi_metrics': {
                'payback_period_years': round(payback_years, 1),
                '5_year_roi_percent': ((yearly_savings * 5 - investment) / investment) * 100,
                'net_present_value': yearly_savings * 4.329 - investment,
                'internal_rate_of_return': 25
            },
            'intangible_benefits': [
                'Improved decision making',
                'Better customer service',
                'Enhanced collaboration',
                'Competitive advantage'
            ]
        }


class ERPSystemIntegrator:
    """Integrate ERP with other systems"""
    
    def design_integrations(self,
                           erp_system: str,
                           external_systems: List[Dict]) -> Dict:
        """Design system integrations"""
        return {
            'erp_system': erp_system,
            'integration_patterns': [
                {'pattern': 'Point-to-Point', 'use_case': 'Simple data exchanges'},
                {'pattern': 'ESB', 'use_case': 'Complex orchestration'},
                {'pattern': 'API Gateway', 'use_case': 'Modern REST APIs'},
                {'pattern': 'iPaaS', 'use_case': 'Cloud integrations'}
            ],
            'key_integrations': [
                {
                    'system': 'CRM',
                    'direction': 'Bidirectional',
                    'data': ['Customers', 'Orders', 'Contacts'],
                    'frequency': 'Real-time'
                },
                {
                    'system': 'E-Commerce',
                    'direction': 'ERP to E-commerce',
                    'data': ['Products', 'Pricing', 'Inventory'],
                    'frequency': 'Hourly'
                },
                {
                    'system': 'WMS',
                    'direction': 'Bidirectional',
                    'data': ['Shipments', 'Inventory', 'Receipts'],
                    'frequency': 'Real-time'
                }
            ],
            'middleware': [
                'MuleSoft',
                'Dell Boomi',
                'Microsoft BizTalk',
                'Custom APIs'
            ]
        }


if __name__ == "__main__":
    erp = ERPImplementationManager()
    
    project = erp.create_implementation_plan(
        "Global ERP Rollout",
        [ERPModule.FINANCE, ERPModule.HRM, ERPModule.SCM],
        18,
        750000
    )
    print(f"ERP Project: {project.name} ({len(project.modules)} modules)")
    
    phases = erp.design_phases(project)
    print(f"Implementation: {len(phases['phases'])} phases planned")
    
    processes = erp.analyze_business_processes([])
    print(f"Process Analysis: {len(processes['pain_points'])} pain points identified")
    
    finance = erp.configure_finance_module()
    print(f"Finance Module: {len(finance['sub_modules'])} sub-modules")
    
    supply_chain = erp.configure_supply_chain_module()
    print(f"Supply Chain: {len(supply_chain['optimizations'])} optimizations")
    
    hr = erp.configure_hr_module()
    print(f"HR Module: {len(hr['compliance'])} compliance areas")
    
    migration = erp.plan_data_migration(['Legacy ERP', 'CRM'], ['Finance', 'SCM'])
    print(f"Data Migration: {len(migration['phases'])} phases")
    
    change = erp.change_management(['Finance Team', 'IT Team'])
    print(f"Change Management: {len(change['training_program']['training_types'])} training types")
    
    roi = erp.calculate_roi(750000, {
        'labor_savings': 250000,
        'efficiency_gains': 200000,
        'error_reduction': 150000,
        'inventory_optimization': 100000,
        'compliance_savings': 75000
    })
    print(f"ERP ROI: {roi['roi_metrics']['payback_period_years']} year payback")
    
    integrations = ERPSystemIntegrator().design_integrations('SAP S/4HANA', [])
    print(f"Integrations: {len(integrations['key_integrations'])} key integrations")
