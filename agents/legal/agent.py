"""Legal Agent for contract management"""
from typing import Dict, List
from datetime import datetime

class LegalManager:
    def __init__(self): self.contracts = {}; self.compliance = {}; self.docusign = {}
    def create_contract(self, title: str, parties: List[str], terms: Dict): 
        cid = f"CON_{len(self.contracts)+1}"
        self.contracts[cid] = {"title": title, "parties": parties, "terms": terms, "status": "draft"}
        return self.contracts[cid]
    def generate_nda(self, party1: str, party2: str, duration: int): 
        return self.create_contract("NDA", [party1, party2], {"duration_years": duration, "confidential": True})
    def check_compliance(self, regulation: str, requirements: List[str]): 
        self.compliance[regulation] = {"checked": datetime.now(), "status": "compliant"}
        return {"regulation": regulation, "compliant": True}
    def request_signature(self, contract_id: str, signer: str): 
        if contract_id in self.contracts:
            self.docusign[contract_id] = {"signer": signer, "sent": datetime.now(), "status": "pending"}
        return self.docusign
    def get_contract_status(self): 
        return {"total": len(self.contracts), "draft": sum(1 for c in self.contracts.values() if c["status"]=="draft")}

if __name__ == "__main__":
    legal = LegalManager()
    nda = legal.generate_nda("Company A", "Company B", 2)
    legal.check_compliance("GDPR", ["data_protection", "consent"])
    legal.request_signature(nda["id"], "ceo@company.com")
    print(legal.get_contract_status())
