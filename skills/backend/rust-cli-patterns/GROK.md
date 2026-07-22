---
name: "rust-cli-patterns"
category: "backend"
version: "2.0.0"
tags: ["backend", "rust-cli-patterns", "rust", "clap", "cli"]
---

# Rust CLI Patterns

## Overview

Production-grade Rust CLI application development guide covering argument parsing with clap, error handling with anyhow/thiserror, progress indicators, colored output, configuration file management, cross-compilation, CI/CD pipelines, testing strategies, and serialization patterns. This module provides patterns for building fast, reliable, and user-friendly command-line tools.

## Core Capabilities

- Structured argument parsing with clap derive macros and subcommands
- Error handling with anyhow for applications and thiserror for libraries
- Progress bars, spinners, and interactive prompts with indicatif and dialoguer
- Colored and styled terminal output with colored and nu-ansi-term
- Multi-format config files (TOML, YAML, JSON) with layered defaults
- Cross-compilation targeting Linux, macOS, Windows, and musl
- CI/CD with GitHub Actions for testing, linting, and release binaries
- Serialization/deserialization with serde for structured data
- Signal handling, cleanup, and graceful shutdown patterns
- Logging with tracing and env-filter integration

## Usage

```rust
use clap::Parser;
use anyhow::Result;

/// A production-grade CLI tool
#[derive(Parser, Debug)]
#[command(name = "mytool", version, about)]
struct Cli {
    /// Input file path
    #[arg(short, long)]
    input: std::path::PathBuf,

    /// Output format
    #[arg(short, long, value_enum, default_value_t = OutputFormat::Json)]
    format: OutputFormat,

    /// Enable verbose logging
    #[arg(short, long, action)]
    verbose: bool,
}

#[derive(clap::ValueEnum, Clone, Debug)]
enum OutputFormat {
    Json,
    Yaml,
    Table,
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    // Initialize tracing
    let filter = if cli.verbose { "debug" } else { "info" };
    tracing_subscriber::fmt()
        .with_env_filter(filter)
        .init();

    // Run the application
    run(cli)
}

fn run(cli: Cli) -> Result<()> {
    let content = std::fs::read_to_string(&cli.input)?;
    tracing::info!(file = %cli.input.display(), "Processing file");

    match cli.format {
        OutputFormat::Json => println!("{}", serde_json::to_string_pretty(&content)?),
        OutputFormat::Yaml => println!("{}", serde_yaml::to_string(&content)?),
        OutputFormat::Table => println!("{content}"),
    }

    Ok(())
}
```

## Best Practices

- Use clap derive macros over builder API for type-safe arguments
- Always use `anyhow::Result` in binaries and `thiserror` in libraries
- Wrap long-running operations with progress indicators
- Validate inputs early and provide helpful error messages
- Use `std::process::exit` sparingly; prefer returning `Result`
- Set up tracing early in `main()` before any business logic
- Use `tempfile` for temporary files with automatic cleanup
- Prefer `indicatif` over manual progress printing
- Use `assert_cmd` and `predicates` for CLI integration tests
- Cross-compile with `cross` for reliable musl builds

## Related Modules

- `clap` — Command-line argument parsing
- `anyhow` — Application-level error handling
- `thiserror` — Library error type derivation
- `indicatif` — Progress bars and spinners
- `serde` — Serialization framework

---

## Advanced Configuration

### Cargo.toml

```toml
[package]
name = "mytool"
version = "2.0.0"
edition = "2021"
authors = ["Your Name <you@example.com>"]
description = "A production-grade CLI tool"
license = "MIT"
rust-version = "1.75"

[dependencies]
clap = { version = "4", features = ["derive", "env", "unicode"] }
anyhow = "1"
thiserror = "1"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
serde_yaml = "0.9"
toml = "0.8"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
indicatif = "0.17"
colored = "2"
dialoguer = "0.11"
tempfile = "3"
dirs = "5"
directories = "5"

[dev-dependencies]
assert_cmd = "2"
predicates = "3"
assert_fs = "1"
tempfile = "3"

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
panic = "abort"
```

### Layered Configuration

