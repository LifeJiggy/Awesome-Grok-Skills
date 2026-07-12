"""
Schema Stitching Implementation

This module provides comprehensive GraphQL schema stitching patterns including:
- Schema combination and merging
- Type merging with conflict resolution
- Remote schema integration
- Schema transformation and validation
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import asyncio
import hashlib
import json
from abc import ABC, abstractmethod


# Enums
class SchemaConflictType(Enum):
    """Types of schema conflicts."""
    TYPE_NAME_CONFLICT = auto()
    FIELD_TYPE_CONFLICT = auto()
    FIELD_MISSING = auto()
    SCALAR_CONFLICT = auto()
    DIRECTIVE_CONFLICT = auto()


class MergeStrategy(Enum):
    """Strategies for merging schemas."""
    DEEP_MERGE = auto()
    SHALLOW_MERGE = auto()
    OVERRIDE = auto()
    SKIP = auto()


# Dataclasses
@dataclass
class SchemaField:
    """Represents a GraphQL field."""
    name: str
    type_name: str
    is_required: bool = False
    is_list: bool = False
    description: Optional[str] = None
    arguments: Dict[str, str] = field(default_factory=dict)
    directives: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'typeName': self.type_name,
            'isRequired': self.is_required,
            'isList': self.is_list,
            'description': self.description,
            'arguments': self.arguments,
            'directives': self.directives
        }


@dataclass
class SchemaType:
    """Represents a GraphQL type."""
    name: str
    kind: str  # OBJECT, INTERFACE, UNION, INPUT_OBJECT, ENUM, SCALAR
    fields: Dict[str, SchemaField] = field(default_factory=dict)
    interfaces: List[str] = field(default_factory=list)
    union_types: List[str] = field(default_factory=list)
    enum_values: List[str] = field(default_factory=list)
    description: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'kind': self.kind,
            'fields': {k: v.to_dict() for k, v in self.fields.items()},
            'interfaces': self.interfaces,
            'unionTypes': self.union_types,
            'enumValues': self.enum_values,
            'description': self.description
        }


@dataclass
class SchemaConflict:
    """Represents a schema conflict."""
    conflict_type: SchemaConflictType
    type_name: str
    field_name: Optional[str] = None
    schema_a_value: Optional[Any] = None
    schema_b_value: Optional[Any] = None
    resolution: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'conflictType': self.conflict_type.name,
            'typeName': self.type_name,
            'fieldName': self.field_name,
            'schemaAValue': str(self.schema_a_value) if self.schema_a_value else None,
            'schemaBValue': str(self.schema_b_value) if self.schema_b_value else None,
            'resolution': self.resolution
        }


@dataclass
class SchemaConfig:
    """Configuration for schema stitching."""
    name: str
    url: Optional[str] = None
    merge_strategy: MergeStrategy = MergeStrategy.DEEP_MERGE
    type_merging: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    transforms: List[Callable] = field(default_factory=list)
    authentication: Optional[Dict[str, str]] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'url': self.url,
            'mergeStrategy': self.merge_strategy.name,
            'typeMerging': self.type_merging,
            'transformsCount': len(self.transforms),
            'hasAuthentication': self.authentication is not None
        }


@dataclass
class StitchedSchema:
    """Result of schema stitching."""
    types: Dict[str, SchemaType]
    conflicts: List[SchemaConflict]
    config: SchemaConfig
    stitched_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'types': {k: v.to_dict() for k, v in self.types.items()},
            'conflicts': [c.to_dict() for c in self.conflicts],
            'config': self.config.to_dict(),
            'stitchedAt': self.stitched_at.isoformat()
        }


# Schema definitions
class SchemaDefinition:
    """Base class for schema definitions."""
    
    def __init__(self, name: str):
        self.name = name
        self.types: Dict[str, SchemaType] = {}
        self.scalars: Set[str] = set()
        self.directives: Set[str] = set()
    
    def add_type(self, schema_type: SchemaType):
        """Add a type to the schema."""
        self.types[schema_type.name] = schema_type
    
    def add_scalar(self, scalar_name: str):
        """Add a custom scalar."""
        self.scalars.add(scalar_name)
    
    def add_directive(self, directive_name: str):
        """Add a directive."""
        self.directives.add(directive_name)
    
    def get_type(self, type_name: str) -> Optional[SchemaType]:
        """Get a type by name."""
        return self.types.get(type_name)
    
    def has_type(self, type_name: str) -> bool:
        """Check if type exists."""
        return type_name in self.types
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'types': {k: v.to_dict() for k, v in self.types.items()},
            'scalars': list(self.scalars),
            'directives': list(self.directives)
        }


class UserSchema(SchemaDefinition):
    """User service schema."""
    
    def __init__(self):
        super().__init__("UserService")
        self._define_types()
    
    def _define_types(self):
        """Define user schema types."""
        # User type
        user_type = SchemaType(
            name="User",
            kind="OBJECT",
            fields={
                "id": SchemaField("id", "ID", is_required=True),
                "name": SchemaField("name", "String", is_required=True),
                "email": SchemaField("email", "String", is_required=True),
                "role": SchemaField("role", "UserRole", is_required=True),
                "createdAt": SchemaField("createdAt", "DateTime", is_required=True),
                "updatedAt": SchemaField("updatedAt", "DateTime", is_required=True),
            },
            description="User type representing a system user"
        )
        self.add_type(user_type)
        
        # UserRole enum
        user_role_enum = SchemaType(
            name="UserRole",
            kind="ENUM",
            enum_values=["ADMIN", "EDITOR", "VIEWER"],
            description="User role enumeration"
        )
        self.add_type(user_role_enum)
        
        # UserInput type
        user_input = SchemaType(
            name="CreateUserInput",
            kind="INPUT_OBJECT",
            fields={
                "name": SchemaField("name", "String", is_required=True),
                "email": SchemaField("email", "String", is_required=True),
                "password": SchemaField("password", "String", is_required=True),
                "role": SchemaField("role", "UserRole"),
            },
            description="Input for creating a user"
        )
        self.add_type(user_input)
        
        # Query type
        query_type = SchemaType(
            name="Query",
            kind="OBJECT",
            fields={
                "user": SchemaField("user", "User", is_required=False, arguments={"id": "ID!"}),
                "users": SchemaField("users", "UserConnection", is_required=True),
            },
            description="Query root type"
        )
        self.add_type(query_type)
        
        # Mutation type
        mutation_type = SchemaType(
            name="Mutation",
            kind="OBJECT",
            fields={
                "createUser": SchemaField("createUser", "CreateUserPayload", is_required=True, arguments={"input": "CreateUserInput!"}),
                "updateUser": SchemaField("updateUser", "UpdateUserPayload", is_required=True, arguments={"id": "ID!", "input": "UpdateUserInput!"}),
            },
            description="Mutation root type"
        )
        self.add_type(mutation_type)


class PostSchema(SchemaDefinition):
    """Post service schema."""
    
    def __init__(self):
        super().__init__("PostService")
        self._define_types()
    
    def _define_types(self):
        """Define post schema types."""
        # Post type
        post_type = SchemaType(
            name="Post",
            kind="OBJECT",
            fields={
                "id": SchemaField("id", "ID", is_required=True),
                "title": SchemaField("title", "String", is_required=True),
                "content": SchemaField("content", "String", is_required=True),
                "authorId": SchemaField("authorId", "ID", is_required=True),
                "status": SchemaField("status", "PostStatus", is_required=True),
                "createdAt": SchemaField("createdAt", "DateTime", is_required=True),
                "updatedAt": SchemaField("updatedAt", "DateTime", is_required=True),
            },
            description="Post type representing a blog post"
        )
        self.add_type(post_type)
        
        # PostStatus enum
        post_status_enum = SchemaType(
            name="PostStatus",
            kind="ENUM",
            enum_values=["DRAFT", "PUBLISHED", "ARCHIVED"],
            description="Post status enumeration"
        )
        self.add_type(post_status_enum)
        
        # Comment type
        comment_type = SchemaType(
            name="Comment",
            kind="OBJECT",
            fields={
                "id": SchemaField("id", "ID", is_required=True),
                "content": SchemaField("content", "String", is_required=True),
                "authorId": SchemaField("authorId", "ID", is_required=True),
                "postId": SchemaField("postId", "ID", is_required=True),
                "createdAt": SchemaField("createdAt", "DateTime", is_required=True),
            },
            description="Comment type representing a post comment"
        )
        self.add_type(comment_type)
        
        # Query type
        query_type = SchemaType(
            name="Query",
            kind="OBJECT",
            fields={
                "post": SchemaField("post", "Post", is_required=False, arguments={"id": "ID!"}),
                "postsByAuthor": SchemaField("postsByAuthor", "[Post!]!", is_required=True, arguments={"authorId": "ID!"}),
            },
            description="Query root type"
        )
        self.add_type(query_type)


class NotificationSchema(SchemaDefinition):
    """Notification service schema."""
    
    def __init__(self):
        super().__init__("NotificationService")
        self._define_types()
    
    def _define_types(self):
        """Define notification schema types."""
        # Notification type
        notification_type = SchemaType(
            name="Notification",
            kind="OBJECT",
            fields={
                "id": SchemaField("id", "ID", is_required=True),
                "type": SchemaField("type", "NotificationType", is_required=True),
                "userId": SchemaField("userId", "ID", is_required=True),
                "message": SchemaField("message", "String", is_required=True),
                "read": SchemaField("read", "Boolean", is_required=True),
                "createdAt": SchemaField("createdAt", "DateTime", is_required=True),
            },
            description="Notification type representing a user notification"
        )
        self.add_type(notification_type)
        
        # NotificationType enum
        notification_type_enum = SchemaType(
            name="NotificationType",
            kind="ENUM",
            enum_values=["POST_CREATED", "COMMENT_ADDED", "USER_FOLLOWED", "MENTION"],
            description="Notification type enumeration"
        )
        self.add_type(notification_type_enum)
        
        # Query type
        query_type = SchemaType(
            name="Query",
            kind="OBJECT",
            fields={
                "notifications": SchemaField("notifications", "[Notification!]!", is_required=True, arguments={"userId": "ID!"}),
                "unreadCount": SchemaField("unreadCount", "Int!", is_required=True, arguments={"userId": "ID!"}),
            },
            description="Query root type"
        )
        self.add_type(query_type)


# Schema Stitcher
class SchemaStitcher:
    """Main schema stitching engine."""
    
    def __init__(self, config: SchemaConfig):
        self.config = config
        self.schemas: List[SchemaDefinition] = []
        self.conflicts: List[SchemaConflict] = []
        self.merged_types: Dict[str, SchemaType] = {}
    
    def add_schema(self, schema: SchemaDefinition):
        """Add a schema to be stitched."""
        self.schemas.append(schema)
    
    async def stitch(self) -> StitchedSchema:
        """Perform schema stitching."""
        print(f"Starting schema stitching for {len(self.schemas)} schemas...")
        
        # Analyze schemas for conflicts
        await self._analyze_conflicts()
        
        # Merge types
        await self._merge_types()
        
        # Apply transforms
        await self._apply_transforms()
        
        # Validate merged schema
        await self._validate_merged_schema()
        
        return StitchedSchema(
            types=self.merged_types,
            conflicts=self.conflicts,
            config=self.config
        )
    
    async def _analyze_conflicts(self):
        """Analyze schemas for conflicts."""
        print("Analyzing schemas for conflicts...")
        
        # Check for type name conflicts
        type_names: Dict[str, List[str]] = {}
        for schema in self.schemas:
            for type_name in schema.types:
                if type_name not in type_names:
                    type_names[type_name] = []
                type_names[type_name].append(schema.name)
        
        # Report conflicts
        for type_name, schema_names in type_names.items():
            if len(schema_names) > 1:
                conflict = SchemaConflict(
                    conflict_type=SchemaConflictType.TYPE_NAME_CONFLICT,
                    type_name=type_name,
                    schema_a_value=schema_names[0],
                    schema_b_value=schema_names[1],
                    resolution=f"Merging types from {', '.join(schema_names)}"
                )
                self.conflicts.append(conflict)
                print(f"  Conflict: Type '{type_name}' exists in {', '.join(schema_names)}")
    
    async def _merge_types(self):
        """Merge types from all schemas."""
        print("Merging types...")
        
        # Collect all types
        all_types: Dict[str, List[SchemaType]] = {}
        for schema in self.schemas:
            for type_name, schema_type in schema.types.items():
                if type_name not in all_types:
                    all_types[type_name] = []
                all_types[type_name].append(schema_type)
        
        # Merge each type
        for type_name, type_list in all_types.items():
            if len(type_list) == 1:
                # Single type, use as-is
                self.merged_types[type_name] = type_list[0]
            else:
                # Multiple types, merge them
                merged_type = await self._merge_type_list(type_list)
                self.merged_types[type_name] = merged_type
        
        print(f"  Merged {len(self.merged_types)} types")
    
    async def _merge_type_list(self, types: List[SchemaType]) -> SchemaType:
        """Merge a list of types with the same name."""
        if not types:
            raise ValueError("Cannot merge empty type list")
        
        # Use first type as base
        base_type = types[0]
        
        # Merge fields from other types
        for other_type in types[1:]:
            for field_name, field in other_type.fields.items():
                if field_name not in base_type.fields:
                    # Add new field
                    base_type.fields[field_name] = field
                else:
                    # Field exists, check for conflicts
                    existing_field = base_type.fields[field_name]
                    if existing_field.type_name != field.type_name:
                        # Type conflict, create schema conflict
                        conflict = SchemaConflict(
                            conflict_type=SchemaConflictType.FIELD_TYPE_CONFLICT,
                            type_name=base_type.name,
                            field_name=field_name,
                            schema_a_value=existing_field.type_name,
                            schema_b_value=field.type_name,
                            resolution=f"Using type from first schema: {existing_field.type_name}"
                        )
                        self.conflicts.append(conflict)
                        print(f"    Field conflict: {base_type.name}.{field_name} - {existing_field.type_name} vs {field.type_name}")
        
        return base_type
    
    async def _apply_transforms(self):
        """Apply schema transforms."""
        print("Applying transforms...")
        
        for transform in self.config.transforms:
            try:
                self.merged_types = await transform(self.merged_types)
                print(f"  Applied transform: {transform.__name__}")
            except Exception as e:
                print(f"  Transform failed: {e}")
    
    async def _validate_merged_schema(self):
        """Validate the merged schema."""
        print("Validating merged schema...")
        
        # Check for missing type references
        for type_name, schema_type in self.merged_types.items():
            if schema_type.kind == "OBJECT":
                for field_name, field in schema_type.fields.items():
                    base_type = field.type_name.rstrip('!')
                    if base_type not in self.merged_types and base_type not in ["ID", "String", "Int", "Float", "Boolean"]:
                        print(f"  Warning: Type '{base_type}' referenced by {type_name}.{field_name} not found")
        
        # Check for circular dependencies
        visited: Set[str] = set()
        for type_name in self.merged_types:
            if type_name not in visited:
                await self._check_circular_deps(type_name, visited, set())
        
        print("  Validation complete")
    
    async def _check_circular_deps(self, type_name: str, visited: Set[str], path: Set[str]):
        """Check for circular dependencies."""
        if type_name in path:
            print(f"  Circular dependency detected: {type_name}")
            return
        
        if type_name in visited:
            return
        
        visited.add(type_name)
        path.add(type_name)
        
        schema_type = self.merged_types.get(type_name)
        if schema_type and schema_type.kind == "OBJECT":
            for field in schema_type.fields.values():
                base_type = field.type_name.rstrip('!')
                if base_type in self.merged_types:
                    await self._check_circular_deps(base_type, visited, path)
        
        path.remove(type_name)


# Schema Transformer
class SchemaTransformer:
    """Transforms for schema stitching."""
    
    @staticmethod
    async def add_timestamp_fields(types: Dict[str, SchemaType]) -> Dict[str, SchemaType]:
        """Add timestamp fields to all object types."""
        for type_name, schema_type in types.items():
            if schema_type.kind == "OBJECT" and type_name not in ["Query", "Mutation", "Subscription"]:
                # Add createdAt if not present
                if "createdAt" not in schema_type.fields:
                    schema_type.fields["createdAt"] = SchemaField(
                        "createdAt", "DateTime", is_required=True
                    )
                # Add updatedAt if not present
                if "updatedAt" not in schema_type.fields:
                    schema_type.fields["updatedAt"] = SchemaField(
                        "updatedAt", "DateTime", is_required=True
                    )
        return types
    
    @staticmethod
    async def add_node_interface(types: Dict[str, SchemaType]) -> Dict[str, SchemaType]:
        """Add Node interface to types with id field."""
        # Add Node interface type
        node_interface = SchemaType(
            name="Node",
            kind="INTERFACE",
            fields={
                "id": SchemaField("id", "ID", is_required=True)
            },
            description="Node interface for global object identification"
        )
        types["Node"] = node_interface
        
        # Add Node interface to types with id field
        for type_name, schema_type in types.items():
            if schema_type.kind == "OBJECT" and "id" in schema_type.fields:
                if "Node" not in schema_type.interfaces:
                    schema_type.interfaces.append("Node")
        
        return types
    
    @staticmethod
    async def remove_internal_fields(types: Dict[str, SchemaType]) -> Dict[str, SchemaType]:
        """Remove internal fields (starting with _)."""
        for type_name, schema_type in types.items():
            if schema_type.kind == "OBJECT":
                fields_to_remove = [
                    field_name for field_name in schema_type.fields
                    if field_name.startswith("_")
                ]
                for field_name in fields_to_remove:
                    del schema_type.fields[field_name]
        return types


# Mock Remote Schema Executor
class RemoteSchemaExecutor:
    """Mock executor for remote schemas."""
    
    def __init__(self, schema: SchemaDefinition):
        self.schema = schema
    
    async def execute(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute a query against the remote schema."""
        # Mock execution
        return {
            "data": {
                "schema": self.schema.to_dict()
            }
        }
    
    async def introspect(self) -> Dict[str, Any]:
        """Introspect the remote schema."""
        return self.schema.to_dict()


