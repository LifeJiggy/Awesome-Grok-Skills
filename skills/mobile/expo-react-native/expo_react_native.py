"""
Expo React Native Module
Part of the mobile skill domain.

Provides Expo project scaffolding, configuration generation, EAS build profiles,
and cross-platform mobile app management utilities.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set


class ExpoWorkflow(Enum):
    MANAGED = "managed"
    BARE = "bare"


class BuildProfile(Enum):
    DEVELOPMENT = "development"
    PREVIEW = "preview"
    PRODUCTION = "production"


class Platform(Enum):
    IOS = "ios"
    ANDROID = "android"
    ALL = "all"


class NotificationType(Enum):
    PUSH = "push"
    LOCAL = "local"
    IN_APP = "in_app"


@dataclass
class ExpoPlugin:
    name: str
    version: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)

    def to_manifest_entry(self) -> Dict[str, Any]:
        if self.config:
            return [self.name, self.config]
        if self.version:
            return [self.name, self.version]
        return [self.name]


@dataclass
class EASBuildProfile:
    name: BuildProfile
    distribution: str = "internal"
    credentials_source: str = "local"
    resource_class: str = "medium"
    node_version: str = "18"
    env: Dict[str, str] = field(default_factory=dict)
    android_build_type: str = "apk"
    ios_simulator: bool = False

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "distribution": self.distribution,
            "credentialsSource": self.credentials_source,
            "resourceClass": self.resource_class,
            "env": self.env,
        }
        if self.name == BuildProfile.DEVELOPMENT:
            result["developmentClient"] = True
            result["distribution"] = "internal"
        if self.name == BuildProfile.PREVIEW:
            result["android"] = {"buildType": self.android_build_type}
        if self.name == BuildProfile.PRODUCTION:
            result["autoIncrement"] = True
        return result


@dataclass
class ExpoConfig:
    name: str
    slug: str
    version: str = "1.0.0"
    orientation: str = "portrait"
    scheme: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    plugins: List[ExpoPlugin] = field(default_factory=list)
    workflows: ExpoWorkflow = ExpoWorkflow.MANAGED
    typed_routes: bool = True
    platforms: List[Platform] = field(default_factory=lambda: [Platform.IOS, Platform.ANDROID])


class ExpoConfigGenerator:
    """Generates expo.config.ts / app.json configuration files."""

    def __init__(self, config: ExpoConfig):
        self.config = config

    def generate_app_json(self) -> str:
        plugins_data = [p.to_manifest_entry() for p in self.config.plugins]
        config_dict: Dict[str, Any] = {
            "expo": {
                "name": self.config.name,
                "slug": self.config.slug,
                "version": self.config.version,
                "orientation": self.config.orientation,
                "scheme": self.config.scheme,
                "extra": self.config.extra,
                "plugins": plugins_data,
                "experiments": {"typedRoutes": self.config.typed_routes},
            }
        }
        return json.dumps(config_dict, indent=2)

    def generate_eas_json(self, profiles: List[EASBuildProfile]) -> str:
        build_section: Dict[str, Any] = {}
        for profile in profiles:
            build_section[profile.name.value] = profile.to_dict()

        eas_config = {
            "cli": {"version": ">= 5.0.0"},
            "build": build_section,
            "submit": {
                "production": {
                    "ios": {"appleId": "", "ascAppId": ""},
                    "android": {"serviceAccountKeyPath": "./google-services.json"},
                }
            },
        }
        return json.dumps(eas_config, indent=2)


class EASBuildManager:
    """Manages EAS Build commands and profiles."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self._profiles: List[EASBuildProfile] = []
        self._build_history: List[Dict[str, Any]] = []

    def add_profile(self, profile: EASBuildProfile) -> EASBuildManager:
        self._profiles.append(profile)
        return self

    def create_default_profiles(self) -> EASBuildManager:
        self._profiles = [
            EASBuildProfile(name=BuildProfile.DEVELOPMENT, distribution="internal"),
            EASBuildProfile(name=BuildProfile.PREVIEW, android_build_type="apk"),
            EASBuildProfile(name=BuildProfile.PRODUCTION),
        ]
        return self

    def generate_build_command(self, profile: BuildProfile, platform: Platform = Platform.ALL) -> str:
        platform_flag = ""
        if platform != Platform.ALL:
            platform_flag = f" --platform {platform.value}"
        return f"eas build --profile {profile.value}{platform_flag} --non-interactive"

    def generate_submit_command(self, platform: Platform = Platform.ALL) -> str:
        platform_flag = ""
        if platform != Platform.ALL:
            platform_flag = f" --platform {platform.value}"
        return f"eas submit --profile production{platform_flag} --non-interactive"

    def record_build(self, build_id: str, platform: str, profile: str) -> None:
        self._build_history.append({
            "build_id": build_id,
            "platform": platform,
            "profile": profile,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "queued",
        })

    def get_build_history(self) -> List[Dict[str, Any]]:
        return list(self._build_history)


