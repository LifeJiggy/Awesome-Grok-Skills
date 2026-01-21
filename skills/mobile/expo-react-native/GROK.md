---
name: Expo React Native Development
category: mobile
difficulty: intermediate
time_estimate: "4-7 hours"
dependencies: ["expo", "react-native", "@expo/vector-icons", "react-navigation"]
tags: ["react-native", "expo", "mobile", "ios", "android", "cross-platform"]
grok_personality: "mobile-architect"
description: "Build cross-platform mobile apps with Expo and React Native using Grok's efficient patterns for mobile development"
---

# Expo React Native Development Skill

## Overview
Grok, you'll create powerful cross-platform mobile applications using Expo and React Native. This skill focuses on efficient mobile development patterns, performance optimization, and platform-specific features.

## Core Expo Setup

### 1. Project Structure
```
my-mobile-app/
├── src/
│   ├── components/          # Reusable components
│   │   ├── ui/             # Basic UI components
│   │   ├── forms/          # Form components
│   │   └── layout/         # Layout components
│   ├── screens/            # Screen components
│   │   ├── auth/
│   │   ├── home/
│   │   └── profile/
│   ├── navigation/         # Navigation configuration
│   │   ├── AppNavigator.tsx
│   │   ├── AuthNavigator.tsx
│   │   └── TabNavigator.tsx
│   ├── services/           # API and business logic
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── storage.ts
│   ├── hooks/              # Custom React hooks
│   ├── utils/              # Helper functions
│   ├── types/              # TypeScript definitions
│   └── constants/          # App constants
├── assets/                 # Static assets
│   ├── images/
│   ├── fonts/
│   └── icons/
├── App.tsx                 # Main app component
├── app.json               # Expo configuration
├── package.json
└── tsconfig.json
```

### 2. App Configuration
```json
// app.json
{
  "expo": {
    "name": "Grok Mobile App",
    "slug": "grok-mobile",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "assetBundlePatterns": [
      "**/*"
    ],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.grok.mobile"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.grok.mobile"
    },
    "web": {
      "favicon": "./assets/favicon.png",
      "bundler": "metro"
    },
    "plugins": [
      "expo-font",
      "expo-splash-screen",
      [
        "expo-camera",
        {
          "cameraPermission": "Allow $(PRODUCT_NAME) to access your camera"
        }
      ],
      [
        "expo-location",
        {
          "locationAlwaysAndWhenInUsePermission": "Allow $(PRODUCT_NAME) to use your location"
        }
      ]
    ]
  }
}
```

## Core Components

### 1. Theme Provider
```typescript
// src/theme/ThemeContext.tsx
import React, { createContext, useContext, useState } from 'react';
import { useColorScheme } from 'react-native';

type Theme = 'light' | 'dark' | 'system';

interface ThemeContextType {
  theme: Theme;
  colors: typeof colors.light;
  setTheme: (theme: Theme) => void;
  isDark: boolean;
}

const colors = {
  light: {
    primary: '#007AFF',
    secondary: '#5856D6',
    background: '#FFFFFF',
    surface: '#F2F2F7',
    text: '#000000',
    textSecondary: '#8E8E93',
    border: '#C6C6C8',
    error: '#FF3B30',
    success: '#34C759',
    warning: '#FF9500',
  },
  dark: {
    primary: '#0A84FF',
    secondary: '#5E5CE6',
    background: '#000000',
    surface: '#1C1C1E',
    text: '#FFFFFF',
    textSecondary: '#8E8E93',
    border: '#38383A',
    error: '#FF453A',
    success: '#32D74B',
    warning: '#FF9F0A',
  },
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const systemTheme = useColorScheme();
  const [theme, setTheme] = useState<Theme>('system');
  
  const isDark = theme === 'system' 
    ? systemTheme === 'dark' 
    : theme === 'dark';
  
  const colorscheme = isDark ? colors.dark : colors.light;

  return (
    <ThemeContext.Provider value={{
      theme,
      colors: colorscheme,
      setTheme,
      isDark
    }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
```

