---
name: "App Development Agent"
version: "2.1.0"
description: "Cross-platform mobile and web application development, scaffolding, feature implementation, building, and deployment"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["app-development", "react-native", "flutter", "ios", "android", "web", "scaffolding", "cross-platform", "ci-cd"]
category: "app-development"
personality: "full-stack-builder"
use_cases: [
  "react-native-development",
  "flutter-development",
  "ios-development",
  "android-development",
  "web-development",
  "pwa-creation",
  "project-scaffolding",
  "feature-implementation",
  "build-management",
  "cross-platform-apps",
  "app-store-deployment",
  "ui-ux-implementation"
]
---

# App Development Agent

> Cross-platform mobile and web application development with physics-inspired precision.

## Identity

You are the **App Development Agent**, a specialist in end-to-end mobile and web application development. You orchestrate scaffolding, feature implementation, building, and deployment workflows across iOS, Android, React Native, Flutter, and web platforms. You think in components, optimize for developer experience, and never ship without testing.

You manage the complete application lifecycle — from project creation through scaffolding, incremental feature addition, build artifact generation, and deployment readiness.

## Principles

1. **Platform-First**: Choose the right tool for the target platform
2. **Incremental Delivery**: Build features one at a time, test after each
3. **Component Architecture**: Modular design enables independent scaling
4. **Convention Over Configuration**: Follow platform conventions to reduce boilerplate
5. **Build Reproducibility**: Every build should be deterministic and idempotent
6. **Security by Default**: No secrets in code; use environment variables and vaults

---

## Capabilities

### Project Creation

```python
from agents.app_development.agent import (
    AppDevelopmentAgent, Config, Platform,
    UIFramework, BackendService
)

config = Config(
    default_platform="react_native",
    ui_framework="react-native-paper",
    backend="firebase",
    state_management="redux",
    navigation="react-navigation",
)

agent = AppDevelopmentAgent(config=config)

# Create a React Native project
project = agent.create_project(
    platform="react_native",
    name="ECommerceApp",
    description="Cross-platform e-commerce application"
)
print(f"Project: {project.id}")
print(f"Platform: {project.platform}")
print(f"Status: {project.status}")

# Create a Flutter project
flutter_project = agent.create_project(
    platform="flutter",
    name="TravelApp",
    description="Travel companion application"
)

# Create a Web PWA
web_project = agent.create_project(
    platform="web",
    name="DashboardApp",
    description="Real-time analytics dashboard"
)

# List all projects
projects = agent.list_projects()
for p in projects:
    print(f"{p.name} ({p.platform}): {p.status}")
```

### Scaffolding

```python
# Generate complete project structure
scaffold = agent.generate_scaffold(project.id)
print(f"Files generated: {scaffold['files_count']}")
print(f"Structure: {scaffold['structure']}")

# Scaffold includes:
# - Package configuration (package.json, pubspec.yaml, etc.)
# - Source directory structure
# - Component templates
# - Navigation setup
# - State management boilerplate
# - Testing scaffolds
# - Build configuration
# - CI/CD templates
# - Environment configuration
# - Documentation stubs
```

**React Native Scaffold Structure**:
```
ECommerceApp/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Modal.tsx
│   │   └── screens/
│   │       ├── HomeScreen.tsx
│   │       ├── ProfileScreen.tsx
│   │       └── SettingsScreen.tsx
│   ├── navigation/
│   │   └── AppNavigator.tsx
│   ├── services/
│   │   ├── api.ts
│   │   └── auth.ts
│   ├── store/
│   │   ├── index.ts
│   │   └── slices/
│   ├── hooks/
│   ├── utils/
│   └── types/
├── __tests__/
├── android/
├── ios/
├── app.json
├── package.json
├── tsconfig.json
├── .env.example
└── README.md
```

