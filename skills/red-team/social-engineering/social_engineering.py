"""
Social Engineering Framework
A comprehensive framework for conducting authorized human-factor security testing.
"""

import asyncio
import logging
import hashlib
import json
import random
import string
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from abc import ABC, abstractmethod
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CampaignType(Enum):
    """Types of social engineering campaigns."""
    PHISHING = "phishing"
    VISHING = "vishing"
    SMISHING = "smishing"
    PRETEXTING = "pretexting"
    PHYSICAL = "physical"


class CampaignStatus(Enum):
    """Status of social engineering campaigns."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class UserAction(Enum):
    """User actions in social engineering campaigns."""
    EMAIL_OPENED = "email_opened"
    LINK_CLICKED = "link_clicked"
    CREDENTIALS_SUBMITTED = "credentials_submitted"
    MALWARE_DOWNLOADED = "malware_downloaded"
    INFORMATION_DISCLOSED = "information_disclosed"
    REPORTED = "reported"


class Severity(Enum):
    """Severity levels for social engineering findings."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class Target:
    """Represents a social engineering target."""
    user_id: str
    email: str
    name: str
    role: str
    department: str
    phone: str = ""
    access_level: str = "standard"
    risk_score: float = 0.0
    
    def __post_init__(self):
        """Validate target after initialization."""
        if not self.user_id:
            raise ValueError("User ID cannot be empty")
        if not self.email or "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")


@dataclass
class CampaignConfig:
    """Configuration for social engineering campaign."""
    campaign_type: CampaignType
    target_group: str
    template: str
    landing_page: str = ""
    send_time: datetime = field(default_factory=datetime.now)
    duration_days: int = 7
    max_sends: int = 1000
    tracking_enabled: bool = True
    randomize_send_time: bool = True
    exclude_recent_targets: bool = True
    exclude_days: int = 30


@dataclass
class CampaignResult:
    """Results from a social engineering campaign."""
    campaign_id: str
    campaign_type: CampaignType
    start_time: datetime
    end_time: Optional[datetime] = None
    status: CampaignStatus = CampaignStatus.DRAFT
    targets_contacted: int = 0
    targets_responded: int = 0
    successful_targets: int = 0
    reported_targets: int = 0
    user_actions: Dict[UserAction, int] = field(default_factory=dict)
    
    @property
    def response_rate(self) -> float:
        """Calculate response rate."""
        if self.targets_contacted == 0:
            return 0.0
        return (self.targets_responded / self.targets_contacted) * 100
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.targets_responded == 0:
            return 0.0
        return (self.successful_targets / self.targets_responded) * 100
    
    @property
    def reporting_rate(self) -> float:
        """Calculate reporting rate."""
        if self.targets_contacted == 0:
            return 0.0
        return (self.reported_targets / self.targets_contacted) * 100