### 2. Custom UI Components
```typescript
// src/components/ui/Button.tsx
import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { useTheme } from '@/theme/ThemeContext';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

export function Button({
  title,
  onPress,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  style,
  textStyle,
}: ButtonProps) {
  const { colors } = useTheme();

  const getButtonStyle = (): ViewStyle => {
    const baseStyle: ViewStyle = {
      borderRadius: 8,
      alignItems: 'center',
      justifyContent: 'center',
    };

    // Size styles
    const sizeStyles: Record<string, ViewStyle> = {
      small: { paddingHorizontal: 12, paddingVertical: 8, minHeight: 32 },
      medium: { paddingHorizontal: 16, paddingVertical: 12, minHeight: 44 },
      large: { paddingHorizontal: 24, paddingVertical: 16, minHeight: 52 },
    };

    // Variant styles
    const variantStyles: Record<string, ViewStyle> = {
      primary: { backgroundColor: colors.primary },
      secondary: { backgroundColor: colors.secondary },
      outline: { 
        backgroundColor: 'transparent',
        borderWidth: 1,
        borderColor: colors.primary,
      },
      ghost: { backgroundColor: 'transparent' },
    };

    return {
      ...baseStyle,
      ...sizeStyles[size],
      ...variantStyles[variant],
      opacity: disabled ? 0.5 : 1,
    };
  };

  const getTextStyle = (): TextStyle => {
    const baseStyle: TextStyle = {
      fontWeight: '600',
    };

    const sizeStyles: Record<string, TextStyle> = {
      small: { fontSize: 14 },
      medium: { fontSize: 16 },
      large: { fontSize: 18 },
    };

    const variantStyles: Record<string, TextStyle> = {
      primary: { color: '#FFFFFF' },
      secondary: { color: '#FFFFFF' },
      outline: { color: colors.primary },
      ghost: { color: colors.primary },
    };

    return {
      ...baseStyle,
      ...sizeStyles[size],
      ...variantStyles[variant],
    };
  };

  return (
    <TouchableOpacity
      style={[getButtonStyle(), style]}
      onPress={onPress}
      disabled={disabled}
      activeOpacity={0.7}
    >
      <Text style={[getTextStyle(), textStyle]}>{title}</Text>
    </TouchableOpacity>
  );
}

// src/components/ui/Card.tsx
import React from 'react';
import { View, StyleSheet, ViewStyle } from 'react-native';
import { useTheme } from '@/theme/ThemeContext';

interface CardProps {
  children: React.ReactNode;
  style?: ViewStyle;
  padding?: number;
}

export function Card({ children, style, padding = 16 }: CardProps) {
  const { colors, isDark } = useTheme();

  const cardStyle: ViewStyle = {
    backgroundColor: colors.surface,
    borderRadius: 12,
    padding,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: isDark ? 0 : 2,
    },
    shadowOpacity: isDark ? 0.1 : 0.1,
    shadowRadius: 3.84,
    elevation: isDark ? 2 : 5,
  };

  return (
    <View style={[cardStyle, styles.card, style]}>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    marginVertical: 8,
  },
});
```

