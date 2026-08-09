from sqlalchemy.orm import Session
from apps.api.models import MemoryChunk

def query_local_index(query: str, db: Session = None) -> dict:
    """
    Search the MemoryChunk table.
    """
    if not db:
        return {"confidence": 0.1, "results": []}
        
    chunks = db.query(MemoryChunk).all()
    if not chunks:
        # Empty index -> LOW_CONFIDENCE
        return {"confidence": 0.1, "results": []}
        
    query_lower = query.lower()
    matches = [c.content for c in chunks if query_lower in c.content.lower()]
    
    if matches:
        return {"confidence": 0.9, "results": matches}
        
    return {"confidence": 0.2, "results": []}
