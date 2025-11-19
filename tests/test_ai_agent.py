"""
Unit tests for AI agent.
"""
import pytest
from app.services.ai_agent import AIComplianceAgent
from app.models.schemas import ComplianceStatus


@pytest.fixture
def ai_agent():
    """Create AIComplianceAgent instance without API key."""
    return AIComplianceAgent(api_key="")


def test_fallback_compliance_check_short_text(ai_agent):
    """Test fallback compliance check with short text."""
    text = "Short text"
    result = ai_agent.check_compliance(text)
    
    assert isinstance(result.status, ComplianceStatus)
    assert result.score >= 0 and result.score <= 100
    assert result.total_issues >= 0
    assert isinstance(result.violations, list)
    assert isinstance(result.summary, str)


def test_fallback_compliance_check_normal_text(ai_agent):
    """Test fallback compliance check with normal text."""
    text = "This is a normal text with sufficient length for analysis. " * 3
    result = ai_agent.check_compliance(text)
    
    assert isinstance(result.status, ComplianceStatus)
    assert result.score >= 0 and result.score <= 100
    assert isinstance(result.summary, str)


def test_fallback_compliance_check_uppercase_text(ai_agent):
    """Test fallback compliance check with uppercase text."""
    text = "THIS IS ALL UPPERCASE TEXT WHICH SHOULD BE FLAGGED AS AN ISSUE."
    result = ai_agent.check_compliance(text)
    
    assert result.total_issues > 0
    assert any("uppercase" in v.issue.lower() for v in result.violations)


def test_fallback_modification(ai_agent):
    """Test fallback document modification."""
    text = "Original text for modification"
    result = ai_agent.modify_document(text)
    
    assert "modified_text" in result
    assert "summary" in result
    assert "changes_made" in result
    assert isinstance(result["changes_made"], int)


def test_custom_guidelines(ai_agent):
    """Test compliance check with custom guidelines."""
    text = "Test document text for analysis."
    guidelines = [
        "Use active voice",
        "Keep sentences short",
        "Avoid jargon"
    ]
    
    result = ai_agent.check_compliance(text, guidelines)
    
    assert isinstance(result, object)
    assert result.score >= 0


def test_default_guidelines_exist(ai_agent):
    """Test that default guidelines are defined."""
    assert hasattr(AIComplianceAgent, 'DEFAULT_GUIDELINES')
    assert isinstance(AIComplianceAgent.DEFAULT_GUIDELINES, list)
    assert len(AIComplianceAgent.DEFAULT_GUIDELINES) > 0


def test_create_default_report(ai_agent):
    """Test creating default report."""
    report = ai_agent._create_default_report()
    
    assert report.status == ComplianceStatus.PARTIAL
    assert report.score == 50.0
    assert report.total_issues == 0
    assert isinstance(report.summary, str)