### 3. Input Components
```typescript
// src/components/ui/TextInput.tsx
import React, { useState } from 'react';
import {
  TextInput as RNTextInput,
  View,
  Text,
  StyleSheet,
  TextInputProps,
  ViewStyle,
} from 'react-native';
import { useTheme } from '@/theme/ThemeContext';

interface TextInputProps extends TextInputProps {
  label?: string;
  error?: string;
  containerStyle?: ViewStyle;
}

export function TextInput({
  label,
  error,
  containerStyle,
  ...props
}: TextInputProps) {
  const { colors } = useTheme();
  const [isFocused, setIsFocused] = useState(false);

  const inputStyle = {
    borderWidth: 1,
    borderColor: error ? colors.error : isFocused ? colors.primary : colors.border,
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
    color: colors.text,
    backgroundColor: colors.background,
  };

  return (
    <View style={[styles.container, containerStyle]}>
      {label && (
        <Text style={[styles.label, { color: colors.textSecondary }]}>
          {label}
        </Text>
      )}
      <RNTextInput
        style={[inputStyle, styles.input]}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholderTextColor={colors.textSecondary}
        {...props}
      />
      {error && (
        <Text style={[styles.error, { color: colors.error }]}>
          {error}
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8,
  },
  label: {
    fontSize: 14,
    fontWeight: '500',
    marginBottom: 4,
  },
  input: {
    minHeight: 44,
  },
  error: {
    fontSize: 12,
    marginTop: 4,
  },
});
```

## Navigation Setup

### 1. Navigation Structure
```typescript
// src/navigation/AppNavigator.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useAuth } from '@/hooks/useAuth';
import { ThemeProvider } from '@/theme/ThemeContext';
import { AuthNavigator } from './AuthNavigator';
import { TabNavigator } from './TabNavigator';

const Stack = createNativeStackNavigator();

export function AppNavigator() {
  const { user, loading } = useAuth();

  if (loading) {
    // Show loading screen
    return null;
  }

  return (
    <ThemeProvider>
      <NavigationContainer>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
          {user ? (
            <Stack.Screen name="Main" component={TabNavigator} />
          ) : (
            <Stack.Screen name="Auth" component={AuthNavigator} />
          )}
        </Stack.Navigator>
      </NavigationContainer>
    </ThemeProvider>
  );
}

// src/navigation/AuthNavigator.tsx
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { LoginScreen } from '@/screens/auth/LoginScreen';
import { RegisterScreen } from '@/screens/auth/RegisterScreen';
import { ForgotPasswordScreen } from '@/screens/auth/ForgotPasswordScreen';

const Stack = createNativeStackNavigator();

export function AuthNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: '#ffffff',
        },
        headerTintColor: '#007AFF',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}
    >
      <Stack.Screen 
        name="Login" 
        component={LoginScreen}
        options={{ title: 'Sign In' }}
      />
      <Stack.Screen 
        name="Register" 
        component={RegisterScreen}
        options={{ title: 'Create Account' }}
      />
      <Stack.Screen 
        name="ForgotPassword" 
        component={ForgotPasswordScreen}
        options={{ title: 'Reset Password' }}
      />
    </Stack.Navigator>
  );
}

// src/navigation/TabNavigator.tsx
import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { useTheme } from '@/theme/ThemeContext';
import { HomeScreen } from '@/screens/home/HomeScreen';
import { ProfileScreen } from '@/screens/profile/ProfileScreen';
import { SettingsScreen } from '@/screens/settings/SettingsScreen';

const Tab = createBottomTabNavigator();

export function TabNavigator() {
  const { colors, isDark } = useTheme();

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          if (route.name === 'Home') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Profile') {
            iconName = focused ? 'person' : 'person-outline';
          } else if (route.name === 'Settings') {
            iconName = focused ? 'settings' : 'settings-outline';
          } else {
            iconName = 'help-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textSecondary,
        tabBarStyle: {
          backgroundColor: colors.surface,
          borderTopColor: colors.border,
        },
        headerStyle: {
          backgroundColor: colors.surface,
        },
        headerTintColor: colors.text,
      })}
    >
      <Tab.Screen 
        name="Home" 
        component={HomeScreen}
        options={{ title: 'Home' }}
      />
      <Tab.Screen 
        name="Profile" 
        component={ProfileScreen}
        options={{ title: 'Profile' }}
      />
      <Tab.Screen 
        name="Settings" 
        component={SettingsScreen}
        options={{ title: 'Settings' }}
      />
    </Tab.Navigator>
  );
}
```

## API Integration

