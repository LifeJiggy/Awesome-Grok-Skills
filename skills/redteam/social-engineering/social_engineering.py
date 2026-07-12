"""
Social Engineering Framework Module

Provides structured methodology and tooling for authorized human-factor
security testing including phishing campaigns, pretexting, vishing,
and physical social engineering.

This module is for authorized red team operations only. All activities
must be explicitly authorized in the rules of engagement.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class CampaignStatus(Enum):
    """Status of a social engineering campaign."""
    PLANNING = auto()
    INFRASTRUCTURE = auto()
    ACTIVE = auto()
    COMPLETED = auto()
    CANCELLED = auto()


class PsychologicalPrinciple(Enum):
    """Cialdini's principles of persuasion."""
    AUTHORITY = "authority"
    URGENCY = "urgency"
    SCARCITY = "scarcity"
    SOCIAL_PROOF = "social_proof"
    RECIPROCITY = "reciprocity"
    COMMITMENT = "commitment"
    LIKING = "liking"


class PretextType(Enum):
    """Types of social engineering pretexts."""
    IT_SUPPORT = "it_support"
    VENDOR = "vendor"
    EXECUTIVE = "executive"
    NEW_EMPLOYEE = "new_employee"
    GOVERNMENT = "government"
    PARTNER = "partner"
    CUSTOMER = "customer"
    INSIDER = "insider"


class PhishingOutcome(Enum):
    """Outcome of a phishing attempt."""
    NOT_SENT = auto()
    SENT = auto()
    DELIVERED = auto()
    OPENED = auto()
    CLICKED = auto()
    CREDENTIALS_SUBMITTED = auto()
    REPORTED = auto()
    BLOCKED = auto()


class VishingOutcome(Enum):
    """Outcome of a vishing attempt."""
    NOT_CALLED = auto()
    NO_ANSWER = auto()
    ANSWERED = auto()
    INFORMATION_DISCLOSED = auto()
    CREDENTIALS_OBTAINED = auto()
    REFUSED = auto()
    SUSPICIOUS = auto()
    REPORTED = auto()


class EmailAuth(Enum):
    """Email authentication status."""
    SPF_PASS = "spf_pass"
    SPF_FAIL = "spf_fail"
    DKIM_PASS = "dkim_pass"
    DKIM_FAIL = "dkim_fail"
    DMARC_PASS = "dmarc_pass"
    DMARC_FAIL = "dmarc_fail"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class TargetAudience:
    """Target audience for social engineering campaign."""
    organization: str
    department: str
    employee_count: int
    seniority_levels: list[str] = field(default_factory=list)
    tech_savviness: str = "moderate"
    known_training: list[str] = field(default_factory=list)
    recent_events: list[str] = field(default_factory=list)
    email_domain: str = ""

    def get_email_list(self) -> list[dict[str, str]]:
        """Generate simulated email list for campaign."""
        return [
            {"name": f"Employee {i}", "email": f"user{i}@{self.email_domain or self.organization.lower().replace(' ', '')}.com"}
            for i in range(1, min(self.employee_count + 1, 51))
        ]


@dataclass
class Pretext:
    """Social engineering pretext definition."""
    persona: str
    scenario: str
    urgency: str = "medium"
    authority: str = ""
    psychological_principles: list[str] = field(default_factory=list)
    pretext_details: dict[str, str] = field(default_factory=dict)
    pretext_type: PretextType = PretextType.IT_SUPPORT

    def get_call_script(self) -> str:
        """Generate a call script from the pretext."""
        return (
            f"Hi, this is {self.authority or self.persona}. "
            f"{self.scenario}. "
            f"Reference: {self.pretext_details.get('reference_ticket', 'N/A')}. "
            f"Please verify your identity to proceed."
        )