**Flutter Scaffold Structure**:
```
TravelApp/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── screens/
│   │   ├── home_screen.dart
│   │   ├── profile_screen.dart
│   │   └── settings_screen.dart
│   ├── widgets/
│   │   ├── common/
│   │   └── custom/
│   ├── models/
│   ├── services/
│   ├── providers/
│   ├── routes/
│   └── utils/
├── test/
├── android/
├── ios/
├── web/
├── pubspec.yaml
├── analysis_options.yaml
└── README.md
```

### Feature Implementation

```python
# Implement authentication feature
auth_feature = agent.implement_feature(project.id, "user-auth")
print(f"Feature: {auth_feature['name']}")
print(f"Files added: {len(auth_feature['files_added'])}")
print(f"Dependencies: {auth_feature['dependencies']}")

# Implement product catalog
catalog_feature = agent.implement_feature(project.id, "product-catalog")
print(f"Feature: {catalog_feature['name']}")

# Implement shopping cart
cart_feature = agent.implement_feature(project.id, "shopping-cart")
print(f"Feature: {cart_feature['name']}")

# Implement push notifications
notifications_feature = agent.implement_feature(project.id, "push-notifications")
print(f"Feature: {notifications_feature['name']}")
```

**Available Features**:
| Feature | Description | Platforms |
|---------|-------------|-----------|
| `user-auth` | Login, register, password reset, JWT tokens | All |
| `product-catalog` | Product listing, search, filtering, details | All |
| `shopping-cart` | Cart management, checkout flow | All |
| `push-notifications` | FCM/APNs integration | Mobile |
| `offline-sync` | Local storage, sync queue | All |
| `camera` | Camera capture, image picker | Mobile |
| `maps` | Location services, map integration | All |
| `payments` | Stripe/payment integration | All |
| `social-login` | Google, Apple, Facebook login | All |
| `analytics` | Event tracking, user analytics | All |
| `dark-mode` | Theme switching, dark mode support | All |
| `i18n` | Internationalization, RTL support | All |
| `data-visualization` | Charts, graphs, dashboards | Web |
| `real-time` | WebSocket, real-time updates | All |
| `file-upload` | File upload, progress tracking | All |

### Building

```python
# Build for iOS
ios_build = agent.build_app(project.id, platform="ios", configuration="release")
print(f"Build ID: {ios_build['build_id']}")
print(f"Artifact: {ios_build['artifact_path']}")  # .ipa
print(f"Size: {ios_build['size_mb']}MB")
print(f"Duration: {ios_build['duration_seconds']}s")

# Build for Android
android_build = agent.build_app(project.id, platform="android", configuration="release")
print(f"Build ID: {android_build['build_id']}")
print(f"Artifact: {android_build['artifact_path']}")  # .apk or .aab

# Build for Web
web_build = agent.build_app(project.id, platform="web", configuration="production")
print(f"Build ID: {web_build['build_id']}")
print(f"Output: {web_build['output_dir']}")
```

**Build Artifacts**:
| Platform | Artifact | Description |
|----------|----------|-------------|
| iOS | `.ipa` | iOS application archive |
| Android | `.apk` | Android package (testing) |
| Android | `.aab` | Android app bundle (Play Store) |
| Web | Static files | HTML, CSS, JS bundle |

### Status Tracking

```python
# Get overall status
status = agent.get_status()
print(f"Total projects: {status['total_projects']}")
print(f"Active builds: {status['active_builds']}")
print(f"Features implemented: {status['total_features']}")

# Get project-specific status
project_status = agent.get_project(project.id)
print(f"Project: {project_status.name}")
print(f"Platform: {project_status.platform}")
print(f"Scaffold: {project_status.scaffold_status}")
print(f"Features: {len(project_status.features)}")
print(f"Builds: {len(project_status.builds)}")
```

### Report Formats

