# 🎬 AI Document Compliance Checker - Demo Guide

This guide demonstrates how to use the AI Document Compliance Checker system.

## 🚀 Quick Start

### Step 1: Start the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python -m app.main
```

The server will start at `http://localhost:8000`

### Step 2: Access API Documentation

Open your browser and navigate to:
```
http://localhost:8000/docs
```

You'll see the interactive Swagger UI with all available endpoints.

## 📝 Demo Scenarios

### Scenario 1: Basic Document Upload and Compliance Check

#### Create a Sample Document

Save this as `sample.txt` (we'll upload it as a test):
```text
THIS IS A TEST DOCUMENT. the document contain some errors. It have grammar mistakes and 
style issues that need to be fixed. The document is written in passive voice which should 
be avoided. this sentence dont have proper capitalization.
```

#### Step 1: Upload the Document

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@sample.pdf" \
  -H "accept: application/json"
```

**Using Python:**
```python
import requests

with open('sample.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/v1/upload', files=files)
    
doc_id = response.json()['document_id']
print(f"Document ID: {doc_id}")
```

**Response:**
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "sample.pdf",
  "file_size": 12345,
  "file_type": "pdf",
  "message": "Document uploaded successfully"
}
```

#### Step 2: Check Compliance

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/check-compliance" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

**Using Python:**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/check-compliance',
    json={'document_id': doc_id}
)

report = response.json()['report']
print(f"Status: {report['status']}")
print(f"Score: {report['score']}/100")
print(f"Issues Found: {report['total_issues']}")

for violation in report['violations']:
    print(f"\n❌ {violation['issue']}")
    print(f"   💡 Suggestion: {violation['suggestion']}")
    print(f"   ⚠️  Severity: {violation['severity']}")
```

**Expected Response:**
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "report": {
    "status": "non_compliant",
    "score": 45.0,
    "total_issues": 5,
    "violations": [
      {
        "line_number": null,
        "issue": "Text is all uppercase",
        "suggestion": "Use proper capitalization",
        "severity": "medium",
        "category": "style"
      },
      {
        "issue": "Grammar error: 'contain' should be 'contains'",
        "suggestion": "Use correct verb form",
        "severity": "high",
        "category": "grammar"
      },
      {
        "issue": "Passive voice detected",
        "suggestion": "Use active voice for clarity",
        "severity": "medium",
        "category": "style"
      }
    ],
    "summary": "Document has multiple compliance issues requiring attention",
    "suggestions": [
      "Review grammar and spelling",
      "Use active voice consistently",
      "Maintain proper capitalization"
    ]
  }
}
```

#### Step 3: Modify Document for Compliance

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/modify" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "550e8400-e29b-41d4-a716-446655440000",
    "preserve_formatting": true
  }'
```

**Using Python:**
```python
response = requests.post(
    'http://localhost:8000/api/v1/modify',
    json={
        'document_id': doc_id,
        'preserve_formatting': True
    }
)

result = response.json()
print(f"Changes Made: {result['changes_made']}")
print(f"Summary: {result['summary']}")
print(f"Download URL: {result['download_url']}")
```

**Response:**
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "modified_document_id": "660e8400-e29b-41d4-a716-446655440000",
  "download_url": "/api/v1/download/660e8400_modified.docx",
  "changes_made": 12,
  "summary": "Modified document to comply with English writing guidelines. Fixed grammar errors, improved sentence structure, and applied active voice."
}
```

#### Step 4: Download Modified Document

**Using cURL:**
```bash
curl -O "http://localhost:8000/api/v1/download/660e8400_modified.docx"
```

**Using Python:**
```python
response = requests.get(
    f"http://localhost:8000{result['download_url']}"
)

with open('modified_document.docx', 'wb') as f:
    f.write(response.content)
    
print("Modified document downloaded!")
```

---

## 📋 Scenario 2: Custom Guidelines

You can provide custom guidelines specific to your needs:

```python
import requests

# Define custom guidelines
custom_guidelines = [
    "Use British English spelling",
    "Keep sentences under 20 words",
    "Avoid contractions (e.g., don't, won't)",
    "Use technical terminology appropriately",
    "Include clear section headers"
]

# Check compliance with custom guidelines
response = requests.post(
    'http://localhost:8000/api/v1/check-compliance',
    json={
        'document_id': doc_id,
        'guidelines': custom_guidelines
    }
)

report = response.json()['report']
print(f"Custom Compliance Score: {report['score']}/100")
```

---

## 🔍 Scenario 3: Batch Processing

Process multiple documents:

```python
import requests
from pathlib import Path

def process_document(file_path):
    """Complete workflow for a single document."""
    
    # Upload
    with open(file_path, 'rb') as f:
        upload_response = requests.post(
            'http://localhost:8000/api/v1/upload',
            files={'file': f}
        )
    
    doc_id = upload_response.json()['document_id']
    print(f"\n📄 Processing: {file_path.name}")
    print(f"Document ID: {doc_id}")
    
    # Check compliance
    compliance_response = requests.post(
        'http://localhost:8000/api/v1/check-compliance',
        json={'document_id': doc_id}
    )
    
    report = compliance_response.json()['report']
    print(f"✅ Status: {report['status']}")
    print(f"📊 Score: {report['score']}/100")
    print(f"⚠️  Issues: {report['total_issues']}")
    
    # Modify if needed
    if report['total_issues'] > 0:
        modify_response = requests.post(
            'http://localhost:8000/api/v1/modify',
            json={'document_id': doc_id}
        )
        
        result = modify_response.json()
        print(f"🔧 Changes Made: {result['changes_made']}")
        
        # Download modified
        download_url = result['download_url']
        download_response = requests.get(
            f"http://localhost:8000{download_url}"
        )
        
        output_file = f"modified_{file_path.name}"
        with open(output_file, 'wb') as f:
            f.write(download_response.content)
        
        print(f"💾 Saved: {output_file}")
    
    return report

# Process multiple files
documents = [
    Path('document1.pdf'),
    Path('document2.docx'),
    Path('report.pdf')
]

results = []
for doc in documents:
    if doc.exists():
        report = process_document(doc)
        results.append({
            'file': doc.name,
            'score': report['score'],
            'issues': report['total_issues']
        })

# Summary
print("\n" + "="*50)
print("BATCH PROCESSING SUMMARY")
print("="*50)
for result in results:
    print(f"{result['file']:30} Score: {result['score']:5.1f}  Issues: {result['issues']}")
```

