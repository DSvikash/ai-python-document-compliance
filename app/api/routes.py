"""
API routes for document compliance checking.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Optional
import os

from app.models.schemas import (
    DocumentUploadResponse,
    ComplianceCheckRequest,
    ComplianceCheckResponse,
    ModificationRequest,
    ModificationResponse,
    ErrorResponse
)
from app.utils.file_handler import FileHandler
from app.services.ai_agent import AIComplianceAgent
from app.config import settings

# Create router
router = APIRouter(prefix="/api/v1", tags=["Document Compliance"])

# Initialize handlers
file_handler = FileHandler(
    upload_dir=settings.UPLOAD_DIR,
    allowed_extensions=settings.ALLOWED_EXTENSIONS,
    max_file_size=settings.MAX_FILE_SIZE
)

ai_agent = AIComplianceAgent(api_key=settings.OPENAI_API_KEY)


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=201,
    summary="Upload Document",
    description="Upload a PDF or Word document for compliance checking"
)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document for compliance analysis.
    
    Args:
        file: PDF or DOCX file
        
    Returns:
        Document upload confirmation with document ID
    """
    # Validate file
    file_handler.validate_file(file)
    
    # Save file
    document_id, file_path = await file_handler.save_file(file)
    
    return DocumentUploadResponse(
        document_id=document_id,
        filename=file.filename,
        file_size=os.path.getsize(file_path),
        file_type=file_path.suffix[1:],
        message="Document uploaded successfully"
    )


@router.post(
    "/check-compliance",
    response_model=ComplianceCheckResponse,
    summary="Check Compliance",
    description="Check if uploaded document complies with English guidelines"
)
async def check_compliance(request: ComplianceCheckRequest):
    """
    Check document compliance against English writing guidelines.
    
    Args:
        request: Compliance check request with document ID
        
    Returns:
        Detailed compliance report
    """
    # Get file path
    file_path = file_handler.get_file_path(request.document_id)
    if not file_path:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {request.document_id}"
        )
    
    # Extract text
    text = file_handler.extract_text(file_path)
    
    # Check compliance
    report = ai_agent.check_compliance(text, request.guidelines)
    
    return ComplianceCheckResponse(
        document_id=request.document_id,
        report=report
    )


@router.post(
    "/modify",
    response_model=ModificationResponse,
    summary="Modify Document",
    description="Modify document to comply with English guidelines"
)
async def modify_document(request: ModificationRequest):
    """
    Modify document to comply with guidelines.
    
    Args:
        request: Modification request with document ID
        
    Returns:
        Modified document details and download URL
    """
    # Get file path
    file_path = file_handler.get_file_path(request.document_id)
    if not file_path:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {request.document_id}"
        )
    
    # Extract text
    original_text = file_handler.extract_text(file_path)
    
    # Modify document
    modification_result = ai_agent.modify_document(original_text, request.guidelines)
    
    # Create modified document
    modified_path = file_handler.create_modified_document(
        file_path,
        modification_result["modified_text"]
    )
    
    modified_doc_id = modified_path.stem.replace("_modified", "")
    
    return ModificationResponse(
        document_id=request.document_id,
        modified_document_id=modified_doc_id,
        download_url=f"/api/v1/download/{modified_path.name}",
        changes_made=modification_result["changes_made"],
        summary=modification_result["summary"]
    )


@router.get(
    "/download/{filename}",
    summary="Download Document",
    description="Download original or modified document"
)
async def download_document(filename: str):
    """
    Download a document.
    
    Args:
        filename: Name of file to download
        
    Returns:
        File for download
    """
    file_path = settings.UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {filename}"
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


@router.get(
    "/health",
    summary="Health Check",
    description="Check API health status"
)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        API health status
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "openai_configured": bool(settings.OPENAI_API_KEY)
    }