class EmailTemplate:
    """Email template for phishing campaigns."""
    
    def __init__(self, name: str, subject: str, body: str, sender_name: str = ""):
        self.name = name
        self.subject = subject
        self.body = body
        self.sender_name = sender_name
        self.created_at = datetime.now()
    
    def render(self, variables: Dict[str, str] = None) -> Tuple[str, str]:
        """Render template with variables."""
        subject = self.subject
        body = self.body
        
        if variables:
            for key, value in variables.items():
                subject = subject.replace(f"{{{{{key}}}}}", value)
                body = body.replace(f"{{{{{key}}}}}", value)
        
        return subject, body
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary."""
        return {
            "name": self.name,
            "subject": self.subject,
            "body": self.body,
            "sender_name": self.sender_name,
            "created_at": self.created_at.isoformat()
        }


class PretextGenerator:
    """Generate social engineering pretexts."""
    
    @staticmethod
    def generate_phishing_pretext(
        scenario: str,
        target_role: str,
        urgency_level: str = "medium"
    ) -> Dict[str, Any]:
        """Generate phishing pretext."""
        pretexts = {
            "password_reset": {
                "subject": "Urgent: Password Reset Required",
                "body": "Dear {name},\n\nYour password will expire in 24 hours. "
                        "Please click the link below to reset your password immediately.\n\n"
                        "{link}\n\nIf you did not request this change, please contact IT support.",
                "sender": "IT Support <it-support@company.com>",
                "urgency": urgency_level
            },
            "account_verification": {
                "subject": "Account Verification Required",
                "body": "Dear {name},\n\nWe need to verify your account information. "
                        "Please click the link below to verify your account.\n\n"
                        "{link}\n\nThank you,\nSecurity Team",
                "sender": "Security Team <security@company.com>",
                "urgency": "high"
            },
            "invoice": {
                "subject": "Overdue Invoice #{invoice_number}",
                "body": "Dear {name},\n\nPlease find attached the overdue invoice #{invoice_number}. "
                        "Click the link below to view and pay the invoice.\n\n"
                        "{link}\n\nThank you,\nAccounts Payable",
                "sender": "Accounts Payable <ap@company.com>",
                "urgency": "medium"
            }
        }
        
        return pretexts.get(scenario, pretexts["password_reset"])
    
    @staticmethod
    def generate_vishing_pretext(
        target_role: str,
        scenario: str,
        urgency_level: str = "medium"
    ) -> Dict[str, Any]:
        """Generate vishing pretext."""
        pretexts = {
            "help_desk": {
                "script": "Hello, this is John from IT Support. We're experiencing some issues "
                         "with the network and need to verify your account. Can you please provide "
                         "your username and current password for verification?",
                "escalation": "I understand your concern, but this is urgent and we need to "
                            "resolve this immediately to prevent service disruption.",
                "closing": "Thank you for your cooperation. We'll let you know when the issue is resolved."
            },
            "executive_assistant": {
                "script": "Hi, this is Sarah from the CEO's office. The CEO is in a meeting and "
                         "needs you to send over the confidential report immediately. Can you email it "
                         "to me at this address?",
                "escalation": "The CEO specifically asked for this information and needs it within the hour.",
                "closing": "Thank you for your prompt assistance."
            }
        }
        
        return pretexts.get(target_role, pretexts["help_desk"])
    
    @staticmethod
    def generate_physical_pretext(
        scenario: str,
        target_area: str,
        disguise: str = "delivery_person"
    ) -> Dict[str, Any]:
        """Generate physical social engineering pretext."""
        pretexts = {
            "tailgating": {
                "approach": "Wait for an employee to enter, then follow closely behind while "
                           "carrying packages or equipment.",
                "excuse": "I have a delivery for the 3rd floor, but I'm not sure where to go. "
                         "Can you hold the door for me?",
                "props": ["delivery_box", "clipboard", "fake_id"],
                "exit_strategy": "Thank the employee and proceed to the target area."
            },
            "impersonation": {
                "approach": "Dress as a maintenance worker or contractor to gain access to restricted areas.",
                "excuse": "I'm here to perform scheduled maintenance on the HVAC system. "
                         "Can you direct me to the mechanical room?",
                "props": ["uniform", "tools", "fake_work_order"],
                "exit_strategy": "Complete the supposed maintenance and leave normally."
            }
        }
        
        return pretexts.get(scenario, pretexts["tailgating"])


class PhishingCampaign:
    """Phishing campaign management."""
    
    def __init__(self, name: str, target_group: str, template: str, landing_page: str = ""):
        self.name = name
        self.target_group = target_group
        self.template = template
        self.landing_page = landing_page
        self.config = None
        self.targets = []
        self.results = []
        self.status = CampaignStatus.DRAFT
    
    def configure(self, **kwargs) -> None:
        """Configure campaign settings."""
        self.config = CampaignConfig(
            campaign_type=CampaignType.PHISHING,
            target_group=self.target_group,
            template=self.template,
            landing_page=self.landing_page,
            **kwargs
        )
        logger.info(f"Configured phishing campaign: {self.name}")
    
    def add_targets(self, targets: List[Target]) -> None:
        """Add targets to campaign."""
        self.targets.extend(targets)
        logger.info(f"Added {len(targets)} targets to campaign {self.name}")
    
    def execute(self) -> str:
        """Execute phishing campaign."""
        if not self.config:
            raise ValueError("Campaign not configured")
        
        self.status = CampaignStatus.ACTIVE
        campaign_id = hashlib.md5(self.name.encode()).hexdigest()[:8]
        
        logger.info(f"Executing phishing campaign: {self.name} (ID: {campaign_id})")
        
        # Simulate campaign execution
        for target in self.targets:
            # Simulate email sending
            logger.info(f"Sending phishing email to {target.email}")
            
            # Simulate user actions
            actions = self._simulate_user_actions(target)
            self.results.append({
                "target": target,
                "actions": actions,
                "timestamp": datetime.now()
            })
        
        self.status = CampaignStatus.COMPLETED
        return campaign_id
    
    def _simulate_user_actions(self, target: Target) -> List[UserAction]:
        """Simulate user actions for demonstration."""
        actions = []
        
        # Randomly determine user actions based on risk score
        if random.random() < 0.7:  # 70% chance email is opened
            actions.append(UserAction.EMAIL_OPENED)
            
            if random.random() < 0.5:  # 50% chance link is clicked
                actions.append(UserAction.LINK_CLICKED)
                
                if random.random() < 0.3:  # 30% chance credentials are submitted
                    actions.append(UserAction.CREDENTIALS_SUBMITTED)
        
        # 10% chance user reports the phishing attempt
        if random.random() < 0.1:
            actions.append(UserAction.REPORTED)
        
        return actions
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get campaign statistics."""
        total_targets = len(self.targets)
        total_opened = 0
        total_clicked = 0
        total_submitted = 0
        total_reported = 0
        
        for result in self.results:
            actions = result["actions"]
            if UserAction.EMAIL_OPENED in actions:
                total_opened += 1
            if UserAction.LINK_CLICKED in actions:
                total_clicked += 1
            if UserAction.CREDENTIALS_SUBMITTED in actions:
                total_submitted += 1
            if UserAction.REPORTED in actions:
                total_reported += 1
        
        return {
            "total_targets": total_targets,
            "emails_opened": total_opened,
            "links_clicked": total_clicked,
            "credentials_submitted": total_submitted,
            "reported": total_reported,
            "open_rate": (total_opened / total_targets * 100) if total_targets > 0 else 0,
            "click_rate": (total_clicked / total_targets * 100) if total_targets > 0 else 0,
            "submission_rate": (total_submitted / total_targets * 100) if total_targets > 0 else 0,
            "report_rate": (total_reported / total_targets * 100) if total_targets > 0 else 0
        }


