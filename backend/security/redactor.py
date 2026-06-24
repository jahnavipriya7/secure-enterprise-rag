import re
from typing import Dict, List, Tuple

class PII_Redactor:
    def __init__(self):
        # Patterns for PII and sensitive enterprise data
        self.patterns: Dict[str, str] = {
            "EMAIL": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
            "PHONE": r"\b(?:\+91[\s-]?)?[6-9]\d{9}\b|\b\d{3}[-\s]\d{3}[-\s]\d{4}\b",
            "AADHAAR": r"\b\d{4}\s\d{4}\s\d{4}\b",
            "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
            "SALARY_RUP": r"₹\s?\d{1,3}(?:,\d{2,3})*(?:,\d{3})*(?:\.\d{2})?",
            "SALARY_USD": r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
        }

    def redact(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Redacts PII and sensitive patterns from the text.
        Returns the redacted text and a list of redactions made.
        """
        redacted_text = text
        redactions = []
        
        for entity_type, pattern in self.patterns.items():
            matches = list(re.finditer(pattern, redacted_text))
            # Process in reverse order to keep character offsets valid
            for match in reversed(matches):
                val = match.group()
                start, end = match.span()
                placeholder = f"[{entity_type}_REDACTED]"
                
                # Check if we already redacted this exact spot (e.g. nested regexes)
                if placeholder in val:
                    continue
                    
                redacted_text = redacted_text[:start] + placeholder + redacted_text[end:]
                redactions.append({
                    "entity_type": entity_type,
                    "original": val,
                    "redacted": placeholder
                })
                
        return redacted_text, redactions
