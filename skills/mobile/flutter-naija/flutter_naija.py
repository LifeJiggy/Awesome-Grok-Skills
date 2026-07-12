"""
Flutter Naija Module
Part of the mobile skill domain.

Provides Flutter project scaffolding, Dart code generation, pubspec management,
and cross-platform deployment utilities with Nigerian tech ecosystem integrations.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set


class FlutterChannel(Enum):
    STABLE = "stable"
    BETA = "beta"
    MASTER = "master"


class TargetPlatform(Enum):
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"
    MACOS = "macos"
    LINUX = "linux"
    WINDOWS = "windows"


class StateManager(Enum):
    RIVERPOD = "riverpod"
    BLOC = "bloc"
    GETX = "getx"
    PROVIDER = "provider"
    NONE = "none"


class StorageType(Enum):
    HIVE = "hive"
    ISAR = "isar"
    DRIFT = "drift"
    SHARED_PREFS = "shared_preferences"
    NONE = "none"


class PaymentGateway(Enum):
    FLUTTERWAVE = "flutterwave"
    PAYSTACK = "paystack"
    MONNIFY = "monnify"
    OANDO = "oando"
    NONE = "none"


@dataclass
class FlutterDependency:
    name: str
    version: str
    description: str = ""
    is_dev: bool = False

    def to_pubspec_entry(self) -> str:
        indent = "  "
        dev_prefix = "  " if not self.is_dev else "  "
        return f'{indent}{self.name}:\n{indent}  {self.version}'


@dataclass
class FlutterConfig:
    name: str
    package_name: str
    description: str = "A Flutter application"
    version: str = "1.0.0+1"
    min_sdk: int = 21
    target_sdk: int = 34
    flutter_channel: FlutterChannel = FlutterChannel.STABLE
    platforms: List[TargetPlatform] = field(
        default_factory=lambda: [TargetPlatform.ANDROID, TargetPlatform.IOS]
    )
    state_manager: StateManager = StateManager.RIVERPOD
    storage: StorageType = StorageType.HIVE
    payment_gateway: PaymentGateway = PaymentGateway.FLUTTERWAVE
    dependencies: List[FlutterDependency] = field(default_factory=list)
    use_codegen: bool = True
    use_freezed: bool = True
    use_go_router: bool = True
    offline_first: bool = True


class PubspecGenerator:
    """Generates pubspec.yaml for Flutter projects."""

    def __init__(self, config: FlutterConfig):
        self.config = config

    def generate(self) -> str:
        deps = self._get_dependencies()
        dev_deps = self._get_dev_dependencies()

        return f"""name: {self.config.name}
description: {self.config.description}
publish_to: 'none'
version: {self.config.version}

environment:
  sdk: '>=3.2.0 <4.0.0'
  flutter: '>=3.16.0'

dependencies:
  flutter:
    sdk: flutter
{deps}
  cupertino_icons: ^1.0.8

dev_dependencies:
  flutter_test:
    sdk: flutter
{dev_deps}
  flutter_lints: ^3.0.1

flutter:
  uses-material-design: true

  assets:
    - assets/images/
    - assets/fonts/
