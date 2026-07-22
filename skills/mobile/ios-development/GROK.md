---
name: ios-development
category: mobile
version: 2.0.0
tags: [mobile, ios, swift, swiftui, xcode]
---

# iOS Development

## Overview

Native iOS application development with Swift and SwiftUI, covering the full lifecycle from Xcode project setup to App Store submission. This skill provides production patterns for SwiftUI declarative UI, Combine data flow, Core Data persistence, Swift concurrency (async/await), and Apple platform integration including WidgetKit, App Clips, and HealthKit. Designed for developers building performant, accessible, and maintainable iOS applications.

## Core Capabilities

- **SwiftUI Views**: Declarative UI with compositional views, adaptive layouts, and system integrations
- **Swift Concurrency**: Structured concurrency with async/await, actors, tasks, and custom executors
- **Combine Framework**: Reactive data pipelines with publishers, subscribers, and operators
- **Core Data + SwiftData**: Local persistence with type-safe models and migration strategies
- **Networking**: URLSession with async/await, Codable serialization, and retry strategies
- **Navigation**: NavigationStack/NavigationPath with deep linking and type-safe routing
- **Accessibility**: VoiceOver support, Dynamic Type, and inclusive design patterns
- **Testing**: XCTest, XCUITest, Swift Testing framework, and mock-based architectures

## Usage Examples

```swift
// SwiftUI View with MVVM pattern
struct ItemListView: View {
    @StateObject private var viewModel = ItemListViewModel()

    var body: some View {
        NavigationStack {
            Group {
                switch viewModel.state {
                case .idle, .loading:
                    ProgressView("Loading items...")
                case .loaded(let items):
                    List(items) { item in
                        NavigationLink(value: item.id) {
                            ItemRowView(item: item)
                        }
                    }
                    .refreshable { await viewModel.refresh() }
                case .error(let message):
                    ContentUnavailableView(
                        "Error",
                        systemImage: "exclamationmark.triangle",
                        description: Text(message)
                    )
                }
            }
            .navigationTitle("Items")
            .navigationDestination(for: Item.ID.self) { id in
                ItemDetailView(itemId: id)
            }
            .task { await viewModel.load() }
        }
    }
}

// ViewModel with async/await and @MainActor
@MainActor
final class ItemListViewModel: ObservableObject {
    @Published private(set) var state: ViewState = .idle

    private let repository: ItemRepositoryProtocol
    private var cancellables = Set<AnyCancellable>()

    init(repository: ItemRepositoryProtocol = ItemRepository()) {
        self.repository = repository
    }

    func load() async {
        state = .loading
        do {
            let items = try await repository.fetchItems()
            state = .loaded(items)
        } catch {
            state = .error(error.localizedDescription)
        }
    }

    func refresh() async {
        await load()
    }
}

// Swift Concurrency Networking
actor ItemRepository: ItemRepositoryProtocol {
    private let session: URLSession
    private let decoder: JSONDecoder
    private let baseURL: URL

    init(baseURL: URL = URL(string: "https://api.example.com")!) {
        self.session = .shared
        self.decoder = JSONDecoder()
        self.decoder.keyDecodingStrategy = .convertFromSnakeCase
        self.baseURL = baseURL
    }

    func fetchItems() async throws -> [Item] {
        let (data, response) = try await session.data(from: baseURL.appendingPathComponent("items"))
        guard let httpResponse = response as? HTTPURLResponse,
              200..<300 ~= httpResponse.statusCode else {
            throw APIError.invalidResponse
        }
        return try decoder.decode([Item].self, from: data)
    }
}

// SwiftData Model
@Model
class PersistedItem {
    var id: UUID
    var name: String
    var createdAt: Date
    var tags: [String]

    init(name: String, tags: [String] = []) {
        self.id = UUID()
        self.name = name
        self.createdAt = Date()
        self.tags = tags
    }
}

// WidgetKit Timeline Provider
struct ItemWidget: Widget {
    let kind = "ItemWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: ItemProvider()) { entry in
            ItemWidgetView(entry: entry)
        }
        .configurationDisplayName("Items")
        .description("View your latest items.")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

// Unit Test with Swift Testing
import Testing

struct ItemRepositoryTests {
    @Test("Fetch items returns decoded items")
    func testFetchItems() async throws {
        let sut = ItemRepository(baseURL: URL(string: "http://localhost:8080")!)
        let items = try await sut.fetchItems()
        #expect(items.count > 0)
    }
}
```

## Best Practices