```rust
use serde::Deserialize;
use std::path::PathBuf;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub output_dir: PathBuf,
    pub format: String,
    pub verbose: bool,
    pub max_concurrent: usize,
    pub timeout_seconds: u64,
}

impl Config {
    pub fn load(cli_args: &Cli) -> anyhow::Result<Self> {
        // Layer 1: Built-in defaults
        let mut builder = config::Config::builder()
            .add_source(config::File::with_name("default_config").required(false))
            .add_source(config::File::with_name("config").required(false));

        // Layer 2: User config file
        if let Some(config_path) = &cli_args.config {
            builder = builder.add_source(config::File::from(config_path.as_path()));
        }

        // Layer 3: Environment variables
        builder = builder.add_source(
            config::Environment::with_prefix("MYTOOL")
                .separator("__")
        );

        // Layer 4: CLI arguments override everything
        let mut config: Config = builder.build()?.try_deserialize()?;

        // CLI overrides
        if cli_args.verbose {
            config.verbose = true;
        }
        if let Some(ref output) = cli_args.output {
            config.output_dir = output.clone();
        }

        Ok(config)
    }
}

/// Default config file (default_config.toml)
const DEFAULT_CONFIG: &str = r#"
output_dir = "./output"
format = "json"
verbose = false
max_concurrent = 4
timeout_seconds = 30
"#;
```

### Environment Variable Integration

```rust
use clap::Parser;

#[derive(Parser, Debug)]
#[command(env_prefix = "MYTOOL_")]
struct Cli {
    /// Database URL (env: MYTOOL_DATABASE_URL)
    #[arg(long, env)]
    database_url: String,

    /// API key (env: MYTOOL_API_KEY)
    #[arg(long, env, hide_env_values = true)]
    api_key: String,

    /// Max retries (env: MYTOOL_MAX_RETRIES)
    #[arg(long, env, default_value_t = 3)]
    max_retries: u32,
}
```

---

## Architecture Patterns

```
┌─────────────────────────────────────────────────────┐
│                    CLI Application                   │
│                                                      │
│  ┌───────────────────────────────────────────────┐  │
│  │              Argument Parsing (clap)            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────┐  │  │
│  │  │  Global   │  │Subcommand│  │  Subcommand │  │  │
│  │  │  Flags    │  │   Build  │  │    Test     │  │  │
│  │  └────┬─────┘  └────┬─────┘  └─────┬──────┘  │  │
│  └───────┼──────────────┼──────────────┼──────────┘  │
│          │              │              │              │
│  ┌───────▼──────────────▼──────────────▼──────────┐  │
│  │           Configuration Layer                   │  │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────┐  │  │
│  │  │ Defaults │  │Config File│  │  Env Vars  │  │  │
│  │  └────┬─────┘  └────┬─────┘  └─────┬──────┘  │  │
│  └───────┼──────────────┼──────────────┼──────────┘  │
│          │              │              │              │
│  ┌───────▼──────────────▼──────────────▼──────────┐  │
│  │           Error Handling (anyhow)                │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │  Context → Error → User-friendly message  │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │           Output Layer                        │   │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────┐ │   │
│  │  │  stdout   │  │  stderr  │  │  File I/O  │ │   │
│  │  │ (colored) │  │ (errors) │  │  (results) │ │   │
│  │  └──────────┘  └──────────┘  └────────────┘ │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘

Data Flow:
═════════

  User Input → parse args → load config → validate → execute → format → output
       │                                                            │
       │         ┌──────────────────────────────────────┐          │
       └────────►│  Error chain: anyhow::Context         │◄─────────┘
                 │  ┌────────────────────────────────┐  │
                 │  │ Error: permission denied        │  │
                 │  │ Context: reading config file    │  │
                 │  │ Context: initializing app       │  │
                 │  └────────────────────────────────┘  │
                 └──────────────────────────────────────┘
```

### Subcommand Pattern

```
mytool
├── build          # Build artifacts
│   ├── --release
│   ├── --target
│   └── --verbose
├── test           # Run tests
│   ├── --filter
│   └── --parallel
├── deploy         # Deploy to environment
│   ├── --env (dev|staging|prod)
│   ├── --dry-run
│   └── --confirm
└── config         # Manage configuration
    ├── show
    ├── set <key> <value>
    └── reset
```

---

## Integration Guide

### Progress Bar Integration

