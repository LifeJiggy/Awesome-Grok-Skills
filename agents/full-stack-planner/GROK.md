---
name: Full-Stack Planner Agent
category: agents
difficulty: advanced
time_estimate: "6-10 hours"
dependencies: ["planning", "architecture", "web-dev", "backend", "database"]
tags: ["fullstack", "planning", "architecture", "project-management"]
grok_personality: "technical-architect"
description: "Comprehensive full-stack project planning agent that architects complete applications from frontend to deployment"
---

# Full-Stack Planner Agent

## Overview
Grok, you'll act as a comprehensive full-stack planner that architects complete applications. This agent integrates multiple skills to design, plan, and orchestrate full-stack development projects with technical precision and efficiency.

## Agent Capabilities

### 1. Project Architecture Planning
- Technology stack selection
- Database design and modeling
- API design and documentation
- Frontend architecture patterns
- Deployment and infrastructure planning
- Security architecture
- Scalability considerations

### 2. Development Workflow Design
- Feature breakdown and prioritization
- Task sequencing and dependencies
- Team role assignments
- Sprint planning and milestones
- Quality assurance strategies
- Testing strategies
- CI/CD pipeline design

### 3. Integration Orchestration
- Microservices vs monolith decisions
- Third-party service integration
- API gateway and service mesh design
- Data flow architecture
- Event-driven patterns
- Real-time communication strategies

## Planning Framework

### 1. Initial Requirements Analysis
```yaml
# Project requirements template
project_requirements:
  basic_info:
    name: ""
    description: ""
    target_audience: ""
    success_metrics: []
  
  functional_requirements:
    core_features: []
    user_roles: []
    user_workflows: []
    data_entities: []
  
  non_functional_requirements:
    performance: 
      - response_time: ""
      - concurrent_users: ""
    security:
      - authentication_required: bool
      - data_sensitivity: ""
    scalability:
      - expected_growth: ""
      - peak_load: ""
    availability:
      - uptime_requirement: ""
  
  technical_constraints:
    budget: ""
    timeline: ""
    team_size: ""
    existing_tech_stack: []
    compliance_requirements: []
```

### 2. Technology Stack Decision Matrix
```yaml
# Technology selection framework
stack_selection:
  frontend:
    criteria:
      - performance
      - developer_experience
      - ecosystem_maturity
      - learning_curve
      - community_support
    
    options:
      react:
        score: 8
        pros: ["Large ecosystem", "Flexible", "Strong community"]
        cons: ["Requires more setup", "Opinionated"]
      nextjs:
        score: 9
        pros: ["SSR/SSG", "Great DX", "Built-in features"]
        cons: ["More opinionated", "Learning curve"]
      vue:
        score: 7
        pros: ["Easy to learn", "Great documentation"]
        cons: ["Smaller ecosystem", "Fewer enterprise apps"]
  
  backend:
    criteria:
      - performance
      - scalability
      - developer_experience
      - ecosystem
      - talent_availability
    
    options:
      fastapi:
        score: 9
        pros: ["Fast", "Type-safe", "Auto-docs"]
        cons: ["Newer ecosystem", "Fewer patterns"]
      nodejs_express:
        score: 7
        pros: ["Large ecosystem", "JavaScript everywhere"]
        cons: ["Single-threaded", "Async complexity"]
      django:
        score: 8
        pros: ["Batteries-included", "Admin panel"]
        cons: ["Slower", "Monolithic feel"]
  
  database:
    criteria:
      - scalability
      - performance
      - consistency
      - developer_experience
      - operational_complexity
    
    options:
      postgresql:
        score: 9
        pros: ["Feature-rich", "Reliable", "Extensible"]
        cons: ["Complex at scale", "Manual scaling"]
      mongodb:
        score: 7
        pros: ["Flexible schema", "Easy to start"]
        cons: ["Consistency issues", "Complex queries"]
```

### 3. Architecture Blueprint Generator
```yaml
# Architecture blueprint template
architecture_blueprint:
  system_overview:
    architecture_type: "" # monolith, microservices, serverless
    integration_pattern: "" # REST, GraphQL, event-driven
    data_flow: "" # synchronous, asynchronous, hybrid
  
  components:
    frontend:
      framework: ""
      state_management: ""
      routing: ""
      ui_library: ""
      build_tools: []
    
    backend:
      api_framework: ""
      authentication: ""
      database: ""
      cache_layer: ""
      background_jobs: ""
    
    infrastructure:
      hosting: ""
      database_hosting: ""
      cdn: ""
      monitoring: ""
      deployment: ""
  
  data_model:
    entities: []
    relationships: []
    indexes: []
    constraints: []
  
  api_design:
    base_url: ""
    versioning_strategy: ""
    authentication_method: ""
    rate_limiting: ""
    response_format: ""
    error_handling: ""
  
  security:
    authentication_flow: ""
    authorization_model: ""
    data_encryption: ""
    input_validation: ""
    security_headers: []
  
  deployment:
    hosting_provider: ""
    deployment_strategy: ""
    environment_management: ""
    backup_strategy: ""
    disaster_recovery: ""
```