"""

    def _get_dependencies(self) -> str:
        lines = []
        if self.config.state_manager == StateManager.RIVERPOD:
            lines.append("  flutter_riverpod: ^2.4.9")
            lines.append("  riverpod_annotation: ^2.3.3")
        elif self.config.state_manager == StateManager.BLOC:
            lines.append("  flutter_bloc: ^8.1.3")
            lines.append("  equatable: ^2.0.5")
        elif self.config.state_manager == StateManager.GETX:
            lines.append("  get: ^4.6.6")

        if self.config.use_go_router:
            lines.append("  go_router: ^13.0.0")

        if self.config.storage == StorageType.HIVE:
            lines.append("  hive_flutter: ^1.1.0")
        elif self.config.storage == StorageType.ISAR:
            lines.append("  isar: ^3.1.0+1")
            lines.append("  isar_flutter_libs: ^3.1.0+1")
        elif self.config.storage == StorageType.DRIFT:
            lines.append("  drift: ^2.14.1")
            lines.append("  sqlite3_flutter_libs: ^0.5.17")

        if self.config.payment_gateway == PaymentGateway.FLUTTERWAVE:
            lines.append("  flutterwave_flutter_pay: ^1.0.0")
        elif self.config.payment_gateway == PaymentGateway.PAYSTACK:
            lines.append("  flutter_paystack: ^1.0.7")

        if self.config.offline_first:
            lines.append("  connectivity_plus: ^5.0.2")
            lines.append("  cached_network_image: ^3.3.0")

        for dep in self.config.dependencies:
            lines.append(f"  {dep.name}: {dep.version}")

        return "\n".join(lines)

    def _get_dev_dependencies(self) -> str:
        lines = [
            "  build_runner: ^2.4.7",
            "  json_serializable: ^6.7.1",
        ]
        if self.config.use_codegen:
            lines.append("  riverpod_generator: ^2.3.9")
            lines.append("  riverpod_lint: ^2.3.7")
        if self.config.use_freezed:
            lines.append("  freezed_annotation: ^2.4.1")
            lines.append("  freezed: ^2.4.6")
        if self.config.storage == StorageType.ISAR:
            lines.append("  isar_generator: ^3.1.0+1")
        if self.config.storage == StorageType.DRIFT:
            lines.append("  drift_dev: ^2.14.1")
            lines.append("  build_runner: ^2.4.7")

        return "\n".join(lines)


class DartCodeGenerator:
    """Generates Dart code for Flutter projects."""

    def __init__(self, config: FlutterConfig):
        self.config = config

    def generate_riverpod_notifier(self, name: str, fields: List[str]) -> str:
        field_params = ", ".join(f"required this.{f}" for f in fields)
        field_decls = "\n".join(f"  final String {f};" for f in fields)

        return f"""import 'package:freezed_annotation/freezed_annotation.dart';

part '{name}.freezed.dart';
part '{name}.g.dart';

@freezed
class {name.capitalize()} with _${name.capitalize()} {{
  const factory {name.capitalize()}({{
    required String id,
{field_decls}
    @Default(false) bool isDeleted,
    @Default(DateTime.now()) DateTime createdAt,
  }}) = _{name.capitalize()};

  factory {name.capitalize()}.fromJson(Map<String, dynamic> json) =>
      _${name.capitalize()}FromJson(json);
}}
"""

    def generate_riverpod_provider(self, model_name: str) -> str:
        return f"""import 'package:flutter_riverpod/flutter_riverpod.dart';

final {model_name}_repository_provider = Provider<{model_name.capitalize()}Repository>(
  (ref) => throw UnimplementedError('Override in main'),
);

class {model_name.capitalize()}Repository {{
  final {model_name.capitalize()}LocalDataSource _local;
  final {model_name.capitalize()}RemoteDataSource _remote;

  {model_name.capitalize()}Repository({{
    required {model_name.capitalize()}LocalDataSource local,
    required {model_name.capitalize()}RemoteDataSource remote,
  }}) : _local = local,
       _remote = remote;

  Future<List<{model_name.capitalize()}>> getAll() async {{
    try {{
      final items = await _remote.getAll();
      await _local.cacheAll(items);
      return items;
    }} catch (_) {{
      return _local.getAll();
    }}
  }}

  Future<{model_name.capitalize()}> getById(String id) async {{
    return await _remote.getById(id) ?? await _local.getById(id);
  }}

  Future<void> save({model_name.capitalize()} item) async {{
    await _remote.save(item);
    await _local.save(item);
  }}

