---
name: "background-jobs"
category: "backend"
version: "2.0.0"
tags: ["backend", "background-jobs", "celery", "queues", "scheduling"]
---

# Background Jobs

## Overview

Production-grade background job processing guide covering task queue architectures with Celery, Bull/BullMQ, and Dramatiq, job scheduling and cron patterns, retry strategies with exponential backoff, dead letter queues for failed job analysis, monitoring dashboards, distributed locking, rate limiting, and idempotency. This module provides patterns for building reliable asynchronous job processing systems that handle millions of tasks daily.

## Core Capabilities

- Task queue setup with Celery (Python), BullMQ (Node.js), and Dramatiq (Python)
- Cron and periodic task scheduling with beat/or scheduler processes
- Retry strategies: exponential backoff, dead letter queues, and circuit breakers
- Distributed locking with Redis and Zookeeper
- Rate limiting per task type and per worker
- Job prioritization and priority queues
- Worker pooling and autoscaling
- Monitoring with Flower, Bull Board, and custom dashboards
- Idempotency keys for exactly-once processing semantics
- Graceful shutdown and worker drain patterns

## Usage

```python
# Celery configuration
from celery import Celery
from celery.schedules import crontab

app = Celery('myapp')
app.config_from_object({
    'broker_url': 'redis://localhost:6379/0',
    'result_backend': 'redis://localhost:6379/1',
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'timezone': 'UTC',
    'enable_utc': True,
    'task_track_started': True,
    'task_acks_late': True,
    'worker_prefetch_multiplier': 1,
    'task_routes': {
        'myapp.tasks.email.*': {'queue': 'email'},
        'myapp.tasks.report.*': {'queue': 'reports'},
    },
    'beat_schedule': {
        'cleanup-sessions': {
            'task': 'myapp.tasks.cleanup_expired_sessions',
            'schedule': crontab(hour=3, minute=0),  # 3 AM daily
        },
        'generate-reports': {
            'task': 'myapp.tasks.generate_daily_reports',
            'schedule': crontab(hour=6, minute=0),  # 6 AM daily
        },
    },
})

# Task definitions
@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, to: str, subject: str, body: str):
    try:
        email_service.send(to=to, subject=subject, body=body)
    except ConnectionError as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 60)

@app.task(bind=True, rate_limit='10/m')
def process_image(self, image_url: str, user_id: int):
    image = download_image(image_url)
    result = transform_image(image)
    upload_result(result, user_id)
    return {'status': 'completed', 'user_id': user_id}

@app.task
def generate_report(report_type: str, date_range: str):
    data = fetch_data(report_type, date_range)
    report = build_report(data)
    upload_to_s3(report)
    notify_users(report_type)
```

## Best Practices

- Always use idempotency keys for tasks with side effects
- Implement retry with exponential backoff and jitter
- Use separate queues for different task priorities and types
- Set appropriate task time limits to prevent stuck workers
- Monitor worker health and queue depths continuously
- Use `acks_late=True` for at-least-once delivery guarantees
- Implement dead letter queues for manual inspection of failures
- Use rate limiting to protect downstream services
- Implement graceful shutdown with task draining
- Log structured data with task IDs for traceability

## Related Modules

- `celery` — Python distributed task queue
- `bullmq` — Node.js Redis-based job queue
- `dramatiq` — Python task queue with actor model
- `redis-queue` — Lightweight Python job queue
- `flower` — Celery monitoring tool

---

## Advanced Configuration

### Celery Production Configuration

