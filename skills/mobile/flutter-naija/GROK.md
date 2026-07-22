---
name: flutter-naija
category: mobile
version: 2.0.0
tags: [mobile, flutter, dart, cross-platform, naija]
---

# Flutter Naija

## Overview

Flutter development toolkit with a Nigerian tech ecosystem focus, covering cross-platform mobile development with Dart and Flutter. This skill provides patterns for Flutter app architecture, widget composition, state management with Riverpod and Bloc, native platform integration, and deployment strategies optimized for the African mobile market including offline-first design, low-bandwidth considerations, and mobile money payment integrations.

## Core Capabilities

- **Flutter Widgets**: Compositional widget trees, custom painters, animations, and responsive layouts
- **State Management**: Riverpod, Bloc/Cubit, andGetX patterns with clean architecture separation
- **Platform Channels**: Native Android/iOS integration via MethodChannel and Platform Interface
- **Navigation**: GoRouter declarative routing with deep linking and nested navigation
- **Local Storage**: Hive, Isar, and drift (SQLite) for offline-first data persistence
- **Networking**: Dio HTTP client with interceptors, caching, and retry logic
- **Payment Integration**: Flutterwave, Paystack, and mobile money SDK integration patterns
- **Testing**: Widget tests, integration tests, and golden image testing

## Usage Examples

```dart
// Riverpod State Management with Clean Architecture
@riverpod
class ItemListNotifier extends _$ItemListNotifier {
  @override
  Future<List<Item>> build() async {
    final repository = ref.watch(itemRepositoryProvider);
    return repository.getItems();
  }

  Future<void> addItem(String name) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final repository = ref.watch(itemRepositoryProvider);
      await repository.createItem(Item(name: name, createdAt: DateTime.now()));
      return repository.getItems();
    });
  }

  Future<void> deleteItem(String id) async {
    state = await AsyncValue.guard(() async {
      final repository = ref.watch(itemRepositoryProvider);
      await repository.deleteItem(id);
      return repository.getItems();
    });
  }
}

// Flutter Widget with Responsive Design
class ItemListScreen extends ConsumerWidget {
  const ItemListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final itemsAsync = ref.watch(itemListNotifierProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Items'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => _showAddDialog(context, ref),
          ),
        ],
      ),
      body: itemsAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => ErrorWidget(message: e.toString()),
        data: (items) => items.isEmpty
            ? const EmptyState(message: 'No items yet')
            : RefreshIndicator(
                onRefresh: () => ref.invalidate(itemListNotifierProvider),
                child: ListView.builder(
                  itemCount: items.length,
                  itemBuilder: (ctx, i) => ItemCard(
                    item: items[i],
                    onDelete: () => ref
                        .read(itemListNotifierProvider.notifier)
                        .deleteItem(items[i].id),
                  ),
                ),
              ),
      ),
    );
  }
}

// GoRouter Configuration
final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        builder: (ctx, state) => const HomeScreen(),
        routes: [
          GoRoute(
            path: 'items',
            builder: (ctx, state) => const ItemListScreen(),
          ),
          GoRoute(
            path: 'items/:id',
            builder: (ctx, state) => ItemDetailScreen(
              itemId: state.pathParameters['id']!,
            ),
          ),
        ],
      ),
    ],
  );
});

// Platform Channel for Native Integration
class NativeBridge {
  static const _channel = MethodChannel('com.example/native_bridge');

  static Future<String> getDeviceInfo() async {
    final result = await _channel.invokeMethod('getDeviceInfo');
    return result as String;
  }

  static Future<bool> shareContent(String content) async {
    final result = await _channel.invokeMethod('shareContent', {
      'content': content,
    });
    return result as bool;
  }
}

// Dio HTTP Client with Interceptors
class ApiClient {
  late final Dio _dio;

  ApiClient({required String baseUrl}) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {'Content-Type': 'application/json'},
    ));

    _dio.interceptors.addAll([
      LogInterceptor(requestBody: true, responseBody: true),
      RetryInterceptor(retries: 3, retryDelay: const Duration(seconds: 2)),
      AuthInterceptor(),
    ]);
  }

  Future<Response> get(String path, {Map<String, dynamic>? queryParameters}) {
    return _dio.get(path, queryParameters: queryParameters);
  }

  Future<Response> post(String path, {dynamic data}) {
    return _dio.post(path, data: data);
  }
}
```

