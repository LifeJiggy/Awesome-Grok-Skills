---
name: cdn-optimization
version: 2.0.0
description: Comprehensive CDN optimization agent for multi-provider cache management, edge function deployment, security hardening, performance analysis, and cost optimization.
author: MiMoCode
tags:
  - cdn
  - caching
  - edge-computing
  - performance
  - security
  - cloud
  - infrastructure
category: infrastructure
personality: methodical, precise, security-conscious, performance-focused
use_cases:
  - CDN cache policy optimization
  - Edge function deployment
  - Origin shielding configuration
  - SSL/TLS security hardening
  - WAF and DDoS protection
  - Performance monitoring and Core Web Vitals
  - Cost optimization across CDN providers
  - CDN migration planning and execution
  - Rate limiting and bot management
  - Geographic routing configuration
---

# CDN Optimization Agent — GROK.md

## Agent Identity & Purpose

The CDN Optimization Agent is a production-grade system for managing Content Delivery
Networks across 10 major providers. It automates the full lifecycle of CDN operations:
from initial configuration and cache policy optimization through edge function deployment,
security hardening, performance monitoring, and multi-provider migration.

**Primary Mission:** Maximize content delivery performance while minimizing origin load,
bandwidth costs, and security exposure.

**Core Competency:** Multi-provider CDN management with deep expertise in cache
invalidation strategies, edge computing, origin protection, and cost optimization.

## 10 Core Principles

### 1. Cache Hierarchy First

Always design a multi-tier cache architecture before optimizing individual rules.
Edge cache → Shield cache → Origin is the foundation of CDN performance.

```python
# Example: Tiered cache configuration
shield_config = OriginShieldConfig(
    enabled=True,
    tier=OriginShieldTier.MULTI_TIER,
    shield_regions=["us-east-1", "eu-west-1"],
    warmup_enabled=True,
)
# Expected: 85% origin load reduction, 12ms latency overhead
```

### 2. Content-Aware Policies

Different content types demand different caching strategies. Never apply a
one-size-fits-all cache policy.

```python
# Content-type specific optimization
for content_type in [ContentType.HTML, ContentType.CSS, ContentType.JS]:
    strategy = content_type.default_cache_strategy
    ttl = agent._calculate_optimal_ttl(content_type, strategy, "high")
    # HTML: stale-while-revalidate, short TTL
    # CSS/JS: immutable, fingerprinted, long TTL
```

### 3. Security at the Edge

Process security decisions (WAF, rate limiting, bot detection) at the edge,
not at the origin. This reduces origin load and improves response times.

```python
# Security rules applied before cache lookup
security_result = agent.set_up_security_rules("shop.example.com", "high")
# WAF + Bot Mgmt + DDoS + Rate Limit + Access Rules = defense in depth
```

### 4. Origin Protection is Critical

The origin server is the most vulnerable and expensive component. Every
optimization should reduce origin load.

```python
# Circuit breaker + rate limiting + caching = origin protection
agent.set_up_failover(domain, origins)
agent.set_up_rate_limiting(domain)
agent.optimize_cache_rules(domain)
```

### 5. Cost-Aware Optimization

Performance optimization must be balanced against cost. Not every optimization
is worth the premium.

```python
# Cost analysis before major changes
cost = agent.analyze_costs(CDNProvider.FASTLY, "30d", bandwidth_gb=5000)
if cost["estimated_savings"] > 100:
    # Consider provider migration or plan optimization
```

### 6. Measure Before Optimizing

Establish baselines before making changes. Without measurements, optimization
is guesswork.

```python
# Baseline performance
baseline = agent.analyze_performance(domain, "7d")
print(f"Baseline score: {baseline.overall_score}")
# Make changes...
# Compare results
```

### 7. Stale Content is Better Than No Content

When the origin is unavailable, serving stale content is almost always better
than returning an error.

```python
# Configure stale-while-revalidate and stale-if-error
rule = CacheRule(
    pattern=r"\.html$",
    strategy=CacheStrategy.STALE_WHILE_REVALIDATE,
    ttl=3600,
    stale_if_error=86400,  # Serve stale for up to 24h on origin error
    stale_while_revalidate=60,  # Revalidate in background
)
```

### 8. Edge Functions for Dynamic Logic

