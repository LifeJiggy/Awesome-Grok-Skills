---
name: "contract-analysis"
category: "legal-reg-tech"
version: "2.0.0"
tags: ["legal", "contracts", "analysis", "extraction", "risk"]
description: "Contract analysis, term extraction, and risk assessment tools"
---

# Contract Analysis

## Overview

The Contract Analysis module provides AI-powered tools for analyzing contracts, extracting key terms, identifying risks, and comparing contract versions. It supports clause identification, obligation tracking, deadline management, and compliance verification against standard terms.

## Core Capabilities

- **Term Extraction**: Extract key terms, dates, and obligations
- **Risk Assessment**: Identify risky clauses and non-standard terms
- **Clause Comparison**: Compare contracts against standard templates
- **Obligation Tracking**: Track contractual obligations and deadlines
- **Renewal Management**: Track contract renewals and expirations
- **Compliance Verification**: Verify contracts meet policy requirements
- **Version Comparison**: Compare contract revisions
- **Summary Generation**: Generate contract summaries

## Usage Examples

### Contract Parsing

```python
from contract_analysis import ContractAnalyzer, Contract

analyzer = ContractAnalyzer()

# Analyze contract
contract = Contract(
    file_path="/contracts/service-agreement.pdf",
    parties=["Acme Corp", "Beta Inc"],
    contract_type="service_agreement",
)

analysis = analyzer.analyze(contract)
print(f"Contract Analysis:")
print(f"  Type: {analysis.contract_type}")
print(f"  Parties: {analysis.parties}")
print(f"  Effective Date: {analysis.effective_date}")
print(f"  Expiration Date: {analysis.expiration_date}")
print(f"  Total Value: ${analysis.total_value:,.2f}")
```

### Risk Assessment

```python
from contract_analysis import RiskAssessor

assessor = RiskAssessor()

# Assess contract risks
risks = assessor.assess(analysis)
print(f"Risk Assessment:")
print(f"  Overall Risk: {risks.overall_risk}")
print(f"  High Risk Clauses: {risks.high_risk_count}")
print(f"  Recommendations: {len(risks.recommendations)}")
for risk in risks.top_risks:
    print(f"    - {risk.clause}: {risk.risk_description}")
```

### Obligation Extraction

```python
from contract_analysis import ObligationExtractor

extractor = ObligationExtractor()

# Extract obligations
obligations = extractor.extract(analysis)
print(f"Obligations ({len(obligations)}):")
for oblig in obligations:
    print(f"  Party: {oblig.party}")
    print(f"  Obligation: {oblig.description}")
    print(f"  Deadline: {oblig.deadline}")
    print(f"  Penalty: {oblig.penalty}")
```

### Contract Comparison

```python
from contract_analysis import ContractComparator

comparator = ContractComparator()

# Compare two contract versions
diff = comparator.compare(
    original="contract-v1.pdf",
    revised="contract-v2.pdf",
)

print(f"Contract Comparison:")
print(f"  Changes: {diff.change_count}")
print(f"  Additions: {diff.additions}")
print(f"  Deletions: {diff.deletions}")
print(f"  Modifications: {diff.modifications}")
```

## Best Practices

- **Standard Terms**: Maintain standard term libraries for comparison
- **Risk Templates**: Define risk thresholds for different contract types
- **Obligation Tracking**: Implement systematic obligation monitoring
- **Regular Review**: Review high-risk contracts regularly
- **Version Control**: Maintain contract version history
- **Stakeholder Review**: Involve relevant stakeholders in contract review
- **Legal Counsel**: Consult legal counsel for complex terms
- **Documentation**: Document all contract analysis findings

## Related Modules

- **legal-documentation**: Document creation for contracts
- **regulatory-compliance**: Compliance verification
- **policy-management**: Policy alignment checking

## Advanced Configuration

### Custom Clause Templates

