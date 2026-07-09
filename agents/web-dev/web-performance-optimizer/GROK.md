---
name: Web Performance Optimization Agent
category: agents/web-dev
difficulty: advanced
time_estimate: "4-6 hours"
dependencies: ["web-performance", "caching", "optimization", "monitoring"]
tags: ["performance", "optimization", "web-dev", "frontend", "backend"]
grok_personality: "speed-optimizer"
description: "Comprehensive web performance optimization agent that analyzes and improves website speed using efficiency-first approach"
---

# Web Performance Optimization Agent

## Overview

This agent optimizes web application performance using physics-inspired principles of efficiency and resource optimization. It combines frontend and backend optimization techniques to achieve maximum speed with minimal resource usage.

## Performance Analysis Framework

### 1. Performance Metrics

```yaml
key_metrics:
  core_web_vitals:
    - lcp: "Largest Contentful Paint < 2.5s"
    - fid: "First Input Delay < 100ms"
    - cls: "Cumulative Layout Shift < 0.1"

  network_performance:
    - ttfb: "Time to First Byte < 200ms"
    - fcp: "First Contentful Paint < 1.8s"
    - tti: "Time to Interactive < 3.8s"

  resource_optimization:
    - bundle_size: "JavaScript < 100KB compressed"
    - image_optimization: "WebP/AVIF format, lazy loading"
    - caching_efficiency: "95%+ cache hit rate"
```

### 2. Analysis Engine

```python
# performance_analyzer.py
class WebPerformanceAnalyzer:
    def __init__(self):
        self.audit_tools = {
            'lighthouse': LighthouseAuditor(),
            'webpagetest': WebPageTest(),
            'bundle_analyzer': BundleAnalyzer(),
            'network_profiler': NetworkProfiler()
        }

    def analyze_performance(self, url_or_build, analysis_type='comprehensive'):
        """Comprehensive performance analysis"""
        results = {
            'overall_score': 0,
            'metrics': {},
            'issues': [],
            'recommendations': [],
            'optimization_potential': {}
        }

        # Run parallel performance audits
        audit_results = self._run_parallel_audits(url_or_build)

        # Analyze different performance aspects
        results['metrics'] = self._extract_metrics(audit_results)
        results['issues'] = self._identify_issues(audit_results)
        results['optimization_potential'] = self._calculate_optimization_potential(audit_results)

        # Generate efficiency-focused recommendations
        results['recommendations'] = self._generate_recommendations(results)

        # Calculate overall score
        results['overall_score'] = self._calculate_performance_score(results)

        return results

    def _generate_recommendations(self, analysis_results):
        """Generate efficiency-focused recommendations"""
        recommendations = []

        # Frontend optimizations
        if analysis_results['metrics']['bundle_size'] > 100000:  # 100KB
            recommendations.append({
                'category': 'bundle_optimization',
                'priority': 'high',
                'description': 'Reduce JavaScript bundle size using tree shaking',
                'implementation': self._generate_bundle_optimization_code(),
                'estimated_impact': '30-50% bundle reduction',
                'physics_analogy': 'Reduce inertial mass - less energy to accelerate'
            })

        # Image optimizations
        if analysis_results['metrics']['unoptimized_images'] > 0:
            recommendations.append({
                'category': 'image_optimization',
                'priority': 'high',
                'description': 'Convert images to modern formats and implement lazy loading',
                'implementation': self._generate_image_optimization_code(),
                'estimated_impact': '50-80% bandwidth reduction',
                'physics_analogy': 'Compress data - reduce entropy in visual information'
            })

        # Caching strategies
        if analysis_results['metrics']['cache_hit_rate'] < 0.95:
            recommendations.append({
                'category': 'caching',
                'priority': 'medium',
                'description': 'Implement aggressive caching strategies',
                'implementation': self._generate_caching_code(),
                'estimated_impact': '10x faster repeat loads',
                'physics_analogy': 'Store potential energy - reuse for faster access'
            })

        return recommendations
```

### 3. Optimization Strategies

```python
# optimizer.py
class PerformanceOptimizer:
    def __init__(self):
        self.optimization_strategies = {
            'frontend': FrontendOptimizer(),
            'backend': BackendOptimizer(),
            'network': NetworkOptimizer(),
            'database': DatabaseOptimizer()
        }

    def optimize_application(self, project_path, optimization_config):
        """Apply multi-layer optimization"""
        optimizations_applied = []

        # Frontend optimization
        frontend_results = self.optimization_strategies['frontend'].optimize(
            project_path, optimization_config.get('frontend', {})
        )
        optimizations_applied.extend(frontend_results)

        # Backend optimization
        backend_results = self.optimization_strategies['backend'].optimize(
            project_path, optimization_config.get('backend', {})
        )
        optimizations_applied.extend(backend_results)

        # Network optimization
        network_results = self.optimization_strategies['network'].optimize(
            project_path, optimization_config.get('network', {})
        )
        optimizations_applied.extend(network_results)

        # Generate performance report
        performance_report = self._generate_optimization_report(optimizations_applied)

        return {
            'optimizations': optimizations_applied,
            'report': performance_report,
            'estimated_improvements': self._estimate_improvements(optimizations_applied)
        }
```

## Usage Examples

### 1. Performance Audit

