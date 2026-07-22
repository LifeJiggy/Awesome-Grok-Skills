---
name: "compliance-automation"
category: "fintech"
version: "2.0.0"
tags: ["fintech", "compliance", "regtech", "aml", "kyc", "regulatory"]
difficulty: "advanced"
estimated_time: "40-55 minutes"
prerequisites: ["python", "financial-regulation-basics"]
---

# Compliance Automation

## Overview

Compliance automation provides systematic tools for meeting financial regulatory requirements including KYC (Know Your Customer), AML (Anti-Money Laundering), sanctions screening, regulatory reporting, and audit trail management. This module automates the detection, monitoring, and reporting of compliance-relevant activities, reducing manual review burden while improving detection accuracy and audit readiness.

## Core Capabilities

- **KYC/CDD Automation**: Customer due diligence workflow automation with document verification, identity proofing, and beneficial ownership identification
- **AML Transaction Monitoring**: Real-time and batch transaction monitoring against configurable rules for structuring, layering, and suspicious patterns
- **Sanctions Screening**: OFAC, EU, UN, and local sanctions list screening with fuzzy matching, alias detection, and batch processing
- **Regulatory Reporting**: Automated SAR (Suspicious Activity Report), CTR (Currency Transaction Report), and jurisdiction-specific regulatory filing
- **Audit Trail Management**: Immutable audit logging with tamper-evident chains, retention management, and regulatory examination support
- **Policy Management**: Compliance policy versioning, attestation tracking, and exception management workflows
- **Risk Assessment**: Periodic BSA/AML risk assessments with automated data collection and scoring
- **Training & Certification**: Compliance training tracking, certification management, and knowledge assessment

## Usage Examples

### KYC/CDD Workflow

```python
from fintech.compliance_automation import KYCWorkflow, CustomerRiskTier

workflow = KYCWorkflow(
    jurisdiction="US",
    enhanced_due_diligence_threshold=1_000_000,
)

# Process customer through KYC
result = workflow.process_customer(
    customer_id="CUST-001",
    customer_type="individual",
    documents=[
        {"type": "passport", "number": "P12345678", "country": "US"},
        {"type": "proof_of_address", "provider": "utility_bill", "age_days": 30},
    ],
    source_of_funds="employment",
    expected_transaction_volume="moderate",
)

print(f"KYC Status: {result.status}")
print(f"Risk Tier: {result.risk_tier.value}")
print(f"Next Review: {result.next_review_date}")
```

### Sanctions Screening

```python
from fintech.compliance_automation import SanctionsScreener

screener = SanctionsScreener(
    lists=["OFAC_SDN", "EU_SANCTIONS", "UN_SANCTIONS", "PEP"],
    fuzzy_threshold=0.85,
    alias_expansion=True,
)

# Screen an entity
matches = screener.screen(
    name="Mohammed Al-Rashid",
    date_of_birth="1985-03-15",
    nationality="AE",
    document_number="E12345678",
)

print(f"Match Found: {matches.has_match}")
if matches.has_match:
    for match in matches.matches:
        print(f"  List: {match.list_name}, Score: {match.score:.2f}")
        print(f"  Entity: {match.entity_name}, Type: {match.entity_type}")
```

### SAR Filing

```python
from fintech.compliance_automation, import SARFiling

filing = SARFiling(
    agency="FinCEN",
    filing_type="initial",
    auto_narrative=True,
)

# Generate SAR from alert
sar = filing.generate_sar(
    alert_id="AML-001",
    subject={
        "name": "John Doe", "dob": "1980-01-15",
        "address": "123 Main St", "ssn_last4": "6789",
    },
    suspicious_activity={
        "type": "structuring",
        "description": "Multiple cash deposits just below $10,000 reporting threshold",
        "amount": 47500,
        "date_range": ("2026-06-01", "2026-06-30"),
        "transactions": ["TXN-001", "TXN-002", "TXN-003"],
    },
)

print(f"SAR Number: {sar.sar_number}")
print(f"Filed: {sar.filing_date}")
print(f"Narrative Length: {len(sar.narrative)} characters")
```

### Audit Trail