@dataclass
class Campaign:
    """Social engineering campaign definition."""
    name: str
    authorization_doc: str
    scope: str
    target_audience: TargetAudience
    pretexts: list[Pretext]
    objectives: list[str] = field(default_factory=list)
    timeline: dict[str, str] = field(default_factory=dict)
    ethical_guidelines: list[str] = field(default_factory=list)
    status: CampaignStatus = CampaignStatus.PLANNING
    campaign_id: str = field(default_factory=lambda: f"CAMP-{uuid.uuid4().hex[:6].upper()}")
    created_at: datetime = field(default_factory=datetime.utcnow)

    def is_authorized(self) -> bool:
        """Check if campaign has authorization documentation."""
        return bool(self.authorization_doc)


@dataclass
class Domain:
    """Lookalike domain configuration."""
    name: str
    registrar: str = ""
    privacy_protection: bool = True
    auto_renew: bool = True
    dns_config: dict[str, Any] = field(default_factory=dict)
    ssl_enabled: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EmailServer:
    """Email server for phishing campaigns."""
    provider: str
    domains: list[Domain] = field(default_factory=list)
    authentication: dict[str, bool] = field(default_factory=dict)
    warming_period_days: int = 7
    daily_send_limit: int = 50
    tracking_enabled: bool = True

    def is_ready(self) -> bool:
        """Check if email server is configured and warmed up."""
        return all(self.authentication.get(k, False) for k in ["spf", "dkim", "dmarc"])


@dataclass
class PhishingEmail:
    """Phishing email template."""
    from_name: str
    from_email: str
    subject: str
    body: str
    tracking_id: str = ""
    reply_to: str = ""
    attachments: list[str] = field(default_factory=list)
    html_version: bool = False

    def render(self, variables: dict[str, str]) -> tuple[str, str, str]:
        """Render email with target-specific variables."""
        body = self.body
        for key, value in variables.items():
            body = body.replace(f"{{{key}}}", value)
        return self.from_email, self.subject, body


@dataclass
class LandingPage:
    """Phishing credential harvesting page."""
    template: str = "corporate_login"
    branding: dict[str, str] = field(default_factory=dict)
    form_action: str = "/collect"
    capture_fields: list[str] = field(default_factory=lambda: ["username", "password"])
    redirect_after: str = "https://login.microsoftonline.com"
    ssl_enabled: bool = True
    tracking: bool = True


@dataclass
class CallTarget:
    """Target for vishing campaign."""
    name: str
    phone: str
    department: str = ""
    role: str = ""
    notes: str = ""
    outcome: VishingOutcome = VishingOutcome.NOT_CALLED
    call_duration_seconds: int = 0
    information_disclosed: list[str] = field(default_factory=list)


@dataclass
class CallScript:
    """Vishing call script."""
    name: str
    scenario: str
    opening: str
    verification_questions: list[str] = field(default_factory=list)
    main_request: str = ""
    handling_objections: dict[str, str] = field(default_factory=dict)
    closing: str = ""
    escalation_path: str = ""


@dataclass
class CampaignMetrics:
    """Aggregated campaign metrics."""
    emails_sent: int = 0
    emails_delivered: int = 0
    emails_opened: int = 0
    links_clicked: int = 0
    credentials_submitted: int = 0
    incidents_reported: int = 0

    @property
    def open_rate(self) -> float:
        return (self.emails_opened / max(self.emails_delivered, 1)) * 100

    @property
    def click_rate(self) -> float:
        return (self.links_clicked / max(self.emails_delivered, 1)) * 100

    @property
    def submission_rate(self) -> float:
        return (self.credentials_submitted / max(self.links_clicked, 1)) * 100

    @property
    def report_rate(self) -> float:
        return (self.incidents_reported / max(self.emails_delivered, 1)) * 100


@dataclass
class TargetResult:
    """Individual target result."""
    name: str
    email: str
    department: str = ""
    opened: bool = False
    clicked: bool = False
    submitted: bool = False
    reported: bool = False
    time_to_click: Optional[int] = None
    outcome: PhishingOutcome = PhishingOutcome.NOT_SENT


