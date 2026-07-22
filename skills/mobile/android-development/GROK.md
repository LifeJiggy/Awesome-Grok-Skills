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

## Advanced Configuration

### Gradle Build Configuration

```kotlin
// build.gradle.kts - Advanced configuration
android {
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        // Room schema export
        ksp {
            arg("room.schemaLocation", "$projectDir/schemas")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
        debug {
            isDebuggable = true
            applicationIdSuffix = ".debug"
        }
    }

    productFlavors {
        create("dev") {
            dimension = "environment"
            applicationIdSuffix = ".dev"
            versionNameSuffix = "-dev"
        }
        create("staging") {
            dimension = "environment"
            applicationIdSuffix = ".staging"
            versionNameSuffix = "-staging"
        }
        create("production") {
            dimension = "environment"
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
        buildConfig = true
        viewBinding = true
    }
}
```

### Hilt Dependency Injection

```kotlin
// Application Module
@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .addConverterFactory(KotlinxSerializationConverterFactory.create())
            .client(provideOkHttpClient())
            .build()
    }

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(AuthInterceptor())
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            })
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        )
        .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
        .build()
    }

    @Provides
    @Singleton
    fun provideItemRepository(
        apiService: ApiService,
        itemDao: ItemDao
    ): ItemRepository {
        return ItemRepositoryImpl(apiService, itemDao)
    }
}

// Repository Implementation
class ItemRepositoryImpl @Inject constructor(
    private val apiService: ApiService,
    private val itemDao: ItemDao
) : ItemRepository {

    override fun getItems(): Flow<List<Item>> {
        return itemDao.getAllItems()
            .map { entities -> entities.map { it.toDomain() } }
            .onStart {
                // Refresh from network
                try {
                    val remoteItems = apiService.getItems()
                    itemDao.upsertAll(remoteItems.map { it.toEntity() })
                } catch (e: Exception) {
                    // Handle network error
                }
            }
    }
}
```

### Room Database Configuration

```kotlin
// Database with migrations
@Database(
    entities = [ItemEntity::class, UserEntity::class],
    version = 3,
    exportSchema = true
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun itemDao(): ItemDao
    abstract fun userDao(): UserDao
}

// Type converters
class Converters {
    @TypeConverter
    fun fromTimestamp(value: Long?): Date? {
        return value?.let { Date(it) }
    }

    @TypeConverter
    fun dateToTimestamp(date: Date?): Long? {
        return date?.time
    }

    @TypeConverter
    fun fromStringList(value: List<String>): String {
        return value.joinToString(",")
    }

    @TypeConverter
    fun toStringList(value: String): List<String> {
        return value.split(",")
    }
}

// Migrations
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE items ADD COLUMN createdAt INTEGER NOT NULL DEFAULT 0")
    }
}

val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE TABLE users (id TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL)")
    }
}
```

## Architecture Patterns

### Android Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Android Architecture                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │   UI     │──▶│ViewModel │──▶│ UseCase  │──▶│Repository│ │
│  │(Compose) │   │(StateFlow)│  │          │   │          │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       │              │              │              │        │
│       ▼              ▼              ▼              ▼        │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  State   │   │  Event   │   │  Domain  │   │   Data   │ │
│  │  Hoisting│   │  Handling│   │  Models  │   │  Sources │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Clean Architecture Layers

```kotlin
// Domain Layer
data class Item(
    val id: String,
    val name: String,
    val description: String,
    val createdAt: Date
)

interface ItemRepository {
    fun getItems(): Flow<List<Item>>
    suspend fun getItem(id: String): Item?
    suspend fun createItem(item: Item): Item
    suspend fun updateItem(item: Item): Item
    suspend fun deleteItem(id: String)
}

// Use Case Layer
class GetItemsUseCase @Inject constructor(
    private val repository: ItemRepository
) {
    operator fun invoke(): Flow<List<Item>> {
        return repository.getItems()
    }
}

// Data Layer
class ItemRepositoryImpl @Inject constructor(
    private val apiService: ApiService,
    private val itemDao: ItemDao
) : ItemRepository {
    // Implementation
}

// UI Layer
@HiltViewModel
class ItemViewModel @Inject constructor(
    private val getItemsUseCase: GetItemsUseCase
) : ViewModel() {
    // ViewModel implementation
}
```

