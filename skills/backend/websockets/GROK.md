---
name: "websockets"
category: "backend"
version: "2.0.0"
tags: ["backend", "websockets", "real-time", "pub-sub", "scaling"]
---

# WebSocket Patterns

## Overview

Production-grade WebSocket development guide covering connection lifecycle management, room-based messaging, publish-subscribe patterns, heartbeat and keepalive mechanisms, reconnection strategies, binary frame handling, horizontal scaling with Redis PubSub, load balancing considerations, and security hardening. This module provides patterns for building reliable real-time applications serving thousands of concurrent connections.

## Core Capabilities

- Connection management with authentication, heartbeats, and graceful shutdown
- Room-based and topic-based messaging with join/leave semantics
- Redis PubSub for cross-server message broadcasting
- Binary and text frame handling with compression
- Client-side reconnection with exponential backoff
- Horizontal scaling with sticky sessions and message fanout
- Connection draining and graceful server shutdown
- Rate limiting per connection and per room
- Message acknowledgment and delivery guarantees
- Authentication via JWT, session tokens, and API keys

## Usage

```python
# FastAPI WebSocket with authentication
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
import json

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.rooms: dict[str, set[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)
        for room_id, members in self.rooms.items():
            members.discard(user_id)

    async def send_to_user(self, user_id: str, message: dict):
        ws = self.active_connections.get(user_id)
        if ws and ws.client_state == WebSocketState.CONNECTED:
            await ws.send_json(message)

    async def broadcast_to_room(self, room_id: str, message: dict):
        for user_id in self.rooms.get(room_id, set()):
            await self.send_to_user(user_id, message)

manager = ConnectionManager()

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    user = await verify_ws_token(token)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    await manager.connect(websocket, user.id)

    try:
        while True:
            data = await websocket.receive_json()
            await handle_message(user, data)
    except WebSocketDisconnect:
        manager.disconnect(user.id)

async def handle_message(user, data):
    msg_type = data.get("type")
    if msg_type == "join_room":
        manager.rooms.setdefault(data["room_id"], set()).add(user.id)
        await manager.broadcast_to_room(data["room_id"], {
            "type": "user_joined",
            "user_id": user.id,
        })
    elif msg_type == "send_message":
        await manager.broadcast_to_room(data["room_id"], {
            "type": "new_message",
            "user_id": user.id,
            "content": data["content"],
        })
```

## Best Practices

- Always authenticate WebSocket connections during the handshake
- Implement heartbeat/ping-pong to detect dead connections
- Use rooms/channels to scope message broadcasting
- Handle backpressure when clients consume slowly
- Implement message acknowledgment for critical messages
- Rate-limit inbound messages per connection
- Use binary frames for large payloads; text for JSON
- Implement graceful shutdown with connection draining
- Monitor connection counts and message rates
- Use Redis PubSub for multi-server message fanout

## Related Modules

- `redis-pubsub` — Distributed message broadcasting
- `socket.io` — Fallback-capable real-time framework
- `ws` — Lightweight WebSocket library
- `fastapi-websocket` — WebSocket support for FastAPI
- `centrifugo` — Scalable real-time messaging server

---

## Advanced Configuration

### WebSocket Server Configuration

```typescript
import { WebSocketServer, WebSocket } from 'ws';
import { createServer } from 'http';
import jwt from 'jsonwebtoken';

const server = createServer();
const wss = new WebSocketServer({
  server,
  path: '/ws',
  maxPayload: 64 * 1024, // 64KB max message size
  perMessageDeflate: {
    zlibDeflateOptions: {
      chunkSize: 1024,
      memLevel: 7,
      level: 3,
    },
    zlibInflateOptions: {
      chunkSize: 10 * 1024,
    },
    threshold: 1024, // Only compress messages > 1KB
  },
  verifyClient: async (info, callback) => {
    try {
      const token = new URL(
        info.req.url,
        `http://${info.req.headers.host}`
      ).searchParams.get('token');

      if (!token) {
        callback(false, 401, 'Unauthorized');
        return;
      }

      const user = jwt.verify(token, process.env.JWT_SECRET);
      info.req.user = user;
      callback(true);
    } catch (err) {
      callback(false, 401, 'Invalid token');
    }
  },
});