```python
from fintech.compliance_automation import AuditTrailManager

audit = AuditTrailManager(
    retention_years=7,
    tamper_evident=True,
    immutable=True,
)

# Record an audit event
audit.record(
    event_type="customer_onboarding",
    actor_id="agent_001",
    customer_id="CUST-001",
    action="kyc_approved",
    details={"documents_verified": True, "risk_tier": "low"},
)

# Generate audit report
report = audit.generate_report(
    start_date="2026-01-01",
    end_date="2026-06-30",
    event_types=["kyc_approved", "sar_filed", "account_opened"],
)

print(f"Events: {report.total_events}")
print(f"Compliance Score: {report.compliance_score:.1%}")
```

## Architecture

```
Customer Touchpoints
├── Onboarding Forms
├── Transaction Systems
├── External Watchlists
└── Regulatory Portals
         │
         ▼
┌─────────────────────┐
│  Compliance Engine   │──→ Rule evaluation, scoring
│  (Rules + ML)        │
└────────┬────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│ KYC/   │ │ AML    │──→ Transaction monitoring
│ CDD    │ │ Screen │
└────┬───┘ └────┬───┘
     │          │
     ▼          ▼
┌─────────────────────┐
│  Reporting Layer     │──→ SAR, CTR, regulatory filings
│  (Automated)         │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Audit Trail         │──→ Immutable event log
│  (Append-only)       │
└─────────────────────┘
```

## Best Practices

- Implement risk-based KYC: enhanced due diligence for high-risk customers, simplified for low-risk
- Screen against ALL applicable sanctions lists, not just OFAC—use jurisdiction-specific lists for international operations
- Maintain 5-year minimum retention for SARs and supporting documentation (7 years recommended)
- Build automated SAR narrative generation using templates reviewed by compliance officers
- Implement positive pay and payee matching for check fraud prevention
- Conduct independent testing of AML systems annually with documented results
- Track and remediate all compliance exceptions with documented risk acceptance
- Maintain segregation of duties in compliance workflows (investigator ≠ approver)
- Generate regulatory reports automatically and validate before filing deadline
- Document all model validation, rule tuning, and threshold changes for regulatory examination

## Related Modules

- `fintech/risk-engine` - ML models powering fraud and AML detection
- `fintech/digital-banking` - Account data feeding compliance checks
- `fintech/payment-systems` - Transaction data for monitoring

## Advanced Configuration

### KYC/CDD Configuration

```yaml
kyc:
  jurisdictions:
    US:
      required_documents:
        - type: "government_id"
          acceptable: ["passport", "drivers_license", "state_id"]
          verification: "document_scan+liveness"
        - type: "proof_of_address"
          acceptable: ["utility_bill", "bank_statement", "lease"]
          max_age_days: 90
      risk_tiers:
        low:
          threshold: 10000
          review_cycle_days: 365
        medium:
          threshold: 100000
          review_cycle_days: 180
        high:
          threshold: 1000000
          review_cycle_days: 90
          enhanced_due_diligence: true
          
    EU:
      required_documents:
        - type: "government_id"
          acceptable: ["passport", "national_id", "residence_permit"]
          verification: "document_scan+liveness+address"
        - type: "proof_of_address"
          acceptable: ["utility_bill", "government_letter", "bank_statement"]
          max_age_days: 90
      risk_tiers:
        low:
          threshold: 10000
          review_cycle_days: 365
        medium:
          threshold: 100000
          review_cycle_days: 180
        high:
          threshold: 1000000
          review_cycle_days: 90
          enhanced_due_diligence: true
          
  verification_providers:
    primary:
      name: "jumio"
      api_key: "${JUMIO_API_KEY}"
      timeout_seconds: 30
    fallback:
      name: "onfido"
      api_key: "${ONFIDO_API_KEY}"
      timeout_seconds: 30
```

### AML Transaction Monitoring

```yaml
aml_monitoring:
  rules:
    structuring:
      enabled: true
      threshold_usd: 10000
      lookback_days: 30
      max_transactions: 3
      max_amount_usd: 25000
      severity: "high"
      
    layering:
      enabled: true
      complexity_threshold: 3
      rapid_movement_hours: 24
      amount_threshold_usd: 50000
      severity: "high"
      
    geographic_anomaly:
      enabled: true
      max_distance_km: 500
      max_time_hours: 2
      high_risk_countries: ["IR", "KP", "SY", "CU"]
      severity: "medium"
      
    unusual_activity:
      enabled: true
      deviation_multiplier: 3.0
      lookback_days: 90
      severity: "low"
      
  alert_management:
    auto_escalation:
      enabled: true
      escalation_threshold: 2
      escalation_window_hours: 24
      
    case_assignment:
      method: "round_robin"
      max_cases_per_analyst: 50
      priority_rules:
        - condition: "severity == 'high'"
          priority: 1
        - condition: "amount > 100000"
          priority: 2
        - condition: "risk_score > 0.8"
          priority: 3
```