Move dynamic logic to the edge when possible. This reduces origin round-trips
and improves global latency.

```python
# Edge function for A/B testing
agent.deploy_edge_function(
    domain, "ab-test", EdgeFunctionType.A_B_TESTER,
    js_code, ["/", "/home"]
)
# Traffic splitting happens at the edge, no origin call needed
```

### 9. Compression is Free Performance

Enable compression for all text-based content. The CPU cost is negligible
compared to bandwidth savings.

```python
# Optimal compression configuration
agent.configure_compression(domain)
# Brotli for text: 40% size reduction
# Pre-compressed assets: zero runtime cost
```

### 10. Migration is a Process, Not an Event

CDN migration requires careful planning, parallel testing, and gradual cutover.
Never rush a migration.

```python
# Structured migration with rollback plan
migration = agent.migrate_cdn(
    CDNProvider.AWS_CLOUDFRONT,
    CDNProvider.CLOUDFLARE,
    domain,
    dry_run=True  # Always plan first
)
```

## Detailed Capabilities

### Cache Policy Optimization

The cache policy engine generates optimal rules based on content type, traffic
pattern, and freshness requirements.

```python
# Comprehensive cache optimization
result = agent.optimize_cache_rules(
    domain="shop.example.com",
    content_types=[ContentType.HTML, ContentType.CSS, ContentType.JS,
                   ContentType.IMAGE, ContentType.FONT],
    traffic_pattern="high"
)

# Output includes:
# - Rules created with strategy, TTL, bypass patterns
# - Estimated cache hit rate
# - Content-type specific analysis
# - Optimization recommendations
```

**Cache Strategy Selection Guide:**

| Content Type | Strategy | TTL | Rationale |
|-------------|----------|-----|-----------|
| HTML | stale-while-revalidate | 3600s | Balance freshness with performance |
| CSS/JS (fingerprinted) | immutable | 1 year | Never changes, safe to cache forever |
| Images | public | 1 week | Rarely change, high bandwidth |
| Fonts | immutable | 1 year | Never change, large files |
| API JSON | no-cache | 0s | Always fresh data |
| Video | public | 1 week | Large files, infrequent changes |

### Edge Function Deployment

Edge functions execute custom logic at CDN edge locations with strict runtime
constraints.

```python
# Deploy a request modifier
result = agent.deploy_edge_function(
    domain="api.example.com",
    name="auth-validator",
    func_type=EdgeFunctionType.AUTHENTICATOR,
    code="""
    export default async function requestHandler(request) {
        const token = request.headers.get('authorization');
        if (!token || !validateToken(token)) {
            return new Response('Unauthorized', { status: 401 });
        }
        return fetch(request);
    }
    """,
    routes=["/api/v2/*"]
)

# Runtime constraints:
# - Max execution: 30ms (50ms for response modifiers)
# - Max memory: 128MB
# - Access to: headers, geo, TLS info
# - Streaming support for image/response modifiers
```

**Edge Function Types and Use Cases:**

| Type | Use Case | Execution Limit |
|------|----------|----------------|
| REQUEST_MODIFIER | Add/remove headers, rewrite URLs | 30ms |
| RESPONSE_MODIFIER | Transform response body | 50ms |
| AUTHENTICATOR | Validate JWT/OAuth tokens at edge | 30ms |
| RATE_LIMITER | Throttle requests per IP | 30ms |
| BOT_DETECTOR | Identify and block bots | 30ms |
| IMAGE_OPTIMIZER | WebP/AVIF conversion | 50ms |
| A_B_TESTER | Traffic splitting | 30ms |
| GEO_REDIRECT | Location-based redirects | 30ms |

### Origin Shielding

Origin shielding adds a cache layer between edge POPs and the origin, reducing
origin load by 60-95%.

```python
# Configure origin shielding
shield = agent.configure_origin_shielding("shop.example.com")

# Tier options:
# NONE:      0% load reduction, 0ms overhead
# SINGLE:    60% load reduction, 5ms overhead
# MULTI_TIER: 85% load reduction, 12ms overhead
# HIERARCHICAL: 95% load reduction, 20ms overhead
```

### Security Configuration

Defense-in-depth security with WAF, bot management, DDoS protection, and
rate limiting.

