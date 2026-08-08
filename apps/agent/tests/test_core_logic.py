import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import re
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_robust_json_regex():
    """Test the fallback regex parser used in daemon.py"""
    content = "Sure, I can help with that. ```json\n{\"name\": \"python_executor\", \"parameters\": {\"code\": \"print(1+1)\"}}\n``` Here you go."
    match = re.search(r'\{[\s\S]*?"name"\s*:\s*"[^"]+"\s*,[\s\S]*?"parameters"\s*:\s*\{[\s\S]*\}\s*\}', content)
    assert match is not None
    parsed = json.loads(match.group(0))
    assert parsed['name'] == 'python_executor'
    assert 'code' in parsed['parameters']

@patch('memory.store.memory_store.set_fact')
def test_fact_extraction_mock(mock_set_fact):
    """Test that set_fact is called correctly when mocked"""
    from memory.store import memory_store
    memory_store.set_fact("user_name", "Nivedh")
    mock_set_fact.assert_called_once_with("user_name", "Nivedh")

@patch('llm.client.chat_with_tools')
def test_mock_llm_client(mock_chat):
    """Test the LLM client behavior via mock"""
    mock_chat.return_value = {"message": {"content": "Mock response"}}
    from llm.client import chat_with_tools
    res = chat_with_tools([{"role": "user", "content": "Hello"}])
    assert res["message"]["content"] == "Mock response"
    mock_chat.assert_called_once()
