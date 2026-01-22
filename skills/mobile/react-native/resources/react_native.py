class ReactNative:
    def __init__(self):
        self.project = None
        self.components = {}
        self.navigation = None

    def create_project(self, name, template="blank", typescript=True):
        self.project = {
            "name": name,
            "template": template,
            "typescript": typescript,
            "expo": True,
            "dependencies": [],
            "dev_dependencies": []
        }
        return self

    def setup_expo(self, sdk_version="49"):
        self.project["expo"] = True
        self.project["expo_sdk_version"] = sdk_version
        self.project["permissions"] = []
        return self

    def setup_react_native_cli(self, arch="new"):
        self.project["expo"] = False
        self.project["architecture"] = arch
        return self

    def create_component(self, name, component_type="functional", props=None):
        component = {
            "name": name,
            "type": component_type,
            "props": props or [],
            "state": None,
            "hooks": [],
            "styles": {}
        }
        self.components[name] = component
        return component

    def setup_react_navigation(self, navigator_type="stack"):
        self.navigation = {
            "type": navigator_type,
            "screens": [],
            "config": {
                "initial_route_name": "Home",
                "header_mode": "float"
            }
        }
        return self

    def add_screen(self, name, component, options=None):
        if self.navigation:
            self.navigation["screens"].append({
                "name": name,
                "component": component,
                "options": options or {}
            })
        return self

    def setup_state_management(self, solution="redux"):
        self.state_management = {
            "solution": solution,
            "store": None,
            "actions": [],
            "reducers": [],
            "selectors": []
        }
        return self

    def setup_redux_toolkit(self):
        self.state_management = {
            "solution": "redux_toolkit",
            "slices": [],
            "store_config": {},
            "middleware": ["thunk"]
        }
        return self

    def setup_react_query(self, config=None):
        self.state_management = {
            "solution": "react_query",
            "queries": [],
            "mutations": [],
            "config": config or {"defaultOptions": {}}
        }
        return self

    def setup_Context(self, context_name, provider_config=None):
        return {
            "context_name": context_name,
            "provider": provider_config,
            "consumers": [],
            "initial_value": None
        }

    def configure_animations(self, animation_type="reanimated"):
        return {
            "library": animation_type,
            "transitions": [],
            "gestures": []
        }

    def setup_testing(self, testing_framework="jest"):
        return {
            "framework": testing_framework,
            "libraries": ["@testing-library/react-native"],
            "coverage_threshold": 80
        }

    def configure_native_modules(self, modules=None):
        return {
            "ios": {"cocoapods": True, "permissions": []},
            "android": {"gradle": True, "permissions": []},
            "modules": modules or []
        }

    def setup_offline_support(self, solution="async_storage"):
        return {
            "storage": solution,
            "sync_strategy": "last_write_wins",
            "conflict_resolution": "server_wins"
        }

    def create_api_service(self, base_url, endpoints=None):
        return {
            "base_url": base_url,
            "endpoints": endpoints or [],
            "interceptors": [],
            "error_handling": {},
            "authentication": None
        }

    def setup_graphql(self, endpoint, client_config=None):
        return {
            "endpoint": endpoint,
            "libraries": ["@apollo/client", "graphql"],
            "config": client_config or {}
        }

    def configure_hermes(self, enabled=True):
        return {
            "enabled": enabled,
            "compiler_config": {},
            "build_config": {}
        }

    def setup_crashlytics(self):
        return {
            "ios": {"crashlytics": True, "debug_symbols": True},
            "android": {"crashlytics": True, "ndk": True}
        }

    def create_hook(self, hook_name, dependencies=None):
        return {
            "name": hook_name,
            "dependencies": dependencies or [],
            "implementation": None
        }

    def setup_push_notifications(self, platform="both"):
        return {
            "platform": platform,
            "service": "expo_notifications",
            "permissions": [],
            "handlers": []
        }