// Connection manager
class ConnectionManager {
  constructor() {
    this.connections = new Map(); // userId -> Set<WebSocket>
    this.rooms = new Map();      // roomId -> Set<userId>
    this.userRooms = new Map();  // userId -> Set<roomId>
  }

  addConnection(userId, ws) {
    if (!this.connections.has(userId)) {
      this.connections.set(userId, new Set());
    }
    this.connections.get(userId).add(ws);
    ws.userId = userId;
    ws.isAlive = true;
  }

  removeConnection(ws) {
    const userId = ws.userId;
    const userConns = this.connections.get(userId);
    if (userConns) {
      userConns.delete(ws);
      if (userConns.size === 0) {
        this.connections.delete(userId);
        // Leave all rooms
        const rooms = this.userRooms.get(userId) || new Set();
        for (const roomId of rooms) {
          this.leaveRoom(userId, roomId);
        }
        this.userRooms.delete(userId);
      }
    }
  }

  joinRoom(userId, roomId) {
    if (!this.rooms.has(roomId)) {
      this.rooms.set(roomId, new Set());
    }
    this.rooms.get(roomId).add(userId);

    if (!this.userRooms.has(userId)) {
      this.userRooms.set(userId, new Set());
    }
    this.userRooms.get(userId).add(roomId);
  }

  leaveRoom(userId, roomId) {
    this.rooms.get(roomId)?.delete(userId);
    this.userRooms.get(userId)?.delete(roomId);
  }

  async broadcast(roomId, message, excludeUserId) {
    const userIds = this.rooms.get(roomId) || new Set();
    for (const userId of userIds) {
      if (userId === excludeUserId) continue;
      await this.sendToUser(userId, message);
    }
  }

  async sendToUser(userId, message) {
    const conns = this.connections.get(userId);
    if (!conns) return;
    const data = JSON.stringify(message);
    for (const ws of conns) {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    }
  }

  broadcastAll(message) {
    const data = JSON.stringify(message);
    for (const [, conns] of this.connections) {
      for (const ws of conns) {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(data);
        }
      }
    }
  }
}
```

### Heartbeat Configuration

```typescript
const HEARTBEAT_INTERVAL = 30000; // 30 seconds
const HEARTBEAT_TIMEOUT = 10000;  // 10 seconds

// Server-side heartbeat
const heartbeatTimer = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) {
      // Connection is dead
      manager.removeConnection(ws);
      return ws.terminate();
    }

    ws.isAlive = false;
    ws.ping();
  });
}, HEARTBEAT_INTERVAL);

wss.on('connection', (ws) => {
  ws.isAlive = true;
  ws.on('pong', () => { ws.isAlive = true; });
});

wss.on('close', () => {
  clearInterval(heartbeatTimer);
});

// Client-side heartbeat
class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.baseReconnectDelay = 1000;
    this.heartbeatInterval = null;
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.reconnectAttempts = 0;
      this.startHeartbeat();
    };

    this.ws.onclose = (event) => {
      this.stopHeartbeat();
      if (!event.wasClean) {
        this.reconnect();
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }));
      }
    }, HEARTBEAT_INTERVAL);
  }

  stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
    }
  }

  reconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    const delay = Math.min(
      this.baseReconnectDelay * Math.pow(2, this.reconnectAttempts),
      30000
    );

    this.reconnectAttempts++;
    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

    setTimeout(() => this.connect(), delay);
  }
}
```

---

## Architecture Patterns

```
┌─────────────────────────────────────────────────────────┐
│                    WebSocket Clients                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │   Web     │  │  Mobile  │  │  IoT / Embedded      │  │
│  │  Browser  │  │   App    │  │  Device              │  │
│  └─────┬────┘  └────┬─────┘  └──────────┬───────────┘  │
└────────┼────────────┼────────────────────┼───────────────┘
         │            │                    │
         ▼            ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                  Load Balancer (nginx)                    │
