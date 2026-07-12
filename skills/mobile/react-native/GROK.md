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