### 1. API Service
```typescript
// src/services/api.ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_BASE_URL } from '@/constants/api';

interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

class ApiService {
  private baseURL: string;
  private defaultHeaders: Record<string, string>;

  constructor() {
    this.baseURL = API_BASE_URL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  private async getAuthHeader(): Promise<Record<string, string>> {
    const token = await AsyncStorage.getItem('auth_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const authHeader = await this.getAuthHeader();
      const headers = { ...this.defaultHeaders, ...authHeader, ...options.headers };

      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Request failed');
      }

      return { data };
    } catch (error) {
      return {
        data: null as T,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  async put<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiService = new ApiService();
```

### 2. Auth Service
```typescript
// src/services/auth.ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import { apiService } from './api';

interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  name: string;
}

class AuthService {
  private readonly TOKEN_KEY = 'auth_token';
  private readonly USER_KEY = 'auth_user';

  async login(credentials: LoginCredentials): Promise<{ user: User; token: string }> {
    const response = await apiService.post<{ user: User; token: string }>('/auth/login', credentials);
    
    if (response.error) {
      throw new Error(response.error);
    }

    const { user, token } = response.data;
    await this.setToken(token);
    await this.setUser(user);

    return { user, token };
  }

  async register(data: RegisterData): Promise<{ user: User; token: string }> {
    const response = await apiService.post<{ user: User; token: string }>('/auth/register', data);
    
    if (response.error) {
      throw new Error(response.error);
    }

    const { user, token } = response.data;
    await this.setToken(token);
    await this.setUser(user);

    return { user, token };
  }

  async logout(): Promise<void> {
    await AsyncStorage.multiRemove([this.TOKEN_KEY, this.USER_KEY]);
  }

  async getToken(): Promise<string | null> {
    return AsyncStorage.getItem(this.TOKEN_KEY);
  }

  private async setToken(token: string): Promise<void> {
    await AsyncStorage.setItem(this.TOKEN_KEY, token);
  }

  async getUser(): Promise<User | null> {
    const userData = await AsyncStorage.getItem(this.USER_KEY);
    return userData ? JSON.parse(userData) : null;
  }

  private async setUser(user: User): Promise<void> {
    await AsyncStorage.setItem(this.USER_KEY, JSON.stringify(user));
  }

  async isAuthenticated(): Promise<boolean> {
    const token = await this.getToken();
    return !!token;
  }
}

export const authService = new AuthService();
```

## Custom Hooks

### 1. Auth Hook
```typescript
// src/hooks/useAuth.ts
import { useState, useEffect } from 'react';
import { authService } from '@/services/auth';
import { User } from '@/types/auth';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const isAuthenticated = await authService.isAuthenticated();
      if (isAuthenticated) {
        const userData = await authService.getUser();
        setUser(userData);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const { user } = await authService.login({ email, password });
      setUser(user);
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Login failed' 
      };
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string, name: string) => {
    setLoading(true);
    try {
      const { user } = await authService.register({ email, password, name });
      setUser(user);
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Registration failed' 
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await authService.logout();
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };
}
```

### 2. API Hook
```typescript
// src/hooks/useApi.ts
import { useState, useEffect, useCallback } from 'react';
import { apiService, ApiResponse } from '@/services/api';

export function useApi<T>(
  endpoint: string,
  options: {
    immediate?: boolean;
    dependencies?: any[];
  } = {}
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { immediate = true, dependencies = [] } = options;

  const execute = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.get<T>(endpoint);
      
      if (response.error) {
        setError(response.error);
      } else {
        setData(response.data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate, ...dependencies]);

  const refetch = () => execute();

  return {
    data,
    loading,
    error,
    refetch,
  };
}

// For mutations (POST, PUT, DELETE)
export function useApiMutation<T, P = any>(
  endpoint: string,
  method: 'POST' | 'PUT' | 'DELETE' = 'POST'
) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = useCallback(async (payload?: P) => {
    setLoading(true);
    setError(null);

    try {
      let response: ApiResponse<T>;

      switch (method) {
        case 'POST':
          response = await apiService.post<T>(endpoint, payload);
          break;
        case 'PUT':
          response = await apiService.put<T>(endpoint, payload);
          break;
        case 'DELETE':
          response = await apiService.delete<T>(endpoint);
          break;
        default:
          throw new Error('Unsupported method');
      }

      if (response.error) {
        setError(response.error);
        return { success: false, error: response.error };
      } else {
        return { success: true, data: response.data };
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, [endpoint, method]);

  return {
    mutate,
    loading,
    error,
  };
}
```