│            ┌─────────────────────────────┐               │
│            │  sticky_sessions on         │               │
│            │  ip_hash or cookie-based    │               │
│            └─────────────────────────────┘               │
└──────────────────┬──────────────────────┬────────────────┘
                   │                      │
         ┌─────────▼────────┐   ┌─────────▼────────┐
         │  WebSocket Srv 1 │   │  WebSocket Srv 2 │
         │  ┌────────────┐  │   │  ┌────────────┐  │
         │  │ Connection  │  │   │  │ Connection  │  │
         │  │ Manager     │  │   │  │ Manager     │  │
         │  │  ┌────────┐ │  │   │  │  ┌────────┐ │  │
         │  │  │ Room 1 │ │  │   │  │  │ Room 1 │ │  │
         │  │  │ Room 2 │ │  │   │  │  │ Room 3 │ │  │
         │  │  └────────┘ │  │   │  │  └────────┘ │  │
         │  └────────────┘  │   │  └────────────┘  │
         └─────────┬────────┘   └─────────┬────────┘
                   │                      │
                   └──────────┬───────────┘
                              │
                   ┌──────────▼──────────┐
                   │     Redis PubSub     │
                   │  ┌────────────────┐ │
                   │  │  Channel: room  │ │
                   │  │  Channel: user  │ │
                   │  │  Channel: event │ │
                   │  └────────────────┘ │
                   └─────────────────────┘

Message Flow (room broadcast):

  Client A ──► Server 1 ──► Redis PubSub ──► Server 2 ──► Client B
                                              Server 1 ──► Client C

Connection Lifecycle:

  [Connect] ──► [Authenticate] ──► [Join Rooms] ──► [Active]
       │              │                │                │
       │              │                │                ▼
       │              │                │         [Heartbeat]
       │              │                │          ↻ ping/pong
       │              │                │
       │              │                ▼
       │              │         [Disconnect]
       │              │              │
       ▼              ▼              ▼
  [Close]      [Close/Error]   [Cleanup & Notify]
```

### Room-Based Messaging Pattern

```
                    ┌──────────────────────┐
                    │       Room           │
                    │   "chat:general"     │
                    │                      │
                    │  ┌──────┐ ┌──────┐  │
                    │  │User A│ │User B│  │
                    │  └──────┘ └──────┘  │
                    │  ┌──────┐ ┌──────┐  │
                    │  │User C│ │User D│  │
                    │  └──────┘ └──────┘  │
                    └──────────────────────┘

User A sends message
    │
    ▼
Server validates & stores
    │
    ▼
Publish to room channel
    │
    ├──► Server 1: send to User B, C
    └──► Server 2: send to User D
```

---

## Integration Guide

### Redis PubSub for Multi-Server

```python
import redis.asyncio as redis
import json

class RedisPubSubManager:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()
        self.subscriptions: dict[str, set] = {}

    async def subscribe(self, channel: str, callback):
        await self.pubsub.subscribe(channel)
        if channel not in self.subscriptions:
            self.subscriptions[channel] = set()
        self.subscriptions[channel].add(callback)

    async def unsubscribe(self, channel: str, callback):
        if channel in self.subscriptions:
            self.subscriptions[channel].discard(callback)
        if not self.subscriptions[channel]:
            await self.pubsub.unsubscribe(channel)
            del self.subscriptions[channel]

    async def publish(self, channel: str, message: dict):
        await self.redis.publish(channel, json.dumps(message))

    async def listen(self):
        async for msg in self.pubsub.listen():
            if msg["type"] == "message":
                channel = msg["channel"]
                data = json.loads(msg["data"])
                for callback in self.subscriptions.get(channel, set()):
                    await callback(data)

