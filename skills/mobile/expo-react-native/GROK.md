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

## Advanced Configuration

### EAS Build Configuration

```json
// eas.json
{
  "cli": {
    "version": ">= 7.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      }
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "simulator": false
      }
    },
    "production": {
      "autoIncrement": true,
      "ios": {
        "simulator": false
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your-apple-id@example.com",
        "ascAppId": "your-asc-app-id",
        "appleTeamId": "your-team-id"
      },
      "android": {
        "serviceAccountKeyPath": "./google-service-account.json",
        "track": "production"
      }
    }
  }
}
```

### Expo Router Configuration

```typescript
// app/_layout.tsx - Advanced layout with providers
import { Stack } from "expo-router";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "@/contexts/AuthContext";
import { ThemeProvider } from "@/contexts/ThemeContext";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 2,
    },
  },
});

export default function RootLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <ThemeProvider>
            <Stack screenOptions={{ headerShown: false }}>
              <Stack.Screen name="(auth)" />
              <Stack.Screen name="(tabs)" />
              <Stack.Screen
                name="modal"
                options={{ presentation: "modal" }}
              />
              <Stack.Screen
                name="detail/[id]"
                options={{ headerShown: true, title: "Detail" }}
              />
            </Stack>
          </ThemeProvider>
        </AuthProvider>
      </QueryClientProvider>
    </GestureHandlerRootView>
  );
}

// app/(auth)/_layout.tsx - Auth flow layout
import { Redirect, Stack } from "expo-router";
import { useAuth } from "@/contexts/AuthContext";

export default function AuthLayout() {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Redirect href="/(tabs)" />;
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="login" />
      <Stack.Screen name="register" />
    </Stack>
  );
}
```

### Expo Notifications Configuration

```typescript
// utils/notifications.ts
import * as Notifications from "expo-notifications";
import * as Device from "expo-device";
import { Platform } from "react-native";

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

export async function registerForPushNotifications() {
  if (!Device.isDevice) {
    console.log("Must use physical device for push notifications");
    return null;
  }

  const { status: existingStatus } =
    await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== "granted") {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== "granted") {
    console.log("Failed to get push token for push notification!");
    return null;
  }

  const token = await Notifications.getExpoPushTokenAsync({
    projectId: "your-project-id",
  });

  if (Platform.OS === "android") {
    Notifications.setNotificationChannelAsync("default", {
      name: "default",
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: "#FF231F7C",
    });
  }

  return token.data;
}

export function setupNotificationListeners(
  onNotificationReceived: (notification: Notifications.Notification) => void,
  onNotificationTapped: (response: Notifications.NotificationResponse) => void
) {
  const receivedSubscription = Notifications.addNotificationReceivedListener(
    onNotificationReceived
  );

  const responseSubscription =
    Notifications.addNotificationResponseReceivedListener(onNotificationTapped);

  return () => {
    receivedSubscription.remove();
    responseSubscription.remove();
  };
}
```

## Architecture Patterns

### Expo Project Structure

```
├── app/                    # Expo Router file-based routing
│   ├── (auth)/            # Auth flow screens
│   ├── (tabs)/            # Tab navigation screens
│   ├── _layout.tsx        # Root layout
│   ├── modal.tsx          # Modal screen
│   └── detail/[id].tsx    # Dynamic route
├── components/            # Reusable UI components
│   ├── ui/               # Base UI components
│   └── features/         # Feature-specific components
├── contexts/              # React contexts
├── hooks/                 # Custom hooks
├── services/              # API and business logic
├── utils/                 # Utility functions
├── types/                 # TypeScript types
├── assets/               # Static assets
├── app.config.ts         # Expo configuration
├── eas.json              # EAS Build configuration
└── tsconfig.json         # TypeScript configuration
```

### State Management Pattern

