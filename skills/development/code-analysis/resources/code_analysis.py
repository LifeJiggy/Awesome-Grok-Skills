"""
Code Analysis Module
Static code analysis and quality assurance
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json
import re


class IssueSeverity(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


class IssueType(Enum):
    SECURITY = "security"
    BUG = "bug"
    PERFORMANCE = "performance"
    CODE_QUALITY = "code_quality"
    STYLE = "style"
    DOCUMENTATION = "documentation"


@dataclass
class CodeIssue:
    issue_id: str
    file_path: str
    line_number: int
    issue_type: IssueType
    severity: IssueSeverity
    message: str
    code_snippet: str
    suggestion: str
    rule_id: str


class CodeAnalyzer:
    """Static code analysis engine"""
    
    def __init__(self):
        self.issues = []
        self.metrics = {}
        self.rules = {}
    
    def analyze(self, file_path: str, source_code: str) -> Dict:
        """Analyze source code"""
        results = {
            'file': file_path,
            'lines_of_code': 0,
            'issues': [],
            'complexity': 0,
            'metrics': {},
            'maintainability_index': 0
        }
        
        lines = source_code.split('\n')
        results['lines_of_code'] = len([l for l in lines if l.strip()])
        
        results['issues'] = self._scan_for_issues(source_code, file_path)
        results['complexity'] = self._calculate_complexity(source_code)
        results['metrics'] = self._calculate_metrics(source_code)
        results['maintainability_index'] = self._calculate_maintainability(results['metrics'])
        
        self.issues.extend(results['issues'])
        
        return results
    
    def _scan_for_issues(self, source_code: str, file_path: str) -> List[CodeIssue]:
        """Scan for code issues"""
        issues = []
        
        security_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', IssueType.SECURITY, IssueSeverity.HIGH,
             "Hardcoded password detected", "Use environment variables"),
            (r'SQL\s*:\s*["\'][^"\']*["\']', IssueType.SECURITY, IssueSeverity.CRITICAL,
             "SQL injection vulnerability", "Use parameterized queries"),
            (r'eval\s*\(', IssueType.SECURITY, IssueSeverity.HIGH,
             "Dangerous eval() usage", "Avoid eval"),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', IssueType.SECURITY, IssueSeverity.HIGH,
             "Hardcoded API key detected", "Use secure vault"),
            (r'secret\s*=\s*["\'][^"\']+["\']', IssueType.SECURITY, IssueSeverity.HIGH,
             "Hardcoded secret detected", "Use secure vault"),
            (r'token\s*=\s*["\'][^"\']+["\']', IssueType.SECURITY, IssueSeverity.HIGH,
             "Hardcoded token detected", "Use secure vault")
        ]
        
        bug_patterns = [
            (r'except\s*:', IssueType.BUG, IssueSeverity.MEDIUM,
             "Bare except clause", "Catch specific exceptions"),
            (r'pass$', IssueType.BUG, IssueSeverity.LOW,
             "Empty except block", "Add error handling"),
            (r'while\s+True:', IssueType.BUG, IssueSeverity.MEDIUM,
             "Infinite while loop detected", "Add exit condition"),
            (r'if\s+.*==\s+True:', IssueType.BUG, IssueSeverity.LOW,
             "Redundant True comparison", "Use 'if' directly")
        ]
        
        quality_patterns = [
            (r'\bTODO\b', IssueType.DOCUMENTATION, IssueSeverity.INFO,
             "TODO comment found", "Address or create ticket"),
            (r'\bFIXME\b', IssueType.CODE_QUALITY, IssueSeverity.LOW,
             "FIXME comment found", "Technical debt"),
            (r'\bprint\s*\(', IssueType.CODE_QUALITY, IssueSeverity.LOW,
             "Debug print statement", "Use logging framework"),
            (r'\bglobal\s+\w+', IssueType.CODE_QUALITY, IssueSeverity.MEDIUM,
             "Global variable used", "Consider passing as parameter")
        ]
        
        patterns = security_patterns + bug_patterns + quality_patterns
        
        for pattern, issue_type, severity, message, suggestion in patterns:
            matches = self._find_matches(source_code, pattern)
            for match in matches:
                issues.append(CodeIssue(
                    issue_id=f"issue_{len(issues)}",
                    file_path=file_path,
                    line_number=match,
                    issue_type=issue_type,
                    severity=severity,
                    message=message,
                    code_snippet=self._get_line(source_code, match),
                    suggestion=suggestion,
                    rule_id=pattern[:30]
                ))
        
        return issues
    
    def _find_matches(self, source_code: str, pattern: str) -> List[int]:
        """Find line numbers matching pattern"""
        lines = source_code.split('\n')
        matches = []
        
        for i, line in enumerate(lines):
            if re.search(pattern, line, re.IGNORECASE):
                matches.append(i + 1)
        
        return matches
    
    def _get_line(self, source_code: str, line_number: int) -> str:
        """Get line content"""
        lines = source_code.split('\n')
        if 1 <= line_number <= len(lines):
            return lines[line_number - 1]
        return ""
    
    def _calculate_complexity(self, source_code: str) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        
        decision_points = ['if ', 'elif ', 'for ', 'while ', 'except ', 'with ', 'and ', 'or ']
        for word in decision_points:
            complexity += source_code.lower().count(word)
        
        return complexity
    
    def _calculate_metrics(self, source_code: str) -> Dict:
        """Calculate code metrics"""
        lines = source_code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        comment_lines = [l for l in lines if l.strip().startswith('#')]
        
        function_count = len(re.findall(r'def\s+\w+', source_code))
        class_count = len(re.findall(r'class\s+\w+', source_code))
        
        import_count = source_code.count('import ') + source_code.count('from ')
        
        avg_line_length = sum(len(l) for l in non_empty_lines) / len(non_empty_lines) if non_empty_lines else 0
        
        return {
            'lines_of_code': len(non_empty_lines),
            'comment_lines': len(comment_lines),
            'comment_ratio': len(comment_lines) / len(non_empty_lines) if non_empty_lines else 0,
            'function_count': function_count,
            'class_count': class_count,
            'import_count': import_count,
            'average_line_length': avg_line_length,
            'max_line_length': max(len(l) for l in non_empty_lines) if non_empty_lines else 0
        }
    
    def _calculate_maintainability(self, metrics: Dict) -> float:
        """Calculate maintainability index (0-100)"""
        loc = metrics.get('lines_of_code', 100)
        complexity = metrics.get('function_count', 5)
        comments = metrics.get('comment_ratio', 0)
        
        base_score = 100
        base_score -= loc * 0.03
        base_score -= complexity * 3
        base_score += comments * 20
        
        return max(0, min(100, base_score))
    
    def get_metrics(self, analysis_results: Dict) -> Dict:
        """Get quality metrics from analysis"""
        return {
            'maintainability_index': analysis_results['maintainability_index'],
            'cyclomatic_complexity': analysis_results['complexity'],
            'lines_of_code': analysis_results['lines_of_code'],
            'issues_by_severity': self._group_issues_by_severity(analysis_results['issues']),
            'issues_by_type': self._group_issues_by_type(analysis_results['issues'])
        }
    
    def _group_issues_by_severity(self, issues: List[CodeIssue]) -> Dict:
        """Group issues by severity"""
        groups = {s.name: 0 for s in IssueSeverity}
        for issue in issues:
            groups[issue.severity.name] += 1
        return groups
    
    def _group_issues_by_type(self, issues: List[CodeIssue]) -> Dict:
        """Group issues by type"""
        groups = {t.value: 0 for t in IssueType}
        for issue in issues:
            groups[issue.issue_type.value] += 1
        return groups
    
    def suggest_refactoring(self, analysis_results: Dict) -> List[Dict]:
        """Suggest refactoring improvements"""
        suggestions = []
        
        complexity = analysis_results['complexity']
        loc = analysis_results['lines_of_code']
        
        if complexity > 20:
            suggestions.append({
                'type': 'complexity',
                'description': f"High cyclomatic complexity: {complexity}",
                'suggestion': "Consider breaking into smaller functions",
                'impact': 'high'
            })
        
        if loc > 300:
            suggestions.append({
                'type': 'size',
                'description': f"Large file: {loc} lines",
                'suggestion': "Consider splitting into multiple modules",
                'impact': 'medium'
            })
        
        metrics = analysis_results['metrics']
        if metrics.get('average_line_length', 0) > 100:
            suggestions.append({
                'type': 'readability',
                'description': "Long lines detected",
                'suggestion': "Break lines at 80-100 characters",
                'impact': 'low'
            })
        
        return suggestions


class CodeQualityDashboard:
    """Code quality dashboard"""
    
    def __init__(self):
        self.analyzer = CodeAnalyzer()
    
    def analyze_project(self, files: Dict[str, str]) -> Dict:
        """Analyze multiple files"""
        results = {
            'files_analyzed': len(files),
            'total_issues': 0,
            'issues_by_severity': {},
            'issues_by_type': {},
            'metrics_summary': {},
            'quality_score': 0
        }
        
        all_issues = []
        total_complexity = 0
        total_loc = 0
        
        for file_path, source_code in files.items():
            analysis = self.analyzer.analyze(file_path, source_code)
            all_issues.extend(analysis['issues'])
            total_complexity += analysis['complexity']
            total_loc += analysis['lines_of_code']
        
        results['total_issues'] = len(all_issues)
        results['issues_by_severity'] = self.analyzer._group_issues_by_severity(all_issues)
        results['issues_by_type'] = self.analyzer._group_issues_by_type(all_issues)
        results['metrics_summary'] = {
            'total_lines': total_loc,
            'average_complexity': total_complexity / len(files) if files else 0
        }
        
        critical_count = results['issues_by_severity'].get('CRITICAL', 0)
        high_count = results['issues_by_severity'].get('HIGH', 0)
        results['quality_score'] = max(0, 100 - critical_count * 10 - high_count * 5 - results['total_issues'])
        
        return results


if __name__ == "__main__":
    dashboard = CodeQualityAnalyzer()
    
    sample_code = '''
def example_function(x, y):
    password = "secret123"  # Hardcoded password
    if x > 0:
        result = x + y
        if y == True:  # Redundant comparison
            print("y is True")
    try:
        eval("x + 1")  # Dangerous eval
    except:  # Bare except
        pass
    return result
'''
    
    analyzer = CodeAnalyzer()
    results = analyzer.analyze("example.py", sample_code)
    
    print(f"Lines of code: {results['lines_of_code']}")
    print(f"Complexity: {results['complexity']}")
    print(f"Issues found: {len(results['issues'])}")
    print(f"Maintainability: {results['maintainability_index']}")
    
    for issue in results['issues']:
        print(f"  [{issue.severity.name}] {issue.message} (line {issue.line_number})")
    
    suggestions = analyzer.suggest_refactoring(results)
    for suggestion in suggestions:
        print(f"  Suggestion: {suggestion['description']}")
    
    metrics = analyzer.get_metrics(results)
    print(f"Quality metrics: {metrics}")