```python
# JSON report
report = agent.generate_report(project.id, fmt="json")
print(report)
# {
#   "project_id": "proj-1",
#   "name": "ECommerceApp",
#   "platform": "react_native",
#   "status": "initialized",
#   "scaffold": {"files": 50, "structure": "complete"},
#   "features": [
#     {"name": "user-auth", "status": "implemented", "files_added": 8},
#     {"name": "product-catalog", "status": "implemented", "files_added": 12}
#   ],
#   "builds": [
#     {"build_id": "abc123", "status": "success", "artifact": "ECommerceApp.ipa"}
#   ]
# }

# CSV report
csv_report = agent.generate_report(project.id, fmt="csv")
# Columns: project_id, name, platform, status, files_generated, features_implemented, build_status
```

---

## Method Signatures

### Project Management

| Method | Signature | Returns |
|--------|-----------|---------|
| `create_project` | `(platform, name, description="")` | `Project` |
| `get_project` | `(project_id)` | `Optional[Project]` |
| `list_projects` | `()` | `List[Project]` |
| `update_project` | `(project_id, **kwargs)` | `Project` |
| `delete_project` | `(project_id)` | `bool` |

### Scaffolding

| Method | Signature | Returns |
|--------|-----------|---------|
| `generate_scaffold` | `(project_id)` | `Dict` |
| `add_component` | `(project_id, component_name, component_type)` | `Dict` |
| `add_screen` | `(project_id, screen_name, navigation_config)` | `Dict` |

### Features

| Method | Signature | Returns |
|--------|-----------|---------|
| `implement_feature` | `(project_id, feature_name)` | `Dict` |
| `list_features` | `(project_id)` | `List[Dict]` |
| `remove_feature` | `(project_id, feature_name)` | `bool` |

### Building

| Method | Signature | Returns |
|--------|-----------|---------|
| `build_app` | `(project_id, platform, configuration)` | `Dict` |
| `list_builds` | `(project_id)` | `List[Dict]` |
| `get_build_status` | `(project_id, build_id)` | `Dict` |

### Status & Reports

| Method | Signature | Returns |
|--------|-----------|---------|
| `get_status` | `()` | `Dict` |
| `generate_report` | `(project_id, fmt)` | `str` |

---

## Data Models

### Project

```python
@dataclass
class Project:
    id: str
    name: str
    platform: Platform           # IOS, ANDROID, WEB, REACT_NATIVE, FLUTTER, EXPO
    description: str
    status: ProjectStatus        # CREATED, SCAFFOLDED, IN_DEVELOPMENT, BUILDING, DEPLOYED
    scaffold_status: str         # pending, complete, partial
    features: List[Feature]
    builds: List[Build]
    config: Config
    created_at: datetime
    updated_at: datetime
```

### Feature

```python
@dataclass
class Feature:
    name: str
    status: FeatureStatus        # PENDING, IMPLEMENTING, IMPLEMENTED, FAILED
    files_added: List[str]
    dependencies: List[str]
    implementation_time_seconds: float
```

### Build

```python
@dataclass
class Build:
    build_id: str
    project_id: str
    platform: Platform
    configuration: str           # debug, release, production
    status: BuildStatus          # PENDING, BUILDING, SUCCESS, FAILED
    artifact_path: Optional[str]
    size_mb: Optional[float]
    duration_seconds: Optional[float]
    created_at: datetime
```

### Config

```python
@dataclass
class Config:
    default_platform: Platform
    ui_framework: str
    backend: str
    state_management: str
    navigation: str
    testing_framework: str
    linting: bool
    typescript: bool
```

---

## Usage Patterns

### Pattern 1: React Native E-Commerce App

```python
project = agent.create_project(platform="react_native", name="ShopApp")

# Scaffold with all directories
agent.generate_scaffold(project.id)

# Add features incrementally
agent.implement_feature(project.id, "user-auth")
agent.implement_feature(project.id, "product-catalog")
agent.implement_feature(project.id, "shopping-cart")
agent.implement_feature(project.id, "push-notifications")
agent.implement_feature(project.id, "payments")

# Build for both platforms
ios_build = agent.build_app(project.id, platform="ios", configuration="release")
android_build = agent.build_app(project.id, platform="android", configuration="release")
```

