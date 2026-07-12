"""
Architecture Decision Records & System Design Documentation

Provides ADR management, C4 model diagrams, deployment guides,
disaster recovery runbooks, component interaction docs, and
architecture consistency validation.
"""

from __future__ import annotations

import re
import json
import hashlib
import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Any
from pathlib import Path


class ADRStatus(Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"


class DiagramLevel(Enum):
    CONTEXT = "context"
    CONTAINER = "container"
    COMPONENT = "component"
    CODE = "code"


class DiagramFormat(Enum):
    PLANTUML = "plantuml"
    MERMAID = "mermaid"
    D2 = "d2"


class IssueSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class StakeholderSignOff:
    name: str
    role: str
    date: str = ""
    approved: bool = False


@dataclass
class ADR:
    id: str
    title: str
    status: ADRStatus = ADRStatus.PROPOSED
    date: str = ""
    authors: list[str] = field(default_factory=list)
    context: str = ""
    decision: str = ""
    alternatives: list[str] = field(default_factory=list)
    consequences: list[str] = field(default_factory=list)
    superseded_by: Optional[str] = None
    supersedes: Optional[str] = None
    sign_offs: list[StakeholderSignOff] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [
            f"# {self.id}: {self.title}\n",
            f"**Status**: {self.status.value}",
            f"**Date**: {self.date}",
            f"**Authors**: {', '.join(self.authors)}\n",
            "## Context\n", self.context.strip(), "\n",
            "## Decision\n", self.decision.strip(), "\n",
        ]
        if self.alternatives:
            lines.append("## Alternatives Considered\n")
            for alt in self.alternatives:
                lines.append(f"- {alt}")
            lines.append("")
        if self.consequences:
            lines.append("## Consequences\n")
            for con in self.consequences:
                lines.append(f"- {con}")
            lines.append("")
        if self.supersedes:
            lines.append(f"\n**Supersedes**: {self.supersedes}")
        if self.superseded_by:
            lines.append(f"\n**Superseded by**: {self.superseded_by}")
        if self.sign_offs:
            lines.append("\n## Sign-Offs\n")
            lines.append("| Name | Role | Date | Approved |")
            lines.append("|------|------|------|----------|")
            for so in self.sign_offs:
                lines.append(f"| {so.name} | {so.role} | {so.date} | {'Yes' if so.approved else 'No'} |")
        return "\n".join(lines)


@dataclass
class ADRIndexEntry:
    id: str
    title: str
    status: ADRStatus
    date: str
    authors: list[str]


class ADRRegistry:
    def __init__(self, decisions_dir: str = "docs/adr/") -> None:
        self.decisions_dir = Path(decisions_dir)
        self._adrs: dict[str, ADR] = {}

    def add(self, adr: ADR) -> None:
        self._adrs[adr.id] = adr

    def get(self, adr_id: str) -> Optional[ADR]:
        return self._adrs.get(adr_id)

    def list_by_status(self, status: ADRStatus) -> list[ADR]:
        return [a for a in self._adrs.values() if a.status == status]

    def generate_index(self) -> str:
        lines = [
            "# Architecture Decision Records\n",
            "| ID | Title | Status | Date | Authors |",
            "|----|-------|--------|------|---------|",
        ]
        for adr in sorted(self._adrs.values(), key=lambda a: a.id):
            authors = ", ".join(adr.authors[:2])
            if len(adr.authors) > 2:
                authors += f" +{len(adr.authors)-2}"
            lines.append(f"| {adr.id} | {adr.title} | {adr.status.value} | {adr.date} | {authors} |")
        return "\n".join(lines)

    def detect_conflicts(self) -> list[tuple[str, str, str]]:
        conflicts = []
        superseded = {a.superseded_by for a in self._adrs.values() if a.superseded_by}
        for adr in self._adrs.values():
            if adr.supersedes and adr.supersedes in self._adrs:
                old = self._adrs[adr.supersedes]
                if old.status == ADRStatus.ACCEPTED:
                    conflicts.append((adr.id, adr.supersedes, "Supersedes an accepted ADR"))
        return conflicts

    def save_all(self) -> list[str]:
        saved = []
        self.decisions_dir.mkdir(parents=True, exist_ok=True)
        for adr in self._adrs.values():
            file_path = self.decisions_dir / f"{adr.id.lower()}-{self._slugify(adr.title)}.md"
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(adr.to_markdown())
                saved.append(str(file_path))
            except OSError:
                pass
        index_path = self.decisions_dir / "index.md"
        try:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(self.generate_index())
            saved.append(str(index_path))
        except OSError:
            pass
        return saved

    def _slugify(self, text: str) -> str:
        slug = text.lower().strip()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_]+", "-", slug)
        return slug[:60]


