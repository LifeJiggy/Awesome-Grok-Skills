---
name: Build Configuration for Grok Applications
category: infrastructure
version: "1.0"
tags:
  - grok
  - xai
  - build
  - deployment
  - configuration
  - infrastructure
  - devops
  - optimization
description: Build configuration guide for Grok applications — setup, deployment, optimization, and production best practices.
---

# Build Configuration for Grok Applications

## Overview

This guide covers the complete build configuration lifecycle for applications using Grok models — from initial project setup through production deployment and optimization. Whether you're building a simple API wrapper, a real-time chat application, or an enterprise AI platform, this document provides the configuration patterns and best practices you need.

## Project Setup

### Directory Structure

```
grok-application/
├── .env                          # Environment variables (never commit)
├── .env.example                  # Template for environment variables
├── .env.production               # Production-specific overrides
├── config/
│   ├── default.ts                # Default configuration
│   ├── production.ts             # Production overrides
│   ├── development.ts            # Development overrides
│   └── types.ts                  # Configuration type definitions
├── src/
│   ├── client/
│   │   ├── grok-client.ts        # Grok API client wrapper
│   │   ├── middleware.ts         # Request/response middleware
│   │   └── cache.ts              # Response caching layer
│   ├── services/
│   │   ├── chat.ts               # Chat service
│   │   ├── completion.ts         # Completion service
│   │   └── vision.ts             # Vision/multimodal service
│   ├── utils/
│   │   ├── token-counter.ts      # Token counting utility
│   │   ├── rate-limiter.ts       # Rate limiting
│   │   └── retry.ts              # Retry logic with backoff
│   └── index.ts                  # Application entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── package.json
├── tsconfig.json
└── README.md
```

### Package Installation