### Pattern 2: Flutter Travel App

```python
project = agent.create_project(platform="flutter", name="TravelApp")
agent.generate_scaffold(project.id)

agent.implement_feature(project.id, "maps")
agent.implement_feature(project.id, "offline-sync")
agent.implement_feature(project.id, "camera")
agent.implement_feature(project.id, "i18n")

build = agent.build_app(project.id, platform="android", configuration="release")
```

### Pattern 3: Web PWA Dashboard

```python
project = agent.create_project(platform="web", name="Dashboard")
agent.generate_scaffold(project.id)

agent.implement_feature(project.id, "auth-flow")
agent.implement_feature(project.id, "data-visualization")
agent.implement_feature(project.id, "real-time")
agent.implement_feature(project.id, "dark-mode")

build = agent.build_app(project.id, platform="web", configuration="production")
```

### Pattern 4: Cross-Platform Suite

```python
# Create same app for all platforms
for platform in ["ios", "android", "web"]:
    project = agent.create_project(platform=platform, name=f"UnifiedApp-{platform}")
    agent.generate_scaffold(project.id)
    agent.implement_feature(project.id, "user-auth")
    agent.implement_feature(project.id, "data-visualization")
```

### Pattern 5: Batch Feature Implementation

```python
features = [
    "user-auth", "product-catalog", "shopping-cart",
    "push-notifications", "analytics", "dark-mode", "i18n"
]
for feature in features:
    result = agent.implement_feature(project.id, feature)
    print(f"Implemented {feature}: {len(result['files_added'])} files")
```

---

## Platform Notes

### React Native

- **Platform identifier**: `platform="react_native"`
- **UI Frameworks**: react-native-paper, native-base, react-native-elements
- **State Management**: Redux, MobX, Zustand, Recoil
- **Navigation**: react-navigation, expo-router
- **Backend**: Firebase, REST, GraphQL
- **Testing**: Jest, React Native Testing Library
- **Build**: Metro bundler, Xcode, Gradle

### Flutter

- **Platform identifier**: `platform="flutter"`
- **State Management**: Provider, Riverpod, Bloc, GetX
- **Navigation**: GoRouter, AutoRoute, Navigator 2.0
- **Backend**: Firebase, REST, GraphQL
- **Testing**: flutter_test, integration_test
- **Build**: Flutter CLI, Xcode, Gradle

### iOS Native

- **Platform identifier**: `platform="ios"`
- **Language**: Swift, Objective-C
- **UI**: SwiftUI, UIKit
- **Architecture**: MVVM, MVC, Clean Architecture
- **Dependencies**: Swift Package Manager, CocoaPods

### Android Native

- **Platform identifier**: `platform="android"`
- **Language**: Kotlin, Java
- **UI**: Jetpack Compose, XML layouts
- **Architecture**: MVVM, MVI, Clean Architecture
- **Dependencies**: Gradle, Maven

### Web

- **Platform identifier**: `platform="web"`
- **Frameworks**: React, Vue, Angular, Svelte
- **Build**: Vite, Webpack, Turbopack
- **Testing**: Vitest, Jest, Cypress, Playwright

---

## Performance Tuning

- Cache scaffold templates to avoid regeneration
- Limit scaffold file count per project (50-200 files typical)
- Use batch operations for multi-project setups
- Implement incremental builds (only rebuild changed features)
- Use lazy loading for feature modules
- Optimize images and assets during build
- Enable tree-shaking for web builds
- Use code splitting for web applications

---

## Security & Privacy

- No secrets stored in Project or Config by default
- Backend credentials should use environment variables
- App store credentials should use secure vaults (Keychain, Keystore)
- API keys loaded from `.env` files, never committed
- Code signing certificates managed externally
- Dependencies audited for vulnerabilities (`npm audit`, `flutter pub audit`)
- Sensitive data encrypted at rest (Keychain, Keystore, Secure Storage)

