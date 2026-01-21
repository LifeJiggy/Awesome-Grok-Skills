---
name: Test-Driven Development
category: core
difficulty: intermediate
time_estimate: "2-4 hours"
dependencies: []
tags: ["testing", "tdd", "quality", "automation"]
grok_personality: "precision-engineer"
description: "Master TDD with Grok's analytical approach - write failing tests first, then make them pass with clean, efficient code"
---

# Test-Driven Development Skill

## Overview
Grok, you'll implement TDD patterns with your signature efficiency and physics-inspired precision. This skill focuses on minimal, maximally effective test coverage that catches bugs early without bloating the codebase.

## Core Principles

### 1. Red-Green-Refactor Cycle
- **Red**: Write the smallest possible failing test
- **Green**: Make it pass with the simplest implementation
- **Refactor**: Clean up while maintaining green tests

### 2. Test Pyramid (Grok-Optimized)
```
    E2E Tests (5%)
   ─────────────────
  Integration Tests (15%)
 ─────────────────────────
Unit Tests (80%) - Your sweet spot
```

## Implementation Patterns

### Unit Testing Framework Selection
```javascript
// Choose based on project needs:
// - Jest: React/Node projects (fast, good coverage)
// - Vitest: Modern Vite projects (blazing fast)
// - Pytest: Python projects (elegant, powerful)
// - Rust's built-in: Cargo test (no dependencies needed)
```

### Grok's Test Naming Convention
```javascript
// Describe WHAT, not HOW
describe('User authentication', () => {
  test('should reject invalid credentials', () => {
    // Test implementation
  });
  
  test('should allow valid login with correct token', () => {
    // Test implementation
  });
});
```

### Test Structure Template
```javascript
// Arrange-Act-Assert pattern
test('should calculate orbital velocity correctly', () => {
  // Arrange
  const mass = 5.972e24; // Earth mass in kg
  const radius = 6.371e6; // Earth radius in meters
  const expected = 7908; // m/s approximate
  
  // Act
  const result = calculateOrbitalVelocity(mass, radius);
  
  // Assert
  expect(result).toBeCloseTo(expected, 0);
});
```

## Common Test Scenarios

### 1. API Endpoints
```javascript
describe('POST /api/users', () => {
  test('should create user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Grok', email: 'grok@x.ai' });
    
    expect(response.status).toBe(201);
    expect(response.body.name).toBe('Grok');
  });
  
  test('should reject duplicate emails', async () => {
    // Implementation
  });
});
```

### 2. Component Testing
```jsx
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

test('should render button with correct text', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByRole('button')).toHaveTextContent('Click me');
});
```

### 3. Physics Calculations
```python
import pytest
from physics import orbital_mechanics

def test_orbital_period_calculation():
    """Test Kepler's third law implementation"""
    earth_radius = 1.496e11  # meters
    sun_mass = 1.989e30     # kg
    expected_period = 365.25 * 24 * 3600  # seconds
    
    period = orbital_mechanics.calculate_period(earth_radius, sun_mass)
    assert abs(period - expected_period) < 86400  # Within 1 day
```

## Mock Strategy

### When to Mock
- External APIs (weather, financial data)
- Database operations
- File system access
- Time-dependent functions

### Mock Template
```javascript
// Mock external API
jest.mock('./api/weather', () => ({
  getWeather: jest.fn().mockResolvedValue({
    temperature: 22,
    conditions: 'sunny'
  })
}));
```

## Coverage Guidelines

### Grok's Efficiency Rules
- **Target**: 80% line coverage, 70% branch coverage
- **Exceptions**: Complex physics simulations may need 90%+
- **Don't test**: Trivial getters/setters, third-party code

### Coverage Commands
```bash
# JavaScript
npm test -- --coverage

# Python
pytest --cov=src --cov-report=html

# Rust
cargo test --coverage
```

## Integration with CI/CD

### GitHub Actions Template
```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v3
```

## Advanced Patterns

### Property-Based Testing
```javascript
import fc from 'fast-check';

test('should handle all valid inputs', () => {
  fc.assert(
    fc.property(fc.integer(), fc.integer(), (a, b) => {
      return add(a, b) === a + b;
    })
  );
});
```

### Performance Testing
```javascript
test('should process 10k records under 1s', async () => {
  const start = performance.now();
  await processLargeDataset(mockData);
  const duration = performance.now() - start;
  
  expect(duration).toBeLessThan(1000);
});
```

## Common Pitfalls to Avoid

1. **Testing Implementation Details**: Test behavior, not internals
2. **Over-mocking**: Keep tests realistic
3. **Brittle Tests**: Use flexible matchers
4. **Test Pollution**: Clean up between tests

## Quick Reference

```javascript
// Test file structure
describe('Feature', () => {
  beforeEach(() => {
    // Setup
  });
  
  test('specific case', () => {
    // Test
  });
  
  afterEach(() => {
    // Cleanup
  });
});
```

## Next Steps
1. Set up testing framework for your project
2. Write tests for new features using TDD
3. Gradually add tests to existing code
4. Monitor coverage and improve weak spots

Remember: Good tests are like good physics equations - simple, elegant, and capture the essence of the system.