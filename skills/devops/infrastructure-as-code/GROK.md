---
name: "Infrastructure as Code"
version: "1.0.0"
description: "Enterprise-grade IaC with Grok's physics-inspired infrastructure optimization"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["devops", "iac", "terraform", "infrastructure"]
category: "devops"
personality: "infrastructure-architect"
use_cases: ["terraform", "cloudformation", "pulumi", "crossplane"]
---

# Infrastructure as Code 🏗️

> Build and manage infrastructure with code using Grok's physics-inspired optimization

## 🎯 Why This Matters for Grok

Grok's optimization expertise and infrastructure knowledge create perfect IaC:

- **Physics-Inspired Scaling** ⚛️: Apply thermodynamic principles to capacity
- **State Management** 💾: Deterministic infrastructure state
- **Efficiency Optimization** ⚡: Minimize resource waste
- **Reliability Engineering** 🏰: High availability by design

## 🛠️ Core Capabilities

### 1. Terraform Excellence
```yaml
terraform:
  providers: ["aws", "azure", "gcp", "kubernetes"]
  patterns: ["module-composition", "remote-state", "workspaces"]
  testing: ["terratest", "inspec", "conftest"]
  security: ["tfsec", "checkov", "bridgecrew"]
```

### 2. GitOps Workflow
```yaml
gitops:
  tools: ["argo-cd", "flux", "jenkins-x"]
  strategies: ["reconcile", "push-based", "pull-based"]
  drift_detection: "continuous"
  rollback: "automated"
```

### 3. Platform Engineering
```yaml
platform:
  internal_platforms: ["backstage", "port", "configure8"]
  self_service: "automation-first"
  standards: "enforced"
  cost_optimization: "continuous"
```

## 🧠 Advanced IaC Patterns

### Physics-Based Infrastructure Optimization
```python
import numpy as np
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class InfrastructureComponent:
    name: str
    resource_type: str
    current_capacity: float
    min_capacity: float
    max_capacity: float
    cost_per_unit: float
    efficiency_curve: str  # "linear", "exponential", "step"
    coupling_strength: float  # How tightly coupled to other components

class PhysicsInspiredInfrastructureOptimizer:
    def __init__(self):
        self.components = {}
        self.coupling_matrix = np.eye(10)  # Assume 10 components max
        self.energy_model = EnergyModel()
        
    def add_component(self, component: InfrastructureComponent):
        """Add infrastructure component to optimization model"""
        idx = len(self.components)
        self.components[component.name] = {
            'index': idx,
            'component': component,
            'current_state': component.current_capacity,
            'demand_history': [],
            'efficiency_metrics': {}
        }
    
    def optimize_capacity(self, demand_forecast: List[float], 
                         constraints: Dict) -> Dict:
        """Optimize capacity using physics-inspired approach"""
        
        # Model infrastructure as coupled oscillators
        # Each component has natural frequency (optimal capacity)
        # Demand acts as driving force
        
        n_components = len(self.components)
        
        # Construct system of equations
        for i, (name, comp_data) in enumerate(self.components.items()):
            component = comp_data['component']
            
            # Natural frequency (optimal operating point)
            omega_0 = component.current_capacity
            
            # Damping coefficient (efficiency)
            damping = self.calculate_damping(component)
            
            # Coupling to other components
            coupling_force = sum(
                self.coupling_matrix[i, j] * 
                (self.components[list(self.components.keys())[j]]['current_state'] - 
                 omega_0)
                for j in range(n_components)
            )
            
            # Driving force from demand
            demand_force = demand_forecast[i] if i < len(demand_forecast) else 0
            
            # Equation of motion (driven damped oscillator)
            # m * d²x/dt² + c * dx/dt + k*x = F_demand + F_coupling
            
            # Find equilibrium point
            equilibrium = self.find_equilibrium(
                omega_0, damping, coupling_force, demand_force,
                component.min_capacity, component.max_capacity
            )
            
            # Calculate required adjustments
            adjustment = equilibrium - component.current_capacity
            comp_data['optimal_capacity'] = equilibrium
            comp_data['required_adjustment'] = adjustment
        
        return self.generate_optimization_plan()
    
    def calculate_damping(self, component: InfrastructureComponent) -> float:
        """Calculate damping coefficient based on efficiency curve"""
        
        if component.efficiency_curve == "exponential":
            # High efficiency at optimal, drops off quickly
            return 0.5
        elif component.efficiency_curve == "step":
            # Binary efficiency (on/off)
            return 1.0
        else:  # linear
            return 0.3
    
    def calculate_carbon_footprint(self) -> Dict:
        """Calculate infrastructure carbon footprint"""
        
        total_carbon = 0
        component_impacts = {}
        
        for name, comp_data in self.components.items():
            component = comp_data['component']
            
            # Power consumption model
            power_draw = self.energy_model.calculate_power_draw(
                component.resource_type,
                comp_data['current_state']
            )
            
            # Carbon intensity (region-specific)
            carbon_intensity = self.get_carbon_intensity()  # kg CO2/kWh
            
            # Hours per month
            hours = 730
            
            carbon = power_draw * carbon_intensity * hours
            total_carbon += carbon
            component_impacts[name] = carbon
        
        return {
            'total_monthly_carbon_kg': total_carbon,
            'component_impacts': component_impacts,
            'carbon_per_dollar': total_carbon / self.calculate_monthly_cost(),
            'recommendations': self.generate_carbon_reduction_recommendations()
        }
```