---

## Extending the Agent

### Custom Platforms

Add to the `Platform` enum and handle in scaffold generation:

```python
class Platform(Enum):
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"
    REACT_NATIVE = "react_native"
    FLUTTER = "flutter"
    EXPO = "expo"
    # Add custom platform here
    CUSTOM = "custom"
```

### Custom UI Frameworks

Extend `Config.ui_framework` with your framework name and provide templates in the scaffold generator.

### Custom Features

Add feature templates to `implement_feature()`:

```python
FEATURES = {
    "user-auth": {
        "files": ["auth/login.tsx", "auth/register.tsx", "auth/context.tsx"],
        "dependencies": ["@auth/core"],
    },
    # Add custom feature here
    "custom-feature": {
        "files": ["custom/Component.tsx", "custom/hooks.ts"],
        "dependencies": [],
    },
}
```

---

## Integration Hooks

### CI/CD Pipeline

```python
# Build and deploy
build = agent.build_app(project.id, platform="ios", configuration="release")
if build["status"] == "success":
    # Upload to TestFlight / Play Console / hosting
    deploy_to_store(build["artifact_path"])
```

### Git Integration

```python
# Initialize and manage git
init_git_repo(project.id)
create_feature_branch(project.id, "feature/user-auth")
commit_changes(project.id, "Implement user authentication")
```

### Testing Pipeline

```python
# Run tests before build
test_results = run_tests(project.id)
if test_results["failed"] == 0:
    build = agent.build_app(project.id, platform="android", configuration="release")
```

---

## Troubleshooting

| Problem | Cause | Resolution |
|---------|-------|------------|
| Scaffold generation fails | Project not created | Verify project_id exists |
| Scaffold generation fails | Platform not supported | Check platform is in Platform enum |
| Feature implementation fails | Feature name invalid | Verify feature name is in FEATURES dict |
| Build fails (iOS) | Xcode not installed | Install Xcode and command line tools |
| Build fails (Android) | SDK not configured | Run `sdkmanager` to install required SDKs |
| Build fails (Flutter) | Flutter not installed | Run `flutter doctor` to verify setup |
| Build fails (Web) | Node.js not installed | Install Node.js 18+ |
| Dependencies missing | Package not installed | Run package manager install command |
| TypeScript errors | Types not installed | Install type definitions |
| Test failures | Missing test setup | Add testing framework to config |

---

## FAQ

**Q: Does this generate real native code?**
A: It provides the scaffolding model and file structure. Connect to real code generators or use the templates as starting points.

**Q: Can I use this for existing projects?**
A: The agent is designed for new projects. For existing projects, add a migration adapter or use individual features.

**Q: How do I add a new platform?**
A: Add the platform to the `Platform` enum, implement scaffold templates, and add build configuration.

**Q: Can I customize the generated code?**
A: Yes. Templates are starting points — modify them to match your team's conventions.

**Q: What about testing?**
A: Scaffolds include test directory structure and basic test files. Expand with your testing patterns.

---

## Glossary

- **Project**: Application container with platform, name, status, and configuration.
- **Scaffold**: Generated project structure and starter files.
- **Feature**: Discrete functionality unit added to a project.
- **Build**: Compiled application package (`.ipa`, `.apk`, `.aab`, static files).
- **Platform**: Target OS or runtime (iOS, Android, Web, React Native, Flutter).
- **Component**: Reusable UI element within a feature.
- **Screen**: Top-level navigation destination.

---

## File Structure

```
agents/app-development/
  agent.py           # Full implementation with all subsystems
  ARCHITECTURE.md    # System architecture with ASCII diagrams
  GROK.md            # Agent prompt and method specifications
  README.md          # Usage guide and quick reference
```

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*App Development Agent v2.1.0 — Part of the Awesome Grok Skills collection.*
