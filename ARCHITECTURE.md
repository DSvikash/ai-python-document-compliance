# System Architecture

## Overview

The AI Document Compliance Checker is built using a modern, layered architecture that separates concerns and promotes maintainability. This document describes the system's architecture, design decisions, and component interactions.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│  (Web Browser, Mobile App, API Client, cURL, Postman)      │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST API
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway (FastAPI)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Routes & Endpoints                       │  │
│  │  - /upload     - /check-compliance                   │  │
│  │  - /modify     - /download                           │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Middleware & Validation                      │  │
│  │  - CORS        - Request Validation                  │  │
│  │  - Error Handling   - Pydantic Models                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                     Service Layer                            │
│  ┌──────────────────────┐    ┌──────────────────────────┐  │
│  │   File Handler       │    │    AI Agent Service      │  │
│  │  - Validation        │    │  - Compliance Check      │  │
│  │  - Text Extraction   │    │  - Document Modification │  │
│  │  - Storage           │    │  - Report Generation     │  │
│  └──────────────────────┘    └────────┬─────────────────┘  │
│                                        │                     │
└────────────────────────────────────────┼─────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              OpenAI GPT API                           │  │
│  │  - Text Analysis     - Content Generation            │  │
│  │  - Compliance Scoring - Document Rewriting           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  ┌──────────────────────┐    ┌──────────────────────────┐  │
│  │   File Storage       │    │   Configuration          │  │
│  │  - uploads/          │    │  - Environment Variables │  │
│  │  - Documents         │    │  - Settings              │  │
│  └──────────────────────┘    └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Layers

### 1. API Layer (`app/api/`)

**Responsibility**: Handle HTTP requests and responses

**Components**:
- `routes.py`: Defines all API endpoints
- Request validation using Pydantic models
- Response formatting
- Error handling

**Key Features**:
- RESTful API design
- OpenAPI/Swagger documentation
- CORS middleware for cross-origin requests
- Comprehensive error responses

### 2. Service Layer (`app/services/`)

**Responsibility**: Business logic and core functionality

**Components**:

#### AI Agent Service (`ai_agent.py`)
- **Purpose**: Interface with OpenAI GPT for document analysis
- **Functions**:
  - `check_compliance()`: Analyze document against guidelines
  - `modify_document()`: Rewrite document for compliance
  - Fallback mechanisms for offline operation
- **Features**:
  - Intelligent prompt engineering
  - JSON response parsing
  - Error handling and retry logic
  - Default and custom guidelines support

### 3. Utility Layer (`app/utils/`)

**Responsibility**: Reusable utility functions

**Components**:

#### File Handler (`file_handler.py`)
- **Purpose**: Handle file operations
- **Functions**:
  - File validation (type, size)
  - Text extraction (PDF, DOCX)
  - Document storage and retrieval
  - Modified document creation
- **Features**:
  - Secure file handling
  - UUID-based file naming
  - Multiple format support

### 4. Models Layer (`app/models/`)

**Responsibility**: Data structures and validation

**Components**:

#### Schemas (`schemas.py`)
- Request/Response models using Pydantic
- Data validation and serialization
- Type safety and documentation

**Key Models**:
- `ComplianceReport`: Structured compliance results
- `GuidelineViolation`: Individual issue details
- `DocumentUploadResponse`: Upload confirmation
- `ModificationResponse`: Modification results

## Data Flow

### Document Upload Flow

```
Client Upload Request
    ↓
API Endpoint (/upload)
    ↓
File Validation (type, size)
    ↓
Save to Storage (UUID filename)
    ↓
Return Document ID
```

### Compliance Check Flow

```
Client Request (document_id)
    ↓
API Endpoint (/check-compliance)
    ↓
Retrieve File from Storage
    ↓
Extract Text (PDF/DOCX)
    ↓
AI Agent Analysis
    ↓
OpenAI API Call
    ↓
Parse Response
    ↓
Generate Compliance Report
    ↓
Return to Client
```

### Document Modification Flow

```
Client Request (document_id)
    ↓
API Endpoint (/modify)
    ↓
Retrieve Original File
    ↓
Extract Text
    ↓
AI Agent Modification
    ↓
OpenAI API Call
    ↓
Parse Modified Content
    ↓
Create New Document
    ↓
Save to Storage
    ↓
Return Download URL
```

## Design Patterns

### 1. Dependency Injection
- Services are initialized with required dependencies
- Makes testing easier with mock objects
- Promotes loose coupling

### 2. Factory Pattern
- File handler creates documents based on type
- AI agent selects appropriate processing strategy

