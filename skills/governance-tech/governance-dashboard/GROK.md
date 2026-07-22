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

## Advanced Configuration

### Dashboard Configuration

```yaml
dashboards:
  executive:
    refresh_interval: "weekly"
    layout: "grid"
    charts:
      - type: "gauge"
        metric: "posture_score"
        thresholds:
          green: 80
          yellow: 60
          red: 40
          
      - type: "line"
        metric: "risk_score_trend"
        period: "12_months"
        
      - type: "pie"
        metric: "control_status_distribution"
        
      - type: "table"
        metric: "top_5_risks"
        columns: ["title", "score", "owner", "status"]
        
  management:
    refresh_interval: "daily"
    layout: "tabs"
    tabs:
      - name: "Compliance"
        charts:
          - type: "bar"
            metric: "framework_compliance"
            
          - type: "heatmap"
            metric: "control_effectiveness_by_domain"
            
      - name: "Risk"
        charts:
          - type: "matrix"
            metric: "risk_heatmap"
            
          - type: "line"
            metric: "risk_trend"
            
      - name: "Audit"
        charts:
          - type: "gantt"
            metric: "audit_schedule"
            
          - type: "stacked_bar"
            metric: "finding_status_by_severity"
            
  operational:
    refresh_interval: "real_time"
    layout: "multi_panel"
    panels:
      - name: "Control Testing"
        charts:
          - type: "progress"
            metric: "testing_completion"
            
          - type: "table"
            metric: "recent_test_results"
            
      - name: "Exceptions"
        charts:
          - type: "timeline"
            metric: "exception_aging"
            
          - type: "pie"
            metric: "exception_status"
            
      - name: "Training"
        charts:
          - type: "bar"
            metric: "training_completion_by_department"
            
          - type: "line"
            metric: "certification_expiration"
```

### KPI Configuration

```yaml
kpis:
  compliance:
    compliance_rate:
      formula: "(effective_controls / total_controls) * 100"
      target: 90
      red_threshold: 70
      yellow_threshold: 80
      unit: "%"
      owner: "CISO"
      
    control_effectiveness:
      formula: "(effective / (effective + ineffective)) * 100"
      target: 95
      red_threshold: 80
      yellow_threshold: 90
      unit: "%"
      owner: "GRC Manager"
      
    assessment_currency:
      formula: "(controls_assessed_on_time / total_controls) * 100"
      target: 100
      red_threshold: 90
      yellow_threshold: 95
      unit: "%"
      owner: "Audit Manager"
      
  risk:
    risk_score_trend:
      formula: "current_score - prior_period_score"
      target: "<=0"
      red_threshold: ">5 increase for 3 periods"
      unit: "score"
      owner: "Risk Manager"
      
    top_risk_closure:
      formula: "(risks_closed_in_top_10 / total_top_10_risks) * 100"
      target: 50
      red_threshold: 20
      unit: "%"
      owner: "Risk Manager"
      
    risk_appetite_adherence:
      formula: "(risks_within_appetite / total_risks) * 100"
      target: 90
      red_threshold: 70
      unit: "%"
      owner: "CRO"
      
  audit:
    audit_coverage:
      formula: "(audits_completed / planned_audits) * 100"
      target: 100
      red_threshold: 80
      unit: "%"
      owner: "Internal Audit"
      
    finding_closure_rate:
      formula: "(findings_closed_on_time / total_findings) * 100"
      target: 90
      red_threshold: 70
      unit: "%"
      owner: "Audit Manager"
      
    mean_time_to_remediate:
      formula: "total_remediation_days / number_of_findings"
      target: 60
      red_threshold: 120
      unit: "days"
      owner: "Compliance Officer"
      
  reporting:
    on_time_submission:
      formula: "(reports_submitted_on_time / total_reports) * 100"
      target: 100
      red_threshold: 95
      unit: "%"
      owner: "Compliance Officer"
      
    first_pass_validation:
      formula: "(reports_passing_first_time / total_reports) * 100"
      target: 90
      red_threshold: 70
      unit: "%"
      owner: "Data Quality Manager"
```