- Use SwiftUI with @Observable macro (iOS 17+) or ObservableObject for older targets
- Prefer structured concurrency (async/await) over completion handlers and Combine for new code
- Use @MainActor for UI-bound state to ensure thread safety
- Implement offline-first architecture with SwiftData as single source of truth
- Use NavigationStack with type-safe navigation destinations over deprecated NavigationView
- Apply MVVM or TCA (The Composable Architecture) for scalable state management
- Test with Swift Testing framework for modern, expressive test syntax
- Use Instruments (Time Profiler, Allocations, Leaks) regularly for performance profiling
- Implement accessibility from the start, not as an afterthought
- Support Dynamic Type, Dark Mode, and all device sizes with adaptive layouts

## Related Modules

- `android-development` - Android-specific patterns and platform differences
- `flutter-naija` - Flutter alternative for iOS development
- `react-native` - React Native cross-platform iOS development
- `expo-react-native` - Expo-managed iOS development workflow

## Advanced Configuration

### Xcode Project Configuration

```swift
// Package.swift - Swift Package Manager configuration
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    products: [
        .library(
            name: "MyApp",
            targets: ["MyApp"]
        ),
    ],
    dependencies: [
        .package(url: "https://github.com/pointfreeco/swift-composable-architecture", from: "1.0.0"),
        .package(url: "https://github.com/kean/Nuke", from: "12.0.0"),
        .package(url: "https://github.com/firebase/firebase-ios-sdk", from: "10.0.0"),
    ],
    targets: [
        .target(
            name: "MyApp",
            dependencies: [
                .product(name: "ComposableArchitecture", package: "swift-composable-architecture"),
                .product(name: "Nuke", package: "Nuke"),
                .product(name: "FirebaseAuth", package: "firebase-ios-sdk"),
            ]
        ),
    ]
)
```

### SwiftData Configuration

```swift
// Models/Item.swift - SwiftData model
import Foundation
import SwiftData

@Model
final class Item {
    var id: UUID
    var name: String
    var description: String
    var price: Double
    var category: String
    var createdAt: Date
    var updatedAt: Date
    
    @Relationship(deleteRule: .cascade)
    var images: [ItemImage]?
    
    init(
        id: UUID = UUID(),
        name: String,
        description: String,
        price: Double,
        category: String,
        createdAt: Date = Date(),
        updatedAt: Date = Date()
    ) {
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.createdAt = createdAt
        self.updatedAt = updatedAt
    }
}

@Model
final class ItemImage {
    var id: UUID
    var url: String
    var order: Int
    
    init(id: UUID = UUID(), url: String, order: Int) {
        self.id = id
        self.url = url
        self.order = order
    }
}

// Persistence.swift - Model container setup
import SwiftData

struct PersistenceController {
    static let shared = PersistenceController()
    
    let container: ModelContainer
    
    init() {
        do {
            container = try ModelContainer(
                for: Item.self, ItemImage.self,
                configurations: ModelConfiguration(
                    isStoredInMemoryOnly: false,
                    allowsSave: true
                )
            )
        } catch {
            fatalError("Could not initialize ModelContainer: \(error)")
        }
    }
    
    init(inMemory: Bool = true) {
        do {
            let config = ModelConfiguration(isStoredInMemoryOnly: inMemory)
            container = try ModelContainer(
                for: Item.self, ItemImage.self,
                configurations: config
            )
        } catch {
            fatalError("Could not initialize ModelContainer: \(error)")
        }
    }
}
```

### Core Data Configuration

```swift
// CoreDataStack.swift - Core Data stack
import CoreData

class CoreDataStack {
    static let shared = CoreDataStack()
    
    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "MyApp")
        container.loadPersistentStores { _, error in
            if let error = error {
                fatalError("Core Data store failed: \(error)")
            }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
        container.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        return container
    }()
    
    var viewContext: NSManagedObjectContext {
        persistentContainer.viewContext
    }
    
    func newBackgroundContext() -> NSManagedObjectContext {
        persistentContainer.newBackgroundContext()
    }
    
    func save() {
        let context = viewContext
        guard context.hasChanges else { return }
        
        do {
            try context.save()
        } catch {
            let nsError = error as NSError
            fatalError("Core Data save error: \(nsError), \(nsError.userInfo)")
        }
    }
}
```

## Architecture Patterns

