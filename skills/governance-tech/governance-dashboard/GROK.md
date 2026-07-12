---
name: governance-dashboard
category: governance-tech
version: "1.0.0"
tags: [dashboard, kpi, compliance-posture, risk-heatmap, executive-reporting, governance]
difficulty: intermediate
estimated_time: 50min
prerequisites: [compliance-framework, audit-systems]
---

# Governance Dashboards

## Overview

This skill covers governance dashboard design and implementation: KPI tracking, compliance posture visualization, risk heatmaps, and executive reporting. Focuses on converting governance, risk, and compliance (GRC) data into actionable intelligence for different stakeholder levels.

## Dashboard Architecture

### Stakeholder Tiers

| Tier | Audience | Focus | Update Frequency |
|------|----------|-------|-----------------|
| Executive | C-suite, Board | Strategic posture, key risks | Monthly/Quarterly |
| Management | Directors, VPs | Operational metrics, trends | Weekly |
| Operational | GRC Team, Analysts | Detailed metrics, exceptions | Real-time/Daily |
| Audit | Internal/External Auditors | Evidence, control status | Per audit cycle |

### Dashboard Hierarchy

```
Executive Summary Dashboard
├── Compliance Posture Dashboard
│   ├── Framework-level compliance %
│   ├── Control status distribution
│   ├── Trend over time
│   └── Top risks
├── Risk Heatmap Dashboard
│   ├── Risk matrix (likelihood × impact)
│   ├── Risk trend analysis
│   ├── Risk appetite comparison
│   └── Top risk contributors
├── Audit Dashboard
│   ├── Audit schedule adherence
│   ├── Finding status and aging
│   ├── Remediation progress
│   └── Repeat finding tracking
├── Regulatory Reporting Dashboard
│   ├── Submission calendar
│   ├── Validation status
│   ├── Deadline tracking
│   └── Submission history
└── Operational Metrics Dashboard
    ├── Control test results
    ├── Exception management
    ├── Training completion
    └── Incident tracking
```

## KPI Framework

### Compliance KPIs

| KPI | Formula | Target | Red Threshold |
|-----|---------|--------|---------------|
| Compliance Rate | (Effective Controls / Total Controls) × 100 | ≥90% | <70% |
| Control Effectiveness | Effective / (Effective + Ineffective) × 100 | ≥95% | <80% |
| Assessment Currency | Controls assessed on time / Total controls × 100 | 100% | <90% |
| Evidence Coverage | Controls with evidence / Total controls × 100 | ≥95% | <80% |
| Exception Rate | Active exceptions / Total controls × 100 | <5% | >15% |

### Risk KPIs

| KPI | Formula | Target | Red Threshold |
|-----|---------|--------|---------------|
| Risk Score Trend | Current risk score vs. prior period | Decreasing | Increasing 3 periods |
| Top 10 Risk Closure | Risks closed in top 10 / Total top 10 risks | ≥50% | <20% |
| Risk Appetite Adherence | Risks within appetite / Total risks | ≥90% | <70% |
| New Risk Rate | New risks identified / Period risks | <20% | >50% |
| Risk Velocity | Average time from identification to closure | <90 days | >180 days |

### Audit KPIs

| KPI | Formula | Target | Red Threshold |
|-----|---------|--------|---------------|
| Audit Coverage | Audits completed / Planned audits × 100 | 100% | <80% |
| Finding Closure Rate | Findings closed on time / Total findings × 100 | ≥90% | <70% |
| Mean Time to Remediate | Total remediation days / Number of findings | <60 days | >120 days |
| Repeat Finding Rate | Repeat findings / Total findings × 100 | <10% | >25% |
| Audit Cycle Time | Average days from planning to report | <45 days | >90 days |

### Reporting KPIs

| KPI | Formula | Target | Red Threshold |
|-----|---------|--------|---------------|
| On-Time Submission | Reports submitted on time / Total reports | 100% | <95% |
| First-Pass Validation | Reports passing validation first time / Total | ≥90% | <70% |
| Data Quality Score | Average validation score across reports | ≥95% | <80% |

## Risk Heatmap Design

### Risk Matrix Structure

```
Impact ↑
  5  │  M   H   H   C   C
  4  │  L   M   H   H   C
  3  │  L   L   M   H   H
  2  │  L   L   L   M   M
  1  │  L   L   L   L   M
     └──────────────────────→
       1    2    3    4    5  Likelihood
```

