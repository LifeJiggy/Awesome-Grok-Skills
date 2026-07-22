---
name: react-native
category: mobile
version: 2.0.0
tags: [mobile, react-native, javascript, typescript, cross-platform]
---

# React Native

## Overview

Bare React Native development for building cross-platform mobile applications with JavaScript/TypeScript. This skill covers React Native core components, native module integration, navigation with React Navigation, state management, performance optimization, and platform-specific code patterns. Unlike Expo's managed workflow, bare React Native provides full access to native project files for maximum customization.

## Core Capabilities

- **Core Components**: View, Text, ScrollView, FlatList, TextInput, and platform-adapted UI elements
- **Native Modules**: Writing custom iOS (ObjC/Swift) and Android (Java/Kotlin) modules with Turbo Modules
- **New Architecture**: Fabric renderer, Turbo Modules, and Codegen for type-safe native bridging
- **React Navigation**: Stack, Tab, Drawer navigators with deep linking and native stack drivers
- **State Management**: Zustand, Jotai, or Redux Toolkit for scalable state with persistence
- **Performance**: Hermes engine, lazy loading, memoization, and interaction manager patterns
- **Debugging**: Flipper integration, React DevTools, and native debugging workflows
- **CI/CD**: Fastlane, Bitrise, or GitHub Actions for automated native builds and deployment

## Usage Examples

```typescript
// React Navigation with typed params
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { NavigationContainer } from "@react-navigation/native";

type RootStackParamList = {
  Home: undefined;
  Detail: { itemId: string; title: string };
  Settings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen
          name="Detail"
          component={DetailScreen}
          options={{ headerShown: true, headerBackTitle: "Back" }}
        />
        <Stack.Screen name="Settings" component={SettingsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Zustand Store with persistence
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import AsyncStorage from "@react-native-async-storage/async-storage";

interface AppState {
  items: Item[];
  favorites: string[];
  addItem: (item: Item) => void;
  removeItem: (id: string) => void;
  toggleFavorite: (id: string) => void;
}

const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      items: [],
      favorites: [],
      addItem: (item) => set((s) => ({ items: [...s.items, item] })),
      removeItem: (id) => set((s) => ({ items: s.items.filter((i) => i.id !== id) })),
      toggleFavorite: (id) =>
        set((s) => ({
          favorites: s.favorites.includes(id)
            ? s.favorites.filter((f) => f !== id)
            : [...s.favorites, id],
        })),
    }),
    { name: "app-storage", storage: createJSONStorage(() => AsyncStorage) }
  )
);

// Performance-Optimized FlatList
const ItemList: React.FC = () => {
  const items = useAppStore((s) => s.items);

  const renderItem = useCallback(({ item }: { item: Item }) => (
    <ItemCard item={item} />
  ), []);

  const keyExtractor = useCallback((item: Item) => item.id, []);

  return (
    <FlatList
      data={items}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      removeClippedSubviews
      maxToRenderPerBatch={10}
      windowSize={5}
      getItemLayout={(_, index) => ({
        length: ITEM_HEIGHT,
        offset: ITEM_HEIGHT * index,
        index,
      })}
    />
  );
};

// Custom Native Module Bridge
import { NativeModules, Platform } from "react-native";

const { DeviceInfoModule } = NativeModules;

interface DeviceInfoInterface {
  getModel: () => Promise<string>;
  getBatteryLevel: () => Promise<number>;
  isJailbroken: () => Promise<boolean>;
}

const DeviceInfo: DeviceInfoInterface = {
  getModel: () => DeviceInfoModule.getModel(),
  getBatteryLevel: () => DeviceInfoModule.getBatteryLevel(),
  isJailbroken: () => Platform.OS === "android"
    ? DeviceInfoModule.isRooted()
    : DeviceInfoModule.isJailbroken(),
};

// TypeScript Component with Props and Memoization
interface ItemCardProps {
  item: Item;
  onPress?: (id: string) => void;
}

const ItemCard: React.FC<ItemCardProps> = React.memo(({ item, onPress }) => (
  <Pressable
    onPress={() => onPress?.(item.id)}
    style={({ pressed }) => [styles.card, pressed && styles.cardPressed]}
  >
    <Text style={styles.title}>{item.name}</Text>
    <Text style={styles.subtitle}>{item.description}</Text>
  </Pressable>
));
```

