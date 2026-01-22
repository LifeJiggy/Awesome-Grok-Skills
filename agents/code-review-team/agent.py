"""
Code Review Team Agent
Automated code review and quality assurance
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class Severity(Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


@dataclass
class CodeIssue:
    line_number: int
    column: int
    message: str
    severity: Severity
    rule_id: str
    file_path: str
    suggestion: str = ""


@dataclass
class ReviewResult:
    file_path: str
    issues: List[CodeIssue]
    score: float
    summary: str


class LinterIntegrator:
    """Code linting integration"""
    
    def __init__(self):
        self.linters = {}
        self.rules = {}
    
    def add_linter(self, name: str, language: str, config: Dict):
        """Add linter configuration"""
        self.linters[name] = {
            "language": language,
            "config": config
        }
    
    def run_linter(self, linter_name: str, code: str) -> List[CodeIssue]:
        """Run linter on code"""
        issues = []
        
        if linter_name == "pylint":
            issues = self._run_pylint(code)
        elif linter_name == "eslint":
            issues = self._run_eslint(code)
        elif linter_name == "ruff":
            issues = self._run_ruff(code)
        
        return issues
    
    def _run_pylint(self, code: str) -> List[CodeIssue]:
        """Run pylint (simulated)"""
        issues = []
        
        if "print(" in code:
            issues.append(CodeIssue(
                line_number=1,
                column=0,
                message="Consider using logging instead of print",
                severity=Severity.WARNING,
                rule_id="W1201",
                file_path="main.py",
                suggestion="Use logger.info() instead"
            ))
        
        return issues
    
    def _run_eslint(self, code: str) -> List[CodeIssue]:
        """Run ESLint (simulated)"""
        return []
    
    def _run_ruff(self, code: str) -> List[CodeIssue]:
        """Run Ruff linter (simulated)"""
        return []


class SecurityScanner:
    """Security vulnerability scanning"""
    
    def __init__(self):
        self.vulnerability_patterns = {
            "sql_injection": r"(execute|query)\s*\(\s*f[\"'].*\{.*\}.*[\"']",
            "hardcoded_secret": r"(api_key|password|secret)\s*=\s*[\"'][^\"']+[\"']",
            "xss": r"(innerHTML|dangerouslySetInnerHTML)",
            "path_traversal": r"(open|read|write)\s*\(\s*f\.\.|[^\"']+\.\./",
            "weak_crypto": r"(md5|sha1)\s*\("
        }
    
    def scan(self, code: str, file_path: str) -> List[CodeIssue]:
        """Scan code for vulnerabilities"""
        import re
        issues = []
        
        for vuln_name, pattern in self.vulnerability_patterns.items():
            matches = re.finditer(pattern, code)
            for match in matches:
                line = code[:match.start()].count('\n') + 1
                issues.append(CodeIssue(
                    line_number=line,
                    column=match.start(),
                    message=f"Potential {vuln_name.replace('_', ' ')} vulnerability",
                    severity=Severity.CRITICAL if "injection" in vuln_name else Severity.ERROR,
                    rule_id=f"SEC-{vuln_name.upper()}",
                    file_path=file_path,
                    suggestion=f"Review and fix potential {vuln_name}"
                ))
        
        return issues


class CodeComplexityAnalyzer:
    """Code complexity analysis"""
    
    def __init__(self):
        self.thresholds = {
            "cyclomatic": {"warning": 10, "error": 20},
            "cognitive": {"warning": 15, "error": 30},
            "lines_of_code": {"warning": 200, "error": 500}
        }
    
    def analyze_complexity(self, code: str) -> Dict:
        """Analyze code complexity"""
        lines = code.split('\n')
        
        cyclomatic = self._calculate_cyclomatic_complexity(code)
        cognitive = self._calculate_cognitive_complexity(code)
        loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        
        return {
            "cyclomatic_complexity": cyclomatic,
            "cognitive_complexity": cognitive,
            "lines_of_code": loc,
            "issues": self._check_thresholds({
                "cyclomatic": cyclomatic,
                "cognitive": cognitive,
                "lines_of_code": loc
            })
        }
    
    def _calculate_cyclomatic_complexity(self, code: str) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        keywords = ['if ', 'elif ', 'else:', 'for ', 'while ', 'except:', 'and ', 'or ']
        for keyword in keywords:
            complexity += code.count(keyword)
        return complexity
    
    def _calculate_cognitive_complexity(self, code: str) -> int:
        """Calculate cognitive complexity (simplified)"""
        complexity = 0
        nesting = 0
        
        for line in code.split('\n'):
            stripped = line.strip()
            if stripped.startswith(('if ', 'for ', 'while ', 'def ', 'class ')):
                nesting += 1
            complexity += nesting
        
        return complexity
    
    def _check_thresholds(self, metrics: Dict) -> List[str]:
        """Check metrics against thresholds"""
        issues = []
        for metric, value in metrics.items():
            if metric in self.thresholds:
                if value >= self.thresholds[metric]["error"]:
                    issues.append(f"High {metric}: {value}")
        return issues


class CodeReviewer:
    """Main code review agent"""
    
    def __init__(self):
        self.linter = LinterIntegrator()
        self.security = SecurityScanner()
        self.complexity = CodeComplexityAnalyzer()
    
    def review_code(self, 
                   code: str,
                   file_path: str,
                   language: str = "python") -> ReviewResult:
        """Perform comprehensive code review"""
        all_issues = []
        
        linter_issues = self.linter.run_linter("pylint", code)
        all_issues.extend(linter_issues)
        
        security_issues = self.security.scan(code, file_path)
        all_issues.extend(security_issues)
        
        complexity = self.complexity.analyze_complexity(code)
        
        for issue in complexity.get("issues", []):
            all_issues.append(CodeIssue(
                line_number=0,
                column=0,
                message=issue,
                severity=Severity.WARNING,
                rule_id="COMPLEXITY",
                file_path=file_path
            ))
        
        score = self._calculate_score(all_issues)
        summary = self._generate_summary(all_issues)
        
        return ReviewResult(
            file_path=file_path,
            issues=all_issues,
            score=score,
            summary=summary
        )
    
    def _calculate_score(self, issues: List[CodeIssue]) -> float:
        """Calculate code quality score"""
        base_score = 100
        
        for issue in issues:
            if issue.severity == Severity.CRITICAL:
                base_score -= 20
            elif issue.severity == Severity.ERROR:
                base_score -= 10
            elif issue.severity == Severity.WARNING:
                base_score -= 5
            elif issue.severity == Severity.INFO:
                base_score -= 1
        
        return max(0, base_score)
    
    def _generate_summary(self, issues: List[CodeIssue]) -> str:
        """Generate review summary"""
        by_severity = {}
        for issue in issues:
            severity = issue.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        summary = f"Found {len(issues)} issues: "
        parts = [f"{count} {sev}" for sev, count in sorted(by_severity.items())]
        summary += ", ".join(parts)
        
        return summary


class ReviewReporter:
    """Generate review reports"""
    
    def __init__(self):
        self.templates = {}
    
    def generate_report(self, 
                       results: List[ReviewResult],
                       format: str = "markdown") -> str:
        """Generate review report"""
        if format == "markdown":
            return self._generate_markdown(results)
        elif format == "json":
            return self._generate_json(results)
        else:
            return self._generate_text(results)
    
    def _generate_markdown(self, results: List[ReviewResult]) -> str:
        """Generate markdown report"""
        lines = ["# Code Review Report", f"Generated: {datetime.now()}", ""]
        
        total_score = sum(r.score for r in results) / len(results) if results else 0
        
        lines.append(f"## Summary")
        lines.append(f"- **Total Files Reviewed**: {len(results)}")
        lines.append(f"- **Average Score**: {total_score:.1f}/100")
        lines.append(f"- **Total Issues**: {sum(len(r.issues) for r in results)}")
        lines.append("")
        
        for result in results:
            lines.append(f"## {result.file_path}")
            lines.append(f"**Score**: {result.score}/100")
            lines.append(f"**Issues**: {len(result.issues)}")
            lines.append("")
            
            for issue in result.issues:
                lines.append(f"- `{issue.severity.value}` {issue.message} (L{issue.line_number})")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_json(self, results: List[ReviewResult]) -> str:
        """Generate JSON report"""
        import json
        return json.dumps({
            "timestamp": datetime.now().isoformat(),
            "total_files": len(results),
            "average_score": sum(r.score for r in results) / len(results) if results else 0,
            "results": [
                {
                    "file": r.file_path,
                    "score": r.score,
                    "issues": [
                        {
                            "line": i.line_number,
                            "severity": i.severity.value,
                            "message": i.message,
                            "rule": i.rule_id
                        }
                        for i in r.issues
                    ]
                }
                for r in results
            ]
        }, indent=2)
    
    def _generate_text(self, results: List[ReviewResult]) -> str:
        """Generate plain text report"""
        lines = []
        for result in results:
            lines.append(f"{result.file_path}: {result.score}/100 ({len(result.issues)} issues)")
        return "\n".join(lines)


if __name__ == "__main__":
    reviewer = CodeReviewer()
    reporter = ReviewReporter()
    
    code = """
def example_function():
    print("Hello World")
    password = "secret123"
    query = f"SELECT * FROM users WHERE id = {user_id}"
    if True and False or True:
        for i in range(10):
            pass
"""
    
    result = reviewer.review_code(code, "example.py")
    report = reporter.generate_report([result])
    
    print(f"Score: {result.score}")
    print(f"Issues: {len(result.issues)}")
    print(f"\nReport:\n{report}")
