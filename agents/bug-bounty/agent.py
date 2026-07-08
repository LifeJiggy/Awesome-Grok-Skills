"""
Bug Bounty Agent - Vulnerability Management and Research.
Comprehensive bug bounty program management with triage, rewards, and advisories.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import hashlib
import logging
import re
import uuid
from collections import defaultdict
from dataclasses import asdict


class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SubmissionStatus(Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    TRIAGED = "triaged"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DUPLICATE = "duplicate"
    RESOLVED = "resolved"
    PUBLISHED = "published"


class ProgramStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class PaymentStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Config:
    min_bounty: int = 100
    max_bounty: int = 50000
    response_time: int = 48
    resolution_time: int = 90
    similarity_threshold: float = 0.8
    min_quality_score: float = 0.5


@dataclass
class Program:
    id: str
    name: str
    description: str
    reward_min: int
    reward_max: int
    status: ProgramStatus
    scope: List[Dict[str, Any]]
    out_of_scope: List[Dict[str, Any]]
    response_time: int
    resolution_time: int
    created_at: datetime
    updated_at: datetime


@dataclass
class Researcher:
    id: str
    username: str
    email: str
    display_name: Optional[str]
    bio: Optional[str]
    skills: List[str]
    reputation: int
    total_bounties: float
    submissions_count: int
    created_at: datetime


@dataclass
class Submission:
    id: str
    program_id: str
    researcher_id: str
    title: str
    description: str
    severity: Optional[Severity]
    status: SubmissionStatus
    bounty: Optional[float]
    cve_id: Optional[str]
    proof_of_concept: Optional[Dict[str, Any]]
    target_url: Optional[str]
    parameter: Optional[str]
    cvss_metrics: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    triage_notes: Optional[str] = None
    quality_score: Optional[float] = None
    duplicate_of: Optional[str] = None


@dataclass
class Advisory:
    id: str
    submission_id: str
    cve_id: Optional[str]
    title: str
    description: str
    affected_versions: List[str]
    remediation: str
    severity: Severity
    status: str
    published: bool
    published_at: Optional[datetime]
    created_at: datetime


@dataclass
class Payment:
    id: str
    submission_id: str
    researcher_id: str
    amount: float
    status: PaymentStatus
    payment_method: str
    transaction_id: Optional[str]
    created_at: datetime


class ValidationResult:
    def __init__(self, valid: bool, issues: List[str]):
        self.valid = valid
        self.issues = issues


class SeverityResult:
    def __init__(self, severity: Severity, cvss_score: float, confidence: float):
        self.severity = severity
        self.cvss_score = cvss_score
        self.confidence = confidence


class BugBountyAgent:
    """Agent for bug bounty program management."""
    
    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._programs: Dict[str, Program] = {}
        self._researchers: Dict[str, Researcher] = {}
        self._submissions: Dict[str, Submission] = {}
        self._advisories: Dict[str, Advisory] = {}
        self._payments: Dict[str, Payment] = {}
        self.logger = logging.getLogger(__name__)
    
    def create_program(self, name: str, description: str,
                       reward_range: str,
                       scope: Optional[List[Dict[str, Any]]] = None,
                       out_of_scope: Optional[List[Dict[str, Any]]] = None,
                       response_time: Optional[int] = None,
                       resolution_time: Optional[int] = None) -> Dict[str, Any]:
        """Create bug bounty program."""
        reward_min, reward_max = self._parse_reward_range(reward_range)
        
        program = Program(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            reward_min=reward_min,
            reward_max=reward_max,
            status=ProgramStatus.DRAFT,
            scope=scope or [],
            out_of_scope=out_of_scope or [],
            response_time=response_time or self._config.response_time,
            resolution_time=resolution_time or self._config.resolution_time,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self._programs[program.id] = program
        self.logger.info(f"Created program: {program.id}")
        
        return {
            "id": program.id,
            "name": program.name,
            "status": program.status.value,
            "reward_range": f"{program.reward_min}-{program.reward_max}"
        }
    
    def _parse_reward_range(self, reward_range: str) -> Tuple[int, int]:
        """Parse reward range string like '100-5000'."""
        match = re.match(r"(\d+)\s*[-–]\s*(\d+)", reward_range)
        if not match:
            raise ValueError(f"Invalid reward range: {reward_range}")
        
        reward_min = int(match.group(1))
        reward_max = int(match.group(2))
        
        if reward_min > reward_max:
            raise ValueError(f"Min bounty cannot exceed max: {reward_range}")
        
        return reward_min, reward_max
    
    def activate_program(self, program_id: str) -> Dict[str, Any]:
        """Activate a bug bounty program."""
        program = self._programs.get(program_id)
        if not program:
            raise ValueError(f"Program not found: {program_id}")
        
        program.status = ProgramStatus.ACTIVE
        program.updated_at = datetime.utcnow()
        
        self.logger.info(f"Activated program: {program_id}")
        
        return {
            "id": program.id,
            "name": program.name,
            "status": program.status.value
        }
    
    def submit_vulnerability(self, program_id: str, researcher_id: str,
                             title: str, description: str,
                             severity: Optional[str] = None,
                             proof_of_concept: Optional[Dict[str, Any]] = None,
                             target_url: Optional[str] = None,
                             parameter: Optional[str] = None,
                             cvss_metrics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Submit vulnerability to bug bounty program."""
        # Validate program exists and is active
        program = self._programs.get(program_id)
        if not program:
            raise ValueError(f"Program not found: {program_id}")
        
        if program.status != ProgramStatus.ACTIVE:
            raise ValueError(f"Program is not active: {program.status.value}")
        
        # Validate researcher exists
        if researcher_id not in self._researchers:
            raise ValueError(f"Researcher not found: {researcher_id}")
        
        # Validate severity if provided
        submission_severity = None
        if severity:
            try:
                submission_severity = Severity(severity.lower())
            except ValueError:
                raise ValueError(f"Invalid severity: {severity}")
        
        submission = Submission(
            id=str(uuid.uuid4()),
            program_id=program_id,
            researcher_id=researcher_id,
            title=title,
            description=description,
            severity=submission_severity,
            status=SubmissionStatus.PENDING,
            bounty=None,
            cve_id=None,
            proof_of_concept=proof_of_concept,
            target_url=target_url,
            parameter=parameter,
            cvss_metrics=cvss_metrics,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self._submissions[submission.id] = submission
        
        self.logger.info(f"Submission created: {submission.id} for program {program_id}")
        
        return {
            "id": submission.id,
            "program_id": submission.program_id,
            "researcher_id": submission.researcher_id,
            "title": submission.title,
            "status": submission.status.value,
            "created_at": submission.created_at.isoformat()
        }
    
    def triage_submission(self, submission_id: str,
                          validate: bool = True,
                          assess_severity: bool = True,
                          check_duplicates: bool = True) -> Dict[str, Any]:
        """Triage vulnerability submission."""
        submission = self._submissions.get(submission_id)
        if not submission:
            raise ValueError(f"Submission not found: {submission_id}")
        
        result = {
            "submission_id": submission_id,
            "valid": True,
            "severity": None,
            "cvss_score": None,
            "duplicates": [],
            "quality_score": None,
            "issues": []
        }
        
        # Step 1: Validate submission
        if validate:
            validation = self._validate_submission(submission)
            result["valid"] = validation.valid
            result["issues"] = validation.issues
            
            if not validation.valid:
                submission.status = SubmissionStatus.REJECTED
                submission.updated_at = datetime.utcnow()
                return result
        
        # Step 2: Assess severity
        if assess_severity:
            severity_result = self._assess_severity(submission)
            result["severity"] = severity_result.severity.value
            result["cvss_score"] = severity_result.cvss_score
            submission.severity = severity_result.severity
        
        # Step 3: Check for duplicates
        if check_duplicates:
            duplicates = self._find_duplicates(submission)
            result["duplicates"] = [
                {"id": d.id, "title": d.title} for d in duplicates
            ]
            
            if duplicates:
                submission.status = SubmissionStatus.DUPLICATE
                submission.duplicate_of = duplicates[0].id
                submission.updated_at = datetime.utcnow()
                return result
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(submission)
        result["quality_score"] = quality_score
        submission.quality_score = quality_score
        
        # Update status
        if submission.severity:
            submission.status = SubmissionStatus.TRIAGED
        else:
            submission.status = SubmissionStatus.VALIDATED
        
        submission.updated_at = datetime.utcnow()
        
        self.logger.info(f"Triage completed for submission: {submission_id}")
        
        return result
    
    def _validate_submission(self, submission: Submission) -> ValidationResult:
        """Validate submission completeness and quality."""
        issues = []
        
        # Check required fields
        if not submission.title or len(submission.title.strip()) < 10:
            issues.append("Title is too short (minimum 10 characters)")
        
        if not submission.description or len(submission.description.strip()) < 50:
            issues.append("Description is too short (minimum 50 characters)")
        
        if not submission.proof_of_concept:
            issues.append("Proof of concept is required")
        else:
            poc = submission.proof_of_concept
            if not poc.get("steps") or len(poc.get("steps", [])) == 0:
                issues.append("Proof of concept must include reproduction steps")
        
        # Check scope compliance
        if submission.target_url:
            program = self._programs.get(submission.program_id)
            if program and not self._is_in_scope(submission.target_url, program):
                issues.append("Target URL is out of scope")
        
        return ValidationResult(
            valid=len(issues) == 0,
            issues=issues
        )
    
    def _is_in_scope(self, target_url: str, program: Program) -> bool:
        """Check if target URL is in program scope."""
        from urllib.parse import urlparse
        
        parsed = urlparse(target_url)
        domain = parsed.netloc or parsed.path
        
        # Check out of scope first
        for excluded in program.out_of_scope:
            pattern = excluded.get("target", "")
            if pattern.startswith("*."):
                suffix = pattern[2:]
                if domain.endswith(suffix):
                    return False
            elif domain == pattern or domain.endswith("." + pattern):
                return False
        
        # Check in scope
        if not program.scope:
            return True
        
        for included in program.scope:
            pattern = included.get("target", "")
            if pattern.startswith("*."):
                suffix = pattern[2:]
                if domain.endswith(suffix):
                    return True
            elif domain == pattern or domain.endswith("." + pattern):
                return True
        
        return False
    
    def _assess_severity(self, submission: Submission) -> SeverityResult:
        """Assess vulnerability severity."""
        # Use provided severity if available
        if submission.severity:
            return SeverityResult(
                severity=submission.severity,
                cvss_score=self._estimate_cvss(submission.severity),
                confidence=0.8
            )
        
        # Otherwise, estimate from CVSS metrics
        if submission.cvss_metrics:
            cvss_score = self._calculate_cvss(submission.cvss_metrics)
            severity = self._cvss_to_severity(cvss_score)
            return SeverityResult(
                severity=severity,
                cvss_score=cvss_score,
                confidence=0.9
            )
        
        # Default to medium if no information
        return SeverityResult(
            severity=Severity.MEDIUM,
            cvss_score=5.0,
            confidence=0.3
        )
    
    def _calculate_cvss(self, metrics: Dict[str, Any]) -> float:
        """Calculate CVSS v3.1 base score from metrics."""
        # Simplified CVSS calculation
        # In production, use a proper CVSS library
        
        av = {"network": 0.85, "adjacent": 0.62, "local": 0.55, "physical": 0.2}
        ac = {"low": 0.77, "high": 0.44}
        pr = {"none": 0.85, "low": 0.62, "high": 0.27}
        ui = {"none": 0.85, "required": 0.62}
        s = {"unchanged": 0, "changed": 1}
        c = {"high": 0.56, "low": 0.22, "none": 0}
        i = {"high": 0.56, "low": 0.22, "none": 0}
        a = {"high": 0.56, "low": 0.22, "none": 0}
        
        attack_vector = av.get(metrics.get("attack_vector", "network"), 0.85)
        attack_complexity = ac.get(metrics.get("attack_complexity", "low"), 0.77)
        privileges_required = pr.get(metrics.get("privileges_required", "none"), 0.85)
        user_interaction = ui.get(metrics.get("user_interaction", "none"), 0.85)
        scope = s.get(metrics.get("scope", "unchanged"), 0)
        confidentiality = c.get(metrics.get("confidentiality", "none"), 0)
        integrity = i.get(metrics.get("integrity", "none"), 0)
        availability = a.get(metrics.get("availability", "none"), 0)
        
        iss = 1 - ((1 - confidentiality) * (1 - integrity) * (1 - availability))
        impact = 7.52 * (iss - 0.029) - 3.25 * pow((iss - 0.02), 15)
        exploitability = 8.22 * attack_vector * attack_complexity * privileges_required * user_interaction
        
        if scope == 0:
            base_score = min(10, impact + exploitability)
        else:
            base_score = min(10, 1.08 * (impact + exploitability))
        
        return max(0.0, round(base_score, 1))
    
    def _estimate_cvss(self, severity: Severity) -> float:
        """Estimate CVSS score from severity."""
        mapping = {
            Severity.LOW: 3.5,
            Severity.MEDIUM: 6.0,
            Severity.HIGH: 8.0,
            Severity.CRITICAL: 9.5
        }
        return mapping.get(severity, 5.0)
    
    def _cvss_to_severity(self, cvss_score: float) -> Severity:
        """Convert CVSS score to severity."""
        if cvss_score >= 9.0:
            return Severity.CRITICAL
        elif cvss_score >= 7.0:
            return Severity.HIGH
        elif cvss_score >= 4.0:
            return Severity.MEDIUM
        else:
            return Severity.LOW
    
    def _find_duplicates(self, submission: Submission) -> List[Submission]:
        """Find duplicate submissions."""
        if not submission.target_url:
            return []
        
        duplicates = []
        
        for existing in self._submissions.values():
            if existing.id == submission.id:
                continue
            
            if existing.target_url == submission.target_url:
                if existing.parameter == submission.parameter:
                    duplicates.append(existing)
                    continue
            
            # Text similarity check
            if self._text_similarity(
                f"{submission.title} {submission.description}",
                f"{existing.title} {existing.description}"
            ) >= self._config.similarity_threshold:
                duplicates.append(existing)
        
        return duplicates
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using simple word overlap."""
        words1 = set(re.findall(r"\w+", text1.lower()))
        words2 = set(re.findall(r"\w+", text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_quality_score(self, submission: Submission) -> float:
        """Calculate quality score for submission."""
        score = 0.0
        
        # Description quality (25%)
        description = submission.description or ""
        if len(description) >= 200:
            score += 0.25
        elif len(description) >= 100:
            score += 0.15
        
        # Proof of concept (25%)
        poc = submission.proof_of_concept or {}
        if poc.get("steps") and len(poc.get("steps", [])) >= 3:
            score += 0.15
        if poc.get("screenshot") or poc.get("video"):
            score += 0.10
        
        # Impact assessment (25%)
        if submission.cvss_metrics:
            score += 0.15
        if submission.target_url:
            score += 0.10
        
        # Remediation suggestions (25%)
        if poc.get("remediation"):
            score += 0.15
        if poc.get("references"):
            score += 0.10
        
        return min(1.0, score)
    
    def calculate_bounty(self, submission_id: str,
                         apply_multipliers: bool = True) -> Dict[str, Any]:
        """Calculate bounty for submission."""
        submission = self._submissions.get(submission_id)
        if not submission:
            raise ValueError(f"Submission not found: {submission_id}")
        
        program = self._programs.get(submission.program_id)
        if not program:
            raise ValueError(f"Program not found: {submission.program_id}")
        
        if not submission.severity:
            raise ValueError("Submission has not been triaged")
        
        # Base bounty from severity
        base_bounty = self._get_base_bounty(submission.severity, program)
        
        # Apply multipliers if requested
        final_bounty = base_bounty
        multipliers_applied = []
        
        if apply_multipliers:
            # Quality multiplier
            if submission.quality_score:
                if submission.quality_score >= 0.9:
                    final_bounty *= 1.5
                    multipliers_applied.append("quality_excellent")
                elif submission.quality_score >= 0.7:
                    final_bounty *= 1.2
                    multipliers_applied.append("quality_good")
            
            # Proof of concept multiplier
            poc = submission.proof_of_concept or {}
            if poc.get("working_exploit"):
                final_bounty *= 1.2
                multipliers_applied.append("working_exploit")
        
        # Apply caps
        final_bounty = max(program.reward_min, min(final_bounty, program.reward_max))
        
        # Update submission
        submission.bounty = round(final_bounty, 2)
        submission.updated_at = datetime.utcnow()
        
        return {
            "submission_id": submission_id,
            "base_bounty": base_bounty,
            "final_bounty": submission.bounty,
            "severity": submission.severity.value,
            "multipliers_applied": multipliers_applied,
            "currency": "USD"
        }
    
    def _get_base_bounty(self, severity: Severity, program: Program) -> float:
        """Get base bounty for severity level."""
        severity_multipliers = {
            Severity.LOW: 1.0,
            Severity.MEDIUM: 2.0,
            Severity.HIGH: 3.0,
            Severity.CRITICAL: 5.0
        }
        
        multiplier = severity_multipliers.get(severity, 1.0)
        return program.reward_min * multiplier
    
    def process_payment(self, submission_id: str) -> Dict[str, Any]:
        """Process bounty payment."""
        submission = self._submissions.get(submission_id)
        if not submission:
            raise ValueError(f"Submission not found: {submission_id}")
        
        if not submission.bounty:
            raise ValueError("Bounty has not been calculated")
        
        if submission.status not in [SubmissionStatus.ACCEPTED, SubmissionStatus.TRIAGED]:
            raise ValueError(f"Submission not ready for payment: {submission.status.value}")
        
        payment = Payment(
            id=str(uuid.uuid4()),
            submission_id=submission_id,
            researcher_id=submission.researcher_id,
            amount=submission.bounty,
            status=PaymentStatus.PROCESSING,
            payment_method="paypal",
            transaction_id=None,
            created_at=datetime.utcnow()
        )
        
        self._payments[payment.id] = payment
        
        # Update researcher total
        researcher = self._researchers.get(submission.researcher_id)
        if researcher:
            researcher.total_bounties += submission.bounty
        
        # Update submission status
        submission.status = SubmissionStatus.ACCEPTED
        submission.updated_at = datetime.utcnow()
        
        self.logger.info(f"Payment processed: {payment.id} for ${payment.amount}")
        
        return {
            "payment_id": payment.id,
            "submission_id": submission_id,
            "amount": payment.amount,
            "status": payment.status.value,
            "researcher_id": submission.researcher_id
        }
    
    def issue_advisory(self, submission_id: str, cve_id: Optional[str] = None,
                       remediation: Optional[str] = None,
                       publish: bool = False) -> Dict[str, Any]:
        """Issue security advisory."""
        submission = self._submissions.get(submission_id)
        if not submission:
            raise ValueError(f"Submission not found: {submission_id}")
        
        if not submission.severity:
            raise ValueError("Submission has not been triaged")
        
        program = self._programs.get(submission.program_id)
        if not program:
            raise ValueError(f"Program not found: {submission.program_id}")
        
        # Assign CVE if not provided
        if not cve_id:
            cve_id = f"CVE-2024-{str(uuid.uuid4().int)[:6]}"
        
        advisory = Advisory(
            id=str(uuid.uuid4()),
            submission_id=submission_id,
            cve_id=cve_id,
            title=f"{program.name} - {submission.title}",
            description=submission.description,
            affected_versions=[],
            remediation=remediation or "",
            severity=submission.severity,
            status="draft" if not publish else "published",
            published=publish,
            published_at=datetime.utcnow() if publish else None,
            created_at=datetime.utcnow()
        )
        
        self._advisories[advisory.id] = advisory
        
        # Update submission
        submission.cve_id = cve_id
        if publish:
            submission.status = SubmissionStatus.PUBLISHED
        submission.updated_at = datetime.utcnow()
        
        self.logger.info(f"Advisory created: {advisory.id}, CVE: {cve_id}")
        
        return {
            "id": advisory.id,
            "submission_id": submission_id,
            "cve_id": advisory.cve_id,
            "title": advisory.title,
            "published": advisory.published,
            "published_at": advisory.published_at.isoformat() if advisory.published_at else None
        }
    
    def register_researcher(self, username: str, email: str,
                           display_name: Optional[str] = None,
                           bio: Optional[str] = None,
                           skills: Optional[List[str]] = None) -> Dict[str, Any]:
        """Register security researcher."""
        # Check if username or email already exists
        for researcher in self._researchers.values():
            if researcher.username == username:
                raise ValueError(f"Username already exists: {username}")
            if researcher.email == email:
                raise ValueError(f"Email already exists: {email}")
        
        researcher = Researcher(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            display_name=display_name,
            bio=bio,
            skills=skills or [],
            reputation=0,
            total_bounties=0.0,
            submissions_count=0,
            created_at=datetime.utcnow()
        )
        
        self._researchers[researcher.id] = researcher
        
        self.logger.info(f"Researcher registered: {researcher.id}")
        
        return {
            "id": researcher.id,
            "username": researcher.username,
            "email": researcher.email,
            "display_name": researcher.display_name
        }
    
    def get_researcher_rankings(self, period: str = "all_time",
                                limit: int = 10) -> List[Dict[str, Any]]:
        """Get researcher rankings."""
        rankings = []
        
        for researcher in self._researchers.values():
            rankings.append({
                "id": researcher.id,
                "username": researcher.username,
                "display_name": researcher.display_name,
                "reputation": researcher.reputation,
                "total_bounties": researcher.total_bounties,
                "submissions_count": researcher.submissions_count
            })
        
        # Sort by total bounties
        rankings.sort(key=lambda r: r["total_bounties"], reverse=True)
        
        # Add ranks
        for idx, ranking in enumerate(rankings):
            ranking["rank"] = idx + 1
        
        return rankings[:limit]
    
    def get_program_stats(self, program_id: str) -> Dict[str, Any]:
        """Get program statistics."""
        program = self._programs.get(program_id)
        if not program:
            raise ValueError(f"Program not found: {program_id}")
        
        submissions = [s for s in self._submissions.values() if s.program_id == program_id]
        
        stats = {
            "program_id": program_id,
            "program_name": program.name,
            "status": program.status.value,
            "total_submissions": len(submissions),
            "by_status": {},
            "by_severity": {},
            "total_bounties": 0.0,
            "avg_bounty": 0.0
        }
        
        for submission in submissions:
            # Count by status
            status = submission.status.value
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            
            # Count by severity
            if submission.severity:
                severity = submission.severity.value
                stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1
            
            # Sum bounties
            if submission.bounty:
                stats["total_bounties"] += submission.bounty
        
        if submissions:
            stats["avg_bounty"] = round(
                stats["total_bounties"] / len(submissions), 2
            )
        
        return stats
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent": "BugBountyAgent",
            "programs": len(self._programs),
            "researchers": len(self._researchers),
            "submissions": len(self._submissions),
            "advisories": len(self._advisories),
            "payments": len(self._payments)
        }


def main():
    """Demo script."""
    print("Bug Bounty Agent Demo")
    print("=" * 50)
    
    agent = BugBountyAgent()
    
    # Create program
    program = agent.create_program(
        name="Demo Bug Bounty Program",
        description="Demo program for testing",
        reward_range="100-5000",
        scope=[
            {"target": "*.example.com", "type": "domain"},
            {"target": "api.example.com", "type": "api"}
        ]
    )
    print(f"\n1. Created program: {program['name']} ({program['id']})")
    
    # Activate program
    agent.activate_program(program["id"])
    print(f"2. Activated program")
    
    # Register researcher
    researcher = agent.register_researcher(
        username="demo_researcher",
        email="researcher@example.com",
        display_name="Demo Researcher",
        skills=["web-security", "sql-injection"]
    )
    print(f"3. Registered researcher: {researcher['username']}")
    
    # Submit vulnerability
    submission = agent.submit_vulnerability(
        program_id=program["id"],
        researcher_id=researcher["id"],
        title="SQL Injection in login form",
        description="The login form is vulnerable to SQL injection allowing authentication bypass.",
        severity="high",
        proof_of_concept={
            "steps": [
                "Navigate to /login",
                "Enter ' OR '1'='1 in username field",
                "Observe successful login"
            ],
            "payload": "' OR '1'='1 --",
            "screenshot": "login_sqli.png"
        },
        target_url="https://example.com/login",
        parameter="username",
        cvss_metrics={
            "attack_vector": "network",
            "attack_complexity": "low",
            "privileges_required": "none",
            "user_interaction": "none",
            "scope": "unchanged",
            "confidentiality": "high",
            "integrity": "high",
            "availability": "high"
        }
    )
    print(f"4. Submitted vulnerability: {submission['id']}")
    
    # Triage submission
    triaged = agent.triage_submission(
        submission["id"],
        validate=True,
        assess_severity=True,
        check_duplicates=True
    )
    print(f"5. Triage result: Valid={triaged['valid']}, Severity={triaged['severity']}")
    
    # Calculate bounty
    bounty = agent.calculate_bounty(submission["id"])
    print(f"6. Calculated bounty: ${bounty['final_bounty']}")
    
    # Issue advisory
    advisory = agent.issue_advisory(
        submission["id"],
        remediation="Use parameterized queries",
        publish=False
    )
    print(f"7. Advisory created: {advisory['cve_id']}")
    
    # Get status
    status = agent.get_status()
    print(f"\n8. Agent status: {status}")


if __name__ == "__main__":
    main()
