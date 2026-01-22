from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class LoadBalancerType(Enum):
    APPLICATION = "Application (Layer 7)"
    NETWORK = "Network (Layer 4)"
    GLOBAL_SERVER = "Global Server (GSLB)"
    CONTAINER = "Container (Layer 7)"


class Algorithm(Enum):
    ROUND_ROBIN = "round-robin"
    LEAST_CONNECTIONS = "least-connections"
    WEIGHTED = "weighted"
    IP_HASH = "ip-hash"
    RANDOM = "random"
    ADAPTIVE = "adaptive"


class HealthCheckType(Enum):
    TCP = "TCP"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    ICMP = "ICMP"


@dataclass
class LoadBalancerConfig:
    lb_id: str
    name: str
    lb_type: LoadBalancerType
    algorithm: Algorithm
    vip: str
    port: int
    servers: List[Dict]


class LoadBalancingManager:
    """Manage load balancing configuration"""
    
    def __init__(self):
        self.lbs = []
    
    def create_load_balancer(self,
                             name: str,
                             lb_type: LoadBalancerType = LoadBalancerType.APPLICATION,
                             algorithm: Algorithm = Algorithm.ROUND_ROBIN) -> LoadBalancerConfig:
        """Create load balancer configuration"""
        return LoadBalancerConfig(
            lb_id=f"LB-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=name,
            lb_type=lb_type,
            algorithm=algorithm,
            vip="10.0.0.100",
            port=443,
            servers=[]
        )
    
    def add_backend_servers(self,
                           lb: LoadBalancerConfig,
                           servers: List[Dict]) -> LoadBalancerConfig:
        """Add backend servers to load balancer"""
        lb.servers = servers
        return lb
    
    def configure_health_checks(self,
                                lb: LoadBalancerConfig,
                                check_type: HealthCheckType,
                                path: str = "/health",
                                interval: int = 30,
                                timeout: int = 10,
                                unhealthy_threshold: int = 3) -> Dict:
        """Configure health check settings"""
        return {
            'load_balancer': lb.name,
            'health_check': {
                'type': check_type.value,
                'endpoint': path if check_type in [HealthCheckType.HTTP, HealthCheckType.HTTPS] else 'N/A',
                'interval_seconds': interval,
                'timeout_seconds': timeout,
                'unhealthy_threshold': unhealthy_threshold,
                'healthy_threshold': 2,
                'expected_codes': [200] if check_type in [HealthCheckType.HTTP, HealthCheckType.HTTPS] else 'N/A'
            },
            'actions_on_failure': [
                'Mark server unhealthy',
                'Stop sending traffic',
                'Log event',
                'Send alert'
            ]
        }
    
    def configure_algorithm(self,
                            lb: LoadBalancerConfig,
                            algorithm: Algorithm,
                            weights: Dict = None) -> Dict:
        """Configure load balancing algorithm"""
        return {
            'load_balancer': lb.name,
            'algorithm': algorithm.value,
            'configuration': {
                'round-robin': 'Distribute requests sequentially',
                'least-connections': 'Route to server with fewest active connections',
                'weighted': 'Route based on server weights',
                'ip-hash': 'Consistent hashing based on client IP',
                'random': 'Random server selection',
                'adaptive': 'Based on real-time server load'
            },
            'weights': weights if algorithm == Algorithm.WEIGHTED else 'N/A',
            'sticky_sessions': {
                'enabled': True if algorithm in [Algorithm.IP_HASH] else False,
                'type': 'Cookie-based' if lb.lb_type == LoadBalancerType.APPLICATION else 'Source IP'
            }
        }
    
    def configure_ssl_termination(self,
                                  lb: LoadBalancerConfig,
                                  cert_name: str) -> Dict:
        """Configure SSL/TLS termination"""
        return {
            'load_balancer': lb.name,
            'ssl_termination': {
                'enabled': True,
                'certificate': cert_name,
                'protocols': ['TLSv1.2', 'TLSv1.3'],
                'ciphers': 'Strong ciphers only',
                'hsts': {'enabled': True, 'max_age': 31536000}
            },
            'backend_encryption': {
                'enabled': True,
                'cert_verify': True
            }
        }
    
    def create_dns_gslb(self,
                       domain: str,
                       lb_servers: List[Dict]) -> Dict:
        """Create Global Server Load Balancing via DNS"""
        return {
            'domain': domain,
            'type': 'GSLB',
            'health_check': {
                'type': 'HTTP',
                'path': '/health',
                'interval': 30
            },
            'fallback': 'backup-loadbalancer.example.com',
            'lb_method': 'weighted_round_robin',
            'servers': [
                {
                    'name': 'Primary LB',
                    'address': '203.0.113.10',
                    'weight': 100,
                    'region': 'US-East',
                    'health': 'Healthy'
                },
                {
                    'name': 'Secondary LB',
                    'address': '203.0.113.20',
                    'weight': 50,
                    'region': 'US-West',
                    'health': 'Healthy'
                }
            ],
            'dns_ttl': 60,
            'geo_routing': {
                'US': ['Primary LB', 'Secondary LB'],
                'EU': ['Secondary LB'],
                'APAC': ['Tertiary LB']
            }
        }
    
    def configure_autoscaling(self,
                             lb: LoadBalancerConfig,
                             min_servers: int = 2,
                             max_servers: int = 10,
                             scale_up_threshold: int = 70,
                             scale_down_threshold: int = 30) -> Dict:
        """Configure autoscaling for backend servers"""
        return {
            'load_balancer': lb.name,
            'autoscaling': {
                'enabled': True,
                'min_servers': min_servers,
                'max_servers': max_servers,
                'scale_up': {
                    'threshold_cpu': scale_up_threshold,
                    'threshold_memory': scale_up_threshold,
                    'cooldown_seconds': 300
                },
                'scale_down': {
                    'threshold_cpu': scale_down_threshold,
                    'threshold_memory': scale_down_threshold,
                    'cooldown_seconds': 600
                }
            },
            'metrics': ['CPU utilization', 'Memory utilization', 'Request count', 'Latency'],
            'scaling_actions': [
                'Add server from pool',
                'Remove server when cooldown expires'
            ]
        }
    
    def calculate_capacity(self,
                          current_rps: int,
                          avg_response_time_ms: float,
                          target_utilization: float = 0.7) -> Dict:
        """Calculate load balancer capacity requirements"""
        capacity_rps = current_rps / target_utilization
        
        return {
            'current_load': {
                'requests_per_second': current_rps,
                'avg_response_time_ms': avg_response_time_ms,
                'peak_rps': int(current_rps * 3)
            },
            'required_capacity': {
                'min_rps': int(capacity_rps),
                'recommended_rps': int(capacity_rps * 1.5),
                'burst_capacity': int(capacity_rps * 2)
            },
            'connection_limits': {
                'max_connections': int(capacity_rps * 100),
                'new_connections_per_second': int(capacity_rps * 10)
            },
            'bandwidth_requirements': {
                'current_mbps': current_rps * avg_response_time_ms / 1000 * 2,
                'required_mbps': capacity_rps * avg_response_time_ms / 1000 * 2,
                'burst_mbps': capacity_rps * 2 * avg_response_time_ms / 1000 * 2
            }
        }
    
    def optimize_performance(self,
                            lb: LoadBalancerConfig,
                            current_metrics: Dict) -> Dict:
        """Optimize load balancer performance"""
        return {
            'load_balancer': lb.name,
            'optimizations': [
                {
                    'area': 'Connection Handling',
                    'recommendation': 'Enable keep-alive connections',
                    'impact': 'Reduce latency by 15-20%'
                },
                {
                    'area': 'SSL/TLS',
                    'recommendation': 'Use TLS 1.3 and session tickets',
                    'impact': 'Reduce handshake overhead by 50%'
                },
                {
                    'area': 'Caching',
                    'recommendation': 'Enable response caching',
                    'impact': 'Reduce backend load by 30%'
                },
                {
                    'area': 'Compression',
                    'recommendation': 'Enable gzip compression',
                    'impact': 'Reduce bandwidth by 60%'
                },
                {
                    'area': 'Health Checks',
                    'recommendation': 'Optimize check interval',
                    'impact': 'Reduce false positives'
                }
            ],
            'current_metrics': current_metrics,
            'target_metrics': {
                'latency_reduction': '20%',
                'throughput_increase': '40%',
                'error_rate_reduction': '50%'
            }
        }
    
    def configure_session_persistence(self,
                                     lb: LoadBalancerConfig,
                                     persistence_type: str,
                                     cookie_name: str = "SESSIONID") -> Dict:
        """Configure session persistence (sticky sessions)"""
        return {
            'load_balancer': lb.name,
            'persistence': {
                'type': persistence_type,  # cookie, source-ip, header
                'cookie_name': cookie_name if persistence_type == 'cookie' else 'N/A',
                'cookie_attributes': {
                    'http_only': True,
                    'secure': True,
                    'same_site': 'Lax',
                    'max_age': 86400
                },
                'timeout': 3600,
                'methods': [
                    'Cookie insertion',
                    'Cookie rewrite',
                    'Cookie passive'
                ]
            },
            'considerations': [
                'May impact load distribution',
                'Session affinity can cause hotspots',
                'Consider application-level session storage'
            ]
        }
    
    def monitor_load_balancer(self,
                             lb: LoadBalancerConfig) -> Dict:
        """Monitor load balancer health and performance"""
        return {
            'load_balancer': lb.name,
            'health': {
                'status': 'Healthy',
                'uptime': '99.99%',
                'last_failure': '2024-01-10'
            },
            'traffic': {
                'requests_per_second': 5000,
                'bytes_in_mbps': 150,
                'bytes_out_mbps': 450,
                'active_connections': 25000
            },
            'backend_pool': {
                'total_servers': len(lb.servers),
                'healthy_servers': len([s for s in lb.servers if s.get('status') == 'Healthy']),
                'unhealthy_servers': 0
            },
            'performance': {
                'avg_latency_ms': 15,
                'p99_latency_ms': 45,
                'error_rate': 0.01
            },
            'alerts': [
                {'severity': 'Warning', 'message': 'CPU utilization 75%'},
                {'severity': 'Info', 'message': 'New server added to pool'}
            ]
        }
    
    def configure_ddos_protection(self,
                                  lb: LoadBalancerConfig) -> Dict:
        """Configure DDoS protection measures"""
        return {
            'load_balancer': lb.name,
            'protection_layers': [
                {
                    'layer': 'Network',
                    'measures': ['Syn cookies', 'Connection limits', 'Rate limiting']
                },
                {
                    'layer': 'Application',
                    'measures': ['WAF rules', 'Bot detection', 'Rate limiting']
                },
                {
                    'layer': 'DNS',
                    'measures': ['Query rate limiting', 'Response rate limiting']
                }
            ],
            'rate_limits': {
                'per_ip': '100 requests/second',
                'global': '10000 requests/second',
                'burst': '200 requests/second'
            },
            'geo_blocking': {
                'enabled': True,
                'blocked_regions': ['Known malicious countries']
            },
            'scrubbing_center': {
                'enabled': True,
                'capacity': '1 Tbps',
                'activation': 'Automatic'
            }
        }