# Integration with ConnectionManager
class DistributedConnectionManager(ConnectionManager):
    def __init__(self, redis_url: str):
        super().__init__()
        self.redis_pubsub = RedisPubSubManager(redis_url)
        self.server_id = os.environ.get("SERVER_ID", "server-1")

    async def broadcast_to_room(self, room_id: str, message: dict):
        # Publish to Redis for other servers
        await self.redis_pubsub.publish(
            f"room:{room_id}",
            {**message, "source_server": self.server_id}
        )
        # Also handle locally
        for user_id in self.rooms.get(room_id, set()):
            await self.send_to_user(user_id, message)

    async def handle_remote_message(self, channel: str, message: dict):
        if message.get("source_server") == self.server_id:
            return  # Skip messages from this server
        room_id = channel.replace("room:", "")
        for user_id in self.rooms.get(room_id, set()):
            await self.send_to_user(user_id, message)
```

### Authentication Middleware

```python
from fastapi import WebSocket, Query
from jose import jwt, JWTError

async def verify_ws_token(token: str = Query(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            return None
        return {"id": user_id, "roles": payload.get("roles", [])}
    except JWTError:
        return None

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
):
    user = await verify_ws_token(token)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    await manager.connect(websocket, user["id"])

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "user_id": user["id"],
            "server_time": datetime.utcnow().isoformat(),
        })

        while True:
            data = await websocket.receive_json()
            await handle_message(user, data)
    except WebSocketDisconnect:
        manager.disconnect(user["id"])
```

### Rate Limiting

```python
import time
from collections import defaultdict

class ConnectionRateLimiter:
    def __init__(self, max_messages: int = 100, window_seconds: int = 60):
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        self.counts: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds

        # Remove old entries
        self.counts[user_id] = [
            t for t in self.counts[user_id] if t > cutoff
        ]

        if len(self.counts[user_id]) >= self.max_messages:
            return False

        self.counts[user_id].append(now)
        return True

rate_limiter = ConnectionRateLimiter(max_messages=100, window_seconds=60)

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    user = await verify_ws_token(token)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    await manager.connect(websocket, user.id)

    try:
        while True:
            data = await websocket.receive_json()

            if not rate_limiter.is_allowed(user.id):
                await websocket.send_json({
                    "type": "error",
                    "code": "RATE_LIMITED",
                    "message": "Too many messages",
                })
                continue

            await handle_message(user, data)
    except WebSocketDisconnect:
        manager.disconnect(user.id)
```

---

## Performance Optimization

| Technique | Impact | When to Use |
|-----------|--------|-------------|
| Message batching | 2-5x throughput | High-frequency updates (chat, gaming) |
| Binary frames (MessagePack) | 30-50% smaller payloads | Binary data or high-frequency JSON |
| Per-message deflate | 60-80% bandwidth reduction | Text-heavy messages > 1KB |
| Connection pooling (Redis) | 5-10x PubSub throughput | Multi-server deployments |
| Room-based scoping | Reduces message fanout | Always — avoid global broadcasts |
| Message deduplication | Prevents duplicate processing | Distributed systems with retries |
| Lazy heartbeat | Reduces ping/pong overhead | Large numbers of idle connections |
| Backpressure handling | Prevents memory overflow | Slow consumers |

### Message Batching

```typescript
class MessageBatcher {
  private batch: Map<string, any[]> = new Map();
  private timer: NodeJS.Timeout | null = null;
  private interval: number;

  constructor(interval: number = 50) {
    this.interval = interval;
  }

  add(roomId: string, message: any) {
    if (!this.batch.has(roomId)) {
      this.batch.set(roomId, []);
    }
    this.batch.get(roomId)!.push(message);

    if (!this.timer) {
      this.timer = setTimeout(() => this.flush(), this.interval);
    }
  }

