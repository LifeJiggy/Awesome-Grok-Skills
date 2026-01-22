"""
Contract Automation Pipeline
Legal tech and smart contract automation
"""

import hashlib
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class ContractStatus(Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    EXECUTED = "executed"
    EXPIRED = "expired"
    TERMINATED = "terminated"


class ClauseType(Enum):
    DEFINITIONS = "definitions"
    PAYMENT_TERMS = "payment_terms"
    CONFIDENTIALITY = "confidentiality"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    LIABILITY = "liability"
    TERMINATION = "termination"
    DISPUTE_RESOLUTION = "dispute_resolution"
    GOVERNING_LAW = "governing_law"


@dataclass
class ContractClause:
    clause_id: str
    clause_type: ClauseType
    content: str
    version: int = 1
    effective_date: datetime = field(default_factory=datetime.now)
    parameters: Dict = field(default_factory=dict)


@dataclass
class Contract:
    contract_id: str
    title: str
    contract_type: str
    parties: List[Dict]
    status: ContractStatus
    clauses: List[ContractClause]
    created_date: datetime
    effective_date: datetime
    expiration_date: Optional[datetime]
    metadata: Dict = field(default_factory=dict)


class ContractGenerator:
    """Generate legal contracts from templates"""
    
    def __init__(self):
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load contract templates"""
        self.templates = {
            "nda": self._nda_template,
            "service_agreement": self._service_agreement_template,
            "employment": self._employment_template,
            "lease": self._lease_template
        }
    
    def generate(self, 
                template_type: str,
                parameters: Dict) -> Contract:
        """Generate contract from template"""
        if template_type not in self.templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        generator = self.templates[template_type]
        return generator(parameters)
    
    def _nda_template(self, params: Dict) -> Contract:
        """Generate NDA template"""
        contract_id = f"NDA{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8].upper()}"
        
        clauses = [
            ContractClause(
                clause_id="DEF001",
                clause_type=ClauseType.DEFINITIONS,
                content=f"This Non-Disclosure Agreement is entered into by and between {params.get('party1', 'Disclosing Party')} and {params.get('party2', 'Receiving Party')}."
            ),
            ContractClause(
                clause_id="CONF001",
                clause_type=ClauseType.CONFIDENTIALITY,
                content="The Receiving Party agrees to hold all Confidential Information in strict confidence."
            ),
            ContractClause(
                clause_id="TERM001",
                clause_type=ClauseType.TERMINATION,
                content="This Agreement shall remain in effect for a period of {params.get('duration', '2')} years."
            )
        ]
        
        return Contract(
            contract_id=contract_id,
            title="Non-Disclosure Agreement",
            contract_type="nda",
            parties=[
                {"name": params.get("party1", "Party A"), "role": "disclosing_party"},
                {"name": params.get("party2", "Party B"), "role": "receiving_party"}
            ],
            status=ContractStatus.DRAFT,
            clauses=clauses,
            created_date=datetime.now(),
            effective_date=datetime.now(),
            expiration_date=datetime.now() + timedelta(days=params.get("duration_years", 2) * 365)
        )
    
    def _service_agreement_template(self, params: Dict) -> Contract:
        """Generate service agreement template"""
        contract_id = f"SA{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8].upper()}"
        
        return Contract(
            contract_id=contract_id,
            title="Service Agreement",
            contract_type="service_agreement",
            parties=[
                {"name": params.get("client", "Client"), "role": "client"},
                {"name": params.get("provider", "Service Provider"), "role": "provider"}
            ],
            status=ContractStatus.DRAFT,
            clauses=[],
            created_date=datetime.now(),
            effective_date=datetime.now(),
            expiration_date=datetime.now() + timedelta(days=365)
        )
    
    def _employment_template(self, params: Dict) -> Contract:
        """Generate employment agreement template"""
        return Contract(
            contract_id=f"EMP{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8].upper()}",
            title="Employment Agreement",
            contract_type="employment",
            parties=[
                {"name": params.get("employer", "Employer"), "role": "employer"},
                {"name": params.get("employee", "Employee"), "role": "employee"}
            ],
            status=ContractStatus.DRAFT,
            clauses=[],
            created_date=datetime.now(),
            effective_date=datetime.now(),
            expiration_date=None
        )
    
    def _lease_template(self, params: Dict) -> Contract:
        """Generate lease agreement template"""
        return Contract(
            contract_id=f"LEASE{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8].upper()}",
            title="Lease Agreement",
            contract_type="lease",
            parties=[
                {"name": params.get("landlord", "Landlord"), "role": "landlord"},
                {"name": params.get("tenant", "Tenant"), "role": "tenant"}
            ],
            status=ContractStatus.DRAFT,
            clauses=[],
            created_date=datetime.now(),
            effective_date=datetime.now(),
            expiration_date=datetime.now() + timedelta(days=365)
        )


class ComplianceChecker:
    """Check contract compliance"""
    
    def __init__(self):
        self.rules = {}
        self.violations = []
    
    def add_rule(self, rule_name: str, rule_func):
        """Add compliance rule"""
        self.rules[rule_name] = rule_func
    
    def check_contract(self, contract: Contract) -> Dict:
        """Check contract for compliance"""
        results = {}
        all_passed = True
        
        for rule_name, rule_func in self.rules.items():
            try:
                passed = rule_func(contract)
                results[rule_name] = {"passed": passed, "details": ""}
                if not passed:
                    all_passed = False
            except Exception as e:
                results[rule_name] = {"passed": False, "details": str(e)}
                all_passed = False
        
        return {
            "contract_id": contract.contract_id,
            "compliance_status": "passed" if all_passed else "failed",
            "results": results
        }
    
    def required_clauses_check(self, contract: Contract) -> bool:
        """Check for required clauses"""
        required_types = {
            "nda": [ClauseType.CONFIDENTIALITY, ClauseType.TERMINATION],
            "service_agreement": [ClauseType.PAYMENT_TERMS, ClauseType.LIABILITY],
            "employment": [ClauseType.LIABILITY, ClauseType.TERMINATION]
        }
        
        required = required_types.get(contract.contract_type, [])
        clause_types = {c.clause_type for c in contract.clauses}
        
        return all(r in clause_types for r in required)
    
    def expiration_check(self, contract: Contract) -> bool:
        """Check if contract is expired"""
        if contract.expiration_date is None:
            return True
        return contract.expiration_date > datetime.now()
    
    def signature_check(self, contract: Contract) -> bool:
        """Check if all parties have signed"""
        return all(
            party.get("signed", False) 
            for party in contract.parties
        )


class ClauseExtractor:
    """Extract and analyze contract clauses"""
    
    def __init__(self):
        self.parsers = {}
    
    def extract_liabilities(self, contract: Contract) -> List[Dict]:
        """Extract liability clauses"""
        liabilities = []
        for clause in contract.clauses:
            if clause.clause_type == ClauseType.LIABILITY:
                liabilities.append({
                    "clause_id": clause.clause_id,
                    "content": clause.content,
                    "limit": self._extract_liability_limit(clause.content)
                })
        return liabilities
    
    def _extract_liability_limit(self, text: str) -> Optional[float]:
        """Extract liability limit from text"""
        import re
        patterns = [
            r"\$\s*([0-9,]+)",
            r"not to exceed\s*([0-9,]+)",
            r"limit.*?([0-9,]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1).replace(",", ""))
        
        return None
    
    def extract_dates(self, contract: Contract) -> List[Dict]:
        """Extract all dates from contract"""
        dates = []
        for clause in contract.clauses:
            if "effective date" in clause.content.lower():
                dates.append({
                    "clause_id": clause.clause_id,
                    "type": "effective_date",
                    "description": clause.content[:100]
                })
        return dates


if __name__ == "__main__":
    generator = ContractGenerator()
    compliance = ComplianceChecker()
    extractor = ClauseExtractor()
    
    compliance.add_rule("required_clauses", compliance.required_clauses_check)
    compliance.add_rule("expiration", compliance.expiration_check)
    compliance.add_rule("signatures", compliance.signature_check)
    
    nda = generator.generate("nda", {
        "party1": "Acme Corp",
        "party2": "Tech Startup Inc",
        "duration": 2
    })
    
    compliance_result = compliance.check_contract(nda)
    liabilities = extractor.extract_liabilities(nda)
    
    print(f"Contract ID: {nda.contract_id}")
    print(f"Status: {nda.status.value}")
    print(f"Compliance: {compliance_result['compliance_status']}")
    print(f"Clauses: {len(nda.clauses)}")
    print(f"Liability clauses: {len(liabilities)}")