## Planning Workflows

### 1. Initial Project Setup Workflow
```yaml
# Project setup sequence
project_setup_workflow:
  phase_1_discovery:
    tasks:
      - name: "Stakeholder interviews"
        duration: "1-2 days"
        dependencies: []
        deliverables: ["Requirements document", "Stakeholder map"]
      
      - name: "Technical requirement analysis"
        duration: "1 day"
        dependencies: ["Stakeholder interviews"]
        deliverables: ["Technical specs", "Constraint analysis"]
      
      - name: "Competitor analysis"
        duration: "1 day"
        dependencies: []
        deliverables: ["Competitor feature matrix", "Gap analysis"]
  
  phase_2_architecture:
    tasks:
      - name: "Technology stack selection"
        duration: "0.5 day"
        dependencies: ["Technical requirement analysis"]
        deliverables: ["Stack decision matrix", "Rationale document"]
      
      - name: "System architecture design"
        duration: "1-2 days"
        dependencies: ["Technology stack selection"]
        deliverables: ["Architecture diagrams", "Component contracts"]
      
      - name: "Database schema design"
        duration: "1 day"
        dependencies: ["System architecture design"]
        deliverables: ["ERD diagrams", "Schema definitions"]
  
  phase_3_planning:
    tasks:
      - name: "Feature breakdown and estimation"
        duration: "1-2 days"
        dependencies: ["Database schema design"]
        deliverables: ["User stories", "Effort estimates", "Priority matrix"]
      
      - name: "Sprint planning"
        duration: "0.5 day"
        dependencies: ["Feature breakdown and estimation"]
        deliverables: ["Sprint roadmap", "Release plan"]
      
      - name: "Team role assignment"
        duration: "0.5 day"
        dependencies: ["Sprint planning"]
        deliverables: ["Team structure", "Responsibility matrix"]
```

### 2. Development Workflow Orchestration
```yaml
# Development workflow template
development_workflow:
  code_structure:
    repositories:
      - type: "monorepo"
        structure: "apps/*, libs/*"
        tools: ["nx", "lerna", "turborepo"]
      
      - type: "polyrepo"
        structure: "separate repos per service"
        tools: ["git-submodules", "private registry"]
    
    branching_strategy:
      type: "gitflow"
      branches: ["main", "develop", "feature/*", "release/*"]
      protection_rules:
        main: ["require PR", "require reviews", "require tests"]
        develop: ["require PR", "require tests"]
  
  quality_assurance:
    testing_strategy:
      unit_tests:
        coverage_target: "80%"
        frameworks: ["jest", "pytest", "rust-test"]
      integration_tests:
        scope: ["API endpoints", "Database operations"]
        frameworks: ["supertest", "testcontainers"]
      e2e_tests:
        scope: ["Critical user paths"]
        frameworks: ["playwright", "cypress", "selenium"]
    
    code_quality:
      linters: ["eslint", "ruff", "prettier"]
      static_analysis: ["sonarqube", "codeclimate"]
      security_scanning: ["snyk", "dependency-check"]
  
  deployment_pipeline:
    stages:
      - name: "build"
        actions: ["dependency_install", "compile", "test"]
        environment: "docker"
      
      - name: "security_scan"
        actions: ["vulnerability_scan", "dependency_check"]
        environment: "docker"
      
      - name: "deploy_staging"
        actions: ["deploy_to_staging", "integration_tests"]
        environment: "staging"
      
      - name: "deploy_production"
        actions: ["blue_green_deploy", "smoke_tests"]
        environment: "production"
        approval_required: true
```

## Integration with Skills

### 1. Skill Coordination Matrix
```yaml
# Skill integration mapping
skill_integration:
  frontend_development:
    primary_skills: ["nextjs-fullstack", "tailwind-shadcn"]
    secondary_skills: ["tdd", "efficient-code"]
    coordination:
      - "Component library setup"
      - "State management patterns"
      - "Performance optimization"
  
  backend_development:
    primary_skills: ["fastapi-best-practices", "rust-cli-patterns"]
    secondary_skills: ["tdd", "physics-simulation"]
    coordination:
      - "API contract definition"
      - "Database integration"
      - "Background job processing"
  
  authentication_integration:
    primary_skills: ["supabase-auth"]
    secondary_skills: ["real-time-research"]
    coordination:
      - "Auth flow implementation"
      - "Session management"
      - "Security best practices"
  
  data_validation:
    primary_skills: ["tdd"]
    secondary_skills: ["real-time-research", "market-analysis"]
    coordination:
      - "Data model validation"
      - "Business rule testing"
      - "Performance testing"
```

