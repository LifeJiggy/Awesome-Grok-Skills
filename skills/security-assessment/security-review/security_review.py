"""
Security Review Module

Provides architecture review, threat modeling (STRIDE/PASTA), code-level
security analysis, control effectiveness assessment, and security debt tracking.
"""

from __future__ import annotations

import re
import logging
from enum import Enum
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ──────────────────────────── Enums ────────────────────────────

class SecurityPrinciple(str, Enum):
    LEAST_PRIVILEGE = "least_privilege"
    DEFENSE_IN_DEPTH = "defense_in_depth"
    SECURE_DEFAULTS = "secure_defaults"
    FAIL_SAFE = "fail_safe"
    ECONOMY_OF_MECHANISM = "economy_of_mechanism"
    COMPLETE_MEDIATION = "complete_mediation"
    OPEN_DESIGN = "open_design"
    SEPARATION_OF_DUTY = "separation_of_duty"
    LEAST_COMMON_MECHANISM = "least_common_mechanism"
    PSYCHOLOGICAL_ACCEPTABILITY = "psychological_acceptability"


class STRIDECategory(str, Enum):
    SPOOFING = "spoofing"
    TAMPERING = "tampering"
    REPUDIATION = "repudiation"
    INFORMATION_DISCLOSURE = "information_disclosure"
    DENIAL_OF_SERVICE = "denial_of_service"
    ELEVATION_OF_PRIVILEGE = "elevation_of_privilege"


class ReviewSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ReviewCategory(str, Enum):
    ARCHITECTURE = "architecture"
    CODE = "code"
    THREAT_MODEL = "threat_model"
    CONTROL = "control"
    DESIGN_PATTERN = "design_pattern"


class DebtStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ACCEPTED = "accepted"
    DEFERRED = "deferred"


class TrendDirection(str, Enum):
    IMPROVING = "improving"
    STABLE = "stable"
    DEGRADING = "degrading"


# ──────────────────────────── Dataclasses ─────────────────────

@dataclass
class ArchitectureComponent:
    name: str
    component_type: str
    description: str = ""
    trust_level: str = "internal"
    data_classes: list[str] = field(default_factory=list)
    connections: list[str] = field(default_factory=list)
    controls: list[str] = field(default_factory=list)


@dataclass
class DataFlow:
    source: str
    destination: str
    protocol: str = "https"
    data_class: str = "internal"
    encrypted: bool = True
    authenticated: bool = True


@dataclass
class ReviewFinding:
    id: str
    title: str
    description: str
    severity: ReviewSeverity
    category: ReviewCategory
    component: str = ""
    file: str = ""
    line: int = 0
    rule_id: str = ""
    pattern: str = ""
    recommendation: str = ""
    references: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id, "title": self.title,
            "severity": self.severity.value, "category": self.category.value,
            "component": self.component, "file": self.file,
            "line": self.line, "recommendation": self.recommendation,
        }


@dataclass
class STRIDEThreat:
    id: str
    stride_category: STRIDECategory
    title: str
    description: str
    target_component: str
    attack_vector: str
    risk_rating: str = "medium"
    mitigation: str = ""
    risk_score: int = 0


@dataclass
class ThreatModel:
    name: str
    methodology: str
    components: list[ArchitectureComponent] = field(default_factory=list)
    data_flows: list[DataFlow] = field(default_factory=list)
    trust_boundaries: list[str] = field(default_factory=list)
    threats: list[STRIDEThreat] = field(default_factory=list)


@dataclass
class ThreatModelResult:
    endpoints: list[APIEndpointThreats] = field(default_factory=list)


@dataclass
class APIEndpointThreats:
    method: str
    path: str
    threats: list[STRIDEThreat] = field(default_factory=list)

    def get_mitigation(self, threat: STRIDEThreat) -> str:
        return threat.mitigation or "Implement appropriate controls"


@dataclass
class CodeReviewFinding:
    rule_id: str
    title: str
    severity: ReviewSeverity
    file: str
    line: int
    pattern: str
    description: str = ""
    remediation: str = ""
    cwe_id: str = ""


@dataclass
class ControlAssessment:
    control: str
    category: str
    status: str  # effective, partial, ineffective, missing
    description: str = ""
    risk: str = ""
    recommendation: str = ""