```python
from contract_analysis import ClauseLibrary, ClauseTemplate

# Create clause library
library = ClauseLibrary()

# Define standard clause templates
library.add_template(
    template_id="liability_limitation_v2",
    title="Limitation of Liability",
    category="risk_allocation",
    standard_text="In no event shall either party be liable for any indirect, incidental, special, consequential, or punitive damages...",
    risk_factors=[
        "unlimited_liability",
        "consequential_damages_included",
        "no_cap_specified",
    ],
    alternatives=[
        {
            "text": "Total liability shall not exceed fees paid in the last 12 months",
            "risk_level": "low",
        },
        {
            "text": "Total liability shall not exceed $1,000,000",
            "risk_level": "medium",
        },
    ],
)

# Add custom templates per contract type
library.add_template(
    template_id="data_protection_saas",
    title="Data Protection Addendum",
    category="privacy",
    contract_types=["saas", "cloud_services"],
    required_clauses=[
        "data_processing_agreement",
        "subprocessor_list",
        "breach_notification",
        "data_return_deletion",
    ],
    regulatory_requirements=["GDPR", "CCPA", "HIPAA"],
)
```

### Risk Scoring Configuration

```python
from contract_analysis import RiskScorer, RiskConfig

config = RiskConfig(
    # Risk weights by category
    weights={
        "financial": 0.35,
        "legal": 0.25,
        "operational": 0.20,
        "compliance": 0.20,
    },
    # Thresholds for risk levels
    thresholds={
        "low": 0.3,
        "medium": 0.6,
        "high": 0.8,
        "critical": 0.9,
    },
    # Contract type-specific adjustments
    type_adjustments={
        "vendor_agreement": {"financial": 1.2, "operational": 0.8},
        "partnership": {"legal": 1.3, "financial": 0.9},
        "employment": {"compliance": 1.5, "legal": 1.1},
    },
)

scorer = RiskScorer(config)

# Configure custom risk rules
scorer.add_rule(
    rule_id="unlimited_indemnity",
    condition=lambda clause: "indemnify" in clause.text.lower() and "cap" not in clause.text.lower(),
    severity="high",
    description="Unlimited indemnification obligation",
    recommendation="Negotiate liability cap on indemnification",
)
```

### Obligation Tracking Rules

```python
from contract_analysis import ObligationTracker, TrackingRule

tracker = ObligationTracker()

# Define tracking rules
tracker.add_rule(
    rule_id="payment_terms",
    pattern=r"payment.*due.*(\d+).*days",
    extract_groups=["days"],
    alert_days_before=7,
    escalation_days=3,
    notification_channels=["email", "slack"],
)

tracker.add_rule(
    rule_id="renewal_notice",
    pattern=r"renewal.*notice.*(\d+).*days",
    extract_groups=["days"],
    auto_renew=True,
    notice_period_days=90,
)

# Set up obligation monitoring
tracker.configure_monitoring(
    check_frequency="daily",
    business_days_only=True,
    holiday_calendar="US_FEDERAL",
)
```

## Architecture Patterns

### Contract Processing Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                  Contract Analysis Pipeline                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Input   │──▶│  Parse   │──▶│ Analyze  │──▶│  Output  │ │
│  │ Handler  │   │  Engine  │   │  Engine  │   │ Generator│ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       │              │              │              │        │
│       ▼              ▼              ▼              ▼        │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Format  │   │  NLP     │   │  Risk    │   │  Report  │ │
│  │ Detector │   │ Processor│   │ Scorer   │   │ Builder  │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Event-Driven Architecture

```yaml
events:
  contract.uploaded:
    description: "New contract uploaded for analysis"
    payload:
      contract_id: "string"
      file_path: "string"
      uploader_id: "string"
    handlers:
      - trigger_analysis_pipeline
      - notify_stakeholders

  contract.analyzed:
    description: "Contract analysis completed"
    payload:
      contract_id: "string"
      analysis_id: "string"
      risk_score: "float"
    handlers:
      - update_contract_status
      - generate_report

  contract.risk_detected:
    description: "High-risk clause detected"
    payload:
      contract_id: "string"
      clause_id: "string"
      severity: "string"
      risk_type: "string"
    handlers:
      - alert_legal_team
      - create_review_task

  obligation.upcoming:
    description: "Obligation deadline approaching"
    payload:
      contract_id: "string"
      obligation_id: "string"
      deadline: "datetime"
      days_remaining: "integer"
    handlers:
      - send_reminder
      - escalate_if_overdue
```