### Alert Configuration

```yaml
alerts:
  channels:
    - type: "email"
      recipients:
        - role: "executive"
          address: "exec-team@company.com"
        - role: "grc"
          address: "grc-team@company.com"
          
    - type: "slack"
      channel: "#governance-alerts"
      webhook_url: "${SLACK_WEBHOOK_URL}"
      
    - type: "pagerduty"
      service_key: "${PAGERDUTY_SERVICE_KEY}"
      
    - type: "webhook"
      url: "https://grc.company.com/api/alerts"
      method: "POST"
      
  rules:
    - name: "critical_risk_escalation"
      condition: "risk_score >= 20"
      severity: "critical"
      channels: ["email", "slack", "pagerduty"]
      recipients: ["executive", "risk_manager"]
      
    - name: "compliance_rate_drop"
      condition: "compliance_rate < 70"
      severity: "high"
      channels: ["email", "slack"]
      recipients: ["grc", "ciso"]
      
    - name: "audit_overdue"
      condition: "audit_overdue_count > 5"
      severity: "medium"
      channels: ["email"]
      recipients: ["audit_manager"]
      
    - name: "reporting_deadline"
      condition: "days_to_deadline <= 7 AND status != 'submitted'"
      severity: "high"
      channels: ["email", "slack"]
      recipients: ["compliance_officer"]
      
    - name: "training_expiring"
      condition: "days_to_certification_expiry <= 30"
      severity: "low"
      channels: ["email"]
      recipients: ["employee", "manager"]
```

## Architecture Patterns

### Data Aggregation Engine

```python
class DataAggregationEngine:
    def __init__(self, source_connectors, transformation_rules):
        self.connectors = source_connectors
        self.rules = transformation_rules
    
    async def aggregate_kpis(self, kpi_definitions: List[KPIDefinition]) -> List[KPIValue]:
        kpi_values = []
        
        for kpi_def in kpi_definitions:
            # Get data from source
            raw_data = await self.connectors[kpi_def.source].fetch_data(
                kpi_def.query,
                kpi_def.time_range,
            )
            
            # Apply transformation
            transformed = self.apply_transformation(raw_data, kpi_def.formula)
            
            # Calculate value
            value = self.calculate_value(transformed)
            
            # Determine status
            status = self.determine_status(value, kpi_def)
            
            kpi_values.append(KPIValue(
                kpi_id=kpi_def.kpi_id,
                name=kpi_def.name,
                value=value,
                unit=kpi_def.unit,
                status=status,
                trend=self.calculate_trend(kpi_def.kpi_id, value),
                timestamp=datetime.utcnow(),
            ))
        
        return kpi_values
    
    def determine_status(self, value: float, kpi_def: KPIDefinition) -> str:
        if value >= kpi_def.target:
            return "green"
        elif value >= kpi_def.yellow_threshold:
            return "yellow"
        else:
            return "red"
```

### Risk Heatmap Generator

```python
class RiskHeatmapGenerator:
    def __init__(self, risk_data_source, color_palette):
        self.risk_data = risk_data_source
        self.colors = color_palette
    
    async def generate_heatmap(self, filters: Dict) -> RiskHeatmap:
        # Get risks
        risks = await self.risk_data.get_risks(filters)
        
        # Initialize matrix
        matrix = [[[] for _ in range(5)] for _ in range(5)]
        
        # Populate matrix
        for risk in risks:
            likelihood_idx = risk.likelihood - 1
            impact_idx = risk.impact - 1
            matrix[likelihood_idx][impact_idx].append(risk)
        
        # Calculate cell totals
        cell_totals = self.calculate_cell_totals(matrix)
        
        # Determine risk zones
        zones = self.determine_zones(matrix)
        
        return RiskHeatmap(
            matrix=matrix,
            cell_totals=cell_totals,
            zones=zones,
            total_risks=len(risks),
            risks_by_zone=self.count_risks_by_zone(zones),
            filters=filters,
        )
    
    def determine_zones(self, matrix):
        zones = {
            "green": [],  # Low-Low to Medium-Medium
            "yellow": [],  # Medium-High to High-Medium
            "red": [],  # High-High to Critical-Critical
        }
        
        for i in range(5):
            for j in range(5):
                score = (i + 1) * (j + 1)
                if score <= 9:
                    zones["green"].append((i, j))
                elif score <= 15:
                    zones["yellow"].append((i, j))
                else:
                    zones["red"].append((i, j))
        
        return zones
```

