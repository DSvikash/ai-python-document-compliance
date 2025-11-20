# Contributing to AI Document Compliance Checker

Thank you for your interest in contributing to the AI Document Compliance Checker project!

## Development Setup

1. **Fork and Clone**
```bash
git clone https://github.com/YOUR_USERNAME/ai-python-document-compliance.git
cd ai-python-document-compliance
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

## Development Workflow

1. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make Changes**
- Write clean, documented code
- Follow PEP 8 style guidelines
- Add tests for new features

3. **Run Tests**
```bash
pytest
pytest --cov=app  # With coverage
```

4. **Commit Changes**
```bash
git add .
git commit -m "feat: description of your changes"
```

5. **Push and Create PR**
```bash
git push origin feature/your-feature-name
```

## Coding Standards

### Python Style
- Follow PEP 8
- Use type hints
- Write docstrings for all functions/classes
- Maximum line length: 100 characters

### Code Structure
- Keep functions small and focused
- Use meaningful variable names
- Comment complex logic
- Avoid code duplication

### Testing
- Write tests for all new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test edge cases and error conditions

## Commit Messages

Follow conventional commits format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

Example:
```
feat: add support for .txt file uploads

- Extended file handler to support text files
- Updated validation logic
- Added tests for text file processing
```

## Pull Request Process

1. **Before Submitting**
   - Ensure all tests pass
   - Update documentation if needed
   - Add entry to CHANGELOG if applicable
   - Rebase on latest main branch

2. **PR Description**
   - Describe what changes were made
   - Explain why the changes were necessary
   - Reference related issues
   - Include screenshots for UI changes

3. **Code Review**
   - Address reviewer comments
   - Keep PRs focused and small
   - Be open to feedback

## Testing Guidelines

### Unit Tests
```python
def test_feature_name():
    """Test description."""
    # Arrange
    input_data = ...
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_value
```

### Integration Tests
```python
def test_api_endpoint():
    """Test API endpoint behavior."""
    response = client.post("/api/v1/endpoint", json=data)
    assert response.status_code == 200
```

## Documentation

### Code Documentation
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When validation fails
    """
    pass
```

### API Documentation
- Update OpenAPI schemas for new endpoints
- Add examples to docstrings
- Update API_EXAMPLES.md for significant changes

## Issue Reporting

### Bug Reports
Include:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack traces

### Feature Requests
Include:
- Use case description
- Proposed solution
- Alternative solutions considered
- Additional context

## Questions?

- Open an issue for discussion
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).
