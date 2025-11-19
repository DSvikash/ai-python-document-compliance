"""
AI Agent for document compliance checking using OpenAI GPT.
"""
import json
import re
from typing import List, Dict, Optional
from openai import OpenAI
from app.models.schemas import (
    ComplianceReport, 
    GuidelineViolation, 
    ComplianceStatus
)


class AIComplianceAgent:
    """AI agent for checking document compliance with English guidelines."""
    
    DEFAULT_GUIDELINES = [
        "Use clear and concise language",
        "Avoid passive voice where possible",
        "Use proper grammar and punctuation",
        "Maintain consistent tense throughout",
        "Use active voice for direct communication",
        "Avoid jargon and complex terminology unless necessary",
        "Ensure proper sentence structure",
        "Use appropriate paragraph breaks",
        "Maintain professional tone",
        "Check for spelling errors"
    ]
    
    def __init__(self, api_key: str):
        """
        Initialize AI Compliance Agent.
        
        Args:
            api_key: OpenAI API key
        """
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = "gpt-3.5-turbo"
    
    def check_compliance(self, text: str, guidelines: Optional[List[str]] = None) -> ComplianceReport:
        """
        Check document compliance against guidelines.
        
        Args:
            text: Document text to check
            guidelines: Optional custom guidelines
            
        Returns:
            ComplianceReport with assessment results
        """
        if not self.client:
            return self._fallback_compliance_check(text, guidelines)
        
        guidelines_to_use = guidelines or self.DEFAULT_GUIDELINES
        
        # Create prompt for GPT
        prompt = self._create_compliance_prompt(text, guidelines_to_use)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert English writing compliance checker. Analyze documents for grammar, style, clarity, and adherence to writing guidelines. Provide detailed, structured feedback."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            return self._parse_compliance_result(result)
            
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return self._fallback_compliance_check(text, guidelines)
    
    def modify_document(self, text: str, guidelines: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Modify document to comply with guidelines.
        
        Args:
            text: Original document text
            guidelines: Optional custom guidelines
            
        Returns:
            Dictionary with modified text and summary
        """
        if not self.client:
            return self._fallback_modification(text, guidelines)
        
        guidelines_to_use = guidelines or self.DEFAULT_GUIDELINES
        
        prompt = self._create_modification_prompt(text, guidelines_to_use)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert editor. Rewrite documents to comply with English writing guidelines while preserving the original meaning and intent."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=3000
            )
            
            result = response.choices[0].message.content
            return self._parse_modification_result(result, text)
            
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return self._fallback_modification(text, guidelines)
    
    def _create_compliance_prompt(self, text: str, guidelines: List[str]) -> str:
        """Create prompt for compliance checking."""
        guidelines_str = "\n".join([f"{i+1}. {g}" for i, g in enumerate(guidelines)])
        
        prompt = f"""
Analyze the following document for compliance with these English writing guidelines:

GUIDELINES:
{guidelines_str}

DOCUMENT TEXT:
{text[:3000]}  # Limit text length

Please provide a detailed compliance report in the following JSON format:
{{
    "status": "compliant" | "non_compliant" | "partial",
    "score": <number between 0-100>,
    "total_issues": <number>,
    "violations": [
        {{
            "issue": "<description>",
            "suggestion": "<how to fix>",
            "severity": "low" | "medium" | "high",
            "category": "grammar" | "style" | "clarity" | "structure"
        }}
    ],
    "summary": "<overall assessment>",
    "suggestions": ["<general suggestion 1>", "<general suggestion 2>"]
}}
"""
        return prompt
    
    def _create_modification_prompt(self, text: str, guidelines: List[str]) -> str:
        """Create prompt for document modification."""
        guidelines_str = "\n".join([f"{i+1}. {g}" for i, g in enumerate(guidelines)])
        
        prompt = f"""
Rewrite the following document to comply with these English writing guidelines:

GUIDELINES:
{guidelines_str}

ORIGINAL DOCUMENT:
{text[:3000]}  # Limit text length

Please provide:
1. The modified document text
2. A brief summary of changes made

Format your response as:
MODIFIED TEXT:
[Your rewritten text here]

CHANGES SUMMARY:
[Summary of changes]
"""
        return prompt
    
    def _parse_compliance_result(self, result: str) -> ComplianceReport:
        """Parse GPT response into ComplianceReport."""
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                data = json.loads(result)
            
            violations = [
                GuidelineViolation(
                    line_number=None,
                    issue=v.get('issue', ''),
                    suggestion=v.get('suggestion', ''),
                    severity=v.get('severity', 'medium'),
                    category=v.get('category', 'general')
                )
                for v in data.get('violations', [])
            ]
            
            return ComplianceReport(
                status=ComplianceStatus(data.get('status', 'partial')),
                score=float(data.get('score', 50)),
                total_issues=data.get('total_issues', len(violations)),
                violations=violations,
                summary=data.get('summary', 'Compliance check completed'),
                suggestions=data.get('suggestions', [])
            )
        except Exception as e:
            print(f"Error parsing compliance result: {str(e)}")
            return self._create_default_report()
    
    def _parse_modification_result(self, result: str, original_text: str) -> Dict[str, any]:
        """Parse GPT modification response."""
        try:
            # Extract modified text
            modified_match = re.search(r'MODIFIED TEXT:\s*(.+?)(?=CHANGES SUMMARY:|$)', result, re.DOTALL)
            modified_text = modified_match.group(1).strip() if modified_match else result
            
            # Extract summary
            summary_match = re.search(r'CHANGES SUMMARY:\s*(.+)', result, re.DOTALL)
            summary = summary_match.group(1).strip() if summary_match else "Document modified for compliance"
            
            # Count changes (simple heuristic)
            original_words = set(original_text.lower().split())
            modified_words = set(modified_text.lower().split())
            changes_made = len(original_words.symmetric_difference(modified_words))
            
            return {
                "modified_text": modified_text,
                "summary": summary,
                "changes_made": min(changes_made, 100)  # Cap at 100 for display
            }
        except Exception as e:
            print(f"Error parsing modification result: {str(e)}")
            return {
                "modified_text": original_text,
                "summary": "Unable to modify document",
                "changes_made": 0
            }
    
    def _fallback_compliance_check(self, text: str, guidelines: Optional[List[str]]) -> ComplianceReport:
        """Fallback compliance check without OpenAI API."""
        violations = []
        
        # Basic checks
        if len(text.split()) < 10:
            violations.append(GuidelineViolation(
                line_number=None,
                issue="Document is too short",
                suggestion="Provide more content for proper analysis",
                severity="high",
                category="structure"
            ))
        
        # Check for common issues
        if text.isupper():
            violations.append(GuidelineViolation(
                line_number=None,
                issue="Text is all uppercase",
                suggestion="Use proper capitalization",
                severity="medium",
                category="style"
            ))
        
        # Calculate score
        score = max(0, 100 - (len(violations) * 20))
        status = ComplianceStatus.COMPLIANT if score >= 80 else (
            ComplianceStatus.PARTIAL if score >= 50 else ComplianceStatus.NON_COMPLIANT
        )
        
        return ComplianceReport(
            status=status,
            score=score,
            total_issues=len(violations),
            violations=violations,
            summary="Basic compliance check completed (OpenAI API not configured)",
            suggestions=["Configure OpenAI API key for detailed analysis"]
        )
    
    def _fallback_modification(self, text: str, guidelines: Optional[List[str]]) -> Dict[str, any]:
        """Fallback modification without OpenAI API."""
        return {
            "modified_text": text,
            "summary": "OpenAI API not configured. Original text returned unchanged.",
            "changes_made": 0
        }
    
    def _create_default_report(self) -> ComplianceReport:
        """Create a default compliance report."""
        return ComplianceReport(
            status=ComplianceStatus.PARTIAL,
            score=50.0,
            total_issues=0,
            violations=[],
            summary="Unable to complete full compliance analysis",
            suggestions=["Please try again or check API configuration"]
        )