## Screen Examples

### 1. Login Screen
```typescript
// src/screens/auth/LoginScreen.tsx
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/Button';
import { TextInput } from '@/components/ui/TextInput';
import { Card } from '@/components/ui/Card';
import { useTheme } from '@/theme/ThemeContext';

export function LoginScreen({ navigation }: any) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading } = useAuth();
  const { colors } = useTheme();

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    const result = await login(email, password);
    
    if (!result.success) {
      Alert.alert('Login Failed', result.error);
    }
  };

  return (
    <KeyboardAvoidingView
      style={[styles.container, { backgroundColor: colors.background }]}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <View style={styles.content}>
        <Text style={[styles.title, { color: colors.text }]}>
          Welcome Back
        </Text>
        <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
          Sign in to continue
        </Text>

        <Card style={styles.form}>
          <TextInput
            label="Email"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
            placeholder="Enter your email"
          />

          <TextInput
            label="Password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            placeholder="Enter your password"
          />

          <Button
            title="Sign In"
            onPress={handleLogin}
            loading={loading}
            style={styles.button}
          />

          <Button
            title="Create Account"
            onPress={() => navigation.navigate('Register')}
            variant="outline"
            style={styles.button}
          />
        </Card>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 32,
  },
  form: {
    marginBottom: 24,
  },
  button: {
    marginTop: 16,
  },
});
```

### 2. Home Screen
```typescript
// src/screens/home/HomeScreen.tsx
import React from 'react';
import { View, Text, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { useApi } from '@/hooks/useApi';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { useTheme } from '@/theme/ThemeContext';

interface Post {
  id: string;
  title: string;
  content: string;
  created_at: string;
}

export function HomeScreen() {
  const { colors } = useTheme();
  const { data: posts, loading, error, refetch } = useApi<Post[]>('/posts');

  const renderPost = ({ item }: { item: Post }) => (
    <Card style={styles.postCard}>
      <Text style={[styles.postTitle, { color: colors.text }]}>
        {item.title}
      </Text>
      <Text style={[styles.postContent, { color: colors.textSecondary }]}>
        {item.content}
      </Text>
      <Text style={[styles.postDate, { color: colors.textSecondary }]}>
        {new Date(item.created_at).toLocaleDateString()}
      </Text>
    </Card>
  );

  if (error) {
    return (
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <Text style={[styles.errorText, { color: colors.error }]}>
          {error}
        </Text>
        <Button title="Retry" onPress={refetch} />
      </View>
    );
  }

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <FlatList
        data={posts}
        renderItem={renderPost}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl refreshing={loading} onRefresh={refetch} />
        }
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text style={[styles.emptyText, { color: colors.textSecondary }]}>
              No posts available
            </Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  list: {
    padding: 16,
  },
  postCard: {
    marginBottom: 16,
  },
  postTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  postContent: {
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 8,
  },
  postDate: {
    fontSize: 12,
  },
  errorText: {
    fontSize: 16,
    textAlign: 'center',
    marginVertical: 20,
  },
  empty: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyText: {
    fontSize: 16,
  },
});
```

## Device Features Integration