class OTAUpdateManager:
    """Manages Expo OTA (Over-the-Air) updates."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self._channels: Dict[str, str] = {}

    def create_channel(self, name: str, branch: str = "main") -> OTAUpdateManager:
        self._channels[name] = branch
        return self

    def generate_update_command(self, channel: str, message: str) -> str:
        return f'eas update --channel {channel} --message "{message}"'

    def generate_rollout_command(self, channel: str, branch: str, percentage: int) -> str:
        return (
            f"eas channel:edit {channel} --branch {branch} "
            f"--rollout-percentage {percentage}"
        )

    def get_channels(self) -> Dict[str, str]:
        return dict(self._channels)


class ExpoRouterGenerator:
    """Generates Expo Router file structures."""

    @staticmethod
    def generate_root_layout(app_name: str) -> str:
        return f'''import {{ Stack }} from "expo-router";

export default function RootLayout() {{
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{{{ headerShown: false }}}} />
      <Stack.Screen name="modal" options={{{{ presentation: "modal" }}}} />
    </Stack>
  );
}}
'''

    @staticmethod
    def generate_tab_layout(tabs: List[str]) -> str:
        tab_screens = []
        for tab in tabs:
            tab_screens.append(
                f'      <Tabs.Screen name="{tab}" options={{{{ title: "{tab.capitalize()}" }}}} />'
            )
        screens = "\n".join(tab_screens)
        return f'''import {{ Tabs }} from "expo-router";

export default function TabLayout() {{
  return (
    <Tabs>
{screens}
    </Tabs>
  );
}}
'''

    @staticmethod
    def generate_screen_template(name: str) -> str:
        return f'''import {{ View, Text, StyleSheet }} from "react-native";

export default function {name.capitalize()}Screen() {{
  return (
    <View style={{styles.container}}>
      <Text style={{styles.title}}>{name.capitalize()}</Text>
    </View>
  );
}}

const styles = StyleSheet.create({{
  container: {{ flex: 1, justifyContent: "center", alignItems: "center" }},
  title: {{ fontSize: 24, fontWeight: "bold" }},
}});
'''

    @staticmethod
    def generate_dynamic_route(name: str) -> str:
        return f'''import {{ useLocalSearchParams }} from "expo-router";
import {{ View, Text }} from "react-native";

export default function {name.capitalize()}Detail() {{
  const {{ id }} = useLocalSearchParams<{{
    id: string;
  }}>();

  return (
    <View style={{{{ flex: 1, justifyContent: "center", alignItems: "center" }}}}>
      <Text>Detail view for {{id}}</Text>
    </View>
  );
}}
'''


def main():
    config = ExpoConfig(
        name="MyExpoApp",
        slug="my-expo-app",
        version="1.0.0",
        scheme="myexpoapp",
        plugins=[
            ExpoPlugin("expo-router"),
            ExpoPlugin("expo-notifications", config={"icon": "./assets/icon.png"}),
            ExpoPlugin("expo-camera"),
        ],
        typed_routes=True,
    )

    gen = ExpoConfigGenerator(config)
    print("=== Expo app.json ===")
    print(gen.generate_app_json()[:500] + "\n...")

    build_mgr = EASBuildManager(Path("."))
    build_mgr.create_default_profiles()

    print("\n=== EAS Build Commands ===")
    print(build_mgr.generate_build_command(BuildProfile.DEVELOPMENT, Platform.IOS))
    print(build_mgr.generate_build_command(BuildProfile.PRODUCTION))

    eas_gen = ExpoConfigGenerator(config)
    print("\n=== eas.json ===")
    print(eas_gen.generate_eas_json(build_mgr._profiles)[:500] + "\n...")

    print("\n=== OTA Update Manager ===")
    ota = OTAUpdateManager(Path("."))
    ota.create_channel("production", "main")
    ota.create_channel("staging", "staging")
    print(ota.generate_update_command("production", "Fix login crash"))
    print(ota.generate_rollout_command("production", "main", 10))

    print("\n=== Expo Router Templates ===")
    router = ExpoRouterGenerator()
    print(router.generate_root_layout("MyApp")[:300])
    print(router.generate_tab_layout(["home", "search", "profile"])[:400])

    print("\nDone.")


if __name__ == "__main__":
    main()
