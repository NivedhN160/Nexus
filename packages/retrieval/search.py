import random

def query_local_index(query: str) -> dict:
    """
    Mock of a local memory/vector index search (e.g. SQLite/Chroma).
    In a real scenario, this queries the local DB.
    """
    query_lower = query.lower()
    
    # Deterministic mock responses for testing
    if "nexus" in query_lower:
        return {"confidence": 0.9, "results": ["Nexus is an integrated personal AI operations platform."]}
    elif "password" in query_lower or "secret" in query_lower:
        return {"confidence": 0.2, "results": []}
    
    # Random fallback for simulation
    conf = random.uniform(0.1, 0.9)
    if conf > 0.7:
        return {"confidence": conf, "results": [f"Found some generic data related to {query}."]}
    return {"confidence": conf, "results": []}
