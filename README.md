# AI Document Compliance Checker

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

An AI-powered system that processes document files (PDF/Word) and checks compliance against English writing guidelines. Built with FastAPI and powered by OpenAI GPT for intelligent document analysis and modification.

## 📋 Features

- **Document Upload**: Accept PDF and Word (.docx) documents via REST API
- **AI-Powered Compliance Checking**: Analyze documents against English writing guidelines
- **Detailed Compliance Reports**: Get comprehensive reports with:
  - Overall compliance status and score
  - Specific violations with severity levels
  - Line-by-line suggestions for improvement
  - Category-based analysis (grammar, style, clarity, structure)
- **Intelligent Document Modification**: AI agent can modify documents to comply with guidelines
- **Interactive API**: RESTful API with comprehensive documentation
- **Secure File Handling**: Validation, size limits, and secure storage
- **Comprehensive Testing**: Unit and integration tests included

## 🏗️ Architecture

```
ai-document-compliance-checker/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py          # FastAPI routes
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   └── ai_agent.py        # AI compliance agent
│   ├── utils/                 # Utilities
│   │   ├── __init__.py
│   │   └── file_handler.py   # File processing
│   ├── __init__.py
│   ├── config.py              # Configuration
│   └── main.py                # FastAPI app entry point
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_api.py           # API integration tests
│   ├── test_file_handler.py  # File handler unit tests
│   └── test_ai_agent.py      # AI agent unit tests
├── uploads/                   # Uploaded documents storage
├── docs/                      # Additional documentation
├── .env.example              # Environment variables template
├── .gitignore
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- OpenAI API key (optional but recommended for full functionality)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-document-compliance-checker
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

5. **Run the application**
```bash
python -m app.main
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Quick Test

```bash
# Health check
curl http://localhost:8000/api/v1/health

# View API documentation
Open http://localhost:8000/docs in your browser
```

## 📚 API Documentation

### Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### 1. Upload Document

Upload a PDF or Word document for analysis.

```bash
POST /api/v1/upload
Content-Type: multipart/form-data

# Example with curl
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "document_id": "uuid-string",
  "filename": "document.pdf",
  "file_size": 12345,
  "file_type": "pdf",
  "message": "Document uploaded successfully"
}
```

#### 2. Check Compliance

Analyze document compliance against English writing guidelines.

```bash
POST /api/v1/check-compliance
Content-Type: application/json

# Example
curl -X POST "http://localhost:8000/api/v1/check-compliance" \
  -H "Content-Type: application/json" \
  -d '{"document_id": "uuid-string"}'
```

**Request Body:**
```json
{
  "document_id": "uuid-string",
  "guidelines": [  // Optional custom guidelines
    "Use active voice",
    "Keep sentences concise"
  ]
}
```

**Response:**
```json
{
  "document_id": "uuid-string",
  "report": {
    "status": "partial",
    "score": 75.5,
    "total_issues": 3,
    "violations": [
      {
        "line_number": 5,
        "issue": "Passive voice detected",
        "suggestion": "Use active voice for clarity",
        "severity": "medium",
        "category": "style"
      }
    ],
    "summary": "Document shows good compliance with minor issues",
    "suggestions": [
      "Consider reviewing paragraph structure",
      "Check for consistent tense usage"
    ]
  }
}
```

#### 3. Modify Document

Request AI to modify document to comply with guidelines.

```bash
POST /api/v1/modify
Content-Type: application/json

# Example
curl -X POST "http://localhost:8000/api/v1/modify" \
  -H "Content-Type: application/json" \
  -d '{"document_id": "uuid-string"}'
```

**Request Body:**
```json
{
  "document_id": "uuid-string",
  "guidelines": [  // Optional
    "Use active voice",
    "Simplify complex sentences"
  ],
  "preserve_formatting": true
}
```

**Response:**
```json
{
  "document_id": "original-uuid",
  "modified_document_id": "modified-uuid",
  "download_url": "/api/v1/download/modified_file.docx",
  "changes_made": 12,
  "summary": "Modified document for better compliance with guidelines"
}
```

#### 4. Download Document

Download original or modified document.

```bash
GET /api/v1/download/{filename}

# Example
curl -O "http://localhost:8000/api/v1/download/modified_file.docx"
```

#### 5. Health Check

Check API status and configuration.

```bash
GET /api/v1/health

# Response
{
  "status": "healthy",
  "app_name": "AI Document Compliance Checker",
  "version": "1.0.0",
  "openai_configured": true
}
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

## 🔧 Configuration

Configure the application by setting environment variables in `.env`:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Application Configuration
APP_NAME=AI Document Compliance Checker
APP_VERSION=1.0.0
DEBUG=True

# File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=pdf,docx

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## 📖 English Guidelines

The AI agent checks documents against comprehensive English writing guidelines including:

1. **Clarity**: Clear and concise language
2. **Grammar**: Proper grammar and punctuation
3. **Voice**: Active voice preference
4. **Consistency**: Consistent tense and style
5. **Structure**: Proper sentence and paragraph structure
6. **Tone**: Appropriate professional tone
7. **Spelling**: Spelling accuracy
8. **Simplicity**: Avoiding unnecessary jargon

You can also provide custom guidelines in API requests.

## 🔍 How It Works

1. **Upload**: User uploads a PDF or Word document via API
2. **Text Extraction**: System extracts text from the document
3. **AI Analysis**: OpenAI GPT analyzes the text against guidelines
4. **Report Generation**: Detailed compliance report is generated
5. **Modification (Optional)**: AI can rewrite document for compliance
6. **Download**: User can download original or modified document

## 🛡️ Security Features

- File type validation (only PDF and DOCX allowed)
- File size limits (configurable, default 10MB)
- Secure file storage with unique IDs
- Input validation using Pydantic models
- Error handling and logging
- CORS configuration for API access control

## 🚧 Limitations & Future Enhancements

### Current Limitations
- PDF modification creates text file (not formatted PDF)
- OpenAI API key required for full functionality
- Fallback mode has limited analysis capabilities

### Planned Enhancements
- Support for additional document formats
- Enhanced PDF modification with formatting preservation
- Batch document processing
- User authentication and document management
- Advanced customization of guidelines
- Integration with grammar checking libraries (spaCy, LanguageTool)
- Asynchronous processing for large documents
- Document comparison and diff views

## 📊 Performance Considerations

- Large documents may take longer to process
- API response times depend on OpenAI API latency
- File size limits help maintain performance
- Async processing recommended for production use

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Author

Created as part of the AI Python Developer Assessment.

## 🙏 Acknowledgments

- FastAPI framework for excellent API development
- OpenAI for powerful language models
- PyPDF2 and python-docx for document processing

## 📞 Support

For questions or issues:
- Open an issue in the GitHub repository
- Check the API documentation at `/docs`
- Review the test files for usage examples

---

**Note**: This is an assessment project demonstrating AI-powered document processing capabilities. For production use, consider additional security measures, scalability improvements, and comprehensive error handling.