```bash
# Audit live website
grok --agent web-performance-optimizer \
  --url "https://example.com" \
  --audit-type comprehensive \
  --output performance-report.json

# Audit local build
grok --agent web-performance-optimizer \
  --project ./my-app \
  --build-path ./dist \
  --optimization-level aggressive
```

### 2. Automatic Optimization

```python
# Example: Optimize React application
optimization_config = {
    'frontend': {
        'framework': 'react',
        'bundle_splitting': True,
        'tree_shaking': True,
        'code_splitting': True,
        'lazy_loading': True
    },
    'backend': {
        'caching': 'redis',
        'compression': 'gzip,brotli',
        'cdn': 'cloudflare'
    },
    'images': {
        'formats': ['webp', 'avif'],
        'lazy_loading': True,
        'responsive_images': True
    }
}

results = await performance_optimizer.optimize_application(
    project_path='./my-react-app',
    optimization_config=optimization_config
)
```

## Advanced Features

### 1. Real-Time Monitoring

```python
# performance_monitor.py
class RealTimePerformanceMonitor:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alert_system = AlertSystem()

    def monitor_application(self, monitoring_config):
        """Real-time performance monitoring"""
        # Set up performance observers
        observers = self._setup_observers(monitoring_config)

        # Collect real-time metrics
        def metrics_callback(metrics):
            # Analyze performance in real-time
            analysis = self._analyze_real_time_metrics(metrics)

            # Trigger alerts for performance degradation
            if analysis['performance_degradation']:
                self.alert_system.trigger_alert(
                    'performance_degradation',
                    analysis
                )

            # Suggest optimizations
            if analysis['optimization_opportunity']:
                self._suggest_optimization(analysis)

        # Start monitoring
        self.metrics_collector.start_monitoring(
            observers,
            callback=metrics_callback
        )
```

### 2. Bundle Analysis

```python
class BundleAnalyzer:
    def analyze_bundle(self, build_path):
        """Analyze JavaScript bundle for optimization opportunities"""
        analysis = {
            'total_size': 0,
            'chunks': [],
            'duplicate_modules': [],
            'tree_shaking_candidates': [],
            'code_splitting_opportunities': []
        }

        # Analyze each chunk
        for chunk in self._get_chunks(build_path):
            chunk_analysis = self._analyze_chunk(chunk)
            analysis['chunks'].append(chunk_analysis)
            analysis['total_size'] += chunk_analysis['size']

        # Find duplicates across chunks
        analysis['duplicate_modules'] = self._find_duplicates(analysis['chunks'])

        # Identify tree shaking candidates
        analysis['tree_shaking_candidates'] = self._find_unused_exports(analysis['chunks'])

        return analysis
```

### 3. Image Optimization

```python
class ImageOptimizer:
    def optimize_images(self, image_paths, config):
        """Optimize images for web delivery"""
        optimized = []

        for path in image_paths:
            # Analyze image
            original = self._analyze_image(path)

            # Generate optimized variants
            variants = {
                'webp': self._convert_to_webp(path, quality=config.get('webp_quality', 80)),
                'avif': self._convert_to_avif(path, quality=config.get('avif_quality', 75)),
                'responsive': self._generate_responsive_variants(path, config.get('breakpoints', [320, 640, 768, 1024, 1280]))
            }

            optimized.append({
                'original': original,
                'variants': variants,
                'savings': self._calculate_savings(original, variants)
            })

        return optimized
```

## Best Practices

1. **Performance Budgets**: Set and enforce performance limits
2. **Progressive Enhancement**: Load content progressively
3. **Resource Prioritization**: Load critical resources first
4. **Continuous Monitoring**: Track performance over time
5. **Physics-Based Optimization**: Apply efficiency principles from physics

## Optimization Checklist

### Frontend

- [ ] Bundle size under 100KB compressed
- [ ] Tree shaking enabled
- [ ] Code splitting implemented
- [ ] Lazy loading for non-critical resources
- [ ] Images in modern formats (WebP/AVIF)
- [ ] Responsive images with srcset
- [ ] Critical CSS inlined
- [ ] Font loading optimized (font-display: swap)

### Backend

- [ ] Gzip/Brotli compression enabled
- [ ] HTTP/2 or HTTP/3 enabled
- [ ] CDN configured for static assets
- [ ] Database queries optimized
- [ ] Response caching configured
- [ ] Connection pooling enabled
- [ ] Keep-alive connections

### Network

- [ ] DNS prefetch configured
- [ ] Preconnect to critical origins
- [ ] HTTP/2 server push for critical resources
- [ ] Service worker for offline support
- [ ] Resource hints (preload, prefetch)

### Monitoring

- [ ] Core Web Vitals tracked
- [ ] Real User Monitoring (RUM) enabled
- [ ] Synthetic monitoring configured
- [ ] Alert thresholds set
- [ ] Performance regression detection

## Troubleshooting

| Issue | Solution |
|-------|----------|
| High LCP | Optimize largest element, preload critical resources |
| High CLS | Set explicit dimensions, avoid dynamic content insertion |
| High FID | Break up long tasks, use web workers |
| Large bundle | Enable tree shaking, code splitting, dynamic imports |
| Slow TTFB | Optimize server response, enable caching |
| Low cache hit rate | Review cache headers, implement service worker |

---

*Optimize with physics principles: minimize energy (resources) for maximum velocity (user experience).*
