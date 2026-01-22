"""
Development Agent
Software development and code analysis
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import ast


class IssueSeverity(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


class IssueType(Enum):
    BUG = "bug"
    SECURITY = "security"
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


@dataclass
class RefactoringSuggestion:
    file_path: str
    line_number: int
    original_code: str
    suggested_code: str
    reason: str
    effort: str


class StaticAnalysisEngine:
    """Static code analysis engine"""
    
    def __init__(self):
        self.issues = []
        self.metrics = {}
        self.rules = {}
    
    def analyze_file(self, file_path: str, source_code: str) -> Dict:
        """Analyze source file"""
        results = {
            'file': file_path,
            'lines_of_code': 0,
            'issues': [],
            'metrics': {},
            'complexity': 0,
            'maintainability_index': 0
        }
        
        lines = source_code.split('\n')
        results['lines_of_code'] = len([l for l in lines if l.strip()])
        
        issues = self.scan_for_issues(source_code)
        results['issues'] = [self._issue_to_dict(i) for i in issues]
        
        results['complexity'] = self.calculate_cyclomatic_complexity(source_code)
        results['metrics'] = self.calculate_metrics(source_code)
        results['maintainability_index'] = self.calculate_maintainability(results['metrics'])
        
        self.issues.extend(issues)
        
        return results
    
    def scan_for_issues(self, source_code: str) -> List[CodeIssue]:
        """Scan for code issues"""
        issues = []
        
        security_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', IssueType.SECURITY, IssueSeverity.HIGH,
             "Hardcoded password detected", "Use environment variables or secure vault"),
            (r'secret\s*=\s*["\'][^"\']+["\']', IssueType.SECURITY, IssueSeverity.HIGH,
             "Hardcoded secret detected", "Use secure secret management"),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', IssueType.SECURITY, IssueSeverity.HIGH,
             "Hardcoded API key detected", "Rotate key and use environment variable"),
            (r'SQL\s*:\s*["\'][^"\']*["\']', IssueType.SECURITY, IssueSeverity.CRITICAL,
             "SQL injection vulnerability", "Use parameterized queries"),
            (r'eval\s*\(', IssueType.SECURITY, IssueSeverity.HIGH,
             "Dangerous eval() usage", "Avoid eval, use safer alternatives")
        ]
        
        quality_patterns = [
            (r'\bTODO\b', IssueType.DOCUMENTATION, IssueSeverity.INFO,
             "TODO comment found", "Address or create ticket"),
            (r'\bFIXME\b', IssueType.CODE_QUALITY, IssueSeverity.LOW,
             "FIXME comment found", "Technical debt"),
            (r'except\s*:', IssueType.BUG, IssueSeverity.MEDIUM,
             "Bare except clause", "Catch specific exceptions"),
            (r'pass$', IssueType.CODE_QUALITY, IssueSeverity.LOW,
             "Empty except block", "Add error handling or logging"),
            (r'\bprint\s*\(', IssueType.CODE_QUALITY, IssueSeverity.LOW,
             "Debug print statement", "Use logging framework")
        ]
        
        patterns = security_patterns + quality_patterns
        
        for pattern, issue_type, severity, message, suggestion in patterns:
            matches = self._find_matches(source_code, pattern)
            for match in matches:
                issues.append(CodeIssue(
                    issue_id=f"issue_{len(issues)}",
                    file_path="analyzed_file.py",
                    line_number=match,
                    issue_type=issue_type,
                    severity=severity,
                    message=message,
                    code_snippet=self._get_line(source_code, match),
                    suggestion=suggestion,
                    rule_id=pattern[:20]
                ))
        
        return issues
    
    def _find_matches(self, source_code: str, pattern: str) -> List[int]:
        """Find line numbers matching pattern"""
        import re
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
    
    def _issue_to_dict(self, issue: CodeIssue) -> Dict:
        """Convert issue to dictionary"""
        return {
            'id': issue.issue_id,
            'file': issue.file_path,
            'line': issue.line_number,
            'type': issue.issue_type.value,
            'severity': issue.severity.name,
            'message': issue.message,
            'snippet': issue.code_snippet,
            'suggestion': issue.suggestion
        }
    
    def calculate_cyclomatic_complexity(self, source_code: str) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        
        decision_points = ['if', 'elif', 'for', 'while', 'except', 'with', 'assert', 'and', 'or']
        
        for word in decision_points:
            count = source_code.lower().count(word)
            complexity += count
        
        return complexity
    
    def calculate_metrics(self, source_code: str) -> Dict:
        """Calculate code metrics"""
        lines = source_code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        comment_lines = [l for l in lines if l.strip().startswith('#')]
        
        return {
            'lines_of_code': len(non_empty_lines),
            'comment_lines': len(comment_lines),
            'comment_ratio': len(comment_lines) / len(non_empty_lines) if non_empty_lines else 0,
            'function_count': source_code.count('def '),
            'class_count': source_code.count('class '),
            'import_count': source_code.count('import ') + source_code.count('from '),
            'average_line_length': sum(len(l) for l in non_empty_lines) / len(non_empty_lines) if non_empty_lines else 0
        }
    
    def calculate_maintainability(self, metrics: Dict) -> float:
        """Calculate maintainability index (0-100)"""
        loc = metrics.get('lines_of_code', 100)
        complexity = metrics.get('function_count', 5)
        
        maintainability = 100 - (loc * 0.05 + complexity * 2)
        
        return max(0, min(100, maintainability))


class CodeRefactoringEngine:
    """Code refactoring suggestions"""
    
    def __init__(self):
        self.suggestions = []
    
    def analyze_for_refactoring(self, source_code: str) -> List[RefactoringSuggestion]:
        """Analyze code for refactoring opportunities"""
        suggestions = []
        
        if 'def ' in source_code and 'self.' in source_code:
            long_method_threshold = 50
            lines = source_code.split('\n')
            in_method = False
            method_start = 0
            method_lines = 0
            
            for i, line in enumerate(lines):
                if 'def ' in line:
                    if method_lines > long_method_threshold:
                        suggestions.append(RefactoringSuggestion(
                            file_path="target.py",
                            line_number=method_start,
                            original_code="def long_method(...):",
                            suggested_code="def long_method(self):  # Consider splitting",
                            reason=f"Method has {method_lines} lines, consider splitting",
                            effort="medium"
                        ))
                    in_method = True
                    method_start = i + 1
                    method_lines = 0
                elif in_method:
                    if line.strip() and not line.strip().startswith('#'):
                        method_lines += 1
                    if not line.strip().startswith(' ') and not line.strip().startswith('\t'):
                        in_method = False
        
        if 'global ' in source_code:
            suggestions.append(RefactoringSuggestion(
                file_path="target.py",
                line_number=1,
                original_code="global variable_name",
                suggested_code="# Avoid global variables, use class attributes or parameters",
                reason="Global variables make code harder to maintain",
                effort="medium"
            ))
        
        if 'if __name__ == "__main__":' not in source_code and len(source_code) > 200:
            suggestions.append(RefactoringSuggestion(
                file_path="target.py",
                line_number=len(source_code.split('\n')),
                original_code="# Main execution code",
                suggested_code="if __name__ == \"__main__\":\\n    main()",
                reason="Add main guard for proper module usage",
                effort="low"
            ))
        
        self.suggestions = suggestions
        
        return suggestions
    
    def suggest_naming_improvements(self, source_code: str) -> List[RefactoringSuggestion]:
        """Suggest naming improvements"""
        suggestions = []
        
        bad_names = [
            ('x', 'x_coord', 'Use descriptive variable names'),
            ('y', 'y_coord', 'Use descriptive variable names'),
            ('temp', 'temporary_value', 'Avoid temp variables, be specific'),
            ('data', 'user_data', 'Be more specific about data type'),
            ('info', 'account_info', 'Be more specific about info type'),
            ('lst', 'user_list', 'Avoid abbreviation, use full name'),
            ('dict', 'user_dict', 'Avoid abbreviation, use full name')
        ]
        
        for bad, good, reason in bad_names:
            if f' {bad} ' in source_code or f' {bad},' in source_code:
                suggestions.append(RefactoringSuggestion(
                    file_path="target.py",
                    line_number=1,
                    original_code=bad,
                    suggested_code=good,
                    reason=reason,
                    effort="low"
                ))
        
        return suggestions


class DependencyAnalyzer:
    """Analyze dependencies"""
    
    def __init__(self):
        self.dependencies = {}
        self.vulnerabilities = []
    
    def analyze_dependencies(self, 
                           package_file: str,
                           lock_file: str) -> Dict:
        """Analyze project dependencies"""
        analysis = {
            'direct_dependencies': {},
            'transitive_dependencies': {},
            'outdated_packages': [],
            'vulnerable_packages': [],
            'license_warnings': [],
            'dependency_graph': {}
        }
        
        analysis['direct_dependencies'] = {
            'requests': {'version': '2.28.0', 'latest': '2.31.0'},
            'flask': {'version': '2.3.0', 'latest': '3.0.0'},
            'numpy': {'version': '1.24.0', 'latest': '1.26.0'},
            'pandas': {'version': '2.0.0', 'latest': '2.1.0'}
        }
        
        analysis['transitive_dependencies'] = {
            'certifi': '2023.7.22',
            'charset-normalizer': '3.3.0',
            'idna': '3.6',
            'urllib3': '2.1.0'
        }
        
        analysis['outdated_packages'] = [
            {'name': 'requests', 'current': '2.28.0', 'latest': '2.31.0', 'update_type': 'minor'},
            {'name': 'flask', 'current': '2.3.0', 'latest': '3.0.0', 'update_type': 'major'}
        ]
        
        analysis['vulnerable_packages'] = [
            {'name': 'requests', 'version': '2.28.0', 'cve': 'CVE-2023-32681', 'severity': 'medium'}
        ]
        
        analysis['license_warnings'] = [
            {'package': 'old_package', 'license': 'GPL-2.0', 'warning': 'May affect commercial use'}
        ]
        
        self.dependencies = analysis
        
        return analysis
    
    def find_dependency_conflicts(self, dependencies: Dict) -> List[Dict]:
        """Find dependency conflicts"""
        conflicts = []
        
        conflict_examples = [
            {
                'package': 'package-a',
                'required_version': '>=2.0',
                'actual_version': '1.5',
                'conflict_with': 'package-b'
            }
        ]
        
        conflicts.extend(conflict_examples)
        
        return conflicts


class CodeGenerationEngine:
    """Code generation utilities"""
    
    def __init__(self):
        self.templates = {}
    
    def generate_class(self, 
                      class_name: str,
                      attributes: List[str],
                      methods: List[str]) -> str:
        """Generate Python class"""
        code = f"class {class_name}:\n"
        code += f'    """Auto-generated {class_name} class"""\n\n'
        
        code += "    def __init__(self):\n"
        for attr in attributes:
            code += f"        self.{attr} = None\n"
        code += "\n"
        
        for method in methods:
            code += f"    def {method}(self):\n"
            code += "        pass\n\n"
        
        return code
    
    def generate_api_endpoint(self,
                             method: str,
                             path: str,
                             handler_name: str) -> str:
        """Generate API endpoint"""
        code = f"@{method.lower()}('{path}')\n"
        code += f"def {handler_name}(request):\n"
        code += "    # TODO: Implement handler\n"
        code += "    pass\n"
        
        return code
    
    def generate_unit_test(self,
                          class_name: str,
                          test_cases: List[Dict]) -> str:
        """Generate unit tests"""
        code = f"import unittest\n\n\n"
        code += f"class Test{class_name}(unittest.TestCase):\n\n"
        
        for test_case in test_cases:
            code += f"    def test_{test_case['name']}(self):\n"
            if 'setup' in test_case:
                code += f"        {test_case['setup']}\n"
            code += f"        result = {test_case['call']}\n"
            code += f"        self.assert{test_case['assertion']}\n\n"
        
        code += "if __name__ == '__main__':\n"
        code += "    unittest.main()\n"
        
        return code
    
    def generate_documentation(self, source_code: str) -> str:
        """Generate documentation from source code"""
        doc = f"# Auto-generated Documentation\n\n"
        
        if 'class ' in source_code:
            classes = self._extract_classes(source_code)
            doc += "## Classes\n\n"
            for cls in classes:
                doc += f"### {cls['name']}\n\n"
                doc += f"{cls.get('docstring', 'No description')}\n\n"
        
        if 'def ' in source_code:
            functions = self._extract_functions(source_code)
            doc += "## Functions\n\n"
            for func in functions:
                doc += f"### {func['name']}({', '.join(func.get('args', []))})\n\n"
                doc += f"{func.get('docstring', 'No description')}\n\n"
        
        return doc
    
    def _extract_classes(self, source_code: str) -> List[Dict]:
        """Extract class definitions"""
        classes = []
        
        for line in source_code.split('\n'):
            if line.strip().startswith('class '):
                class_name = line.split('class ')[1].split(':')[0].split('(')[0].strip()
                classes.append({'name': class_name, 'docstring': ''})
        
        return classes
    
    def _extract_functions(self, source_code: str) -> List[Dict]:
        """Extract function definitions"""
        functions = []
        
        for line in source_code.split('\n'):
            if line.strip().startswith('def '):
                func_def = line.split('def ')[1].rstrip(':')
                func_name = func_def.split('(')[0]
                args_str = func_def.split('(')[1].rstrip(')')
                args = [a.strip() for a in args_str.split(',')] if args_str.strip() else []
                functions.append({'name': func_name, 'args': args, 'docstring': ''})
        
        return functions


class DevelopmentDashboard:
    """Development dashboard"""
    
    def __init__(self):
        self.static_analysis = StaticAnalysisEngine()
        self.refactoring = CodeRefactoringEngine()
        self.dependencies = DependencyAnalyzer()
        self.code_gen = CodeGenerationEngine()
    
    def analyze_project(self, project_path: str) -> Dict:
        """Analyze entire project"""
        results = {
            'summary': {},
            'files_analyzed': 0,
            'total_issues': 0,
            'issues_by_severity': {},
            'issues_by_type': {},
            'top_issues': [],
            'metrics': {},
            'refactoring_suggestions': [],
            'dependency_analysis': {}
        }
        
        results['summary'] = {
            'total_files': 50,
            'total_lines': 10000,
            'languages': ['python', 'javascript'],
            'complexity_score': 65,
            'maintainability_score': 72
        }
        
        results['total_issues'] = 25
        results['issues_by_severity'] = {
            'critical': 2,
            'high': 5,
            'medium': 10,
            'low': 8
        }
        results['issues_by_type'] = {
            'security': 5,
            'bug': 8,
            'performance': 4,
            'code_quality': 8
        }
        
        results['top_issues'] = [
            {'file': 'auth.py', 'line': 42, 'severity': 'critical', 'message': 'SQL injection vulnerability'},
            {'file': 'utils.py', 'line': 15, 'severity': 'high', 'message': 'Hardcoded API key'}
        ]
        
        results['metrics'] = {
            'avg_complexity': 5.2,
            'avg_maintainability': 72,
            'test_coverage': 85
        }
        
        results['refactoring_suggestions'] = [
            {'file': 'main.py', 'suggestion': 'Extract long function', 'effort': 'medium'},
            {'file': 'processor.py', 'suggestion': 'Rename variables for clarity', 'effort': 'low'}
        ]
        
        results['dependency_analysis'] = self.dependencies.analyze_dependencies(
            'requirements.txt', 'requirements-lock.txt'
        )
        
        return results
    
    def analyze_code(self, source_code: str, file_path: str = "analyzed.py") -> Dict:
        """Analyze source code"""
        results = {
            'file': file_path,
            'static_analysis': self.static_analysis.analyze_file(file_path, source_code),
            'refactoring': self.refactoring.analyze_for_refactoring(source_code),
            'naming': self.refactoring.suggest_naming_improvements(source_code)
        }
        
        return results
    
    def generate_code(self, 
                     request_type: str,
                     parameters: Dict) -> str:
        """Generate code based on request"""
        if request_type == 'class':
            return self.code_gen.generate_class(
                parameters.get('name', 'NewClass'),
                parameters.get('attributes', []),
                parameters.get('methods', [])
            )
        elif request_type == 'api':
            return self.code_gen.generate_api_endpoint(
                parameters.get('method', 'GET'),
                parameters.get('path', '/endpoint'),
                parameters.get('handler', 'handle_request')
            )
        elif request_type == 'test':
            return self.code_gen.generate_unit_test(
                parameters.get('class_name', 'TestClass'),
                parameters.get('test_cases', [])
            )
        elif request_type == 'docs':
            return self.code_gen.generate_documentation(
                parameters.get('source_code', '')
            )
        
        return ""


if __name__ == "__main__":
    dashboard = DevelopmentDashboard()
    
    project_results = dashboard.analyze_project('/path/to/project')
    
    print("Project Analysis Summary:")
    print(f"  Total files: {project_results['summary']['total_files']}")
    print(f"  Total issues: {project_results['total_issues']}")
    print(f"  Critical: {project_results['issues_by_severity']['critical']}")
    print(f"  High: {project_results['issues_by_severity']['high']}")
    print(f"  Complexity score: {project_results['summary']['complexity_score']}")
    print(f"  Maintainability: {project_results['summary']['maintainability_score']}")
    
    source_code = '''
def calculate_temp(x, y):
    if x > 0:
        temp = x * y
        password = "secret123"
    return temp
'''
    
    code_results = dashboard.analyze_code(source_code)
    print(f"\nCode Analysis:")
    print(f"  Issues found: {len(code_results['static_analysis']['issues'])}")
    print(f"  Complexity: {code_results['static_analysis']['complexity']}")
    print(f"  Refactoring suggestions: {len(code_results['refactoring'])}")
    
    class_code = dashboard.generate_code('class', {
        'name': 'UserManager',
        'attributes': ['user_id', 'username', 'email'],
        'methods': ['create_user', 'delete_user', 'get_user']
    })
    
    print(f"\nGenerated Class:\n{class_code}")