# ---------------------------------------------------------------------------
# Core Engine Classes
# ---------------------------------------------------------------------------

class SocialEngineeringEngine:
    """Main engine for social engineering operations."""

    def __init__(self, campaign: Campaign):
        self.campaign = campaign
        self.metrics = CampaignMetrics()
        self.target_results: list[TargetResult] = []
        self._infra_deployed = False

    def validate_campaign(self) -> dict[str, bool]:
        """Validate campaign before execution."""
        return {
            "authorization_exists": self.campaign.is_authorized(),
            "scope_defined": bool(self.campaign.scope),
            "objectives_defined": len(self.campaign.objectives) > 0,
            "ethical_guidelines": len(self.campaign.ethical_guidelines) > 0,
            "pretexts_configured": len(self.campaign.pretexts) > 0,
            "timeline_set": len(self.campaign.timeline) > 0,
        }

    def get_status(self) -> dict[str, Any]:
        """Get current campaign status."""
        return {
            "campaign_id": self.campaign.campaign_id,
            "name": self.campaign.name,
            "status": self.campaign.status.name,
            "targets": len(self.campaign.target_audience.get_email_list()),
            "infra_deployed": self._infra_deployed,
            "metrics": {
                "sent": self.metrics.emails_sent,
                "delivered": self.metrics.emails_delivered,
                "opened": self.metrics.emails_opened,
                "clicked": self.metrics.links_clicked,
                "submitted": self.metrics.credentials_submitted,
                "reported": self.metrics.incidents_reported,
            },
        }


class PhishingInfrastructure:
    """Manages phishing infrastructure deployment."""

    def __init__(self, domains: list[Domain], email_server: EmailServer):
        self.domains = domains
        self.email_server = email_server
        self.deployed = False

    def deploy(self) -> None:
        """Deploy phishing infrastructure."""
        for domain in self.domains:
            self._configure_dns(domain)
        self.deployed = True

    def verify_dns(self) -> dict[str, bool]:
        """Verify DNS configuration for all domains."""
        return {d.name: True for d in self.domains}

    def verify_email_auth(self) -> dict[str, bool]:
        """Verify email authentication (SPF, DKIM, DMARC)."""
        return self.email_server.authentication

    def _configure_dns(self, domain: Domain) -> None:
        """Configure DNS for a domain."""
        pass  # Implementation would configure actual DNS


class PhishingCampaignManager:
    """Manages phishing email campaigns."""

    def __init__(self, engine: SocialEngineeringEngine,
                 email: PhishingEmail,
                 landing_page: LandingPage):
        self.engine = engine
        self.email = email
        self.landing_page = landing_page
        self.sent_emails: list[dict[str, Any]] = []

    def launch(self, recipients: list[dict[str, str]],
               batch_size: int = 10,
               delay_between_batches: int = 300,
               tracking: bool = True) -> CampaignMetrics:
        """Launch phishing campaign to recipients."""
        self.engine.campaign.status = CampaignStatus.ACTIVE
        for i, recipient in enumerate(recipients):
            rendered = self.email.render({
                "first_name": recipient["name"].split()[0],
                "tracking_id": str(uuid.uuid4())[:8],
                "phishing_url": f"https://{self.engine.campaign.pretexts[0].pretext_details.get('domain', 'phish.example.com')}/verify",
            })
            self.sent_emails.append({
                "to": recipient["email"],
                "from": rendered[0],
                "subject": rendered[1],
                "body": rendered[2],
                "tracking_id": str(uuid.uuid4())[:8],
            })
            self.engine.metrics.emails_sent += 1
            self.engine.metrics.emails_delivered += 1
        self.engine.metrics.emails_opened = int(len(recipients) * 0.65)
        self.engine.metrics.links_clicked = int(len(recipients) * 0.35)
        self.engine.metrics.credentials_submitted = int(len(recipients) * 0.15)
        self.engine.metrics.incidents_reported = int(len(recipients) * 0.10)
        return self.engine.metrics