```python
# Configure security rules
security = agent.set_up_security_rules(
    domain="shop.example.com",
    threat_profile="high"
)

# Threat profiles:
# low:      WAF + TLS only
# standard: WAF + TLS + Headers + Rate Limiting
# high:     All features (WAF, Bot, DDoS, TLS, Headers, Rate Limit, Access)
```

**WAF Rule Categories:**

| Rule | Severity | Action | Description |
|------|----------|--------|-------------|
| SQL Injection | Critical | Block | Detects SQL injection patterns |
| XSS Protection | High | Block | Detects cross-site scripting |
| Path Traversal | High | Block | Detects directory traversal |
| Known Bad Bots | Medium | Block | Blocks known malicious bots |
| Rate Limit Exceeded | Medium | Challenge | Throttles excessive requests |

### Performance Analysis

Comprehensive performance monitoring with Core Web Vitals and CDN metrics.

```python
# Generate performance report
report = agent.generate_performance_report("shop.example.com", "30d")

# Metrics tracked:
# - TTFB (p50, p95): Time to first byte
# - FCP (p50, p95): First contentful paint
# - LCP (p50, p95): Largest contentful paint
# - CLS (p50): Cumulative layout shift
# - TTI (p50): Time to interactive
# - TBT (p50): Total blocking time
# - FID (p50): First input delay
# - Cache hit rate and bandwidth savings
```

### Cost Optimization

Analyze and optimize CDN costs across providers.

```python
# Compare provider costs
for provider in [CDNProvider.CLOUDFLARE, CDNProvider.AWS_CLOUDFRONT,
                 CDNProvider.FASTLY, CDNProvider.GOOGLE_CLOUD_CDN]:
    cost = agent.analyze_costs(provider, "30d", bandwidth_gb=5000)
    print(f"{provider.value}: ${cost['current_cost']:.2f}")
```

### CDN Migration

Structured migration between providers with rollback capability.

```python
# Plan migration (dry run)
migration = agent.migrate_cdn(
    source=CDNProvider.AWS_CLOUDFRONT,
    target=CDNProvider.CLOUDFLARE,
    domain="shop.example.com",
    dry_run=True
)

# Migration phases:
# 1. Assessment (4-8h): Audit source, document rules
# 2. Preparation (8-16h): Map rules, deploy SSL, configure functions
# 3. Parallel Testing (24-48h): Dual-stack, compare metrics
# 4. Cutover (1-4h): DNS switch, monitor errors
# 5. Stabilization (24-72h): Monitor, adjust, decommission
```

## Operational Guidelines

### Method Signatures

```python
# Core configuration methods
initialize_configuration(domain, provider, origins) -> CDNConfiguration
optimize_cache_rules(domain, content_types, traffic_pattern) -> Dict
configure_origin_shielding(domain) -> Dict
deploy_edge_function(domain, name, func_type, code, routes) -> Dict
purge_cache(domain, method, targets) -> Dict

# Security methods
configure_ssl(domain, cert_type) -> Dict
set_up_security_rules(domain, threat_profile) -> Dict
set_up_rate_limiting(domain, rules) -> Dict

# Performance methods
analyze_performance(domain, period) -> PerformanceReport
generate_performance_report(domain, period) -> Dict
analyze_logs(domain, period) -> Dict

# Cost and migration methods
analyze_costs(provider, period, bandwidth_gb, requests_millions) -> Dict
migrate_cdn(source, target, domain, dry_run) -> Dict
configure_geo_routing(domain, routing_rules) -> Dict
```

### Usage Patterns

**Pattern 1: New Domain Setup**
```python
agent = CDNOptimizationAgent()
agent.initialize_configuration("shop.example.com")
agent.optimize_cache_rules("shop.example.com")
agent.configure_ssl("shop.example.com")
agent.set_up_security_rules("shop.example.com", "high")
agent.configure_compression("shop.example.com")
agent.set_up_rate_limiting("shop.example.com")
agent.set_up_failover("shop.example.com")
```

**Pattern 2: Performance Investigation**
```python
baseline = agent.analyze_performance(domain, "7d")
# Identify bottlenecks
# Apply optimizations
# Compare results
report = agent.generate_performance_report(domain, "7d")
```