```bash
# Core dependencies
npm install openai dotenv
npm install -D typescript @types/node tsx

# Optional: caching and rate limiting
npm install ioredis bull

# Optional: monitoring
npm install prom-client @opentelemetry/api

# Optional: validation
npm install zod
```

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "paths": {
      "@/*": ["./src/*"]
    },
    "types": ["node"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

## Environment Configuration

### Environment Variables

```bash
# .env.example

# Required: API Configuration
XAI_API_KEY=xai-your-api-key-here
GROK_MODEL=grok-4-5

# Optional: API Configuration
GROK_BASE_URL=https://api.x.ai/v1
GROK_MAX_TOKENS=4096
GROK_TEMPERATURE=0.7
GROK_TIMEOUT_MS=60000

# Optional: Application Configuration
APP_ENV=development
APP_PORT=3000
APP_LOG_LEVEL=info

# Optional: Caching (Redis)
REDIS_URL=redis://localhost:6379
CACHE_TTL_SECONDS=3600
CACHE_MAX_SIZE=10000

# Optional: Rate Limiting
RATE_LIMIT_RPM=60
RATE_LIMIT_TPM=500000

# Optional: Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090

# Optional: Security
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
API_KEY_HEADER=X-API-Key
```

### Type-Safe Configuration

```typescript
// config/types.ts
import { z } from 'zod';

const ConfigSchema = z.object({
  grok: z.object({
    apiKey: z.string().min(1, 'XAI_API_KEY is required'),
    baseUrl: z.string().url().default('https://api.x.ai/v1'),
    model: z.string().default('grok-4-5'),
    maxTokens: z.number().int().min(1).max(32768).default(4096),
    temperature: z.number().min(0).max(2).default(0.7),
    timeoutMs: z.number().int().min(1000).max(300000).default(60000),
  }),
  app: z.object({
    env: z.enum(['development', 'staging', 'production']).default('development'),
    port: z.number().int().min(1).max(65535).default(3000),
    logLevel: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  }),
  cache: z.object({
    enabled: z.boolean().default(false),
    redisUrl: z.string().url().optional(),
    ttlSeconds: z.number().int().min(0).default(3600),
    maxSize: z.number().int().min(0).default(10000),
  }),
  rateLimit: z.object({
    rpm: z.number().int().min(1).default(60),
    tpm: z.number().int().min(1).default(500000),
  }),
  security: z.object({
    allowedOrigins: z.array(z.string()).default(['http://localhost:3000']),
    apiKeyHeader: z.string().default('X-API-Key'),
  }),
});

export type Config = z.infer<typeof ConfigSchema>;

// config/default.ts
import dotenv from 'dotenv';
import { ConfigSchema } from './types';

dotenv.config();

export const config = ConfigSchema.parse({
  grok: {
    apiKey: process.env.XAI_API_KEY,
    baseUrl: process.env.GROK_BASE_URL,
    model: process.env.GROK_MODEL,
    maxTokens: process.env.GROK_MAX_TOKENS ? parseInt(process.env.GROK_MAX_TOKENS) : undefined,
    temperature: process.env.GROK_TEMPERATURE ? parseFloat(process.env.GROK_TEMPERATURE) : undefined,
    timeoutMs: process.env.GROK_TIMEOUT_MS ? parseInt(process.env.GROK_TIMEOUT_MS) : undefined,
  },
  app: {
    env: process.env.APP_ENV,
    port: process.env.APP_PORT ? parseInt(process.env.APP_PORT) : undefined,
    logLevel: process.env.APP_LOG_LEVEL,
  },
  cache: {
    enabled: process.env.REDIS_URL !== undefined,
    redisUrl: process.env.REDIS_URL,
    ttlSeconds: process.env.CACHE_TTL_SECONDS ? parseInt(process.env.CACHE_TTL_SECONDS) : undefined,
    maxSize: process.env.CACHE_MAX_SIZE ? parseInt(process.env.CACHE_MAX_SIZE) : undefined,
  },
  rateLimit: {
    rpm: process.env.RATE_LIMIT_RPM ? parseInt(process.env.RATE_LIMIT_RPM) : undefined,
    tpm: process.env.RATE_LIMIT_TPM ? parseInt(process.env.RATE_LIMIT_TPM) : undefined,
  },
  security: {
    allowedOrigins: process.env.ALLOWED_ORIGINS?.split(','),
    apiKeyHeader: process.env.API_KEY_HEADER,
  },
});
```

## Client Configuration

### Grok Client Wrapper

```typescript
// src/client/grok-client.ts
import OpenAI from 'openai';
import { config } from '../../config';

export class GrokClient {
  private client: OpenAI;
  private requestCount = 0;
  private tokenCount = 0;

  constructor() {
    this.client = new OpenAI({
      apiKey: config.grok.apiKey,
      baseURL: config.grok.baseUrl,
      timeout: config.grok.timeoutMs,
      maxRetries: 3,
    });
  }

  async chat(
    messages: OpenAI.ChatCompletionMessageParam[],
    options: Partial<OpenAI.ChatCompletionCreateParams> = {}
  ): Promise<OpenAI.ChatCompletion> {
    return this.client.chat.completions.create({
      model: options.model || config.grok.model,
      messages,
      max_tokens: options.max_tokens || config.grok.maxTokens,
      temperature: options.temperature ?? config.grok.temperature,
      ...options,
    });
  }

  async chatStream(
    messages: OpenAI.ChatCompletionMessageParam[],
    options: Partial<OpenAI.ChatCompletionCreateParams> = {}
  ): Promise<AsyncIterable<OpenAI.ChatCompletionChunk>> {
    return this.client.chat.completions.create({
      model: options.model || config.grok.model,
      messages,
      max_tokens: options.max_tokens || config.grok.maxTokens,
      temperature: options.temperature ?? config.grok.temperature,
      stream: true,
      ...options,
    });
  }

  getMetrics() {
    return {
      requestCount: this.requestCount,
      tokenCount: this.tokenCount,
    };
  }
}

export const grokClient = new GrokClient();
```

### Middleware

```typescript
// src/client/middleware.ts
import { GrokClient } from './grok-client';

type MessageInterceptor = (messages: any[]) => any[];
type ResponseInterceptor = (response: any) => any;

export class GrokMiddleware {
  private requestInterceptors: MessageInterceptor[] = [];
  private responseInterceptors: ResponseInterceptor[] = [];

  addRequestInterceptor(interceptor: MessageInterceptor) {
    this.requestInterceptors.push(interceptor);
  }

  addResponseInterceptor(interceptor: ResponseInterceptor) {
    this.responseInterceptors.push(interceptor);
  }

  async chat(client: GrokClient, messages: any[], options: any = {}) {
    // Apply request interceptors
    let processedMessages = messages;
    for (const interceptor of this.requestInterceptors) {
      processedMessages = interceptor(processedMessages);
    }

    // Make the API call
    const response = await client.chat(processedMessages, options);

    // Apply response interceptors
    let processedResponse = response;
    for (const interceptor of this.responseInterceptors) {
      processedResponse = interceptor(processedResponse);
    }

    return processedResponse;
  }
}

// Usage
const middleware = new GrokMiddleware();

// Add token counting interceptor
middleware.addRequestInterceptor((messages) => {
  const totalTokens = estimateTokens(messages);
  if (totalTokens > 100000) {
    console.warn(`High token count: ${totalTokens}`);
  }
  return messages;
});

// Add logging interceptor
middleware.addResponseInterceptor((response) => {
  console.log(`Model: ${response.model}, Tokens: ${response.usage?.total_tokens}`);
  return response;
});
```

### Response Caching

```typescript
// src/client/cache.ts
import Redis from 'ioredis';
import { createHash } from 'crypto';
import { config } from '../../config';

export class ResponseCache {
  private redis: Redis | null = null;
  private memoryCache: Map<string, { data: any; expiry: number }> = new Map();

  constructor() {
    if (config.cache.enabled && config.cache.redisUrl) {
      this.redis = new Redis(config.cache.redisUrl);
    }
  }

  private generateKey(messages: any[], options: any): string {
    const payload = JSON.stringify({ messages, options });
    return `grok:cache:${createHash('sha256').update(payload).digest('hex')}`;
  }

  async get(messages: any[], options: any): Promise<any | null> {
    const key = this.generateKey(messages, options);

    // Check memory cache first
    const memEntry = this.memoryCache.get(key);
    if (memEntry && memEntry.expiry > Date.now()) {
      return memEntry.data;
    }

    // Check Redis
    if (this.redis) {
      const data = await this.redis.get(key);
      if (data) {
        const parsed = JSON.parse(data);
        this.memoryCache.set(key, { data: parsed, expiry: Date.now() + config.cache.ttlSeconds * 1000 });
        return parsed;
      }
    }

    return null;
  }

  async set(messages: any[], options: any, response: any): Promise<void> {
    const key = this.generateKey(messages, options);
    const serialized = JSON.stringify(response);

    // Store in memory
    this.memoryCache.set(key, {
      data: response,
      expiry: Date.now() + config.cache.ttlSeconds * 1000,
    });

    // Store in Redis
    if (this.redis) {
      await this.redis.setex(key, config.cache.ttlSeconds, serialized);
    }
  }

  async invalidate(pattern: string): Promise<void> {
    if (this.redis) {
      const keys = await this.redis.keys(`grok:cache:${pattern}*`);
      if (keys.length > 0) {
        await this.redis.del(...keys);
      }
    }
    // Clear matching memory entries
    for (const [key] of this.memoryCache) {
      if (key.includes(pattern)) {
        this.memoryCache.delete(key);
      }
    }
  }
}
```

## Docker Configuration

### Production Dockerfile

```dockerfile
# docker/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY tsconfig.json ./
COPY src/ ./src/
RUN npx tsc

FROM node:20-alpine AS runtime

RUN apk add --no-cache dumb-init
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001 -G appgroup

WORKDIR /app
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/package.json ./

USER appuser
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/index.js"]
```

### Docker Compose

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - XAI_API_KEY=${XAI_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      redis:
        condition: service_healthy
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app

volumes:
  redis_data:
```

### Nginx Configuration

```nginx
# docker/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream grok_app {
        server app:3000;
    }

    # Rate limiting zone
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" $request_time';

    server {
        listen 80;
        server_name yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com;

        ssl_certificate /etc/nginx/certs/fullchain.pem;
        ssl_certificate_key /etc/nginx/certs/privkey.pem;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        # API proxy
        location /api/ {
            limit_req zone=api burst=20 nodelay;

            proxy_pass http://grok_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # SSE streaming support
            proxy_http_version 1.1;
            proxy_set_header Connection '';
            proxy_buffering off;
            proxy_cache off;
            proxy_read_timeout 300s;

            # Request size limit
            client_max_body_size 10m;
        }

        # Health check
        location /health {
            proxy_pass http://grok_app/health;
            access_log off;
        }
    }
}
```

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run typecheck

      - name: Unit tests
        run: npm test

      - name: Build
        run: npm run build

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: |
          echo "Deploying to production..."
          # Add your deployment script here
```