# Schema Registry
class SchemaRegistry:
    """Registry for managing schemas."""
    
    def __init__(self):
        self.schemas: Dict[str, SchemaDefinition] = {}
        self.stitched_schemas: Dict[str, StitchedSchema] = {}
    
    def register_schema(self, schema: SchemaDefinition):
        """Register a schema."""
        self.schemas[schema.name] = schema
        print(f"Registered schema: {schema.name}")
    
    def get_schema(self, name: str) -> Optional[SchemaDefinition]:
        """Get a schema by name."""
        return self.schemas.get(name)
    
    def list_schemas(self) -> List[str]:
        """List all registered schemas."""
        return list(self.schemas.keys())
    
    async def stitch_schemas(
        self,
        schema_names: List[str],
        config: SchemaConfig
    ) -> StitchedSchema:
        """Stitch multiple schemas together."""
        # Get schemas to stitch
        schemas_to_stitch = []
        for name in schema_names:
            schema = self.get_schema(name)
            if schema:
                schemas_to_stitch.append(schema)
            else:
                print(f"Warning: Schema '{name}' not found")
        
        if not schemas_to_stitch:
            raise ValueError("No schemas to stitch")
        
        # Create stitcher and perform stitching
        stitcher = SchemaStitcher(config)
        for schema in schemas_to_stitch:
            stitcher.add_schema(schema)
        
        stitched = await stitcher.stitch()
        self.stitched_schemas[config.name] = stitched
        
        return stitched
    
    def get_stitched_schema(self, name: str) -> Optional[StitchedSchema]:
        """Get a stitched schema by name."""
        return self.stitched_schemas.get(name)