### iOS Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                iOS Architecture                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │   View   │──▶│ViewModel │──▶│  UseCase │──▶│Repository│ │
│  │(SwiftUI) │   │(TCA/VM)  │   │          │   │          │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       │              │              │              │        │
│       ▼              ▼              ▼              ▼        │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  State   │   │  Action  │   │  Domain  │   │   Data   │ │
│  │  Binding │   │  Handling│   │  Models  │   │  Sources │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### TCA (The Composable Architecture)

```swift
// Features/ItemList/ItemListFeature.swift
import ComposableArchitecture

@Reducer
struct ItemListFeature {
    @ObservableState
    struct State: Equatable {
        var items: IdentifiedArrayOf<Item> = []
        var isLoading = false
        var error: String?
    }
    
    enum Action {
        case onAppear
        case refreshItems
        case itemsLoaded(Result<[Item], Error>)
        case itemTapped(Item.ID)
        case deleteItems(IndexSet)
    }
    
    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .onAppear, .refreshItems:
                state.isLoading = true
                return .run { send in
                    let items = try await self.itemClient.fetchItems()
                    await send(.itemsLoaded(.success(items)))
                } catch: { error, send in
                    await send(.itemsLoaded(.failure(error)))
                }
                
            case .itemsLoaded(.success(let items)):
                state.isLoading = false
                state.items = IdentifiedArray(uniqueElements: items)
                return .none
                
            case .itemsLoaded(.failure(let error)):
                state.isLoading = false
                state.error = error.localizedDescription
                return .none
                
            case .itemTapped(let id):
                return .none
                
            case .deleteItems(let indexSet):
                state.items.remove(atOffsets: indexSet)
                return .none
            }
        }
    }
}

// Features/ItemList/ItemListViewModel.swift
import SwiftUI

@View
struct ItemListView: View {
    @Bindable var store: StoreOf<ItemListFeature>
    
    var body: some View {
        List {
            ForEach(store.items) { item in
                NavigationLink(state: ItemDetailFeature.State(item: item)) {
                    ItemRowView(item: item)
                }
            }
            .onDelete { store.send(.deleteItems($0)) }
        }
        .overlay {
            if store.isLoading {
                ProgressView()
            }
        }
        .refreshable {
            await store.send(.refreshItems).finish()
        }
        .onAppear {
            store.send(.onAppear)
        }
    }
}
```

### MVVM Pattern

```swift
// ViewModels/ItemListViewModel.swift
import SwiftUI
import Combine

@MainActor
final class ItemListViewModel: ObservableObject {
    @Published var items: [Item] = []
    @Published var isLoading = false
    @Published var error: String?
    
    private let repository: ItemRepository
    private var cancellables = Set<AnyCancellable>()
    
    init(repository: ItemRepository = ItemRepositoryImpl()) {
        self.repository = repository
    }
    
    func loadItems() async {
        isLoading = true
        error = nil
        
        do {
            items = try await repository.fetchItems()
        } catch {
            self.error = error.localizedDescription
        }
        
        isLoading = false
    }
    
    func refresh() async {
        await loadItems()
    }
    
    func deleteItem(_ item: Item) async {
        do {
            try await repository.deleteItem(item)
            items.removeAll { $0.id == item.id }
        } catch {
            self.error = error.localizedDescription
        }
    }
}

// Views/ItemListViewModel.swift
import SwiftUI

struct ItemListView: View {
    @StateObject private var viewModel = ItemListViewModel()
    
    var body: some View {
        NavigationStack {
            Group {
                switch (viewModel.isLoading, viewModel.error, viewModel.items) {
                case (true, _, _):
                    ProgressView("Loading items...")
                case (_, let error?, _):
                    ContentUnavailableView(
                        "Error",
                        systemImage: "exclamationmark.triangle",
                        description: Text(error)
                    )
                case (_, _, let items) where items.isEmpty:
                    ContentUnavailableView(
                        "No Items",
                        systemImage: "list.bullet",
                        description: Text("Add some items to get started")
                    )
                case (_, _, let items):
                    List(items) { item in
                        NavigationLink(value: item) {
                            ItemRowView(item: item)
                        }
                    }
                    .refreshable {
                        await viewModel.refresh()
                    }
                }
            }
            .navigationTitle("Items")
            .task {
                await viewModel.loadItems()
            }
        }
    }
}
```

## Integration Guide

### Firebase Integration