  Future<void> delete(String id) async {{
    await _remote.delete(id);
    await _local.delete(id);
  }}
}}
"""

    def generate_flutter_widget(self, name: str, model_name: str) -> str:
        return f"""import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class {name}Screen extends ConsumerWidget {{
  const {name}Screen({{super.key}});

  @override
  Widget build(BuildContext context, WidgetRef ref) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('{name}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => _showAddDialog(context, ref),
          ),
        ],
      ),
      body: _buildBody(context, ref),
    );
  }}

  Widget _buildBody(BuildContext context, WidgetRef ref) {{
    final itemsAsync = ref.watch({model_name}_list_provider);

    return itemsAsync.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (e, s) => Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 48, color: Colors.red),
            const SizedBox(height: 16),
            Text(e.toString(), textAlign: TextAlign.center),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => ref.invalidate({model_name}_list_provider),
              child: const Text('Retry'),
            ),
          ],
        ),
      ),
      data: (items) => items.isEmpty
          ? const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.inbox_outlined, size: 48, color: Colors.grey),
                  SizedBox(height: 16),
                  Text('No items yet'),
                ],
              ),
            )
          : RefreshIndicator(
              onRefresh: () async {{
                ref.invalidate({model_name}_list_provider);
              }},
              child: ListView.separated(
                itemCount: items.length,
                separatorBuilder: (_, __) => const Divider(height: 1),
                itemBuilder: (ctx, i) => ListTile(
                  title: Text(items[i].name),
                  subtitle: Text(items[i].createdAt.toIso8601String()),
                  trailing: IconButton(
                    icon: const Icon(Icons.delete_outline),
                    onPressed: () => _confirmDelete(context, ref, items[i].id),
                  ),
                ),
              ),
            ),
    );
  }}

  void _showAddDialog(BuildContext context, WidgetRef ref) {{
    final controller = TextEditingController();
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Add {model_name.capitalize()}'),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(hintText: 'Name'),
          autofocus: true,
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancel'),
          ),
          FilledButton(
            onPressed: () {{
              if (controller.text.isNotEmpty) {{
                ref.read({model_name}_list_provider.notifier).add(
                  name: controller.text,
                );
                Navigator.pop(ctx);
              }}
            }},
            child: const Text('Add'),
          ),
        ],
      ),
    );
  }}

  void _confirmDelete(BuildContext context, WidgetRef ref, String id) {{
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Delete?'),
        content: const Text('This action cannot be undone.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancel'),
          ),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () {{
              ref.read({model_name}_list_provider.notifier).delete(id);
              Navigator.pop(ctx);
            }},
            child: const Text('Delete'),
          ),
        ],
      ),
    );
  }}
}}
"""

    def generate_flutter_payment_service(self) -> str:
        return f"""import 'dart:convert';
import 'package:http/http.dart' as http;

enum PaymentStatus {{ success, failed, pending, cancelled }}

class PaymentResult {{
  final PaymentStatus status;
  final String? transactionId;
  final String? message;
  final Map<String, dynamic>? data;

  const PaymentResult({{
    required this.status,
    this.transactionId,
    this.message,
    this.data,
  }});
}}

class PaymentService {{
  final String apiKey;
  final String secretKey;
  final bool isTestMode;

  PaymentService({{
    required this.apiKey,
    required this.secretKey,
    this.isTestMode = true,
  }});

  String get _baseUrl => isTestMode
      ? 'https://api.flutterwave.com/v3'
      : 'https://api.flutterwave.com/v3';

  Future<PaymentResult> initializePayment({{
    required double amount,
    required String currency,
    required String email,
    required String name,
    String? phone,
    Map<String, dynamic>? metadata,
  }}) async {{
    final body = {{
      'tx_ref': 'tx_\${{DateTime.now().millisecondsSinceEpoch}}',
      'amount': amount.toString(),
      'currency': currency,
      'email': email,
      'name': name,
      if (phone != null) 'phone_number': phone,
      'meta': metadata,
    }};

    final response = await http.post(
      Uri.parse('\$_baseUrl/payments'),
      headers: {{
        'Authorization': 'Bearer \$secretKey',
        'Content-Type': 'application/json',
      }},
      body: jsonEncode(body),
    );

    if (response.statusCode == 200) {{
      final data = jsonDecode(response.body);
      if (data['status'] == 'success') {{
        return const PaymentResult(
          status: PaymentStatus.success,
          message: 'Payment initialized',
        );
      }}
    }}

    return const PaymentResult(
      status: PaymentStatus.failed,
      message: 'Payment initialization failed',
    );
  }}