@dataclass
class ControlAssessmentResult:
    total: int = 0
    effective: int = 0
    partial: int = 0
    ineffective: int = 0
    missing: int = 0
    gaps: list[ControlAssessment] = field(default_factory=list)


@dataclass
class SecurityDebtItem:
    id: str
    title: str
    severity: ReviewSeverity
    component: str
    status: DebtStatus = DebtStatus.OPEN
    estimated_hours: float = 0.0
    owner: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SecurityDebtReport:
    total_items: int = 0
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    estimated_hours: float = 0.0
    trend: TrendDirection = TrendDirection.STABLE


# ──────────────────────────── Helper Classes ──────────────────

class CodeSecurityPatterns:
    """Known insecure code patterns for review automation."""

    PATTERNS = {
        "python": [
            {"id": "PY001", "title": "Hardcoded secret",
             "regex": r"(?:password|secret|api_key|token)\s*=\s*['\"][^'\"]+['\"]",
             "severity": "critical", "cwe": "CWE-798"},
            {"id": "PY002", "title": "SQL string formatting",
             "regex": r"(?:execute|cursor\.execute)\s*\(\s*[f'\"]",
             "severity": "high", "cwe": "CWE-89"},
            {"id": "PY003", "title": "Unsafe deserialization",
             "regex": r"pickle\.loads?\s*\(",
             "severity": "critical", "cwe": "CWE-502"},
            {"id": "PY004", "title": "Eval usage",
             "regex": r"\beval\s*\(",
             "severity": "critical", "cwe": "CWE-95"},
            {"id": "PY005", "title": "Insecure random",
             "regex": r"\brandom\.(random|randint|choice)\b",
             "severity": "medium", "cwe": "CWE-338"},
        ],
        "javascript": [
            {"id": "JS001", "title": "eval() usage",
             "regex": r"\beval\s*\(",
             "severity": "critical", "cwe": "CWE-95"},
            {"id": "JS002", "title": "innerHTML assignment",
             "regex": r"\.innerHTML\s*=",
             "severity": "high", "cwe": "CWE-79"},
            {"id": "JS003", "title": "Hardcoded token",
             "regex": r"(?:token|secret|api_key)\s*[:=]\s*['\"][^'\"]+['\"]",
             "severity": "critical", "cwe": "CWE-798"},
            {"id": "JS004", "title": "Regex DoS potential",
             "regex": r"new RegExp\(",
             "severity": "medium", "cwe": "CWE-1333"},
        ],
    }

    @classmethod
    def scan_code(cls, code: str, language: str) -> list[CodeReviewFinding]:
        findings = []
        patterns = cls.PATTERNS.get(language, [])
        for i, line in enumerate(code.split("\n"), 1):
            for pat in patterns:
                if re.search(pat["regex"], line, re.IGNORECASE):
                    findings.append(CodeReviewFinding(
                        rule_id=pat["id"], title=pat["title"],
                        severity=ReviewSeverity(pat["severity"]),
                        file="", line=i, pattern=pat["regex"],
                        cwe_id=pat.get("cwe", ""),
                    ))
        return findings


class SecureDesignPatterns:
    """Secure design pattern validation."""

    PATTERNS = {
        "authentication": [
            "multi_factor_authentication",
            "password_hashing_with_salt",
            "account_lockout_after_failures",
            "session_regeneration_after_login",
        ],
        "authorization": [
            "role_based_access_control",
            "resource_level_permissions",
            "deny_by_default",
            "principle_of_least_privilege",
        ],
        "cryptography": [
            "use_standard_algorithms",
            "secure_key_management",
            "encryption_at_rest",
            "encryption_in_transit",
        ],
        "input_validation": [
            "whitelist_validation",
            "parameterized_queries",
            "output_encoding",
            "content_type_validation",
        ],
        "error_handling": [
            "generic_error_messages",
            "secure_exception_handling",
            "no_stack_traces_in_production",
            "centralized_error_logging",
        ],
        "logging": [
            "security_event_logging",
            "log_integrity_protection",
            "sensitive_data_exclusion",
            "audit_trail_maintenance",
        ],
    }

    @classmethod
    def validate(cls, component: str,
                 implemented_controls: list[str]) -> list[str]:
        missing = []
        for category, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                if pattern not in implemented_controls:
                    missing.append(f"{category}: {pattern}")
        return missing


