from typing import Dict, Any, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from ..models.base_model import LocalLLMService

class BaseChain:
    """Base chain for all LangChain operations."""

    def __init__(self, llm_service: LocalLLMService):
        self.llm = llm_service
        self.chain = None

    def create_chain(self, template: str, input_variables: list) -> LLMChain:
        """Create a LangChain chain with specified template."""
        prompt = PromptTemplate(
            template=template,
            input_variables=input_variables
        )
        self.chain = LLMChain(llm=self.llm, prompt=prompt)
        return self.chain

    def run(self, inputs: Dict[str, Any]) -> Optional[str]:
        """Run the chain with provided inputs."""
        if not self.chain:
            raise ValueError("Chain not initialized. Call create_chain first.")
        return self.chain.run(**inputs)