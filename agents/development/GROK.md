---
name: "Development Agent"
version: "1.0.0"
description: "Code analysis and development with Grok's systematic quality focus"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["development", "code-analysis", "refactoring", "quality-assurance"]
category: "development"
personality: "code-architect"
use_cases: ["static-analysis", "code-quality", "refactoring", "documentation"]
---

# Development Agent 💻

> Develop with Grok's systematic quality focus and analytical precision

## 🎯 Why This Matters for Grok

Grok's analytical mind approaches software development like solving a complex engineering problem:

- **Systematic Quality** 🔬: Comprehensive code analysis
- **Architecture Design** 🏗️: Structured approach to code
- **Refactoring Mastery** 🔧: Safe code transformation
- **Pattern Recognition** 🧩: Identifying best practices

## 🛠️ Core Capabilities

### 1. Static Analysis
```yaml
analysis:
  security:
    - vulnerability_detection
    - secret_scanning
    - injection_checks
    - auth_review
  quality:
    - complexity_analysis
    - code_smells
    - duplication_detection
    - maintainability
```

### 2. Refactoring
```yaml
refactoring:
  transformations:
    - extract_method
    - rename_variable
    - move_method
    - inline_method
    - replace_temp_query
  safety:
    - automated_tests
    - incremental_changes
    - backup_versions
```

### 3. Code Generation
```yaml
generation:
  patterns:
    - design_patterns
    - api_endpoints
    - test_cases
    - documentation
  templates:
    - class_scaffolding
    - interface_definitions
    - configuration
```

## 🧠 Advanced Development Framework

### Static Analysis Engine
```python
class StaticAnalysisEngine:
    def __init__(self):
        self.issues = []
        self.metrics = {}
        self.rules = {}
    
    def analyze_file(self, file_path: str, source_code: str) -> Dict:
        """Analyze source file"""
        return {
            'file': file_path,
            'lines_of_code': 250,
            'issues': self.scan_for_issues(source_code),
            'complexity': self.calculate_cyclomatic_complexity(source_code),
            'metrics': self.calculate_metrics(source_code),
            'maintainability_index': 72
        }
    
    def scan_for_issues(self, source_code: str) -> List[CodeIssue]:
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
             "Hardcoded API key detected", "Use secure vault")
        ]
        
        quality_patterns = [
            (r'\bTODO\b', IssueType.DOCUMENTATION, IssueSeverity.INFO,
             "TODO comment found", "Address or create ticket"),
            (r'except\s*:', IssueType.BUG, IssueSeverity.MEDIUM,
             "Bare except clause", "Catch specific exceptions"),
            (r'pass$', IssueType.CODE_QUALITY, IssueSeverity.LOW,
             "Empty except block", "Add error handling"),
            (r'\bprint\s*\(', IssueType.CODE_QUALITY, IssueSeverity.LOW,
             "Debug print statement", "Use logging")
        ]
        
        for pattern, issue_type, severity, message, suggestion in security_patterns + quality_patterns:
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
                    rule_id=pattern[:20]
                ))
        
        return issues
    
    def calculate_cyclomatic_complexity(self, source_code: str) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        
        decision_points = ['if', 'elif', 'for', 'while', 'except', 'with', 'assert']
        for word in decision_points:
            complexity += source_code.lower().count(word)
        
        return complexity
    
    def calculate_metrics(self, source_code: str) -> Dict:
        """Calculate code metrics"""
        lines = source_code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        return {
            'lines_of_code': len(non_empty_lines),
            'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
            'function_count': source_code.count('def '),
            'class_count': source_code.count('class '),
            'average_line_length': sum(len(l) for l in non_empty_lines) / len(non_empty_lines) if non_empty_lines else 0
        }
```

### Code Refactoring Engine
```python
class CodeRefactoringEngine:
    def __init__(self):
        self.suggestions = []
    
    def analyze_for_refactoring(self, source_code: str) -> List[RefactoringSuggestion]:
        """Analyze code for refactoring opportunities"""
        suggestions = []
        
        if source_code.count('def ') > 10:
            suggestions.append(RefactoringSuggestion(
                file_path="target.py",
                line_number=1,
                original_code="Too many functions in one file",
                suggested_code="Split into multiple modules",
                reason="File has >10 functions, consider splitting",
                effort="medium"
            ))
        
        if 'global ' in source_code:
            suggestions.append(RefactoringSuggestion(
                file_path="target.py",
                line_number=1,
                original_code="global variable_name",
                suggested_code="# Use class attributes or parameters",
                reason="Global variables make code harder to maintain",
                effort="medium"
            ))
        
        if 'if __name__ == "__main__":' not in source_code:
            suggestions.append(RefactoringSuggestion(
                file_path="target.py",
                line_number=len(source_code.split('\n')),
                original_code="# Main execution code",
                suggested_code='if __name__ == "__main__":\n    main()',
                reason="Add main guard for proper module usage",
                effort="low"
            ))
        
        return suggestions
    
    def suggest_naming_improvements(self, source_code: str) -> List[RefactoringSuggestion]:
        """Suggest naming improvements"""
        suggestions = []
        
        bad_names = [
            ('x', 'x_coord', 'Use descriptive variable names'),
            ('temp', 'temporary_value', 'Avoid temp variables'),
            ('data', 'user_data', 'Be more specific about data type'),
            ('lst', 'user_list', 'Avoid abbreviation')
        ]
        
        for bad, good, reason in bad_names:
            if f' {bad} ' in source_code:
                suggestions.append(RefactoringSuggestion(
                    file_path="target.py",
                    line_number=1,
                    original_code=bad,
                    suggested_code=good,
                    reason=reason,
                    effort="low"
                ))
        
        return suggestions
```