```typescript
// contexts/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from "react";
import * as SecureStore from "expo-secure-store";
import { useRouter } from "expo-router";

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  user: User | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    checkAuthState();
  }, []);

  const checkAuthState = async () => {
    try {
      const token = await SecureStore.getItemAsync("auth_token");
      if (token) {
        const userData = await fetchUser(token);
        setUser(userData);
      }
    } catch (error) {
      console.error("Auth state check failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      const response = await api.login(email, password);
      await SecureStore.setItemAsync("auth_token", response.token);
      setUser(response.user);
      router.replace("/(tabs)");
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    await SecureStore.deleteItemAsync("auth_token");
    setUser(null);
    router.replace("/(auth)/login");
  };

  return (
    <AuthContext.Provider
      value={{ isAuthenticated: !!user, isLoading, login, logout, user }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
```

### API Layer Pattern

```typescript
// services/api.ts
import * as SecureStore from "expo-secure-store";
import Constants from "expo-constants";

const baseURL =
  Constants.expoConfig?.extra?.apiBase ?? "https://api.example.com";

class ApiClient {
  private async getHeaders(): Promise<HeadersInit> {
    const token = await SecureStore.getItemAsync("auth_token");
    return {
      "Content-Type": "application/json",
      Authorization: token ? `Bearer ${token}` : "",
    };
  }

  async request<T>(
    method: string,
    path: string,
    body?: unknown
  ): Promise<T> {
    const headers = await this.getHeaders();
    const response = await fetch(`${baseURL}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new ApiError(error.message, response.status);
    }

    return response.json();
  }

  get<T>(path: string) {
    return this.request<T>("GET", path);
  }

  post<T>(path: string, body: unknown) {
    return this.request<T>("POST", path, body);
  }

  put<T>(path: string, body: unknown) {
    return this.request<T>("PUT", path, body);
  }

  delete<T>(path: string) {
    return this.request<T>("DELETE", path);
  }
}

export const api = new ApiClient();
```

## Integration Guide

### Firebase Integration

```typescript
// config/firebase.ts
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";

const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: process.env.FIREBASE_AUTH_DOMAIN,
  projectId: process.env.FIREBASE_PROJECT_ID,
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.FIREBASE_APP_ID,
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);
```

### Analytics Integration

```typescript
// utils/analytics.ts
import * as Analytics from "expo-analytics";

const analytics = new Analytics.Analytics("UA-XXXXX-Y");

export const trackEvent = (
  category: string,
  action: string,
  label?: string,
  value?: number
) => {
  analytics.event(category, action, label, value);
};

export const trackScreenView = (screenName: string) => {
  analytics.hit(new Analytics.Hit("screenview", screenName));
};

export const trackTiming = (
  category: string,
  variable: string,
  time: number
) => {
  analytics.timing(category, variable, time);
};
```

## Performance Optimization

### Image Optimization

```typescript
// components/OptimizedImage.tsx
import React from "react";
import { Image, ImageStyle, StyleProp } from "react-native";
import { BlurView } from "expo-blur";

interface OptimizedImageProps {
  uri: string;
  style?: StyleProp<ImageStyle>;
  placeholder?: boolean;
}

export function OptimizedImage({
  uri,
  style,
  placeholder = true,
}: OptimizedImageProps) {
  const [loaded, setLoaded] = React.useState(false);

  return (
    <>
      {placeholder && !loaded && (
        <BlurView intensity={100} style={[style, { position: "absolute" }]}>
          <Image
            source={{ uri }}
            style={[style, { opacity: 0 }]}
            onLoad={() => setLoaded(true)}
          />
        </BlurView>
      )}
      <Image
        source={{ uri }}
        style={[style, !loaded && { opacity: 0 }]}
        onLoad={() => setLoaded(true)}
        resizeMode="cover"
      />
    </>
  );
}
```

### Bundle Optimization

```typescript
// utils/bundleOptimizer.ts
import * as Updates from "expo-updates";

export const checkForUpdates = async () => {
  try {
    if (__DEV__) return false;

    const update = await Updates.checkForUpdateAsync();
    if (update.isAvailable) {
      await Updates.fetchUpdateAsync();
      await Updates.reloadAsync();
      return true;
    }
    return false;
  } catch (error) {
    console.error("Error checking for updates:", error);
    return false;
  }
};
```

### Memory Management

```typescript
// hooks/useMemoryOptimization.ts
import { useEffect, useRef } from "react";
import { AppState, AppStateStatus } from "react-native";

