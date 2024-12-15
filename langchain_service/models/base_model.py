# ./langchain_service/models/base_model.py
# Purpose: Core model class for loading and managing LLMs
# Handles: Model initialization, CUDA setup, model verification
# Used by: Conversation and summarization chains

"""Base model implementation for LangChain service."""
import os
import signal
import psutil
import torch
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from functools import partial
from threading import Event, Lock
from tqdm import tqdm
from typing import Optional, Dict, ClassVar
from huggingface_hub import model_info, login, HfFolder
from transformers import AutoModelForCausalLM, AutoTokenizer
from config.model_config import ModelConfig

# Local imports
logger = logging.getLogger(__name__)

class ModelLoadError(Exception):
    """Raised when model loading fails."""
    pass

class QuantizationError(Exception):
    """Raised when quantization fails."""
    pass

class ModelLoadTimeout(Exception):
    """Raised when model loading exceeds timeout."""
    pass

class LocalLLMService:
    """Service for managing local LLM operations."""

    def __init__(self, config: ModelConfig):
        """Initialize service with model configuration."""
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None

        # Set GPU memory limit (60% of available memory)
        if torch.cuda.is_available():
            total_memory = torch.cuda.get_device_properties(0).total_memory
            self.max_memory = {0: f"{int(total_memory * 0.6 / 1024**2)}MB"}
            logger.info(f"GPU memory limit set to {self.max_memory[0]}")

        # Set cache directory
        self.cache_dir = os.path.join(os.getcwd(), "model_cache")
        os.makedirs(self.cache_dir, exist_ok=True)

        # Login to HuggingFace
        if os.getenv("HUGGINGFACE_TOKEN"):
            login(token=os.getenv("HUGGINGFACE_TOKEN"))
            logger.info("Authenticated with HuggingFace")
        else:
            logger.warning("No HuggingFace token found in environment")

    def load_model(self, timeout: int = 300) -> bool:
        """Load the model with device mapping."""
        try:
            logger.info(f"Loading model {self.config.name}")

            # Show progress during downloads
            with tqdm(desc="Loading model") as pbar:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.config.name,
                    cache_dir=self.cache_dir,
                    trust_remote_code=True,
                    token=os.getenv("HUGGINGFACE_TOKEN")
                )
                pbar.update(50)

                # Let Accelerate handle device mapping automatically
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.config.name,
                    cache_dir=self.cache_dir,
                    trust_remote_code=True,
                    token=os.getenv("HUGGINGFACE_TOKEN"),
                    device_map="auto",  # This handles CUDA allocation
                    max_memory=self.max_memory,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                )
                pbar.update(50)

            # No need to manually move model to device - device_map="auto" handles this
            logger.info("Model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Model loading failed: {str(e)}")
            raise ModelLoadError(f"Failed to load model: {str(e)}")

    def generate(self, input_text: str) -> Optional[str]:
        """Generate text using the loaded model."""
        try:
            if not self.model or not self.tokenizer:
                logger.error("Model not loaded")
                return None

            inputs = self.tokenizer(input_text, return_tensors="pt")
            # Move inputs to the same device as model
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

            outputs = self.model.generate(**inputs, max_length=100)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            logger.error("Generation failed: %s", str(e))
            return None