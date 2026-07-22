---
name: "architecture-docs"
category: "technical-writing"
version: "1.0.0"
tags: ["technical-writing", "architecture-docs", "adr", "c4-model", "system-design", "runbooks"]
---

# Architecture Decision Records & System Design Documentation

## Overview

Architecture documentation captures the reasoning behind system design choices, not just the outcomes. This module provides tooling for creating, managing, and rendering Architecture Decision Records (ADRs), C4 model diagrams, component interaction documentation, data flow diagrams, deployment architecture guides, and operational runbooks.

The ADR system follows the Michael Nygard template with extensions for status tracking, supersession chains, and stakeholder sign-off. Each ADR captures the decision context, considered alternatives, the rationale for the chosen approach, and the consequences. The module enforces ADR numbering, maintains a decision log index, and detects conflicting or superseded decisions.

C4 model support enables generation of Container, Component, and Code diagrams from structured data. Instead of hand-drawing diagrams that go stale, you define your architecture in a DSL (or extract it from code metadata) and generate PlantUML, Mermaid, or D2 diagrams programmatically. The system validates that diagram elements reference real components and that relationships are consistent across abstraction levels.

Operational documentation — deployment guides, disaster recovery runbooks, and on-call playbooks — follows a structured template that ensures completeness. The module checks that every production service has a corresponding runbook, that runbooks include escalation contacts, and that recovery procedures have been tested.

Architecture consistency validation compares documented components against actual infrastructure manifests (Kubernetes YAML, Terraform configs, CloudFormation templates) to detect drift between what is described in documentation and what is actually deployed. This catches stale documentation before it misleads engineers during incidents.

## Core Capabilities

- **Architecture Decision Records**: Create, query, and manage ADRs with status tracking, supersession chains, stakeholder sign-off, and automated index generation.
- **C4 Model Diagrams**: Generate Context, Container, Component, and Code diagrams from structured definitions with PlantUML, Mermaid, or D2 output.
- **Component Interaction Documentation**: Document API contracts, message flows, and event-driven interactions between system components with sequence diagrams.
- **Data Flow Diagrams**: Model data movement through systems with trust boundaries, encryption indicators, and data classification labels.
- **Deployment Architecture Guides**: Document deployment topologies, infrastructure dependencies, environment configurations, and scaling policies.
- **Disaster Recovery Runbooks**: Structured runbooks with step-by-step recovery procedures, RTO/RPO targets, escalation contacts, and verification checklists.
- **On-Call Documentation**: Service ownership matrices, alert escalation paths, known issues databases, and incident response playbooks.
- **Architecture Consistency Validation**: Verify that documentation matches actual infrastructure, detect drift between described and deployed architectures.

## Usage Examples

### Creating Architecture Decision Records

```python
from architecture_docs import ADR, ADRStatus, ADRRegistry

# Create a new ADR
adr = ADR(
    id="ADR-003",
    title="Use PostgreSQL as Primary Database",
    status=ADRStatus.ACCEPTED,
    date="2025-01-15",
    authors=["Alice Chen", "Bob Martinez"],
    context="""
    We need to select a primary relational database for the new payment service.
    Requirements include ACID compliance, JSON support, and horizontal read scaling.
    """,
    decision="""
    We will use PostgreSQL 16 as the primary database.
    
    PostgreSQL provides ACID compliance, native JSON/JSONB support, and can scale
    reads via streaming replication. The team has production experience with PostgreSQL.
    """,
    alternatives=[
        "MySQL 8.0 — Lacks mature JSON querying and weaker partitioning support.",
        "CockroachDB — Stronger distributed guarantees but operational complexity exceeds our team capacity.",
        "Amazon Aurora — Managed but introduces vendor lock-in and higher cost at our scale."
    ],
    consequences=[
        "Team must become proficient with PostgreSQL-specific features (JSONB, partitioning).",
        "We need to invest in replication monitoring and failover automation.",
        "Future migration to a distributed DB would require significant schema refactoring."
    ],
    superseded_by=None,
    supersedes="ADR-001"
)

# Register and generate index
registry = ADRRegistry(decisions_dir="docs/adr/")
registry.add(adr)
index = registry.generate_index()
print(index)
```

### C4 Model Diagram Generation