@dataclass
class C4Person:
    name: str
    description: str = ""


@dataclass
class C4System:
    name: str
    description: str = ""
    tech: str = ""


@dataclass
class C4Container:
    name: str
    tech: str = ""
    description: str = ""


@dataclass
class C4Relationship:
    source: str
    destination: str
    label: str = ""
    tech: str = ""


class C4Diagram:
    def __init__(self, system_name: str, level: DiagramLevel = DiagramLevel.CONTAINER,
                 format: DiagramFormat = DiagramFormat.MERMAID) -> None:
        self.system_name = system_name
        self.level = level
        self.format = format
        self.persons: list[C4Person] = []
        self.systems: list[C4System] = []
        self.containers: list[C4Container] = []
        self.relationships: list[C4Relationship] = []

    def add_person(self, name: str, description: str = "") -> None:
        self.persons.append(C4Person(name=name, description=description))

    def add_system(self, name: str, tech: str = "", description: str = "") -> None:
        self.systems.append(C4System(name=name, tech=tech, description=description))

    def add_container(self, name: str, tech: str = "", description: str = "") -> None:
        self.containers.append(C4Container(name=name, tech=tech, description=description))

    def add_relationship(self, source: str, destination: str, label: str = "",
                         tech: str = "") -> None:
        self.relationships.append(C4Relationship(
            source=source, destination=destination, label=label, tech=tech
        ))

    def _sanitize_id(self, name: str) -> str:
        return re.sub(r"[^a-zA-Z0-9]", "", name)

    def render(self, output_path: str = "") -> str:
        if self.format == DiagramFormat.MERMAID:
            content = self._render_mermaid()
        elif self.format == DiagramFormat.PLANTUML:
            content = self._render_plantuml()
        elif self.format == DiagramFormat.D2:
            content = self._render_d2()
        else:
            content = self._render_mermaid()
        if output_path:
            try:
                out = Path(output_path)
                out.parent.mkdir(parents=True, exist_ok=True)
                with open(out, "w", encoding="utf-8") as f:
                    f.write(content)
            except OSError:
                pass
        return content

    def _render_mermaid(self) -> str:
        lines = ["```mermaid", "graph TD"]
        for person in self.persons:
            pid = self._sanitize_id(person.name)
            lines.append(f'    {pid}("{person.name}\\n{person.description}")')
        for system in self.systems:
            sid = self._sanitize_id(system.name)
            lines.append(f'    {sid}["{system.name}\\n{system.tech}"]')
        for container in self.containers:
            cid = self._sanitize_id(container.name)
            lines.append(f'    {cid}["{container.name}\\n{container.tech}"]')
        for rel in self.relationships:
            src = self._sanitize_id(rel.source)
            dst = self._sanitize_id(rel.destination)
            label = rel.label
            if rel.tech:
                label += f" ({rel.tech})"
            lines.append(f"    {src} -->|{label}| {dst}")
        lines.append("```")
        return "\n".join(lines)

    def _render_plantuml(self) -> str:
        lines = ["@startuml", f"title {self.system_name} — {self.level.value}"]
        for person in self.persons:
            lines.append(f'actor "{person.name}" as {self._sanitize_id(person.name)}')
        for system in self.systems:
            lines.append(f'component "{system.name}" as {self._sanitize_id(system.name)}')
        for container in self.containers:
            lines.append(f'node "{container.name}" as {self._sanitize_id(container.name)}')
        for rel in self.relationships:
            src = self._sanitize_id(rel.source)
            dst = self._sanitize_id(rel.destination)
            lines.append(f'{src} --> {dst} : {rel.label}')
        lines.append("@enduml")
        return "\n".join(lines)

    def _render_d2(self) -> str:
        lines = [f"{self._sanitize_id(self.system_name)}: {self.system_name}"]
        for person in self.persons:
            pid = self._sanitize_id(person.name)
            lines.append(f"{pid}: {{shape: person; label: \"{person.name}\"}}")
        for container in self.containers:
            cid = self._sanitize_id(container.name)
            lines.append(f"{cid}: {{label: \"{container.name}\\n{container.tech}\"}}")
        for rel in self.relationships:
            src = self._sanitize_id(rel.source)
            dst = self._sanitize_id(rel.destination)
            lines.append(f'{src} -> {dst}: "{rel.label}"')
        return "\n".join(lines)


@dataclass
class SequenceMessage:
    from_component: str
    to_component: str
    label: str
    is_async: bool = False


