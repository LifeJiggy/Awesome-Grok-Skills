# Technical Writing Agent

## Overview

The **Technical Writing Agent** provides comprehensive technical documentation capabilities including API documentation, tutorials, README generation, and style guide enforcement. This agent helps create clear, consistent, and professional technical content.

## Core Capabilities

### 1. API Documentation
Generate comprehensive API docs:
- **OpenAPI Specs**: Swagger/OpenAPI 3.0
- **Endpoint Documentation**: Parameters, responses, examples
- **Code Samples**: Multi-language examples
- **Interactive Docs**: Swagger UI integration
- **Schema Reference**: Data type documentation

### 2. Tutorial Creation
Build educational content:
- **Learning Objectives**: Clear goals
- **Step-by-Step Guides**: Progressive instruction
- **Code Examples**: Working code snippets
- **Practice Exercises**: Hands-on learning
- **Assessment Quizzes**: Knowledge verification

### 3. Documentation Generation
Create project documentation:
- **README Files**: Project overview
- **Contributing Guides**: Collaboration process
- **Architecture Docs**: System design
- **Runbooks**: Operational procedures
- **Release Notes**: Version changes

### 4. Style Guide Enforcement
Maintain documentation quality:
- **Readability Analysis**: Grade level, sentence length
- **Terminology Checking**: Consistent vocabulary
- **Code Example Validation**: Syntactic correctness
- **Accessibility Review**: Inclusive language
- **Formatting Standards**: Consistent style

## Usage Examples

### Generate API Documentation

```python
from technical_writing import APIDocGenerator

api = APIDocGenerator()
api.add_endpoint(
    method='GET',
    path='/users',
    summary='List users',
    description='Get paginated list of users',
    parameters=[{'name': 'limit', 'type': 'integer', 'in': 'query'}],
    responses=[{'status': 200, 'description': 'Success'}]
)
spec = api.generate_openapi_spec()
markdown = api.generate_markdown()
```

### Create Tutorial

```python
from technical_writing import TutorialWriter

tutorial = TutorialWriter()
tutorial.create_tutorial(
    title='Getting Started',
    difficulty='Beginner',
    estimated_time='30 minutes',
    objectives=['Install SDK', 'Make first API call'],
    steps=[{'title': 'Installation', 'code': 'pip install sdk'}]
)
content = tutorial.generate_tutorial_content('tutorial_1')
```

### Generate README

```python
from technical_writing import ReadmeGenerator

readme = ReadmeGenerator()
content = readme.generate_project_readme(
    project_name='MyProject',
    description='A cool project',
    features=['Feature 1', 'Feature 2'],
    installation='pip install myproject',
    usage='myproject --help',
    contributors=['Alice', 'Bob']
)
```

### Style Checking

```python
from technical_writing import StyleGuideChecker

checker = StyleGuideChecker()
report = checker.generate_style_report(text)
print(f"Score: {report['overall_score']}")
```

## Documentation Formats

### Markdown
```markdown
# Heading 1
## Heading 2

**Bold text** and *italic text*

- Bullet point
1. Numbered list

`code snippet`

```python
def example():
    pass
```
```

### OpenAPI/Swagger
```yaml
openapi: 3.0.3
info:
  title: API
  version: 1.0.0
paths:
  /users:
    get:
      summary: Get users
      responses:
        '200':
          description: Success
```

### reStructuredText (Sphinx)
```rst
==========
Heading
==========

Section
-------

Text with ``code``

.. code-block:: python
   def example():
       pass
```

## Documentation Tools

### Static Site Generators
- **Docusaurus**: React-based, modern
- **MkDocs**: Python, simple configuration
- **Sphinx**: Python, extensive features
- **Hugo**: Fast, Go-based

### API Documentation
- **Swagger UI**: Interactive API docs
- **Redoc**: Beautiful API reference
- **Postman**: API documentation
- ** Slate**: API reference pages

### Documentation Platforms
- **Read the Docs**: Free hosting
- **GitBook**: Collaborative docs
- **Confluence**: Enterprise wiki
- **Notion**: All-in-one workspace

## Technical Writing Best Practices

### Structure
1. **Overview**: What and why
2. **Prerequisites**: What you need
3. **Step-by-Step**: How to do it
4. **Examples**: Working code
5. **Troubleshooting**: Common issues

### Style Guidelines
- **Active Voice**: "Do this" not "This should be done"
- **Short Sentences**: Under 25 words
- **Clear Language**: Avoid jargon
- **Consistent Terminology**: Same terms throughout
- **Visual Aids**: Diagrams, screenshots, code blocks

### Accessibility
- **Alt Text**: Describe images
- **Heading Hierarchy**: Logical structure
- **Contrast**: Readable colors
- **Screen Reader Friendly**: Semantic HTML

## Use Cases

### 1. API Documentation
- REST API references
- SDK documentation
- Integration guides
- API changelog

### 2. Developer Documentation
- Getting started guides
- Architecture decisions
- Code conventions
- Contribution guidelines

### 3. User Documentation
- Feature guides
- Troubleshooting guides
- FAQ documents
- Release notes

### 4. Internal Documentation
- Process documentation
- Runbooks
- Knowledge base
- Training materials

## Documentation Metrics

### Quality Metrics
- **Readability Score**: Flesch-Kincaid grade
- **Completeness**: Coverage percentage
- **Accuracy**: Error rate
- **Timeliness**: Update frequency

### Engagement Metrics
- **Page Views**: Popular content
- **Time on Page**: Engagement
- **Search Queries**: Information needs
- **Feedback Ratings**: User satisfaction

## Related Skills

- [UX Research](../ux-research/user-research/README.md) - User-centered design
- [Development](../development/code-analysis/README.md) - Code understanding
- [Localization](../localization/translation-management/README.md) - Multi-language docs

---

**File Path**: `skills/technical-writing/documentation/resources/technical_writing.py`