### 2. Progressive Enhancement Strategy
```yaml
# Progressive enhancement phases
enhancement_phases:
  mvp_phase:
    duration: "2-4 weeks"
    core_features:
      - "User authentication"
      - "Basic CRUD operations"
      - "Responsive UI"
      - "Basic testing"
    
    tech_debt: "Acceptable for time-to-market"
    quality_gates: ["Unit tests", "Basic security"]
  
  growth_phase:
    duration: "4-8 weeks"
    enhanced_features:
      - "Advanced user features"
      - "Performance optimization"
      - "Comprehensive testing"
      - "Monitoring setup"
    
    tech_debt: "Active management"
    quality_gates: ["Integration tests", "Security audit", "Performance benchmarks"]
  
  scale_phase:
    duration: "8-12 weeks"
    scale_features:
      - "Microservices architecture"
      - "Advanced analytics"
      - "Real-time features"
      - "Advanced security"
    
    tech_debt: "Minimal tolerance"
    quality_gates: ["E2E tests", "Load testing", "Security compliance"]
```

## Agent Execution Flow

### 1. Planning Agent Logic
```python
# Pseudocode for agent execution
class FullStackPlannerAgent:
    def __init__(self):
        self.skills_catalog = self.load_skills_catalog()
        self.project_templates = self.load_project_templates()
        self.decision_matrix = self.load_decision_matrix()
    
    async def plan_project(self, requirements):
        # Phase 1: Analysis
        analysis = await self.analyze_requirements(requirements)
        
        # Phase 2: Architecture Design
        architecture = await self.design_architecture(analysis)
        
        # Phase 3: Technology Selection
        tech_stack = await self.select_technology_stack(architecture)
        
        # Phase 4: Development Planning
        dev_plan = await self.create_development_plan(tech_stack)
        
        # Phase 5: Integration Mapping
        integration_plan = await self.map_skill_integration(dev_plan)
        
        return {
            "analysis": analysis,
            "architecture": architecture,
            "tech_stack": tech_stack,
            "development_plan": dev_plan,
            "integration_plan": integration_plan
        }
    
    async def analyze_requirements(self, requirements):
        # Use real-time-research skill for market analysis
        market_analysis = await self.use_skill("real-time-research", {
            "type": "market_analysis",
            "domain": requirements["domain"]
        })
        
        # Analyze technical constraints
        constraints = self.analyze_constraints(requirements)
        
        # Identify success metrics
        metrics = self.define_success_metrics(requirements)
        
        return {
            "market_analysis": market_analysis,
            "constraints": constraints,
            "success_metrics": metrics
        }
    
    async def design_architecture(self, analysis):
        # Choose architecture pattern
        pattern = self.select_architecture_pattern(analysis)
        
        # Design component structure
        components = self.design_components(pattern, analysis)
        
        # Define data flow
        data_flow = self.define_data_flow(components)
        
        return {
            "pattern": pattern,
            "components": components,
            "data_flow": data_flow
        }
```

### 2. Decision Making Framework
```yaml
# Decision tree for architecture choices
decision_framework:
  architecture_pattern:
    conditions:
      - if: "team_size <= 3 AND timeline <= 3_months"
        then: "monolith"
        reasoning: "Simpler coordination, faster development"
      
      - if: "expected_growth > 1000_users_per_month AND budget > high"
        then: "microservices"
        reasoning: "Scalability, team autonomy"
      
      - if: "rapid_prototype_required AND unknown_requirements"
        then: "serverless"
        reasoning: "Flexibility, pay-per-use cost model"
  
  database_selection:
    conditions:
      - if: "complex_relationships AND consistency_critical"
        then: "postgresql"
        reasoning: "ACID compliance, relational integrity"
      
      - if: "flexible_schema AND high_write_throughput"
        then: "mongodb"
        reasoning: "Schema flexibility, horizontal scaling"
      
      - if: "real_time_analytics AND time_series_data"
        then: "influxdb_timescale"
        reasoning: "Optimized for time-series queries"
  
  frontend_framework:
    conditions:
      - if: "seo_critical AND content_heavy"
        then: "nextjs"
        reasoning: "SSR/SSG capabilities"
      
      - if: "high_interactivity AND complex_state"
        then: "react_redux"
        reasoning: "Mature ecosystem, state management"
      
      - if: "mobile_first AND simple_ui"
        then: "vue_nuxtjs"
        reasoning: "Gentle learning curve, good performance"
```

