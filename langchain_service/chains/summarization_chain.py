# ./langchain_service/chains/summarization_chain.py
# Purpose: Text summarization using LLMs
# Handles: Document summarization, length control, output formatting
# Dependencies: base_model.py, LangChain's LLMChain

from typing import Dict, Any, Optional
from langchain.chains.summarize import LLMChain
from langchain.prompts import PromptTemplate
from ..models.base_model import LocalLLMService
import logging

logger = logging.getLogger(__name__)

class SummarizationChain:
    """Chain for text summarization tasks."""

    def __init__(self, llm_service: LocalLLMService):
        self.llm = llm_service
        self.chain = self._create_chain()

    def _create_chain(self) -> LLMChain:
        """Create a summarization chain with default template."""
        template = """Summarize the following text in a concise way:
        {text}

        Summary:"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["text"]
        )
        return LLMChain(llm=self.llm, prompt=prompt)

    def summarize(self, text: str, max_length: int = 200) -> Optional[str]:
        """Generate a summary of the input text."""
        try:
            return self.chain.run(text=text)[:max_length]
        except Exception as e:
            logger.error("Error in summarization: %s", str(e))
            return None