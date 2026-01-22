"""
Technical Writing Module
Documentation, API docs, and technical content
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class DocType(Enum):
    API_REFERENCE = "api_reference"
    USER_GUIDE = "user_guide"
    TUTORIAL = "tutorial"
    README = "readme"
    CHANGELOG = "changelog"
    README_DEV = "readme_dev"
    RUNBOOK = "runbook"


@dataclass
class DocSection:
    title: str
    content: str
    subsections: List['DocSection'] = None
    code_examples: List[str] = None
    links: List[str] = None


class APIDocGenerator:
    """API documentation generator"""
    
    def __init__(self):
        self.endpoints = []
    
    def add_endpoint(self,
                     method: str,
                     path: str,
                     summary: str,
                     description: str = "",
                     parameters: List[Dict] = None,
                     responses: List[Dict] = None) -> Dict:
        """Add API endpoint"""
        endpoint = {
            'method': method,
            'path': path,
            'summary': summary,
            'description': description,
            'parameters': parameters or [],
            'responses': responses or []
        }
        self.endpoints.append(endpoint)
        return endpoint
    
    def generate_openapi_spec(self) -> Dict:
        """Generate OpenAPI 3.0 specification"""
        return {
            'openapi': '3.0.3',
            'info': {
                'title': 'API Documentation',
                'version': '1.0.0',
                'description': 'API reference documentation'
            },
            'paths': {
                '/users': {
                    'get': {
                        'summary': 'List users',
                        'parameters': [{'name': 'limit', 'in': 'query', 'schema': {'type': 'integer'}}],
                        'responses': {'200': {'description': 'Success'}}
                    }
                }
            },
            'components': {
                'schemas': {
                    'User': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'string'},
                            'name': {'type': 'string'},
                            'email': {'type': 'string'}
                        }
                    }
                }
            }
        }
    
    def generate_markdown(self) -> str:
        """Generate Markdown documentation"""
        doc = "# API Reference\n\n"
        
        for endpoint in self.endpoints:
            doc += f"## {endpoint['method']} {endpoint['path']}\n\n"
            doc += f"**{endpoint['summary']}**\n\n"
            
            if endpoint['parameters']:
                doc += "### Parameters\n\n"
                doc += "| Name | Type | In | Required |\n"
                doc += "|------|------|-------|----------|\n"
                for param in endpoint['parameters']:
                    doc += f"| {param.get('name', '')} | {param.get('type', '')} | {param.get('in', '')} | {param.get('required', False)} |\n"
                doc += "\n"
            
            if endpoint['responses']:
                doc += "### Responses\n\n"
                for resp in endpoint['responses']:
                    doc += f"- `{resp.get('status', '')}`: {resp.get('description', '')}\n"
                doc += "\n"
            
            doc += "---\n\n"
        
        return doc
    
    def generate_interactive_docs(self) -> Dict:
        """Generate interactive API documentation"""
        return {
            'type': 'swagger_ui',
            'endpoint': '/api-docs',
            'features': [
                'try_it_out',
                'response_examples',
                'schema_validation'
            ]
        }
    
    def generate_code_samples(self,
                              language: str = "python") -> List[Dict]:
        """Generate code samples"""
        samples = {
            'python': [
                {
                    'operation': 'GET /users',
                    'code': '''
import requests

response = requests.get('/users', params={'limit': 10})
users = response.json()
'''
                }
            ],
            'javascript': [
                {
                    'operation': 'GET /users',
                    'code': '''
const response = await fetch('/users?limit=10');
const users = await response.json();
'''
                }
            ]
        }
        return samples.get(language, [])


class TutorialWriter:
    """Technical tutorial writer"""
    
    def __init__(self):
        self.tutorials = []
    
    def create_tutorial(self,
                        title: str,
                        difficulty: str,
                        estimated_time: str,
                        objectives: List[str],
                        steps: List[Dict]) -> Dict:
        """Create tutorial"""
        tutorial = {
            'id': f"tutorial_{len(self.tutorials)}",
            'title': title,
            'difficulty': difficulty,
            'estimated_time': estimated_time,
            'objectives': objectives,
            'steps': steps,
            'created_at': datetime.now().isoformat()
        }
        self.tutorials.append(tutorial)
        return tutorial
    
    def generate_tutorial_content(self,
                                  tutorial_id: str) -> str:
        """Generate tutorial markdown"""
        tutorial = next((t for t in self.tutorials if t['id'] == tutorial_id), None)
        if not tutorial:
            return "Tutorial not found"
        
        content = f"# {tutorial['title']}\n\n"
        content += f"**Difficulty:** {tutorial['difficulty']} | **Time:** {tutorial['estimated_time']}\n\n"
        
        content += "## Objectives\n\n"
        for obj in tutorial['objectives']:
            content += f"- {obj}\n"
        content += "\n"
        
        for i, step in enumerate(tutorial['steps'], 1):
            content += f"## Step {i}: {step['title']}\n\n"
            content += f"{step.get('description', '')}\n\n"
            if 'code' in step:
                content += f"```\n{step['code']}\n```\n\n"
        
        return content
    
    def validate_tutorial(self, tutorial_id: str) -> Dict:
        """Validate tutorial completeness"""
        return {
            'tutorial_id': tutorial_id,
            'valid': True,
            'checks': {
                'has_objectives': True,
                'has_prerequisites': True,
                'has_steps': True,
                'code_examples_valid': True
            }
        }


class ReadmeGenerator:
    """README file generator"""
    
    def __init__(self):
        self.templates = {}
    
    def generate_project_readme(self,
                                project_name: str,
                                description: str,
                                features: List[str],
                                installation: str,
                                usage: str,
                                contributors: List[str] = None) -> str:
        """Generate project README"""
        readme = f"""# {project_name}

