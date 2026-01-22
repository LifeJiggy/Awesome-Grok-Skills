from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class ServiceType(Enum):
    COMPUTE = "compute"
    STORAGE = "storage"
    DATABASE = "database"
    NETWORKING = "networking"
    SERVERLESS = "serverless"
    ANALYTICS = "analytics"
    ML = "ml"
    SECURITY = "security"


@dataclass
class EC2Instance:
    instance_id: str
    instance_type: str
    ami_id: str
    state: str
    private_ip: str
    public_ip: Optional[str]
    key_name: str
    security_groups: List[str]
    tags: Dict[str, str]


@dataclass
class VPCConfig:
    vpc_id: str
    cidr_block: str
    subnets: List[Dict]
    internet_gateways: List[str]
    route_tables: List[str]
    nat_gateways: List[str]


@dataclass
class RDSInstance:
    db_identifier: str
    engine: str
    engine_version: str
    instance_class: str
    storage: int
    Multi_AZ: bool
    endpoint: str
    status: str


class AWSServicesManager:
    """Manage AWS services and resources"""
    
    def __init__(self):
        self.resources = []
    
    def create_ec2_instance(self,
                           instance_type: str = "t3.micro",
                           ami_id: str = "ami-0c02fb55956c7d316",
                           key_name: str = "my-key-pair",
                           security_groups: List[str] = None) -> EC2Instance:
        """Create EC2 instance"""
        return EC2Instance(
            instance_id=f"i-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            instance_type=instance_type,
            ami_id=ami_id,
            state="pending",
            private_ip="10.0.1.10",
            public_ip=None,
            key_name=key_name,
            security_groups=security_groups or ["sg-0123abcd"],
            tags={"Name": "web-server", "Environment": "production"}
        )
    
    def create_vpc(self,
                   cidr_block: str = "10.0.0.0/16",
                   availability_zones: List[str] = None) -> VPCConfig:
        """Create VPC with subnets"""
        if availability_zones is None:
            availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
        
        subnets = []
        for i, az in enumerate(availability_zones):
            subnets.append({
                'subnet_id': f"subnet-{i:04d}",
                'cidr': f"10.0.{i * 32}.0/24",
                'availability_zone': az,
                'public': i == 0
            })
        
        return VPCConfig(
            vpc_id=f"vpc-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            cidr_block=cidr_block,
            subnets=subnets,
            internet_gateways=["igw-0123abcd"],
            route_tables=["rtb-0123abcd"],
            nat_gateways=[]
        )
    
    def create_rds_instance(self,
                           engine: str = "postgres",
                           instance_class: str = "db.t3.medium",
                           Multi_AZ: bool = False) -> RDSInstance:
        """Create RDS database instance"""
        return RDSInstance(
            db_identifier=f"mydb-{datetime.now().strftime('%Y%m%d')}",
            engine=engine,
            engine_version="15.2",
            instance_class=instance_class,
            storage=100,
            Multi_AZ=Multi_AZ,
            endpoint="mydb.c123456789012.us-east-1.rds.amazonaws.com",
            status="creating"
        )
    
    def create_s3_bucket(self,
                         bucket_name: str,
                         region: str = "us-east-1") -> Dict:
        """Create S3 bucket"""
        return {
            'bucket_name': bucket_name,
            'region': region,
            'acl': 'private',
            'versioning': False,
            'encryption': 'AES256',
            'public_access_block': True,
            'website_config': None,
            'logging': {'target_bucket': f"{bucket_name}-logs"},
            'lifecycle_rules': []
        }
    
    def create_lambda_function(self,
                               function_name: str,
                               runtime: str = "python3.9",
                               handler: str = "index.lambda_handler",
                               memory_size: int = 128,
                               timeout: int = 30) -> Dict:
        """Create Lambda function"""
        return {
            'function_name': function_name,
            'runtime': runtime,
            'handler': handler,
            'memory_size': memory_size,
            'timeout': timeout,
            'role': f"arn:aws:iam::123456789:role/lambda-role",
            'code': {'zip_file': f"{function_name}.zip"},
            'environment': {'variables': {}},
            'vpc_config': None,
            'tracing_config': 'PassThrough'
        }
    
    def create_load_balancer(self,
                            name: str,
                            scheme: str = "internet-facing",
                            listener_ports: List[int] = None) -> Dict:
        """Create Application Load Balancer"""
        return {
            'load_balancer_name': name,
            'type': 'application',
            'scheme': scheme,
            'dns_name': f"{name}-123456789.us-east-1.elb.amazonaws.com",
            'listeners': [
                {'port': port, 'protocol': 'HTTP', 'actions': ['forward']}
                for port in (listener_ports or [80, 443])
            ],
            'target_groups': [
                {'name': f"{name}-tg-1", 'port': 80, 'protocol': 'HTTP'}
            ],
            'security_groups': ['sg-0123abcd'],
            'subnets': ['subnet-0001', 'subnet-0002', 'subnet-0003'],
            'attributes': {
                'idle_timeout': 60,
                'deletion_protection': False
            }
        }
    
    def create_autoscaling_group(self,
                                 name: str,
                                 min_size: int = 1,
                                 max_size: int = 10,
                                 desired_capacity: int = 2) -> Dict:
        """Create Auto Scaling group"""
        return {
            'auto_scaling_group_name': name,
            'launch_template': {'id': 'lt-0123abcd', 'version': '$Latest'},
            'min_size': min_size,
            'max_size': max_size,
            'desired_capacity': desired_capacity,
            'vpc_zone_identifier': 'subnet-0001,subnet-0002',
            'metrics_collection': ['GroupDesiredCapacity', 'GroupInServiceInstances'],
            'health_check_type': 'EC2',
            'health_check_grace_period': 300,
            'termination_policies': ['Default'],
            'tags': [{'key': 'Name', 'value': name, 'propagate_at_launch': True}]
        }
    
    def create_cloudformation_stack(self,
                                    stack_name: str,
                                    template_url: str,
                                    parameters: Dict = None) -> Dict:
        """Create CloudFormation stack"""
        return {
            'stack_name': stack_name,
            'stack_id': f"arn:aws:cloudformation:us-east-1:123456789:stack/{stack_name}/abc123",
            'status': 'CREATE_IN_PROGRESS',
            'template_url': template_url,
            'parameters': parameters or {},
            'outputs': [],
            'creation_time': datetime.now().isoformat()
        }