class HAProxyConfiguration:
    """Generate HAProxy configuration"""
    
    def create_config(self,
                      frontend_name: str,
                      backends: List[Dict],
                      global_settings: Dict = None) -> str:
        """Generate HAProxy configuration file"""
        config = f'''global
    log 127.0.0.1 local0 info
    maxconn 50000
    tune.ssl.default-dh-param 2048
'''
        if global_settings:
            if global_settings.get('timeout'):
                config += f'''    timeout connect {global_settings['timeout']}s
    timeout client {global_settings['timeout']}s
    timeout server {global_settings['timeout']}s
'''
        
        config += '''
defaults
    log global
    mode http
    option httplog
    option dontlognull
    retries 3
'''
        
        config += f'''
frontend {frontend_name}
    bind *:80
    bind *:443 ssl crt /etc/ssl/private/cert.pem
    http-request redirect scheme https code 301 unless {{ ssl_fc }}
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk GET /health
    server web1 10.0.1.10:80 check
    server web2 10.0.1.11:80 check
    server web3 10.0.1.12:80 check backup
'''
        
        for backend in backends:
            config += f'''
frontend {backend['name']}
    bind *:{backend['port']}
    default_backend {backend['name']}_servers

backend {backend['name']}_servers
    balance {backend.get('algorithm', 'roundrobin')}
'''
            for server in backend.get('servers', []):
                config += f"    server {server['name']} {server['ip']}:{server['port']} check\n"
        
        return config


