from dataclasses import dataclass, field
from typing import Dict, Optional
import os

@dataclass
class CacheConfig:
    cache_dir: str = "model_cache"
    max_cache_size: int = 100  # GB
    keep_in_memory: bool = False

class ModelConfig:
    def __init__(
        self,
        name: str,
        model_type: str = "",
        quantization: bool = False,
        description: str = "",
        max_memory: Dict[int, str] = None,
    ):
        self.name = name
        self.model_type = model_type
        self.quantization = quantization
        self.description = description
        self.max_memory = max_memory or {0: "10GB"}

# Existing predefined configurations
vision_model_config = ModelConfig(
    name="unsloth/Llama-3.2-11B-Vision-Instruct",
    model_type="vision",
    quantization=True,
    description="Vision model with dynamic quantization",
)

text_model_config = ModelConfig(
    name="gpt2",
    model_type="text",
    quantization=True,
    description="Text model with dynamic quantization",
)

MODEL_CONFIGS = {
    # Vision Processing
    "vision": ModelConfig(
        name="unsloth/Llama-3.2-11B-Vision-Instruct-bnb-4bit",
        max_memory={0: "6GB"},
        model_type="vision",
        description="4-bit quantized Llama 3.2 vision model"
    ),
    # Text Processing
    "text": ModelConfig(
        name="mistralai/Mistral-Large-Instruct-2411",
        max_memory={0: "6GB"},
        model_type="text",
        description="Latest Mistral Large model with multilingual support"
    )
}