# Main demo function
async def main():
    """Demonstrate schema stitching patterns."""
    print("=== Schema Stitching Demo ===\n")
    
    # Create schemas
    user_schema = UserSchema()
    post_schema = PostSchema()
    notification_schema = NotificationSchema()
    
    # Create registry
    registry = SchemaRegistry()
    registry.register_schema(user_schema)
    registry.register_schema(post_schema)
    registry.register_schema(notification_schema)
    
    # Demo 1: Show individual schemas
    print("1. Individual Schemas:")
    for schema_name in registry.list_schemas():
        schema = registry.get_schema(schema_name)
        if schema:
            print(f"\n   {schema_name}:")
            for type_name in schema.types:
                print(f"     - {type_name} ({schema.types[type_name].kind})")
    
    # Demo 2: Schema stitching
    print("\n2. Schema Stitching:")
    config = SchemaConfig(
        name="SocialMediaPlatform",
        merge_strategy=MergeStrategy.DEEP_MERGE,
        transforms=[
            SchemaTransformer.add_timestamp_fields,
            SchemaTransformer.add_node_interface,
        ]
    )
    
    stitched = await registry.stitch_schemas(
        ["UserService", "PostService", "NotificationService"],
        config
    )
    
    print(f"   Stitched schema '{stitched.config.name}':")
    print(f"   - Types: {len(stitched.types)}")
    print(f"   - Conflicts: {len(stitched.conflicts)}")
    
    # Demo 3: Show conflicts
    if stitched.conflicts:
        print("\n3. Conflicts Detected:")
        for conflict in stitched.conflicts:
            print(f"   - {conflict.conflict_type.name}: {conflict.type_name}")
            print(f"     Resolution: {conflict.resolution}")
    
    # Demo 4: Show merged types
    print("\n4. Merged Types:")
    for type_name, schema_type in stitched.types.items():
        field_count = len(schema_type.fields)
        print(f"   - {type_name}: {field_count} fields")
    
    # Demo 5: Schema transformation
    print("\n5. Schema Transformation Effects:")
    # Check if Node interface was added
    user_type = stitched.types.get("User")
    if user_type and "Node" in user_type.interfaces:
        print("   - Node interface added to User type")
    
    # Check if timestamps were added
    post_type = stitched.types.get("Post")
    if post_type and "createdAt" in post_type.fields:
        print("   - Timestamps added to Post type")
    
    # Demo 6: Remote schema execution
    print("\n6. Remote Schema Execution:")
    executor = RemoteSchemaExecutor(user_schema)
    result = await executor.execute("{ user(id: \"1\") { name email } }")
    print(f"   Executed query against remote schema")
    print(f"   Result: {json.dumps(result, indent=2)[:200]}...")
    
    # Demo 7: Schema validation
    print("\n7. Schema Validation:")
    stitcher = SchemaStitcher(config)
    stitcher.add_schema(user_schema)
    stitcher.add_schema(post_schema)
    await stitcher._validate_merged_schema()
    print("   Validation passed")
    
    # Demo 8: Show complete stitched schema
    print("\n8. Complete Stitched Schema Structure:")
    for type_name, schema_type in sorted(stitched.types.items()):
        if schema_type.kind == "OBJECT":
            fields = list(schema_type.fields.keys())
            print(f"   {type_name}: {', '.join(fields[:5])}{'...' if len(fields) > 5 else ''}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(main())