### Deployment Script

```bash
#!/bin/bash
# scripts/deploy.sh

set -euo pipefail

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}

echo "Deploying Grok Application v${VERSION} to ${ENVIRONMENT}..."

# Validate environment
if [ ! -f ".env.${ENVIRONMENT}" ]; then
  echo "Error: .env.${ENVIRONMENT} not found"
  exit 1
fi

# Build
echo "Building..."
docker build -t grok-app:${VERSION} -f docker/Dockerfile .

# Test
echo "Running tests..."
docker run --rm grok-app:${VERSION} npm test

# Deploy
echo "Deploying..."
docker compose -f docker/docker-compose.yml --env-file .env.${ENVIRONMENT} up -d

# Health check
echo "Waiting for health check..."
for i in {1..30}; do
  if curl -sf http://localhost:3000/health > /dev/null; then
    echo "Deployment successful!"
    exit 0
  fi
  sleep 2
done

echo "Health check failed!"
docker compose logs app
exit 1
```

## Performance Optimization

### Connection Pooling

```typescript
// Optimize HTTP connections to the Grok API
import https from 'https';
import http from 'http';

const agent = new https.Agent({
  keepAlive: true,
  keepAliveMsecs: 30000,
  maxSockets: 10,
  maxFreeSockets: 5,
  timeout: 60000,
});

const client = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1',
  httpAgent: agent,
});
```