### Sanctions Screening Configuration

```yaml
sanctions:
  lists:
    OFAC_SDN:
      url: "https://www.treasury.gov/ofac/downloads/sdn.csv"
      refresh_hours: 24
      enabled: true
      
    EU_SANCTIONS:
      url: "https://webgate.ec.europa.eu/fsd/fsf/public/files/xmlFullSanctionsList_1_1/content"
      refresh_hours: 24
      enabled: true
      
    UN_SANCTIONS:
      url: "https://scsanctions.un.org/resources/xml/en/consolidated.xml"
      refresh_hours: 24
      enabled: true
      
    PEP:
      provider: "worldcheck"
      api_key: "${WORLDCHECK_API_KEY}"
      refresh_days: 30
      enabled: true
      
  matching:
    algorithm": "jaro_winkler"
    threshold_exact: 0.95
    threshold_fuzzy: 0.85
    alias_expansion: true
    transliteration: true
    date_of_birth_weight: 0.3
    nationality_weight: 0.2
```

## Architecture Patterns

### Compliance Event Processing

```python
class ComplianceEventProcessor:
    def __init__(self, event_store, compliance_engine):
        self.event_store = event_store
        self.compliance_engine = compliance_engine
    
    async def process_event(self, event: ComplianceEvent):
        # Store event
        await self.event_store.store(event)
        
        # Run compliance checks
        checks = await self.compliance_engine.run_checks(event)
        
        # Generate alerts if needed
        alerts = await self.generate_alerts(checks)
        
        # Update audit trail
        await self.update_audit_trail(event, checks, alerts)
        
        return ComplianceResult(
            event=event,
            checks=checks,
            alerts=alerts,
        )
```

### KYC Workflow Pattern

```python
class KYCWorkflowEngine:
    def __init__(self, verification_providers, risk_engine):
        self.providers = verification_providers
        self.risk_engine = risk_engine
    
    async def process_kyc(self, customer: Customer) -> KYCResult:
        # Step 1: Document verification
        doc_result = await self.verify_documents(customer.documents)
        
        # Step 2: Identity proofing
        identity_result = await self.prove_identity(customer)
        
        # Step 3: Sanctions screening
        sanctions_result = await self.screen_sanctions(customer)
        
        # Step 4: Risk assessment
        risk_result = await self.assess_risk(customer, doc_result, identity_result, sanctions_result)
        
        # Step 5: Determine outcome
        outcome = self.determine_outcome(doc_result, identity_result, sanctions_result, risk_result)
        
        return KYCResult(
            customer_id=customer.id,
            status=outcome.status,
            risk_tier=outcome.risk_tier,
            verification_results={
                'document': doc_result,
                'identity': identity_result,
                'sanctions': sanctions_result,
                'risk': risk_result,
            },
            next_review_date=outcome.next_review_date,
        )
```

### SAR Filing Pattern

```python
class SARFilingEngine:
    def __init__(self, filing_api, narrative_generator):
        self.filing_api = filing_api
        self.narrative_generator = narrative_generator
    
    async def file_sar(self, alert: AMLAlert) -> SARFilingResult:
        # Generate narrative
        narrative = await self.narrative_generator.generate(alert)
        
        # Prepare filing
        filing_data = {
            'alert_id': alert.id,
            'subject': alert.subject,
            'suspicious_activity': alert.activity,
            'narrative': narrative,
            'filing_type': 'initial',
            'filing_agency': 'FinCEN',
        }
        
        # Submit filing
        result = await self.filing_api.submit(filing_data)
        
        # Update alert status
        await self.update_alert_status(alert.id, 'filed', result.sar_number)
        
        return SARFilingResult(
            sar_number=result.sar_number,
            filing_date=result.filing_date,
            status='filed',
        )
```

### Audit Trail Pattern