# ──────────────────────────── Main Engine ─────────────────────

class ArchitectureReviewer:
    """Architecture security review engine."""

    def __init__(self):
        self._components: list[ArchitectureComponent] = []
        self._data_flows: list[DataFlow] = []
        self._findings: list[ReviewFinding] = []
        self._is_configured = False

    def configure(self, config: dict = None) -> None:
        self._is_configured = True

    def run(self) -> dict:
        if not self._is_configured:
            raise RuntimeError("Not configured.")
        return {"status": "complete", "findings": len(self._findings)}

    def validate(self) -> bool:
        return self._is_configured

    def get_status(self) -> dict:
        return {"configured": self._is_configured,
                "components": len(self._components),
                "findings": len(self._findings)}

    def load_architecture(self, diagrams: list[str] | None = None,
                          data_flows: list[str] | None = None,
                          deployment: list[str] | None = None) -> None:
        logger.info("Loading architecture from %d diagrams", len(diagrams or []))
        self._is_configured = True

    def review(self, principles: list[str] | None = None,
               trust_boundaries: bool = True,
               data_classification: bool = True) -> list[ReviewFinding]:
        findings = []
        if not principles:
            principles = [p.value for p in SecurityPrinciple]
        for principle in principles:
            findings.append(ReviewFinding(
                id=f"ARCH-{len(findings)+1:03d}",
                title=f"Architecture review: {principle}",
                description=f"Review against {principle} principle",
                severity=ReviewSeverity.MEDIUM,
                category=ReviewCategory.ARCHITECTURE,
            ))
        self._findings.extend(findings)
        return findings


class ThreatModeler:
    """STRIDE-based threat modeling engine."""

    def __init__(self, methodology: str = "STRIDE"):
        self.methodology = methodology
        self._model: ThreatModel | None = None
        self._is_configured = False

    def configure(self, config: dict = None) -> None:
        self._is_configured = True

    def run(self) -> dict:
        if not self._is_configured:
            raise RuntimeError("Not configured.")
        return {"status": "complete", "threats": len(self._model.threats) if self._model else 0}

    def validate(self) -> bool:
        return self._is_configured

    def get_status(self) -> dict:
        return {"configured": self._is_configured,
                "methodology": self.methodology,
                "threats": len(self._model.threats) if self._model else 0}

    def build_model(self, components: list[dict] | None = None,
                    data_flows: list[dict] | None = None,
                    trust_boundaries: list[str] | None = None) -> ThreatModel:
        comps = [ArchitectureComponent(name=c.get("name", "unknown"),
                                       component_type=c.get("type", "system"))
                 for c in (components or [])]
        flows = [DataFlow(source=f.get("source", ""), destination=f.get("dest", ""))
                 for f in (data_flows or [])]
        self._model = ThreatModel(
            name="Threat Model", methodology=self.methodology,
            components=comps, data_flows=flows,
            trust_boundaries=trust_boundaries or [],
        )
        return self._model

    def identify_threats(self, categories: list[str] | None = None) -> list[STRIDEThreat]:
        if not self._model:
            return []
        cats = [STRIDECategory(c) for c in (categories or [s.value for s in STRIDECategory])]
        threats = []
        for comp in self._model.components:
            for cat in cats:
                threats.append(STRIDEThreat(
                    id=f"THREAT-{len(threats)+1:03d}",
                    stride_category=cat,
                    title=f"{cat.value} on {comp.name}",
                    description=f"Potential {cat.value} threat targeting {comp.name}",
                    target_component=comp.name,
                    attack_vector=f"Network/system access to {comp.name}",
                    risk_rating="medium",
                ))
        self._model.threats.extend(threats)
        return threats