### State Management Pattern

```kotlin
// Sealed class for UI states
sealed class ItemUiState {
    data object Loading : ItemUiState()
    data class Success(val items: List<Item>) : ItemUiState()
    data class Error(val message: String) : ItemUiState()
}

// ViewModel with state management
@HiltViewModel
class ItemViewModel @Inject constructor(
    private val getItemsUseCase: GetItemsUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow<ItemUiState>(ItemUiState.Loading)
    val uiState: StateFlow<ItemUiState> = _uiState.asStateFlow()

    private val _events = Channel<ItemEvent>()
    val events: Flow<ItemEvent> = _events.receiveAsFlow()

    init {
        loadItems()
    }

    private fun loadItems() {
        viewModelScope.launch {
            getItemsUseCase()
                .catch { e ->
                    _uiState.value = ItemUiState.Error(e.message ?: "Unknown error")
                }
                .collect { items ->
                    _uiState.value = ItemUiState.Success(items)
                }
        }
    }

    fun onAction(action: ItemAction) {
        when (action) {
            is ItemAction.Refresh -> loadItems()
            is ItemAction.DeleteItem -> deleteItem(action.id)
        }
    }

    private fun deleteItem(id: String) {
        viewModelScope.launch {
            try {
                // Delete item
                _events.send(ItemEvent.ItemDeleted)
                loadItems()
            } catch (e: Exception) {
                _events.send(ItemEvent.Error(e.message ?: "Delete failed"))
            }
        }
    }
}

// Actions and Events
sealed class ItemAction {
    data object Refresh : ItemAction()
    data class DeleteItem(val id: String) : ItemAction()
}

sealed class ItemEvent {
    data object ItemDeleted : ItemEvent()
    data class Error(val message: String) : ItemEvent()
}
```

## Integration Guide

### Firebase Integration

```kotlin
// Firebase Configuration
@Module
@InstallIn(SingletonComponent::class)
object FirebaseModule {
    @Provides
    @Singleton
    fun provideFirebaseAuth(): FirebaseAuth {
        return FirebaseAuth.getInstance()
    }

    @Provides
    @Singleton
    fun provideFirestore(): FirebaseFirestore {
        return FirebaseFirestore.getInstance()
    }

    @Provides
    @Singleton
    fun provideFirebaseMessaging(): FirebaseMessaging {
        return FirebaseMessaging.getInstance()
    }
}

// Push Notifications
class PushNotificationService : FirebaseMessagingService() {
    override fun onNewToken(token: String) {
        super.onNewToken(token)
        // Send token to server
    }

    override fun onMessageReceived(message: RemoteMessage) {
        super.onMessageReceived(message)
        // Handle notification
    }
}
```

### Analytics Integration

```kotlin
// Analytics Module
@Module
@InstallIn(SingletonComponent::class)
object AnalyticsModule {
    @Provides
    @Singleton
    fun provideAnalytics(): AnalyticsHelper {
        return AnalyticsHelper()
    }
}

class AnalyticsHelper @Inject constructor() {
    private val firebaseAnalytics = FirebaseAnalytics.getInstance(FirebaseApp.getInstance())

    fun logEvent(name: String, params: Bundle? = null) {
        firebaseAnalytics.logEvent(name, params)
    }

    fun logScreenView(screenName: String) {
        val params = bundleOf(
            FirebaseAnalytics.Param.SCREEN_NAME to screenName
        )
        logEvent(FirebaseAnalytics.Event.SCREEN_VIEW, params)
    }

    fun logPurchase(itemId: String, price: Double, currency: String) {
        val params = bundleOf(
            FirebaseAnalytics.Param.ITEM_ID to itemId,
            FirebaseAnalytics.Param.PRICE to price,
            FirebaseAnalytics.Param.CURRENCY to currency
        )
        logEvent(FirebaseAnalytics.Event.PURCHASE, params)
    }
}
```