### Risk Appetite Boundaries

- **Green zone (L-L to M-M)** — Within appetite, monitor
- **Yellow zone (M-H to H-M)** — Near appetite boundary, active management
- **Red zone (H-H to C-C)** — Exceeds appetite, executive escalation required

### Heatmap Data Requirements

Each risk entry needs:
- **Risk ID** — Unique identifier
- **Risk title** — Descriptive name
- **Likelihood** — 1-5 scale (Very Low to Very High)
- **Impact** — 1-5 scale (Negligible to Catastrophic)
- **Risk score** — Likelihood × Impact
- **Risk owner** — Accountable individual
- **Category** — Risk category (strategic, operational, financial, compliance)
- **Treatment** — Accept, mitigate, transfer, avoid
- **Last assessed** — Date of most recent assessment

## Compliance Posture Visualization

### Posture Score Calculation

```
Posture Score = (
    Framework Compliance × 0.30 +
    Control Effectiveness × 0.25 +
    Risk Posture × 0.20 +
    Audit Health × 0.15 +
    Reporting Compliance × 0.10
) × 100
```

### Posture Categories

- **Strong (80-100)** — Controls effective, risks within appetite, audits on track
- **Adequate (60-79)** — Mostly effective, some areas need attention
- **Needs Improvement (40-59)** — Significant gaps, active remediation required
- **Weak (0-39)** — Critical gaps, executive intervention required

### Posture Trend Analysis

Track posture scores over time to identify:
- **Improving trend** — Remediation efforts working
- **Declining trend** — New risks or control degradation
- **Stable at target** — Sustained effective governance
- **Volatile** — Inconsistent control effectiveness

## Executive Reporting

### Executive Summary Structure

1. **Overall posture rating** — Single score with trend arrow
2. **Key metrics dashboard** — 5-7 critical KPIs
3. **Top 5 risks** — Highest-rated risks requiring attention
4. **Critical findings** — Findings requiring executive action
5. **Upcoming deadlines** — Regulatory submissions due in next 30 days
6. **Recommendations** — Prioritized actions for the board/executive team

### Board Report Format

```
GOVERNANCE POSTURE - [Period]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POSTURE SCORE: [XX/100] [↑↓→]

COMPLIANCE: [XX]% effective controls
RISK: [X] critical/high risks open
AUDIT: [X] findings outstanding (X overdue)
REPORTING: [X/X] submissions on time

TOP RISKS:
1. [Risk title] - Score: [X] - Owner: [Name]
2. ...

CRITICAL FINDINGS:
1. [Finding title] - Due: [Date] - Status: [Status]
2. ...

RECOMMENDATIONS:
1. [Action item]
2. ...
```

## Dashboard Implementation Patterns

### Data Aggregation Layer

```
Source Systems → ETL Pipeline → Data Warehouse → Dashboard API → Frontend
    ↓              ↓                ↓                ↓              ↓
  ERP/CRM      Transform        Aggregated        REST/GraphQL   Charts/
  Logs         Normalize        KPIs               Endpoints     Tables
  GRC Tools    Enrich           Metrics                          Alerts
```

### Real-Time vs. Batch Updates

| Data Type | Update Method | Frequency | Latency Tolerance |
|-----------|--------------|-----------|-------------------|
| Risk scores | Batch | Daily | 24 hours |
| Control status | Batch | Weekly | 7 days |
| Finding status | Near real-time | On change | 1 hour |
| KPI metrics | Batch | Daily | 24 hours |
| Alert triggers | Real-time | Immediate | 5 minutes |

### Dashboard Refresh Strategy

1. **Critical alerts** — Push notification on state change
2. **Operational metrics** — Refresh every 4 hours during business hours
3. **Management reports** — Daily batch refresh
4. **Executive dashboards** — Weekly refresh with weekly email summary
5. **Board materials** — Generated on-demand before meetings

## Common Anti-Patterns

1. **Vanity metrics** — Showing metrics that look good but don't drive action
2. **Dashboard overload** — Too many dashboards, nobody uses them
3. **Data without context** — Numbers without benchmarks or trends
4. **Static dashboards** — Never updated, lose credibility
5. **One-size-fits-all** — Same dashboard for executives and analysts
6. **Metric gaming** — Optimizing metrics instead of actual governance
7. **Alert fatigue** — Too many alerts, all ignored
8. **Missing drill-down** — Can't go from summary to detail
