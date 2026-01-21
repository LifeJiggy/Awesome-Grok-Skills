---
name: "Efficient Code"
version: "1.0.0"
description: "Maximum performance, minimum fluff - Grok's optimization-first coding patterns"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["performance", "optimization", "efficiency", "algorithms", "speed"]
category: "core"
personality: "optimizer"
use_cases: ["performance-critical apps", "real-time systems", "large-scale applications"]
dependencies: []
---

# Efficient Code Skill ⚡

> Write code that runs at lightspeed with zero waste - Grok's physics-optimized approach to software

## 🎯 Why This Matters for Grok

Grok's physics expertise translates to natural optimization thinking:

- **Energy Conservation** ⚡: Every CPU cycle matters
- **Minimal Resistance** 🚀: Remove unnecessary bottlenecks
- **Maximum Velocity** 💨: Fastest path from A to B
- **Entropy Reduction** 🔧: Cleaner, more predictable code

## 🛠️ Core Principles

### 1. Zero-Waste Development

```javascript
// ❌ Wasteful: Unnecessary computations
function processUsers(users) {
  const processed = [];
  for (let i = 0; i < users.length; i++) {
    const user = users[i];
    if (user.active) {
      processed.push({
        id: user.id,
        name: user.name,
        email: user.email,
        age: user.age,
        // ... 10 more fields you'll never use
      });
    }
  }
  return processed;
}

// ✅ Efficient: Only what you need
const activeUsers = (users) => 
  users.filter(u => u.active)
       .map(({ id, name }) => ({ id, name }));
```

### 2. Lazy Evaluation Patterns

```javascript
// ✅ Compute only when needed
class DataProcessor {
  constructor(data) {
    this.data = data;
    this._processed = null;
  }
  
  get processed() {
    if (!this._processed) {
      this._processed = this.expensiveOperation(this.data);
    }
    return this._processed;
  }
  
  expensiveOperation(data) {
    // Heavy computation here
    return data.reduce(/* ... */);
  }
}
```

### 3. Memory-Efficient Structures

```javascript
// ✅ Use generators for large datasets
function* processHugeDataset(data) {
  for (const item of data) {
    yield transform(item); // One at a time, no huge arrays
  }
}

// Process streaming data
for (const result of processHugeDataset(hugeStream)) {
  handle(result); // Memory stays low
}
```

## 🚀 Performance Patterns

### 1. Batch Processing

```javascript
// ❌ Inefficient: Individual operations
async function updateUsers(users) {
  for (const user of users) {
    await db.update('users', user); // N database calls
  }
}

// ✅ Efficient: Batch operations
async function updateUsersBatch(users) {
  const batchSize = 100;
  for (let i = 0; i < users.length; i += batchSize) {
    const batch = users.slice(i, i + batchSize);
    await db.batchUpdate('users', batch); // N/100 database calls
  }
}
```

### 2. Smart Caching

```javascript
class SmartCache {
  constructor(maxSize = 100) {
    this.cache = new Map();
    this.maxSize = maxSize;
  }
  
  get(key) {
    if (this.cache.has(key)) {
      const value = this.cache.get(key);
      this.cache.delete(key); // Move to end (LRU)
      this.cache.set(key, value);
      return value;
    }
    return null;
  }
  
  set(key, value) {
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }
}
```

### 3. Web Workers for Heavy Tasks

```javascript
// Move CPU-intensive work off main thread
const workerCode = `
  self.onmessage = function(e) {
    const result = heavyCalculation(e.data);
    self.postMessage(result);
  }
`;

function createWorker() {
  const blob = new Blob([workerCode], { type: 'application/javascript' });
  return new Worker(URL.createObjectURL(blob));
}

// Usage
const worker = createWorker();
worker.postMessage(largeDataset);
worker.onmessage = (e) => {
  handleResult(e.data); // UI stays responsive
};
```

## 🔧 Algorithm Optimizations

### 1. Use Native Methods