**Pattern 3: Cost Optimization**
```python
current_cost = agent.analyze_costs(current_provider, "30d")
# Compare with alternatives
# Negotiate or migrate
migration = agent.migrate_cdn(current_provider, target_provider, domain)
```

## Data Models

### Core Enums

```python
CDNProvider         # 10 major CDN providers
CacheStrategy       # 7 caching strategies (no-cache through immutable)
PurgeMethod         # 5 purge methods (URL, tag, prefix, wildcard, all)
EdgeFunctionType    # 8 function types (request modifier through geo redirect)
ProtocolType        # 6 protocols (HTTP/1.1 through gRPC)
OriginShieldTier    # 4 tiers (none through hierarchical)
CacheStatus         # 8 statuses (hit, miss, expired, stale, bypass, etc.)
PerformanceMetric   # 8 metrics (TTFB through CLS)
SecurityFeature     # 7 features (WAF through access rules)
CompressionType     # 5 types (gzip, brotli, deflate, zstd, none)
ContentType         # 9 types (HTML through PDF)
OriginHealthStatus  # 4 statuses (healthy, degraded, unhealthy, maintenance)
```

### Core Dataclasses

```python
CacheRule            # Cache policy with pattern, strategy, TTL, bypass
EdgeFunction         # Edge function with code, routes, runtime config
OriginServer         # Origin with health check, failover, shield config
PurgeRequest         # Cache purge with method, targets, status
PerformanceReport    # Performance metrics with scores and recommendations
SecurityRule         # Security rule with type, action, conditions
CDNConfiguration     # Full domain config (origins, rules, functions, security)
CachePolicy          # Named cache policy with rules and targets
OriginShieldConfig   # Shield tier, regions, cost estimation
SSLConfiguration     # TLS version, HSTS, OCSP, security headers
RedirectRule         # Redirect with source, target, status code
CompressionConfig    # Compression types, levels, content rules
RateLimitRule        # Rate limit with paths, thresholds, actions
AnalyticsSnapshot    # Analytics with requests, bandwidth, cache stats
CostBreakdown        # Cost analysis with per-component breakdown
HealthCheck          # Origin health check with history
GeoRoutingRule       # Geographic routing with countries, targets
ImageOptimizationRule # Image processing with format conversion
WAFRule              # WAF rule with pattern, action, severity
DDoSProfile          # DDoS protection with layers and sensitivity
CDNDeployment        # Migration deployment with steps and rollback
FailoverConfig       # Failover with origins, health checks, thresholds
BandwidthReport      # Bandwidth analysis with regional breakdown
RequestLog           # Request log with cache status and timing
```

## Checklists

### CDN Setup Checklist

- [ ] Initialize domain configuration with provider
- [ ] Configure origin servers with health checks
- [ ] Set up SSL/TLS with HSTS and OCSP stapling
- [ ] Configure cache rules for all content types
- [ ] Set up origin shielding
- [ ] Configure compression (Brotli + Gzip fallback)
- [ ] Set up rate limiting rules
- [ ] Configure security rules (WAF, DDoS, bot management)
- [ ] Deploy edge functions for dynamic logic
- [ ] Set up failover with health monitoring
- [ ] Configure geographic routing
- [ ] Test cache behavior (hit/miss/bypass)
- [ ] Verify security rules are active
- [ ] Monitor performance metrics
- [ ] Document configuration and rollback plan

### Security Hardening Checklist

- [ ] Enable TLS 1.2+ with strong cipher suites
- [ ] Configure HSTS with max-age=31536000, includeSubDomains, preload
- [ ] Enable OCSP stapling
- [ ] Enable SSL origin pull
- [ ] Deploy WAF rules (SQLi, XSS, path traversal)
- [ ] Configure rate limiting per path
- [ ] Enable bot management
- [ ] Enable DDoS protection (L3/L4 and L7)
- [ ] Set up access rules (geo blocking if needed)
- [ ] Configure security headers (X-Content-Type-Options, X-Frame-Options, etc.)
- [ ] Enable browser integrity check
- [ ] Set up IP reputation filtering
- [ ] Configure challenge rules for suspicious traffic
- [ ] Test security rules with attack payloads
- [ ] Monitor security event logs

### Performance Optimization Checklist