class VishingCampaign:
    """Vishing campaign management."""
    
    def __init__(self, name: str, target_list: List[str], pretext: Dict[str, Any], call_script: str = ""):
        self.name = name
        self.target_list = target_list
        self.pretext = pretext
        self.call_script = call_script
        self.results = []
    
    def execute(self) -> List[Dict[str, Any]]:
        """Execute vishing campaign."""
        logger.info(f"Executing vishing campaign: {self.name}")
        
        results = []
        for target_id in self.target_list:
            # Simulate vishing call
            result = {
                "target": target_id,
                "pretext_used": self.pretext,
                "information_disclosed": random.randint(0, 3),
                "actions_performed": random.randint(0, 2),
                "call_duration": random.randint(30, 300),
                "timestamp": datetime.now()
            }
            results.append(result)
        
        self.results = results
        return results


class PhysicalSocialEngineering:
    """Physical social engineering testing."""
    
    def __init__(self, name: str, pretext: Dict[str, Any], authorized_personnel: List[str] = None):
        self.name = name
        self.pretext = pretext
        self.authorized_personnel = authorized_personnel or []
        self.result = None
    
    def execute(self) -> Dict[str, Any]:
        """Execute physical social engineering test."""
        logger.info(f"Executing physical test: {self.name}")
        
        # Simulate physical social engineering test
        self.result = {
            "access_achieved": random.random() > 0.3,
            "access_duration": random.randint(5, 60),
            "sensitive_areas_accessed": random.randint(0, 3),
            "information_gathered": random.randint(0, 5),
            "security_bypassed": random.randint(0, 2),
            "timestamp": datetime.now()
        }
        
        return self.result