```python
from architecture_docs import C4Diagram, DiagramLevel, DiagramFormat

diagram = C4Diagram(
    system_name="E-Commerce Platform",
    level=DiagramLevel.CONTAINER,
    format=DiagramFormat.MERMAID
)

diagram.add_person("Customer", "Browses products and places orders")
diagram.add_system("Web Application", "React SPA", "Delivers the storefront UI")
diagram.add_container("API Gateway", "Kong", "Routes and authenticates requests")
diagram.add_container("Order Service", "Node.js", "Processes order transactions")
diagram.add_container("PostgreSQL", "Database", "Stores order and product data")
diagram.add_container("Redis", "Cache", "Caches sessions and product catalog")

diagram.add_relationship("Customer", "Web Application", "Uses", "HTTPS")
diagram.add_relationship("Web Application", "API Gateway", "Calls", "REST/JSON")
diagram.add_relationship("API Gateway", "Order Service", "Routes to", "gRPC")
diagram.add_relationship("Order Service", "PostgreSQL", "Reads/Writes", "TCP/5432")
diagram.add_relationship("Order Service", "Redis", "Caches", "TCP/6379")

# Generate diagram
output = diagram.render(output_path="_build/c4-container.md")
print(f"Generated: {output}")
```

### Deployment Architecture Guide

```python
from architecture_docs import DeploymentGuide, Environment, ServiceDeployment

guide = DeploymentGuide(
    system_name="E-Commerce Platform",
    environments=[
        Environment(name="production", region="us-east-1", cluster="prod-eks"),
        Environment(name="staging", region="us-east-1", cluster="staging-eks"),
    ]
)

guide.add_service(ServiceDeployment(
    service_name="order-service",
    replicas={"production": 3, "staging": 1},
    cpu="500m",
    memory="512Mi",
    health_check="/health",
    port=3000,
    env_vars=["DATABASE_URL", "REDIS_URL", "JWT_SECRET"],
    scaling_policy="horizontal-pod-autoscaler",
    min_replicas=2,
    max_replicas=10
))

guide.render(output="docs/deployment.md")
```

### Disaster Recovery Runbook

```python
from architecture_docs import Runbook, RunbookStep, EscalationContact

runbook = Runbook(
    service="order-service",
    title="Order Service Disaster Recovery",
    rto_minutes=30,
    rpo_minutes=5,
    last_tested="2025-01-10",
    contacts=[
        EscalationContact(name="On-Call Engineer", channel="pagerduty", priority=1),
        EscalationContact(name="DBA Team", channel="slack#dba", priority=2),
        EscalationContact(name="Platform Lead", channel="phone", priority=3),
    ]
)

runbook.add_step(RunbookStep(
    order=1, title="Assess Impact",
    action="Check monitoring dashboard for order-service error rates and latency.",
    expected="Identified scope of outage and affected components.",
    verification="Error rate > 5% for > 2 minutes confirms incident."
))

runbook.add_step(RunbookStep(
    order=2, title="Failover Database",
    action="Promote read replica to primary: `aws rds failover-cluster <cluster-id>`",
    expected="New primary accepts writes within 60 seconds.",
    verification="Run `psql -c 'SELECT pg_is_in_recovery()'` returns false."
))

runbook.render(output="docs/runbooks/order-service-dr.md")
```

### Architecture Consistency Validation

```python
from architecture_docs import ArchitectureValidator

validator = ArchitectureValidator(
    doc_dir="docs/architecture/",
    infra_manifest="k8s/",
    codebase="src/"
)

issues = validator.validate()
for issue in issues:
    print(f"[{issue.severity}] {issue.category}: {issue.message}")
    if issue.suggestion:
        print(f"  Fix: {issue.suggestion}")

print(f"\nTotal issues: {len(issues)}")
```

## Best Practices

