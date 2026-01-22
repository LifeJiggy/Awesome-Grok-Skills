# Network Engineering

## Overview

Network Engineering encompasses the design, implementation, management, and troubleshooting of computer networks that form the backbone of modern digital infrastructure. This skill covers network architecture, routing and switching protocols, network security, and emerging technologies like software-defined networking and cloud networking. Network engineers ensure reliable, secure, and performant connectivity across enterprise environments, data centers, and cloud platforms that applications depend on.

## Core Capabilities

Routing protocol implementation and optimization covers OSPF, BGP, EIGRP, and IS-IS for enterprise and service provider networks. Switching architecture design includes VLAN configuration, spanning tree optimization, and layer 3 switching for scalable campus networks. Network security implementation covers firewalls, IDS/IPS systems, VPNs, and zero-trust architecture principles. Software-defined networking enables centralized control plane management through SDN controllers and network automation.

Network monitoring and observability tools provide visibility into traffic patterns, latency, and device health. Capacity planning and network optimization ensure performance meets application requirements as traffic grows. Cloud networking integrates hybrid and multi-cloud architectures with VPC design, direct connect, and SD-WAN technologies. IPv6 transition strategies address the exhaustion of IPv4 addresses and future-proof network addressing.

## Usage Examples

```python
from network_skill import NetworkManager, RouterConfig, NetworkMonitor, TopologyDesigner

# Create network topology design
topology = TopologyDesigner(
    name="Enterprise Headquarters Network",
    environment="production"
)

# Define network structure
topology.add_site(
    site_name="HQ",
    location="New York",
    timezone="America/New_York",
    devices=[
        {"name": "HQ-CORE-01", "type": "router", "model": "Cisco ASR-1001-X"},
        {"name": "HQ-CORE-02", "type": "router", "model": "Cisco ASR-1001-X"},
        {"name": "HQ-DIST-A", "type": "switch", "model": "Cisco C9300"},
        {"name": "HQ-DIST-B", "type": "switch", "model": "Cisco C9300"},
        {"name": "HQ-FW-01", "type": "firewall", "model": "Palo Alto PA-3410"},
        {"name": "HQ-FW-02", "type": "firewall", "model": "Palo Alto PA-3410"}
    ],
    wan_connections=[
        {"provider": "Verizon", "bandwidth": "10Gbps", "type": "MPLS"},
        {"provider": "Comcast", "bandwidth": "5Gbps", "type": "Internet"}
    ]
)

# Generate IP addressing scheme
addressing = topology.generate_ip_scheme(
    vlan_definitions=[
        {"vlan": 10, "name": "Management", "size": 256},
        {"vlan": 20, "name": "Servers", "size": 512},
        {"vlan": 30, "name": "User-Workstations", "size": 1024},
        {"vlan": 40, "name": "Voice", "size": 512},
        {"vlan": 50, "name": "Wireless-Guest", "size": 2048},
        {"vlan": 60, "name": "DMZ", "size": 256}
    ],
    network="10.1.0.0/16",
    use_ipv6=True
)
print("IP Scheme Generated:")
for vlan in addressing:
    print(f"  VLAN {vlan['vlan']} ({vlan['name']}): {vlan['network']}")

# Configure core router
router_config = RouterConfig(
    device="HQ-CORE-01",
    vendor="Cisco",
    os="IOS-XE"
)

# Generate OSPF configuration
ospf_config = router_config.generate_ospf(
    process_id=1,
    router_id="10.1.0.1",
    networks=[
        {"network": "10.1.0.0/16", "area": 0},
        {"network": "10.2.0.0/16", "area": 0}
    ],
    reference_bandwidth=100000,
    hello_interval=10,
    dead_interval=40,
    passive_interfaces=["GigabitEthernet0/0/1"]
)

# Generate BGP configuration for WAN
bgp_config = router_config.generate_bgp(
    as_number=65001,
    router_id="10.1.0.1",
    neighbors=[
        {"neighbor": "203.0.113.1", "as": 64501, "description": "ISP-1"},
        {"neighbor": "203.0.113.3", "as": 64502, "description": "ISP-2"}
    ],
    networks_to_advertise=["10.1.0.0/16"],
    route_maps=[
        {"name": "PREPEND-AS", "direction": "outbound", "action": "prepend", "times": 2}
    ]
)

# Generate firewall security policy
firewall_config = router_config.generate_firewall_policies(
    device_type="Palo Alto",
    policies=[
        {
            "name": "Allow-Inside-To-DMZ-Web",
            "source_zone": "Inside",
            "destination_zone": "DMZ",
            "source_ip": ["10.1.0.0/16"],
            "destination_ip": ["10.1.60.0/24"],
            "application": ["web-browsing", "ssl"],
            "action": "allow",
            "log": True
        },
        {
            "name": "Allow-DMZ-To-Outside",
            "source_zone": "DMZ",
            "destination_zone": "Outside",
            "source_ip": ["10.1.60.0/24"],
            "destination_ip": ["any"],
            "application": ["http", "https"],
            "action": "allow",
            "log": True
        },
        {
            "name": "Block-Inside-To-Outside-Gaming",
            "source_zone": "Inside",
            "destination_zone": "Outside",
            "source_ip": ["10.1.0.0/16"],
            "destination_ip": ["any"],
            "application": ["gaming"],
            "action": "deny",
            "log": True
        }
    ]
)

# Deploy configuration to device
deployment = router_config.deploy_config(
    device_ip="10.1.0.1",
    username="admin",
    ssh_key="~/.ssh/id_rsa",
    enable_password="ENABLE_SECRET"
)
print(f"Configuration Deployed: {deployment.success}")
print(f"Changes Applied: {deployment.changes_count}")

# Monitor network health
monitor = NetworkMonitor(
    poll_interval=30,
    retention_days=30
)

# Check device status
status = monitor.get_device_status(
    devices=["HQ-CORE-01", "HQ-CORE-02", "HQ-FW-01", "HQ-FW-02"],
    metrics=["cpu", "memory", "interface_status", "temperature"]
)
print("Device Status:")
for device, metrics in status.items():
    print(f"  {device}:")
    print(f"    CPU: {metrics['cpu']}%")
    print(f"    Memory: {metrics['memory']}%")
    print(f"    Status: {metrics['overall_status']}")

# Generate traffic analysis report
traffic_report = monitor.analyze_traffic(
    time_range="last_24h",
    interfaces=["GigabitEthernet0/0/0", "GigabitEthernet0/0/1"],
    top_talkers=10
)
print(f"Total Traffic: {traffic_report['total_bytes']}")
print(f"Peak Bandwidth: {traffic_report['peak_mbps']} Mbps")
print(f"Top Applications: {traffic_report['top_applications']}")
```

## Best Practices

Design networks with redundancy and high availability in mind, eliminating single points of failure at critical points. Use hierarchical network design with clear separation between core, distribution, and access layers. Implement comprehensive monitoring from day one, establishing baselines for normal behavior to detect anomalies. Apply defense in depth principles with multiple security layers including perimeter firewalls, internal segmentation, and endpoint protection.

Document all network configurations, addressing schemes, and logical topology in maintained design documents. Automate routine configuration tasks using Ansible, Python, or network automation frameworks to reduce human error. Plan for growth with addressing schemes and capacity that accommodate future expansion. Regularly test failover mechanisms and backup systems to ensure they work when needed.

## Related Skills

- Load Balancing (traffic distribution across servers)
- Cloud Architecture (cloud networking integration)
- Network Security (firewall and VPN configuration)
- DevOps (infrastructure automation and CI/CD)

## Use Cases

Enterprise network engineering connects thousands of users across multiple buildings and data centers with reliable, secure connectivity. Data center networking provides the high-bandwidth, low-latency fabric that servers and applications depend on. Service provider networks deliver internet connectivity and wholesale bandwidth to businesses and consumers. Cloud networking integrates on-premises infrastructure with AWS, Azure, and GCP for hybrid cloud architectures.
