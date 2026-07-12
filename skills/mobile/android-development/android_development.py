"""
Android Development Module
Part of the mobile skill domain.

Provides Android project scaffolding, architecture generation, dependency management,
and build configuration utilities for production Android applications.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Protocol


class ArchitectureType(Enum):
    MVVM = "mvvm"
    MVI = "mvi"
    CLEAN_ARCHITECTURE = "clean_architecture"
    MVP = "mvp"


class BuildType(Enum):
    DEBUG = "debug"
    RELEASE = "release"
    STAGING = "staging"


class PermissionType(Enum):
    CAMERA = "android.permission.CAMERA"
    INTERNET = "android.permission.INTERNET"
    LOCATION_FINE = "android.permission.ACCESS_FINE_LOCATION"
    LOCATION_COARSE = "android.permission.ACCESS_COARSE_LOCATION"
    STORAGE_READ = "android.permission.READ_EXTERNAL_STORAGE"
    STORAGE_WRITE = "android.permission.WRITE_EXTERNAL_STORAGE"
    NOTIFICATIONS = "android.permission.POST_NOTIFICATIONS"
    BLUETOOTH = "android.permission.BLUETOOTH"


@dataclass
class Dependency:
    group: str
    artifact: String = ""
    version: String = ""
    configuration: String = "implementation"
    is_bom: bool = False

    @property
    def declaration(self) -> str:
        if self.is_bom:
            return f'implementation(platform("{self.group}:{self.artifact}:{self.version}"))'
        return f'{self.configuration}("{self.group}:{self.artifact}:{self.version}")'


@dataclass
class AndroidConfig:
    application_id: str = "com.example.app"
    min_sdk: int = 24
    target_sdk: int = 34
    compile_sdk: int = 34
    version_code: int = 1
    version_name: str = "1.0.0"
    architecture: ArchitectureType = ArchitectureType.MVVM
    build_types: List[BuildType] = field(default_factory=lambda: [BuildType.DEBUG, BuildType.RELEASE])
    permissions: List[PermissionType] = field(default_factory=list)
    use_hilt: bool = True
    use_compose: bool = True
    use_room: bool = True
    use_navigation: bool = True
    kotlin_version: str = "1.9.22"
    agp_version: String = "8.2.2"


@dataclass
class ProjectModule:
    name: str
    path: str
    dependencies: List[str] = field(default_factory=list)
    is_library: bool = False
    package_structure: str = ""


class GradleBuildGenerator:
    """Generates Gradle build scripts for Android projects."""

    def __init__(self, config: AndroidConfig):
        self.config = config
        self._dependencies: List[Dependency] = []
        self._modules: List[ProjectModule] = []

    def add_dependency(self, dep: Dependency) -> GradleBuildGenerator:
        self._dependencies.append(dep)
        return self

    def add_module(self, module: ProjectModule) -> GradleBuildGenerator:
        self._modules.append(module)
        return self

    def generate_build_gradle(self) -> str:
        dep_lines = "\n    ".join(d.declaration for d in self._dependencies)
        return f"""plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    {"id("com.google.dagger.hilt.android")" if self.config.use_hilt else ""}
    id("com.google.devtools.ksp") kspVersion("1.9.22-1.0.17")
}}

android {{
    namespace = "{self.config.application_id}"
    compileSdk = {self.config.compile_sdk}

    defaultConfig {{
        applicationId = "{self.config.application_id}"
        minSdk = {self.config.min_sdk}
        targetSdk = {self.config.target_sdk}
        versionCode = {self.config.version_code}
        versionName = "{self.config.version_name}"
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }}
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }}

    kotlinOptions {{
        jvmTarget = "17"
    }}

    buildFeatures {{
        compose = {str(self.config.use_compose).lower()}
    }}
}}

dependencies {{
    {dep_lines}
}}
"""

    def generate_settings_gradle(self) -> str:
        module_includes = "\n".join(f'include(":{m.path}")' for m in self._modules)
        return f"""pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}

dependencyResolution {{
    repositories {{
        google()
        mavenCentral()
    }}
}}

