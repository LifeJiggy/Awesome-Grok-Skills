# Business Intelligence Agent Architecture

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Deep Dives](#component-deep-dives)
- [Data Flow](#data-flow)
- [Design Patterns](#design-patterns)
- [Technology Stack](#technology-stack)
- [Security Architecture](#security-architecture)
- [Scalability](#scalability)
- [Deployment Architecture](#deployment-architecture)
- [Monitoring & Observability](#monitoring--observability)

---

## Overview

The Business Intelligence (BI) Agent is a comprehensive analytics platform that transforms raw data into actionable business insights. It provides end-to-end BI capabilities including data ingestion, transformation, analysis, visualization, and distribution.

### Core Capabilities

```
┌─────────────────────────────────────────────────────────────────┐
│                    Business Intelligence Agent                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │  Report    │  │ Dashboard │  │   KPI     │  │  Self-    │  │
│  │  Engine    │  │ Designer  │  │  Tracker  │  │  Service  │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │  Viz       │  │  Alert    │  │  Data     │  │  Export   │  │
│  │  Engine    │  │  Manager  │  │  Catalog  │  │  Service  │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Modularity**: Each component is independently testable and replaceable
2. **Extensibility**: Plugin architecture for custom visualizations and data sources
3. **Performance**: Lazy loading, caching, and incremental computation
4. **Security**: Role-based access control at every layer
5. **Scalability**: Horizontal scaling for data processing and rendering

---

## System Architecture

### High-Level Architecture

```
                          ┌──────────────────────┐
                          │     API Gateway       │
                          │    (Rate Limiting)    │
                          └──────────┬───────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
              ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
              │  Report    │   │ Dashboard │   │   KPI     │
              │  Service   │   │  Service  │   │  Service  │
              └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
                    │                │                │
                    └────────────────┼────────────────┘
                                     │
                          ┌──────────▼───────────┐
                          │   Orchestration Layer │
                          │    (Event Bus)        │
                          └──────────┬───────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
        ┌─────▼─────┐         ┌─────▼─────┐         ┌─────▼─────┐
        │   Data     │         │   Query   │         │   Cache   │
        │  Catalog   │         │  Engine   │         │  Layer    │
        └─────┬─────┘         └─────┬─────┘         └─────┬─────┘
              │                      │                      │
              └──────────────────────┼──────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
              ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
              │   SQL      │   │  NoSQL    │   │   Data    │
              │  Database  │   │  Store    │   │   Lake    │
              └───────────┘   └───────────┘   └───────────┘
```

### Component Interaction Matrix

```
                    Report  Dashboard  KPI   Viz    Alert  Self-Svc
                    ──────  ─────────  ────  ────   ─────  ────────
Report Manager        ●        ○        ●     ●      ●       ●
Dashboard Designer    ○        ●        ●     ●      ○       ●
KPI Analyzer          ●        ●        ●     ●      ●       ○
Viz Engine            ●        ●        ●     ●      ○       ●
Alert Manager         ●        ○        ●     ○      ●       ○
Self-Service          ●        ●        ○     ●      ○       ●

● = Direct dependency    ○ = No dependency
```

---

## Component Deep Dives

### 1. Report Manager

The Report Manager handles the lifecycle of business reports from creation through generation and distribution.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Report Manager                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Template    │    │   Scheduler  │    │   Delivery   │     │
│  │   Registry   │───▶│   Service    │───▶│   Service    │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│         │                   │                    │              │
│         ▼                   ▼                    ▼              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Report     │    │   Execution  │    │   Archive    │     │
│  │   Store      │    │   Engine     │    │   Store      │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Responsibilities:**
- Report definition and versioning
- Scheduled and on-demand generation
- Multi-format output (PDF, Excel, HTML, JSON)
- Distribution via email, Slack, webhooks
- Report versioning and audit trail

**Report Generation Flow:**

```
User Request ──▶ Validate Parameters ──▶ Load Template
     │                                        │
     │                                        ▼
     │                               ┌─────────────┐
     │                               │  Execute     │
     │                               │  Queries     │
     │                               └──────┬──────┘
     │                                      │
     │                                      ▼
     │                               ┌─────────────┐
     │                               │  Aggregate   │
     │                               │  Results     │
     │                               └──────┬──────┘
     │                                      │
     │                                      ▼
     │                               ┌─────────────┐
     │                               │  Format      │
     │                               │  Output      │
     │                               └──────┬──────┘
     │                                      │
     ▼                                      ▼
Deliver ─────────────────────────────── Archive
```

### 2. Dashboard Designer

The Dashboard Designer provides visual composition tools for creating interactive data dashboards.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Dashboard Designer                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   Layout    │    │   Widget    │    │   Theme     │        │
│  │   Engine    │    │   Registry  │    │   Manager   │        │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘        │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             │                                   │
│                    ┌────────▼────────┐                          │
│                    │  Composition    │                          │
│                    │  Engine         │                          │
│                    └────────┬────────┘                          │
│                             │                                   │
│              ┌──────────────┼──────────────┐                   │
│              │              │              │                    │
│        ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐             │
│        │  Preview   │ │  Export   │ │  Share    │             │
│        │  Service   │ │  Service  │ │  Service  │             │
│        └───────────┘ └───────────┘ └───────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Widget Types Supported:**

| Widget Type | Data Requirement | Interactivity | Use Case |
|-------------|------------------|---------------|----------|
| KPI Card | Single metric | Drill-down | Executive summary |
| Line Chart | Time series | Zoom, Pan | Trend analysis |
| Bar Chart | Categorical | Sort, Filter | Comparison |
| Pie Chart | Proportional | Highlight | Composition |
| Table | Multi-dimensional | Sort, Paginate | Detail view |
| Funnel | Sequential stages | Tooltip | Conversion analysis |
| Heatmap | Matrix data | Hover | Pattern detection |
| Gauge | Single metric | Threshold | Real-time monitoring |

### 3. KPI Tracker

The KPI Tracker monitors key performance indicators and triggers alerts when thresholds are breached.

```
┌─────────────────────────────────────────────────────────────────┐
│                       KPI Tracker                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    KPI Definition Layer                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │ Formula  │  │ Threshold│  │ Schedule │  │ Owner  │ │   │
│  │  │ Engine   │  │ Manager  │  │ Manager  │  │ Assign │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Calculation Layer                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │ Real-time│  │ Batch    │  │ Rolling  │  │Compare │ │   │
│  │  │ Calc     │  │ Calc     │  │ Window   │  │Periods │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Alerting Layer                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │Threshold │  │ Anomaly  │  │ Trend    │  │ Notif  │ │   │
│  │  │ Check    │  │ Detection│  │ Analysis │  │ Router │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**KPI Status Machine:**

```
                    ┌─────────────┐
                    │   No Data   │
                    └──────┬──────┘
                           │ data received
                           ▼
                    ┌─────────────┐
            ┌──────│  On Track   │──────┐
            │      └──────┬──────┘      │
            │             │             │
     improves│      degrades│      degrades
            │             │             │
            ▼             ▼             ▼
     ┌──────────┐  ┌──────────┐  ┌──────────┐
     │Exceeding │  │ At Risk  │  │ Failing  │
     └──────────┘  └──────────┘  └──────────┘
```

### 4. Visualization Engine

The Visualization Engine renders data into interactive charts and graphs.

```
┌─────────────────────────────────────────────────────────────────┐
│                   Visualization Engine                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Data Input ──▶ ┌─────────────┐ ──▶ ┌─────────────┐            │
│                 │   Transform │     │   Render    │            │
│                 │   Layer     │     │   Layer     │            │
│                 └─────────────┘     └──────┬──────┘            │
│                                            │                    │
│                                    ┌───────▼───────┐           │
│                                    │  Interactivity │           │
│                                    │  Layer         │           │
│                                    └───────┬───────┘           │
│                                            │                    │
│                    ┌───────────────────────┼──────────┐        │
│                    │                       │          │        │
│              ┌─────▼─────┐           ┌─────▼─────┐   │        │
│              │   SVG     │           │  Canvas   │   │        │
│              │  Output   │           │  Output   │   │        │
│              └───────────┘           └───────────┘   │        │
│                                                      │        │
│                                              ┌───────▼──────┐ │
│                                              │   Export     │ │
│                                              │   (PNG/PDF)  │ │
│                                              └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Color Palette System:**

```python
PALETTES = {
    "default": ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"],
    "pastel": ["#a8d8ea", "#f8b4b4", "#b4e8c0", "#f8e4b4", "#d4b4e8"],
    "bold": ["#0056b3", "#dc3545", "#28a745", "#fd7e14", "#6f42c1"],
    "monochrome": ["#2c3e50", "#34495e", "#7f8c8d", "#95a5a6", "#bdc3c7"]
}
```

### 5. Alert Manager

The Alert Manager handles threshold monitoring and notification routing.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Alert Manager                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Alert Rules Engine                      │   │
│  │                                                          │   │
│  │   KPI Value ──▶ Threshold Check ──▶ Severity Assignment │   │
│  │                                              │           │   │
│  │                                              ▼           │   │
│  │                                    ┌──────────────┐      │   │
│  │                                    │ Deduplication│      │   │
│  │                                    │ & Throttling │      │   │
│  │                                    └──────┬───────┘      │   │
│  └───────────────────────────────────────────┼──────────────┘   │
│                                              │                  │
│                    ┌─────────────────────────┼─────────┐       │
│                    │                         │         │       │
│              ┌─────▼─────┐            ┌─────▼─────┐    │       │
│              │   Email   │            │   Slack   │    │       │
│              │  Channel  │            │  Channel  │    │       │
│              └───────────┘            └───────────┘    │       │
│                                                        │       │
│              ┌───────────┐            ┌───────────┐    │       │
│              │   Webhook │            │   In-App  │◀───┘       │
│              │  Channel  │            │  Channel  │            │
│              └───────────┘            └───────────┘            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6. Data Catalog

The Data Catalog maintains metadata about all available data sources.

```
┌─────────────────────────────────────────────────────────────────┐
│                       Data Catalog                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │  Source     │    │  Schema     │    │  Lineage    │        │
│  │  Registry   │    │  Manager    │    │  Tracker    │        │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘        │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             │                                   │
│                    ┌────────▼────────┐                          │
│                    │   Discovery     │                          │
│                    │   Service       │                          │
│                    └────────┬────────┘                          │
│                             │                                   │
│              ┌──────────────┼──────────────┐                   │
│              │              │              │                    │
│        ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐             │
│        │  Search   │ │  Quality  │ │  Access   │             │
│        │  Index    │ │  Rules    │ │  Control  │             │
│        └───────────┘ └───────────┘ └───────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### End-to-End Data Flow

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Data   │    │  Data   │    │  Data   │    │  Data   │    │  Data   │
│ Sources │───▶│ Ingest  │───▶│Transform│───▶│  Store  │───▶│  Serve  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
  ┌──────┐     ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
  │ APIs │     │ ETL  │      │Clean │      │Cache │      │Report│
  │ DBs  │     │Jobs  │      │Enrich│      │Store │      │Dash  │
  │ Files│     │ CDC  │      │Agg   │      │Data  │      │Alert │
  └──────┘     └──────┘      └──────┘      └──────┘      └──────┘
```

### Data Transformation Pipeline

```
Raw Data ──▶ ┌──────────────┐
             │  Validation   │──▶ Invalid ──▶ Error Queue
             └──────┬───────┘
                    │ Valid
                    ▼
             ┌──────────────┐
             │  Cleansing    │──▶ Duplicates ──▶ Dedup Store
             └──────┬───────┘
                    │ Clean
                    ▼
             ┌──────────────┐
             │  Enrichment   │──▶ External Data ──▶ Join
             └──────┬───────┘
                    │ Enriched
                    ▼
             ┌──────────────┐
             │Aggregation    │
             └──────┬───────┘
                    │ Aggregated
                    ▼
             ┌──────────────┐
             │  Serving     │──▶ API / Cache / Export
             │  Layer       │
             └──────────────┘
```

---

## Design Patterns

### 1. Repository Pattern

All data access is abstracted through repository interfaces:

```python
class ReportRepository:
    def save(self, report: Report) -> str: ...
    def get(self, report_id: str) -> Optional[Report]: ...
    def list(self, filters: Dict) -> List[Report]: ...
    def delete(self, report_id: str) -> bool: ...
```

### 2. Strategy Pattern

Visualization rendering uses interchangeable strategies:

```python
class RenderStrategy:
    def render(self, data: Dict, config: Dict) -> Output: ...

class LineChartRender(RenderStrategy): ...
class BarChartRender(RenderStrategy): ...
class PieChartRender(RenderStrategy): ...
```

### 3. Observer Pattern

KPI changes trigger notifications through observers:

```python
class KPIObserver:
    def on_kpi_updated(self, kpi: KPI): ...
    def on_threshold_breached(self, kpi: KPI, threshold: float): ...

class AlertObserver(KPIObserver):
    def on_threshold_breached(self, kpi: KPI, threshold: float):
        self.send_alert(kpi, threshold)
```

### 4. Builder Pattern

Complex reports are built incrementally:

```python
report = (ReportBuilder()
    .set_name("Quarterly Sales")
    .add_metric("revenue")
    .add_dimension("region")
    .set_schedule("quarterly")
    .add_filter({"date_range": "last_quarter"})
    .build())
```

### 5. Factory Pattern

Dashboard creation uses factories for different types:

```python
class DashboardFactory:
    @staticmethod
    def create_executive() -> Dashboard: ...
    @staticmethod
    def create_operational() -> Dashboard: ...
    @staticmethod
    def create_analytical() -> Dashboard: ...
```

---

## Technology Stack

### Core Components

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Gateway | Kong / AWS API Gateway | Rate limiting, authentication |
| Application | Python 3.11+ | Core business logic |
| Query Engine | SQLAlchemy + Pandas | Data transformation |
| Cache | Redis | Query result caching |
| Database | PostgreSQL | Metadata storage |
| Message Queue | RabbitMQ / Kafka | Event processing |
| Scheduler | APScheduler / Celery | Report scheduling |

### Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | React / Vue.js | Dashboard UI |
| Charts | D3.js / Chart.js / ECharts | Visualization |
| State | Redux / Pinia | State management |
| Build | Vite / Webpack | Asset bundling |

### Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Container | Docker | Application packaging |
| Orchestration | Kubernetes | Container management |
| CI/CD | GitHub Actions | Deployment pipeline |
| Monitoring | Prometheus + Grafana | System monitoring |
| Logging | ELK Stack | Log aggregation |

---

## Security Architecture

### Authentication & Authorization

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User ──▶ ┌─────────────┐                                      │
│           │   OAuth2    │                                      │
│           │   / OIDC    │                                      │
│           └──────┬──────┘                                      │
│                  │                                              │
│                  ▼                                              │
│           ┌─────────────┐                                      │
│           │    JWT      │                                      │
│           │   Token     │                                      │
│           └──────┬──────┘                                      │
│                  │                                              │
│    ┌─────────────┼─────────────┐                               │
│    │             │             │                                │
│    ▼             ▼             ▼                                │
│ ┌──────┐    ┌──────┐    ┌──────┐                              │
│ │Role  │    │Data  │    │API   │                              │
│ │Check │    │Filter│    │Limit │                              │
│ └──────┘    └──────┘    └──────┘                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Role-Based Access Control (RBAC)

| Role | Reports | Dashboards | KPIs | Admin |
|------|---------|------------|------|-------|
| Viewer | Read | Read | Read | No |
| Analyst | Read/Write | Read/Write | Read/Write | No |
| Manager | Read/Write | Read/Write | Read/Write | Limited |
| Admin | Full | Full | Full | Full |

### Data Protection

- **Encryption at Rest**: AES-256 for stored data
- **Encryption in Transit**: TLS 1.3 for all connections
- **Data Masking**: PII masking in non-production environments
- **Audit Logging**: All data access logged with user attribution

---

## Scalability

### Horizontal Scaling Architecture

```
                    ┌─────────────────┐
                    │   Load Balancer  │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
      ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
      │  BI Node 1 │   │  BI Node 2 │   │  BI Node 3 │
      └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
            │                │                │
            └────────────────┼────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
        │  Redis    │ │ PostgreSQL│ │  Object   │
        │  Cluster  │ │  Cluster  │ │  Storage  │
        └───────────┘ └───────────┘ └───────────┘
```

### Performance Targets

| Metric | Target | Strategy |
|--------|--------|----------|
| API Response Time | < 200ms | Redis caching |
| Dashboard Load | < 2s | Lazy loading, CDN |
| Report Generation | < 30s | Async processing |
| Query Execution | < 10s | Query optimization |
| Concurrent Users | 1000+ | Horizontal scaling |

### Caching Strategy

```
Request ──▶ ┌─────────────┐
            │    L1       │──── Hit ──▶ Response
            │   Cache     │
            │  (Memory)   │
            └──────┬──────┘
                   │ Miss
                   ▼
            ┌─────────────┐
            │    L2       │──── Hit ──▶ Populate L1 ──▶ Response
            │   Cache     │
            │  (Redis)    │
            └──────┬──────┘
                   │ Miss
                   ▼
            ┌─────────────┐
            │   Source    │──── Populate L1, L2 ──▶ Response
            │   System    │
            └─────────────┘
```

---

## Deployment Architecture

### Docker Compose (Development)

```yaml
version: '3.8'
services:
  bi-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/bi
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache

  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine
```

### Kubernetes (Production)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bi-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bi-agent
  template:
    spec:
      containers:
        - name: bi-agent
          image: bi-agent:latest
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "1Gi"
              cpu: "500m"
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
```

---

## Monitoring & Observability

### Metrics Collection

```
┌─────────────────────────────────────────────────────────────────┐
│                    Observability Stack                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│  │   Metrics   │    │    Logs     │    │   Traces    │        │
│  │ (Prometheus)│    │  (ELK)      │    │  (Jaeger)   │        │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘        │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             │                                   │
│                    ┌────────▼────────┐                          │
│                    │   Grafana       │                          │
│                    │   Dashboard     │                          │
│                    └─────────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Metrics

| Category | Metric | Alert Threshold |
|----------|--------|-----------------|
| Availability | Uptime | < 99.9% |
| Performance | API Latency (p95) | > 500ms |
| Performance | Query Duration | > 10s |
| Errors | Error Rate | > 1% |
| Business | Reports Generated | < expected |
| Business | Active Users | < baseline |

### Health Check Endpoints

```python
@app.route("/health")
def health_check():
    return {
        "status": "healthy",
        "components": {
            "database": check_database(),
            "cache": check_cache(),
            "scheduler": check_scheduler(),
            "storage": check_storage()
        },
        "version": "1.0.0",
        "uptime": get_uptime()
    }
```