### Compliance Posture Calculator

```python
class CompliancePostureCalculator:
    def __init__(self, compliance_data, risk_data, audit_data, reporting_data):
        self.compliance = compliance_data
        self.risk = risk_data
        self.audit = audit_data
        self.reporting = reporting_data
    
    async def calculate_posture(self) -> CompliancePosture:
        # Get component scores
        compliance_score = await self.compliance.get_framework_compliance()
        control_effectiveness = await self.compliance.get_control_effectiveness()
        risk_posture = await self.risk.get_risk_posture_score()
        audit_health = await self.audit.get_audit_health_score()
        reporting_compliance = await self.reporting.get_reporting_compliance()
        
        # Calculate weighted posture score
        posture_score = (
            compliance_score * 0.30 +
            control_effectiveness * 0.25 +
            risk_posture * 0.20 +
            audit_health * 0.15 +
            reporting_compliance * 0.10
        )
        
        # Determine posture category
        if posture_score >= 80:
            category = "strong"
        elif posture_score >= 60:
            category = "adequate"
        elif posture_score >= 40:
            category = "needs_improvement"
        else:
            category = "weak"
        
        # Calculate trend
        trend = await self.calculate_trend(posture_score)
        
        return CompliancePosture(
            posture_score=posture_score,
            category=category,
            trend=trend,
            components={
                "compliance": compliance_score,
                "control_effectiveness": control_effectiveness,
                "risk_posture": risk_posture,
                "audit_health": audit_health,
                "reporting_compliance": reporting_compliance,
            },
            timestamp=datetime.utcnow(),
        )
```

### Executive Report Generator

```python
class ExecutiveReportGenerator:
    def __init__(self, posture_calculator, risk_data, finding_data, deadline_data):
        self.posture_calc = posture_calculator
        self.risks = risk_data
        self.findings = finding_data
        self.deadlines = deadline_data
    
    async def generate_report(self, period: str) -> ExecutiveReport:
        # Get posture
        posture = await self.posture_calc.calculate_posture()
        
        # Get top risks
        top_risks = await self.risks.get_top_risks(limit=5)
        
        # Get critical findings
        critical_findings = await self.findings.get_critical_findings()
        
        # Get upcoming deadlines
        upcoming_deadlines = await self.deadlines.get_upcoming(days=30)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(
            posture, top_risks, critical_findings
        )
        
        return ExecutiveReport(
            period=period,
            posture=posture,
            top_risks=top_risks,
            critical_findings=critical_findings,
            upcoming_deadlines=upcoming_deadlines,
            recommendations=recommendations,
            generated_at=datetime.utcnow(),
        )
```

## Integration Guide

### GRC Platform Integration

```python
class GRCPlatformIntegration:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
    
    async def get_controls(self) -> List[Control]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/controls",
                headers=headers,
            )
        
        return self.parse_controls(response.json())
    
    async def get_risks(self) -> List[Risk]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/risks",
                headers=headers,
            )
        
        return self.parse_risks(response.json())
    
    async def get_findings(self) -> List[Finding]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/findings",
                headers=headers,
            )
        
        return self.parse_findings(response.json())
```

### BI Tool Integration