### Request Batching

```typescript
// Batch similar requests to reduce API overhead
async function batchRequests<T>(
  items: T[],
  processor: (item: T) => Promise<any>,
  batchSize: number = 5,
  delayMs: number = 1000
): Promise<any[]> {
  const results = [];

  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await Promise.all(batch.map(processor));
    results.push(...batchResults);

    // Respect rate limits
    if (i + batchSize < items.length) {
      await sleep(delayMs);
    }
  }

  return results;
}
```

### Monitoring and Metrics

```typescript
// src/utils/metrics.ts
import { Registry, Counter, Histogram, Gauge } from 'prom-client';

const registry = new Registry();

export const metrics = {
  httpRequestDuration: new Histogram({
    name: 'grok_http_request_duration_seconds',
    help: 'Duration of HTTP requests to Grok API',
    buckets: [0.1, 0.5, 1, 2, 5, 10, 30],
    registers: [registry],
  }),

  tokensUsed: new Counter({
    name: 'grok_tokens_used_total',
    help: 'Total tokens consumed',
    labelNames: ['type'], // 'prompt' or 'completion'
    registers: [registry],
  }),

  activeRequests: new Gauge({
    name: 'grok_active_requests',
    help: 'Number of active requests to Grok API',
    registers: [registry],
  }),

  cacheHits: new Counter({
    name: 'grok_cache_hits_total',
    help: 'Total cache hits',
    registers: [registry],
  }),

  cacheMisses: new Counter({
    name: 'grok_cache_misses_total',
    help: 'Total cache misses',
    registers: [registry],
  }),

  errors: new Counter({
    name: 'grok_errors_total',
    help: 'Total API errors',
    labelNames: ['status', 'type'],
    registers: [registry],
  }),
};

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', registry.contentType);
  res.end(await registry.metrics());
});
```

## Common Pitfalls and Solutions

### Pitfall 1: Missing Error Handling