## Performance Optimization

### Image Loading Optimization

```kotlin
// Coil Image Loading
@Composable
fun AsyncImage(
    model: String,
    contentDescription: String?,
    modifier: Modifier = Modifier
) {
    AsyncImage(
        model = ImageRequest.Builder(LocalContext.current)
            .data(model)
            .crossfade(true)
            .memoryCachePolicy(CachePolicy.ENABLED)
            .diskCachePolicy(CachePolicy.ENABLED)
            .build(),
        contentDescription = contentDescription,
        modifier = modifier,
        placeholder = painterResource(R.drawable.placeholder),
        error = painterResource(R.drawable.error)
    )
}
```

### Database Optimization

```kotlin
// Room Database Optimization
@Dao
interface ItemDao {
    @Query("SELECT * FROM items WHERE id = :id")
    suspend fun getItemById(id: String): ItemEntity?

    @Query("SELECT * FROM items ORDER BY updatedAt DESC LIMIT :limit")
    fun getRecentItems(limit: Int): Flow<List<ItemEntity>>

    @Transaction
    suspend fun upsertItems(items: List<ItemEntity>) {
        items.forEach { item ->
            insertOrUpdate(item)
        }
    }

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdate(item: ItemEntity)
}

// Database Indexing
@Entity(
    tableName = "items",
    indices = [
        Index(value = ["name"]),
        Index(value = ["updatedAt"])
    ]
)
data class ItemEntity(
    @PrimaryKey val id: String,
    val name: String,
    val updatedAt: Long
)
```

### Memory Optimization

```kotlin
// Memory Leak Prevention
class ItemFragment : Fragment() {
    private var _binding: FragmentItemBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentItemBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

// ViewModel Scope Management
@HiltViewModel
class ItemViewModel @Inject constructor(
    private val repository: ItemRepository
) : ViewModel() {
    private val _items = MutableStateFlow<List<Item>>(emptyList())
    val items: StateFlow<List<Item>> = _items.asStateFlow()

    init {
        viewModelScope.launch {
            repository.getItems()
                .collect { items ->
                    _items.value = items
                }
        }
    }

    // viewModelScope automatically cancels when ViewModel is cleared
}
```

## Security Considerations

### Data Encryption

```kotlin
// EncryptedSharedPreferences
class SecurePreferences @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val sharedPreferences = EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    fun saveToken(token: String) {
        sharedPreferences.edit().putString("auth_token", token).apply()
    }

    fun getToken(): String? {
        return sharedPreferences.getString("auth_token", null)
    }
}
```

### Network Security

```kotlin
// Certificate Pinning
class NetworkSecurityConfig {
    companion object {
        fun create(context: Context): NetworkSecurityConfig {
            return Builder()
                .certificatePinner(
                    CertificatePinner.Builder()
                        .add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
                        .build()
                )
                .build()
        }
    }
}

// ProGuard Rules
// -keep class com.example.app.data.models.** { *; }
// -keep class com.example.app.data.api.** { *; }
// -keepclassmembers class * {
#     @com.google.gson.annotations.SerializedName <fields>;
# }
```

## Troubleshooting Guide

### Common Issues

#### Issue: Compose Recomposition Issues

```kotlin
// Symptom: Excessive recomposition
// Diagnosis:
@Composable
fun OptimizedComposable(items: List<Item>) {
    // Use key for stable lists
    LazyColumn {
        items(items, key = { it.id }) { item ->
            ItemRow(item = item)
        }
    }
}

// Use derivedStateOf for computed values
@Composable
fun FilteredList(items: List<Item>, filter: String) {
    val filteredItems by remember(items, filter) {
        derivedStateOf {
            items.filter { it.name.contains(filter, ignoreCase = true) }
        }
    }
}
```