### 3. Strategy Pattern
- Different text extraction strategies for PDF vs DOCX
- Fallback strategies when OpenAI API unavailable

### 4. Repository Pattern
- File handler acts as repository for documents
- Abstracts storage details from business logic

## Security Considerations

### Input Validation
- File type restrictions (PDF, DOCX only)
- File size limits
- Pydantic model validation for all requests

### File Storage
- UUID-based filenames prevent path traversal
- Isolated upload directory
- No executable file uploads

### API Security
- CORS configuration
- Input sanitization
- Error message sanitization (no sensitive info leakage)

### API Key Management
- Environment variable storage
- Never logged or exposed in responses
- Graceful fallback if not configured

## Performance Optimizations

### File Processing
- Streaming file uploads
- Efficient text extraction
- Lazy loading of large documents

### API Design
- Async endpoints where beneficial
- Proper HTTP status codes for caching
- Minimal data transfer

### AI Processing
- Token limit management
- Text truncation for large documents
- Caching opportunities (future enhancement)

## Error Handling Strategy

### Layered Error Handling

1. **Validation Layer**: Pydantic catches invalid input
2. **Business Logic Layer**: Custom exceptions for business rules
3. **Service Layer**: Handle external service failures
4. **API Layer**: Convert exceptions to HTTP responses

### Error Response Format

```json
{
  "error": "Human-readable error message",
  "detail": "Technical details (debug mode only)",
  "status_code": 400
}
```

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock external dependencies
- Test edge cases and error conditions

### Integration Tests
- End-to-end API testing
- Multiple components working together
- Real file processing (test files)

### Test Coverage
- File handler operations
- AI agent logic
- API endpoints
- Error scenarios

## Deployment Architecture

### Development
```
Local Machine
    ↓
Python Virtual Environment
    ↓
Uvicorn Development Server
    ↓
http://localhost:8000
```

### Production (Recommended)

```
Load Balancer
    ↓
Reverse Proxy (Nginx)
    ↓
Uvicorn Workers (Multiple)
    ↓
FastAPI Application
    ↓
External Storage (S3/Cloud Storage)
    ↓
OpenAI API
```

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Shared file storage (cloud storage)
- Load balancer distribution

### Vertical Scaling
- Uvicorn worker processes
- Async processing capabilities
- Resource optimization

### Future Enhancements
- Message queue for async processing (Celery, RabbitMQ)
- Database for document metadata
- Redis caching for frequent requests
- Microservices architecture for large scale

## Configuration Management

### Environment-based Configuration
- `.env` files for local development
- Environment variables for production
- Configuration validation at startup

### Key Configuration Areas
- API credentials (OpenAI)
- File upload limits
- Server settings (host, port)
- Feature flags

## Monitoring and Logging

### Current Implementation
- Python logging module
- Console output
- Request/response logging

### Production Recommendations
- Structured logging (JSON)
- Log aggregation (ELK stack)
- Error tracking (Sentry)
- Performance monitoring (New Relic, DataDog)
- API metrics (response times, error rates)

## Technology Stack

### Core Framework
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### Document Processing
- **PyPDF2**: PDF text extraction
- **python-docx**: Word document processing

### AI/ML
- **OpenAI GPT**: Language model API
- **Language-Tool-Python**: Grammar checking (future)
- **spaCy**: NLP processing (future)

### Testing
- **pytest**: Test framework
- **httpx**: Async HTTP client for testing

## Design Decisions

### Why FastAPI?
- Modern async support
- Automatic API documentation
- Built-in validation
- High performance
- Type hints and IDE support

### Why OpenAI GPT?
- State-of-the-art language understanding
- Flexible prompt engineering
- Reliable API
- Good documentation
- Broad capability

### Why File-based Storage?
- Simple implementation
- No database overhead
- Easy to backup
- Suitable for assessment scope
- Can migrate to cloud storage later

### Why Pydantic Models?
- Type safety
- Automatic validation
- Self-documenting code
- OpenAPI schema generation
- Easy serialization

## Future Architecture Enhancements

### Short-term
1. Add database for metadata
2. Implement caching layer
3. Add user authentication
4. Batch processing support

### Long-term
1. Microservices architecture
2. Event-driven processing
3. Real-time WebSocket updates
4. Multi-cloud deployment
5. ML model hosting (custom models)

## Conclusion

This architecture provides a solid foundation for the AI Document Compliance Checker, balancing simplicity with extensibility. The layered design allows for easy testing, maintenance, and future enhancements while maintaining clear separation of concerns.