```python
class AuditTrailManager:
    def __init__(self, immutable_store, retention_policy):
        self.store = immutable_store
        self.retention = retention_policy
    
    async def record_event(self, event: AuditEvent):
        # Create audit entry
        entry = AuditEntry(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            event_type=event.event_type,
            actor_id=event.actor_id,
            resource_id=event.resource_id,
            action=event.action,
            details=event.details,
            previous_hash=await self.get_previous_hash(),
        )
        
        # Compute hash for tamper evidence
        entry.hash = self.compute_hash(entry)
        
        # Store immutably
        await self.store.append(entry)
    
    async def verify_integrity(self, start_time: datetime, end_time: datetime) -> bool:
        """Verify audit trail integrity"""
        entries = await self.store.get_entries(start_time, end_time)
        
        previous_hash = None
        for entry in entries:
            if previous_hash and entry.previous_hash != previous_hash:
                return False
            
            if not self.verify_hash(entry):
                return False
            
            previous_hash = entry.hash
        
        return True
```

## Integration Guide

### Jumio KYC Integration

```python
import httpx

class JumioIntegration:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.jumio.com/v2"
    
    async def verify_document(self, document: Document) -> VerificationResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "customer_id": document.customer_id,
            "callback_url": document.callback_url,
            "document": {
                "type": document.type,
                "country": document.country,
                "number": document.number,
            },
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/id-verification",
                headers=headers,
                json=payload,
            )
        
        return self.parse_response(response.json())
```

### Chainalysis AML Integration

```python
class ChainalysisIntegration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.chainalysis.com/api/v2"
    
    async def screen_transaction(self, transaction: Transaction) -> ScreeningResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "transaction": {
                "hash": transaction.hash,
                "source_address": transaction.source_address,
                "destination_address": transaction.destination_address,
                "amount": str(transaction.amount),
                "asset": transaction.asset,
            },
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/transactions",
                headers=headers,
                json=payload,
            )
        
        return self.parse_response(response.json())
```

### FinCEN SAR Filing Integration

```python
class FinCENIntegration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://efiling.fincen.gov/api/v1"
    
    async def submit_sar(self, sar_data: dict) -> FilingResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/sar/submit",
                headers=headers,
                json=sar_data,
            )
        
        return self.parse_response(response.json())
```

## Performance Optimization

### Batch Processing

```python
class BatchProcessor:
    def __init__(self, batch_size: int = 1000):
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

### Caching Strategy

```python
class ComplianceCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get_sanctions_match(self, name: str) -> Optional[List]:
        cache_key = f"sanctions:{hash(name)}"
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        return None
    
    async def cache_sanctions_match(self, name: str, matches: List):
        cache_key = f"sanctions:{hash(name)}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            json.dumps(matches)
        )
```

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_transactions_customer_date 
ON transactions (customer_id, created_at DESC);

CREATE INDEX idx_alerts_status_severity 
ON alerts (status, severity);

CREATE INDEX idx_kyc_customer_status 
ON kyc_records (customer_id, status);

-- Partition tables by date
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    event_type VARCHAR(50),
    actor_id VARCHAR(100),
    resource_id VARCHAR(100),
    action VARCHAR(50),
    details JSONB,
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE audit_logs_2026_07 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
```

## Security Considerations

### Data Encryption

```python
from cryptography.fernet import Fernet

class ComplianceEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive compliance data"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive compliance data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class ComplianceAccessControl:
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
class ComplianceAuditLogger:
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

**Issue: High false positive rate in sanctions screening**
```python
async def tune_sanctions_thresholds():
    # Analyze recent alerts
    alerts = await get_recent_alerts(days=30)
    
    # Calculate false positive rate by threshold
    for threshold in [0.95, 0.90, 0.85, 0.80]:
        fp_count = sum(1 for a in alerts if a.score >= threshold and a.resolution == 'false_positive')
        tp_count = sum(1 for a in alerts if a.score >= threshold and a.resolution == 'true_positive']
        
        fpr = fp_count / (fp_count + tp_count) if (fp_count + tp_count) > 0 else 0
        
        print(f"Threshold: {threshold}")
        print(f"  False positives: {fp_count}")
        print(f"  True positives: {tp_count}")
        print(f"  FPR: {fpr:.2%}")