#### Issue: Memory Leaks

```kotlin
// Symptom: OutOfMemoryError or increasing memory usage
// Diagnosis:
class LeakDiagnostics {
    fun analyzeMemory(context: Context) {
        val runtime = Runtime.getRuntime()
        val usedMemory = runtime.totalMemory() - runtime.freeMemory()
        val maxMemory = runtime.maxMemory()

        Log.d("Memory", "Used: ${usedMemory / 1024 / 1024}MB")
        Log.d("Memory", "Max: ${maxMemory / 1024 / 1024}MB")
        Log.d("Memory", "Usage: ${usedMemory * 100 / maxMemory}%")
    }
}

// Resolution:
// 1. Use weak references
// 2. Cancel coroutines in onCleared
// 3. Nullify references in onDestroyView
```

#### Issue: ANR (Application Not Responding)

```kotlin
// Symptom: ANR dialogs appearing
// Diagnosis:
class ANRDiagnostics {
    fun checkMainThread() {
        if (Looper.myLooper() == Looper.getMainLooper()) {
            Log.w("ANR", "Running on main thread")
        }
    }
}

// Resolution:
// 1. Move heavy operations to background
// 2. Use coroutines with Dispatchers.IO
// 3. Optimize database queries
```

## API Reference

### Compose UI Components

```kotlin
// Custom Composable
@Composable
fun CustomCard(
    title: String,
    subtitle: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        onClick = onClick,
        modifier = modifier,
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = subtitle,
                style = MaterialTheme.typography.bodyMedium
            )
        }
    }
}
```

### Navigation

```kotlin
// Navigation Setup
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = "home"
    ) {
        composable("home") {
            HomeScreen(
                onItemClick = { itemId ->
                    navController.navigate("detail/$itemId")
                }
            )
        }
        composable(
            route = "detail/{itemId}",
            arguments = listOf(navArgument("itemId") { type = NavType.StringType })
        ) { backStackEntry ->
            val itemId = backStackEntry.arguments?.getString("itemId") ?: ""
            DetailScreen(itemId = itemId)
        }
    }
}
```

## Data Models

### Domain Models

```kotlin
// Domain Model
data class Item(
    val id: String,
    val name: String,
    val description: String,
    val price: Double,
    val imageUrl: String,
    val createdAt: Date,
    val updatedAt: Date
)

// API Response
@Serializable
data class ItemResponse(
    @SerialName("id") val id: String,
    @SerialName("name") val name: String,
    @SerialName("description") val description: String,
    @SerialName("price") val price: Double,
    @SerialName("image_url") val imageUrl: String,
    @SerialName("created_at") val createdAt: String,
    @SerialName("updated_at") val updatedAt: String
)

// Database Entity
@Entity(tableName = "items")
data class ItemEntity(
    @PrimaryKey val id: String,
    val name: String,
    val description: String,
    val price: Double,
    val imageUrl: String,
    val createdAt: Long,
    val updatedAt: Long
)

// Mapper Extensions
fun ItemResponse.toDomain(): Item {
    return Item(
        id = id,
        name = name,
        description = description,
        price = price,
        imageUrl = imageUrl,
        createdAt = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(createdAt) ?: Date(),
        updatedAt = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(updatedAt) ?: Date()
    )
}

fun Item.toEntity(): ItemEntity {
    return ItemEntity(
        id = id,
        name = name,
        description = description,
        price = price,
        imageUrl = imageUrl,
        createdAt = createdAt.time,
        updatedAt = updatedAt.time
    )
}
```

## Deployment Guide

### Build Configuration