  flush() {
    for (const [roomId, messages] of this.batch) {
      this.sendBatch(roomId, messages);
    }
    this.batch.clear();
    this.timer = null;
  }

  private sendBatch(roomId: string, messages: any[]) {
    const batched = {
      type: 'batch',
      messages,
      timestamp: Date.now(),
    };
    // Broadcast batched message
    manager.broadcastToRoom(roomId, batched);
  }
}
```

### Backpressure Handling

```typescript
class BackpressureHandler {
  private queue: Map<string, any[]> = new Map();
  private maxQueueSize: number;

  constructor(maxQueueSize: number = 1000) {
    this.maxQueueSize = maxQueueSize;
  }

  async send(ws: WebSocket, message: any): Promise<boolean> {
    if (ws.bufferedAmount > this.maxQueueSize) {
      // Client is too slow — drop messages
      this.dropMessage(ws);
      return false;
    }

    ws.send(JSON.stringify(message));
    return true;
  }

  private dropMessage(ws: WebSocket) {
    const userId = (ws as any).userId;
    console.warn(`Dropping messages for slow client: ${userId}`);
  }
}
```

---

## Security Considerations

### Connection Authentication

- Always authenticate during the WebSocket handshake (HTTP upgrade)
- Never trust client-claimed user IDs; validate JWT/session server-side
- Implement token refresh for long-lived connections
- Log all connection/disconnection events for audit
- Validate message structure and sanitize all user input

### Message Validation

```python
from pydantic import BaseModel, Field, validator

class WebSocketMessage(BaseModel):
    type: str = Field(..., max_length=50)
    room_id: str = Field(None, max_length=100)
    content: str = Field(None, max_length=4096)

    @validator("type")
    def validate_type(cls, v):
        allowed = {"join_room", "leave_room", "send_message", "typing"}
        if v not in allowed:
            raise ValueError(f"Invalid message type: {v}")
        return v

async def handle_validated_message(user, raw_data):
    try:
        msg = WebSocketMessage(**raw_data)
        # Process validated message
        if msg.type == "join_room":
            await join_room(user, msg.room_id)
        elif msg.type == "send_message":
            await send_message(user, msg.room_id, msg.content)
    except ValueError as e:
        await send_error(user, "INVALID_MESSAGE", str(e))
```

### Security Checklist

- Use `wss://` (TLS) in production; never `ws://`
- Validate Origin header against allowed origins
- Implement connection limits per IP and per user
- Rate-limit inbound messages per connection
- Sanitize all user-generated content before broadcasting
- Log suspicious activity (rapid reconnects, message floods)
- Use separate authentication for WebSocket vs HTTP APIs
- Implement message size limits (64KB recommended)
- Rotate JWT signing keys periodically
- Use secure cookies for session-based WebSocket auth

---

## Troubleshooting Guide

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| Connection drops every 30s | Missing heartbeat/pong response | Ensure client responds to pings |
| Messages not received by others | Server not using Redis PubSub | Add Redis for cross-server broadcasting |
| `403 Forbidden` on connect | Missing/invalid auth token | Check token validation in verifyClient |
| Memory grows over time | Connection leak (not cleaned up) | Verify `removeConnection` on close |
| Slow message delivery | Large payload without compression | Enable per-message deflate |
| Connection refused | Load balancer not configured for WS | Enable WebSocket upgrade in nginx config |
| Duplicate messages | No message deduplication | Add message IDs and client-side dedup |
| `ECONNRESET` errors | Server restarting without draining | Implement graceful shutdown |
| Client reconnects fail | Token expired during disconnect | Refresh token before reconnect |
| Binary data corrupted | Mixing text and binary frames | Separate text/binary handlers |

---

## API Reference