```rust
use indicatif::{ProgressBar, ProgressStyle, MultiProgress};
use std::time::Duration;

fn process_with_progress(items: &[Item]) -> anyhow::Result<()> {
    let pb = ProgressBar::new(items.len() as u64);
    pb.set_style(
        ProgressStyle::with_template(
            "{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} {msg}"
        )
        .unwrap()
        .progress_chars("#>-"),
    );

    for item in items {
        // Process item
        process_item(item)?;
        pb.inc(1);
        pb.set_message(format!("Processing {}", item.name));
    }

    pb.finish_with_message("done");
    Ok(())
}

fn multi_progress_example() -> anyhow::Result<()> {
    let multi = MultiProgress::new();

    let pb1 = multi.add(ProgressBar::new(100));
    pb1.set_style(ProgressStyle::with_template(
        "Download: [{bar:30}] {pos}/{len}"
    ).unwrap());

    let pb2 = multi.add(ProgressBar::new(100));
    pb2.set_style(ProgressStyle::with_template(
        "Upload:   [{bar:30}] {pos}/{len}"
    ).unwrap());

    // Simulate concurrent progress
    for i in 0..100 {
        pb1.inc(1);
        if i % 2 == 0 { pb2.inc(1); }
        std::thread::sleep(Duration::from_millis(20));
    }

    pb1.finish_with_message("complete");
    pb2.finish_with_message("complete");
    Ok(())
}
```

### Colored Output

```rust
use colored::*;

fn print_results(results: &[Result]) {
    println!("{}", "Results Summary".bold().underline());
    println!();

    for result in results {
        let status = match result.status {
            Status::Success => "PASS".green().bold(),
            Status::Failure => "FAIL".red().bold(),
            Status::Skipped => "SKIP".yellow(),
        };

        println!(
            "  [{}] {} ({})",
            status,
            result.name.white(),
            result.duration.as_millis().to_string().dimmed(),
        );
    }

    println!();
    let passed = results.iter().filter(|r| r.status == Status::Success).count();
    let total = results.len();
    println!(
        "  {} passed, {} failed, {} total",
        passed.to_string().green().bold(),
        (total - passed).to_string().red().bold(),
        total,
    );
}

fn print_error_chain(err: &anyhow::Error) {
    eprintln!("{}", "Error:".red().bold());
    for (i, cause) in err.chain().enumerate() {
        if i == 0 {
            eprintln!("  {}", cause.to_string().red());
        } else {
            eprintln!("  {}: {}", "caused by".dimmed(), cause.to_string().dimmed());
        }
    }
}
```

### Signal Handling and Cleanup

```rust
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

pub struct Shutdown {
    running: Arc<AtomicBool>,
}

impl Shutdown {
    pub fn new() -> Self {
        let running = Arc::new(AtomicBool::new(true));
        let r = running.clone();

        ctrlc::set_handler(move || {
            tracing::warn!("Received shutdown signal");
            r.store(false, Ordering::SeqCst);
        })
        .expect("Error setting Ctrl-C handler");

        Self { running }
    }

    pub fn is_running(&self) -> bool {
        self.running.load(Ordering::SeqCst)
    }
}

fn main() -> anyhow::Result<()> {
    let shutdown = Shutdown::new();
    let temp_dir = tempfile::tempdir()?;

    // Register cleanup
    let _guard = scopeguard::guard((), |_| {
        tracing::info!("Cleaning up...");
        let _ = std::fs::remove_dir_all(temp_dir.path());
    });

    while shutdown.is_running() {
        process_next_item()?;
    }

    tracing::info!("Graceful shutdown complete");
    Ok(())
}
```

---

## Performance Optimization

| Technique | Impact | When to Use |
|-----------|--------|-------------|
| Parallel processing with rayon | 2-8x throughput | CPU-bound operations on collections |
| Streaming I/O | Constant memory | Large file processing |
| Memory mapping (memmap2) | Reduced copies | Read-heavy large file access |
| Release profile LTO | 10-20% smaller binary | Always for release builds |
| Strip debug symbols | 30-50% smaller binary | Release builds |
| Link-time optimization | 5-15% faster runtime | Release builds |
| Compile-time validation | Zero-cost abstractions | When possible |
| Enum dispatch | Branch prediction hints | Small enum matching |

### Streaming Processing

```rust
use std::io::{BufRead, BufReader};
use std::fs::File;

fn process_large_file(path: &std::path::Path) -> anyhow::Result<usize> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut count = 0;

    for line in reader.lines() {
        let line = line?;
        if line.contains("ERROR") {
            count += 1;
        }
    }

    Ok(count)
}

// Using iterator chains for zero-allocation processing
fn filter_and_transform(input: &[Record]) -> Vec<Record> {
    input
        .iter()
        .filter(|r| r.severity >= Severity::Warning)
        .map(|r| Record {
            message: r.message.to_uppercase(),
            ..r.clone()
        })
        .collect()
}
```