```python
# celery_config.py
import os
from celery import Celery
from celery.schedules import crontab

app = Celery('production')

# Broker and backend
app.config_from_object({
    'broker_url': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    'result_backend': os.getenv('REDIS_URL', 'redis://localhost:6379/1'),
    'result_backend_transport_options': {
        'visibility_timeout': 43200,  # 12 hours
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
    },

    # Serialization
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],

    # Time
    'timezone': 'UTC',
    'enable_utc': True,

    # Task execution
    'task_track_started': True,
    'task_acks_late': True,
    'task_reject_on_worker_lost': True,
    'task_acks_on_failure': False,
    'worker_prefetch_multiplier': 1,
    'worker_max_tasks_per_child': 1000,
    'worker_max_memory_per_child': 500000,  # 500MB

    # Time limits
    'task_soft_time_limit': 300,  # 5 minutes
    'task_time_limit': 600,       # 10 minutes

    # Retry
    'task_default_retry_delay': 60,
    'task_max_retries': 3,

    # Queue routing
    'task_routes': {
        'myapp.tasks.email.*': {'queue': 'email'},
        'myapp.tasks.report.*': {'queue': 'reports'},
        'myapp.tasks.image.*': {'queue': 'media'},
        'myapp.tasks.payment.*': {'queue': 'critical'},
    },

    # Queue definitions
    'task_queues': {
        'default': {'exchange': 'default', 'routing_key': 'default'},
        'email': {'exchange': 'email', 'routing_key': 'email'},
        'reports': {'exchange': 'reports', 'routing_key': 'reports'},
        'media': {'exchange': 'media', 'routing_key': 'media'},
        'critical': {'exchange': 'critical', 'routing_key': 'critical'},
    },

    # Beat schedule
    'beat_schedule': {
        'cleanup-sessions': {
            'task': 'myapp.tasks.cleanup_expired_sessions',
            'schedule': crontab(hour=3, minute=0),
            'options': {'queue': 'default'},
        },
        'generate-reports': {
            'task': 'myapp.tasks.generate_daily_reports',
            'schedule': crontab(hour=6, minute=0),
            'options': {'queue': 'reports'},
        },
        'sync-payments': {
            'task': 'myapp.tasks.sync_payment_status',
            'schedule': crontab(minute='*/5'),  # Every 5 minutes
            'options': {'queue': 'critical'},
        },
    },
})
```

### BullMQ Configuration

```typescript
// queue.config.ts
import { Queue, Worker, QueueEvents } from 'bullmq';
import Redis from 'ioredis';

const connection = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  maxRetriesPerRequest: null,
  enableReadyCheck: false,
});

// Queue definitions
export const emailQueue = new Queue('email', {
  connection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 1000,
    },
    removeOnComplete: { age: 86400 },  // 24 hours
    removeOnFail: { age: 604800 },     // 7 days
  },
});

export const reportQueue = new Queue('reports', { connection });
export const mediaQueue = new Queue('media', { connection });

// Worker definitions
export const emailWorker = new Worker(
  'email',
  async (job) => {
    const { to, subject, body } = job.data;
    await emailService.send({ to, subject, body });
    return { success: true, messageId: result.id };
  },
  {
    connection,
    concurrency: 5,
    limiter: {
      max: 10,
      duration: 60000,  // 10 jobs per minute
    },
  }
);

// Job event handlers
emailWorker.on('completed', (job) => {
  console.log(`Email job ${job.id} completed`);
});

emailWorker.on('failed', (job, err) => {
  console.error(`Email job ${job?.id} failed:`, err.message);
});

// Scheduled jobs with node-cron
import cron from 'node-cron';

cron.schedule('0 3 * * *', async () => {
  await reportQueue.add('cleanup-sessions', {
    type: 'cleanup',
    olderThan: '24h',
  });
});

cron.schedule('0 6 * * *', async () => {
  await reportQueue.add('daily-report', {
    type: 'daily',
    date: new Date().toISOString().split('T')[0],
  });
});
```

### Dramatiq Configuration