### WebSocket Events

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `connected` | Server → Client | `{ user_id, server_time }` | Connection established |
| `ping` | Client → Server | `{}` | Keepalive ping |
| `pong` | Server → Client | `{}` | Keepalive pong response |
| `join_room` | Client → Server | `{ room_id }` | Join a room |
| `leave_room` | Client → Server | `{ room_id }` | Leave a room |
| `send_message` | Client → Server | `{ room_id, content }` | Send message to room |
| `new_message` | Server → Client | `{ room_id, user_id, content }` | New message received |
| `user_joined` | Server → Client | `{ room_id, user_id }` | User joined room |
| `user_left` | Server → Client | `{ room_id, user_id }` | User left room |
| `typing` | Client → Server | `{ room_id }` | User is typing |
| `error` | Server → Client | `{ code, message }` | Error occurred |

### Close Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| `1000` | Normal closure | Clean disconnect |
| `1001` | Going away | Page unload, navigation |
| `1002` | Protocol error | Invalid frame received |
| `1003` | Unsupported data | Received unsupported frame type |
| `1006` | Abnormal closure | Connection dropped without close frame |
| `1008` | Policy violation | Message violates server policy |
| `1011` | Internal error | Server-side error |
| `4001` | Unauthorized | Authentication failed |
| `4003` | Forbidden | Insufficient permissions |
| `4004` | Not found | Room/resource not found |
| `4008` | Rate limited | Too many messages |
| `4009` | Server shutting down | Graceful shutdown in progress |

---

## Data Models

### Connection State

```typescript
interface ConnectionState {
  userId: string;
  connectionId: string;
  connectedAt: Date;
  lastActivity: Date;
  rooms: Set<string>;
  metadata: Record<string, any>;
  isAlive: boolean;
}

interface ConnectionInfo {
  userId: string;
  connectionCount: number;
  rooms: string[];
  connectedAt: Date;
  lastMessageAt: Date;
}
```

### Message Types

```typescript
// Outbound messages (server → client)
interface ConnectedMessage {
  type: 'connected';
  userId: string;
  serverTime: string;
}

interface NewMessage {
  type: 'new_message';
  roomId: string;
  userId: string;
  content: string;
  messageId: string;
  timestamp: string;
}

interface UserEvent {
  type: 'user_joined' | 'user_left';
  roomId: string;
  userId: string;
}

interface ErrorMessage {
  type: 'error';
  code: string;
  message: string;
  retryAfter?: number;
}

// Inbound messages (client → server)
interface JoinRoomMessage {
  type: 'join_room';
  roomId: string;
}

interface SendMessage {
  type: 'send_message';
  roomId: string;
  content: string;
}

interface PingMessage {
  type: 'ping';
}

// Batched messages
interface BatchMessage {
  type: 'batch';
  messages: (NewMessage | UserEvent)[];
  timestamp: number;
}
```

### Room State

```typescript
interface Room {
  id: string;
  name: string;
  members: Set<string>;
  createdAt: Date;
  metadata: Record<string, any>;
  maxMembers?: number;
  requireAuth?: boolean;
}

interface RoomInfo {
  id: string;
  memberCount: number;
  createdAt: Date;
}
```

---

## Deployment Guide

### Docker Configuration

```dockerfile
FROM node:20-alpine

RUN addgroup -g 1001 -S wsgroup && \
    adduser -S wsuser -u 1001 -G wsgroup

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

USER wsuser

EXPOSE 8080

CMD ["node", "server.js"]
```

### nginx Configuration

