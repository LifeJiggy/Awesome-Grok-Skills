---
name: android-development
category: mobile
version: 2.0.0
tags: [mobile, android, kotlin, jetpack-compose, gradle]
---

# Android Development

## Overview

Comprehensive Android application development toolkit covering native Android development with Kotlin and Java, Jetpack Compose UI framework, Gradle build system, Android architecture patterns, and platform-specific APIs. This skill provides production-ready patterns for building performant, accessible, and maintainable Android applications targeting the full spectrum of Android devices.

## Core Capabilities

- **Jetpack Compose UI**: Declarative UI development with Material 3 theming, animations, and state management
- **Android Architecture**: MVVM, MVI, Clean Architecture, and repository pattern implementations
- **Gradle Build System**: Custom build scripts, product flavors, build types, and dependency management
- **Room Database**: Type-safe local persistence with migrations and reactive queries
- **Networking**: Retrofit + OkHttp configuration, interceptors, serialization with Kotlinx Serialization
- **Background Work**: WorkManager scheduling, foreground services, and coroutine-based concurrency
- **Permissions**: Runtime permission handling, permission groups, and denied-state flows
- **Testing**: Unit tests with JUnit5, UI tests with Compose testing, and integration tests

## Usage Examples

```kotlin
// Android ViewModel with StateFlow pattern
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val repository: ItemRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<HomeUiState>(HomeUiState.Loading)
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        loadItems()
    }

    private fun loadItems() {
        viewModelScope.launch {
            repository.getItems()
                .catch { e -> _uiState.value = HomeUiState.Error(e.message ?: "Unknown error") }
                .collect { items -> _uiState.value = HomeUiState.Success(items) }
        }
    }

    fun refresh() {
        _uiState.value = HomeUiState.Loading
        loadItems()
    }
}

// Jetpack Compose Screen
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(viewModel: HomeViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = { TopAppBar(title = { Text("Home") }) }
    ) { padding ->
        when (val state = uiState) {
            is HomeUiState.Loading -> CircularProgressIndicator(modifier = Modifier.padding(padding))
            is HomeUiState.Success -> ItemList(items = state.items, modifier = Modifier.padding(padding))
            is HomeUiState.Error -> ErrorMessage(message = state.message, onRetry = viewModel::refresh)
        }
    }
}

// Retrofit API Definition
interface ApiService {
    @GET("items")
    suspend fun getItems(): Response<List<Item>>

    @POST("items")
    suspend fun createItem(@Body item: CreateItemRequest): Response<Item>

    @Path("id") @DELETE("items/{id}")
    suspend fun deleteItem(@Path("id") itemId: String): Response<Unit>
}

// Room Database Entity and DAO
@Entity(tableName = "items")
data class ItemEntity(
    @PrimaryKey val id: String,
    val name: String,
    val updatedAt: Long
)

@Dao
interface ItemDao {
    @Query("SELECT * FROM items ORDER BY updatedAt DESC")
    fun getAllItems(): Flow<List<ItemEntity>>

    @Upsert
    suspend fun upsertItem(item: ItemEntity)

    @Query("DELETE FROM items WHERE id = :id")
    suspend fun deleteById(id: String)
}
```

## Best Practices

- Use Kotlin Coroutines and Flow for all asynchronous operations instead of RxJava
- Implement unidirectional data flow (UDF) with Compose state hoisting
- Apply dependency injection with Hilt/Dagger for testability and modularity
- Use DataStore instead of SharedPreferences for type-safe preferences
- Follow Material Design 3 guidelines for consistent UI/UX
- Implement offline-first architecture with Room as single source of truth
- Use ProGuard/R8 rules carefully to avoid reflection-based crashes
- Profile memory, CPU, and battery usage regularly with Android Profiler
- Target the latest stable SDK while maintaining backward compatibility
- Write Compose preview functions for rapid UI iteration

## Related Modules

- `ios-development` - Cross-platform considerations and platform parity patterns
- `flutter-naija` - Flutter alternative for Android development
- `react-native` - React Native cross-platform mobile development
- `expo-react-native` - Managed React Native workflow for rapid prototyping