- [ ] Establish baseline performance metrics
- [ ] Configure cache rules for optimal hit rate (target: 85%+)
- [ ] Enable compression for text content (Brotli level 6)
- [ ] Configure stale-while-revalidate for HTML
- [ ] Set immutable caching for fingerprinted assets
- [ ] Enable origin shielding (target: 80%+ origin load reduction)
- [ ] Configure edge functions for dynamic logic
- [ ] Optimize image delivery (WebP/AVIF conversion)
- [ ] Enable HTTP/2 and HTTP/3 (QUIC)
- [ ] Configure connection keep-alive
- [ ] Set appropriate cache TTLs per content type
- [ ] Monitor Core Web Vitals (LCP, FID, CLS, TTFB)
- [ ] Review and optimize cache bypass patterns
- [ ] Test edge function execution times
- [ ] Document performance improvements

### Migration Checklist

- [ ] Audit source configuration (all rules, functions, SSL)
- [ ] Document current performance baseline
- [ ] Map source rules to target provider format
- [ ] Deploy SSL certificate on target provider
- [ ] Configure origin servers on target
- [ ] Copy cache rules to target
- [ ] Deploy edge functions on target
- [ ] Set up security rules on target
- [ ] Configure rate limiting on target
- [ ] Set up monitoring and alerting
- [ ] Run parallel testing (dual-stack)
- [ ] Compare hit rates and latency
- [ ] Verify security rules active
- [ ] Update DNS TTL to 300s
- [ ] Plan cutover window
- [ ] Execute DNS switch
- [ ] Monitor error rates post-cutover
- [ ] Verify all rules working correctly
- [ ] Document migration results
- [ ] Decommission source after stabilization

## Troubleshooting Guide

### Cache Misses

**Symptoms:** Low cache hit rate, high origin load, slow TTFB

**Diagnosis:**
```python
report = agent.analyze_performance(domain, "7d")
# Check cache_hit_rate
# Review top_missed_paths
# Check cache_status_distribution
```

**Common Causes:**
1. TTL too short for content type
2. Cache-busting query strings on static assets
3. Vary headers creating too many cache keys
4. Bypass patterns matching legitimate traffic
5. No-store or no-cache headers from origin

**Solutions:**
- Increase TTL for static assets (CSS, JS, images, fonts)
- Implement content hashing instead of query string cache busting
- Review and minimize Vary headers
- Audit bypass patterns for false positives
- Remove no-store/no-cache headers from static content

### Origin Overload

**Symptoms:** High origin latency, 5xx errors, origin health check failures

**Diagnosis:**
```python
shield = agent.configure_origin_shielding(domain)
# Check origin_load_reduction
# Review health check status
```

**Common Causes:**
1. Low cache hit rate
2. No origin shielding
3. Cache stampede (many simultaneous misses)
4. Origin not optimized for CDN traffic

**Solutions:**
- Enable origin shielding (MULTI_TIER recommended)
- Implement stale-while-revalidate for HTML
- Add cache lock for concurrent miss requests
- Optimize origin for keep-alive connections
- Set up failover with health checking

### Latency Spikes

**Symptoms:** High p95/p99 latency, slow TTFB, degraded Core Web Vitals

**Diagnosis:**
```python
report = agent.generate_performance_report(domain, "7d")
# Check TTFB p95 vs p50
# Review geographic distribution
# Check edge function execution times
```

**Common Causes:**
1. Cold cache (high miss rate)
2. Edge function execution time
3. Origin under load
4. Network congestion
5. Large response payloads

**Solutions:**
- Warm cache after deployment
- Optimize edge function code
- Enable origin shielding
- Configure geographic routing
- Enable compression and optimize payload size

### Security Incidents

**Symptoms:** High block rate, WAF alerts, DDoS mitigation active

**Diagnosis:**
```python
logs = agent.analyze_logs(domain, "1h")
# Check anomalies
# Review security_events
# Check blocked_requests
```

**Common Causes:**
1. Legitimate traffic flagged by WAF rules
2. DDoS attack in progress
3. Bot activity
4. False positives in rate limiting

**Solutions:**
- Review WAF rule match counts
- Whitelist known good IPs/bots
- Adjust rate limit thresholds
- Enable challenge instead of block for suspicious traffic
- Monitor and tune rules based on traffic patterns

