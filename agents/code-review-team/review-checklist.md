# Code Review Checklist

## 🎯 Performance Review
- [ ] Algorithmic efficiency (time/space complexity)
- [ ] Memory usage and potential leaks
- [ ] Database query optimization
- [ ] Network request batching
- [ ] Bundle size impact
- [ ] Rendering performance (React/Vue/Angular)

## 🔒 Security Review
- [ ] Input validation and sanitization
- [ ] Authentication and authorization
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Sensitive data exposure
- [ ] Dependency vulnerabilities

## 🧪 Code Quality Review
- [ ] Function and variable naming
- [ ] Code organization and structure
- [ ] Comments and documentation
- [ ] Error handling
- [ ] Edge cases covered
- [ ] Code duplication
- [ ] SOLID principles adherence

## 🧪 Testing Review
- [ ] Unit test coverage
- [ ] Integration tests
- [ ] E2E tests for critical paths
- [ ] Test naming and organization
- [ ] Mock usage appropriateness
- [ ] Test data management

## 📱 Specific Reviews

### Frontend Focus
- [ ] Accessibility (WCAG compliance)
- [ ] Responsive design
- [ ] Browser compatibility
- [ ] SEO optimization
- [ ] Loading performance
- [ ] User experience patterns

### Backend Focus
- [ ] API design consistency
- [ ] Rate limiting
- [ ] Caching strategies
- [ ] Logging and monitoring
- [ ] Error response format
- [ ] API documentation

### Database Focus
- [ ] Index usage
- [ ] Query optimization
- [ ] Data normalization
- [ ] Backup strategies
- [ ] Connection pooling
- [ ] Migration scripts

## 🚀 Deployment Review
- [ ] Environment configuration
- [ ] CI/CD pipeline
- [ ] Monitoring and alerting
- [ ] Rollback strategy
- [ ] Health checks
- [ ] Resource allocation

## 💬 Review Communication

### Positive Feedback Patterns
- "Great use of [pattern] to solve [problem]"
- "Excellent separation of concerns"
- "Well-structured error handling"
- "Clean, readable code"

### Constructive Feedback Patterns
- "Consider extracting [logic] into a separate function"
- "This could benefit from memoization"
- "Think about edge cases like [scenario]"
- "Let's ensure we validate user input here"

### Suggestion Hierarchy
1. **Critical**: Security, performance, correctness
2. **Important**: Code quality, maintainability  
3. **Nice to have**: Style, minor optimizations

## 📊 Review Metrics

### Code Quality Score
- **Performance**: 25%
- **Security**: 25%
- **Maintainability**: 20%
- **Testing**: 15%
- **Documentation**: 15%

### Approval Thresholds
- **Auto-approve**: Score > 90
- **Minor changes**: Score 80-90
- **Major changes**: Score 70-79
- **Reject**: Score < 70

## 🔄 Review Process

### Automated Checks (Pre-review)
```bash
npm run lint
npm run typecheck  
npm run test:coverage
npm run security-audit
bundlephobia check
```

### Manual Review Steps
1. **High-level understanding** (5 min)
2. **Line-by-line review** (15-30 min)
3. **Performance analysis** (10 min)
4. **Security assessment** (10 min)
5. **Final recommendation** (5 min)

### Post-review Actions
- [ ] Create issues for major problems
- [ ] Suggest refactoring opportunities
- [ ] Document decisions made
- [ ] Update team guidelines