```nginx
upstream websocket_backend {
    ip_hash;  # Sticky sessions
    server ws-server-1:8080;
    server ws-server-2:8080;
    server ws-server-3:8080;
}

server {
    listen 443 ssl;
    server_name ws.example.com;

    ssl_certificate /etc/ssl/certs/ws.example.com.pem;
    ssl_certificate_key /etc/ssl/private/ws.example.com.key;

    location /ws {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;

        # Buffering
        proxy_buffering off;
        proxy_cache off;
    }
}
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ws-server
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: ws-server
  template:
    metadata:
      labels:
        app: ws-server
    spec:
      containers:
        - name: ws
          image: registry.example.com/ws-server:2.0.0
          ports:
            - containerPort: 8080
          env:
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: ws-secrets
                  key: redis-url
            - name: SERVER_ID
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
          livenessProbe:
            tcpSocket:
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "250m"

# Graceful shutdown: send SIGTERM, wait for connections to drain
# Kubernetes default terminationGracePeriodSeconds: 30
```

---

## Monitoring and Observability

### Metrics Collection

```typescript
import { Counter, Histogram, Gauge } from 'prom-client';

const connectionsTotal = new Counter({
  name: 'websocket_connections_total',
  help: 'Total WebSocket connections',
  labelNames: ['status'],
});

const activeConnections = new Gauge({
  name: 'websocket_active_connections',
  help: 'Currently active WebSocket connections',
});

const messagesTotal = new Counter({
  name: 'websocket_messages_total',
  help: 'Total WebSocket messages',
  labelNames: ['direction', 'type'],
});

const messageLatency = new Histogram({
  name: 'websocket_message_latency_seconds',
  help: 'Message delivery latency',
  buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5],
});

// Track metrics in connection manager
wss.on('connection', (ws) => {
  activeConnections.inc();
  connectionsTotal.inc({ status: 'connected' });

  ws.on('close', () => {
    activeConnections.dec();
    connectionsTotal.inc({ status: 'disconnected' });
  });

  ws.on('message', (data) => {
    messagesTotal.inc({ direction: 'inbound', type: 'message' });
  });
});
```

### Logging

```python
import structlog

logger = structlog.get_logger()

async def handle_connection(websocket, user_id):
    logger.info(
        "ws_connected",
        user_id=user_id,
        remote_addr=websocket.client.host,
    )
    try:
        while True:
            data = await websocket.receive_json()
            logger.debug(
                "ws_message_received",
                user_id=user_id,
                type=data.get("type"),
            )
    except WebSocketDisconnect:
        logger.info("ws_disconnected", user_id=user_id)
```

---

## Testing Strategy

### Unit Tests

```typescript
import { WebSocketServer, WebSocket } from 'ws';
import { ConnectionManager } from './manager';

describe('ConnectionManager', () => {
  let manager: ConnectionManager;

  beforeEach(() => {
    manager = new ConnectionManager();
  });

  it('adds and removes connections', () => {
    const ws = { userId: 'user-1', readyState: WebSocket.OPEN } as WebSocket;
    manager.addConnection('user-1', ws);
    expect(manager.connections.has('user-1')).toBe(true);

    manager.removeConnection(ws);
    expect(manager.connections.has('user-1')).toBe(false);
  });

  it('manages room membership', () => {
    manager.joinRoom('user-1', 'room-1');
    expect(manager.rooms.get('room-1')?.has('user-1')).toBe(true);

    manager.leaveRoom('user-1', 'room-1');
    expect(manager.rooms.get('room-1')?.has('user-1')).toBe(false);
  });
});
```

### Integration Tests