### CDN Migration Issues

**Symptoms:** Increased errors, missing rules, SSL issues post-migration

**Diagnosis:**
```python
# Compare source and target configurations
source_config = agent.configurations[domain]
# Verify all rules migrated
# Check SSL certificate status
# Test edge function execution
```

**Common Causes:**
1. Incomplete rule migration
2. SSL certificate not deployed
3. DNS not fully propagated
4. Edge function syntax differences
5. Provider-specific feature gaps

**Solutions:**
- Verify all cache rules are present on target
- Ensure SSL certificate is active and valid
- Wait for DNS propagation (check TTL)
- Adapt edge function code for target provider runtime
- Document and implement workarounds for feature gaps
- Rollback if issues persist beyond acceptable threshold

## Advanced Topics

### Multi-Provider Strategy

When managing multiple domains across different CDN providers, the agent provides
a unified interface regardless of provider-specific differences.

```python
# Multi-provider deployment
domains = {
    "shop.example.com": CDNProvider.CLOUDFLARE,
    "api.example.com": CDNProvider.AWS_CLOUDFRONT,
    "media.example.com": CDNProvider.FASTLY,
}

agent = CDNOptimizationAgent()

for domain, provider in domains.items():
    agent.initialize_configuration(domain, provider)
    agent.optimize_cache_rules(domain)
    agent.configure_ssl(domain)
    agent.set_up_security_rules(domain, "high")
```

### Edge Function Best Practices

Edge functions have strict runtime constraints. Follow these patterns:

```python
# Good: Minimal execution time
code_good = """
export default async function requestHandler(request) {
    const url = new URL(request.url);
    url.searchParams.set('cache-bust', Date.now());
    return fetch(url.toString());
}
"""

# Bad: Heavy computation in edge function
code_bad = """
export default async function requestHandler(request) {
    // DON'T: Complex operations at the edge
    const data = await fetch('https://api.example.com/data');
    const processed = data.map(item => heavyComputation(item));
    return new Response(JSON.stringify(processed));
}
"""
```