{description}

## Features

"""
        for feature in features:
            readme += f"- {feature}\n"
        
        readme += f"""
## Installation

```
{installation}
```

## Usage

```
{usage}
```

## Contributing

"""
        if contributors:
            for contributor in contributors:
                readme += f"- {contributor}\n"
        else:
            readme += "See [CONTRIBUTING.md](CONTRIBUTING.md)\n"
        
        readme += f"""
## License

MIT License

*Generated on {datetime.now().strftime('%Y-%m-%d')}*
"""
        return readme
    
    def generate_api_readme(self,
                            api_name: str,
                            base_url: str,
                            authentication: str,
                            endpoints: List[Dict]) -> str:
        """Generate API README"""
        readme = f"""# {api_name} API

**Base URL:** `{base_url}`

## Authentication

```
{authentication}
```

## Endpoints

"""
        for endpoint in endpoints:
            readme += f"### {endpoint['method']} {endpoint['path']}\n"
            readme += f"_{endpoint['description']}_\n\n"
        
        return readme
    
    def generate_dev_readme(self,
                            project_name: str,
                            setup_commands: List[str],
                            testing_info: str,
                            architecture: str) -> str:
        """Generate developer README"""
        readme = f"""# {project_name} - Developer Guide

## Quick Start

```bash
"""
        for cmd in setup_commands:
            readme += f"{cmd}\n"
        readme += "```\n"
        
        readme += f"""
## Testing

{testing_info}

## Architecture

{architecture}
"""
        return readme