```python
class BIToolIntegration:
    def __init__(self, tool_name: str, connection_string: str):
        self.tool_name = tool_name
        self.connection = connection_string
    
    async def create_dashboard(self, dashboard_config: DashboardConfig) -> Dashboard:
        if self.tool_name == "tableau":
            return await self.create_tableau_dashboard(dashboard_config)
        elif self.tool_name == "powerbi":
            return await self.create_powerbi_dashboard(dashboard_config)
        elif self.tool_name == "looker":
            return await self.create_looker_dashboard(dashboard_config)
    
    async def refresh_data(self, dashboard_id: str) -> RefreshResult:
        # Trigger data refresh
        await self.trigger_refresh(dashboard_id)
        
        # Wait for completion
        status = await self.wait_for_refresh(dashboard_id)
        
        return RefreshResult(
            dashboard_id=dashboard_id,
            status=status,
            refreshed_at=datetime.utcnow(),
        )
```

### Alert System Integration

```python
class AlertSystemIntegration:
    def __init__(self, alert_config: AlertConfig):
        self.config = alert_config
    
    async def send_alert(self, alert: Alert) -> AlertResult:
        results = []
        
        for channel in alert.channels:
            if channel.type == "email":
                result = await self.send_email(alert, channel)
            elif channel.type == "slack":
                result = await self.send_slack(alert, channel)
            elif channel.type == "pagerduty":
                result = await self.send_pagerduty(alert, channel)
            elif channel.type == "webhook":
                result = await self.send_webhook(alert, channel)
            
            results.append(result)
        
        return AlertResult(
            alert_id=alert.alert_id,
            channels_notified=len(results),
            successful=len([r for r in results if r.success]),
            failed=len([r for r in results if not r.success]),
        )
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_kpis_name_date ON kpi_values (kpi_name, calculated_at DESC);
CREATE INDEX idx_risks_score ON risks (risk_score DESC);
CREATE INDEX idx_findings_status ON findings (status, severity);
CREATE INDEX idx_controls_effective ON controls (is_effective, framework);

-- Create materialized view for posture calculation
CREATE MATERIALIZED VIEW compliance_posture_summary AS
SELECT 
    DATE(calculated_at) as calculation_date,
    AVG(CASE WHEN is_effective THEN 100 ELSE 0 END) as compliance_rate,
    COUNT(*) as total_controls,
    SUM(CASE WHEN is_effective THEN 1 ELSE 0 END) as effective_controls
FROM controls
GROUP BY DATE(calculated_at);

-- Partition KPI values by month
CREATE TABLE kpi_values (
    id UUID PRIMARY KEY,
    kpi_name VARCHAR(100),
    value DECIMAL(10,2),
    unit VARCHAR(20),
    status VARCHAR(20),
    calculated_at TIMESTAMP
) PARTITION BY RANGE (calculated_at);
```

### Caching Strategy

```python
class GovernanceDashboardCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get_kpi_value(self, kpi_name: str) -> Optional[KPIValue]:
        cache_key = f"kpi:{kpi_name}"
        cached = await self.redis.get(cache_key)
        if cached:
            return KPIValue.from_json(cached)
        return None
    
    async def cache_kpi_value(self, kpi_name: str, value: KPIValue):
        cache_key = f"kpi:{kpi_name}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            value.to_json()
        )
    
    async def get_posture_score(self) -> Optional[float]:
        cache_key = "posture_score"
        cached = await self.redis.get(cache_key)
        if cached:
            return float(cached)
        return None
    
    async def cache_posture_score(self, score: float):
        cache_key = "posture_score"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            str(score)
        )
```

### Batch Processing

```python
class GovernanceBatchProcessor:
    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size
    
    async def process_batch(self, items: List, processor: Callable):
        batches = [
            items[i:i+self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*[
                processor(item) for item in batch
            ])
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Data Encryption

```python
from cryptography.fernet import Fernet

class GovernanceDataEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive governance data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive governance data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class GovernanceAccessControl:
    def __init__(self):
        self.permissions = {}
        self.roles = {}
    
    def check_permission(self, user_id: str, action: str) -> bool:
        user_roles = self.roles.get(user_id, [])
        for role in user_roles:
            role_permissions = self.permissions.get(role, [])
            if action in role_permissions:
                return True
        return False
    
    def grant_role(self, user_id: str, role: str):
        if user_id not in self.roles:
            self.roles[user_id] = []
        self.roles[user_id].append(role)
```

### Audit Logging

```python
class GovernanceAuditLogger:
    def __init__(self, db):
        self.db = db
    
    async def log_event(self, event: AuditEvent):
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'actor_id': event.actor_id,
            'action': event.action,
            'resource_id': event.resource_id,
            'details': event.details,
            'ip_address': event.ip_address,
            'user_agent': event.user_agent,
        }
        
        await self.db.audit_logs.insert(audit_entry)
```

## Troubleshooting Guide

### Common Issues

**Issue: Dashboard data not refreshing**
```python
async def diagnose_dashboard_refresh(dashboard_id: str):
    # Check data sources
    sources = await get_data_sources(dashboard_id)
    
    print(f"Dashboard {dashboard_id}:")
    for source in sources:
        status = await check_source_status(source)
        print(f"  {source.name}: {status}")
        
        if status != "healthy":
            print(f"    WARNING: Source unhealthy")
            print(f"    Recommendation: Check connectivity and credentials")
    
    # Check refresh schedule
    schedule = await get_refresh_schedule(dashboard_id)
    print(f"\nRefresh schedule: {schedule}")
    
    # Check last refresh
    last_refresh = await get_last_refresh(dashboard_id)
    print(f"Last refresh: {last_refresh}")
```

**Issue: KPI calculation errors**
```python
async def diagnose_kpi_errors(kpi_name: str):
    # Get KPI definition
    kpi_def = await get_kpi_definition(kpi_name)
    print(f"KPI: {kpi_name}")
    print(f"  Formula: {kpi_def.formula}")
    print(f"  Source: {kpi_def.source}")
    
    # Get raw data
    raw_data = await fetch_raw_data(kpi_def)
    print(f"  Raw data points: {len(raw_data)}")
    
    # Calculate manually
    calculated = await calculate_kpi(kpi_def, raw_data)
    print(f"  Calculated value: {calculated}")
    
    # Compare with stored value
    stored = await get_stored_kpi_value(kpi_name)
    print(f"  Stored value: {stored}")
    
    if abs(calculated - stored) > 0.01:
        print(f"  WARNING: Calculation mismatch")
        print(f"  Recommendation: Recalculate and update")
```

**Issue: Alert not triggering**
```python
async def diagnose_alert_failure(alert_rule: str):
    # Get alert rule
    rule = await get_alert_rule(alert_rule)
    print(f"Alert rule: {alert_rule}")
    print(f"  Condition: {rule.condition}")
    print(f"  Channels: {rule.channels}")
    
    # Check data
    data = await fetch_alert_data(rule)
    print(f"  Current value: {data.value}")
    print(f"  Threshold: {rule.threshold}")
    
    # Check if condition met
    condition_met = evaluate_condition(data.value, rule.condition)
    print(f"  Condition met: {condition_met}")
    
    if not condition_met:
        print(f"  INFO: Condition not met, alert not triggered")
    else:
        print(f"  WARNING: Condition met but alert not sent")
        
        # Check channels
        for channel in rule.channels:
            status = await check_channel_status(channel)
            print(f"  Channel {channel.type}: {status}")
            
            if status != "healthy":
                print(f"    Recommendation: Check channel configuration")
```

## API Reference

### Dashboard API

```python
# Get dashboard data
GET /api/v1/dashboards/{dashboard_id}
Response:
{
    "dashboard_id": "EXEC-001",
    "name": "Executive Dashboard",
    "kpis": [
        {
            "name": "Compliance Rate",
            "value": 92.5,
            "unit": "%",
            "status": "green",
            "trend": "increasing"
        }
    ],
    "last_refreshed": "2026-07-01T08:00:00Z"
}

