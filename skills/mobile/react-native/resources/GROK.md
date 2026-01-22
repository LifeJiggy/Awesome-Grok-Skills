# React Native

## Overview

React Native enables cross-platform mobile application development using React and JavaScript, allowing developers to build native mobile apps for iOS and Android from a single codebase. This skill covers component development, navigation, state management, native module integration, and platform-specific considerations. React Native bridges JavaScript code to native platform APIs, delivering near-native performance with web development productivity.

## Core Capabilities

React components render native UI elements using JSX syntax with props, state, and lifecycle methods. React Navigation provides routing and navigation patterns for stack, tab, and drawer navigation. State management solutions including Redux, Redux Toolkit, and React Query manage application data and server state. Native modules enable access to platform-specific APIs not available through the React Native framework.

Expo provides a managed workflow simplifying development, building, and deployment. Reanimated enables high-performance animations and gestures. Testing frameworks including Jest and React Native Testing Library support unit and integration testing. CodePush enables over-the-air updates without app store review cycles.

## Usage Examples

```python
from react_native import ReactNative

app = ReactNative()

app.create_project(
    name="MyMobileApp",
    template="blank",
    typescript=True
)

app.setup_expo(sdk_version="49")

component = app.create_component(
    name="TaskList",
    component_type="functional",
    props=["tasks", "onTaskPress"]
)

app.setup_react_navigation(navigator_type="stack")

app.add_screen(
    name="Home",
    component="HomeScreen",
    options={"title": "Home"}
)

app.add_screen(
    name="Details",
    component="DetailsScreen",
    options={"title": "Details"}
)

app.setup_redux_toolkit()

app.setup_react_query()

app.configure_animations(animation_type="reanimated")

app.setup_testing(testing_framework="jest")

app.setup_push_notifications(platform="both")

app.setup_offline_support(solution="async_storage")
```

## Best Practices

Use functional components with hooks instead of class components for better performance and readability. Optimize list rendering with FlatList and proper key usage to avoid unnecessary re-renders. Memoize callbacks and expensive computations with useMemo and useCallback. Handle loading and error states consistently across the application.

Test components thoroughly with React Native Testing Library. Use platform-specific code when necessary for platform-native behavior. Implement proper error boundaries to catch and handle rendering errors. Monitor performance with Flipper and React DevTools.

## Related Skills

- iOS Development (iOS-specific development)
- Android Development (Android-specific development)
- JavaScript Development (language fundamentals)
- Redux (state management)

## Use Cases

Enterprise mobile apps leverage React Native for cross-platform consistency and reduced development costs. Consumer apps use React Native for rapid iteration and over-the-air updates. Internal tools benefit from code sharing between mobile and web applications. Startups choose React Native for MVP development with option to go native later.
