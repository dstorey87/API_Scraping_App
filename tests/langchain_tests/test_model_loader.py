# ./tests/langchain_tests/test_model_loader.py
# Purpose: Test suite for model loading functionality
# Tests: CUDA detection, model initialization, memory management
# Dependencies: pytest, torch, config/model_config.py, langchain_service/models/base_model.py

import pytest
import torch
from torch import cuda
import logging
from config.model_config import MODEL_CONFIGS
from langchain_service.models.base_model import LocalLLMService, ModelLoadError  # Updated import path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def model_service():
    """Create LLM service instance for testing."""
    return LocalLLMService(MODEL_CONFIGS["text"])

def test_cuda_availability():
    """Verify CUDA is available and properly configured."""
    assert cuda.is_available()
    device_name = cuda.get_device_name()
    logger.info("Found GPU: %s", device_name)
    assert device_name == "NVIDIA GeForce GTX 1080 Ti"

def test_model_initialization(model_service):
    """Test model service initialization."""
    assert model_service.device == "cuda"
    assert model_service.config == MODEL_CONFIGS["text"]
    assert model_service.model is None  # Model not loaded initially

def test_model_loading(model_service):
    """Test model loading process."""
    success = model_service.load_model()
    assert success
    assert model_service.model is not None
    assert model_service.tokenizer is not None

@pytest.mark.skipif(
    not cuda.is_available(),
    reason="Test requires CUDA GPU"
)
def test_model_cuda_transfer(model_service):
    """Test model transfer to CUDA."""
    success = model_service.load_model()
    assert success
    assert next(model_service.model.parameters()).device.type == "cuda"

def test_model_load_error():
    """Test error handling for invalid model loading."""
    invalid_config = MODEL_CONFIGS["text"]
    invalid_config.name = "invalid/model"
    service = LocalLLMService(invalid_config)

    with pytest.raises(ModelLoadError):
        service.load_model()

def test_model_gpu_memory():
    """Test GPU memory management."""
    service = LocalLLMService(MODEL_CONFIGS["text"])
    if torch.cuda.is_available():
        assert hasattr(service, 'max_memory')
        memory_limit = int(service.max_memory[0].rstrip('MB'))
        total_memory = torch.cuda.get_device_properties(0).total_memory / 1024**2
        assert memory_limit <= int(total_memory * 0.6)  # Verify 60% limit