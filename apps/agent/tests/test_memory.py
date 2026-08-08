import pytest
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory.store import memory_store

def test_sqlite_facts():
    memory_store.set_fact("test_key", "test_value")
    val = memory_store.get_fact("test_key")
    assert val == "test_value"

def test_chroma_indexing():
    memory_store.add_interaction("user", "Hello this is a test.")
    memory_store.add_interaction("assistant", "I acknowledge the test.")
    
    recent = memory_store.get_recent_context(limit=2)
    assert len(recent) >= 2
    
    # Wait for ChromaDB to flush
    time.sleep(1)
    
    # Semantic search
    res = memory_store.semantic_search("acknowledge")
    assert len(res) > 0
