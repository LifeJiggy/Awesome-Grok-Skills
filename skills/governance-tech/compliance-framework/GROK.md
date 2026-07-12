---
name: compliance-framework
category: governance-tech
version: "1.0.0"
tags: [compliance, iso27001, soc2, nist-csf, cobit, governance, risk-management]
difficulty: intermediate
estimated_time: 60min
prerequisites: [governance-foundations, risk-management-basics]
---

# Compliance Framework Management

## Overview

This skill covers the full lifecycle of compliance framework management across major standards: ISO 27001, SOC 2, NIST CSF, and COBIT. It addresses framework selection rationale, control mapping across standards, organizational maturity assessment, gap analysis methodology, and continuous monitoring architectures.

## Framework Selection Methodology

### When to Use Which Framework

| Framework | Best For | Trigger |
|-----------|----------|---------|
| ISO 27001 | International certification, third-party assurance | Customers require ISMS certification |
| SOC 2 | SaaS/service organizations, Trust Services Criteria | Enterprise clients request SOC 2 report |
| NIST CSF | US critical infrastructure, risk-based approach | Federal requirements or voluntary adoption |
| COBIT | IT governance alignment with business goals | Board-level IT governance mandate |

### Selection Decision Tree

1. **Regulatory mandate exists?** → Use the mandated framework
2. **Customer contractual requirement?** → Use the customer-specified framework
3. **No mandate, need international recognition?** → ISO 27001
4. **No mandate, primarily US-based?** → NIST CSF
5. **Service/SaaS organization?** → SOC 2
6. **Board-level IT governance focus?** → COBIT
7. **Multiple frameworks needed?** → Start with NIST CSF (maps to others easily)

## Control Mapping Architecture

### Cross-Framework Control Correspondence

Control mapping establishes equivalences between different frameworks' requirements. This enables:
- Single control satisfaction of multiple framework requirements
- Gap identification when adopting a new framework
- Reduced audit fatigue through shared evidence

### Mapping Strategy

1. **Atomic mapping** — Map individual sub-controls, not entire domains
2. **One-to-many** — A single control often satisfies multiple framework requirements
3. **Coverage gaps** — Some requirements have no equivalent; these need new controls
4. **Evidence reuse** — Mapped controls share audit evidence where control objectives align

### Common Mapping Domains

- **Access Control** — ISO A.9 / SOC 2 CC6 / NIST PR.AC / COBIT DSS05
- **Incident Response** — ISO A.16 / SOC 2 CC7 / NIST RS / COBIT DSS02
- **Risk Assessment** — ISO A.6 / SOC 2 CC3 / NIST ID.RA / COBIT BAI06
- **Change Management** — ISO A.12 / SOC 2 CC8 / NIST PR.IP / COBIT BAI06
- **Business Continuity** — ISO A.17 / SOC 2 A1.2 / NIST RC / COBIT DSS04

## Maturity Assessment Model

### Five-Level Maturity Scale

1. **Initial (Ad-hoc)** — Processes unpredictable, reactive
2. **Developing (Repeatable)** — Basic processes established, inconsistently applied
3. **Defined (Documented)** — Processes standardized, documented, and approved
4. **Managed (Measured)** — Processes measured, controlled, and objectively managed
5. **Optimizing (Continuous)** — Continuous improvement, adaptive, predictive

### Assessment Dimensions

- **Policy & Governance** — Strategy, policy lifecycle, executive sponsorship
- **People & Culture** — Training, awareness, security culture
- **Process & Operations** — Operational procedures, SOPs, runbooks
- **Technology & Tools** — Security tooling, automation, integration
- **Metrics & Reporting** — KPIs, dashboards, board reporting

## Gap Analysis Methodology

### Gap Analysis Process

1. **Define target state** — Select framework and applicable controls
2. **Assess current state** — Evidence-based assessment of existing controls
3. **Identify gaps** — Compare current vs. target, categorize gap severity
4. **Prioritize remediation** — Risk-based prioritization with effort/impact scoring
5. **Create remediation roadmap** — Phased plan with milestones and ownership

### Gap Severity Classification

- **Critical** — No control exists, high-risk requirement unmet
- **Major** — Control exists but incomplete or ineffective
- **Minor** — Control partially implemented, documentation gaps
- **Observation** — Control effective but could be strengthened

## Continuous Monitoring Architecture

### Monitoring Components

1. **Automated evidence collection** — Tool integration for control evidence
2. **Change detection** — Monitor for changes affecting control effectiveness
3. **Exception tracking** — Document and manage control exceptions
4. **Metrics aggregation** — Roll up control status to framework-level posture
5. **Reporting cadence** — Automated compliance posture reports

### Monitoring Frequency by Control Type

| Control Type | Frequency | Method |
|-------------|-----------|--------|
| Configuration | Real-time | Automated scanning |
| Access reviews | Monthly | Identity governance tool |
| Vulnerability management | Weekly | Scanner + ticketing |
| Policy compliance | Quarterly | Automated + manual review |
| Third-party risk | Annually | Assessment questionnaire |
| Penetration testing | Annually | External engagement |

## Implementation Patterns

### Evidence Collection Automation

```
Control Evidence Pipeline:
1. Identify evidence source (tool, system, document)
2. Define collection method (API, export, screenshot)
3. Schedule collection frequency
4. Store in evidence repository with metadata
5. Link to control in compliance tracker
6. Alert on missing or stale evidence
```

### Control Ownership Model

Each control requires:
- **Owner** — Accountable individual for control effectiveness
- **Operator** — Day-to-day executor of the control
- **Assessor** — Independent evaluator of control operating effectiveness
- **Reviewer** — Approves control design and monitors exceptions

## Common Anti-Patterns

1. **Framework shopping** — Choosing easiest framework instead of most appropriate
2. **Copy-paste policies** — Using generic policies without organizational context
3. **Evidence hoarding** — Collecting everything instead of what's needed
4. **Audit-only compliance** — Preparing only for audit dates, not maintaining posture
5. **Control sprawl** — Implementing redundant controls without mapping
6. **Missing continuous monitoring** — Annual assessments leave 11-month gaps

## Integration Points

- **Risk Management** — Framework controls address identified risks
- **Incident Response** — IR procedures satisfy multiple framework requirements
- **Vendor Management** — Third-party assessments feed framework evidence
- **Change Management** — Change processes maintain control effectiveness
- **Business Continuity** — BCP/DR testing satisfies resilience requirements