1. **Write ADRs before coding, not after**: Architecture decisions should be documented when they are made, not retroactively. An ADR written after the fact is justification, not documentation.
2. **Keep ADRs lightweight**: An ADR is a decision record, not a design document. Target 1-2 pages. If an ADR exceeds 3 pages, break it into an ADR plus a supplementary design document.
3. **Use the C4 model for diagram consistency**: Always work at the correct abstraction level. Context diagrams show system boundaries, Container diagrams show deployable units, Component diagrams show internal structure.
4. **Treat runbooks as executable procedures**: Every step in a disaster recovery runbook should be copy-pasteable into a terminal. Abstract instructions like "restart the service" are insufficient.
5. **Validate documentation against infrastructure**: Architecture docs go stale. Automate validation that documented components match deployed infrastructure.
6. **Track superseded decisions**: When a decision is overturned, don't delete the old ADR. Mark it as superseded and link to the new one. The reasoning behind the original choice remains valuable context.
7. **Include escalation contacts in every runbook**: A runbook without contacts is a procedure that can't be followed at 3 AM. Always include primary, secondary, and tertiary contacts.
8. **Test runbooks regularly**: A disaster recovery runbook that hasn't been tested is a hypothesis, not a procedure. Schedule quarterly DR tests and update runbooks based on findings.
9. **Document data flow trust boundaries**: When documenting data flows, always indicate which components are in trusted vs untrusted zones. This directly informs security architecture decisions.
10. **Version deployment guides per environment**: Production, staging, and development environments often have different configurations. Maintain separate deployment guides or clearly parameterize by environment.

## Related Modules

- [documentation](../documentation/GROK.md) — General technical documentation authoring and lifecycle management
- [api-docs](../api-docs/GROK.md) — OpenAPI specification generation and API reference documentation
- [tutorials](../tutorials/GROK.md) — Progressive tutorial authoring and learning path design
- [release-notes](../release-notes/GROK.md) — Automated release note generation and changelog management

## Advanced Configuration

### ADR Registry Configuration

Configure the ADR registry with custom settings:

```yaml
# adr-config.yml
adr:
  directory: docs/adr/
  template: templates/adr-template.md
  numbering:
    format: "ADR-{sequence:03d}"
    auto_increment: true
  index:
    auto_generate: true
    include_status: true
    group_by_status: true
  validation:
    required_fields:
      - context
      - decision
      - alternatives
      - consequences
    status_values:
      - proposed
      - accepted
      - deprecated
      - superseded
```

### C4 Diagram Configuration

Customize C4 diagram generation:

```yaml
c4:
  default_format: mermaid
  output_dir: docs/diagrams/
  plantuml:
    include_legend: true
    theme: cerulean
  mermaid:
    theme: default
    theme_variables:
      primaryColor: "#4A90D9"
      lineColor: "#5C6BC0"
      fontSize: 14
  d2:
    theme: 0
    sketch: false
```

### Runbook Template Configuration

```yaml
runbook:
  template: templates/runbook-template.md
  required_sections:
    - title
    - rto_minutes
    - rpo_minutes
    - contacts
    - steps
    - verification
  escalation:
    max_contacts: 5
    require_primary: true
    require_secondary: true
  validation:
    step_action_format: "code_block"
    require_verification: true
```

### Architecture Validation Rules

```yaml
validation:
  documentation_vs_infrastructure:
    enabled: true
    infra_manifests:
      - k8s/
      - terraform/
      - cloudformation/
    ignore_patterns:
      - "*/debug/*"
      - "*/test/*"
  component_consistency:
    check_deployments: true
    check_services: true
    check_namespaces: true
  naming_conventions:
    service_prefix: ""
    namespace_format: "^[a-z][a-z0-9-]*$"
```

## Architecture Patterns

### ADR Lifecycle

ADRs follow a defined lifecycle with status transitions:

```python
from architecture_docs import ADRStatus, ADRRegistry

# Status transitions
valid_transitions = {
    ADRStatus.PROPOSED: [ADRStatus.ACCEPTED, ADRStatus.DEPRECATED],
    ADRStatus.ACCEPTED: [ADRStatus.DEPRECATED, ADRStatus.SUPERSEDED],
    ADRStatus.DEPRECATED: [ADRStatus.SUPERSEDED],
    ADRStatus.SUPERSEDED: [],  # Terminal state
}

def transition_adr(adr, new_status, registry):
    if new_status not in valid_transitions[adr.status]:
        raise ValueError(f"Cannot transition from {adr.status} to {new_status}")
    adr.status = new_status
    registry.update(adr)
```

### C4 Diagram Generation Pipeline

Diagrams are generated from structured definitions through a pipeline:

```
Component Definition -> Validation -> Layout -> Rendering -> Output
        |                  |            |           |           |
   DSL Input         Rule Check    Auto-Layout   PlantUML    Markdown/PDF
   Code Metadata     Consistency   Positioning   Mermaid     SVG/PNG
```