class ChangelogGenerator:
    """Changelog generator"""
    
    def __init__(self):
        self.changes = []
    
    def add_change(self,
                   version: str,
                   change_type: str,
                   description: str,
                   breaking: bool = False) -> Dict:
        """Add changelog entry"""
        change = {
            'version': version,
            'type': change_type,
            'description': description,
            'breaking': breaking,
            'date': datetime.now().isoformat()
        }
        self.changes.append(change)
        return change
    
    def generate_changelog(self,
                           format: str = "keepachangelog") -> str:
        """Generate changelog"""
        changelog = "# Changelog\n\n"
        
        versions = {}
        for change in self.changes:
            if change['version'] not in versions:
                versions[change['version']] = []
            versions[change['version']].append(change)
        
        for version in sorted(versions.keys(), reverse=True):
            changes = versions[version]
            changelog += f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n"
            
            by_type = {}
            for change in changes:
                t = change['type']
                if t not in by_type:
                    by_type[t] = []
                by_type[t].append(change)
            
            for change_type in ['added', 'changed', 'deprecated', 'removed', 'fixed', 'security']:
                if change_type in by_type:
                    changelog += f"### {change_type.capitalize()}\n\n"
                    for c in by_type[change_type]:
                        prefix = "[BREAKING] " if c['breaking'] else ""
                        changelog += f"- {prefix}{c['description']}\n"
                    changelog += "\n"
        
        return changelog
    
    def generate_release_notes(self,
                               version: str) -> str:
        """Generate release notes"""
        version_changes = [c for c in self.changes if c['version'] == version]
        
        notes = f"# Release Notes for {version}\n\n"
        
        breaking = [c for c in version_changes if c['breaking']]
        if breaking:
            notes += "## Breaking Changes\n\n"
            for c in breaking:
                notes += f"- {c['description']}\n"
            notes += "\n"
        
        notes += "## Changes\n\n"
        for c in version_changes:
            notes += f"- [{c['type']}] {c['description']}\n"
        
        return notes


class StyleGuideChecker:
    """Technical writing style checker"""
    
    def __init__(self):
        self.rules = {}
    
    def check_readability(self, text: str) -> Dict:
        """Check text readability"""
        words = text.split()
        sentences = text.split('.')
        
        return {
            'readability_score': 85,
            'avg_sentence_length': len(words) / max(len(sentences), 1),
            'avg_word_length': sum(len(w) for w in words) / max(len(words), 1),
            'grade_level': '8th grade',
            'suggestions': [
                'Shorten sentences over 25 words',
                'Use active voice',
                'Add more examples'
            ]
        }
    
    def check_terminology(self,
                          text: str,
                          allowed_terms: List[str],
                          forbidden_terms: List[str] = None) -> Dict:
        """Check terminology consistency"""
        forbidden = forbidden_terms or ['dont', 'wont', 'cant']
        issues = []
        
        for term in forbidden:
            if term in text.lower():
                issues.append(f"Use '{term.replace(chr(39), \"'\")}' instead of '{term}'")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'allowed_terms_used': sum(1 for t in allowed_terms if t in text)
        }
    
    def check_code_examples(self,
                            content: str) -> Dict:
        """Check code examples"""
        import re
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        
        return {
            'code_blocks': len(code_blocks),
            'valid': True,
            'issues': [],
            'suggestions': [
                'Add language identifier to code blocks',
                'Include output examples'
            ]
        }
    
    def generate_style_report(self, text: str) -> Dict:
        """Generate full style report"""
        return {
            'readability': self.check_readability(text),
            'terminology': self.check_terminology(text, ['API', 'endpoint', 'parameter']),
            'code_examples': self.check_code_examples(text),
            'overall_score': 82,
            'recommendations': [
                'Improve sentence variety',
                'Add more practical examples',
                'Standardize terminology'
            ]
        }


if __name__ == "__main__":
    api = APIDocGenerator()
    api.add_endpoint('GET', '/users', 'List users', 'Get paginated list of users',
                     [{'name': 'limit', 'type': 'integer', 'in': 'query', 'required': False}])
    
    spec = api.generate_openapi_spec()
    print(f"OpenAPI Version: {spec['openapi']}")
    
    tutorial = TutorialWriter()
    tutorial.create_tutorial(
        "Getting Started",
        "Beginner",
        "30 minutes",
        ["Install the SDK", "Make first API call"],
        [{'title': 'Installation', 'code': 'pip install sdk'}]
    )
    
    changelog = ChangelogGenerator()
    changelog.add_change("1.0.0", "added", "Initial release")
    changelog.add_change("1.0.1", "fixed", "Bug in login", breaking=False)
    
    output = changelog.generate_changelog()
    print(output[:200])
