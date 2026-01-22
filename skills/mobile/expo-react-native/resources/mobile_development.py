"""
Mobile Development Pipeline
Cross-platform mobile app development
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class Platform(Enum):
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"


@dataclass
class MobileConfig:
    app_name: str
    bundle_id: str
    version: str
    min_sdk: int
    target_sdk: int
    permissions: List[str] = None
    
    def __post_init__(self):
        if self.permissions is None:
            self.permissions = ["internet"]


class ExpoRNBuilder:
    """Expo React Native build configuration"""
    
    def __init__(self):
        self.supported_sdk = 49
        self.default_permissions = [
            "CAMERA",
            "CAMERA_ROLL",
            "NOTIFICATIONS",
            "LOCATION"
        ]
    
    def generate_app_json(self, config: MobileConfig) -> Dict:
        """Generate app.json configuration"""
        return {
            "expo": {
                "name": config.app_name,
                "slug": config.app_name.lower().replace(" ", "-"),
                "version": config.version,
                "orientation": "portrait",
                "icon": "./assets/icon.png",
                "userInterfaceStyle": "light",
                "splash": {
                    "image": "./assets/splash.png",
                    "resizeMode": "contain",
                    "backgroundColor": "#ffffff"
                },
                "updates": {
                    "fallbackToCacheTimeout": 0
                },
                "assetBundlePatterns": [
                    "**/*"
                ],
                "ios": {
                    "supportsTablet": True,
                    "bundleIdentifier": config.bundle_id,
                    "infoPlist": {
                        "NSCameraUsageDescription": "This app uses the camera",
                        "NSPhotoLibraryUsageDescription": "This app uses the photo library"
                    }
                },
                "android": {
                    "adaptiveIcon": {
                        "foregroundImage": "./assets/adaptive-icon.png",
                        "backgroundColor": "#FFFFFF"
                    },
                    "package": config.bundle_id,
                    "versionCode": 1,
                    "permissions": config.permissions
                },
                "web": {
                    "favicon": "./assets/favicon.png"
                },
                "plugins": [
                    [
                        "expo-location",
                        {
                            "locationAlwaysAndWhenInUsePermission": "Allow access to your location"
                        }
                    ]
                ]
            }
        }
    
    def generate_navigation(self, screens: List[Dict]) -> str:
        """Generate React Navigation configuration"""
        imports = "import { createNativeStackNavigator } from '@react-navigation/native-stack';"
        
        navigator = """
const Stack = createNativeStackNavigator();

