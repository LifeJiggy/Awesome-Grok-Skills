# Load Balancing

## Overview

Load balancing distributes network traffic or computational workloads across multiple servers to ensure optimal resource utilization, maximize throughput, minimize response time, and prevent overload on any single resource. This skill covers hardware and software load balancing solutions, algorithm selection, health checking strategies, and session persistence requirements. Load balancers serve as critical infrastructure components that directly impact application availability, performance, and scalability.

## Core Capabilities

Load balancing algorithms determine how traffic is distributed across backend servers, with options including round robin, weighted round robin, least connections, weighted least connections, IP hash, and URL-based routing. Health checking ensures traffic only routes to healthy servers through TCP, HTTP, and custom health probe configurations. SSL/TLS termination offloads encryption processing from backend servers and simplifies certificate management. Session persistence (sticky sessions) maintains user sessions on specific servers when required by application architecture.

Global server load balancing extends traffic distribution across geographic regions for disaster recovery and optimal user experience. Auto-scaling integration dynamically adjusts backend capacity based on traffic demand. Layer 4 (TCP/UDP) and Layer 7 (HTTP/HTTPS) load balancing serve different use cases and protocol requirements. Traffic management features include rate limiting, circuit breaking, and request queuing for graceful degradation under load.

## Usage Examples