## Best Practices

- Design for low-bandwidth environments: implement aggressive caching, compressed images, and lazy loading
- Use Riverpod for dependency injection and state management with code generation
- Implement offline-first with Hive or Isar for local data persistence
- Use `go_router` for declarative navigation with deep linking support
- Leverage `flutter_animate` for performant, declarative animations
- Optimize for Android Go devices with reduced animation and image quality modes
- Integrate Flutterwave/Paystack SDK for Nigerian payment processing
- Use `flutter_localizations` and `intl` for Yoruba, Igbo, and Hausa language support
- Profile with DevTools for frame rendering performance and memory usage
- Write golden image tests for visual regression detection

## Related Modules

- `android-development` - Native Android development with Kotlin
- `ios-development` - Native iOS development with Swift/SwiftUI
- `react-native` - React Native alternative for cross-platform development
- `expo-react-native` - Expo-managed React Native workflow

## Advanced Configuration

### Flutter Project Structure

```yaml
# pubspec.yaml
name: flutter_naija_app
description: A Flutter app for Nigerian users
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  # State Management
  flutter_riverpod: ^2.4.0
  riverpod_annotation: ^2.3.0
  
  # Navigation
  go_router: ^12.0.0
  
  # Networking
  dio: ^5.3.0
  retrofit: ^4.0.0
  
  # Local Storage
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  isar: ^3.1.0+1
  
  # UI
  flutter_animate: ^4.3.0
  shimmer: ^3.0.0
  cached_network_image: ^3.3.0
  
  # Nigerian Integration
  flutterwave_flutter: ^1.0.0
  paystack_flutter: ^1.0.0
  
  # Localization
  flutter_localizations:
    sdk: flutter
  intl: ^0.18.0
  
  # Firebase
  firebase_core: ^2.24.0
  firebase_messaging: ^14.7.0
  firebase_analytics: ^10.8.0
  
  # Utils
  url_launcher: ^6.2.0
  connectivity_plus: ^5.0.0
  path_provider: ^2.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  build_runner: ^2.4.0
  riverpod_generator: ^2.3.0
  hive_generator: ^2.0.0
  isar_generator: ^3.1.0+1
  mockito: ^5.4.0
  golden_toolkit: ^0.15.0

flutter:
  uses-material-design: true
  
  assets:
    - assets/images/
    - assets/icons/
    - assets/l10n/
  
  fonts:
    - family: Nunito
      fonts:
        - asset: assets/fonts/Nunito-Regular.ttf
        - asset: assets/fonts/Nunito-Bold.ttf
          weight: 700
        - asset: assets/fonts/Nunito-Light.ttf
          weight: 300
```

### Riverpod State Management

```dart
// lib/providers/item_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../models/item.dart';
import '../services/api_service.dart';

part 'item_provider.g.dart';

@riverpod
class ItemList extends _$ItemList {
  @override
  Future<List<Item>> build() async {
    final apiService = ref.watch(apiServiceProvider);
    return apiService.getItems();
  }

  Future<void> addItem(Item item) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final apiService = ref.read(apiServiceProvider);
      await apiService.createItem(item);
      return apiService.getItems();
    });
  }

  Future<void> deleteItem(String id) async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final apiService = ref.read(apiServiceProvider);
      await apiService.deleteItem(id);
      return apiService.getItems();
    });
  }
}

@riverpod
class ItemDetail extends _$ItemDetail {
  @override
  Future<Item?> build(String id) async {
    final apiService = ref.watch(apiServiceProvider);
    return apiService.getItem(id);
  }
}

// lib/providers/connectivity_provider.dart
@riverpod
Stream<bool> connectivity(ConnectivityRef ref) {
  return Connectivity().onConnectivityChanged.map((results) {
    return results.any((result) => result != ConnectivityResult.none);
  });
}
```

### GoRouter Navigation