class InteractionDiagram:
    def __init__(self, title: str, format: DiagramFormat = DiagramFormat.MERMAID) -> None:
        self.title = title
        self.format = format
        self.participants: list[str] = []
        self.messages: list[SequenceMessage] = []

    def add_participant(self, name: str) -> None:
        if name not in self.participants:
            self.participants.append(name)

    def add_message(self, from_component: str, to_component: str, label: str,
                    is_async: bool = False) -> None:
        self.add_participant(from_component)
        self.add_participant(to_component)
        self.messages.append(SequenceMessage(
            from_component=from_component, to_component=to_component,
            label=label, is_async=is_async
        ))

    def render(self) -> str:
        if self.format == DiagramFormat.MERMAID:
            return self._render_mermaid()
        return self._render_plantuml()

    def _render_mermaid(self) -> str:
        lines = ["```mermaid", "sequenceDiagram"]
        for p in self.participants:
            safe = re.sub(r"[^a-zA-Z0-9]", "", p)
            lines.append(f"    participant {safe} as {p}")
        for msg in self.messages:
            src = re.sub(r"[^a-zA-Z0-9]", "", msg.from_component)
            dst = re.sub(r"[^a-zA-Z0-9]", "", msg.to_component)
            arrow = "-->>" if msg.is_async else "->>"
            lines.append(f"    {src} {arrow} {dst}: {msg.label}")
        lines.append("```")
        return "\n".join(lines)

    def _render_plantuml(self) -> str:
        lines = ["@startuml", f"title {self.title}"]
        for p in self.participants:
            safe = re.sub(r"[^a-zA-Z0-9]", "", p)
            lines.append(f'participant "{p}" as {safe}')
        for msg in self.messages:
            src = re.sub(r"[^a-zA-Z0-9]", "", msg.from_component)
            dst = re.sub(r"[^a-zA-Z0-9]", "", msg.to_component)
            arrow = "-->" if msg.is_async else "->"
            lines.append(f"{src} {arrow} {dst} : {msg.label}")
        lines.append("@enduml")
        return "\n".join(lines)


@dataclass
class DataFlowNode:
    name: str
    type: str
    classification: str = "internal"
    encrypted: bool = False


@dataclass
class DataFlowEdge:
    source: str
    destination: str
    data_type: str = ""
    protocol: str = ""
    encrypted: bool = False


class DataFlowDiagram:
    def __init__(self, title: str) -> None:
        self.title = title
        self.nodes: list[DataFlowNode] = []
        self.edges: list[DataFlowEdge] = []
        self.trust_boundary: list[str] = []

    def add_node(self, name: str, node_type: str = "process",
                 classification: str = "internal", encrypted: bool = False) -> None:
        self.nodes.append(DataFlowNode(
            name=name, type=node_type,
            classification=classification, encrypted=encrypted
        ))

    def add_edge(self, source: str, destination: str, data_type: str = "",
                 protocol: str = "", encrypted: bool = False) -> None:
        self.edges.append(DataFlowEdge(
            source=source, destination=destination,
            data_type=data_type, protocol=protocol, encrypted=encrypted
        ))

    def add_trust_boundary(self, name: str) -> None:
        if name not in self.trust_boundary:
            self.trust_boundary.append(name)

    def render_mermaid(self) -> str:
        lines = ["```mermaid", "graph LR"]
        for node in self.nodes:
            nid = re.sub(r"[^a-zA-Z0-9]", "", node.name)
            border = "solid" if node.encrypted else "dashed"
            label = f"{node.name}\\n{node.classification}"
            if node.type == "datastore":
                lines.append(f'    {nid}[["{label}"]]')
            else:
                lines.append(f'    {nid}["{label}"]')
        for edge in self.edges:
            src = re.sub(r"[^a-zA-Z0-9]", "", edge.source)
            dst = re.sub(r"[^a-zA-Z0-9]", "", edge.destination)
            label = edge.data_type or edge.protocol or "data"
            lines.append(f'    {src} -->|"{label}"| {dst}')
        lines.append("```")
        return "\n".join(lines)


@dataclass
class ServiceDeployment:
    service_name: str
    replicas: dict[str, int] = field(default_factory=dict)
    cpu: str = "250m"
    memory: str = "256Mi"
    health_check: str = "/health"
    port: int = 8080
    env_vars: list[str] = field(default_factory=list)
    scaling_policy: str = "fixed"
    min_replicas: int = 1
    max_replicas: int = 1


@dataclass
class Environment:
    name: str
    region: str = ""
    cluster: str = ""


