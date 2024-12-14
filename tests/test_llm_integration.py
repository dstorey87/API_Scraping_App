import pytest
import sys
import os
from torch import cuda
from config.model_config import ModelConfig, MODEL_CONFIGS
from langchain_service.base_model import LocalLLMService

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_cuda_setup():
    """Verify CUDA configuration"""
    assert cuda.is_available()
    assert cuda.get_device_name() == "NVIDIA GeForce GTX 1080 Ti"

def test_model_service():
    """Test model service initialization"""
    # Use 'text' key instead of 'mistral' to match MODEL_CONFIGS
    service = LocalLLMService(MODEL_CONFIGS["text"])
    assert service.device == "cuda"
    # Update expected model name to match the config
    assert service.config.name == "mistralai/Mistral-Large-Instruct-2411"

def test_model_initialization():
    """Test model loading and CUDA availability"""
    config = ModelConfig(
        name="mistralai/Mistral-7B-Instruct-v0.1",
        max_memory={0: "6GB"}
    )
    service = LocalLLMService(config)
    assert service.device == "cuda"
    assert cuda.is_available()