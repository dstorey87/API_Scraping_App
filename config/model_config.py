# ./config/model_config.py

from dataclasses import dataclass
from typing import Dict, Optional
import os

@dataclass
class ModelConfig:
    """Configuration for LLM models."""
    name: str
    max_memory: Dict[int, str]
    model_type: str = "text"
    use_4bit: bool = True
    description: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.95
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    auth_token: Optional[str] = None  # Add this line

MODEL_CONFIGS = {
    "text": ModelConfig(
        name="HuggingFaceH4/zephyr-7b-beta",  # Change to an open-access model
        max_memory={0: "6GB"},
        model_type="text",
        use_4bit=True,
        description="Zephyr 7B model for text generation",
        temperature=0.7,
        max_tokens=2048
    )
}

# Default configurations for different model types
DEFAULT_CONFIGS = {
    "text": {
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 0.95,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    },
    "code": {
        "temperature": 0.2,
        "max_tokens": 4096,
        "top_p": 0.99,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    },
    "chat": {
        "temperature": 0.9,
        "max_tokens": 2048,
        "top_p": 0.95,
        "frequency_penalty": 0.3,
        "presence_penalty": 0.6
    }
}

# Model requirements for CUDA compatibility
CUDA_REQUIREMENTS = {
    "min_vram": "6GB",
    "recommended_vram": "8GB",
    "cuda_version": "11.8",
    "torch_version": "2.1.0",
    "cudnn_version": "8.9.2"
}