```python
# dramatiq_config.py
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import (
    AgeLimit,
    TimeLimit,
    ShutdownNotify,
    Callbacks,
    Pipelines,
    Retries,
)
from dramatiq.rate_limits import SlidingWindowLimiter

broker = RedisBroker(url='redis://localhost:6379/0')
dramatiq.set_broker(broker)

# Add middleware
broker.add_middleware(AgeLimit())
broker.add_middleware(TimeLimit(max_time=300000))  # 5 minutes
broker.add_middleware(ShutdownNotify())
broker.add_middleware(Callbacks())
broker.add_middleware(Pipelines())
broker.add_middleware(Retries(max_retries=3))

@dramatiq.actor(max_retries=3, min_backoff=1000, max_backoff=60000)
def send_email(to: str, subject: str, body: str):
    email_service.send(to=to, subject=subject, body=body)

@dramatiq.actor(priority=0, max_retries=5)
def process_payment(payment_id: int):
    payment = Payment.get(payment_id)
    payment.process()

@dramatiq.actor(queue_name='reports')
def generate_report(report_type: str):
    data = fetch_data(report_type)
    build_and_upload_report(data)
```

---

## Architecture Patterns

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Web Server / API                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │  │
│  │  │  REST    │  │  GraphQL │  │  WebSocket   │  │  │
│  │  │  API     │  │  API     │  │  Server      │  │  │
│  │  └────┬─────┘  └────┬─────┘  └──────┬───────┘  │  │
│  └───────┼──────────────┼───────────────┼───────────┘  │
│          │              │               │               │
│          ▼              ▼               ▼               │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Task Dispatch Layer                     │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │  │
│  │  │  Enqueue    │  │  Priority  │  │  Delay     │ │  │
│  │  │  Tasks      │  │  Queue     │  │  Schedule  │ │  │
│  │  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘ │  │
│  └─────────┼───────────────┼───────────────┼─────────┘  │
└────────────┼───────────────┼───────────────┼─────────────┘
             │               │               │
             ▼               ▼               ▼
┌─────────────────────────────────────────────────────────┐
│                  Message Broker (Redis)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ default  │  │ critical │  │ email    │              │
│  │  queue   │  │  queue   │  │  queue   │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │              │              │                     │
│  ┌────┴──────────────┴──────────────┴────┐              │
│  │          Dead Letter Queue             │              │
│  └───────────────────────────────────────┘              │
└──────────────────┬──────────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┬──────────────┐
    │              │              │              │
    ▼              ▼              ▼              ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│Worker 1│  │Worker 2│  │Worker 3│  │Worker 4│
