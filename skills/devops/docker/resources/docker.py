class Docker:
    def __init__(self):
        self.images = {}
        self.containers = {}
        self.compose_project = None

    def create_dockerfile(self, base_image, workdir="/app", user=None):
        dockerfile = {
            "base_image": base_image,
            "workdir": workdir,
            "user": user,
            "commands": [],
            "expose_ports": [],
            "environment": [],
            "volumes": [],
            "entrypoint": None,
            "cmd": None
        }
        return dockerfile

    def add_run_command(self, dockerfile, command):
        dockerfile["commands"].append(f"RUN {command}")
        return dockerfile

    def add_env_variable(self, dockerfile, key, value):
        dockerfile["environment"].append({"key": key, "value": value})
        return dockerfile

    def add_volume(self, dockerfile, source, target):
        dockerfile["volumes"].append({"source": source, "target": target})
        return dockerfile

    def add_copy_command(self, dockerfile, source, destination):
        dockerfile["commands"].append(f"COPY {source} {destination}")
        return dockerfile

    def add_workdir(self, dockerfile, path):
        dockerfile["commands"].append(f"WORKDIR {path}")
        return dockerfile

    def create_multi_stage_build(self, stage_name, from_image, commands):
        return {
            "stage_name": stage_name,
            "from": from_image,
            "commands": commands,
            "as": stage_name
        }

    def create_image(self, name, tag="latest", dockerfile=None):
        self.images[name] = {
            "name": name,
            "tag": tag,
            "dockerfile": dockerfile,
            "layers": [],
            "size_mb": 0,
            "built": False
        }
        return self.images[name]

    def create_container(self, name, image, ports=None, volumes=None, env=None, restart_policy="always"):
        self.containers[name] = {
            "name": name,
            "image": image,
            "ports": ports or [],  # [{"host": 8080, "container": 80}]
            "volumes": volumes or [],
            "environment": env or [],
            "restart_policy": restart_policy,
            "network_mode": "bridge",
            "healthcheck": None,
            "status": "created"
        }
        return self.containers[name]

    def add_healthcheck(self, container, test, interval_seconds=30, timeout_seconds=3, retries=3):
        container["healthcheck"] = {
            "test": test,
            "interval": f"{interval_seconds}s",
            "timeout": f"{timeout_seconds}s",
            "retries": retries,
            "start_period": "5s"
        }
        return container

    def configure_network(self, network_name, driver="bridge", internal=False):
        return {
            "network_name": network_name,
            "driver": driver,
            "internal": internal,
            "subnet": None,
            "gateway": None,
            "attachable": True
        }

    def create_volume(self, volume_name, driver="local", driver_opts=None):
        return {
            "volume_name": volume_name,
            "driver": driver,
            "driver_opts": driver_opts or {},
            "labels": {}
        }

    def create_docker_compose(self, version="3.8", project_name=None):
        self.compose_project = {
            "version": version,
            "project_name": project_name,
            "services": {},
            "networks": {},
            "volumes": {}
        }
        return self

    def add_service(self, service_name, image, build=None, ports=None, environment=None, volumes=None):
        if self.compose_project:
            self.compose_project["services"][service_name] = {
                "image": image,
                "build": build,
                "ports": ports or [],
                "environment": environment or {},
                "volumes": volumes or [],
                "restart": "always",
                "depends_on": [],
                "healthcheck": None,
                "networks": ["default"]
            }
        return self

    def configure_service_scaling(self, service_name, replicas=1):
        if self.compose_project and service_name in self.compose_project["services"]:
            self.compose_project["services"][service_name]["deploy"] = {
                "replicas": replicas,
                "resources": {
                    "limits": {"cpus": "0.5", "memory": "512M"},
                    "reservations": {"cpus": "0.1", "memory": "128M"}
                }
            }
        return self

    def add_depends_on(self, service_name, dependency, condition="service_healthy"):
        if self.compose_project and service_name in self.compose_project["services"]:
            self.compose_project["services"][service_name]["depends_on"].append({
                "service": dependency,
                "condition": condition
            })
        return self

    def configure_healthcheck(self, service_name, test, interval=None, timeout=None, retries=None):
        if self.compose_project and service_name in self.compose_project["services"]:
            self.compose_project["services"][service_name]["healthcheck"] = {
                "test": test,
                "interval": interval,
                "timeout": timeout,
                "retries": retries,
                "start_period": "10s"
            }
        return self

    def create_secret(self, secret_name, file_path=None, environment=None):
        return {
            "secret_name": secret_name,
            "file": file_path,
            "environment": environment,
            "external": False
        }

    def configure_logging(self, driver="json-file", options=None):
        return {
            "driver": driver,
            "options": options or {
                "max-size": "10m",
                "max-file": "3"
            }
        }

    def build_image(self, dockerfile_path, tag, build_args=None):
        return {
            "dockerfile": dockerfile_path,
            "tag": tag,
            "build_args": build_args or {},
            "cache": True,
            "target": None
        }

    def run_container(self, image, name, detach=True, ports=None, volumes=None, env=None):
        return {
            "image": image,
            "name": name,
            "detach": detach,
            "ports": ports or [],
            "volumes": volumes or [],
            "environment": env or {},
            "remove": not detach
        }

    def create_dockerignore(self, patterns=None):
        return {
            "patterns": patterns or [
                ".git",
                ".dockerignore",
                "Dockerfile",
                "docker-compose.yml",
                "node_modules",
                "*.log"
            ]
        }

    def configure_registry_auth(self, registry, username, password):
        return {
            "registry": registry,
            "auth": {
                "username": username,
                "password": password
            }
        }

    def create_security_context(self, run_as_user=1000, read_only_rootfs=False, allow_privilege_escalation=False):
        return {
            "run_as_user": run_as_user,
            "read_only_rootfs": read_only_rootfs,
            "allow_privilege_escalation": allow_privilege_escalation,
            "capabilities": {"add": None, "drop": ["ALL"]}
        }

    def configure_resource_limits(self, cpu_limit, memory_limit, cpu_reservation=None, memory_reservation=None):
        return {
            "limits": {
                "cpus": cpu_limit,
                "memory": memory_limit
            },
            "reservations": {
                "cpus": cpu_reservation,
                "memory": memory_reservation
            }
        }