```typescript
import WebSocket from 'ws';

describe('WebSocket Integration', () => {
  let ws: WebSocket;

  afterEach(() => {
    ws?.close();
  });

  it('connects and receives welcome message', (done) => {
    ws = new WebSocket('ws://localhost:8080/ws?token=valid-token');

    ws.on('open', () => {
      ws.on('message', (data) => {
        const msg = JSON.parse(data.toString());
        expect(msg.type).toBe('connected');
        expect(msg.userId).toBe('user-1');
        done();
      });
    });
  });

  it('broadcasts messages to room', (done) => {
    const ws1 = new WebSocket('ws://localhost:8080/ws?token=token1');
    const ws2 = new WebSocket('ws://localhost:8080/ws?token=token2');
    let receivedCount = 0;

    const checkDone = () => {
      receivedCount++;
      if (receivedCount === 2) done();
    };

    ws1.on('open', () => {
      ws1.send(JSON.stringify({ type: 'join_room', roomId: 'room-1' }));
      ws1.on('message', (data) => {
        const msg = JSON.parse(data.toString());
        if (msg.type === 'new_message') checkDone();
      });
    });

    ws2.on('open', () => {
      ws2.send(JSON.stringify({ type: 'join_room', roomId: 'room-1' }));
      ws2.on('message', (data) => {
        const msg = JSON.parse(data.toString());
        if (msg.type === 'new_message') checkDone();
      });

      setTimeout(() => {
        ws1.send(JSON.stringify({
          type: 'send_message',
          roomId: 'room-1',
          content: 'Hello!',
        }));
      }, 100);
    });
  });
});
```

---

## Versioning and Migration

### Protocol Versioning

```typescript
// Include version in connection handshake
const ws = new WebSocket('ws://localhost:8080/ws?version=2&token=...');

// Server checks version and handles accordingly
wss.on('connection', (ws, req) => {
  const url = new URL(req.url, 'http://localhost');
  const clientVersion = parseInt(url.searchParams.get('version') || '1');

  if (clientVersion < MIN_SUPPORTED_VERSION) {
    ws.close(4005, 'Protocol version not supported');
    return;
  }

  ws.protocolVersion = clientVersion;
});
```

### Message Format Migration

```typescript
// v1: flat structure
interface V1Message {
  type: string;
  data: any;
}

// v2: structured with metadata
interface V2Message {
  type: string;
  payload: any;
  metadata: {
    version: number;
    timestamp: string;
    requestId?: string;
  };
}

// Handle both versions
function handleIncomingMessage(raw: string) {
  const msg = JSON.parse(raw);

  if (msg.metadata?.version === 2) {
    return handleV2Message(msg);
  } else {
    return handleV1Message(msg);
  }
}
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **WebSocket** | Full-duplex communication protocol over a single TCP connection |
| **Heartbeat** | Periodic ping/pong exchange to detect dead connections |
| **Room** | Logical grouping of connections for scoped message broadcasting |
| **PubSub** | Publish-Subscribe pattern for decoupled message distribution |
| **Sticky Session** | Load balancer routing that sends a client to the same server |
| **Backpressure** | Mechanism to slow down message production when consumer is slow |
| **Per-message Deflate** | WebSocket extension for per-frame compression |
| **Close Frame** | Protocol frame signaling connection termination |
| **Connection Draining** | Graceful shutdown waiting for active connections to close |
| **Binary Frame** | WebSocket frame carrying binary data (vs text frame) |

---

## Changelog

### 2.0.0 (2024-12-01)

- Added Redis PubSub for multi-server message fanout
- Added connection draining and graceful shutdown
- Added per-connection rate limiting
- Added backpressure handling for slow consumers
- Added message batching for high-frequency updates
- Added comprehensive security checklist
- Added Kubernetes deployment with rolling updates

### 1.1.0 (2024-06-15)

- Added heartbeat/ping-pong patterns
- Added reconnection with exponential backoff
- Added room-based messaging
- Added binary frame handling

### 1.0.0 (2024-01-01)

- Initial release
- Basic WebSocket connection management
- Simple message broadcasting
- Authentication patterns

---

## Contributing Guidelines

1. Fork the repository and create a feature branch
2. Follow the existing code patterns and conventions
3. Add tests for new patterns (target: 85% coverage)
4. Update this document for any new patterns
5. Run linter and formatter before committing
6. Submit a pull request with a clear description

### Code Style

- Use TypeScript strict mode
- Prefer async/await over callbacks
- Handle all error cases explicitly
- Document non-obvious behavior
- Keep message handlers under 30 lines

---

## License

MIT License. See [LICENSE](LICENSE) for details.
