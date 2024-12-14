"""Base model implementation for LangChain service."""
import os
import torch
import logging
from typing import Optional, Dict
from huggingface_hub import model_info, login
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from config.model_config import ModelConfig

# Local imports
logger = logging.getLogger(__name__)

class ModelCacheManager:
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self._cache_info = {}
        self.cache_info_path = os.path.join(cache_dir, "cache_info.json")
        self._load_cache_info()

    def has_cached_model(self, model_name: str) -> bool:
        """Check if model exists in cache."""
        return model_name in self._cache_info

    def load_cached_model(self, model_name: str) -> bool:
        """Load model from cache."""
        return bool(self._cache_info.get(model_name))

    def _load_cache_info(self) -> None:
        """Load cache information using proper encoding."""
        if os.path.exists(self.cache_info_path):
            with open(self.cache_info_path, 'r', encoding='utf-8') as f:
                self._cache_info = json.load(f)

class ModelLoadError(Exception):
    """Raised when model loading fails."""
    pass

class QuantizationError(Exception):
    """Raised when quantization fails."""
    pass

class LocalLLMService:
    """Service for managing local LLM operations."""

    def __init__(self, config: ModelConfig):
        """Initialize service with model configuration."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.config = config
        self.model = None
        self.tokenizer = None

        # Create cache directory
        os.makedirs("model_cache", exist_ok=True)

        # Authenticate with HuggingFace
        token = os.getenv("HUGGINGFACE_TOKEN")
        if token:
            login(token)

        logger.info("Initialized service with device: %s", self.device)

    def verify_model(self) -> Dict:
        """Verify model compatibility and requirements."""
        try:
            info = model_info(self.config.name)

            verification = {
                "size_gb": None,
                "tags": getattr(info, 'tags', []),
                "architecture": getattr(info, 'modelId', self.config.name),
                "pipeline": getattr(info, 'pipeline_tag', None)
            }

            logger.info("Model verification complete: %s", verification)
            return verification
        except Exception as e:
            logger.error("Model verification failed: %s", str(e))
            raise ModelLoadError(str(e))

    def load_model(self) -> bool:
        """Load the model."""
        try:
            logger.info("Loading model: %s", self.config.name)

            # Load the tokenizer without resume_download
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.name,
                cache_dir="model_cache",
                trust_remote_code=True
            )

            # Load the model without resume_download
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.name,
                cache_dir="model_cache",
                trust_remote_code=True
            ).to(self.device)

            logger.info("Model loaded successfully")
            return True

        except Exception as e:
            logger.error("Model loading failed: %s", str(e))
            return False

    def generate(self, input_text: str) -> Optional[str]:
        """Generate text using the loaded model."""
        try:
            if not self.model or not self.tokenizer:
                logger.error("Model not loaded")
                return None

            inputs = self.tokenizer(input_text, return_tensors="pt").to(self.device)
            outputs = self.model.generate(**inputs, max_length=100)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            logger.error("Generation failed: %s", str(e))
            return None