class DeploymentGuide:
    def __init__(self, system_name: str, environments: list[Environment] | None = None) -> None:
        self.system_name = system_name
        self.environments = environments or []
        self.services: list[ServiceDeployment] = []

    def add_service(self, service: ServiceDeployment) -> None:
        self.services.append(service)

    def render(self, output: str = "deployment.md") -> str:
        lines = [
            f"# {self.system_name} — Deployment Guide\n",
            "## Environments\n",
        ]
        for env in self.environments:
            lines.append(f"### {env.name.title()}")
            lines.append(f"- **Region**: {env.region}")
            lines.append(f"- **Cluster**: {env.cluster}\n")

        lines.append("## Services\n")
        lines.append("| Service | Replicas (prod) | CPU | Memory | Port | Scaling |")
        lines.append("|---------|-----------------|-----|--------|------|---------|")
        for svc in self.services:
            prod_replicas = svc.replicas.get("production", 1)
            lines.append(
                f"| {svc.service_name} | {prod_replicas} | {svc.cpu} | "
                f"{svc.memory} | {svc.port} | {svc.scaling_policy} |"
            )
        lines.append("\n## Environment Variables\n")
        all_vars: set[str] = set()
        for svc in self.services:
            for v in svc.env_vars:
                all_vars.add(v)
        for var in sorted(all_vars):
            lines.append(f"- `{var}`")

        content = "\n".join(lines)
        try:
            with open(output, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError:
            pass
        return content


@dataclass
class EscalationContact:
    name: str
    channel: str
    priority: int = 1


@dataclass
class RunbookStep:
    order: int
    title: str
    action: str
    expected: str = ""
    verification: str = ""
    rollback: str = ""


class Runbook:
    def __init__(self, service: str, title: str, rto_minutes: int = 60,
                 rpo_minutes: int = 15, last_tested: str = "",
                 contacts: list[EscalationContact] | None = None) -> None:
        self.service = service
        self.title = title
        self.rto_minutes = rto_minutes
        self.rpo_minutes = rpo_minutes
        self.last_tested = last_tested
        self.contacts = contacts or []
        self.steps: list[RunbookStep] = []

    def add_step(self, step: RunbookStep) -> None:
        self.steps.append(step)
        self.steps.sort(key=lambda s: s.order)

    def render(self, output: str = "runbook.md") -> str:
        lines = [
            f"# {self.title}\n",
            f"**Service**: {self.service}",
            f"**RTO**: {self.rto_minutes} minutes",
            f"**RPO**: {self.rpo_minutes} minutes",
            f"**Last Tested**: {self.last_tested}\n",
            "## Escalation Contacts\n",
            "| Priority | Name | Channel |",
            "|----------|------|---------|",
        ]
        for contact in sorted(self.contacts, key=lambda c: c.priority):
            lines.append(f"| {contact.priority} | {contact.name} | {contact.channel} |")
        lines.append("\n## Recovery Steps\n")
        for step in self.steps:
            lines.append(f"### Step {step.order}: {step.title}\n")
            lines.append(f"**Action**: {step.action}\n")
            if step.expected:
                lines.append(f"**Expected Result**: {step.expected}\n")
            if step.verification:
                lines.append(f"**Verification**: {step.verification}\n")
            if step.rollback:
                lines.append(f"**Rollback**: {step.rollback}\n")
        content = "\n".join(lines)
        try:
            out = Path(output)
            out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError:
            pass
        return content


@dataclass
class ArchitectureIssue:
    severity: IssueSeverity
    category: str
    message: str
    suggestion: str = ""
    file_path: str = ""


class ArchitectureValidator:
    def __init__(self, doc_dir: str = "docs/architecture/",
                 infra_manifest: str = "k8s/",
                 codebase: str = "src/") -> None:
        self.doc_dir = Path(doc_dir)
        self.infra_manifest = Path(infra_manifest)
        self.codebase = Path(codebase)

    def validate(self) -> list[ArchitectureIssue]:
        issues: list[ArchitectureIssue] = []
        doc_files = list(self.doc_dir.rglob("*.md")) if self.doc_dir.exists() else []
        infra_files = list(self.infra_manifest.rglob("*.yaml")) if self.infra_manifest.exists() else []
        code_files = list(self.codebase.rglob("*.py")) if self.codebase.exists() else []
        if not doc_files:
            issues.append(ArchitectureIssue(
                severity=IssueSeverity.WARNING,
                category="coverage",
                message="No architecture documentation files found",
                suggestion="Create architecture docs in docs/architecture/"
            ))
        if not infra_files:
            issues.append(ArchitectureIssue(
                severity=IssueSeverity.INFO,
                category="infrastructure",
                message="No Kubernetes manifests found",
                suggestion="Add K8s manifests to k8s/ directory"
            ))
        described_services = set()
        for doc_file in doc_files:
            try:
                with open(doc_file, "r", encoding="utf-8") as f:
                    content = f.read()
            except (FileNotFoundError, UnicodeDecodeError):
                continue
            service_mentions = re.findall(r"###?\s+(.+?)(?:Service|Server|API)", content)
            for s in service_mentions:
                described_services.add(s.strip().lower())
        deployed_services: set[str] = set()
        for infra_file in infra_files:
            try:
                with open(infra_file, "r", encoding="utf-8") as f:
                    content = f.read()
            except (FileNotFoundError, UnicodeDecodeError):
                continue
            name_match = re.search(r"^\s*name:\s*(.+)$", content, re.MULTILINE)
            if name_match:
                deployed_services.add(name_match.group(1).strip().lower())
        undeployed = described_services - deployed_services
        for svc in undeployed:
            issues.append(ArchitectureIssue(
                severity=IssueSeverity.WARNING,
                category="drift",
                message=f"Documented service '{svc}' not found in deployment manifests",
                suggestion=f"Verify '{svc}' is deployed or remove from docs"
            ))
        return issues


def main() -> None:
    print("=" * 60)
    print("Architecture Decision Records & System Design Documentation")
    print("=" * 60)

    adr = ADR(
        id="ADR-003", title="Use PostgreSQL as Primary Database",
        status=ADRStatus.ACCEPTED, date="2025-01-15",
        authors=["Alice Chen", "Bob Martinez"],
        context="We need a primary relational database with ACID compliance.",
        decision="We will use PostgreSQL 16 as the primary database.",
        alternatives=["MySQL 8.0", "CockroachDB", "Amazon Aurora"],
        consequences=["Team must learn PostgreSQL-specific features",
                       "Need replication monitoring investment"]
    )
    registry = ADRRegistry(decisions_dir="docs/adr/")
    registry.add(adr)
    print(f"\n[ADR] {adr.id}: {adr.title} — status: {adr.status.value}")

    diagram = C4Diagram(system_name="E-Commerce Platform", level=DiagramLevel.CONTAINER)
    diagram.add_person("Customer", "Browses products")
    diagram.add_container("API Gateway", "Kong", "Routes requests")
    diagram.add_container("Order Service", "Node.js", "Processes orders")
    diagram.add_container("PostgreSQL", "Database", "Stores data")
    diagram.add_relationship("Customer", "API Gateway", "Uses", "HTTPS")
    diagram.add_relationship("API Gateway", "Order Service", "Routes to", "gRPC")
    diagram.add_relationship("Order Service", "PostgreSQL", "Reads/Writes")
    mermaid = diagram.render()
    print(f"\n[C4] Generated diagram ({len(mermaid)} chars)")

    seq = InteractionDiagram(title="Order Flow")
    seq.add_message("Customer", "API Gateway", "POST /orders")
    seq.add_message("API Gateway", "Order Service", "CreateOrder")
    seq.add_message("Order Service", "PostgreSQL", "INSERT order")
    seq.add_message("Order Service", "API Gateway", "OrderCreated")
    print(f"\n[Sequence] {len(seq.messages)} messages in flow")

    guide = DeploymentGuide(
        system_name="E-Commerce Platform",
        environments=[
            Environment(name="production", region="us-east-1", cluster="prod-eks"),
        ]
    )
    guide.add_service(ServiceDeployment(
        service_name="order-service", replicas={"production": 3},
        cpu="500m", memory="512Mi", port=3000, scaling_policy="hpa"
    ))
    print(f"\n[Deployment] {len(guide.services)} services configured")

    runbook = Runbook(
        service="order-service", title="Order Service DR",
        rto_minutes=30, rpo_minutes=5,
        contacts=[EscalationContact(name="On-Call", channel="pagerduty", priority=1)]
    )
    runbook.add_step(RunbookStep(
        order=1, title="Assess Impact",
        action="Check monitoring dashboard",
        verification="Error rate > 5% confirms incident"
    ))
    print(f"\n[Runbook] {runbook.service} — {len(runbook.steps)} steps, RTO: {runbook.rto_minutes}min")

    validator = ArchitectureValidator()
    print(f"\n[Validator] Ready to check doc/infra consistency")

    print("\n" + "=" * 60)
    print("All architecture documentation components initialized.")
    print("=" * 60)


if __name__ == "__main__":
    main()