```dart
// lib/router/app_router.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../screens/home_screen.dart';
import '../screens/detail_screen.dart';
import '../screens/settings_screen.dart';
import '../screens/profile_screen.dart';

final routerProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/',
    debugLogDiagnostics: true,
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomeScreen(),
        routes: [
          GoRoute(
            path: 'detail/:id',
            builder: (context, state) {
              final id = state.pathParameters['id']!;
              return DetailScreen(id: id);
            },
          ),
        ],
      ),
      GoRoute(
        path: '/settings',
        builder: (context, state) => const SettingsScreen(),
      ),
      GoRoute(
        path: '/profile',
        builder: (context, state) => const ProfileScreen(),
      ),
    ],
    errorBuilder: (context, state) => Scaffold(
      body: Center(
        child: Text('Page not found: ${state.error}'),
      ),
    ),
  );
});
```

## Architecture Patterns

### Clean Architecture

```
├── lib/
│   ├── core/                    # Core utilities
│   │   ├── constants/          # App constants
│   │   ├── theme/              # App theme
│   │   ├── utils/              # Utility functions
│   │   └── errors/             # Error handling
│   ├── data/                   # Data layer
│   │   ├── models/             # Data models
│   │   ├── repositories/       # Repository implementations
│   │   └── services/           # API and local services
│   ├── domain/                 # Domain layer
│   │   ├── entities/           # Business entities
│   │   ├── repositories/       # Repository interfaces
│   │   └── usecases/           # Use cases
│   ├── presentation/           # Presentation layer
│   │   ├── screens/            # Screen widgets
│   │   ├── widgets/            # Reusable widgets
│   │   └── providers/          # State providers
│   └── main.dart               # App entry point
```

### Domain Layer

```dart
// lib/domain/entities/item.dart
class Item {
  final String id;
  final String name;
  final String description;
  final double price;
  final String category;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Item({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.category,
    required this.createdAt,
    required this.updatedAt,
  });

  Item copyWith({
    String? id,
    String? name,
    String? description,
    double? price,
    String? category,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Item(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      price: price ?? this.price,
      category: category ?? this.category,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}

// lib/domain/repositories/item_repository.dart
abstract class ItemRepository {
  Future<List<Item>> getItems();
  Future<Item?> getItem(String id);
  Future<Item> createItem(Item item);
  Future<Item> updateItem(Item item);
  Future<void> deleteItem(String id);
}

// lib/domain/usecases/get_items_usecase.dart
class GetItemsUseCase {
  final ItemRepository repository;

  GetItemsUseCase(this.repository);

  Future<List<Item>> call() async {
    return await repository.getItems();
  }
}
```

### Data Layer

```dart
// lib/data/models/item_model.dart
import '../../domain/entities/item.dart';

class ItemModel extends Item {
  const ItemModel({
    required super.id,
    required super.name,
    required super.description,
    required super.price,
    required super.category,
    required super.createdAt,
    required super.updatedAt,
  });

  factory ItemModel.fromJson(Map<String, dynamic> json) {
    return ItemModel(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      price: (json['price'] as num).toDouble(),
      category: json['category'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'price': price,
      'category': category,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}

// lib/data/repositories/item_repository_impl.dart
import '../../domain/entities/item.dart';
import '../../domain/repositories/item_repository.dart';
import '../models/item_model.dart';
import '../services/api_service.dart';

class ItemRepositoryImpl implements ItemRepository {
  final ApiService apiService;

  ItemRepositoryImpl(this.apiService);

  @override
  Future<List<Item>> getItems() async {
    final response = await apiService.getItems();
    return response.map((json) => ItemModel.fromJson(json)).toList();
  }

  @override
  Future<Item?> getItem(String id) async {
    final response = await apiService.getItem(id);
    if (response != null) {
      return ItemModel.fromJson(response);
    }
    return null;
  }

  @override
  Future<Item> createItem(Item item) async {
    final itemModel = ItemModel(
      id: item.id,
      name: item.name,
      description: item.description,
      price: item.price,
      category: item.category,
      createdAt: item.createdAt,
      updatedAt: item.updatedAt,
    );
    final response = await apiService.createItem(itemModel.toJson());
    return ItemModel.fromJson(response);
  }

  @override
  Future<Item> updateItem(Item item) async {
    final itemModel = ItemModel(
      id: item.id,
      name: item.name,
      description: item.description,
      price: item.price,
      category: item.category,
      createdAt: item.createdAt,
      updatedAt: item.updatedAt,
    );
    final response = await apiService.updateItem(item.id, itemModel.toJson());
    return ItemModel.fromJson(response);
  }

  @override
  Future<void> deleteItem(String id) async {
    await apiService.deleteItem(id);
  }
}
```