```swift
// AppDelegate.swift - Firebase setup
import FirebaseCore
import FirebaseAuth
import FirebaseFirestore

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        FirebaseApp.configure()
        return true
    }
}

// Services/FirebaseAuthService.swift
import FirebaseAuth

actor FirebaseAuthService {
    static let shared = FirebaseAuthService()
    
    var auth: Auth { Auth.auth() }
    
    func signIn(email: String, password: String) async throws -> User {
        let result = try await auth.signIn(withEmail: email, password: password)
        return User(firebaseUser: result.user)
    }
    
    func signUp(email: String, password: String) async throws -> User {
        let result = try await auth.createUser(withEmail: email, password: password)
        return User(firebaseUser: result.user)
    }
    
    func signOut() throws {
        try auth.signOut()
    }
    
    func resetPassword(email: String) async throws {
        try await auth.sendPasswordReset(withEmail: email)
    }
}
```

### CloudKit Integration

```swift
// Services/CloudKitService.swift
import CloudKit

actor CloudKitService {
    static let shared = CloudKitService()
    
    private let container: CKContainer
    private let database: CKDatabase
    
    init() {
        container = CKContainer.default()
        database = container.privateCloudDatabase
    }
    
    func save(_ record: CKRecord) async throws -> CKRecord {
        try await database.save(record)
    }
    
    func fetch(recordID: CKRecord.ID) async throws -> CKRecord {
        try await database.record(for: recordID)
    }
    
    func delete(recordID: CKRecord.ID) async throws {
        try await database.deleteRecord(withID: recordID)
    }
    
    func query(predicate: NSPredicate, sortDescriptors: [NSSortDescriptor] = []) async throws -> [CKRecord] {
        let query = CKQuery(recordType: "Item", predicate: predicate)
        query.sortDescriptors = sortDescriptors
        
        let (matchResults, _) = try await database.records(matching: query)
        return matchResults.compactMap { try? $0.1.get() }
    }
}
```

### HealthKit Integration

```swift
// Services/HealthKitService.swift
import HealthKit

class HealthKitService {
    static let shared = HealthKitService()
    
    private let healthStore = HKHealthStore()
    
    func requestAuthorization() async throws {
        let readTypes: Set<HKObjectType> = [
            HKObjectType.quantityType(forIdentifier: .stepCount)!,
            HKObjectType.quantityType(forIdentifier: .heartRate)!,
            HKObjectType.quantityType(forIdentifier: .activeEnergyBurned)!,
        ]
        
        try await healthStore.requestAuthorization(toShare: Set(), read: readTypes)
    }
    
    func fetchStepCount(startDate: Date, endDate: Date) async throws -> Double {
        let stepCountType = HKQuantityType.quantityType(forIdentifier: .stepCount)!
        let predicate = HKQuery.predicateForSamples(withStart: startDate, end: endDate)
        
        return try await withCheckedThrowingContinuation { continuation in
            let query = HKStatisticsQuery(
                quantityType: stepCountType,
                quantitySamplePredicate: predicate,
                options: .cumulativeSum
            ) { _, result, error in
                if let error = error {
                    continuation.resume(throwing: error)
                    return
                }
                
                let sum = result?.sumQuantity()?.doubleValue(for: .count()) ?? 0
                continuation.resume(returning: sum)
            }
            
            healthStore.execute(query)
        }
    }
}
```

## Performance Optimization

### Image Caching

```swift
// Services/ImageCache.swift
import SwiftUI
import Nuke

actor ImageCache {
    static let shared = ImageCache()
    
    private let imagePipeline = ImagePipeline {
        $0.dataCache = try? DataCache(name: "com.app.imagecache")
        $0.imageCache = ImageCache.shared
        $0.isRateLimiterEnabled = false
    }
    
    func loadImage(from url: URL) async throws -> UIImage {
        let request = ImageRequest(url: url)
        let image = try await imagePipeline.image(for: request).image
        return image
    }
    
    func preloadImages(urls: [URL]) {
        for url in urls {
            let request = ImageRequest(url: url)
            imagePipeline.startImagePipelineTask(with: request)
        }
    }
    
    func clearCache() {
        URLCache.shared.removeAllCachedResponses()
    }
}

// Views/AsyncImageView.swift
import SwiftUI
import NukeUI

struct AsyncImageView: View {
    let url: URL?
    var placeholder: Image = Image(systemName: "photo")
    
    var body: some View {
        LazyImage(url: url) { state in
            if let image = state.image {
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } else if state.isLoading {
                ProgressView()
            } else {
                placeholder
                    .foregroundColor(.secondary)
            }
        }
        .clipped()
    }
}
```

### Memory Management