### Data Flow Architecture

```python
from contract_analysis import (
    InputHandler,
    ParserEngine,
    AnalyzerEngine,
    OutputGenerator,
)

class ContractPipeline:
    def __init__(self):
        self.input_handler = InputHandler()
        self.parser = ParserEngine()
        self.analyzer = AnalyzerEngine()
        self.output_generator = OutputGenerator()

    async def process(self, contract_input: ContractInput) -> AnalysisResult:
        # Stage 1: Input handling
        validated_input = await self.input_handler.validate(contract_input)
        format_info = self.input_handler.detect_format(validated_input)

        # Stage 2: Parsing
        parsed_contract = await self.parser.parse(
            content=validated_input.content,
            format=format_info.format,
            metadata=format_info.metadata,
        )

        # Stage 3: Analysis
        analysis_result = await self.analyzer.analyze(
            contract=parsed_contract,
            analysis_types=["risk", "obligation", "compliance"],
        )

        # Stage 4: Output generation
        output = await self.output_generator.generate(
            analysis=analysis_result,
            formats=["json", "pdf", "summary"],
        )

        return output
```

## Integration Guide

### Document Management System Integration

```python
from contract_analysis import DMSIntegration

dms = DMSIntegration(
    provider="sharepoint",
    site_url="https://company.sharepoint.com",
    client_id="your_client_id",
    client_secret="your_client_secret",
)

# Sync contracts from DMS
async def sync_contracts():
    contracts = await dms.list_documents(
        library="Legal/Contracts",
        filter={"status": "active"},
    )

    for contract in contracts:
        # Download contract content
        content = await dms.download_document(contract.id)

        # Analyze contract
        analysis = await analyzer.analyze(content)

        # Store analysis results
        await dms.update_metadata(
            document_id=contract.id,
            metadata={
                "risk_score": analysis.risk_score,
                "last_analyzed": datetime.utcnow(),
                "findings_count": len(analysis.findings),
            },
        )
```

### Legal Workflow Integration

```python
from contract_analysis import WorkflowIntegration

workflow = WorkflowIntegration(
    platform="salesforce",
    api_key="your_api_key",
)

# Create contract review workflow
workflow.create_workflow(
    name="Contract Review Process",
    steps=[
        {
            "name": "Initial Analysis",
            "action": "run_contract_analysis",
            "assignee": "legal_team",
        },
        {
            "name": "Risk Review",
            "action": "review_risk_findings",
            "condition": "risk_score > 0.7",
            "assignee": "senior_counsel",
        },
        {
            "name": "Approval",
            "action": "approve_contract",
            "assignee": "legal_director",
        },
        {
            "name": "Signature",
            "action": "collect_signatures",
            "integration": "docusign",
        },
    ],
)

# Trigger workflow for new contract
await workflow.start(
    workflow_id="contract_review_process",
    contract_id="contract-001",
    trigger_event="contract.uploaded",
)
```

### AI Enhancement Integration

```python
from contract_analysis import AIEnhancer

enhancer = AIEnhancer(
    model="gpt-4",
    api_key="your_openai_key",
)

# Enhance analysis with AI insights
enhanced_analysis = await enhancer.enhance_analysis(
    base_analysis=analysis,
    enhancements=[
        "explain_risks",
        "suggest_negotiations",
        "compare_market_standards",
        "predict_dispute_probability",
    ],
)

# Generate AI-powered summary
summary = await enhancer.generate_summary(
    contract=contract,
    audience="executive",
    focus_areas=["financial_impact", "key_risks", "recommendations"],
)
```

## Performance Optimization

### Parallel Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from contract_analysis import ContractAnalyzer

analyzer = ContractAnalyzer()

async def batch_analyze_contracts(contracts: list):
    """Analyze multiple contracts in parallel."""
    semaphore = asyncio.Semaphore(10)  # Limit concurrent analyses

    async def analyze_with_semaphore(contract):
        async with semaphore:
            return await analyzer.analyze_async(contract)

    tasks = [analyze_with_semaphore(c) for c in contracts]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return {
        "successful": [r for r in results if not isinstance(r, Exception)],
        "failed": [r for r in results if isinstance(r, Exception)],
    }

