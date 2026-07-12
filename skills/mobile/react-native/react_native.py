"""
React Native Module
Part of the mobile skill domain.

Provides React Native project scaffolding, native module bridge generation,
performance configuration, and cross-platform deployment utilities.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set


class ReactNativeArch(Enum):
    OLD = "old_architecture"
    NEW = "new_architecture"


class NavigationLib(Enum):
    REACT_NAVIGATION = "react-navigation"
    FLIPPER = "flipper"
    NONE = "none"


class StateManager(Enum):
    ZUSTAND = "zustand"
    REDUX_TOOLKIT = "redux-toolkit"
    JOTAI = "jotai"
    MOBX = "mobx"
    CONTEXT_API = "context-api"


class StyleSheetFlavor(Enum):
    STYLES_SHEET = "StyleSheet"  # React Native built-in
    TWIND = "twind"
    NATIVE_WIND = "native-wind"
    TAMAGUI = "tamagui"


@dataclass
class NativeModuleSpec:
    name: str
    methods: List[Dict[str, str]] = field(default_factory=list)
    constants: Dict[str, str] = field(default_factory=dict)
    events: List[str] = field(default_factory=list)

    def to_turbo_module_spec(self) -> str:
        method_lines = []
        for m in self.methods:
            params = ", ".join(f"{k}: {v}" for k, v in m.get("params", {}).items()) if "params" in m else ""
            ret = m.get("return", "void")
            method_lines.append(f"  {m['name']}({params}): Promise<{ret}>;")

        events_str = ", ".join(f"'{e}'" for e in self.events) if self.events else ""

        return f"""// Turbo Module Spec: {self.name}
import type {{ TurboModule }} from 'react-native';
import {{ TurboModuleRegistry }} from 'react-native';

export interface Spec extends TurboModule {{
{chr(10).join(method_lines)}
  getConstants(): {{
{chr(10).join(f"    {k}: {v};" for k, v in self.constants.items()) if self.constants else "    // no constants"}
  }};
}}

export default TurboModuleRegistry.getEnforcing<Spec>('{self.name}');
"""


@dataclass
class ReactNativeConfig:
    name: str
    bundle_id: str
    version: str = "1.0.0"
    architecture: ReactNativeArch = ReactNativeArch.NEW
    navigation: NavigationLib = NavigationLib.REACT_NAVIGATION
    state_manager: StateManager = StateManager.ZUSTAND
    style_flavor: StyleSheetFlavor = StyleSheetFlavor.NATIVE_WIND
    use_hermes: bool = True
    use_flipper: bool = True
    use_codegen: bool = True
    min_sdk: int = 23
    target_sdk: int = 34
    ios_deployment_target: str = "14.0"
    native_modules: List[NativeModuleSpec] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


class PackageJsonGenerator:
    """Generates package.json for React Native projects."""

    def __init__(self, config: ReactNativeConfig):
        self.config = config

    def generate(self) -> str:
        deps = self._get_dependencies()
        dev_deps = self._get_dev_dependencies()

        return f"""{{
  "name": "{self.config.name}",
  "version": "{self.config.version}",
  "private": true,
  "scripts": {{
    "android": "react-native run-android",
    "ios": "react-native run-ios",
    "start": "react-native start",
    "lint": "eslint . --ext .ts,.tsx",
    "test": "jest",
    "clean": "react-native clean",
    "codegen": "react-native codegen"
  }},
  "dependencies": {{
{deps}
  }},
  "devDependencies": {{
{dev_deps}
  }},
  "engines": {{
    "node": ">=18"
  }}
}}
"""

    def _get_dependencies(self) -> str:
        lines = []
        lines.append('    "react": "^18.2.0",')
        lines.append('    "react-native": "^0.73.2",')

        if self.config.use_hermes:
            lines.append('    "react-native-flipper": "^0.232.0",')

        if self.config.navigation == NavigationLib.REACT_NAVIGATION:
            lines.append('    "@react-navigation/native": "^6.1.9",')
            lines.append('    "@react-navigation/native-stack": "^6.9.17",')
            lines.append('    "react-native-screens": "^3.29.0",')
            lines.append('    "react-native-safe-area-context": "^4.8.2",')

        if self.config.state_manager == StateManager.ZUSTAND:
            lines.append('    "zustand": "^4.4.7",')
            lines.append('    "@react-native-async-storage/async-storage": "^1.21.0",')
        elif self.config.state_manager == StateManager.REDUX_TOOLKIT:
            lines.append('    "@reduxjs/toolkit": "^2.0.1",')
            lines.append('    "react-redux": "^9.0.4",')

        if self.config.style_flavor == StyleSheetFlavor.NATIVE_WIND:
            lines.append('    "nativewind": "^2.0.11",')
            lines.append('    "tailwindcss": "^3.4.0",')

        lines.append('    "react-native-reanimated": "^3.6.1",')
        lines.append('    "react-native-gesture-handler": "^2.14.0",')
        lines.append('    "react-native-vector-icons": "^10.0.3",')

        for dep in self.config.dependencies:
            lines.append(f'    "{dep}",')

        return "\n".join(lines)

    def _get_dev_dependencies(self) -> str:
        lines = [
            '    "@types/react": "^18.2.48",',
            '    "@types/react-native": "^0.73.0",',
            '    "typescript": "^5.3.3",',
            '    "jest": "^29.7.0",',
            '    "@testing-library/react-native": "^12.4.3",',
            '    "eslint": "^8.56.0",',
            '    "@typescript-eslint/eslint-plugin": "^6.19.0",',
            '    "prettier": "^3.2.4",',
        ]
        if self.config.use_flipper:
            lines.append('    "flipper-pod": "^0.232.0",')
        if self.config.use_codegen:
            lines.append('    "@react-native/codegen": "^0.73.2",')
        return "\n".join(lines)


class NativeModuleGenerator:
    """Generates React Native native module bridge code."""

    def __init__(self, config: ReactNativeConfig):
        self.config = config

    def generate_typescript_spec(self, module: NativeModuleSpec) -> str:
        return module.to_turbo_module_spec()

    def generate_ios_swift(self, module: NativeModuleSpec) -> str:
        method_impls = []
        for m in module.methods:
            params = m.get("params", {})
            param_str = ", ".join(f"{k}: {self._ts_to_swift_type(v)}" for k, v in params.items())
            method_impls.append(f"""
    @objc func {m['name']}({param_str}, resolve: @escaping RCTPromiseResolveBlock, rejecter reject: @escaping RCTPromiseRejectBlock) {{
        // TODO: Implement {m['name']}
        resolve(nil)
    }}""")

        constants_impl = ""
        if module.constants:
            const_entries = ", ".join(f'"{k}": {v}' for k, v in module.constants.items())
            constants_impl = f"""
    override func constantsToExport() -> [AnyHashable: Any]! {{
        return [{const_entries}]
    }}"""

        return f"""import Foundation
