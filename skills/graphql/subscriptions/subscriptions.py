"""
GraphQL Subscriptions Implementation

This module provides comprehensive GraphQL subscription patterns including:
- WebSocket transport and connection management
- Real-time update mechanisms
- Filtering and subscription management
- Scaling and horizontal deployment
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Set, Tuple, Union
import asyncio
import json
import hashlib
from abc import ABC, abstractmethod
from collections import defaultdict
import uuid


# Enums
class SubscriptionStatus(Enum):
    """Subscription connection status."""
    CONNECTING = auto()
    CONNECTED = auto()
    DISCONNECTING = auto()
    DISCONNECTED = auto()
    ERROR = auto()


class MessageType(Enum):
    """WebSocket message types."""
    CONNECTION_INIT = auto()
    CONNECTION_ACK = auto()
    CONNECTION_ERROR = auto()
    CONNECTION_TERMINATE = auto()
    START = auto()
    START_ACK = auto()
    STOP = auto()
    COMPLETE = auto()
    ERROR = auto()
    DATA = auto()
    PING = auto()
    PONG = auto()


class EventType(Enum):
    """Event types for subscriptions."""
    POST_CREATED = auto()
    POST_UPDATED = auto()
    POST_DELETED = auto()
    COMMENT_ADDED = auto()
    COMMENT_UPDATED = auto()
    USER_STATUS_CHANGED = auto()
    NOTIFICATION = auto()
    CUSTOM = auto()


# Dataclasses
@dataclass
class SubscriptionFilter:
    """Filter for subscription events."""
    field_name: str
    field_value: Any
    operator: str = "eq"  # eq, neq, gt, lt, in, contains

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'fieldName': self.field_name,
            'fieldValue': str(self.field_value),
            'operator': self.operator
        }


@dataclass
class SubscriptionOptions:
    """Options for subscription configuration."""
    filters: List[SubscriptionFilter] = field(default_factory=list)
    max_connections: int = 1000
    heartbeat_interval: int = 30
    connection_timeout: int = 60
    retry_attempts: int = 3
    retry_delay: int = 1000

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'filtersCount': len(self.filters),
            'maxConnections': self.max_connections,
            'heartbeatInterval': self.heartbeat_interval,
            'connectionTimeout': self.connection_timeout,
            'retryAttempts': self.retry_attempts,
            'retryDelay': self.retry_delay
        }


@dataclass
class Subscription:
    """Represents an active subscription."""
    id: str
    query: str
    variables: Dict[str, Any]
    options: SubscriptionOptions
    status: SubscriptionStatus = SubscriptionStatus.CONNECTING
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    client_id: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'query': self.query[:100] + '...' if len(self.query) > 100 else self.query,
            'variables': self.variables,
            'options': self.options.to_dict(),
            'status': self.status.name,
            'createdAt': self.created_at.isoformat(),
            'lastActivity': self.last_activity.isoformat(),
            'clientId': self.client_id
        }


@dataclass
class SubscriptionEvent:
    """Event for subscription delivery."""
    id: str
    type: EventType
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'type': self.type.name,
            'payload': self.payload,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


@dataclass
class WebSocketMessage:
    """WebSocket message format."""
    type: MessageType
    id: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        result = {'type': self.type.name}
        if self.id:
            result['id'] = self.id
        if self.payload:
            result['payload'] = self.payload
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WebSocketMessage':
        """Create from dictionary."""
        return cls(
            type=MessageType[data['type']],
            id=data.get('id'),
            payload=data.get('payload')
        )


@dataclass
class ConnectionMetrics:
    """Metrics for subscription connections."""
    total_connections: int = 0
    active_connections: int = 0
    total_messages: int = 0
    messages_per_second: float = 0.0
    average_latency: float = 0.0
    error_rate: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'totalConnections': self.total_connections,
            'activeConnections': self.active_connections,
            'totalMessages': self.total_messages,
            'messagesPerSecond': self.messages_per_second,
            'averageLatency': self.average_latency,
            'errorRate': self.error_rate,
            'lastUpdated': self.last_updated.isoformat()
        }


# Pub/Sub System
class PubSub:
    """Publish/Subscribe system for GraphQL subscriptions."""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.events: List[SubscriptionEvent] = []
        self.metrics = ConnectionMetrics()
    
    async def publish(self, event: SubscriptionEvent):
        """Publish an event to subscribers."""
        print(f"Publishing event: {event.type.name}")
        
        # Store event
        self.events.append(event)
        
        # Update metrics
        self.metrics.total_messages += 1
        
        # Notify subscribers
        topic = event.type.name
        for callback in self.subscribers.get(topic, []):
            try:
                await callback(event)
            except Exception as e:
                print(f"Error notifying subscriber: {e}")
    
    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to a topic."""
        print(f"Subscribing to: {topic}")
        self.subscribers[topic].append(callback)
    
    def unsubscribe(self, topic: str, callback: Callable):
        """Unsubscribe from a topic."""
        if topic in self.subscribers:
            self.subscribers[topic] = [
                cb for cb in self.subscribers[topic] if cb != callback
            ]
    
    def get_metrics(self) -> ConnectionMetrics:
        """Get pub/sub metrics."""
        return self.metrics


