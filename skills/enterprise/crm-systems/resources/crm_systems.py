class CRMSystem:
    def __init__(self, platform="salesforce"):
        self.platform = platform
        self.modules = {}

    def configure_sales_cloud(self):
        self.modules["sales"] = {
            "leads": {"status": ["new", "contacted", "qualified", "converted"]},
            "opportunities": {"stages": ["prospecting", "qualification", "proposal", "negotiation", "closed"]},
            "accounts": {"types": ["prospect", "customer", "partner"]},
            "contacts": {"roles": ["decision maker", "influencer", "champion"]}
        }
        return self

    def configure_service_cloud(self):
        self.modules["service"] = {
            "cases": {"priority": ["low", "medium", "high", "critical"]},
            " entitlements": {"types": ["phone", "email", "chat"]},
            "knowledge_base": {"article_types": ["faq", "how-to", "troubleshooting"]},
            "live_agent": {"availability_status": ["available", "away", "offline"]}
        }
        return self

    def configure_marketing_cloud(self):
        self.modules["marketing"] = {
            "campaigns": {"types": ["email", "social", "event", "advertising"]},
            "journeys": {"status": ["draft", "active", "paused", "completed"]},
            "segments": {"criteria": ["behavioral", "demographic", "firmographic"]},
            "lead_scoring": {"weights": {"engagement": 0.4, "demographics": 0.3, "fit": 0.3}}
        }
        return self

    def create_lead(self, first_name, last_name, company, email, source="web"):
        return {
            "lead_id": "LD-001",
            "first_name": first_name,
            "last_name": last_name,
            "company": company,
            "email": email,
            "phone": None,
            "source": source,
            "status": "new",
            "score": 0,
            "owner": None,
            "created_date": "2024-01-15"
        }

    def create_opportunity(self, name, account_id, stage, amount, close_date):
        return {
            "opp_id": "OPP-001",
            "name": name,
            "account_id": account_id,
            "stage": stage,
            "amount": amount,
            "probability": self._get_probability(stage),
            "close_date": close_date,
            "type": "new business",
            "lead_source": None,
            "next_step": None
        }

    def _get_probability(self, stage):
        probabilities = {
            "prospecting": 0.10,
            "qualification": 0.20,
            "proposal": 0.50,
            "negotiation": 0.70,
            "closed_won": 1.00,
            "closed_lost": 0
        }
        return probabilities.get(stage, 0)

    def create_case(self, subject, description, priority, account_id, contact_id):
        return {
            "case_id": "CS-001",
            "subject": subject,
            "description": description,
            "priority": priority,
            "status": "new",
            "origin": "web",
            "account_id": account_id,
            "contact_id": contact_id,
            "product": None,
            "entitlement_id": None,
            "owner": None
        }

    def setup_automation(self, automation_type="flow"):
        return {
            "type": automation_type,
            "triggers": [],
            "actions": [],
            "active": True,
            "last_modified_date": "2024-01-15"
        }

    def configure_integration(self, target_system, integration_type="api"):
        return {
            "target": target_system,
            "type": integration_type,
            "endpoint": None,
            "authentication": {"type": "oauth2", "scope": None},
            "sync_direction": "bidirectional",
            "frequency": "realtime"
        }

    def create_report(self, report_type, filters=None):
        return {
            "report_id": "RPT-001",
            "type": report_type,
            "format": "tabular",
            "filters": filters or [],
            "groupings": [],
            "aggregates": [],
            "schedule": None
        }

    def configure_analytics(self, dashboard_type="sales"):
        return {
            "dashboard_id": "DB-001",
            "type": dashboard_type,
            "components": [],
            "refresh_frequency": "hourly",
            "sharing": {"type": "private", "shared_with": []}
        }

    def setup_data_model(self, custom_objects=None):
        return {
            "standard_objects": [],
            "custom_objects": custom_objects or [],
            "relationships": [],
            "validation_rules": [],
            "lookup_filters": []
        }

    def configure_security_model(self):
        return {
            "profiles": [],
            "permission_sets": [],
            "sharing_rules": {"org_default": "private"},
            "role_hierarchy": [],
            "field_level_security": {}
        }

    def calculate_pipeline_forecast(self, opportunities):
        return {
            "total_pipeline": sum(o["amount"] for o in opportunities),
            "weighted_pipeline": sum(o["amount"] * o["probability"] for o in opportunities),
            "by_stage": {},
            "by_rep": {},
            "forecast_period": "Q1 2024",
            "commit": 0,
            "best_case": 0,
            "pipeline_coverage": 0
        }

    def create_campaign(self, name, type, status, budget, start_date, end_date):
        return {
            "campaign_id": "CMP-001",
            "name": name,
            "type": type,
            "status": status,
            "budget": budget,
            "start_date": start_date,
            "end_date": end_date,
            "expected_revenue": 0,
            "actual_cost": 0,
            "leads_generated": 0,
            "opportunities_created": 0
        }
