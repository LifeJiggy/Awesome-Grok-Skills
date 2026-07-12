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
