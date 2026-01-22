#!/usr/bin/env python3
"""
InsurTech - Insurance Technology Implementation
Underwriting, claims, and insurance operations.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
import random

class InsuranceType(Enum):
    AUTO = "auto"
    HOME = "home"
    LIFE = "life"
    HEALTH = "health"
    TRAVEL = "travel"
    PROPERTY = "property"
    BUSINESS = "business"
    PET = "pet"

class CoverageLevel(Enum):
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ULTIMATE = "ultimate"

class ClaimStatus(Enum):
    FILED = "filed"
    INVESTIGATION = "investigation"
    APPROVED = "approved",
    DENIED = "denied"
    PAID = "paid"
    CLOSED = "closed"

@dataclass
class Policy:
    id: str
    policy_number: str
    insured_name: str
    insurance_type: InsuranceType
    coverage_level: CoverageLevel
    premium: float
    deductible: float
    coverage_limit: float
    start_date: datetime
    end_date: datetime
    status: str

@dataclass
class Claim:
    id: str
    policy_id: str
    claim_type: str
    amount_claimed: float
    status: ClaimStatus
    filed_date: datetime
    investigation_notes: List[str]
    damage_assessment: Dict[str, Any]

class UnderwritingEngine:
    """AI-powered insurance underwriting."""
    
    def __init__(self):
        self.risk_models: Dict[str, Dict] = {}
        self.quotes: List[Dict] = []
    
    def calculate_risk_score(self, applicant_data: Dict,
                            insurance_type: InsuranceType) -> Dict[str, Any]:
        """Calculate risk score for applicant."""
        base_score = random.uniform(50, 150)
        
        risk_factors = {
            'age': random.uniform(0.8, 1.2),
            'location': random.uniform(0.9, 1.1),
            'history': random.uniform(0.85, 1.15),
            'behavior': random.uniform(0.9, 1.1)
        }
        
        adjusted_score = base_score * \
                        risk_factors['age'] * \
                        risk_factors['location'] * \
                        risk_factors['history'] * \
                        risk_factors['behavior']
        
        return {
            'insurance_type': insurance_type.value,
            'base_risk_score': round(base_score, 1),
            'adjusted_risk_score': round(adjusted_score, 1),
            'risk_tier': 'low' if adjusted_score < 80 else 'medium' if adjusted_score < 120 else 'high',
            'risk_factors': risk_factors,
            'confidence': round(random.uniform(75, 95), 1),
            'recommendations': [
                'Consider higher deductible for premium pricing',
                'Offer loyalty discount',
                'Require additional documentation'
            ]
        }
    
    def generate_quote(self, applicant_data: Dict,
                      insurance_type: InsuranceType,
                      coverage_level: CoverageLevel) -> Dict[str, Any]:
        """Generate insurance quote."""
        risk = self.calculate_risk_score(applicant_data, insurance_type)
        
        base_premiums = {
            InsuranceType.AUTO: 1200,
            InsuranceType.HOME: 1500,
            InsuranceType.LIFE: 800,
            InsuranceType.HEALTH: 2400,
            InsuranceType.TRAVEL: 150,
            InsuranceType.PROPERTY: 2000,
            InsuranceType.BUSINESS: 3500,
            InsuranceType.PET: 400
        }
        
        coverage_multipliers = {
            CoverageLevel.BASIC: 1.0,
            CoverageLevel.STANDARD: 1.5,
            CoverageLevel.PREMIUM: 2.0,
            CoverageLevel.ULTIMATE: 3.0
        }
        
        base_premium = base_premiums.get(insurance_type, 1000)
        premium = base_premium * coverage_multipliers[coverage_level]
        
        if risk['risk_tier'] == 'high':
            premium *= 1.3
        elif risk['risk_tier'] == 'low':
            premium *= 0.9
        
        quote = {
            'quote_id': f"QT_{len(self.quotes) + 1}",
            'insurance_type': insurance_type.value,
            'coverage_level': coverage_level.value,
            'base_premium': round(premium, 2),
            'monthly_premium': round(premium / 12, 2),
            'deductible': random.randint(500, 5000),
            'coverage_limit': random.randint(100000, 1000000),
            'risk_score': risk['adjusted_risk_score'],
            'valid_until': (datetime.now() + timedelta(days=30)).isoformat(),
            'discounts': [
                {'type': 'Multi-policy', 'amount': round(premium * 0.1, 2)},
                {'type': 'Loyalty', 'amount': round(premium * 0.05, 2)}
            ],
            'features': self._get_coverage_features(insurance_type, coverage_level)
        }
        
        self.quotes.append(quote)
        return quote
    
    def _get_coverage_features(self, insurance_type: InsuranceType,
                               level: CoverageLevel) -> List[str]:
        """Get coverage features based on type and level."""
        features = {
            InsuranceType.AUTO: ['Liability', 'Collision', 'Comprehensive'],
            InsuranceType.HOME: ['Dwelling', 'Contents', 'Liability'],
            InsuranceType.LIFE: ['Death benefit', 'Terminal illness'],
            InsuranceType.HEALTH: ['Hospital', 'Outpatient', 'Prescription']
        }
        
        basic_features = features.get(insurance_type, ['Basic coverage'])
        
        if level in [CoverageLevel.PREMIUM, CoverageLevel.ULTIMATE]:
            basic_features.extend(['Add-ons', 'Worldwide coverage', '24/7 support'])
        
        return basic_features

class ClaimsProcessor:
    """Automated insurance claims processing."""
    
    def __init__(self):
        self.claims: Dict[str, Claim] = {}
        self.fraud_checks: List[Dict] = []
    
    def file_claim(self, policy_id: str, claim_type: str,
                  amount: float) -> Claim:
        """File new insurance claim."""
        claim = Claim(
            id=f"CLM_{len(self.claims) + 1}",
            policy_id=policy_id,
            claim_type=claim_type,
            amount_claimed=amount,
            status=ClaimStatus.FILED,
            filed_date=datetime.now(),
            investigation_notes=[],
            damage_assessment={}
        )
        self.claims[claim.id] = claim
        return claim
    
    def assess_damage(self, claim_id: str,
                     damage_data: Dict) -> Dict[str, Any]:
        """Assess claim damage using AI."""
        assessment = {
            'claim_id': claim_id,
            'estimated_damage': damage_data.get('amount', random.uniform(1000, 50000)),
            'damage_categories': {
                'structural': random.uniform(0, 10000),
                'contents': random.uniform(0, 5000),
                'additional': random.uniform(0, 2000)
            },
            'severity_level': random.choice(['Minor', 'Moderate', 'Major', 'Total Loss']),
            'repair_time_estimate': f"{random.randint(1, 30)} days",
            'ai_confidence': round(random.uniform(85, 98), 1),
            'recommended_action': random.choice(['Approve', 'Review', 'Investigate'])
        }
        
        if claim_id in self.claims:
            self.claims[claim_id].damage_assessment = assessment
            self.claims[claim_id].status = ClaimStatus.INVESTIGATION
        
        return assessment
    
    def detect_fraud(self, claim_id: str) -> Dict[str, Any]:
        """Detect potential fraud in claim."""
        indicators = []
        risk_score = 0
        
        if random.random() < 0.1:
            indicators.append('Suspicious claim pattern detected')
            risk_score += 30
        if random.random() < 0.15:
            indicators.append('Unusual filing timing')
            risk_score += 20
        if random.random() < 0.1:
            indicators.append('Inconsistent damage documentation')
            risk_score += 25
        
        result = {
            'claim_id': claim_id,
            'fraud_risk_score': min(100, risk_score),
            'risk_level': 'high' if risk_score > 50 else 'medium' if risk_score > 25 else 'low',
            'indicators': indicators,
            'recommended_action': 'Manual review' if risk_score > 30 else 'Auto-approve',
            'confidence': round(random.uniform(80, 95), 1)
        }
        
        self.fraud_checks.append(result)
        return result
    
    def process_payout(self, claim_id: str) -> Dict[str, Any]:
        """Process claim payout."""
        if claim_id not in self.claims:
            return {'error': 'Claim not found'}
        
        claim = self.claims[claim_id]
        assessment = claim.damage_assessment
        
        approved_amount = assessment.get('estimated_damage', 0) * random.uniform(0.8, 1.0)
        
        return {
            'claim_id': claim_id,
            'approved_amount': round(approved_amount, 2),
            'deductible': 500,
            'net_payout': round(approved_amount - 500, 2),
            'payment_method': 'Direct deposit',
            'estimated_delivery': '2-3 business days',
            'status': ClaimStatus.PAID
        }

class CustomerManager:
    """Manages insurance customers."""
    
    def __init__(self):
        self.customers: Dict[str, Dict] = []
        self.policies: Dict[str, Policy] = {}
    
    def onboard_customer(self, customer_data: Dict) -> Dict[str, Any]:
        """Onboard new customer."""
        customer_id = f"CUST_{len(self.customers) + 1}"
        
        return {
            'customer_id': customer_id,
            'onboarding_status': 'completed',
            'kyc_verified': True,
            'eligible_products': ['auto', 'home', 'life'],
            'risk_profile': random.choice(['conservative', 'moderate', 'aggressive']),
            'recommended_coverage': self._get_recommendations(customer_data),
            'next_steps': ['Upload documents', 'Select coverage', 'Complete payment']
        }
    
    def _get_recommendations(self, data: Dict) -> List[str]:
        """Get coverage recommendations."""
        return [
            'Consider increasing liability limits',
            'Add umbrella policy for additional protection',
            'Bundle home and auto for 15% discount'
        ]
    
    def get_customer_lifetime_value(self, customer_id: str) -> Dict[str, Any]:
        """Calculate customer lifetime value."""
        return {
            'customer_id': customer_id,
            'current_policies': random.randint(1, 4),
            'years_with_company': random.randint(1, 15),
            'total_premiums_paid': round(random.uniform(5000, 50000), 2),
            'claims_filed': random.randint(0, 5),
            'claims_paid': round(random.uniform(0, 20000), 2),
            'ltv_estimate': round(random.uniform(10000, 100000), 2),
            'churn_risk': round(random.uniform(5, 30), 1),
            'retention_recommendations': [
                'Offer loyalty discount',
                'Proactive customer outreach',
                'Review coverage annually'
            ]
        }
    
    def renew_policy(self, policy_id: str) -> Dict[str, Any]:
        """Process policy renewal."""
        if policy_id not in self.policies:
            return {'error': 'Policy not found'}
        
        policy = self.policies[policy_id]
        renewal_premium = policy.premium * random.uniform(0.95, 1.05)
        
        return {
            'policy_id': policy_id,
            'renewal_premium': round(renewal_premium, 2),
            'coverage_changes': [
                'Increased liability limits',
                'Added roadside assistance'
            ],
            'renewal_bonus': round(renewal_premium * 0.05, 2),
            'valid_until': (datetime.now() + timedelta(days=365)).isoformat(),
            'action_required': 'Confirm renewal'
        }

class ProductDesigner:
    """Designs insurance products."""
    
    def __init__(self):
        self.products: List[Dict] = []
    
    def design_micro_insurance(self, target_market: str,
                              coverage_type: str) -> Dict[str, Any]:
        """Design micro-insurance product."""
        product = {
            'product_name': f'{target_market} {coverage_type} Protection',
            'target_market': target_market,
            'coverage_type': coverage_type,
            'premium': round(random.uniform(1, 10), 2),
            'coverage_period': 'Daily/Weekly/Monthly',
            'coverage_limit': random.randint(1000, 10000),
            'distribution': ['Mobile app', 'API', 'Retail partners'],
            'claims_process': 'Instant auto-approval',
            'target_profit_margin': round(random.uniform(15, 25), 1)
        }
        self.products.append(product)
        return product
    
    def design_parametric_insurance(self, trigger_event: str,
                                   payout_amount: float) -> Dict[str, Any]:
        """Design parametric insurance product."""
        return {
            'product_name': f'{trigger_event} Parametric Cover',
            'trigger': trigger_event,
            'payout_amount': payout_amount,
            'trigger_threshold': random.uniform(0.1, 0.5),
            'verification': 'Satellite/IoT based',
            'payout_speed': 'Within 24 hours',
            'premium_rate': round(random.uniform(2, 8), 2),
            'use_cases': [
                'Flight delay insurance',
                'Weather-related crop insurance',
                'Event cancellation'
            ]
        }

class InsurTechAgent:
    """Main InsurTech agent."""
    
    def __init__(self):
        self.underwriting = UnderwritingEngine()
        self.claims = ClaimsProcessor()
        self.customers = CustomerManager()
        self.products = ProductDesigner()
    
    def create_insurance_package(self, customer_data: Dict,
                                insurance_types: List[str]) -> Dict[str, Any]:
        """Create comprehensive insurance package."""
        quotes = []
        total_premium = 0
        
        for ins_type in insurance_types:
            quote = self.underwriting.generate_quote(
                customer_data,
                InsuranceType[ins_type.upper()],
                CoverageLevel.STANDARD
            )
            quotes.append({
                'type': ins_type,
                'quote': quote
            })
            total_premium += quote['monthly_premium']
        
        return {
            'package_id': f"PKG_{random.randint(1000, 9999)}",
            'customer': customer_data.get('name', 'Customer'),
            'quotes': quotes,
            'total_monthly_premium': round(total_premium, 2),
            'bundle_discount': round(total_premium * 0.1, 2),
            'final_premium': round(total_premium * 0.9, 2),
            'recommended_products': self.products.design_micro_insurance(
                'young_professionals',
                'health'
            )
        }
    
    def file_claim_and_track(self, policy_id: str,
                            claim_type: str,
                            amount: float) -> Dict[str, Any]:
        """File claim and track through process."""
        claim = self.claims.file_claim(policy_id, claim_type, amount)
        assessment = self.claims.assess_damage(claim.id, {'amount': amount})
        fraud_check = self.claims.detect_fraud(claim.id)
        
        return {
            'claim_id': claim.id,
            'status': claim.status.value,
            'damage_assessment': assessment,
            'fraud_check': fraud_check,
            'next_steps': [
                'Complete documentation',
                'Schedule inspection if needed',
                'Await approval'
            ],
            'estimated_resolution': f"{random.randint(3, 14)} days"
        }
    
    def get_insurtech_dashboard(self) -> Dict[str, Any]:
        """Get InsurTech dashboard."""
        return {
            'underwriting': {
                'quotes_generated': len(self.underwriting.quotes)
            },
            'claims': {
                'claims_filed': len(self.claims.claims),
                'fraud_checks': len(self.claims.fraud_checks)
            },
            'customers': {
                'total_customers': len(self.customers.customers),
                'policies': len(self.customers.policies)
            },
            'products': {
                'products_designed': len(self.products.products)
            }
        }

def main():
    """Main entry point."""
    agent = InsurTechAgent()
    
    package = agent.create_insurance_package(
        {'name': 'John Doe', 'age': 35, 'location': 'New York'},
        ['auto', 'home']
    )
    print(f"Insurance package: {package}")

if __name__ == "__main__":
    main()