```swift
// Utils/MemoryMonitor.swift
import Foundation
import os

actor MemoryMonitor {
    static let shared = MemoryMonitor()
    
    private let logger = Logger(subsystem: Bundle.main.bundleIdentifier!, category: "Memory")
    
    func checkMemoryUsage() {
        var info = mach_task_basic_info()
        var count = mach_msg_type_number_t(MemoryLayout<mach_task_basic_info>.size) / 4
        
        let result = withUnsafeMutablePointer(to: &info) {
            $0.withMemoryRebound(to: integer_t.self, capacity: 1) {
                task_info(mach_task_self_, task_flavor_t(MACH_TASK_BASIC_INFO), $0, &count)
            }
        }
        
        if result == KERN_SUCCESS {
            let usedMB = info.resident_size / 1024 / 1024
            logger.info("Memory usage: \(usedMB) MB")
            
            if usedMB > 500 {
                logger.warning("High memory usage detected")
                NotificationCenter.default.post(name: .highMemoryUsage, object: nil)
            }
        }
    }
    
    func monitorMemoryContinuously() {
        Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in
            Task {
                await self?.checkMemoryUsage()
            }
        }
    }
}

extension Notification.Name {
    static let highMemoryUsage = Notification.Name("highMemoryUsage")
}
```

### Background Task Management

```swift
// Services/BackgroundTaskManager.swift
import BackgroundTasks
import UIKit

class BackgroundTaskManager {
    static let shared = BackgroundTaskManager()
    
    private let refreshTaskIdentifier = "com.app.refresh"
    private let processingTaskIdentifier = "com.app.processing"
    
    func registerTasks() {
        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: refreshTaskIdentifier,
            using: nil
        ) { task in
            self.handleAppRefresh(task: task as! BGAppRefreshTask)
        }
        
        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: processingTaskIdentifier,
            using: nil
        ) { task in
            self.handleProcessing(task: task as! BGProcessingTask)
        }
    }
    
    func scheduleAppRefresh() {
        let request = BGAppRefreshTaskRequest(identifier: refreshTaskIdentifier)
        request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60)
        
        do {
            try BGTaskScheduler.shared.submit(request)
        } catch {
            print("Could not schedule app refresh: \(error)")
        }
    }
    
    func scheduleProcessing() {
        let request = BGProcessingTaskRequest(identifier: processingTaskIdentifier)
        request.requiresNetworkConnectivity = true
        request.requiresExternalPower = false
        
        do {
            try BGTaskScheduler.shared.submit(request)
        } catch {
            print("Could not schedule processing: \(error)")
        }
    }
    
    private func handleAppRefresh(task: BGAppRefreshTask) {
        scheduleAppRefresh()
        
        let operation = RefreshOperation()
        task.expirationHandler = {
            operation.cancel()
        }
        
        operation.completionBlock = {
            task.setTaskCompleted(success: !operation.isCancelled)
        }
        
        OperationQueue.main.addOperation(operation)
    }
    
    private func handleProcessing(task: BGProcessingTask) {
        scheduleProcessing()
        
        let operation = ProcessingOperation()
        task.expirationHandler = {
            operation.cancel()
        }
        
        operation.completionBlock = {
            task.setTaskCompleted(success: !operation.isCancelled)
        }
        
        OperationQueue.main.addOperation(operation)
    }
}
```

## Security Considerations

### Keychain Services

```swift
// Services/KeychainService.swift
import Security

class KeychainService {
    static let shared = KeychainService()
    
    func save(key: String, value: String) throws {
        guard let data = value.data(using: .utf8) else {
            throw KeychainError.encodingFailed
        }
        
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
        ]
        
        SecItemDelete(query as CFDictionary)
        
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status)
        }
    }
    
    func save(key: String, data: Data) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
        ]
        
        SecItemDelete(query as CFDictionary)
        
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status)
        }
    }
    
    func retrieve(key: String) throws -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne,
        ]
        
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        guard status == errSecSuccess, let data = result as? Data else {
            if status == errSecItemNotFound {
                return nil
            }
            throw KeychainError.retrieveFailed(status)
        }
        
        return String(data: data, encoding: .utf8)
    }
    
    func delete(key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
        ]
        
        let status = SecItemDelete(query as CFDictionary)
        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.deleteFailed(status)
        }
    }
}

enum KeychainError: Error {
    case encodingFailed
    case saveFailed(OSStatus)
    case retrieveFailed(OSStatus)
    case deleteFailed(OSStatus)
}
```

### App Transport Security