class NginxLoadBalancer:
    """Configure Nginx as load balancer"""
    
    def create_upstream(self,
                        name: str,
                        servers: List[Dict],
                        algorithm: str = "round-robin") -> str:
        """Generate Nginx upstream configuration"""
        config = f'upstream {name} {{\n'
        
        for server in servers:
            weight = server.get('weight', 1)
            backup = ' backup' if server.get('backup') else ''
            config += f'    server {server["ip"]}:{server["port"]} weight={weight}{backup};\n'
        
        config += '}\n'
        return config
    
    def create_proxy_config(self,
                            upstream_name: str,
                            domain: str) -> str:
        """Generate Nginx proxy configuration"""
        return f'''server {{
    listen 80;
    server_name {domain};
    return 301 https://$server_name$request_uri;
}}

server {{
    listen 443 ssl http2;
    server_name {domain};

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {{
        proxy_pass http://{upstream_name};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 90s;
    }}
}}
'''


if __name__ == "__main__":
    lb = LoadBalancingManager()
    
    load_balancer = lb.create_load_balancer(
        "Web-LB-1",
        LoadBalancerType.APPLICATION,
        Algorithm.LEAST_CONNECTIONS
    )
    print(f"Load Balancer: {load_balancer.name} ({load_balancer.lb_type.value})")
    
    load_balancer = lb.add_backend_servers(load_balancer, [
        {'name': 'web-1', 'ip': '10.0.1.10', 'port': 80, 'weight': 2, 'status': 'Healthy'},
        {'name': 'web-2', 'ip': '10.0.1.11', 'port': 80, 'weight': 1, 'status': 'Healthy'},
        {'name': 'web-3', 'ip': '10.0.1.12', 'port': 80, 'weight': 1, 'status': 'Healthy'}
    ])
    print(f"Backend servers: {len(load_balancer.servers)}")
    
    health = lb.configure_health_checks(
        load_balancer,
        HealthCheckType.HTTP,
        path="/health",
        interval=30
    )
    print(f"Health Check: {health['health_check']['type']} every {health['health_check']['interval_seconds']}s")
    
    algo = lb.configure_algorithm(load_balancer, Algorithm.WEIGHTED, {'web-1': 2, 'web-2': 1, 'web-3': 1})
    print(f"Algorithm: {algo['algorithm']} with weights configured")
    
    ssl = lb.configure_ssl_termination(load_balancer, "web-cert-2024")
    print(f"SSL: {ssl['ssl_termination']['protocols']} enabled")
    
    gslb = lb.create_dns_gslb("app.example.com", [])
    print(f"GSLB: {gslb['lb_method']} routing")
    
    auto = lb.configure_autoscaling(load_balancer, min_servers=2, max_servers=10)
    print(f"Autoscaling: {auto['autoscaling']['min_servers']}-{auto['autoscaling']['max_servers']} servers")
    
    capacity = lb.calculate_capacity(5000, 15)
    print(f"Capacity: {capacity['required_capacity']['recommended_rps']} RPS recommended")
    
    optimize = lb.optimize_performance(load_balancer, {'latency_ms': 18})
    print(f"Optimizations: {len(optimize['optimizations'])} recommendations")
    
    persistence = lb.configure_session_persistence(load_balancer, "cookie")
    print(f"Session Persistence: {persistence['persistence']['type']}")
    
    monitor = lb.monitor_load_balancer(load_balancer)
    print(f"Monitor: {monitor['health']['uptime']} uptime")
    
    ddos = lb.configure_ddos_protection(load_balancer)
    print(f"DDoS Protection: {len(ddos['protection_layers'])} layers")
    
    haproxy = HAProxyConfiguration().create_config("web-frontend", [])
    print(f"HAProxy config: {len(haproxy)} chars")
    
    nginx = NginxLoadBalancer().create_upstream("web_servers", [
        {'name': 'web1', 'ip': '10.0.1.10', 'port': 80, 'weight': 2},
        {'name': 'web2', 'ip': '10.0.1.11', 'port': 80, 'weight': 1}
    ])
    print(f"Nginx upstream: {len(nginx.splitlines())} lines")
