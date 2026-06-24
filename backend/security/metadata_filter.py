from typing import List, Dict

# Role access hierarchies
# admin: can access all documents
# hr: can access HR docs, employee docs, intern docs (but not admin policy docs)
# employee: can access employee docs and intern docs (but not HR salaries or admin docs)
# intern: can access intern docs only (onboarding guides)

def filter_chunks_by_role(chunks: List[Dict], user_role: str) -> List[Dict]:
    """
    Filter chunks based on the user's role before vector retrieval.
    This guarantees that unauthorized document chunks are completely excluded from the search space.
    """
    filtered_chunks = []
    
    for chunk in chunks:
        allowed_roles = chunk.get("metadata", {}).get("allowed_roles", [])
        
        # Admin gets absolute access
        if user_role == "admin":
            filtered_chunks.append(chunk)
        # Check if user role is explicitly in allowed_roles
        elif user_role in allowed_roles:
            filtered_chunks.append(chunk)
            
    return filtered_chunks