export function useMemoryOptimization() {
  const appState = useRef(AppState.currentState);

  useEffect(() => {
    const subscription = AppState.addEventListener(
      "change",
      handleAppStateChange
    );

    return () => subscription.remove();
  }, []);

  const handleAppStateChange = (nextState: AppStateStatus) => {
    if (appState.current === "active" && nextState.match(/inactive|background/)) {
      // App going to background - cleanup resources
      cleanupResources();
    }

    if (appState.current.match(/inactive|background/) && nextState === "active") {
      // App coming to foreground - refresh resources
      refreshResources();
    }

    appState.current = nextState;
  };

  const cleanupResources = () => {
    // Cancel ongoing requests, clear caches, etc.
  };

  const refreshResources = () => {
    // Refresh data, reconnect sockets, etc.
  };
}
```

## Security Considerations

### Secure Storage

```typescript
// utils/secureStorage.ts
import * as SecureStore from "expo-secure-store";

export const secureStorage = {
  async set(key: string, value: string): Promise<void> {
    try {
      await SecureStore.setItemAsync(key, value);
    } catch (error) {
      console.error("Failed to save to secure storage:", error);
      throw error;
    }
  },

  async get(key: string): Promise<string | null> {
    try {
      return await SecureStore.getItemAsync(key);
    } catch (error) {
      console.error("Failed to read from secure storage:", error);
      throw error;
    }
  },

  async remove(key: string): Promise<void> {
    try {
      await SecureStore.deleteItemAsync(key);
    } catch (error) {
      console.error("Failed to delete from secure storage:", error);
      throw error;
    }
  },

  async clear(): Promise<void> {
    try {
      await SecureStore.deleteItemAsync("auth_token");
      await SecureStore.deleteItemAsync("refresh_token");
      await SecureStore.deleteItemAsync("user_data");
    } catch (error) {
      console.error("Failed to clear secure storage:", error);
      throw error;
    }
  },
};
```

### Certificate Pinning

```typescript
// config/networkSecurity.ts
import * as SSLCertificateStore from "expo-ssl-certificate-store";

export const setupCertificatePinning = async () => {
  const certificates = [
    {
      host: "api.example.com",
      certificate: require("../certs/api.example.com.pem"),
    },
  ];

  await SSLCertificateStore.addCertificates(certificates);
};
```

## Troubleshooting Guide

### Common Issues

#### Issue: OTA Update Failures

```typescript
// utils/updateDiagnostics.ts
import * as Updates from "Updates";

export const diagnoseUpdateIssue = async () => {
  const update = await Updates.checkForUpdateAsync();

  console.log("Update available:", update.isAvailable);
  console.log("Update manifest:", update.manifest);

  if (update.isAvailable) {
    try {
      await Updates.fetchUpdateAsync();
      console.log("Update fetched successfully");
    } catch (error) {
      console.error("Failed to fetch update:", error);
    }
  }
};
```

#### Issue: Navigation Deep Links

```typescript
// utils/deepLinkDiagnostics.ts
import * as Linking from "expo-linking";

export const testDeepLink = async (url: string) => {
  const supported = await Linking.canOpenURL(url);
  console.log("Deep link supported:", supported);

  if (supported) {
    await Linking.openURL(url);
  }
};
```

#### Issue: Push Notification Issues

```typescript
// utils/notificationDiagnostics.ts
import * as Notifications from "expo-notifications";

export const diagnosePushNotifications = async () => {
  const settings = await Notifications.getPermissionsAsync();
  console.log("Notification permissions:", settings);

  if (settings.status !== "granted") {
    console.log("Notification permissions not granted");
    return;
  }

  const token = await Notifications.getExpoPushTokenAsync({
    projectId: "your-project-id",
  });
  console.log("Push token:", token.data);
};
```

## API Reference

### Expo Router API

```typescript
// Navigation methods
import { useRouter, useLocalSearchParams, useNavigation } from "expo-router";