## Integration Guide

### Nigerian Payment Integration

```dart
// lib/services/payment_service.dart
import 'package:flutterwave_flutter/flutterwave.dart';
import 'package:paystack_flutter/paystack_flutter.dart';

class PaymentService {
  final Flutterwave flutterwave;
  final PaystackClient paystackClient;

  PaymentService({
    required this.flutterwave,
    required this.paystackClient,
  });

  // Flutterwave payment
  Future<ChargeResponse?> initiateFlutterwavePayment({
    required double amount,
    required String currency,
    required String email,
    required String name,
    String? phone,
  }) async {
    try {
      final Charge charge = Charge()
        ..amount = (amount * 100).toInt()
        ..currency = currency
        ..email = email
        ..name = name
        ..phone = phone;

      final CheckoutResponse response = await flutterwave.checkout(
        charge: charge,
      );

      if (response.success) {
        return ChargeResponse(
          transactionId: response.txRef,
          status: 'success',
          amount: amount,
        );
      }
      return null;
    } catch (e) {
      return null;
    }
  }

  // Paystack payment
  Future<ChargeResponse?> initiatePaystackPayment({
    required double amount,
    required String email,
    required String reference,
  }) async {
    try {
      final Charge charge = Charge()
        ..amount = (amount * 100).toInt()
        ..email = email
        ..reference = reference;

      final InitializeTransactionResponse response =
          await paystackClient.initializeTransaction(charge);

      if (response.status) {
        final VerifyTransactionResponse verifyResponse =
            await paystackClient.verifyTransaction(response.reference);

        if (verifyResponse.status) {
          return ChargeResponse(
            transactionId: response.reference,
            status: 'success',
            amount: amount,
          );
        }
      }
      return null;
    } catch (e) {
      return null;
    }
  }
}

// lib/models/charge_response.dart
class ChargeResponse {
  final String transactionId;
  final String status;
  final double amount;

  const ChargeResponse({
    required this.transactionId,
    required this.status,
    required this.amount,
  });
}
```

### Nigerian Language Support

```dart
// lib/l10n/app_localizations.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

class AppLocalizations {
  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  static const supportedLocales = [
    Locale('en', 'NG'), // English (Nigeria)
    Locale('yo', 'NG'), // Yoruba
    Locale('ig', 'NG'), // Igbo
    Locale('ha', 'NG'), // Hausa
  ];

  static const localizationsDelegates = [
    GlobalMaterialLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
    AppLocalizations.delegate,
  ];

  final Locale locale;

  AppLocalizations(this.locale);

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  // English strings
  String get appTitle => 'Flutter Naija';
  String get home => 'Home';
  String get settings => 'Settings';
  String get profile => 'Profile';
  String get save => 'Save';
  String get cancel => 'Cancel';
  String get delete => 'Delete';
  String get edit => 'Edit';
  String get loading => 'Loading...';
  String get error => 'Error';
  String get retry => 'Retry';
  String get noData => 'No data available';
  String get networkError => 'Network error. Please check your connection.';

  // Yoruba strings
  String get yoAppTitle => 'Flutter Naija';
  String get yoHome => 'Ile';
  String get yoSettings => 'Eto';
  String get yoProfile => 'Profaili';
  String get yoSave => 'Fi pamole';
  String get yoCancel => 'Fagile';
  String get yoDelete => 'Yọ ki';
  String get yoEdit => 'Ṣe atunto';
  String get yoLoading => 'N gbani...';
  String get yoError => 'Aṣiṣa';
  String get yoRetry => 'Gbige lẹhin';
  String get yoNoData => 'Ko si data';
  String get yoNetworkError => 'Aṣiṣa eto. Jọwọ ṣe akiyesi eto yin.';
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) {
    return ['en', 'yo', 'ig', 'ha'].contains(locale.languageCode);
  }

  @override
  Future<AppLocalizations> load(Locale locale) async {
    return AppLocalizations(locale);
  }

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}
```