function AppNavigator() {
  return (
    <Stack.Navigator>
"""
        
        for screen in screens:
            navigator += f"""
      <Stack.Screen
        name="{screen['name']}"
        component={require('./screens/{screen['name']}').default}
        options={{ title: '{screen.get('title', screen['name'])}' }}
      />
"""
        
        navigator += """
    </Stack.Navigator>
  );
}
"""
        return imports + navigator


class FlutterNaijaBuilder:
    """Flutter build configuration with Nigerian context"""
    
    def __init__(self):
        self.naija_banks = [
            "First Bank of Nigeria",
            "Zenith Bank",
            " Guaranty Trust Bank",
            "Access Bank",
            "United Bank for Africa",
            "EcoBank",
            "Sterling Bank",
            "Fidelity Bank",
            "Union Bank of Nigeria",
            " Keystone Bank"
        ]
        self.naija_states = [
            "Lagos", "Abuja", "Port Harcourt", "Kano", "Ibadan",
            "Enugu", "Calabar", "Abuja FCT", "Owerri", "Benin"
        ]
    
    def generate_pubspec(self, 
                        app_name: str,
                        version: str = "1.0.0") -> str:
        """Generate pubspec.yaml"""
        return f'''name: {app_name.lower().replace(" ", "_")}
description: A new Flutter project.
version: {version}
environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  provider: ^6.0.5
  http: ^1.1.0
  shared_preferences: ^2.2.0
  fluttertoast: ^8.2.2
  intl: ^0.18.1
  flutter_localizations:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/
'''
    
    def generate_nigerian_payment(self, 
                                  provider: str = "paystack") -> str:
        """Generate Nigerian payment integration"""
        if provider == "paystack":
            return '''
class PaystackService {
  static final String publicKey = "pk_test_...";
  
  Future<PaymentResponse> initializePayment({
    required String email,
    required double amount,
    String? reference,
  }) async {
    // Initialize transaction
    final response = await http.post(
      Uri.parse("https://api.paystack.co/transaction/initialize"),
      headers: {
        "Authorization": "Bearer $publicKey",
        "Content-Type": "application/json",
      },
      body: jsonEncode({
        "email": email,
        "amount": (amount * 100).toInt(), // Convert to kobo
        "reference": reference ?? "ref_${DateTime.now().millisecondsSinceEpoch}",
        "currency": "NGN",
      }),
    );
    
    return PaymentResponse.fromJson(jsonDecode(response.body));
  }
  
  Future<bool> verifyPayment(String reference) async {
    final response = await http.get(
      Uri.parse("https://api.paystack.co/transaction/verify/$reference"),
      headers: {
        "Authorization": "Bearer $publicKey",
      },
    );
    
    final data = jsonDecode(response.body);
    return data["data"]["status"] == "success";
  }
}
'''
        return ""
    
    def generate_localization(self) -> Dict:
        """Generate Nigerian English localization"""
        return {
            "appTitle": "My App",
            "welcome": "Welcome",
            "login": "Sign In",
            "register": "Create Account",
            "bankTransfer": "Bank Transfer",
            "ussd": "USSD",
            "mobileMoney": "Mobile Money",
            "success": "Success",
            "error": "Error",
            "retry": "Try Again",
            "loading": "Loading...",
            "noInternet": "No internet connection",
            "selectBank": "Select Bank",
            "enterAmount": "Enter Amount",
            "confirmPayment": "Confirm Payment",
            "transactionSuccessful": "Transaction Successful",
            "transactionFailed": "Transaction Failed",
            "receipt": "Receipt",
            "shareReceipt": "Share Receipt"
        }


class CrossPlatformUtils:
    """Cross-platform utility functions"""
    
    @staticmethod
    def format_currency(amount: float, currency: str = "NGN") -> str:
        """Format currency for Nigerian context"""
        if currency == "NGN":
            return "₦{:,.2f}".format(amount)
        elif currency == "USD":
            return "${:,.2f}".format(amount)
        return "{:,.2f} {}".format(amount, currency)
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """Validate Nigerian phone number"""
        import re
        patterns = [
            r"^234[789]\d{9}$",
            r"^0[789]\d{9}$",
            r"^\+234[789]\d{9}$"
        ]
        return any(re.match(p, phone) for p in patterns)
    
    @staticmethod
    def format_phone_number(phone: str) -> str:
        """Format Nigerian phone number to standard format"""
        import re
        if re.match(r"^0[789]\d{9}$", phone):
            return "+234" + phone[1:]
        if re.match(r"^234[789]\d{9}$", phone):
            return "+" + phone
        return phone


if __name__ == "__main__":
    expo_builder = ExpoRNBuilder()
    flutter_builder = FlutterNaijaBuilder()
    
    config = MobileConfig(
        app_name="My App",
        bundle_id="com.example.myapp",
        version="1.0.0",
        min_sdk=21,
        target_sdk=33
    )
    
    app_json = expo_builder.generate_app_json(config)
    screens = [
        {"name": "Home", "title": "Home"},
        {"name": "Profile", "title": "My Profile"},
        {"name": "Settings", "title": "Settings"}
    ]
    navigation = expo_builder.generate_navigation(screens)
    
    pubspec = flutter_builder.generate_pubspec("My App")
    payment = flutter_builder.generate_nigerian_payment("paystack")
    localization = flutter_builder.generate_localization()
    
    print(f"App config: {config.app_name}")
    print(f"Navigation screens: {len(screens)}")
    print(f"Pubspec generated: {len(pubspec)} bytes")
    print(f"Localization keys: {len(localization)}")
    print(f"Phone valid: {CrossPlatformUtils.validate_phone_number('08012345678')}")
    print(f"Formatted currency: {CrossPlatformUtils.format_currency(1500.50)}")