### Infrastructure Validation Pipeline

```
K8s Manifests -> Parsing -> Component Extraction -> Documentation Comparison -> Issues
                    |              |                        |                     |
              YAML Load      Service/Deployment      Component Map         Drift Report
              Schema Check   Namespace Extract       Relationship Map     Fix Suggestions
```

### Runbook Execution Model

Runbooks follow a structured execution model with verification at each step:

```python
from architecture_docs import Runbook, RunbookStep, ExecutionResult

runbook = Runbook(service="order-service", title="DR Runbook")

for step in runbook.steps:
    result = execute_step(step)
    if not result.verification_passed:
        log_failure(step, result)
        escalate(runbook.contacts)
        break
    log_success(step, result)
```

## Integration Guide

### LMS Integration (SCORM)

Export architecture documentation as SCORM packages for training:

```python
from architecture_docs import SCORMExporter

exporter = SCORMExporter(
    adrs_dir="docs/adr/",
    diagrams_dir="docs/diagrams/"
)

exporter.export(
    output_path="architecture-training-scorm.zip",
    manifest={"title": "Architecture Training", "version": "1.0"}
)
```

### CI/CD Pipeline Integration

```yaml
# .github/workflows/arch-docs.yml
name: Architecture Documentation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate ADRs
        run: python -m architecture_docs.adr validate --dir docs/adr/
      - name: Validate Diagrams
        run: python -m architecture_docs.diagrams validate --dir docs/diagrams/
      - name: Check Infrastructure Drift
        run: python -m architecture_docs.validate --infra k8s/ --docs docs/
```

### IDE Integration

Real-time architecture documentation validation through LSP:

```python
from architecture_docs import ArchitectureLSPServer

server = ArchitectureLSPServer(
    adr_dir="docs/adr/",
    diagram_dir="docs/diagrams/",
    watch_patterns=["docs/**/*.md", "k8s/**/*.yaml"]
)
server.start()
```

## Performance Optimization

### Caching Diagram Output

Cache generated diagrams to avoid regeneration:

```python
from architecture_docs import C4Diagram, CacheConfig

diagram = C4Diagram(
    system_name="E-Commerce",
    level=DiagramLevel.CONTAINER,
    format=DiagramFormat.MERMAID,
    cache_config=CacheConfig(enabled=True, cache_dir=".diagram-cache/")
)
```

### Parallel ADR Validation

Validate multiple ADRs concurrently:

```python
from architecture_docs import ADRRegistry, ParallelConfig

registry = ADRRegistry(
    decisions_dir="docs/adr/",
    parallel_config=ParallelConfig(enabled=True, workers=4)
)
issues = registry.validate_all()
```

### Incremental Infrastructure Validation

Only validate changed infrastructure manifests:

```yaml
- name: Incremental Validation
  run: |
    CHANGED=$(git diff --name-only origin/main -- 'k8s/**')
    if [ -n "$CHANGED" ]; then
      python -m architecture_docs.validate --infra-files $CHANGED --docs docs/
    fi
```

## Security Considerations

### Access Control

Control who can create, modify, or supersede ADRs:

```python
from architecture_docs import AccessControl, ADRPermission

acl = AccessControl()
acl.grant(role="architect", permissions=[ADRPermission.CREATE, ADRPermission.SUPERSEDE])
acl.grant(role="developer", permissions=[ADRPermission.READ, ADRPermission.COMMENT])
acl.grant(role="viewer", permissions=[ADRPermission.READ])
```

### Audit Logging

Track all ADR and diagram changes:

```python
from architecture_docs import AuditLogger

logger = AuditLogger(log_file="audit.log")
logger.log_adr_created(adr_id="ADR-003", author="Alice Chen")
logger.log_adr_superseded(adr_id="ADR-001", by="ADR-003", reason="New database choice")
logger.log_diagram_generated(system="E-Commerce", format="mermaid")
```

### Diagram Content Security

Sanitize diagram output to prevent XSS in rendered HTML:

```python
from architecture_docs import C4Diagram, SecurityConfig

diagram = C4Diagram(
    system_name="Internal System",
    security_config=SecurityConfig(
        sanitize_output=True,
        strip_html=True,
        validate_relationships=True
    )
)
```

### Sensitive Data in Diagrams