// Navigate to route
const router = useRouter();
router.push("/detail/123");
router.replace("/(tabs)");
router.back();

// Get route params
const { id } = useLocalSearchParams<{ id: string }>();

// Set navigation options
const navigation = useNavigation();
navigation.setOptions({ title: "New Title" });
```

### Expo Notifications API

```typescript
// Notification methods
import * as Notifications from "expo-notifications";

// Schedule local notification
await Notifications.scheduleNotificationAsync({
  content: {
    title: "Reminder",
    body: "You have a meeting in 30 minutes",
    data: { meetingId: "123" },
  },
  trigger: {
    seconds: 60 * 30, // 30 minutes
  },
});

// Cancel notification
await Notifications.cancelScheduledNotificationAsync("notification-id");
```

### Expo SecureStore API

```typescript
// Secure storage methods
import * as SecureStore from "expo-secure-store";

// Store value
await SecureStore.setItemAsync("key", "value");

// Get value
const value = await SecureStore.getItemAsync("key");

// Delete value
await SecureStore.deleteItemAsync("key");

// Check if key exists
const exists = await SecureStore.getItemAsync("key") !== null;
```

## Data Models

### TypeScript Types

```typescript
// types/models.ts
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Item {
  id: string;
  title: string;
  description: string;
  imageUrl: string;
  price: number;
  category: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}

// types/navigation.ts
export type RootStackParamList = {
  "(auth)": undefined;
  "(tabs)": undefined;
  modal: undefined;
  "detail/[id]": { id: string };
};

export type AuthStackParamList = {
  login: undefined;
  register: undefined;
};

export type TabParamList = {
  index: undefined;
  settings: undefined;
};
```

## Deployment Guide

### EAS Build Process

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to EAS
eas login

# Configure project
eas build:configure

# Build for development
eas build --profile development --platform ios
eas build --profile development --platform android

# Build for preview
eas build --profile preview --platform all

# Build for production
eas build --profile production --platform all
```

### EAS Submit Process

```bash
# Submit to App Store
eas submit --platform ios --profile production

# Submit to Play Store
eas submit --platform android --profile production

# Submit to both stores
eas submit --platform all --profile production
```

### OTA Update Process

```bash
# Publish OTA update
eas update --branch main --message "Bug fixes"

# Publish to specific channel
eas update --channel production --message "Performance improvements"

# Rollback update
eas update --branch main --rollback
```

## Monitoring & Observability

### Error Tracking

```typescript
// utils/errorTracking.ts
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "your-dsn",
  environment: __DEV__ ? "development" : "production",
  enableAutoSessionTracking: true,
  sessionTrackingIntervalMillis: 30000,
  enableNative: true,
});

export const captureError = (error: Error, context?: Record<string, unknown>) => {
  Sentry.withScope((scope) => {
    if (context) {
      Object.entries(context).forEach(([key, value]) => {
        scope.setExtra(key, value);
      });
    }
    Sentry.captureException(error);
  });
};

export const captureMessage = (message: string, level: Sentry.Severity = "info") => {
  Sentry.captureMessage(message, level);
};
```

### Performance Monitoring

```typescript
// utils/performance.ts
import * as Performance from "expo-performance";

export const measureAsync = async <T>(
  name: string,
  fn: () => Promise<T>
): Promise<T> => {
  const trace = Performance.startTrace(name);
  try {
    const result = await fn();
    trace.stop();
    return result;
  } catch (error) {
    trace.stop();
    throw error;
  }
};

export const measureSync = <T>(name: string, fn: () => T): T => {
  const trace = Performance.startTrace(name);
  try {
    const result = fn();
    trace.stop();
    return result;
  } catch (error) {
    trace.stop();
    throw error;
  }
};
```

## Testing Strategy

### Unit Tests