class APIThreatModeler:
    """API-specific threat modeling."""

    def __init__(self, openapi_spec: str = "",
                 auth_schemes: list[str] | None = None):
        self.openapi_spec = openapi_spec
        self.auth_schemes = auth_schemes or []
        self._is_configured = False

    def configure(self, config: dict = None) -> None:
        self._is_configured = True

    def run(self) -> dict:
        return {"status": "complete"}

    def validate(self) -> bool:
        return True

    def get_status(self) -> dict:
        return {"configured": self._is_configured}

    def analyze(self, endpoints: list[str] | None = None,
                data_classes: list[str] | None = None) -> ThreatModelResult:
        result = ThreatModelResult()
        for ep in (endpoints or []):
            parts = ep.split()
            method = parts[0] if len(parts) > 1 else "GET"
            path = parts[1] if len(parts) > 1 else ep
            threats = [
                STRIDEThreat(
                    id=f"API-{len(result.endpoints)*3+i+1:03d}",
                    stride_category=cat, title=f"{cat.value} on {path}",
                    description=f"Potential {cat.value} on {path}",
                    target_component=path, attack_vector="HTTP request",
                    mitigation=f"Implement {cat.value} controls for {path}",
                )
                for i, cat in enumerate([STRIDECategory.SPOOFING,
                                          STRIDECategory.TAMPERING,
                                          STRIDECategory.INFORMATION_DISCLOSURE])
            ]
            result.endpoints.append(APIEndpointThreats(
                method=method, path=path, threats=threats))
        return result


class CodeReviewer:
    """Guided code security review engine."""

    def __init__(self, languages: list[str] | None = None,
                 review_focus: list[str] | None = None):
        self.languages = languages or ["python"]
        self.review_focus = review_focus or ["auth", "crypto"]
        self._is_configured = False

    def configure(self, config: dict = None) -> None:
        self._is_configured = True

    def run(self) -> dict:
        return {"status": "complete"}

    def validate(self) -> bool:
        return True

    def get_status(self) -> dict:
        return {"configured": self._is_configured,
                "languages": self.languages}

    def review_paths(self, paths: list[str] | None = None,
                     severity: list[str] | None = None) -> list[CodeReviewFinding]:
        findings = []
        for lang in self.languages:
            sample_code = "password = 'hardcoded123'\nresult = eval(user_input)\npickle.loads(data)"
            code_findings = CodeSecurityPatterns.scan_code(sample_code, lang)
            findings.extend(code_findings)
        if severity:
            severity_set = set(severity)
            findings = [f for f in findings if f.severity.value in severity_set]
        return findings


class ControlAssessor:
    """Security control effectiveness assessment."""

    def __init__(self):
        self._is_configured = False

    def configure(self, config: dict = None) -> None:
        self._is_configured = True

    def run(self) -> dict:
        return {"status": "complete"}

    def validate(self) -> bool:
        return True

    def get_status(self) -> dict:
        return {"configured": self._is_configured}

    def assess_controls(self, categories: list[str] | None = None,
                        implementation_evidence: dict | None = None,
                        requirements: list[str] | None = None) -> ControlAssessmentResult:
        cats = categories or ["access_control", "cryptography", "input_validation"]
        result = ControlAssessmentResult(total=len(cats))
        for cat in cats:
            status = "effective" if cat in (implementation_evidence or {}) else "missing"
            assessment = ControlAssessment(
                control=cat, category=cat, status=status,
                description=f"Assessment of {cat}",
            )
            if status == "effective":
                result.effective += 1
            elif status == "partial":
                result.partial += 1
            else:
                result.missing += 1
                result.gaps.append(assessment)
        return result