### 1. Camera Service
```typescript
// src/services/camera.ts
import * as ImagePicker from 'expo-image-picker';

interface CameraResult {
  uri: string;
  base64?: string;
  width: number;
  height: number;
}

class CameraService {
  async requestPermissions(): Promise<boolean> {
    const result = await ImagePicker.requestCameraPermissionsAsync();
    return result.status === 'granted';
  }

  async takePicture(options?: ImagePicker.CameraOptions): Promise<CameraResult | null> {
    const hasPermission = await this.requestPermissions();
    
    if (!hasPermission) {
      throw new Error('Camera permission denied');
    }

    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,
      allowsEditing: true,
      ...options,
    });

    if (result.canceled) {
      return null;
    }

    return {
      uri: result.assets[0].uri,
      base64: result.assets[0].base64,
      width: result.assets[0].width,
      height: result.assets[0].height,
    };
  }

  async pickFromGallery(options?: ImagePicker.ImagePickerOptions): Promise<CameraResult | null> {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,
      allowsEditing: true,
      ...options,
    });

    if (result.canceled) {
      return null;
    }

    return {
      uri: result.assets[0].uri,
      base64: result.assets[0].base64,
      width: result.assets[0].width,
      height: result.assets[0].height,
    };
  }
}

export const cameraService = new CameraService();
```

### 2. Location Service
```typescript
// src/services/location.ts
import * as Location from 'expo-location';

interface LocationCoordinates {
  latitude: number;
  longitude: number;
  altitude?: number;
  accuracy?: number;
}

class LocationService {
  async requestPermissions(): Promise<boolean> {
    const { status } = await Location.requestForegroundPermissionsAsync();
    return status === 'granted';
  }

  async getCurrentLocation(): Promise<LocationCoordinates | null> {
    const hasPermission = await this.requestPermissions();
    
    if (!hasPermission) {
      throw new Error('Location permission denied');
    }

    try {
      const location = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.Balanced,
      });

      return {
        latitude: location.coords.latitude,
        longitude: location.coords.longitude,
        altitude: location.coords.altitude || undefined,
        accuracy: location.coords.accuracy || undefined,
      };
    } catch (error) {
      console.error('Error getting location:', error);
      return null;
    }
  }

  async watchLocation(
    callback: (location: LocationCoordinates) => void
  ): Promise<Location.LocationSubscription | null> {
    const hasPermission = await this.requestPermissions();
    
    if (!hasPermission) {
      throw new Error('Location permission denied');
    }

    try {
      return await Location.watchPositionAsync(
        {
          accuracy: Location.Accuracy.Balanced,
          timeInterval: 1000,
          distanceInterval: 10,
        },
        (location) => {
          callback({
            latitude: location.coords.latitude,
            longitude: location.coords.longitude,
            altitude: location.coords.altitude || undefined,
            accuracy: location.coords.accuracy || undefined,
          });
        }
      );
    } catch (error) {
      console.error('Error watching location:', error);
      return null;
    }
  }
}

export const locationService = new LocationService();
```

## Quick Start Setup

### 1. Installation Commands
```bash
# Create new Expo app
npx create-expo-app my-grok-app --template

# Install navigation
npm install @react-navigation/native @react-navigation/native-stack @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context

# Install UI libraries
npm install @expo/vector-icons react-native-svg
npm install react-native-async-storage react-native-gesture-handler

# Install device features
npx expo install expo-camera expo-location expo-image-picker
```

### 2. App Entry Point
```typescript
// App.tsx
import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { AppNavigator } from '@/navigation/AppNavigator';

export default function App() {
  return (
    <>
      <StatusBar style="auto" />
      <AppNavigator />
    </>
  );
}
```

## Best Practices

1. **Performance**: Use FlatList for long lists, optimize images
2. **Memory**: Clean up listeners and subscriptions in useEffect cleanup
3. **Offline**: Implement caching and offline support
4. **Security**: Store sensitive data securely, use HTTPS
5. **Accessibility**: Add accessibility labels and hints

Remember: Mobile development requires attention to platform-specific behaviors and performance constraints. Test thoroughly on both iOS and Android devices.