# Subscription Manager
class SubscriptionManager:
    """Manage GraphQL subscriptions."""
    
    def __init__(self, pubsub: PubSub):
        self.pubsub = pubsub
        self.subscriptions: Dict[str, Subscription] = {}
        self.connections: Dict[str, Dict[str, Any]] = {}
        self.metrics = ConnectionMetrics()
    
    async def create_subscription(
        self,
        query: str,
        variables: Dict[str, Any],
        options: Optional[SubscriptionOptions] = None,
        client_id: Optional[str] = None
    ) -> Subscription:
        """Create a new subscription."""
        subscription_id = str(uuid.uuid4())
        
        subscription = Subscription(
            id=subscription_id,
            query=query,
            variables=variables,
            options=options or SubscriptionOptions(),
            client_id=client_id
        )
        
        self.subscriptions[subscription_id] = subscription
        self.metrics.total_connections += 1
        self.metrics.active_connections += 1
        
        print(f"Created subscription: {subscription_id}")
        return subscription
    
    async def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancel a subscription."""
        if subscription_id in self.subscriptions:
            subscription = self.subscriptions[subscription_id]
            subscription.status = SubscriptionStatus.DISCONNECTED
            del self.subscriptions[subscription_id]
            self.metrics.active_connections -= 1
            
            print(f"Cancelled subscription: {subscription_id}")
            return True
        return False
    
    async def get_subscription(self, subscription_id: str) -> Optional[Subscription]:
        """Get a subscription by ID."""
        return self.subscriptions.get(subscription_id)
    
    async def list_subscriptions(self, client_id: Optional[str] = None) -> List[Subscription]:
        """List subscriptions, optionally filtered by client."""
        subscriptions = list(self.subscriptions.values())
        
        if client_id:
            subscriptions = [s for s in subscriptions if s.client_id == client_id]
        
        return subscriptions
    
    async def handle_event(self, event: SubscriptionEvent):
        """Handle an incoming event and notify relevant subscriptions."""
        print(f"Handling event: {event.type.name}")
        
        for subscription in self.subscriptions.values():
            if await self._should_notify(subscription, event):
                await self._notify_subscription(subscription, event)
    
    async def _should_notify(self, subscription: Subscription, event: SubscriptionEvent) -> bool:
        """Check if subscription should be notified of event."""
        # Check filters
        for filter_option in subscription.options.filters:
            if not self._matches_filter(event, filter_option):
                return False
        
        # Check query relevance (simplified)
        query_lower = subscription.query.lower()
        event_type = event.type.name.lower()
        
        return event_type in query_lower
    
    def _matches_filter(self, event: SubscriptionEvent, filter_option: SubscriptionFilter) -> bool:
        """Check if event matches filter."""
        event_value = event.payload.get(filter_option.field_name)
        
        if filter_option.operator == "eq":
            return event_value == filter_option.field_value
        elif filter_option.operator == "neq":
            return event_value != filter_option.field_value
        elif filter_option.operator == "gt":
            return event_value > filter_option.field_value
        elif filter_option.operator == "lt":
            return event_value < filter_option.field_value
        elif filter_option.operator == "in":
            return event_value in filter_option.field_value
        elif filter_option.operator == "contains":
            return filter_option.field_value in str(event_value)
        
        return False
    
    async def _notify_subscription(self, subscription: Subscription, event: SubscriptionEvent):
        """Notify a subscription of an event."""
        try:
            # Update subscription status
            subscription.status = SubscriptionStatus.CONNECTED
            subscription.last_activity = datetime.now()
            
            # Create response message
            message = WebSocketMessage(
                type=MessageType.DATA,
                id=subscription.id,
                payload={
                    'data': event.payload,
                    'extensions': {
                        'timestamp': event.timestamp.isoformat(),
                        'eventId': event.id
                    }
                }
            )
            
            # In real implementation, send via WebSocket
            print(f"  Notifying subscription {subscription.id}: {event.type.name}")
            
            # Update metrics
            self.metrics.total_messages += 1
            
        except Exception as e:
            print(f"  Error notifying subscription {subscription.id}: {e}")
            subscription.status = SubscriptionStatus.ERROR
    
    def get_metrics(self) -> ConnectionMetrics:
        """Get subscription manager metrics."""
        return self.metrics


# WebSocket Connection Manager
class WebSocketManager:
    """Manage WebSocket connections for subscriptions."""
    
    def __init__(self):
        self.connections: Dict[str, Dict[str, Any]] = {}
        self.heartbeat_interval: int = 30
        self.connection_timeout: int = 60
        self.metrics = ConnectionMetrics()
    
    async def handle_connection(self, connection_id: str, connection_params: Dict[str, Any]):
        """Handle new WebSocket connection."""
        print(f"New connection: {connection_id}")
        
        self.connections[connection_id] = {
            'id': connection_id,
            'params': connection_params,
            'status': SubscriptionStatus.CONNECTED,
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'subscriptions': []
        }
        
        self.metrics.total_connections += 1
        self.metrics.active_connections += 1
        
        # Send connection ack
        ack_message = WebSocketMessage(
            type=MessageType.CONNECTION_ACK,
            payload={'connectionId': connection_id}
        )
        
        print(f"  Sent connection ack: {connection_id}")
        return ack_message
    
    async def handle_disconnect(self, connection_id: str):
        """Handle WebSocket disconnection."""
        if connection_id in self.connections:
            connection = self.connections[connection_id]
            connection['status'] = SubscriptionStatus.DISCONNECTED
            
            # Cancel all subscriptions for this connection
            for subscription_id in connection.get('subscriptions', []):
                print(f"  Cancelling subscription: {subscription_id}")
            
            del self.connections[connection_id]
            self.metrics.active_connections -= 1
            
            print(f"Connection disconnected: {connection_id}")
    
    async def handle_message(self, connection_id: str, message: WebSocketMessage):
        """Handle incoming WebSocket message."""
        if connection_id not in self.connections:
            print(f"Unknown connection: {connection_id}")
            return
        
        connection = self.connections[connection_id]
        connection['last_activity'] = datetime.now()
        
        print(f"Message from {connection_id}: {message.type.name}")
        
        # Handle different message types
        if message.type == MessageType.START:
            await self._handle_start(connection_id, message)
        elif message.type == MessageType.STOP:
            await self._handle_stop(connection_id, message)
        elif message.type == MessageType.PING:
            await self._handle_ping(connection_id)
        elif message.type == MessageType.CONNECTION_TERMINATE:
            await self.handle_disconnect(connection_id)
    
    async def _handle_start(self, connection_id: str, message: WebSocketMessage):
        """Handle subscription start."""
        if not message.id or not message.payload:
            return
        
        subscription_id = message.id
        query = message.payload.get('query', '')
        variables = message.payload.get('variables', {})
        
        print(f"  Starting subscription: {subscription_id}")
        
        # Add subscription to connection
        connection = self.connections[connection_id]
        connection['subscriptions'].append(subscription_id)
        
        # Send start ack
        ack_message = WebSocketMessage(
            type=MessageType.START_ACK,
            id=subscription_id
        )
        
        print(f"  Sent start ack: {subscription_id}")
    
    async def _handle_stop(self, connection_id: str, message: WebSocketMessage):
        """Handle subscription stop."""
        if not message.id:
            return
        
        subscription_id = message.id
        
        print(f"  Stopping subscription: {subscription_id}")
        
        # Remove subscription from connection
        connection = self.connections[connection_id]
        if subscription_id in connection['subscriptions']:
            connection['subscriptions'].remove(subscription_id)
        
        # Send complete message
        complete_message = WebSocketMessage(
            type=MessageType.COMPLETE,
            id=subscription_id
        )
        
        print(f"  Sent complete: {subscription_id}")
    
    async def _handle_ping(self, connection_id: str):
        """Handle ping message."""
        pong_message = WebSocketMessage(type=MessageType.PONG)
        print(f"  Sent pong: {connection_id}")
        return pong_message
    
    async def heartbeat_check(self):
        """Check for dead connections."""
        now = datetime.now()
        dead_connections = []
        
        for connection_id, connection in self.connections.items():
            last_activity = connection['last_activity']
            elapsed = (now - last_activity).total_seconds()
            
            if elapsed > self.connection_timeout:
                dead_connections.append(connection_id)
        
        # Disconnect dead connections
        for connection_id in dead_connections:
            await self.handle_disconnect(connection_id)
            print(f"  Disconnected dead connection: {connection_id}")
    
    def get_metrics(self) -> ConnectionMetrics:
        """Get WebSocket manager metrics."""
        return self.metrics
    
    def get_connection_count(self) -> int:
        """Get number of active connections."""
        return len(self.connections)


# Subscription Client
class SubscriptionClient:
    """Client-side subscription manager."""
    
    def __init__(self, url: str):
        self.url = url
        self.subscriptions: Dict[str, Subscription] = {}
        self.connection_status: SubscriptionStatus = SubscriptionStatus.DISCONNECTED
        self.message_queue: List[WebSocketMessage] = []
        self.reconnect_attempts: int = 0
        self.max_reconnect_attempts: int = 5
    
    async def connect(self):
        """Connect to WebSocket server."""
        print(f"Connecting to: {self.url}")
        self.connection_status = SubscriptionStatus.CONNECTING
        
        # Simulate connection
        await asyncio.sleep(0.1)
        
        self.connection_status = SubscriptionStatus.CONNECTED
        print("Connected successfully")
        
        # Send connection init
        init_message = WebSocketMessage(
            type=MessageType.CONNECTION_INIT,
            payload={'authToken': 'mock-token'}
        )
        
        await self.send_message(init_message)
    
    async def disconnect(self):
        """Disconnect from WebSocket server."""
        print("Disconnecting...")
        self.connection_status = SubscriptionStatus.DISCONNECTING
        
        # Cancel all subscriptions
        for subscription_id in list(self.subscriptions.keys()):
            await self.unsubscribe(subscription_id)
        
        self.connection_status = SubscriptionStatus.DISCONNECTED
        print("Disconnected")
    
    async def subscribe(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        callback: Optional[Callable] = None
    ) -> str:
        """Subscribe to a GraphQL subscription."""
        subscription_id = str(uuid.uuid4())
        
        subscription = Subscription(
            id=subscription_id,
            query=query,
            variables=variables or {},
            options=SubscriptionOptions(),
            client_id="local"
        )
        
        self.subscriptions[subscription_id] = subscription
        
        # Send start message
        start_message = WebSocketMessage(
            type=MessageType.START,
            id=subscription_id,
            payload={
                'query': query,
                'variables': variables or {}
            }
        )
        
        await self.send_message(start_message)
        print(f"Subscribed: {subscription_id}")
        
        return subscription_id
    
    async def unsubscribe(self, subscription_id: str):
        """Unsubscribe from a subscription."""
        if subscription_id in self.subscriptions:
            del self.subscriptions[subscription_id]
            
            # Send stop message
            stop_message = WebSocketMessage(
                type=MessageType.STOP,
                id=subscription_id
            )
            
            await self.send_message(stop_message)
            print(f"Unsubscribed: {subscription_id}")
    
    async def send_message(self, message: WebSocketMessage):
        """Send a message to the server."""
        # In real implementation, send via WebSocket
        self.message_queue.append(message)
        print(f"  Sent: {message.type.name}")
    
    async def handle_message(self, message: WebSocketMessage):
        """Handle incoming message from server."""
        print(f"  Received: {message.type.name}")
        
        if message.type == MessageType.DATA:
            # Handle subscription data
            subscription_id = message.id
            if subscription_id in self.subscriptions:
                subscription = self.subscriptions[subscription_id]
                subscription.last_activity = datetime.now()
                
                # Process data
                data = message.payload.get('data') if message.payload else None
                print(f"    Data: {data}")
        
        elif message.type == MessageType.ERROR:
            # Handle error
            error = message.payload.get('message') if message.payload else 'Unknown error'
            print(f"    Error: {error}")
    
    def get_subscription_count(self) -> int:
        """Get number of active subscriptions."""
        return len(self.subscriptions)


# Scaling Manager
class ScalingManager:
    """Manage horizontal scaling for subscriptions."""
    
    def __init__(self):
        self.instances: List[Dict[str, Any]] = []
        self.load_balancer: Dict[str, Any] = {}
        self.metrics: Dict[str, Any] = {
            'total_instances': 0,
            'total_connections': 0,
            'messages_per_instance': 0
        }
    
    async def add_instance(self, instance_id: str, endpoint: str):
        """Add a new server instance."""
        instance = {
            'id': instance_id,
            'endpoint': endpoint,
            'connections': 0,
            'status': 'healthy',
            'created_at': datetime.now()
        }
        
        self.instances.append(instance)
        self.metrics['total_instances'] += 1
        
        print(f"Added instance: {instance_id}")
    
    async def remove_instance(self, instance_id: str):
        """Remove a server instance."""
        self.instances = [
            i for i in self.instances if i['id'] != instance_id
        ]
        self.metrics['total_instances'] -= 1
        
        print(f"Removed instance: {instance_id}")
    
    async def distribute_connection(self, connection_id: str) -> Dict[str, Any]:
        """Distribute a connection to an instance."""
        # Find least loaded instance
        if not self.instances:
            raise ValueError("No instances available")
        
        least_loaded = min(self.instances, key=lambda i: i['connections'])
        least_loaded['connections'] += 1
        self.metrics['total_connections'] += 1
        
        print(f"Distributed connection {connection_id} to instance {least_loaded['id']}")
        return least_loaded
    
    async def get_instance_metrics(self) -> List[Dict[str, Any]]:
        """Get metrics for all instances."""
        return [
            {
                'id': instance['id'],
                'connections': instance['connections'],
                'status': instance['status']
            }
            for instance in self.instances
        ]
    
    def get_total_connections(self) -> int:
        """Get total connections across all instances."""
        return sum(instance['connections'] for instance in self.instances)


# Event Filter
class EventFilter:
    """Filter events for subscriptions."""
    
    def __init__(self):
        self.filters: Dict[str, List[SubscriptionFilter]] = defaultdict(list)
    
    def add_filter(self, subscription_id: str, filter_option: SubscriptionFilter):
        """Add a filter for a subscription."""
        self.filters[subscription_id].append(filter_option)
    
    def remove_filter(self, subscription_id: str, field_name: str):
        """Remove a filter from a subscription."""
        if subscription_id in self.filters:
            self.filters[subscription_id] = [
                f for f in self.filters[subscription_id]
                if f.field_name != field_name
            ]
    
    def should_deliver(self, subscription_id: str, event: SubscriptionEvent) -> bool:
        """Check if event should be delivered to subscription."""
        filters = self.filters.get(subscription_id, [])
        
        for filter_option in filters:
            if not self._matches_filter(event, filter_option):
                return False
        
        return True
    
    def _matches_filter(self, event: SubscriptionEvent, filter_option: SubscriptionFilter) -> bool:
        """Check if event matches filter."""
        event_value = event.payload.get(filter_option.field_name)
        
        if filter_option.operator == "eq":
            return event_value == filter_option.field_value
        elif filter_option.operator == "neq":
            return event_value != filter_option.field_value
        elif filter_option.operator == "gt":
            return event_value > filter_option.field_value
        elif filter_option.operator == "lt":
            return event_value < filter_option.field_value
        elif filter_option.operator == "in":
            return event_value in filter_option.field_value
        elif filter_option.operator == "contains":
            return filter_option.field_value in str(event_value)
        
        return False


# Main demo function
async def main():
    """Demonstrate GraphQL subscription patterns."""
    print("=== GraphQL Subscriptions Demo ===\n")
    
    # Demo 1: Pub/Sub System
    print("1. Pub/Sub System:")
    
    pubsub = PubSub()
    
    # Subscribe to events
    async def post_created_handler(event: SubscriptionEvent):
        print(f"    Post created: {event.payload.get('title')}")
    
    async def comment_added_handler(event: SubscriptionEvent):
        print(f"    Comment added: {event.payload.get('content')}")
    
    pubsub.subscribe("POST_CREATED", post_created_handler)
    pubsub.subscribe("COMMENT_ADDED", comment_added_handler)
    
    # Publish events
    post_event = SubscriptionEvent(
        id=str(uuid.uuid4()),
        type=EventType.POST_CREATED,
        payload={"id": "1", "title": "New Post", "authorId": "1"}
    )
    
    comment_event = SubscriptionEvent(
        id=str(uuid.uuid4()),
        type=EventType.COMMENT_ADDED,
        payload={"id": "1", "content": "Great post!", "postId": "1", "authorId": "2"}
    )
    
    await pubsub.publish(post_event)
    await pubsub.publish(comment_event)
    
    print(f"  PubSub metrics: {pubsub.get_metrics().to_dict()}")
    
    # Demo 2: Subscription Manager
    print("\n2. Subscription Manager:")
    
    manager = SubscriptionManager(pubsub)
    
    # Create subscriptions
    subscription1 = await manager.create_subscription(
        query="subscription { postCreated { id title } }",
        variables={},
        options=SubscriptionOptions(
            filters=[SubscriptionFilter(field_name="authorId", field_value="1")]
        ),
        client_id="client-1"
    )
    
    subscription2 = await manager.create_subscription(
        query="subscription { commentAdded(postId: \"1\") { id content } }",
        variables={"postId": "1"},
        client_id="client-2"
    )
    
    print(f"  Created {len(manager.subscriptions)} subscriptions")
    
    # Handle events
    await manager.handle_event(post_event)
    await manager.handle_event(comment_event)
    
    # Demo 3: WebSocket Manager
    print("\n3. WebSocket Manager:")
    
    ws_manager = WebSocketManager()
    
    # Handle connections
    connection1 = await ws_manager.handle_connection(
        "conn-1",
        {"authToken": "token-1"}
    )
    
    connection2 = await ws_manager.handle_connection(
        "conn-2",
        {"authToken": "token-2"}
    )
    
    print(f"  Active connections: {ws_manager.get_connection_count()}")
    
    # Handle messages
    start_message = WebSocketMessage(
        type=MessageType.START,
        id="sub-1",
        payload={
            "query": "subscription { postCreated { id } }",
            "variables": {}
        }
    )
    
    await ws_manager.handle_message("conn-1", start_message)
    
    # Heartbeat check
    await ws_manager.heartbeat_check()
    
    # Demo 4: Subscription Client
    print("\n4. Subscription Client:")
    
    client = SubscriptionClient("ws://localhost:4000/graphql")
    await client.connect()
    
    # Subscribe
    subscription_id = await client.subscribe(
        query="subscription { postCreated { id title } }",
        variables={}
    )
    
    print(f"  Client subscriptions: {client.get_subscription_count()}")
    
    # Handle incoming message
    data_message = WebSocketMessage(
        type=MessageType.DATA,
        id=subscription_id,
        payload={"data": {"id": "1", "title": "New Post"}}
    )
    
    await client.handle_message(data_message)
    
    # Demo 5: Scaling Manager
    print("\n5. Scaling Manager:")
    
    scaling = ScalingManager()
    
    # Add instances
    await scaling.add_instance("instance-1", "http://server1:4000")
    await scaling.add_instance("instance-2", "http://server2:4000")
    await scaling.add_instance("instance-3", "http://server3:4000")
    
    # Distribute connections
    for i in range(10):
        await scaling.distribute_connection(f"conn-{i}")
    
    print(f"  Total instances: {len(scaling.instances)}")
    print(f"  Total connections: {scaling.get_total_connections()}")
    
    # Get instance metrics
    instance_metrics = await scaling.get_instance_metrics()
    for metrics in instance_metrics:
        print(f"    Instance {metrics['id']}: {metrics['connections']} connections")
    
    # Demo 6: Event Filter
    print("\n6. Event Filter:")
    
    event_filter = EventFilter()
    
    # Add filters
    event_filter.add_filter(
        "sub-1",
        SubscriptionFilter(field_name="authorId", field_value="1")
    )
    
    event_filter.add_filter(
        "sub-2",
        SubscriptionFilter(field_name="postId", field_value="1")
    )
    
    # Test filters
    test_event = SubscriptionEvent(
        id=str(uuid.uuid4()),
        type=EventType.POST_CREATED,
        payload={"authorId": "1", "title": "Test"}
    )
    
    should_deliver_1 = event_filter.should_deliver("sub-1", test_event)
    should_deliver_2 = event_filter.should_deliver("sub-2", test_event)
    
    print(f"  Should deliver to sub-1: {should_deliver_1}")
    print(f"  Should deliver to sub-2: {should_deliver_2}")
    
    # Demo 7: Connection Lifecycle
    print("\n7. Connection Lifecycle:")
    
    # Create subscription
    lifecycle_sub = await manager.create_subscription(
        query="subscription { userStatusChanged { status } }",
        variables={"userId": "1"}
    )
    
    print(f"  Subscription status: {lifecycle_sub.status.name}")
    
    # Update status
    lifecycle_sub.status = SubscriptionStatus.CONNECTED
    print(f"  Updated status: {lifecycle_sub.status.name}")
    
    # Cancel subscription
    await manager.cancel_subscription(lifecycle_sub.id)
    print(f"  Cancelled subscription: {lifecycle_sub.id}")
    
    # Demo 8: Metrics Collection
    print("\n8. Metrics Collection:")
    
    # Get metrics from different components
    pubsub_metrics = pubsub.get_metrics()
    manager_metrics = manager.get_metrics()
    ws_metrics = ws_manager.get_metrics()
    
    print(f"  PubSub metrics: {pubsub_metrics.to_dict()}")
    print(f"  Manager metrics: {manager_metrics.to_dict()}")
    print(f"  WebSocket metrics: {ws_metrics.to_dict()}")
    
    # Demo 9: Error Handling
    print("\n9. Error Handling:")
    
    # Simulate error
    error_message = WebSocketMessage(
        type=MessageType.ERROR,
        id="sub-error",
        payload={"message": "Subscription failed"}
    )
    
    await client.handle_message(error_message)
    
    # Demo 10: Cleanup
    print("\n10. Cleanup:")
    
    # Disconnect client
    await client.disconnect()
    
    # Disconnect WebSocket connections
    await ws_manager.handle_disconnect("conn-1")
    await ws_manager.handle_disconnect("conn-2")
    
    print(f"  Final connection count: {ws_manager.get_connection_count()}")
    print(f"  Final subscription count: {manager.get_metrics().active_connections}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(main())