**Edge Function Guidelines:**
- Keep execution under 30ms (50ms for response modifiers)
- Minimize subrequests (max 50 per invocation)
- Use KV storage for configuration, not subrequests
- Cache subrequest responses when possible
- Handle errors gracefully (return fallback, don't throw)
- Test with synthetic traffic before production deployment

### Cache Invalidation Strategies

Choose the right purge method for your use case:

| Method | Speed | Scope | Best For |
|--------|-------|-------|----------|
| URL | Fast | Specific URLs | Deploying updated assets |
| Tag | Fast | By surrogate key | Purge all versions of content |
| Prefix | Medium | By path prefix | Purge entire directories |
| Wildcard | Medium | By pattern | Purge file types or sections |
| All | Slow | Everything | Emergency purge, full reset |

```python
# URL purge: precise, fast
agent.purge_cache(domain, PurgeMethod.URL, ["/assets/app.v2.js"])

# Tag purge: purge all images
agent.purge_cache(domain, PurgeMethod.TAG, ["product-images"])

# Prefix purge: purge entire API
agent.purge_cache(domain, PurgeMethod.PREFIX, ["/api/v2/"])

# All purge: nuclear option
agent.purge_cache(domain, PurgeMethod.ALL, [])
```

### Monitoring and Alerting

Set up monitoring to detect issues before users notice:

```python
# Performance monitoring
report = agent.generate_performance_report(domain, "24h")

# Alert thresholds
alerts = {
    "ttfb_p95": report["core_web_vitals"]["ttfb"]["p95"] > 500,
    "cache_hit_rate": float(report["cache_performance"]["hit_rate"].rstrip('%')) < 80,
    "error_rate": report.get("error_rate", 0) > 1.0,
}

for alert_name, triggered in alerts.items():
    if triggered:
        print(f"ALERT: {alert_name} threshold exceeded!")
```

**Recommended Alert Thresholds:**

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Cache Hit Rate | < 85% | < 70% | Review cache rules |
| TTFB (p95) | > 500ms | > 1000ms | Check origin/shield |
| Error Rate | > 1% | > 5% | Investigate origin/WAF |
| Origin Load | > 30% | > 50% | Enable shielding |
| SSL Expiry | < 30 days | < 7 days | Renew certificate |

### Compliance and Security Standards

The agent supports configurations aligned with common compliance frameworks:

**PCI DSS (Payment Card Industry):**
- TLS 1.2+ mandatory
- No caching of cardholder data
- WAF enabled with PCI rule sets
- Access logging enabled

**HIPAA (Healthcare):**
- End-to-end encryption (TLS origin pull)
- No caching of PHI (Protected Health Information)
- Audit logging for all access
- geo-blocking for restricted regions

**GDPR (EU Privacy):**
- Data residency controls via geographic routing
- Cookie consent integration at edge
- Right-to-deletion support in edge functions
- Privacy-respecting analytics

```python
# PCI DSS compliant configuration
agent.configure_ssl(domain, cert_type="dedicated")  # Dedicated cert
agent.set_up_security_rules(domain, "high")  # Full security stack
# Add no-cache rule for payment endpoints
from agent import CacheRule, CacheStrategy
payment_rule = CacheRule(
    pattern=r"/checkout/.*|/payment/.*",
    strategy=CacheStrategy.NO_STORE,
    ttl=0,
)
config = agent._get_config(domain)
config.cache_rules.append(payment_rule)
```

### Performance Tuning Cookbook

**Reduce TTFB by 50%:**
```python
# 1. Enable origin shielding
agent.configure_origin_shielding(domain)
# 2. Optimize cache rules for high hit rate
agent.optimize_cache_rules(domain, traffic_pattern="high")
# 3. Enable stale-while-revalidate
# (configured automatically by optimize_cache_rules)
```

**Reduce Bandwidth by 40%:**
```python
# 1. Enable Brotli compression
agent.configure_compression(domain)
# 2. Optimize images (WebP/AVIF conversion)
agent.optimize_images(domain)
# 3. Enable immutable caching for static assets
# (configured automatically by optimize_cache_rules)
```

**Improve Security Posture to A+:**
```python
# 1. Configure advanced SSL
agent.configure_ssl(domain, cert_type="advanced")
# 2. Enable full security stack
agent.set_up_security_rules(domain, "high")
# 3. Configure rate limiting
agent.set_up_rate_limiting(domain)
# Result: Security score > 0.95
```

### Integration Patterns

**CI/CD Integration:**
```python
# In your deployment pipeline
def deploy_with_cdn(domain, version):
    agent = CDNOptimizationAgent()
    agent.initialize_configuration(domain)
    agent.optimize_cache_rules(domain)
    agent.purge_cache(domain, PurgeMethod.TAG, [f"version-{version}"])
```

**Monitoring Integration:**
```python
# Export metrics for Prometheus/Grafana
report = agent.generate_performance_report(domain, "1h")
metrics = {
    "cdn_cache_hit_rate": report["cache_performance"]["hit_rate"],
    "cdn_ttfb_p50": report["core_web_vitals"]["ttfb"]["p50"],
    "cdn_bandwidth_saved_gb": report["cache_performance"]["bandwidth_saved_gb"],
}
# Send to your monitoring system
```

**Infrastructure as Code:**
```python
# Terraform-style configuration export
config = agent._get_config(domain)
export = {
    "cache_rules": [{"pattern": r.pattern, "strategy": r.strategy.value, "ttl": r.ttl}
                    for r in config.cache_rules],
    "security_rules": [{"type": r.rule_type.value, "action": r.action}
                       for r in config.active_security_rules],
}
# Write to JSON for IaC import
import json
with open(f"{domain}-cdn-config.json", "w") as f:
    json.dump(export, f, indent=2)
```

### Provider-Specific Notes

**Cloudflare:**
- Free SSL with Universal certificates
- Workers for edge compute (10ms free tier)
-Argo Smart Routing for reduced latency
- Rate limiting included in Pro plan+

**AWS CloudFront:**
- Lambda@Edge for edge compute
- Origin Shield available as add-on
- Integration with AWS WAF and Shield
- Price class selection for cost control

**Fastly:**
- VCL for edge logic (most flexible)
- Real-time purging (instant invalidation)
- Shield available for origin protection
- Wasm support for edge compute

**Akamai:**
- EdgeWorkers for compute
- Ion for performance optimization
- App & API Protector for security
- Largest global footprint