### Parallel Processing with Rayon

```rust
use rayon::prelude::*;

fn process_items_parallel(items: Vec<Item>) -> Vec<Result<Output, Error>> {
    items
        .into_par_iter()
        .map(|item| {
            // Each item processed in parallel
            process_item(item)
        })
        .collect()
}

fn parallel_file_processing(paths: Vec<PathBuf>) -> anyhow::Result<()> {
    paths.par_iter().try_for_each(|path| {
        let content = std::fs::read_to_string(path)?;
        let parsed: Data = serde_json::from_str(&content)?;
        process(parsed)?;
        Ok(())
    })
}
```

---

## Security Considerations

- Never store secrets in config files committed to git; use environment variables or keyring
- Validate all user input before passing to shell commands (prevent injection)
- Use `secrecy` crate for sensitive values (API keys, passwords) to prevent logging
- Set restrictive file permissions on config files containing credentials
- Verify checksums for downloaded binaries in update workflows
- Avoid `unwrap()` in production code; use `expect()` with meaningful messages
- Use `tempfile` for temporary files to prevent race conditions
- Sanitize file paths to prevent directory traversal
- Validate URLs and file paths before network operations
- Use `zeroize` to clear sensitive data from memory

### Secret Management

```rust
use secrecy::{Secret, ExposeSecret};

#[derive(Debug, Deserialize)]
struct Credentials {
    api_key: Secret<String>,
    database_url: Secret<String>,
}

impl Credentials {
    fn from_env() -> anyhow::Result<Self> {
        Ok(Self {
            api_key: Secret::new(
                std::env::var("API_KEY").context("API_KEY not set")?
            ),
            database_url: Secret::new(
                std::env::var("DATABASE_URL").context("DATABASE_URL not set")?
            ),
        })
    }

    fn connect(&self) -> anyhow::Result<Connection> {
        // expose_secret() only when needed for the actual operation
        Connection::new(self.database_url.expose_secret())
    }
}

// Prevent Debug from leaking secrets
impl std::fmt::Debug for Credentials {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Credentials")
            .field("api_key", &"[REDACTED]")
            .field("database_url", &"[REDACTED]")
            .finish()
    }
}
```

---

## Troubleshooting Guide

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| Slow compile times | Large dependency tree, no caching | Use `cargo nextest`, enable `sccache`, reduce features |
| `linker not found` | Missing cross-compilation toolchain | Install target: `rustup target add` |
| `permission denied` on binary | File not executable after install | `chmod +x` or rebuild with `cargo install` |
| Color not showing | `$NO_COLOR` set or non-TTY | Check `colored::control::set_override(true)` |
| Config not loading | File not in expected path | Use `--config` flag or `MYTOOL_CONFIG` env var |
| Panics in production | Unwrap on None/Err | Replace with `context()` and `?` operator |
| Binary too large (>10MB) | Debug symbols, unused deps | `cargo install cargo-embed`, `strip = true` in profile |
| Memory usage grows | Unbounded buffering | Use streaming with `BufReader`/`BufWriter` |
| Ctrl+C not working | Signal handler not registered | Use `ctrlc` crate in `main()` |
| `target/` disk usage | Old build artifacts | `cargo clean`, use `cargo-sweep` |

---

## API Reference

### Clap Derive Macros

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `#[command(...)]` | Configure the parser | `#[command(name = "mytool", version)]` |
| `#[arg(...)]` | Configure a field | `#[arg(short, long, default_value_t = 5)]` |
| `#[arg(value_enum)]` | Enum argument | `#[arg(value_enum, default_value_t = Format::Json)]` |
| `#[command(flatten)]` | Inline nested args | Common options shared across subcommands |
| `#[command(subcommand)]` | Enum subcommands | Each variant becomes a subcommand |
| `#[arg(group = "g")]` | Mutually exclusive args | Only one of the group can be provided |
| `#[arg(hide = true)]` | Hide from help | Internal/debug flags |
| `#[arg(env = "VAR")]` | Read from env var | Fallback to environment variable |

### Error Handling Patterns

```rust
use anyhow::{Context, Result, bail, ensure};

fn read_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .context(format!("Failed to read config from {path}"))?;

    let config: Config = toml::from_str(&content)
        .context("Failed to parse config")?;

    ensure!(
        config.max_connections > 0,
        "max_connections must be positive, got {}",
        config.max_connections
    );

    if config.api_key.is_empty() {
        bail!("API key is required");
    }

    Ok(config)
}
```