  Future<PaymentResult> verifyPayment(String transactionId) async {{
    final response = await http.get(
      Uri.parse('\$_baseUrl/transactions/\$transactionId/verify'),
      headers: {{'Authorization': 'Bearer \$secretKey'}},
    );

    if (response.statusCode == 200) {{
      final data = jsonDecode(response.body);
      return PaymentResult(
        status: data['data']['status'] == 'successful'
            ? PaymentStatus.success
            : PaymentStatus.failed,
        transactionId: transactionId,
        data: data['data'],
      );
    }}

    return const PaymentResult(
      status: PaymentStatus.failed,
      message: 'Verification failed',
    );
  }}
}}
"""


class FlutterProjectScaffolder:
    """Creates Flutter project directory structure."""

    def __init__(self, config: FlutterConfig, base_path: Path):
        self.config = config
        self.base_path = base_path
        self.pubspec_gen = PubspecGenerator(config)
        self.dart_gen = DartCodeGenerator(config)

    def get_directory_structure(self) -> List[str]:
        return [
            f"lib/{self.config.name}/",
            f"lib/{self.config.name}/core/",
            f"lib/{self.config.name}/core/theme/",
            f"lib/{self.config.name}/core/router/",
            f"lib/{self.config.name}/core/network/",
            f"lib/{self.config.name}/core/storage/",
            f"lib/{self.config.name}/features/",
            f"lib/{self.config.name}/features/home/",
            f"lib/{self.config.name}/features/home/presentation/",
            f"lib/{self.config.name}/features/home/data/",
            f"lib/{self.config.name}/features/home/domain/",
            "assets/images/",
            "assets/fonts/",
            "test/",
            "integration_test/",
        ]

    def get_summary(self) -> Dict[str, Any]:
        return {
            "name": self.config.name,
            "package_name": self.config.package_name,
            "flutter_channel": self.config.flutter_channel.value,
            "platforms": [p.value for p in self.config.platforms],
            "state_manager": self.config.state_manager.value,
            "storage": self.config.storage.value,
            "payment_gateway": self.config.payment_gateway.value,
            "offline_first": self.config.offline_first,
            "use_codegen": self.config.use_codegen,
            "use_freezed": self.config.use_freezed,
            "use_go_router": self.config.use_go_router,
        }


def main():
    config = FlutterConfig(
        name="naija_app",
        package_name="com.naija.app",
        description="A Flutter app with Nigerian market integrations",
        state_manager=StateManager.RIVERPOD,
        storage=StorageType.HIVE,
        payment_gateway=PaymentGateway.FLUTTERWAVE,
        offline_first=True,
        use_codegen=True,
        use_freezed=True,
        dependencies=[
            FlutterDependency("dio", "^5.4.0", "HTTP client"),
            FlutterDependency("flutter_secure_storage", "^9.0.0", "Secure storage"),
        ],
    )

    print("=== Flutter Project Configuration ===")
    scaffolder = FlutterProjectScaffolder(config, Path("."))
    for key, value in scaffolder.get_summary().items():
        print(f"  {key}: {value}")

    print("\n=== pubspec.yaml ===")
    pubspec = PubspecGenerator(config)
    print(pubspec.generate()[:600] + "\n...")

    print("\n=== Freezed Model ===")
    dart_gen = DartCodeGenerator(config)
    print(dart_gen.generate_riverpod_notifier("item", ["name", "description"]))

    print("\n=== Flutter Widget ===")
    print(dart_gen.generate_flutter_widget("Items", "item")[:500] + "\n...")

    print("\n=== Payment Service ===")
    print(dart_gen.generate_flutter_payment_service()[:500] + "\n...")

    print("\n=== Directory Structure ===")
    for d in scaffolder.get_directory_structure():
        print(f"  {d}/")

    print("\nDone.")


if __name__ == "__main__":
    main()
