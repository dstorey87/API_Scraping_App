import os
import pytest
import torch
import logging
from config.model_config import ModelConfig
from langchain_service.base_model import LocalLLMService, ModelLoadError, QuantizationError

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/test.log', mode='w')
    ]
)
logger = logging.getLogger(__name__)

# Define GPU mark
gpu_mark = pytest.mark.skipif(
    not torch.cuda.is_available(),
    reason="Test requires CUDA GPU"
)

@pytest.fixture(scope="session")
def model_config():
    """Create test model configuration."""
    return ModelConfig(
        name="gpt2",  # Replace with your model name
        model_type="text",
        quantization=True,
        description="Model with dynamic quantization"
    )

@pytest.mark.skipif(
    not os.getenv("HUGGINGFACE_TOKEN"),
    reason="No HuggingFace token available"
)
def test_model_loading(model_config):
    """Test model loading with quantization."""
    logger.info("Starting model load test...")
    service = LocalLLMService(model_config)

    assert service.load_model(), "Model loading failed"
