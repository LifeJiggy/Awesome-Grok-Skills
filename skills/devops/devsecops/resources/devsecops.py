class DevSecOps:
    def __init__(self):
        self.pipeline = {}

    def create_pipeline(self, name, stages=None):
        self.pipeline = {
            "name": name,
            "stages": stages or [],
            "triggers": [],
            "approvals": [],
            "environment": {}
        }
        return self

    def add_stage(self, stage_name, stage_type, actions=None):
        stage = {
            "name": stage_name,
            "type": stage_type,
            "actions": actions or []
        }
        self.pipeline["stages"].append(stage)
        return stage

    def add_sast_scan(self, stage, tool="sonarqube", rules_profile="Sonar way"):
        return {
            "stage": stage,
            "tool": tool,
            "type": "sast",
            "config": {
                "rules_profile": rules_profile,
                "quality_gate": True,
                "fail_on_blocker": True,
                "fail_on_critical": True
            }
        }

    def add_dast_scan(self, stage, tool="owasp_zap", target_url=None):
        return {
            "stage": stage,
            "tool": tool,
            "type": "dast",
            "config": {
                "target_url": target_url,
                "scan_type": "full",
                "passive_scan": True,
                "active_scan": True,
                "alert_threshold": "Medium"
            }
        }

    def add_sca_scan(self, stage, tool="snyk", severity_threshold="medium"):
        return {
            "stage": stage,
            "tool": tool,
            "type": "sca",
            "config": {
                "severity_threshold": severity_threshold,
                "fail_on_vulnerability": True,
                "license_check": True
            }
        }

    def add_container_scan(self, stage, tool="trivy", fail_on_critical=True):
        return {
            "stage": stage,
            "tool": tool,
            "type": "container",
            "config": {
                "fail_on_critical": fail_on_critical,
                "severity": ["CRITICAL", "HIGH", "MEDIUM"],
                "ignore_unfixed": False
            }
        }

    def add_infra_scan(self, stage, tool="checkov", policy_pack="aws-cis"):
        return {
            "stage": stage,
            "tool": tool,
            "type": "infrastructure",
            "config": {
                "policy_pack": policy_pack,
                "output_format": "json",
                "fail_on": "high"
            }
        }

    def add_secret_scan(self, stage, tool="gitleaks", rules="default"):
        return {
            "stage": stage,
            "tool": tool,
            "type": "secret",
            "config": {
                "rules": rules,
                "fail_on_secret": True,
                "verbose": True
            }
        }

    def configure_policy_gate(self, gate_name, conditions=None, action="fail"):
        return {
            "name": gate_name,
            "conditions": conditions or [],
            "action": action,
            "override_role": None
        }

    def create_compliance_check(self, standard="SOC2", controls=None):
        return {
            "standard": standard,
            "controls": controls or [],
            "automated": True,
            "evidence_collection": True
        }

    def configure_shift_left_metrics(self):
        return {
            "metrics": [
                "mean_time_to_detect",
                "mean_time_to_remediate",
                "security_coverage_percent",
                "vulnerability_age"
            ],
            "dashboard": True,
            "reporting": "weekly"
        }

    def create_security_chatbot(self, name, platform="slack", responders=None):
        return {
            "name": name,
            "platform": platform,
            "responders": responders or ["security-team"],
            "commands": ["scan", "report", "block"],
            "auto_response": True
        }

    def add_approval_gate(self, stage, approvers=None, timeout_hours=24):
        approval = {
            "stage": stage,
            "approvers": approvers or ["security-review"],
            "timeout_hours": timeout_hours,
            "auto_approve_emergency": False
        }
        self.pipeline["approvals"].append(approval)
        return approval

    def configure_security_feedback(self, channel="slack", report_format="html"):
        return {
            "channel": channel,
            "report_format": report_format,
            "include_metrics": True,
            "include_trends": True
        }

    def create_vulnerability_triage(self, workflow="default", slas=None):
        return {
            "workflow": workflow,
            "slas": slas or [
                {"severity": "critical", "hours": 4},
                {"severity": "high", "hours": 24},
                {"severity": "medium", "hours": 72},
                {"severity": "low", "hours": 720}
            ],
            "escalation": {"enabled": True}
        }

    def add_security_testing_environment(self, env_name, isolation_level="network"):
        return {
            "name": env_name,
            "isolation": isolation_level,
            "ephemeral": True,
            "cleanup": "automatic"
        }

    def create_security_metrics_dashboard(self, panels=None):
        return {
            "panels": panels or [
                {"name": "Open Vulnerabilities", "query": "count(vulnerabilities{status=open})"},
                {"name": "MTTD", "query": "avg(mttd_hours)"},
                {"name": "MTTR", "query": "avg(mttr_hours)"},
                {"name": "Security Coverage", "query": "security_coverage_percent"}
            ],
            "refresh_interval": "5m",
            "retention": "30d"
        }

    def configure_pen_test_schedule(self, frequency="quarterly", scope="full"):
        return {
            "frequency": frequency,
            "scope": scope,
            "providers": ["internal", "external"],
            "reporting": {"formats": ["pdf", "html"], "distribution": ["security", "leadership"]}
        }
