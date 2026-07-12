---
name: "social-engineering"
category: "redteam"
version: "1.0.0"
tags: ["redteam", "social-engineering", "phishing", "pretexting", "human-factors"]
---

# Social Engineering Framework

## Overview

The Social Engineering module provides structured methodology and tooling for authorized human-factor security testing. Social engineering remains the most effective initial access vector in real-world attacks — technical defenses are meaningless if an employee hands over credentials or clicks a malicious link. This module covers the full spectrum of social engineering techniques used in professional red team engagements: phishing, pretexting, vishing, physical social engineering, and information elicitation.

This module is designed for authorized red team operations where social engineering is part of the agreed scope. It includes campaign planning, infrastructure setup, payload delivery, tracking, reporting, and remediation guidance. Every interaction is logged for evidence capture and post-engagement debriefing.

Social engineering requires exceptional operational discipline. Unlike technical attacks, social engineering directly involves real people — employees, receptionists, executives. This module emphasizes ethical boundaries, authorization verification, and responsible disclosure to protect both the client's employees and the testing organization.

**Authorization is mandatory.** Social engineering activities must be explicitly authorized in the rules of engagement. Never conduct social engineering without written permission and defined boundaries.

## Core Capabilities

### 1. Campaign Planning & Pretext Development
- Target audience analysis and persona development
- Pretext creation (IT support, vendor, executive, new employee)
- Psychological principle application (authority, urgency, social proof, reciprocity)
- Campaign timeline and milestone planning
- Risk assessment and mitigation strategy

### 2. Phishing Infrastructure & Delivery
- Lookalike domain registration and configuration
- Email authentication setup (SPF, DKIM, DMARC) for legitimacy
- Phishing landing page development and hosting
- Credential harvesting and token capture
- Payload delivery mechanisms (macro documents, ISOs, LNKs, HTML smuggling)
- Email campaign management and tracking

### 3. Pretexting & Vishing
- Phone-based pretext development and scripts
- Help desk impersonation scenarios
- Vendor and partner impersonation
- Executive impersonation (CEO fraud, wire transfer requests)
- IT support social engineering (remote access, credential collection)
- VoIP infrastructure and call recording

### 4. Physical Social Engineering
- Tailgating and piggybacking techniques
- Badge cloning and RFID testing
- Physical access pretext development
- Lock bypass and physical security testing
- USB drop campaigns

### 5. Information Elicitation & OSINT
- Employee information gathering from public sources
- Social media reconnaissance and profiling
- Organizational chart and reporting structure mapping
- Technology stack and process inference from public data
- Breach database correlation for credential exposure

## Usage Examples

### Plan a Social Engineering Campaign

```python
from social_engineering import Campaign, TargetAudience, Pretext

# Define target audience
audience = TargetAudience(
    organization="ACME Corporation",
    department="finance",
    employee_count=45,
    seniority_levels=["manager", "director", "vp"],
    tech_savviness="moderate",
    known_training=["annual_security_awareness"],
    recent_events=["new_hire_orientation", "quarterly_meeting"],
)

# Develop pretext
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
        "deadline": "24 hours",
        "consequence": "Account lockout",
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
        "Evaluate incident reporting behavior",
    ],
    timeline={
        "planning": "2024-01-15 to 2024-01-20",
        "infrastructure": "2024-01-20 to 2024-01-25",
        "execution": "2024-01-25 to 2024-02-01",
        "reporting": "2024-02-01 to 2024-02-05",
    },
    ethical_guidelines=[
        "No actual malware deployment",
        "Credential capture only for demonstration",
        "Immediate notification to IT upon campaign completion",
        "Full debrief with affected employees",
    ],
)
```

### Set Up Phishing Infrastructure

```python
from social_engineering import PhishingInfrastructure, Domain, EmailServer

# Register lookalike domains
domains = [
    Domain(
        name="acme-security.com",
        registrar="authorized_registrar",
        privacy_protection=True,
        auto_renew=True,
        dns_config={
            "mx": "mail.acme-security.com",
            "a": "10.0.0.100",
            "txt": "v=spf1 mx a ip4:10.0.0.100 ~all",
        },
    ),
    Domain(
        name="acme-corp.net",
        registrar="authorized_registrar",
        privacy_protection=True,
    ),
]

# Configure email server
email_server = EmailServer(
    provider="authorized_provider",
    domains=domains,
    authentication={
        "spf": True,
        "dkim": True,
        "dmarc": True,
    },
    warming_period_days=7,
    daily_send_limit=50,
    tracking_enabled=True,
)

# Set up infrastructure
infra = PhishingInfrastructure(domains=domains, email_server=email_server)
infra.deploy()
infra.verify_dns()
infra.verify_email_auth()
```

### Create and Launch Phishing Campaign

```python
from social_engineering import PhishingCampaign, PhishingEmail, LandingPage

# Design phishing email
email = PhishingEmail(
    from_name="IT Security Team",
    from_email="security@acme-security.com",
    subject="URGENT: Your Password Expires in 24 Hours",
    body="""
    Dear {first_name},

    Our security monitoring has detected that your password is set to expire 
    within 24 hours. To prevent account lockout and maintain access to company 
    systems, please verify your credentials immediately.

    Click here to verify: {phishing_url}

    If you do not verify within 24 hours, your account will be temporarily 
    locked per company policy SEC-2024-0089.

    Thank you,
    Mike Johnson
    IT Security Team
    ACME Corporation
    """,
    tracking_id="{tracking_id}",
    reply_to="support@acme-security.com",
)

# Create credential harvesting landing page
landing_page = LandingPage(
    template="corporate_login",
    branding={
        "company_name": "ACME Corporation",
        "logo_url": "https://acme.com/logo.png",
        "colors": {"primary": "#003366", "secondary": "#ffffff"},
    },
    form_action="/collect",
    capture_fields=["username", "password"],
    redirect_after="https://outlook.office365.com",
    ssl_enabled=True,
)

# Launch campaign
campaign = PhishingCampaign(campaign=campaign, email=email, landing_page=landing_page)
results = campaign.launch(
    recipients=audience.get_email_list(),
    batch_size=10,
    delay_between_batches=300,  # seconds
    tracking=True,
)
```