```python
from architecture_docs import DataClassification

classifier = DataClassification(
    sensitive_labels=["SECRET", "CONFIDENTIAL"],
    redact_patterns=[r"password", r"api_key", r"secret"]
)

# Redact sensitive data from diagrams
clean_diagram = classifier.clean(diagram)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| ADR numbering conflict | Manual ADR creation bypassed registry | Use `registry.renumber()` to fix |
| C4 diagram too complex | Too many components at one level | Move to lower abstraction level |
| Runbook missing contacts | Template not followed | Add escalation contacts to runbook |
| Infrastructure drift detected | Documentation not updated | Update docs to match actual infrastructure |
| Diagram generation fails | Invalid component references | Check component IDs in diagram definition |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from architecture_docs import C4Diagram
diagram = C4Diagram(system_name="Debug", debug=True)
```

### Log Output

```
[DEBUG] architecture_docs.adr: Validating ADR-003
[DEBUG] architecture_docs.diagrams: Generating C4 container diagram
[WARNING] architecture_docs.validate: Component 'payment-service' in docs not in k8s manifests
[ERROR] architecture_docs.runbook: Missing escalation contact for order-service
[INFO] architecture_docs.adr: ADR index updated with 12 entries
```

## API Reference

### ADR

```python
class ADR:
    def __init__(self, id: str, title: str, status: ADRStatus,
                 date: str, authors: List[str], context: str,
                 decision: str, alternatives: List[str],
                 consequences: List[str], superseded_by: str = None,
                 supersedes: str = None):
        """Initialize an ADR."""

    def to_markdown(self) -> str:
        """Render ADR as Markdown."""

    def validate(self) -> List[str]:
        """Validate ADR completeness."""
```

### ADRRegistry

```python
class ADRRegistry:
    def __init__(self, decisions_dir: str,
                 parallel_config: ParallelConfig = None):
        """Initialize the ADR registry."""

    def add(self, adr: ADR) -> None:
        """Add an ADR to the registry."""

    def generate_index(self) -> str:
        """Generate a decision log index."""

    def validate_all(self) -> List[ValidationIssue]:
        """Validate all ADRs in the registry."""

    def supersede(self, old_id: str, new_id: str) -> None:
        """Mark an ADR as superseded by another."""
```

### C4Diagram

```python
class C4Diagram:
    def __init__(self, system_name: str, level: DiagramLevel,
                 format: DiagramFormat, cache_config: CacheConfig = None):
        """Initialize a C4 diagram."""

    def add_person(self, name: str, description: str) -> None:
        """Add a person element to the diagram."""

    def add_system(self, name: str, technology: str, description: str) -> None:
        """Add a system element."""

    def add_relationship(self, source: str, destination: str,
                         label: str, technology: str = None) -> None:
        """Add a relationship between elements."""

    def render(self, output_path: str = None) -> str:
        """Render the diagram and return the output."""
```

## Data Models

### ADR

```python
@dataclass
class ADR:
    id: str
    title: str
    status: ADRStatus
    date: str
    authors: List[str]
    context: str
    decision: str
    alternatives: List[str]
    consequences: List[str]
    superseded_by: Optional[str]
    supersedes: Optional[str]
    metadata: Dict[str, Any]
```

### C4Element

```python
@dataclass
class C4Element:
    id: str
    name: str
    type: str  # person, system, container, component
    technology: Optional[str]
    description: str
    properties: Dict[str, str]
```

### Runbook

```python
@dataclass
class Runbook:
    service: str
    title: str
    rto_minutes: int
    rpo_minutes: int
    last_tested: str
    contacts: List[EscalationContact]
    steps: List[RunbookStep]
    verification_checklist: List[str]
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "-m", "architecture_docs.server", "--host", "0.0.0.0", "--port", "8080"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: architecture-docs-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: architecture-docs
  template:
    spec:
      containers:
        - name: architecture-docs
          image: architecture-docs:latest
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 1Gi
```

## Monitoring & Observability

### Metrics Collection

```python
from architecture_docs import MetricsCollector

metrics = MetricsCollector(prefix="architecture_docs")
metrics.histogram("adr_processing_seconds", duration, labels={"status": "accepted"})
metrics.counter("diagrams_generated_total", count, labels={"level": "container"})
metrics.gauge("adr_total_count", count, labels={"status": "accepted"})
```

### Alerting Rules