## Best Practices

- Use Hermes engine for faster startup and reduced memory consumption
- Leverage FlatList virtualization for long lists with proper getItemLayout
- Use `React.memo`, `useCallback`, and `useMemo` to prevent unnecessary re-renders
- Prefer Zustand over Redux for simpler state management with less boilerplate
- Use `react-native-reanimated` for 60fps animations on the UI thread
- Implement `removeClippedSubviews` and `windowSize` for FlatList optimization
- Use Codegen and Turbo Modules for the New Architecture when possible
- Keep the bridge calls minimal; batch native module calls when needed
- Use Flipper for debugging network requests, state, and layout issues
- Run `react-native-profile` and Hermes performance monitor in development

## Related Modules

- `expo-react-native` - Expo-managed React Native for faster prototyping
- `android-development` - Native Android development patterns
- `ios-development` - Native iOS development patterns
- `flutter-naija` - Flutter alternative for cross-platform development

## Advanced Configuration

### Metro Bundler Configuration

```javascript
// metro.config.js
const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

const defaultConfig = getDefaultConfig(__dirname);

const config = {
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: true,
      },
    }),
  },
  resolver: {
    sourceExts: ['js', 'jsx', 'json', 'ts', 'tsx', 'cjs', 'mjs'],
    assetExts: [
      'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg',
      'ttf', 'otf', 'woff', 'woff2',
    ],
  },
  cacheStores: [
    {
      name: 'metro-cache',
      get: (key) => /* implement */,
      set: (key, value) => /* implement */,
    },
  ],
};

module.exports = mergeConfig(defaultConfig, config);
```

### Babel Configuration

```javascript
// babel.config.js
module.exports = {
  presets: ['module:@react-native/babel-preset'],
  plugins: [
    ['@babel/plugin-proposal-decorators', { legacy: true }],
    'react-native-reanimated/plugin',
    [
      'module-resolver',
      {
        root: ['./src'],
        extensions: ['.ios.js', '.android.js', '.js', '.ts', '.tsx', '.json'],
        alias: {
          '@components': './src/components',
          '@screens': './src/screens',
          '@services': './src/services',
          '@hooks': './src/hooks',
          '@utils': './src/utils',
          '@navigation': './src/navigation',
        },
      },
    ],
  ],
  env: {
    production: {
      plugins: ['transform-remove-console'],
    },
  },
};
```

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "esnext",
    "module": "commonjs",
    "lib": ["es2019"],
    "allowJs": true,
    "jsx": "react-native",
    "noEmit": true,
    "isolatedModules": true,
    "strict": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "baseUrl": "./src",
    "paths": {
      "@components/*": ["components/*"],
      "@screens/*": ["screens/*"],
      "@services/*": ["services/*"],
      "@hooks/*": ["hooks/*"],
      "@utils/*": ["utils/*"],
      "@navigation/*": ["navigation/*"]
    }
  },
  "exclude": [
    "node_modules",
    "babel.config.js",
    "metro.config.js",
    "jest.config.js"
  ]
}
```

## Architecture Patterns

### React Native Project Structure

```
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── common/         # Common components
│   │   └── features/       # Feature-specific components
│   ├── screens/            # Screen components
│   ├── navigation/         # Navigation configuration
│   ├── services/           # API and business logic
│   ├── hooks/              # Custom hooks
│   ├── store/              # State management
│   ├── utils/              # Utility functions
│   ├── types/              # TypeScript types
│   └── assets/             # Static assets
├── android/                # Android native code
├── ios/                    # iOS native code
├── __tests__/             # Test files
├── app.json               # App configuration
├── babel.config.js        # Babel configuration
├── metro.config.js        # Metro bundler configuration
├── tsconfig.json          # TypeScript configuration
└── package.json           # Dependencies
```

### State Management with Zustand

```typescript
// store/useItemStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface Item {
  id: string;
  name: string;
  description: string;
  price: number;
}

