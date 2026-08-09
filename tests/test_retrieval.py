import pytest
from packages.retrieval.loop import retrieve_and_evaluate, RAGState
from packages.retrieval.search import query_local_index

def test_retrieval_high_confidence():
    res = retrieve_and_evaluate("nexus")
    assert res["state"] == RAGState.ANSWER

def test_retrieval_low_confidence():
    res = retrieve_and_evaluate("secret password")
    assert res["state"] == RAGState.LOW_CONFIDENCE
