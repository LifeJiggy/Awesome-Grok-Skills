#!/bin/bash

# Test Runner Script - Automated Test Execution and Coverage

set -e

PROJECT_TYPE=${1:-auto}
COVERAGE=${2:-true}

detect_project_type() {
  if [ -f "package.json" ]; then
    echo "node"
  elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
    echo "python"
  elif [ -f "Cargo.toml" ]; then
    echo "rust"
  elif [ -f "go.mod" ]; then
    echo "go"
  else
    echo "unknown"
  fi
}

run_node_tests() {
  echo "🧪 Running Node.js tests..."
  
  # Check if Jest is configured
  if [ -f "jest.config.js" ] || grep -q "jest" package.json; then
    if [ "$COVERAGE" = "true" ]; then
      npm test -- --coverage --watchAll=false
    else
      npm test -- --watchAll=false
    fi
  # Check if Vitest is configured
  elif [ -f "vitest.config.js" ] || grep -q "vitest" package.json; then
    if [ "$COVERAGE" = "true" ]; then
      npm run test:coverage
    else
      npm run test
    fi
  else
    echo "❌ No test framework detected. Please configure Jest or Vitest."
    exit 1
  fi
}

run_python_tests() {
  echo "🧪 Running Python tests..."
  
  if [ "$COVERAGE" = "true" ]; then
    pytest --cov=. --cov-report=html --cov-report=term
  else
    pytest -v
  fi
}

run_rust_tests() {
  echo "🧪 Running Rust tests..."
  
  if [ "$COVERAGE" = "true" ]; then
    cargo install cargo-tarpaulin 2>/dev/null || true
    cargo tarpaulin --out Html
  else
    cargo test
  fi
}

run_go_tests() {
  echo "🧪 Running Go tests..."
  
  if [ "$COVERAGE" = "true" ]; then
    go test -coverprofile=coverage.out ./...
    go tool cover -html=coverage.out
  else
    go test ./...
  fi
}

# Main execution
if [ "$PROJECT_TYPE" = "auto" ]; then
  PROJECT_TYPE=$(detect_project_type)
fi

echo "📋 Detected project type: $PROJECT_TYPE"

case $PROJECT_TYPE in
  "node")
    run_node_tests
    ;;
  "python")
    run_python_tests
    ;;
  "rust")
    run_rust_tests
    ;;
  "go")
    run_go_tests
    ;;
  *)
    echo "❌ Unknown project type: $PROJECT_TYPE"
    echo "Usage: $0 [node|python|rust|go|auto] [coverage|no-coverage]"
    exit 1
    ;;
esac

echo "✅ Tests completed successfully!"