import React

@objc({module.name}Module)
class {module.name}Module: NSObject {{

    static func requiresMainQueueSetup() -> Bool {{
        return false
    }}
{constants_impl}
{"".join(method_impls)}
}}
"""

    def generate_android_kotlin(self, module: NativeModuleSpec) -> str:
        method_impls = []
        for m in module.methods:
            params = m.get("params", {})
            param_str = ", ".join(f"{k}: {self._ts_to_kotlin_type(v)}" for k, v in params.items())
            method_impls.append(f"""
    @ReactMethod
    fun {m['name']}({param_str}, promise: Promise) {{
        // TODO: Implement {m['name']}
        promise.resolve(null)
    }}""")

        constants_impl = ""
        if module.constants:
            const_entries = "\n".join(f'            put("{k}", {v})' for k, v in module.constants.items())
            constants_impl = f"""
    override fun getConstants(): MutableMap<String, Any> {{
        return mutableMapOf(
{const_entries}
        )
    }}"""

        return f"""package com.{self.config.bundle_id.replace(".", ".")}

import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.bridge.ReactContextBaseJavaModule
import com.facebook.react.bridge.ReactMethod
import com.facebook.react.bridge.Promise

class {module.name}Module(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {{

    override fun getName(): String = "{module.name}"
{constants_impl}
{"".join(method_impls)}
}}
"""

    def generate_ios_podspec(self) -> str:
        return f"""require 'json'

package = JSON.parse(File.read(File.join(__dir__, 'package.json')))

Pod::Spec.new do |s|
  s.name         = "{self.config.name}"
  s.version      = package['version']
  s.summary      = package['description']
  s.homepage     = "https://github.com/example/{self.config.name}"
  s.license      = "MIT"
  s.author       = "Author"
  s.source       = {{ :git => "https://github.com/example/{self.config.name}.git", :tag => s.version }}

  s.platform     = :ios, "{self.config.ios_deployment_target}"
  s.swift_version = "5.0"

  s.source_files = "ios/**/*.{h,m,mm,swift}"

  s.dependency "React-Core"
end
"""

    @staticmethod
    def _ts_to_swift_type(ts_type: str) -> str:
        mapping = {"string": "String", "number": "Double", "boolean": "Bool", "void": "Void"}
        return mapping.get(ts_type, "Any")

    @staticmethod
    def _ts_to_kotlin_type(ts_type: str) -> str:
        mapping = {"string": "String", "number": "Double", "boolean": "Boolean", "void": "Unit"}
        return mapping.get(ts_type, "Any?")


class ReactNativePerformanceConfig:
    """Generates performance optimization configurations."""

    def __init__(self, config: ReactNativeConfig):
        self.config = config

    def generate_hermes_config(self) -> str:
        return f"""// Hermes Engine Configuration
// Enabled: {self.config.use_hermes}

// In android/app/build.gradle:
// project.ext.react = [
//     enableHermes: {str(self.config.use_hermes).lower()},
//     hermesCommand: "node_modules/hermes-engine/{'osx-bin' if platform == 'darwin' else 'linux64-bin'}/hermesc"
// ]

// In ios/Podfile:
// :hermes_enabled => {str(self.config.use_hermes).lower()}
"""

    def generate_flipper_config(self) -> str:
        return f"""// Flipper Debug Configuration
// Enabled: {self.config.use_flipper}

// In ios/YourApp/AppDelegate.m:
#if DEBUG
#import <FlipperKit/FlipperClient.h>
#import <FlipperKitLayoutPlugin/FlipperKitLayoutPlugin.h>
#import <FlipperKitUserDefaultsPlugin/FKUserDefaultsPlugin.h>
#import <FlipperKitNetworkPlugin/FlipperKitNetworkPlugin.h>

static void InitializeFlipper(UIApplication *application) {{
    FlipperClient *client = [FlipperClient sharedClient];
    SKDescriptorMapper *layoutDescriptorMapper = [[SKDescriptorMapper alloc] init];
    [client addPlugin:[[FlipperKitLayoutPlugin alloc] initWithDescriptorMapper:layoutDescriptorMapper]];
    [client addPlugin:[[FKUserDefaultsPlugin alloc] initWithSuiteName:nil]];
    [client addPlugin:[[FlipperKitNetworkPlugin alloc] initWithNetworkAdapter:[SKIOSNetworkAdapter new]]];
    [client start];
}}
#endif
"""

    def generate_performance_hooks(self) -> str:
        return f"""import {{ InteractionManager, AppState, Performance }} from 'react-native';

export class PerformanceManager {{
  private static marks: Map<string, number> = new Map();

  static mark(name: string): void {{
    this.marks.set(name, performance.now());
  }}

  static measure(name: string): number {{
    const start = this.marks.get(name);
    if (!start) return 0;
    const duration = performance.now() - start;
    this.marks.delete(name);

    if (__DEV__) {{
      console.log(`[PERF] ${{name}}: ${{duration.toFixed(2)}}ms`);
    }}

    return duration;
  }}

  static async runAfterInteractions<T>(fn: () => Promise<T>): Promise<T> {{
    return new Promise((resolve) => {{
      InteractionManager.runAfterInteractions(async () => {{
        const result = await fn();
        resolve(result);
      }});
    }});
  }}

  static trackAppStartup(): void {{
    this.mark('app_startup');
    AppState.addEventListener('change', (state) => {{
      if (state === 'active') {{
        this.measure('app_startup');
      }}
    }});
  }}
}}
"""


class MetroConfigGenerator:
    """Generates Metro bundler configuration."""

    def generate(self, config: ReactNativeConfig) -> str:
        return f"""const {{ getDefaultConfig, mergeConfig }} = require('@react-native/metro-config');

const config = {{
  resolver: {{
    sourceExts: ['ts', 'tsx', 'js', 'jsx', 'json'],
    assetExts: ['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'],
  }},
  transformer: {{
    getTransformOptions: async () => ({
      transform: {{
        experimentalImportSupport: true,
        inlineRequires: true,
      }},
    }),
  }},
  serializer: {{
    customSerializer: undefined,
  }},
}};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
"""


def main():
    config = ReactNativeConfig(
        name="MyRNApp",
        bundle_id="com.example.myrnapp",
        architecture=ReactNativeArch.NEW,
        navigation=NavigationLib.REACT_NAVIGATION,
        state_manager=StateManager.ZUSTAND,
        style_flavor=StyleSheetFlavor.NATIVE_WIND,
        use_hermes=True,
        use_flipper=True,
        native_modules=[
            NativeModuleSpec(
                name="DeviceUtils",
                methods=[
                    {"name": "getModel", "return": "string"},
                    {"name": "getBatteryLevel", "return": "number"},
                ],
                constants={"platform": "'react-native'"},
            ),
        ],
    )

    print("=== React Native Configuration ===")
    print(f"  Architecture: {config.architecture.value}")
    print(f"  Navigation: {config.navigation.value}")
    print(f"  State: {config.state_manager.value}")
    print(f"  Hermes: {config.use_hermes}")

    pkg_gen = PackageJsonGenerator(config)
    print("\n=== package.json ===")
    print(pkg_gen.generate()[:500] + "\n...")

    mod_gen = NativeModuleGenerator(config)
    print("\n=== Turbo Module Spec ===")
    print(mod_gen.generate_typescript_spec(config.native_modules[0]))

    print("\n=== Swift Native Module ===")
    print(mod_gen.generate_ios_swift(config.native_modules[0])[:500] + "\n...")

    print("\n=== Kotlin Native Module ===")
    print(mod_gen.generate_android_kotlin(config.native_modules[0])[:500] + "\n...")

    perf = ReactNativePerformanceConfig(config)
    print("\n=== Performance Hooks ===")
    print(perf.generate_performance_hooks()[:400] + "\n...")

    metro = MetroConfigGenerator()
    print("\n=== Metro Config ===")
    print(metro.generate(config)[:400] + "\n...")

    print("\nDone.")


if __name__ == "__main__":
    main()
