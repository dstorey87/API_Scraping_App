# ./langchain_service/chains/conversation_chain.py
# Purpose: Implements conversational AI functionality
# Handles: Chat history, context management, response generation
# Dependencies: base_model.py, LangChain's ConversationChain

from typing import Dict, Any, Optional
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from ..models.base_model import LocalLLMService
import logging

logger = logging.getLogger(__name__)

class ConversationChainService:
    """Service for managing conversation chains with local LLMs."""

    def __init__(self, llm_service: LocalLLMService):
        self.llm = llm_service
        self.memory = ConversationBufferMemory()
        self.chain = self._create_chain()

    def _create_chain(self) -> ConversationChain:
        """Create a conversation chain with memory."""
        return ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )

    def process_input(self, user_input: str) -> Optional[str]:
        """Process user input through the conversation chain."""
        try:
            response = self.chain.predict(input=user_input)
            return response
        except Exception as e:
            logger.error("Error processing conversation input: %s", str(e))
            return None