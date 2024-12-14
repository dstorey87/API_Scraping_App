# setup_project.ps1

# Create main project directory and subdirectories
$directories = @(
    "o1_langchain_integration",
    "o1_langchain_integration/config",
    "o1_langchain_integration/models", 
    "o1_langchain_integration/utils",
    "o1_langchain_integration/chains",
    "o1_langchain_integration/logs"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Force -Path $dir
}

# Create and populate requirements.txt
@"
langchain>=0.1.0
python-dotenv>=0.19.0
pydantic>=2.0.0
loguru>=0.7.0
typing-extensions>=4.5.0
"@ | Set-Content "o1_langchain_integration/requirements.txt"

# Create and populate config/model_config.py
@"
from pydantic import BaseSettings
from typing import Optional

class O1ModelConfig(BaseSettings):
    model_path: str
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.95
    timeout: int = 300
    
    class Config:
        env_file = ".env"

model_config = O1ModelConfig()
"@ | Set-Content "o1_langchain_integration/config/model_config.py"

# Create and populate models/o1_loader.py
@"
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
from ..config.model_config import model_config

class O1ModelLoader(LLM):
    model_path: str
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_path = model_config.model_path
        
    @property
    def _llm_type(self) -> str:
        return "o1_model"
        
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
    ) -> str:
        # Implementation for model inference
        # This will be implemented when Docker setup is available
        pass
"@ | Set-Content "o1_langchain_integration/models/o1_loader.py"

# Create and populate utils/logging_config.py
@"
from loguru import logger
import sys

def setup_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    logger.add(
        "logs/o1_langchain.log",
        rotation="500 MB",
        retention="10 days",
        level="DEBUG"
    )
"@ | Set-Content "o1_langchain_integration/utils/logging_config.py"

# Create and populate chains/base_chain.py
@"
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from ..models.o1_loader import O1ModelLoader

def create_base_chain():
    llm = O1ModelLoader()
    prompt = PromptTemplate(
        input_variables=["query"],
        template="Please process the following query: {query}"
    )
    return LLMChain(llm=llm, prompt=prompt)
"@ | Set-Content "o1_langchain_integration/chains/base_chain.py"

# Create and populate utils/data_handler.py
@"
from pathlib import Path
from typing import Union, List
import json

class DataHandler:
    @staticmethod
    def read_file(file_path: Union[str, Path]) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return path.read_text(encoding='utf-8')
    
    @staticmethod
    def write_file(file_path: Union[str, Path], content: str) -> None:
        path = Path(file_path)
        path.write_text(content, encoding='utf-8')
    
    @staticmethod
    def load_json(file_path: Union[str, Path]) -> dict:
        return json.loads(DataHandler.read_file(file_path))
"@ | Set-Content "o1_langchain_integration/utils/data_handler.py"

# Create __init__.py files for package structure
$null | Set-Content "o1_langchain_integration/__init__.py"
$null | Set-Content "o1_langchain_integration/config/__init__.py"
$null | Set-Content "o1_langchain_integration/models/__init__.py"
$null | Set-Content "o1_langchain_integration/utils/__init__.py"
$null | Set-Content "o1_langchain_integration/chains/__init__.py"

# Create .env file template
@"
MODEL_PATH=path/to/your/o1/model
"@ | Set-Content "o1_langchain_integration/.env"

Write-Host "Project structure created successfully!"