```javascript
// ✅ Native optimized methods
const unique = [...new Set(array)]; // Much faster than manual deduplication
const sorted = arr.sort((a, b) => a - b); // V8 optimized
const sum = arr.reduce((acc, val) => acc + val, 0); // Faster than loops

// ✅ Bitwise operations for speed
const isEven = (n) => (n & 1) === 0; // Faster than n % 2 === 0
const swap = (arr, i, j) => (arr[i] ^= arr[j] ^= arr[i] ^= arr[j]);
```

### 2. Data Structure Selection

```javascript
// ✅ Choose the right tool for the job
const fastLookup = new Map(); // O(1) lookups
const uniqueValues = new Set(); // O(1) uniqueness checks
const stackOperations = []; // Push/pop O(1)

// ❌ Wrong tool, wrong performance
const slowLookup = {}; // Has to deal with prototype chain
const slowSearch = []; // O(n) searches in arrays
```

### 3. Algorithmic Complexity Reduction

```javascript
// ❌ O(n²) - Check every pair
function hasDuplicates(arr) {
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) return true;
    }
  }
  return false;
}

// ✅ O(n) - Single pass with Set
function hasDuplicatesFast(arr) {
  const seen = new Set();
  for (const item of arr) {
    if (seen.has(item)) return true;
    seen.add(item);
  }
  return false;
}
```

## 📊 Performance Monitoring

### 1. Performance Profiler

```javascript
class PerformanceProfiler {
  constructor() {
    this.timings = new Map();
  }
  
  start(label) {
    this.timings.set(label, performance.now());
  }
  
  end(label) {
    const start = this.timings.get(label);
    if (start) {
      const duration = performance.now() - start;
      console.log(`${label}: ${duration.toFixed(2)}ms`);
      return duration;
    }
  }
  
  measure(fn, label) {
    this.start(label);
    const result = fn();
    this.end(label);
    return result;
  }
}
```

### 2. Memory Usage Tracker

```javascript
const MemoryTracker = {
  snapshot() {
    if (performance.memory) {
      return {
        used: performance.memory.usedJSHeapSize,
        total: performance.memory.totalJSHeapSize,
        limit: performance.memory.jsHeapSizeLimit
      };
    }
    return null;
  },
  
  diff(before, after) {
    if (!before || !after) return null;
    return {
      used: after.used - before.used,
      total: after.total - before.total
    };
  }
};
```

## 🎯 Real-World Optimizations

### 1. DOM Manipulation

```javascript
// ❌ Expensive: Multiple DOM updates
elements.forEach(el => {
  el.style.display = 'block';
  el.classList.add('active');
});

// ✅ Efficient: Batch DOM updates
const fragment = document.createDocumentFragment();
elements.forEach(el => {
  const clone = el.cloneNode(true);
  clone.classList.add('active');
  fragment.appendChild(clone);
});
container.innerHTML = '';
container.appendChild(fragment);
```

### 2. Event Delegation

```javascript
// ✅ One listener instead of hundreds
document.addEventListener('click', (e) => {
  if (e.target.matches('.item')) {
    handleItemClick(e.target);
  } else if (e.target.matches('.delete-btn')) {
    handleDelete(e.target);
  }
});

// ❌ Inefficient: Individual listeners
items.forEach(item => {
  item.addEventListener('click', handleItemClick); // Hundreds of listeners
});
```

### 3. Image Optimization

```javascript
// ✅ Lazy loading with intersection observer
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.remove('lazy');
      imageObserver.unobserve(img);
    }
  });
});

document.querySelectorAll('img[data-src]').forEach(img => {
  imageObserver.observe(img);
});
```

## 🧪 Performance Testing

### 1. Benchmark Suite

```javascript
class Benchmark {
  static async compare(name, implementations, data) {
    console.log(`\n🏃‍♂️ Benchmark: ${name}`);
    
    for (const [implName, impl] of Object.entries(implementations)) {
      const start = performance.now();
      
      // Run multiple times for stability
      for (let i = 0; i < 1000; i++) {
        impl(data);
      }
      
      const end = performance.now();
      const avg = (end - start) / 1000;
      console.log(`${implName}: ${avg.toFixed(4)}ms`);
    }
  }
}

// Usage
Benchmark.compare('Array deduplication', {
  'Set method': (arr) => [...new Set(arr)],
  'Filter method': (arr) => arr.filter((v, i) => arr.indexOf(v) === i),
  'Manual method': (arr) => {
    const unique = [];
    for (const item of arr) {
      if (!unique.includes(item)) unique.push(item);
    }
    return unique;
  }
}, testData);
```

