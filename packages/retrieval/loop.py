from enum import Enum
from .search import query_local_index

class RAGState(str, Enum):
    ANSWER = "ANSWER"
    REWRITE_QUERY = "REWRITE_QUERY"
    CLARIFY = "CLARIFY"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"

def retrieve_and_evaluate(query: str, attempt: int = 1) -> dict:
    """
    SentinelRAG pattern: Evaluate confidence and decide state.
    """
    res = query_local_index(query)
    conf = res["confidence"]
    
    if conf >= 0.7:
        return {"state": RAGState.ANSWER, "data": res["results"]}
    
    if conf >= 0.4 and attempt == 1:
        # Give LLM a chance to rewrite
        return {"state": RAGState.REWRITE_QUERY, "data": []}
        
    if conf < 0.2:
        return {"state": RAGState.LOW_CONFIDENCE, "data": []}
        
    return {"state": RAGState.CLARIFY, "data": []}
