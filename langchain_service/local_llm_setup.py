from typing import Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate

class LocalLLMService:
    """Service for managing local LLM operations."""

    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.1"):
        """Initialize LLM service with specified model."""
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.pipeline = None

    def load_model(self) -> None:
        """Load model and tokenizer."""
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",
            torch_dtype=torch.float16
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def create_chain(self, prompt_template: Optional[str] = None) -> HuggingFacePipeline:
        """Create LangChain pipeline with optional prompt template."""
        if not self.model or not self.tokenizer:
            self.load_model()

        if prompt_template:
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["query"]
            )

        self.pipeline = HuggingFacePipeline(
            llm=self.model,
            tokenizer=self.tokenizer
        )

        return self.pipeline