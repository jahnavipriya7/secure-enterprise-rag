import json
import urllib.request
import urllib.error
from typing import Dict, List

class LocalLLMManager:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url

    def is_ollama_available(self) -> bool:
        """Check if local Ollama service is running."""
        try:
            req = urllib.request.Request(f"{self.ollama_url}/api/tags")
            with urllib.request.urlopen(req, timeout=1.0) as response:
                return response.status == 200
        except Exception:
            return False

    def query_ollama(self, model: str, prompt: str) -> str:
        """Query local Ollama instance."""
        url = f"{self.ollama_url}/api/generate"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        json_data = json.dumps(data).encode("utf-8")
        
        req = urllib.request.Request(
            url, 
            data=json_data, 
            headers={"Content-Type": "application/json"}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=15.0) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                return res_json.get("response", "")
        except Exception as e:
            return f"Ollama error: {str(e)}"

    def generate_response(self, system_prompt: str, context: str, query: str) -> Dict:
        """
        Generate response using local Ollama if available, otherwise fall back
        to a smart local context-grounded response generator.
        """
        full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion:\n{query}"
        
        ollama_active = self.is_ollama_available()
        model_used = "Phi-3-Mini (via Ollama)" if ollama_active else "Smart Grounded Local Fallback Engine"
        
        if ollama_active:
            # Try using Phi-3 or TinyLlama (checks for loaded tags, default to phi3)
            response_text = self.query_ollama("phi3", full_prompt)
        else:
            # Smart context-grounded response generation based on context availability
            response_text = self.fallback_generator(context, query)
            
        return {
            "response": response_text,
            "model": model_used,
            "ollama_active": ollama_active
        }

    def fallback_generator(self, context: str, query: str) -> str:
        """
        Fallback generator that parses the secure prompt's context and query
        to generate a fully grounded answer.
        """
        q = query.lower()
        
        # Check if context is empty
        if not context or "No authorized context" in context or len(context.strip()) < 5:
            return "I am sorry, but I do not have access to any authorized documents containing that information. Please check your role permissions."
            
        # Segment context into lines/sentences
        sentences = []
        for line in context.split("\n"):
            line = line.strip()
            if line.startswith("-") or line.startswith("[") or not line:
                continue
            sentences.extend([s.strip() for s in line.split(". ") if s.strip()])
            
        # Query matching categories
        if "leave" in q or "vacation" in q or "holiday" in q:
            ans_parts = []
            for s in sentences:
                if any(x in s.lower() for x in ["leave", "sick", "annual", "vacation", "insurance", "benefits"]):
                    ans_parts.append(s)
            if ans_parts:
                return "Based on the authorized Employee Leave Policy: " + ". ".join(ans_parts) + "."
            
        if "onboard" in q or "intern" in q or "transcript" in q:
            ans_parts = []
            for s in sentences:
                if any(x in s.lower() for x in ["onboard", "intern", "badge", "transcript", "laptop", "badge"]):
                    ans_parts.append(s)
            if ans_parts:
                return "According to the Intern Onboarding Guide: " + ". ".join(ans_parts) + "."

        if "vpn" in q or "work from home" in q or "wfh" in q or "remote" in q or "internet" in q:
            ans_parts = []
            for s in sentences:
                if any(x in s.lower() for x in ["vpn", "work from home", "remote", "wfh", "allowance", "hours"]):
                    ans_parts.append(s)
            if ans_parts:
                return "Based on the Remote Work and VPN Policy: " + ". ".join(ans_parts) + "."

        if "salary" in q or "compensation" in q or "pan" in q or "aadhaar" in q or "pay" in q:
            ans_parts = []
            for s in sentences:
                if any(x in s.lower() for x in ["salary", "compensation", "base", "ctc", "pan", "aadhaar", "bank"]):
                    ans_parts.append(s)
            if ans_parts:
                return "Based on the secure Executive Salary and Compensation Policy: " + ". ".join(ans_parts) + "."

        if "admin" in q or "credential" in q or "root" in q or "vault" in q or "keys" in q:
            ans_parts = []
            for s in sentences:
                if any(x in s.lower() for x in ["admin", "root", "credential", "vault", "keys", "emergency"]):
                    ans_parts.append(s)
            if ans_parts:
                return "According to the Admin Root Access Guidelines: " + ". ".join(ans_parts) + "."

        # Generic context rephraser if not matched to specific topics but context is available
        return f"Based on the provided documents: {context.strip()}"
