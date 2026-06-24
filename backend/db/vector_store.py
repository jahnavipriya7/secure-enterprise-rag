import faiss
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from backend.security.metadata_filter import filter_chunks_by_role

# Pre-defined mock enterprise documents with security metadata
MOCK_DOCUMENTS = [
    {
        "id": 1,
        "title": "Admin Root Access Guideline",
        "text": "Admin System Access Guideline: Only users with admin credentials can change root configurations. The root credential password pattern is revised annually by IT Security. Security keys should be stored in the enterprise secure vault. Secrets like Root Access API Keys (e.g. key: ADMIN_SECURE_TOKEN_9988) must never be shared in plaintext. Emergency contact: admin-ops@enterprise.com.",
        "metadata": {
            "department": "IT Security",
            "allowed_roles": ["admin"]
        }
    },
    {
        "id": 2,
        "title": "Executive Salary and Compensation Policy",
        "text": "Executive Salary and Compensation Policy: Base salaries are reviewed annually. The base CTC for senior leadership ranges from ₹25,00,000 to ₹40,00,000. Under HR guidelines, PAN cards and bank account details are confidential. Employee HR ID cards require verifying Aadhaar 2345 6789 0123. Senior executive PAN is ABCDE1234F. Contact HR director at hr-director@enterprise.com or call +91 9900011223.",
        "metadata": {
            "department": "HR",
            "allowed_roles": ["hr", "admin"]
        }
    },
    {
        "id": 3,
        "title": "Employee Leave Policy",
        "text": "Employee Leave Policy: Full-time employees are eligible for 18 days of paid annual leave. Leave requests must be submitted in the employee portal and approved by the reporting manager. Sick leave requires a medical certificate if extending beyond 3 consecutive days. For leave-related queries email leave-admin@enterprise.com or call +91 9876543210. Under standard benefits, a health insurance allowance of $1,200 is also provided.",
        "metadata": {
            "department": "HR",
            "allowed_roles": ["employee", "hr", "admin"]
        }
    },
    {
        "id": 4,
        "title": "Intern Onboarding Guide",
        "text": "Intern Onboarding Guide: Welcome to the company. Onboarding requires submitting graduation transcripts, standard IT security declaration forms, and personal ID copies. You will receive your laptop, corporate email access, and security badge on Day 1. Intern queries can be resolved by emailing intern-help@enterprise.com or calling 555-0199.",
        "metadata": {
            "department": "Onboarding",
            "allowed_roles": ["intern", "employee", "hr", "admin"]
        }
    },
    {
        "id": 5,
        "title": "Remote Work and VPN Policy",
        "text": "Work From Home Policy: Eligible employees can work remotely up to 2 days per week with manager approval. Core working hours are 10 AM to 4 PM. High-speed internet allowance is up to ₹1,500 per month. Details on VPN setup and token generation can be retrieved from the IT intranet wiki. For help, contact network-support@enterprise.com.",
        "metadata": {
            "department": "Engineering",
            "allowed_roles": ["employee", "hr", "admin"]
        }
    }
]

class VectorStoreManager:
    def __init__(self):
        print("Initializing SentenceTransformer model 'all-MiniLM-L6-v2'...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384  # Embedding dimension of all-MiniLM-L6-v2
        
        # Populate embeddings for the mock documents
        self.chunks = []
        for doc in MOCK_DOCUMENTS:
            print(f"Embedding document: {doc['title']}")
            embedding = self.model.encode(doc["text"]).astype("float32")
            self.chunks.append({
                "id": doc["id"],
                "title": doc["title"],
                "text": doc["text"],
                "metadata": doc["metadata"],
                "embedding": embedding
            })
        print("Vector store populated successfully.")

    def get_all_documents(self) -> List[Dict]:
        """Return the source documents without embeddings for display in UI."""
        return [
            {
                "id": c["id"],
                "title": c["title"],
                "text": c["text"],
                "department": c["metadata"]["department"],
                "allowed_roles": c["metadata"]["allowed_roles"]
            }
            for c in self.chunks
        ]

    def search(self, query: str, user_role: str, top_k: int = 2) -> List[Dict]:
        """
        Execute security-first semantic search.
        1. Filter documents based on user role.
        2. Embed query.
        3. Index authorized vectors in FAISS.
        4. Retrieve top_k matches.
        """
        # Step 1: Pre-retrieval Metadata Filtering
        allowed_chunks = filter_chunks_by_role(self.chunks, user_role)
        
        if not allowed_chunks:
            return []
            
        # Step 2: Embed Query
        query_vector = self.model.encode([query]).astype("float32")
        
        # Step 3: Extract vectors and index in FAISS
        allowed_embeddings = np.array([c["embedding"] for c in allowed_chunks]).astype("float32")
        
        # Create a temporary FAISS index for filtered vectors
        index = faiss.IndexFlatL2(self.dimension)
        index.add(allowed_embeddings)
        
        # Step 4: Perform nearest neighbor search
        search_k = min(top_k, len(allowed_chunks))
        distances, indices = index.search(query_vector, search_k)
        
        results = []
        for rank in range(search_k):
            idx = indices[0][rank]
            score = float(distances[0][rank])
            
            # Map index back to the matching chunk from the filtered list
            matched_chunk = allowed_chunks[idx]
            
            # Convert L2 distance to a basic similarity score (higher is more similar)
            # FAISS IndexFlatL2 returns squared L2 distance. We can map it using exp(-distance)
            similarity = round(float(np.exp(-score / 2.0)), 2)
            
            results.append({
                "id": matched_chunk["id"],
                "title": matched_chunk["title"],
                "text": matched_chunk["text"],
                "department": matched_chunk["metadata"]["department"],
                "allowed_roles": matched_chunk["metadata"]["allowed_roles"],
                "similarity_score": similarity
            })
            
        # Sort results by similarity score descending
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results
