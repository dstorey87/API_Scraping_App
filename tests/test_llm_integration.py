import pytest
import sys
import os
from torch import cuda
from config.model_config import MODEL_CONFIGS
from langchain_service.models.base_model import LocalLLMService

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_cuda_available():
    """Test CUDA availability."""
    assert cuda.is_available()
    assert cuda.device_count() > 0

def test_model_initialization():
    """Test model loading and configuration."""
    service = LocalLLMService(MODEL_CONFIGS["text"].name)
    assert service.device == "cuda"
    assert service.model_name == "mistralai/Mistral-7B-Instruct-v0.1"

def test_chain_creation():
    """Test LangChain pipeline creation."""
    service = LocalLLMService(MODEL_CONFIGS["text"].name)
    chain = service.create_chain()
    assert chain is not None