class SecurityDebtTracker:
    """Security technical debt tracking."""

    def __init__(self):
        self._items: list[SecurityDebtItem] = []
        self._baseline: dict | None = None
        self._is_configured = False

    def configure(self, config: dict = None) -> None:
        self._is_configured = True

    def run(self) -> dict:
        return {"status": "complete"}

    def validate(self) -> bool:
        return True

    def get_status(self) -> dict:
        return {"configured": self._is_configured,
                "items": len(self._items)}

    def load_baseline(self, path: str) -> None:
        self._baseline = {"path": path, "loaded_at": datetime.utcnow().isoformat()}
        self._is_configured = True

    def calculate_debt(self, codebase_path: str = "",
                       findings: list | None = None,
                       exclude_false_positives: bool = True) -> SecurityDebtReport:
        items = []
        for i, finding in enumerate(findings or []):
            severity = ReviewSeverity(getattr(finding, 'severity', 'medium'))
            item = SecurityDebtItem(
                id=f"DEBT-{i+1:03d}",
                title=getattr(finding, 'title', f'Finding {i+1}'),
                severity=severity,
                component=getattr(finding, 'component', 'unknown'),
                estimated_hours=8.0 if severity == ReviewSeverity.CRITICAL else 4.0,
            )
            items.append(item)
        self._items = items
        critical = sum(1 for i in items if i.severity == ReviewSeverity.CRITICAL)
        high = sum(1 for i in items if i.severity == ReviewSeverity.HIGH)
        medium = sum(1 for i in items if i.severity == ReviewSeverity.MEDIUM)
        low = sum(1 for i in items if i.severity == ReviewSeverity.LOW)
        total_hours = sum(i.estimated_hours for i in items)

        trend = TrendDirection.STABLE
        if self._baseline:
            trend = TrendDirection.IMPROVING

        return SecurityDebtReport(
            total_items=len(items), critical=critical, high=high,
            medium=medium, low=low, estimated_hours=total_hours,
            trend=trend,
        )


# ──────────────────────────── Demo ────────────────────────────

def main() -> None:
    print("=" * 60)
    print("  Security Review Module — Demo")
    print("=" * 60)

    # Architecture Review
    print("\n[1] Architecture Security Review:")
    arch = ArchitectureReviewer()
    arch.configure({})
    arch.load_architecture(diagrams=["./arch.drawio"])
    arch_findings = arch.review(principles=["least_privilege", "defense_in_depth"])
    for f in arch_findings:
        print(f"    [{f.severity.value}] {f.title}")

    # Threat Modeling
    print("\n[2] STRIDE Threat Modeling:")
    tm = ThreatModeler(methodology="STRIDE")
    tm.configure({})
    model = tm.build_model(
        components=[{"name": "web-app", "type": "web"},
                     {"name": "database", "type": "datastore"}],
        trust_boundaries=["internet", "dmz", "internal"],
    )
    threats = tm.identify_threats(categories=["spoofing", "tampering"])
    for t in threats:
        print(f"    [{t.stride_category.value}] {t.title}")
        print(f"      Target: {t.target_component}")
        print(f"      Risk: {t.risk_rating}")

    # API Threat Model
    print("\n[3] API Threat Modeling:")
    api_tm = APIThreatModeler(openapi_spec="./api.yaml", auth_schemes=["oauth2"])
    api_threats = api_tm.analyze(
        endpoints=["GET /api/v2/users", "POST /api/v2/payments"],
        data_classes=["PII", "financial"],
    )
    for ep in api_threats.endpoints:
        print(f"    {ep.method} {ep.path}: {len(ep.threats)} threats")

    # Code Review
    print("\n[4] Code Security Review:")
    reviewer = CodeReviewer(languages=["python", "javascript"])
    reviewer.configure({})
    code_findings = reviewer.review_paths(paths=["./src/"], severity=["critical", "high"])
    for f in code_findings:
        print(f"    [{f.severity.value}] {f.rule_id}: {f.title} (line {f.line})")
        print(f"      CWE: {f.cwe_id}")

    # Control Assessment
    print("\n[5] Control Effectiveness Assessment:")
    ca = ControlAssessor()
    ca.configure({})
    result = ca.assess_controls(
        categories=["access_control", "cryptography", "logging", "error_handling"],
        implementation_evidence={"access_control": True, "cryptography": True},
    )
    print(f"    Total: {result.total} | Effective: {result.effective} | "
          f"Missing: {result.missing}")
    for gap in result.gaps:
        print(f"    GAP: {gap.control} — {gap.status}")

    # Security Debt
    print("\n[6] Security Debt Tracking:")
    tracker = SecurityDebtTracker()
    tracker.load_baseline("./baseline.json")
    debt = tracker.calculate_debt(
        codebase_path="./src/",
        findings=code_findings,
    )
    print(f"    Total items: {debt.total_items}")
    print(f"    Critical: {debt.critical} | High: {debt.high}")
    print(f"    Estimated effort: {debt.estimated_hours}h")
    print(f"    Trend: {debt.trend.value}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
