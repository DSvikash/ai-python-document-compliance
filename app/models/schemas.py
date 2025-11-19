"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum


class ComplianceStatus(str, Enum):
    """Compliance status enum."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL = "partial"


class GuidelineViolation(BaseModel):
    """Model for a guideline violation."""
    line_number: Optional[int] = Field(None, description="Line number where violation occurs")
    issue: str = Field(..., description="Description of the issue")
    suggestion: str = Field(..., description="Suggested correction")
    severity: str = Field(..., description="Severity level: low, medium, high")
    category: str = Field(..., description="Category of violation (grammar, style, clarity, etc.)")


class ComplianceReport(BaseModel):
    """Model for compliance assessment report."""
    status: ComplianceStatus = Field(..., description="Overall compliance status")
    score: float = Field(..., ge=0, le=100, description="Compliance score (0-100)")
    total_issues: int = Field(..., description="Total number of issues found")
    violations: List[GuidelineViolation] = Field(default_factory=list, description="List of violations")
    summary: str = Field(..., description="Summary of the assessment")
    suggestions: List[str] = Field(default_factory=list, description="General suggestions")


class DocumentUploadResponse(BaseModel):
    """Response model for document upload."""
    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    file_type: str = Field(..., description="File type (pdf or docx)")
    message: str = Field(..., description="Success message")


class ComplianceCheckRequest(BaseModel):
    """Request model for compliance check."""
    document_id: str = Field(..., description="Document identifier")
    guidelines: Optional[List[str]] = Field(
        None, 
        description="Custom guidelines to check against"
    )


class ComplianceCheckResponse(BaseModel):
    """Response model for compliance check."""
    document_id: str = Field(..., description="Document identifier")
    report: ComplianceReport = Field(..., description="Compliance report")


class ModificationRequest(BaseModel):
    """Request model for document modification."""
    document_id: str = Field(..., description="Document identifier")
    guidelines: Optional[List[str]] = Field(
        None,
        description="Guidelines to comply with"
    )
    preserve_formatting: bool = Field(
        True,
        description="Whether to preserve original formatting"
    )


class ModificationResponse(BaseModel):
    """Response model for document modification."""
    document_id: str = Field(..., description="Original document identifier")
    modified_document_id: str = Field(..., description="Modified document identifier")
    download_url: str = Field(..., description="URL to download modified document")
    changes_made: int = Field(..., description="Number of changes made")
    summary: str = Field(..., description="Summary of modifications")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")