---

## 🌐 Scenario 4: Web Integration

### HTML + JavaScript Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document Compliance Checker</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; }
        .container { padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        button { padding: 10px 20px; margin: 10px 0; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background: #f5f5f5; }
        .violation { margin: 10px 0; padding: 10px; border-left: 3px solid #ff6b6b; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📄 Document Compliance Checker</h1>
        
        <input type="file" id="fileInput" accept=".pdf,.docx">
        <button onclick="uploadDocument()">Upload & Check</button>
        
        <div id="results" class="result" style="display:none;"></div>
    </div>

    <script>
        let documentId = null;
        const API_BASE = 'http://localhost:8000/api/v1';

        async function uploadDocument() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select a file');
                return;
            }

            const formData = new FormData();
            formData.append('file', file);

            try {
                // Upload
                const uploadResponse = await fetch(`${API_BASE}/upload`, {
                    method: 'POST',
                    body: formData
                });
                
                const uploadData = await uploadResponse.json();
                documentId = uploadData.document_id;
                
                // Check compliance
                const complianceResponse = await fetch(`${API_BASE}/check-compliance`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ document_id: documentId })
                });
                
                const complianceData = await complianceResponse.json();
                displayResults(complianceData.report);
                
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        function displayResults(report) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            
            let html = `
                <h2>Compliance Report</h2>
                <p><strong>Status:</strong> ${report.status}</p>
                <p><strong>Score:</strong> ${report.score}/100</p>
                <p><strong>Issues Found:</strong> ${report.total_issues}</p>
                <h3>Violations:</h3>
            `;
            
            report.violations.forEach(v => {
                html += `
                    <div class="violation">
                        <strong>${v.issue}</strong><br>
                        💡 ${v.suggestion}<br>
                        <small>Severity: ${v.severity} | Category: ${v.category}</small>
                    </div>
                `;
            });
            
            if (report.total_issues > 0) {
                html += `<button onclick="modifyDocument()">Fix Document</button>`;
            }
            
            resultsDiv.innerHTML = html;
        }

        async function modifyDocument() {
            try {
                const response = await fetch(`${API_BASE}/modify`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ document_id: documentId })
                });
                
                const data = await response.json();
                window.open(`${API_BASE}${data.download_url}`, '_blank');
                
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }
    </script>
</body>
</html>
```

---

## 📱 API Testing with Postman

### Import Collection

Create a Postman collection with these requests:

1. **Health Check**
   - GET: `http://localhost:8000/api/v1/health`

2. **Upload Document**
   - POST: `http://localhost:8000/api/v1/upload`
   - Body: form-data with key `file`

3. **Check Compliance**
   - POST: `http://localhost:8000/api/v1/check-compliance`
   - Body (JSON):
   ```json
   {
     "document_id": "{{document_id}}"
   }
   ```

4. **Modify Document**
   - POST: `http://localhost:8000/api/v1/modify`
   - Body (JSON):
   ```json
   {
     "document_id": "{{document_id}}"
   }
   ```

---

## 🎓 Advanced Usage

### Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_second=2):
    """Decorator to rate limit API calls."""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls_per_second=2)
def check_compliance(doc_id):
    # Your API call here
    pass
```

### Error Handling

```python
def safe_api_call(func, *args, **kwargs):
    """Wrapper for safe API calls."""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
    
    return None
```

---

## 📊 Monitoring

### Check API Health

```python
def check_api_health():
    """Monitor API health."""
    try:
        response = requests.get('http://localhost:8000/api/v1/health')
        data = response.json()
        
        print(f"Status: {data['status']}")
        print(f"Version: {data['version']}")
        print(f"OpenAI Configured: {data['openai_configured']}")
        
        return data['status'] == 'healthy'
    except Exception as e:
        print(f"API is down: {e}")
        return False

# Run health check
if check_api_health():
    print("✅ API is healthy and ready")
else:
    print("❌ API is not responding")
```

---

## 🎯 Tips for Best Results

1. **File Quality**: Use clear, well-formatted documents
2. **File Size**: Keep files under 10MB for best performance
3. **API Key**: Configure OpenAI API key for full functionality
4. **Guidelines**: Provide specific guidelines for better results
5. **Error Handling**: Always check response status codes
6. **Rate Limiting**: Respect API rate limits in production

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Upload fails
- Check file type (only PDF and DOCX)
- Check file size (max 10MB)
- Verify file is not corrupted

**Issue**: Compliance check returns low scores
- Ensure OpenAI API key is configured
- Check document text quality
- Try with custom guidelines

**Issue**: Server not responding
- Check if server is running
- Verify port 8000 is not in use
- Check logs for errors

---

## 📚 Additional Resources

- **Full API Documentation**: http://localhost:8000/docs
- **Repository**: https://github.com/DSvikash/ai-python-document-compliance
- **README**: Comprehensive setup guide
- **Architecture**: System design documentation

---

**Happy Testing! 🎉**
