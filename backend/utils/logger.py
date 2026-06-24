import os
import json
from datetime import datetime, timezone
from typing import List, Dict

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "audit.log")

class AuditLogger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        os.makedirs(LOG_DIR, exist_ok=True)

    def log_event(
        self,
        username: str,
        role: str,
        query: str,
        action: str,
        risk_score: int,
        model: str,
        retrieved_docs: List[str] = None,
        issues_flagged: List[str] = None
    ) -> Dict:
        """Appends a structured JSON audit entry to audit.log."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "username": username,
            "role": role,
            "query": query,
            "action": action,  # "allow", "block", "monitor"
            "risk_score": risk_score,
            "model": model,
            "retrieved_documents": retrieved_docs or [],
            "issues_flagged": issues_flagged or []
        }
        
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"Error writing to audit log: {str(e)}")
            
        return entry

    def get_logs(self, limit: int = 50) -> List[Dict]:
        """Reads the latest entries from audit.log."""
        if not os.path.exists(LOG_FILE):
            return []
            
        logs = []
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Read latest lines first
                for line in reversed(lines):
                    if line.strip():
                        logs.append(json.loads(line))
                        if len(logs) >= limit:
                            break
        except Exception as e:
            print(f"Error reading audit log: {str(e)}")
            
        return logs