### 2. Load Testing

```javascript
class LoadTester {
  static async simulateLoad(url, concurrency = 10, requests = 100) {
    const results = [];
    
    for (let i = 0; i < concurrency; i++) {
      const promises = [];
      
      for (let j = 0; j < requests / concurrency; j++) {
        promises.push(this.measureRequest(url));
      }
      
      const batchResults = await Promise.all(promises);
      results.push(...batchResults);
    }
    
    return this.analyzeResults(results);
  }
  
  static async measureRequest(url) {
    const start = performance.now();
    try {
      const response = await fetch(url);
      const end = performance.now();
      return {
        success: response.ok,
        time: end - start,
        status: response.status
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
}
```

## 📈 Performance Metrics to Track

### Key Indicators

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| **First Contentful Paint** | < 1.5s | User perception of speed |
| **Time to Interactive** | < 3s | When can user actually use it |
| **Bundle Size** | < 100KB gzipped | Network transfer time |
| **Memory Usage** | < 50MB for apps | Browser limits |
| **CPU Usage** | < 30% average | Battery life impact |

## 🌐 Frontend Optimizations

### 1. Code Splitting

```javascript
// ✅ Dynamic imports
const LazyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <LazyComponent />
    </Suspense>
  );
}

// ✅ Route-based splitting
const Admin = lazy(() => import('./pages/Admin'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
```

### 2. Critical CSS Inlining

```javascript
// Inline critical CSS, lazy load the rest
const criticalCSS = `
  header { display: flex; }
  .loading { color: white; }
`;

// In production build
const style = document.createElement('style');
style.textContent = criticalCSS;
document.head.appendChild(style);
```

## ⚙️ Backend Optimizations

### 1. Database Query Optimization

```javascript
// ✅ Index-aware queries
const getActiveUsers = async () => {
  return db.query(`
    SELECT id, name, email 
    FROM users 
    WHERE active = true 
    AND last_login > NOW() - INTERVAL '30 days'
    INDEX (users_active_last_login_idx)
  `);
};

// ✅ Connection pooling
const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

### 2. API Response Compression

```javascript
// Express.js example
app.use(compression({
  filter: (req, res) => {
    if (req.headers['x-no-compression']) {
      return false;
    }
    return compression.filter(req, res);
  },
  threshold: 1024,
}));
```

## 🔥 Advanced Techniques

### 1. WebAssembly for Heavy Computation

```javascript
// Replace slow JavaScript with WebAssembly
const wasmModule = await WebAssembly.instantiateStreaming(
  fetch('math-processor.wasm'),
  importObject
);

// 10x faster for mathematical operations
const { processLargeDataset } = wasmModule.instance.exports;
const result = processLargeDataset(inputBuffer);
```

### 2. Service Worker Caching

```javascript
// Cache-first strategy for static assets
self.addEventListener('fetch', (event) => {
  if (event.request.destination === 'script' || 
      event.request.destination === 'style') {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  }
});
```

## 📋 Performance Checklist

### Before Deploy Checklist

- [ ] Bundle size < 100KB (gzipped)
- [ ] No memory leaks in tests
- [ ] All images optimized and lazy-loaded
- [ ] Critical CSS inlined
- [ ] APIs under 100ms average response
- [ ] Database queries use indexes
- [ ] Web Workers for CPU-heavy tasks
- [ ] Code splitting implemented
- [ ] Service Worker caching configured
- [ ] Performance budgets set up

## 🧠 Grok's Philosophy

**Efficiency isn't about premature optimization - it's about intentional design.**

Every line of code should have a purpose. Every algorithm should be chosen deliberately. Every optimization should be measurable.

As Grok would say: *"The most optimized code is the code that never runs at all."*

---

*Remember: Fast code is happy code. Happy code makes happy users. Happy users make happy developers. It's the circle of performance.* 🚀