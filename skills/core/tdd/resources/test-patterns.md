# Test Patterns & Templates

## Unit Test Templates

### JavaScript/TypeScript
```javascript
// Async function test template
test('should handle async operations correctly', async () => {
  // Arrange
  const inputData = { /* test data */ };
  const expectedResult = { /* expected */ };
  
  // Act
  const result = await functionUnderTest(inputData);
  
  // Assert
  expect(result).toEqual(expectedResult);
});

// Error handling template
test('should throw appropriate error for invalid input', () => {
  // Arrange
  const invalidInput = { /* invalid data */ };
  
  // Act & Assert
  expect(() => functionUnderTest(invalidInput))
    .toThrow('Expected error message');
});
```

### Python
```python
# Pytest fixture template
@pytest.fixture
def sample_data():
    return {"key": "value", "number": 42}

def test_function_with_fixture(sample_data):
    result = process_data(sample_data)
    assert result["status"] == "success"

# Mock template
@patch('module.external_service')
def test_with_mock(mock_service):
    mock_service.return_value = {"data": "mocked"}
    result = call_external()
    assert result["data"] == "mocked"
```

## Integration Test Templates

### API Testing
```javascript
describe('API Integration', () => {
  test('POST /api/endpoint', async () => {
    const response = await request(app)
      .post('/api/endpoint')
      .send({ data: 'test' })
      .expect(201);
      
    expect(response.body.success).toBe(true);
  });
});
```

### Database Testing
```python
def test_database_transaction():
    with test_db.transaction():
        user = User.create(name="Test User")
        assert user.id is not None
        # Transaction will roll back
```

## Test Data Generators

### JavaScript
```javascript
// Factory pattern
const createUser = (overrides = {}) => ({
  id: faker.datatype.uuid(),
  name: faker.name.findName(),
  email: faker.internet.email(),
  ...overrides
});
```

### Python
```python
# Factory pattern with factory_boy
class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    name = factory.Faker('name')
    email = factory.Faker('email')
```

## Common Assertions

### JavaScript
```javascript
// Object matching
expect(result).toEqual(expect.objectContaining({
  name: 'John',
  age: expect.any(Number)
}));

// Array matching
expect(items).toEqual(
  expect.arrayContaining([
    expect.objectContaining({ id: 1 })
  ])
);
```

### Python
```python
# Dictionary matching
assert result == {'name': 'John', 'age': 30}

# List matching
assert any(item['id'] == 1 for item in items)
```