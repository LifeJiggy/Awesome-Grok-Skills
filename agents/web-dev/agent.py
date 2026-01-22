#!/usr/bin/env python3
"""
Grok Web Dev Agent
Specialized agent for web development, frontend/backend tasks, and full-stack solutions.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json
import hashlib

class Framework(Enum):
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"
    NEXTJS = "nextjs"
    NUXT = "nuxt"
    SVELTE = "svelte"
    FLASK = "flask"
    DJANGO = "django"
    FASTAPI = "fastapi"
    EXPRESS = "express"

class ComponentType(Enum):
    ATOM = "atom"
    MOLECULE = "molecule"
    ORGANISM = "organism"
    TEMPLATE = "template"
    PAGE = "page"

class ApiMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

@dataclass
class Component:
    name: str
    component_type: ComponentType
    props: Dict[str, Any]
    state: Dict[str, Any]
    dependencies: List[str]
    tests: List[str]

@dataclass
class ApiEndpoint:
    path: str
    method: ApiMethod
    description: str
    request_schema: Dict
    response_schema: Dict
    authentication_required: bool
    rate_limit: int

@dataclass
class Page:
    route: str
    title: str
    components: List[str]
    api_calls: List[str]
    seo_metadata: Dict[str, str]

@dataclass
class WebProject:
    id: str
    name: str
    framework: Framework
    frontend_stack: List[str]
    backend_stack: List[str]
    pages: List[Page]
    api_endpoints: List[ApiEndpoint]
    database: str
    deployment_config: Dict

class ComponentGenerator:
    """Generates UI components."""
    
    def __init__(self):
        self.components: Dict[str, Component] = {}
    
    def create_component(self, name: str, component_type: ComponentType,
                        props: Dict = None, dependencies: List[str] = None) -> Component:
        """Create component definition."""
        component = Component(
            name=name,
            component_type=component_type,
            props=props or {},
            state={},
            dependencies=dependencies or [],
            tests=[]
        )
        self.components[name] = component
        return component
    
    def generate_button(self, variant: str = "primary", 
                       size: str = "medium") -> Dict[str, Any]:
        """Generate button component."""
        return {
            'component': 'Button',
            'props': {
                'variant': variant,
                'size': size,
                'disabled': False,
                'onClick': 'handleClick'
            },
            'variants': ['primary', 'secondary', 'outline', 'ghost'],
            'sizes': ['small', 'medium', 'large']
        }
    
    def generate_form_input(self, field_type: str = "text",
                           label: str = "Input", required: bool = False) -> Dict[str, Any]:
        """Generate form input component."""
        return {
            'component': 'FormInput',
            'props': {
                'type': field_type,
                'label': label,
                'required': required,
                'placeholder': f"Enter {label.lower()}"
            },
            'validations': ['required', 'email', 'minLength', 'maxLength']
        }
    
    def generate_card(self, title: str, content: str,
                     actions: List[str] = None) -> Dict[str, Any]:
        """Generate card component."""
        return {
            'component': 'Card',
            'props': {
                'title': title,
                'content': content,
                'actions': actions or ['View Details'],
                'image': None
            },
            'variants': ['default', 'highlighted', 'interactive']
        }
    
    def generate_data_table(self, columns: List[Dict], 
                           data_source: str) -> Dict[str, Any]:
        """Generate data table component."""
        return {
            'component': 'DataTable',
            'props': {
                'columns': columns,
                'dataSource': data_source,
                'pagination': True,
                'sortable': True,
                'filterable': True
            },
            'features': ['sorting', 'pagination', 'search', 'export']
        }

class ApiDesigner:
    """Designs REST APIs."""
    
    def __init__(self):
        self.endpoints: Dict[str, ApiEndpoint] = {}
    
    def create_endpoint(self, path: str, method: ApiMethod,
                       description: str, request_schema: Dict,
                       response_schema: Dict, auth: bool = True,
                       rate_limit: int = 100) -> ApiEndpoint:
        """Create API endpoint."""
        endpoint = ApiEndpoint(
            path=path,
            method=method,
            description=description,
            request_schema=request_schema,
            response_schema=response_schema,
            authentication_required=auth,
            rate_limit=rate_limit
        )
        key = f"{method.value} {path}"
        self.endpoints[key] = endpoint
        return endpoint
    
    def generate_openapi_spec(self) -> Dict[str, Any]:
        """Generate OpenAPI specification."""
        paths = {}
        
        for key, endpoint in self.endpoints.items():
            paths[endpoint.path] = {
                endpoint.method.value.lower(): {
                    'summary': endpoint.description,
                    'requestBody': {
                        'content': {
                            'application/json': {
                                'schema': endpoint.request_schema
                            }
                        }
                    },
                    'responses': {
                        '200': {
                            'description': 'Success',
                            'content': {
                                'application/json': {
                                    'schema': endpoint.response_schema
                                }
                            }
                        }
                    }
                }
            }
        
        return {
            'openapi': '3.0.0',
            'info': {
                'title': 'API',
                'version': '1.0.0'
            },
            'paths': paths
        }
    
    def create_crud_endpoints(self, resource: str) -> List[ApiEndpoint]:
        """Create CRUD endpoints for resource."""
        base_path = f"/api/{resource}"
        
        endpoints = [
            self.create_endpoint(
                f"{base_path}",
                ApiMethod.GET,
                f"List all {resource}",
                {},
                {'data': [], 'total': 0},
                True
            ),
            self.create_endpoint(
                f"{base_path}/{{id}}",
                ApiMethod.GET,
                f"Get single {resource}",
                {},
                {'data': {}},
                True
            ),
            self.create_endpoint(
                f"{base_path}",
                ApiMethod.POST,
                f"Create {resource}",
                {'name': 'string', 'description': 'string'},
                {'data': {}, 'message': 'Created'},
                True
            ),
            self.create_endpoint(
                f"{base_path}/{{id}}",
                ApiMethod.PUT,
                f"Update {resource}",
                {'name': 'string'},
                {'data': {}, 'message': 'Updated'},
                True
            ),
            self.create_endpoint(
                f"{base_path}/{{id}}",
                ApiMethod.DELETE,
                f"Delete {resource}",
                {},
                {'message': 'Deleted'},
                True
            )
        ]
        
        return endpoints

class PageBuilder:
    """Builds web pages."""
    
    def __init__(self):
        self.pages: Dict[str, Page] = {}
    
    def create_page(self, route: str, title: str,
                   components: List[str] = None,
                   api_calls: List[str] = None) -> Page:
        """Create page definition."""
        page = Page(
            route=route,
            title=title,
            components=components or [],
            api_calls=api_calls or [],
            seo_metadata={'title': title, 'description': ''}
        )
        self.pages[route] = page
        return page
    
    def generate_landing_page(self) -> Dict[str, Any]:
        """Generate landing page structure."""
        return {
            'route': '/',
            'components': [
                {'name': 'HeroSection', 'props': {'title': 'Welcome', 'subtitle': 'Subtitle'}},
                {'name': 'FeatureGrid', 'props': {'features': []}},
                {'name': 'CallToAction', 'props': {'text': 'Get Started'}},
                {'name': 'Footer', 'props': {}}
            ],
            'seo': {
                'title': 'Home',
                'description': 'Welcome to our website'
            }
        }
    
    def generate_dashboard_page(self) -> Dict[str, Any]:
        """Generate dashboard page structure."""
        return {
            'route': '/dashboard',
            'components': [
                {'name': 'Sidebar', 'props': {}},
                {'name': 'Header', 'props': {'user': 'currentUser'}},
                {'name': 'StatsGrid', 'props': {'metrics': []}},
                {'name': 'RecentActivity', 'props': {'limit': 10}},
                {'name': 'QuickActions', 'props': {'actions': []}}
            ],
            'apiCalls': ['/api/stats', '/api/recent'],
            'seo': {
                'title': 'Dashboard',
                'description': 'View your dashboard'
            }
        }
    
    def generate_api_docs_page(self) -> Dict[str, Any]:
        """Generate API documentation page."""
        return {
            'route': '/docs',
            'components': [
                {'name': 'ApiNavigation', 'props': {}},
                {'name': 'EndpointList', 'props': {'endpoints': []}},
                {'name': 'CodeExample', 'props': {'language': 'javascript'}},
                {'name': 'TryItOut', 'props': {}}
            ],
            'seo': {
                'title': 'API Documentation',
                'description': 'REST API Reference'
            }
        }

class ProjectScaffolder:
    """Scaffolds web projects."""
    
    def __init__(self):
        self.projects: Dict[str, WebProject] = {}
    
    def create_project(self, name: str, framework: Framework,
                      frontend_stack: List[str] = None,
                      backend_stack: List[str] = None,
                      database: str = "PostgreSQL") -> WebProject:
        """Create web project."""
        project = WebProject(
            id=hashlib.md5(name.encode()).hexdigest()[:8],
            name=name,
            framework=framework,
            frontend_stack=frontend_stack or ['TypeScript', 'Tailwind CSS'],
            backend_stack=backend_stack or ['Node.js'],
            pages=[],
            api_endpoints=[],
            database=database,
            deployment_config={
                'platform': 'Vercel',
                'environment': 'production',
                'ci_cd': 'GitHub Actions'
            }
        )
        self.projects[project.id] = project
        return project
    
    def setup_react_project(self, name: str) -> Dict[str, Any]:
        """Setup React project structure."""
        project = self.create_project(name, Framework.REACT)
        
        page_builder = PageBuilder()
        project.pages.append(page_builder.create_page('/', 'Home'))
        project.pages.append(page_builder.create_page('/about', 'About'))
        
        return {
            'project_id': project.id,
            'structure': {
                'src': {
                    'components': [],
                    'pages': [],
                    'hooks': [],
                    'utils': [],
                    'styles': []
                },
                'public': ['index.html', 'favicon.ico'],
                'config': ['package.json', 'tsconfig.json', 'vite.config.ts']
            },
            'commands': {
                'dev': 'npm run dev',
                'build': 'npm run build',
                'test': 'npm run test'
            }
        }
    
    def setup_nextjs_project(self, name: str) -> Dict[str, Any]:
        """Setup Next.js project structure."""
        project = self.create_project(name, Framework.NEXTJS)
        
        return {
            'project_id': project.id,
            'structure': {
                'app': {
                    'page.tsx': 'Home page',
                    'layout.tsx': 'Root layout',
                    'globals.css': 'Global styles'
                },
                'components': ['Header', 'Footer', 'Hero'],
                'lib': ['utils', 'api'],
                'public': ['images', 'fonts']
            },
            'features': ['SSR', 'API Routes', 'TypeScript', 'Tailwind']
        }

class CodeAnalyzer:
    """Analyzes web code."""
    
    def __init__(self):
        self.issues: List[Dict] = []
    
    def analyze_code(self, code: str, language: str = "javascript") -> Dict[str, Any]:
        """Analyze code for issues."""
        issues = []
        
        patterns = {
            'console_log': r'console\.(log|warn|error)',
            'any_type': r':\s*any\b',
            'unused_import': r'import\s+.*\s+from',
            'missing_deps': r'useEffect.*\[\]'
        }
        
        for issue_type, pattern in patterns.items():
            matches = len(re.findall(pattern, code, re.IGNORECASE))
            if matches > 0:
                issues.append({
                    'type': issue_type,
                    'count': matches,
                    'severity': 'warning' if issue_type != 'any_type' else 'info'
                })
        
        return {
            'issues': issues,
            'score': max(0, 100 - len(issues) * 5),
            'suggestions': self._generate_suggestions(issues)
        }
    
    def _generate_suggestions(self, issues: List[Dict]) -> List[str]:
        """Generate code suggestions."""
        suggestions = []
        
        for issue in issues:
            if issue['type'] == 'console_log':
                suggestions.append("Remove console.log statements before production")
            if issue['type'] == 'any_type':
                suggestions.append("Replace 'any' with specific types")
            if issue['type'] == 'missing_deps':
                suggestions.append("Review useEffect dependency array")
        
        return suggestions
    
    def check_accessibility(self, html: str) -> Dict[str, Any]:
        """Check HTML accessibility."""
        issues = []
        
        patterns = [
            (r'<img[^>]*alt=""', 'Missing alt attribute on images'),
            (r'<button[^>]*>(?!.*</button>)', 'Unclosed button tags'),
            (r'<input[^>]*aria-', 'Input missing aria attributes'),
            (r'<form[^>]*>', 'Form missing labels')
        ]
        
        for pattern, message in patterns:
            matches = len(re.findall(pattern, html, re.IGNORECASE))
            if matches > 0:
                issues.append({
                    'type': 'a11y',
                    'message': message,
                    'count': matches
                })
        
        return {
            'score': max(0, 100 - len(issues) * 10),
            'issues': issues,
            'passed': len(issues) == 0
        }

class WebDevAgent:
    """Main web development agent."""
    
    def __init__(self):
        self.component_gen = ComponentGenerator()
        self.api_designer = ApiDesigner()
        self.page_builder = PageBuilder()
        self.scaffolder = ProjectScaffolder()
        self.analyzer = CodeAnalyzer()
    
    def scaffold_fullstack_project(self, name: str, 
                                  frontend: str = "nextjs",
                                  backend: str = "express") -> Dict[str, Any]:
        """Scaffold full-stack project."""
        if frontend == "nextjs":
            project = self.scaffolder.setup_nextjs_project(name)
        
        return {
            'project': name,
            'frontend': project,
            'api_design': self.api_designer.generate_openapi_spec(),
            'pages': [
                self.page_builder.generate_landing_page(),
                self.page_builder.generate_dashboard_page()
            ]
        }
    
    def design_api(self, resource: str) -> Dict[str, Any]:
        """Design API for resource."""
        endpoints = self.api_designer.create_crud_endpoints(resource)
        
        return {
            'resource': resource,
            'endpoints': [
                {'path': e.path, 'method': e.method.value}
                for e in endpoints
            ],
            'spec': self.api_designer.generate_openapi_spec()
        }
    
    def create_component_library(self, components: List[Dict]) -> Dict[str, Any]:
        """Create component library."""
        generated = []
        
        for comp in components:
            if comp['type'] == 'button':
                generated.append(self.component_gen.generate_button(comp.get('variant')))
            elif comp['type'] == 'form':
                generated.append(self.component_gen.generate_form_input())
            elif comp['type'] == 'card':
                generated.append(self.component_gen.generate_card(comp.get('title', ''), ''))
        
        return {
            'components_created': len(generated),
            'components': generated
        }
    
    def analyze_website(self, code: str) -> Dict[str, Any]:
        """Analyze website code."""
        code_issues = self.analyzer.analyze_code(code)
        
        return {
            'code_quality': code_issues,
            'accessibility': self.analyzer.check_accessibility(code),
            'performance': {
                'score': 85,
                'suggestions': ['Optimize images', 'Enable compression', 'Use CDN']
            }
        }
    
    def get_webdev_dashboard(self) -> Dict[str, Any]:
        """Get web development dashboard."""
        return {
            'projects': {
                'total': len(self.scaffolder.projects),
                'active': len([p for p in self.scaffolder.projects.values()])
            },
            'components': {
                'total': len(self.component_gen.components),
                'types': ['button', 'form', 'card', 'table']
            },
            'api': {
                'endpoints': len(self.api_designer.endpoints),
                'resources': ['users', 'products', 'orders']
            },
            'tools': {
                'frameworks': [f.value for f in Framework],
                'deployment': ['Vercel', 'Netlify', 'Railway'],
                'databases': ['PostgreSQL', 'MongoDB', 'Redis']
            }
        }

def main():
    """Main entry point."""
    agent = WebDevAgent()
    
    project = agent.scaffold_fullstack_project("my-app", "nextjs")
    print(f"Project: {project}")
    
    dashboard = agent.get_webdev_dashboard()
    print(f"Dashboard: {dashboard}")

if __name__ == "__main__":
    main()