# CPU-bound analysis with thread pool
def parallel_clause_extraction(contract):
    """Extract clauses using thread pool for CPU-bound work."""
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(extract_financial_clauses, contract),
            executor.submit(extract_legal_clauses, contract),
            executor.submit(extract_operational_clauses, contract),
        ]

        results = [f.result() for f in futures]

    return merge_clause_results(results)
```

### Caching Strategies

```python
from contract_analysis import AnalysisCache
import redis

cache = AnalysisCache(
    redis_client=redis.Redis(host="localhost", port=6379),
    ttl=3600,  # 1 hour
)

@cache.cache_analysis
async def analyze_contract(contract_id: str):
    """Cached contract analysis."""
    contract = await get_contract(contract_id)
    return await analyzer.analyze(contract)

@cache.cache_clause_library
def get_clause_template(clause_type: str):
    """Cached clause template retrieval."""
    return clause_library.get_template(clause_type)

# Cache invalidation
async def invalidate_contract_cache(contract_id: str):
    """Invalidate cache when contract changes."""
    await cache.invalidate(f"analysis:{contract_id}")
    await cache.invalidate_pattern(f"clauses:{contract_id}:*")
```

### Database Optimization

```python
from contract_analysis import QueryOptimizer

optimizer = QueryOptimizer()

@optimizer.optimize(
    indexes=["contract_status_idx", "risk_score_idx"],
    cache_ttl=300,
)
def search_contracts(
    status: str = None,
    min_risk_score: float = None,
    max_risk_score: float = None,
    contract_type: str = None,
):
    """Optimized contract search."""
    query = db.query(Contract)

    if status:
        query = query.filter(Contract.status == status)
    if min_risk_score is not None:
        query = query.filter(Contract.risk_score >= min_risk_score)
    if max_risk_score is not None:
        query = query.filter(Contract.risk_score <= max_risk_score)
    if contract_type:
        query = query.filter(Contract.type == contract_type)

    return query.all()

# Pagination
@optimizer.paginate(default_page_size=50, max_page_size=200)
def list_obligations(contract_id: str, page: int = 1):
    """Paginated obligation listing."""
    return db.query(Obligation).filter(
        Obligation.contract_id == contract_id
    ).offset((page - 1) * 50).limit(50).all()
```

## Security Considerations

### Document Access Control

```python
from contract_analysis import AccessControl, Permission

access_control = AccessControl()

# Define permissions
permissions = {
    "contract.read": "Read contract and analysis results",
    "contract.analyze": "Trigger contract analysis",
    "contract.approve": "Approve contract after review",
    "contract.delete": "Delete contract and associated data",
    "obligation.manage": "Manage obligation tracking",
    "report.generate": "Generate contract reports",
}

# Check permissions
@access_control.require_permission("contract.read")
async def get_contract_analysis(contract_id: str):
    """Access-controlled contract retrieval."""
    return await analyzer.get_analysis(contract_id)

# Role-based access
access_control.define_role(
    role="legal_reviewer",
    permissions=[
        "contract.read",
        "contract.analyze",
        "obligation.manage",
    ],
)

access_control.define_role(
    role="contract_admin",
    permissions=list(permissions.keys()),
)
```

### Data Encryption

```python
from contract_analysis import EncryptionService
from cryptography.fernet import Fernet

encryption = EncryptionService(
    algorithm="AES-256-GCM",
    key_rotation_days=90,
)

# Encrypt sensitive contract data
def encrypt_contract_data(contract: Contract) -> Contract:
    """Encrypt sensitive fields in contract."""
    encrypted = contract.copy()
    sensitive_fields = [
        "financial_terms",
        "confidentiality_clause",
        "personal_data",
    ]

    for field in sensitive_fields:
        if hasattr(encrypted, field):
            value = getattr(encrypted, field)
            setattr(encrypted, field, encryption.encrypt(value))

    return encrypted

# Encrypt at rest
@encryption.encrypt_at_rest
async def store_contract(contract: Contract):
    """Store encrypted contract."""
    return await db.store(contract)
```

### Audit Logging

```python
from contract_analysis import AuditLogger
from datetime import datetime