rootProject.name = "{self.config.application_id.split('.')[-1]}"
{module_includes}
"""

    def generate_version_catalog(self) -> str:
        return f"""[versions]
kotlin = "{self.config.kotlin_version}"
agp = "{self.config.agp_version}"
hilt = "2.50"
room = "2.6.1"
navigation = "2.7.7"
compose-bom = "2024.02.00"
retrofit = "2.9.0"
okhttp = "4.12.0"
coroutines = "1.7.3"
lifecycle = "2.7.0"
hilt-navigation = "1.1.0"
ksp = "1.9.22-1.0.17"

[libraries]
compose-bom = {{ group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }}
compose-ui = {{ group = "androidx.compose.ui", name = "ui" }}
compose-material3 = {{ group = "androidx.compose.material3", name = "material3" }}
compose-ui-tooling = {{ group = "androidx.compose.ui", name = "ui-tooling" }}
lifecycle-runtime = {{ group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycle" }}
lifecycle-viewmodel = {{ group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycle" }}
hilt-android = {{ group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }}
hilt-compiler = {{ group = "com.google.dagger", name = "hilt-compiler", version.ref = "hilt" }}
hilt-navigation = {{ group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "hilt-navigation" }}
room-runtime = {{ group = "androidx.room", name = "room-runtime", version.ref = "room" }}
room-ktx = {{ group = "androidx.room", name = "room-ktx", version.ref = "room" }}
room-compiler = {{ group = "androidx.room", name = "room-compiler", version.ref = "room" }}
navigation-compose = {{ group = "androidx.navigation", name = "navigation-compose", version.ref = "navigation" }}
retrofit = {{ group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }}
retrofit-serialization = {{ group = "com.squareup.retrofit2", name = "converter-kotlinx-serialization", version.ref = "retrofit" }}
okhttp = {{ group = "com.squareup.okhttp3", name = "okhttp", version.ref = "okhttp" }}
okhttp-logging = {{ group = "com.squareup.okhttp3", name = "logging-interceptor", version.ref = "okhttp" }}
coroutines-core = {{ group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-core", version.ref = "coroutines" }}
coroutines-android = {{ group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-android", version.ref = "coroutines" }}

[plugins]
android-application = {{ id = "com.android.application", version.ref = "agp" }}
kotlin-android = {{ id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }}
hilt = {{ id = "com.google.dagger.hilt.android", version.ref = "hilt" }}
ksp = {{ id = "com.google.devtools.ksp", version.ref = "ksp" }}
"""


class PermissionManager:
    """Manages Android runtime permissions declarations."""

    def __init__(self):
        self._declared: List[PermissionType] = []
        self._callback: Optional[Callable[[PermissionType], None]] = None

    def declare(self, *permissions: PermissionType) -> PermissionManager:
        for perm in permissions:
            if perm not in self._declared:
                self._declared.append(perm)
        return self

    def on_result(self, callback: Callable[[PermissionType], None]) -> PermissionManager:
        self._callback = callback
        return self

    def generate_manifest_entries(self) -> str:
        if not self._declared:
            return "<!-- No permissions declared -->"
        lines = [f'    <uses-permission android:name="{p.value}" />' for p in self._declared]
        return "\n".join(lines)

    def generate_permission_handler(self) -> str:
        permission_map = {p.value.split(".")[-1].lower(): p.value for p in self._declared}
        return f"""class PermissionHandler {{
    private val requiredPermissions = listOf(
{chr(10).join(f'        "{v}"' for v in permission_map.values())}
    )

    fun checkPermissions(context: Context): List<String> {{
        return requiredPermissions.filter {{
            ContextCompat.checkSelfPermission(context, it) != PackageManager.PERMISSION_GRANTED
        }}
    }}

    fun requestPermissions(activity: Activity, permissions: List<String>) {{
        ActivityCompat.requestPermissions(activity, permissions.toTypedArray(), REQUEST_CODE)
    }}
}}

const val REQUEST_CODE = 1001
"""

    @property
    def declared_count(self) -> int:
        return len(self._declared)


class AndroidProjectScaffolder:
    """Creates Android project directory structure."""

    def __init__(self, config: AndroidConfig, base_path: Path):
        self.config = config
        self.base_path = base_path
        self.build_gen = GradleBuildGenerator(config)
        self.perm_manager = PermissionManager()

    def scaffold(self) -> Dict[str, Path]:
        created: Dict[str, Path] = {}
        package_path = self.config.application_id.replace(".", "/")

        directories = [
            "app/src/main/java" + package_path,
            "app/src/main/java" + package_path + "/di",
            "app/src/main/java" + package_path + "/data/repository",
            "app/src/main/java" + package_path + "/data/local",
            "app/src/main/java" + package_path + "/data/remote",
            "app/src/main/java" + package_path + "/domain/usecase",
            "app/src/main/java" + package_path + "/domain/model",
            "app/src/main/java" + package_path + "/ui/home",
            "app/src/main/java" + package_path + "/ui/theme",
            "app/src/main/res/values",
            "app/src/test/java" + package_path,
            "app/src/androidTest/java" + package_path,
            "gradle",
        ]

        for d in directories:
            dir_path = self.base_path / d
            dir_path.mkdir(parents=True, exist_ok=True)
            created[d] = dir_path

        # Write build files
        build_gradle = self.base_path / "app" / "build.gradle.kts"
        build_gradle.write_text(self.build_gen.generate_build_gradle(), encoding="utf-8")
        created["app/build.gradle.kts"] = build_gradle

        settings_gradle = self.base_path / "settings.gradle.kts"
        settings_gradle.write_text(self.build_gen.generate_settings_gradle(), encoding="utf-8")
        created["settings.gradle.kts"] = settings_gradle

        version_catalog = self.base_path / "gradle" / "libs.versions.toml"
        version_catalog.write_text(self.build_gen.generate_version_catalog(), encoding="utf-8")
        created["gradle/libs.versions.toml"] = version_catalog

        return created

    def get_summary(self) -> Dict[str, Any]:
        return {
            "application_id": self.config.application_id,
            "min_sdk": self.config.min_sdk,
            "target_sdk": self.config.target_sdk,
            "architecture": self.config.architecture.value,
            "use_compose": self.config.use_compose,
            "use_hilt": self.config.use_hilt,
            "use_room": self.config.use_room,
            "permissions_declared": self.perm_manager.declared_count,
            "build_types": [bt.value for bt in self.config.build_types],
        }


class ManifestGenerator:
    """Generates AndroidManifest.xml content."""

    def __init__(self, config: AndroidConfig, permissions: Optional[PermissionManager] = None):
        self.config = config
        self.permissions = permissions or PermissionManager()

    def generate(self) -> str:
        perm_entries = self.permissions.generate_manifest_entries()
        return f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

{perm_entries}

    <application
        android:name=".App"
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.App">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.App">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""


def main():
    config = AndroidConfig(
        application_id="com.example.myapp",
        min_sdk=26,
        target_sdk=34,
        architecture=ArchitectureType.CLEAN_ARCHITECTURE,
        use_compose=True,
        use_hilt=True,
        use_room=True,
    )

    scaffolder = AndroidProjectScaffolder(config, Path("./my-android-app"))
    summary = scaffolder.get_summary()
    print("=== Android Project Configuration ===")
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print("\n=== Generated Gradle Build Script ===")
    gen = GradleBuildGenerator(config)
    gen.add_dependency(Dependency("androidx.core", "core-ktx", "1.12.0"))
    gen.add_dependency(Dependency("androidx.activity", "activity-compose", "1.8.2"))
    print(gen.generate_build_gradle()[:500] + "\n...")

    print("=== Manifest Generation ===")
    manifest_gen = ManifestGenerator(config, scaffolder.perm_manager)
    print(manifest_gen.generate()[:400] + "\n...")

    print("\n=== Project scaffold created ===")
    print(f"Architecture: {config.architecture.value}")
    print(f"Compose UI: {config.use_compose}")
    print(f"Hilt DI: {config.use_hilt}")
    print("Done.")


if __name__ == "__main__":
    main()