### Firebase Integration

```dart
// lib/services/firebase_service.dart
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:firebase_analytics/firebase_analytics.dart';

class FirebaseService {
  static FirebaseAnalytics? _analytics;
  static FirebaseMessaging? _messaging;

  static Future<void> initialize() async {
    await Firebase.initializeApp();
    _analytics = FirebaseAnalytics.instance;
    _messaging = FirebaseMessaging.instance;

    // Request notification permissions
    await _messaging!.requestPermission(
      alert: true,
      badge: true,
      sound: true,
    );

    // Get FCM token
    final token = await _messaging!.getToken();
    print('FCM Token: $token');

    // Handle foreground messages
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      print('Foreground message: ${message.notification?.title}');
    });

    // Handle background messages
    FirebaseMessaging.onBackgroundMessage(_backgroundMessageHandler);

    // Handle notification taps
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      print('Notification tapped: ${message.data}');
    });
  }

  @pragma('vm:entry-point')
  static Future<void> _backgroundMessageHandler(
      RemoteMessage message) async {
    print('Background message: ${message.notification?.title}');
  }

  static Future<void> logEvent(String name, {Map<String, dynamic>? parameters}) async {
    await _analytics?.logEvent(name: name, parameters: parameters);
  }

  static Future<void> setUserId(String userId) async {
    await _analytics?.setUserId(id: userId);
  }

  static Future<void> setCurrentScreen(String screenName) async {
    await _analytics?.logScreenView(screenName: screenName);
  }
}
```

## Performance Optimization

### Image Optimization

```dart
// lib/widgets/optimized_image.dart
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';

class OptimizedImage extends StatelessWidget {
  final String url;
  final double? width;
  final double? height;
  final BoxFit fit;
  final BorderRadius? borderRadius;

  const OptimizedImage({
    super.key,
    required this.url,
    this.width,
    this.height,
    this.fit = BoxFit.cover,
    this.borderRadius,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: borderRadius ?? BorderRadius.circular(8),
      child: CachedNetworkImage(
        imageUrl: url,
        width: width,
        height: height,
        fit: fit,
        placeholder: (context, url) => Container(
          width: width,
          height: height,
          color: Colors.grey[200],
          child: const Center(
            child: CircularProgressIndicator(),
          ),
        ),
        errorWidget: (context, url, error) => Container(
          width: width,
          height: height,
          color: Colors.grey[200],
          child: const Icon(Icons.error),
        ),
        memCacheHeight: (height ?? 200).toInt(),
        memCacheWidth: (width ?? 200).toInt(),
      ),
    );
  }
}
```

### List Optimization

```dart
// lib/widgets/optimized_list.dart
import 'package:flutter/material.dart';

class OptimizedList<T> extends StatelessWidget {
  final List<T> items;
  final Widget Function(BuildContext, T, int) itemBuilder;
  final Widget Function(BuildContext, int)? separatorBuilder;
  final Future<void> Function()? onRefresh;
  final ScrollController? controller;
  final bool shrinkWrap;

  const OptimizedList({
    super.key,
    required this.items,
    required this.itemBuilder,
    this.separatorBuilder,
    this.onRefresh,
    this.controller,
    this.shrinkWrap = false,
  });

  @override
  Widget build(BuildContext context) {
    Widget listWidget;

    if (separatorBuilder != null) {
      listWidget = ListView.separated(
        controller: controller,
        shrinkWrap: shrinkWrap,
        itemCount: items.length,
        addAutomaticKeepAlives: true,
        addRepaintBoundaries: true,
        itemBuilder: (context, index) => itemBuilder(context, items[index], index),
        separatorBuilder: separatorBuilder!,
      );
    } else {
      listWidget = ListView.builder(
        controller: controller,
        shrinkWrap: shrinkWrap,
        itemCount: items.length,
        addAutomaticKeepAlives: true,
        addRepaintBoundaries: true,
        itemBuilder: (context, index) => itemBuilder(context, items[index], index),
      );
    }

    if (onRefresh != null) {
      return RefreshIndicator(
        onRefresh: onRefresh!,
        child: listWidget,
      );
    }

    return listWidget;
  }
}
```