logger = AuditLogger(
    storage="database",
    retention_days=2555,  # 7 years
)

def log_contract_action(
    action: str,
    user_id: str,
    contract_id: str,
    details: dict = None,
):
    """Log contract-related action."""
    logger.log(
        timestamp=datetime.utcnow(),
        action=action,
        user_id=user_id,
        resource_type="contract",
        resource_id=contract_id,
        ip_address=get_client_ip(),
        details=details or {},
    )

# Example usage
log_contract_action(
    action="contract.analyzed",
    user_id="user-001",
    contract_id="contract-001",
    details={
        "risk_score": 0.75,
        "findings_count": 5,
        "analysis_duration_ms": 2500,
    },
)
```

## Troubleshooting Guide

### Common Issues

#### Issue: PDF Parsing Failures

```python
# Symptom: Cannot extract text from PDF
# Diagnosis:
from contract_analysis import ParserDiagnostics

diagnostics = ParserDiagnostics()

result = diagnostics.analyze_pdf("contract.pdf")
print(f"PDF Version: {result.pdf_version}")
print(f"Text Layer: {result.has_text_layer}")
print(f"OCR Required: {result.ocr_required}")
print(f"Encryption: {result.is_encrypted}")

# Resolution:
# 1. Run OCR if no text layer
# 2. Use alternative PDF parser
# 3. Convert to text format first
```

#### Issue: Inaccurate Risk Scoring

```python
# Symptom: Risk scores don't match manual review
# Diagnosis:
from contract_analysis import ScoringDiagnostics

scoring_diag = ScoringDiagnostics()

comparison = scoring_diag.compare_scores(
    contract_id="contract-001",
    ai_score=0.75,
    manual_score=0.45,
)

print(f"Score discrepancy: {comparison.delta}")
print(f"Mismatched clauses: {comparison.mismatched_clauses}")
print(f"Weight differences: {comparison.weight_diff}")

# Resolution:
# 1. Review risk weights
# 2. Update clause library
# 3. Adjust scoring thresholds
```

#### Issue: Obligation Tracking Misses

```python
# Symptom: Obligations not being detected
# Diagnosis:
from contract_analysis import ObligationDiagnostics

oblig_diag = ObligationDiagnostics()

analysis = oblig_diag.analyze_detection_rate(
    contract_ids=["c1", "c2", "c3"],
    expected_obligations=50,
    detected_obligations=35,
)

print(f"Detection rate: {analysis.detection_rate:.1%}")
print(f"Missed patterns: {analysis.missed_patterns}")
print(f"False positives: {analysis.false_positives}")

# Resolution:
# 1. Update extraction patterns
# 2. Add missing clause types
# 3. Retrain NLP models
```

### Performance Issues

```python
# Symptom: Slow analysis processing
# Diagnosis:
from contract_analysis import PerformanceProfiler

profiler = PerformanceProfiler()

profile = profiler.profile_analysis(
    contract_size_mb=50,
    iterations=10,
)

print(f"Avg parse time: {profile.avg_parse_ms:.2f}ms")
print(f"Avg analysis time: {profile.avg_analysis_ms:.2f}ms")
print(f"Bottleneck: {profile.bottleneck}")

# Resolution:
# 1. Optimize PDF parsing
# 2. Use streaming for large files
# 3. Implement parallel processing
```

## API Reference

### Contract Analysis API

```python
# POST /api/v2/contracts/analyze
# Analyze a contract

@router.post("/contracts/analyze")
async def analyze_contract(
    request: AnalyzeContractRequest,
) -> AnalysisResponse:
    """
    Analyze a contract document.

    Args:
        request: Analysis request with contract data

    Returns:
        AnalysisResponse with analysis results
    """
    pass

# GET /api/v2/contracts/{contract_id}/analysis
# Get analysis results

@router.get("/contracts/{contract_id}/analysis")
async def get_analysis(
    contract_id: str,
) -> AnalysisResponse:
    """
    Get contract analysis results.

    Args:
        contract_id: Contract identifier

    Returns:
        AnalysisResponse with analysis results
    """
    pass

# POST /api/v2/contracts/compare
# Compare two contracts

