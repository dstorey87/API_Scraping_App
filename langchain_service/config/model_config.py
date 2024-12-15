# ./config/model_config.py
# Purpose: Configuration settings for all LLM models
# Handles: Model parameters, memory settings, CUDA config
# Used by: All LangChain service components

import os
from dataclasses import dataclass
from typing import Dict, Optional
from . import HUGGINGFACE_TOKEN

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
    auth_token: str = HUGGINGFACE_TOKEN

MODEL_CONFIGS = {
    "text": ModelConfig(
        name="mistralai/Mistral-7B-Instruct-v0.1",
        max_memory={0: "6GB"},
        model_type="text",
        use_4bit=True,
        description="Mistral 7B Instruct model for text generation",
        temperature=0.7,
        max_tokens=2048
    ),
    "summarization": ModelConfig(
        name="mistralai/Mistral-7B-Instruct-v0.1",
        max_memory={0: "6GB"},
        model_type="text",
        use_4bit=True,
        description="Mistral model optimized for summarization",
        temperature=0.3,  # Lower temperature for more focused summaries
        max_tokens=512,
        top_p=0.95,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
}