│(email) │  │(default│  │(reports│  │(critical│
│        │  │        │  │        │  │        │
└───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘
    │           │            │            │
    ▼           ▼            ▼            ▼
┌─────────────────────────────────────────────────┐
│              External Services                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  Email   │  │  Storage │  │  Payment     │  │
│  │  API     │  │  (S3)    │  │  Gateway     │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└─────────────────────────────────────────────────┘

Job Lifecycle:

  Enqueue ──► Pending ──► Active ──► Completed
                  │            │
                  │            ├──► Retry (max attempts)
                  │            │
                  │            └──► Failed ──► Dead Letter Queue
                  │
                  └──► Delayed (scheduled/retry backoff)
```

### Retry and Dead Letter Flow

```
Task Execution Attempt:

  ┌──────────────┐
  │  Start Task  │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐     ┌─────────────────┐
  │   Execute    │────►│   Success       │
  │   Task       │     │   (Complete)    │
  └──────┬───────┘     └─────────────────┘
         │ Error
         ▼
  ┌──────────────┐
  │  Retry Left? │
  └──────┬───────┘
    Yes  │   No
    │    │    │
    ▼    │    ▼
  ┌──────┴──┐  ┌──────────────────┐
  │ Exponential│  │  Dead Letter    │
  │ Backoff   │  │  Queue          │
  │ + Jitter  │  │  (Manual Review)│
  └─────────┘  └──────────────────┘

Retry Timing:

  Attempt 1: immediate
  Attempt 2: 60s + random(0-30s)
  Attempt 3: 120s + random(0-60s)
  Attempt 4: 240s + random(0-120s)
  ...
```

---

## Integration Guide

### Celery with SQLAlchemy

```python
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Celery('myapp')
app.config_from_object('celery_config')

# Database setup per worker
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@app.task(bind=True)
def process_order(self, order_id: int):
    session = SessionLocal()
    try:
        order = session.query(Order).get(order_id)
        if not order:
            return {'error': 'Order not found'}

        # Process order
        order.status = 'processing'
        session.commit()

        result = payment_service.charge(order.total)
        order.status = 'paid'
        session.commit()

        return {'order_id': order_id, 'status': 'paid'}
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
```

### Idempotency Keys

```python
import uuid
import hashlib
from functools import wraps

def idempotent(task_func):
    """Decorator for idempotent task execution"""
    @wraps(task_func)
    def wrapper(*args, **kwargs):
        # Generate idempotency key from function name + args
        key_data = f"{task_func.__name__}:{args}:{sorted(kwargs.items())}"
        idempotency_key = hashlib.sha256(key_data.encode()).hexdigest()

        # Check if already processed
        cache_key = f"idempotent:{idempotency_key}"
        if redis_client.exists(cache_key):
            return redis_client.get(cache_key)

        # Execute and cache result
        result = task_func(*args, **kwargs)
        redis_client.setex(cache_key, 86400, result)  # Cache for 24 hours
        return result

    return wrapper

@app.task
@idempotent
def charge_payment(user_id: int, amount: float, idempotency_key: str = None):
    # Use provided idempotency key or generate one
    key = idempotency_key or str(uuid.uuid4())

    # Check if payment already processed
    existing = Payment.query.filter_by(idempotency_key=key).first()
    if existing:
        return {'status': 'already_processed', 'payment_id': existing.id}

    # Process payment
    payment = Payment(user_id=user_id, amount=amount, idempotency_key=key)
    payment.process()
    return {'status': 'completed', 'payment_id': payment.id}
```

### Distributed Locking

```python
import redis
import time
from contextlib import contextmanager

class DistributedLock:
    def __init__(self, redis_client, lock_name, timeout=10, blocking_timeout=60):
        self.redis = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.timeout = timeout
        self.blocking_timeout = blocking_timeout
        self.lock_value = None

    def acquire(self):
        self.lock_value = str(uuid.uuid4())
        end_time = time.time() + self.blocking_timeout

        while time.time() < end_time:
            if self.redis.set(
                self.lock_name,
                self.lock_value,
                nx=True,
                ex=self.timeout,
            ):
                return True
            time.sleep(0.1)
        return False

    def release(self):
        if self.lock_value:
            # Lua script for atomic check-and-delete
            script = """
            if redis.call("get", KEYS[1]) == ARGV[1] then
                return redis.call("del", KEYS[1])
            else
                return 0
            end
            """
            self.redis.eval(script, 1, self.lock_name, self.lock_value)
            self.lock_value = None

    def __enter__(self):
        if not self.acquire():
            raise TimeoutError(f"Could not acquire lock: {self.lock_name}")
        return self

    def __exit__(self, *args):
        self.release()

# Usage
@app.task
def sync_inventory(product_id: int):
    with DistributedLock(redis_client, f"inventory:{product_id}") as lock:
        # Only one worker processes this product at a time
        inventory = inventory_service.get(product_id)
        updated = inventory_service.sync(inventory)
        return {'synced': updated}
```

---

## Performance Optimization

| Technique | Impact | When to Use |
|-----------|--------|-------------|
| Worker concurrency tuning | 2-5x throughput | CPU-bound vs I/O-bound tasks |
| Batch processing | 10-50x throughput | High-volume simple tasks |
| Prefetch tuning | Reduced memory usage | Workers with large tasks |
| Result backend TTL | Reduced Redis memory | Don't keep results forever |
| Separate queues | Better resource isolation | Different task priorities |
| Rate limiting | Protection for downstream | API calls, external services |
| Task compression | Reduced broker bandwidth | Large task payloads |
| Worker pooling | Better resource utilization | Heterogeneous workloads |

### Worker Tuning

```bash
# Celery worker tuning
celery -A myapp worker \
  --concurrency=4 \           # CPU-bound: 2x cores; I/O-bound: 4-8x cores
  --prefetch-multiplier=1 \   # One task at a time for large tasks
  --max-tasks-per-child=1000 \ # Prevent memory leaks
  --max-memory-per-child=500000 \  # 500MB limit
  -Q default,email,reports \  # Queue subscription
  --without-gossip \          # Reduce overhead for many workers
  --without-mingle            # Reduce startup overhead
```

### Batch Processing

```python
@app.task(bind=True)
def batch_process_users(self, user_ids: list[int]):
    """Process multiple users in a single task"""
    session = SessionLocal()
    try:
        users = session.query(User).filter(User.id.in_(user_ids)).all()
        results = []

        for user in users:
            try:
                result = process_user(user)
                results.append({'user_id': user.id, 'status': 'success'})
            except Exception as e:
                results.append({'user_id': user.id, 'status': 'failed', 'error': str(e)})

        return {'processed': len(results), 'results': results}
    finally:
        session.close()

# Enqueue in batches
def enqueue_batch(tasks: list, batch_size: int = 100):
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        batch_process_users.delay(batch)
```

---

## Security Considerations

- Never execute arbitrary code from job payloads; validate all inputs
- Use encrypted connections (TLS) for broker communication
- Implement job-level authentication for sensitive operations
- Log all job executions with user context for audit trail
- Use secrets management (Vault, AWS Secrets Manager) for credentials
- Restrict worker permissions to minimum required
- Implement rate limiting to prevent abuse
- Sanitize job payloads to prevent injection attacks
- Use separate queues for sensitive vs non-sensitive jobs
- Rotate broker credentials regularly

### Secure Task Execution

```python
import hmac
import hashlib

def sign_task(task_name: str, payload: dict, secret: str) -> str:
    """Create HMAC signature for task payload"""
    message = f"{task_name}:{json.dumps(payload, sort_keys=True)}"
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

def verify_task_signature(task_name: str, payload: dict, signature: str, secret: str) -> bool:
    """Verify task payload signature"""
    expected = sign_task(task_name, payload, secret)
    return hmac.compare_digest(expected, signature)

@app.task
def sensitive_operation(user_id: int, action: str, _signature: str = None):
    # Verify signature
    if not verify_task_signature(
        'sensitive_operation',
        {'user_id': user_id, 'action': action},
        _signature,
        TASK_SECRET,
    ):
        raise SecurityError("Invalid task signature")

    # Execute operation
    return perform_operation(user_id, action)
```

---

## Troubleshooting Guide

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| Tasks stuck in PENDING | Worker not connected to broker | Check broker URL and worker startup |
| Tasks in RETRY repeatedly | Task always failing | Check task logic, fix root cause |
| Worker memory growing | Memory leak in task | Use `max_memory_per_child` limit |
| Tasks executing twice | `acks_late=True` without idempotency | Add idempotency keys |
| Queue depth growing | Workers too slow or too few | Add workers or optimize tasks |
| Worker crashes | Unhandled exception | Add try/except, check worker logs |
| Rate limit exceeded | Too many tasks | Increase rate limit or add delays |
| Redis memory full | Too many results stored | Set result TTL, clear old results |
| Beat schedule missed | Beat process not running | Run beat as separate process |
| Dead letter queue full | Systemic task failures | Investigate DLQ, fix root cause |
| Task latency high | Worker busy or queue full | Tune concurrency, add workers |

### Debugging Checklist

```bash
# Check worker status
celery -A myapp inspect active
celery -A myapp inspect reserved
celery -A myapp inspect stats

# Check queue depths
celery -A myapp inspect active_queues

# Check registered tasks
celery -A myapp inspect registered

# Monitor events
celery -A myapp events

# Flower monitoring
celery -A myapp flower --port=5555

# Purge stuck tasks
celery -A myapp purge

# Check Redis queues
redis-cli LLEN celery
redis-cli LLEN email
```

---

## API Reference

### Task Decorator Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `bind` | bool | False | Task receives `self` as first argument |
| `max_retries` | int | 3 | Maximum retry attempts |
| `default_retry_delay` | int | 60 | Seconds between retries |
| `rate_limit` | str | None | Rate limit (e.g., '10/m', '100/h') |
| `time_limit` | int | None | Hard time limit in seconds |
| `soft_time_limit` | int | None | Soft time limit (raises SoftTimeLimitExceeded) |
| `queue` | str | 'default' | Queue to route task to |
| `priority` | int | None | Task priority (0=highest, 9=lowest) |
| `acks_late` | bool | False | Ack after completion (at-least-once) |
| `ignore_result` | bool | False | Don't store task result |

### Worker CLI Options

| Option | Description |
|--------|-------------|
| `--concurrency=N` | Number of worker processes/threads |
| `--prefetch-multiplier=N` | Tasks prefetched per worker process |
| `--max-tasks-per-child=N` | Restart worker after N tasks |
| `--max-memory-per-child=N` | Restart worker after N bytes |
| `--queues=Q1,Q2` | Subscribe to specific queues |
| `--hostname=NAME` | Worker hostname for monitoring |
| `--without-gossip` | Disable gossip protocol |
| `--without-mingle` | Disable worker synchronization |
| `-O fair` | Fair scheduling across queues |

---

## Data Models

### Task State Model

```python
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class TaskState(str, Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RETRY = "RETRY"
    REVOKED = "REVOKED"

class TaskInfo(BaseModel):
    task_id: str
    task_name: str
    state: TaskState
    args: list
    kwargs: dict
    queue: str
    worker: str | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    retries: int
    result: dict | None
    error: str | None

class QueueInfo(BaseModel):
    name: str
    depth: int
    consumers: int
    message_rate: float
    workers: list[str]

class WorkerInfo(BaseModel):
    hostname: str
    status: str
    active_tasks: int
    reserved_tasks: int
    pool: str
    concurrency: int
    pid: int
```

### Job Configuration

```python
class JobConfig(BaseModel):
    task_name: str
    queue: str = "default"
    priority: int = 5
    max_retries: int = 3
    retry_delay: int = 60
    time_limit: int = 300
    rate_limit: str | None = None
    idempotency_key: str | None = None
    metadata: dict = {}
```

---

## Deployment Guide

### Docker Compose

```yaml
version: "3.9"
services:
  # Celery Worker
  celery-worker:
    build: .
    command: celery -A myapp worker -l info -c 4 -Q default,email,reports
    environment:
      - REDIS_URL=redis://redis:6379/0
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      redis:
        condition: service_healthy
      db:
        condition: service_healthy

  # Celery Beat (scheduler)
  celery-beat:
    build: .
    command: celery -A myapp beat -l info
    environment:
      - REDIS_URL=redis://redis:6379/0

  # Flower (monitoring)
  flower:
    build: .
    command: celery -A myapp flower --port=5555
    ports:
      - "5555:5555"
    environment:
      - REDIS_URL=redis://redis:6379/0

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celery-worker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: celery-worker
  template:
    metadata:
      labels:
        app: celery-worker
    spec:
      containers:
        - name: worker
          image: registry.example.com/myapp-worker:2.0.0
          command: ["celery", "-A", "myapp", "worker", "-l", "info", "-c", "4"]
          env:
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: worker-secrets
                  key: redis-url
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: worker-secrets
                  key: database-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"

---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: celery-beat
spec:
  schedule: "0 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: beat
              image: registry.example.com/myapp-worker:2.0.0
              command: ["celery", "-A", "myapp", "beat", "-l", "info"]
          restartPolicy: OnFailure
```

---

## Monitoring and Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, Info

task_total = Counter(
    'celery_tasks_total',
    'Total tasks executed',
    ['task_name', 'status'],
)

task_duration = Histogram(
    'celery_task_duration_seconds',
    'Task execution duration',
    ['task_name'],
    buckets=[0.1, 0.5, 1, 5, 10, 30, 60, 300],
)

active_tasks = Gauge(
    'celery_active_tasks',
    'Currently executing tasks',
    ['worker'],
)

queue_depth = Gauge(
    'celery_queue_depth',
    'Number of tasks in queue',
    ['queue'],
)

# Task signal handlers
from celery.signals import task_prerun, task_postrun, task_failure

@task_prerun.connect
def task_prerun_handler(sender, task_id, task, **kwargs):
    active_tasks.labels(worker=sender.hostname).inc()
    task_total.labels(task_name=task.name, status='started').inc()

@task_postrun.connect
def task_postrun_handler(sender, task_id, task, retval, **kwargs):
    active_tasks.labels(worker=sender.hostname).dec()
    task_total.labels(task_name=task.name, status='success').inc()

@task_failure.connect
def task_failure_handler(sender, task_id, exception, **kwargs):
    task_total.labels(task_name=sender.name, status='failure').inc()
```

### Structured Logging

```python
import structlog
import uuid

logger = structlog.get_logger()

@app.task(bind=True)
def process_order(self, order_id: int):
    task_id = self.request.id
    log = logger.bind(task_id=task_id, order_id=order_id)

    log.info("task_started", task_name="process_order")

    try:
        order = Order.query.get(order_id)
        if not order:
            log.warning("order_not_found")
            return {'error': 'Order not found'}

        payment = payment_service.charge(order.total)
        log.info("payment_processed", amount=order.total, payment_id=payment.id)

        order.status = 'paid'
        db.session.commit()

        log.info("task_completed")
        return {'order_id': order_id, 'payment_id': payment.id}

    except Exception as e:
        log.error("task_failed", error=str(e))
        raise
```

### Health Checks

```python
from celery import Celery
from redis import Redis

def check_celery_health(app: Celery) -> dict:
    """Check Celery worker health"""
    stats = app.control.inspect(timeout=5.0).stats()
    if not stats:
        return {'status': 'unhealthy', 'reason': 'No workers responding'}

    active = app.control.inspect(timeout=5.0).active()
    reserved = app.control.inspect(timeout=5.0).reserved()

    return {
        'status': 'healthy',
        'workers': len(stats),
        'active_tasks': sum(len(t) for t in (active or {}).values()),
        'reserved_tasks': sum(len(t) for t in (reserved or {}).values()),
    }

def check_redis_health(redis_url: str) -> dict:
    """Check Redis broker health"""
    try:
        r = Redis.from_url(redis_url)
        r.ping()
        info = r.info('memory')
        return {
            'status': 'healthy',
            'memory_used': info['used_memory_human'],
            'memory_peak': info['used_memory_peak_human'],
        }
    except Exception as e:
        return {'status': 'unhealthy', 'reason': str(e)}
```

---

## Testing Strategy

### Unit Tests

```python
import pytest
from celery import Celery
from myapp.tasks import send_email, process_order

@pytest.fixture
def celery_app():
    app = Celery('test')
    app.config_from_object({
        'broker_url': 'memory://',
        'result_backend': 'cache+memory://',
    })
    return app

@pytest.fixture
def celery_worker(celery_app):
    worker = celery_app.Worker(include=['myapp.tasks'])
    worker.start()
    yield worker
    worker.stop()

def test_send_email(celery_app, celery_worker):
    result = send_email.delay(
        to='test@example.com',
        subject='Test',
        body='Hello',
    )
    assert result.get(timeout=10) == {'status': 'sent'}

def test_process_order(celery_app, celery_worker):
    order = create_test_order()
    result = process_order.delay(order.id)
    assert result.get(timeout=10)['order_id'] == order.id
```

### Integration Tests

```python
import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.integration
def test_order_processing_pipeline(celery_app, celery_worker):
    """Test full order processing pipeline"""
    order = create_test_order()

    with patch('myapp.services.payment_service.charge') as mock_charge:
        mock_charge.return_value = MagicMock(id='pay_123')

        result = process_order.delay(order.id)
        output = result.get(timeout=30)

        assert output['status'] == 'paid'
        assert output['payment_id'] == 'pay_123'

        # Verify database state
        updated_order = Order.query.get(order.id)
        assert updated_order.status == 'paid'

@pytest.mark.integration
def test_retry_on_failure(celery_app, celery_worker):
    """Test task retries on failure"""
    call_count = 0

    @celery_app.task(bind=True)
    def flaky_task(self):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Temporary failure")
        return "success"

    result = flaky_task.delay()
    assert result.get(timeout=30) == "success"
    assert call_count == 3
```

---

## Versioning and Migration

### Task Versioning

```python
# Version tasks with naming convention
# v1: myapp.tasks.process_order_v1
# v2: myapp.tasks.process_order_v2

# Router handles version routing
app.conf.task_routes = {
    'myapp.tasks.process_order_v1': {'queue': 'legacy'},
    'myapp.tasks.process_order_v2': {'queue': 'default'},
}

# Gradual migration: run both versions
# Monitor v2, then remove v1
```

### Migration Checklist

```markdown
## Background Job Migration Checklist

- [ ] Export existing task definitions and schedules
- [ ] Document queue topology and routing rules
- [ ] Backup Redis broker data
- [ ] Deploy new worker code alongside old
- [ ] Verify new workers process tasks correctly
- [ ] Update task routing to new queues
- [ ] Monitor error rates during migration
- [ ] Remove old worker processes
- [ ] Clean up old queue definitions
- [ ] Update monitoring dashboards
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **Broker** | Message broker (Redis, RabbitMQ) that stores and distributes tasks |
| **Worker** | Process that polls the broker for tasks and executes them |
| **Beat** | Scheduler process that enqueues periodic tasks on cron schedules |
| **Dead Letter Queue** | Queue for tasks that exceeded max retries |
| **Idempotency** | Property ensuring task produces same result when executed multiple times |
| **Prefetch** | Number of tasks a worker pulls from the broker in advance |
| **Ack Late** | Acknowledging task after completion rather than when received |
| **Rate Limit** | Maximum tasks per time period for a task type |
| **Circuit Breaker** | Pattern to stop calling failing downstream services |
| **Backoff** | Increasing delay between retry attempts |

---

## Changelog

### 2.0.0 (2024-12-01)

- Added BullMQ and Dramatiq patterns alongside Celery
- Added distributed locking patterns
- Added idempotency key implementation
- Added rate limiting per task type
- Added batch processing patterns
- Added Prometheus metrics integration
- Added Kubernetes CronJob deployment

### 1.1.0 (2024-06-15)

- Added dead letter queue configuration
- Added retry with exponential backoff
- Added Flower monitoring setup
- Added Docker Compose deployment

### 1.0.0 (2024-01-01)

- Initial release
- Core Celery patterns
- Basic task definitions
- Queue routing

---

## Contributing Guidelines

1. Fork the repository and create a feature branch
2. Follow the existing code patterns
3. Add tests for new patterns (target: 85% coverage)
4. Update this document for any new patterns
5. Verify task execution with integration tests
6. Submit a pull request with a clear description

### Code Style

- Use type hints for task arguments
- Add docstrings to all task functions
- Handle exceptions explicitly in tasks
- Log structured data with task IDs
- Use separate queues for different concerns
- Keep tasks focused and single-purpose

---

## License

MIT License. See [LICENSE](LICENSE) for details.