class CampaignManager:
    """Manage multiple social engineering campaigns."""
    
    def __init__(self):
        self.campaigns = {}
        self.results = {}
    
    def execute_campaign(self, campaign: PhishingCampaign) -> str:
        """Execute a campaign and return its ID."""
        campaign_id = campaign.execute()
        self.campaigns[campaign_id] = campaign
        self.results[campaign_id] = campaign.get_statistics()
        return campaign_id
    
    def is_complete(self, campaign_id: str) -> bool:
        """Check if campaign is complete."""
        if campaign_id not in self.campaigns:
            return False
        return self.campaigns[campaign_id].status == CampaignStatus.COMPLETED
    
    def get_statistics(self, campaign_id: str) -> Dict[str, Any]:
        """Get campaign statistics."""
        return self.results.get(campaign_id, {})
    
    def list_campaigns(self) -> List[str]:
        """List all campaigns."""
        return list(self.campaigns.keys())
    
    def get_overall_statistics(self) -> Dict[str, Any]:
        """Get overall statistics across all campaigns."""
        total_targets = 0
        total_opened = 0
        total_clicked = 0
        total_submitted = 0
        total_reported = 0
        
        for stats in self.results.values():
            total_targets += stats.get("total_targets", 0)
            total_opened += stats.get("emails_opened", 0)
            total_clicked += stats.get("links_clicked", 0)
            total_submitted += stats.get("credentials_submitted", 0)
            total_reported += stats.get("reported", 0)
        
        return {
            "total_campaigns": len(self.campaigns),
            "total_targets": total_targets,
            "overall_open_rate": (total_opened / total_targets * 100) if total_targets > 0 else 0,
            "overall_click_rate": (total_clicked / total_targets * 100) if total_targets > 0 else 0,
            "overall_submission_rate": (total_submitted / total_targets * 100) if total_targets > 0 else 0,
            "overall_report_rate": (total_reported / total_targets * 100) if total_targets > 0 else 0
        }


class CampaignAnalytics:
    """Analytics for social engineering campaigns."""
    
    def __init__(self):
        self.reports = []
    
    def generate_report(
        self,
        campaign_ids: List[str],
        report_type: str = "executive_summary",
        include_recommendations: bool = True
    ) -> 'Report':
        """Generate comprehensive report."""
        logger.info(f"Generating {report_type} report for campaigns: {campaign_ids}")
        
        # Simulate report generation
        report = Report(
            report_type=report_type,
            campaign_ids=campaign_ids,
            generated_at=datetime.now(),
            include_recommendations=include_recommendations
        )
        
        self.reports.append(report)
        return report
    
    def get_key_metrics(self) -> Dict[str, Any]:
        """Get key metrics across campaigns."""
        return {
            "susceptibility_rate": 23.5,
            "most_effective_vector": "password_reset",
            "improvement_trend": "positive",
            "avg_response_time": "2.3 hours",
            "top_vulnerable_department": "finance"
        }


class Report:
    """Social engineering test report."""
    
    def __init__(
        self,
        report_type: str,
        campaign_ids: List[str],
        generated_at: datetime,
        include_recommendations: bool = True
    ):
        self.report_type = report_type
        self.campaign_ids = campaign_ids
        self.generated_at = generated_at
        self.include_recommendations = include_recommendations
        self.content = self._generate_content()
    
    def _generate_content(self) -> Dict[str, Any]:
        """Generate report content."""
        return {
            "executive_summary": "This report summarizes the results of social engineering testing.",
            "key_findings": [
                "23.5% of employees clicked on phishing links",
                "15.2% submitted credentials",
                "8.7% reported the phishing attempts"
            ],
            "recommendations": [
                "Implement regular security awareness training",
                "Enhance email filtering and anti-phishing controls",
                "Establish clear reporting procedures for suspicious emails"
            ] if self.include_recommendations else [],
            "detailed_results": {},
            "appendices": []
        }
    
    def export_to_pdf(self, filename: str) -> None:
        """Export report to PDF."""
        logger.info(f"Exporting report to PDF: {filename}")
        # Simulate PDF export
    
    def export_to_json(self, filename: str) -> None:
        """Export report to JSON."""
        logger.info(f"Exporting report to JSON: {filename}")
        # Simulate JSON export


