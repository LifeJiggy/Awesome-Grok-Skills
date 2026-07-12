"""
GraphQL API Design Implementation

This module provides comprehensive GraphQL API design patterns including:
- Schema design with type system
- Mutation patterns with input validation
- Cursor-based pagination
- N+1 query prevention with DataLoader
- Error handling patterns
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Generic, List, Optional, TypeVar, Union
from collections import defaultdict
import asyncio
import hashlib
import json


# Type variables for generic types
T = TypeVar('T')
Node = TypeVar('Node')


# Enums
class PostStatus(Enum):
    """Post status enumeration."""
    DRAFT = auto()
    PUBLISHED = auto()
    ARCHIVED = auto()
    DELETED = auto()


class UserRole(Enum):
    """User role enumeration."""
    ADMIN = auto()
    EDITOR = auto()
    VIEWER = auto()


class ErrorCode(Enum):
    """Error code enumeration for consistent error handling."""
    VALIDATION_ERROR = auto()
    AUTHENTICATION_ERROR = auto()
    AUTHORIZATION_ERROR = auto()
    NOT_FOUND = auto()
    CONFLICT = auto()
    INTERNAL_ERROR = auto()
    RATE_LIMIT_EXCEEDED = auto()


class SortDirection(Enum):
    """Sort direction enumeration."""
    ASC = auto()
    DESC = auto()


class UserSortField(Enum):
    """User sort field enumeration."""
    NAME = auto()
    EMAIL = auto()
    CREATED_AT = auto()
    UPDATED_AT = auto()


# Dataclasses
@dataclass
class UserError:
    """Error type for GraphQL mutations."""
    field: Optional[str]
    message: str
    code: ErrorCode
    details: Optional[dict] = None

    def to_dict(self) -> dict:
        """Convert error to dictionary."""
        return {
            'field': self.field,
            'message': self.message,
            'code': self.code.name,
            'details': self.details
        }


@dataclass
class PageInfo:
    """Page information for cursor-based pagination."""
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str] = None
    end_cursor: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'hasNextPage': self.has_next_page,
            'hasPreviousPage': self.has_previous_page,
            'startCursor': self.start_cursor,
            'endCursor': self.end_cursor
        }


@dataclass
class Edge(Generic[Node]):
    """Edge type for connections."""
    node: Node
    cursor: str

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'node': self.node,
            'cursor': self.cursor
        }


@dataclass
class Connection(Generic[Node]):
    """Connection type for pagination."""
    edges: List[Edge[Node]]
    page_info: PageInfo
    total_count: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'edges': [edge.to_dict() for edge in self.edges],
            'pageInfo': self.page_info.to_dict(),
            'totalCount': self.total_count
        }


@dataclass
class User:
    """User type."""
    id: str
    name: str
    email: str
    role: UserRole
    created_at: datetime
    updated_at: datetime
    posts: List['Post'] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role.name,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
        }


@dataclass
class Post:
    """Post type."""
    id: str
    title: str
    content: str
    author_id: str
    status: PostStatus
    created_at: datetime
    updated_at: datetime
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'authorId': self.author_id,
            'status': self.status.name,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
            'tags': self.tags
        }


# Input types
@dataclass
class CreateUserInput:
    """Input for creating a user."""
    name: str
    email: str
    password: str
    role: UserRole = UserRole.VIEWER

    def validate(self) -> List[UserError]:
        """Validate input."""
        errors = []
        if not self.name or len(self.name) < 2:
            errors.append(UserError(
                field='name',
                message='Name must be at least 2 characters',
                code=ErrorCode.VALIDATION_ERROR
            ))
        if '@' not in self.email:
            errors.append(UserError(
                field='email',
                message='Invalid email format',
                code=ErrorCode.VALIDATION_ERROR
            ))
        if len(self.password) < 8:
            errors.append(UserError(
                field='password',
                message='Password must be at least 8 characters',
                code=ErrorCode.VALIDATION_ERROR
            ))
        return errors


@dataclass
class UpdatePostInput:
    """Input for updating a post."""
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[PostStatus] = None
    tags: Optional[List[str]] = None

    def validate(self) -> List[UserError]:
        """Validate input."""
        errors = []
        if self.title is not None and len(self.title) < 3:
            errors.append(UserError(
                field='title',
                message='Title must be at least 3 characters',
                code=ErrorCode.VALIDATION_ERROR
            ))
        return errors


@dataclass
class UserFilter:
    """Filter for user queries."""
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
    created_after: Optional[datetime] = None


@dataclass
class UserSort:
    """Sort configuration for user queries."""
    field: UserSortField
    direction: SortDirection


# Payload types
@dataclass
class CreateUserPayload:
    """Payload for create user mutation."""
    user: Optional[User] = None
    errors: List[UserError] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'user': self.user.to_dict() if self.user else None,
            'errors': [error.to_dict() for error in self.errors]
        }


@dataclass
class UpdatePostPayload:
    """Payload for update post mutation."""
    post: Optional[Post] = None
    errors: List[UserError] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'post': self.post.to_dict() if self.post else None,
            'errors': [error.to_dict() for error in self.errors]
        }


# DataLoader implementation
class DataLoader(Generic[T]):
    """Generic DataLoader for batching and caching."""
    
    def __init__(self, batch_fn, max_batch_size: int = 100):
        self.batch_fn = batch_fn
        self.max_batch_size = max_batch_size
        self.cache: dict[str, T] = {}
        self.queue: List[str] = []
        self.callbacks: dict[str, list] = defaultdict(list)
    
    async def load(self, key: str) -> Optional[T]:
        """Load a single key."""
        if key in self.cache:
            return self.cache[key]
        
        # Create promise for this key
        future = asyncio.get_event_loop().create_future()
        self.callbacks[key].append(future)
        
        if key not in self.queue:
            self.queue.append(key)
            
            # Trigger batch if queue is full or on next tick
            if len(self.queue) >= self.max_batch_size:
                await self._dispatch_batch()
            else:
                asyncio.get_event_loop().call_soon(self._dispatch_batch_if_pending)
        
        return await future
    
    async def load_many(self, keys: List[str]) -> List[Optional[T]]:
        """Load multiple keys."""
        return await asyncio.gather(*[self.load(key) for key in keys])
    
    async def _dispatch_batch_if_pending(self):
        """Dispatch batch if there are pending keys."""
        if self.queue:
            await self._dispatch_batch()
    
    async def _dispatch_batch(self):
        """Dispatch the current batch."""
        if not self.queue:
            return
        
        keys_to_load = self.queue.copy()
        self.queue.clear()
        
        try:
            results = await self.batch_fn(keys_to_load)
            
            # Resolve promises
            for key, result in zip(keys_to_load, results):
                self.cache[key] = result
                for callback in self.callbacks[key]:
                    if not callback.done():
                        callback.set_result(result)
                self.callbacks[key].clear()
        
        except Exception as e:
            # Reject all promises
            for key in keys_to_load:
                for callback in self.callbacks[key]:
                    if not callback.done():
                        callback.set_exception(e)
                self.callbacks[key].clear()


# Database simulation
class MockDatabase:
    """Mock database for demonstration."""
    
    def __init__(self):
        self.users: dict[str, User] = {}
        self.posts: dict[str, Post] = {}
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize with sample data."""
        # Create users
        users = [
            User(
                id='1',
                name='Alice Johnson',
                email='alice@example.com',
                role=UserRole.ADMIN,
                created_at=datetime(2024, 1, 15),
                updated_at=datetime(2024, 6, 20)
            ),
            User(
                id='2',
                name='Bob Smith',
                email='bob@example.com',
                role=UserRole.EDITOR,
                created_at=datetime(2024, 2, 10),
                updated_at=datetime(2024, 7, 15)
            ),
            User(
                id='3',
                name='Charlie Brown',
                email='charlie@example.com',
                role=UserRole.VIEWER,
                created_at=datetime(2024, 3, 5),
                updated_at=datetime(2024, 8, 10)
            ),
        ]
        
        for user in users:
            self.users[user.id] = user
        
        # Create posts
        posts = [
            Post(
                id='1',
                title='Getting Started with GraphQL',
                content='GraphQL is a query language for APIs...',
                author_id='1',
                status=PostStatus.PUBLISHED,
                created_at=datetime(2024, 4, 1),
                updated_at=datetime(2024, 4, 15),
                tags=['graphql', 'tutorial']
            ),
            Post(
                id='2',
                title='Advanced Schema Design',
                content='Learn about advanced schema patterns...',
                author_id='1',
                status=PostStatus.PUBLISHED,
                created_at=datetime(2024, 5, 10),
                updated_at=datetime(2024, 5, 20),
                tags=['graphql', 'advanced']
            ),
            Post(
                id='3',
                title='Draft Post',
                content='This is a draft...',
                author_id='2',
                status=PostStatus.DRAFT,
                created_at=datetime(2024, 6, 1),
                updated_at=datetime(2024, 6, 5),
                tags=['draft']
            ),
        ]
        
        for post in posts:
            self.posts[post.id] = post
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)
    
    async def get_users_by_ids(self, user_ids: List[str]) -> List[User]:
        """Get multiple users by IDs."""
        return [self.users[uid] for uid in user_ids if uid in self.users]
    
    async def create_user(self, input_data: CreateUserInput) -> User:
        """Create a new user."""
        user_id = str(len(self.users) + 1)
        user = User(
            id=user_id,
            name=input_data.name,
            email=input_data.email,
            role=input_data.role,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.users[user_id] = user
        return user
    
    async def get_posts_by_author_id(self, author_id: str) -> List[Post]:
        """Get posts by author ID."""
        return [post for post in self.posts.values() if post.author_id == author_id]
    
    async def update_post(self, post_id: str, input_data: UpdatePostInput) -> Optional[Post]:
        """Update a post."""
        post = self.posts.get(post_id)
        if not post:
            return None
        
        if input_data.title is not None:
            post.title = input_data.title
        if input_data.content is not None:
            post.content = input_data.content
        if input_data.status is not None:
            post.status = input_data.status
        if input_data.tags is not None:
            post.tags = input_data.tags
        
        post.updated_at = datetime.now()
        return post


# GraphQL Resolvers
class GraphQLResolver:
    """GraphQL resolver implementation."""
    
    def __init__(self, db: MockDatabase):
        self.db = db
        self.user_loader = DataLoader(db.get_user)
        self.posts_by_author_loader = DataLoader(db.get_posts_by_author_id)
    
    async def resolve_user(self, user_id: str) -> Optional[User]:
        """Resolve a single user."""
        return await self.user_loader.load(user_id)
    
    async def resolve_users(
        self,
        first: Optional[int] = None,
        after: Optional[str] = None,
        last: Optional[int] = None,
        before: Optional[str] = None,
        filter_input: Optional[UserFilter] = None,
        sort: Optional[UserSort] = None
    ) -> Connection[User]:
        """Resolve users with pagination."""
        users = list(self.db.users.values())
        
        # Apply filters
        if filter_input:
            users = self._apply_user_filter(users, filter_input)
        
        # Apply sorting
        if sort:
            users = self._apply_user_sort(users, sort)
        
        # Apply cursor-based pagination
        edges, page_info = self._apply_pagination(
            users, first, after, last, before
        )
        
        return Connection(
            edges=edges,
            page_info=page_info,
            total_count=len(users)
        )
    
    async def resolve_user_posts(self, user: User) -> List[Post]:
        """Resolve posts for a user (N+1 prevention)."""
        return await self.posts_by_author_loader.load(user.id)
    
    async def create_user(self, input_data: CreateUserInput) -> CreateUserPayload:
        """Create a new user mutation."""
        # Validate input
        validation_errors = input_data.validate()
        if validation_errors:
            return CreateUserPayload(errors=validation_errors)
        
        # Check for email conflict
        existing_user = next(
            (u for u in self.db.users.values() if u.email == input_data.email),
            None
        )
        if existing_user:
            return CreateUserPayload(
                errors=[UserError(
                    field='email',
                    message='Email already exists',
                    code=ErrorCode.CONFLICT
                )]
            )
        
        # Create user
        user = await self.db.create_user(input_data)
        return CreateUserPayload(user=user)
    
    async def update_post(
        self,
        post_id: str,
        input_data: UpdatePostInput
    ) -> UpdatePostPayload:
        """Update a post mutation."""
        # Validate input
        validation_errors = input_data.validate()
        if validation_errors:
            return UpdatePostPayload(errors=validation_errors)
        
        # Check if post exists
        post = await self.db.update_post(post_id, input_data)
        if not post:
            return UpdatePostPayload(
                errors=[UserError(
                    field='post',
                    message='Post not found',
                    code=ErrorCode.NOT_FOUND
                )]
            )
        
        return UpdatePostPayload(post=post)
    
    def _apply_user_filter(
        self,
        users: List[User],
        filter_input: UserFilter
    ) -> List[User]:
        """Apply filter to users."""
        result = users
        
        if filter_input.name:
            result = [u for u in result if filter_input.name.lower() in u.name.lower()]
        
        if filter_input.email:
            result = [u for u in result if filter_input.email.lower() in u.email.lower()]
        
        if filter_input.role:
            result = [u for u in result if u.role == filter_input.role]
        
        if filter_input.created_after:
            result = [u for u in result if u.created_at >= filter_input.created_after]
        
        return result
    
    def _apply_user_sort(
        self,
        users: List[User],
        sort: UserSort
    ) -> List[User]:
        """Apply sorting to users."""
        sort_key = {
            UserSortField.NAME: lambda u: u.name,
            UserSortField.EMAIL: lambda u: u.email,
            UserSortField.CREATED_AT: lambda u: u.created_at,
            UserSortField.UPDATED_AT: lambda u: u.updated_at,
        }[sort.field]
        
        reverse = sort.direction == SortDirection.DESC
        return sorted(users, key=sort_key, reverse=reverse)
    
    def _apply_pagination(
        self,
        items: List[Any],
        first: Optional[int],
        after: Optional[str],
        last: Optional[int],
        before: Optional[str]
    ) -> tuple[List[Edge], PageInfo]:
        """Apply cursor-based pagination."""
        # Convert items to edges with cursors
        edges = []
        for i, item in enumerate(items):
            cursor = self._encode_cursor(str(i))
            edges.append(Edge(node=item, cursor=cursor))
        
        # Apply after cursor
        if after:
            after_index = self._decode_cursor(after)
            edges = [e for e in edges if self._decode_cursor(e.cursor) > after_index]
        
        # Apply before cursor
        if before:
            before_index = self._decode_cursor(before)
            edges = [e for e in edges if self._decode_cursor(e.cursor) < before_index]
        
        # Apply first limit
        if first is not None:
            edges = edges[:first]
        
        # Apply last limit
        if last is not None:
            edges = edges[-last:] if len(edges) > last else edges
        
        # Calculate page info
        has_next_page = len(edges) > 0 and edges[-1].cursor != self._encode_cursor(str(len(items) - 1))
        has_previous_page = len(edges) > 0 and edges[0].cursor != self._encode_cursor('0')
        
        page_info = PageInfo(
            has_next_page=has_next_page,
            has_previous_page=has_previous_page,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-1].cursor if edges else None
        )
        
        return edges, page_info
    
    def _encode_cursor(self, value: str) -> str:
        """Encode cursor value."""
        return hashlib.base64_64(value.encode()).decode()
    
    def _decode_cursor(self, cursor: str) -> int:
        """Decode cursor value."""
        return int(hashlib.base64_64decode(cursor.encode()).decode())