@router.post("/contracts/compare")
async def compare_contracts(
    request: CompareContractsRequest,
) -> ComparisonResponse:
    """
    Compare two contract versions.

    Args:
        request: Comparison request with contract IDs

    Returns:
        ComparisonResponse with comparison results
    """
    pass
```

### Obligation Management API

```python
# GET /api/v2/contracts/{contract_id}/obligations
# List contract obligations

@router.get("/contracts/{contract_id}/obligations")
async def list_obligations(
    contract_id: str,
    status: str = None,
    deadline_before: date = None,
) -> ObligationListResponse:
    """
    List contract obligations.

    Args:
        contract_id: Contract identifier
        status: Filter by status
        deadline_before: Filter by deadline

    Returns:
        ObligationListResponse with obligations
    """
    pass

# PUT /api/v2/obligations/{obligation_id}/complete
# Mark obligation as complete

@router.put("/obligations/{obligation_id}/complete")
async def complete_obligation(
    obligation_id: str,
    completion_data: CompletionRequest,
) -> ObligationResponse:
    """
    Mark an obligation as completed.

    Args:
        obligation_id: Obligation identifier
        completion_data: Completion details

    Returns:
        ObligationResponse with updated obligation
    """
    pass
```

### Risk Assessment API

```python
# POST /api/v2/contracts/{contract_id}/risk-assessment
# Run risk assessment

@router.post("/contracts/{contract_id}/risk-assessment")
async def assess_risk(
    contract_id: str,
    assessment_config: RiskAssessmentConfig = None,
) -> RiskAssessmentResponse:
    """
    Run risk assessment on a contract.

    Args:
        contract_id: Contract identifier
        assessment_config: Optional assessment configuration

    Returns:
        RiskAssessmentResponse with risk results
    """
    pass

# GET /api/v2/risk-rules
# List risk rules

@router.get("/risk-rules")
async def list_risk_rules(
    category: str = None,
    severity: str = None,
) -> RiskRuleListResponse:
    """
    List available risk rules.

    Args:
        category: Filter by category
        severity: Filter by severity

    Returns:
        RiskRuleListResponse with risk rules
    """
    pass
```

## Data Models

### Contract Model

```python
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional
from enum import Enum

class ContractStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"

@dataclass
class Contract:
    id: str
    title: str
    contract_type: str
    status: ContractStatus
    parties: List[str]
    effective_date: Optional[date]
    expiration_date: Optional[date]
    total_value: Optional[float]
    currency: str
    file_path: str
    version: int
    created_at: datetime
    updated_at: datetime
    created_by: str
    metadata: dict

@dataclass
class ContractClause:
    id: str
    contract_id: str
    clause_type: str
    title: str
    content: str
    page_number: int
    section_number: str
    risk_level: Optional[str]
    non_standard: bool
    created_at: datetime
```

### Analysis Model

```python
@dataclass
class ContractAnalysis:
    id: str
    contract_id: str
    analysis_date: datetime
    risk_score: float
    risk_level: str
    findings_count: int
    high_risk_clauses: List[str]
    obligations_count: int
    key_terms: List[KeyTerm]
    summary: str
    recommendations: List[str]
    analysis_duration_ms: int

@dataclass
class KeyTerm:
    term: str
    value: str
    clause_id: str
    category: str
    confidence: float
```

### Risk Model

```python
@dataclass
class RiskAssessment:
    id: str
    contract_id: str
    assessment_date: datetime
    overall_risk: str
    risk_score: float
    risk_factors: List[RiskFactor]
    recommendations: List[RiskRecommendation]

@dataclass
class RiskFactor:
    id: str
    category: str
    severity: str
    description: str
    clause_id: str
    impact: str
    mitigation: str

@dataclass
class RiskRecommendation:
    priority: str
    action: str
    rationale: str
    target_clause: Optional[str]
```

### Obligation Model

```python
@dataclass
class Obligation:
    id: str
    contract_id: str
    party: str
    description: str
    obligation_type: str
    deadline: Optional[date]
    recurrence: Optional[str]
    status: str
    penalty: Optional[str]
    reminder_days_before: int
    created_at: datetime
    updated_at: datetime