```swift
// Info.plist configuration
// ATS (App Transport Security) settings
/*
 <key>NSAppTransportSecurity</key>
 <dict>
     <key>NSAllowsArbitraryLoads</key>
     <false/>
     <key>NSExceptionDomains</key>
     <dict>
         <key>api.example.com</key>
         <dict>
             <key>NSExceptionRequiresForwardSecrecy</key>
             <true/>
             <key>NSIncludesSubdomains</key>
             <true/>
             <key>NSExceptionRequiresCertificateTransparency</key>
             <true/>
         </dict>
     </dict>
 </dict>
 */
```

## Troubleshooting Guide

### Common Issues

#### Issue: SwiftData Migration

```swift
// Utils/MigrationHandler.swift
import SwiftData

struct MigrationHandler {
    static func handleMigration() {
        do {
            let config = ModelConfiguration(isStoredInMemoryOnly: false)
            let container = try ModelContainer(
                for: Item.self,
                configurations: config
            )
            
            // Check if migration is needed
            let description = container.managedObjectModel
            print("Model description: \(description)")
            
        } catch {
            print("Migration error: \(error)")
        }
    }
}
```

#### Issue: Combine Memory Leaks

```swift
// Utils/CombineMemoryLeakDetector.swift
import Combine

class CombineMemoryLeakDetector {
    static let shared = CombineMemoryLeakDetector()
    
    private var cancellables = Set<AnyCancellable>()
    
    func track<T: AnyObject>(_ object: T, name: String) {
        let pointer = Unmanaged.passUnretained(object).toOpaque()
        
        Just(object)
            .sink { _ in }
            .store(in: &cancellables)
        
        print("Tracking object: \(name) at \(pointer)")
    }
    
    func detectLeaks() {
        print("Active subscriptions: \(cancellables.count)")
    }
}
```

## API Reference

### SwiftUI View Modifiers

```swift
// Custom View Modifiers
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(color: .black.opacity(0.1), radius: 4, x: 0, y: 2)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }
}

// Usage
CardView()
    .cardStyle()
```

### Navigation

```swift
// Navigation with types
enum NavigationRoute: Hashable {
    case detail(Item)
    case settings
    case profile
}

struct ContentView: View {
    @State private var path = NavigationPath()
    
    var body: some View {
        NavigationStack(path: $path) {
            List {
                NavigationLink(value: NavigationRoute.settings) {
                    Text("Settings")
                }
            }
            .navigationDestination(for: NavigationRoute.self) { route in
                switch route {
                case .detail(let item):
                    ItemDetailView(item: item)
                case .settings:
                    SettingsView()
                case .profile:
                    ProfileView()
                }
            }
        }
    }
}
```

## Data Models

### Domain Models

```swift
// Models/Item.swift
import Foundation

struct Item: Identifiable, Codable, Hashable {
    let id: UUID
    let name: String
    let description: String
    let price: Double
    let imageUrl: URL?
    let category: String
    let createdAt: Date
    let updatedAt: Date
    
    init(
        id: UUID = UUID(),
        name: String,
        description: String,
        price: Double,
        imageUrl: URL? = nil,
        category: String,
        createdAt: Date = Date(),
        updatedAt: Date = Date()
    ) {
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.imageUrl = imageUrl
        self.category = category
        self.createdAt = createdAt
        self.updatedAt = updatedAt
    }
}

// API Response
struct ItemResponse: Codable {
    let id: String
    let name: String
    let description: String
    let price: Double
    let imageUrl: String
    let category: String
    let createdAt: String
    let updatedAt: String
}

extension ItemResponse {
    func toDomain() -> Item {
        let dateFormatter = ISO8601DateFormatter()
        
        return Item(
            id: UUID(uuidString: id) ?? UUID(),
            name: name,
            description: description,
            price: price,
            imageUrl: URL(string: imageUrl),
            category: category,
            createdAt: dateFormatter.date(from: createdAt) ?? Date(),
            updatedAt: dateFormatter.date(from: updatedAt) ?? Date()
        )
    }
}
```

## Deployment Guide

### App Store Submission

```swift
// Scripts/validate_app.sh
#!/bin/bash
echo "Validating app..."
xcodebuild -exportArchive \
    -archivePath "build/MyApp.xcarchive" \
    -exportOptionsPlist "ExportOptions.plist" \
    -exportPath "build/export"

echo "Uploading to App Store..."
xcrun altool --upload-app \
    --type ios \
    --file "build/export/MyApp.ipa" \
    --username "your-apple-id@example.com" \
    --password "@keychain:AC_PASSWORD"
```