### Animation Optimization

```dart
// lib/widgets/animated_card.dart
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

class AnimatedCard extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final Duration animationDuration;

  const AnimatedCard({
    super.key,
    required this.child,
    this.onTap,
    this.animationDuration = const Duration(milliseconds: 300),
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: child
          .animate(duration: animationDuration)
          .fadeIn()
          .slideY(begin: 0.1, end: 0)
          .scale(begin: const Offset(0.95, 0.95)),
    );
  }
}
```

## Security Considerations

### Secure Storage

```dart
// lib/services/secure_storage_service.dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorageService {
  static const FlutterSecureStorage _storage = FlutterSecureStorage(
    aOptions: AndroidOptions(encryptedSharedPreferences: true),
    iOptions: IOSOptions(
      accessibility: KeychainAccessibility.first_unlock_this_device,
    ),
  );

  static Future<void> saveToken(String key, String value) async {
    await _storage.write(key: key, value: value);
  }

  static Future<String?> getToken(String key) async {
    return await _storage.read(key: key);
  }

  static Future<void> deleteToken(String key) async {
    await _storage.delete(key: key);
  }

  static Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
```

### Certificate Pinning

```dart
// lib/services/network_security.dart
import 'dart:io';

class NetworkSecurity {
  static HttpClient createHttpClient() {
    final client = HttpClient()
      ..badCertificateCallback = (X509Certificate cert, String host, int port) {
        // Implement certificate pinning logic
        return cert.sha256 == 'YOUR_CERTIFICATE_SHA256';
      };
    return client;
  }
}
```

## Troubleshooting Guide

### Common Issues

#### Issue: Build Failures

```bash
# Clean Flutter
flutter clean
flutter pub get

# iOS specific
cd ios && pod install && cd ..

# Android specific
cd android && ./gradlew clean && cd ..
```

#### Issue: Performance Issues

```dart
// lib/utils/performance_monitor.dart
import 'package:flutter/material.dart';

class PerformanceMonitor {
  static void startTrace(String name) {
    debugPrint('Performance: Starting $name');
  }

  static void stopTrace(String name) {
    debugPrint('Performance: Stopping $name');
  }

  static void logFrameTime(Duration frameTime) {
    if (frameTime.inMilliseconds > 16) {
      debugPrint('Performance: Slow frame detected: ${frameTime.inMilliseconds}ms');
    }
  }
}
```

#### Issue: Memory Leaks

```dart
// lib/utils/memory_monitor.dart
import 'dart:developer' as developer;

class MemoryMonitor {
  static void logMemoryUsage() {
    developer.log('Memory usage logged');
  }

  static void checkForLeaks() {
    // Implement memory leak detection
  }
}
```

## API Reference

### Riverpod API

```dart
// Provider types
final counterProvider = StateProvider<int>((ref) => 0);
final futureProvider = FutureProvider<List<Item>>((ref) async {
  final apiService = ref.watch(apiServiceProvider);
  return apiService.getItems();
});
final streamProvider = StreamProvider<String>((ref) {
  return Stream.periodic(const Duration(seconds: 1), (i) => '$i');
});

// Using providers
final counter = ref.watch(counterProvider);
final items = ref.watch(futureProvider);
```

### GoRouter API

```dart
// Navigation methods
context.go('/details/$id');
context.push('/details/$id');
context.goNamed('details', pathParameters: {'id': id});
context.pop();
context.pushReplacement('/');
```

## Data Models

### Domain Models

```dart
// lib/models/item.dart
class Item {
  final String id;
  final String name;
  final String description;
  final double price;
  final String imageUrl;
  final String category;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Item({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.imageUrl,
    required this.category,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Item.fromJson(Map<String, dynamic> json) {
    return Item(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      price: (json['price'] as num).toDouble(),
      imageUrl: json['image_url'],
      category: json['category'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'price': price,
      'image_url': imageUrl,
      'category': category,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}
```

