import pytest
from o1_langchain_integration.model_verify import verify_llama_models
import os

def test_huggingface_token():
    """Test HuggingFace token is set"""
    assert os.getenv("HUGGINGFACE_API_TOKEN") is not None

def test_model_verification():
    """Test model verification returns valid data"""
    models = verify_llama_models()
    assert isinstance(models, list)
    if models:
        assert all(isinstance(model, dict) for model in models)