interface ItemState {
  items: Item[];
  isLoading: boolean;
  error: string | null;
  addItem: (item: Item) => void;
  removeItem: (id: string) => void;
  updateItem: (id: string, updates: Partial<Item>) => void;
  fetchItems: () => Promise<void>;
  clearError: () => void;
}

export const useItemStore = create<ItemState>()(
  devtools(
    persist(
      (set, get) => ({
        items: [],
        isLoading: false,
        error: null,

        addItem: (item) => {
          set((state) => ({ items: [...state.items, item] }));
        },

        removeItem: (id) => {
          set((state) => ({
            items: state.items.filter((item) => item.id !== id),
          }));
        },

        updateItem: (id, updates) => {
          set((state) => ({
            items: state.items.map((item) =>
              item.id === id ? { ...item, ...updates } : item
            ),
          }));
        },

        fetchItems: async () => {
          set({ isLoading: true, error: null });
          try {
            const response = await fetch('https://api.example.com/items');
            const items = await response.json();
            set({ items, isLoading: false });
          } catch (error) {
            set({ error: error.message, isLoading: false });
          }
        },

        clearError: () => set({ error: null }),
      }),
      {
        name: 'item-storage',
        partialize: (state) => ({ items: state.items }),
      }
    )
  )
);
```

### Navigation with React Navigation

```typescript
// navigation/AppNavigator.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/Ionicons';