```

**Issue: SAR filing delays**
```python
async def diagnose_sar_delays():
    # Get pending SARs
    pending_sars = await get_pending_sars()
    
    for sar in pending_sars:
        days_pending = (datetime.utcnow() - sar.created_at).days
        
        print(f"SAR {sar.sar_number}:")
        print(f"  Created: {sar.created_at}")
        print(f"  Days pending: {days_pending}")
        print(f"  Status: {sar.status}")
        
        if days_pending > 30:
            print(f"  WARNING: SAR overdue")
            print(f"  Action: Escalate to compliance officer")
```

**Issue: Audit trail integrity failure**
```python
async def verify_audit_trail_integrity(start_date: date, end_date: date):
    entries = await get_audit_entries(start_date, end_date)
    
    previous_hash = None
    for entry in entries:
        if previous_hash and entry.previous_hash != previous_hash:
            print(f"INTEGRITY FAILURE at {entry.timestamp}")
            print(f"  Expected previous hash: {previous_hash}")
            print(f"  Actual previous hash: {entry.previous_hash}")
            return False
        
        if not verify_hash(entry):
            print(f"HASH VERIFICATION FAILURE at {entry.timestamp}")
            return False
        
        previous_hash = entry.hash
    
    print("Audit trail integrity verified")
    return True
```

## API Reference

### KYC API

```python
# Process KYC
POST /api/v1/kyc/process
Request:
{
    "customer_id": "CUST-001",
    "documents": [
        {"type": "passport", "number": "P12345678", "country": "US"}
    ],
    "source_of_funds": "employment"
}

Response:
{
    "status": "approved",
    "risk_tier": "low",
    "next_review_date": "2027-07-01",
    "verification_results": {
        "document": {"status": "verified", "score": 0.98},
        "sanctions": {"status": "clear", "matches": []}
    }
}
```

### AML API

```python
# Monitor transaction
POST /api/v1/aml/monitor
Request:
{
    "transaction_id": "TXN-001",
    "customer_id": "CUST-001",
    "amount": 9500,
    "type": "cash_deposit"
}

Response:
{
    "alert_triggered": true,
    "rule": "structuring",
    "severity": "high",
    "confidence": 0.85,
    "recommendation": "review"
}
```

### Sanctions API

```python
# Screen entity
POST /api/v1/sanctions/screen
Request:
{
    "name": "John Doe",
    "date_of_birth": "1980-01-15",
    "nationality": "US"
}

Response:
{
    "has_match": false,
    "matches": [],
    "screened_lists": ["OFAC_SDN", "EU_SANCTIONS", "UN_SANCTIONS"]
}
```

## Data Models

### Customer Model

```python
class Customer:
    customer_id: str
    name: str
    date_of_birth: date
    nationality: str
    address: Address
    risk_tier: RiskTier
    kyc_status: KYCStatus
    kyc_verified_at: Optional[datetime]
    next_review_date: Optional[date]
    source_of_funds: str
    occupation: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### Alert Model

```python
class Alert:
    alert_id: str
    customer_id: str
    transaction_id: Optional[str]
    rule_name: str
    severity: str
    confidence: float
    description: str
    status: str  # open, investigating, resolved
    resolution: Optional[str]
    analyst_id: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### SAR Model

```python
class SAR:
    sar_number: str
    alert_id: str
    customer_id: str
    filing_type: str  # initial, continuing, joint
    filing_agency: str
    subject: dict
    suspicious_activity: dict
    narrative: str
    filing_date: Optional[datetime]
    status: str  # draft, pending, filed
    created_at: datetime
    updated_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: compliance-service
  namespace: compliance-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: compliance-service
  template:
    metadata:
      labels:
        app: compliance-service
    spec:
      containers:
      - name: compliance
        image: your-registry/compliance-service:2.0.0
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

# KYC metrics
kyc_processing_counter = Counter(
    'kyc_processing_total',
    'Total KYC processes',
    ['status', 'risk_tier']
)

kyc_processing_duration = Histogram(
    'kyc_processing_duration_seconds',
    'KYC processing duration',
    ['verification_type'],
    buckets=[1, 5, 10, 30, 60, 300]
)

# AML metrics
aml_alerts_counter = Counter(
    'aml_alerts_total',
    'Total AML alerts',
    ['rule', 'severity']
)

