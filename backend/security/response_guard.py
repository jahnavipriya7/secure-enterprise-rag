import re
from typing import Dict, List, Tuple
from backend.security.redactor import PII_Redactor

class ResponseGuard:
    def __init__(self):
        self.redactor = PII_Redactor()
        self.forbidden_keywords = [
            r"ignore previous instructions",
            r"developer mode active",
            r"bypass successful",
            r"system prompt is:",
            r"here is the hidden instruction"
        ]

    def validate_and_sanitize(self, response_text: str) -> Tuple[str, bool, List[Dict]]:
        """
        Validate generated LLM response. Redact any leaked PII and block if prompt instructions leak.
        Returns (sanitized_response, was_flagged, issues_found).
        """
        issues_found = []
        was_flagged = False
        sanitized_text = response_text
        
        # 1. Check for prompt leakage / forbidden keywords
        for kw in self.forbidden_keywords:
            if re.search(kw, response_text, re.IGNORECASE):
                was_flagged = True
                issues_found.append({
                    "type": "FORBIDDEN_KEYWORD",
                    "detail": f"Response contains unauthorized key phrase: '{kw}'"
                })
                sanitized_text = "System violation: An internal security policy blocked the generated output due to unsafe structure."
                return sanitized_text, was_flagged, issues_found

        # 2. Check for PII leakage (Aadhaar, PAN, Emails, Phone, etc.)
        sanitized_text, redactions = self.redactor.redact(response_text)
        if redactions:
            was_flagged = True
            for r in redactions:
                issues_found.append({
                    "type": "PII_LEAK",
                    "detail": f"Redacted leaked {r['entity_type']}"
                })
                
        return sanitized_text, was_flagged, issues_found
