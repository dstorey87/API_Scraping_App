import pytest
from torch import cuda
from langchain_service.base_model import LocalLLMService

def test_cuda_availability():
    assert cuda.is_available(), "CUDA not available"

def test_local_llm_service():
    service = LocalLLMService(model_path="test_model")
    assert service.device in ["cuda", "cpu"]

def test_model_worker():
    if not cuda.is_available():
        pytest.skip("CUDA not available")