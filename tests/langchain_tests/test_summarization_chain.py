# ./tests/langchain_tests/test_summarization_chain.py

import pytest
from langchain_service.chains.summarization_chain import SummarizationChain
from langchain_service.models.base_model import LocalLLMService
from config.model_config import MODEL_CONFIGS

@pytest.fixture
def llm_service():
    """Create LLM service instance for testing."""
    return LocalLLMService(MODEL_CONFIGS["text"])

@pytest.fixture
def summarization_chain(llm_service):
    """Create summarization chain instance."""
    return SummarizationChain(llm_service)

def test_summarization_chain_creation(summarization_chain):
    """Test chain initialization."""
    assert summarization_chain.chain is not None

def test_summarization(summarization_chain):
    """Test text summarization."""
    test_text = "This is a long text that needs to be summarized. " * 10
    summary = summarization_chain.summarize(test_text)
    assert summary is not None
    assert len(summary) <= 200