```typescript
// __tests__/utils/api.test.ts
import { api } from "@/utils/api";

describe("ApiClient", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should make GET request", async () => {
    const mockFetch = jest.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: "test" }),
    });
    global.fetch = mockFetch;

    const result = await api.get("/test");
    expect(result).toEqual({ data: "test" });
    expect(mockFetch).toHaveBeenCalledWith(
      "https://api.example.com/test",
      expect.objectContaining({ method: "GET" })
    );
  });

  it("should handle API errors", async () => {
    const mockFetch = jest.fn().mockResolvedValue({
      ok: false,
      json: () => Promise.resolve({ message: "Not found" }),
    });
    global.fetch = mockFetch;

    await expect(api.get("/nonexistent")).rejects.toThrow("Not found");
  });
});
```

### Component Tests

```typescript
// __tests__/components/ItemCard.test.tsx
import React from "react";
import { render, fireEvent } from "@testing-library/react-native";
import { ItemCard } from "@/components/ItemCard";

describe("ItemCard", () => {
  const mockItem = {
    id: "1",
    title: "Test Item",
    description: "Test Description",
    price: 29.99,
  };

  it("renders correctly", () => {
    const { getByText } = render(
      <ItemCard item={mockItem} onPress={() => {}} />
    );

    expect(getByText("Test Item")).toBeTruthy();
    expect(getByText("$29.99")).toBeTruthy();
  });

  it("calls onPress when tapped", () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <ItemCard item={mockItem} onPress={onPress} />
    );

    fireEvent.press(getByText("Test Item"));
    expect(onPress).toHaveBeenCalledWith("1");
  });
});
```

## Versioning & Migration

### App Versioning

```json
// app.config.ts
export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  version: "1.2.3",
  ios: {
    buildNumber: "45",
  },
  android: {
    versionCode: 45,
  },
});
```

### EAS Build Versioning

```json
// eas.json
{
  "build": {
    "production": {
      "autoIncrement": true
    }
  }
}
```

### OTA Update Versioning

```bash
# Versioned OTA updates
eas update --branch production --message "v1.2.3 - Bug fixes"
```

## Glossary

### Expo React Native Terms

| Term | Definition |
|------|------------|
| **Expo** | Framework for React Native apps |
| **EAS Build** | Cloud build service for native builds |
| **EAS Submit** | App store submission service |
| **OTA Update** | Over-the-air JavaScript updates |
| **Expo Router** | File-based navigation system |
| **Dev Client** | Custom development build |
| **Managed Workflow** | Expo-managed native code |
| **Bare Workflow** | Manual native code management |
| **Expo Go** | Expo's development client |
| **App Config** | Expo configuration file |

## Changelog

### Version 2.0.0 (2024-01-15)
- Added Expo Router v3
- Implemented EAS Update channels
- Enhanced TypeScript support
- Added Dev Client

### Version 1.5.0 (2023-10-01)
- Added EAS Build
- Implemented OTA updates
- Enhanced notifications
- Added analytics

### Version 1.4.0 (2023-07-15)
- Added Expo Router
- Implemented tab navigation
- Enhanced deep linking
- Added testing

### Version 1.3.0 (2023-04-01)
- Added Expo SDK 49
- Implemented camera
- Added file system
- Enhanced API

### Version 1.2.0 (2023-01-15)
- Added basic Expo
- Implemented navigation
- Added storage
- Enhanced documentation

### Version 1.1.0 (2022-10-01)
- Added Expo setup
- Implemented basic UI
- Added networking
- Enhanced UI

### Version 1.0.0 (2022-07-15)
- Initial release
- Basic Expo React Native
- Cross-platform support
- Basic functionality

## Contributing Guidelines

### Development Setup

```bash
# Clone repository
git clone https://github.com/company/expo-app.git
cd expo-app

# Install dependencies
npm install

# Start development server
npx expo start

# Run on iOS simulator
npx expo run:ios

# Run on Android emulator
npx expo run:android
```

### Code Standards

- Follow TypeScript strict mode
- Use Expo Router for navigation
- Implement proper error handling
- Write unit and component tests
- Use Expo conventions
- Follow React Native best practices

## License

MIT License

Copyright (c) 2024 Expo React Native Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
