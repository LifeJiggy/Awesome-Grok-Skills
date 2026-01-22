class Microservices:
    def __init__(self):
        self.services = {}
        self.architecture = None

    def define_architecture(self, name, pattern="layered"):
        self.architecture = {
            "name": name,
            "pattern": pattern,  # layered, hexagonal, event-driven, CQRS
            "services": {},
            "communication": {},
            "infrastructure": {}
        }
        return self

    def create_service(self, service_name, domain, responsibilities=None, technologies=None):
        service = {
            "name": service_name,
            "domain": domain,
            "responsibilities": responsibilities or [],
            "technologies": technologies or {},
            "endpoints": [],
            "data_stores": [],
            "dependencies": [],
            "events": []
        }
        self.services[service_name] = service
        if self.architecture:
            self.architecture["services"][service_name] = service
        return service

    def add_endpoint(self, service_name, endpoint):
        if service_name in self.services:
            self.services[service_name]["endpoints"].append(endpoint)
        return self

    def add_dependency(self, service_name, dependency, dependency_type="sync"):
        if service_name in self.services:
            self.services[service_name]["dependencies"].append({
                "service": dependency,
                "type": dependency_type
            })
        return self

    def add_event(self, service_name, event_name, event_type="domain"):
        if service_name in self.services:
            self.services[service_name]["events"].append({
                "name": event_name,
                "type": event_type,
                "producer": service_name,
                "consumers": []
            })
        return self

    def define_api_gateway(self, name, routes=None, authentication=None, rate_limiting=None):
        return {
            "name": name,
            "type": "api-gateway",
            "routes": routes or [],
            "authentication": authentication or {"type": "oauth2"},
            "rate_limiting": rate_limiting or {"requests_per_minute": 1000},
            "caching": {"enabled": True, "ttl_seconds": 300}
        }

    def define_service_mesh(self, name, mesh_type="istio", observability=None, security=None):
        return {
            "name": name,
            "type": "service-mesh",
            "implementation": mesh_type,
            "observability": observability or {"tracing": True, "metrics": True, "logging": True},
            "security": security or {"mtls": True, "authorization": True}
        }

    def configure_service_discovery(self, provider="consul", health_check=None):
        return {
            "provider": provider,
            "health_check": health_check or {"interval_seconds": 30, "timeout_seconds": 5},
            "registration": {"enabled": True, "deregistration": "immediate"},
            "catalog_sync": {"enabled": True, "interval_seconds": 60}
        }

    def define_circuit_breaker(self, service_name, failure_threshold=5, reset_timeout_seconds=60):
        return {
            "service": service_name,
            "failure_threshold": failure_threshold,
            "reset_timeout_seconds": reset_timeout_seconds,
            "half_open_requests": 3,
            "window_seconds": 60
        }

    def define_bulkhead(self, service_name, max_concurrent_calls=100, max_wait_duration_ms=5000):
        return {
            "service": service_name,
            "max_concurrent_calls": max_concurrent_calls,
            "max_wait_duration_ms": max_wait_duration_ms
        }

    def define_retry_policy(self, service_name, max_attempts=3, backoff_multiplier=2, max_backoff_ms=10000):
        return {
            "service": service_name,
            "max_attempts": max_attempts,
            "backoff_multiplier": backoff_multiplier,
            "max_backoff_ms": max_backoff_ms,
            "retry_on": ["5xx", "timeout", "connection_error"]
        }

    def define_timeout_policy(self, service_name, default_timeout_ms=30000):
        return {
            "service": service_name,
            "default_timeout_ms": default_timeout_ms,
            "per_endpoint_timeouts": {}
        }

    def configure_api_composition(self, composer_type="graphql", services=None):
        return {
            "type": composer_type,
            "services": services or [],
            "caching": {"enabled": True},
            "error_handling": {"mode": "fail_fast"}
        }

    def define_saga_pattern(self, saga_name, steps=None, compensation_strategy="sequential"):
        return {
            "name": saga_name,
            "steps": steps or [],
            "compensation_strategy": compensation_strategy,
            "orchestration": {"type": "centralized", "manager": None},
            "retry_policy": {"max_attempts": 3}
        }

    def add_saga_step(self, saga_name, step_name, service, action, compensation):
        return {
            "saga": saga_name,
            "step": step_name,
            "service": service,
            "action": action,
            "compensation": compensation
        }

    def define_event_sourcing(self, service_name, event_store=None, snapshot_policy=None):
        return {
            "service": service_name,
            "event_store": event_store or {"type": "kafka", "topic": f"{service_name}-events"},
            "snapshot_policy": snapshot_policy or {"interval_events": 1000},
            "event_schema": {"version": "1.0"}
        }

    def define_cqrs_pattern(self, service_name, read_model=None, write_model=None):
        return {
            "service": service_name,
            "write_model": write_model or {"type": "domain_model"},
            "read_model": read_model or {"type": "projection", "refresh": "eventual"},
            "synchronization": {"type": "event-driven", "broker": "kafka"}
        }

    def configure_health_checks(self, service_name, checks=None):
        return {
            "service": service_name,
            "checks": checks or [
                {"type": "liveness", "endpoint": "/health", "interval_seconds": 30},
                {"type": "readiness", "endpoint": "/ready", "interval_seconds": 10}
            ],
            "aggregation": {"type": "and"}
        }

    def define_service_level_objectives(self, service_name, slo_config=None):
        return {
            "service": service_name,
            "objectives": slo_config or [
                {"name": "availability", "target": 0.999, "window": "30d"},
                {"name": "latency_p99", "target": 200, "unit": "ms", "window": "7d"},
                {"name": "error_rate", "target": 0.001, "window": "1h"}
            ],
            "measurement": {"tool": "prometheus", "interval": "1m"}
        }

    def configure_distributed_tracing(self, service_name, tracer="jaeger", sample_rate=0.01):
        return {
            "service": service_name,
            "tracer": tracer,
            "sample_rate": sample_rate,
            "propagation": {"format": ["w3c", "b3"]},
            "context_propagation": True
        }

    def define_api_contract(self, service_name, contract_type="openapi", version="1.0"):
        return {
            "service": service_name,
            "type": contract_type,
            "version": version,
            "documentation": {"enabled": True, "endpoint": "/docs"},
            "validation": {"enabled": True, "strict_mode": True}
        }

    def configure_service_telemetry(self, service_name, metrics=None, logs=None, traces=None):
        return {
            "service": service_name,
            "telemetry": {
                "metrics": metrics or {"enabled": True, "endpoint": "/metrics"},
                "logs": logs or {"level": "INFO", "format": "json"},
                "traces": traces or {"enabled": True, "sample_rate": 0.01}
            }
        }

    def define_deployment_strategy(self, service_name, strategy="rolling", blue_green_config=None, canary_config=None):
        strategies = {
            "rolling": {"description": "Gradual rollout across instances", "max_surge": "25%", "max_unavailable": "25%"},
            "blue_green": blue_green_config or {"switch_strategy": "atomic", "rollback_timeout_seconds": 300},
            "canary": canary_config or {"initial_percentage": 5, "increment": 5, "pause_duration_minutes": 10}
        }
        return {
            "service": service_name,
            "strategy": strategy,
            "config": strategies.get(strategy, {})
        }