# Sanctions metrics
sanctions_screening_counter = Counter(
    'sanctions_screening_total',
    'Total sanctions screenings',
    ['list', 'result']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Compliance Automation",
    "panels": [
      {
        "title": "KYC Processing Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(kyc_processing_total[5m])",
            "legendFormat": "{{status}} - {{risk_tier}}"
          }
        ]
      },
      {
        "title": "AML Alerts by Rule",
        "type": "pie",
        "targets": [
          {
            "expr": "rate(aml_alerts_total[5m])",
            "legendFormat": "{{rule}}"
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
- name: compliance_alerts
  rules:
  - alert: HighKYCRejectionRate
    expr: rate(kyc_processing_total{status="rejected"}[5m]) / rate(kyc_processing_total[5m]) > 0.2
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "KYC rejection rate exceeds 20%"
      
  - alert: AMLAlertBacklog
    expr: aml_alerts_pending > 100
    for: 1h
    labels:
      severity: critical
    annotations:
      summary: "AML alert backlog exceeds 100"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from datetime import date

class TestKYCWorkflow:
    def test_approve_low_risk_customer(self, kyc_workflow):
        result = kyc_workflow.process_customer(
            customer_id="CUST-001",
            documents=[
                {"type": "passport", "number": "P12345678", "country": "US"},
            ],
            source_of_funds="employment",
        )
        assert result.status == "approved"
        assert result.risk_tier == "low"
    
    def test_escalate_high_risk_customer(self, kyc_workflow):
        result = kyc_workflow.process_customer(
            customer_id="CUST-002",
            documents=[
                {"type": "passport", "number": "P87654321", "country": "IR"},
            ],
            source_of_funds="unknown",
        )
        assert result.status == "pending_review"
        assert result.risk_tier == "high"
```

### Integration Tests

```python
class TestEndToEndCompliance:
    async def test_aml_monitoring_flow(self, aml_monitor, alert_manager):
        # Create transaction
        transaction = Transaction(
            id="TXN-001",
            customer_id="CUST-001",
            amount=9500,
            type="cash_deposit",
        )
        
        # Monitor transaction
        result = await aml_monitor.monitor_transaction(transaction)
        
        assert result.alert_triggered == True
        assert result.rule == "structuring"
        
        # Create alert
        alert = await alert_manager.create_alert(result)
        assert alert.alert_id is not None
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class ComplianceUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def screen_sanctions(self):
        self.client.post("/api/v1/sanctions/screen", json={
            "name": "John Doe",
            "date_of_birth": "1980-01-15",
            "nationality": "US",
        })
    
    @task(5)
    def process_kyc(self):
        self.client.post("/api/v1/kyc/process", json={
            "customer_id": f"CUST-{self.customer_counter}",
            "documents": [{"type": "passport", "number": "P12345678", "country": "US"}],
        })
        self.customer_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/kyc/process", methods=["POST"])
@app.route("/api/v2/kyc/process", methods=["POST"])
async def process_kyc():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await process_kyc_v2()
    return await process_kyc_v1()
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

- **AML**: Anti-Money Laundering - regulations to prevent money laundering
- **BSA**: Bank Secrecy Act - US law requiring financial institutions to assist government in detecting money laundering
- **CDD**: Customer Due Diligence - process of verifying customer identity and assessing risk
- **CTR**: Currency Transaction Report - report for cash transactions over $10,000
- **EDD**: Enhanced Due Diligence - additional verification for high-risk customers
- **FinCEN**: Financial Crimes Enforcement Network - US agency responsible for AML regulations
- **KYC**: Know Your Customer - process of verifying customer identity
- **PEP**: Politically Exposed Person - individual with prominent public function
- **SAR**: Suspicious Activity Report - report for suspicious transactions
- **SDN**: Specially Designated Nationals - OFAC list of sanctioned entities

## Changelog

### Version 2.0.0 (2026-07-01)
- Added multi-jurisdiction support
- Implemented automated SAR narrative generation
- Enhanced sanctions screening with fuzzy matching
- Added graph-based AML pattern detection

### Version 1.5.0 (2026-01-15)
- Added KYC workflow automation
- Implemented case management
- Enhanced audit trail with tamper evidence

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic AML monitoring
- Sanctions screening

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def process_kyc(
    customer: Customer,
    documents: List[Document],
) -> KYCResult:
    """Process customer through KYC workflow.
    
    Args:
        customer: Customer to verify.
        documents: Identity documents.
    
    Returns:
        KYC result with status and risk tier.
    
    Raises:
        KYCError: If processing fails.
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

Copyright (c) 2026 Compliance Automation Platform

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
