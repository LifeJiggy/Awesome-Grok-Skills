class Kubernetes:
    def __init__(self):
        self.cluster = None
        self.namespaces = {}

    def create_cluster(self, name, version="1.28", provider="on_prem"):
        self.cluster = {
            "name": name,
            "version": version,
            "provider": provider,
            "nodes": [],
            "control_plane": {},
            "addon_services": []
        }
        return self

    def add_node(self, node_name, node_type, zone=None, labels=None, taints=None):
        self.cluster["nodes"].append({
            "name": node_name,
            "type": node_type,  # control-plane, worker
            "zone": zone,
            "labels": labels or {},
            "taints": taints or [],
            "spec": {
                "unschedulable": False,
                "pod_cidr": None
            }
        })
        return self

    def create_namespace(self, namespace_name, resource_quotas=None, limit_ranges=None):
        self.namespaces[namespace_name] = {
            "name": namespace_name,
            "resource_quotas": resource_quotas or {},
            "limit_ranges": limit_ranges or {},
            "network_policies": []
        }
        return self

    def create_deployment(self, name, namespace, image, replicas=1, labels=None):
        return {
            "api_version": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": name, "namespace": namespace},
            "spec": {
                "replicas": replicas,
                "selector": {"match_labels": labels or {"app": name}},
                "template": {
                    "metadata": {"labels": labels or {"app": name}},
                    "spec": {
                        "containers": [{
                            "name": name,
                            "image": image,
                            "ports": [],
                            "resources": {"limits": {}, "requests": {}},
                            "liveness_probe": None,
                            "readiness_probe": None,
                            "startup_probe": None,
                            "env": [],
                            "env_from": [],
                            "volume_mounts": [],
                            "image_pull_policy": "Always"
                        }],
                        "volumes": [],
                        "restart_policy": "Always"
                    }
                }
            }
        }

    def add_container_port(self, deployment, port, container_port, protocol="TCP"):
        for container in deployment["spec"]["template"]["spec"]["containers"]:
            if container["name"] == deployment["metadata"]["name"]:
                container["ports"].append({
                    "container_port": container_port,
                    "protocol": protocol,
                    "name": f"{container_port}-{protocol.lower()}"
                })
        return deployment

    def add_resource_limits(self, deployment, cpu_limit, memory_limit, cpu_request=None, memory_request=None):
        for container in deployment["spec"]["template"]["spec"]["containers"]:
            if container["name"] == deployment["metadata"]["name"]:
                container["resources"]["limits"] = {
                    "cpu": cpu_limit,
                    "memory": memory_limit
                }
                container["resources"]["requests"] = {
                    "cpu": cpu_request or cpu_limit,
                    "memory": memory_request or memory_limit
                }
        return deployment

    def add_liveness_probe(self, deployment, probe_type="httpGet", path="/health", port=8080):
        for container in deployment["spec"]["template"]["spec"]["containers"]:
            if container["name"] == deployment["metadata"]["name"]:
                container["liveness_probe"] = {
                    probe_type: {"path": path, "port": port},
                    "initial_delay_seconds": 15,
                    "period_seconds": 10,
                    "timeout_seconds": 3,
                    "failure_threshold": 3,
                    "success_threshold": 1
                }
        return deployment

    def add_readiness_probe(self, deployment, probe_type="httpGet", path="/ready", port=8080):
        for container in deployment["spec"]["template"]["spec"]["containers"]:
            if container["name"] == deployment["metadata"]["name"]:
                container["readiness_probe"] = {
                    probe_type: {"path": path, "port": port},
                    "initial_delay_seconds": 5,
                    "period_seconds": 5,
                    "timeout_seconds": 3,
                    "failure_threshold": 3,
                    "success_threshold": 1
                }
        return deployment

    def create_service(self, name, namespace, service_type="ClusterIP", selector=None, ports=None):
        return {
            "api_version": "v1",
            "kind": "Service",
            "metadata": {"name": name, "namespace": namespace},
            "spec": {
                "type": service_type,  # ClusterIP, NodePort, LoadBalancer, ExternalName
                "selector": selector or {"app": name},
                "ports": ports or [{"port": 80, "target_port": 8080, "protocol": "TCP"}],
                "session_affinity": "None"
            }
        }

    def create_configmap(self, name, namespace, data=None, literals=None):
        return {
            "api_version": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": name, "namespace": namespace},
            "data": data or {},
            "binary_data": {}
        }

    def create_secret(self, name, namespace, secret_type="Opaque", data=None, string_data=None):
        return {
            "api_version": "v1",
            "kind": "Secret",
            "metadata": {"name": name, "namespace": namespace},
            "type": secret_type,  # Opaque, kubernetes.io/tls, kubernetes.io/basic-auth
            "data": data or {},
            "string_data": string_data or {}
        }

    def create_ingress(self, name, namespace, rules=None, tls_config=None):
        return {
            "api_version": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {"name": name, "namespace": namespace, "annotations": {}},
            "spec": {
                "ingress_class_name": "nginx",
                "rules": rules or [],
                "tls": tls_config or []
            }
        }

    def add_ingress_rule(self, ingress, host, path, service_name, service_port):
        ingress["spec"]["rules"].append({
            "host": host,
            "http": {
                "paths": [{
                    "path": path,
                    "path_type": "Prefix",
                    "backend": {
                        "service": {
                            "name": service_name,
                            "port": {"number": service_port}
                        }
                    }
                }]
            }
        })
        return ingress

    def create_persistent_volume_claim(self, name, namespace, storage_size, access_modes=None):
        return {
            "api_version": "v1",
            "kind": "PersistentVolumeClaim",
            "metadata": {"name": name, "namespace": namespace},
            "spec": {
                "access_modes": access_modes or ["ReadWriteOnce"],
                "resources": {"requests": {"storage": storage_size}},
                "storage_class_name": "standard"
            }
        }

    def create_statefulset(self, name, namespace, image, replicas=1, volume_claims=None):
        return {
            "api_version": "apps/v1",
            "kind": "StatefulSet",
            "metadata": {"name": name, "namespace": namespace},
            "spec": {
                "replicas": replicas,
                "service_name": f"{name}-headless",
                "selector": {"match_labels": {"app": name}},
                "template": {
                    "metadata": {"labels": {"app": name}},
                    "spec": {
                        "containers": [{
                            "name": name,
                            "image": image,
                            "ports": [],
                            "volume_mounts": []
                        }]
                    }
                },
                "volume_claim_templates": volume_claims or []
            }
        }

    def create_daemonset(self, name, namespace, image, labels=None):
        return {
            "api_version": "apps/v1",
            "kind": "DaemonSet",
            "metadata": {"name": name, "namespace": namespace},
            "spec": {
                "selector": {"match_labels": labels or {"app": name}},
                "template": {
                    "metadata": {"labels": labels or {"app": name}},
                    "spec": {
                        "containers": [{
                            "name": name,
                            "image": image,
                            "volume_mounts": []
                        }],
                        "tolerations": []
                    }
                }
            }
        }

    def create_job(self, name, namespace, image, completions=1, backoff_limit=6):
        return {
            "api_version": "batch/v1",
            "kind": "Job",
            "metadata": {"name": name, "namespace": namespace},
            "spec": {
                "completions": completions,
                "backoff_limit": backoff_limit,
                "template": {
                    "metadata": {"labels": {"app": name}},
                    "spec": {
                        "restart_policy": "Never",
                        "containers": [{
                            "name": name,
                            "image": image
                        }]
                    }
                }
            }
        }

    def create_cronjob(self, name, namespace, image, schedule="* * * * *", concurrency_policy="Forbid"):
        return {
            "api_version": "batch/v1beta1",
            "kind": "CronJob",
            "metadata": {"name": name, "namespace": namespace},
            "spec": {
                "schedule": schedule,
                "concurrency_policy": concurrency_policy,
                "job_template": {
                    "spec": {
                        "template": {
                            "metadata": {"labels": {"app": name}},
                            "spec": {
                                "restart_policy": "Never",
                                "containers": [{
                                    "name": name,
                                    "image": image
                                }]
                            }
                        }
                    }
                }
            }
        }

    def create_hpa(self, name, namespace, deployment_name, min_replicas=1, max_replicas=10, cpu_threshold=70):
        return {
            "api_version": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {"name": name, "namespace": namespace},
            "spec": {
                "scale_target_ref": {
                    "api_version": "apps/v1",
                    "kind": "Deployment",
                    "name": deployment_name
                },
                "min_replicas": min_replicas,
                "max_replicas": max_replicas,
                "metrics": [{
                    "type": "Resource",
                    "resource": {
                        "name": "cpu",
                        "target": {
                            "type": "Utilization",
                            "average_utilization": cpu_threshold
                        }
                    }
                }]
            }
        }

    def create_network_policy(self, name, namespace, pod_selector, ingress_rules=None, egress_rules=None):
        return {
            "api_version": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": name, "namespace": namespace},
            "spec": {
                "pod_selector": {"match_labels": pod_selector},
                "policy_types": ["Ingress", "Egress"],
                "ingress": ingress_rules or [],
                "egress": egress_rules or []
            }
        }

    def create_service_account(self, name, namespace, automount_token=True):
        return {
            "api_version": "v1",
            "kind": "ServiceAccount",
            "metadata": {"name": name, "namespace": namespace},
            "automount_service_account_token": automount_token
        }

    def create_rbac_role(self, name, namespace, rules):
        return {
            "api_version": "rbac.authorization.k8s.io/v1",
            "kind": "Role",
            "metadata": {"name": name, "namespace": namespace},
            "rules": rules or []
        }

    def create_rbac_cluster_role(self, name, rules):
        return {
            "api_version": "rbac.authorization.k8s.io/v1",
            "kind": "ClusterRole",
            "metadata": {"name": name},
            "rules": rules or []
        }

    def create_role_binding(self, name, namespace, role_name, subjects):
        return {
            "api_version": "rbac.authorization.k8s.io/v1",
            "kind": "RoleBinding",
            "metadata": {"name": name, "namespace": namespace},
            "subjects": subjects or [],
            "role_ref": {
                "api_group": "rbac.authorization.k8s.io",
                "kind": "Role",
                "name": role_name
            }
        }
