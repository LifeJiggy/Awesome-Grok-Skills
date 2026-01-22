"""
Infrastructure as Code Pipeline
Terraform and cloud infrastructure automation
"""

import yaml
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class InfrastructureConfig:
    cloud_provider: str
    region: str
    environment: str
    tags: Dict = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = {"environment": self.environment}


class TerraformGenerator:
    """Generate Terraform configurations"""
    
    def __init__(self):
        self.providers = {
            "aws": {
                "source": "hashicorp/aws",
                "version": "~> 5.0"
            },
            "gcp": {
                "source": "hashicorp/google",
                "version": "~> 4.0"
            },
            "azure": {
                "source": "hashicorp/azurerm",
                "version": "~> 3.0"
            }
        }
    
    def generate_provider(self, config: InfrastructureConfig) -> str:
        """Generate provider configuration"""
        provider = self.providers.get(config.cloud_provider, {})
        return f'''terraform {{
  required_providers {{
    {config.cloud_provider} = {{
      source  = "{provider.get("source", "unknown/unknown")}"
      version = "{provider.get("version", "~> 1.0")}"
    }}
  }}
  
  backend "s3" {{
    bucket = "{config.environment}-terraform-state"
    key    = "infrastructure.tfstate"
    region = "{config.region}"
  }}
}}
'''
    
    def generate_vpc(self, 
                     cidr: str = "10.0.0.0/16",
                     subnets: List[Dict] = None) -> str:
        """Generate VPC configuration"""
        subnet_configs = ""
        if subnets:
            for i, subnet in enumerate(subnets):
                subnet_configs += f'''
  subnet {{
    name             = "{subnet.get("name", f"subnet-{i}")}"
    cidr_block       = "{subnet.get("cidr", f"10.0.{i}.0/24")}"
    availability_zone = "{subnet.get("az", "us-east-1a")}"
  }}
'''
        
        return f'''resource "aws_vpc" "main" {{
  cidr_block           = "{cidr}"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {{
    Name        = "main-vpc"
    Environment = "production"
  }}
}}{subnet_configs}
'''
    
    def generate_eks(self, 
                     cluster_name: str,
                     node_groups: List[Dict]) -> str:
        """Generate EKS cluster configuration"""
        ng_configs = ""
        for ng in node_groups:
            ng_configs += f'''
  node_group {{
    name            = "{ng.get("name", "default")}"
    instance_types  = {ng.get("instance_types", ["t3.medium"])}
    desired_size   = {ng.get("desired", 2)}
    max_size        = {ng.get("max", 5)}
    min_size        = {ng.get("min", 1)}
  }}
'''
        
        return f'''resource "aws_eks_cluster" "main" {{
  name     = "{cluster_name}"
  role_arn = aws_iam_role.eks_cluster.arn
  
  vpc_config {{
    subnet_ids = aws_subnet.public[*].id
  }}
  
  enabled_cluster_log_types = ["api", "audit"]
  
  depends_on = [aws_iam_role_policy_attachment.eks_cluster]
}}

resource "aws_eks_node_group" "main" {{
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "main-nodes"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = aws_subnet.private[*].id{ng_configs}
}}
'''


class K8sManifestGenerator:
    """Generate Kubernetes manifests"""
    
    def __init__(self):
        self.ingress_controller = "nginx"
    
    def generate_deployment(self,
                           name: str,
                           image: str,
                           replicas: int = 3,
                           ports: List[int] = [80]) -> str:
        """Generate Kubernetes deployment"""
        ports_yaml = "\n".join([f'''      - containerPort: {p}''' for p in ports])
        
        return f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
  labels:
    app: {name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
      - name: {name}
        image: {image}
        ports:
{ports_yaml}
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
'''
    
    def generate_service(self,
                        name: str,
                        port: int = 80,
                        target_port: int = 80) -> str:
        """Generate Kubernetes service"""
        return f'''apiVersion: v1
kind: Service
metadata:
  name: {name}
spec:
  type: ClusterIP
  selector:
    app: {name}
  ports:
  - port: {port}
    targetPort: {target_port}
'''
    
    def generate_ingress(self, 
                        name: str,
                        host: str,
                        service_name: str,
                        service_port: int = 80) -> str:
        """Generate Kubernetes ingress"""
        return f'''apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {name}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: {host}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {service_name}
            port:
              number: {service_port}
'''


class CostOptimizer:
    """Cloud cost optimization"""
    
    def __init__(self):
        self.recommendations = []
    
    def analyze_cost(self, resources: List[Dict]) -> Dict:
        """Analyze cloud costs and suggest optimizations"""
        total_cost = 0
        by_service = {}
        recommendations = []
        
        for resource in resources:
            cost = self._estimate_cost(resource)
            total_cost += cost
            service = resource.get("service", "other")
            by_service[service] = by_service.get(service, 0) + cost
            
            if resource.get("type") == "instance":
                if resource.get("size") in ["xlarge", "2xlarge"]:
                    recommendations.append({
                        "resource": resource.get("name"),
                        "recommendation": "Right-size instance",
                        "potential_savings": cost * 0.3
                    })
        
        return {
            "total_monthly_cost": total_cost,
            "by_service": by_service,
            "recommendations": recommendations,
            "potential_monthly_savings": sum(r["potential_savings"] for r in recommendations)
        }
    
    def _estimate_cost(self, resource: Dict) -> float:
        """Estimate monthly cost for resource"""
        rates = {
            "instance": 0.10,
            "storage": 0.02,
            "database": 0.15,
            "network": 0.05
        }
        return rates.get(resource.get("type"), 0.05)


if __name__ == "__main__":
    tf_gen = TerraformGenerator()
    k8s_gen = K8sManifestGenerator()
    cost_optimizer = CostOptimizer()
    
    config = InfrastructureConfig(
        cloud_provider="aws",
        region="us-east-1",
        environment="production"
    )
    
    provider = tf_gen.generate_provider(config)
    vpc = tf_gen.generate_vpc()
    deployment = k8s_gen.generate_deployment("web", "nginx:latest")
    
    resources = [
        {"name": "web-1", "type": "instance", "size": "xlarge", "hours": 720},
        {"name": "db-1", "type": "database", "size": "large", "hours": 720},
        {"name": "storage-1", "type": "storage", "size": "100gb", "hours": 720}
    ]
    
    cost_analysis = cost_optimizer.analyze_cost(resources)
    
    print(f"Total monthly cost: ${cost_analysis['total_monthly_cost']:.2f}")
    print(f"Potential savings: ${cost_analysis['potential_monthly_savings']:.2f}")
    print(f"Recommendations: {len(cost_analysis['recommendations'])}")