### CI/CD Configuration

```yaml
# .github/workflows/ios.yml
name: iOS CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: macos-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Select Xcode
      run: sudo xcode-select -s /Applications/Xcode.app
    
    - name: Install dependencies
      run: |
        brew install swiftlint
        bundle install
    
    - name: Build
      run: |
        xcodebuild build \
          -scheme "MyApp" \
          -destination "platform=iOS Simulator,name=iPhone 15" \
          CODE_SIGNING_ALLOWED=NO
    
    - name: Test
      run: |
        xcodebuild test \
          -scheme "MyApp" \
          -destination "platform=iOS Simulator,name=iPhone 15" \
          CODE_SIGNING_ALLOWED=NO
```

## Monitoring & Observability

### Crash Reporting

```swift
// Services/CrashReportingService.swift
import FirebaseCrashlytics

class CrashReportingService {
    static let shared = CrashReportingService()
    
    func logError(_ error: Error, context: [String: Any]? = nil) {
        Crashlytics.crashlytics().record(error: error)
        
        if let context = context {
            for (key, value) in context {
                Crashlytics.crashlytics().setCustomValue(value, forKey: key)
            }
        }
    }
    
    func logMessage(_ message: String) {
        Crashlytics.crashlytics().log(message)
    }
    
    func setUserID(_ userID: String) {
        Crashlytics.crashlytics().setUserID(userID)
    }
    
    func setCustomValue(_ value: Any, forKey key: String) {
        Crashlytics.crashlytics().setCustomValue(value, forKey: key)
    }
}
```

### Performance Monitoring

```swift
// Services/PerformanceMonitoring.swift
import FirebasePerformance

class PerformanceMonitoring {
    static let shared = PerformanceMonitoring()
    
    func startTrace(name: String) -> Trace? {
        let trace = Performance.startTrace(name: name)
        return trace
    }
    
    func stopTrace(_ trace: Trace?) {
        trace?.stop()
    }
    
    func logNetworkRequest(url: String, method: String) {
        guard let requestURL = URL(string: url) else { return }
        
        let metric = Performance.networkTrace(request: URLRequest(url: requestURL))
        metric.start()
        
        // After request completes
        metric.stop()
    }
}
```

## Testing Strategy

### Unit Tests

```swift
// Tests/ViewModelTests/ItemListViewModelTests.swift
import XCTest
import Combine

@MainActor
final class ItemListViewModelTests: XCTestCase {
    var viewModel: ItemListViewModel!
    var mockRepository: MockItemRepository!
    var cancellables: Set<AnyCancellable>!
    
    override func setUp() {
        super.setUp()
        mockRepository = MockItemRepository()
        viewModel = ItemListViewModel(repository: mockRepository)
        cancellables = []
    }
    
    override func tearDown() {
        viewModel = nil
        mockRepository = nil
        cancellables = nil
        super.tearDown()
    }
    
    func testLoadItemsSuccess() async {
        // Given
        let expectedItems = [
            Item(id: UUID(), name: "Test Item", description: "Description", price: 9.99, category: "Test")
        ]
        mockRepository.itemsToReturn = expectedItems
        
        // When
        await viewModel.loadItems()
        
        // Then
        XCTAssertEqual(viewModel.items.count, 1)
        XCTAssertEqual(viewModel.items.first?.name, "Test Item")
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNil(viewModel.error)
    }
    
    func testLoadItemsFailure() async {
        // Given
        mockRepository.errorToThrow = TestError.networkError
        
        // When
        await viewModel.loadItems()
        
        // Then
        XCTAssertTrue(viewModel.items.isEmpty)
        XCTAssertNotNil(viewModel.error)
        XCTAssertFalse(viewModel.isLoading)
    }
}

enum TestError: Error {
    case networkError
}

class MockItemRepository: ItemRepository {
    var itemsToReturn: [Item] = []
    var errorToThrow: Error?
    
    func fetchItems() async throws -> [Item] {
        if let error = errorToThrow {
            throw error
        }
        return itemsToReturn
    }
    
    func deleteItem(_ item: Item) async throws {
        if let error = errorToThrow {
            throw error
        }
    }
}
```

### UI Tests

