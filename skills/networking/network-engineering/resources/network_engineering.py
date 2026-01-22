from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class NetworkDeviceType(Enum):
    ROUTER = "router"
    SWITCH = "switch"
    FIREWALL = "firewall"
    LOAD_BALANCER = "load_balancer"
    WIRELESS_CONTROLLER = "wireless_controller"
    ACCESS_POINT = "access_point"


class NetworkLayer(Enum):
    CORE = "core"
    DISTRIBUTION = "distribution"
    ACCESS = "access"


@dataclass
class NetworkDevice:
    device_id: str
    hostname: str
    device_type: NetworkDeviceType
    ip_address: str
    mac_address: str
    layer: NetworkLayer
    status: str


class NetworkEngineeringManager:
    """Manage network engineering tasks"""
    
    def __init__(self):
        self.devices = []
    
    def design_network_topology(self,
                                requirements: Dict) -> Dict:
        """Design network topology"""
        return {
            'topology_type': 'Three-tier',
            'layers': {
                'core': {
                    'devices': ['Core-Router-1', 'Core-Router-2'],
                    'function': 'High-speed routing between distribution layers',
                    'redundancy': 'Active-Active',
                    'bandwidth': '100Gbps'
                },
                'distribution': {
                    'devices': ['Dist-Switch-1', 'Dist-Switch-2', 'Dist-Switch-3'],
                    'function': 'Routing, ACLs, QoS',
                    'redundancy': 'Active-Standby',
                    'bandwidth': '40Gbps'
                },
                'access': {
                    'devices': ['Access-Switches'],
                    'function': 'Endpoint connectivity',
                    'redundancy': 'Stack or redundant uplink',
                    'bandwidth': '10Gbps'
                }
            },
            'addressing': {
                'network': '10.0.0.0/16',
                'vlans': [
                    {'id': 10, 'name': 'Management', 'subnet': '10.0.10.0/24'},
                    {'id': 20, 'name': 'Servers', 'subnet': '10.0.20.0/24'},
                    {'id': 30, 'name': 'Users', 'subnet': '10.0.30.0/24'},
                    {'id': 40, 'name': 'Guest', 'subnet': '10.0.40.0/24'},
                    {'id': 50, 'name': 'Voice', 'subnet': '10.0.50.0/24'},
                    {'id': 60, 'name': 'IoT', 'subnet': '10.0.60.0/24'}
                ]
            },
            'routing': {
                'igp': 'OSPF',
                'egp': 'BGP',
                'redundancy': 'HSRP/VRRP'
            }
        }
    
    def configure_router(self,
                         hostname: str,
                         interfaces: List[Dict]) -> Dict:
        """Generate router configuration"""
        config = f'''!
hostname {hostname}
!
'''
        for iface in interfaces:
            config += f'''interface {iface['name']}
 description {iface.get('description', '')}
 ip address {iface['ip']} {iface['mask']}
'''
            if iface.get('shutdown') == False:
                config += ' no shutdown\n'
            config += '!\n'
        
        config += '''router ospf 1
 network 10.0.0.0 0.0.255.255 area 0
!
ip classless
!
'''
        return {
            'hostname': hostname,
            'config': config,
            'interfaces': len(interfaces)
        }
    
    def configure_switch(self,
                         hostname: str,
                         vlans: List[Dict],
                         trunk_ports: List[str],
                         access_ports: List[Dict]) -> Dict:
        """Generate switch configuration"""
        config = f'''!
hostname {hostname}
!
'''
        for vlan in vlans:
            config += f'''vlan {vlan['id']}
 name {vlan['name']}
!
'''
        config += '!\n'
        
        for port in trunk_ports:
            config += f'''interface range gi1/0/{port}
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
!
'''
        
        for port in access_ports:
            config += f'''interface gi1/0/{port['id']}
 switchport mode access
 switchport access vlan {port['vlan']}
 spanning-tree portfast
!
'''
        
        return {
            'hostname': hostname,
            'vlans_configured': len(vlans),
            'trunk_ports': len(trunk_ports),
            'access_ports': len(access_ports),
            'config': config
        }
    
    def calculate_subnet(self,
                         network_address: str,
                         required_hosts: int) -> Dict:
        """Calculate optimal subnet"""
        import math
        
        if required_hosts <= 2:
            prefix = 30
        elif required_hosts <= 6:
            prefix = 29
        elif required_hosts <= 14:
            prefix = 28
        elif required_hosts <= 30:
            prefix = 27
        elif required_hosts <= 62:
            prefix = 26
        elif required_hosts <= 126:
            prefix = 25
        elif required_hosts <= 254:
            prefix = 24
        elif required_hosts <= 510:
            prefix = 23
        elif required_hosts <= 1022:
            prefix = 22
        else:
            prefix = 16
        
        return {
            'network_address': network_address,
            'prefix': f'/{prefix}',
            'subnet_mask': self._prefix_to_mask(prefix),
            'usable_hosts': 2 ** (32 - prefix) - 2,
            'range': f'{network_address} - {self._broadcast_address(network_address, prefix)}',
            'gateway': self._next_ip(network_address, 1)
        }
    
    def _prefix_to_mask(self, prefix: int) -> str:
        mask = (0xffffffff << (32 - prefix)) & 0xffffffff
        return '.'.join([str((mask >> (8 * i)) & 0xff) for i in range(3, -1, -1)])
    
    def _broadcast_address(self, network: str, prefix: int) -> str:
        parts = list(map(int, network.split('.')))
        mask = (0xffffffff << (32 - prefix)) & 0xffffffff
        network_int = (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
        broadcast = (network_int | (0xffffffff - mask)) & 0xffffffff
        return '.'.join([str((broadcast >> (8 * i)) & 0xff) for i in range(3, -1, -1)])
    
    def _next_ip(self, network: str, offset: int) -> str:
        parts = list(map(int, network.split('.')))
        network_int = (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]
        next_ip = network_int + offset
        return '.'.join([str((next_ip >> (8 * i)) & 0xff) for i in range(3, -1, -1)])
    
    def design_vlan_structure(self,
                              department_requirements: List[Dict]) -> Dict:
        """Design VLAN structure"""
        vlans = []
        vlan_id = 10
        
        for dept in department_requirements:
            vlan = {
                'id': vlan_id,
                'name': f"{dept['name']}-VLAN",
                'subnet': dept.get('subnet', f'10.0.{vlan_id}.0/24'),
                'purpose': dept['purpose'],
                'devices': dept.get('devices', 50),
                'security_level': dept.get('security', 'standard'),
                ' QinQ': dept.get('qinq', False),
                'services': dept.get('services', ['DHCP', 'DNS'])
            }
            vlans.append(vlan)
            vlan_id += 10
        
        return {
            'total_vlans': len(vlans),
            'vlan_range': f'10-{vlan_id-10}',
            'inter_vlan_routing': True,
            'vlan_consumption': f'{len(vlans)}/{1000}',
            'structure': vlans
        }
    
    def configure_vpn(self,
                      vpn_type: str,
                      remote_networks: List[str],
                      encryption: str = "AES256") -> Dict:
        """Configure VPN settings"""
        return {
            'type': vpn_type,  # site-to-site, remote-access, SSL
            'mode': 'tunnel' if vpn_type == 'site-to-site' else 'client',
            'encryption': encryption,
            'authentication': 'PSK',
            'ike_version': 2,
            'algorithms': {
                'encryption': encryption,
                'integrity': 'SHA256',
                'dh_group': '14 (2048-bit)'
            },
            'remote_networks': remote_networks,
            'tunnel_interface': 'Tunnel0',
            'keepalive': '10 30',
            'example_config': f'''
crypto isakmp policy 10
 encr {encryption.lower()}
 authentication pre-share
 hash sha
 group 14
 lifetime 86400

crypto isakmp key SECRETKEY address 203.0.113.1

crypto ipsec transform-set VPN-TS esp-{encryption.lower()} esp-sha256-hmac

crypto map VPN-MAP 10 ipsec-isakmp
 set peer 203.0.113.1
 set transform-set VPN-TS
 match address VPN-TRAFFIC

access-list VPN-TRAFFIC permit ip 10.0.0.0 0.0.255.255 {remote_networks[0]} 0.0.0.255
'''
        }
    
    def plan_network_capacity(self,
                              current_users: int,
                              growth_rate: float,
                              peak_concurrency: float) -> Dict:
        """Plan network capacity"""
        projected_users = int(current_users * (1 + growth_rate) ** 3)
        peak_users = int(current_users * peak_concurrency)
        
        return {
            'current_state': {
                'users': current_users,
                'peak_concurrent': peak_users,
                'bandwidth_mbps': 1000
            },
            'projections': {
                '1_year': int(current_users * (1 + growth_rate)),
                '2_years': int(current_users * (1 + growth_rate) ** 2),
                '3_years': projected_users
            },
            'bandwidth_requirements': {
                'current_mbps': 1000,
                'projected_mbps': int(1000 * (1 + growth_rate) ** 3),
                'recommended_mbps': int(1000 * (1 + growth_rate) ** 3 * 1.5)
            },
            'switch_capacity': {
                'current_ports': 48,
                'required_ports': int(projected_users / 2),
                'recommended': '48-port PoE+ with 10G uplink'
            },
            'wifi_capacity': {
                'access_points': 20,
                'recommended': int(peak_users / 30),
                'channel_planning': 'Non-overlapping 5GHz channels'
            }
        }
    
    def troubleshoot_connectivity_issue(self,
                                         symptom: str) -> Dict:
        """Generate troubleshooting guide"""
        guides = {
            'no_connectivity': {
                'steps': [
                    'Check physical connectivity (link lights)',
                    'Verify IP configuration (ipconfig/ifconfig)',
                    'Test DNS resolution (nslookup)',
                    'Ping default gateway',
                    'Ping remote host',
                    'Check firewall settings',
                    'Verify VLAN membership',
                    'Check port security'
                ],
                'common_causes': [
                    'Physical cable disconnect',
                    'IP conflict',
                    'DNS server down',
                    'VLAN mismatch',
                    'Firewall block'
                ]
            },
            'slow_network': {
                'steps': [
                    'Check interface errors',
                    'Monitor bandwidth utilization',
                    'Check for broadcast storms',
                    'Verify duplex mismatch',
                    'Scan for malware',
                    'Check for loops',
                    'Review QoS configuration'
                ],
                'common_causes': [
                    'High utilization',
                    'Duplex mismatch',
                    'Network loop',
                    'Malware/spam',
                    'Backplane saturation'
                ]
            },
            'intermittent_connectivity': {
                'steps': [
                    'Check cable integrity',
                    'Verify spanning tree',
                    'Monitor port errors over time',
                    'Check power supply',
                    'Review logs for errors',
                    'Test with different cable'
                ],
                'common_causes': [
                    'Failing cable',
                    'Flapping port',
                    'Power issues',
                    'Intermittent device failure'
                ]
            }
        }
        
        return guides.get(symptom, guides['no_connectivity'])
    
    def generate_network_report(self,
                                network_info: Dict) -> Dict:
        """Generate network assessment report"""
        return {
            'report_id': f"NW-RPT-{datetime.now().strftime('%Y%m%d')}",
            'generated': datetime.now().isoformat(),
            'executive_summary': {
                'overall_health': 'Good',
                'uptime_percentage': 99.95,
                'total_devices': 150,
                'critical_issues': 2,
                'warnings': 8
            },
            'device_inventory': {
                'routers': 4,
                'switches': 45,
                'firewalls': 2,
                'wireless_aps': 35
            },
            'bandwidth_analysis': {
                'avg_utilization': 45,
                'peak_utilization': 78,
                'bottlenecks': ['Core-Router-1 uplink']
            },
            'security_posture': {
                'vulnerabilities_found': 12,
                'critical': 1,
                'high': 3,
                'medium': 5,
                'low': 3,
                'compliance_status': 'PCI-DSS Compliant'
            },
            'recommendations': [
                'Upgrade core router uplink to 100Gbps',
                'Patch 3 critical vulnerabilities within 7 days',
                'Implement 802.1X authentication',
                'Review access control lists quarterly'
            ]
        }


class NetworkSecurityManager:
    """Manage network security"""
    
    def configure_firewall_rules(self,
                                policy: Dict) -> Dict:
        """Generate firewall rule set"""
        return {
            'policy': policy.get('name', 'Default Policy'),
            'default_action': policy.get('default', 'deny'),
            'rules': [
                {'id': 100, 'action': 'permit', 'src': '10.0.10.0/24', 'dst': '10.0.20.0/24', 'port': '443', 'service': 'HTTPS'},
                {'id': 110, 'action': 'permit', 'src': '10.0.10.0/24', 'dst': '10.0.30.0/24', 'port': '80', 'service': 'HTTP'},
                {'id': 120, 'action': 'permit', 'src': 'any', 'dst': '10.0.40.0/24', 'port': '53', 'service': 'DNS'},
                {'id': 200, 'action': 'deny', 'src': 'any', 'dst': 'any', 'port': 'any', 'service': 'all'}
            ],
            'nat_rules': [
                {'internal': '10.0.10.100', 'external': '203.0.113.50', 'port': '443'}
            ]
        }
    
    def design_network_segmentation(self) -> Dict:
        """Design network segmentation"""
        return {
            'zones': [
                {'name': 'DMZ', 'security_level': 'High', 'devices': ['Web servers', 'Mail servers']},
                {'name': 'Internal LAN', 'security_level': 'Medium', 'devices': ['Workstations', 'Printers']},
                {'name': 'Server Farm', 'security_level': 'High', 'devices': ['Database servers', 'App servers']},
                {'name': 'Management', 'security_level': 'Critical', 'devices': ['Network devices', 'Monitoring']},
                {'name': 'Guest', 'security_level': 'Low', 'devices': ['Guest WiFi']},
                {'name': 'IoT', 'security_level': 'Medium', 'devices': ['Smart devices', 'Sensors']}
            ],
            'micro_segmentation': True,
            'zero_trust': True,
            'east_west_controls': 'Internal firewall'
        }


if __name__ == "__main__":
    net = NetworkEngineeringManager()
    
    topology = net.design_network_topology({
        'users': 500,
        'servers': 50,
        'wireless': True
    })
    print(f"Topology: {topology['topology_type']} with {len(topology['layers'])} layers")
    
    router_config = net.configure_router("Core-Router-1", [
        {'name': 'GigabitEthernet0/0', 'ip': '10.0.10.1', 'mask': '255.255.255.0', 'shutdown': False},
        {'name': 'GigabitEthernet0/1', 'ip': '10.0.20.1', 'mask': '255.255.255.0', 'shutdown': False}
    ])
    print(f"Router: {router_config['hostname']} with {router_config['interfaces']} interfaces")
    
    subnet = net.calculate_subnet("192.168.1.0", 60)
    print(f"Subnet: {subnet['network_address']}{subnet['prefix']}, {subnet['usable_hosts']} hosts")
    
    vlan_design = net.design_vlan_structure([
        {'name': 'Engineering', 'purpose': 'Engineering team devices', 'devices': 100},
        {'name': 'Marketing', 'purpose': 'Marketing team devices', 'devices': 50}
    ])
    print(f"VLANs: {vlan_design['total_vlans']} configured")
    
    vpn = net.configure_vpn("site-to-site", ["192.168.100.0/24", "192.168.101.0/24"])
    print(f"VPN: {vpn['type']} with {vpn['encryption']} encryption")
    
    capacity = net.plan_network_capacity(500, 0.15, 0.7)
    print(f"Capacity: {capacity['projections']['3_years']} projected users in 3 years")
    
    troubleshoot = net.troubleshoot_connectivity_issue("slow_network")
    print(f"Troubleshooting: {len(troubleshoot['steps'])} steps for slow network")
    
    report = net.generate_network_report(topology)
    print(f"Report: {report['executive_summary']['overall_health']} health rating")
    
    security = NetworkSecurityManager().configure_firewall_rules({'name': 'Corporate Policy'})
    print(f"Firewall: {len(security['rules'])} rules configured")