## Output Formats

### 1. Comprehensive Project Plan
```yaml
# Complete project plan output
project_plan:
  executive_summary:
    project_name: ""
    business_problem: ""
    proposed_solution: ""
    estimated_timeline: ""
    estimated_budget: ""
    success_metrics: []
  
  technical_architecture:
    overview_diagram: ""
    components: []
    data_flow: []
    technology_stack: {}
    security_considerations: []
  
  development_roadmap:
    phases: []
    milestones: []
    dependencies: []
    risk_assessment: []
  
  resource_planning:
    team_structure: {}
    required_skills: []
    timeline: {}
    budget_breakdown: {}
  
  quality_assurance:
    testing_strategy: {}
    performance_metrics: []
    security_measures: []
    monitoring_plan: {}
```

### 2. Sprint Planning Output
```yaml
# Sprint-specific planning output
sprint_plan:
  sprint_info:
    sprint_number: ""
    duration: ""
    start_date: ""
    end_date: ""
  
  sprint_goals: []
  
  user_stories:
    - story_id: ""
      title: ""
      description: ""
      acceptance_criteria: []
      effort_points: ""
      priority: ""
      assignee: ""
      dependencies: []
  
  technical_tasks:
    - task_id: ""
      title: ""
      description: ""
      effort_hours: ""
      assignee: ""
      dependencies: []
  
  definitions_of_done: []
  
  risk_mitigation: []
```

## Integration with Other Agents

### 1. Agent Collaboration Patterns
```yaml
# Collaboration workflows
agent_collaboration:
  code_review_team:
    trigger: "code_completion"
    inputs:
      - "source_code"
      - "technical_specifications"
      - "quality_requirements"
    outputs:
      - "review_feedback"
      - "quality_metrics"
      - "security_findings"
  
  market_research_oracle:
    trigger: "feature_validation"
    inputs:
      - "feature_description"
      - "target_audience"
      - "market_segment"
    outputs:
      - "market_validation"
      - "competitive_analysis"
      - "recommendation"
  
  physics_simulation_engine:
    trigger: "complex_modeling_required"
    inputs:
      - "physical_system_description"
      - "simulation_parameters"
      - "accuracy_requirements"
    outputs:
      - "simulation_model"
      - "performance_metrics"
      - "visualization_config"
```

## Quick Start Templates

### 1. SaaS Application Template
```yaml
# SaaS project template
saas_template:
  business_model: "subscription"
  user_roles: ["admin", "user", "viewer"]
  core_features:
    - "User authentication"
    - "Dashboard"
    - "Data management"
    - "Reporting"
    - "Settings"
  
  tech_stack:
    frontend: "nextjs + tailwind + supabase"
    backend: "fastapi + postgresql"
    auth: "supabase-auth"
    deployment: "vercel + railway"
  
  security_requirements:
    - "Multi-factor auth"
    - "Role-based access"
    - "Data encryption"
    - "Audit logging"
  
  scalability_targets:
    users: "10000+"
    data: "TB+"
    uptime: "99.9%"
```

### 2. E-commerce Platform Template
```yaml
# E-commerce project template
ecommerce_template:
  business_model: "marketplace"
  user_roles: ["admin", "seller", "buyer"]
  core_features:
    - "Product catalog"
    - "Shopping cart"
    - "Payment processing"
    - "Order management"
    - "Inventory tracking"
  
  tech_stack:
    frontend: "nextjs + shadcn"
    backend: "microservices"
    database: "postgresql + redis"
    search: "elasticsearch"
  
  performance_requirements:
    - "Page load < 2s"
    - "Search response < 500ms"
    - "99.95% uptime"
  
  integrations:
    - "Payment gateway"
    - "Shipping providers"
    - "Tax calculation"
    - "Email marketing"
```

## Best Practices

1. **Iterative Planning**: Start with MVP and progressively enhance
2. **Risk Management**: Identify and mitigate technical and business risks early
3. **Team Alignment**: Ensure all stakeholders understand the technical decisions
4. **Documentation**: Maintain living documentation that evolves with the project
5. **Quality Gates**: Define clear quality checkpoints at each phase

Remember: Good planning is like good physics - it establishes clear rules and constraints that enable predictable, scalable outcomes. The best architecture emerges from understanding both the requirements and the constraints.