# Query complexity analyzer
class QueryComplexityAnalyzer:
    """Analyze query complexity to prevent abuse."""
    
    def __init__(self, max_complexity: int = 1000):
        self.max_complexity = max_complexity
        self.field_complexities: dict[str, int] = {
            'users': 10,
            'user': 5,
            'posts': 8,
            'post': 3,
            'comments': 6,
            'comment': 2,
        }
    
    def analyze(self, query: str) -> tuple[bool, int]:
        """Analyze query complexity."""
        # Simple complexity analysis (in real implementation, use AST)
        complexity = 0
        
        # Count field accesses
        for field, cost in self.field_complexities.items():
            complexity += query.lower().count(field) * cost
        
        # Add connection overhead
        if 'connection' in query.lower():
            complexity *= 2
        
        is_valid = complexity <= self.max_complexity
        return is_valid, complexity
    
    def get_max_complexity(self) -> int:
        """Get maximum allowed complexity."""
        return self.max_complexity


# Main demo function
async def main():
    """Demonstrate GraphQL API design patterns."""
    print("=== GraphQL API Design Demo ===\n")
    
    # Initialize database and resolver
    db = MockDatabase()
    resolver = GraphQLResolver(db)
    
    # Demo 1: Query users with pagination
    print("1. Query Users with Pagination:")
    connection = await resolver.resolve_users(first=2)
    print(f"   Total users: {connection.total_count}")
    print(f"   Has next page: {connection.page_info.has_next_page}")
    for edge in connection.edges:
        user = edge.node
        print(f"   - {user.name} ({user.email})")
    
    # Demo 2: Query with filters
    print("\n2. Query Users with Filter:")
    filter_input = UserFilter(role=UserRole.ADMIN)
    filtered_connection = await resolver.resolve_users(filter_input=filter_input)
    for edge in filtered_connection.edges:
        user = edge.node
        print(f"   - {user.name} (Role: {user.role.name})")
    
    # Demo 3: Create user mutation
    print("\n3. Create User Mutation:")
    create_input = CreateUserInput(
        name="Diana Prince",
        email="diana@example.com",
        password="securepass123",
        role=UserRole.EDITOR
    )
    create_result = await resolver.create_user(create_input)
    if create_result.user:
        print(f"   Created: {create_result.user.name}")
    if create_result.errors:
        for error in create_result.errors:
            print(f"   Error: {error.message}")
    
    # Demo 4: Update post mutation
    print("\n4. Update Post Mutation:")
    update_input = UpdatePostInput(
        title="Updated Title",
        status=PostStatus.PUBLISHED
    )
    update_result = await resolver.update_post("1", update_input)
    if update_result.post:
        print(f"   Updated: {update_result.post.title} - {update_result.post.status.name}")
    if update_result.errors:
        for error in update_result.errors:
            print(f"   Error: {error.message}")
    
    # Demo 5: N+1 prevention with DataLoader
    print("\n5. N+1 Prevention with DataLoader:")
    user = await resolver.resolve_user("1")
    if user:
        posts = await resolver.resolve_user_posts(user)
        print(f"   User: {user.name}")
        print(f"   Posts count: {len(posts)}")
        for post in posts:
            print(f"     - {post.title} ({post.status.name})")
    
    # Demo 6: Query complexity analysis
    print("\n6. Query Complexity Analysis:")
    analyzer = QueryComplexityAnalyzer(max_complexity=1000)
    test_query = """
    query {
        users(first: 10) {
            edges {
                node {
                    id
                    name
                    posts {
                        id
                        title
                        comments {
                            id
                            content
                        }
                    }
                }
            }
        }
    }
    """
    is_valid, complexity = analyzer.analyze(test_query)
    print(f"   Query valid: {is_valid}")
    print(f"   Complexity: {complexity}/{analyzer.get_max_complexity()}")
    
    # Demo 7: Error handling
    print("\n7. Error Handling:")
    invalid_input = CreateUserInput(
        name="",  # Invalid: too short
        email="invalid-email",  # Invalid: no @
        password="123"  # Invalid: too short
    )
    error_result = await resolver.create_user(invalid_input)
    if error_result.errors:
        for error in error_result.errors:
            print(f"   {error.field}: {error.message} ({error.code.name})")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(main())