import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "enterprise-rag-super-secret-key-do-not-leak"
ALGORITHM = "HS256"

# In-memory users for testing
MOCK_USERS = {
    "admin_user": {"password": "adminpassword", "role": "admin", "department": "Management"},
    "hr_user": {"password": "hrpassword", "role": "hr", "department": "HR"},
    "emp_user": {"password": "emppassword", "role": "employee", "department": "Engineering"},
    "intern_user": {"password": "internpassword", "role": "intern", "department": "Onboarding"}
}

security_agent = HTTPBearer()

def create_access_token(username: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    """Generate JWT Token for a validated user role."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=8)
    
    to_encode = {
        "username": username,
        "role": role,
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(credentials: HTTPAuthorizationCredentials = Security(security_agent)) -> Dict:
    """Decode and validate a JWT token, retrieving user identity and role."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"username": username, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid credentials token")
