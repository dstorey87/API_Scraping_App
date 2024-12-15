# ./tests/langchain_tests/test_conversation_chain.py

import pytest
from langchain_service.chains.conversation_chain import ConversationChainService
from langchain_service.models.base_model import LocalLLMService
from config.model_config import MODEL_CONFIGS

@pytest.fixture
def llm_service():
    """Create LLM service instance."""
    return LocalLLMService(MODEL_CONFIGS["text"])

@pytest.fixture
def conversation_service(llm_service):
    """Create conversation chain service instance."""
    return ConversationChainService(llm_service)

def test_conversation_chain_creation(conversation_service):
    """Test conversation chain initialization."""
    assert conversation_service.chain is not None
    assert conversation_service.memory is not None

def test_conversation_processing(conversation_service):
    """Test processing input through conversation chain."""
    response = conversation_service.process_input("Hello, how are you?")
    assert response is not None
    assert isinstance(response, str)