### Track Campaign Results and Generate Report

```python
from social_engineering import CampaignTracker, Report

# Track campaign metrics
tracker = CampaignTracker(campaign)

metrics = tracker.get_metrics()
print(f"Emails sent: {metrics.emails_sent}")
print(f"Emails delivered: {metrics.emails_delivered}")
print(f"Emails opened: {metrics.emails_opened}")
print(f"Links clicked: {metrics.links_clicked}")
print(f"Credentials submitted: {metrics.credentials_submitted}")
print(f"Reports made: {metrics.incidents_reported}")

print(f"\nOpen rate: {metrics.open_rate}%")
print(f"Click rate: {metrics.click_rate}%")
print(f"Submission rate: {metrics.submission_rate}%")
print(f"Report rate: {metrics.report_rate}%")

# Individual-level tracking
for target in metrics.targets:
    if target.clicked or target.submitted:
        print(f"\n{target.name} ({target.department}):")
        print(f"  Opened: {target.opened}")
        print(f"  Clicked: {target.clicked}")
        print(f"  Submitted: {target.submitted}")
        print(f"  Reported: {target.reported}")
        print(f"  Time to click: {target.time_to_click}s")

# Generate report
report = Report(
    campaign=campaign,
    metrics=metrics,
    executive_summary=True,
    individual_results=True,
    recommendations=True,
    remediation_plan=True,
)

report.generate(
    format="docx",
    output_path="./reports/acme_phishing_report.docx",
    include_evidence=True,
    anonymize_results=False,  # True for executive audience
)
```

### Pretexting and Vishing Campaign

```python
from social_engineering import VishingCampaign, CallScript, CallTarget

# Design call scripts
helpdesk_script = CallScript(
    name="IT Help Desk - Password Reset",
    scenario="Help desk calling about password expiration",
    opening="Hi, this is Mike from IT Security. I'm calling about your password expiration notification.",
    verification_questions=[
        "Can you confirm your employee ID?",
        "What department are you in?",
    ],
    main_request="I need to verify your identity to process the password extension.",
    handling_objections={
        "suspicious": "I understand your concern. You can call back at the main IT number to verify.",
        "busy": "I'll schedule a callback at a better time.",
        "refuse": "No problem, but your account will be locked at end of day.",
    },
    closing="Thank you for your cooperation. Your password has been extended.",
    escalation_path="Transfer to IT Manager if employee refuses",
)

# Define call targets
targets = [
    CallTarget(
        name="Jane Doe",
        phone="+1-555-0101",
        department="finance",
        role="Director",
        notes="Known to be helpful, may comply without verification",
    ),
    CallTarget(
        name="Bob Smith",
        phone="+1-555-0102",
        department="engineering",
        role="Manager",
        notes="Security-conscious, may ask for verification",
    ),
]

# Launch vishing campaign
vishing = VishingCampaign(
    campaign=campaign,
    scripts=[helpdesk_script],
    targets=targets,
    caller_id_spoofing=True,
    recording_enabled=True,
    results_tracking=True,
)

results = vishing.execute(
    call_window="10:00-16:00",
    max_calls_per_day=10,
    retry_attempts=2,
)
```

## Best Practices

### Authorization and Ethics
1. **Written authorization is non-negotiable.** Every social engineering activity must be explicitly authorized in the rules of engagement.
2. **Define clear boundaries.** What types of social engineering are permitted? Which departments? What information can be requested?
3. **Include debrief requirements.** Plan for post-campaign employee education and awareness.
4. **Respect employee dignity.** The goal is to test security posture, not embarrass individuals. Report aggregate metrics alongside individual results.

### Operational Security
1. **Use dedicated infrastructure.** Separate phishing domains, email servers, and phone systems from personal infrastructure.
2. **Minimize data collection.** Only collect what's necessary for the engagement. Destroy sensitive data after reporting.
3. **Monitor for real-world impact.** If a phishing campaign inadvertently triggers real incident response, be prepared to coordinate with the client immediately.
4. **Avoid real malware.** Use credential harvesting pages and controlled payloads, not actual malicious software.

### Campaign Design
1. **Research the target organization.** Effective pretexts reflect the organization's actual tools, vendors, and processes.
2. **Layer psychological principles.** Combine authority, urgency, and social proof for realistic campaigns.
3. **Test incrementally.** Start with low-sophistication campaigns before advancing to targeted spear-phishing.
4. **Track everything.** Every interaction should be logged with timestamps for evidence and reporting.

### Reporting
1. **Balance individual and aggregate results.** Executives need organizational metrics; security teams need individual follow-up.
2. **Provide actionable remediation.** Each finding should include specific training recommendations.
3. **Frame positively.** Employees who fall for phishing need training, not punishment. Frame results as organizational improvement opportunities.
4. **Include positive findings.** Employees who reported the phishing attempt deserve recognition.

## Related Modules

- **red-team-operations** — Full-scope adversary simulation incorporating social engineering
- **adversary-emulation** — Threat actor TTP mapping for realistic pretext development
- **offensive-osint** — Open-source intelligence gathering for target research
- **penetration-testing** — Technical testing to complement social engineering findings
- **evidence-hygiene** — Proper handling and redaction of social engineering evidence
- **report-writing** — Professional report authoring for social engineering findings
