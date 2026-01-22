"""Integration Agent for system integration"""
from typing import Dict, List
from datetime import datetime

class IntegrationManager:
    def __init__(self): self.connections = {}; self.api_mappings = {}; self.webhooks = {}
    def add_connection(self, source: str, dest: str, auth_type: str): 
        self.connections[f"{source}->{dest}"] = {"auth": auth_type, "status": "active"}
        return self.connections
    def create_api_mapping(self, source_api: str, dest_api: str, field_map: Dict): 
        self.api_mappings[f"{source_api}:{dest_api}"] = field_map
        return self.api_mappings
    def register_webhook(self, url: str, events: List[str], secret: str): 
        self.webhooks[url] = {"events": events, "secret": secret, "active": True}
        return self.webhooks
    def sync_data(self, source: str, dest: str, data: Dict): 
        key = f"{source}->{dest}"
        if key in self.api_mappings:
            mapped = {self.api_mappings[key].get(k, k): v for k, v in data.items()}
            return {"synced": mapped, "timestamp": datetime.now()}
        return {"error": "No mapping found"}
    def get_integration_health(self): 
        return {"total": len(self.connections), "active": sum(1 for v in self.connections.values() if v["status"]=="active")}

if __name__ == "__main__":
    im = IntegrationManager()
    im.add_connection("Salesforce", "HubSpot", "oauth2")
    im.create_api_mapping("salesforce", "hubspot", {"email": "email", "name": "full_name"})
    result = im.sync_data("Salesforce", "HubSpot", {"email": "test@test.com", "name": "John"})
    print(f"Integration health: {im.get_integration_health()}")