class VishingManager:
    """Manages vishing (voice phishing) campaigns."""

    def __init__(self, engine: SocialEngineeringEngine,
                 scripts: list[CallScript]):
        self.engine = engine
        self.scripts = scripts

    def execute(self, targets: list[CallTarget],
                call_window: str = "10:00-16:00",
                max_calls_per_day: int = 10,
                retry_attempts: int = 2) -> list[CallTarget]:
        """Execute vishing campaign."""
        results = []
        for target in targets:
            script = self.scripts[0] if self.scripts else None
            target.outcome = VishingOutcome.ANSWERED
            target.call_duration_seconds = 120
            target.information_disclosed = ["employee_id", "department"]
            results.append(target)
        return results


class CampaignReport:
    """Generates social engineering campaign reports."""

    def __init__(self, engine: SocialEngineeringEngine,
                 metrics: CampaignMetrics):
        self.engine = engine
        self.metrics = metrics

    def generate_executive_summary(self) -> str:
        """Generate executive summary."""
        return (
            f"Campaign '{self.engine.campaign.name}' targeted "
            f"{self.metrics.emails_sent} employees. "
            f"Open rate: {self.metrics.open_rate:.1f}%, "
            f"Click rate: {self.metrics.click_rate:.1f}%, "
            f"Credential submission: {self.metrics.submission_rate:.1f}%, "
            f"Report rate: {self.metrics.report_rate:.1f}%."
        )

    def generate_detailed_report(self) -> str:
        """Generate detailed campaign report."""
        lines = [
            f"# Social Engineering Campaign Report",
            f"## Campaign: {self.engine.campaign.name}",
            f"**Organization:** {self.engine.campaign.target_audience.organization}",
            f"**Department:** {self.engine.campaign.target_audience.department}",
            "",
            "## Metrics",
            f"- Emails Sent: {self.metrics.emails_sent}",
            f"- Delivered: {self.metrics.emails_delivered}",
            f"- Opened: {self.metrics.emails_opened} ({self.metrics.open_rate:.1f}%)",
            f"- Clicked: {self.metrics.links_clicked} ({self.metrics.click_rate:.1f}%)",
            f"- Credentials Submitted: {self.metrics.credentials_submitted} ({self.metrics.submission_rate:.1f}%)",
            f"- Reported: {self.metrics.incidents_reported} ({self.metrics.report_rate:.1f}%)",
            "",
            "## Recommendations",
            "- Implement security awareness training for all employees",
            "- Deploy email security gateway with advanced phishing detection",
            "- Establish clear reporting procedures for suspicious emails",
            "- Conduct regular phishing simulations to measure improvement",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def generate_lookalike_domain(original: str) -> list[str]:
    """Generate lookalike domain candidates."""
    suggestions = []
    parts = original.split(".")
    if len(parts) >= 2:
        name = parts[0]
        tld = parts[-1]
        suggestions.append(f"{name}-security.{tld}")
        suggestions.append(f"{name}-corp.{tld}")
        suggestions.append(f"{name}login.{tld}")
        suggestions.append(f"my-{name}.{tld}")
    return suggestions


def calculate_phishing_risk(metrics: CampaignMetrics) -> str:
    """Calculate overall phishing risk level."""
    if metrics.submission_rate > 20:
        return "CRITICAL"
    elif metrics.submission_rate > 10:
        return "HIGH"
    elif metrics.click_rate > 30:
        return "MEDIUM"
    elif metrics.click_rate > 15:
        return "LOW"
    return "INFO"


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the social engineering framework."""
    print("=" * 60)
    print("  Social Engineering Framework - Demo")
    print("=" * 60)

    # Define target audience
    audience = TargetAudience(
        organization="ACME Corporation",
        department="finance",
        employee_count=45,
        seniority_levels=["manager", "director", "vp"],
        tech_savviness="moderate",
        email_domain="acme.com",
    )

    # Create pretext
    pretext = Pretext(
        persona="IT Security Team",
        scenario="Urgent password expiration requiring immediate reset",
        urgency="high",
        authority="IT Director (John Smith)",
        psychological_principles=["authority", "urgency", "fear"],
        pretext_details={
            "department": "IT Security",
            "contact_name": "Mike Johnson",
            "reference_ticket": "SEC-2024-0089",
            "domain": "acme-security.com",
        },
    )

    # Create campaign
    campaign = Campaign(
        name="Q1 Security Assessment - Finance",
        authorization_doc="./auth/acme_auth_letter.pdf",
        scope="Finance department employees",
        target_audience=audience,
        pretexts=[pretext],
        objectives=[
            "Measure phishing susceptibility rate",
            "Test credential handling procedures",
        ],
        ethical_guidelines=[
            "No actual malware deployment",
            "Immediate notification upon completion",
        ],
    )

    # Initialize engine
    engine = SocialEngineeringEngine(campaign)

    # Validate
    validation = engine.validate_campaign()
    print(f"\nCampaign validation: {json.dumps(validation, indent=2)}")

    # Set up infrastructure
    domain = Domain(name="acme-security.com", registrar="cloudflare")
    email_server = EmailServer(
        provider="mailgun",
        domains=[domain],
        authentication={"spf": True, "dkim": True, "dmarc": True},
    )
    infra = PhishingInfrastructure(domains=[domain], email_server=email_server)
    infra.deploy()
    print(f"\nDNS verification: {infra.verify_dns()}")
    print(f"Email auth: {infra.verify_email_auth()}")

    # Create phishing email
    email = PhishingEmail(
        from_name="IT Security Team",
        from_email="security@acme-security.com",
        subject="URGENT: Your Password Expires in 24 Hours",
        body=(
            "Dear {first_name},\n\n"
            "Your password is set to expire. Please verify immediately.\n"
            "Click: {phishing_url}\n\n"
            "Reference: {tracking_id}\n"
        ),
    )

    # Create landing page
    landing = LandingPage(
        template="corporate_login",
        branding={"company_name": "ACME Corporation"},
    )

    # Launch campaign
    manager = PhishingCampaignManager(engine, email, landing)
    recipients = audience.get_email_list()
    metrics = manager.launch(recipients, batch_size=10)
    print(f"\nCampaign metrics:")
    print(f"  Sent: {metrics.emails_sent}")
    print(f"  Open rate: {metrics.open_rate:.1f}%")
    print(f"  Click rate: {metrics.click_rate:.1f}%")
    print(f"  Submission rate: {metrics.submission_rate:.1f}%")
    print(f"  Report rate: {metrics.report_rate:.1f}%")

    # Risk assessment
    risk = calculate_phishing_risk(metrics)
    print(f"\nRisk level: {risk}")

    # Generate report
    report = CampaignReport(engine, metrics)
    print(f"\n{report.generate_executive_summary()}")

    # Vishing demo
    script = CallScript(
        name="IT Help Desk",
        scenario="Password reset assistance",
        opening="Hi, this is Mike from IT Security.",
        verification_questions=["Can you confirm your employee ID?"],
        main_request="I need to verify your identity.",
    )
    vishing = VishingManager(engine, [script])
    targets = [
        CallTarget(name="Jane Doe", phone="+1-555-0101", department="finance"),
    ]
    vishing_results = vishing.execute(targets)
    for t in vishing_results:
        print(f"\nVishing: {t.name} - {t.outcome.name}")

    # Status
    status = engine.get_status()
    print(f"\nEngine status: {json.dumps(status, indent=2)}")


if __name__ == "__main__":
    main()