import HomeScreen from '../screens/HomeScreen';
import DetailScreen from '../screens/DetailScreen';
import SettingsScreen from '../screens/SettingsScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function HomeTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;
          if (route.name === 'Home') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Profile') {
            iconName = focused ? 'person' : 'person-outline';
          } else if (route.name === 'Settings') {
            iconName = focused ? 'settings' : 'settings-outline';
          }
          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: 'gray',
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Main"
          component={HomeTabs}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Detail"
          component={DetailScreen}
          options={{ title: 'Details' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

## Integration Guide

### Redux Toolkit Integration

```typescript
// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import itemReducer from './itemSlice';

export const store = configureStore({
  reducer: {
    items: itemReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// store/itemSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

interface Item {
  id: string;
  name: string;
  description: string;
  price: number;
}

interface ItemState {
  items: Item[];
  isLoading: boolean;
  error: string | null;
}

const initialState: ItemState = {
  items: [],
  isLoading: false,
  error: null,
};

export const fetchItems = createAsyncThunk(
  'items/fetchItems',
  async () => {
    const response = await fetch('https://api.example.com/items');
    return response.json();
  }
);

const itemSlice = createSlice({
  name: 'items',
  initialState,
  reducers: {
    addItem: (state, action) => {
      state.items.push(action.payload);
    },
    removeItem: (state, action) => {
      state.items = state.items.filter((item) => item.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchItems.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchItems.fulfilled, (state, action) => {
        state.isLoading = false;
        state.items = action.payload;
      })
      .addCase(fetchItems.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch items';
      });
  },
});

export const { addItem, removeItem } = itemSlice.actions;
export default itemSlice.reducer;
```

### React Query Integration

```typescript
// hooks/useItems.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';

export function useItems() {
  return useQuery({
    queryKey: ['items'],
    queryFn: api.getItems,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

export function useCreateItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.createItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}

export function useUpdateItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }) => api.updateItem(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}

export function useDeleteItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.deleteItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}
```

### Push Notifications

```typescript
// services/notifications.ts
import messaging from '@react-native-firebase/messaging';
import notifee, { AndroidImportance } from '@notifee/react-native';

class NotificationService {
  static async requestPermission() {
    const authStatus = await messaging().requestPermission();
    const enabled =
      authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
      authStatus === messaging.AuthorizationStatus.PROVISIONAL;

    return enabled;
  }

  static async getToken() {
    const token = await messaging().getToken();
    return token;
  }

  static async setupListeners() {
    // Foreground messages
    messaging().onMessage(async (remoteMessage) => {
      await this.displayNotification(remoteMessage);
    });

    // Background messages
    messaging().setBackgroundMessageHandler(async (remoteMessage) => {
      console.log('Background message:', remoteMessage);
    });

    // Notification opened
    messaging().onNotificationOpenedApp((remoteMessage) => {
      console.log('Notification opened:', remoteMessage);
    });

    // Quit state
    const remoteMessage = await messaging().getInitialNotification();
    if (remoteMessage) {
      console.log('Quit state notification:', remoteMessage);
    }
  }

  static async displayNotification(remoteMessage: any) {
    await notifee.requestPermission();

    await notifee.displayNotification({
      title: remoteMessage.notification?.title || 'New Notification',
      body: remoteMessage.notification?.body || '',
      android: {
        channelId: 'default',
        importance: AndroidImportance.HIGH,
        smallIcon: 'ic_notification',
      },
    });
  }

  static async createChannels() {
    await notifee.createChannel({
      id: 'default',
      name: 'Default Channel',
      importance: AndroidImportance.HIGH,
    });
  }
}

export default NotificationService;
```

## Performance Optimization

### Image Optimization

```typescript
// components/OptimizedImage.tsx
import React from 'react';
import { Image, ImageStyle, StyleProp } from 'react-native';
import FastImage from 'react-native-fast-image';

interface OptimizedImageProps {
  uri: string;
  style?: StyleProp<ImageStyle>;
  resizeMode?: 'cover' | 'contain' | 'stretch' | 'center';
}

export function OptimizedImage({
  uri,
  style,
  resizeMode = 'cover',
}: OptimizedImageProps) {
  return (
    <FastImage
      style={style}
      source={{ uri, priority: FastImage.priority.normal }}
      resizeMode={resizeMode}
    />
  );
}

// Preload images
export function preloadImages(uris: string[]) {
  FastImage.preload(
    uris.map((uri) => ({ uri, priority: FastImage.priority.normal }))
  );
}
```

### List Optimization

```typescript
// components/OptimizedFlatList.tsx
import React, { useCallback, useMemo } from 'react';
import { FlatList, FlatListProps, ViewToken } from 'react-native';

interface OptimizedFlatListProps<T> extends FlatListProps<T> {
  keyExtractor?: (item: T, index: number) => string;
}

export function OptimizedFlatList<T>({
  data,
  renderItem,
  keyExtractor,
  ...props
}: OptimizedFlatListProps<T>) {
  const getItemLayout = useCallback(
    (data: any, index: number) => ({
      length: 80,
      offset: 80 * index,
      index,
    }),
    []
  );

  const renderItemMemoized = useCallback(
    ({ item, index }: { item: T; index: number }) =>
      renderItem({ item, index, separators: { highlight: () => {}, unhighlight: () => {}, updateProps: () => {} } }),
    [renderItem]
  );

  return (
    <FlatList
      data={data}
      renderItem={renderItemMemoized}
      keyExtractor={keyExtractor || ((item: any) => item.id)}
      getItemLayout={getItemLayout}
      removeClippedSubviews
      maxToRenderPerBatch={10}
      windowSize={5}
      initialNumToRender={10}
      {...props}
    />
  );
}
```

### Animation Optimization

```typescript
// components/AnimatedCard.tsx
import React from 'react';
import { StyleSheet, View } from 'react-native';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  withTiming,
} from 'react-native-reanimated';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';

interface AnimatedCardProps {
  children: React.ReactNode;
  onPress?: () => void;
}

export function AnimatedCard({ children, onPress }: AnimatedCardProps) {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  const tap = Gesture.Tap()
    .onBegin(() => {
      scale.value = withSpring(0.95);
      opacity.value = withTiming(0.8, { duration: 100 });
    })
    .onFinalize(() => {
      scale.value = withSpring(1);
      opacity.value = withTiming(1, { duration: 100 });
    })
    .onEnd(() => {
      onPress?.();
    });

  return (
    <GestureDetector gesture={tap}>
      <Animated.View style={[styles.card, animatedStyle]}>
        {children}
      </Animated.View>
    </GestureDetector>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
});
```

## Security Considerations

### Secure Storage

```typescript
// services/secureStorage.ts
import * as Keychain from 'react-native-keychain';

class SecureStorage {
  static async set(key: string, value: string): Promise<boolean> {
    try {
      return await Keychain.setGenericPassword(key, value, {
        accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
        service: 'com.myapp.securestorage',
      });
    } catch (error) {
      console.error('Failed to save to secure storage:', error);
      return false;
    }
  }

  static async get(key: string): Promise<string | null> {
    try {
      const credentials = await Keychain.getGenericPassword({
        service: 'com.myapp.securestorage',
      });
      if (credentials) {
        return credentials.password;
      }
      return null;
    } catch (error) {
      console.error('Failed to read from secure storage:', error);
      return null;
    }
  }

  static async remove(key: string): Promise<boolean> {
    try {
      return await Keychain.resetGenericPassword({
        service: 'com.myapp.securestorage',
      });
    } catch (error) {
      console.error('Failed to delete from secure storage:', error);
      return false;
    }
  }

  static async clear(): Promise<boolean> {
    try {
      return await Keychain.resetGenericPassword();
    } catch (error) {
      console.error('Failed to clear secure storage:', error);
      return false;
    }
  }
}

export default SecureStorage;
```

### Certificate Pinning

```typescript
// services/networkSecurity.ts
import { Platform } from 'react-native';
import RNSSSLessionManager from 'react-native-ssl-session-manager';

class NetworkSecurity {
  static async setupCertificatePinning() {
    if (Platform.OS === 'ios') {
      await RNSSSLessionManager.pinCertificates(['api.example.com']);
    }
  }

  static async validateCertificate(url: string): Promise<boolean> {
    try {
      const isValid = await RNSSSLessionManager.validateCertificate(url);
      return isValid;
    } catch (error) {
      console.error('Certificate validation failed:', error);
      return false;
    }
  }
}

export default NetworkSecurity;
```

## Troubleshooting Guide

### Common Issues

#### Issue: Metro Bundler Issues

```bash
# Clear Metro cache
npx react-native start --reset-cache

# Or manually
rm -rf node_modules/.cache
rm -rf /tmp/metro-*
rm -rf /tmp/react-*

# Watchman issues
watchman watch-del-all
watchman shutdown-server
```

#### Issue: iOS Build Failures

```bash
# Clean iOS build
cd ios
rm -rf Pods
rm -rf build
pod install
cd ..

# Reset cache
npx react-native start --reset-cache
```

#### Issue: Android Build Failures

```bash
# Clean Android build
cd android
./gradlew clean
cd ..

# Clear Gradle cache
rm -rf ~/.gradle/caches
```

#### Issue: Performance Issues

```typescript
// utils/performanceMonitor.ts
import { PerformanceObserver, performance } from 'perf_hooks';

class PerformanceMonitor {
  static startMeasure(name: string) {
    performance.mark(`${name}-start`);
  }

  static endMeasure(name: string) {
    performance.mark(`${name}-end`);
    performance.measure(name, `${name}-start`, `${name}-end`);

    const measure = performance.getEntriesByName(name)[0];
    console.log(`${name}: ${measure.duration.toFixed(2)}ms`);

    performance.clearMarks(`${name}-start`);
    performance.clearMarks(`${name}-end`);
    performance.clearMeasures(name);
  }

  static logMemoryUsage() {
    const used = process.memoryUsage();
    console.log(`Memory: ${(used.heapUsed / 1024 / 1024).toFixed(2)} MB`);
  }
}

export default PerformanceMonitor;
```

## API Reference

### React Navigation API

```typescript
// Navigation methods
import { useNavigation, useRoute, useFocusEffect } from '@react-navigation/native';

// Navigate to route
const navigation = useNavigation();
navigation.navigate('Detail', { id: '123' });
navigation.goBack();
navigation.popToTop();

// Get route params
const route = useRoute();
const { id } = route.params;

// Focus effect
useFocusEffect(
  React.useCallback(() => {
    // Screen is focused
    return () => {
      // Screen is unfocused
    };
  }, [])
);
```

### React Query API

```typescript
// Query methods
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Fetch data
const { data, isLoading, error, refetch } = useQuery({
  queryKey: ['items'],
  queryFn: fetchItems,
});

// Mutate data
const mutation = useMutation({
  mutationFn: createItem,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['items'] });
  },
});

mutation.mutate(newItem);
```

## Data Models

### TypeScript Types

```typescript
// types/models.ts
export interface Item {
  id: string;
  name: string;
  description: string;
  price: number;
  imageUrl: string;
  category: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
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
  Main: undefined;
  Detail: { id: string };
  Settings: undefined;
  Profile: undefined;
};

export type TabParamList = {
  Home: undefined;
  Profile: undefined;
  Settings: undefined;
};
```

## Deployment Guide

### Build Configuration

```json
// app.json
{
  "name": "MyApp",
  "displayName": "My App",
  "expo": {
    "name": "MyApp",
    "slug": "myapp",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.myapp.ios"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.myapp.android"
    }
  }
}
```

### CI/CD Configuration

```yaml
# .github/workflows/react-native.yml
name: React Native CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm install
    
    - name: Run tests
      run: npm test
    
    - name: Build Android
      run: cd android && ./gradlew assembleRelease
    
    - name: Build iOS
      run: |
        cd ios
        pod install
        xcodebuild -workspace MyApp.xcworkspace -scheme MyApp -configuration Release
```

## Monitoring & Observability

### Crash Reporting

```typescript
// services/crashReporting.ts
import crashlytics from '@react-native-firebase/crashlytics';

class CrashReporting {
  static logError(error: Error, context?: Record<string, any>) {
    crashlytics().recordError(error);

    if (context) {
      Object.entries(context).forEach(([key, value]) => {
        crashlytics().setAttribute(key, String(value));
      });
    }
  }

  static logMessage(message: string) {
    crashlytics().log(message);
  }

  static setUserID(userID: string) {
    crashlytics().setUserId(userID);
  }

  static setAttribute(key: string, value: string) {
    crashlytics().setAttribute(key, value);
  }
}

export default CrashReporting;
```

### Analytics

```typescript
// services/analytics.ts
import analytics from '@react-native-firebase/analytics';

class Analytics {
  static logEvent(name: string, params?: Record<string, any>) {
    analytics().logEvent(name, params);
  }

  static setCurrentScreen(screenName: string) {
    analytics().logScreenView({ screen_name: screenName });
  }

  static setUserProperty(name: string, value: string) {
    analytics().setUserProperty(name, value);
  }

  static logPurchase(itemId: string, price: number, currency: string) {
    analytics().logPurchase({
      value: price,
      currency: currency,
      items: [{ item_id: itemId }],
    });
  }
}

export default Analytics;
```

## Testing Strategy

### Unit Tests

```typescript
// __tests__/store/useItemStore.test.ts
import { renderHook, act } from '@testing-library/react-hooks';
import { useItemStore } from '../../store/useItemStore';

describe('useItemStore', () => {
  beforeEach(() => {
    useItemStore.setState({ items: [], isLoading: false, error: null });
  });

  it('should add an item', () => {
    const { result } = renderHook(() => useItemStore());

    const newItem = {
      id: '1',
      name: 'Test Item',
      description: 'Test Description',
      price: 9.99,
    };

    act(() => {
      result.current.addItem(newItem);
    });

    expect(result.current.items).toHaveLength(1);
    expect(result.current.items[0]).toEqual(newItem);
  });

  it('should remove an item', () => {
    const { result } = renderHook(() => useItemStore());

    act(() => {
      result.current.addItem({ id: '1', name: 'Test', description: '', price: 0 });
      result.current.removeItem('1');
    });

    expect(result.current.items).toHaveLength(0);
  });
});
```

### Component Tests

```typescript
// __tests__/components/ItemCard.test.tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { ItemCard } from '../../components/ItemCard';

describe('ItemCard', () => {
  const mockItem = {
    id: '1',
    name: 'Test Item',
    description: 'Test Description',
    price: 29.99,
  };

  it('renders correctly', () => {
    const { getByText } = render(
      <ItemCard item={mockItem} onPress={() => {}} />
    );

    expect(getByText('Test Item')).toBeTruthy();
    expect(getByText('$29.99')).toBeTruthy();
  });

  it('calls onPress when tapped', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <ItemCard item={mockItem} onPress={onPress} />
    );

    fireEvent.press(getByText('Test Item'));
    expect(onPress).toHaveBeenCalledWith('1');
  });
});
```

## Versioning & Migration

### React Native Upgrade

```bash
# Check current version
npx react-native --version

# Upgrade React Native
npx react-native upgrade

# Manual upgrade steps
# 1. Update package.json dependencies
# 2. Update iOS Podfile
# 3. Update Android build.gradle
# 4. Run pod install
# 5. Clean and rebuild
```

### API Versioning

```typescript
// services/apiClient.ts
const API_VERSIONS = {
  v1: 'https://api.example.com/v1',
  v2: 'https://api.example.com/v2',
};

class APIClient {
  private baseURL: string;

  constructor(version: keyof typeof API_VERSIONS = 'v2') {
    this.baseURL = API_VERSIONS[version];
  }

  async request<T>(
    method: string,
    path: string,
    body?: unknown
  ): Promise<T> {
    const response = await fetch(`${this.baseURL}${path}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

export const apiClient = new APIClient('v2');
```

## Glossary

### React Native Terms

| Term | Definition |
|------|------------|
| **React Native** | Cross-platform mobile framework |
| **Metro** | JavaScript bundler for React Native |
| **Hermes** | JavaScript engine optimized for React Native |
| **Bridge** | Communication between JS and native code |
| **Turbo Modules** | New architecture for native modules |
| **Codegen** | TypeScript to native code generation |
| **New Architecture** | React Native's new architecture |
| **Reanimated** | Animation library for React Native |
| **Gesture Handler** | Gesture handling library |
| **Navigation** | Routing and navigation library |

## Changelog

### Version 2.0.0 (2024-01-15)
- Added New Architecture support
- Implemented Turbo Modules
- Enhanced Hermes engine
- Added Codegen

### Version 1.5.0 (2023-10-01)
- Added Reanimated v3
- Implemented Gesture Handler
- Enhanced navigation
- Added testing utilities

### Version 1.4.0 (2023-07-15)
- Added React Query
- Implemented Zustand
- Enhanced TypeScript
- Added performance monitoring

### Version 1.3.0 (2023-04-01)
- Added React Navigation v6
- Implemented Redux Toolkit
- Enhanced state management
- Added API

### Version 1.2.0 (2023-01-15)
- Added basic React Native
- Implemented basic UI
- Added networking
- Enhanced documentation

### Version 1.1.0 (2022-10-01)
- Added React Native setup
- Implemented basic navigation
- Added state management
- Enhanced UI

### Version 1.0.0 (2022-07-15)
- Initial release
- Basic React Native
- Cross-platform support
- Basic functionality

## Contributing Guidelines

### Development Setup

```bash
# Clone repository
git clone https://github.com/company/react-native-app.git
cd react-native-app

# Install dependencies
npm install

# iOS setup
cd ios && pod install && cd ..

# Start Metro
npx react-native start

# Run on iOS
npx react-native run-ios

# Run on Android
npx react-native run-android
```

### Code Standards

- Follow TypeScript strict mode
- Use functional components with hooks
- Implement proper error handling
- Write unit and component tests
- Use React Navigation for routing
- Follow React Native best practices

## License

MIT License

Copyright (c) 2024 React Native Contributors

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