```python
from load_balancer_skill import LoadBalancer, HealthChecker, TrafficManager, AutoScaler

# Configure application load balancer
lb = LoadBalancer(
    type="application",  # layer 7
    vendor="aws",  # or "nginx", "f5", "ha-proxy"
    region="us-east-1"
)

# Create target group for web servers
target_group = lb.create_target_group(
    name="web-servers-tg",
    protocol="HTTP",
    port=80,
    vpc_id="vpc-12345678",
    health_check_config={
        "path": "/health",
        "protocol": "HTTP",
        "interval_seconds": 30,
        "timeout_seconds": 5,
        "healthy_threshold_count": 2,
        "unhealthy_threshold_count": 3,
        "matcher": {"http_codes": ["200-299"]}
    },
    attributes={
        "deregistration_delay_seconds": 30,
        "stickiness_enabled": True,
        "stickiness_type": "lb_cookie",
        "stickiness_duration_seconds": 86400
    }
)
print(f"Target Group ARN: {target_group.arn}")

# Register backend servers
servers = [
    {"id": "i-001", "ip": "10.0.1.10", "port": 80, "weight": 100},
    {"id": "i-002", "ip": "10.0.1.11", "port": 80, "weight": 100},
    {"id": "i-003", "ip": "10.0.1.12", "port": 80, "weight": 100},
    {"id": "i-004", "ip": "10.0.1.13", "port": 80, "weight": 50}  # Lower weight
]

for server in servers:
    lb.register_targets(
        target_group_arn=target_group.arn,
        targets=[{"id": server["id"], "port": server["port"]}]
    )

# Create load balancer with routing rules
load_balancer = lb.create_load_balancer(
    name="production-alb",
    scheme="internet-facing",
    security_groups=["sg-0123456789abcdef0"],
    subnets=["subnet-12345678", "subnet-87654321"],
    ip_address_type="ipv4",
    listeners=[
        {
            "protocol": "HTTPS",
            "port": 443,
            "certificate_arn": "arn:aws:acm:us-east-1:123456789:certificate/xxx",
            "default_actions": [{
                "type": "forward",
                "target_group_arn": target_group.arn
            }]
        },
        {
            "protocol": "HTTP",
            "port": 80,
            "default_actions": [{
                "type": "redirect",
                "protocol": "HTTPS",
                "port": "443",
                "status_code": "HTTP_301"
            }]
        }
    ]
)
print(f"Load Balancer DNS: {load_balancer.dns_name}")

# Configure path-based routing
lb.add_rule(
    listener_arn=load_balancer.listeners[0],
    priority=100,
    conditions=[{"field": "path-pattern", "values": ["/api/*", "/v1/*"]}],
    actions=[{
        "type": "forward",
        "target_group_arn": target_group.arn
    }]
)

# Configure host-based routing for multi-tenant
lb.add_rule(
    listener_arn=load_balancer.listeners[0],
    priority=200,
    conditions=[{"field": "host-header", "values": ["tenant1.example.com", "tenant2.example.com"]}],
    actions=[{
        "type": "forward",
        "target_group_arn": target_group.arn
    }]
)

# Configure health checker
health_checker = HealthChecker(
    protocol="tcp",
    endpoint="10.0.1.10:80"
)

# Check health of individual servers
health_status = health_checker.check_all(
    targets=servers,
    check_types=["tcp", "http"],
    http_path="/health"
)
print("Server Health Status:")
for server, status in health_status.items():
    print(f"  {server['ip']}: {status['overall']} ({status['details']})")

# Configure traffic management
traffic_manager = TrafficManager(
    load_balancer_arn=load_balancer.arn
)

# Set up weighted target group for canary deployment
traffic_manager.configure_weighted_routing(
    target_groups=[
        {"arn": target_group.arn, "weight": 90},  # Current version
        {"arn": "arn:new-version-tg", "weight": 10}  # Canary version
    ]
)

# Configure rate limiting
traffic_manager.set_rate_limit(
    rule_name="api-rate-limit",
    average=1000,
    burst=2000,
    conditions=[{"field": "path-pattern", "values": ["/api/*"]}]
)

# Configure circuit breaker
traffic_manager.set_circuit_breaker(
    threshold=5,  # 5 consecutive failures
    timeout_seconds=30  # 30 second open period
)

# Set up auto-scaling integration
auto_scaler = AutoScaler(
    cloud_provider="aws",
    load_balancer_arn=load_balancer.arn,
    target_group_arn=target_group.arn
)

# Create auto-scaling group
asg = auto_scaler.create_auto_scaling_group(
    name="web-servers-asg",
    min_size=2,
    max_size=20,
    desired_capacity=4,
    launch_config={
        "image_id": "ami-0123456789",
        "instance_type": "t3.medium",
        "key_name": "production-key",
        "security_groups": ["sg-0123456789abcdef0"],
        "user_data": "#!/bin/bash\napt-get update\napt-get install -y nginx"
    },
    scaling_policies=[
        {
            "name": "scale-out-on-cpu",
            "metric": "CPUUtilization",
            "threshold": 70,
            "adjustment": 2,
            "cooldown_seconds": 300
        },
        {
            "name": "scale-in-on-cpu",
            "metric": "CPUUtilization",
            "threshold": 30,
            "adjustment": -1,
            "cooldown_seconds": 300
        },
        {
            "name": "scale-on-request-count",
            "metric": "RequestCountPerTarget",
            "threshold": 1000,
            "adjustment": 2,
            "cooldown_seconds": 300
        }
    ]
)
print(f"Auto Scaling Group ARN: {asg.arn}")

# Get load balancer metrics
metrics = lb.get_metrics(
    metric_names=["RequestCount", "Latency", "HTTPCode_ELB_5XX", "HealthyHostCount"],
    period=300,
    start_time="PT1H"
)
print("Load Balancer Metrics:")
for metric, values in metrics.items():
    print(f"  {metric}: Average={values['average']}, Max={values['max']}")
```

## Best Practices

Choose the appropriate load balancing type based on application needs, using Layer 7 for HTTP/HTTPS applications that benefit from content-based routing, and Layer 4 for TCP/UDP protocols or when minimal latency is critical. Implement health checks that accurately reflect application readiness, not just TCP connectivity, including application-level checks where possible. Configure appropriate timeouts and connection draining to allow graceful server removal without disrupting active user sessions.

Plan for high availability with multi-AZ deployment to survive data center failures. Use weighted routing for gradual traffic shifting during deployments, enabling canary releases and blue-green deployments. Monitor load balancer metrics continuously, setting up alerts for increased error rates, latency degradation, or healthy host count drops. Test failover procedures regularly to ensure they work correctly.

## Related Skills

- Network Engineering (infrastructure design)
- Site Reliability Engineering (availability monitoring)
- Cloud Architecture (cloud load balancing services)
- Performance Testing (load testing methodologies)

## Use Cases

Web application load balancing distributes user traffic across multiple web servers for horizontal scalability and high availability. API gateway load balancing routes requests to microservice backends based on URL paths, headers, or method types. Database read replica load balancing distributes read queries across replicas while directing writes to the primary. Global load balancing routes users to the nearest healthy data center for optimal performance and disaster recovery.