## Deployment Guide

### Android Configuration

```gradle
// android/app/build.gradle
android {
    compileSdkVersion 34

    defaultConfig {
        applicationId "com.example.flutter_naija"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
    }

    buildTypes {
        release {
            signingConfig signingConfigs.debug
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### iOS Configuration

```ruby
# ios/Podfile
platform :ios, '13.0'

target 'Runner' do
  use_frameworks!
  use_modular_headers!

  flutter_install_all_ios_pods File.dirname(File.realpath(__FILE__))
end
```

### CI/CD Configuration

```yaml
# .github/workflows/flutter.yml
name: Flutter CI

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
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'
    
    - name: Install dependencies
      run: flutter pub get
    
    - name: Analyze code
      run: flutter analyze
    
    - name: Run tests
      run: flutter test
    
    - name: Build APK
      run: flutter build apk --release
    
    - name: Build iOS
      run: flutter build ios --release --no-codesign
```

## Monitoring & Observability

### Crash Reporting

```dart
// lib/services/crash_reporting_service.dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/foundation.dart';

class CrashReportingService {
  static Future<void> initialize() async {
    FlutterError.onError = (errorDetails) {
      FirebaseCrashlytics.instance.recordFlutterFatalError(errorDetails);
    };

    PlatformDispatcher.instance.onError = (error, stack) {
      FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    };
  }

  static void logError(dynamic error, StackTrace? stackTrace) {
    FirebaseCrashlytics.instance.recordError(error, stackTrace);
  }

  static void logMessage(String message) {
    FirebaseCrashlytics.instance.log(message);
  }

  static void setCustomKey(String key, dynamic value) {
    FirebaseCrashlytics.instance.setCustomKey(key, value.toString());
  }

  static void setUserId(String userId) {
    FirebaseCrashlytics.instance.setUserId(userId);
  }
}
```

### Analytics

```dart
// lib/services/analytics_service.dart
import 'package:firebase_analytics/firebase_analytics.dart';

class AnalyticsService {
  static final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;

  static Future<void> logEvent(String name, {Map<String, dynamic>? parameters}) async {
    await _analytics.logEvent(name: name, parameters: parameters);
  }

  static Future<void> setCurrentScreen(String screenName) async {
    await _analytics.logScreenView(screenName: screenName);
  }

  static Future<void> logPurchase({
    required String itemId,
    required double value,
    required String currency,
  }) async {
    await _analytics.logPurchase(
      currency: currency,
      value: value,
      items: [
        AnalyticsEventItem(itemId: itemId),
      ],
    );
  }
}
```

## Testing Strategy

### Unit Tests

```dart
// test/domain/usecases/get_items_usecase_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:flutter_naija/domain/entities/item.dart';
import 'package:flutter_naija/domain/repositories/item_repository.dart';
import 'package:flutter_naija/domain/usecases/get_items_usecase.dart';

class MockItemRepository extends Mock implements ItemRepository {}

void main() {
  late GetItemsUseCase useCase;
  late MockItemRepository mockRepository;

  setUp(() {
    mockRepository = MockItemRepository();
    useCase = GetItemsUseCase(mockRepository);
  });

  test('should get items from repository', () async {
    // Arrange
    final items = [
      Item(
        id: '1',
        name: 'Test Item',
        description: 'Test Description',
        price: 9.99,
        category: 'Test',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      ),
    ];

    when(mockRepository.getItems()).thenAnswer((_) async => items);

    // Act
    final result = await useCase();

    // Assert
    expect(result, items);
    verify(mockRepository.getItems());
    verifyNoMoreInteractions(mockRepository);
  });
}
```

### Widget Tests

```dart
// test/presentation/screens/home_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_naija/presentation/screens/home_screen.dart';