---

## Data Models

### CLI Argument Structs

```rust
use clap::{Parser, Subcommand, Args};
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "mytool", version, about, long_about = None)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,

    /// Global configuration file
    #[arg(short, long, global = true)]
    pub config: Option<PathBuf>,

    /// Enable verbose output
    #[arg(short, long, global = true, action)]
    pub verbose: bool,

    /// Dry run mode
    #[arg(short = 'n', long, global = true, action)]
    pub dry_run: bool,
}

#[derive(Subcommand)]
pub enum Commands {
    /// Build project artifacts
    Build(BuildArgs),

    /// Run test suite
    Test(TestArgs),

    /// Deploy to target environment
    Deploy(DeployArgs),
}

#[derive(Args)]
pub struct BuildArgs {
    /// Build in release mode
    #[arg(short, long)]
    pub release: bool,

    /// Target triple
    #[arg(short, long)]
    pub target: Option<String>,

    /// Output directory
    #[arg(short, long, default_value = "./target/output")]
    pub output: PathBuf,

    /// Number of parallel jobs
    #[arg(short, long)]
    pub jobs: Option<usize>,
}

#[derive(Args)]
pub struct TestArgs {
    /// Filter tests by name
    #[arg(short, long)]
    pub filter: Option<String>,

    /// Run tests in parallel
    #[arg(long, default_value_t = true)]
    pub parallel: bool,

    /// Generate coverage report
    #[arg(long)]
    pub coverage: bool,
}

#[derive(Args)]
pub struct DeployArgs {
    /// Target environment
    #[arg(short, long, value_enum)]
    pub env: Environment,

    /// Skip confirmation prompt
    #[arg(long)]
    pub yes: bool,
}

#[derive(clap::ValueEnum, Clone, Debug)]
pub enum Environment {
    Dev,
    Staging,
    Production,
}
```

---

## Deployment Guide

### Cross-Compilation Targets

```bash
# Install targets
rustup target add x86_64-unknown-linux-gnu
rustup target add x86_64-unknown-linux-musl
rustup target add x86_64-apple-darwin
rustup target add aarch64-apple-darwin
rustup target add x86_64-pc-windows-msvc

# Build for musl (static linking)
cargo build --release --target x86_64-unknown-linux-musl

# Using cross for Docker-based builds
cargo install cross
cross build --release --target x86_64-unknown-linux-musl
```

### GitHub Actions CI/CD

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        target:
          - x86_64-unknown-linux-musl
          - x86_64-apple-darwin
          - aarch64-apple-darwin
          - x86_64-pc-windows-msvc

    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.target }}

      - name: Build
        run: cargo build --release --target ${{ matrix.target }}

      - name: Package
        run: |
          cd target/${{ matrix.target }}/release
          tar czf ../../../mytool-${{ matrix.target }}.tar.gz mytool

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: mytool-*.tar.gz
```

---

## Monitoring and Observability

### Tracing Integration

```rust
use tracing::{info, warn, error, debug, instrument};

#[instrument(skip(config), fields(name = %config.name))]
fn process_config(config: &Config) -> anyhow::Result<()> {
    info!("Starting processing");
    debug!(?config, "Full configuration");

    // ... processing ...

    info!("Processing complete");
    Ok(())
}

fn setup_logging(verbose: bool) {
    let filter = if verbose {
        "debug,hyper=info,reqwest=info"
    } else {
        "info,mytool=debug"
    };

    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new(filter))
        )
        .with_target(false)
        .with_thread_ids(true)
        .with_file(true)
        .with_line_number(true)
        .init();
}
```

### Structured Metrics

```rust
use prometheus::{Encoder, TextEncoder, Counter, Histogram, Registry};

lazy_static::lazy_static! {
    static ref REQUEST_COUNT: Counter =
        Counter::new("mytool_requests_total", "Total requests").unwrap();
    static ref REQUEST_DURATION: Histogram =
        Histogram::with_opts(
            histogram_opts!("mytool_request_duration_seconds", "Request duration")
        ).unwrap();
    static ref REGISTRY: Registry = Registry::new();
}

