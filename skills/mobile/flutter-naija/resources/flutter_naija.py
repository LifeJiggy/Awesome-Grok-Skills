"""
Flutter Naija Development
Flutter with Nigerian context and localization
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class NigerianBank(Enum):
    FIRST_BANK = "011"
    ZENITH_BANK = "057"
    GTBANK = "058"
    ACCESS_BANK = "044"
    UBA = "033"
    ECOBANK = "050"
    STERLING_BANK = "232"
    FIDELITY_BANK = "070"
    UNION_BANK = "032"
    KEYSTONE = "082"


@dataclass
class NigerianPhoneNumber:
    number: str
    operator: str = ""
    is_valid: bool = False
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        """Validate Nigerian phone number"""
        import re
        patterns = [
            r"^234[789]\d{9}$",
            r"^0[789]\d{9}$",
        ]
        for pattern in patterns:
            if re.match(pattern, self.number):
                self.is_valid = True
                if self.number.startswith("234"):
                    prefix = self.number[3:6]
                else:
                    prefix = self.number[1:4]
                self.operator = self._get_operator(prefix)
                break
    
    def _get_operator(self, prefix: str) -> str:
        """Get operator from prefix"""
        operators = {
            "080": "MTN",
            "081": "MTN",
            "090": "MTN",
            "070": "Airtel",
            "080": "Glo",
            "081": "Glo",
            "090": "Glo",
            "080": "9mobile",
            "081": "9mobile",
            "090": "9mobile"
        }
        return operators.get(prefix, "Unknown")


class FlutterNaijaUtils:
    """Flutter utilities with Nigerian context"""
    
    @staticmethod
    def format_naira(amount: float) -> str:
        """Format amount in Nigerian Naira"""
        return "₦{:,.2f}".format(amount)
    
    @staticmethod
    def validate_bvn(bvn: str) -> bool:
        """Validate Bank Verification Number"""
        return len(bvn) == 11 and bvn.isdigit()
    
    @staticmethod
    def validate_account_number(account: str, bank_code: str) -> bool:
        """Validate bank account number"""
        if len(account) != 10:
            return False
        if not account.isdigit():
            return False
        return bank_code in [b.value for b in NigerianBank]
    
    @staticmethod
    def generate_ussd_code(bank_code: str, account: str) -> str:
        """Generate USSD code for banking"""
        return f"*{bank_code}*{account}#"
    
    @staticmethod
    def format_business_name(name: str) -> str:
        """Format business name for CAC registration"""
        words = name.strip().split()
        return " ".join([w.capitalize() for w in words])


class LocalizationGenerator:
    """Generate Nigerian English localization"""
    
    def __init__(self):
        self.translations = {
            "en_NG": {
                "app_title": "My App",
                "welcome": "Welcome to {app_name}",
                "login": "Sign In",
                "login_button": "Proceed",
                "register": "Create Account",
                "forgot_password": "Forgot Password?",
                "reset_password": "Reset Password",
                "email": "Email Address",
                "password": "Password",
                "confirm_password": "Confirm Password",
                "phone": "Phone Number",
                "otp": "One Time Password",
                "verify": "Verify",
                "resend_otp": "Resend OTP",
                "bank_transfer": "Bank Transfer",
                "ussd_payment": "USSD Payment",
                "card_payment": "Card Payment",
                "select_bank": "Select Bank",
                "enter_amount": "Enter Amount",
                "payment_reference": "Payment Reference",
                "transaction_successful": "Transaction Successful",
                "transaction_failed": "Transaction Failed",
                "insufficient_funds": "Insufficient Funds",
                "network_error": "Network Error",
                "try_again": "Try Again",
                "cancel": "Cancel",
                "confirm": "Confirm",
                "submit": "Submit",
                "save": "Save",
                "edit": "Edit",
                "delete": "Delete",
                "loading": "Loading...",
                "no_internet": "No Internet Connection",
                "location_permission": "Location Permission Required",
                "camera_permission": "Camera Permission Required",
                "notification_permission": "Enable Notifications",
                "select_date": "Select Date",
                "select_time": "Select Time",
                "ngn_symbol": "₦",
                "transfer_to": "Transfer to",
                "from_account": "From Account",
                "to_account": "To Account",
                "account_number": "Account Number",
                "account_name": "Account Name",
                "bank_name": "Bank Name",
                "bvn_label": "BVN",
                "nin_label": "NIN"
            }
        }
    
    def generate_translations(self, locale: str = "en_NG") -> Dict:
        """Generate translations for locale"""
        return self.translations.get(locale, self.translations["en_NG"])
    
    def generate_ar_translations(self) -> Dict:
        """Generate Arabic translations"""
        return {
            "app_title": "تطبيقي",
            "welcome": "مرحباً بكم في {app_name}",
            "login": "تسجيل الدخول",
            "register": "إنشاء حساب",
            "loading": "جاري التحميل...",
            "ngn_symbol": "₦"
        }


class PaymentIntegration:
    """Nigerian payment gateway integration"""
    
    def __init__(self):
        self.providers = {
            "paystack": {"name": "Paystack", "fee_percent": 1.5},
            "flutterwave": {"name": "Flutterwave", "fee_percent": 1.5},
            "monnify": {"name": "Monnify", "fee_percent": 0.75},
            "stripe": {"name": "Stripe", "fee_percent": 2.9}
        }
    
    def initialize_transaction(self, 
                              provider: str,
                              amount: float,
                              customer_email: str,
                              reference: str = None) -> Dict:
        """Initialize payment transaction"""
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        
        provider_config = self.providers[provider]
        fee = amount * provider_config["fee_percent"] / 100
        
        return {
            "provider": provider,
            "amount": amount,
            "fee": fee,
            "total": amount + fee,
            "currency": "NGN",
            "customer_email": customer_email,
            "reference": reference or f"ref_{hash(str(amount))}",
            "status": "initialized"
        }
    
    def verify_transaction(self, 
                          provider: str,
                          reference: str) -> Dict:
        """Verify transaction status"""
        return {
            "reference": reference,
            "status": "successful",
            "amount": 10000,
            "currency": "NGN"
        }
    
    def calculate_transfer_fee(self, 
                              amount: float,
                              bank_code: str) -> float:
        """Calculate bank transfer fee"""
        if bank_code in ["057", "058", "044"]:
            return 10  # Free or low fee for major banks
        elif amount < 5000:
            return 10
        elif amount < 50000:
            return 25
        else:
            return 50


class BVNValidator:
    """Bank Verification Number validator"""
    
    def __init__(self):
        self.weights = [3, 7, 3, 3, 7, 3, 3, 7, 3, 3, 1]
    
    def validate(self, bvn: str) -> bool:
        """Validate BVN using checksum"""
        if len(bvn) != 11:
            return False
        if not bvn.isdigit():
            return False
        
        try:
            checksum = int(bvn[10])
            calculated = self._calculate_checksum(bvn[:10])
            return checksum == calculated
        except:
            return False
    
    def _calculate_checksum(self, digits: str) -> int:
        """Calculate BVN checksum"""
        total = sum(int(d) * w for d, w in zip(digits, self.weights))
        return total % 10


if __name__ == "__main__":
    flutter_utils = FlutterNaijaUtils()
    localizer = LocalizationGenerator()
    payments = PaymentIntegration()
    bvn = BVNValidator()
    
    phone = NigerianPhoneNumber("08012345678")
    print(f"Phone valid: {phone.is_valid}, Operator: {phone.operator}")
    
    print(f"Naira format: {flutter_utils.format_naira(1500.50)}")
    print(f"BVN valid: {bvn.validate('12345678901')}")
    
    transaction = payments.initialize_transaction(
        "paystack",
        10000,
        "customer@email.com"
    )
    
    translations = localizer.generate_translations()
    print(f"Translation keys: {len(translations)}")
    
    fee = payments.calculate_transfer_fee(10000, "057")
    print(f"Transfer fee: ₦{fee}")
