# Docker

## Overview

Docker is a platform for developing, shipping, and running applications in isolated containers. This skill covers Dockerfile creation, image building, container management, and Docker Compose orchestration. Docker containers provide consistent environments from development through production, solving the "works on my machine" problem that plagues complex software systems.

## Core Capabilities

Dockerfile instructions define image layers including FROM, RUN, COPY, ENV, EXPOSE, and ENTRYPOINT. Multi-stage builds enable efficient final images by separating build dependencies from runtime. Container networking connects containers through bridges, overlays, and host networks. Volume management persists data outside container lifecycles.

Docker Compose defines multi-container applications with YAML configuration. Container orchestration through Docker Swarm provides basic clustering capabilities. Docker BuildKit enables efficient parallel builds with advanced caching. Container security includes user namespaces, seccomp profiles, and capability management.

## Usage Examples

```python
from docker import Docker

docker = Docker()

dockerfile = docker.create_dockerfile(
    base_image="node:20-alpine",
    workdir="/app",
    user="node"
)

docker.add_env_variable(dockerfile, "NODE_ENV", "production")
docker.add_env_variable(dockerfile, "API_URL", "https://api.example.com")

docker.add_run_command(dockerfile, "npm ci --only=production")
docker.add_copy_command(dockerfile, ".", "/app")
docker.add_workdir(dockerfile, "/app")

docker.add_volume(dockerfile, "./data", "/app/data")

dockerfile["entrypoint"] = ["npm", "start"]
dockerfile["cmd"] = ["start"]
dockerfile["expose_ports"].append(3000)

docker.create_image(
    name="my-node-app",
    tag="v1.0.0",
    dockerfile=dockerfile
)

container = docker.create_container(
    name="my-node-app-prod",
    image="my-node-app:v1.0.0",
    ports=[{"host": 8080, "container": 3000}],
    volumes=[{"host": "./logs", "container": "/app/logs"}],
    env=[{"key": "NODE_ENV", "value": "production"}],
    restart_policy="unless-stopped"
)

docker.add_healthcheck(
    container,
    test=["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"],
    interval_seconds=30,
    timeout_seconds=3,
    retries=3
)

network = docker.configure_network(
    network_name="app-network",
    driver="bridge"
)

volume = docker.create_volume(
    volume_name="app-data",
    driver="local"
)

compose = docker.create_docker_compose(
    version="3.8",
    project_name="myapp"
)

compose.add_service(
    service_name="api",
    image="my-node-app:v1.0.0",
    ports=["8080:3000"],
    environment={"NODE_ENV": "production"},
    volumes=["./api:/app"]
)

compose.add_service(
    service_name="db",
    image="postgres:15",
    environment={
        "POSTGRES_DB": "myapp",
        "POSTGRES_USER": "user",
        "POSTGRES_PASSWORD": "password"
    },
    volumes=["postgres_data:/var/lib/postgresql/data"]
)

compose.add_depends_on("api", "db", condition="service_healthy")

compose.configure_service_scaling("api", replicas=3)

compose.configure_healthcheck(
    service_name="api",
    test=["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"],
    interval="30s",
    timeout="3s",
    retries=3
)

compose.add_service(
    service_name="redis",
    image="redis:7-alpine",
    volumes=["redis_data:/data"]
)

compose.add_service(
    service_name="nginx",
    image="nginx:alpine",
    ports=["80:80"],
    volumes=["./nginx.conf:/etc/nginx/nginx.conf:ro"]
)

security_context = docker.create_security_context(
    run_as_user=1000,
    read_only_rootfs=True,
    allow_privilege_escalation=False
)

resource_limits = docker.configure_resource_limits(
    cpu_limit="1.0",
    memory_limit="512M",
    cpu_reservation="0.5",
    memory_reservation="256M"
)

logging = docker.configure_logging(
    driver="json-file",
    options={"max-size": "10m", "max-file": "3"}
)

dockerignore = docker.create_dockerignore(patterns=[
    ".git",
    "node_modules",
    "*.log",
    ".env",
    "Dockerfile*",
    "docker-compose*"
])
```

## Best Practices

Use specific image tags instead of `latest` for reproducible builds. Minimize image layers by combining related commands. Use multi-stage builds to keep final images small. Don't include secrets in images; use runtime injection.

Prefer non-root users inside containers for security. Use .dockerignore to exclude unnecessary files from build context. Implement health checks for reliable container orchestration. Set resource limits to prevent containers from affecting system performance. Use named volumes for persistent data rather than bind mounts.

## Related Skills

- Kubernetes (container orchestration)
- CI/CD Pipelines (automation workflows)
- Container Orchestration (container management)
- DevOps (development operations)

## Use Cases

Microservices architecture uses Docker containers to isolate and deploy individual services. CI/CD pipelines build Docker images as artifacts for consistent deployments. Local development environments replicate production configurations with Docker Compose. Legacy application containerization modernizes existing applications without rewriting. Machine learning workflows package models and dependencies in portable containers.