fn record_request(duration: std::time::Duration) {
    REQUEST_COUNT.inc();
    REQUEST_DURATION.observe(duration.as_secs_f64());
}
```

---

## Testing Strategy

### Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use assert_fs::TempDir;

    #[test]
    fn test_parse_args() {
        let cli = Cli::try_parse_from(["mytool", "build", "--release"]).unwrap();
        match cli.command {
            Commands::Build(args) => assert!(args.release),
            _ => panic!("Expected Build command"),
        }
    }

    #[test]
    fn test_config_loading() {
        let temp = TempDir::new().unwrap();
        let config_path = temp.path().join("config.toml");
        std::fs::write(&config_path, r#"
            output_dir = "./output"
            format = "json"
            verbose = false
        "#).unwrap();

        let config = Config::load_from_file(&config_path).unwrap();
        assert_eq!(config.format, "json");
    }

    #[test]
    fn test_error_messages() {
        let result = read_config("/nonexistent/path");
        assert!(result.is_err());
        let err = result.unwrap_err().to_string();
        assert!(err.contains("Failed to read config"));
    }
}
```

### Integration Tests

```rust
use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_cli_help() {
    Command::cargo_bin("mytool")
        .unwrap()
        .arg("--help")
        .assert()
        .success()
        .stdout(predicate::str::contains("A production-grade CLI tool"));
}

#[test]
fn test_build_release() {
    let temp = TempDir::new().unwrap();
    Command::cargo_bin("mytool")
        .unwrap()
        .args(["build", "--release", "--output", temp.path().to_str().unwrap()])
        .assert()
        .success();
}

#[test]
fn test_invalid_input() {
    Command::cargo_bin("mytool")
        .unwrap()
        .arg("build")
        .arg("--invalid-flag")
        .assert()
        .failure()
        .stderr(predicate::str::contains("unexpected argument"));
}
```

---

## Versioning and Migration

### Version Management

```rust
// Cargo.toml uses semantic versioning
// [package]
// version = "2.0.0"

// Check version at runtime
fn check_version() {
    println!("{} v{}", env!("CARGO_PKG_NAME"), env!("CARGO_PKG_VERSION"));
}

// Migration guide in CHANGELOG.md
// - Deprecate old flags with warnings
// - Support both old and new config formats for 1 major version
// - Provide migration command: mytool config migrate
```

### Backward Compatibility

```rust
// Support deprecated flags with warnings
#[arg(long, hide = true, value_parser = parse_deprecated_bool)]
deprecated_flag: Option<bool>,

fn parse_deprecated_bool(s: &str) -> Result<bool, String> {
    tracing::warn!(
        "The --deprecated-flag is deprecated and will be removed in v3.0.0. \
         Use --new-flag instead."
    );
    s.parse::<bool>().map_err(|e| e.to_string())
}
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **clap** | Rust library for parsing command-line arguments with derive macros |
| **anyhow** | Application-level error handling with context chains |
| **thiserror** | Library-level error type derivation for custom error enums |
| **indicatif** | Progress bar and spinner library for terminal output |
| **serde** | Serialization/deserialization framework for structured data |
| **cross** | Docker-based cross-compilation tool for Rust |
| **LTO** | Link-Time Optimization; reduces binary size and improves runtime |
| **musl** | Alternative libc for static linking on Linux |
| **tracing** | Structured logging and diagnostics framework |
| **rayon** | Data parallelism library for iterators |

---

## Changelog

### 2.0.0 (2024-12-01)

- Added layered configuration system (defaults → config file → env vars → CLI)
- Added secret management with secrecy crate patterns
- Added cross-compilation guide for musl and Windows targets
- Added GitHub Actions CI/CD pipeline
- Added tracing integration with structured logging
- Expanded testing strategy with integration tests

### 1.1.0 (2024-06-15)

- Added progress bar patterns with indicatif
- Added colored output examples
- Added signal handling and cleanup patterns
- Added parallel processing with rayon

### 1.0.0 (2024-01-01)

- Initial release
- Core clap patterns
- Basic error handling
- CLI testing with assert_cmd

---

## Contributing Guidelines

1. Fork the repository and create a feature branch
2. Follow Rust naming conventions (snake_case for functions, CamelCase for types)
3. Add tests for new patterns (target: > 90% coverage)
4. Run `cargo clippy` and `cargo fmt` before committing
5. Update this document for any new patterns
6. Submit a pull request with a clear description

### Code Style

- Use `rustfmt` with default settings
- Run `cargo clippy -- -D warnings` with no warnings
- Use `?` operator instead of `.unwrap()` in non-test code
- Document public items with `///` doc comments
- Keep functions under 50 lines

---

## License

MIT License. See [LICENSE](LICENSE) for details.