```kotlin
// release build.gradle.kts
android {
    signingConfigs {
        create("release") {
            storeFile = file("keystore/release.jks")
            storePassword = System.getenv("KEYSTORE_PASSWORD")
            keyAlias = System.getenv("KEY_ALIAS")
            keyPassword = System.getenv("KEY_PASSWORD")
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

### CI/CD Configuration

```yaml
# .github/workflows/android.yml
name: Android CI

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
    
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
    
    - name: Setup Gradle
      uses: gradle/gradle-build-action@v2
    
    - name: Grant execute permission for gradlew
      run: chmod +x gradlew
    
    - name: Build with Gradle
      run: ./gradlew build
    
    - name: Run Tests
      run: ./gradlew test
    
    - name: Build APK
      run: ./gradlew assembleRelease
```

## Monitoring & Observability

### Crash Reporting

```kotlin
// Firebase Crashlytics
class CrashReporting @Inject constructor() {
    private val crashlytics = Firebase.crashlytics

    fun logError(throwable: Throwable, message: String? = null) {
        message?.let { crashlytics.log(it) }
        crashlytics.recordException(throwable)
    }

    fun setCustomKey(key: String, value: Any) {
        when (value) {
            is String -> crashlytics.setCustomKey(key, value)
            is Boolean -> crashlytics.setCustomKey(key, value)
            is Double -> crashlytics.setCustomKey(key, value)
            is Float -> crashlytics.setCustomKey(key, value)
            is Int -> crashlytics.setCustomKey(key, value)
            is Long -> crashlytics.setCustomKey(key, value)
        }
    }

    fun setUserId(userId: String) {
        crashlytics.setUserId(userId)
    }
}
```

### Performance Monitoring

```kotlin
// Firebase Performance
class PerformanceMonitoring @Inject constructor() {
    private val performance = Firebase.performance

    fun startTrace(traceName: String): Trace {
        return performance.newTrace(traceName).apply {
            start()
        }
    }

    fun stopTrace(trace: Trace) {
        trace.stop()
    }

    fun logNetworkRequest(url: String, method: String) {
        val metric = performance.newHttpMetric(url, method)
        metric.start()
        // After request completes
        metric.stop()
    }
}
```

## Testing Strategy

### Unit Tests

```kotlin
// ViewModel Tests
class ItemViewModelTest {
    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private lateinit var viewModel: ItemViewModel
    private lateinit var getItemsUseCase: GetItemsUseCase

    @Before
    fun setup() {
        getItemsUseCase = mockk()
        viewModel = ItemViewModel(getItemsUseCase)
    }

    @Test
    fun `when loadItems succeeds, uiState is Success`() = runTest {
        val items = listOf(Item("1", "Test", "Description", 10.0, "", Date(), Date()))
        every { getItemsUseCase() } returns flowOf(items)

        viewModel.loadItems()

        val state = viewModel.uiState.value
        assert(state is ItemUiState.Success)
        assertEquals(items, (state as ItemUiState.Success).items)
    }

    @Test
    fun `when loadItems fails, uiState is Error`() = runTest {
        every { getItemsUseCase() } returns flow { throw Exception("Network error") }

        viewModel.loadItems()

        val state = viewModel.uiState.value
        assert(state is ItemUiState.Error)
    }
}
```

### UI Tests

```kotlin
// Compose UI Tests
class HomeScreenTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun displayLoadingState() {
        composeTestRule.setContent {
            HomeScreen(uiState = ItemUiState.Loading)
        }

        composeTestRule.onNodeWithTag("loading_indicator").assertIsDisplayed()
    }

    @Test
    fun displaySuccessState() {
        val items = listOf(Item("1", "Test Item", "Description", 10.0, "", Date(), Date()))

        composeTestRule.setContent {
            HomeScreen(uiState = ItemUiState.Success(items))
        }

        composeTestRule.onNodeWithText("Test Item").assertIsDisplayed()
    }

    @Test
    fun clickItem_navigatesToDetail() {
        var clickedItemId: String? = null

        composeTestRule.setContent {
            HomeScreen(
                uiState = ItemUiState.Success(listOf(Item("1", "Test", "Desc", 10.0, "", Date(), Date()))),
                onItemClick = { clickedItemId = it }
            )
        }

        composeTestRule.onNodeWithText("Test").performClick()
        assertEquals("1", clickedItemId)
    }
}
```

## Versioning & Migration

### API Versioning

```kotlin
// API Version Configuration
object ApiConfig {
    const val BASE_URL = "https://api.example.com/"
    const val API_VERSION = "v2"