```swift
// UITests/ItemListUITests.swift
import XCTest

final class ItemListUITests: XCTestCase {
    let app = XCUIApplication()
    
    override func setUpWithError() throws {
        continueAfterFailure = false
        app.launch()
    }
    
    func testItemListDisplays() throws {
        // Then
        let table = app.tables.firstMatch
        XCTAssertTrue(table.exists)
    }
    
    func testTapItemNavigatesToDetail() throws {
        // When
        let firstItem = app.cells.firstMatch
        firstItem.tap()
        
        // Then
        let backButton = app.navigationBars.buttons.firstMatch
        XCTAssertTrue(backButton.exists)
    }
    
    func testPullToRefresh() throws {
        // When
        let table = app.tables.firstMatch
        table.swipeDown()
        
        // Then
        let refreshIndicator = table.activityIndicators.firstMatch
        XCTAssertTrue(refreshIndicator.exists)
    }
}
```

## Versioning & Migration

### App Versioning

```swift
// VersionManager.swift
import Foundation

struct AppVersion {
    let major: Int
    let minor: Int
    let patch: Int
    
    var description: String {
        "\(major).\(minor).\(patch)"
    }
    
    static let current: AppVersion = {
        guard let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String,
              let versionNumbers = version.split(separator: ".").compactMap({ Int($0) }),
              versionNumbers.count >= 3 else {
            return AppVersion(major: 1, minor: 0, patch: 0)
        }
        
        return AppVersion(
            major: versionNumbers[0],
            minor: versionNumbers[1],
            patch: versionNumbers[2]
        )
    }()
}

// Usage
let currentVersion = AppVersion.current
print("App version: \(currentVersion.description)")
```

### API Versioning

```swift
// Services/APIClient.swift
import Foundation

enum APIVersion: String {
    case v1 = "v1"
    case v2 = "v2"
}

class APIClient {
    static let shared = APIClient()
    
    private let baseURL = "https://api.example.com"
    private var apiVersion: APIVersion = .v2
    
    func setAPIVersion(_ version: APIVersion) {
        self.apiVersion = version
    }
    
    func request<T: Decodable>(
        path: String,
        method: String = "GET",
        body: Data? = nil
    ) async throws -> T {
        let url = URL(string: "\(baseURL)/\(apiVersion.rawValue)\(path)")!
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.httpBody = body
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(T.self, from: data)
    }
}
```

## Glossary

### iOS Development Terms

| Term | Definition |
|------|------------|
| **SwiftUI** | Apple's declarative UI framework |
| **Combine** | Reactive programming framework |
| **SwiftData** | Modern data persistence framework |
| **Core Data** | Apple's object graph and persistence framework |
| **TCA** | The Composable Architecture |
| **NavigationStack** | Modern navigation container |
| **@StateObject** | Observable object lifecycle manager |
| **@ObservedObject** | Observable object reference |
| **@State** | Local view state |
| **@Environment** | Environment values provider |

## Changelog

### Version 2.0.0 (2024-01-15)
- Added SwiftData support
- Implemented TCA architecture
- Enhanced Swift concurrency
- Added WidgetKit support

### Version 1.5.0 (2023-10-01)
- Added SwiftUI enhancements
- Implemented Combine pipelines
- Enhanced Core Data
- Added CloudKit integration

### Version 1.4.0 (2023-07-15)
- Added NavigationStack
- Implemented async/await
- Enhanced accessibility
- Added HealthKit

### Version 1.3.0 (2023-04-01)
- Added SwiftUI basics
- Implemented MVVM
- Enhanced testing
- Added networking

### Version 1.2.0 (2023-01-15)
- Added basic iOS
- Implemented UIKit
- Added Core Data
- Enhanced documentation

### Version 1.1.0 (2022-10-01)
- Added Swift basics
- Implemented basic UI
- Added networking
- Enhanced UI

### Version 1.0.0 (2022-07-15)
- Initial release
- Basic iOS development
- SwiftUI support
- Basic functionality

## Contributing Guidelines

### Development Setup

```bash
# Clone repository
git clone https://github.com/company/ios-app.git
cd ios-app

# Open in Xcode
open MyApp.xcodeproj

# Install dependencies
bundle install

# Build project
xcodebuild build -scheme "MyApp"

# Run tests
xcodebuild test -scheme "MyApp" -destination "platform=iOS Simulator,name=iPhone 15"
```

### Code Standards

- Follow Swift style guide
- Use meaningful variable names
- Write unit tests for ViewModels
- Write UI tests for SwiftUI views
- Implement accessibility
- Follow Apple's Human Interface Guidelines

## License

MIT License

Copyright (c) 2024 iOS Development Contributors

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
