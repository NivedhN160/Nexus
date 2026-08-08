import pytest
import os
from src.config import Config
from src.agent import PatchedGoogleGenAI

def test_config_validation_with_key(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "fake_key")
    Config.validate() # Should not raise

def test_config_validation_without_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(Config, "GEMINI_API_KEY", "")
    with pytest.raises(ValueError):
        Config.validate()

def test_patched_genai():
    llm = PatchedGoogleGenAI(model="gemini-2.0-flash", api_key="fake")
    assert llm.provider == "google"
    assert llm.model_name == "gemini-2.0-flash"