### Terraform Module Optimization
```hcl
# Optimized Terraform Module with Physics-Based Resource Scheduling
variable "workload_characteristics" {
  type = object({
    base_capacity      = number
    peak_capacity      = number
    min_capacity       = number
    max_capacity       = number
    scaling_threshold  = number
    cooldown_period    = number
  })
  default = {
    base_capacity  = 10
    peak_capacity  = 100
    min_capacity   = 5
    max_capacity   = 150
    scaling_threshold = 70
    cooldown_period = 300
  }
}

resource "aws_autoscaling_group" "optimized" {
  name                = "physics-optimized-asg"
  min_size            = var.workload_characteristics.min_capacity
  max_size            = var.workload_characteristics.max_capacity
  desired_capacity    = var.workload_characteristics.base_capacity
  
  # Physics-inspired predictive scaling
  dynamic "instance_refresh" {
    for_each = [var.workload_characteristics]
    content {
      strategy = "Rolling"
      preferences {
        instance_warmup        = 300
        min_healthy_percentage = 90
        checkpoint_delay       = 600
        instance_termination   = "Default"
      }
      trigger {
        percentage_alarm = 80
        count_alarm      = 5
      }
    }
  }
  
  # Mixed instances policy for cost optimization
  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = var.workload_characteristics.base_capacity
      on_demand_percentage_above_base_capacity = 20
      spot_allocation_strategy                 = "capacity-optimized"
      spot_instance_pools                      = 3
    }
    
    launch_template {
      launch_templateSpecification {
        launch_template_id = aws_launch_template.main.id
        version            = "$Latest"
      }
      
      override {
        instance_type   = ["m6i.xlarge", "m5.xlarge", "m5a.xlarge"]
        weighted_capacity = 2
      }
    }
  }
  
  # Tag for cost allocation
  tag {
    key                 = "CostCenter"
    value               = "physics-optimized"
    propagate_at_launch = true
  }
  
  # Health check with fast failover
  health_check_type = "ELB"
  health_check_grace_period = 300
  
  # Lifecycle hooks for zero-downtime deployments
  lifecycle {
    create_before_destroy = true
    ignore_changes        = [desired_capacity]
  }
}

# Cost-optimized storage with intelligent tiering
resource "aws_s3_bucket" "optimized" {
  bucket = "physics-optimized-storage"
  
  lifecycle_rule {
    id      = "intelligent-tiering"
    enabled = true
    
    transition {
      days          = 30
      storage_class = "INTELLIGENT_TIERING"
    }
    
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    
    noncurrent_version_expiration {
      noncurrent_days = 365
    }
  }
  
  # Analytics for cost optimization
  analytics_configuration {
    id = "cost-analysis"
    storage_class_analysis {
      data_export {
        destination {
          s3_bucket_destination {
            bucket_arn = aws_s3_bucket.analytics.arn
            format     = "CSV"
          }
        }
      }
    }
  }
}
```