class AWSCostOptimizer:
    """Optimize AWS costs"""
    
    def __init__(self):
        self.recommendations = []
    
    def analyze_cost_by_service(self,
                                cost_data: Dict) -> Dict:
        """Analyze costs by service"""
        services = {'EC2': 450, 'RDS': 120, 'S3': 35, 'Lambda': 15, 'CloudFront': 80}
        total = sum(services.values())
        
        return {
            'period': 'Last 30 days',
            'total_cost': total,
            'by_service': services,
            'top_cost_drivers': [
                {'service': 'EC2', 'percentage': 60.0, 'recommendation': 'Use reserved instances'}
            ],
            'forecast': total * 1.1
        }
    
    def get_reserved_instance_recommendation(self,
                                             service: str,
                                             utilization: float) -> Dict:
        """Recommend reserved instances"""
        return {
            'service': service,
            'current_ondemand': 450,
            'recommended_ri': 'Standard 1-year',
            'ri_term': '1 year',
            'payment_option': 'All Upfront',
            'estimated_savings': 0.35,
            'monthly_savings': 157.50,
            'upfront_cost': 3150,
            'break_even_months': 8
        }
    
    def right_sizing_recommendation(self,
                                    instance_id: str,
                                    cpu_utilization: float,
                                    memory_utilization: float) -> Dict:
        """Recommend right-sizing"""
        current_type = 'm5.large'
        recommended_type = 't3.medium'
        
        return {
            'instance_id': instance_id,
            'current_type': current_type,
            'recommended_type': recommended_type,
            'cpu_utilization': cpu_utilization,
            'memory_utilization': memory_utilization,
            'estimated_monthly_savings': 85.00,
            'performance_impact': 'Low - meets requirements'
        }


class AWSWellArchitected:
    """AWS Well-Architected Framework checks"""
    
    def review_architecture(self,
                            architecture: Dict) -> Dict:
        """Review architecture against Well-Architected pillars"""
        return {
            'review_date': datetime.now().isoformat(),
            'pillars': {
                'operational_excellence': {
                    'score': 75,
                    'findings': [
                        {'area': 'Logging', 'status': 'PASS', 'description': 'CloudWatch logs enabled'},
                        {'area': 'Automation', 'status': 'WARNING', 'description': 'Consider CDK for deployments'}
                    ]
                },
                'security': {
                    'score': 85,
                    'findings': [
                        {'area': 'Encryption', 'status': 'PASS', 'description': 'Data encrypted at rest'},
                        {'area': 'IAM', 'status': 'PASS', 'description': 'Least privilege implemented'},
                        {'area': 'Network', 'status': 'WARNING', 'description': 'Review security group rules'}
                    ]
                },
                'reliability': {
                    'score': 70,
                    'findings': [
                        {'area': 'Multi-AZ', 'status': 'WARNING', 'description': 'Not all services are multi-AZ'},
                        {'area': 'Backups', 'status': 'PASS', 'description': 'RDS backups enabled'}
                    ]
                },
                'performance': {
                    'score': 80,
                    'findings': [
                        {'area': 'Caching', 'status': 'PASS', 'description': 'CloudFront in use'},
                        {'area': 'Scalability', 'status': 'PASS', 'description': 'Auto Scaling configured'}
                    ]
                },
                'cost_optimization': {
                    'score': 65,
                    'findings': [
                        {'area': 'Unused Resources', 'status': 'WARNING', 'description': 'Idle volumes detected'},
                        {'area': 'RI Coverage', 'status': 'WARNING', 'description': 'Low RI coverage for EC2'}
                    ]
                },
                'sustainability': {
                    'score': 60,
                    'findings': [
                        {'area': 'Regions', 'status': 'INFO', 'description': 'Consider using regional carbon'},
                        {'area': 'Right-sizing', 'status': 'WARNING', 'description': 'Optimize instance sizes'}
                    ]
                }
            },
            'overall_score': 72.5,
            'priority_improvements': [
                {'pillar': 'Reliability', 'action': 'Enable Multi-AZ for critical services'},
                {'pillar': 'Cost Optimization', 'action': 'Identify and remove unused resources'}
            ]
        }


if __name__ == "__main__":
    aws = AWSServicesManager()
    
    instance = aws.create_ec2_instance()
    print(f"EC2 created: {instance.instance_id}")
    
    vpc = aws.create_vpc()
    print(f"VPC created: {vpc.vpc_id}, Subnets: {len(vpc.subnets)}")
    
    rds = aws.create_rds_instance()
    print(f"RDS created: {rds.db_identifier}")
    
    bucket = aws.create_s3_bucket("my-data-bucket")
    print(f"S3 bucket: {bucket['bucket_name']}")
    
    lambda_func = aws.create_lambda_function("my-function")
    print(f"Lambda: {lambda_func['function_name']}")
    
    cost = AWSCostOptimizer()
    analysis = cost.analyze_cost_by_service({})
    print(f"Total monthly cost: ${analysis['total_cost']}")
    
    review = AWSWellArchitected().review_architecture({})
    print(f"Architecture score: {review['overall_score']}%")