    object Headers {
        const val API_VERSION = "X-API-Version"
        const val AUTHORIZATION = "Authorization"
    }
}

// Retrofit with versioning
fun createRetrofit(): Retrofit {
    return Retrofit.Builder()
        .baseUrl(ApiConfig.BASE_URL)
        .addConverterFactory(KotlinxSerializationConverterFactory.create())
        .client(
            OkHttpClient.Builder()
                .addInterceptor { chain ->
                    val request = chain.request().newBuilder()
                        .addHeader(ApiConfig.Headers.API_VERSION, ApiConfig.API_VERSION)
                        .build()
                    chain.proceed(request)
                }
                .build()
        )
        .build()
}
```

### Database Migrations

```kotlin
// Room Database Migration Strategy
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE items ADD COLUMN priority INTEGER NOT NULL DEFAULT 0")
    }
}

val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE TABLE categories (id TEXT PRIMARY KEY NOT NULL, name TEXT NOT NULL)")
        db.execSQL("ALTER TABLE items ADD COLUMN categoryId TEXT")
    }
}

// Migration with destructive fallback
Room.databaseBuilder(context, AppDatabase::class.java, "database")
    .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
    .fallbackToDestructiveMigration()
    .build()
```

## Glossary

### Android Development Terms

| Term | Definition |
|------|------------|
| **Activity** | Android component for UI screens |
| **Fragment** | Reusable UI component within Activity |
| **ViewModel** | Manages UI-related data |
| **LiveData** | Observable data holder |
| **StateFlow** | Kotlin Flow for state management |
| **Coroutines** | Kotlin's asynchronous programming |
| **Hilt** | Dependency injection framework |
| **Room** | SQLite abstraction layer |
| **Retrofit** | Type-safe HTTP client |
| **Compose** | Declarative UI toolkit |
| **Gradle** | Build automation tool |
| **ProGuard** | Code obfuscation tool |
| **Material Design** | Google's design system |
| **Jetpack** | Android development libraries |

## Changelog

### Version 2.0.0 (2024-01-15)
- Added Compose Multiplatform support
- Implemented Kotlin 2.0 features
- Enhanced Hilt integration
- Added Performance Monitoring

### Version 1.5.0 (2023-10-01)
- Added Room database
- Implemented DataStore
- Enhanced navigation
- Added testing utilities

### Version 1.4.0 (2023-07-15)
- Added Jetpack Compose
- Implemented Material 3
- Enhanced animations
- Added accessibility

### Version 1.3.0 (2023-04-01)
- Added MVVM architecture
- Implemented repository pattern
- Added dependency injection
- Enhanced API

### Version 1.2.0 (2023-01-15)
- Added basic architecture
- Implemented networking
- Added local storage
- Enhanced documentation

### Version 1.1.0 (2022-10-01)
- Added Kotlin support
- Implemented basic UI
- Added build configuration
- Enhanced UI

### Version 1.0.0 (2022-07-15)
- Initial release
- Basic Android development
- REST API integration
- Local storage

## Contributing Guidelines

### Development Setup

```bash
# Clone repository
git clone https://github.com/company/android-app.git
cd android-app

# Open in Android Studio
# File -> Open -> Select project folder

# Build project
./gradlew build

# Run tests
./gradlew test

# Build APK
./gradlew assembleDebug
```

### Code Standards

- Follow Kotlin coding conventions
- Use meaningful variable names
- Write unit tests for ViewModels
- Write UI tests for Composables
- Use Compose preview functions
- Follow Material Design guidelines

## License

MIT License

Copyright (c) 2024 Android Development Contributors

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
