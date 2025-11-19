# API Usage Examples

This document provides practical examples of using the AI Document Compliance Checker API.

## Table of Contents
- [Python Examples](#python-examples)
- [JavaScript Examples](#javascript-examples)
- [cURL Examples](#curl-examples)
- [Postman Collection](#postman-collection)

## Python Examples

### Complete Workflow

```python
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def upload_document(file_path):
    """Upload a document and return document ID."""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{API_BASE}/upload", files=files)
    
    if response.status_code == 201:
        return response.json()['document_id']
    else:
        raise Exception(f"Upload failed: {response.text}")

def check_compliance(document_id, custom_guidelines=None):
    """Check document compliance."""
    payload = {'document_id': document_id}
    if custom_guidelines:
        payload['guidelines'] = custom_guidelines
    
    response = requests.post(
        f"{API_BASE}/check-compliance",
        json=payload
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Compliance check failed: {response.text}")

def modify_document(document_id):
    """Request document modification."""
    payload = {'document_id': document_id}
    response = requests.post(f"{API_BASE}/modify", json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Modification failed: {response.text}")

def download_document(filename, output_path):
    """Download a document."""
    response = requests.get(f"{API_BASE}/download/{filename}")
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded to {output_path}")
    else:
        raise Exception(f"Download failed: {response.text}")

# Example: Complete workflow
if __name__ == "__main__":
    # 1. Upload document
    print("Uploading document...")
    doc_id = upload_document("sample.pdf")
    print(f"Document uploaded: {doc_id}")
    
    # 2. Check compliance
    print("\nChecking compliance...")
    report = check_compliance(doc_id)
    print(f"Compliance Status: {report['report']['status']}")
    print(f"Score: {report['report']['score']}")
    print(f"Total Issues: {report['report']['total_issues']}")
    
    # 3. Display violations
    print("\nViolations:")
    for violation in report['report']['violations']:
        print(f"  - {violation['issue']}")
        print(f"    Suggestion: {violation['suggestion']}")
        print(f"    Severity: {violation['severity']}")
    
    # 4. Modify document if needed
    if report['report']['total_issues'] > 0:
        print("\nModifying document...")
        modified = modify_document(doc_id)
        print(f"Changes made: {modified['changes_made']}")
        print(f"Summary: {modified['summary']}")
        
        # 5. Download modified document
        filename = modified['download_url'].split('/')[-1]
        download_document(filename, f"modified_{filename}")
```

### Custom Guidelines Example

```python
# Define custom guidelines
custom_guidelines = [
    "Use British English spelling",
    "Keep sentences under 20 words",
    "Avoid contractions",
    "Use technical terminology appropriately",
    "Include section headers"
]

# Check with custom guidelines
doc_id = upload_document("technical_doc.pdf")
report = check_compliance(doc_id, custom_guidelines)

print(f"Custom Compliance Check Results:")
print(json.dumps(report, indent=2))
```

## JavaScript Examples

### Using Fetch API

```javascript
const BASE_URL = 'http://localhost:8000';
const API_BASE = `${BASE_URL}/api/v1`;

// Upload document
async function uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data.document_id;
}

// Check compliance
async function checkCompliance(documentId, guidelines = null) {
    const payload = { document_id: documentId };
    if (guidelines) {
        payload.guidelines = guidelines;
    }
    
    const response = await fetch(`${API_BASE}/check-compliance`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
        throw new Error(`Compliance check failed: ${response.statusText}`);
    }
    
    return await response.json();
}

// Modify document
async function modifyDocument(documentId) {
    const response = await fetch(`${API_BASE}/modify`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ document_id: documentId })
    });
    
    if (!response.ok) {
        throw new Error(`Modification failed: ${response.statusText}`);
    }
    
    return await response.json();
}

// Complete workflow example
async function processDocument(file) {
    try {
        // Upload
        console.log('Uploading document...');
        const docId = await uploadDocument(file);
        console.log(`Document ID: ${docId}`);
        
        // Check compliance
        console.log('Checking compliance...');
        const report = await checkCompliance(docId);
        console.log(`Status: ${report.report.status}`);
        console.log(`Score: ${report.report.score}`);
        
        // Display violations
        if (report.report.violations.length > 0) {
            console.log('\nViolations:');
            report.report.violations.forEach(v => {
                console.log(`- ${v.issue}`);
                console.log(`  Suggestion: ${v.suggestion}`);
            });
        }
        
        // Modify if needed
        if (report.report.total_issues > 0) {
            console.log('\nModifying document...');
            const modified = await modifyDocument(docId);
            console.log(`Changes made: ${modified.changes_made}`);
            
            // Download link
            const downloadUrl = `${BASE_URL}${modified.download_url}`;
            console.log(`Download: ${downloadUrl}`);
        }
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Usage with file input
// <input type="file" id="fileInput" accept=".pdf,.docx">
document.getElementById('fileInput').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        processDocument(file);
    }
});
```

## cURL Examples

### Basic Operations

```bash
# 1. Health check
curl http://localhost:8000/api/v1/health

# 2. Upload document
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@document.pdf" \
  -o upload_response.json

# Extract document_id from response
DOC_ID=$(cat upload_response.json | jq -r '.document_id')

# 3. Check compliance
curl -X POST "http://localhost:8000/api/v1/check-compliance" \
  -H "Content-Type: application/json" \
  -d "{\"document_id\": \"$DOC_ID\"}" \
  | jq .

# 4. Check with custom guidelines
curl -X POST "http://localhost:8000/api/v1/check-compliance" \
  -H "Content-Type: application/json" \
  -d "{
    \"document_id\": \"$DOC_ID\",
    \"guidelines\": [
      \"Use active voice\",
      \"Keep sentences concise\"
    ]
  }" | jq .

# 5. Modify document
curl -X POST "http://localhost:8000/api/v1/modify" \
  -H "Content-Type: application/json" \
  -d "{\"document_id\": \"$DOC_ID\"}" \
  -o modify_response.json

# Extract download filename
FILENAME=$(cat modify_response.json | jq -r '.download_url' | cut -d'/' -f4)

# 6. Download modified document
curl -O "http://localhost:8000/api/v1/download/$FILENAME"
```

### Batch Processing Script

```bash
#!/bin/bash

# Process multiple documents
for file in documents/*.pdf; do
    echo "Processing $file..."
    
    # Upload
    response=$(curl -s -X POST "http://localhost:8000/api/v1/upload" \
      -F "file=@$file")
    
    doc_id=$(echo $response | jq -r '.document_id')
    echo "Document ID: $doc_id"
    
    # Check compliance
    report=$(curl -s -X POST "http://localhost:8000/api/v1/check-compliance" \
      -H "Content-Type: application/json" \
      -d "{\"document_id\": \"$doc_id\"}")
    
    score=$(echo $report | jq -r '.report.score')
    echo "Compliance Score: $score"
    
    # Save report
    echo $report | jq . > "reports/${file##*/}_report.json"
    
    echo "---"
done

echo "Batch processing complete!"
```

## Postman Collection

### Environment Variables
```json
{
  "name": "AI Document Compliance",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "enabled": true
    },
    {
      "key": "document_id",
      "value": "",
      "enabled": true
    }
  ]
}
```

### Collection Structure

1. **Health Check**
   - Method: GET
   - URL: `{{base_url}}/api/v1/health`

2. **Upload Document**
   - Method: POST
   - URL: `{{base_url}}/api/v1/upload`
   - Body: form-data with file
   - Tests: 
     ```javascript
     pm.environment.set("document_id", pm.response.json().document_id);
     ```

3. **Check Compliance**
   - Method: POST
   - URL: `{{base_url}}/api/v1/check-compliance`
   - Body: 
     ```json
     {
       "document_id": "{{document_id}}"
     }
     ```

4. **Modify Document**
   - Method: POST
   - URL: `{{base_url}}/api/v1/modify`
   - Body:
     ```json
     {
       "document_id": "{{document_id}}"
     }
     ```

5. **Download Document**
   - Method: GET
   - URL: `{{base_url}}/api/v1/download/{filename}`

## Error Handling

### Python Example
```python
def safe_api_call(func, *args, **kwargs):
    """Wrapper for safe API calls with error handling."""
    try:
        return func(*args, **kwargs)
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Is the server running?")
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

# Usage
result = safe_api_call(check_compliance, doc_id)
if result:
    print(f"Score: {result['report']['score']}")
```

## Rate Limiting and Best Practices

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
def check_compliance_limited(document_id):
    return check_compliance(document_id)

# Process multiple documents with rate limiting
for doc_path in document_paths:
    doc_id = upload_document(doc_path)
    result = check_compliance_limited(doc_id)
    print(f"Processed {doc_path}: Score {result['report']['score']}")
```

---

For more examples and updates, check the project repository and API documentation at `/docs`.