async def main():
    """Main demonstration function."""
    print("=" * 60)
    print("Social Engineering Framework Demonstration")
    print("=" * 60)
    
    # Create sample targets
    targets = [
        Target(
            user_id="user001",
            email="john.doe@company.com",
            name="John Doe",
            role="manager",
            department="finance",
            phone="+1-555-0101",
            access_level="elevated",
            risk_score=0.7
        ),
        Target(
            user_id="user002",
            email="jane.smith@company.com",
            name="Jane Smith",
            role="analyst",
            department="engineering",
            phone="+1-555-0102",
            access_level="standard",
            risk_score=0.4
        ),
        Target(
            user_id="user003",
            email="bob.wilson@company.com",
            name="Bob Wilson",
            role="director",
            department="hr",
            phone="+1-555-0103",
            access_level="elevated",
            risk_score=0.6
        )
    ]
    
    print(f"Created {len(targets)} sample targets")
    
    # Demo 1: Phishing Campaign
    print("\n" + "=" * 60)
    print("Demo 1: Phishing Campaign")
    print("=" * 60)
    
    # Create phishing campaign
    phishing_campaign = PhishingCampaign(
        name="Q4 Security Assessment",
        target_group="all_employees",
        template="credential_harvest",
        landing_page="https://test.company.com/phish"
    )
    
    # Configure campaign
    phishing_campaign.configure(
        send_time=datetime.now(),
        duration_days=7,
        max_sends=1000,
        tracking_enabled=True
    )
    
    # Add targets
    phishing_campaign.add_targets(targets)
    
    # Execute campaign
    campaign_manager = CampaignManager()
    campaign_id = campaign_manager.execute_campaign(phishing_campaign)
    print(f"Campaign ID: {campaign_id}")
    
    # Get statistics
    stats = campaign_manager.get_statistics(campaign_id)
    print(f"Emails sent: {stats.get('total_targets', 0)}")
    print(f"Opened: {stats.get('emails_opened', 0)}")
    print(f"Clicked: {stats.get('links_clicked', 0)}")
    print(f"Credentials submitted: {stats.get('credentials_submitted', 0)}")
    print(f"Reported: {stats.get('reported', 0)}")
    
    # Demo 2: Vishing Campaign
    print("\n" + "=" * 60)
    print("Demo 2: Vishing Campaign")
    print("=" * 60)
    
    # Generate vishing pretext
    pretext = PretextGenerator.generate_vishing_pretext(
        target_role="help_desk",
        scenario="password_reset",
        urgency_level="high"
    )
    
    # Create vishing campaign
    vishing_campaign = VishingCampaign(
        name="IT Support Impersonation",
        target_list=["user001", "user002", "user003"],
        pretext=pretext,
        call_script=pretext.get("script", "")
    )
    
    # Execute campaign
    vishing_results = vishing_campaign.execute()
    print(f"Vishing campaign executed: {len(vishing_results)} calls")
    
    for result in vishing_results:
        print(f"  Target: {result['target']}")
        print(f"  Information disclosed: {result['information_disclosed']}")
        print(f"  Actions performed: {result['actions_performed']}")
    
    # Demo 3: Physical Social Engineering
    print("\n" + "=" * 60)
    print("Demo 3: Physical Social Engineering")
    print("=" * 60)
    
    # Generate physical pretext
    physical_pretext = PretextGenerator.generate_physical_pretext(
        scenario="tailgating",
        target_area="server_room",
        disguise="delivery_person"
    )
    
    # Create physical test
    physical_test = PhysicalSocialEngineering(
        name="Physical Access Test",
        pretext=physical_pretext,
        authorized_personnel=["security_team", "management"]
    )
    
    # Execute test
    physical_result = physical_test.execute()
    print(f"Physical test result:")
    print(f"  Access achieved: {physical_result['access_achieved']}")
    print(f"  Duration of access: {physical_result['access_duration']} minutes")
    print(f"  Sensitive areas accessed: {physical_result['sensitive_areas_accessed']}")
    
    # Demo 4: Campaign Analytics
    print("\n" + "=" * 60)
    print("Demo 4: Campaign Analytics")
    print("=" * 60)
    
    # Initialize analytics
    analytics = CampaignAnalytics()
    
    # Generate report
    report = analytics.generate_report(
        campaign_ids=[campaign_id],
        report_type="executive_summary",
        include_recommendations=True
    )
    
    print(f"Report generated: {report.report_type}")
    print(f"Generated at: {report.generated_at}")
    
    # Get key metrics
    metrics = analytics.get_key_metrics()
    print(f"\nKey Metrics:")
    print(f"  Susceptibility rate: {metrics['susceptibility_rate']}%")
    print(f"  Most effective vector: {metrics['most_effective_vector']}")
    print(f"  Improvement trend: {metrics['improvement_trend']}")
    
    # Get overall statistics
    overall_stats = campaign_manager.get_overall_statistics()
    print(f"\nOverall Statistics:")
    print(f"  Total campaigns: {overall_stats['total_campaigns']}")
    print(f"  Overall open rate: {overall_stats['overall_open_rate']:.1f}%")
    print(f"  Overall click rate: {overall_stats['overall_click_rate']:.1f}%")
    print(f"  Overall submission rate: {overall_stats['overall_submission_rate']:.1f}%")
    
    print("\n" + "=" * 60)
    print("Demonstration completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())