"""
iOS Development Module
Part of the mobile skill domain.

Provides iOS project scaffolding, SwiftUI code generation, Swift Package Manager
configuration, and App Store deployment utilities.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set


class IosPlatform(Enum):
    IOS = "ios"
    IOS_SIMULATOR = "ios-simulator"
    MACOS = "macos"
    TVOS = "tvos"
    WATCHOS = "watchos"


class IosMinimumVersion(Enum):
    IOS_15 = "15.0"
    IOS_16 = "16.0"
    IOS_17 = "17.0"
    IOS_18 = "18.0"


class BuildConfiguration(Enum):
    DEBUG = "Debug"
    RELEASE = "Release"
    STAGING = "Staging"


class SwiftPackageManager(Enum):
    SWIFT_PACKAGE = "Swift Package"
    COCOAPODS = "CocoaPods"
    CARTHAGE = "Carthage"
    NONE = "None"


@dataclass
class SwiftPackage:
    url: str
    name: Optional[str] = None
    version: Optional[str] = None
    branch: Optional[str] = None
    products: List[str] = field(default_factory=list)

    def to_package_dependency(self) -> Dict[str, Any]:
        requirement: Dict[str, Any] = {}
        if self.version:
            requirement["upToNextMajorVersion"] = {"minimumVersion": self.version}
        elif self.branch:
            requirement["branch"] = self.branch

        entry: Dict[str, Any] = {
            "url": self.url,
            "requirement": requirement,
        }
        if self.name:
            entry["identity"] = self.name.lower().replace(" ", "-")
        return entry


@dataclass
class IosProjectConfig:
    name: str
    bundle_id: str
    team_id: str = ""
    deployment_target: IosMinimumVersion = IosMinimumVersion.IOS_17
    swift_version: str = "5.9"
    platforms: List[IosPlatform] = field(default_factory=lambda: [IosPlatform.IOS])
    build_configs: List[BuildConfiguration] = field(
        default_factory=lambda: [BuildConfiguration.DEBUG, BuildConfiguration.RELEASE]
    )
    package_manager: SwiftPackageManager = SwiftPackageManager.SWIFT_PACKAGE
    packages: List[SwiftPackage] = field(default_factory=list)
    use_swiftui: bool = True
    use_swift_data: bool = True
    use_async_await: bool = True
    entitlements: List[str] = field(default_factory=list)


@dataclass
class IosScheme:
    name: str
    build_config: BuildConfiguration = BuildConfiguration.DEBUG
    target: str = "App"
    test_plan: Optional[str] = None
    launch_arguments: List[str] = field(default_factory=list)

    def to_xcscheme_data(self) -> Dict[str, Any]:
        return {
            "Scheme": {
                "@lastUpgradeVersion": "1540",
                "BuildAction": {
                    "BuildActionEntries": [{
                        "BuildForTesting": "YES",
                        "BuildForRunning": "YES",
                        "BuildForProfiling": "YES",
                        "BuildForArchiving": "YES",
                        "BlueprintName": self.target,
                    }]
                },
                "TestAction": {
                    "BuildConfiguration": self.build_config.value,
                    "SelectedDebuggerIdentifier": "Xcode.DebuggerFoundation.Debugger.LLDB",
                    "SelectedLauncherIdentifier": "Xcode.DebuggerFoundation.Launcher.LLDB",
                },
                "LaunchAction": {
                    "BuildConfiguration": self.build_config.value,
                    "SelectedDebuggerIdentifier": "Xcode.DebuggerFoundation.Debugger.LLDB",
                    "LaunchStyle": "0",
                    "DebugServiceExtension": "internal",
                },
            }
        }


class XcodeProjectGenerator:
    """Generates Xcode project configuration files."""

    def __init__(self, config: IosProjectConfig):
        self.config = config
        self._schemes: List[IosScheme] = []
        self._build_settings: Dict[str, Dict[str, str]] = {}

    def add_scheme(self, scheme: IosScheme) -> XcodeProjectGenerator:
        self._schemes.append(scheme)
        return self

    def generate_info_plist(self) -> str:
        entitlements_str = ""
        if self.config.entitlements:
            entitlements_str = f"""
    <key>com.apple.security.app-sandbox</key>
    <true/>"""

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleDisplayName</key>
    <string>{self.config.name}</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundleIdentifier</key>
    <string>{self.config.bundle_id}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{self.config.name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>MinimumOSVersion</key>
    <string>{self.config.deployment_target.value}</string>
    <key>UIApplicationSceneManifest</key>
    <dict>
        <key>UIApplicationSupportsMultipleScenes</key>
        <false/>
    </dict>
    <key>UILaunchScreen</key>
    <dict/>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
    </array>{entitlements_str}
</dict>
</plist>
"""

    def generate_package_swift(self) -> str:
        package_deps = []
        for pkg in self.config.packages:
            dep = pkg.to_package_dependency()
            package_deps.append(json.dumps(dep, indent=8))

        deps_section = ",\n".join(package_deps) if package_deps else "    // No external packages"

        return f"""// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "{self.config.name}",
    platforms: [
        .iOS(.v{self.config.deployment_target.value.split('.')[0]})
    ],
    products: [
        .library(name: "{self.config.name}", targets: ["{self.config.name}"]),
    ],
    dependencies: [
{deps_section}
    ],
    targets: [
        .target(
            name: "{self.config.name}",
            dependencies: []
        ),
        .testTarget(
            name: "{self.config.name}Tests",
            dependencies: ["{self.config.name}"]
        ),
    ]
)
"""

    def generate_swiftui_app(self) -> str:
        return f"""import SwiftUI

@main
struct {self.config.name}App: App {{
    var body: some Scene {{
        WindowGroup {{
            ContentView()
        }}
    }}
}}

struct ContentView: View {{
    var body: some View {{
        NavigationStack {{
            List {{
                Section("Getting Started") {{
                    Text("Welcome to {self.config.name}")
                        .font(.headline)
                }}
            }}
            .navigationTitle("{self.config.name}")
        }}
    }}
}}
"""

    def generate_swift_data_model(self) -> str:
        return f"""import Foundation
import SwiftData

@Model
final class Item {{
    var id: UUID
    var name: String
    var createdAt: Date
    var updatedAt: Date

    init(name: String) {{
        self.id = UUID()
        self.name = name
        self.createdAt = Date()
        self.updatedAt = Date()
    }}
}}

@Model
final class UserProfile {{
    var id: UUID
    var displayName: String
    var email: String
    var createdAt: Date

    init(displayName: String, email: String) {{
        self.id = UUID()
        self.displayName = displayName
        self.email = email
        self.createdAt = Date()
    }}
}}
"""

    def generate_swift_view_model(self) -> str:
        return f"""import Foundation
import SwiftUI
import SwiftData

@MainActor
@Observable
final class ItemViewModel {{
    var items: [Item] = []
    var isLoading = false
    var errorMessage: String?

    private let repository: ItemRepositoryProtocol

    init(repository: ItemRepositoryProtocol = ItemRepository()) {{
        self.repository = repository
    }}

    func load() async {{
        isLoading = true
        defer {{ isLoading = false }}

        do {{
            items = try await repository.fetchItems()
        }} catch {{
            errorMessage = error.localizedDescription
        }}
    }}

    func create(name: String) async {{
        do {{
            let item = try await repository.createItem(name: name)
            items.insert(item, at: 0)
        }} catch {{
            errorMessage = error.localizedDescription
        }}
    }}

    func delete(at offsets: IndexSet) async {{
        for index in offsets {{
            do {{
                try await repository.deleteItem(items[index])
                items.remove(at: index)
            }} catch {{
                errorMessage = error.localizedDescription
            }}
        }}
    }}
}}
"""

    def generate_networking_layer(self) -> str:
        return f"""import Foundation

enum APIError: Error {{
    case invalidURL
    case invalidResponse
    case unauthorized
    case notFound
    case serverError(Int)
    case decodingError(Error)
}}

protocol APIClientProtocol {{
    func request<T: Decodable>(_ endpoint: String, method: HTTPMethod) async throws -> T
    func request<T: Decodable, B: Encodable>(_ endpoint: String, method: HTTPMethod, body: B) async throws -> T
}}

enum HTTPMethod: String {{
    case GET, POST, PUT, DELETE, PATCH
}}

final class APIClient: APIClientProtocol {{
    private let session: URLSession
    private let baseURL: URL
    private let decoder: JSONDecoder

    init(baseURL: URL = URL(string: "https://api.example.com")!) {{
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        self.session = URLSession(configuration: config)
        self.baseURL = baseURL
        self.decoder = JSONDecoder()
        self.decoder.keyDecodingStrategy = .convertFromSnakeCase
        self.decoder.dateDecodingStrategy = .iso8601
    }}

    func request<T: Decodable>(_ endpoint: String, method: HTTPMethod) async throws -> T {{
        let url = baseURL.appendingPathComponent(endpoint)
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let (data, response) = try await session.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {{
            throw APIError.invalidResponse
        }}

        switch httpResponse.statusCode {{
        case 200..<300:
            return try decoder.decode(T.self, from: data)
        case 401:
            throw APIError.unauthorized
        case 404:
            throw APIError.notFound
        default:
            throw APIError.serverError(httpResponse.statusCode)
        }}
    }}

    func request<T: Decodable, B: Encodable>(
        _ endpoint: String, method: HTTPMethod, body: B
    ) async throws -> T {{
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(body)

        let (data, response) = try await session.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse,
              200..<300 ~= httpResponse.statusCode else {{
            throw APIError.invalidResponse
        }}
        return try decoder.decode(T.self, from: data)
    }}
}}
"""


