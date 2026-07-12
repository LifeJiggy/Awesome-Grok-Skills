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