```typescript
// BAD: No error handling
const response = await client.chat(messages);

// GOOD: Comprehensive error handling
import { GrokError } from './errors';

async function safeChat(messages: Message[], retries = 3): Promise<string> {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await client.chat(messages);
      return response.choices[0].message.content;
    } catch (error) {
      if (error.status === 429) {
        // Rate limited — exponential backoff
        const delay = Math.pow(2, attempt) * 1000;
        await sleep(delay);
        continue;
      }
      if (error.status === 500 || error.status === 503) {
        // Server error — retry
        await sleep(1000 * attempt);
        continue;
      }
      // Client error — don't retry
      throw new GrokError(`API error: ${error.message}`, error.status);
    }
  }
  throw new GrokError('Max retries exceeded', 503);
}
```

### Pitfall 2: Unbounded Context Growth

```typescript
// BAD: Context grows unbounded
const messages = [];
messages.push({ role: 'user', content: userInput });
const response = await client.chat(messages); // Eventually hits token limit

// GOOD: Context management
class ConversationManager {
  private messages: Message[] = [];
  private maxTokens = 200000;
  private systemPrompt: string;

  constructor(systemPrompt: string) {
    this.systemPrompt = systemPrompt;
  }

  async addAndRespond(userMessage: string): Promise<string> {
    this.messages.push({ role: 'user', content: userMessage });

    // Estimate token count
    const estimatedTokens = this.estimateTokens();

    if (estimatedTokens > this.maxTokens * 0.8) {
      // Summarize older messages
      await this.summarizeOlderMessages();
    }

    const response = await client.chat([
      { role: 'system', content: this.systemPrompt },
      ...this.messages,
    ]);

    this.messages.push({ role: 'assistant', content: response.choices[0].message.content });
    return response.choices[0].message.content;
  }

  private estimateTokens(): number {
    // Rough estimate: 4 chars per token
    return this.messages.reduce((sum, m) => sum + Math.ceil(m.content.length / 4), 0);
  }

  private async summarizeOlderMessages(): Promise<void> {
    const older = this.messages.slice(0, -4);
    const recent = this.messages.slice(-4);

    const summary = await client.chat([
      { role: 'system', content: 'Summarize this conversation concisely.' },
      { role: 'user', content: JSON.stringify(older) },
    ]);

    this.messages = [
      { role: 'system', content: `Previous conversation summary: ${summary.choices[0].message.content}` },
      ...recent,
    ];
  }
}
```

### Pitfall 3: Ignoring Rate Limits

```typescript
// GOOD: Proactive rate limiting
import { RateLimiter } from './rate-limiter';

const limiter = new RateLimiter({
  maxRequests: 60,
  windowMs: 60000,
});

async function rateLimitedChat(messages: Message[]): Promise<string> {
  await limiter.acquire();
  try {
    return await client.chat(messages);
  } finally {
    limiter.release();
  }
}
```

### Pitfall 4: No Health Checks

```typescript
// GOOD: Health check endpoint
app.get('/health', async (req, res) => {
  const checks = {
    grok: await checkGrokConnectivity(),
    redis: await checkRedisConnectivity(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
  };

  const healthy = Object.values(checks).every(c => c !== false);
  res.status(healthy ? 200 : 503).json(checks);
});

async function checkGrokConnectivity(): Promise<boolean> {
  try {
    await client.chat([{ role: 'user', content: 'ping' }], { max_tokens: 5 });
    return true;
  } catch {
    return false;
  }
}
```

## Security Checklist

- [ ] API keys stored in environment variables, not code
- [ ] `.env` files in `.gitignore`
- [ ] HTTPS enforced in production
- [ ] Rate limiting configured
- [ ] Input validation and sanitization
- [ ] CORS properly configured
- [ ] Request size limits enforced
- [ ] Health checks implemented
- [ ] Error messages don't leak internal details
- [ ] Secrets rotated periodically
- [ ] Audit logging enabled
- [ ] Dependencies regularly updated

## Related Documentation

- [Grok 4.5](./grok-4-5.md) — Model specification
- [Grok Code Fast 1](./grok-code-fast-1.md) — Code model
- [Best Practices](./grok-best-practices.md) — Optimization guide
- [Vision Capabilities](./grok-vision.md) — Multimodal reference