# Refresh dashboard
POST /api/v1/dashboards/{dashboard_id}/refresh
Response:
{
    "status": "refreshing",
    "estimated_completion": "2026-07-01T08:05:00Z"
}
```

### KPI API

```python
# Get KPI value
GET /api/v1/kpis/{kpi_name}
Response:
{
    "kpi_name": "Compliance Rate",
    "value": 92.5,
    "unit": "%",
    "status": "green",
    "trend": "increasing",
    "target": 90,
    "thresholds": {
        "green": 90,
        "yellow": 80,
        "red": 70
    },
    "calculated_at": "2026-07-01T08:00:00Z"
}

# Get KPI history
GET /api/v1/kpis/{kpi_name}/history
Query Parameters:
  - period: 30d
  - granularity: daily
Response:
{
    "kpi_name": "Compliance Rate",
    "history": [
        {"date": "2026-06-01", "value": 88.5},
        {"date": "2026-06-02", "value": 89.2},
        ...
    ]
}
```

### Risk Heatmap API

```python
# Get risk heatmap
GET /api/v1/risks/heatmap
Query Parameters:
  - category: all
  - owner: all
Response:
{
    "matrix": [
        [{"count": 2, "risks": [...]}, ...],
        ...
    ],
    "zones": {
        "green": 15,
        "yellow": 8,
        "red": 3
    },
    "total_risks": 26,
    "filters": {}
}
```

## Data Models

### KPI Model

```python
class KPI:
    kpi_id: str
    name: str
    description: str
    formula: str
    source: str
    target: float
    yellow_threshold: float
    red_threshold: float
    unit: str
    owner: str
    category: str  # compliance, risk, audit, reporting
    created_at: datetime
    updated_at: datetime
```

### KPI Value Model

```python
class KPIValue:
    value_id: str
    kpi_id: str
    name: str
    value: float
    unit: str
    status: str  # green, yellow, red
    trend: str  # increasing, decreasing, stable
    target: float
    calculated_at: datetime
```

### Risk Model

```python
class Risk:
    risk_id: str
    title: str
    description: str
    likelihood: int  # 1-5
    impact: int  # 1-5
    risk_score: int  # likelihood * impact
    category: str
    owner: str
    treatment: str  # accept, mitigate, transfer, avoid
    status: str  # open, in_progress, closed
    last_assessed: datetime
    created_at: datetime
    updated_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: governance-dashboard-service
  namespace: governance-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: governance-dashboard-service
  template:
    metadata:
      labels:
        app: governance-dashboard-service
    spec:
      containers:
      - name: governance-dashboard
        image: your-registry/governance-dashboard-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8443
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8443
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Database Migration