@dataclass
class ObligationCompletion:
    id: str
    obligation_id: str
    completed_at: datetime
    completed_by: str
    evidence: Optional[str]
    notes: Optional[str]
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

# Install system dependencies for PDF parsing
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: contract-analysis-api
  namespace: legal-tech
spec:
  replicas: 3
  selector:
    matchLabels:
      app: contract-analysis-api
  template:
    metadata:
      labels:
        app: contract-analysis-api
    spec:
      containers:
      - name: contract-analysis-api
        image: legal-tech/contract-analysis:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: contract-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: contract-secrets
              key: redis-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        volumeMounts:
        - name: tesseract-data
          mountPath: /usr/share/tesseract-ocr
      volumes:
      - name: tesseract-data
        emptyDir: {}
```

### CI/CD Pipeline

```yaml
# .github/workflows/contract-analysis.yml
name: Contract Analysis CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    - name: Run tests
      run: pytest --cov=contract_analysis tests/
    - name: Run linting
      run: ruff check .

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Build and push Docker image
      run: |
        docker build -t legal-tech/contract-analysis:${{ github.sha }} .
        docker push legal-tech/contract-analysis:${{ github.sha }}
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/contract-analysis-api \
          contract-analysis-api=legal-tech/contract-analysis:${{ github.sha }} \
          -n legal-tech
```

## Monitoring & Observability

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
ANALYSIS_COUNT = Counter(
    'contract_analyses_total',
    'Total contract analyses',
    ['contract_type', 'status']
)

ANALYSIS_DURATION = Histogram(
    'contract_analysis_duration_seconds',
    'Analysis duration in seconds',
    ['contract_type'],
    buckets=[1, 5, 10, 30, 60, 120]
)

RISK_SCORE_DISTRIBUTION = Histogram(
    'contract_risk_score',
    'Risk score distribution',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

OBLIGATIONS_ACTIVE = Gauge(
    'contract_obligations_active',
    'Number of active obligations'
)
```

### Logging Configuration

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "contract_id": getattr(record, "contract_id", None),
            "user_id": getattr(record, "user_id", None),
        }
        return json.dumps(log_entry)

def setup_logging():
    logger = logging.getLogger("contract_analysis")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    return logger
```

### Distributed Tracing

```python
from opentelemetry import trace

tracer = trace.get_tracer("contract-analysis-service")

@tracer.start_as_current_span("analyze_contract")
def analyze_contract(contract_id: str):
    span = trace.get_current_span()
    span.set_attribute("contract.id", contract_id)

    # Analysis logic
    result = perform_analysis(contract_id)

    span.set_attribute("contract.risk_score", result.risk_score)
    span.set_attribute("contract.findings", result.findings_count)

    return result
```

## Testing Strategy

### Unit Tests

```python
import pytest
from contract_analysis import ContractAnalyzer, RiskAssessor

class TestContractAnalyzer:
    def setup_method(self):
        self.analyzer = ContractAnalyzer()

    def test_extract_parties(self):
        """Test party extraction."""
        text = "This Agreement is between Acme Corp and Beta Inc."
        parties = self.analyzer.extract_parties(text)
        assert len(parties) == 2
        assert "Acme Corp" in parties
        assert "Beta Inc" in parties

    def test_extract_dates(self):
        """Test date extraction."""
        text = "Effective Date: January 1, 2024. Expiration: December 31, 2024."
        dates = self.analyzer.extract_dates(text)
        assert len(dates) == 2

    def test_risk_scoring(self):
        """Test risk scoring."""
        clauses = [
            {"type": "liability", "content": "Unlimited liability"},
            {"type": "indemnity", "content": "Broad indemnification"},
        ]
        score = self.analyzer.calculate_risk_score(clauses)
        assert 0 <= score <= 1
        assert score > 0.5  # High risk expected
```

### Integration Tests

```python
import pytest
from httpx import AsyncClient
from contract_analysis import app