void main() {
  testWidgets('HomeScreen displays correctly', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: HomeScreen(),
        ),
      ),
    );

    expect(find.text('Home'), findsOneWidget);
    expect(find.byType(ListView), findsOneWidget);
  });

  testWidgets('HomeScreen shows loading indicator', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: HomeScreen(),
        ),
      ),
    );

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });
}
```

### Golden Tests

```dart
// test/golden/home_screen_golden_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:golden_toolkit/golden_toolkit.dart';
import 'package:flutter_naija/presentation/screens/home_screen.dart';

void main() {
  testAppWidget('HomeScreen golden test', (tester) async {
    await tester.pumpWidgetBuilder(
      const MaterialApp(
        home: HomeScreen(),
      ),
      surfaceSize: const Size(375, 812),
    );

    await tester.pumpAndSettle();

    await screenMatchesGolden(tester, 'home_screen');
  });
}
```

## Versioning & Migration

### App Versioning

```dart
// lib/utils/version_manager.dart
import 'package:package_info_plus/package_info_plus.dart';

class VersionManager {
  static Future<String> getAppVersion() async {
    final packageInfo = await PackageInfo.fromPlatform();
    return packageInfo.version;
  }

  static Future<int> getBuildNumber() async {
    final packageInfo = await PackageInfo.fromPlatform();
    return int.parse(packageInfo.buildNumber);
  }

  static Future<String> getPackageName() async {
    final packageInfo = await PackageInfo.fromPlatform();
    return packageInfo.packageName;
  }
}
```

### API Versioning

```dart
// lib/services/api_client.dart
enum ApiVersion {
  v1,
  v2,
}

class ApiClient {
  final ApiVersion version;
  final String baseUrl;

  ApiClient({
    this.version = ApiVersion.v2,
    required this.baseUrl,
  });

  String get apiUrl => '$baseUrl/${version.name}';

  Future<dynamic> get(String path) async {
    final response = await dio.get('$apiUrl$path');
    return response.data;
  }

  Future<dynamic> post(String path, {dynamic data}) async {
    final response = await dio.post('$apiUrl$path', data: data);
    return response.data;
  }
}
```

## Glossary

### Flutter Terms

| Term | Definition |
|------|------------|
| **Flutter** | Cross-platform UI toolkit by Google |
| **Dart** | Programming language for Flutter |
| **Widget** | Building block of Flutter UI |
| **StatelessWidget** | Widget without mutable state |
| **StatefulWidget** | Widget with mutable state |
| **Riverpod** | State management solution |
| **GoRouter** | Declarative routing solution |
| **Isar** | Fast NoSQL database |
| **Hive** | Lightweight key-value database |
| **DevTools** | Flutter debugging tools |

## Changelog

### Version 2.0.0 (2024-01-15)
- Added Riverpod with code generation
- Implemented GoRouter navigation
- Enhanced Firebase integration
- Added Nigerian payment support

### Version 1.5.0 (2023-10-01)
- Added Hive local storage
- Implemented Isar database
- Enhanced animations
- Added localization

### Version 1.4.0 (2023-07-15)
- Added Dio networking
- Implemented Retrofit
- Enhanced state management
- Added testing

### Version 1.3.0 (2023-04-01)
- Added basic Flutter
- Implemented Material Design
- Enhanced UI
- Added API

### Version 1.2.0 (2023-01-15)
- Added Flutter setup
- Implemented basic screens
- Added navigation
- Enhanced documentation

### Version 1.1.0 (2022-10-01)
- Added basic Flutter
- Implemented basic UI
- Added state management
- Enhanced UI

### Version 1.0.0 (2022-07-15)
- Initial release
- Basic Flutter Naija
- Cross-platform support
- Basic functionality

## Contributing Guidelines

### Development Setup

```bash
# Clone repository
git clone https://github.com/company/flutter-naija.git
cd flutter-naija

# Install dependencies
flutter pub get

# Run code generation
dart run build_runner build

# Run app
flutter run

# Run tests
flutter test

# Build APK
flutter build apk --release

# Build iOS
flutter build ios --release
```

### Code Standards

- Follow Dart style guide
- Use meaningful variable names
- Write unit and widget tests
- Implement proper error handling
- Use clean architecture
- Follow Flutter best practices

## License

MIT License

Copyright (c) 2024 Flutter Naija Contributors

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
