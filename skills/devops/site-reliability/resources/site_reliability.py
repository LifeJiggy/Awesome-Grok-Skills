class SiteReliability:
    def __init__(self):
        self.slos = []
        self.slis = {}

    def create_sli(self, name, category, indicator, measurement_method):
        return {
            "name": name,
            "category": category,
            "indicator": indicator,
            "measurement_method": measurement_method
        }

    def create_slo(self, name, sli_name, target, window, compliance_period="calendar_month"):
        slo = {
            "name": name,
            "sli": sli_name,
            "target": target,
            "window": window,
            "compliance_period": compliance_period,
            "error_budget": 1 - target
        }
        self.slos.append(slo)
        return slo

    def create_availability_slo(self, name, target, window="30d"):
        return self.create_slo(
            name=name,
            sli_name="availability",
            target=target,
            window=window
        )

    def create_latency_slo(self, name, threshold_ms, target_percent, window="30d"):
        return self.create_slo(
            name=name,
            sli_name=f"latency_{threshold_ms}ms",
            target=target_percent,
            window=window
        )

    def create_throughput_slo(self, name, target_rps, window="30d"):
        return self.create_slo(
            name=name,
            sli_name="throughput",
            target=target_rps,
            window=window
        )

    def create_error_rate_slo(self, name, max_error_rate, window="30d"):
        return self.create_slo(
            name=name,
            sli_name="error_rate",
            target=1 - max_error_rate,
            window=window
        )

    def calculate_error_budget(self, slo, actual_performance):
        target = slo["target"]
        actual = actual_performance
        error_budget_remaining = max(0, target - actual)
        burn_rate = (1 - actual) / (1 - target) if target < 1 else 0
        return {
            "budget_remaining": error_budget_remaining,
            "burn_rate": burn_rate,
            "status": "healthy" if burn_rate < 0.5 else "warning" if burn_rate < 1 else "critical"
        }

    def create_runbook(self, name, steps, escalation_path=None):
        return {
            "name": name,
            "steps": steps,
            "escalation_path": escalation_path or ["on_call"],
            "automation": {"enabled": False, "scripts": []},
            "verification": {"method": None, "expected_result": None}
        }

    def create_incident_response(self, severity_levels=None, response_steps=None):
        return {
            "severity_levels": severity_levels or [
                {"level": 1, "name": "SEV-1", "response_time_min": 15, "description": "Critical outage"},
                {"level": 2, "name": "SEV-2", "response_time_min": 30, "description": "Major degradation"},
                {"level": 3, "name": "SEV-3", "response_time_min": 60, "description": "Minor issue"},
                {"level": 4, "name": "SEV-4", "response_time_min": 240, "description": "Cosmetic"}
            ],
            "response_steps": response_steps or ["detect", "assess", "contain", "resolve", "post_mortem"]
        }

    def create_post_mortem_template(self, sections=None):
        return {
            "sections": sections or [
                "summary",
                "timeline",
                "impact",
                "root_cause",
                "resolution",
                "lessons_learned",
                "action_items"
            ],
            "blameless": True,
            "template": ""
        }

    def create_on_call_schedule(self, rotation_type="weekly", handoff_day="Friday", handoff_hour="12:00"):
        return {
            "rotation_type": rotation_type,
            "handoff_day": handoff_day,
            "handoff_hour": handoff_hour,
            "escalation_chain": [
                {"level": 1, "escalate_after_minutes": 30},
                {"level": 2, "escalate_after_minutes": 60},
                {"level": 3, "escalate_after_minutes": 120}
            ]
        }

    def create_toil_metrics(self):
        return {
            "toil_activities": [],
            "metrics": {
                "total_toil_hours": 0,
                "toil_per_engineer": 0,
                "automation_opportunities": []
            },
            "reduction_target": {"percent": 20, "timeframe": "6 months"}
        }

    def create_capacity_plan(self, current_capacity, growth_rate, headroom_percent=20):
        return {
            "current_capacity": current_capacity,
            "growth_rate": growth_rate,
            "headroom_percent": headroom_percent,
            "projections": [],
            "scaling_triggers": []
        }

    def create_service_catalog(self, services=None):
        return {
            "services": services or [],
            "ownership_model": "drei",
            "classification": ["tier_1", "tier_2", "tier_3"]
        }

    def create_health_check_endpoint(self, path="/health", checks=None):
        return {
            "path": path,
            "checks": checks or [
                {"name": "liveness", "type": "liveness"},
                {"name": "readiness", "type": "readiness"}
            ],
            "exposed": True,
            "authenticated": False
        }

    def create_synthetic_monitoring(self, name, url, frequency_minutes=5, locations=None):
        return {
            "name": name,
            "target_url": url,
            "frequency_minutes": frequency_minutes,
            "locations": locations or ["us-east-1", "us-west-2", "eu-west-1"],
            "assertions": [
                {"type": "status_code", "expected": 200},
                {"type": "latency", "max_ms": 500}
            ]
        }

    def create_canary_analysis(self, baseline_deployment, canary_deployment, metrics, success_criteria):
        return {
            "baseline": baseline_deployment,
            "canary": canary_deployment,
            "metrics": metrics,
            "success_criteria": success_criteria,
            "promotion_policy": "automatic" if success_criteria["threshold"] > 0.95 else "manual"
        }

    def create_disaster_recovery_plan(self, rpo_hours, rto_hours, test_frequency="quarterly"):
        return {
            "rpo_hours": rpo_hours,
            "rto_hours": rto_hours,
            "test_frequency": test_frequency,
            "recovery_procedures": [],
            "failover_mode": "automated" if rto_hours <= 4 else "manual"
        }

    def create_architecture_review(self, review_type="design", participants=None, criteria=None):
        return {
            "type": review_type,
            "participants": participants or [],
            "criteria": criteria or [
                "reliability",
                "scalability",
                "security",
                "cost_efficiency"
            ],
            "approval_threshold": "unanimous"
        }

    def create_sre_dashboard(self, panels=None):
        return {
            "panels": panels or [
                {"name": "Service Health", "type": "status"},
                {"name": "SLO Status", "type": "slo"},
                {"name": "Error Budget", "type": "budget"},
                {"name": "Incident Rate", "type": "incident"}
            ],
            "refresh_interval": "1m",
            "retention": "30d"
        }