```bash
# Run migrations
alembic upgrade head

# Verify migration status
alembic current

# Rollback if needed
alembic downgrade -1
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Dashboard metrics
dashboard_refresh_counter = Counter(
    'governance_dashboard_refresh_total',
    'Total dashboard refreshes',
    ['dashboard_id', 'status']
)

dashboard_refresh_duration = Histogram(
    'governance_dashboard_refresh_duration_seconds',
    'Dashboard refresh duration',
    ['dashboard_id'],
    buckets=[10, 30, 60, 120, 300]
)

# KPI metrics
kpi_calculation_counter = Counter(
    'governance_kpi_calculation_total',
    'Total KPI calculations',
    ['kpi_name', 'status']
)

kpi_value_gauge = Gauge(
    'governance_kpi_value',
    'Current KPI value',
    ['kpi_name', 'status']
)

# Alert metrics
alerts_triggered_counter = Counter(
    'governance_alerts_triggered_total',
    'Total alerts triggered',
    ['rule_name', 'channel']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Governance Dashboard Monitoring",
    "panels": [
      {
        "title": "Dashboard Refresh Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(governance_dashboard_refresh_total[5m])",
            "legendFormat": "{{dashboard_id}} - {{status}}"
          }
        ]
      },
      {
        "title": "KPI Values",
        "type": "gauge",
        "targets": [
          {
            "expr": "governance_kpi_value",
            "legendFormat": "{{kpi_name}}"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
groups:
- name: governance_alerts
  rules:
  - alert: DashboardRefreshFailed
    expr: rate(governance_dashboard_refresh_total{status="failed"}[5m]) > 0
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Dashboard refresh failure detected"
      
  - alert: KPIValueStale
    expr: time() - governance_kpi_last_calculated > 86400
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "KPI values not updated in 24 hours"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestKPICalculation:
    def test_calculate_compliance_rate(self, kpi_calculator):
        effective = 85
        total = 100
        
        rate = kpi_calculator.calculate_compliance_rate(effective, total)
        
        assert rate == 85.0
    
    def test_determine_kpi_status(self, kpi_calculator):
        # Green
        assert kpi_calculator.determine_status(95, 90, 80, 70) == "green"
        
        # Yellow
        assert kpi_calculator.determine_status(85, 90, 80, 70) == "yellow"
        
        # Red
        assert kpi_calculator.determine_status(75, 90, 80, 70) == "red"
```

### Integration Tests

```python
class TestEndToEndGovernance:
    async def test_dashboard_generation(self, governance_system):
        # Generate dashboard
        dashboard = await governance_system.generate_dashboard(
            dashboard_type="executive",
        )
        
        assert dashboard.dashboard_id is not None
        assert len(dashboard.kpis) > 0
        
        # Get dashboard data
        data = await governance_system.get_dashboard_data(dashboard.dashboard_id)
        assert data.kpis is not None
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class GovernanceUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def get_dashboard(self):
        self.client.get(f"/api/v1/dashboards/dashboard-{self.dashboard_counter}")
        self.dashboard_counter += 1
    
    @task(5)
    def get_kpi(self):
        self.client.get(f"/api/v1/kpis/kpi-{self.kpi_counter}")
        self.kpi_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/dashboards", methods=["GET"])
@app.route("/api/v2/dashboards", methods=["GET"])
async def get_dashboards():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await get_dashboards_v2()
    return await get_dashboards_v1()
```

### Database Migration Strategy

```bash
# Forward migration
alembic upgrade head

# Specific version
alembic upgrade ae1027a6555

# Downgrade
alembic downgrade -1
```

## Glossary

- **GRC**: Governance, Risk, and Compliance
- **KPI**: Key Performance Indicator
- **Risk Appetite**: Amount of risk organization is willing to accept
- **Risk Heatmap**: Visual representation of risks by likelihood and impact
- **Control Effectiveness**: Measure of how well controls achieve objectives
- **Compliance Rate**: Percentage of controls that are effective
- **Finding Closure Rate**: Percentage of audit findings remediated on time
- **Mean Time to Remediate**: Average time to close audit findings
- **Risk Velocity**: Speed at which risks are identified and closed
- **Posture Score**: Composite score of governance effectiveness

## Changelog

### Version 2.0.0 (2026-07-01)
- Added real-time dashboard updates
- Implemented predictive analytics
- Enhanced alert system
- Added mobile-responsive design

### Version 1.5.0 (2026-01-15)
- Added risk heatmap
- Implemented KPI tracking
- Enhanced executive reporting

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic dashboard functionality
- Compliance tracking

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def calculate_posture_score(
    compliance_score: float,
    risk_score: float,
    audit_score: float,
) -> float:
    """Calculate overall compliance posture score.
    
    Args:
        compliance_score: Framework compliance percentage.
        risk_score: Risk posture score.
        audit_score: Audit health score.
    
    Returns:
        Posture score between 0 and 100.
    """
    pass
```

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from team lead
6. Address review comments
7. Merge after approval

## License

MIT License

Copyright (c) 2026 Governance Dashboard Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
