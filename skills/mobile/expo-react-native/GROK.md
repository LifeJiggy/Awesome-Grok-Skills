---
name: expo-react-native
category: mobile
version: 2.0.0
tags: [mobile, expo, react-native, javascript, cross-platform]
---

# Expo React Native

## Overview

Expo-managed React Native development for rapid cross-platform mobile app creation. Expo provides a managed workflow with pre-built native modules, OTA updates, EAS Build services, and a comprehensive CLI toolchain. This skill covers Expo SDK usage, managed vs. bare workflows, Expo Router navigation, EAS Build/Submit pipelines, and production-grade patterns for shipping iOS and Android apps from a single JavaScript/TypeScript codebase.

## Core Capabilities

- **Expo Router**: File-based routing with deep linking, typed routes, and stack/tab/navigator patterns
- **EAS Build**: Cloud-based native builds with custom build profiles and matrix builds
- **EAS Submit**: Automated App Store and Play Store submission pipelines
- **OTA Updates**: Over-the-air JavaScript bundle updates with channel-based rollout
- **Expo Modules**: Native module creation with Swift/Kotlin via Expo Modules API
- **Notifications**: Push notification handling with Expo Notifications SDK
- **Camera, Media, FileSystem**: Access to device hardware through managed APIs
- **Dev Client**: Custom development builds with native module support

## Usage Examples

```typescript
// app/_layout.tsx — Expo Router root layout
import { Stack } from "expo-router";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="modal" options={{ presentation: "modal" }} />
        <Stack.Screen name="detail/[id]" options={{ headerShown: true, title: "Detail" }} />
      </Stack>
    </QueryClientProvider>
  );
}

// app/(tabs)/_layout.tsx — Tab navigation
import { Tabs } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="index" options={{
        title: "Home",
        tabBarIcon: ({ color, size }) => <Ionicons name="home" size={size} color={color} />
      }} />
      <Tabs.Screen name="settings" options={{
        title: "Settings",
        tabBarIcon: ({ color, size }) => <Ionicons name="settings" size={size} color={color} />
      }} />
    </Tabs>
  );
}

// hooks/useApiClient.ts — Custom hook with EAS constants
import * as SecureStore from "expo-secure-store";
import Constants from "expo-constants";

export function useApiClient() {
  const baseURL = Constants.expoConfig?.extra?.apiBase ?? "https://api.example.com";

  const fetchWithAuth = async (path: string, options: RequestInit = {}) => {
    const token = await SecureStore.getItemAsync("auth_token");
    return fetch(`${baseURL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...options.headers,
      },
    });
  };

  return { fetchWithAuth };
}

// app.config.ts — Dynamic Expo configuration
import { ExpoConfig, ConfigContext } from "expo/config";

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: "MyApp",
  slug: "myapp",
  version: "1.0.0",
  orientation: "portrait",
  icon: "./assets/icon.png",
  scheme: "myapp",
  extra: {
    apiBase: process.env.API_BASE_URL ?? "https://api.example.com",
    eas: { projectId: "your-project-id" },
  },
  plugins: [
    "expo-router",
    ["expo-notifications", { icon: "./assets/notification-icon.png" }],
    ["expo-camera", { cameraPermission: "Allow camera access for scanning." }],
  ],
  experiments: { typedRoutes: true },
});
```

## Best Practices

- Use Expo Router for file-based navigation with typed routes enabled
- Prefer EAS Build over local builds for reproducible, CI-compatible native builds
- Use EAS Update with channel-based rollouts for safe OTA deployments
- Store sensitive data with expo-secure-store, never AsyncStorage
- Use `expo-constants` for environment-specific configuration
- Implement error boundaries at layout and screen levels
- Use React Query or SWR for server state management
- Test with Expo Dev Client for custom native module support
- Leverage `expo prebuild` to inspect and customize native code when needed
- Profile bundle size with `expo export` and analyze with `react-native-bundle-visualizer`

## Related Modules

- `react-native` - Bare React Native development without Expo managed workflow
- `android-development` - Native Android development considerations
- `ios-development` - Native iOS development considerations
- `flutter-naija` - Alternative cross-platform framework comparison
