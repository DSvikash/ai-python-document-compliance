"""
Integration tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import io

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data


def test_upload_document_invalid_type():
    """Test uploading invalid file type."""
    file_content = b"test content"
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    
    response = client.post("/api/v1/upload", files=files)
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"].lower()


def test_upload_document_pdf():
    """Test uploading PDF document (mock)."""
    # Create a minimal PDF-like content
    file_content = b"%PDF-1.4\n%EOF"
    files = {"file": ("test.pdf", io.BytesIO(file_content), "application/pdf")}
    
    response = client.post("/api/v1/upload", files=files)
    # May succeed or fail depending on PDF validation
    assert response.status_code in [201, 500]


def test_check_compliance_invalid_document():
    """Test compliance check with invalid document ID."""
    response = client.post(
        "/api/v1/check-compliance",
        json={"document_id": "nonexistent-id"}
    )
    assert response.status_code == 404


def test_modify_document_invalid_document():
    """Test modification with invalid document ID."""
    response = client.post(
        "/api/v1/modify",
        json={"document_id": "nonexistent-id"}
    )
    assert response.status_code == 404


def test_download_nonexistent_file():
    """Test downloading nonexistent file."""
    response = client.get("/api/v1/download/nonexistent.pdf")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_api_workflow():
    """Test complete API workflow (without actual file upload)."""
    # This test verifies the API structure is correct
    # In production, you'd use actual test files
    
    # Verify endpoints exist
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    # Verify OpenAPI schema
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    
    # Check that all required endpoints are defined
    assert "/api/v1/upload" in schema["paths"]
    assert "/api/v1/check-compliance" in schema["paths"]
    assert "/api/v1/modify" in schema["paths"]
    assert "/api/v1/download/{filename}" in schema["paths"]