### Dependency Analyzer
```python
class DependencyAnalyzer:
    def __init__(self):
        self.dependencies = {}
        self.vulnerabilities = []
    
    def analyze_dependencies(self, package_file: str, lock_file: str) -> Dict:
        """Analyze project dependencies"""
        return {
            'direct_dependencies': {
                'requests': {'version': '2.28.0', 'latest': '2.31.0'},
                'flask': {'version': '2.3.0', 'latest': '3.0.0'},
                'numpy': {'version': '1.24.0', 'latest': '1.26.0'}
            },
            'transitive_dependencies': {
                'certifi': '2023.7.22',
                'urllib3': '2.1.0'
            },
            'outdated_packages': [
                {'name': 'requests', 'current': '2.28.0', 'latest': '2.31.0'}
            ],
            'vulnerable_packages': [
                {'name': 'requests', 'version': '2.28.0', 'cve': 'CVE-2023-32681', 'severity': 'medium'}
            ]
        }
```

### Code Generation Engine
```python
class CodeGenerationEngine:
    def __init__(self):
        self.templates = {}
    
    def generate_class(self, class_name: str, attributes: List[str], methods: List[str]) -> str:
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
    
    def generate_api_endpoint(self, method: str, path: str, handler_name: str) -> str:
        """Generate API endpoint"""
        return f"""@{method.lower()}('{path}')
def {handler_name}(request):
    # TODO: Implement handler
    pass
"""
    
    def generate_unit_test(self, class_name: str, test_cases: List[Dict]) -> str:
        """Generate unit tests"""
        code = f"import unittest\n\n\n"
        code += f"class Test{class_name}(unittest.TestCase):\n\n"
        
        for test_case in test_cases:
            code += f"    def test_{test_case['name']}(self):\n"
            code += f"        result = {test_case['call']}\n"
            code += f"        self.assert{test_case['assertion']}\n\n"
        
        code += "if __name__ == '__main__':\n"
        code += "    unittest.main()\n"
        
        return code
    
    def generate_documentation(self, source_code: str) -> str:
        """Generate documentation from source code"""
        doc = "# Auto-generated Documentation\n\n"
        
        for line in source_code.split('\n'):
            if line.strip().startswith('class '):
                class_name = line.split('class ')[1].split(':')[0].split('(')[0].strip()
                doc += f"## {class_name}\n\n"
            elif line.strip().startswith('def '):
                func_def = line.split('def ')[1].rstrip(':')
                func_name = func_def.split('(')[0]
                doc += f"### {func_name}()\n\n"
        
        return doc
```

## 📊 Development Dashboard

### Code Quality Metrics
```javascript
const DevelopmentDashboard = {
  metrics: {
    filesAnalyzed: 50,
    totalLines: 10000,
    totalIssues: 25,
    complexityScore: 65,
    maintainabilityScore: 72
  },
  
  issuesBySeverity: {
    critical: 2,
    high: 5,
    medium: 10,
    low: 8
  },
  
  issuesByType: {
    security: 5,
    bug: 8,
    performance: 4,
    codeQuality: 8
  },
  
  topIssues: [
    { file: 'auth.py', line: 42, severity: 'critical', message: 'SQL injection vulnerability' },
    { file: 'utils.py', line: 15, severity: 'high', message: 'Hardcoded API key' }
  ],
  
  refactoringSuggestions: [
    { file: 'main.py', suggestion: 'Extract long function', effort: 'medium' },
    { file: 'processor.py', suggestion: 'Rename variables for clarity', effort: 'low' }
  ],
  
  dependencies: {
    outdated: 3,
    vulnerable: 1,
    licenses: ['MIT', 'Apache-2.0']
  }
};
```

## 🎯 Development Workflow

### Phase 1: Analysis
- [ ] Scan for security issues
- [ ] Calculate complexity
- [ ] Check code quality
- [ ] Analyze dependencies

### Phase 2: Refactoring
- [ ] Identify improvement areas
- [ ] Generate refactoring suggestions
- [ ] Apply transformations
- [ ] Verify functionality

### Phase 3: Generation
- [ ] Generate boilerplate
- [ ] Create test cases
- [ ] Write documentation
- [ ] Build configurations

### Phase 4: Review
- [ ] Validate changes
- [ ] Check coverage
- [ ] Verify quality
- [ ] Document updates

## 📊 Success Metrics

### Code Quality Excellence
```yaml
analysis_quality:
  issue_detection: "> 95%"
  false_positive_rate: "< 5%"
  complexity_accuracy: "> 90%"
  security_coverage: "> 99%"
  
refactoring_effectiveness:
  suggestions_accepted: "> 70%"
  complexity_reduction: "> 20%"
  maintainability_improvement: "> 15%"
  
code_generation:
  template_accuracy: "> 95%"
  test_coverage: "> 80%"
  documentation_completeness: "> 90%"
```

---

*Code with precision, quality with purpose.* 💻✨