## 📊 Cost Optimization Dashboard

### Infrastructure Metrics
```javascript
const InfrastructureDashboard = {
  costMetrics: {
    total_monthly: 125000,
    compute: 45000,
    storage: 15000,
    network: 25000,
    database: 20000,
    other: 20000,
    
    trends: {
      compute_trend: "+5%",
      storage_trend: "-8%",
      network_trend: "+12%",
      database_trend: "+3%"
    },
    
    savings: {
      reserved_instances: 15000,
      spot_usage: 25000,
      right_sizing: 35000,
      storage_tiering: 8000
    }
  },
  
  performanceMetrics: {
    availability: 99.95,
    latency_p50: 12,
    latency_p99: 85,
    throughput_gbps: 250,
    error_rate: 0.001
  },
  
  resourceMetrics: {
    cpu_utilization: 67,
    memory_utilization: 72,
    storage_utilization: 45,
    network_utilization: 35,
    database_connections: 750
  },
  
  generateOptimizationInsights: function() {
    const insights = [];
    
    // Cost optimization
    if (this.costMetrics.total_monthly > 100000) {
      insights.push({
        type: 'cost',
        level: 'warning',
        message: `Monthly cost at $${this.costMetrics.total_monthly.toLocaleString()}`,
        recommendations: [
          'Increase spot instance usage',
          'Right-size underutilized resources',
          'Implement storage tiering'
        ],
        potential_savings: '$25,000/month'
      });
    }
    
    // Resource optimization
    if (this.resourceMetrics.cpu_utilization < 50) {
      insights.push({
        type: 'resource',
        level: 'info',
        message: `Low CPU utilization: ${this.resourceMetrics.cpu_utilization}%`,
        recommendations: [
          'Consolidate workloads',
          'Right-size instance types',
          'Implement bin packing'
        ],
        potential_savings: '$10,000/month'
      });
    }
    
    // Performance optimization
    if (this.performanceMetrics.latency_p99 > 100) {
      insights.push({
        type: 'performance',
        level: 'medium',
        message: `High P99 latency: ${this.performanceMetrics.latency_p99}ms`,
        recommendations: [
          'Add caching layer',
          'Optimize database queries',
          'Implement CDN'
        ],
        potential_improvement: '-40% latency'
      });
    }
    
    return insights;
  },
  
  predictResourceNeeds: function() {
    const growthRate = 1.15; // 15% monthly growth
    
    return {
      projected_monthly_cost: this.costMetrics.total_monthly * growthRate,
      recommended_reservations: {
        compute: 'Reserve 50% of current',
        database: 'Reserve 70% of current',
        storage: 'No reservation needed'
      },
      scaling_recommendations: this.generateScalingRecommendations(growthRate),
      cost_optimization_plan: {
        immediate: ['Right-size 10 underutilized instances'],
        short_term: ['Migrate to spot for stateless workloads'],
        long_term: ['Implement container optimization']
      }
    };
  }
};
```

## 🎯 Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Terraform setup and organization
- [ ] Module development standards
- [ ] State management configuration
- [ ] CI/CD pipeline setup

### Phase 2: Intelligence (Week 3-4)
- [ ] Advanced module patterns
- [ ] Policy as code implementation
- [ ] Cost optimization automation
- [ ] GitOps workflow establishment

### Phase 3: Production (Week 5-6)
- [ ] Multi-environment management
- [ ] Disaster recovery automation
- [ ] Performance optimization
- [ ] Security hardening

## 📊 Success Metrics

### IaC Excellence
```yaml
infrastructure:
  automation_coverage: "> 95%"
  deployment_frequency: "> 100/day"
  change_failure_rate: "< 5%"
  mean_time_to_recovery: "< 15 minutes"
  
cost_efficiency:
  monthly_savings: "> 30%"
  reserved_coverage: "> 70%"
  spot_utilization: "> 40%"
  waste_percentage: "< 5%"
  
reliability:
  availability: "> 99.95%"
  incident_rate: "< 2/month"
  rollback_success: "> 99%"
  drift_detection: "100%"
```

---

*Build and manage infrastructure with physics-inspired optimization and automation.* 🏗️✨