```yaml
groups:
  - name: architecture-docs
    rules:
      - alert: ADRProcessingSlow
        expr: architecture_docs_adr_processing_seconds > 30
        labels:
          severity: warning
        annotations:
          summary: "ADR processing is slow"
      - alert: DiagramGenerationFailures
        expr: rate(architecture_docs_diagram_errors_total[1h]) > 5
        labels:
          severity: critical
        annotations:
          summary: "High diagram generation failure rate"
```

## Testing Strategy

### Unit Tests

```python
def test_adr_creation():
    adr = ADR(
        id="ADR-001", title="Use PostgreSQL", status=ADRStatus.ACCEPTED,
        date="2025-01-15", authors=["Alice"], context="Need a database",
        decision="Use PostgreSQL", alternatives=["MySQL"], consequences=["Training needed"]
    )
    assert adr.validate() == []

def test_c4_diagram_generation():
    diagram = C4Diagram("Test", DiagramLevel.CONTAINER, DiagramFormat.MERMAID)
    diagram.add_person("User", "End user")
    diagram.add_system("App", "Web App", "Main application")
    diagram.add_relationship("User", "App", "Uses")
    output = diagram.render()
    assert "User" in output
    assert "App" in output
```

### Integration Tests

```python
def test_adr_lifecycle():
    registry = ADRRegistry(decisions_dir="test/fixtures/adr/")
    adr = create_test_adr()
    registry.add(adr)
    index = registry.generate_index()
    assert "ADR-001" in index

    registry.supersede("ADR-001", "ADR-002")
    updated = registry.get("ADR-001")
    assert updated.status == ADRStatus.SUPERSEDED
```

## Versioning & Migration

### Semantic Versioning

The architecture docs module follows semantic versioning:
- **Major**: Breaking changes to ADR format or diagram schema
- **Minor**: New features, new diagram formats, new validation rules
- **Patch**: Bug fixes, improved validation messages

### Deprecation Policy

Deprecated features receive warnings for one minor version before removal. Migration guides are provided for all breaking changes.

## Glossary

| Term | Definition |
|------|-----------|
| **ADR** | Architecture Decision Record documenting a design choice and its rationale |
| **C4 Model** | Four-level abstraction model for software architecture diagrams |
| **Runbook** | Step-by-step operational procedure for incident response |
| **Supersession** | The replacement of one ADR with a newer decision |
| **Decision Log** | An index of all ADRs and their current status |
| **Infrastructure Drift** | Discrepancy between documented and actual deployed architecture |
| **Escalation Contact** | Primary, secondary, or tertiary contact for incident response |
| **Trust Boundary** | A security perimeter separating trusted from untrusted components |

## Changelog

### v1.4.0 (Latest)
- Added advanced diagram formatting options
- Added ADR search functionality
- Improved infrastructure validation accuracy

### v1.3.0
- Added data flow diagrams with trust boundaries
- Added infrastructure validation against K8s manifests
- Improved diagram rendering performance

### v1.2.0
- Added on-call documentation templates
- Added escalation contact management
- Improved runbook step verification

### v1.1.0
- Added deployment architecture guides
- Added disaster recovery runbook templates
- Improved C4 diagram generation

### v1.0.0
- Initial release with ADR management
- C4 model diagram generation
- Architecture consistency validation

## Contributing Guidelines

### How to Contribute

1. Fork the repository and create a feature branch
2. Follow existing code style and patterns
3. Write tests for new features
4. Update documentation as needed
5. Ensure all CI checks pass
6. Submit a pull request with a clear description

### Adding New ADR Templates

1. Create a new template in `templates/adr/`
2. Follow the existing template structure
3. Register the template in `ADRRegistry`
4. Write tests for the new template
5. Update documentation

### Adding New Diagram Formats

1. Create a new renderer extending `BaseDiagramRenderer`
2. Implement the `render()` method
3. Register with `C4Diagram`
4. Write tests for the new format
5. Update documentation

## License

MIT License

Copyright (c) 2025 Example Organization

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

### Dependencies

- `pyyaml` >= 6.0 — YAML parsing for diagrams and configuration
- `plantuml` >= 1.0 — PlantUML diagram rendering
- `mermaid-py` >= 0.3 — Mermaid diagram rendering
- `requests` >= 2.31 — HTTP client for diagram rendering
- `jinja2` >= 3.1 — Template rendering for ADRs and runbooks
