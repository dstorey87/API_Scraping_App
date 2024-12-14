import pytest
from torch import cuda
from langchain_service.base_model import LocalLLMService
from config.model_config import ModelConfig, CacheConfig
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

MODEL_CONFIGS = {
    "vision": ModelConfig(
        name="unsloth/Llama-3.2-11B-Vision-Instruct-bnb-4bit",
        max_memory={0: "6GB"},
        model_type="vision",
        use_4bit=True,
        description="4-bit quantized Llama 3.2 vision model"
    ),
    "text": ModelConfig(
        name="mistralai/Mistral-Large-Instruct-2411",
        max_memory={0: "6GB"},
        model_type="text",
        use_4bit=True,
        description="Latest Mistral Large model"
    )
}

@pytest.fixture
def model_service():
    """Initialize model service with cache"""
    config = ModelConfig(
        name="mistralai/Mistral-Large-Instruct-2411",
        max_memory={0: "6GB"},
        cache_config=CacheConfig(cache_dir="test_model_cache")
    )
    return LocalLLMService(config)

@pytest.fixture(scope="session")
def model_config():
    """Create test model configuration for the vision model."""
    return ModelConfig(
        name="unsloth/Llama-3.2-11B-Vision-Instruct",
        # Commented out or removed model_type and quantization params if not needed
        description="Vision model without text model",
    )

def test_cuda_setup():
    """Test CUDA availability"""
    logger.info("Testing CUDA setup...")
    assert cuda.is_available()
    device_name = cuda.get_device_name()
    logger.info(f"Found GPU: {device_name}")
    assert device_name == "NVIDIA GeForce GTX 1080 Ti"

def test_model_config():
    """Test model configuration"""
    config = MODEL_CONFIGS["vision"]
    assert config.name == "unsloth/Llama-3.2-11B-Vision-Instruct-bnb-4bit"
    assert config.use_4bit == True

@pytest.mark.gpu
def test_model_loading():
    """Test model loading with GPU"""
    service = LocalLLMService(MODEL_CONFIGS["vision"])
    service.load_model()
    assert service.model is not None
    assert service.processor is not None
    if cuda.is_available():
        assert next(service.model.parameters()).device.type == "cuda"

@pytest.mark.gpu
def test_mistral_loading():
    """Test Mistral model loading with GPU"""
    service = LocalLLMService(MODEL_CONFIGS["text"])
    service.load_model()
    assert service.model is not None
    if cuda.is_available():
        assert next(service.model.parameters()).device.type == "cuda"

@pytest.mark.gpu
def test_model_configs():
    """Test model configurations"""
    logger.info("Verifying model configurations...")

    logger.info("Checking vision model config...")
    assert MODEL_CONFIGS["vision"].name == "unsloth/Llama-3.2-11B-Vision-Instruct-bnb-4bit"
    logger.info("Vision model config verified")

    logger.info("Checking text model config...")
    assert MODEL_CONFIGS["text"].name == "mistralai/Mistral-Large-Instruct-2411"
    logger.info("Text model config verified")

def test_model_caching(model_service):
    """Test model caching functionality"""
    logger.info("Testing model caching...")

    # First load should download
    logger.info("First load - should download...")
    assert model_service.load_model()

    # Second load should use cache
    logger.info("Second load - should use cache...")
    start_time = time.time()
    assert model_service.load_model()
    load_time = time.time() - start_time

    logger.info(f"Cached load time: {load_time:.2f}s")

@pytest.mark.skipif(
    not os.getenv("HUGGINGFACE_TOKEN"),
    reason="No HuggingFace token available"
)
def test_model_loading(model_config):
    """Test vision model loading."""
    logger.info("Starting vision model load test...")
    service = LocalLLMService(model_config)

    assert service.load_model(), "Vision model loading failed"