@pytest.mark.asyncio
class TestContractAPI:
    async def test_analyze_contract(self, async_client: AsyncClient):
        """Test contract analysis endpoint."""
        with open("test_contract.pdf", "rb") as f:
            response = await async_client.post(
                "/api/v2/contracts/analyze",
                files={"file": ("contract.pdf", f, "application/pdf")},
            )

        assert response.status_code == 200
        data = response.json()
        assert "analysis_id" in data
        assert "risk_score" in data

    async def test_list_obligations(self, async_client: AsyncClient):
        """Test obligation listing."""
        response = await async_client.get(
            "/api/v2/contracts/contract-001/obligations"
        )

        assert response.status_code == 200
        data = response.json()
        assert "obligations" in data
```

## Versioning & Migration

### API Versioning

```python
from fastapi import APIRouter

# Version 1 API
v1_router = APIRouter(prefix="/api/v1")

@v1_router.post("/contracts/analyze")
async def analyze_contract_v1():
    """V1: Basic contract analysis."""
    pass

# Version 2 API
v2_router = APIRouter(prefix="/api/v2")

@v2_router.post("/contracts/analyze")
async def analyze_contract_v2(
    request: AnalyzeContractRequest,
    enhancements: List[str] = None,
):
    """V2: Enhanced analysis with AI improvements."""
    pass

app.include_router(v1_router)
app.include_router(v2_router)
```

### Database Migrations

```python
# migrations/001_initial_schema.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'contracts',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('contract_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('risk_score', sa.Float),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )

    op.create_table(
        'obligations',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('contract_id', sa.String(50), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('deadline', sa.Date),
        sa.Column('status', sa.String(20), nullable=False),
    )

def downgrade():
    op.drop_table('obligations')
    op.drop_table('contracts')
```

## Glossary

### Contract Terms

| Term | Definition |
|------|------------|
| **Clause** | A distinct section of a contract |
| **Indemnification** | Agreement to compensate for loss or damage |
| **Liability** | Legal responsibility for debts or obligations |
| **Warranty** | Promise that facts are true or will be fulfilled |
| **Covenant** | Promise to do or not do something |
| **Force Majeure** | Unforeseeable circumstances preventing fulfillment |
| **Termination** | Ending of a contract |
| **Breach** | Violation of contract terms |
| **Remedy** | Legal solution for breach of contract |
| **Governing Law** | Jurisdiction whose laws apply to the contract |

### Analysis Terms

| Term | Definition |
|------|------------|
| **Risk Score** | Numerical assessment of contract risk (0-1) |
| **Risk Level** | Categorization of risk (low/medium/high/critical) |
| **Obligation** | Duty or requirement specified in contract |
| **Deadline** | Date by which obligation must be fulfilled |
| **Penalty** | Consequence for failing to meet obligations |
| **Non-Standard** | Terms deviating from standard templates |
| **Material Adverse Change** | Significant negative change affecting contract |
| **Due Diligence** | Investigation before entering contract |

## Changelog

### Version 2.0.0 (2024-01-15)
- Added AI-powered risk scoring
- Implemented parallel processing
- Added obligation tracking
- Enhanced PDF parsing
- Added custom clause templates

### Version 1.5.0 (2023-10-01)
- Added contract comparison
- Implemented version tracking
- Added obligation alerts
- Enhanced reporting

### Version 1.4.0 (2023-07-15)
- Added batch processing
- Implemented caching
- Added performance monitoring
- Enhanced error handling

### Version 1.3.0 (2023-04-01)
- Added DMS integration
- Implemented workflow support
- Added audit logging
- Enhanced security

### Version 1.2.0 (2023-01-15)
- Added basic risk assessment
- Implemented clause extraction
- Added party identification
- Enhanced API

### Version 1.1.0 (2022-10-01)
- Added PDF parsing
- Implemented text extraction
- Added basic analysis
- Enhanced documentation

### Version 1.0.0 (2022-07-15)
- Initial release
- Basic contract analysis
- REST API
- PostgreSQL support

## Contributing Guidelines

### Development Setup

```bash
# Clone repository
git clone https://github.com/company/contract-analysis.git
cd contract-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Start development server
uvicorn main:app --reload
```

### Code Standards

- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Maintain 80% test coverage
- Run linting before commit

### Pull Request Process

1. Create feature branch
2. Make changes with tests
3. Run full test suite
4. Submit PR with description
5. Address review feedback
6. Merge after approval

## License

MIT License

Copyright (c) 2024 Contract Analysis Contributors

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
