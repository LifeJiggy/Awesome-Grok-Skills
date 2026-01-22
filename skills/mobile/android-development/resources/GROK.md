# Android Development

## Overview

Android Development involves creating applications for the Android operating system, the world's most widely used mobile platform running on billions of devices globally. This skill requires proficiency in Kotlin or Java programming, Android SDK components, Jetpack libraries, and Material Design guidelines. Android developers must navigate device fragmentation across manufacturers, OS versions, and screen sizes while delivering consistent user experiences. The platform emphasizes openness, customization, and Google Play distribution, with strong support for background processing, notifications, and hardware integration.

## Core Capabilities

Kotlin has become the preferred language for Android development, offering concise syntax, null safety, coroutines for asynchronous programming, and full interoperability with existing Java codebases. Android Jetpack provides a suite of libraries that accelerate development with best-practice implementations for data persistence, navigation, lifecycle management, and UI components. Jetpack Compose enables declarative UI development, allowing developers to build modern, reactive interfaces with less boilerplate code than traditional XML layouts.

Room database provides abstraction over SQLite for local data persistence with compile-time query validation and automatic migrations. WorkManager handles reliable background work that survives process death, essential for syncing, notifications, and scheduled tasks. Navigation component simplifies in-app navigation with type-safe arguments and deep link handling. Hilt dependency injection integrates cleanly with the Android framework for testable, maintainable architecture.

## Usage Examples

```python
from android_skill import AndroidApp, KotlinCodeGenerator, GradleProject, PlayStoreManager

# Initialize Android app project
app_project = AndroidApp(
    name="TaskMaster",
    package_name="com.company.taskmaster",
    min_sdk=24,
    target_sdk=34,
    compile_sdk=34,
    language="kotlin"
)

# Generate Kotlin ViewModel
view_model = KotlinCodeGenerator.create_viewmodel(
    name="TaskViewModel",
    application_class="Application",
    properties=[
        ("_tasks", "MutableLiveData<List<Task>>", "private"),
        ("isLoading", "LiveData<Boolean>", "public"),
        ("errorMessage", "LiveData<String>", "public")
    ],
    methods=[
        "fun loadTasks() { viewModelScope.launch { repository.getTasks() } }",
        "fun addTask(task: Task) { viewModelScope.launch { repository.insert(task) } }",
        "fun updateTask(task: Task) { viewModelScope.launch { repository.update(task) } }",
        "fun deleteTask(task: Task) { viewModelScope.launch { repository.delete(task) } }"
    ],
    dependencies=["repository: TaskRepository", "dispatcher: CoroutineDispatcher"]
)

# Generate Jetpack Compose screen
compose_screen = KotlinCodeGenerator.create_composable(
    name="TaskListScreen",
    view_model="TaskViewModel",
    state_holder="TaskListUiState",
    components=["LazyColumn", "TaskItem", "FloatingActionButton"],
    columns=1,
    has_appbar=True,
    has_scaffold=True
)

# Create Gradle build configuration
gradle_project = GradleProject(
    project_name="taskmaster",
    android_gradle_plugin="8.2.0",
    kotlin_version="1.9.21",
    buildscript_repositories=["google()", "mavenCentral()"],
    dependencies={
        "implementation": [
            "androidx.core:core-ktx:1.12.0",
            "androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0",
            "androidx.lifecycle:lifecycle-runtime-ktx:2.7.0",
            "androidx.activity:activity-compose:1.8.2",
            "androidx.compose.ui:ui",
            "androidx.compose.ui:ui-graphics",
            "androidx.compose.ui:ui-tooling-preview",
            "androidx.room:room-runtime:2.6.1",
            "androidx.room:room-ktx:2.6.1"
        ],
        "testImplementation": [
            "junit:junit:4.13.2",
            "org.mockito:mockito-core:5.8.0",
            "org.mockito.kotlin:mockito-kotlin:5.2.1",
            "androidx.arch.core:core-testing:2.2.0"
        ],
        "androidTestImplementation": [
            "androidx.test.ext:junit:1.1.5",
            "androidx.test.espresso:espresso-core:3.5.1",
            "androidx.compose.ui:ui-test-junit4"
        ]
    }
)

# Generate Android manifest
manifest = gradle_project.generate_manifest(
    package_name="com.company.taskmaster",
    activities=[
        {
            "name": ".MainActivity",
            "exported": True,
            "launcher": True,
            "theme": "@style/Theme.TaskMaster"
        },
        {
            "name": ".TaskDetailActivity",
            "exported": False,
            "parent_activity": ".MainActivity"
        }
    ],
    permissions=[
        "android.permission.INTERNET",
        "android.permission.POST_NOTIFICATIONS"
    ],
    features=[
        {"name": "android.hardware.camera", "required": False}
    ]
)

# Build debug APK
build_result = gradle_project.build(
    variant="debug",
    tasks=["assembleDebug"],
    options={"parallel": True, "configure_on_demand": True}
)
print(f"Build Status: {build_result.status}")
print(f"APK Location: {build_result.output_path}")

# Manage Google Play Store release
play_store = PlayStoreManager(
    package_name="com.company.taskmaster",
    service_account_json="credentials.json"
)

# Create new release
release = play_store.create_release(
    track="internal",
    version_code=12,
    version_name="1.2.0",
    release_notes={
        "en-US": "Added task sharing and collaborative lists"
    },
    obb=False,
    rollout_percentage=100
)

# Upload APK and commit release
play_store.upload_apk(
    apk_path="app/build/outputs/apk/debug/app-debug.apk",
    track="internal"
)
```

## Best Practices

Embrace Kotlin as the primary language, leveraging its null safety, extension functions, and coroutines for cleaner, more maintainable code. Adopt the MVVM architecture with unidirectional data flow, separating UI concerns from business logic for testability. Use Jetpack libraries to benefit from backwards compatibility and reduce boilerplate code. Implement proper dependency injection with Hilt to facilitate testing and modular architecture.

Design for performance from the start, using profiling tools, optimizing RecyclerView with DiffUtil, and minimizing memory allocations in frequently-called code paths. Handle configuration changes properly to preserve UI state using ViewModel and saved instance state. Support dark mode and dynamic colors following Material 3 guidelines. Test comprehensively with unit tests, instrumented tests, and lint checks to catch issues before production release.

## Related Skills

- iOS Development (mobile development for Apple platforms)
- Test Automation (automated testing for mobile applications)
- Performance Testing (Android app performance optimization)
- Kotlin Programming (language-specific development skills)

## Use Cases

Android Development skills enable creation of applications reaching the vast Android user base across consumer, enterprise, and specialized domains. Consumer apps leverage Android's notification system, widgets, and home screen integration for daily utility. Enterprise applications utilize Android's enterprise APIs for secure deployment, MDM integration, and work profiles. IoT applications connect to smart devices using Bluetooth, NFC, and network APIs that Android supports extensively.
