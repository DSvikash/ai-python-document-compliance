"""
Unit tests for file handler.
"""
import pytest
from pathlib import Path
import tempfile
import shutil
from unittest.mock import Mock

from app.utils.file_handler import FileHandler
from fastapi import UploadFile, HTTPException


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def file_handler(temp_dir):
    """Create FileHandler instance."""
    return FileHandler(
        upload_dir=temp_dir,
        allowed_extensions=["pdf", "docx"],
        max_file_size=1024 * 1024  # 1MB
    )


def test_validate_file_valid_extension(file_handler):
    """Test file validation with valid extension."""
    mock_file = Mock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.file = Mock()
    mock_file.file.tell.return_value = 1024  # 1KB
    mock_file.file.seek.return_value = None
    
    # Should not raise exception
    file_handler.validate_file(mock_file)


def test_validate_file_invalid_extension(file_handler):
    """Test file validation with invalid extension."""
    mock_file = Mock(spec=UploadFile)
    mock_file.filename = "test.txt"
    mock_file.file = Mock()
    mock_file.file.tell.return_value = 1024
    mock_file.file.seek.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        file_handler.validate_file(mock_file)
    
    assert exc_info.value.status_code == 400
    assert "not allowed" in str(exc_info.value.detail).lower()


def test_validate_file_too_large(file_handler):
    """Test file validation with oversized file."""
    mock_file = Mock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.file = Mock()
    mock_file.file.tell.return_value = 2 * 1024 * 1024  # 2MB
    mock_file.file.seek.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        file_handler.validate_file(mock_file)
    
    assert exc_info.value.status_code == 400
    assert "too large" in str(exc_info.value.detail).lower()


def test_get_file_path_exists(file_handler, temp_dir):
    """Test getting file path for existing document."""
    # Create a test file
    test_file = temp_dir / "test-id.pdf"
    test_file.write_text("test content")
    
    result = file_handler.get_file_path("test-id")
    assert result == test_file


def test_get_file_path_not_exists(file_handler):
    """Test getting file path for non-existent document."""
    result = file_handler.get_file_path("nonexistent-id")
    assert result is None


def test_extract_text_from_docx_not_exist(file_handler):
    """Test extracting text from non-existent DOCX file."""
    with pytest.raises(HTTPException) as exc_info:
        file_handler.extract_text_from_docx(Path("nonexistent.docx"))
    
    assert exc_info.value.status_code == 500


def test_extract_text_unsupported_format(file_handler, temp_dir):
    """Test extracting text from unsupported format."""
    test_file = temp_dir / "test.txt"
    test_file.write_text("test content")
    
    with pytest.raises(HTTPException) as exc_info:
        file_handler.extract_text(test_file)
    
    assert exc_info.value.status_code == 400
    assert "unsupported" in str(exc_info.value.detail).lower()