class AppStoreConfigGenerator:
    """Generates App Store Connect configuration."""

    def __init__(self, config: IosProjectConfig):
        self.config = config

    def generate_fastlane_matchfile(self) -> str:
        return f"""git_url("https://github.com/{self.config.team_id}/certificates")
storage_mode("git")
type("appstore")
app_identifier("{self.config.bundle_id}")
username("apple@example.com")
team_id("{self.config.team_id}")
"""

    def generate_gymfile(self) -> str:
        return f"""scheme("{self.config.name}")
output_directory("./build")
output_name("{self.config.name}.ipa")
export_method("app-store")
clean(true)
"""

    def generate_firebase_config(self) -> str:
        return f"""# Firebase iOS Configuration
# Place GoogleService-Info.plist in the app bundle
# Ensure Firebase is initialized in AppDelegate

import Firebase

@main
class AppDelegate: UIResponder, UIApplicationDelegate {{
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {{
        FirebaseApp.configure()
        return true
    }}
}}
"""


def main():
    config = IosProjectConfig(
        name="MyApp",
        bundle_id="com.example.myapp",
        team_id="TEAM123",
        deployment_target=IosMinimumVersion.IOS_17,
        packages=[
            SwiftPackage(url="https://github.com/Alamofire/Alamofire", version="5.9.0"),
            SwiftPackage(url="https://github.com/firebase/firebase-ios-sdk", version="10.20.0"),
        ],
        entitlements=["com.apple.security.app-sandbox"],
    )

    gen = XcodeProjectGenerator(config)
    print("=== Info.plist ===")
    print(gen.generate_info_plist()[:500] + "\n...")

    print("\n=== Package.swift ===")
    print(gen.generate_package_swift()[:500] + "\n...")

    print("\n=== SwiftUI App ===")
    print(gen.generate_swiftui_app())

    print("\n=== Swift Data Model ===")
    print(gen.generate_swift_data_model()[:400] + "\n...")

    print("\n=== ViewModel ===")
    print(gen.generate_swift_view_model()[:400] + "\n...")

    print("\n=== Networking Layer ===")
    print(gen.generate_networking_layer()[:400] + "\n...")

    app_store = AppStoreConfigGenerator(config)
    print("\n=== Fastlane Matchfile ===")
    print(app_store.generate_fastlane_matchfile())

    print("\nDone.")


if __name__ == "__main__":
    main()
